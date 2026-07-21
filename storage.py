# -*- coding: utf-8 -*-
"""
storage.py — Persistence + the gamification engine for MIND ARENA.

Two interchangeable storage backends, chosen automatically at import time:

  * **Postgres** (used in the cloud) — if a connection string is configured via
    the DATABASE_URL environment variable or a Streamlit secret, everything is
    stored in a single `mind_arena_kv (k, v jsonb)` table. This survives
    restarts/redeploys, which the ephemeral cloud filesystem does not.
  * **Local JSON files** (used on your machine) — if no DB is configured, each
    profile is one JSON file under mind_arena_data/profiles/ plus a small
    registry file, exactly as before. Zero setup for local play.

Either way the profile data is the same shape, so switching backends is
transparent to the rest of the app. This module owns:

  * profile management (create / list / load / save / delete)
  * streak logic (breaks if you miss a day, real calendar based)
  * XP / level curve and themed rank names
  * badge / achievement unlocking
  * the per-day history that powers the calendar heat-map
"""

import hashlib
import json
import os
import random
import re
import secrets
import threading
from datetime import date, datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mind_arena_data")
PROFILES_DIR = os.path.join(DATA_DIR, "profiles")
REGISTRY_PATH = os.path.join(PROFILES_DIR, "_registry.json")
LEGACY_SAVE_PATH = os.path.join(DATA_DIR, "progress.json")  # pre-profiles single save


# ---------------------------------------------------------------------------
# Backend selection: Postgres (cloud) or local JSON files.
# ---------------------------------------------------------------------------

def _get_db_url():
    """Find a Postgres URL from the environment or Streamlit secrets, if any."""
    url = os.environ.get("DATABASE_URL")
    if url:
        return url.strip()
    try:  # only available when running under Streamlit
        import streamlit as st
        if "DATABASE_URL" in st.secrets:
            return str(st.secrets["DATABASE_URL"]).strip()
        pg = st.secrets.get("postgres")
        if isinstance(pg, dict) and pg.get("url"):
            return str(pg["url"]).strip()
    except Exception:
        pass
    return None


_DB_URL = _get_db_url()
_USE_PG = bool(_DB_URL)
_PG_LOCK = threading.Lock()
_pg_conn = None


def _pg():
    """Return a live psycopg2 connection, (re)connecting and ensuring schema."""
    global _pg_conn
    import psycopg2
    if _pg_conn is None or getattr(_pg_conn, "closed", 1):
        _pg_conn = psycopg2.connect(_DB_URL)
        _pg_conn.autocommit = True
        with _pg_conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS mind_arena_kv "
                "(k text PRIMARY KEY, v jsonb NOT NULL)"
            )
    return _pg_conn


def _kv_get(key):
    with _PG_LOCK:
        with _pg().cursor() as cur:
            cur.execute("SELECT v FROM mind_arena_kv WHERE k = %s", (key,))
            row = cur.fetchone()
    return row[0] if row else None  # psycopg2 decodes jsonb -> Python object


def _kv_set(key, value):
    from psycopg2.extras import Json
    with _PG_LOCK:
        with _pg().cursor() as cur:
            cur.execute(
                "INSERT INTO mind_arena_kv (k, v) VALUES (%s, %s) "
                "ON CONFLICT (k) DO UPDATE SET v = EXCLUDED.v",
                (key, Json(value)),
            )


def _kv_del(key):
    with _PG_LOCK:
        with _pg().cursor() as cur:
            cur.execute("DELETE FROM mind_arena_kv WHERE k = %s", (key,))


def _profile_key(slug: str) -> str:
    return f"profile:{slug}"


# --- backend-agnostic raw read/write of the registry and profile blobs -------

def _read_registry_raw():
    """Return the stored registry dict, or None if it doesn't exist yet."""
    if _USE_PG:
        return _kv_get("registry")
    if not os.path.exists(REGISTRY_PATH):
        return None
    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _write_registry_raw(reg: dict) -> None:
    if _USE_PG:
        _kv_set("registry", reg)
    else:
        _atomic_write(REGISTRY_PATH, reg)


