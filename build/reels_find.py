"""
"Find the error": a voiced suspense Reel.

Built on what made the balloon Reel work (a countdown, waiting, a payoff held
back) but the viewer plays: one number on an income statement is wrong, and
they get ten seconds to find it before the reveal.

The statement is consistent except for one cell. Depreciation rises by 10:
  before: EBITDA 50, D&A 10, EBIT 40, tax at 25% 10.0, net income 30
  after:  EBITDA 50, D&A 20, EBIT 30, tax at 25%  7.5, net income 22.5
The screen shows 20 for net income after. That is the error: 20 ignores the
tax shield of 2.5 (25% of the extra 10).

Voice: Kokoro af_heart via build/voice.py. Captions are burned in, word by
word, because most people watch muted.

    KOKORO_DIR=/path/to/kokoro python build/reels_find.py [voice]
"""

import base64
import io
import json
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image

from motion import A, build, OUT
from reels_motion import ch, SHADOW
from voice import Voice, write_wav, SR

RED, TEAL, INK = "#D93A12", "#5EC8B4", "#0A0A0A"
SLUG = "w1-find-the-error"

# (id, text, colours for key words, where it shows: cap = caption bar, big = centre)
LINES = [
    ("a1", "One number on this screen is wrong.", {"wrong": RED}, "cap"),
    ("a2", "Interviewers hide it on purpose.", {}, "cap"),
    ("a3", "You have ten seconds.", {"ten": RED, "seconds": RED}, "cap"),
    ("a4", "Go.", {"go": RED}, "cap"),
    ("c1", "Look at every line.", {}, "cap"),
    ("n3", "Three.", {}, "none"), ("n2", "Two.", {}, "none"), ("n1", "One.", {}, "none"),
    ("c2", "Time.", {"time": RED}, "cap"),
    ("b1", "Revenue is fine. EBITDA is fine.", {}, "cap"),
    ("b2", "But depreciation went up by ten.", {"ten": TEAL}, "cap"),
    ("b3", "So EBIT falls by ten.", {}, "cap"),
    ("b4", "And tax falls too. Twenty five percent of ten, two and a half.", {"tax": TEAL, "two": TEAL, "and": None, "half": TEAL}, "cap"),
    ("b5", "So net income falls by seven and a half, not ten.", {"seven": TEAL, "not": RED, "ten": RED}, "cap"),
    ("b6", "It should be twenty two and a half. That's the tax shield.", {"shield": TEAL}, "cap"),
    ("e1", "If you caught it, you're ready.", {"ready": TEAL}, "big"),
    ("e2", "If you didn't, that's okay. Now you are.", {"now": TEAL, "you": None, "are": TEAL}, "big"),
    ("e3", "Follow for two questions a day.", {"follow": RED}, "big"),
]

GAP, SECTION = .28, .55
COUNT = 10.0


def synth(voice_name):
    v = Voice(voice_name, speed=1.0)
    clips, words = {}, {}
    for key, text, _, _ in LINES:
        clips[key] = v.say(text)
        # Word timings inside the phrase, proportional to phoneme length.
        toks = text.replace(",", "").replace(".", "").split()
        lens = [max(len(v.phonemes(t)), 1) for t in toks]
        dur = len(clips[key]) / SR
        acc, ts = 0, []
        for n in lens:
            ts.append(round(dur * acc / sum(lens), 3))
            acc += n
        words[key] = list(zip(text.split(), ts))
    return clips, words


def timeline(clips):
    d = {k: len(a) / SR for k, a in clips.items()}
    t, at = .25, {}
    for k in ("a1", "a2", "a3", "a4"):
        at[k] = t
        t += d[k] + (GAP if k != "a3" else .45)
    count0 = at["a4"] + .1                       # the countdown starts on "Go"
    at["c1"] = count0 + 3.2
    for k, n in (("n3", 7), ("n2", 8), ("n1", 9)):
        at[k] = count0 + n
    at["c2"] = count0 + COUNT
    t = at["c2"] + d["c2"] + SECTION
    for k in ("b1", "b2", "b3", "b4", "b5", "b6"):
        at[k] = t
        t += d[k] + GAP + (.15 if k in ("b4", "b5") else 0)
    t += SECTION - GAP
    for k in ("e1", "e2", "e3"):
        at[k] = t
        t += d[k] + GAP + .2
    total = t + 1.4
    return at, d, count0, total


