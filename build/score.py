"""
Original scoring for cinematic finance videos (13 Nov 2026).

Pietro's last verdicts on our synthesised beds were "terrible", "we are not at a lunapark" and "even too
dramatic" (8 to 12 Nov). The beds in music.py were made of modelled oscillators. This engine writes notes
(harmony, voice leading, a motif that develops) and plays them on sampled instruments from the GeneralUser
GS SoundFont (S. Christian Collins, v2.0.3: free for private or commercial music; licence text in
docs/rights/ledger.md), rendered offline with TinySoundFont, then puts them in a synthetic hall.

A cue follows the film: sections with their own mood, aligned to shot or chapter times.

    from score import compose
    stems = compose([(0, 6.0, "bustle"), (6.0, 12.6, "discover"), (12.6, 17.3, "decide"), (17.3, 20.6, "peak")],
                    key="F", seed=3)
    # stems: {"strings": stereo array, "keys": ..., "winds": ..., "perc": ...}, 48 kHz float32, unmixed

Moods (the finance cue library): bustle (market excitement), explain (light educational), discover
(financial discovery), mystery (historical mystery), decide (suspense, a decision), peak (crisis building,
unresolved), crash (crisis), reflect (reflection), resolve (resolution), quiz (quiz tension), reveal (quiz
answer). Each sets an instrumentation, a progression and a rhythm; the seed varies voicing, motif and
pattern so two videos never share a cue. Nothing here quotes a melody, progression or arrangement of a
commercial recording: progressions are generic diatonic ones, the motif is generated from the seed.

The SoundFont lives outside the repo (setup_voice.sh fetches it to ~/voice-tools/soundfonts).
"""

import os
import random

import numpy as np

SR = 48000
SF = os.environ.get("SOUNDFONT", os.path.expanduser("~/voice-tools/soundfonts/GeneralUser-GS.sf2"))
NOTE = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}
NOTE.update({"Db": 1, "Eb": 3, "Gb": 6, "Ab": 8, "Bb": 10})
MAJOR, MINOR = [0, 2, 4, 5, 7, 9, 11], [0, 2, 3, 5, 7, 8, 10]

# GM presets (bank 0). Grouped into stems so the mix can balance them.
INSTR = dict(harpsichord=(6, "keys"), piano=(0, "keys"), celesta=(8, "keys"), glock=(9, "keys"), marimba=(12, "keys"),
             pizz=(45, "strings"), strings=(49, "strings"), fast_strings=(48, "strings"), trem=(44, "strings"),
             cello=(42, "strings"), bass=(43, "strings"), oboe=(68, "winds"), flute=(73, "winds"), clarinet=(71, "winds"),
             bassoon=(70, "winds"), horn=(60, "winds"), timpani=(47, "perc"),
             # 17 Nov (Pietro: "experiment with different kinds of music and not always use the same music"): the
             # instruments of the other styles (STYLES below)
             epiano=(4, "keys"), vibes=(11, "keys"), musicbox=(10, "keys"), harp=(46, "keys"), kalimba=(108, "keys"),
             nylon=(24, "keys"), steel=(25, "keys"), upbass=(32, "strings"), fbass=(33, "strings"), fretless=(35, "strings"),
             mtrumpet=(59, "winds"), trombone=(57, "winds"), asax=(65, "winds"), panflute=(75, "winds"), choir=(52, "strings"),
             warmpad=(89, "strings"), halopad=(94, "strings"), kit=(0, "drums"), brushkit=(40, "drums"))