def _read_profile_raw(slug: str):
    """Return the stored state dict for `slug`, or None. Quarantines corruption."""
    if _USE_PG:
        return _kv_get(_profile_key(slug))
    path = _profile_path(slug)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        try:
            os.rename(path, path + ".corrupt")
        except OSError:
            pass
        return None


def _write_profile_raw(slug: str, state: dict) -> None:
    if _USE_PG:
        _kv_set(_profile_key(slug), state)
    else:
        _atomic_write(_profile_path(slug), state)


def _profile_exists(slug: str) -> bool:
    if _USE_PG:
        return _kv_get(_profile_key(slug)) is not None
    return os.path.exists(_profile_path(slug))


def _delete_profile_raw(slug: str) -> None:
    if _USE_PG:
        _kv_del(_profile_key(slug))
    else:
        try:
            os.remove(_profile_path(slug))
        except OSError:
            pass

# ---------------------------------------------------------------------------
# Level curve & rank titles
# ---------------------------------------------------------------------------

RANKS = [
    (0,    "Rookie Rambler"),
    (150,  "Warm-Up Wordsmith"),
    (400,  "Quick Thinker"),
    (750,  "Sharp Speaker"),
    (1200, "Silver Tongue"),
    (1800, "Mind Blade"),
    (2600, "Rhetoric Ronin"),
    (3600, "Master Orator"),
    (5000, "Cerebral Champion"),
    (7000, "Grandmaster of Mind & Voice"),
]

# Badge catalog: id -> (emoji, title, description)
BADGES = {
    "first_run":      ("🌱", "First Steps", "Complete your very first full run."),
    "streak_3":       ("🔥", "On Fire", "Reach a 3-day streak."),
    "streak_7":       ("🗓️", "Week Warrior", "Reach a 7-day streak."),
    "streak_30":      ("👑", "Unbreakable", "Reach a 30-day streak."),
    "puzzle_master":  ("🧩", "Puzzle Master", "Solve 5+ brain teasers in one run."),
    "silver_tongue":  ("🎙️", "Golden Voice", "Score 85+ on a speaking round."),
    "iron_will":      ("🛡️", "Iron Will", "Finish all three stages in a single run."),
    "night_owl":      ("🦉", "Night Owl", "Train after 10 PM."),
    "early_bird":     ("🐦", "Early Bird", "Train before 7 AM."),
    "centurion":      ("💯", "Centurion", "Reach a total of 5000 XP."),
    "comeback":       ("💫", "Comeback Kid", "Return and train after breaking a streak."),
    "marathoner":     ("🏅", "Marathoner", "Complete 25 total runs."),
}


def _today() -> date:
    return date.today()


def _default_state(profile: str = None, slug: str = None) -> dict:
    return {
        "profile": profile,           # display name
        "slug": slug,                 # filename-safe id
        "xp": 0,
        "streak": 0,
        "longest_streak": 0,
        "last_played": None,          # ISO date string
        "total_runs": 0,
        "best_score": 0,
        "badges": [],                 # list of badge ids unlocked
        "history": {},                # "YYYY-MM-DD": {score, brain, speech, challenge}
        "created": datetime.now().isoformat(timespec="seconds"),
        # "Shuffle-bag" decks so a player sees EVERY question/prompt once before
        # any repeats (and never the same one two runs running). Each holds the
        # not-yet-dealt indices; *_size records the pool size it was built for so
        # the bag rebuilds automatically when the content bank grows.
        "teaser_deck": [],
        "teaser_deck_size": None,
        "prompt_deck": [],
        "prompt_deck_size": None,
    }


# ---------------------------------------------------------------------------
# Profile registry & files
# ---------------------------------------------------------------------------

def _slugify(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_-]+", "_", (name or "").strip()).strip("_").lower()
    return (s or "player")[:40]


