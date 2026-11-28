"""
Reel, 28 Nov 2026 (slot A, 12:30 ET): $10,000 at 8% a year, how long until it doubles? The third full-frame Reel and
the first on the home desk set (reel_film.home_desk, 28 Nov), the same day as the trading floor (slot B).

Narrator: voice_clone.narrator(), EMMA (Kokoro bf_emma, 0.97) from 27 Nov to 4 Dec (Pietro, 27 Nov). No subtitles.
The follow ask said in the last line and shown. Voice and effects only in the file: the music is a trending licensed
track Instagram attaches at posting. The analyst, her flat and the amounts are invented (an example, not advice).

Every number worked (8% a year, paid once a year, reinvested; checked in _check()):
    Wrong answer (simple interest): 8% of $10,000 = $800 a year; $10,000 more takes 10,000 / 800 = 12.5 years
    Year 1: 10,000 x 1.08 = 10,800 (+800)
    Year 2: 10,800 x 1.08 = 11,664 (+864: interest on the interest)
    Years 3 to 9: 12,597.12, 13,604.89, 14,693.28, 15,868.74, 17,138.24, 18,509.30, 19,990.05
    After 9 years: 10,000 x 1.08^9 = 19,990.05, just under $20,000 (exact doubling time ln 2 / ln 1.08 = 9.006 years)
    Rule of 72 (a standard approximation, not a statistic): 72 / 8 = 9
Close (asked, not answered): 6% a year: 72 / 6 = 12 years (1.06^12 = 2.012).
Comment bonus: 12% a year: 72 / 12 = 6 years (1.12^6 = 1.974, a little under double).

Hook candidates (28 Nov, scored 1 to 5 on clash, number early, second person, length, send-to-a-friend):
    1. "$10,000 at 8%. How long to double?"                          clash 3, number 5, you 3, length 5, send 5 = 21
    2. "8% a year. Not 12.5 years to double."                         gives half the answer early
    3. "$800 a year. So 12.5 years to double? No."                    clash 5, number 5, you 2, length 4, send 4 = 20
    4. "Your $10,000 doubles in 9 years, not 12.5."                   gives the answer in 2 s (the standard forbids)
    5. "Answer before she does: 8%, how long to double?"              clash 2, number 4, you 4, length 4, send 3 = 17
Chosen: 1, with the wrong answer struck in the next beat.

Story (docs/production/reel-film-standard.md): a first bonus at stake; the wrong answer (divide: 12.5 years) struck;
the mechanism drawn on her screen as it is said (year bars, each adding a little more); the payoff in one number
(9 years, the year 9 bar touching $20,000); the shortcut (72 / 8); the question back (6%) and the follow ask.

    python3 build/reelf_doubling.py            stills (fast look)
    python3 build/reelf_doubling.py render     the Reel, its clean master and checks
"""

import json
import math
import sys

import cine as C
from reel_film import (W, H, lay, cam_x, cam_y, shot, hook, narration, beats, at_word, captions, home_desk,
                       marker_text, film, full_frame_check, sound, follow_ask, INK, RED, TEAL, MUSTARD, GREEN, _r)

SLUG = "w3-doubling-72"
LINES = [
    "Her first bonus: ten thousand dollars, invested at eight percent a year. How long until it doubles?",
    "Most people divide. Eight hundred a year, so twelve and a half years. That's wrong.",
    "The eight percent is paid on the growing balance. Year one adds eight hundred. Year two adds eight sixty-four.",
    "Every year the interest earns interest, so each year adds a little more than the last.",
    "After nine years, not twelve and a half, she has just under twenty thousand dollars.",
    "The shortcut is to divide seventy-two by the rate. Seventy-two over eight is nine.",
    "Your turn: at six percent, how long does it take to double? Tell me in the comments, "
    "and follow for a new interview question every day.",
]
HOLDS = {4: .5}

