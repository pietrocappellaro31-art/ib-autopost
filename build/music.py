"""
Original background music for YouTube videos (8 Nov, Pietro: "always put some
viral music in the background"). From 10 Nov the default, track(), is a
dramatic piano and cello piece (see the bottom of this file); the pop style
described below is kept as track_pop() for re-renders only.

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


def track_pop(total_s, seed=1, breaks=(), level=.9):
    """The first style (8 Nov): four-chord pop with drums. Retired 10 Nov (Pietro: "we are not at a
    lunapark"); kept so old videos can be re-rendered."""
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


# ------------------------------------------------- piano and cello (10 Nov) ----
# Pietro, 10 Nov: "The music is terrible, we are not at a lunapark. We prefer
# piano or cello. Something more dramatic." So the default is now a slow minor
# piece: a piano ostinato (broken chords, left-hand octaves) and a cello line
# in its low register, with a soft low drum at the start of each phrase and a
# hall reverb. Everything is synthesised here (additive piano with stretched,
# decaying partials; bowed cello with body resonances and delayed vibrato); no
# samples, nothing to license.

from scipy.signal import fftconvolve


def piano(f, dur, vel=.7, rng=None):
    """One piano note: three slightly detuned strings, stretched partials whose
    upper harmonics die first, and a soft hammer thump."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    B = 1.2e-4                                                      # inharmonicity
    x = np.zeros(n)
    for k in range(1, 14):
        fk = f * k * np.sqrt(1 + B * k * k)
        if fk > 9000:
            break
        amp = vel ** (1 + k * .12) / k ** 1.15
        dec = (.55 + .0016 * f) * (1 + .55 * (k - 1))                # higher partials and higher notes decay faster
        for dt in (-.0009, 0, .0011):
            x += amp * np.sin(2 * np.pi * fk * (1 + dt) * t + (rng.random() * 6.28 if rng is not None else 0)) * (
                .65 * np.exp(-t * dec) + .35 * np.exp(-t * dec * .18))  # two-stage decay, the piano's "aftersound"
    x /= 3
    hn = int(.012 * SR)
    if rng is not None:
        x[:hn] += lp(rng.standard_normal(hn), 1200) * np.linspace(1, 0, hn) * .08 * vel
    x *= np.minimum(t / .003, 1) * np.clip((dur - t) / .08, 0, 1)
    return lp(x, 2600 + 3600 * vel)


def cello(f, dur, vel=.6, rng=None):
    """A bowed cello note: bright harmonic series through three body
    resonances, a slow bow attack, vibrato that arrives after the onset, a
    little bow noise."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    vib = 1 + .0035 * np.sin(2 * np.pi * 5.3 * t + (rng.random() * 6 if rng is not None else 0)) * np.clip((t - .35) / .5, 0, 1)
    ph = 2 * np.pi * f * np.cumsum(vib) / SR
    x = sum(np.sin(k * ph) / k ** 1.05 * (1 if k < 9 else .5) for k in range(1, 22) if k * f < 10000)
    from scipy.signal import iirpeak
    y = x * .25
    for fc, q, g in ((230, 3, 1.4), (580, 4, .9), (1550, 3, .45)):
        b, a = iirpeak(fc, q, fs=SR)
        y = y + g * lfilter(b, a, x)
    if rng is not None:
        y += hp(lp(rng.standard_normal(n), 5000), 1500) * .03
    swell = np.minimum(t / .28, 1) ** 1.6 * (1 + .18 * np.sin(np.pi * np.clip(t / dur, 0, 1)))
    rel = np.clip((dur - t) / .35, 0, 1)
    return lp(y * swell * rel * vel, 4200) * .35


def drum(rng):
    """A low, soft, timpani-like hit."""
    n = int(2.2 * SR)
    t = np.arange(n) / SR
    f = 52 + 30 * np.exp(-t * 9)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    x[: int(.02 * SR)] += lp(rng.standard_normal(int(.02 * SR)), 900) * .4
    return x * .9


def hall(x, seconds=2.6, wet=.28, rng=None):
    rng = rng or np.random.default_rng(0)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-t * 6.9 / seconds)
    ir = lp(ir, 3800)
    ir[: int(.02 * SR)] = 0                                          # a short pre-delay
    ir /= np.sqrt(np.sum(ir ** 2))
    return (1 - wet) * x + wet * fftconvolve(x, ir)[: len(x)] * 3.0


