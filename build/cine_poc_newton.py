"""
Proof of concept for the cinematic engine (13 Nov 2026): "Newton buys back in", about 20 seconds, the June
1720 moment from YouTube #6 (build/youtube_ep006.py), filmed instead of drawn beside a caption.

  Shot 1  Exchange Alley, London, June 1720. The camera tracks along a street of coffee houses; people
          cross at their own pace, two pairs talk, a hawker holds up the price list; the camera pushes into it.
  Shot 2  Match on the paper: Newton (our illustration, not a portrait) reads the same list in his study.
          The two prices lift off the page, April and June, and the jump between them is drawn. He reacts.
  Shot 3  Insert, top down: his hand writes the order. Shot 4: coins move from the bonds jar to the South Sea
          jar, all but one ("almost all").
  Shot 5  The approximate 1720 price path on parchment: where he sold, where he bought, where it peaked.

Narration (HEART: Kokoro af_heart at 0.9, en-us):
  "June, seventeen twenty. In Exchange Alley, it seemed everyone was getting rich."
  "Newton had sold his South Sea shares in April. Since then, the price had more than doubled."
  "So he sold almost all his government bonds, and bought back in."
  "He was buying close to the top."

Facts, from the sources already checked for YouTube #6 (see its docstring):
  - Newton sold his whole stake, or nearly, on 19 and 23 April 1720; in June he sold almost all of the
    government bonds he had bought and put the money into South Sea stock, later purchases close to the peak
    (Odlyzko, Notes and Records 2019; Physics Today, July 2020).
  - Approximate share prices: about £128 January, £175 February, £330 March, about £350 end of April, £550
    end of May, £890 early June, £1,000 first reached early August (Wikipedia "South Sea Company"; The National
    Archives blog, 2020). No July price is drawn: none was sourced.
  - Jonathan's and Garraway's coffee houses stood in Exchange Alley, where shares were traded (Wikipedia
    "Exchange Alley"); Castaing's "Course of the Exchange" printed share prices from 1698.
  - The street, the study, the letter and the people are our illustration (badge on screen: RECONSTRUCTION).
    No invented dialogue; the letter's words paraphrase what the records say he did.

    python3 build/cine_poc_newton.py            render, mix both masters, measure
    python3 build/cine_poc_newton.py --stills   key frames only (fast look)
    python3 build/cine_poc_newton.py --vertical the same film reframed for a 9:16 Short
"""

import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402

SLUG = "cine-poc-newton-1720"
LINES = [
    "June, seventeen twenty. In Exchange Alley, it seemed everyone was getting rich.",
    "Newton had sold his South Sea shares in April. Since then, the price had more than doubled.",
    "So he sold almost all his government bonds, and bought back in.",
    "He was buying close to the top.",
]
# shot starts and the narration start (film seconds); shot lengths follow from the next start
PLAN = dict(s1=0.0, s2=6.0, s3=12.6, s4=14.4, s5=17.3, end=20.6, l1=0.6, l2=6.5, l3=12.85, l4=17.65)
BIG = 10000
LX, LY = -3200, -1400


def lay(z, inner, noblur=False):
    return C.layer(z, inner, x=LX, y=LY, w=BIG, h=4000, noblur=noblur)


def badge(text, w, h):
    s = min(w, h) / 1080
    top = int(58 * s) if w > h else int(158 * s)
    return (f'<div class="badge" style="right:{int(70 * s)}px;top:{top}px;font-size:{int(17 * s)}px;padding:{int(7 * s)}px {int(12 * s)}px">'
            f'{text}</div>')


def title(k, h_, w, h, at=.3, d=3.6):
    s = min(w, h) / 1080
    left, bottom = int(96 * s), (int(170 * s) if w > h else int(760 * s))
    return (f'<div class="a" data-fx="life" data-at="{at}" data-d="{d}" data-fi=".5" data-fo=".6" style="position:absolute;left:0;bottom:0;'
            f'width:{int(1100 * s)}px;height:{int(520 * s) if w > h else int(1100 * s)}px;background:radial-gradient(ellipse at 0% 100%,rgba(20,12,4,.55),rgba(20,12,4,0) 70%)"></div>'
            f'<div class="title a" data-fx="life" data-at="{at}" data-d="{d}" data-fi=".5" data-fo=".6" style="left:{left}px;bottom:{bottom}px">'
            f'<div class="k" style="font-size:{int(24 * s)}px">{k}</div><div class="h" style="font-size:{int(84 * s)}px">{h_}</div></div>')