C.LOOKS["analyst_f"] = {'coat': '#7A3B4A', 'coat2': '#5E2D39', 'vest': '#F7F5F2', 'legs': '#2B2F3A', 'stock': '#2B2F3A',
                        'shoe': '#0A0A0A', 'skin': '#F1CBAA', 'hair': '#5A3A28', 'hat': '', 'style': 'dress', 'cuff': '#F7F5F2'}
LOOK = "analyst_f"
HX = 800
VALS = [10000 * 1.08 ** y for y in range(10)]


def _check():
    assert round(VALS[1], 2) == 10800 and round(VALS[2], 2) == 11664 and round(VALS[9], 2) == 19990.05
    assert 10000 / 800 == 12.5 and 72 / 8 == 9 and 72 / 6 == 12 and 72 / 12 == 6
    assert abs(math.log(2) / math.log(1.08) - 9.006) < .001


_check()
FLOOR, ANC = home_desk(hero_x=HX)
SX, SY, SW, SH = ANC["screen"]
BASE = SY + SH - 44
PX = 0.0075                       # screen px per dollar: $20,000 = 150 px (numbers sit above the chart)
X0, XSTEP, BWID = SX + 34, 24, 16 # year 0 at X0, one year per 24 px, years 0 to 13 on the axis


def floor_layers(screen_svg, trader, thought="", extra=""):
    z = {k: v[0] for k, v in FLOOR.items()}
    layers = [lay(z["wall"], FLOOR["wall"][1]), lay(z["row"], FLOOR["row"][1]), lay(z["floor"], FLOOR["floor"][1]),
              lay(z["chair"], FLOOR["chair"][1]), lay(.8, trader["svg"]), lay(.82, thought),
              lay(z["desk"], FLOOR["desk"][1] + screen_svg)]
    if extra:
        layers.append(lay(1.2, extra))
    return layers


_N = [0]


def trader(pose=None):
    """A new id per shot (the runtime animates the first element with an id)."""
    _N[0] += 1
    seat = lambda name, **o: C.pose("seated", **{**C.POSES.get(name, {}), **o})
    p = pose or [[0, seat("relaxed", head=-4)]]
    return C.actor(f"tr{_N[0]}", LOOK, pos=[[0, HX, 1060]], pose_keys=p, dir=1, walk=False, seed=3, scale=1.0)


def seat(name, **o):
    return C.pose("seated", **{**C.POSES.get(name, {}), **o})


def T(x, y, text, size, fill=INK, anchor="start", weight=700, family="Sans", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="\'{family}\',sans-serif" font-weight="{weight}" font-size="{size}" '
            f'text-anchor="{anchor}" fill="{fill}" {extra}>{text}</text>')


def fade(t, d=.25):
    return C.kv(opacity=[[0, 0], [t, 0], [t + d, 1]])


def header(text="HER BONUS"):
    return T(SX + 22, SY + 40, text, 24, INK, weight=700, extra='letter-spacing="3"') + \
        f'<path d="M{SX + 22},{SY + 56} L{SX + SW - 22},{SY + 56}" stroke="{INK}" stroke-width="2.4"/>'


def ytop(v):
    return BASE - v * PX


def xyear(y):
    return X0 + y * XSTEP


def counter(c0, c1, ta, x=None, y=None, size=64, color=INK, d=.9):
    x = x or SX + SW - 30
    y = y or SY + 130
    return (f'<text x="{x}" y="{y}" font-family="\'Serif\',serif" font-weight="700" font-size="{size}" text-anchor="end" '
            f'fill="{color}" data-pre="$" data-dec="0" {C.kv(count=[[0, c0], [ta, c0], [ta + d, c1, "lin"]])}>${c0:,}</text>')


def baseline():
    return f'<path d="M{SX + 30},{BASE} L{SX + SW - 30},{BASE}" stroke="{INK}" stroke-width="3"/>'


