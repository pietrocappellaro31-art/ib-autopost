"""
Reel, 28 Nov 2026 (slot B, 18:00 ET): down 50%, then up 50%. Is she back to even? The second full-frame Reel and the
first on the trading floor set (reel_film.trading_floor, 28 Nov), after the 27 Nov interview room.

Narrator: voice_clone.narrator(), EMMA (Kokoro bf_emma, 0.97) from 27 Nov to 4 Dec (Pietro, 27 Nov; CLAUDE.md wins over
the task prompt's HEART). No subtitles. The follow ask said in the last line and shown (follow_ask). Voice and
effects only in the file: the music is a trending licensed track Instagram attaches at posting. The trader, the desk,
the bank and the tickers on the wall are invented (set dressing; no real company, no real price).

Every number worked (plain arithmetic, no market data; a percent change is always measured from the price before it):
    Start                    $100
    Monday  -50%             100 x 0.50 = 50 lost, 100 - 50 = $50
    Friday  +50%             50 x 0.50 = $25 gained (half of fifty, not half of a hundred)
    End of the week          50 + 25 = $75, so still $25 below $100 (100 x 0.5 x 1.5 = 75)
    Back to $100 from $50    needs +$50 on $50 = 50 / 50 = 100%
Close (asked, not answered in the Reel): down 20% then up 20%: 100 x 0.8 = 80, 80 x 1.2 = 96, so $96.
Comment bonus: up 50% first, then down 50%: 100 x 1.5 = 150, 150 x 0.5 = 75, the same $75 (the order does not matter).
(build/check_down_up.py-style check run inline at build time: see _check().)

Hook candidates (28 Nov, scored 1 to 5 on clash, number early, second person, length, send-to-a-friend):
    1. "Down 50%. Up 50%. Even?"                                      clash 5, number 5, you 3, length 5, send 5 = 23
    2. "Lose 50%, gain 50%: you're not back to $100."                 clash 4, number 5, you 4, length 4, send 4 = 21
    3. "It's not $100. Down 50% then up 50% leaves $75."              gives the answer in 2 s (the standard forbids)
    4. "Most traders get this wrong: -50%, +50%."                     an unsourced claim about traders: cut
    5. "Answer before the bell: -50% then +50%?"                      clash 3, number 4, you 3, length 4, send 3 = 17
Chosen: 1 (the clash shape of the top-reach Reels: margin vs markup 1,531, both numbers on screen, the question last).

Story (docs/production/reel-film-standard.md):
    hook (said and shown in 2 s): her stock, down 50% then up 50%, and on screen "Down 50%. Up 50%. Even?"
    the wrong answer most people give (back to $100), struck out
    the mechanism on her monitor as it is said: the $100 bar loses half, the gain is half of the $50 that is left
    the payoff in one number, counted on the screen: $75
    what it means: from $50 you need +100% to get back
    the question back (down 20%, up 20%) and the follow ask, said and shown

    python3 build/reelf_down_up.py            stills (fast look)
    python3 build/reelf_down_up.py render     the Reel, its clean master and checks
"""

import json
import sys

import cine as C
from reel_film import (W, H, lay, cam_x, cam_y, shot, hook, narration, beats, at_word, captions, trading_floor,
                       marker_text, film, full_frame_check, sound, follow_ask, INK, RED, TEAL, MUSTARD, GREEN, _r)

SLUG = "w3-down-up"
LINES = [
    "Trading floor. Her stock is worth a hundred dollars. It drops fifty percent on Monday, then climbs fifty percent "
    "by Friday. Is she back to even?",
    "Most people say yes. Minus fifty, plus fifty. That's wrong.",
    "Monday's drop takes half of a hundred. She's left with fifty dollars.",
    "Friday's gain is half of the fifty she has left, not half of a hundred. Only twenty-five dollars comes back.",
    "Fifty plus twenty-five. She ends the week at seventy-five dollars.",
    "To get back to a hundred, her fifty has to double. That's a one hundred percent gain.",
    "Your turn: down twenty percent, then up twenty. Where does she end? Tell me in the comments, "
    "and follow for a new interview question every day.",
]
HOLDS = {4: .5}                    # a beat of air after the payoff

C.LOOKS["trader_f"] = {'coat': '#2E4A5A', 'coat2': '#223845', 'vest': '#F7F5F2', 'legs': '#2B2F3A', 'stock': '#2B2F3A',
                       'shoe': '#0A0A0A', 'skin': '#C68A62', 'hair': '#1E1410', 'hat': '', 'style': 'dress', 'cuff': '#F7F5F2'}
LOOK = "trader_f"
HX = 800