# ---------------------------------------------------------------------------------------------- shot 1
def shot_street(w, h, dur, vertical=False):
    lay_, anc = L.street_1720()
    back_svg, back = L.crowd(9, (-200, 2700), anc["ground_back"], .6, z_seed=2, dur=dur + 1, talkers=2, prefix="b")
    main_svg, main = L.crowd(4, (150, 2300), anc["ground_main"], .8, z_seed=5, dur=dur + 1, talkers=1, prefix="m",
                             dirs=(1, 1, -1))
    # the hawker holds up the day's price list
    paper = f'<g transform="translate(0,-10) scale(.55)">{L.newspaper(hi=0)}</g>'
    hawk = C.actor("hawker", "trader_cap", pos=[[0, 1400, anc["ground_main"]]], scale=.85, seed=7, dir=-1, walk=False,
                   holdF=paper, upright=True,
                   pose_keys=[[0, C.pose("relaxed", shF=96, elF=30)], [.8, C.pose("hold_up", mouth=2)], [1.6, C.pose("hold_up", mouth=0)],
                              [2.4, C.pose("hold_up", mouth=2, shF=128)], [3.2, C.pose("hold_up", mouth=0)], [dur, C.pose("hold_up")]])
    # a man waves a share certificate at a friend (excitement, without words)
    cert = f'<g transform="scale(.45)">{L.certificate()}</g>'
    waver = C.actor("waver", "gent_mus", pos=[[0, 760, anc["ground_main"] + 6]], scale=.82, seed=9, dir=1, walk=False,
                    holdF=cert, upright=True,
                    pose_keys=[[0, C.pose("hold_up", mouth=1, brow=.6)], [.7, C.pose("cheer", shB=-10, elB=10)],
                               [1.4, C.pose("hold_up", mouth=1)], [2.1, C.pose("cheer", shB=-10, elB=10)], [2.8, C.pose("hold_up", mouth=1)]])
    friend = C.actor("friend", "gent_teal", pos=[[0, 905, anc["ground_main"] + 4]], scale=.8, seed=12, dir=-1, walk=False,
                     pose_keys=[[0, C.pose("shrug")], [1.2, C.pose("talk_a")], [2.0, C.pose("talk_b", mouth=1)], [3, C.pose("talk_a")]])
    # someone hurries past very close to the lens (blurred by depth of field)
    passer = C.actor("passer", "gent_ink", pos=[[0, -400, 1180], [dur, 2600, 1180, "lin"]], scale=1.35, seed=4, dir=1, t0=0)
    layers = [lay(z, s, noblur=(k == "sky")) for k, (z, s) in lay_.items() if k != "street"]
    layers.append(lay(.62, back_svg))
    layers.append(lay(.8, lay_["street"][1] + main_svg + waver["svg"] + friend["svg"] + hawk["svg"]))
    layers.append(lay(1.15, passer["svg"]))
    layers.append(lay(1.3, L.foreground_1720()))
    # the push ends centred on the hawker's paper (world x of the paper on the z .8 layer -> camera x)
    px, py = 1316, 594                      # measured with the browser (identity camera), see docs/production/animation-engine.md
    cx, cy = 960 + (px - 960) / .8, 540 + (py - 540) / .8
    cam = [[0, 700, 560, 1.0], [3.9, 1080, 548, 1.09, "sine"], [dur - .35, cx, cy, 3.1, "inout"], [dur, cx, cy, 3.4, "lin"]]
    over = [title("Exchange Alley, London", "June 1720", w, h), badge("Reconstruction", w, h)]
    actors = back + main + [waver, friend, hawk, passer]
    return dict(dur=dur, layers=layers, actors=actors, cam=cam, focus=[[0, .8], [4.4, .8], [dur, .8]], dof=11, shake=.5,
                over=over, grade="warm"), dict(main=main, back=back, hawker=hawk, passer=passer)


# ---------------------------------------------------------------------------------------------- shots 2 and 4
def study_set(newton_pose, newton_hold="", jars=None, coins=None, w=1920, h=1080):
    lay_, anc = L.study_1720()
    desk_top = anc["desk_y"]
    props = (f'<g transform="translate(1240,{desk_top})">{L.cup()}</g>'
             f'<g transform="translate(800,{desk_top})">{L.ledger_book()}</g>'
             f'<g transform="translate(800,{desk_top - 40})">{L.ledger_book(170, 30, "#2E4A5A")}</g>'
             f'<g transform="translate(640,{desk_top})"><ellipse cx="0" cy="-6" rx="26" ry="8" fill="{C.INK}"/>'
             f'<rect x="-18" y="-30" width="36" height="26" rx="6" fill="#2A2522" stroke="{C.INK}" stroke-width="3"/></g>'
             f'<g transform="translate(652,{desk_top - 26}) rotate(18)">{L.quill(120)}</g>')
    if jars:
        props += jars
    newton = C.actor("newton", "newton", pos=[[0, 330, 990]], scale=1.0, seed=3, dir=1, walk=False, holdF=newton_hold, upright=True,
                     pose_keys=newton_pose)
    layers = [lay(z, s, noblur=(k == "floor")) for k, (z, s) in lay_.items() if k not in ("desk",)]
    layers.append(lay(.8, newton["svg"]))
    layers.append(lay(.85, lay_["desk"][1] + props + (coins or "")))
    layers.append(lay(1.25, f'<rect x="1700" y="-200" width="400" height="1600" fill="#3B2A1C"/>'
                            f'<rect x="1690" y="-200" width="24" height="1600" fill="#5A3D29"/>'))   # a doorframe close to the lens
    return layers, newton, anc