def cam_screen(zoom, dx=0, dy=0):
    return cam_x(SX + SW / 2 + dx, .86), cam_y(SY + SH / 2 + dy, .86), zoom


def target_line(op=.6):
    y = ytop(20000)
    return (f'<path d="M{SX + 24},{y} L{SX + SW - 24},{y}" stroke="{INK}" stroke-width="3" stroke-dasharray="10 9" opacity="{op}"/>'
            + T(SX + 30, y + 26, "$20,000", 22, INK, weight=700, extra=f'opacity="{op}"'))


def ybar(y, t=None, fill=TEAL, d=.35):
    v = VALS[y]
    r = f'<rect x="{xyear(y) - BWID / 2}" y="{ytop(v):.1f}" width="{BWID}" height="{v * PX:.1f}" fill="{fill}" stroke="{INK}" stroke-width="2.2"/>'
    if t is None:
        return r
    return f'<g {C.kv(clip=[[0, 100, 0, 0, 0], [t, 100, 0, 0, 0], [t + d, 0, 0, 0, 0, "out"]])}>{r}</g>'


def axis(upto=13, labels=(0, 5, 9)):
    s = baseline()
    for y in labels:
        s += T(xyear(y), BASE + 28, f"Y{y}", 20, INK, anchor="middle", weight=600, extra='opacity=".75"')
    return s


def simple_line(t0, t1, op=1.0):
    """The wrong answer: the same $800 every year, a straight line that reaches $20,000 only at 12.5 years."""
    x1, y1 = xyear(12.5), ytop(20000)
    return (f'<path d="M{xyear(0)},{ytop(10000)} L{x1},{y1}" stroke="{RED}" stroke-width="5" stroke-dasharray="6 8" fill="none" opacity="{op}" '
            f'{C.kv(dash=[[0, 0], [t0, 0], [t1, 1, "inout"]])}/>')


def s0(b, d):
    t_ten = at_word(b, 0, "ten", 0)
    t_eight = at_word(b, 0, "eight", 0)
    t_dbl = at_word(b, 0, "doubles?", 0)
    tr = trader([[0, seat("relaxed", head=-2)], [t_eight, seat("relaxed", head=-6, brow=.6)], [t_dbl, seat("concern", head=4, lean=8)],
                 [d, seat("concern", head=6, lean=8)]])
    s = header() + axis(labels=()) + target_line(0) 
    s += f'<g {fade(t_ten)}>' + ybar(0) + T(SX + 30, SY + 125, "$10,000", 58, INK, family="Serif") + '</g>'
    s += T(SX + SW - 30, SY + 125, "8%", 58, TEAL, anchor="end", family="Serif", extra=fade(t_eight))
    s += f'<g {fade(t_dbl)}>' + target_line(.7) + T(SX + SW - 30, SY + 210, "x2 in ? years", 34, RED, anchor="end", family="Serif") + '</g>'
    layers = floor_layers(s, tr)
    cam = [[0, cam_x(HX + 225, .8), cam_y(690, .8), .9], [t_eight, *cam_screen(1.3, -60, 30), "inout"], [d, *cam_screen(1.45, -40, 20), "sine"]]
    over = [hook([[("$10,000", True), (" at ", False), ("8%.", True)], [("How long", False)], [("to ", False), ("double?", True)]], at=0,
                 d=max(2.6, t_eight + .3), top=230, size=120)]
    fx = [("paper", .1, .25, 0, dict(sec=.3, crisp=.6)), ("hit", t_ten, .3, 0, dict(pitch=196)), ("tap", t_eight, .3, 0, dict()), ("hit", t_dbl, .35, 0, dict(pitch=330))]
    return shot(d, layers, [tr], cam, over), fx