PROGS = ([0, 8, 3, 10], [0, 5, 8, 7], [0, 8, 5, 7], [0, 3, 8, 7])     # i VI III VII, i iv VI V, i VI iv V, i III VI V


def track(total_s, seed=1, breaks=(), level=.9):
    """The default bed from 10 Nov: dramatic piano and cello in a minor key."""
    rng = np.random.default_rng(seed)
    bpm = float(rng.choice([66, 70, 72, 76, 80]))
    key = int(rng.choice([NOTE[k] for k in ("A", "C", "D", "E", "F", "G")]))
    prog = PROGS[int(rng.integers(len(PROGS)))]
    beat = 60 / bpm
    bar = 4 * beat
    n = int((total_s + 3) * SR)
    out = {k: np.zeros(n) for k in ("piano", "cello", "drum")}
    tonic = 45 + key if key <= 5 else 33 + key                      # around A2
    pat = [[0, 2, 1, 2, 3, 2, 1, 2], [0, 1, 2, 3, 2, 1, 2, 1], [0, 2, 3, 2, 1, 2, 3, 2]][int(rng.integers(3))]
    D = drum(rng)

    def put(buf, x, at):
        i = int(at * SR)
        if 0 <= i < n:
            buf[i:i + len(x)] += x[: n - i]

    nbars = int(np.ceil(total_s / bar)) + 1
    brk = sorted(breaks)
    last = None
    for b in range(nbars):
        t0 = b * bar
        quiet = any(br <= t0 < br + bar for br in brk)
        deg = prog[b % 4]
        minor = deg in (0, 5)                                        # i and iv minor; VI, III, VII, V major
        root = tonic + deg - (12 if deg > 7 else 0)
        chord = [root, root + (3 if minor else 4), root + 7, root + 12]
        if deg == 7:
            chord[1] = root + 4                                      # the major V, the pull home
        # left hand: low octave on beats 1 and 3
        for k in (0, 2):
            put(out["piano"], piano(hz(root - 12), beat * 2.2, .62 if k == 0 else .5, rng) * .9, t0 + k * beat + rng.uniform(0, .008))
        # right hand: the broken chord, an octave up, eighth notes, softer off the beat
        for k, idx in enumerate(pat):
            v = (.55 if k % 2 == 0 else .42) * (.8 if quiet else 1) + rng.uniform(-.04, .04)
            put(out["piano"], piano(hz(chord[idx] + 12), beat * 1.4, v, rng) * .55, t0 + k * beat / 2 + rng.uniform(0, .012))
        # cello: in from bar 2, two notes a bar, chord tones in its low register, moving by step where it can
        if b >= 2 and not quiet:
            for h in (0, 2):
                cands = [m for m in chord[:3] for m in (m - 12, m) if 36 <= m <= 57]
                tgt = min(cands, key=lambda m: abs(m - (last or cands[len(cands) // 2])) + rng.uniform(0, 3))
                last = tgt
                put(out["cello"], cello(hz(tgt), beat * 2.15, .62 + .1 * (b % 8 >= 4), rng), t0 + h * beat)
        if b >= 2 and b % 4 == 0 and not quiet:
            put(out["drum"], D * .55, t0)
    t = np.arange(n) / SR
    mix = out["piano"] * .9 + out["cello"] * 1.0 + out["drum"] * .5
    mix = hall(mix, rng=rng)
    fade = np.minimum(1, t / 1.2) * np.clip((total_s + 2 - t) / 3, 0, 1)
    mix = mix * fade / (np.percentile(np.abs(mix), 99.9) + 1e-9)    # loudest notes near 1, then only a gentle soft clip
    mix = np.tanh(mix * .9)
    mix = mix / (np.abs(mix).max() + 1e-9) * level
    return mix[: int((total_s + .5) * SR)].astype(np.float32), dict(bpm=bpm, key=list(NOTE)[key], prog=prog, seed=seed, style="piano and cello")
