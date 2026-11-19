"""
Filmed beats for YouTube #13, GameStop, January 2021 (19 Nov 2026). Sets, props and shots for build/cine.py, used by
build/youtube_ep013.py as kind="cine" beats (cinematic-standard.md section 8: step 3, sets, the first present-day
rooms and the "city street today" the build order named next; step 4, data in the world: a board that counts the
same shares sold twice, a laptop whose sourced price prints land as they are said).

Sets (our own generic drawings; no real firm, app, building, logo or person is copied; everything is badged):
  street_today(night)   a city street of today: glass and brick towers with lit windows, shopfronts, a bus shelter,
                        modern street lamps, a traffic light that changes, a digital billboard that takes content
  kitchen_2021(night)   a small kitchen at night or early morning: a window on the city, a pendant lamp, a table with
                        a laptop whose screen takes content, a mug that steams, a phone that buzzes
  ops_room_dawn()       an operations room before dawn: a window going from night to dawn, a wall clock that moves,
                        a desk with a big monitor that takes content and a phone that rings
Props: phone_screen() (a phone's face, our illustration of a trading app: no name, no logo), hand_phone() (a hand
holding a phone, big, for close-ups), notice_screen() (an automated notice typing in, sourced figures only),
prints_chart() (sourced price prints on a true time axis, dashed where nothing is sourced).
2021 looks (cine.LOOKS): hoodie_2021, tee_2021, jacket_2021, coat_2021, lady_2021, lady_2021b, ops_2021.

Shots (fn(w, h, dur, ctx) -> dict(shots, foley, amb); ctx["segs"] are the beat's sentences, (text, start, end)):
  hook_109      the hook: 109% counts up on a phone from the first frame; the phone lowers and the camera pulls back
                onto a night street of people on their phones
  lend_twice    the puzzle: one bundle of 100 shares passes from an owner to a short seller to a second owner, is
                lent again, and sold to a third; tags OWNS / OWES appear over each; a billboard counts SHARES THAT EXIST
                100, SOLD SHORT 0 -> 100 -> 200, COUNTED AS OWNED 100 -> 200 -> 300
  laptop_prints January 22 to 27, 2021 at a kitchen table at night: the laptop's chart lands each sourced price as
                it is said (open and close of the 22nd, close of the 27th); the viewer's brows go up
  dawn_notice   5:11 a.m., 28 January 2021 (reconstruction): the clock, the phone rings, the monitor types the
                notice: on deposit $696m, shortfall about $3bn
  buy_grey      our illustration of an app: BUY goes grey (position closing only); a thumb taps BUY, nothing; SELL works
Facts on screen come only from the sources in youtube_ep013.py's docstring. Nobody in a shot speaks, and nobody is
a likeness or a portrait of anyone at GameStop, Robinhood, the NSCC, a fund or Reddit.
"""

import math
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402
from cine_1907 import lay, badge, seg_t, word_t   # noqa: E402
from cine_1920 import title                       # noqa: E402
from cine_1971 import kt, board_rows_svg, desk_phone   # noqa: E402
from cine_1974 import wall_clock                  # noqa: E402

INK, RED, TEAL, MUSTARD, PAPER = C.INK, C.RED, C.TEAL, C.MUSTARD, "#F7F5F2"
GLASS, SCREEN = "#0E1A22", "#101418"
_r, _t = L._r, L._t

C.LOOKS.update({
    # 19 Nov, YouTube #13 (2021): hoodies, T-shirts, jackets, a winter coat. Generic clothes, nobody's likeness. A
    # "tie" the colour of the shirt reads as no tie.
    "hoodie_2021": dict(coat="#3E4A5C", coat2="#2E3846", vest="#3E4A5C", legs="#2F3440", stock="#2F3440", shoe="#E8E4DC", skin="#E5B391",
                        hair="#3A2A20", hat="", style="suit", cuff="#3E4A5C", tie="#3E4A5C", era="1971"),
    "tee_2021": dict(coat="#C9733A", coat2="#A85E2E", vest="#F1EEE6", legs="#3B4A66", stock="#3B4A66", shoe="#F2F2F2", skin="#8D5A3B",
                     hair="#14100D", hat="", style="suit", cuff="#C9733A", tie="#F1EEE6", era="1971"),
    "jacket_2021": dict(coat="#2E5A4E", coat2="#224539", vest="#E8E4DC", legs="#2B2B30", stock="#2B2B30", shoe=INK, skin="#F0C7A4",
                        hair="#8A6A4A", hat="", style="suit", cuff="#E8E4DC", tie="#E8E4DC", era="1971"),
    "coat_2021": dict(coat="#6B5A4A", coat2="#544638", vest="#D9D2C6", legs="#2F2F34", stock="#2F2F34", shoe=INK, skin="#C98E68",
                      hair="#1E1410", hat="", style="long", cuff="#D9D2C6", era="1971"),
    "lady_2021": dict(coat="#7A3B4A", coat2="#5E2D39", vest="#F4EFE4", legs="#2F3440", stock="#2F3440", shoe=INK, skin="#F1CBAA",
                      hair="#5A3A28", hat="", style="suit", cuff="#7A3B4A", tie="#F4EFE4", era="1971"),
    "lady_2021b": dict(coat="#D9A441", coat2="#B8882F", vest="#F4EFE4", legs="#2B2B30", stock="#2B2B30", shoe=INK, skin="#B97A55",
                       hair="#14100D", hat="", style="suit", cuff="#D9A441", tie="#F4EFE4", era="1971"),
    "ops_2021": dict(coat="#47505A", coat2="#363D45", vest="#E9EEF2", legs="#2B3140", stock="#2B3140", shoe=INK, skin="#E8BC9A",
                     hair="#5A3A28", hat="", style="suit", cuff="#E9EEF2", tie="#E9EEF2", era="1971"),
})
STREET_LOOKS = ["hoodie_2021", "coat_2021", "lady_2021", "tee_2021", "jacket_2021", "lady_2021b", "hoodie_2021", "coat_2021"]


# ------------------------------------------------------------------------------------------------ props

def mini_phone():
    """A phone held in a figure's hand (holdF), its screen lit."""
    return (f'<g transform="translate(0,-6) rotate(-8)">' + _r(-11, -20, 22, 40, INK, rx=4, sw=1.6)
            + f'<rect x="-8" y="-16" width="16" height="30" rx="2" fill="#9FE0D2" data-flick=\'[0.95,0.05,3]\'/></g>')