def s1(b, d):
    t_div = at_word(b, 1, "divide.", 1)
    t_wrong = at_word(b, 1, "wrong.", 1)
    tr = trader([[0, seat("relaxed", head=0, mouth=1, brow=.5)], [t_div, seat("shrug", mouth=1, brow=.8)],
                 [t_wrong, seat("concern")], [d, seat("concern", head=8)]])
    tx, ty = HX - 10, 590
    thought = (f'<g {C.kv(opacity=[[0, 0], [t_div - .1, 0], [t_div + .2, 1]], translate=[[0, tx, ty + 20, 0, .42], [t_div - .1, tx, ty + 20, 0, .42], [t_div + .35, tx, ty, 0, .55, "out"]])}>'
               f'<circle cx="-40" cy="190" r="12" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="-20" cy="150" r="20" fill="#fff" stroke="{INK}" stroke-width="4"/>'
               f'<rect x="-210" y="-100" width="420" height="220" rx="96" fill="#fff" stroke="{INK}" stroke-width="5"/>'
               + T(0, -28, "$10,000 \u00f7 800", 40, INK, anchor="middle", family="Serif")
               + T(0, 64, "= 12.5 yrs", 72, INK, anchor="middle", family="Serif")
               + f'<path d="M-170,46 L170,6" stroke="{RED}" stroke-width="16" stroke-linecap="round" {C.kv(dash=[[0, 0], [t_wrong, 0], [t_wrong + .3, 1]])}/></g>')
    s = header() + axis(labels=()) + target_line() + ybar(0) + simple_line(at_word(b, 1, "eight", 1), at_word(b, 1, "years.", 1, end=True))
    layers = floor_layers(s, tr, thought)
    cam = [[0, cam_x(HX + 45, .8), cam_y(720, .8), 1.85], [d, cam_x(HX + 50, .8), cam_y(712, .8), 1.97, "sine"]]
    from motion import A
    over = [A(A(f'<div style="font-family:Serif,serif;font-weight:700;font-size:150px;color:{RED};text-shadow:0 0 4px #000,0 6px 24px rgba(0,0,0,.7)">WRONG</div>',
                "stamp", t_wrong, .35, rot=-8), "life", 0, d, style="position:absolute;left:0;right:150px;top:1000px;text-align:center", fi=.01, fo=.2)]
    fx = [("paper", t_div, .25, -.3, dict(sec=.3, crisp=.6)), ("stamp", t_wrong, .55, 0), ("quill", t_wrong, .3, 0, dict(sec=.3, rate=4))]
    return shot(d, layers, [tr], cam, over), fx


def s2(b, d):
    t_grow = at_word(b, 2, "growing", 2)
    t_y1 = at_word(b, 2, "one", 2)
    t_y2 = at_word(b, 2, "two", 2)
    t_864 = at_word(b, 2, "sixty-four.", 2)
    tr = trader()
    s = header() + axis(labels=(0, 2)) + target_line() + ybar(0)
    s += simple_line(-2, -1, op=.35)
    s += ybar(1, t_y1) + ybar(2, t_y2)
    s += T(SX + 30, SY + 125, "+$800", 46, GREEN, family="Serif", extra=C.kv(opacity=[[0, 0], [t_y1, 0], [t_y1 + .2, 1], [t_864 - .4, 1], [t_864 - .2, 0]]))
    s += T(SX + 30, SY + 125, "+$864", 46, GREEN, family="Serif", extra=fade(t_864 - .2))
    s += counter(10000, 11664, t_y1, x=SX + SW - 30, y=SY + 125, size=40, color=INK, d=max(.8, t_864 - t_y1))
    layers = floor_layers(s, tr)
    cam = [[0, *cam_screen(1.62, 0, 10)], [d, *cam_screen(1.72, 0, 0), "sine"]]
    fx = [("marker", t_grow, .35, 0, dict(sec=.4)), ("clink", t_y1 + .2, .45, 0, dict(glass=False)), ("clink", t_y2 + .2, .5, 0, dict(glass=False))]
    return shot(d, layers, [tr], cam, [], shake=.15, vig=.3), fx


