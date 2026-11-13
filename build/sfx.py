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


# ------------------------------------------------------------------------------------------------------------------
# 13 Nov (cinematic upgrade): foley and ambience for filmed scenes (cine.py). Same rule as above: everything is
# synthesised here, so there is nothing to license, and every sound belongs to an action on screen (a foot that
# lands, a page that turns, a coin that drops). Still no whoosh on routine transitions. These run at 48 kHz for
# the stereo masters (master.py); the Reel sounds above stay at 24 kHz.

FSR = 48000


def _ft(sec):
    return np.arange(int(sec * FSR)) / FSR


def _band(x, lo, hi, order=2):
    from scipy.signal import butter, lfilter
    b, a = butter(order, [max(lo, 20) / (FSR / 2), min(hi, FSR / 2 - 100) / (FSR / 2)], "band")
    return lfilter(b, a, x)


def footstep(seed=0, surface="cobble"):
    """A heel then a toe on stone: two short filtered noise taps and a soft low knock."""
    rng = np.random.default_rng(seed)
    t = _ft(.16)
    out = np.zeros(len(t))
    for k, (at, g) in enumerate(((0, 1.0), (rng.uniform(.035, .06), .55))):
        n = rng.standard_normal(len(t))
        env = np.where(t >= at, np.exp(-(t - at) * rng.uniform(70, 110)), 0)
        out += _band(n, 350, 2600 if surface == "cobble" else 1600) * env * g
    out += np.sin(2 * np.pi * rng.uniform(95, 130) * t) * np.exp(-t * 45) * .35
    return (out / (np.abs(out).max() + 1e-9)).astype(np.float32)


def paper(seed=0, sec=.45, crisp=1.0):
    """Handled paper: a burst of crinkles (sparse clicks through a mid-high band) under a soft rustle."""
    rng = np.random.default_rng(seed)
    t = _ft(sec)
    env = np.sin(np.pi * np.clip(t / sec, 0, 1)) ** .7
    rustle = _band(rng.standard_normal(len(t)), 1200, 7000) * env * .35
    clicks = np.zeros(len(t))
    for _ in range(int(sec * 70 * crisp)):
        i = rng.integers(0, len(t) - 200)
        clicks[i:i + 200] += rng.standard_normal(200) * np.exp(-np.arange(200) / 30) * rng.uniform(.3, 1)
    out = rustle + _band(clicks, 2000, 9000) * env
    return (out / (np.abs(out).max() + 1e-9)).astype(np.float32)


def quill(sec=1.1, seed=0, rate=9.0):
    """A nib on paper: high scratchy noise pulsed at the speed of handwriting."""
    rng = np.random.default_rng(seed)
    t = _ft(sec)
    strokes = (.5 + .5 * np.sin(2 * np.pi * rate * t + rng.uniform(0, 6))) ** 2
    strokes *= (.6 + .4 * np.abs(np.sin(2 * np.pi * 2.3 * t)))
    edge = np.clip(t / .05, 0, 1) * np.clip((sec - t) / .08, 0, 1)
    out = _band(rng.standard_normal(len(t)), 2500, 9500) * strokes * edge
    return (out / (np.abs(out).max() + 1e-9)).astype(np.float32)


def clink(seed=0, glass=False):
    """A coin landing on coins: a click and a few inharmonic metal partials; glass adds a jar's ring."""
    rng = np.random.default_rng(seed)
    t = _ft(.6 if glass else .35)
    out = _band(rng.standard_normal(len(t)), 3000, 12000) * np.exp(-t * 400) * .6
    for f, g, d in ((2350, 1, 26), (3610, .7, 34), (5230, .5, 44), (6980, .35, 60)):
        out += np.sin(2 * np.pi * f * rng.uniform(.97, 1.03) * t) * np.exp(-t * d) * g * .35
    if glass:
        out += np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 9) * .18 + np.sin(2 * np.pi * 2640 * t) * np.exp(-t * 12) * .1
    return (out / (np.abs(out).max() + 1e-9)).astype(np.float32)


def soft_hit(seed=0, pitch=220):
    """A felt mallet on a low wooden bar: the cue for a number or a flag landing on a chart."""
    t = _ft(.7)
    out = sum(np.sin(2 * np.pi * pitch * m * t) * np.exp(-t * (6 + 5 * m)) / m for m in (1, 2.76, 5.4))
    out += np.sin(2 * np.pi * pitch / 2 * t) * np.exp(-t * 9) * .5
    return (out / (np.abs(out).max() + 1e-9)).astype(np.float32)