def _check():
    a = 100 * .5
    b = a + a * .5
    assert (a, b, 100 - b, (100 - a) / a) == (50, 75, 25, 1.0)
    assert round(100 * .8 * 1.2, 6) == 96 and 100 * 1.5 * .5 == 75


_check()
FLOOR, ANC = trading_floor(hero_x=HX)
SX, SY, SW, SH = ANC["screen"]
BASE = SY + SH - 44               # the bars' baseline on the screen
PX = 1.9                          # screen px per dollar: $100 = 190 px
BX0, BW_ = SX + 36, 110           # the bar


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


def header(text="HER STOCK"):
    return T(SX + 22, SY + 40, text, 24, INK, weight=700, extra='letter-spacing="3"') + \
        f'<path d="M{SX + 22},{SY + 56} L{SX + SW - 22},{SY + 56}" stroke="{INK}" stroke-width="2.4"/>'


def ytop(v):
    return BASE - v * PX


def screen_chart(t_drop, t_rise, t_q):
    """The hook's chart: $100 on Monday falls to $50, then climbs half again; the end is a question mark."""
    x0, x1, x2 = SX + 40, SX + 190, SX + 330
    y100, y50, y75 = ytop(100), ytop(50), ytop(75)
    s = header() + f'<path d="M{SX + 30},{BASE} L{SX + SW - 30},{BASE}" stroke="{INK}" stroke-width="3"/>'
    s += f'<path d="M{x0},{y100} L{SX + SW - 30},{y100}" stroke="{INK}" stroke-width="2" stroke-dasharray="8 8" opacity=".45"/>'
    s += T(x0, y100 - 12, "$100", 30, INK, family="Serif")
    s += (f'<path d="M{x0},{y100} L{x1},{y50}" fill="none" stroke="{RED}" stroke-width="9" stroke-linecap="round" '
          f'{C.kv(dash=[[0, 0], [t_drop, 0], [t_drop + .6, 1, "inout"]])}/>')
    s += f'<g {fade(t_drop + .4)}>' + T(x1 - 10, y50 + 44, "-50%", 34, RED, anchor="middle", family="Serif") + '</g>'
    s += (f'<path d="M{x1},{y50} L{x2},{y75}" fill="none" stroke="{GREEN}" stroke-width="9" stroke-linecap="round" '
          f'{C.kv(dash=[[0, 0], [t_rise, 0], [t_rise + .6, 1, "inout"]])}/>')
    s += f'<g {fade(t_rise + .4)}>' + T(x1 + 80, y75 - 30, "+50%", 34, GREEN, anchor="middle", family="Serif") + '</g>'
    s += (f'<g {C.kv(opacity=[[0, 0], [t_q, 0], [t_q + .2, 1]], translate=[[0, 0, 12], [t_q, 0, 12], [t_q + .35, 0, 0, "out"]])}>'
          f'<circle cx="{x2}" cy="{y75}" r="34" fill="{MUSTARD}" stroke="{INK}" stroke-width="3"/>'
          + T(x2, y75 + 15, "?", 44, INK, anchor="middle", family="Serif") + '</g>')
    s += T(x0, BASE + 32, "MON", 22, INK, weight=600) + T(x2, BASE + 32, "FRI", 22, INK, anchor="middle", weight=600)
    return s


def bar(v, fill, top_v=None, extra=""):
    """A bar from the baseline up to v (or from v to top_v)."""
    lo, hi = (0, v) if top_v is None else (v, top_v)
    return (f'<rect x="{BX0}" y="{ytop(hi)}" width="{BW_}" height="{(hi - lo) * PX}" fill="{fill}" stroke="{INK}" '
            f'stroke-width="3" {extra}/>')


def counter(c0, c1, ta, x=None, y=None, size=64, color=INK, d=.9):
    x = x or SX + SW - 30
    y = y or SY + 130
    return (f'<text x="{x}" y="{y}" font-family="\'Serif\',serif" font-weight="700" font-size="{size}" text-anchor="end" '
            f'fill="{color}" data-pre="$" data-dec="0" {C.kv(count=[[0, c0], [ta, c0], [ta + d, c1]])}>${c0}</text>')


def dashed_100(op=.55):
    return (f'<path d="M{SX + 24},{ytop(100)} L{BX0 + BW_ + 22},{ytop(100)}" stroke="{INK}" stroke-width="3" stroke-dasharray="10 9" opacity="{op}"/>'
            + T(BX0 + BW_ + 30, ytop(100) + 9, "$100", 26, INK, weight=700, extra=f'opacity="{min(1, op + .2) if op else 0:.2f}"'))


