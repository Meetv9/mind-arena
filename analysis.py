# -*- coding: utf-8 -*-
"""
analysis.py — Offline acoustic analysis of a recorded speech.

We deliberately avoid heavy ML / cloud speech-to-text so the game always works
with nothing but numpy + Python's stdlib `wave`. From the raw waveform we can
still measure the things that matter most for a *speaker*:

  * duration vs the target (did you fill the time non-stop?)
  * speaking energy & volume consistency (are you projecting? steady?)
  * pause structure — silence ratio and number of long pauses (hesitation)
  * an estimated speaking pace (WPM) from energy-peak / syllable proxy
  * pitch variation proxy (monotone vs dynamic delivery)

Everything degrades gracefully: if the audio can't be read we return a clear,
non-crashing result the UI can still show.
"""

import io
import wave
import numpy as np


def _read_wav(audio_bytes: bytes):
    """Return (samples float32 mono in [-1,1], sample_rate) or (None, None)."""
    try:
        with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            raw = wf.readframes(n_frames)

        if sampwidth == 2:
            data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        elif sampwidth == 4:
            data = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
        elif sampwidth == 1:
            data = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
        else:
            return None, None

        if n_channels > 1:
            data = data.reshape(-1, n_channels).mean(axis=1)
        return data, framerate
    except Exception:
        return None, None


def _frame_energy(samples, sr, frame_ms=30):
    frame_len = max(1, int(sr * frame_ms / 1000))
    n = len(samples) // frame_len
    if n == 0:
        return np.array([]), frame_len
    trimmed = samples[: n * frame_len].reshape(n, frame_len)
    rms = np.sqrt(np.mean(trimmed ** 2, axis=1) + 1e-12)
    return rms, frame_len


def analyze_speech(audio_bytes: bytes, target_seconds: int = 60) -> dict:
    """
    Analyze a recording and return a rich, UI-ready dict. Never raises.
    """
    result = {
        "ok": False,
        "duration": 0.0,
        "target": target_seconds,
        "wpm_estimate": 0,
        "silence_ratio": 0.0,
        "long_pauses": 0,
        "volume_consistency": 0.0,
        "pitch_variation": 0.0,
        "avg_volume": 0.0,
        "score": 0,
        "metrics": {},
        "feedback": [],
        "wins": [],
    }

    samples, sr = _read_wav(audio_bytes)
    if samples is None or len(samples) == 0 or sr is None:
        result["feedback"] = ["Couldn't read the audio clearly — but the important thing is you spoke. "
                              "Try recording again in a quieter spot, or just self-rate below."]
        return result

    duration = len(samples) / sr
    result["duration"] = round(duration, 1)

    rms, frame_len = _frame_energy(samples, sr)
    if len(rms) == 0:
        result["feedback"] = ["Recording was too short to analyze. Aim to keep talking for the full time."]
        return result

    # --- silence / pause detection ---
    # Adaptive threshold: a fraction of the loud-speech level.
    peak = np.percentile(rms, 90)
    floor = np.percentile(rms, 10)
    thresh = floor + 0.15 * (peak - floor)
    voiced = rms > thresh
    silence_ratio = float(1.0 - voiced.mean())

    # count "long" pauses (>= ~0.6s of continuous silence within the speech)
    frame_sec = frame_len / sr
    long_pause_frames = max(1, int(0.6 / frame_sec))
    long_pauses = 0
    run = 0
    for v in voiced:
        if not v:
            run += 1
        else:
            if run >= long_pause_frames:
                long_pauses += 1
            run = 0
    if run >= long_pause_frames:
        long_pauses += 1

    # --- volume ---
    avg_volume = float(np.mean(rms))
    vol_std = float(np.std(rms))
    # consistency: lower relative std = steadier. Map to 0..1 (1 = very steady)
    volume_consistency = float(max(0.0, 1.0 - min(1.0, vol_std / (avg_volume + 1e-6))))

    # --- pace estimate via energy peaks (syllable proxy) ---
    voiced_rms = rms.copy()
    # smooth
    if len(voiced_rms) >= 3:
        kernel = np.ones(3) / 3
        smooth = np.convolve(voiced_rms, kernel, mode="same")
    else:
        smooth = voiced_rms
    pk_thresh = thresh
    peaks = 0
    for i in range(1, len(smooth) - 1):
        if smooth[i] > pk_thresh and smooth[i] >= smooth[i - 1] and smooth[i] > smooth[i + 1]:
            peaks += 1
    syllables = peaks
    speaking_time = max(0.5, duration * (1.0 - silence_ratio))
    syllables_per_sec = syllables / speaking_time
    # ~1.5 syllables per English word on average
    wpm_estimate = int((syllables_per_sec / 1.5) * 60)
    wpm_estimate = max(0, min(300, wpm_estimate))

    # --- pitch variation proxy via zero-crossing rate variability ---
    # ZCR tracks (roughly) with pitch/brightness; its variance hints at how
    # much the voice moves vs a flat monotone.
    seg = frame_len
    n_seg = len(samples) // seg
    if n_seg >= 2:
        segs = samples[: n_seg * seg].reshape(n_seg, seg)
        signs = np.sign(segs)
        zcr = np.mean(np.abs(np.diff(signs, axis=1)) > 0, axis=1)
        # only where voiced
        vlen = min(len(zcr), len(voiced))
        zcr_voiced = zcr[:vlen][voiced[:vlen]]
        if len(zcr_voiced) > 2:
            pitch_variation = float(min(1.0, np.std(zcr_voiced) / (np.mean(zcr_voiced) + 1e-6)))
        else:
            pitch_variation = 0.0
    else:
        pitch_variation = 0.0

    result.update({
        "ok": True,
        "wpm_estimate": wpm_estimate,
        "silence_ratio": round(silence_ratio, 3),
        "long_pauses": long_pauses,
        "volume_consistency": round(volume_consistency, 3),
        "pitch_variation": round(pitch_variation, 3),
        "avg_volume": round(avg_volume, 4),
    })

    result["metrics"] = {
        "Duration": f"{duration:.1f}s / {target_seconds}s target",
        "Pace (est.)": f"~{wpm_estimate} words/min",
        "Silence": f"{silence_ratio*100:.0f}% of the time",
        "Long pauses": f"{long_pauses}",
        "Volume steadiness": f"{volume_consistency*100:.0f}%",
        "Vocal variety": f"{pitch_variation*100:.0f}%",
    }

    _score_and_advise(result, target_seconds, duration, wpm_estimate,
                      silence_ratio, long_pauses, volume_consistency, pitch_variation)
    return result


