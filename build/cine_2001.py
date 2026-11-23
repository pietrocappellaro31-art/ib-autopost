"""
Filmed beats for YouTube #16, Enron, 1999 to 2001 (23 Nov 2026). Sets, props and shots for build/cine.py, used by
build/youtube_ep016.py as kind="cine" beats.

cinematic-standard.md section 8, step 3 (sets): the boardroom the build order named next ("a boardroom today"),
built as a glass-walled boardroom of 2000 that serves today too (dusk or day): a city through floor-to-ceiling
glass, a wall display that takes content, a long table with laptops, papers, water and a conference speakerphone
whose light pulses when a meeting is held by telephone, chairs, a wall clock whose hands move, directors who sit,
read, turn and react. Step 4 (data in the world): bars on a true scale on the wall display (assets on and off the
books; net income as reported against restated), ten years of a deal's profit that slide into year one, a hedge
whose two sides count against each other, a share price on a true axis with only its two sourced prints.

Sets (our own generic drawings: no real company's name on a building, no logo, no likeness; everything is badged):
  boardroom_2001(screen, dusk, speaker, clock_path, dur)  the boardroom. Layers (z): wall .4 (glass on the city at
                     x -760..520, the wall display 1000 x 540 at x 620..1620, y 110..650, a clock at (1800, 230)),
                     floor .6, chairs .74, people .78 (seated at y 990, seats at seat_xs), table .85 (top y 860)
Props: speakerphone(), paper_sheet(), box_prop() (a cardboard box held in both hands), year_blocks() (ten years of a
deal that slide into year one), hedge_board() (an investment and a partner's money counting against each other),
price_axis() (two sourced prints on a true dollar axis, the stretch between them dashed and unlabelled).

Shots (fn(w, h, dur, ctx) -> dict(shots, foley, amb)):
  hook_27bn     frame 0: the boardroom's wall display fills the frame: ALL ASSETS $60BN, OFF ITS BOOKS counts $0 to
                $27BN by 1.4 s, ALMOST 50% lands; on the question the camera pulls back to the directors at the table
  share_path    a city street at night; the billboard puts the two sourced prints on a true axis: $90.75 (Aug 2000)
                and $0.26 (close, 30 Nov 2001), the stretch between dashed and unlabelled
  revenue_jump  an office of 2000: the wall screen draws gross revenues $40bn (1999) and $100bn (2000) on one scale
  waiver_1/2    28 June 1999 (reconstruction): a special board meeting by teleconference, the speakerphone's light
                pulsing, the LJM proposal slid onto the table; part 2: RATIFIED is stamped on the waiver
  mtm_1/mtm_2   our example: a deal worth $10 a year for ten years; part 1 counts it as it comes ($10 this year);
                part 2 slides all ten years into year one: $77 reported now (today's value at 5% a year)
  three_pct     the SPE rule as a grid: 100 squares of an entity's assets, at least 3 from an outside owner
  raptor_1/2    the puzzle (our numbers): an investment falls $100 to $60, the partner's $100 of Enron shares
                covers the $40; part 2: the shares fall 70% to $30, the hedge cannot pay, and its $30 is Enron stock
  charge_oct    October 2001 at a kitchen table at night: the laptop types the $710M charge and the $1.2BN cut to
                shareholders' equity
  restate       8 November 2001: the wall screen draws net income as reported and as restated, 1997 to 2000, on
                one true scale ($m)
  collapse      2 December 2001 (reconstruction): a street at night, people carrying boxes past a billboard
Facts on screen come only from the sources in youtube_ep016.py's docstring. Nobody speaks; nobody is a likeness.
"""

import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402
from cine_1907 import lay, badge, seg_t, word_t   # noqa: E402,F401
from cine_1920 import title                       # noqa: E402
from cine_1971 import kt                          # noqa: E402
from cine_1974 import wall_clock                  # noqa: E402
from cine_2021 import street_today, kitchen_2021, _tower, _fold, _ktf, STREET_LOOKS, SCREEN   # noqa: E402
from cine_2023 import bank_office_today, wall_bars, rows_screen, find_t, _alive, _readers     # noqa: E402

INK, RED, TEAL, MUSTARD, PAPER = C.INK, C.RED, C.TEAL, C.MUSTARD, "#F7F5F2"
_r, _t = L._r, L._t
LIGHT, DIM = "#F4F1EA", "#8FA3A8"

C.LOOKS.update({
    # 23 Nov, YouTube #16: boardroom and office clothes of about 2000, generic; nobody's likeness.
    "dir_2001": dict(coat="#26304A", coat2="#1C2438", vest="#F1F2F4", legs="#26304A", stock="#26304A", shoe=INK, skin="#EBC3A3",
                     hair="#CFC8BE", hat="", style="suit", cuff="#F1F2F4", tie=RED, era="1971"),
    "dir_2001b": dict(coat="#3A3A3E", coat2="#2A2A2E", vest="#EEF0F2", legs="#3A3A3E", stock="#3A3A3E", shoe=INK, skin="#C99372",
                      hair="#2A1E18", hat="", style="suit", cuff="#EEF0F2", tie=TEAL, era="1971"),
    "dir_2001c": dict(coat="#4A3A30", coat2="#3A2C24", vest="#F4EFE4", legs="#33302E", stock="#33302E", shoe=INK, skin="#F1CBAA",
                      hair="#EDE7DD", hat="", style="suit", cuff="#F4EFE4", tie=MUSTARD, era="1971"),
    "dir_2001d": dict(coat="#5A2E2A", coat2="#47231F", vest="#F4EFE4", legs="#2F2F34", stock="#2F2F34", shoe=INK, skin="#8A5638",
                      hair="#14100D", hat="", style="suit", cuff="#5A2E2A", tie="#F4EFE4", era="1971"),
    "staff_2001": dict(coat="#6B7A8A", coat2="#56636F", vest="#F1F2F4", legs="#2B3140", stock="#2B3140", shoe=INK, skin="#E8BC9A",
                       hair="#5A3A28", hat="", style="suit", cuff="#F1F2F4", tie="#2B3140", era="1971"),
})
DIR_LOOKS = ["dir_2001", "dir_2001b", "dir_2001c", "dir_2001d", "staff_2001"]


# ------------------------------------------------------------------------------------------------ props

def speakerphone(x, y, live=True):
    """A conference speakerphone on the table at (x, y = table top): a low grey triangle with a light that pulses."""
    s = (f'<path d="M{x - 70},{y} L{x},{y - 34} L{x + 70},{y} Z" fill="#4A4F55" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
         + f'<ellipse cx="{x}" cy="{y - 12}" rx="26" ry="6" fill="#2A2E33"/>')
    if live:
        s += (f'<circle cx="{x}" cy="{y - 24}" r="6" fill="#7FE0A0" data-flick=\'[0.9,0.6,2]\'/>'
              f'<circle cx="{x}" cy="{y - 24}" r="16" fill="#7FE0A0" opacity=".25" data-flick=\'[0.25,0.25,2]\'/>')
    return s


def paper_sheet(w, h, head, sub, lines=(), t_lines=(), stamp="", t_stamp=99.0, seed=3):
    """A document on the table, seen from above (origin its centre): a heading, greeked lines, sourced lines that ink
    in at their times, and an optional stamp that lands at t_stamp."""
    out = (_r(-w / 2, -h / 2, w, h, PAPER, rx=4, sw=3.4)
           + _t(-w / 2 + 34, -h / 2 + 58, head, 34, fill=INK, anchor="start", family="Serif", weight=700)
           + _t(-w / 2 + 34, -h / 2 + 88, sub, 15, fill="#7A6A55", anchor="start", family="Sans", weight=600, extra='letter-spacing="3"')
           + L._greek(-w / 2 + 34, -h / 2 + 124, w - 68, 3, gap=22, seed=seed))
    for k, (txt, t) in enumerate(zip(lines, t_lines)):
        out += _ktf(_t(-w / 2 + 34, -h / 2 + 226 + 44 * k, txt, 28, fill=RED if k == 0 else INK, anchor="start", family="Sans", weight=700), t, .4)
    if stamp:
        sc = [[0, 2.2], [t_stamp - .01, 2.2], [t_stamp + .22, 1.0, "out"]] if t_stamp > 0 else [[0, 1.0]]
        op = [[0, 0], [t_stamp - .01, 0], [t_stamp + .08, .92]] if t_stamp > 0 else [[0, .92]]
        out += (f'<g transform="translate({w / 2 - 170},{h / 2 - 80}) rotate(-12)"><g {C.kv(scale=sc, opacity=op)}>'
                + f'<rect x="-140" y="-40" width="280" height="80" rx="8" fill="none" stroke="{RED}" stroke-width="7"/>'
                + _t(0, 16, stamp, 44, fill=RED, family="Sans", weight=700, extra='letter-spacing="4"') + "</g></g>")
    return out


def box_prop():
    """A cardboard box held in both hands (holdF), as people carry their things out of an office."""
    return (f'<g transform="translate(-10,-40)">' + _r(-46, -36, 92, 64, "#C49A6C", rx=3, sw=2.6)
            + f'<path d="M-46,-36 L-30,-50 L30,-50 L46,-36" fill="#D8B48A" stroke="{INK}" stroke-width="2.4"/>'
            + _r(-20, -46, 40, 12, "#F4F1EA", sw=1.6) + "</g>")


