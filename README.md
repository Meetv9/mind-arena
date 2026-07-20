# 🧠⚡ Mind Arena

A personal, offline, gamified **6-minute daily brain + speech workout**. Three
non-stop trials sharpen your thinking and speaking every day, with streaks, XP,
levels, badges, a real clock & calendar, and automatic analysis of your voice.

## The 6-minute run

| Stage | Time | What happens |
|-------|------|--------------|
| **1 · Brain Teaser Blitz** | 2:00 | Rapid-fire riddles, logic, patterns, quick-math. Solve as many as you can before the timer auto-advances. |
| **2 · The Speaking Forge** | ~2:30 | A 2–3 minute NON-STOP mini-speech on a random prompt with a "prop" you must weave in. Record it and get instant analysis. |
| **3 · Boss Challenge** | ~2:30 | A progressive-difficulty speed challenge (Accidental Expert, Alphabet Sprint, Reverse Interview, Taboo Twist, Emotion Rollercoaster, Rapid-Fire Reframe). Record & analyze. |

Everything is compulsory to finish. Finish all three in one sitting for a bonus
and the **Iron Will** badge.

## Profiles (unlimited, no login, no database)

On launch you pick a **profile** or create a new one — make as many as you like
(you, a friend, "Morning Me", "Debate Prep"...). Each profile is a separate save
file with its **own streak, XP, badges and history**, so people sharing one
laptop never mix stats. Switch any time via **🔄 Switch profile** on the home
screen. There's no login: whoever is playing simply chooses their profile.

## Gamification

- 🔥 **Daily streak** — real calendar based. Miss a day and it breaks (come back
  for the *Comeback Kid* badge). Streak multiplies your XP (up to ×2).
- ✨ **XP & 10 ranks** — from *Rookie Rambler* to *Grandmaster of Mind & Voice*.
- 🏅 **12 badges** — endurance, streaks, golden-voice, night-owl, and more.
- 📅 **Calendar heat-map** — see every day you trained, brighter = higher score.

## Speech analysis (offline)

After you record, the app measures — with no internet and no cloud — your
**duration/endurance, speaking pace (WPM estimate), pause structure, volume
steadiness,** and **vocal variety**, then gives a 0–100 score plus specific
coaching. No mic? Speak out loud anyway and self-rate.

## Speaking Coach

The **Speaking Coach & Warm-up** tab on the home screen has a 60-second vocal
warm-up, tongue twisters, and concise guides on speaking confidently, sounding
excellent, and fixing a harsh/hoarse voice.

## Run it

```bash
cd mind-arena
pip install -r requirements.txt      # only if streamlit/numpy aren't installed
streamlit run app.py
```

Or on macOS just double-click **`run.command`**.

Your progress is saved locally in `mind_arena_data/profiles/` (one JSON file per
profile, plus a small registry). Nothing ever leaves your machine.

> Tip: allow microphone access in your browser when prompted so the voice
> analysis works.