# 17 Nov: musical styles. The moods (above) decide harmony and rhythm; a style decides what plays it, by swapping each
# instrument for another (None drops it), plus an optional drum part, a tempo factor and how much hall. The same film
# plan therefore sounds like a chamber orchestra one day and a jazz combo, a solo piano or an ambient synth score the
# next. youtube.pick_style() rotates them so no style repeats within the last three films (library.json originals).
STYLES = {
    "orchestral": dict(label="chamber orchestra: strings, piano, woodwinds, horn, timpani", swap={}, bpm=1.0, wet=.22),
    "noir_jazz": dict(label="late-night jazz combo: Rhodes, upright bass, vibraphone, muted trumpet, alto sax, brushes",
                      swap=dict(strings="epiano", fast_strings="epiano", trem="epiano", cello="upbass", bass="upbass", pizz="upbass",
                                clarinet="mtrumpet", oboe="asax", flute="asax", bassoon="trombone", horn="trombone", piano="vibes",
                                harpsichord="vibes", marimba="vibes", celesta="vibes", glock="vibes", timpani=None),
                      kit="brushes", bpm=.9, wet=.16),
    "solo_piano": dict(label="solo piano with a low cello line",
                       swap=dict(strings="piano", fast_strings="piano", trem="piano", cello="cello", bass="cello", pizz="piano",
                                 harpsichord="piano", marimba="piano", celesta="piano", glock="piano", oboe="piano", clarinet="piano",
                                 flute="piano", horn="cello", bassoon="cello", timpani=None),
                       bpm=.88, wet=.26),
    "ambient": dict(label="ambient electronic: warm pads, Rhodes, kalimba, fretless bass, pan flute",
                    swap=dict(strings="warmpad", fast_strings="warmpad", trem="halopad", cello="fretless", bass="fretless", pizz="fretless",
                              piano="epiano", harpsichord="kalimba", marimba="kalimba", oboe="panflute", clarinet="panflute", flute="panflute",
                              horn="choir", bassoon="choir", celesta="musicbox", glock="musicbox", timpani=None),
                    bpm=.85, wet=.3),
    "acoustic": dict(label="acoustic: nylon and steel guitars, upright bass, flute, soft shaker",
                     swap=dict(piano="nylon", harpsichord="steel", marimba="steel", cello="upbass", pizz="upbass", bass="upbass",
                               oboe="flute", clarinet="flute", horn="cello", bassoon="cello", trem="strings", celesta="glock", timpani=None),
                     kit="folk", bpm=1.0, wet=.18),
    "mallets": dict(label="minimalist mallets: marimba, vibraphone, soft pads, electric bass, clarinet",
                    swap=dict(piano="marimba", harpsichord="marimba", strings="warmpad", fast_strings="warmpad", trem="vibes", cello="fbass",
                              pizz="fbass", bass="fbass", oboe="clarinet", flute="clarinet", celesta="vibes", glock="vibes", timpani=None),
                    bpm=1.05, wet=.2),
    "harp": dict(label="harp and celesta with strings and flute",
                 swap=dict(piano="harp", harpsichord="harp", marimba="harp", oboe="flute", clarinet="flute", glock="celesta", timpani=None),
                 bpm=.95, wet=.28),
}


# mood -> (mode, degree progression (one chord per bar; a tuple splits the bar), texture flags)
MOODS = {
    "bustle":   ("major", [1, 5, 6, 4],              dict(arp="harpsichord", bass="pizz", lead="oboe", pulse=2)),
    "explain":  ("major", [1, 6, 4, 5],              dict(arp="piano", pad="strings", bass="cello", pulse=1)),
    "discover": ("major", [4, 1, (2, 5), 6],         dict(pad="strings", bell="celesta", bass="cello", arp="harpsichord", pulse=1)),
    "mystery":  ("minor", [1, 6, 4, 5],              dict(pad="strings", bass="cello", lead="clarinet", pulse=0)),
    "decide":   ("minor", [1, 6, (4, 5), 1],         dict(ost="cello", bass="pizz", pad="strings", timp=1, pulse=2)),
    "peak":     ("minor", [(6, 5)],                    dict(trem="trem", bass="bass", timp=2, horn="horn", pulse=0, unresolved=True)),
    "crash":    ("minor", [1, 6, 2, 5],              dict(trem="trem", ost="cello", timp=1, horn="horn", pulse=2)),
    "reflect":  ("minor", [6, 4, 1, 5],              dict(arp="piano", pad="strings", pulse=0)),
    "resolve":  ("major", [4, 5, 1, 1],              dict(arp="piano", pad="strings", bass="cello", bell="celesta", pulse=1)),
    "quiz":     ("minor", [1, 1, 6, 5],              dict(arp="marimba", bass="pizz", pulse=2, tick=True)),
    "reveal":   ("major", [4, 5, 1],                 dict(pad="strings", bell="glock", bass="cello", pulse=0)),
}