def year_blocks(t_show, t_this, t_slide=None, x0=60, y0=270, part=1):
    """Our example: ten years of a deal, $10 each (boxes Y1..Y10 in a row on a wall screen, 1000 x 500). Part 1: they
    appear in turn from t_show; at t_this Y1 lights as THIS YEAR. Part 2: from t_slide every later year slides into
    the Y1 column and stacks on it (mark to market books today's estimate of all ten years at once)."""
    s = ""
    bw, bh, gap = 78, 96, 12
    for k in range(10):
        x = x0 + k * (bw + gap)
        box = (_r(0, 0, bw, bh, TEAL if k == 0 else "#5E7378", rx=6, sw=2.4)
               + _t(bw / 2, 40, f"Y{k + 1}", 22, fill=LIGHT, family="Sans", weight=700) + _t(bw / 2, 76, "$10", 26, fill="#fff", family="Sans", weight=700))
        appear = t_show + .14 * k
        if part in (2, 3) and k > 0:
            ty = y0 - 22 * k                                                    # stacked above Y1, squeezed
            tr = [[0, x, y0], [t_slide + .07 * k, x, y0], [t_slide + .07 * k + .9, x0, ty, "inout"]]
            s += f'<g {C.kv(translate=tr)}>' + (_ktf(box, appear, .3) if part == 3 else box) + "</g>"
        else:
            s += f'<g transform="translate({x},{y0})">' + (_ktf(box, appear, .3) if part in (1, 3) else box) + "</g>"
    if part in (1, 3):
        hi = _ktf(_r(x0 - 8, y0 - 8, bw + 16, bh + 16, "none", rx=10, sw=0)
                  + f'<rect x="{x0 - 8}" y="{y0 - 8}" width="{bw + 16}" height="{bh + 16}" rx="10" fill="none" stroke="{MUSTARD}" stroke-width="6"/>'
                  + _t(x0 + bw / 2, y0 + bh + 34, "THIS YEAR", 22, fill=MUSTARD, family="Sans", weight=700, extra='letter-spacing="2"'), t_this, .3)
        s += hi if part == 1 else f'<g {C.kv(opacity=[[0, 1], [t_slide - .01, 1], [t_slide + .3, 0]])}>{hi}</g>'
    return s


def hedge_board(t_inv, t_cover, t_sh=None, t_fail=None, part=1):
    """The puzzle on a wall display (1000 x 540), our numbers. Left: ENRON'S INVESTMENT counts $100 -> $60 at t_inv,
    a -$40 LOSS tag. Right: THE PARTNER'S MONEY, ENRON SHARES $100. At t_cover an arrow PAYS $40 runs from the right
    to the left and LOSS COVERED lands. Part 2 opens on that end state: at t_sh the shares count $100 -> $30
    (DOWN 70%), at t_fail OWES $40, HAS $30 and THE HEDGE FAILS land, then the $30 IS ENRON'S OWN STOCK."""
    p2 = part == 2
    inv_keys = [[0, 60]] if p2 else [[0, 100], [t_inv, 100], [t_inv + 1.0, 60, "out"]]
    sh_keys = [[0, 100], [t_sh, 100], [t_sh + 1.1, 30, "out"]] if p2 else [[0, 100]]
    cnt = lambda x, y, keys, col, size=96: (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="{size}" '
                                            f'fill="{col}" {C.kv(count=keys)} data-dec="0" data-pre="$" data-suf="">${keys[0][1]}</text>')
    s = (_t(500, 50, "OUR EXAMPLE · A HEDGE PAID IN ITS OWN SHARES", 22, fill=DIM, family="Sans", weight=700, extra='letter-spacing="3"')
         + _r(40, 80, 420, 300, "#22303A", rx=14, sw=0) + _r(540, 80, 420, 300, "#22303A", rx=14, sw=0)
         + _t(250, 128, "ENRON'S INVESTMENT", 26, fill="#C9D4D6", family="Sans", weight=700, extra='letter-spacing="2"')
         + _t(750, 128, "THE PARTNER'S MONEY", 26, fill="#C9D4D6", family="Sans", weight=700, extra='letter-spacing="2"')
         + _t(750, 160, "ALL OF IT ENRON SHARES", 18, fill=MUSTARD, family="Sans", weight=700, extra='letter-spacing="2"')
         + cnt(250, 270, inv_keys, LIGHT) + cnt(750, 270, sh_keys, LIGHT)
         + _ktf(_r(170, 300, 160, 50, RED, rx=25, sw=0) + _t(250, 334, "-$40", 28, fill="#fff", family="Sans", weight=700), 0 if p2 else t_inv + 1.0, .3))
    arrow = (f'<path d="M560,420 L440,420" stroke="{TEAL}" stroke-width="10" stroke-linecap="round" '
             f'{C.kv(dash=[[0, 0], [t_cover, 0], [t_cover + .7, 1]]) if not p2 else ""} pathLength="1" stroke-dasharray="1 1"/>'
             f'<path d="M462,402 L436,420 L462,438" fill="none" stroke="{TEAL}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
             + _t(500, 462, "PAYS $40", 24, fill="#9FE0D2", family="Sans", weight=700, extra='letter-spacing="2"'))
    s += _ktf(arrow, t_cover, .3) if not p2 else f'<g {C.kv(opacity=[[0, 1], [t_fail - .01, 1], [t_fail + .3, 0]])}>{arrow}</g>'
    covered = _r(330, 486, 340, 44, TEAL, rx=22, sw=0) + _t(500, 516, "LOSS COVERED", 24, fill="#fff", family="Sans", weight=700, extra='letter-spacing="3"')
    if not p2:
        s += _ktf(covered, t_cover + .8, .3)
    else:
        s += f'<g {C.kv(opacity=[[0, 1], [t_fail - .01, 1], [t_fail + .3, 0]])}>{covered}</g>'
        s += _ktf(_r(670, 300, 160, 50, RED, rx=25, sw=0) + _t(750, 334, "DOWN 70%", 22, fill="#fff", family="Sans", weight=700), t_sh + 1.1, .3)
        s += _ktf(_t(500, 526, "OWES $40 · HAS $30", 30, fill=MUSTARD, family="Sans", weight=700, extra='letter-spacing="2"'), t_fail, .3)
        sc = [[0, 2.0], [t_fail + .6 - .01, 2.0], [t_fail + .85, 1.0, "out"]]
        s += (f'<g transform="translate(500,418) rotate(-6)"><g {C.kv(scale=sc, opacity=[[0, 0], [t_fail + .59, 0], [t_fail + .66, 1]])}>'
              + f'<rect x="-250" y="-46" width="500" height="92" rx="10" fill="#1B2A30" stroke="{RED}" stroke-width="8"/>'
              + _t(0, 18, "THE HEDGE FAILS", 50, fill=RED, family="Sans", weight=700, extra='letter-spacing="4"') + "</g></g>")
    return s