def soundtrack(clips, at, count0, total, reveal_at):
    n = int(total * SR) + SR
    mix = np.zeros(n, dtype=np.float32)

    def put(sig, t, gain=1.0):
        i = int(t * SR)
        mix[i:i + len(sig)] += sig[: max(0, n - i)] * gain

    for k, a in clips.items():
        put(a, at[k])
    tt = np.arange(int(.05 * SR)) / SR
    tick = (np.sin(2 * np.pi * 1900 * tt) * np.exp(-tt * 70)).astype(np.float32)
    for k in range(int(COUNT)):
        put(tick, count0 + k, .22 if k < 7 else .34)
    tt = np.arange(int(.5 * SR)) / SR
    thud = (np.sin(2 * np.pi * 62 * tt) * np.exp(-tt * 7)).astype(np.float32)
    put(thud, count0 + COUNT, .55)
    tt = np.arange(int(1.0 * SR)) / SR
    ding = ((np.sin(2 * np.pi * 1318.5 * tt) + .5 * np.sin(2 * np.pi * 1975.5 * tt)) * np.exp(-tt * 4.5)).astype(np.float32)
    put(ding, reveal_at + .62, .16)
    # Loudness: lift the voice to a consistent level, then keep peaks safe.
    voice_rms = np.sqrt(np.mean(np.concatenate(list(clips.values())) ** 2))
    mix *= .12 / max(voice_rms, 1e-6)
    peak = np.abs(mix).max()
    if peak > .95:
        mix *= .95 / peak
    return mix


def noise_tile():
    rng = np.random.default_rng(7)
    a = (rng.random((170, 170)) * 255).astype(np.uint8)
    img = Image.fromarray(a, "L").resize((512, 512), Image.BILINEAR)
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def caption(key, text, cols, words, start, dur, big=False, hold=None):
    spans = []
    for w, t in words:
        bare = w.strip(".,").lower()
        c = cols.get(bare)
        cattr = f' data-c="{c}"' if c else ""
        spans.append(f'<span class="w" data-t="{t}"{cattr}>{w}</span>')
    inner = " ".join(spans)
    if big:
        return A(A(f'<div class="num" style="font-size:96px;line-height:1.1">{inner}</div>', "kara", start, dur),
                 "life", start - .1, hold or dur + .55, fo=.01 if hold else .3,
                 style="position:absolute;left:0;right:0;top:470px;text-align:center;z-index:8")
    begin = -1 if key == "a1" else start - .05       # the first line is on screen at frame 0
    return A(A(f'<div style="font-size:50px;font-weight:600;line-height:1.25">{inner}</div>', "kara", start, dur),
             "life", begin, dur + .35 + (start - begin - .05), fi=.12, fo=.15,
             style="position:absolute;left:0;right:0;top:1060px;text-align:center;z-index:8;"
                   "text-shadow:0 2px 14px rgba(0,0,0,.8)")