KEYS = ["C", "D", "Eb", "E", "F", "G", "A", "Bb"]


def pick(slug, base_bpm, style=None, key=None, bpm=None, n_avoid=3):
    """17 Nov (Pietro: "experiment with different kinds of music and not always use the same music"). The style, key and
    tempo for one video: never a style or a key used by the last n_avoid scored videos (long films, Shorts, Reels: the
    "originals" in build/music_library/library.json), the tempo moved up to 8% either way; seeded on the slug so a
    re-render keeps its music. Arguments that are given win."""
    import music_library
    rng = random.Random(sum(map(ord, slug)) * 7 + 3)
    past = [o for o in music_library.load().get("originals", []) if o.get("video") != slug]
    past.sort(key=lambda o: (o.get("added", ""), o.get("id", "")))
    recent = past[-n_avoid:]
    used_styles = {o.get("style") or "orchestral" for o in recent}
    used_keys = {o.get("key") for o in recent}
    style = style or rng.choice([k for k in STYLES if k not in used_styles] or list(STYLES))
    key = key or rng.choice([k for k in KEYS if k not in used_keys] or KEYS)
    bpm = bpm or round(base_bpm * rng.uniform(.92, 1.08))
    return dict(style=style, key=key, bpm=bpm, avoided=sorted(used_styles), label=STYLES[style]["label"])

def midi(name):
    """'D4' -> 62."""
    n, o = name[:-1], int(name[-1])
    return 12 * (o + 1) + NOTE[n]


class Score:
    def __init__(self, bpm=80, key="F", seed=1):
        self.bpm, self.key, self.rng = bpm, NOTE[key], random.Random(seed)
        self.events = []                       # (t, dur, instrument, key, vel)
        self.cc = []                           # (t, instrument, cc, value)

    def beat(self, b):
        return b * 60 / self.bpm

    def note(self, instr, key, t, dur, vel=80):
        if 20 <= key <= 108 and dur > 0:
            self.events.append((t, dur, instr, int(key), int(max(1, min(127, vel)))))

    def swell(self, instr, t0, t1, v0, v1, cc=11):
        n = max(2, int((t1 - t0) * 20))
        for i in range(n + 1):
            self.cc.append((t0 + (t1 - t0) * i / n, instr, cc, int(v0 + (v1 - v0) * i / n)))

    def render(self, total, tail=2.5, gain=0.0):
        """Each stem on its own synth; returns {stem: float32 stereo (n, 2)}."""
        import tinysoundfont as tsf
        n = int((total + tail) * SR)
        stems = {}
        for stem in sorted({INSTR[e[2]][1] for e in self.events}):
            syn = tsf.Synth(samplerate=SR, gain=gain)
            sf = syn.sfload(SF)
            chans = {}
            for i, name in enumerate(sorted({e[2] for e in self.events if INSTR[e[2]][1] == stem})):
                if stem == "drums":                               # 17 Nov: a GM drum kit on channel 9
                    chans[name] = 9
                    syn.program_select(9, sf, 0, INSTR[name][0], True)
                    continue
                chans[name] = i if i < 9 else i + 1               # skip channel 9 (drums)
                syn.program_select(chans[name], sf, 0, INSTR[name][0])
                syn.control_change(chans[name], 11, 110)
            q = []
            for t, d, name, k, v in self.events:
                if name in chans:
                    q.append((int(t * SR), 1, chans[name], k, v))
                    q.append((int((t + d) * SR), 0, chans[name], k, 0))
            for t, name, cc, val in self.cc:
                if name in chans:
                    q.append((int(t * SR), 2, chans[name], cc, val))
            q.sort(key=lambda e: (e[0], e[1]))
            out = np.zeros((n, 2), np.float32)
            pos = 0
            syn.start() if False else None
            for at, kind, ch, k, v in q:
                at = min(at, n)
                if at > pos:
                    buf = np.frombuffer(syn.generate(at - pos), dtype=np.float32).reshape(-1, 2)
                    out[pos:at] = buf
                    pos = at
                if kind == 1:
                    syn.noteon(ch, k, v)
                elif kind == 0:
                    syn.noteoff(ch, k)
                else:
                    syn.control_change(ch, k, v)
            if pos < n:
                out[pos:] = np.frombuffer(syn.generate(n - pos), dtype=np.float32).reshape(-1, 2)
            stems[stem] = out
        return stems