def price_axis(t1, t2, w=900, h=380):
    """Two sourced prints of Enron's share price on a true dollar axis (0 to $100) inside a billboard (w x h):
    $90.75 in August 2000 and $0.26 at the close on 30 Nov 2001 (History.com). Nothing in between is sourced here, so
    the stretch between them is a dashed line with no points, labelled as such."""
    x0, x1, yb, yt = 120, w - 90, h - 70, 70
    y_of = lambda v: yb - (yb - yt) * v / 100
    s = (_t(40, 44, "ENRON SHARE PRICE · $ · TRUE SCALE", 24, fill=LIGHT, anchor="start", family="Sans", weight=700, extra='letter-spacing="3"')
         + f'<path d="M{x0},{yt - 10} L{x0},{yb} L{x1 + 30},{yb}" fill="none" stroke="#5E7378" stroke-width="3"/>')
    for v in (0, 50, 100):
        s += _t(x0 - 14, y_of(v) + 8, f"${v}", 20, fill=DIM, anchor="end", family="Sans", weight=600)
        s += f'<path d="M{x0},{y_of(v):.0f} L{x1 + 30},{y_of(v):.0f}" stroke="#2E3A40" stroke-width="1.5"/>'
    pa, pb = (x0 + 40, y_of(90.75)), (x1, y_of(.26))
    s += _ktf(f'<circle cx="{pa[0]}" cy="{pa[1]:.0f}" r="13" fill="{MUSTARD}" stroke="{INK}" stroke-width="3"/>'
              + _t(pa[0] + 26, pa[1] + 10, "$90.75", 40, fill=MUSTARD, anchor="start", family="Serif", weight=700)
              + _t(pa[0] + 26, pa[1] + 40, "AUGUST 2000", 18, fill=DIM, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"'), t1, .3)
    s += (f'<path d="M{pa[0]},{pa[1]:.0f} L{pb[0]},{pb[1]:.0f}" stroke="#C9D4D6" stroke-width="4" stroke-dasharray="10 10" fill="none" '
          f'{C.kv(opacity=[[0, 0], [t1 + .4, 0], [t2, .85]])}/>')
    s += _ktf(_t((pa[0] + pb[0]) / 2 + 30, (pa[1] + pb[1]) / 2 + 50, "IN BETWEEN: NOT SHOWN", 16, fill=DIM, family="Sans", weight=700,
                 extra='letter-spacing="2"'), t1 + .8, .3)
    s += _ktf(f'<circle cx="{pb[0]}" cy="{pb[1]:.0f}" r="13" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
              + _t(pb[0], pb[1] - 60, "$0.26", 44, fill=RED, family="Serif", weight=700)
              + _t(pb[0], pb[1] - 30, "NOV 30, 2001", 18, fill=DIM, family="Sans", weight=700, extra='letter-spacing="2"'), t2, .3)
    return s


# ------------------------------------------------------------------------------------------------ the set

def boardroom_2001(screen="", seed=71, dusk=True, speaker=False, clock_path=None, dur=10.0, papers=True):
    """A glass-walled boardroom of about 2000 that also stands for today (generic). Layers (z): wall .4 (floor-to-
    ceiling glass on the city at x -760..520, the wall display 1000 x 540 at x 620..1620, y 110..650 whose screen takes
    `screen`, a clock at (1800, 230) if clock_path), floor .6, chairs .74, table .85 (top y 860 from x -120 to 1720:
    laptops, papers, water, and the speakerphone at x 820 when `speaker`). People sit at y 990 (z .78) at seat_xs.
    Returns (layers, anchors)."""
    rng = random.Random(seed)
    wall = C.defs() + '<rect x="-1800" y="-900" width="5600" height="2600" fill="#D6D0C6"/>'
    wall += "".join(_r(-1700 + k * 400, -30, 260, 22, "#F6F4EE", rx=6, sw=0) for k in range(14))          # ceiling lights
    gx, gy, gw, gh = -760, 70, 1280, 720
    top, bot = ("#2C3552", "#E59A62") if dusk else ("#A9C3D6", "#E8EEEE")
    wall += (f'<defs><linearGradient id="br01{seed}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
             f'<stop offset="1" stop-color="{bot}"/></linearGradient></defs>'
             f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="url(#br01{seed})"/>')
    x = gx
    while x < gx + gw:
        bw, bh = rng.uniform(60, 160), rng.uniform(240, 640)
        bw = min(bw, gx + gw - x)
        wall += _tower(x, bw, gy + gh - bh, gy + gh, rng.choice(["#2A3246", "#343C56", "#3A3F52"]) if dusk else rng.choice(["#8E9CAA", "#A3AFBA", "#7F8D9B"]),
                       .4 if dusk else .05, rng, cols=2, glass=True)
        x += bw + 5
    for k in range(1, 5):                                                              # mullions
        wall += f'<path d="M{gx + gw * k / 5:.0f},{gy} L{gx + gw * k / 5:.0f},{gy + gh}" stroke="#4A4F57" stroke-width="9"/>'
    wall += f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="none" stroke="#4A4F57" stroke-width="16"/>'
    wall += f'<path d="M{gx + 40},{gy + gh - 20} L{gx + 300},{gy + 30}" stroke="#F4F7F8" stroke-width="22" opacity=".12"/>'   # a reflection
    wall += _r(560, 700, 1700, 90, "#7A5A42", sw=3) + "".join(_r(580 + k * 210, 716, 190, 58, "#86654B", rx=3, sw=1.6) for k in range(8))  # wood panel
    wall += (f'<g transform="translate(620,110)">' + _r(-20, -20, 1040, 580, "#1E2228", rx=10, sw=4)
             + f'<rect width="1000" height="540" rx="4" fill="{SCREEN}"/>{screen}'
             + '<rect width="1000" height="540" fill="#9FE0D2" opacity=".04" data-flick=\'[0.04,0.02,3]\'/></g>')
    if clock_path:
        wall += wall_clock(1800, 230, 90, clock_path, dur, sec0=rng.randint(0, 59))
    pl = 1840                                                                           # a plant in the corner
    wall += (_r(pl - 50, 640, 100, 140, "#B9AC9A", rx=8, sw=3)
             + f'<g data-swing=\'[0.8,0.5,2,{pl},640]\'>' + "".join(
                 f'<path d="M{pl},640 C{pl + dx * .4:.0f},{560 - k * 18} {pl + dx:.0f},{520 - k * 24} {pl + dx * 1.2:.0f},{480 - k * 28}" '
                 f'stroke="#3F6B4A" stroke-width="16" fill="none" stroke-linecap="round"/>' for k, dx in enumerate((-80, -36, 18, 64, 100))) + "</g>")
    floor = ('<rect x="-1800" y="780" width="5600" height="900" fill="#5A4E46"/>'
             '<ellipse cx="800" cy="1000" rx="1500" ry="150" fill="#6B3A2E" opacity=".45"/>')
    seat_xs = list(range(40, 1700, 240))
    chairs = "".join(_r(x - 54, 740, 108, 170, "#1F2226", rx=16, sw=3) + _r(x - 40, 756, 80, 120, "#2C3036", rx=12, sw=0) for x in seat_xs)
    table = (_r(-120, 860, 1840, 42, "#4A2E1E", rx=10, sw=3.6) + _r(-90, 902, 1780, 26, "#33201A", sw=3)
             + _r(40, 928, 40, 160, "#2A1A12", sw=2.6) + _r(1560, 928, 40, 160, "#2A1A12", sw=2.6))
    if papers:
        for k, px in enumerate(seat_xs):
            if k % 2 == 0:                                                              # an open laptop
                table += (f'<path d="M{px + 20},856 L{px + 34},800 L{px + 118},800 L{px + 104},856 Z" fill="#3A3F46" stroke="{INK}" stroke-width="2.4"/>'
                          + f'<path d="M{px + 38},806 L{px + 114},806 L{px + 102},850 L{px + 26},850 Z" fill="#9FE0D2" opacity=".35" data-flick=\'[0.35,0.15,{k}]\'/>'
                          + _r(px + 10, 854, 120, 8, "#4A4F55", rx=3, sw=2))
            else:
                table += f'<g transform="translate({px + 60},854) rotate({rng.uniform(-6, 6):.1f})">' + _r(-50, -9, 100, 12, PAPER, sw=2) + "</g>"
            table += _r(px - 70, 818, 16, 40, "#CFE3E6", rx=4, sw=2)                   # water
    if speaker:
        table += speakerphone(820, 860)
    layers = dict(wall=(0.4, wall), floor=(0.6, floor), chairs=(0.74, chairs), table=(0.85, table))
    return layers, dict(table_y=860, seat_y=990, seat_xs=seat_xs, screen=(1120, 380), door_x=2100, speaker=(820, 840))


def directors(anc, dur, react_at=None, seats=(0, 2, 3, 5, 6), seed=200, prefix="dr", mood="concern"):
    """Directors seated along the table: they read, look up, turn to the display and live between their actions;
    at react_at each reacts in turn (brows, a lean back)."""
    xs = anc["seat_xs"]
    out = []
    for j, si in enumerate(seats):
        x = xs[si]
        face = -1 if x > 1120 else 1
        keys = [[0, C.pose("sit_read" if j % 2 else "seated", head=8 if j % 2 else -6)]]
        if react_at is not None:
            ta = react_at + .15 * j
            keys += [[ta, C.pose("seated", head=-10, eyeY=-.6)], [ta + .4, C.pose("seated", head=-16, lean=-6, brow=.8, mouth=(-1 if mood == "concern" else 0))],
                     [dur, C.pose("seated", head=-12, lean=-4, brow=.5)]]
        keys = _alive(keys, dur, t0=.7 + .3 * j, every=1.8 + .2 * (j % 3), amp=5)
        out.append(C.actor(f"{prefix}{j}", DIR_LOOKS[j % len(DIR_LOOKS)], pos=[[0, x, anc["seat_y"]]], scale=.9, seed=seed + j, dir=face, walk=False,
                           pose_keys=keys))
    return out


def _room_layers(layers_, ppl, extra_front=""):
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.8, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.85, layers_["table"][1] + extra_front))
    return layers


def _zx(x, z=.4):
    return 960 + (x - 960) / z


def _zy(y, z=.4):
    return 540 + (y - 540) / z


# ------------------------------------------------------------------------------------------------ shots

def shot_hook_27bn(w, h, dur, ctx):
    """The hook. Frame 0: the boardroom's wall display fills the frame. ENRON'S ASSETS (Senate, 2002: the chart the
    Finance Committee reviewed in October 2000, "$27 billion out of $60 billion of Enron's assets, or almost 50
    percent, were held off Enron's books"): ALL ASSETS $60BN is drawn at frame 0, OFF ITS BOOKS counts $0 to $27BN by
    1.4 s on the same scale, ALMOST 50% lands at 1.6 s. On the question (the last sentence) the camera pulls back to
    the table, where the directors look up from their papers."""
    n = len(ctx.get("segs") or [0])
    t_q = min(dur - 3.0, max(3.5, seg_t(ctx, n - 1, 0.0) - .4))
    sc = 13.0                                                                           # px per $bn
    scr = (_t(40, 60, "ENRON'S ASSETS · OCTOBER 2000", 30, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="3"')
           + _t(40, 92, "$ BILLION · A CHART SHOWN TO THE BOARD'S FINANCE COMMITTEE", 17, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
           + _t(40, 162, "ALL ASSETS", 24, fill=DIM, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + f'<rect x="40" y="178" width="{60 * sc:.0f}" height="90" fill="#5E7378"/>'
           + _t(40 + 60 * sc + 14, 240, "$60BN", 44, fill=LIGHT, anchor="start", family="Sans", weight=700)
           + _t(40, 330, "OFF ITS BOOKS", 24, fill=RED, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + f'<rect x="40" y="346" width="{27 * sc:.0f}" height="90" fill="{RED}" {C.kv(width=[[0, 0], [.05, 0], [1.4, round(27 * sc), "out"]])}/>'
           + f'<text x="{40 + 27 * sc + 16:.0f}" y="420" font-family="\'Serif\',serif" font-weight="700" font-size="84" fill="{RED}" '
             f'{C.kv(count=[[0, 0], [.05, 0], [1.4, 27, "out"]])} data-dec="0" data-pre="$" data-suf="BN">$27BN</text>'
           + kt(_r(700, 330, 260, 70, MUSTARD, rx=35, sw=0) + _t(830, 377, "ALMOST 50%", 32, fill=INK, family="Sans", weight=700, extra='letter-spacing="2"'), None, 1.6, .35)
           + _t(40, 500, "US SENATE INVESTIGATIONS SUBCOMMITTEE, 2002", 18, fill="#5E7378", anchor="start", family="Sans", weight=600, extra='letter-spacing="2"'))
    layers_, anc = boardroom_2001(screen=scr, seed=71, dusk=True)
    ppl = directors(anc, dur, react_at=t_q + .2)
    stand = C.actor("hk_p", "staff_2001", pos=[[0, 1700, 960]], scale=.98, seed=231, dir=-1, walk=False,
                    pose_keys=_alive([[0, C.pose("point", head=-6)], [2.2, C.pose("point", head=-8)], [3.0, C.pose("relaxed", head=8)],
                                      [t_q, C.pose("relaxed", head=10)], [t_q + .6, C.pose("concern", head=14)], [dur, C.pose("concern", head=10)]], dur, t0=3.4))
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k not in ("table",)]
    layers.append(lay(.66, stand["svg"]))
    layers += _room_layers(dict(table=layers_["table"]), ppl)[-2:]
    sx, sy = anc["screen"]
    cam = [[0, _zx(sx), _zy(sy), 1.02], [1.4, _zx(sx + 6), _zy(sy), 1.04, "sine"], [t_q, _zx(sx), _zy(sy + 10), 1.06, "sine"],
           [t_q + 1.8, 900, 560, .84, "inout"], [dur, 920, 560, .8, "sine"]]
    over = [badge("Our illustration · figures from the US Senate report, 2002", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl + [stand], cam=cam, focus=[[0, .4], [t_q + .6, .4], [t_q + 1.8, .8]], dof=5, shake=.3, over=over,
                grade="dusk", vig=1.1)
    import sfx
    foley = [("tick", .12, .3, 0), ("hit", 1.45, .35, 0, dict(pitch=150)), ("tick", 1.65, .3, .1), ("paper", t_q + .3, .25, -.2)]
    amb = sfx.room_tone(dur + .5, seed=711, clock=False, street=.1) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_share_path(w, h, dur, ctx):
    """A city street at night (our illustration, not Houston's real streets). The billboard draws Enron's share price on
    a true axis from $0 to $100 with only its two sourced prints (History.com: "$90.75 in August 2000 to $0.26 by
    closing on November 30, 2001"): $90.75 lands on 'ninety', $0.26 on 'twenty six'; the stretch between is dashed,
    labelled IN BETWEEN: NOT SHOWN. People walk past; some read their phones."""
    t1 = max(.8, find_t(ctx, "ninety") - .2)
    t2 = max(t1 + 1.4, find_t(ctx, "twenty six") - .2)
    layers_, anc = street_today(night=True, seed=27, billboard=price_axis(t1, t2))
    _, cr = L.crowd(9, (-600, 2600), anc["feet"], .95, z_seed=17, looks=STREET_LOOKS, speed=(55, 95), dur=dur + 1, talkers=0, prefix="sp")
    ppl = _readers(cr, STREET_LOOKS, every=3)
    layers = [lay(z, s, noblur=(k in ("light", "sky"))) for k, (z, s) in layers_.items()]
    layers.insert(len(layers) - 1, lay(.76, "".join(a["svg"] for a in ppl)))
    cam = [[0, 960, 600, .9], [t1 - .4, 960, 405, 1.0, "inout"], [t2 + 1.4, 975, 405, 1.02, "sine"], [dur, 960, 560, .92, "inout"]]
    over = [title("Houston, 2000 to 2001", "One share of Enron", w, h, d=min(2.6, t1 + .4)), badge("Our illustration · two prints from History.com", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, .5], [t2 + 1.6, .5], [dur, .76]], dof=4, shake=.3, over=over, grade="cool",
                vig=1.1, tin=("dissolve", .35))
    import sfx
    foley = [("tick", t1 + .1, .3, 0), ("hit", t2 + .1, .35, .1, dict(pitch=130))]
    foley += [("step", t, .05, -.2) for a in ppl[:3] for t in C.footsteps(a, dur)][:18]
    amb = sfx.city_ambience(dur + .5, seed=271, night=True, traffic=.5) * .6
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_revenue_jump(w, h, dur, ctx):
    """An office of about 2000 (our illustration). The wall screen draws Enron's gross revenues on one true scale as
    they are said (Senate, 2002: "Enron's gross revenues had jumped from $40 billion in 1999 to $100 billion in
    2000"); people come in and cross the floor; a seated man turns to watch."""
    t40 = max(1.0, find_t(ctx, "forty") - .2)
    t100 = max(t40 + 1.0, find_t(ctx, "hundred") - .2)
    sc = 8.0
    scr = (_t(40, 56, "ENRON · GROSS REVENUES", 24, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + _t(40, 84, "$ BILLION · US SENATE REPORT, 2002", 16, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
           + wall_bars(40, 170, [("1999", 40, "#5E7378", t40, "$40BN"), ("2000", 100, TEAL, t100, "$100BN")], sc, bar_h=70, gap=70, size=26))
    layers_, anc = bank_office_today(screen=scr, seed=81, front_monitor=False, dusk=False)
    feet = anc["feet"]
    looks = ["staff_2001", "dir_2001b", "office_2023", "dir_2001d", "office_2023c"]
    ppl = []
    for i in range(5):
        t0 = .2 + i * (dur / 5.5)
        x0 = -700 if i % 2 == 0 else 2600
        v = 150 if i % 2 == 0 else -140
        pos = [[0, x0, feet + (i % 3) * 14], [t0, x0, feet + (i % 3) * 14], [dur + 1, x0 + v * (dur + 1 - t0), feet + (i % 3) * 14, "lin"]]
        ppl.append(C.actor(f"rv{i}", looks[i], pos=pos, scale=.95, seed=250 + i, dir=1 if v > 0 else -1, amp=22))
    sit = C.actor("rv_s", "dir_2001c", pos=[[0, 1420, 1000]], scale=.92, seed=260, dir=-1, walk=False,
                  pose_keys=_alive([[0, C.pose("seated", head=10, eyeY=1)], [t100, C.pose("seated", head=10, eyeY=1)],
                                    [t100 + .4, C.pose("seated", head=-14, lean=-4, brow=.8)], [dur, C.pose("seated", head=-10)]], dur, t0=.6))
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k not in ("back", "front")]
    layers.append(lay(.62, layers_["back"][1]))
    layers.append(lay(.7, "".join(a["svg"] for a in ppl + [sit])))
    layers.append(lay(.86, layers_["front"][1]))
    cam = [[0, 880, 600, .92], [t40 - .3, 980, 500, 1.1, "inout"], [t100 + 1.0, 1010, 470, 1.2, "sine"], [dur, 990, 520, 1.08, "inout"]]
    over = [title("Houston, 1999 to 2000", "A company growing fast", w, h, d=min(2.8, t40 - .2)), badge("Our illustration · figures from the US Senate report", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl + [sit], cam=cam, focus=[[0, .55]], dof=3, shake=.2, over=over, grade="warm", vig=1.05,
                tin=("dissolve", .35))
    import sfx
    foley = [("tick", t40 + .1, .3, 0), ("tick", t100 + .1, .3, 0), ("hit", t100 + .9, .3, .1, dict(pitch=170))]
    foley += [("step", t, .05, -.2) for a in ppl[:3] for t in C.footsteps(a, dur)][:18]
    amb = sfx.room_tone(dur + .5, seed=811, clock=False, street=.15) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_waiver(w, h, dur, ctx, part=1):
    """28 June 1999 (reconstruction, not the real room): a special board meeting held by teleconference (Senate,
    2002). The room is nearly empty, the speakerphone's light pulses, the clock runs. Part 1: a member of staff slides
    the proposal onto the table (PROPOSAL: LJM; a fund run by Enron's CFO that would deal with Enron); part 2 opens on
    it and RATIFIED is stamped on the code of conduct waiver as 'ratified' is said (the Senate's words: "the Board
    ratified the code of conduct waiver and approved the LJM1 proposal with little study or debate")."""
    p2 = part == 2
    clock = [[0, 14, 2 + (8 if p2 else 0)], [dur, 14, 2 + (8 if p2 else 0) + dur / 60 * 6]]
    layers_, anc = boardroom_2001(screen=_t(500, 290, "SPECIAL MEETING · BY TELECONFERENCE", 30, fill="#5E7378", family="Sans", weight=700,
                                              extra='letter-spacing="3"'), seed=73, dusk=False, speaker=True, clock_path=clock, dur=dur)
    xs = anc["seat_xs"]
    t_slide = .9
    t_stamp = max(1.0, find_t(ctx, "ratified") + .1) if p2 else 99.0
    t_l1 = max(.6, find_t(ctx, "fund") - .1) if not p2 else 0
    lines = ("CODE OF CONDUCT: WAIVER", "A FUND RUN BY ENRON'S CFO", "IT WOULD DEAL WITH ENRON")
    t_lines = (t_l1, t_l1 + .6, t_l1 + 1.2) if not p2 else (0, 0, 0)
    sheet = paper_sheet(560, 470, "PROPOSAL: LJM", "JUNE 28, 1999 · OUR ILLUSTRATION", lines, t_lines, stamp="RATIFIED", t_stamp=t_stamp if p2 else 999)
    if not p2:
        big = f'<g {C.kv(translate=[[0, 1500, 640], [t_slide, 1500, 640], [t_slide + 1.0, 960, 520, "out"]], opacity=[[0, 0], [t_slide, 0], [t_slide + .3, 1]])}>' \
              f'<g transform="rotate(-3)">{sheet}</g></g>'
    else:
        big = f'<g transform="translate(960,520) rotate(-3)">{sheet}</g>'
    stf_pos = [[0, 2200, 960], [.1, 2200, 960], [.9, 1600, 960, "out"], [2.8, 1600, 960], [3.8, 2300, 960, "inout"], [dur, 2300, 960]] if not p2 else [[0, 2300, 960]]
    staff = C.actor("wv_s", "staff_2001", pos=stf_pos, scale=.98, seed=241, dir=-1,
                    pose_keys=[[0, C.pose("relaxed")], [.9, C.pose("reach", head=6)], [1.8, C.pose("relaxed", head=4)], [dur, C.pose("relaxed")]])
    ppl = directors(anc, dur, seats=(1, 4), seed=210 + part, prefix=f"wv{part}")
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k not in ("table",)]
    layers.append(lay(.7, staff["svg"]))
    layers.append(lay(.8, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.85, layers_["table"][1]))
    layers.append(lay(.92, big))
    spx, spy = anc["speaker"]
    if not p2:
        cam = [[0, _zx(spx, .85), _zy(spy - 40, .85), 1.35], [t_slide, _zx(spx, .85), _zy(spy - 60, .85), 1.3, "sine"],
               [t_slide + 1.6, 960, 560, 1.12, "inout"], [dur, 960, 540, 1.18, "sine"]]
    else:
        cam = [[0, 960, 540, 1.18], [t_stamp - .5, 960, 560, 1.3, "inout"], [t_stamp + 1.4, 960, 560, 1.34, "sine"], [dur, 940, 560, 1.0, "inout"]]
    over = ([title("June 28, 1999", "A special meeting of the board", w, h, d=min(2.8, dur - .6))] if not p2 else []) + \
        [badge("Reconstruction · not the real room · our illustration of the papers", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[staff] + ppl, cam=cam, focus=[[0, .85], [t_slide + 1.2, .92]], dof=4, shake=.25, over=over,
                grade="warm", vig=1.1, tin=("dissolve", .35) if not p2 else ("cut", 0))
    import sfx
    foley = ([("paper", t_slide + .1, .4, .2)] + [("step", t, .05, .3) for t in C.footsteps(staff, dur)][:8] if not p2 else []) + \
        ([("stamp", t_stamp + .2, .55, 0)] if p2 else [("tick", t, .2, 0) for t in t_lines])
    amb = sfx.room_tone(dur + .5, seed=731 + part, clock=True, street=.08) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_waiver_2(w, h, dur, ctx):
    return shot_waiver(w, h, dur, ctx, part=2)


def shot_mtm(w, h, dur, ctx, part=1):
    """Our example (not an Enron contract): a deal expected to bring in $10 a year for ten years, on an office wall
    screen. Part 1: the ten years appear; Y1 lights as THIS YEAR and PROFIT, COUNTED AS IT COMES $10 lands. Part 2:
    every later year slides into the year-one column (mark to market books today's estimate of all ten at once) and
    PROFIT IN YEAR ONE, MARKED TO MARKET counts $0 to $77 (the ten payments discounted at 5% a year: 77.22,
    build/plans/ep016_checks.py). An analyst stands at the screen."""
    p2 = part == 2
    if part == 3:                                                                       # 23 Nov: both phases in one beat
        t_show = max(.6, find_t(ctx, "ten dollars a year") - .3)
        t_this = max(t_show + 1.8, find_t(ctx, "this year") - .1)
        t_slide = max(t_this + 1.6, find_t(ctx, "all ten") - .3)
        t_77 = max(t_slide + 1.6, find_t(ctx, "seventy seven") - .3)
    elif not p2:
        t_show = max(.6, find_t(ctx, "ten dollars a year") - .3)
        t_this = max(t_show + 1.8, find_t(ctx, "this year") - .1)
        t_slide = t_77 = 99.0
    else:
        t_show = t_this = 0
        t_slide = max(.6, find_t(ctx, "all ten") - .3)
        t_77 = max(t_slide + 1.6, find_t(ctx, "seventy seven") - .3)
    scr = (_t(40, 56, "OUR EXAMPLE · A DEAL WORTH $10 A YEAR FOR 10 YEARS", 22, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + year_blocks(t_show, t_this, t_slide, part=part))
    if part == 3:
        first = (_t(40, 450, "PROFIT, COUNTED AS IT COMES:", 26, fill=DIM, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
                 + _t(880, 450, "$10 THIS YEAR", 40, fill=MUSTARD, anchor="end", family="Sans", weight=700))
        scr += f'<g {C.kv(opacity=[[0, 0], [t_this + .4, 0], [t_this + .7, 1], [t_slide, 1], [t_slide + .3, 0]])}>{first}</g>'
    if part == 3 or p2:
        scr += (_ktf(_t(40, 450, "YEAR ONE, MARKED TO MARKET:", 26, fill=DIM, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"'), t_77 - .4, .3)
                + f'<text x="880" y="456" text-anchor="end" font-family="\'Serif\',serif" font-weight="700" font-size="64" fill="{RED}" '
                  f'{C.kv(count=[[0, 0], [t_77, 0], [t_77 + 1.0, 77, "out"]], opacity=[[0, 0], [t_77 - .05, 0], [t_77, 1]])} data-dec="0" data-pre="$" data-suf="">$77</text>'
                + _ktf(_t(880, 488, "TODAY'S VALUE OF ALL TEN YEARS, AT 5% A YEAR", 16, fill=DIM, anchor="end", family="Sans", weight=600, extra='letter-spacing="2"'), t_77 + 1.0, .3))
    elif not p2:
        scr += _ktf(_t(40, 450, "PROFIT, COUNTED AS IT COMES:", 26, fill=DIM, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
                    + _t(880, 450, "$10 THIS YEAR", 40, fill=MUSTARD, anchor="end", family="Sans", weight=700), t_this + .4, .3)
    if False:
        scr += (_ktf(_t(40, 450, "YEAR ONE, MARKED TO MARKET:", 26, fill=DIM, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"'), t_77 - .4, .3)
                + f'<text x="880" y="456" text-anchor="end" font-family="\'Serif\',serif" font-weight="700" font-size="64" fill="{RED}" '
                  f'{C.kv(count=[[0, 0], [t_77, 0], [t_77 + 1.0, 77, "out"]], opacity=[[0, 0], [t_77 - .05, 0], [t_77, 1]])} data-dec="0" data-pre="$" data-suf="">$77</text>'
                + _ktf(_t(880, 488, "TODAY'S VALUE OF ALL TEN YEARS, AT 5% A YEAR", 16, fill=DIM, anchor="end", family="Sans", weight=600, extra='letter-spacing="2"'), t_77 + 1.0, .3))
    layers_, anc = bank_office_today(screen=scr, seed=91 if not p2 else 91, front_monitor=False, dusk=True)
    feet = anc["feet"]
    if not p2:
        pos = [[0, -200, feet], [.3, -200, feet], [2.4, 380, feet, "inout"], [dur, 400, feet]]
        keys = [[0, C.pose("relaxed")], [2.5, C.pose("relaxed", head=-12)], [t_this, C.pose("point", head=-14)], [t_this + 1.3, C.pose("relaxed", head=-10)],
                [dur, C.pose("relaxed", head=-8)]]
    else:
        pos = [[0, 400, feet]]
        keys = [[0, C.pose("relaxed", head=-8)], [t_slide, C.pose("point", head=-14)], [t_slide + 1.2, C.pose("relaxed", head=-10)],
                [t_77 + .3, C.pose("shrug", head=-4)], [t_77 + 1.6, C.pose("concern", head=-8)], [dur, C.pose("concern", head=-6)]]
    if part == 3:
        keys = [k for k in keys if k[0] < t_slide - .3] + [[t_slide, C.pose("point", head=-14)], [t_slide + 1.2, C.pose("relaxed", head=-10)],
                                                             [t_77 + .3, C.pose("shrug", head=-4)], [t_77 + 1.6, C.pose("concern", head=-8)], [dur, C.pose("concern", head=-6)]]
    an = C.actor(f"mt{part}", "staff_2001", pos=pos, scale=1.0, seed=271, dir=1, pose_keys=_alive(_fold(keys), dur, t0=1.0, every=1.9))
    sit = C.actor(f"mt_s{part}", "dir_2001b", pos=[[0, 1420, 1000]], scale=.92, seed=272, dir=-1, walk=False,
                  pose_keys=_alive([[0, C.pose("seated", head=-10)], [dur, C.pose("seated", head=-12)]], dur, t0=.5, every=1.7))
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k not in ("back", "front")]
    layers.append(lay(.62, layers_["back"][1]))
    layers.append(lay(.7, an["svg"] + sit["svg"]))
    layers.append(lay(.86, layers_["front"][1]))
    sx, sy = anc["wall_screen"]
    if not p2:
        cam = [[0, 900, 560, .92], [t_show - .2, _zx(sx - 60), _zy(sy - 20), 1.14, "inout"], [t_this, _zx(sx - 220), _zy(sy), 1.24, "inout"], [dur, _zx(sx - 200), _zy(sy), 1.26, "sine"]]
    else:
        cam = [[0, _zx(sx - 200), _zy(sy), 1.26], [t_slide + 1.4, _zx(sx - 120), _zy(sy - 10), 1.2, "inout"], [t_77 + .2, _zx(sx + 40), _zy(sy + 20), 1.3, "inout"],
               [dur, _zx(sx), _zy(sy), 1.14, "sine"]]
    if part == 3:
        cam = [[0, 900, 560, .92], [t_show - .2, _zx(sx - 60), _zy(sy - 20), 1.14, "inout"], [t_this, _zx(sx - 220), _zy(sy), 1.24, "inout"],
               [t_slide, _zx(sx - 200), _zy(sy), 1.26, "sine"], [t_slide + 1.4, _zx(sx - 120), _zy(sy - 10), 1.2, "inout"],
               [t_77 + .2, _zx(sx + 40), _zy(sy + 20), 1.3, "inout"], [dur, _zx(sx), _zy(sy), 1.14, "sine"]]
    over = ([title("Mark to market", "Our example", w, h, d=min(2.6, t_show + .6))] if not p2 else []) + [badge("Our example · not an Enron contract", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[an, sit], cam=cam, focus=[[0, .5]], dof=3, shake=.2, over=over, grade="dusk", vig=1.05,
                tin=("dissolve", .35) if not p2 else ("cut", 0))
    import sfx
    if not p2:
        foley = [("tick", t_show + .14 * k, .18, -.3 + .06 * k, dict(tock=True)) for k in range(10)] + [("tick", t_this, .3, 0)]
        foley += [("step", t, .05, -.3) for t in C.footsteps(an, dur)][:8]
    else:
        foley = [("tick", t_slide + .07 * k + .9, .2, -.2 + .05 * k, dict(tock=True)) for k in range(1, 10)] + [("hit", t_77 + 1.0, .35, 0, dict(pitch=150))]
    if part == 3:
        foley += [("tick", t_slide + .07 * k + .9, .2, -.2 + .05 * k, dict(tock=True)) for k in range(1, 10)] + [("hit", t_77 + 1.0, .35, 0, dict(pitch=150))]
    amb = sfx.room_tone(dur + .5, seed=911 + part, clock=False, street=.12) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_mtm_2(w, h, dur, ctx):
    return shot_mtm(w, h, dur, ctx, part=2)


def shot_mtm_both(w, h, dur, ctx):
    """23 Nov: the two parts in one beat (counted as it comes, then marked to market), so chapter 3 opens on the filmed
    mtm_term without three filmed beats in a row."""
    return shot_mtm(w, h, dur, ctx, part=3)


def shot_three_pct(w, h, dur, ctx):
    """The rule for keeping an entity off the books, as the Powers report gives it ("an owner independent of the
    company must make a substantive equity investment of at least 3% of the SPE's assets, and that 3% must remain at
    risk"), drawn on the boardroom display as 100 squares of the entity's assets (our illustration): the squares fill
    in, then three turn red, OUTSIDE OWNER: AT LEAST 3%, AT RISK."""
    t_grid = .5
    t3 = max(t_grid + 2.0, find_t(ctx, "three percent") - .2)
    sq, gap, gx, gy = 34, 6, 60, 110
    cells = ""
    for k in range(100):
        r, c = divmod(k, 10)
        col = RED if k >= 97 else "#5E7378"
        base = _r(gx + c * (sq + gap), gy + r * (sq + gap), sq, sq, "#5E7378", rx=4, sw=0)
        cells += _ktf(base, t_grid + .02 * k, .2)
        if k >= 97:
            cells += _ktf(_r(gx + c * (sq + gap), gy + r * (sq + gap), sq, sq, col, rx=4, sw=0), t3 + .15 * (k - 97), .25)
    scr = (_t(60, 70, "AN ENTITY'S ASSETS · 100 SQUARES", 22, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + cells
           + _ktf(_t(520, 220, "OUTSIDE OWNER:", 30, fill=LIGHT, anchor="start", family="Sans", weight=700)
                  + _t(520, 290, "AT LEAST 3%", 62, fill=RED, anchor="start", family="Serif", weight=700)
                  + _t(520, 340, "AND IT MUST STAY AT RISK", 22, fill=MUSTARD, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
                  + _t(520, 470, "THE POWERS REPORT, 2002", 16, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"'), t3 + .5, .3))
    layers_, anc = boardroom_2001(screen=scr, seed=75, dusk=True)
    ppl = directors(anc, dur, seats=(0, 3, 5), seed=220, prefix="tp")
    layers = _room_layers(layers_, ppl)
    sx, sy = anc["screen"]
    cam = [[0, 960, 560, .9], [t_grid + .4, _zx(sx - 40), _zy(sy), 1.2, "inout"], [t3 + .4, _zx(sx + 40), _zy(sy - 10), 1.3, "inout"], [dur, _zx(sx + 60), _zy(sy), 1.34, "sine"]]
    over = [badge("Our illustration · the rule as the Powers report gives it", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, .4]], dof=4, shake=.2, over=over, grade="dusk", vig=1.1, tin=("dissolve", .35))
    import sfx
    foley = [("tick", t_grid + .2 * k, .12, -.3 + .06 * k, dict(tock=True)) for k in range(10)] + [("hit", t3 + .1, .35, 0, dict(pitch=160))]
    amb = sfx.room_tone(dur + .5, seed=751, clock=False, street=.1) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_raptor(w, h, dur, ctx, part=1):
    """The puzzle, our numbers (not the Raptors' real figures), in two beats on the boardroom's display (hedge_board).
    Part 1 sentences: our numbers, Enron owns an investment worth $100, a partner promises to cover any fall with $100
    of Enron shares, it falls to $60, the partner owes $40 and the loss disappears. Part 2: Enron's shares fall 70%,
    worth $30, owes $40, can't pay, and the $30 is Enron's own stock. A presenter stands at the display; at the
    failure the directors lean back."""
    p2 = part == 2
    if not p2:
        t_inv = max(1.2, find_t(ctx, "sixty") - .2)
        t_cover = max(t_inv + 1.4, find_t(ctx, "forty") - .2)
        t_sh = t_fail = 99.0
    else:
        t_inv = t_cover = 0
        t_sh = max(.6, find_t(ctx, "seventy") - .4)
        t_fail = max(t_sh + 1.6, find_t(ctx, "can't pay") - .3)
    scr = hedge_board(t_inv, t_cover, t_sh, t_fail, part=part)
    layers_, anc = boardroom_2001(screen=scr, seed=77, dusk=True)
    ppl = directors(anc, dur, react_at=(t_fail + .7) if p2 else None, seats=(0, 2, 5, 6), seed=230 + part, prefix=f"rp{part}")
    keys = ([[0, C.pose("relaxed", head=8)], [t_inv, C.pose("point", head=-6)], [t_inv + 1.0, C.pose("relaxed", head=-4)],
             [t_cover, C.pose("point", head=-8)], [t_cover + 1.2, C.pose("relaxed", head=6)], [dur, C.pose("relaxed", head=4)]] if not p2 else
            [[0, C.pose("relaxed", head=4)], [t_sh, C.pose("point", head=-8)], [t_sh + 1.2, C.pose("relaxed", head=-4)],
             [t_fail + .6, C.pose("concern", head=8)], [dur, C.pose("concern", head=6)]])
    pres = C.actor(f"rp_p{part}", "staff_2001", pos=[[0, 1700, 960]], scale=.98, seed=241, dir=-1, walk=False, pose_keys=_alive(keys, dur, t0=1.2, every=2.0))
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.66, pres["svg"]))
    layers.append(lay(.8, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.85, layers_["table"][1]))
    sx, sy = anc["screen"]
    if not p2:
        cam = [[0, 960, 560, .88], [t_inv - .6, _zx(sx - 100), _zy(sy), 1.16, "inout"], [t_cover, _zx(sx), _zy(sy + 20), 1.2, "inout"],
               [dur, _zx(sx + 10), _zy(sy + 20), 1.24, "sine"]]
    else:
        cam = [[0, _zx(sx + 10), _zy(sy + 20), 1.24], [t_sh, _zx(sx + 120), _zy(sy), 1.3, "inout"], [t_fail + .4, _zx(sx), _zy(sy), 1.32, "inout"],
               [t_fail + 2.2, 960, 560, .9, "inout"], [dur, 960, 560, .88, "sine"]]
    over = ([title("The puzzle", "Our numbers, not Enron's", w, h, d=min(2.6, t_inv - .3))] if not p2 else []) + [badge("Our example · not the Raptors' real figures", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl + [pres], cam=cam, focus=[[0, .4]], dof=4, shake=.2, over=over, grade="dusk", vig=1.1,
                tin=("dissolve", .35) if not p2 else ("cut", 0))
    import sfx
    foley = ([("tick", t_inv + .1, .3, -.2), ("tick", t_cover + .1, .3, .2), ("tap", t_cover + .9, .3, 0)] if not p2 else
             [("tick", t_sh + .1, .3, .2), ("tick", t_fail, .3, 0), ("stamp", t_fail + .75, .5, 0)])
    amb = sfx.room_tone(dur + .5, seed=771 + part, clock=False, street=.1) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_raptor_2(w, h, dur, ctx):
    return shot_raptor(w, h, dur, ctx, part=2)


def shot_charge_oct(w, h, dur, ctx):
    """October 2001 at a kitchen table at night (our illustration). The laptop types what the Senate report says Enron
    recorded: "a $710 million charge to earnings and a $1.2 billion reduction in shareholder equity"."""
    t_c = max(1.0, find_t(ctx, "seven hundred and ten") - .2)
    t_e = max(t_c + 1.0, find_t(ctx, "one point two") - .2)
    scr = (_t(24, 44, "OCTOBER 2001 · ENRON REPORTS", 20, fill=LIGHT, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + _t(24, 70, "OUR ILLUSTRATION · FIGURES FROM THE US SENATE REPORT", 13, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
           + rows_screen([("CHARGE TO EARNINGS", None, RED, t_c - .2, [[0, 0], [t_c, 0], [t_c + .8, 710, "out"]], (0, "$", "M")),
                          ("SHAREHOLDERS' EQUITY", None, MUSTARD, t_e - .2, [[0, 0], [t_e, 0], [t_e + .8, 1.2, "out"]], (1, "-$", "BN"))],
                         x0=24, y0=160, step=100, wid=560, size=24))
    layers_, anc = kitchen_2021(night=True, seed=37, screen=scr)
    sx, sy = anc["seat"]
    viewer = C.actor("co", "dir_2001b", pos=[[0, sx, sy]], scale=1.0, seed=281, dir=-1, walk=False,
                     pose_keys=_alive([[0, C.pose("seated", head=10, eyeY=1)], [t_c - .3, C.pose("seated", head=12, lean=10, eyeY=1)],
                                       [t_c + .9, C.pose("seated", head=-4, lean=-4, brow=1, mouth=2)], [t_e + .8, C.pose("seated", shF=30, elF=110, head=6, brow=-1)],
                                       [dur, C.pose("seated", shF=30, elF=110, head=4, brow=-1)]], dur, t0=.8))
    layers = [lay(z, s, noblur=(k in ("glow",))) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.82, viewer["svg"]))
    layers.append(lay(.85, layers_["table"][1]))
    lx, ly = anc["laptop"]
    cam = [[0, _zx(900, .85), _zy(640, .85), .95], [t_c - .4, _zx(lx, .85), _zy(ly - 240, .85), 1.5, "inout"], [t_e + .8, _zx(lx + 20, .85), _zy(ly - 240, .85), 1.6, "sine"],
           [dur, _zx(900, .85), _zy(620, .85), 1.15, "inout"]]
    over = [title("October 2001", "The results", w, h, d=min(2.6, t_c - .3)), badge("Our illustration · figures from the US Senate report", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[viewer], cam=cam, focus=[[0, .85]], dof=4, shake=.25, over=over, grade="warm", vig=1.15, tin=("dissolve", .35))
    import sfx
    foley = [("tick", t, .3, 0) for t in (t_c, t_e)] + [("hit", t_c + .9, .3, 0, dict(pitch=160))]
    amb = sfx.room_tone(dur + .5, seed=821, clock=False, street=.2) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_restate(w, h, dur, ctx):
    """8 November 2001 in the office (our illustration). The wall screen draws Enron's net income as reported and as
    restated for 1997 to 2000, $ million, on one true scale (Form 8-K, 8 Nov 2001, Table 1: reported 105, 703, 893,
    979; restated 9, 590, 643, 847): the reported bars draw as 'restate' is said, the restated bars on 'fell', the
    1997 pair last flagged. An analyst walks to the screen and stops."""
    t_rep = max(1.0, find_t(ctx, "restate") + .2)
    t_res = max(t_rep + 1.6, find_t(ctx, "fell") - .2)
    sc = .64                                                                            # px per $m
    rows = [("1997", 105, 9), ("1998", 703, 590), ("1999", 893, 643), ("2000", 979, 847)]
    scr = (_t(40, 50, "ENRON · NET INCOME · $ MILLION", 24, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + _t(40, 76, "AS REPORTED (GREY) AND RESTATED (TEAL) · FORM 8-K, NOVEMBER 8, 2001", 15, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"'))
    for k, (yr, a, b) in enumerate(rows):
        y = 112 + k * 96
        scr += _t(40, y + 46, yr, 26, fill=LIGHT, anchor="start", family="Sans", weight=700)
        for j, (v, col, t) in enumerate(((a, "#5E7378", t_rep + .25 * k), (b, TEAL, t_res + .3 * k))):
            yy = y + j * 40
            wpx = max(v * sc, 3)
            scr += (f'<rect x="130" y="{yy}" width="{wpx:.0f}" height="34" fill="{col}" {C.kv(width=[[0, 0], [t - .01, 0], [t + .7, round(wpx), "out"]])}/>'
                    + _ktf(_t(130 + wpx + 12, yy + 27, f"${v}M", 22, fill=LIGHT if j == 0 else "#9FE0D2", anchor="start", family="Sans", weight=700), t + .6, .25))
    scr += _ktf(_r(560, 112, 300, 40, RED, rx=20, sw=0) + _t(710, 140, "1997: $105M TO $9M", 20, fill="#fff", family="Sans", weight=700), t_res + 1.6, .3)
    layers_, anc = bank_office_today(screen=scr, seed=93, front_monitor=False)
    feet = anc["feet"]
    walker = C.actor("rs_a", "staff_2001", pos=[[0, -260, feet], [t_rep - .4, -260, feet], [t_rep + 2.0, 400, feet, "inout"], [dur, 420, feet]],
                     scale=1.0, seed=291, dir=1,
                     pose_keys=_alive([[0, C.pose("relaxed", head=-4)], [t_rep + 2.1, C.pose("relaxed", head=-14, eyeY=-1)],
                                       [t_res + 1.6, C.pose("point", head=-16)], [t_res + 2.8, C.pose("concern", head=-12)], [dur, C.pose("concern", head=-10)]], dur, t0=t_res + 3.0))
    sitters = [C.actor(f"rs_s{i}", look, pos=[[0, x, 1000]], scale=.92, seed=300 + i, dir=1 if i == 0 else -1, walk=False,
                       pose_keys=_alive([[0, C.pose("seated", head=10, eyeY=1)], [t_res + .2 * i, C.pose("seated", head=10, eyeY=1)],
                                         [t_res + .5 + .2 * i, C.pose("seated", head=-12, lean=-4, brow=.6)], [dur, C.pose("seated", head=-10)]], dur, t0=.6 + i))
               for i, (x, look) in enumerate(((60, "dir_2001d"), (1420, "office_2023c")))]
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k not in ("back", "front")]
    layers.append(lay(.62, layers_["back"][1]))
    layers.append(lay(.7, "".join(a["svg"] for a in [walker] + sitters)))
    layers.append(lay(.86, layers_["front"][1]))
    sx, sy = anc["wall_screen"]
    cam = [[0, 900, 560, .9], [t_rep - .3, _zx(sx - 80), _zy(sy), 1.12, "inout"], [t_res + .2, _zx(sx - 40), _zy(sy - 10), 1.22, "inout"],
           [dur, _zx(sx - 30), _zy(sy - 10), 1.26, "sine"]]
    over = [title("November 8, 2001", "The restatement", w, h, d=min(2.8, t_rep + .4)), badge("Our illustration · figures from Enron's Form 8-K", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[walker] + sitters, cam=cam, focus=[[0, .55]], dof=3, shake=.2, over=over, grade="cool", vig=1.05,
                tin=("dissolve", .35))
    import sfx
    foley = [("tick", t_rep + .25 * k + .1, .22, -.2) for k in range(4)] + [("tick", t_res + .3 * k + .1, .25, .2) for k in range(4)]
    foley += [("hit", t_res + 1.7, .35, 0, dict(pitch=140))] + [("step", t, .05, -.3) for t in C.footsteps(walker, dur)][:10]
    amb = sfx.room_tone(dur + .5, seed=931, clock=False, street=.12) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_collapse(w, h, dur, ctx):
    """2 December 2001 (reconstruction, not Enron's real street or building): a city street at night; the billboard
    says DECEMBER 2, 2001 · ENRON FILES FOR CHAPTER 11 (Britannica: "On December 2, 2001, Enron filed for Chapter 11
    bankruptcy protection") with the last sourced print, $0.26 at the close on 30 Nov; people walk out carrying
    cardboard boxes, others pass on their phones."""
    t_b = max(.8, find_t(ctx, "December") - .2)
    bb = (_t(450, 96, "DECEMBER 2, 2001", 44, fill=LIGHT, family="Sans", weight=700, extra='letter-spacing="4"')
          + kt(_t(450, 196, "ENRON FILES FOR", 46, fill=LIGHT, family="Serif", weight=700) + _t(450, 262, "CHAPTER 11", 74, fill=RED, family="Serif", weight=700),
               None, t_b, .4)
          + _t(450, 330, "SHARES AT THE CLOSE ON NOV 30: $0.26", 20, fill=MUSTARD, family="Sans", weight=700, extra='letter-spacing="2"'))
    layers_, anc = street_today(night=True, seed=29, billboard=bb)
    feet = anc["feet"]
    carriers = []
    for i in range(4):
        t0 = .2 + i * 1.3
        x0, v = (-500, 110) if i % 2 == 0 else (2500, -100)
        carriers.append(C.actor(f"cb{i}", DIR_LOOKS[(i + 1) % len(DIR_LOOKS)],
                                pos=[[0, x0, feet + (i % 2) * 12], [t0, x0, feet + (i % 2) * 12], [dur + 1, x0 + v * (dur + 1 - t0), feet + (i % 2) * 12, "lin"]],
                                scale=1.0, seed=320 + i, dir=1 if v > 0 else -1, holdF=box_prop(),
                                pose_keys=[[0, C.pose("relaxed", shF=64, elF=70, shB=58, elB=72, head=10, eyeY=1)]]))
    _, cr = L.crowd(4, (-600, 2600), feet, .95, z_seed=19, looks=STREET_LOOKS, speed=(60, 90), dur=dur + 1, talkers=0, prefix="cl")
    ppl = carriers + _readers(cr, STREET_LOOKS, every=2)
    layers = [lay(z, s, noblur=(k in ("light", "sky"))) for k, (z, s) in layers_.items()]
    layers.insert(len(layers) - 1, lay(.76, "".join(a["svg"] for a in ppl)))
    cam = [[0, 960, 560, .9], [t_b - .3, 960, 470, 1.04, "inout"], [t_b + 2.0, 970, 480, 1.06, "sine"], [dur, 980, 600, .9, "inout"]]
    over = [badge("Reconstruction · not the real street or building", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, .5], [t_b + 2.2, .5], [dur, .76]], dof=4, shake=.3, over=over, grade="cool",
                vig=1.15, tin=("dissolve", .35))
    import sfx
    foley = [("hit", t_b + .1, .35, 0, dict(pitch=120))] + [("step", t, .06, -.2) for a in ppl[:4] for t in C.footsteps(a, dur)][:22]
    amb = sfx.city_ambience(dur + .5, seed=291, night=True, traffic=.4) * .6
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_mtm_term(w, h, dur, ctx):
    """23 Nov (motion: the quietest 6 s window of the first cut, 0.50 at 1:32, was this beat drawn). Mark to market as
    Britannica describes it ("allowed the company to write unrealized future gains from some trading contracts into
    current income statements"), on an office wall screen (our illustration): three contract cards marked FUTURE GAINS
    appear on the first sentence, MARK TO MARKET types on its words, and on 'current income' the cards slide left into
    the CURRENT INCOME box, which counts them in. An analyst walks to the screen."""
    t_cards = .6
    t_term = max(t_cards + 1.0, find_t(ctx, "mark to market") - .1)
    t_move = max(t_term + 1.2, find_t(ctx, "current income") - .4)
    card = lambda k: (_r(0, 0, 230, 96, "#5E7378", rx=8, sw=0) + _t(115, 40, f"CONTRACT {'ABC'[k]}", 22, fill=LIGHT, family="Sans", weight=700, extra='letter-spacing="2"')
                      + _t(115, 74, "FUTURE GAINS", 18, fill=MUSTARD, family="Sans", weight=700, extra='letter-spacing="2"'))
    cards = ""
    for k in range(3):
        x0, y0 = 600, 130 + k * 116
        x1, y1 = 120 + k * 14, 250 + k * 22
        tr = [[0, x0, y0], [t_move + .15 * k, x0, y0], [t_move + .15 * k + .9, x1, y1, "inout"]]
        cards += f'<g {C.kv(translate=tr)}>' + _ktf(card(k), t_cards + .3 * k, .3) + "</g>"
    scr = (_ktf(_t(40, 64, "MARK TO MARKET", 40, fill=LIGHT, anchor="start", family="Serif", weight=700), t_term, .3)
           + _ktf(_t(40, 96, "ENCYCLOPAEDIA BRITANNICA'S DESCRIPTION · OUR ILLUSTRATION", 15, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"'), t_term + .3, .3)
           + _r(60, 200, 340, 230, "none", rx=12, sw=0) + f'<rect x="60" y="200" width="340" height="230" rx="12" fill="none" stroke="{TEAL}" stroke-width="5" stroke-dasharray="12 8"/>'
           + _t(230, 470, "CURRENT INCOME", 26, fill="#9FE0D2", family="Sans", weight=700, extra='letter-spacing="3"')
           + cards
           + _ktf(_r(560, 470, 380, 46, RED, rx=23, sw=0) + _t(750, 502, "UNREALISED GAINS", 22, fill="#fff", family="Sans", weight=700, extra='letter-spacing="3"'), t_move + 1.4, .3))
    layers_, anc = bank_office_today(screen=scr, seed=95, front_monitor=False)
    feet = anc["feet"]
    an = C.actor("mtt", "staff_2001", pos=[[0, 2300, feet], [.4, 2300, feet], [3.0, 1640, feet, "inout"], [dur, 1620, feet]], scale=1.0, seed=275, dir=-1,
                 pose_keys=_alive([[0, C.pose("relaxed")], [3.1, C.pose("relaxed", head=-12)], [t_move, C.pose("point", head=-14)], [t_move + 1.4, C.pose("relaxed", head=-10)],
                                   [dur, C.pose("relaxed", head=-8)]], dur, t0=3.4, every=1.8))
    ppl = []
    for i in range(3):
        t0 = .3 + i * (dur / 3.2)
        x0, v = (-700, 140) if i % 2 == 0 else (2600, -130)
        ppl.append(C.actor(f"mtw{i}", ["office_2023", "dir_2001d", "office_2023c"][i], pos=[[0, x0, feet + 20], [t0, x0, feet + 20], [dur + 1, x0 + v * (dur + 1 - t0), feet + 20, "lin"]],
                           scale=.95, seed=280 + i, dir=1 if v > 0 else -1, amp=22))
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k not in ("back", "front")]
    layers.append(lay(.62, layers_["back"][1]))
    layers.append(lay(.7, "".join(a["svg"] for a in [an] + ppl)))
    layers.append(lay(.86, layers_["front"][1]))
    sx, sy = anc["wall_screen"]
    cam = [[0, 940, 580, .9], [t_term - .3, _zx(sx - 40), _zy(sy), 1.12, "inout"], [t_move + .2, _zx(sx - 160), _zy(sy + 10), 1.22, "inout"], [dur, _zx(sx - 120), _zy(sy), 1.2, "sine"]]
    over = [title("Houston, the late 1990s", "How Enron counted", w, h, d=min(2.6, t_term - .2)), badge("Our illustration · Britannica's description", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[an] + ppl, cam=cam, focus=[[0, .55]], dof=3, shake=.2, over=over, grade="warm", vig=1.05, tin=("dissolve", .35))
    import sfx
    foley = [("tick", t_cards + .3 * k, .2, .2, dict(tock=True)) for k in range(3)] + [("tick", t_term, .3, 0)]
    foley += [("tick", t_move + .15 * k + .9, .22, -.2, dict(tock=True)) for k in range(3)] + [("hit", t_move + 1.4, .3, 0, dict(pitch=160))]
    foley += [("step", t, .05, .3) for t in C.footsteps(an, dur)][:8]
    amb = sfx.room_tone(dur + .5, seed=951, clock=False, street=.12) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_round_trip(w, h, dur, ctx):
    """23 Nov (motion: the second quietest window of the first cut, 0.60 at 5:06, was this beat drawn). The Powers
    report's point ("Enron never escaped the risk of loss, because it had provided the bulk of the capital with which
    the SPEs would pay Enron") drawn as a loop on the boardroom display (our illustration): ENRON, an arrow ENRON STOCK
    to THE RAPTORS draws on 'provided', the arrow back PAYS ENRON draws on 'pay', then THE SAME MONEY, ROUND TRIP lands;
    the presenter points along it and the directors look up."""
    t_a = max(1.0, find_t(ctx, "provided") - .2)
    t_b = max(t_a + 1.2, find_t(ctx, "would pay") - .2)
    t_c = t_b + 1.2
    box = lambda x, y, txt, col: _r(x, y, 300, 120, col, rx=14, sw=0) + _t(x + 150, y + 74, txt, 34, fill="#fff", family="Sans", weight=700, extra='letter-spacing="3"')
    arc = lambda d, t: (f'<path d="{d}" fill="none" stroke="{MUSTARD}" stroke-width="9" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" '
                        f'{C.kv(dash=[[0, 0], [t, 0], [t + .9, 1]])}/>')
    scr = (_t(500, 54, "THE DRAWBACK · THE POWERS REPORT, 2002", 22, fill=DIM, family="Sans", weight=700, extra='letter-spacing="3"')
           + box(60, 200, "ENRON", RED) + box(640, 200, "RAPTORS", "#5E7378")
           + arc("M360,230 C440,120 560,120 640,230", t_a) + _ktf(_t(500, 128, "ENRON STOCK", 24, fill=MUSTARD, family="Sans", weight=700, extra='letter-spacing="2"'), t_a + .6, .3)
           + arc("M640,300 C560,420 440,420 360,300", t_b) + _ktf(_t(500, 430, "PAYS ENRON", 24, fill=MUSTARD, family="Sans", weight=700, extra='letter-spacing="2"'), t_b + .6, .3)
           + _ktf(_r(250, 470, 500, 48, TEAL, rx=24, sw=0) + _t(500, 503, "THE SAME MONEY, ROUND TRIP", 22, fill="#fff", family="Sans", weight=700, extra='letter-spacing="3"'), t_c, .3))
    layers_, anc = boardroom_2001(screen=scr, seed=79, dusk=True)
    ppl = directors(anc, dur, react_at=t_c, seats=(0, 2, 5, 6), seed=240, prefix="rt")
    pres = C.actor("rt_p", "staff_2001", pos=[[0, 1700, 960]], scale=.98, seed=243, dir=-1, walk=False,
                   pose_keys=_alive([[0, C.pose("relaxed", head=6)], [t_a, C.pose("point", head=-6)], [t_a + 1.2, C.pose("relaxed", head=-2)],
                                     [t_b, C.pose("point", head=-8)], [t_b + 1.2, C.pose("relaxed", head=6)], [dur, C.pose("concern", head=8)]], dur, t0=1.0, every=1.9))
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.66, pres["svg"]))
    layers.append(lay(.8, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.85, layers_["table"][1]))
    sx, sy = anc["screen"]
    cam = [[0, 960, 560, .88], [t_a - .4, _zx(sx - 20), _zy(sy), 1.18, "inout"], [t_b + 1.0, _zx(sx + 20), _zy(sy + 10), 1.24, "sine"], [dur, 980, 540, 1.0, "inout"]]
    over = [badge("Our illustration · the Powers report's finding", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl + [pres], cam=cam, focus=[[0, .4]], dof=4, shake=.2, over=over, grade="dusk", vig=1.1, tin=("dissolve", .35))
    import sfx
    foley = [("tick", t_a + .1, .3, -.2), ("tick", t_b + .1, .3, .2), ("hit", t_c + .1, .3, 0, dict(pitch=170))]
    amb = sfx.room_tone(dur + .5, seed=791, clock=False, street=.1) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


SHOTS = dict(hook_27bn=shot_hook_27bn, share_path=shot_share_path, revenue_jump=shot_revenue_jump, waiver_1=shot_waiver, waiver_2=shot_waiver_2,
             mtm_1=shot_mtm, mtm_2=shot_mtm_2, three_pct=shot_three_pct, raptor_1=shot_raptor, raptor_2=shot_raptor_2, charge_oct=shot_charge_oct,
             restate=shot_restate, collapse=shot_collapse,
             mtm_term=shot_mtm_term, round_trip=shot_round_trip, mtm=shot_mtm_both)


if __name__ == "__main__":
    # stills for a quick look: python3 build/cine_2001.py [name ...]
    names = sys.argv[1:] or list(SHOTS)
    work = C.OUT / "cine-2001-stills"
    work.mkdir(parents=True, exist_ok=True)
    demo = dict(segs=[("Of the company's sixty billion, ninety dollars, ten dollars a year for ten years, a fund, three percent, restate.", .3, 3.6),
                      ("It falls to sixty, the partner owes forty, this year, seven hundred and ten, fell, ratified, all ten.", 3.8, 7.6),
                      ("Twenty six cents, seventy percent, can't pay, one point two, seventy seven dollars, December, forty, hundred.", 7.8, 11.0),
                      ("So why did the board let it go on?", 11.2, 14.0)])
    for nm in names:
        built = SHOTS[nm](1920, 1080, 15.0, demo)
        html, total = C.film_html(built["shots"], 1920, 1080)
        print(nm, [p.name for p in C.stills(html, [0.2, 1.6, total * .4, total * .7, total - .3], work, nm)])