def phone_screen(w, h, body="", head="", sub=""):
    """A phone's face (w x h, origin top left), our illustration of a trading app: no name, no logo. body: SVG in
    the screen's own coordinates, drawn under an optional header."""
    out = (f'<rect width="{w}" height="{h}" rx="{w * .12:.0f}" fill="{INK}"/>'
           f'<rect x="{w * .05:.0f}" y="{w * .05:.0f}" width="{w * .9:.0f}" height="{h - w * .1:.0f}" rx="{w * .09:.0f}" fill="{SCREEN}"/>'
           f'<rect x="{w * .38:.0f}" y="{w * .08:.0f}" width="{w * .24:.0f}" height="{w * .05:.0f}" rx="{w * .025:.0f}" fill="#000"/>')
    if head:
        out += _t(w * .12, w * .32, head, w * .085, fill="#F4F1EA", anchor="start", family="Sans", weight=700)
    if sub:
        out += _t(w * .12, w * .42, sub, w * .045, fill="#8FA3A8", anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
    return out + body + f'<rect width="{w}" height="{h}" rx="{w * .12:.0f}" fill="none" stroke="#000" stroke-width="5"/>'


def hand_phone(w=560, h=1080, body="", head="", sub="", skin="#E5B391", sleeve="#3E4A5C"):
    """A big hand holding a phone upright, for close-ups (origin: the phone's top left). The thumb rests on the
    phone's left edge; the fingers wrap the right edge; a sleeve below."""
    ph = phone_screen(w, h, body, head, sub)
    hand = (f'<path d="M{w * .9:.0f},{h * .55:.0f} C{w * 1.08:.0f},{h * .56:.0f} {w * 1.1:.0f},{h * .9:.0f} {w * .98:.0f},{h * 1.08:.0f} '
            f'L{w * .1:.0f},{h * 1.12:.0f} C{-w * .1:.0f},{h * .98:.0f} {-w * .1:.0f},{h * .78:.0f} {w * .02:.0f},{h * .7:.0f} Z" fill="{skin}" stroke="{INK}" stroke-width="5"/>')
    fingers = "".join(f'<rect x="{w * .9:.0f}" y="{h * (.6 + .08 * k):.0f}" width="{w * .16:.0f}" height="{h * .07:.0f}" rx="{h * .035:.0f}" fill="{skin}" stroke="{INK}" stroke-width="4"/>'
                      for k in range(4))
    thumb = (f'<path d="M{w * .02:.0f},{h * .62:.0f} C{-w * .08:.0f},{h * .54:.0f} {-w * .02:.0f},{h * .44:.0f} {w * .05:.0f},{h * .48:.0f} '
             f'L{w * .08:.0f},{h * .64:.0f} Z" fill="{skin}" stroke="{INK}" stroke-width="4"/>')
    sl = _r(-w * .02, h * 1.06, w * 1.06, h * .6, sleeve, rx=30, sw=5)
    return sl + hand + ph + fingers + thumb


def prints_chart(x0, y0, w, h, prints, t_of, vmax=400, day0=20, day1=32, label_size=20):
    """Sourced price prints on a true time axis (days of January 2021; day 32 = 1 February). prints: [(day, value,
    label)]; t_of: the shot second each lands. Nothing joins them but a faint dashed line, because nothing between
    them is sourced. The y axis is in dollars from 0."""
    X = lambda d: x0 + w * (d - day0) / (day1 - day0)
    Y = lambda v: y0 + h - h * v / vmax
    s = f'<path d="M{x0},{y0 + h} L{x0 + w},{y0 + h} M{x0},{y0} L{x0},{y0 + h}" stroke="#8FA3A8" stroke-width="2"/>'
    for v in range(100, vmax + 1, 100):
        s += f'<path d="M{x0},{Y(v):.0f} L{x0 + w},{Y(v):.0f}" stroke="#8FA3A8" stroke-width="1" opacity=".3"/>'
        s += _t(x0 - 10, Y(v) + 7, f"${v}", label_size, fill="#8FA3A8", anchor="end", family="Sans", weight=600)
    for d, lab in ((22, "JAN 22"), (25, "25"), (27, "27"), (29, "29"), (32, "FEB 1")):
        s += f'<path d="M{X(d):.0f},{y0 + h} L{X(d):.0f},{y0 + h + 8}" stroke="#8FA3A8" stroke-width="2"/>'
        s += _t(X(d), y0 + h + 34, lab, label_size, fill="#8FA3A8", family="Sans", weight=600)
    pts = [(X(p[0]), Y(p[1])) for p in prints]
    for k in range(1, len(pts)):
        (ax, ay), (bx, by) = pts[k - 1], pts[k]
        s += (f'<path d="M{ax:.0f},{ay:.0f} L{bx:.0f},{by:.0f}" stroke="#F6D58A" stroke-width="3" stroke-dasharray="6 10" '
              f'{C.kv(opacity=[[0, 0], [t_of[k] - .05, 0], [t_of[k] + .3, .8]])}/>')
    for k, ((px, py), pr) in enumerate(zip(pts, prints)):
        lab = pr[2]
        dx, dy, anc = pr[3] if len(pr) > 3 else (14, -24, "start")      # label offset from the point
        s += kt(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="9" fill="{RED}" stroke="#F4F1EA" stroke-width="3"/>'
                + (f'<path d="M{px:.0f},{py:.0f} L{px + dx * .8:.0f},{py + dy * .8:.0f}" stroke="#F4F1EA" stroke-width="1.5" opacity=".6"/>' if abs(dy) > 30 else "")
                + _t(px + dx, py + dy, lab, label_size + 4, fill="#F4F1EA", anchor=anc, family="Sans", weight=700), None, t_of[k], .35)
    s += _t(x0 + w, y0 - 14, "SOURCED PRINTS ONLY · SEC STAFF REPORT, 2021", label_size - 4, fill="#8FA3A8", anchor="end", family="Sans", weight=600,
            extra='letter-spacing="2"')
    return s


def laptop(x, y, sw=620, sh=380, screen=""):
    """An open laptop standing on a table at (x, y = table top); screen: SVG in its own box (0..sw, 0..sh)."""
    return (f'<g transform="translate({x - sw / 2 - 20},{y - sh - 60})">'
            + _r(0, 0, sw + 40, sh + 40, "#2B2F36", rx=16, sw=3.4)
            + f'<g transform="translate(20,20)"><rect width="{sw}" height="{sh}" rx="4" fill="{SCREEN}"/>{screen}'
            + f'<rect width="{sw}" height="{sh}" fill="#9FE0D2" opacity=".04" data-flick=\'[0.04,0.02,2]\'/></g>'
            + f'<path d="M-40,{sh + 40} L{sw + 80},{sh + 40} L{sw + 50},{sh + 60} L-10,{sh + 60} Z" fill="#9AA0A8" stroke="{INK}" stroke-width="3"/></g>')


def notice_screen(w, h, rows, t_rows, t_head=.3):
    """An automated notice on a monitor: a header, then rows that type in at their times. rows: (label, value,
    colour, count keys or None)."""
    s = kt(_t(40, 64, "CLEARING HOUSE · AUTOMATED NOTICE", 30, fill="#F4F1EA", anchor="start", family="Sans", weight=700), None, t_head, .25)
    s += kt(_t(40, 104, "05:11 ET · JANUARY 28, 2021 · OUR ILLUSTRATION OF THE NOTICE", 18, fill="#8FA3A8", anchor="start", family="Sans", weight=600,
               extra='letter-spacing="2"'), None, t_head + .2, .25)
    for k, ((lab, val, col, keys), t) in enumerate(zip(rows, t_rows)):
        y = 190 + 78 * k
        row = _t(40, y, lab, 28, fill="#C9D4D6", anchor="start", family="Sans", weight=600)
        if keys:
            row += (f'<text x="{w - 40}" y="{y}" text-anchor="end" font-family="\'Sans\',sans-serif" font-weight="700" font-size="40" fill="{col}" '
                    f'{C.kv(count=keys)} data-dec="0" data-pre="$" data-suf="{val}">$0{val}</text>')
        else:
            row += _t(w - 40, y, val, 40, fill=col, anchor="end", family="Sans", weight=700)
        s += kt(row, None, t, .2)
    return s


# ------------------------------------------------------------------------------------------------ sets

def _tower(x, w, top, base, body, lit, rng, cols=None, glass=False):
    s = f'<rect x="{x:.0f}" y="{top:.0f}" width="{w:.0f}" height="{base - top:.0f}" fill="{body}" stroke="{INK}" stroke-width="3"/>'
    cols = cols or max(2, int(w // 46))
    rows = int((base - top - 30) // 44)
    for r in range(rows):
        for c in range(cols):
            wx = x + 14 + c * (w - 28) / cols
            wy = top + 18 + r * 44
            on = rng.random() < lit
            col = "#F6D58A" if on else ("#2B3548" if glass else "#3A3F4A")
            op = rng.uniform(.55, .95) if on else .9
            extra = f' data-flick=\'[{op:.2f},0.05,{rng.randint(0, 9)}]\'' if on else ""
            s += f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{(w - 28) / cols - 10:.0f}" height="26" fill="{col}" opacity="{op:.2f}"{extra}/>'
    return s


def street_today(night=True, seed=21, billboard=""):
    """A city street of today. Layers (z): sky .15, far towers .3, near buildings with shopfronts and the billboard
    .5, light .55, pavement .6, furniture (lamps, shelter, traffic light) .7. People walk at y 1010 (z .74 to .8).
    billboard: SVG drawn in the billboard's box (0..900, 0..380), centred at x 960, y 210 on the z .5 layer.
    Returns (layers, anchors)."""
    rng = random.Random(seed)
    top, bot = ("#141B2E", "#3A4466") if night else ("#AFC6D6", "#E6ECEC")
    sky = C.defs() + (f'<defs><linearGradient id="sky21{seed}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
                      f'<stop offset="1" stop-color="{bot}"/></linearGradient></defs>'
                      f'<rect x="-2400" y="-1200" width="7200" height="2600" fill="url(#sky21{seed})"/>')
    if night:
        sky += "".join(f'<circle cx="{rng.uniform(-2000, 4000):.0f}" cy="{rng.uniform(-600, 300):.0f}" r="{rng.uniform(1, 2.4):.1f}" fill="#F4F1EA" '
                       f'data-flick=\'[0.7,0.25,{k % 9}]\'/>' for k in range(60))
    far = ""
    x = -2200
    while x < 4400:
        bw, bh = rng.uniform(160, 320), rng.uniform(380, 900)
        far += _tower(x, bw, 760 - bh, 780, rng.choice(["#2A3246", "#323A52", "#262C3E"]) if night else rng.choice(["#8E9CAA", "#A3AFBA", "#7F8D9B"]),
                      .3 if night else .05, rng, glass=True)
        x += bw + rng.uniform(10, 60)
    near = ""
    x = -1500
    k = 0
    while x < 3500:
        bw = rng.uniform(420, 640)
        body = rng.choice(["#7A4A3A", "#5E5A56", "#8A6A52", "#4E5560"]) if night else rng.choice(["#B8735A", "#9A948C", "#C4A07E", "#8A939E"])
        h_ = rng.uniform(560, 760)
        if abs(x + bw / 2 - 960) < 380 and billboard:
            h_ = 800
        near += _tower(x, bw, 860 - h_, 900, body, .45 if night else .0, rng, cols=4)
        # a shopfront at street level: a lit window, an awning, a door
        sf = rng.choice([TEAL, RED, MUSTARD, "#3E4F66"])
        near += (_r(x + 20, 700, bw - 40, 200, "#1E2228", sw=3) + f'<rect x="{x + 34:.0f}" y="714" width="{bw - 150:.0f}" height="150" '
                 f'fill="{"#F6E7B8" if night else "#D6E2F3"}" opacity="{.85 if night else .9}"/>'
                 + _r(x + bw - 106, 730, 66, 170, "#3A2E28", sw=2.6)
                 + f'<path d="M{x + 10:.0f},700 L{x + bw - 10:.0f},700 L{x + bw - 30:.0f},650 L{x + 30:.0f},650 Z" fill="{sf}" stroke="{INK}" stroke-width="3"/>')
        x += bw + 8
        k += 1
    if billboard:
        near += (f'<g transform="translate(510,20)">' + _r(-16, -16, 932, 412, "#2A2E34", rx=10, sw=4)
                 + f'<rect width="900" height="380" rx="4" fill="{SCREEN}"/>{billboard}'
                 + f'<rect width="900" height="380" fill="#9FE0D2" opacity=".05" data-flick=\'[0.05,0.03,4]\'/></g>')
    light = ""
    if night:
        for lx in range(-1200, 3600, 700):
            light += f'<ellipse cx="{lx}" cy="1010" rx="300" ry="90" fill="url(#glowWarm)" opacity=".55"/>'
    pave = (f'<rect x="-2400" y="900" width="7200" height="160" fill="{"#4A4D52" if night else "#A8A39A"}"/>'
            f'<rect x="-2400" y="1060" width="7200" height="18" fill="{"#6A6D72" if night else "#C9C4BA"}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-2400" y="1078" width="7200" height="600" fill="{"#23262B" if night else "#5A5D62"}"/>')
    pave += "".join(f'<rect x="{x}" y="1180" width="120" height="12" fill="#E8E4DC" opacity=".7"/>' for x in range(-2400, 4800, 260))
    furn = ""
    for lx in range(-1200, 3600, 700):                                                 # modern lamps: a slim pole and an arm
        furn += (f'<path d="M{lx},1060 L{lx},560 L{lx + 90},540" fill="none" stroke="#2A2E34" stroke-width="12" stroke-linecap="round"/>'
                 + _r(lx + 70, 530, 70, 18, "#2A2E34", rx=6, sw=2.4)
                 + (f'<rect x="{lx + 76}" y="546" width="58" height="6" fill="#FFF1C8" data-flick=\'[1,0.03,{lx % 7}]\'/>' if night else ""))
    sx = 1880                                                                           # a bus shelter
    furn += (f'<rect x="{sx}" y="820" width="360" height="240" fill="#BFD3DE" opacity=".25" stroke="#2A2E34" stroke-width="6"/>'
             + _r(sx - 10, 806, 380, 20, "#2A2E34", sw=2.4) + _r(sx + 40, 960, 280, 16, "#5A5F6A", sw=2))
    tl = 260                                                                            # a traffic light that changes
    furn += (f'<path d="M{tl},1060 L{tl},720" stroke="#2A2E34" stroke-width="12"/>' + _r(tl - 26, 620, 52, 140, "#2A2E34", rx=8, sw=2.4)
             + f'<circle cx="{tl}" cy="650" r="15" fill="{RED}" {C.kv(opacity=[[0, 1], [5.0, 1], [5.1, .2], [11, .2], [11.1, 1]])}/>'
             + f'<circle cx="{tl}" cy="690" r="15" fill="{MUSTARD}" opacity=".2"/>'
             + f'<circle cx="{tl}" cy="730" r="15" fill="#3FBF7F" {C.kv(opacity=[[0, .2], [5.0, .2], [5.1, 1], [11, 1], [11.1, .2]])}/>')
    layers = dict(sky=(0.15, sky), far=(0.3, far), near=(0.5, near), light=(0.55, light), pave=(0.6, pave), furn=(0.7, furn))
    return layers, dict(feet=1010, billboard=(960, 210))


def kitchen_2021(night=True, seed=31, screen="", mug_steam=True):
    """A small kitchen: a window on the city (night or early morning), a pendant lamp, a table (top at y 860 on the
    z .85 layer) with a laptop at x 760 whose screen takes content, a mug; the chair at x 1260 (seat y 990).
    Returns (layers, anchors)."""
    rng = random.Random(seed)
    wall = C.defs() + f'<rect x="-1600" y="-900" width="5200" height="2600" fill="{"#C9BBA8" if night else "#E2D6C4"}"/>'
    wall += f'<rect x="-1600" y="-900" width="5200" height="2600" fill="#141B2E" opacity="{.35 if night else 0}"/>'
    wx, wy, ww, wh = 1380, 120, 640, 560
    sky = (f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="{"#1D2638" if night else "#D9C3A0"}"/>')
    x = wx
    while x < wx + ww:
        bw, bh = rng.uniform(40, 90), rng.uniform(150, 420)
        bw = min(bw, wx + ww - x)
        sky += _tower(x, bw, wy + wh - bh, wy + wh, "#2E3A50" if night else "#8E8A86", .35 if night else .05, rng, cols=2)
        x += bw + 4
    wall += sky + (f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#F1EEE6" stroke-width="20"/>'
                   f'<path d="M{wx + ww / 2},{wy} L{wx + ww / 2},{wy + wh}" stroke="#F1EEE6" stroke-width="12"/>')
    for k in range(3):                                                                  # cupboards, left
        wall += _r(-420 + k * 300, 140, 280, 300, "#E8E1D4", rx=6, sw=3) + _r(-420 + k * 300 + 120, 270, 40, 12, "#9A948C", rx=4, sw=1.6)
    wall += _r(-440, 600, 960, 30, "#B9AC9A", sw=3) + _r(-440, 630, 960, 270, "#E8E1D4", sw=3)
    lamp = (f'<path d="M760,-200 L760,330" stroke="{INK}" stroke-width="4"/>'
            f'<g data-swing=\'[0.6,0.4,1,760,-200]\'><path d="M680,400 L840,400 L800,330 L720,330 Z" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
            f'<ellipse cx="760" cy="402" rx="60" ry="10" fill="#FFF1C8"/></g>')
    glow = f'<ellipse cx="760" cy="860" rx="700" ry="260" fill="url(#glowWarm)" opacity="{.7 if night else .35}"/>'
    floor = f'<rect x="-1600" y="900" width="5200" height="800" fill="#8A7A66"/><rect x="-1600" y="900" width="5200" height="800" fill="url(#boards)" opacity=".1"/>'
    chair = _r(1190, 980, 150, 22, "#5E3D27", rx=6, sw=3) + _r(1310, 780, 26, 220, "#5E3D27", rx=8, sw=3) + _r(1200, 1000, 18, 120, "#5E3D27", sw=2.4)
    table = (_r(140, 860, 1240, 34, "#B07A4E", rx=6, sw=3.6) + _r(190, 894, 26, 200, "#8A5E3A", sw=2.6) + _r(1300, 894, 26, 200, "#8A5E3A", sw=2.6)
             + laptop(760, 860, screen=screen)
             + f'<g transform="translate(1130,860)">{L.cup()}</g>'
             + (f'<g data-steam=\'[1130,800,3]\'></g>' if mug_steam else ""))
    layers = dict(wall=(0.4, wall), lamp=(0.5, lamp), glow=(0.52, glow), floor=(0.6, floor), chair=(0.78, chair), table=(0.85, table))
    return layers, dict(table_y=860, seat=(1250, 990), laptop=(760, 860))


def ops_room_dawn(dur, clock_path, screen="", ring_at=(), lift=None, seed=41):
    """An operations room before dawn: a wide window from night to dawn (keyed), a wall clock at x 1560 y 230 on the
    wall (z .45), a desk (top y 860, z .85) with a big monitor at x 820 (screen 900 x 520) and a desk phone at x 1360.
    Returns (layers, anchors)."""
    rng = random.Random(seed)
    wall = C.defs() + '<rect x="-1600" y="-900" width="5200" height="2600" fill="#9CA3A8"/>'
    wx, wy, ww, wh = -700, 80, 1300, 640
    wall += (f'<defs><linearGradient id="dawn21" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A2236"/>'
             f'<stop offset=".7" stop-color="#3A3F5E"/><stop offset="1" stop-color="#C98A6A"/></linearGradient></defs>'
             f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="url(#dawn21)"/>'
             f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="#F2B880" {C.kv(opacity=[[0, 0], [dur, .22]])}/>')
    x = wx
    while x < wx + ww:
        bw, bh = rng.uniform(60, 140), rng.uniform(180, 520)
        bw = min(bw, wx + ww - x)
        wall += _tower(x, bw, wy + wh - bh, wy + wh, "#232B40", .25, rng, cols=2, glass=True)
        x += bw + 6
    for k in range(1, 4):
        wall += f'<path d="M{wx + ww * k / 4:.0f},{wy} L{wx + ww * k / 4:.0f},{wy + wh}" stroke="#5A6068" stroke-width="12"/>'
    wall += f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#5A6068" stroke-width="20"/>'
    wall += wall_clock(1560, 230, 100, clock_path, dur, sec0=rng.randint(0, 50))
    for k in range(4):                                                                  # a row of server lights on a rack, right
        wall += _r(1880 + k * 10, 380 + k * 0, 220, 460, "#2A2E34", rx=6, sw=3) if k == 0 else ""
    for r in range(8):
        for c in range(4):
            wall += f'<circle cx="{1910 + c * 46}" cy="{410 + r * 54}" r="6" fill="{TEAL if (r + c) % 3 else MUSTARD}" data-flick=\'[0.9,0.5,{(r * 4 + c) % 9}]\'/>'
    floor = '<rect x="-1600" y="900" width="5200" height="800" fill="#5A5F66"/>'
    mon_w, mon_h = 900, 520
    mon = (f'<g transform="translate({820 - mon_w / 2 - 20},{860 - mon_h - 110})">' + _r(0, 0, mon_w + 40, mon_h + 40, "#22262C", rx=12, sw=3.4)
           + f'<g transform="translate(20,20)"><rect width="{mon_w}" height="{mon_h}" fill="{SCREEN}"/>{screen}'
           + f'<rect width="{mon_w}" height="{mon_h}" fill="#9FE0D2" opacity=".04" data-flick=\'[0.04,0.02,5]\'/></g>'
           + _r(mon_w / 2 - 20, mon_h + 40, 80, 50, "#22262C", sw=2.6) + _r(mon_w / 2 - 110, mon_h + 86, 260, 20, "#22262C", rx=6, sw=2.6) + "</g>")
    desk = (_r(120, 860, 1500, 36, "#C9C4BA", rx=4, sw=3.6) + _r(160, 896, 1420, 220, "#A9A39A", sw=3) + mon
            + desk_phone(1360, 860, ring_at=ring_at, lift=lift, color="#2A2A2E")
            + f'<g transform="translate(1500,860)">{L.cup()}</g>')
    layers = dict(wall=(0.45, wall), floor=(0.6, floor), desk=(0.85, desk))
    return layers, dict(desk_y=860, seat=(1240, 990), phone_x=1360, monitor=(820, 860 - mon_h / 2 - 90))


# ------------------------------------------------------------------------------------------------ shots

def shot_hook_109(w, h, dur, ctx):
    """The hook. Frame 0: a phone fills the frame and its number counts to 109% within 1.4 s (short interest as a share
    of shares outstanding, 31 Dec 2020: SEC staff report 2021, p. 26, 109.26%). On the question the phone lowers out
    of frame and the camera pulls back onto a night street where people walk and look at their phones."""
    t_q = min(dur - 3.0, max(3.5, seg_t(ctx, 2, 0.0) - .4))
    body = (_t(560 * .12, 560 * .62, "SHORT INTEREST", 40, fill="#8FA3A8", anchor="start", family="Sans", weight=700, extra='letter-spacing="3"')
            + f'<text x="{560 * .1:.0f}" y="{560 * 1.0:.0f}" font-family="\'Serif\',serif" font-weight="700" font-size="165" fill="{RED}" '
              f'{C.kv(count=[[0, 100], [.15, 100], [1.4, 109, "out"]])} data-dec="0" data-suf="%">109%</text>'
            + _t(560 * .12, 560 * 1.18, "OF ALL ITS SHARES", 40, fill="#F4F1EA", anchor="start", family="Sans", weight=700)
            + _t(560 * .12, 560 * 1.28, "DECEMBER 31, 2020", 30, fill="#8FA3A8", anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
            + f'<path d="M{560 * .12:.0f},{560 * 1.45:.0f} L{560 * .88:.0f},{560 * 1.45:.0f}" stroke="#2E3A40" stroke-width="3"/>'
            + _t(560 * .12, 560 * 1.54, "SOLD SHORT:", 34, fill="#F4F1EA", anchor="start", family="Sans", weight=600)
            + kt(_t(560 * .12, 560 * 1.64, "MORE THAN EXIST", 38, fill=MUSTARD, anchor="start", family="Sans", weight=700), None, 1.6, .4)
            + _t(560 * .12, 560 * 1.77, "SEC STAFF REPORT, 2021", 24, fill="#5E7378", anchor="start", family="Sans", weight=600, extra='letter-spacing="2"'))
    hp = hand_phone(560, 1080, body=body, head="GME", sub="GAMESTOP CORP.")
    ph = (f'<g {C.kv(translate=[[0, 712, 40, -2], [t_q, 712, 50, -1], [t_q + 1.4, 780, 1500, 8, "inout"], [dur, 780, 1500, 8]])}>'
          f'<g transform="scale(.88)">{hp}</g></g>')
    layers_, anc = street_today(night=True, seed=21)
    cr_svg, cr = L.crowd(8, (-500, 2500), anc["feet"], .95, z_seed=5, looks=STREET_LOOKS, speed=(45, 80), dur=dur + 1, talkers=0, prefix="hs")
    # every other walker reads a phone: rebuild those with a phone in hand and a reading pose
    ppl = []
    for i, a in enumerate(cr):
        if i % 2 == 0:
            sp = a["spec"]
            a = C.actor(sp["id"], STREET_LOOKS[i % len(STREET_LOOKS)], pos=sp["pos"], scale=sp["scale"], seed=sp["seed"], dir=sp["dir"],
                        pose_keys=[[0, C.pose("relaxed", shF=70, elF=95, head=14, eyeY=1)]], holdF=mini_phone())
        ppl.append(a)
    stand = C.actor("hs_lamp", "hoodie_2021", pos=[[0, 1180, anc["feet"]]], scale=1.0, seed=77, dir=-1, walk=False, holdF=mini_phone(),
                    pose_keys=[[0, C.pose("relaxed", shF=70, elF=95, head=16, eyeY=1)], [t_q + 1.6, C.pose("relaxed", shF=70, elF=95, head=16, eyeY=1)],
                               [t_q + 2.1, C.pose("relaxed", shF=70, elF=95, head=-6, brow=.8)], [dur, C.pose("relaxed", shF=70, elF=95, head=10, eyeY=1)]])
    ppl.append(stand)
    layers = [lay(z, s, noblur=(k in ("light", "sky"))) for k, (z, s) in layers_.items()]
    layers.insert(len(layers) - 1, lay(.76, "".join(a["svg"] for a in ppl)))
    layers.append(lay(1.0, ph))
    cam = [[0, 960, 560, 1.0], [t_q, 960, 545, 1.03, "sine"], [t_q + 1.6, 960, 560, .86, "inout"], [dur, 990, 560, .82, "sine"]]
    over = [badge("Our illustration · not a real app", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, 1.0], [t_q + .6, 1.0], [t_q + 1.6, .76]], dof=6, shake=.35, over=over,
                grade="cool", vig=1.15)
    import sfx
    foley = [("tap", .12, .5, .1), ("tap", 1.45, .35, .1), ("buzz", t_q - .9, .25, .2)] + [("step", t, .05, -.2) for a in ppl[:3] for t in C.footsteps(a, dur)][:18]
    amb = sfx.city_ambience(dur + .5, seed=210, night=True) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def _fold(keys, v0=None):
    """Keyed values where some keys may fall before the shot starts (t <= 0: already happened). Returns keys from 0
    with the state at 0 folded in, sorted."""
    keys = sorted(keys, key=lambda k: k[0])
    before = [k for k in keys if k[0] <= 0]
    after = [k for k in keys if k[0] > 0]
    first = list(before[-1]) if before else (list(keys[0]) if v0 is None else [0, *v0])
    first[0] = 0
    if len(first) > 3 and isinstance(first[-1], str):
        first = first[:-1]
    return [first] + after


def _ktf(svg, at, d=.35):
    """kt() that shows an item already there when its time is before the shot (a second part of one scene)."""
    return svg if at <= 0 else kt(svg, None, at, d)


def shot_lend_twice(w, h, dur, ctx, part=1):
    """The puzzle (our illustration, a company with 100 shares), in two parts (one beat each: Kokoro cannot say all
    eight sentences in one pass). One bundle of 100 shares passes along five people as the narration says it: owner 1
    -> short seller 1 (lent) -> owner 2 (sold) | -> short seller 2 (lent again) -> owner 3 (sold). OWNS and OWES tags
    land over each; the billboard counts SHARES THAT EXIST 100 (never moves), SOLD SHORT 0 -> 100 -> 200, COUNTED AS
    OWNED 100 -> 200 -> 300. Part 2 opens on the state part 1 ended in. The mechanism is the SEC staff report's
    (p. 26): 'the same shares are lent multiple times by successive purchasers'.
    Part 1 sentences: 0 picture, 1 lends and sells, 2 owner 2 owns, 3 owner 1 still counts hers.
    Part 2 sentences: 0 the broker can lend again, 1 a second short seller borrows and sells, 2 still only 100, 3 but 200."""
    n = len(ctx.get("segs") or [])
    S = lambda i, f=0.0: seg_t(ctx, min(i, max(n - 1, 0)), f)
    never, gone = dur + 99, -9.0
    if part == 1:
        t_lend1, t_sell1, t_own2, t_still = S(1, .25), S(1, .7), S(2, .3), S(3, .2)
        t_lend2, t_lend2b, t_sell2, t_only, t_end3 = never, never, never, never, never
    else:
        t_lend1, t_sell1, t_own2, t_still = gone, gone + .5, gone + 1, gone + 1.5
        t_lend2, t_lend2b, t_sell2, t_only, t_end3 = S(0, .55), S(1, .25), S(1, .7), S(2, .1), S(3, .55)
    rows = [("SHARES THAT EXIST", [[0, 100]], 0, "", "", "#F4ECDD"),
            ("SOLD SHORT", _fold([[gone - 1, 0], [t_sell1 - .1, 0], [t_sell1 + .6, 100], [t_sell2 - .1, 100], [t_sell2 + .6, 200]]), 0, "", "", "#F08A6A"),
            ("COUNTED AS OWNED", _fold([[gone - 1, 100], [t_own2 - .1, 100], [t_own2 + .6, 200], [t_end3 - .1, 200], [t_end3 + .6, 300]]), 0, "", "", "#F6D58A")]
    rows = [(l, [k for k in ks if k[0] < never - 50], *rest) for l, ks, *rest in rows]
    bb = ('<g transform="translate(450,8) scale(.86)">' + board_rows_svg(0, rows, top=100, wid=880) + "</g>"
          + _ktf(_r(30, 310, 840, 50, RED, rx=6, sw=0) + _t(450, 346, "STILL ONLY 100 SHARES", 30, fill="#fff", family="Sans", weight=700), t_only, .3))
    layers_, anc = street_today(night=False, seed=22, billboard=bb)
    feet = anc["feet"]
    xs = [140, 560, 960, 1360, 1780]
    looks = ["lady_2021", "jacket_2021", "tee_2021", "coat_2021", "lady_2021b"]
    hand_y = feet - 150
    hand = {0: [t_lend1], 1: [t_lend1, t_sell1], 2: [t_sell1, t_lend2b], 3: [t_lend2b, t_sell2], 4: [t_sell2]}
    ppl = []
    for i, x in enumerate(xs):
        d = 1 if i < 4 else -1
        keys = [[gone - 2, C.pose("relaxed", head=4)]]
        for t in hand.get(i, []):
            keys += [[t - .35, C.pose("relaxed")], [t, C.pose("reach", head=6)], [t + .6, C.pose("relaxed", head=2)]]
        if i in (1, 3):                                            # the short sellers: concern once they owe
            t_owe = t_sell1 if i == 1 else t_sell2
            keys += [[t_owe + .9, C.pose("concern", head=4)], [t_owe + 60, C.pose("concern", head=2)]]
        elif i == 0:
            keys += [[t_still, C.pose("hold_up", head=-6, brow=.6)], [t_still + 1.4, C.pose("relaxed", head=0)]]
        keys = [k for k in keys if k[0] < never - 50]
        keys = _fold(keys)
        # keep them alive between actions: a small head turn every couple of seconds
        t = 1.0 + .4 * i
        while t < dur:
            if all(abs(t - k[0]) > .8 for k in keys):
                base = dict(max((k for k in keys if k[0] <= t), key=lambda k: k[0])[1])
                base["head"] = base.get("head", 0) + (6 if int(t) % 2 else -6)
                keys.append([round(t, 2), base])
            t += 2.1
        keys.sort(key=lambda k: k[0])
        ppl.append(C.actor(f"lt{i}", looks[i], pos=[[0, x, feet]], scale=1.08, seed=40 + i, dir=d, walk=False, pose_keys=keys))
    pk = (_r(-70, -44, 140, 88, PAPER, rx=6, sw=3) + _r(-62, -36, 124, 72, "none", rx=4, sw=1.6)
          + _t(0, -2, "100", 34, fill=RED, family="Serif", weight=700) + _t(0, 26, "SHARES", 16, fill=INK, family="Sans", weight=700, extra='letter-spacing="2"'))
    path = [[gone - 2, xs[0] + 70, hand_y], [t_lend1 - .1, xs[0] + 70, hand_y], [t_lend1 + .5, xs[1] - 50, hand_y - 30, "inout"],
            [t_sell1 - .1, xs[1] + 60, hand_y], [t_sell1 + .5, xs[2] - 60, hand_y - 30, "inout"], [t_lend2b - .1, xs[2] + 60, hand_y],
            [t_lend2b + .5, xs[3] - 60, hand_y - 30, "inout"], [t_sell2 - .1, xs[3] + 60, hand_y], [t_sell2 + .5, xs[4] - 70, hand_y - 10, "inout"]]
    path = _fold([k for k in path if k[0] < never - 50])
    bundle = f'<g {C.kv(translate=path)}>{pk}</g>'

    def tag(x, txt, col, t, y=feet - 400):
        return _ktf(_r(x - 120, y - 34, 240, 54, col, rx=27, sw=2.6) + _t(x, y + 3, txt, 24, fill="#fff", family="Sans", weight=700), t)
    tags = ""
    for x, txt, col, t, y in ((xs[0], "OWNS 100", TEAL, .4 if part == 1 else gone, feet - 440), (xs[0], "LENT", "#5A6068", t_still, feet - 505),
                              (xs[1], "OWES 100", RED, t_sell1 + .3, feet - 440), (xs[2], "OWNS 100", TEAL, t_own2, feet - 440),
                              (xs[3], "OWES 100", RED, t_sell2 + .3, feet - 440), (xs[4], "OWNS 100", TEAL, t_end3, feet - 440)):
        if t < never - 50:
            tags += tag(x, txt, col, t, y)
    for x, txt, t in ((xs[1], "SHORT SELLER 1", t_lend1), (xs[3], "SHORT SELLER 2", t_lend2b), (xs[0], "OWNER 1", .4 if part == 1 else gone),
                      (xs[2], "OWNER 2", t_sell1 + .3), (xs[4], "OWNER 3", t_sell2 + .3)):
        if t < never - 50:
            tags += _ktf(_t(x, feet + 60, txt, 22, fill=INK, family="Sans", weight=700), t, .3)
    layers = [lay(z, s, noblur=(k in ("light", "sky"))) for k, (z, s) in layers_.items()]
    layers.append(lay(.8, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.8, tags + bundle))
    zx = lambda x, z=.8: 960 + (x - 960) / z
    if part == 1:
        cam = [[0, zx(420), 500, .95], [t_lend1, zx(500), 500, .95, "inout"], [t_sell1 + .5, zx(760), 500, .95, "inout"],
               [t_still - .2, zx(600), 500, .92, "inout"], [dur, zx(640), 490, .9, "sine"]]
    else:
        cam = [[0, zx(760), 500, .95], [t_lend2 - .2, zx(1000), 500, .95, "inout"], [t_sell2 + .6, zx(1360), 500, .95, "inout"],
               [t_only - .2, 960, 470, .78, "inout"], [dur, 960, 460, .8, "sine"]]
    over = [badge("Our illustration · a company with 100 shares", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, .8]], dof=4, shake=.25, over=over, grade="warm", vig=1.0,
                tin=("dissolve", .35) if part == 1 else ("cut", 0))
    import sfx
    foley = [("paper", t + .1, .35, (xs[k] - 960) / 1200) for k, t in enumerate((t_lend1, t_sell1, t_lend2b, t_sell2)) if 0 < t < dur]
    foley += [(nm, t, g, 0, *rest) for nm, t, g, *rest in (("flap", t_sell1 + .1, .3), ("flap", t_own2, .3), ("flap", t_sell2 + .1, .3), ("flap", t_end3, .3),
                                                          ("hit", t_only + .1, .35, dict(pitch=150))) if 0 < t < dur]
    amb = sfx.city_ambience(dur + .5, seed=220 + part, night=False, traffic=.7) * .55
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_lend_twice_2(w, h, dur, ctx):
    return shot_lend_twice(w, h, dur, ctx, part=2)


def shot_laptop_prints(w, h, dur, ctx):
    """22 to 27 January 2021 at a kitchen table at night (our illustration). The laptop's chart lands each sourced
    print as it is said: 22 Jan about $43 and about $72 some three hours later, 27 Jan close $347.51 (SEC staff report
    2021, p. 19; the x position of the 22nd's two prints within the day is approximate); a tag for the 22nd's 197.2 million shares (p. 20). The viewer leans in, then sits back, brows up."""
    t1 = max(.8, word_t(ctx, 0, "forty three"))
    t2 = max(t1 + .8, word_t(ctx, 0, "seventy two"))
    t_vol = max(t2 + .8, seg_t(ctx, 1, .15))
    t3 = max(t_vol + .8, word_t(ctx, 2, "three hundred"))
    sw_, sh_ = 620, 380
    scr = (_t(24, 40, "GME · DAILY PRICES THAT ARE SOURCED", 18, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + prints_chart(80, 70, 510, 240, [(22.42, 43, "ABOUT $43", (-6, 40, "end")), (22.55, 72, "ABOUT $72, 3 HOURS LATER", (20, -70, "start")),
                                             (27.67, 347.51, "CLOSE $347.51", (-16, 6, "end"))],
                          [t1, t2, t3], vmax=400, label_size=15)
           + kt(_r(320, 244, 250, 40, TEAL, rx=6, sw=0) + _t(445, 271, "197.2M SHARES ON THE 22ND", 15, fill="#fff", family="Sans", weight=700), None, t_vol, .3))
    layers_, anc = kitchen_2021(night=True, screen=scr)
    sx, sy = anc["seat"]
    viewer = C.actor("kv", "hoodie_2021", pos=[[0, sx, sy]], scale=1.0, seed=88, dir=-1, walk=False,
                     pose_keys=[[0, C.pose("seated", head=10, eyeY=1)], [t1 - .3, C.pose("seated", head=12, lean=10, eyeY=1)],
                                [t3, C.pose("seated", head=12, lean=12, eyeY=1)], [t3 + .5, C.pose("seated", head=-4, lean=-4, brow=1, mouth=2)],
                                [t3 + 2.0, C.pose("seated", head=6, lean=4, brow=.6)], [dur, C.pose("seated", head=8, lean=6, eyeY=1)]])
    layers = [lay(z, s, noblur=(k in ("glow",))) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.82, viewer["svg"]))
    layers.append(lay(.85, layers_["table"][1]))
    zx = lambda x, z=.85: 960 + (x - 960) / z
    zy = lambda y, z=.85: 540 + (y - 540) / z
    lx, ly = anc["laptop"]
    cam = [[0, zx(900), zy(640), .95], [t1 - .2, zx(lx), zy(ly - 240), 1.5, "inout"], [t3 + .4, zx(lx + 20), zy(ly - 240), 1.62, "sine"],
           [t3 + 1.6, zx(950), zy(640), 1.05, "inout"], [dur, zx(980), zy(640), 1.08, "sine"]]
    over = [title("January 2021", "A kitchen table", w, h, d=min(2.6, t1 - .3)), badge("Our illustration · prices from the SEC staff report", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[viewer], cam=cam, focus=[[0, .85]], dof=4, shake=.25, over=over, grade="warm", vig=1.15, tin=("dissolve", .35))
    import sfx
    foley = [("tick", t, .3, 0) for t in (t1, t2, t3)] + [("buzz", t_vol - .2, .25, .4), ("hit", t3 + .15, .35, 0, dict(pitch=180))]
    amb = sfx.room_tone(dur + .5, seed=231, clock=False, street=.2) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_dawn_notice(w, h, dur, ctx):
    """5:11 a.m. ET, 28 January 2021 (reconstruction, not the real office). The clock moves from 5:11; the phone rings
    and is answered; the monitor types the notice: on deposit about $696 million, shortfall about $3 billion (Tenev,
    testimony of 18 February 2021). The person on the phone straightens up."""
    t_ring = .9
    t_lift = 2.0
    t_dep = max(2.4, seg_t(ctx, 1, .2))
    t_short = max(t_dep + 1.2, word_t(ctx, 1, "three billion"))
    clock = [[0, 5, 11], [dur, 5, 11 + dur / 60 * 3]]
    rows = [("ON DEPOSIT", "M", "#C9D4D6", [[0, 0], [t_dep, 0], [t_dep + .8, 696, "out"]]),
            ("SHORTFALL, ABOUT", "BN", RED, [[0, 0], [t_short, 0], [t_short + .9, 3, "out"]])]
    scr = notice_screen(900, 520, rows, [t_dep - .2, t_short - .2], t_head=.5)
    layers_, anc = ops_room_dawn(dur, clock, screen=scr, ring_at=[t_ring, t_ring + 1.0 * 0], lift=(t_lift, None))
    sx, sy = anc["seat"]
    from cine_1971 import handset
    op = C.actor("op", "ops_2021", pos=[[0, sx + 160, sy]], scale=1.0, seed=91, dir=-1, walk=False, holdF=handset(),
                 pose_keys=[[0, C.pose("seated", head=20, eyeY=1.4, lean=10)], [t_lift - .3, C.pose("seated", head=10, lean=6)],
                            [t_lift, C.pose("seated", shF=150, elF=130, head=4)], [t_short + .4, C.pose("seated", shF=150, elF=130, head=-6, brow=-1, mouth=-1, lean=-4)],
                            [dur, C.pose("seated", shF=150, elF=130, head=2, brow=-1)]])
    # until he lifts it, the handset is on the desk phone (desk_phone draws it); hide the held one until then
    op["svg"] = op["svg"].replace(handset(), f'<g {C.kv(opacity=[[0, 0], [t_lift - .01, 0], [t_lift, 1]])}>{handset()}</g>')
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k != "desk"]
    layers.append(lay(.82, op["svg"]))
    layers.append(lay(.85, layers_["desk"][1]))
    zx = lambda x, z=.85: 960 + (x - 960) / z
    zy = lambda y, z=.85: 540 + (y - 540) / z
    mx, my = anc["monitor"]
    cam = [[0, zx(1300), zy(420), 1.0], [t_lift, zx(1150), zy(520), 1.06, "inout"], [t_dep - .2, zx(mx), zy(my), 1.42, "inout"],
           [dur, zx(mx + 20), zy(my + 10), 1.5, "sine"]]
    over = [title("5:11 a.m., January 28, 2021", "An automated notice", w, h, d=min(3.0, t_dep - .4)), badge("Reconstruction · not the real office", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[op], cam=cam, focus=[[0, .85]], dof=4, shake=.25, over=over, grade="cool", vig=1.2, tin=("dissolve", .35))
    import sfx
    foley = [("ring", t_ring, .3, .3, dict(sec=1.0)), ("clank", t_lift, .2, .3, dict(pitch=200)), ("tick", t_dep, .3, -.2), ("hit", t_short + .2, .4, 0, dict(pitch=120))]
    amb = sfx.room_tone(dur + .5, seed=241, clock=True, street=.08) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_buy_grey(w, h, dur, ctx):
    """Our illustration of an app on the morning of 28 January 2021 (no real app's name, look or logo). The BUY button
    greys out and locks; 'POSITION CLOSING ONLY' (the SEC staff report's term, p. 35) appears; a thumb taps BUY and
    nothing happens; it taps SELL and the button answers."""
    t_grey = max(1.0, word_t(ctx, 0, "stop"))
    t_tap1 = max(t_grey + 1.2, seg_t(ctx, 1, .1))
    t_tap2 = max(t_tap1 + 1.2, word_t(ctx, 1, "couldn't"))
    W_, H_ = 560, 1080
    btn = lambda x, label, col: _r(x, 760, 200, 110, col, rx=55, sw=0) + _t(x + 100, 830, label, 46, fill="#fff", family="Sans", weight=700)
    body = (f'<path d="M60,520 L120,500 L180,510 L240,440 L300,470 L360,380 L420,420 L500,330" fill="none" stroke="#5E7378" stroke-width="6" stroke-linejoin="round"/>'
            + _t(60, 300, "SHARES", 30, fill="#8FA3A8", anchor="start", family="Sans", weight=700, extra='letter-spacing="3"')
            + _t(60, 600, "OUR ILLUSTRATION · NO REAL APP", 20, fill="#5E7378", anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
            + f'<g>{btn(50, "BUY", TEAL)}</g>'
            + f'<g {C.kv(opacity=[[0, 0], [t_grey, 0], [t_grey + .4, 1]])}>{_r(50, 760, 200, 110, "#4A4F55", rx=55, sw=0)}'
              f'{_t(150, 830, "BUY", 46, fill="#8A8F95", family="Sans", weight=700)}'
              f'<g transform="translate(218,770)"><rect x="-16" y="0" width="32" height="26" rx="4" fill="{MUSTARD}"/>'
              f'<path d="M-9,0 L-9,-10 A9,9 0 0 1 9,-10 L9,0" fill="none" stroke="{MUSTARD}" stroke-width="5"/></g></g>'
            + f'<g {C.kv(translate=[[0, 0, 0, 0, 1], [t_tap2, 0, 0, 0, 1], [t_tap2 + .1, 0, 0, 0, .94], [t_tap2 + .3, 0, 0, 0, 1]])}>{btn(310, "SELL", RED)}</g>'
            + kt(_r(40, 660, 480, 64, "#2A2E34", rx=10, sw=0) + _t(280, 703, "POSITION CLOSING ONLY", 30, fill=MUSTARD, family="Sans", weight=700), None, t_grey + .4, .35)
            + f'<circle cx="150" cy="815" r="70" fill="none" stroke="#fff" stroke-width="4" {C.kv(opacity=[[0, 0], [t_tap1, 0], [t_tap1 + .05, .8], [t_tap1 + .5, 0]])}/>'
            + f'<circle cx="410" cy="815" r="70" fill="none" stroke="#fff" stroke-width="4" {C.kv(opacity=[[0, 0], [t_tap2, 0], [t_tap2 + .05, .9], [t_tap2 + .5, 0]])}/>')
    hp = hand_phone(W_, H_, body=body, head="GME", sub="JANUARY 28, 2021", skin="#C98E68", sleeve="#7A3B4A")
    # the other hand's index finger: comes in from the right, taps BUY, then SELL
    P = lambda bx, by: (690 + bx * .9, 20 + by * .9)            # phone coordinates -> world (translate 690,20, scale .9)
    (bx1, by1), (bx2, by2) = P(150, 815), P(410, 815)
    fpath = [[0, 1700, 1300], [t_tap1 - .6, 1500, 1150], [t_tap1, bx1, by1, "out"], [t_tap1 + .5, bx1 + 60, by1 + 70],
             [t_tap2 - .3, bx2, by2 + 80], [t_tap2, bx2, by2, "out"], [t_tap2 + .6, bx2 + 120, by2 + 160], [dur, bx2 + 400, by2 + 500]]
    finger = (f'<g {C.kv(translate=fpath)}>'
              f'<path d="M-26,0 C-26,-30 26,-30 26,0 L30,260 L-30,260 Z" fill="#C98E68" stroke="{INK}" stroke-width="5"/>'
              f'<path d="M-14,-6 C-14,-18 14,-18 14,-6" fill="none" stroke="{INK}" stroke-width="3" opacity=".4"/></g>')
    ph = f'<g transform="translate(690,20) scale(.9)">{hp}</g>'
    layers_, anc = kitchen_2021(night=False, seed=32, mug_steam=True)
    layers = [lay(z, s, noblur=(k == "glow")) for k, (z, s) in layers_.items()]
    layers.append(lay(1.0, ph + finger))
    cam = [[0, 960, 520, 1.0], [t_grey, 940, 600, 1.15, "inout"], [t_tap1, 930, 640, 1.25, "inout"], [dur, 940, 650, 1.28, "sine"]]
    over = [badge("Our illustration · not a real app", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[], cam=cam, focus=[[0, 1.0]], dof=7, shake=.3, over=over, grade="warm", vig=1.1, tin=("dissolve", .3))
    import sfx
    foley = [("clank", t_grey + .1, .2, 0, dict(pitch=260)), ("tap", t_tap1, .6, .2), ("tap", t_tap1 + .25, .4, .2), ("tap", t_tap2, .6, .3)]
    amb = sfx.room_tone(dur + .5, seed=251, clock=False, street=.25) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


SHOTS = dict(hook_109=shot_hook_109, lend_twice=shot_lend_twice, lend_twice_2=shot_lend_twice_2, laptop_prints=shot_laptop_prints, dawn_notice=shot_dawn_notice, buy_grey=shot_buy_grey)


if __name__ == "__main__":
    # stills for a quick look: python3 build/cine_2021.py [name ...]
    names = sys.argv[1:] or list(SHOTS)
    work = C.OUT / "cine-2021-stills"
    work.mkdir(parents=True, exist_ok=True)
    demo = dict(segs=[("On the last day of twenty twenty, short sellers had sold more GameStop shares than the company had.", .3, 4.0),
                      ("A hundred and nine percent of them, from forty three to seventy two, it owed three billion, stop.", 4.2, 8.0),
                      ("How can you sell more of something than exists, three hundred, they couldn't buy?", 8.2, 11.5),
                      ("The first one still counts hers.", 11.7, 13.5), ("And the broker lends them again.", 13.7, 15.5),
                      ("A second short seller borrows them and sells them.", 15.7, 18.5), ("Still only a hundred.", 18.7, 20.0),
                      ("But two hundred sold short.", 20.2, 23.0)])
    for nm in names:
        built = SHOTS[nm](1920, 1080, 24.0 if nm == "lend_twice" else 12.5, demo)
        html, total = C.film_html(built["shots"], 1920, 1080)
        print(nm, C.stills(html, [0.2, 1.6, total * .4, total * .7, total - .3], work, nm))