def _score_and_advise(result, target, duration, wpm, silence_ratio,
                      long_pauses, vol_consistency, pitch_var):
    """Turn raw metrics into a 0..100 score + specific coaching."""
    feedback = []
    wins = []
    score = 0.0

    # 1) Duration / endurance (30 pts) — did you fill the time non-stop?
    fill = min(1.0, duration / target)
    dur_pts = 30 * fill
    score += dur_pts
    if fill >= 0.95:
        wins.append(f"You went the distance — {duration:.0f}s of non-stop speaking. That endurance is the whole game.")
    elif fill >= 0.6:
        feedback.append(f"You spoke {duration:.0f}s of the {target}s target. Push to fill the *entire* clock next time — the last 20 seconds is where real fluency is forged.")
    else:
        feedback.append(f"Only {duration:.0f}s of {target}s. The mission is *non-stop* — even repeating or rephrasing beats stopping. Keep the sound going.")

    # 2) Pace (20 pts) — ideal ~130-160 wpm
    if wpm == 0:
        pace_pts = 5
        feedback.append("Couldn't detect a clear pace — project a bit more and enunciate.")
    elif 125 <= wpm <= 165:
        pace_pts = 20
        wins.append(f"Excellent pace (~{wpm} wpm) — right in the confident, easy-to-follow zone.")
    elif wpm < 125:
        pace_pts = 12
        feedback.append(f"Your pace (~{wpm} wpm) is on the slow side. A touch more energy and momentum will sound more assured — aim for 130–160.")
    else:
        pace_pts = 11
        feedback.append(f"You're racing (~{wpm} wpm). Slow down ~20%, add deliberate pauses at your key points — authority lives in the pauses.")
    score += pace_pts

    # 3) Pauses / hesitation (20 pts)
    if silence_ratio <= 0.18 and long_pauses <= 2:
        pause_pts = 20
        wins.append("Smooth flow with very little dead air — you kept momentum beautifully.")
    elif silence_ratio <= 0.32:
        pause_pts = 13
        if long_pauses >= 3:
            feedback.append(f"You had {long_pauses} long pauses. A little silence is powerful, but too much reads as hesitation — try bridging with a linking phrase instead of stopping.")
        else:
            feedback.append("Flow was decent. Trim the longer gaps by planning your next sentence while finishing the current one.")
    else:
        pause_pts = 7
        feedback.append(f"Lots of silence ({silence_ratio*100:.0f}%) and {long_pauses} long pauses. This is the #1 thing to attack: keep talking through the uncertainty — fluency beats perfection here.")
    score += pause_pts

    # 4) Volume steadiness (15 pts)
    if vol_consistency >= 0.55:
        vol_pts = 15
        wins.append("Steady, controlled projection — your volume didn't wobble.")
    elif vol_consistency >= 0.35:
        vol_pts = 10
        feedback.append("Your volume drifted a little. Support your voice from the belly (diaphragm) so you don't trail off at the ends of sentences.")
    else:
        vol_pts = 5
        feedback.append("Volume was uneven — likely trailing off. Breathe at the full stops and drive each sentence all the way to its final word.")
    score += vol_pts

    # 5) Vocal variety (15 pts)
    if pitch_var >= 0.35:
        var_pts = 15
        wins.append("Great vocal variety — you weren't a monotone, which keeps a listener locked in.")
    elif pitch_var >= 0.2:
        var_pts = 10
        feedback.append("Some vocal variety, but you can stretch it further. Consciously go higher on excitement and lower on serious points — range = interest.")
    else:
        var_pts = 5
        feedback.append("Delivery leaned monotone. Exaggerate your pitch changes on purpose next time; it'll feel over-the-top to you and just right to a listener.")
    score += var_pts

    result["score"] = int(round(min(100, score)))
    result["feedback"] = feedback
    result["wins"] = wins

    # a short priority tip
    if result["score"] >= 85:
        result["headline"] = "🏆 Outstanding delivery."
    elif result["score"] >= 70:
        result["headline"] = "💪 Strong — a few tweaks from excellent."
    elif result["score"] >= 50:
        result["headline"] = "📈 Solid base. Attack the notes below."
    else:
        result["headline"] = "🌱 Every rep counts. Focus on one fix below."