def scene(clips, words, at, d, count0, total):
    T = lambda k: at[k]
    reveal_at = T("b6")                              # 22.5 appears as she says it
    rows = [("Revenue", "100", "100"), ("EBITDA", "50", "50"), ("Depreciation", "10", "20"),
            ("EBIT", "40", "30"), ("Tax at 25%", "10.0", "7.5"), ("Net income", "30", "20")]
    card_top = 590                                   # frame y
    head, rh = 100, 92
    row_y = [card_top + head + rh * i + rh / 2 for i in range(len(rows))]
    end_card = T("e1") - .2

    # Focus bars on rows during the reveal.
    focus = [(0, "b1", d["b1"] * .5, "rgba(255,255,255,.07)"), (1, "b1", d["b1"], "rgba(255,255,255,.07)"),
             (2, "b2", d["b2"], "rgba(255,255,255,.1)"), (3, "b3", d["b3"], "rgba(255,255,255,.1)"),
             (4, "b4", d["b4"], "rgba(94,200,180,.18)"), (5, "b5", d["b5"] + d["b6"] + .6, "rgba(217,58,18,.2)")]
    bars = ""
    for i, k, dur, col in focus:
        start = T(k) + (d["b1"] * .5 if (k == "b1" and i == 1) else 0)
        bars += A("", "life", start, dur + .2, fi=.2, fo=.25,
                  style=f"position:absolute;left:-20px;right:-20px;top:{head + rh * i}px;height:{rh}px;"
                        f"background:{col};border-radius:14px")

    def row(i, label, b, a):
        after = a
        if i == 5:
            # The wrong 20 carries its own pen circle and strike, and leaves with them;
            # 22.5 then lands clean in teal.
            wrong = (f'<span style="position:relative;display:inline-block">{a}'
                     + '<svg class="a pen" data-fx="draw" data-at="' + str(round(T("b5") + .4, 2))
                     + '" data-d=".55" width="0" height="0" style="position:absolute;left:0;top:0"></svg>'
                     + A("", "strike", reveal_at, .3, style=f"position:absolute;left:-8px;right:-8px;top:50%;height:7px;"
                         f"background:{RED};border-radius:4px") + '</span>')
            after = (A(wrong, "life", -1, reveal_at + 1.6, fo=.25, style="display:inline-block")
                     + A(f'<span style="color:{TEAL};text-shadow:0 0 24px rgba(94,200,180,.45)">22.5</span>',
                         "pop", reveal_at + .62, .45, style="position:absolute;right:0;top:0"))
        return (f'<div style="position:relative;display:grid;grid-template-columns:1fr 180px 180px;align-items:center;'
                f'height:{rh}px;border-bottom:1px solid rgba(255,255,255,.08)">'
                f'<span style="font-size:42px;font-weight:500;opacity:.9">{label}</span>'
                f'<span class="num" style="font-size:58px;text-align:right;opacity:.75">{b}</span>'
                f'<span class="num" style="font-size:58px;text-align:right"><span style="position:relative;display:inline-block">{after}</span></span></div>')

    card = (f'<div style="position:relative;background:linear-gradient(180deg,#171a1c,#101213);border:2px solid rgba(255,255,255,.12);'
            f'border-radius:28px;padding:0 34px 18px;box-shadow:0 40px 90px rgba(0,0,0,.6)">'
            f'<div style="position:relative">{bars}'
            f'<div style="display:grid;grid-template-columns:1fr 180px 180px;align-items:end;height:{head}px;'
            f'border-bottom:2px solid rgba(255,255,255,.18);padding-bottom:14px;box-sizing:border-box">'
            f'<span style="font-size:24px;font-weight:600;letter-spacing:.14em;opacity:.6">INCOME STATEMENT, $M</span>'
            f'<span style="font-size:24px;font-weight:600;letter-spacing:.14em;opacity:.6;text-align:right">BEFORE</span>'
            f'<span style="font-size:24px;font-weight:600;letter-spacing:.14em;text-align:right;color:{TEAL}">AFTER<br>'
            f'<span style="opacity:.8">D&amp;A +10</span></span></div>'
            + "".join(row(i, *r) for i, r in enumerate(rows)) + '</div></div>')
    card = A(card, "life", -1, end_card + 1, fi=.5, fo=.4,
             style=f"position:absolute;left:0;right:0;top:{card_top - 230}px;z-index:4")

    # Countdown ring and number above the card.
    ring = (f'<svg width="190" height="190" viewBox="0 0 190 190" style="display:block">'
            f'<circle cx="95" cy="95" r="84" fill="rgba(0,0,0,.35)" stroke="rgba(255,255,255,.14)" stroke-width="9"/>'
            f'</svg>'
            f'<svg class="a" data-fx="draw" data-lin="1" data-at="{count0}" data-d="{COUNT}" width="190" height="190" viewBox="0 0 190 190" '
            f'style="position:absolute;left:0;top:0;transform:rotate(-90deg)">'
            f'<path d="M95 11 a84 84 0 1 1 -0.01 0" fill="none" stroke="{RED}" stroke-width="9" stroke-linecap="round" '
            f'transform="rotate(90 95 95)"/></svg>')
    number = A(A("10", "count", count0, COUNT, cls="num",
                 style="font-size:96px;line-height:1",
                 **{"from": COUNT, "to": 0, "lin": 1, "pad": 1, "ceil": 1, "pre": "", "suf": "", "show": 1}),
               "beat", count0, 1, n=int(COUNT), style="display:inline-block")
    countdown = A(f'<div style="position:relative;width:190px;height:190px;margin:0 auto">{ring}'
                  f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">{number}</div></div>',
                  "life", T("a3") - .1, count0 + COUNT + 1.0 - (T("a3") - .1), fi=.35, fo=.4,
                  style="position:absolute;left:0;right:0;top:120px;z-index:6")

    hud = A('<div style="display:flex;justify-content:space-between;font-size:26px;font-weight:600;letter-spacing:.12em">'
            f'<span><span style="color:{RED}">&#9679;</span> FIND THE ERROR</span>'
            '<span>ERRORS FOUND '
            + A("0", "count", reveal_at + .3, .2, style="display:inline",
                **{"from": 0, "to": 1, "lin": 1, "pad": 1, "pre": "", "suf": "", "show": 1})
            + '/1</span></div>', "life", -1, end_card + 1, fo=.4, style="position:absolute;left:0;right:0;top:0;z-index:7")

    # Spotlight: searching during the countdown, then walking the explanation.
    def spot(y, x=540):
        return [x - 450, y - 450]
    keys = [[0, *spot(row_y[2]), 1, .0]]
    keys.append([count0 - .2, *spot(row_y[0]), 1, .9])
    path = [row_y[3], row_y[1], row_y[5], row_y[0], row_y[4], row_y[2], row_y[5], row_y[3]]
    for j, y in enumerate(path):
        keys.append([count0 + .4 + j * 1.2, *spot(y, 540 + (-140 if j % 2 else 140)), 1.05, .9])
    for k, i in (("b1", 0), ("b2", 2), ("b3", 3), ("b4", 4), ("b5", 5)):
        keys.append([T(k), *spot(row_y[i]), .9, 1])
    keys.append([end_card, *spot(row_y[5]), .9, 0])
    spotlight = A("", "kf", 0, 1, kf=json.dumps([[round(a, 3) for a in k] for k in keys]),
                  style="position:absolute;left:0;top:0;width:900px;height:900px;border-radius:50%;"
                        "background:radial-gradient(circle,rgba(255,236,214,.15),rgba(255,236,214,0) 62%);"
                        "mix-blend-mode:screen")

    grain = A("", "grain", 0, 1, op=.06, fps=12,
              style=f"position:absolute;left:0;top:0;width:1300px;height:2150px;background:url({noise_tile()});"
                    "mix-blend-mode:overlay")
    vignette = ('<div style="position:absolute;inset:0;background:radial-gradient(ellipse 75% 60% at 50% 45%,'
                'rgba(0,0,0,0),rgba(0,0,0,.65))"></div>')
    art = (f'<div class="nochk" style="position:absolute;left:-84px;top:-230px;width:1080px;height:1920px;z-index:2;'
           f'pointer-events:none;overflow:hidden">{spotlight}</div>')
    over = (f'<div class="nochk" style="position:absolute;left:-84px;top:-230px;width:1080px;height:1920px;z-index:9;'
            f'pointer-events:none;overflow:hidden">{vignette}{grain}</div>')

    caps = "".join(caption(k, txt, cols, words[k], T(k), d[k], big=(where == "big"), hold=(total + 2 if k == "e3" else None))
                   for k, txt, cols, where in LINES if where != "none")
    # The last line holds the brand under it.
    brand = A(f'<div style="text-align:center"><div class="num" style="font-size:150px;line-height:1">IB<span style="color:{RED}">.</span></div>'
              '<div style="font-size:26px;font-weight:600;letter-spacing:.24em;opacity:.75;margin-top:14px">INVESTMENT BANKING INTERVIEWS</div></div>',
              "rise", T("e3") + .2, .5, style="position:absolute;left:0;right:0;top:760px;z-index:8")
    return dict(dur=total, push=.03, html=art + hud + countdown + card + caps + brand + over), reveal_at


def main(voice_name="af_heart"):
    clips, words = synth(voice_name)
    at, d, count0, total = timeline(clips)
    sc, reveal_at = scene(clips, words, at, d, count0, total)
    mp4, cover, problems = build(SLUG + "-silent", [sc], theme="ink", cover_at=at["a4"] - .08, crf=20)
    audio = soundtrack(clips, at, count0, total + .6, reveal_at)
    work = OUT / SLUG
    work.mkdir(parents=True, exist_ok=True)
    wav = work / "voice.wav"
    write_wav(wav, audio)
    final = work / f"{SLUG}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-i", str(wav), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                    "-movflags", "+faststart", str(final)], check=True)
    (work / "cover.jpg").write_bytes(pathlib.Path(cover).read_bytes())
    json.dump({"at": at, "dur": d, "count0": count0, "total": total, "voice": voice_name},
              open(work / "timeline.json", "w"), indent=1)
    print(f"  -> {final.name}  {total:.1f}s  voice {voice_name}")
    return final


if __name__ == "__main__":
    main(*(sys.argv[1:2] or []))
