"""
Sound design for Reels: the standard from 6 Nov (Pietro: "that's the standard
we're going to use every time from now on", and "the more you add, the
better"). Every motion beat that has a physical feel gets a sound: ticks on a
timer or a spinning number, a soft ding on a reveal, a low thump when time
runs out, a pop when something lands.

No whoosh on swipes between scenes: Pietro found it annoying (6 Nov), the
only effect he did. whoosh() stays here for reference and is not in SOUNDS.
All synthesised here, so there is nothing to license.

They sit under the voice and under the music Pietro adds in the app: quiet,
short, never more than one at a time where it matters.

    from sfx import track, mux
    wav = track([("pop", 4.9), ("tick", 7.4), ("ding", 9.1)], total=30)
    mux("reel-silent.mp4", wav, "reel.mp4")        # for a Reel without voice
"""

import subprocess

import numpy as np

SR = 24000


def _t(sec):
    return np.arange(int(sec * SR)) / SR


def tick():
    t = _t(.05)
    return (np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 70)).astype(np.float32)


def whoosh(sec=.34, seed=3):
    rng = np.random.default_rng(seed)
    n = int(sec * SR)
    x = np.convolve(rng.standard_normal(n), np.ones(24) / 24, "same")      # soft, low noise
    env = np.sin(np.pi * np.arange(n) / n) ** 2
    return (x * env / np.abs(x).max()).astype(np.float32)


def ding(decay=5):
    t = _t(1.0)
    return ((np.sin(2 * np.pi * 1318.5 * t) + .5 * np.sin(2 * np.pi * 1975.5 * t)) * np.exp(-t * decay)).astype(np.float32)


def thump():
    t = _t(.5)
    return (np.sin(2 * np.pi * 62 * t) * np.exp(-t * 7)).astype(np.float32)


def pop():
    t = _t(.09)
    f = 520 + 900 * np.exp(-t * 60)                                         # a quick downward blip
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45)).astype(np.float32)


SOUNDS = {"tick": (tick, .22), "ding": (ding, .13), "thump": (thump, .55), "pop": (pop, .3)}


def track(events, total, gain=1.0):
    """events: (name, seconds) or (name, seconds, gain). Returns float32 mono at SR."""
    buf = np.zeros(int((total + 1) * SR), np.float32)
    for ev in events:
        name, at = ev[0], ev[1]
        fn, g = SOUNDS[name]
        sig = fn() * (ev[2] if len(ev) > 2 else g) * gain
        i = int(at * SR)
        buf[i:i + len(sig)] += sig[: max(0, len(buf) - i)]
    return buf


def mux(silent_mp4, sfx, out, lufs=-24):
    """Put an effects-only track on a silent Reel, quieter than a voiced mix
    (-24 LUFS against -16) so the music added in the app carries it."""
    import tempfile
    import wave
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        with wave.open(f.name, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(sfx, -1, 1) * 32767).astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent_mp4), "-i", f.name,
                        "-filter_complex", f"[1:a]loudnorm=I={lufs}:TP=-3:LRA=11[a]", "-map", "0:v", "-map", "[a]",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest",
                        "-movflags", "+faststart", str(out)], check=True)