def shot_reading(w, h, dur, t_since, t_doubled):
    """Newton reads the list; the April and June prices lift off it; he reacts when the narration says
    'more than doubled'. Times are shot seconds."""
    paper = f'<g transform="translate(0,95) scale(.62)">{L.newspaper(hi=0)}</g>'
    pose_keys = [[0, C.pose("sit_read")], [t_since, C.pose("sit_read", head=6)],
                 [t_doubled, C.pose("sit_read", brow=1, mouth=2, head=-2, eyeY=0)],
                 [t_doubled + .9, C.pose("sit_read", brow=.8, mouth=0, shF=40, elF=58, shB=36, elB=62, head=-6, eyeY=-.5)],
                 [dur, C.pose("sit_read", brow=.6, mouth=-1, shF=34, elF=56, shB=30, elB=60, head=-8, eyeY=-.5)]]
    layers, newton, anc = study_set(pose_keys, paper)
    # the two prices lift off the paper into the room, with the jump drawn between them (z .9, in the world)
    hand = (466, 778)
    a_at, b_at = t_since - 1.6, t_since + .5
    ax, ay, bx, by = 850, 790, 1190, 590
    tag = lambda x, y, k, v, col, t: (
        f'<g {C.kv(translate=[[0, hand[0], hand[1], 0, .25], [t, hand[0], hand[1], 0, .25], [t + .9, x, y, 0, .78, "out"]], opacity=[[0, 0], [t, 0], [t + .25, 1]])}>'
        f'<rect x="-120" y="-70" width="240" height="140" rx="16" fill="#F4ECDD" stroke="{C.INK}" stroke-width="4"/>'
        f'<text x="0" y="-22" font-family="\'Sans\',sans-serif" font-weight="600" font-size="24" letter-spacing="3" text-anchor="middle" fill="{col}">{k}</text>'
        f'<text x="0" y="44" font-family="\'Serif\',serif" font-weight="700" font-size="66" text-anchor="middle" fill="{C.INK}">{v}</text></g>')
    jump = (f'<path d="M{ax + 96},{ay - 16} C{ax + 200},{ay - 30} {bx - 170},{by + 100} {bx - 104},{by + 34}" fill="none" stroke="{C.RED}" '
            f'stroke-width="8" stroke-linecap="round" {C.kv(dash=[[0, 0], [b_at + .5, 0], [b_at + 1.4, 1]])}/>'
            f'<g {C.kv(opacity=[[0, 0], [b_at + 1.3, 0], [b_at + 1.6, 1]], translate=[[0, bx - 112, by + 34, -30, .4], [b_at + 1.3, bx - 112, by + 34, -30, .4], [b_at + 1.7, bx - 112, by + 34, -30, .8, "out"]])}>'
            f'<path d="M-18,-10 L18,0 L-18,10 Z" fill="{C.RED}" stroke="{C.INK}" stroke-width="2"/></g>'
            f'<g {C.kv(opacity=[[0, 0], [t_doubled - .1, 0], [t_doubled + .25, 1]], translate=[[0, 1070, 745, 0, .5], [t_doubled - .1, 1070, 745, 0, .5], [t_doubled + .5, 1070, 745, -6, .75, "out"]])}>'
            f'<rect x="-120" y="-44" width="240" height="88" rx="44" fill="{C.RED}" stroke="{C.INK}" stroke-width="4"/>'
            f'<text x="0" y="18" font-family="\'Serif\',serif" font-weight="700" font-size="52" text-anchor="middle" fill="#fff">×2.5</text></g>')
    note = (f'<g {C.kv(opacity=[[0, 0], [a_at + .8, 0], [a_at + 1.2, .85]])}><text x="{ax - 92}" y="{ay - 82}" font-family="\'Sans\',sans-serif" '
            f'font-weight="600" font-size="17" letter-spacing="2.5" fill="#F7F5F2">APPROXIMATE PRICE PER SHARE</text></g>')
    numbers = tag(ax, ay, "END OF APRIL", "£350", C.TEAL, a_at) + tag(bx, by, "EARLY JUNE", "£890", C.RED, b_at) + jump + note
    layers.insert(-1, lay(.9, numbers))
    # match the end of shot 1: start close on the paper, pull back to a medium shot, drift towards the numbers
    pcx, pcy = 960 + (hand[0] - 960) / .8, 540 + (hand[1] - 540) / .8
    cam = [[0, pcx, pcy, 3.0], [1.9, 791, 746, 1.54, "inout"], [t_since + .4, 812, 736, 1.56, "sine"], [dur, 840, 720, 1.62, "sine"]]
    over = [badge("Reconstruction · Newton is our illustration", w, h)]
    return dict(dur=dur, layers=layers, actors=[newton], cam=cam, focus=[[0, .8], [2, .8], [dur, .85]], dof=5, shake=.35,
                over=over, grade="warm", tin=("dissolve", .5))