def s3(b, d):
    t_int = at_word(b, 3, "interest", 3)
    t_more = at_word(b, 3, "more", 3)
    tr = trader()
    s = header() + axis(labels=(0, 5, 8)) + target_line() + simple_line(-2, -1, op=.35)
    s += "".join(ybar(y) for y in range(3))
    span = max(1.2, t_more - t_int + .6)
    ts = [t_int - .2 + span * k / 6 for k in range(6)]
    s += "".join(ybar(y, t, d=.3) for y, t in zip(range(3, 9), ts))
    # the extra over $800 a year, growing: the gap between the bars and the straight line
    s += f'<g {fade(t_int)}>' + T(SX + 30, SY + 96, "interest", 28, TEAL, family="Serif") + T(SX + 30, SY + 128, "on interest", 28, TEAL, family="Serif") + '</g>'
    s += counter(11664, 18509, ts[0], x=SX + SW - 30, y=SY + 125, size=40, color=INK, d=span)
    layers = floor_layers(s, tr)
    cam = [[0, *cam_screen(1.72, 0, 0)], [d, *cam_screen(1.82, 6, -4), "sine"]]
    fx = [("clink", t + .15, .35 + .03 * k, 0, dict(glass=False)) for k, t in enumerate(ts)]
    return shot(d, layers, [tr], cam, [], shake=.15, vig=.3), fx


def s4(b, d):
    t_nine = at_word(b, 4, "nine", 4)
    t_twelve = at_word(b, 4, "twelve", 4)
    t_twenty = at_word(b, 4, "twenty", 4)
    tr = trader([[0, seat("relaxed", head=-4)], [t_nine, seat("relaxed", head=-8, brow=.8, mouth=1)], [d, seat("relaxed", head=-10, brow=.8, mouth=1)]])
    s = header() + axis(labels=(0, 9)) + target_line(.9) + "".join(ybar(y) for y in range(9))
    s += ybar(9, t_nine, fill=MUSTARD, d=.5)
    s += simple_line(-2, -1, op=.6)
    s += (f'<g {fade(t_twelve)}><circle cx="{xyear(12.5)}" cy="{ytop(20000)}" r="9" fill="{RED}" stroke="{INK}" stroke-width="2"/>'
          + T(xyear(12.5), BASE + 28, "12.5", 20, RED, anchor="middle", weight=700) + '</g>')
    s += T(SX + 30, SY + 130, "9 years", 58, INK, family="Serif", extra=fade(t_nine + .15))
    s += counter(18509, 19990, t_twenty - .2, x=SX + SW - 30, y=SY + 125, size=28, color=TEAL, d=.6)
    layers = floor_layers(s, tr)
    cam = [[0, *cam_screen(1.6, 0, 0)], [t_nine, *cam_screen(1.76, -10, -8), "inout"], [d, *cam_screen(1.82, -10, -10), "sine"]]
    fx = [("hit", t_nine + .1, .55, 0, dict(pitch=196)), ("clink", t_nine + .4, .5, 0, dict(glass=False)), ("tap", t_twelve, .3, 0, dict())]
    return shot(d, layers, [tr], cam, [], shake=.15, vig=.3), fx


def s5(b, d):
    t_72 = at_word(b, 5, "seventy-two", 5)
    t_72b = at_word(b, 5, "seventy-two", 5, nth=2)
    t_nine = at_word(b, 5, "nine.", 5)
    tr = trader([[0, seat("relaxed", head=0, brow=.5)], [t_72, seat("point", lean=8, head=-4, brow=.6)], [d, seat("point", lean=8, head=-6, brow=.6)]])
    s = header("THE SHORTCUT") + baseline()
    s += marker_text("r0", SX + 30, SY + 140, "72 ÷ rate", 64, INK, t_72, t_72 + .6, family="Serif")
    s += marker_text("r1", SX + 30, SY + 250, "72 ÷ 8 = 9", 80, TEAL, t_72b, t_nine + .2, family="Serif")
    layers = floor_layers(s, tr)
    cam = [[0, cam_x(HX + 215, .84), cam_y(700, .84), .94], [d, cam_x(HX + 245, .84), cam_y(670, .84), 1.1, "sine"]]
    fx = [("marker", t_72, .45, 0, dict(sec=.6)), ("marker", t_72b, .45, 0, dict(sec=.8)), ("hit", t_nine, .35, 0, dict(pitch=262))]
    return shot(d, layers, [tr], cam, []), fx