def clock_tick(seed=0, tock=False):
    t = _ft(.06)
    f = 2900 if not tock else 2300
    out = np.sin(2 * np.pi * f * t) * np.exp(-t * 160) + _band(np.random.default_rng(seed).standard_normal(len(t)), 2000, 8000) * np.exp(-t * 300) * .5
    return (out / (np.abs(out).max() + 1e-9)).astype(np.float32)


def street_ambience(sec, seed=0, crowd=1.0):
    """A busy old street with no cars: distant city air, a low murmur of many people (shaped noise, no
    speech), occasional far-off cart wheels on stone. Stereo, peak about .5."""
    rng = np.random.default_rng(seed)
    n = int(sec * FSR)
    t = np.arange(n) / FSR
    out = np.zeros((n, 2), np.float32)
    for c in range(2):
        air = _band(rng.standard_normal(n), 60, 500) * .5
        murmur = np.zeros(n)
        for v in range(6):                                       # voices far away: formant-ish bands, swelling
            f0 = rng.uniform(280, 900)
            band = _band(rng.standard_normal(n), f0 * .8, f0 * 1.4)
            mod = .5 + .5 * np.sin(2 * np.pi * rng.uniform(.6, 2.4) * t + rng.uniform(0, 6)) * np.sin(2 * np.pi * rng.uniform(.1, .3) * t + rng.uniform(0, 6))
            murmur += band * np.clip(mod, 0, 1) ** 2
        out[:, c] = air + murmur * .55 * crowd
    for _ in range(int(sec / 4)):                                # a cart far off
        at = rng.uniform(0, max(sec - 2, .1))
        i0, ln = int(at * FSR), int(1.8 * FSR)
        tt = np.arange(ln) / FSR
        rumble = _band(rng.standard_normal(ln), 60, 260) * np.sin(np.pi * tt / 1.8) ** 2 * (.6 + .4 * np.sign(np.sin(2 * np.pi * 7 * tt)))
        pan = rng.uniform(.2, .8)
        out[i0:i0 + ln, 0] += rumble[: max(0, min(ln, n - i0))] * .5 * (1 - pan)
        out[i0:i0 + ln, 1] += rumble[: max(0, min(ln, n - i0))] * .5 * pan
    return (out / (np.abs(out).max() + 1e-9) * .5).astype(np.float32)


def room_tone(sec, seed=0, clock=True, street=.25):
    """A quiet room: low air, the street faintly through a window, a pendulum clock if wanted."""
    rng = np.random.default_rng(seed)
    n = int(sec * FSR)
    out = np.zeros((n, 2), np.float32)
    far = street_ambience(sec, seed + 1, crowd=.6) * street
    for c in range(2):
        out[:, c] = _band(rng.standard_normal(n), 40, 300) * .25 + far[:, c]
    if clock:
        k = 0
        for at in np.arange(.3, sec, 1.0):
            s = clock_tick(k, tock=bool(k % 2)) * .25
            i = int(at * FSR)
            out[i:i + len(s), :] += s[: max(0, min(len(s), n - i)), None]
            k += 1
    return (out / (np.abs(out).max() + 1e-9) * .4).astype(np.float32)


FOLEY = {"step": footstep, "paper": paper, "quill": quill, "clink": clink, "hit": soft_hit, "tick": clock_tick}


def foley_track(events, total, stereo=True):
    """events: (name, seconds, gain[, pan -1..1][, kwargs]). Returns float32 (n, 2) at 48 kHz."""
    n = int((total + 1.5) * FSR)
    buf = np.zeros((n, 2), np.float32)
    for k, ev in enumerate(events):
        name, at, g = ev[0], ev[1], ev[2]
        pan = ev[3] if len(ev) > 3 else 0.0
        kw = ev[4] if len(ev) > 4 else {}
        kw.setdefault("seed", k)
        sig = FOLEY[name](**kw) * g
        i = int(at * FSR)
        m = max(0, min(len(sig), n - i))
        gl, gr = ((1 - pan) / 2) ** .5, ((1 + pan) / 2) ** .5        # constant-power pan
        buf[i:i + m, 0] += sig[:m] * gl
        buf[i:i + m, 1] += sig[:m] * gr
    return buf