def shot_letter(w, h, dur, t_a, t_b):
    """Insert shot, top down: the hand writes the order. t_a/t_b: when each line starts (shot seconds).
    The nib follows the ink: the text is revealed left to right and the hand's origin is the nib."""
    size, lh, x_text, y1 = 84, 120, 560, 470
    lines = ("Sell the bonds.", "Buy South Sea.")
    cw = .43 * size                                  # average italic character width at this size
    write = 1.15
    sheet = (f'<g transform="translate(960,560) rotate(-2)"><rect x="-560" y="-330" width="1120" height="660" rx="4" fill="#F6EFE0" stroke="{C.INK}" stroke-width="5"/>'
             f'<rect x="-552" y="-322" width="1104" height="644" fill="url(#paperlines)" opacity=".45"/>'
             f'<text x="-500" y="-240" font-family="\'Sans\',sans-serif" font-weight="600" font-size="22" letter-spacing="4" fill="#7A6A55">LONDON, JUNE 1720</text></g>')
    ink = ""
    for i, (line, t0) in enumerate(zip(lines, (t_a, t_b))):
        ink += (f'<g {C.kv(clip=[[0, -10, 100, -10, 0], [t0, -10, 100, -10, 0], [t0 + write, -10, 0, -10, 0, "lin"]])}>'
                f'<text x="{x_text}" y="{y1 + i * lh}" font-family="\'Serif\',serif" font-style="italic" font-weight="400" font-size="{size}" '
                f'fill="#2A2018">{line}</text></g>')
    ink += (f'<path d="M{x_text},{y1 + lh + 26} C{x_text + 200},{y1 + lh + 18} {x_text + 420},{y1 + lh + 30} {x_text + 600},{y1 + lh + 20}" fill="none" '
            f'stroke="#2A2018" stroke-width="5" stroke-linecap="round" {C.kv(dash=[[0, 0], [t_b + write + .05, 0], [t_b + write + .45, 1, "out"]])}/>')
    desk = (C.defs() + f'<rect x="-1000" y="-800" width="4000" height="2800" fill="url(#boards)"/>'
            f'<rect x="-1000" y="-800" width="4000" height="2800" fill="#000" opacity=".2"/>'
            + sheet + ink
            + f'<g transform="translate(1620,250)"><circle r="78" fill="#2A2522" stroke="{C.INK}" stroke-width="5"/><circle r="44" fill="#0A0A0A"/></g>'
            + "".join(f'<g transform="translate({300 + 70 * k},{920 - 18 * k})"><circle r="42" fill="{C.MUSTARD}" stroke="{C.INK}" stroke-width="4"/>'
                      f'<circle r="30" fill="none" stroke="{C.INK}" stroke-width="2" opacity=".5"/></g>' for k in range(3))
            + C.shaft(-300, -200, 900, 1800, angle=-38, op=.2) + C.motes(100, 0, 1400, 1000, n=30, op=.55, spd=6, seed=11))
    def track(t0, line, y):
        k, n = [], 14
        width = cw * len(line)
        for i in range(n + 1):
            t = t0 + write * i / n
            k.append([t, x_text + width * i / n, y - 10 + (10 if i % 2 else -10), "lin"])
        return k
    keys = ([[0, 1500, 1000], [t_a - .3, x_text, y1 - 10]] + track(t_a, lines[0], y1)
            + [[t_b - .12, x_text, y1 + lh - 10]] + track(t_b, lines[1], y1 + lh)
            + [[t_b + write + .05, x_text, y1 + lh + 26], [t_b + write + .45, x_text + 600, y1 + lh + 20], [dur, x_text + 900, y1 + lh + 200]])
    coat, skin = C.LOOKS["newton"]["coat"], C.LOOKS["newton"]["skin"]
    hand = (f'<g {C.kv(translate=keys)}>'
            f'<path d="M150,90 C300,150 520,260 900,330 L860,520 C560,470 300,330 110,190 Z" fill="{coat}" stroke="{C.INK}" stroke-width="6"/>'
            f'<path d="M70,60 C120,70 170,110 190,160 C150,200 90,190 40,140 Z" fill="#F7F5F2" stroke="{C.INK}" stroke-width="6"/>'
            f'<path d="M150,90 C175,120 185,140 190,160" fill="none" stroke="{C.INK}" stroke-width="4"/>'
            f'<path d="M6,4 C30,-16 80,-4 110,30 C130,60 110,110 70,120 C30,124 4,96 -4,60 C-8,40 -4,16 6,4 Z" fill="{skin}" stroke="{C.INK}" stroke-width="6"/>'
            f'<path d="M30,40 C46,30 70,34 82,50" fill="none" stroke="{C.INK}" stroke-width="4" stroke-linecap="round"/>'
            f'<g transform="rotate(-62)"><path d="M0,0 L18,-2 L4,8 Z" fill="#2A2018"/>'
            f'<path d="M4,0 C60,-10 160,-40 330,-30 C220,-70 120,-50 40,-14 Z" fill="#F7F5F2" stroke="{C.INK}" stroke-width="5"/>'
            f'<path d="M4,0 L330,-30" stroke="{C.INK}" stroke-width="3"/>'
            f'<path d="M80,-12 C150,-30 230,-40 300,-34" fill="none" stroke="#CFC6B6" stroke-width="3"/></g></g>')
    layers = [lay(1.0, desk), lay(1.0, hand)]
    cam = [[0, 900, 560, 1.06], [dur, 880, 540, 1.12, "sine"]]
    return dict(dur=dur, layers=layers, actors=[], cam=cam, dof=0, shake=.25, grade="warm", vig=.8,
                over=[badge("Reconstruction", w, h)], tin=("cut", 0))