def chord(key, mode, degree, octave=4, seventh=False):
    """Scale-degree triad (1-based) as MIDI notes, root position in the given octave."""
    sc = MAJOR if mode == "major" else MINOR
    root = 12 * (octave + 1) + key
    tones = []
    for k in (0, 2, 4) + ((6,) if seventh else ()):
        i = degree - 1 + k
        tones.append(root + sc[i % 7] + 12 * (i // 7))
    if mode == "minor" and degree == 5:                       # harmonic minor: a major dominant
        tones[1] += 1
    return tones


def voice_lead(prev, tones, lo=52, hi=76):
    """Choose the inversion of tones nearest to the previous voicing, inside a range."""
    pcs = sorted({t % 12 for t in tones})
    best, score = None, 1e9
    for base in range(lo, hi - 7):
        v = sorted(min((p + 12 * o for o in range(3, 8) if base <= p + 12 * o <= base + 14), default=0) for p in pcs)
        if 0 in v:
            continue
        s = sum(abs(a - b) for a, b in zip(v, prev)) if prev else abs(sum(v) / len(v) - (lo + hi) / 2)
        if s < score:
            best, score = v, s
    return best


def motif(rng, length=6):
    """A short motif in scale steps (0 = chord root), mostly stepwise, one leap, ends on a chord tone."""
    steps, cur = [], rng.choice([2, 4])
    for i in range(length):
        steps.append(cur)
        mv = rng.choice([-1, 1, 1, -1, 2, -2]) if i != length // 2 else rng.choice([3, -3, 4])
        cur = max(-2, min(8, cur + mv))
    steps[-1] = rng.choice([0, 2, 4])
    return steps


class _Styled(Score):
    """A Score that plays every note on the style's instrument instead (None drops the note)."""
    def __init__(self, bpm, key, seed, swap):
        super().__init__(bpm, key, seed)
        self.swap = swap

    def note(self, instr, key, t, dur, vel=80):
        instr = self.swap.get(instr, instr)
        if instr:
            super().note(instr, key, t, dur, vel)

    def swell(self, instr, t0, t1, v0, v1, cc=11):
        instr = self.swap.get(instr, instr)
        if instr:
            super().swell(instr, t0, t1, v0, v1, cc)


def kit_bar(sc, kit, ta, bl, energy, rng):
    """One bar of drums: brushes (ride, brushed snare on 2 and 4, hi-hat foot) or folk (soft kick, shaker, rim)."""
    q = bl / 4
    if kit == "brushes":
        for b in range(4):
            sc.note("brushkit", 51, ta + b * q, .2, 38 + 8 * energy + rng.randint(-4, 4))          # ride
            sc.note("brushkit", 51, ta + b * q + q * .66, .1, 26 + 6 * energy)                    # the swung skip
            if b % 2:
                sc.note("brushkit", 38, ta + b * q, .2, 30 + 10 * energy)                          # brushed snare
                sc.note("brushkit", 44, ta + b * q, .1, 34)                                        # hi-hat foot
    elif kit == "folk":
        sc.note("kit", 36, ta, .2, 46 + 10 * energy)
        sc.note("kit", 36, ta + 2 * q + q * .5, .2, 34 + 8 * energy)
        for e in range(8):
            sc.note("kit", 70, ta + e * q / 2, .08, (30 if e % 2 else 42) + 6 * energy + rng.randint(-3, 3))   # shaker
        if energy > 1:
            sc.note("kit", 37, ta + q, .1, 40)
            sc.note("kit", 37, ta + 3 * q, .1, 40)


def compose(sections, key="F", bpm=80, seed=1, level=1.0, style="orchestral"):
    """sections: [(t0, t1, mood)] in film seconds. Returns the rendered stems and the Score (for logs).
    style: a STYLES name (17 Nov); "orchestral" is the 13 to 16 Nov sound."""
    rng = random.Random(seed)
    sty = STYLES[style]
    bpm = bpm * sty.get("bpm", 1.0)
    sc = _Styled(bpm, key, seed, sty["swap"])
    sc.style = style
    kk = NOTE[key]
    bar = sc.beat(4)
    mot = motif(rng)
    prev = None
    for si, (t0, t1, mood) in enumerate(sections):
        mode, prog, tex = MOODS[mood]
        scale = MAJOR if mode == "major" else MINOR
        # a minor section in a major key uses the relative minor; a major one in a minor key the relative major
        sk = kk if mode == "major" else (kk + 9) % 12
        nbars = max(1, round((t1 - t0) / bar))
        bl = (t1 - t0) / nbars                                # stretch bars so sections meet shot cuts exactly
        b8 = bl / 8
        for b in range(nbars):
            if sty.get("kit") and tex.get("pulse", 1) >= 1:
                kit_bar(sc, sty["kit"], t0 + b * bl, bl, tex.get("pulse", 1), rng)
            deg = prog[b % len(prog)]
            halves = deg if isinstance(deg, tuple) else (deg,)
            for hi_, d in enumerate(halves):
                ta = t0 + b * bl + hi_ * bl / len(halves)
                dur = bl / len(halves)
                tones = chord(sk, mode, d, 3)
                v = voice_lead(prev, tones)
                prev = v
                last = (b == nbars - 1 and hi_ == len(halves) - 1)
                fade = (si == len(sections) - 1 and tex.get("unresolved") and last)
                if tex.get("pad"):
                    for k in v:
                        sc.note(tex["pad"], k, ta, dur + .08, 58 + 8 * (b % 2))
                if tex.get("trem"):
                    for k in v + [v[0] + 12]:
                        sc.note(tex["trem"], k, ta, dur + .05, 64)
                    sc.swell(tex["trem"], ta, ta + dur, 70, 120 if not fade else 105)
                if tex.get("bass"):
                    root = 12 * 3 + sk + scale[(d - 1) % 7] + (1 if mode == "minor" and d == 5 and False else 0)
                    root = root - 12 if root > 50 else root
                    if tex["bass"] == "pizz":
                        for q in range(0, 8, 2):
                            sc.note("pizz", root + (12 if q == 4 else 0), ta + q * b8 * (len(halves) and 1 / len(halves)), .3, 86 if q == 0 else 70)
                    else:
                        sc.note(tex["bass"], root, ta, dur + .05, 72)
                if tex.get("arp"):
                    inst = tex["arp"]
                    pat = [0, 1, 2, 1, 2, 3, 2, 1] if rng.random() < .5 else [0, 2, 1, 2, 3, 2, 1, 2]
                    pool = v + [v[0] + 12]
                    steps = int(8 / len(halves)) if tex.get("pulse", 1) >= 1 else 4
                    for q in range(steps):
                        k = pool[pat[q % len(pat)] % len(pool)]
                        step = dur / steps
                        sc.note(inst, k + (12 if inst in ("harpsichord", "marimba") else 0), ta + q * step, step * .95,
                                (78 if q % 2 == 0 else 62) + rng.randint(-4, 4))
                if tex.get("ost"):
                    root = 12 * 3 + sk + scale[(d - 1) % 7]
                    for q in range(int(8 / len(halves))):
                        k = root + (7 if q % 4 == 2 else 0) + (12 if q % 8 == 4 else 0)
                        sc.note(tex["ost"], k - 12 if k > 55 else k, ta + q * b8, b8 * .9, 84 if q % 2 == 0 else 66)
                if tex.get("tick"):
                    for q in range(int(8 / len(halves))):
                        sc.note("pizz", 12 * 6 + sk, ta + q * b8, .12, 70 if q % 2 == 0 else 50)
                if tex.get("timp"):
                    root = 12 * 2 + sk + scale[(d - 1) % 7]
                    root = root + 12 if root < 36 else root
                    if tex["timp"] == 2 and last:
                        n = int(dur / .09)
                        for q in range(n):                        # a roll that grows
                            sc.note("timpani", root, ta + q * .09, .1, int(40 + 70 * q / n))
                    elif hi_ == 0:
                        sc.note("timpani", root, ta, .6, 64)
                if tex.get("horn") and hi_ == 0:
                    sc.note("horn", v[0] - 12 if v[0] > 60 else v[0], ta, dur * len(halves), 60)
                    sc.swell("horn", ta, ta + dur * len(halves), 60, 110)
                if tex.get("bell") and hi_ == 0 and b % 2 == 0:
                    sc.note(tex["bell"], v[-1] + 12, ta + bl * .5, 1.2, 60)
                if tex.get("pad") and fade:
                    sc.swell(tex["pad"], ta, ta + dur, 100, 125)
            # the motif: stated in the first lead section, answered (inverted, lower) later
            if tex.get("lead") and b % 2 == 0 and nbars > 1:
                root = 12 * 5 + sk
                mm = mot if (si % 2 == 0) else [m - 2 for m in reversed(mot)]
                for q, st in enumerate(mm):
                    k = root + scale[st % 7] + 12 * (st // 7)
                    sc.note(tex["lead"], k, t0 + b * bl + q * bl / 4, bl / 4 * .92, 74 if q == 0 else 64)
    stems = sc.render(sections[-1][1])
    return {k: v * level for k, v in stems.items()}, sc


def hall(x, seconds=1.9, wet=.22, seed=2, pre=.022):
    """A synthetic stereo hall: decorrelated decaying noise as the impulse response, darkened over time."""
    from scipy.signal import fftconvolve, butter, lfilter
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    env = np.exp(-6.9 * t / seconds)
    ir = np.zeros((n + int(pre * SR), 2), np.float32)
    for c in range(2):
        noise = rng.standard_normal(n) * env
        b, a = butter(1, 5200 / (SR / 2), "low")
        dark = lfilter(b, a, noise)
        mixk = np.clip(t / seconds * 2, 0, 1)
        ir[int(pre * SR):, c] = (noise * (1 - mixk) + dark * mixk) * .02
    out = np.zeros((len(x) + len(ir) - 1, 2), np.float32)
    for c in range(2):
        out[:, c] = fftconvolve(x[:, c], ir[:, c])
    y = np.zeros_like(out)
    y[:len(x)] = x * (1 - wet)
    return (y + out * wet / max(np.abs(out).max(), 1e-9) * np.abs(x).max() * 1.6)[:len(x) + int(.0 * SR)]


def master_music(stems, balance=None, wet=.22):
    """Balance the stems, add the hall, return one stereo music stem (peak about -6 dBFS)."""
    balance = balance or dict(strings=1.0, keys=.85, winds=.8, perc=.7, drums=.6)
    n = max(len(v) for v in stems.values())
    mix = np.zeros((n, 2), np.float32)
    for k, v in stems.items():
        mix[:len(v)] += v * balance.get(k, 1.0)
    mix = hall(mix, wet=wet)
    # 17 Nov: styles differ a lot in density (solo piano vs a soft acoustic bed), so normalise by loudness (RMS 0.08,
    # what the orchestral palette had at a 0.5 peak) instead of by peak, keeping the peak at 0.9 at most; the music
    # then sits about as far under the voice whatever the style.
    rms = float(np.sqrt(np.mean(mix[np.abs(mix).mean(1) > 1e-5] ** 2))) if np.any(np.abs(mix) > 1e-5) else 1e-9
    g = min(.08 / max(rms, 1e-9), .9 / max(np.abs(mix).max(), 1e-9))
    return (mix * g).astype(np.float32)