def _atomic_write(path: str, data: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


def _profile_path(slug: str) -> str:
    return os.path.join(PROFILES_DIR, f"{slug}.json")


def _load_registry() -> dict:
    reg = _read_registry_raw()
    if reg is None:
        reg = {"profiles": [], "last_active": None}
        # one-time migration of an old single-save file (local file backend only)
        if not _USE_PG and os.path.exists(LEGACY_SAVE_PATH):
            try:
                entry = create_profile("Player 1")
                with open(LEGACY_SAVE_PATH, "r", encoding="utf-8") as f:
                    old = json.load(f)
                old.update({"profile": entry["name"], "slug": entry["slug"]})
                for k, v in _default_state().items():
                    old.setdefault(k, v)
                _write_profile_raw(entry["slug"], old)
                os.rename(LEGACY_SAVE_PATH, LEGACY_SAVE_PATH + ".migrated")
                return _load_registry()
            except (OSError, json.JSONDecodeError):
                pass
        _write_registry_raw(reg)
        return reg
    reg.setdefault("profiles", [])
    reg.setdefault("last_active", None)
    return reg


def backend_name() -> str:
    """Human-readable name of the active storage backend (for diagnostics)."""
    return "Postgres (cloud)" if _USE_PG else "Local JSON files"


def list_profiles() -> list:
    """Return the registry's profile entries: [{name, slug, created}, ...]."""
    return _load_registry()["profiles"]


def last_active_profile():
    return _load_registry().get("last_active")


def create_profile(name: str, pin: str = None) -> dict:
    reg = _load_registry()
    name = (name or "").strip()[:30] or "Player"
    existing = {p["slug"] for p in reg["profiles"]}
    base = _slugify(name)
    slug = base
    i = 2
    while slug in existing:
        slug = f"{base}-{i}"
        i += 1
    entry = {"name": name, "slug": slug, "created": datetime.now().isoformat(timespec="seconds")}
    if pin:
        salt = secrets.token_hex(8)
        entry["pin_salt"] = salt
        entry["pin_hash"] = _hash_pin(pin, salt)
    reg["profiles"].append(entry)
    reg["last_active"] = name
    _write_registry_raw(reg)
    _write_profile_raw(slug, _default_state(name, slug))
    return entry


# ---------------------------------------------------------------------------
# Optional per-profile PIN (light protection for a shared computer — the save
# files are local JSON, so this deters casual snooping, not a determined user).
# We store only a salted SHA-256 hash, never the PIN itself.
# ---------------------------------------------------------------------------

def _hash_pin(pin: str, salt: str) -> str:
    return hashlib.sha256((salt + str(pin)).encode("utf-8")).hexdigest()


def get_entry(name_or_slug: str):
    return _find_entry(_load_registry(), name_or_slug)


def has_pin(entry: dict) -> bool:
    return bool(entry and entry.get("pin_hash"))


def verify_pin(entry: dict, pin: str) -> bool:
    if not has_pin(entry):
        return True
    return _hash_pin(pin or "", entry.get("pin_salt", "")) == entry["pin_hash"]


def set_pin(slug: str, pin: str) -> None:
    """Set/change a PIN (truthy pin) or remove it (falsy pin)."""
    reg = _load_registry()
    for p in reg["profiles"]:
        if p["slug"] == slug:
            if pin:
                salt = secrets.token_hex(8)
                p["pin_salt"] = salt
                p["pin_hash"] = _hash_pin(pin, salt)
            else:
                p.pop("pin_salt", None)
                p.pop("pin_hash", None)
            break
    _write_registry_raw(reg)


def delete_profile(slug: str) -> None:
    reg = _load_registry()
    reg["profiles"] = [p for p in reg["profiles"] if p["slug"] != slug]
    if reg.get("last_active") and _slugify(reg["last_active"]) == slug:
        reg["last_active"] = None
    _write_registry_raw(reg)
    _delete_profile_raw(slug)


def _find_entry(reg, name):
    for p in reg["profiles"]:
        if p["name"] == name or p["slug"] == _slugify(name):
            return p
    return None


def load_state(name: str) -> dict:
    """Load (or create) the profile named `name` and mark it as last-active."""
    reg = _load_registry()
    entry = _find_entry(reg, name)
    if entry is None:
        entry = create_profile(name)
        reg = _load_registry()

    slug = entry["slug"]
    state = _read_profile_raw(slug)
    if state is None:
        state = _default_state(entry["name"], slug)
        _write_profile_raw(slug, state)

    for k, v in _default_state(entry["name"], slug).items():
        state.setdefault(k, v)
    state["profile"] = entry["name"]
    state["slug"] = slug

    reg["last_active"] = entry["name"]
    _write_registry_raw(reg)
    return state


def save_state(state: dict) -> None:
    slug = state.get("slug") or _slugify(state.get("profile") or "player")
    state["slug"] = slug
    _write_profile_raw(slug, state)


def draw_from_deck(state: dict, deck_key: str, total: int, k: int) -> list:
    """Deal `k` unique indices in [0, total) from a persistent per-profile
    "shuffle-bag" stored in state[deck_key].

    Guarantees:
      * a player sees every item once before ANY repeat (the bag is only
        reshuffled once it is empty);
      * no repeats within a single draw;
      * when the bag reshuffles mid-draw, the just-dealt items are pushed to the
        back, so you never get the same item twice across the boundary either;
      * if the content pool size changes (the bank grew/shrank), the bag rebuilds
        automatically and stale/out-of-range indices are dropped.

    The caller is responsible for persisting the mutated `state` (save_state).
    """
    if total <= 0:
        return []
    k = max(0, min(k, total))
    size_key = deck_key + "_size"

    deck = state.get(deck_key)
    if not isinstance(deck, list) or state.get(size_key) != total:
        deck = []                      # pool changed (or first use) -> rebuild
        state[size_key] = total
    else:
        deck = [i for i in deck if isinstance(i, int) and 0 <= i < total]

    drawn = []
    while len(drawn) < k:
        if not deck:
            fresh = list(range(total))
            random.shuffle(fresh)
            if drawn:                  # avoid an immediate repeat across reshuffle
                just = set(drawn)
                deck = [i for i in fresh if i not in just] + [i for i in fresh if i in just]
            else:
                deck = fresh
        drawn.append(deck.pop(0))

    state[deck_key] = deck
    return drawn


def profile_summary(entry: dict) -> dict:
    """Light read of a profile for the picker cards (never raises)."""
    s = _read_profile_raw(entry["slug"]) or _default_state(entry["name"], entry["slug"])
    status = streak_status(s)
    return {
        "name": entry["name"],
        "slug": entry["slug"],
        "xp": s.get("xp", 0),
        "streak": status["current"],
        "rank": rank_name(s.get("xp", 0)),
        "runs": s.get("total_runs", 0),
        "locked": has_pin(entry),
    }


# ---------------------------------------------------------------------------
# Streak logic
# ---------------------------------------------------------------------------

def streak_status(state: dict) -> dict:
    """Compute the live streak situation without mutating saved state."""
    last = state.get("last_played")
    today = _today()
    if last is None:
        return {"current": 0, "played_today": False, "at_risk": False, "broken": False}

    last_date = date.fromisoformat(last)
    delta = (today - last_date).days

    if delta == 0:
        return {"current": state["streak"], "played_today": True, "at_risk": False, "broken": False}
    if delta == 1:
        # played yesterday: streak alive but today not done yet -> at risk
        return {"current": state["streak"], "played_today": False, "at_risk": True, "broken": False}
    # missed one or more full days
    return {"current": 0, "played_today": False, "at_risk": False, "broken": state["streak"] > 0}


# ---------------------------------------------------------------------------
# XP / level helpers
# ---------------------------------------------------------------------------

def level_for_xp(xp: int) -> int:
    lvl = 1
    for i, (threshold, _) in enumerate(RANKS):
        if xp >= threshold:
            lvl = i + 1
    return lvl


def rank_name(xp: int) -> str:
    name = RANKS[0][1]
    for threshold, title in RANKS:
        if xp >= threshold:
            name = title
    return name


def level_progress(xp: int):
    """Return (current_level, xp_into_level, xp_needed_for_next, pct 0..1)."""
    lvl = level_for_xp(xp)
    cur_threshold = RANKS[lvl - 1][0]
    if lvl >= len(RANKS):
        return lvl, xp - cur_threshold, None, 1.0
    next_threshold = RANKS[lvl][0]
    span = next_threshold - cur_threshold
    into = xp - cur_threshold
    return lvl, into, next_threshold - xp, max(0.0, min(1.0, into / span))


# ---------------------------------------------------------------------------
# Recording a completed run
# ---------------------------------------------------------------------------

def _check_badges(state: dict, run: dict, was_broken_before: bool) -> list:
    newly = []
    have = set(state["badges"])
    hour = datetime.now().hour

    def unlock(bid):
        if bid not in have:
            have.add(bid)
            newly.append(bid)

    if state["total_runs"] >= 1:
        unlock("first_run")
    if state["streak"] >= 3:
        unlock("streak_3")
    if state["streak"] >= 7:
        unlock("streak_7")
    if state["streak"] >= 30:
        unlock("streak_30")
    if run.get("brain_solved", 0) >= 5:
        unlock("puzzle_master")
    if max(run.get("speech_score", 0), run.get("challenge_score", 0)) >= 85:
        unlock("silver_tongue")
    if run.get("all_stages", False):
        unlock("iron_will")
    if hour >= 22:
        unlock("night_owl")
    if hour < 7:
        unlock("early_bird")
    if state["xp"] >= 5000:
        unlock("centurion")
    if state["total_runs"] >= 25:
        unlock("marathoner")
    if was_broken_before:
        unlock("comeback")

    state["badges"] = sorted(have)
    return newly


def record_run(state: dict, run: dict) -> dict:
    """
    Commit a finished run to persistent state and return a summary of what
    changed (xp gained, level-ups, streak, new badges) for the results screen.

    `run` expects keys: brain_score, brain_solved, speech_score, challenge_score,
    all_stages (bool).
    """
    today = _today()
    today_iso = today.isoformat()

    status = streak_status(state)
    was_broken_before = status["broken"]

    # --- streak update ---
    last = state.get("last_played")
    if last is None:
        state["streak"] = 1
    else:
        last_date = date.fromisoformat(last)
        delta = (today - last_date).days
        if delta == 0:
            # already played today — keep streak, this is a repeat run
            state["streak"] = max(state["streak"], 1)
        elif delta == 1:
            state["streak"] += 1
        else:
            state["streak"] = 1  # missed day(s): reset (this run restarts it)

    state["longest_streak"] = max(state["longest_streak"], state["streak"])

    # --- score & xp ---
    base = int(run.get("brain_score", 0) + run.get("speech_score", 0) + run.get("challenge_score", 0))
    streak_multiplier = 1.0 + min(state["streak"], 20) * 0.05  # up to +100%
    all_stage_bonus = 50 if run.get("all_stages", False) else 0
    xp_gain = int((base + all_stage_bonus) * streak_multiplier)

    level_before = level_for_xp(state["xp"])
    state["xp"] += xp_gain
    level_after = level_for_xp(state["xp"])

    # --- bookkeeping ---
    state["total_runs"] += 1
    state["best_score"] = max(state["best_score"], base)
    state["last_played"] = today_iso
    state["history"][today_iso] = {
        "score": base,
        "brain": int(run.get("brain_score", 0)),
        "speech": int(run.get("speech_score", 0)),
        "challenge": int(run.get("challenge_score", 0)),
        "xp": xp_gain,
    }

    new_badges = _check_badges(state, run, was_broken_before)
    save_state(state)

    return {
        "xp_gain": xp_gain,
        "base_score": base,
        "streak": state["streak"],
        "streak_multiplier": streak_multiplier,
        "level_before": level_before,
        "level_after": level_after,
        "leveled_up": level_after > level_before,
        "rank": rank_name(state["xp"]),
        "new_badges": new_badges,
    }


# ---------------------------------------------------------------------------
# Calendar data for the heat-map
# ---------------------------------------------------------------------------

def month_grid(state: dict, year: int, month: int):
    """
    Return a list of weeks; each week is a list of 7 cells.
    Cell = None (padding) or dict {day, played, score, is_today}.
    Week starts Monday.
    """
    first = date(year, month, 1)
    # days in month
    if month == 12:
        nxt = date(year + 1, 1, 1)
    else:
        nxt = date(year, month + 1, 1)
    days_in_month = (nxt - first).days

    start_weekday = first.weekday()  # Monday=0
    history = state.get("history", {})
    today = _today()

    cells = [None] * start_weekday
    for d in range(1, days_in_month + 1):
        iso = date(year, month, d).isoformat()
        rec = history.get(iso)
        cells.append({
            "day": d,
            "played": rec is not None,
            "score": rec["score"] if rec else 0,
            "is_today": (year == today.year and month == today.month and d == today.day),
        })
    while len(cells) % 7 != 0:
        cells.append(None)

    return [cells[i:i + 7] for i in range(0, len(cells), 7)]