def shot_coins(w, h, dur, t0):
    """The bonds jar empties into the South Sea jar, all but one coin. t0: when the first coin moves."""
    jx_a, jx_b, base = 990, 1190, 860
    jars = (f'<g transform="translate({jx_a},{base})">{L.jar("BONDS", color=C.TEAL)}</g>'
            f'<g transform="translate({jx_b},{base})">{L.jar("SOUTH SEA", color=C.RED)}</g>')
    n = 7
    coins = ""
    for i in range(n):
        ya = base - 20 - i * 9
        yb = base - 20 - (i if i < n - 1 else 0) * 9
        if i == 0:                                         # the one coin that stays
            coins += f'<g transform="translate({jx_a},{ya})">{L.coin(26)}</g>'
            continue
        k = n - 1 - i                                      # top coin goes first
        t = t0 + k * .34
        yb = base - 20 - (k) * 9
        coins += (f'<g {C.kv(translate=[[0, jx_a, ya], [t, jx_a, ya], [t + .22, (jx_a + jx_b) / 2, base - 300, "out"], [t + .46, jx_b, yb, "in"]])}>'
                  f'{L.coin(26)}</g>')
    newton_pose = [[0, C.pose("sit_write", shF=50, elF=40, head=10)], [dur, C.pose("sit_write", shF=50, elF=40, head=6, brow=.3)]]
    layers, newton, anc = study_set(newton_pose, jars=jars, coins=coins)
    cam = [[0, 1120, 700, 1.75], [dur, 1100, 690, 1.86, "sine"]]
    return dict(dur=dur, layers=layers, actors=[newton], cam=cam, focus=[[0, .85]], dof=8, shake=.3, grade="warm",
                over=[badge("Reconstruction", w, h)], tin=("cut", 0))