def baseline():
    return f'<path d="M{SX + 30},{BASE} L{SX + SW - 30},{BASE}" stroke="{INK}" stroke-width="3"/>'


def cam_screen(zoom, dx=0, dy=0):
    return cam_x(SX + SW / 2 + dx, .86), cam_y(SY + SH / 2 + dy, .86), zoom


# ----------------------------------------------------------------------------------------------- the shots

def s0(b, d):
    t_drop = at_word(b, 0, "drops", 0)
    t_rise = at_word(b, 0, "climbs", 0)
    t_q = at_word(b, 0, "even?", 0)
    tr = trader([[0, seat("relaxed", head=-2)], [t_drop, seat("concern", head=4, lean=10)], [t_rise, seat("relaxed", head=-6, brow=.6)],
                 [d, seat("relaxed", head=-8, brow=.7)]])
    layers = floor_layers(screen_chart(t_drop, t_rise, t_q), tr)
    # open wide on the floor with her and the screen, push towards the screen as the line moves
    cam = [[0, cam_x(HX + 225, .8), cam_y(690, .8), .9], [t_rise, *cam_screen(1.4, -60, 30), "inout"], [d, *cam_screen(1.5, -50, 20), "sine"]]
    over = [hook([[("Down ", False), ("50%.", True)], [("Up ", False), ("50%.", True)], [("Even?", True)]], at=0,
                 d=max(2.6, t_drop + .2), top=230, size=128)]
    fx = [("hit", t_drop + .3, .35, 0, dict(pitch=131)), ("hit", t_rise + .3, .3, 0, dict(pitch=262)), ("hit", t_q, .3, 0, dict(pitch=330))]
    return shot(d, layers, [tr], cam, over), fx


def s1(b, d):
    t_yes = at_word(b, 1, "yes.", 1)
    t_wrong = at_word(b, 1, "wrong.", 1)
    tr = trader([[0, seat("relaxed", head=0, mouth=1, brow=.5)], [t_yes, seat("shrug", mouth=1, brow=.8)],
                 [t_wrong, seat("concern")], [d, seat("concern", head=8)]])
    tx, ty = HX + 20, 590
    thought = (f'<g {C.kv(opacity=[[0, 0], [t_yes - .1, 0], [t_yes + .2, 1]], translate=[[0, tx, ty + 20, 0, .42], [t_yes - .1, tx, ty + 20, 0, .42], [t_yes + .35, tx, ty, 0, .55, "out"]])}>'
               f'<circle cx="-40" cy="190" r="12" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="-20" cy="150" r="20" fill="#fff" stroke="{INK}" stroke-width="4"/>'
               f'<rect x="-210" y="-100" width="420" height="220" rx="96" fill="#fff" stroke="{INK}" stroke-width="5"/>'
               + T(0, -28, "-50% +50%", 46, INK, anchor="middle", family="Serif")
               + T(0, 64, "= $100", 92, INK, anchor="middle", family="Serif")
               + f'<path d="M-170,46 L170,6" stroke="{RED}" stroke-width="16" stroke-linecap="round" {C.kv(dash=[[0, 0], [t_wrong, 0], [t_wrong + .3, 1]])}/></g>')
    layers = floor_layers(screen_chart(-5, -5, -5), tr, thought)
    cam = [[0, cam_x(HX + 45, .8), cam_y(720, .8), 1.85], [d, cam_x(HX + 50, .8), cam_y(712, .8), 1.97, "sine"]]
    from motion import A
    over = [A(A(f'<div style="font-family:Serif,serif;font-weight:700;font-size:150px;color:{RED};text-shadow:0 0 4px #000,0 6px 24px rgba(0,0,0,.7)">WRONG</div>',
                "stamp", t_wrong, .35, rot=-8), "life", 0, d, style="position:absolute;left:0;right:150px;top:1000px;text-align:center", fi=.01, fo=.2)]
    fx = [("paper", t_yes, .25, -.3, dict(sec=.3, crisp=.6)), ("stamp", t_wrong, .55, 0), ("quill", t_wrong, .3, 0, dict(sec=.3, rate=4))]
    return shot(d, layers, [tr], cam, over), fx


