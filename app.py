# -*- coding: utf-8 -*-
"""
🧠⚡ MIND ARENA — a 6-minute daily brain + speech sharpening game.

Three non-stop stages, everything compulsory:
    STAGE 1  ·  Brain Teaser Blitz        (2:00)  — rapid riddles/logic/patterns
    STAGE 2  ·  The Speaking Forge         (2:30)  — 2-3 min non-stop mini-speech
    STAGE 3  ·  Progressive Boss Challenge (2:30)  — escalating speed challenges

Built to run locally:  streamlit run app.py
Only dependency beyond Streamlit is numpy (for offline speech analysis).
"""

import time
import random
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

import content
import storage
import analysis

# ---------------------------------------------------------------------------
# Page config + theme
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Mind Arena", page_icon="🧠", layout="wide",
                   initial_sidebar_state="collapsed")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Poppins:wght@400;500;600;700&display=swap');

:root { --neon:#00e5ff; --neon2:#ff2bd6; --gold:#ffd24a; --green:#38f5a8; --bg:#0b0f1a; }

/* animated deep-space background */
.stApp {
  background:
    radial-gradient(1200px 600px at 15% -10%, rgba(0,229,255,.14), transparent 55%),
    radial-gradient(1000px 500px at 90% 0%, rgba(255,43,214,.12), transparent 55%),
    radial-gradient(900px 700px at 50% 120%, rgba(56,245,168,.10), transparent 55%),
    linear-gradient(160deg, #0a0e18 0%, #0b0f1a 45%, #0a0d16 100%);
  background-attachment: fixed;
}
/* faint starfield overlay */
.stApp::before {
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    radial-gradient(1px 1px at 20% 30%, rgba(255,255,255,.35), transparent),
    radial-gradient(1px 1px at 70% 60%, rgba(255,255,255,.25), transparent),
    radial-gradient(1px 1px at 40% 80%, rgba(255,255,255,.30), transparent),
    radial-gradient(1px 1px at 85% 20%, rgba(255,255,255,.20), transparent),
    radial-gradient(1px 1px at 55% 15%, rgba(255,255,255,.22), transparent);
  background-size: 100% 100%;
  opacity:.5; animation: twinkle 6s ease-in-out infinite alternate;
}
@keyframes twinkle { from{opacity:.30} to{opacity:.7} }

.block-container { padding-top: 1.0rem; max-width: 1120px; position:relative; z-index:1; }
html, body, [class*="css"] { font-family:'Poppins', sans-serif; }
h1,h2,h3,h4 { font-family:'Orbitron', sans-serif; letter-spacing:1px; }

/* ---- hero title ---- */
.arena-title {
  font-family:'Orbitron', sans-serif;
  font-size: 3.1rem; font-weight: 900; text-align:center; margin-bottom:2px;
  background: linear-gradient(90deg,#00e5ff,#7a5cff,#ff2bd6,#ffd24a,#00e5ff);
  background-size: 300% auto;
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  animation: hue 8s linear infinite, glowpulse 3s ease-in-out infinite;
  filter: drop-shadow(0 0 18px rgba(0,229,255,.35));
}
@keyframes hue { to { background-position: 300% center; } }
@keyframes glowpulse {
  0%,100%{ filter: drop-shadow(0 0 14px rgba(0,229,255,.30)); }
  50%{ filter: drop-shadow(0 0 30px rgba(255,43,214,.45)); }
}
.subtitle { text-align:center; color:#9db3d4; margin-top:-4px; font-size:1.02rem; font-weight:400; }

/* ---- glass cards ---- */
.card {
  background: linear-gradient(145deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
  border:1px solid rgba(0,229,255,.22); border-radius:18px; padding:18px 22px;
  box-shadow: 0 8px 30px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.06);
  backdrop-filter: blur(6px); transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.card:hover {
  transform: translateY(-4px);
  border-color: rgba(0,229,255,.55);
  box-shadow: 0 14px 40px rgba(0,229,255,.18), inset 0 1px 0 rgba(255,255,255,.08);
}
.stat-num { font-family:'Poppins',sans-serif; font-size:2.2rem; font-weight:700;
  color:#eafcff; line-height:1; text-shadow:0 0 16px rgba(0,229,255,.5); }
.stat-lbl { font-size:.72rem; color:#8aa0c0; text-transform:uppercase; letter-spacing:1.5px; margin-top:4px; }
.streak-fire { font-size:2.6rem; animation: flicker 2.5s ease-in-out infinite; }
@keyframes flicker { 0%,100%{transform:scale(1);filter:drop-shadow(0 0 8px #ff7a1a)} 50%{transform:scale(1.12);filter:drop-shadow(0 0 18px #ff4d1a)} }

/* ---- prompt / teaser box ---- */
.prompt-box {
  position:relative;
  background: linear-gradient(135deg, rgba(0,229,255,.10), rgba(255,43,214,.10));
  border:1px solid rgba(255,210,74,.30); border-radius:22px; padding:28px; text-align:center;
  box-shadow: 0 10px 40px rgba(0,0,0,.35);
  animation: breathe 5s ease-in-out infinite;
}
@keyframes breathe {
  0%,100%{ box-shadow:0 10px 40px rgba(0,0,0,.35), 0 0 0 1px rgba(0,229,255,.10); }
  50%{ box-shadow:0 10px 50px rgba(0,0,0,.4), 0 0 26px rgba(0,229,255,.22); }
}
.prop-emoji { font-size:5.2rem; line-height:1; filter: drop-shadow(0 0 22px rgba(0,229,255,.6));
  animation: floaty 4s ease-in-out infinite; }
@keyframes floaty { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
.teaser-q { font-family:'Poppins',sans-serif; font-size:1.55rem; font-weight:600; color:#f2f9ff; line-height:1.55; }

/* ---- badges ---- */
.badge-chip {
  display:inline-block; background:linear-gradient(145deg, rgba(255,210,74,.16), rgba(255,210,74,.05));
  border:1px solid rgba(255,210,74,.45); border-radius:22px; padding:7px 15px; margin:5px;
  font-size:.92rem; font-weight:500; transition: transform .15s ease;
}
.badge-chip:hover { transform: translateY(-2px) scale(1.03); }
.badge-locked { opacity:.30; filter:grayscale(.6); }

/* ---- calendar ---- */
.cal-cell { display:inline-block; width:32px; height:32px; margin:3px; border-radius:9px;
  text-align:center; line-height:32px; font-size:.74rem; color:#cfe;
  border:1px solid rgba(255,255,255,.06); transition: transform .12s ease; }
.cal-cell:hover { transform: scale(1.15); }

/* ---- buttons ---- */
.stButton>button {
  border-radius:14px; font-weight:600; font-family:'Poppins',sans-serif;
  border:1px solid rgba(0,229,255,.35); background: rgba(255,255,255,.04);
  transition: all .18s ease;
}
.stButton>button:hover {
  border-color: rgba(0,229,255,.8); box-shadow:0 0 18px rgba(0,229,255,.35);
  transform: translateY(-2px);
}
.stButton>button[kind="primary"] {
  background: linear-gradient(90deg,#00e5ff,#4aa8ff,#ff2bd6);
  background-size:200% auto; color:#04121a; border:none; font-weight:700;
  box-shadow:0 6px 24px rgba(0,229,255,.35);
}
.stButton>button[kind="primary"]:hover { background-position:right center; transform: translateY(-2px) scale(1.01); box-shadow:0 8px 30px rgba(255,43,214,.4); }
.big-btn>button { font-family:'Orbitron',sans-serif; font-size:1.25rem; padding:.85rem 0; letter-spacing:1px;
  animation: ctapulse 2.4s ease-in-out infinite; }
@keyframes ctapulse { 0%,100%{box-shadow:0 6px 24px rgba(0,229,255,.30)} 50%{box-shadow:0 8px 34px rgba(255,43,214,.5)} }

/* ---- misc ---- */
.coach-tip { background:linear-gradient(145deg, rgba(255,255,255,.05), rgba(255,255,255,.01));
  border-left:3px solid var(--neon); padding:11px 15px; border-radius:10px; margin:9px 0; }
.stTabs [data-baseweb="tab"] { font-family:'Poppins',sans-serif; font-weight:600; }
[data-testid="stMetricValue"] { font-family:'Poppins',sans-serif; font-weight:700; color:#eafcff; }
hr { border-color: rgba(255,255,255,.08); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Stage durations (seconds)
DUR_BRAIN = 120
DUR_SPEAK = 150
DUR_BOSS = 150


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

def init_session():
    ss = st.session_state
    if "stage" not in ss:
        ss.stage = "profiles"     # start at the profile picker
    if "run" not in ss:
        ss.run = {}


def go_to(stage):
    st.session_state.stage = stage
    st.session_state.timer_start = time.time()
    st.rerun()


def select_profile(name):
    st.session_state.state = storage.load_state(name)
    st.session_state.run = {}
    go_to("home")


def switch_profile():
    st.session_state.pop("state", None)
    st.session_state.run = {}
    go_to("profiles")


def start_new_run():
    state = st.session_state.state
    lvl = storage.level_for_xp(state["xp"])
    teasers = random.sample(content.BRAIN_TEASERS, k=min(14, len(content.BRAIN_TEASERS)))
    prop, prompt = random.choice(content.SPEECH_PROMPTS)
    boss = content.pick_boss_challenge(lvl)
    st.session_state.run = {
        "teasers": teasers,
        "t_idx": 0,
        "revealed": False,
        "solved": 0,
        "attempted": 0,
        "prop": prop,
        "prompt": prompt,
        "boss": boss,
        "speech_analysis": None,
        "speech_selfrate": 3,
        "challenge_analysis": None,
        "challenge_selfrate": 3,
    }
    go_to("s1_brain")


# ---------------------------------------------------------------------------
# Reusable widgets
# ---------------------------------------------------------------------------

def live_clock():
    components.html("""
    <div id="clk" style="font-family:Trebuchet MS,sans-serif;text-align:center;
        color:#00e5ff;font-size:1.5rem;font-weight:800;
        text-shadow:0 0 14px rgba(0,229,255,.5);"></div>
    <div id="dte" style="font-family:Trebuchet MS,sans-serif;text-align:center;
        color:#8aa0c0;font-size:.8rem;letter-spacing:1px;"></div>
    <script>
      function tick(){
        const n=new Date();
        document.getElementById('clk').textContent=n.toLocaleTimeString();
        document.getElementById('dte').textContent=n.toLocaleDateString(undefined,
          {weekday:'long',year:'numeric',month:'long',day:'numeric'});
      }
      tick(); setInterval(tick,1000);
    </script>
    """, height=70)


def timer_ring(duration, auto_advance_to=None):
    """A 1-second-updating countdown ring. If auto_advance_to is set, the stage
    changes automatically when the clock hits zero."""

    @st.fragment(run_every=1)
    def _ring():
        start = st.session_state.get("timer_start", time.time())
        remaining = max(0.0, duration - (time.time() - start))
        pct = remaining / duration if duration else 0
        mm, sscnd = divmod(int(remaining), 60)
        if pct > 0.5:
            col = "#38f5a8"
        elif pct > 0.2:
            col = "#ffd24a"
        else:
            col = "#ff5d6c"
        deg = int(pct * 360)
        components.html(f"""
        <div style="display:flex;justify-content:center;">
          <div style="width:130px;height:130px;border-radius:50%;
             background:conic-gradient({col} {deg}deg, rgba(255,255,255,.08) {deg}deg);
             display:flex;align-items:center;justify-content:center;">
            <div style="width:104px;height:104px;border-radius:50%;background:#0b0f1a;
               display:flex;flex-direction:column;align-items:center;justify-content:center;
               font-family:Trebuchet MS,sans-serif;">
              <div style="font-size:1.9rem;font-weight:800;color:{col};">{mm:01d}:{sscnd:02d}</div>
              <div style="font-size:.6rem;color:#8aa0c0;letter-spacing:1px;">REMAINING</div>
            </div>
          </div>
        </div>
        """, height=145)
        if remaining <= 0:
            if auto_advance_to:
                go_to(auto_advance_to)
            else:
                st.markdown("<p style='text-align:center;color:#ff5d6c;font-weight:700;'>"
                            "⏰ Time's up — land your final sentence and continue!</p>",
                            unsafe_allow_html=True)

    _ring()


def stage_header(num, title, subtitle):
    st.markdown(f"<h2 style='text-align:center;'>STAGE {num} · {title}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>{subtitle}</p>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# PROFILE PICKER
# ---------------------------------------------------------------------------

def render_profiles():
    st.markdown("<div class='arena-title'>🧠⚡ MIND ARENA ⚡🧠</div>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Choose your fighter — or create a new one. Every profile keeps its own streak, XP & badges.</p>",
                unsafe_allow_html=True)
    live_clock()
    st.write("")

    # ---- PIN unlock gate (shown when a locked profile is being opened) ----
    unlock_slug = st.session_state.get("unlock_target")
    if unlock_slug:
        entry = storage.get_entry(unlock_slug)
        if entry and storage.has_pin(entry):
            st.markdown(f"#### 🔒 Enter PIN for **{entry['name']}**")
            with st.form("unlock_form", clear_on_submit=True):
                pin = st.text_input("PIN", type="password", label_visibility="collapsed",
                                    placeholder="Enter your PIN")
                u1, u2 = st.columns(2)
                ok = u1.form_submit_button("🔓 Unlock & Play", use_container_width=True, type="primary")
                cancel = u2.form_submit_button("Cancel", use_container_width=True)
            if cancel:
                st.session_state.pop("unlock_target", None)
                st.rerun()
            if ok:
                if storage.verify_pin(entry, pin):
                    st.session_state.pop("unlock_target", None)
                    select_profile(entry["name"])
                else:
                    st.error("Wrong PIN. Try again.")
            return
        else:
            st.session_state.pop("unlock_target", None)

    profiles = storage.list_profiles()
    last = storage.last_active_profile()

    if profiles:
        st.markdown("#### 👥 Your profiles")
        summaries = [storage.profile_summary(p) for p in profiles]
        # order: last-active first
        summaries.sort(key=lambda s: (s["name"] != last, -s["xp"]))
        cols = st.columns(3)
        for i, s in enumerate(summaries):
            with cols[i % 3]:
                star = "⭐ " if s["name"] == last else ""
                lock = " 🔒" if s["locked"] else ""
                st.markdown(
                    f"<div class='card' style='text-align:center;'>"
                    f"<div style='font-size:1.35rem;font-weight:700;color:#eafcff;'>{star}{s['name']}{lock}</div>"
                    f"<div class='stat-lbl' style='margin-top:2px;'>{s['rank']}</div>"
                    f"<div style='margin-top:10px;'>🔥 <b>{s['streak']}</b> &nbsp;·&nbsp; ✨ <b>{s['xp']}</b> XP &nbsp;·&nbsp; {s['runs']} runs</div>"
                    f"</div>", unsafe_allow_html=True)
                btn_label = f"🔒 Play as {s['name']}" if s["locked"] else f"▶️ Play as {s['name']}"
                if st.button(btn_label, key=f"play_{s['slug']}", use_container_width=True, type="primary"):
                    if s["locked"]:
                        st.session_state["unlock_target"] = s["slug"]
                        st.rerun()
                    else:
                        select_profile(s["name"])
        st.write("")

    st.markdown("#### ➕ Create a new profile")
    st.markdown("<div style='color:#ffd24a;font-size:.92rem;margin-bottom:6px;'>🔒 Want to save your progress and keep "
                "others from checking your play? Add a PIN to your profile — it's optional.</div>",
                unsafe_allow_html=True)
    with st.form("new_profile_form", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            new_name = st.text_input("Profile name", key="new_profile_name",
                                     placeholder="e.g. Meet, Morning Me, Debate Prep...",
                                     label_visibility="collapsed")
            new_pin = st.text_input("PIN (optional)", key="new_profile_pin", type="password",
                                    placeholder="Optional PIN — leave blank for no lock",
                                    label_visibility="collapsed")
        with c2:
            submitted = st.form_submit_button("Create & Play", use_container_width=True, type="primary")
    if submitted:
        name = (new_name or "").strip()
        if not name:
            st.warning("Give your profile a name first.")
        else:
            entry = storage.create_profile(name, pin=(new_pin or "").strip() or None)
            select_profile(entry["name"])

    if profiles:
        with st.expander("🔐 Manage profiles · PINs · delete"):
            st.caption("A PIN lightly protects a profile on a shared computer (save files are local, so it's not "
                       "bank-grade security). Deleting a profile permanently erases its streak, XP and history.")
            for p in profiles:
                entry = storage.get_entry(p["slug"])
                locked = storage.has_pin(entry)
                st.markdown(f"**{p['name']}** {'🔒 locked' if locked else '🔓 no PIN'}")
                with st.form(f"pinform_{p['slug']}", clear_on_submit=True):
                    cur_pin = ""
                    if locked:
                        cur_pin = st.text_input("Current PIN", type="password", key=f"cur_{p['slug']}",
                                                placeholder="Current PIN (needed to change/remove/delete)")
                    new_p = st.text_input("New PIN", type="password", key=f"newpin_{p['slug']}",
                                          placeholder="New PIN (to set or change)")
                    m1, m2, m3 = st.columns(3)
                    set_btn = m1.form_submit_button("Set / change PIN", use_container_width=True)
                    rem_btn = m2.form_submit_button("Remove PIN", use_container_width=True)
                    del_btn = m3.form_submit_button("🗑️ Delete profile", use_container_width=True)

                if locked and (set_btn or rem_btn or del_btn) and not storage.verify_pin(entry, cur_pin):
                    st.error(f"Wrong current PIN for {p['name']} — action blocked.")
                elif set_btn:
                    if (new_p or "").strip():
                        storage.set_pin(p["slug"], new_p.strip())
                        st.success(f"PIN set for {p['name']}.")
                        st.rerun()
                    else:
                        st.warning("Enter a new PIN to set.")
                elif rem_btn:
                    storage.set_pin(p["slug"], None)
                    st.info(f"PIN removed for {p['name']}.")
                    st.rerun()
                elif del_btn:
                    storage.delete_profile(p["slug"])
                    st.rerun()
                st.divider()


# ---------------------------------------------------------------------------
# HOME / DASHBOARD
# ---------------------------------------------------------------------------

def render_home():
    state = st.session_state.state
    status = storage.streak_status(state)

    top = st.columns([3, 1])
    with top[1]:
        st.markdown(f"<div style='text-align:right;color:#9db3d4;padding-top:6px;'>👤 <b style='color:#eafcff;'>{state['profile']}</b></div>",
                    unsafe_allow_html=True)
        if st.button("🔄 Switch profile", use_container_width=True):
            switch_profile()

    st.markdown("<div class='arena-title'>🧠⚡ MIND ARENA ⚡🧠</div>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Six minutes. Three trials. Sharpen your mind and voice — every single day.</p>",
                unsafe_allow_html=True)

    live_clock()

    # streak alert banner
    if status["broken"]:
        st.error("💔 Your streak broke — you missed a day. Train now to start a fresh streak (and grab the Comeback Kid badge).")
    elif status["played_today"]:
        st.success("✅ You've trained today. Come back tomorrow to keep the streak alive — or run again for bonus XP!")
    elif status["at_risk"]:
        st.warning(f"🔥 Your {status['current']}-day streak is ALIVE but at risk — train today before midnight to keep it!")

    lvl, into, need, pct = storage.level_progress(state["xp"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card' style='text-align:center;'><div class='streak-fire'>🔥</div>"
                    f"<div class='stat-num'>{status['current']}</div>"
                    f"<div class='stat-lbl'>Day Streak</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card' style='text-align:center;'>"
                    f"<div class='stat-num'>{state['xp']}</div>"
                    f"<div class='stat-lbl'>Total XP</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card' style='text-align:center;'>"
                    f"<div class='stat-num'>Lv {lvl}</div>"
                    f"<div class='stat-lbl'>{storage.rank_name(state['xp'])}</div></div>",
                    unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card' style='text-align:center;'>"
                    f"<div class='stat-num'>{state['total_runs']}</div>"
                    f"<div class='stat-lbl'>Runs · Best {state['best_score']}</div></div>",
                    unsafe_allow_html=True)

    st.write("")
    if need is not None:
        st.markdown(f"**Level {lvl} → {lvl+1}**  ·  {need} XP to *{storage.RANKS[lvl][1]}*")
        st.progress(pct)
    else:
        st.markdown("**MAX RANK REACHED — Grandmaster of Mind & Voice** 👑")
        st.progress(1.0)

    st.write("")
    cta = st.columns([1, 2, 1])[1]
    with cta:
        st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
        label = "🔁 TRAIN AGAIN (bonus XP)" if status["played_today"] else "▶️  START DAILY RUN"
        if st.button(label, use_container_width=True, type="primary"):
            start_new_run()
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption("6 minutes · non-stop · everything compulsory")

    st.write("")
    tab_cal, tab_coach, tab_badges = st.tabs(["📅 Calendar & Streak", "🎙️ Speaking Coach & Warm-up", "🏅 Achievements"])

    with tab_cal:
        render_calendar(state)
    with tab_coach:
        render_coach()
    with tab_badges:
        render_badges(state)


def render_calendar(state):
    now = datetime.now()
    weeks = storage.month_grid(state, now.year, now.month)
    st.markdown(f"#### {now.strftime('%B %Y')}")
    html = "<div style='line-height:1.1;'>"
    html += "".join(f"<span class='cal-cell' style='border:none;color:#8aa0c0;'>{d}</span>"
                    for d in ["M", "T", "W", "T", "F", "S", "S"])
    html += "<br>"
    for week in weeks:
        for cell in week:
            if cell is None:
                html += "<span class='cal-cell' style='border:none;background:none;'></span>"
            else:
                if cell["played"]:
                    s = cell["score"]
                    if s >= 150:
                        bg = "rgba(56,245,168,.85)"
                    elif s >= 80:
                        bg = "rgba(56,245,168,.55)"
                    else:
                        bg = "rgba(56,245,168,.30)"
                    border = "2px solid #ffd24a" if cell["is_today"] else "1px solid rgba(56,245,168,.5)"
                    html += f"<span class='cal-cell' title='Score {s}' style='background:{bg};border:{border};color:#04240f;font-weight:700;'>{cell['day']}</span>"
                else:
                    border = "2px solid #ffd24a" if cell["is_today"] else "1px solid rgba(255,255,255,.06)"
                    html += f"<span class='cal-cell' style='border:{border};'>{cell['day']}</span>"
        html += "<br>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
    st.caption(f"🟩 Green = trained that day (brighter = higher score).  🟨 Yellow border = today.  "
               f"Longest streak ever: **{state['longest_streak']} days**.")


def render_coach():
    st.markdown("Warm up **before** you speak, then keep these principles in mind. "
                "Two minutes here compounds into a sharper voice for life.")

    with st.expander("🌬️ 60-Second Vocal Warm-up (do this before every run)", expanded=True):
        for title, body in content.VOICE_WARMUPS:
            st.markdown(f"<div class='coach-tip'><b>{title}</b><br>{body}</div>", unsafe_allow_html=True)
        st.markdown(f"**Tongue twister of the moment:** *{random.choice(content.TONGUE_TWISTERS)}* "
                    "— say it 3× (slow → medium → fast, always crisp).")

    with st.expander("💪 How to speak CONFIDENTLY"):
        for tip in content.COACH_CONFIDENCE:
            st.markdown(f"<div class='coach-tip'>{tip}</div>", unsafe_allow_html=True)

    with st.expander("✨ How to sound EXCELLENT (delivery & prosody)"):
        for tip in content.COACH_EXCELLENCE:
            st.markdown(f"<div class='coach-tip'>{tip}</div>", unsafe_allow_html=True)

    with st.expander("🩺 Voice health & fixing a harsh / hoarse voice"):
        for tip in content.COACH_VOICE_HEALTH:
            st.markdown(f"<div class='coach-tip'>{tip}</div>", unsafe_allow_html=True)

    with st.expander("🧱 The instant structure for ANY impromptu speech"):
        st.markdown(content.SPEECH_STRUCTURE_TIP)


def render_badges(state):
    have = set(state["badges"])
    st.markdown(f"**{len(have)} / {len(storage.BADGES)} unlocked**")
    html = ""
    for bid, (emoji, title, desc) in storage.BADGES.items():
        cls = "badge-chip" if bid in have else "badge-chip badge-locked"
        lock = "" if bid in have else " 🔒"
        html += f"<span class='{cls}' title='{desc}'>{emoji} {title}{lock}</span>"
    st.markdown(html, unsafe_allow_html=True)
    st.caption("Hover a badge to see how to unlock it.")


# ---------------------------------------------------------------------------
# STAGE 1 — BRAIN TEASER BLITZ
# ---------------------------------------------------------------------------

def render_brain():
    run = st.session_state.run
    stage_header(1, "BRAIN TEASER BLITZ", "Solve as many as you can. Speed and instinct — trust your gut, then move on.")

    timer_ring(DUR_BRAIN, auto_advance_to="s2_speak")

    l, r = st.columns([3, 1])
    with r:
        st.markdown(f"<div class='card' style='text-align:center;'>"
                    f"<div class='stat-num'>{run['solved']}</div><div class='stat-lbl'>Solved</div>"
                    f"<hr style='opacity:.15'>"
                    f"<div class='stat-num' style='color:#8aa0c0;'>{run['attempted']}</div>"
                    f"<div class='stat-lbl'>Attempted</div></div>", unsafe_allow_html=True)

    teasers = run["teasers"]
    idx = run["t_idx"] % len(teasers)
    t = teasers[idx]

    with l:
        st.markdown(f"<div class='prompt-box'>"
                    f"<div style='color:#ffd24a;letter-spacing:2px;font-size:.8rem;'>{t['type'].upper()} · #{run['attempted']+1}</div>"
                    f"<div class='teaser-q'>{t['q']}</div></div>", unsafe_allow_html=True)
        st.write("")
        if run["revealed"]:
            st.success(f"💡 **Answer:** {t['a']}")

        b1, b2, b3 = st.columns(3)
        with b1:
            if not run["revealed"]:
                if st.button("👁️ Reveal answer", use_container_width=True):
                    run["revealed"] = True
                    st.rerun()
        with b2:
            if st.button("✅ Got it!", use_container_width=True, type="primary"):
                run["solved"] += 1
                run["attempted"] += 1
                _next_teaser(run)
        with b3:
            if st.button("⏭️ Skip / Next", use_container_width=True):
                run["attempted"] += 1
                _next_teaser(run)

    st.caption("The stage auto-advances to the Speaking Forge when the timer hits zero. "
               "Or jump ahead ⤵️")
    if st.button("Skip to Stage 2 →"):
        go_to("s2_speak")


def _next_teaser(run):
    run["t_idx"] += 1
    run["revealed"] = False
    st.rerun()


# ---------------------------------------------------------------------------
# STAGE 2 — THE SPEAKING FORGE
# ---------------------------------------------------------------------------

def render_speak():
    run = st.session_state.run
    stage_header(2, "THE SPEAKING FORGE", "A 2–3 minute NON-STOP mini-speech. Weave the prop into it. Don't stop — fluency beats perfection.")

    timer_ring(DUR_SPEAK)

    st.markdown(f"<div class='prompt-box'>"
                f"<div class='prop-emoji'>{run['prop']}</div>"
                f"<div style='color:#ffd24a;letter-spacing:2px;font-size:.8rem;margin-top:8px;'>YOUR PROMPT · MUST INCLUDE THE PROP ABOVE</div>"
                f"<div class='teaser-q' style='margin-top:6px;'>{run['prompt']}</div></div>",
                unsafe_allow_html=True)

    with st.expander("⚡ Quick structure reminder (P-E-P)"):
        st.markdown(content.SPEECH_STRUCTURE_TIP)

    st.write("")
    st.markdown("#### 🎙️ Record your speech, then analyze it")
    audio = st.audio_input("Hit record, speak for the whole timer, then stop.", key="speak_audio")

    if audio is not None:
        if st.button("🔍 Analyze my speech", type="primary"):
            with st.spinner("Analyzing your delivery..."):
                run["speech_analysis"] = analysis.analyze_speech(audio.getvalue(), target_seconds=120)
            st.rerun()

    if run["speech_analysis"]:
        _show_analysis(run["speech_analysis"])
    else:
        st.info("No mic? No problem — speak out loud anyway (that's the real training), then self-rate below.")
        run["speech_selfrate"] = st.slider("How did that speech FEEL? (1 = shaky, 5 = on fire)",
                                            1, 5, run["speech_selfrate"], key="speak_self")

    st.write("")
    if st.button("Continue to Final Boss →", type="primary", use_container_width=True):
        go_to("s3_boss")


# ---------------------------------------------------------------------------
# STAGE 3 — PROGRESSIVE BOSS CHALLENGE
# ---------------------------------------------------------------------------

def render_boss():
    run = st.session_state.run
    boss = run["boss"]
    diff_dots = "🔴" * boss["difficulty"] + "⚪" * (3 - boss["difficulty"])
    stage_header(3, "BOSS CHALLENGE", f"Progressive difficulty {diff_dots} — the final trial. Push your mind to its edge.")

    timer_ring(DUR_BOSS)

    st.markdown(f"<div class='prompt-box'>"
                f"<div class='prop-emoji'>{boss['icon']}</div>"
                f"<div style='color:#ff2bd6;letter-spacing:2px;font-size:1rem;font-weight:800;margin-top:6px;'>{boss['name']}</div>"
                f"<div class='teaser-q' style='margin-top:8px;'>{boss['brief']}</div>"
                f"<div style='color:#eaf6ff;margin-top:12px;font-size:1.05rem;'>{boss['task']}</div>"
                f"<div style='color:#8aa0c0;margin-top:12px;font-size:.85rem;'>🧠 Trains: {boss['trains']}</div>"
                f"</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 🎙️ Record your boss attempt")
    audio = st.audio_input("Record your 60-second challenge run.", key="boss_audio")

    if audio is not None:
        if st.button("🔍 Analyze my attempt", type="primary"):
            with st.spinner("Analyzing..."):
                run["challenge_analysis"] = analysis.analyze_speech(audio.getvalue(), target_seconds=60)
            st.rerun()

    if run["challenge_analysis"]:
        _show_analysis(run["challenge_analysis"])
    else:
        run["challenge_selfrate"] = st.slider("How did the boss challenge FEEL? (1–5)",
                                               1, 5, run["challenge_selfrate"], key="boss_self")

    st.write("")
    if st.button("🏁 FINISH RUN & See Results", type="primary", use_container_width=True):
        go_to("results")


def _show_analysis(res):
    st.markdown(f"### {res.get('headline','Analysis')}  ·  Score: **{res['score']}/100**")
    if res.get("metrics"):
        cols = st.columns(len(res["metrics"]))
        for col, (k, v) in zip(cols, res["metrics"].items()):
            col.metric(k, v)
    if res.get("wins"):
        st.markdown("**✅ What you did well:**")
        for w in res["wins"]:
            st.markdown(f"- {w}")
    if res.get("feedback"):
        st.markdown("**🎯 Sharpen this next time:**")
        for f in res["feedback"]:
            st.markdown(f"- {f}")


# ---------------------------------------------------------------------------
# RESULTS
# ---------------------------------------------------------------------------

def render_results():
    run = st.session_state.run
    state = st.session_state.state

    if not run.get("_committed"):
        brain_solved = run["solved"]
        brain_score = brain_solved * 20

        sp = run.get("speech_analysis")
        speech_score = sp["score"] if sp else run.get("speech_selfrate", 3) * 18
        ch = run.get("challenge_analysis")
        challenge_score = ch["score"] if ch else run.get("challenge_selfrate", 3) * 18

        summary = storage.record_run(state, {
            "brain_score": brain_score,
            "brain_solved": brain_solved,
            "speech_score": speech_score,
            "challenge_score": challenge_score,
            "all_stages": True,
        })
        run["_committed"] = True
        run["_summary"] = summary
        run["_scores"] = (brain_score, speech_score, challenge_score)
        st.balloons()

    summary = run["_summary"]
    brain_score, speech_score, challenge_score = run["_scores"]

    st.markdown("<div class='arena-title'>🏁 RUN COMPLETE</div>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>You showed up. That's the whole game — and your streak agrees.</p>",
                unsafe_allow_html=True)

    if summary["leveled_up"]:
        st.success(f"🎉 **LEVEL UP!** You're now Level {summary['level_after']} — **{summary['rank']}**")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🧩 Brain", f"{brain_score}", f"{st.session_state.run['solved']} solved")
    c2.metric("🎙️ Speaking", f"{int(speech_score)}")
    c3.metric("⚡ Boss", f"{int(challenge_score)}")
    c4.metric("✨ XP Gained", f"+{summary['xp_gain']}", f"×{summary['streak_multiplier']:.2f} streak")

    st.write("")
    cc1, cc2, cc3 = st.columns(3)
    cc1.markdown(f"<div class='card' style='text-align:center;'><div class='streak-fire'>🔥</div>"
                 f"<div class='stat-num'>{summary['streak']}</div><div class='stat-lbl'>Day Streak</div></div>",
                 unsafe_allow_html=True)
    cc2.markdown(f"<div class='card' style='text-align:center;'>"
                 f"<div class='stat-num'>{state['xp']}</div><div class='stat-lbl'>Total XP</div></div>",
                 unsafe_allow_html=True)
    cc3.markdown(f"<div class='card' style='text-align:center;'>"
                 f"<div class='stat-num'>Lv {summary['level_after']}</div>"
                 f"<div class='stat-lbl'>{summary['rank']}</div></div>", unsafe_allow_html=True)

    if summary["new_badges"]:
        st.write("")
        st.markdown("### 🏅 New Achievements Unlocked!")
        chips = ""
        for bid in summary["new_badges"]:
            emoji, title, desc = storage.BADGES[bid]
            chips += f"<span class='badge-chip'>{emoji} <b>{title}</b> — {desc}</span>"
        st.markdown(chips, unsafe_allow_html=True)

    # combined coaching recap
    st.write("")
    st.markdown("### 🧭 Your coaching focus for tomorrow")
    tips = []
    for res in (run.get("speech_analysis"), run.get("challenge_analysis")):
        if res and res.get("feedback"):
            tips.extend(res["feedback"])
    if tips:
        # show the top 2 most actionable
        for t in tips[:2]:
            st.markdown(f"- {t}")
    else:
        st.markdown("- Record your speech next time (mic permitting) to unlock detailed voice analytics — "
                    "pace, pauses, volume steadiness and vocal variety.")

    st.write("")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("🏠 Back to Home", use_container_width=True, type="primary"):
            st.session_state.run = {}
            go_to("home")
    with b2:
        if st.button("🔁 Run Again", use_container_width=True):
            start_new_run()


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

def main():
    init_session()
    stage = st.session_state.stage

    # must have a profile selected for anything other than the picker
    if stage != "profiles" and "state" not in st.session_state:
        st.session_state.stage = "profiles"
        stage = "profiles"

    # top-right exit for in-run stages
    if stage not in ("home", "results", "profiles"):
        top = st.columns([6, 1])[1]
        with top:
            if st.button("✖ Quit", help="Abandon this run (no score saved)"):
                st.session_state.run = {}
                go_to("home")

    if stage == "profiles":
        render_profiles()
    elif stage == "home":
        render_home()
    elif stage == "s1_brain":
        render_brain()
    elif stage == "s2_speak":
        render_speak()
    elif stage == "s3_boss":
        render_boss()
    elif stage == "results":
        render_results()
    else:
        st.session_state.stage = "home"
        st.rerun()


if __name__ == "__main__":
    main()