# ---------------------------------------------------------------------------------------------- shot 5
def shot_chart(w, h, dur, t_bought):
    # month positions: Jan = 1 ... Aug = 8; no July point (none sourced)
    pts = [("Jan", 128, 1), ("Feb", 175, 2), ("Mar", 330, 3), ("Apr", 350, 4.0), ("May", 550, 5), ("Jun", 890, 6.1), ("Aug", 1000, 8.1)]
    ticks = [(m, lab) for m, lab in zip(range(1, 9), ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG"])]
    # the line must reach June before its flag lands (first render: the flag popped up ahead of the line)
    t_bought = max(t_bought, .95)
    chart = L.price_line(pts, 380, 300, 1300, 560, 1100, upto=5, draw=(.05, .85), xspan=(.6, 8.4), ticks=ticks,
                         flags=[(3, "SOLD", C.TEAL, .5), (5, "BOUGHT BACK", C.RED, t_bought)],
                         dashed_after=(t_bought + .5, t_bought + 1.2), label_size=30)
    px_, py_ = 380 + 1300 * (8.1 - .6) / 7.8, 300 + 560 - 560 * 1000 / 1100
    peak = (f'<g {C.kv(opacity=[[0, 0], [t_bought + 1.0, 0], [t_bought + 1.4, 1]])}>'
            f'<circle cx="{px_}" cy="{py_}" r="12" fill="#F3E7CF" stroke="{C.RED}" stroke-width="5"/>'
            f'<text x="{px_}" y="{py_ + 56}" font-family="\'Sans\',sans-serif" font-weight="600" font-size="26" letter-spacing="2" '
            f'text-anchor="middle" fill="{C.INK}">PEAK, AUGUST</text>'
            f'<text x="{px_}" y="{py_ + 92}" font-family="\'Serif\',serif" font-weight="700" font-size="34" text-anchor="middle" fill="{C.INK}">~£1,000</text></g>')
    head = (f'<text x="380" y="200" font-family="\'Sans\',sans-serif" font-weight="600" font-size="30" letter-spacing="4" fill="{C.INK}">SOUTH SEA STOCK, 1720</text>'
            f'<text x="380" y="240" font-family="\'Sans\',sans-serif" font-weight="400" font-size="24" fill="{C.INK}" opacity=".75">'
            f'Approximate price per share. Sources: Wikipedia, "South Sea Company"; The National Archives (2020); Odlyzko (2019)</text>')
    if h > w:                                              # vertical: the title and sources are a screen overlay (reframe)
        head = ""
    layers = [lay(.2, L.parchment(), noblur=True), lay(1.0, head + chart + peak)]
    cam = [[0, 980, 560, .98], [dur, 1060, 540, 1.06, "sine"]]
    return dict(dur=dur, layers=layers, actors=[], cam=cam, focus=[[0, 1]], dof=4, shake=.2, grade="none", vig=.7,
                over=[], tin=("dissolve", .45))


# ---------------------------------------------------------------------------------------------- voice and timing
def narration(work):
    """Say each line once (cached per line: an edited line re-says only itself), then find word times."""
    from voice import write_wav, SR
    from voice_clone import make_voice
    from voice_check import transcribe, wer
    cache = work / "lines"
    cache.mkdir(parents=True, exist_ok=True)
    v = None
    out = []
    for i, text in enumerate(LINES):
        key = cache / f"{i:02d}.json"
        wav = cache / f"{i:02d}.wav"
        meta = json.load(open(key)) if key.exists() else {}
        if meta.get("text") != text or meta.get("voice") != "HEART" or not wav.exists():
            v = v or make_voice("HEART")
            write_wav(wav, v.say(text))
            heard, words = transcribe(str(wav), with_words=True)
            meta = dict(text=text, voice="HEART", heard=heard, wer=float(wer(text, heard)), words=words)
            json.dump(meta, open(key, "w"), indent=1)
        import wave
        with wave.open(str(wav)) as wf:
            n = wf.getnframes()
        meta["dur"] = n / SR
        meta["wav"] = str(wav)
        out.append(meta)
    return out


def script_words(text, heard_words, start, dur):
    """Map the script's words onto the recogniser's timeline (it may spell numbers as digits)."""
    ws = text.split()
    if heard_words and len(heard_words) == len(ws):
        return [(w, start + a, start + b) for w, (_, a, b) in zip(ws, heard_words)]
    if heard_words:
        a0, a1 = heard_words[0][1], heard_words[-1][2]
    else:
        a0, a1 = 0.05, dur - .05
    lens = np.cumsum([0] + [len(w) + 1 for w in ws])
    return [(w, start + a0 + (a1 - a0) * lens[i] / lens[-1], start + a0 + (a1 - a0) * lens[i + 1] / lens[-1]) for i, w in enumerate(ws)]


def sentences(voice, starts, words):
    """Caption lines one sentence at a time, timed by their own words; each ends before the next begins
    (first render: two sentences crossfaded on top of each other)."""
    out = []
    for m, s0, wd in zip(voice, starts, words):
        cur = []
        for x in wd:
            cur.append(x)
            if x[0].endswith((".", "?", "!")):
                out.append((" ".join(y[0] for y in cur), cur[0][1], cur[-1][2] + .15, cur))
                cur = []
        if cur:
            out.append((" ".join(y[0] for y in cur), cur[0][1], cur[-1][2] + .15, cur))
    for i in range(len(out) - 1):
        nxt = out[i + 1][1]
        if out[i][2] > nxt - .35:
            out[i] = (out[i][0], out[i][1], nxt - .35, out[i][3])
    return out


def word_time(words, token):
    for w, a, b in words:
        if w.strip(".,").lower() == token:
            return a
    raise KeyError(token)


# ---------------------------------------------------------------------------------------------- build
def build(w=1920, h=1080, vertical=False):
    work = C.OUT / (SLUG + ("-vertical" if vertical else ""))
    work.mkdir(parents=True, exist_ok=True)
    voice = narration(C.OUT / SLUG)
    P = PLAN
    starts = [P["l1"], P["l2"], P["l3"], P["l4"]]
    words = [script_words(m["text"], m["words"], s, m["dur"]) for m, s in zip(voice, starts)]
    t_since = word_time(words[1], "since") - P["s2"]
    t_doubled = word_time(words[1], "doubled") - P["s2"]
    t_buying = word_time(words[3], "buying") - P["s5"]
    t_bought = word_time(words[2], "bought") - P["s4"]
    t_sell = word_time(words[2], "sold") - P["s3"]
    s1, ex = shot_street(w, h, P["s2"] - P["s1"], vertical)
    t_a = max(.25, t_sell - .3)
    t_coin = max(.15, t_bought - .9)
    shots = [s1,
             shot_reading(w, h, P["s3"] - P["s2"], t_since, t_doubled),
             shot_letter(w, h, P["s4"] - P["s3"], t_a, t_a + 1.25),
             shot_coins(w, h, P["s5"] - P["s4"], t_coin),
             shot_chart(w, h, P["end"] - P["s5"], t_buying - .2)]
    # the moments the sound follows (film seconds), derived from the same numbers as the picture
    fx = dict(tag_april=P["s2"] + t_since - 1.6 + .9, tag_june=P["s2"] + t_since + .5 + .9, times=P["s2"] + t_doubled + .3,
              lower_paper=P["s2"] + t_doubled + .9, write_a=P["s3"] + t_a, write_b=P["s3"] + t_a + 1.25, underline=P["s3"] + t_a + 1.25 + 1.2,
              coins=[P["s4"] + t_coin + k * .34 + .46 for k in range(6)], flag_sold=P["s5"] + .75 + .3,
              flag_bought=P["s5"] + t_buying - .2 + .35, peak=P["s5"] + t_buying - .2 + 1.2, push=P["s2"] - .45)
    if vertical:                                   # 9:16: same world, the camera frames the action
        reframe(shots, t_since, w, h)
    caps = C.captions(sentences(voice, starts, words), w, h)
    html, total = C.film_html(shots, w, h, caps=caps)
    cues = dict(total=total, starts=starts, voice=[dict(wav=m["wav"], at=s, dur=m["dur"], wer=m["wer"], heard=m["heard"]) for m, s in zip(voice, starts)],
                shots=[P["s1"], P["s2"], P["s3"], P["s4"], P["s5"]], t_since=t_since + P["s2"], t_doubled=t_doubled + P["s2"],
                t_bought=t_bought + P["s4"], t_sell=t_sell + P["s3"], t_buying=t_buying + P["s5"],
                steps=sorted(set(sum((C.footsteps(a, P["s2"]) for a in ex["main"] + [ex["passer"]]), []))),
                steps_near=sorted(set(sum((C.footsteps(a, P["s2"]) for a in [ex["passer"]] + ex["main"][:1]), []))),
                steps_back=sorted(set(sum((C.footsteps(a, P["s2"]) for a in ex["back"]), []))), fx=fx)
    json.dump(cues, open(work / "cues.json", "w"), indent=1)
    return html, total, work, cues


def sound(work, cues, silent_mp4, lufs=-14.0):
    """Stems for the film, then the clean and the scored master (master.dual)."""
    import sfx
    import score
    from master import Stems, dual
    from voice import MASTER
    P, fx, total = PLAN, cues["fx"], cues["total"]
    st = Stems(total)
    for v in cues["voice"]:
        st.voice_at(v["wav"], v["at"])
    # ambience: the street, then the study (a short crossfade at the cut), quieter under the inserts
    street = sfx.street_ambience(P["s2"] + .8, seed=3)
    fade = np.clip((P["s2"] + .5 - np.arange(len(street)) / sfx.FSR) / .9, 0, 1)
    st.add("amb", street * fade[:, None])
    room = sfx.room_tone(total - P["s2"] + .6, seed=5, clock=True, street=.3)
    rin = np.clip(np.arange(len(room)) / sfx.FSR / .7, 0, 1)
    st.add("amb", room * rin[:, None] * .9, at=P["s2"] - .5)
    ev = []
    # 13 Nov, measured: 65 footsteps under six seconds of narration took DNSMOS from 3.42 to 2.65 (ambience alone
    # cost 0.08). Only the passer-by close to the lens and the nearest walkers are heard; the far crowd is the murmur.
    for i, t in enumerate(cues["steps_near"]):
        if t < P["s2"] - .3:
            ev.append(("step", t, .45, (-.3, .3)[i % 2]))
    ev += [("paper", .85, .35, .35), ("paper", 2.45, .3, .35), ("paper", .75, .22, -.25), ("paper", 2.15, .2, -.25),
           ("paper", fx["push"], .6, 0, dict(sec=.55, crisp=1.6)), ("paper", P["s2"] + .1, .45, -.1),
           ("hit", fx["tag_april"], .45, -.2, dict(pitch=196)), ("hit", fx["tag_june"], .5, .25, dict(pitch=262)),
           ("hit", fx["times"], .38, .1, dict(pitch=330)), ("paper", fx["lower_paper"], .4, -.1),
           ("quill", fx["write_a"], .5, .1, dict(sec=1.15)), ("quill", fx["write_b"], .5, .1, dict(sec=1.15)),
           ("quill", fx["underline"], .4, .15, dict(sec=.4, rate=4)),
           ("paper", P["s5"] - .2, .2, 0, dict(sec=.6, crisp=.5)),
           ("hit", fx["flag_sold"], .42, -.2, dict(pitch=220)), ("hit", fx["flag_bought"], .55, .2, dict(pitch=147)),
           ("hit", fx["peak"], .35, .3, dict(pitch=294))]
    ev += [("clink", t, .55, .25, dict(glass=True)) for t in fx["coins"]]
    st.add("foley", sfx.foley_track(ev, total))
    stems, sc = score.compose([(P["s1"], P["s2"], "bustle"), (P["s2"], P["s3"], "discover"), (P["s3"], P["s5"], "decide"),
                               (P["s5"], P["end"], "peak")], key="F", bpm=80, seed=3)
    music = score.master_music(stems, balance=dict(strings=1.0, keys=2.2, winds=1.3, perc=.45))
    st.add("music", music)
    script = " ".join(LINES)
    rep = dual(st, silent_mp4, work, SLUG, lufs=lufs, tp=-1.5, script=script, chain=MASTER, foley_level_db=-20.0)
    rep["score"] = dict(engine="score.py + GeneralUser GS v2.0.3 via TinySoundFont", notes=len(sc.events), key="F major / D minor",
                        bpm=80, sections=["bustle", "discover", "decide", "peak"], seed=3)
    rep["foley_events"] = len(ev)
    json.dump(rep, open(work / f"{SLUG}-masters.json", "w"), indent=1)
    return rep


def reframe(shots, t_since=3.0, w=1080, h=1920):
    """Vertical framing: the stage fit is done by cine.stage() (the frame shows about 607 world px across at zoom 1),
    so each shot gets its own camera. 13 Nov, after the first vertical render: the study lost Newton (the camera sat
    on the bookcase), the captions covered the price tags and the jars, and the chart was cropped to March to June
    with its title and sources off the frame. Now: the study starts on Newton reading and follows the April price as
    it lifts off his paper to the two tags; the jars sit above the caption line; the chart pulls back to March to
    August with a screen-space title and the sources."""
    s1, s2, s3, s4, s5 = shots
    s1["cam"] = [[0, 900, 600, 1.0], [4.6, 1250, 600, 1.12, "sine"], s1["cam"][-1]]
    a_at = t_since - 1.6                                   # when the April tag leaves Newton's hand (shot_reading)
    nx = 960 + (420 - 960) / .8                            # Newton and his paper (layer z .8) at the frame centre
    tx, ty = 960 + (1020 - 960) / .9, 540 + (690 - 540) / .9   # the middle of the two tags (layer z .9)
    s2["cam"] = [s2["cam"][0], [1.9, nx, 830, 1.0, "inout"], [max(2.0, a_at + .4), nx + 20, 830, 1.0, "sine"],
                 [max(2.6, a_at + 1.5), tx, ty, .9, "inout"], [s2["dur"], tx + 20, ty - 6, .93, "sine"]]
    s3["cam"] = [[0, 820, 520, 1.25], [s3["dur"], 800, 520, 1.3, "sine"]]
    jx = 960 + (1090 - 960) / .85                          # between the two jars (layer z .85), both in frame
    s4["cam"] = [[0, jx, 800, 1.6], [s4["dur"], jx, 790, 1.68, "sine"]]
    s5["cam"] = [[0, 1240, 600, .6], [s5["dur"], 1250, 590, .615, "sine"]]
    k = min(w, h) / 1080
    s5["over"] = s5.get("over", []) + [
        f'<div style="position:absolute;left:{int(70 * k)}px;right:{int(70 * k)}px;top:{int(300 * k)}px;font-family:Sans,sans-serif;color:#0A0A0A">'
        f'<div style="font-weight:600;font-size:{int(40 * k)}px;letter-spacing:4px">SOUTH SEA STOCK, 1720</div>'
        f'<div style="font-size:{int(28 * k)}px;opacity:.75;margin-top:{int(10 * k)}px;line-height:1.3">Approximate price per share. Sources: '
        f'Wikipedia, "South Sea Company"; The National Archives (2020); Odlyzko (2019)</div></div>']


if __name__ == "__main__":
    vertical = "--vertical" in sys.argv
    w, h = (1080, 1920) if vertical else (1920, 1080)
    html, total, work, cues = build(w, h, vertical)
    if "--stills" in sys.argv:
        ts = [.5, 3.0, 5.6, 6.3, 8.5, 10.2, 11.8, 13.3, 14.0, 15.4, 16.6, 17.6, 18.8, 20.2]
        print(C.stills(html, ts, work, "still", w, h))
    else:
        if "--audio-only" in sys.argv:
            mp4 = work / f"{SLUG}-silent.mp4"
        else:
            mp4, secs = C.render(html, total, work, SLUG, w, h, fps=30)
            json.dump(dict(render_seconds=round(secs, 1), frames=int(round(total * 30))), open(work / "render.json", "w"))
        rep = sound(work, cues, mp4, lufs=-14.0)
        print(json.dumps({k: v for k, v in rep.items() if k != "masters"}, indent=1))
        for k, m in rep["masters"].items():
            print(k, {x: m[x] for x in m if x != "heard"})