def s2(b, d):
    t_half = at_word(b, 2, "half", 2)
    t_fifty = at_word(b, 2, "fifty", 2)
    tr = trader()
    s = header("MONDAY") + baseline() + dashed_100(.0)
    s += bar(0, TEAL, 50)
    # the top half, red, drops off the bar as "half" is said
    s += (f'<g {C.kv(translate=[[0, 0, 0], [t_half, 0, 0], [t_half + .7, 60, 260, 14, 1, "in"]], opacity=[[0, 1], [t_half + .45, 1], [t_half + .7, 0]])}>'
          + bar(50, RED, 100) + T(BX0 + BW_ / 2, ytop(75) + 12, "-$50", 34, "#fff", anchor="middle", family="Serif") + '</g>')
    s += f'<g {fade(t_half + .55)}>' + dashed_100() + '</g>'
    s += T(BX0 + BW_ / 2, ytop(25) + 12, "$50", 34, "#fff", anchor="middle", family="Serif", extra=fade(t_fifty))
    s += counter(100, 50, t_half, y=SY + 210, size=84, color=INK)
    s += T(SX + SW - 30, SY + 258, "-50%", 44, RED, anchor="end", family="Serif", extra=fade(t_half + .2))
    layers = floor_layers(s, tr)
    cam = [[0, *cam_screen(1.62, 0, 10)], [d, *cam_screen(1.72, 0, 0), "sine"]]
    fx = [("paper", .05, .25, 0, dict(sec=.3, crisp=.6)), ("hit", t_half + .2, .45, 0, dict(pitch=110)), ("tap", t_fifty, .3, 0, dict())]
    return shot(d, layers, [tr], cam, [], shake=.15, vig=.3), fx


def s3(b, d):
    t_half = at_word(b, 3, "half", 3)
    t_not = at_word(b, 3, "not", 3)
    t_25 = at_word(b, 3, "twenty-five", 3)
    tr = trader()
    s = header("FRIDAY") + baseline() + dashed_100() + bar(0, TEAL, 50)
    s += T(BX0 + BW_ / 2, ytop(25) + 12, "$50", 34, "#fff", anchor="middle", family="Serif")
    # "half of fifty": a bracket beside the $50 bar, then a ghost half of a hundred struck out
    bx = BX0 + BW_ + 16
    s += (f'<g {fade(t_half)}><path d="M{bx},{ytop(50)} L{bx + 16},{ytop(50)} L{bx + 16},{ytop(0)} L{bx},{ytop(0)}" fill="none" stroke="{INK}" stroke-width="3"/>'
          + T(bx + 26, ytop(25) + 10, "x 50%", 30, INK, family="Serif") + '</g>')
    s += (f'<g {C.kv(opacity=[[0, 0], [t_not, 0], [t_not + .25, 1], [t_25 - .1, 1], [t_25 + .2, 0]])}><rect x="{BX0}" y="{ytop(100)}" width="{BW_}" height="{50 * PX}" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="8 7"/>'
          + T(BX0 + BW_ / 2, ytop(75) + 10, "+$50?", 30, RED, anchor="middle", family="Serif")
          + f'<path d="M{BX0 - 6},{ytop(60)} L{BX0 + BW_ + 6},{ytop(92)}" stroke="{RED}" stroke-width="8" stroke-linecap="round" {C.kv(dash=[[0, 0], [t_not + .4, 0], [t_not + .7, 1]])}/></g>')
    # the real gain: $25 rises onto the bar
    s += (f'<g {C.kv(clip=[[0, 100, 0, 0, 0], [t_25, 100, 0, 0, 0], [t_25 + .5, 0, 0, 0, 0, "out"]])}>'
          + bar(50, GREEN, 75) + T(BX0 + BW_ / 2, ytop(62.5) + 12, "+$25", 32, "#fff", anchor="middle", family="Serif") + '</g>')
    s += T(SX + SW - 30, SY + 196, "+$25", 58, GREEN, anchor="end", family="Serif", extra=fade(t_25 + .2))
    layers = floor_layers(s, tr)
    cam = [[0, *cam_screen(1.68, 0, 0)], [d, *cam_screen(1.8, 10, -6), "sine"]]
    fx = [("marker", t_half, .4, 0, dict(sec=.5)), ("marker", t_not + .4, .4, 0, dict(sec=.3)), ("clink", t_25 + .2, .5, 0, dict(glass=False))]
    return shot(d, layers, [tr], cam, [], shake=.15, vig=.3), fx