def s6(b, d):
    t_six = at_word(b, 6, "six", 6)
    t_dbl = at_word(b, 6, "double?", 6)
    tr = trader([[0, seat("relaxed", head=-4)], [t_dbl, seat("relaxed", head=-10, brow=.7, mouth=1)], [d, seat("relaxed", head=-12, brow=.7, mouth=1)]])
    s = header("YOUR TURN") + baseline()
    s += marker_text("q0", SX + 30, SY + 140, "6% a year", 60, INK, t_six, t_six + .5, family="Serif")
    s += marker_text("q1", SX + 30, SY + 240, "x2 in ? years", 56, TEAL, t_dbl - .2, t_dbl + .4, family="Serif")
    layers = floor_layers(s, tr)
    cam = [[0, cam_x(HX + 230, .84), cam_y(660, .84), .96], [d * .6, cam_x(HX + 255, .84), cam_y(640, .84), 1.1, "sine"], [d, cam_x(HX + 275, .84), cam_y(625, .84), 1.2, "inout"]]
    t_fol = at_word(b, 6, "follow", 6)
    over = [follow_ask(t_fol, d)]
    fx = [("marker", t_six, .45, .1, dict(sec=.5)), ("marker", t_dbl, .45, .1, dict(sec=.6)), ("tap", t_fol + .9, .45, .2, dict())]
    return shot(d, layers, [tr], cam, over), fx


def build():
    work = C.OUT / SLUG
    work.mkdir(parents=True, exist_ok=True)
    voice = narration(LINES, work)
    b = beats(voice, HOLDS)
    shots, events = [], []
    for i, fn in enumerate((s0, s1, s2, s3, s4, s5, s6)):
        s, fx = fn(b, b["durs"][i])
        shots.append(s)
        events += [(e[0], round(e[1] + b["shot_starts"][i], 3), *e[2:]) for e in fx]
    html, total = film(shots, captions(voice, b))
    json.dump(dict(beats=b, voice=[dict(text=m["text"], heard=m["heard"], wer=m["wer"], dur=m["dur"]) for m in voice]),
              open(work / "cues.json", "w"), indent=1)
    return html, total, work, voice, b, events


if __name__ == "__main__":
    html, total, work, voice, b, events = build()
    print(f"total {total:.1f} s; lines wer: {[round(m['wer'], 3) for m in voice]}")
    for m in voice:
        if m["wer"]:
            print("  heard:", m["heard"])
    mids = [round(s + d * k, 2) for s, d in zip(b["shot_starts"], b["durs"]) for k in (.15, .8)]
    if "render" not in sys.argv:
        pngs = C.stills(html, mids, work, "still", W, H)
        print(json.dumps(full_frame_check(pngs), indent=0))
    else:
        mp4, secs = C.render(html, total, work, SLUG, W, H, fps=30, workers=4)
        rep = sound(work, SLUG, voice, b, events)
        pngs = C.stills(html, mids, work, "still", W, H)
        rep["full_frame"] = full_frame_check(pngs)
        rep["render_seconds"] = round(secs, 1)
        json.dump(rep, open(work / "report.json", "w"), indent=1, default=str)
        m = rep["masters"]["clean"]
        print({k: m.get(k) for k in ("file", "lufs", "true_peak", "clipped_samples", "dnsmos", "wer_of_master")})
        print("full frame:", all(x["ok"] for x in rep["full_frame"]))
