"""
Measure how far the narration sits over each score style, and the music level that puts it LEVEL_TARGET_DB over
(19 Nov 2026, YouTube #13; the 18 Nov next improvement in docs/daily/quality-log.md).

Why: master_music() levels every style to the same RMS, yet the voice sat only 18.8 dB over the mallets score (#11)
and 19.3 dB over the harp score (#12), against 26 to 29 dB for the orchestral scores of #7 to #10, all at the same
music level .22. The score gate (18 dB) passed, barely. This script measures it the way youtube.sound_report() does
(the same voice chain, the same sidechain ducking, the same speech mask), on a real narration, for every style, and
prints the level per style for score.STYLE_LEVEL.

    python3 build/score_levels.py build/out/<slug> [seconds=150] [--write]

<slug> must hold synth.pkl (any long film after yt_timing.py). --write puts the levels into build/score.py.
"""

import json
import pathlib
import pickle
import re
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import score as SC              # noqa: E402
import master as M              # noqa: E402
import quality                  # noqa: E402
from voice import MASTER        # noqa: E402

BASE = .22                      # the 13 Nov level every style used until today


def narration(work, seconds):
    """The film's own lines from synth.pkl, beats only, joined with the engine's gaps, up to `seconds`."""
    store = pickle.load(open(work / "synth.pkl", "rb"))
    sr = 24000
    parts, n = [], 0
    for (voice, speed, text), (a, segs) in store.items():
        if len(text.split()) < 6:                    # chapter titles are short: skip
            continue
        parts += [np.asarray(a, np.float32), np.zeros(int(.75 * sr), np.float32)]
        n += len(a) + int(.75 * sr)
        if n > seconds * sr:
            break
    v = np.concatenate(parts)[: int(seconds * sr)]
    return v / max(np.abs(v).max(), 1e-6) * .7, sr


def vom(voice_wav, music_wav, level, tmp):
    """Voice over the ducked music while speaking, in dB (sound_report's measure)."""
    ducked = tmp / "ducked.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(voice_wav), "-i", str(music_wav), "-filter_complex",
                    f"[0:a]{MASTER},aresample=48000[key];[1:a]aresample=48000,volume={level}[m];"
                    f"[m][key]sidechaincompress=threshold=0.02:ratio=5:attack=30:release=350:makeup=1[md]",
                    "-map", "[md]", "-ac", "1", str(ducked)], check=True)
    v, m = quality.load16(voice_wav), quality.load16(ducked)
    k = min(len(v), len(m))
    v, m = v[:k], m[:k]
    rv = np.sqrt(np.convolve(v ** 2, np.ones(1600) / 1600, "same"))
    on = rv > .25 * np.percentile(rv[rv > 1e-4], 90)
    return float(20 * np.log10(np.sqrt(np.mean(v[on] ** 2)) / max(np.sqrt(np.mean(m[on] ** 2)), 1e-9)))


def main():
    work = pathlib.Path(sys.argv[1])
    secs = float(next((a for a in sys.argv[2:] if a.replace(".", "").isdigit()), 150))
    tmp = pathlib.Path(tempfile.mkdtemp())
    v, sr = narration(work, secs)
    vw = tmp / "voice.wav"
    _write(vw, v, sr)
    plan = ["mystery", "decide", "explain", "crash", "resolve"]
    cut = [secs * i / len(plan) for i in range(len(plan) + 1)]
    sections = [(cut[i], cut[i + 1], plan[i]) for i in range(len(plan))]
    out = {}
    for style in SC.STYLES:
        stems, _ = SC.compose(sections, key="D", bpm=80, seed=13, style=style)
        mw = tmp / f"{style}.wav"
        M.write_wav(mw, SC.master_music(stems, wet=SC.STYLES[style].get("wet", .22)))
        d0 = vom(vw, mw, BASE, tmp)
        lvl = round(BASE * 10 ** ((d0 - SC.LEVEL_TARGET_DB) / 20), 4)
        d1 = vom(vw, mw, lvl, tmp)
        out[style] = dict(at_022_db=round(d0, 1), level=lvl, at_level_db=round(d1, 1))
        print(f"{style:11s} voice over music at .22: {d0:5.1f} dB -> level {lvl:.4f}: {d1:5.1f} dB", flush=True)
    json.dump(out, open(work / "score_levels.json", "w"), indent=1)
    if "--write" in sys.argv:
        p = pathlib.Path(__file__).parent / "score.py"
        s = p.read_text()
        body = "STYLE_LEVEL = {" + ", ".join(f'"{k}": {v["level"]}' for k, v in out.items()) + "}"
        s = re.sub(r"STYLE_LEVEL = \{[^}]*\}", body, s, count=1)
        p.write_text(s)
        print("written:", body)


def _write(path, x, sr):
    import wave
    y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(y.tobytes())


if __name__ == "__main__":
    main()