def s4(b, d):
    t_plus = at_word(b, 4, "plus", 4)
    t_75 = at_word(b, 4, "seventy-five", 4)
    tr = trader([[0, seat("relaxed", head=-4)], [t_75, seat("concern", head=6, brow=.8)], [d, seat("concern", head=8, brow=.8)]])
    s = header("END OF THE WEEK") + baseline() + dashed_100(.75) + bar(0, TEAL, 50) + bar(50, GREEN, 75)
    s += T(BX0 + BW_ / 2, ytop(25) + 12, "$50", 34, "#fff", anchor="middle", family="Serif")
    s += T(BX0 + BW_ / 2, ytop(62.5) + 12, "+$25", 30, "#fff", anchor="middle", family="Serif")
    # the gap to Monday's $100, in red, after the payoff
    s += (f'<g {fade(t_75 + .7)}><rect x="{BX0}" y="{ytop(100)}" width="{BW_}" height="{25 * PX}" fill="{RED}" opacity=".18" stroke="{RED}" stroke-width="3" stroke-dasharray="8 7"/>'
          + T(BX0 + BW_ / 2, ytop(87.5) + 12, "-$25", 32, RED, anchor="middle", family="Serif") + '</g>')
    s += counter(50, 75, t_plus, x=SX + SW - 22, y=SY + 240, size=100, color=INK, d=max(.6, t_75 - t_plus + .2))
    layers = floor_layers(s, tr)
    cam = [[0, *cam_screen(1.6, 0, 0)], [t_75, *cam_screen(1.78, 20, -10), "inout"], [d, *cam_screen(1.84, 20, -12), "sine"]]
    fx = [("tap", t_plus, .3, 0, dict()), ("hit", t_75 + .1, .55, 0, dict(pitch=196)), ("stamp", t_75 + .7, .3, 0)]
    return shot(d, layers, [tr], cam, [], shake=.15, vig=.3), fx


def s5(b, d):
    t_double = at_word(b, 5, "double.", 5)
    t_100 = at_word(b, 5, "hundred", 5, nth=2)
    tr = trader([[0, seat("relaxed", head=0, brow=.5)], [t_double, seat("point", lean=8, head=-4, brow=.6)], [d, seat("point", lean=8, head=-6, brow=.6)]])
    s = header("BACK TO $100?") + baseline() + dashed_100(.8) + bar(0, TEAL, 50)
    s += T(BX0 + BW_ / 2, ytop(25) + 12, "$50", 34, "#fff", anchor="middle", family="Serif")
    s += (f'<g {C.kv(clip=[[0, 100, 0, 0, 0], [t_double, 100, 0, 0, 0], [t_double + .6, 0, 0, 0, 0, "out"]])}>'
          + bar(50, MUSTARD, 100) + T(BX0 + BW_ / 2, ytop(75) + 12, "+$50", 34, INK, anchor="middle", family="Serif") + '</g>')
    s += T(SX + SW - 30, SY + 200, "+100%", 62, GREEN, anchor="end", family="Serif", extra=fade(t_100))
    s += T(SX + SW - 30, SY + 240, "on $50", 30, INK, anchor="end", weight=600, extra=fade(t_100 + .2))
    layers = floor_layers(s, tr)
    # a wider frame: her and the screen, so the world comes back before the close
    cam = [[0, cam_x(HX + 225, .84), cam_y(690, .84), .94], [d, cam_x(HX + 230, .84), cam_y(680, .84), 1.02, "sine"]]
    fx = [("clink", t_double + .3, .5, 0, dict(glass=False)), ("hit", t_100, .4, 0, dict(pitch=262))]
    return shot(d, layers, [tr], cam, []), fx


def s6(b, d):
    t_down = at_word(b, 6, "down", 6)
    t_up = at_word(b, 6, "up", 6)
    t_q = at_word(b, 6, "where", 6)
    tr = trader([[0, seat("relaxed", head=-4)], [t_q, seat("relaxed", head=-10, brow=.7, mouth=1)], [d, seat("relaxed", head=-12, brow=.7, mouth=1)]])
    s = header("YOUR TURN") + baseline()
    s += marker_text("q0", SX + 30, SY + 120, "$100", 52, INK, .1, .5, family="Serif")
    s += marker_text("q1", SX + 30, SY + 180, "-20%", 52, RED, t_down, t_down + .4, family="Serif")
    s += marker_text("q2", SX + 180, SY + 180, "+20%", 52, GREEN, t_up, t_up + .4, family="Serif")
    s += marker_text("q3", SX + 30, SY + 245, "= $?", 60, TEAL, t_q, t_q + .5, family="Serif")
    layers = floor_layers(s, tr)
    cam = [[0, cam_x(HX + 250, .84), cam_y(650, .84), 1.0], [d, cam_x(HX + 255, .84), cam_y(640, .84), 1.08, "sine"]]
    t_fol = at_word(b, 6, "follow", 6)
    over = [follow_ask(t_fol, d)]
    fx = [("marker", t_down, .45, .1, dict(sec=.5)), ("marker", t_up, .45, .1, dict(sec=.5)), ("marker", t_q, .45, .1, dict(sec=.6)),
          ("tap", t_fol + .9, .45, .2, dict())]
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
