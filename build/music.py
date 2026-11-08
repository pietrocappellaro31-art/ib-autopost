"""
Original background music for YouTube videos (8 Nov, Pietro: "always put some
viral music in the background").

Real trending songs are not an option: every one is copyrighted, Content ID
would claim the video and its ad revenue, and the channel is aiming for
monetisation. So each video gets its own track, synthesised here from
scratch (nothing sampled, nothing to license), in the style that trends on
short-form and explainer channels: a four-chord pop progression (vi-IV-I-V),
a punchy kick and clap, off-beat hats, a plucked arpeggio and a warm bass,
at 96 to 118 BPM. The seed changes the key, tempo, pattern and sound, so no
two videos share a track.

The music drops out for a beat at each chapter card and comes back in, and
it is ducked under the voice when the mix is made (youtube.py).

    from music import track
    a = track(total_s=120, seed=1, breaks=[25.9, 50.5])     # float32 mono, 48 kHz
"""

import numpy as np
from scipy.signal import butter, lfilter

SR = 48000
NOTE = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def lp(x, f, order=2):
    b, a = butter(order, min(f / (SR / 2), .99), "low")
    return lfilter(b, a, x)


def hp(x, f, order=2):
    b, a = butter(order, min(f / (SR / 2), .99), "high")
    return lfilter(b, a, x)


def env(n, a=.005, d=.2, s=0.0, r=.05, hold=None):
    """Attack, decay to sustain level, release, over n samples."""
    t = np.arange(n) / SR
    e = np.minimum(t / max(a, 1e-4), 1.0)
    e *= s + (1 - s) * np.exp(-np.maximum(t - a, 0) / max(d, 1e-4))
    if hold is not None:
        rel = np.clip((t - hold) / max(r, 1e-4), 0, 1)
        e *= 1 - rel
    return e


def kick(rng):
    n = int(.45 * SR)
    t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t * 32)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    x[: int(.004 * SR)] += rng.standard_normal(int(.004 * SR)) * .3          # click
    return np.tanh(x * 1.6)


def clap(rng):
    n = int(.25 * SR)
    noise = hp(lp(rng.standard_normal(n), 6000), 900)
    e = np.zeros(n)
    for k in (0, .011, .022):                                                  # three quick hits, like hands
        i = int(k * SR)
        e[i:] += np.exp(-np.arange(n - i) / SR * (60 if k < .02 else 18))
    return noise * e * .5


def hat(rng, open_=False):
    n = int((.18 if open_ else .05) * SR)
    x = hp(rng.standard_normal(n), 7000)
    return x * np.exp(-np.arange(n) / SR * (14 if open_ else 70)) * .35


def saw(f, n, detune=0.0, rng=None):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in (-detune, 0, detune) if detune else (0,):
        ph = (f * (1 + d) * t + (rng.random() if rng is not None else 0)) % 1.0
        out += 2 * ph - 1
    return out / (3 if detune else 1)


def pluck(f, n, bright):
    t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * f * t)) * .5 + np.sin(2 * np.pi * 2 * f * t) * .3
    return lp(x, bright) * np.exp(-t * 9)


def track(total_s, seed=1, breaks=(), level=.9):
    rng = np.random.default_rng(seed)
    bpm = float(rng.choice([96, 100, 104, 108, 112, 116, 118]))
    key = int(rng.choice([NOTE[k] for k in ("A", "C", "D", "E", "F", "G")]))
    beat = 60 / bpm
    bar = 4 * beat
    n = int((total_s + 2) * SR)
    out = {k: np.zeros(n) for k in ("drums", "bass", "pad", "arp")}
    # vi IV I V in the key (minor-feel pop loop), one chord per bar
    root = 57 + key - 12 if key > 6 else 57 + key                              # around A3
    prog = [(9, "m"), (5, ""), (0, ""), (7, "")]
    prog = [(root - 9 + d, q) for d, q in prog]
    arp_pat = rng.choice([[0, 1, 2, 1, 3, 2, 1, 2], [0, 2, 1, 3, 0, 2, 1, 3], [0, 1, 2, 3, 2, 1, 2, 3]])
    hat_open = bool(rng.random() < .5)
    bright = float(rng.choice([1800, 2400, 3200]))
    K, C = kick(rng), clap(rng)
    H_, HO = hat(rng), hat(rng, True)

    def put(buf, x, at):
        i = int(at * SR)
        if 0 <= i < n:
            buf[i:i + len(x)] += x[: n - i]

    nbars = int(np.ceil(total_s / bar)) + 1
    brk = sorted(breaks)
    for b in range(nbars):
        t0 = b * bar
        # drums are out for the bar after a chapter card starts, then back in
        quiet = any(br <= t0 < br + bar for br in brk) or b == 0
        deg, q = prog[b % 4]
        chord = [deg, deg + (3 if q == "m" else 4), deg + 7, deg + 12]
        # pad: the chord, held, soft
        npad = int(bar * SR)
        pad = sum(saw(hz(m), npad, .006, rng) for m in chord) / 4
        pad = lp(pad, 1400) * env(npad, a=.25, d=9, s=.8, r=.2, hold=bar - .2)
        put(out["pad"], pad * .5, t0)
        # bass: root on the beat and the and-of-two
        for k, step in enumerate((0, 1.5, 2, 3)):
            nb = int(beat * .9 * SR)
            x = lp(saw(hz(deg - 12), nb) + .6 * np.sin(2 * np.pi * hz(deg - 24) * np.arange(nb) / SR), 420)
            put(out["bass"], x * env(nb, a=.004, d=.25, s=.5, r=.04, hold=beat * .8) * .8, t0 + step * beat)
        # arp: eighth notes over the chord, an octave up
        if b >= 1:
            for k, idx in enumerate(arp_pat):
                na = int(beat * .5 * SR)
                put(out["arp"], pluck(hz(chord[idx] + 12), na, bright) * .45, t0 + k * beat / 2)
        if quiet:
            continue
        for k in range(4):
            put(out["drums"], K * .95, t0 + k * beat)                       # four on the floor
            if k in (1, 3):
                put(out["drums"], C * .9, t0 + k * beat)
            put(out["drums"], (HO if hat_open and k % 2 else H_) * .8, t0 + k * beat + beat / 2)
            put(out["drums"], H_ * .4, t0 + k * beat + beat / 4 * 3)
    # sidechain pump: everything but the drums dips on each kick, the sound of the genre
    t = np.arange(n) / SR
    pump = 1 - .45 * np.exp(-((t % beat) / .09))
    mix = out["drums"] * 1.0 + (out["bass"] * .9 + out["pad"] * .55 + out["arp"] * .5) * pump
    fade = np.minimum(1, t / 1.5) * np.clip((total_s + 1.5 - t) / 2.5, 0, 1)
    mix = np.tanh(mix * fade * 1.2)
    mix = mix / (np.abs(mix).max() + 1e-9) * level
    return mix.astype(np.float32), dict(bpm=bpm, key=list(NOTE)[key], seed=seed)


def write(path, x):
    import wave
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
