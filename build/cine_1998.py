"""
Filmed beats for YouTube #12, Long-Term Capital Management, 1998 (18 Nov 2026). Sets, props and shots for
build/cine.py, used by build/youtube_ep012.py as kind="cine" beats (cinematic-standard.md section 8: step 3, sets,
the first late-1990s rooms; step 2, people: cine.sit_keys, a sitting-down transition; step 4, data in the world:
a capital board that counts down and a screen whose two yields close and then open).

Sets (our own generic drawings; no real firm, building, logo or person is copied; everything is badged):
  fund_room_1998()   an open-plan trading room of 1998: tall windows on trees and an overcast sky, rows of desks with
                     beige CRT monitors whose screens flicker, a wall board (split-flap style) for counted figures
  boardroom_1998()   a panelled meeting room at night: a long table, chairs, a wall clock whose hands move, tall
                     windows on an invented night skyline, papers on the table
Props: crt() (a monitor with live screen content), yield_screen() (two yield lines on a CRT: they close, then open),
term_sheet() (greeked except its heading and the three sourced terms).
1998 looks (cine.LOOKS): shirt_1998, shirt_1998b, suit_1998, suit_1998b, suit_1998c, lady_1998.

Shots (fn(w, h, dur, ctx) -> dict(shots, foley, amb); ctx["segs"] are the beat's sentences, (text, start, end)):
  capital_hook   the hook: the trading room; the board's CAPITAL row counts from $4.8bn (1 Jan) to $4.1bn (31 Jul)
                 to $2.3bn (31 Aug) as the loss is said; the traders turn to it
  gap_close      our illustration of the convergence trade: on a CRT, the newer and the older bond's yields draw
                 with a small gap that narrows; a trader taps the screen
  gap_open       after 17 August: the same screen, the gap opens instead; the trader steps back
  fed_evening    22 Sept 1998, evening (reconstruction, not the real room): the clock runs from 7:00 to 8:30 while
                 bankers come in and sit down (cine.sit_keys) around the table
  fed_deal       23 Sept 1998: the clock near six; the term sheet is passed along and signed; three sourced terms
                 rise off it: $3.6bn, 14 firms, 90%
Facts on screen come only from the sources in youtube_ep012.py's docstring. Nobody in a shot speaks, and nobody is a
likeness: the figures are "our illustration", not portraits of anyone at LTCM, the New York Fed or any bank.
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
from cine_1971 import kt, board_rows_svg, desk_phone, handset   # noqa: E402
from cine_1974 import wall_clock                  # noqa: E402

INK, RED, TEAL, MUSTARD, PAPER = C.INK, C.RED, C.TEAL, C.MUSTARD, "#F7F5F2"
SCREEN, GLOW = "#0F2A24", "#5EC8B4"
_r, _t = L._r, L._t

C.LOOKS.update({
    "shirt_1998": dict(coat="#B9CBE0", coat2="#9FB4CC", vest="#F2F2F2", legs="#3B3F4A", stock="#3B3F4A", shoe=INK, skin="#E5B391",
                       hair="#4A3424", hat="", style="suit", cuff="#F2F2F2", tie="#8A3B22", era="1971"),
    "shirt_1998b": dict(coat="#F1EEE6", coat2="#D9D4C8", vest="#F7F5F2", legs="#4A4440", stock="#4A4440", shoe=INK, skin="#8D5A3B",
                        hair="#14100D", hat="", style="suit", cuff="#F7F5F2", tie=TEAL, era="1971"),
    "suit_1998": dict(coat="#2B3140", coat2="#1F2430", vest="#EEF1F4", legs="#2B3140", stock="#2B3140", shoe=INK, skin="#F0C7A4",
                      hair="#8A6A4A", hat="", style="suit", cuff="#EEF1F4", tie=RED, era="1971"),
    "suit_1998b": dict(coat="#3E3A36", coat2="#2E2B28", vest="#F2EEE6", legs="#3E3A36", stock="#3E3A36", shoe=INK, skin="#C98E68",
                       hair="#2A2018", hat="", style="suit", cuff="#F2EEE6", tie=MUSTARD, era="1971"),
    "suit_1998c": dict(coat="#47505A", coat2="#363D45", vest="#F4F4F4", legs="#47505A", stock="#47505A", shoe=INK, skin="#E8BC9A",
                       hair="#B8B0A6", hat="", style="suit", cuff="#F4F4F4", tie="#3E4F66", era="1971"),
    "lady_1998": dict(coat="#5A3C4A", coat2="#46303A", vest="#F4EFE4", legs="#3A3A40", stock="#3A3A40", shoe=INK, skin="#B97A55",
                      hair="#1E1410", hat="", style="dress", cuff="#F4EFE4", tie=RED, era="1971"),
})
FUND_LOOKS = ("shirt_1998", "shirt_1998b", "suit_1998", "lady_1998", "shirt_1998", "suit_1998b")
FED_LOOKS = ("suit_1998", "suit_1998b", "suit_1998c", "lady_1998", "suit_1998b", "suit_1998")


# ------------------------------------------------------------------------------------------------ props

def crt(x, y, w=220, h=170, screen="", seed=0):
    """A beige CRT monitor standing on a desk at (x, y = desk top). screen: SVG drawn in the screen's own box
    (0..w-36, 0..h-40). The screen glows and flickers slightly."""
    sw_, sh_ = w - 36, h - 40
    return (f'<g transform="translate({x - w / 2},{y - h - 34})">'
            + _r(0, 0, w, h, "#D9D2C1", rx=12, sw=3) + _r(10, 12, w - 20, h - 26, "#B8B09C", rx=8, sw=2)
            + f'<g transform="translate(18,20)"><rect width="{sw_}" height="{sh_}" rx="6" fill="{SCREEN}"/>{screen}'
            + f'<rect width="{sw_}" height="{sh_}" rx="6" fill="{GLOW}" opacity=".06" data-flick=\'[0.06,0.03,{seed % 7}]\'/></g>'
            + _r(w / 2 - 34, h, 68, 22, "#C9C1AE", sw=2.4) + _r(w / 2 - 70, h + 20, 140, 14, "#C9C1AE", rx=4, sw=2.4) + "</g>")


def _ticker_lines(sw_, sh_, seed):
    """Greeked rows on a small screen: bars that change length now and then (nothing legible)."""
    rng = random.Random(seed)
    out = ""
    for k in range(6):
        y = 16 + k * (sh_ - 24) / 6
        a, b = rng.uniform(.3, .9), rng.uniform(.3, .9)
        out += (f'<rect x="10" y="{y:.0f}" height="6" fill="{GLOW}" opacity=".55" width="{sw_ - 20}" '
                f'{C.kv(clip=[[0, 0, (1 - a) * 100, 0, 0], [1.5 + k * .4, 0, (1 - a) * 100, 0, 0], [1.8 + k * .4, 0, (1 - b) * 100, 0, 0]])}/>')
    return out


def yield_screen(w, h, t_draw=(0.3, 3.0), t_open=None, label=True):
    """Two yields on one honest-looking but illustrative axis (no numbers: our illustration). The newer bond's line
    (teal) sits a little below the older bond's (mustard): the newer one is pricier, so it yields less. From t_draw
    the two lines draw left to right and the gap narrows; if t_open is given, from then the gap opens again."""
    x0, x1, ym = 40, w - 40, h * .52
    n = 24
    close = [(x0 + (x1 - x0) * k / n, 70 * (1 - k / n) ** 1.3 + 8) for k in range(n + 1)]
    top = "M" + " L".join(f"{x:.0f},{ym - g / 2:.0f}" for x, g in close)
    bot = "M" + " L".join(f"{x:.0f},{ym + g / 2:.0f}" for x, g in close)
    out = (f'<path d="M{x0},{h - 40} L{x1},{h - 40} M{x0},30 L{x0},{h - 40}" stroke="{GLOW}" stroke-width="2" opacity=".5"/>'
           f'<path d="{top}" fill="none" stroke="{MUSTARD}" stroke-width="5" {C.kv(dash=[[0, 0], [t_draw[0], 0], [t_draw[1], 1]])}/>'
           f'<path d="{bot}" fill="none" stroke="{GLOW}" stroke-width="5" {C.kv(dash=[[0, 0], [t_draw[0], 0], [t_draw[1], 1]])}/>')
    if label:
        out += (_t(x0 + 10, 28, "OLDER BOND", 18, fill=MUSTARD, anchor="start", family="Sans", weight=700)
                + _t(x0 + 10, h - 52, "NEWER BOND", 18, fill=GLOW, anchor="start", family="Sans", weight=700)
                + _t(x1 - 4, 28, "YIELD · OUR ILLUSTRATION", 14, fill="#9FC9BE", anchor="end", family="Sans", weight=600))
    if t_open is not None:
        # the gap opens: from the end of the drawn lines, a second pair goes further apart
        g0 = close[-1][1]
        far = [(x1 + 0 * k, g0) for k in range(1)]
        xs = [x1 - (x1 - x0) * .35 + (x1 - x0) * .35 * k / 10 for k in range(11)]
        gx = [g0 + 150 * (k / 10) ** 1.4 for k in range(11)]
        # redraw on a fresh panel to the right: the old lines dim, new ones show the widening
        out = out.replace(f'stroke="{MUSTARD}" stroke-width="5"', f'stroke="{MUSTARD}" stroke-width="5" {C.kv(opacity=[[0, 1], [t_open, 1], [t_open + .4, .25]])}', 1)
        out = out.replace(f'stroke="{GLOW}" stroke-width="5"', f'stroke="{GLOW}" stroke-width="5" {C.kv(opacity=[[0, 1], [t_open, 1], [t_open + .4, .25]])}', 1)
        top2 = "M" + " L".join(f"{x0 + (x - xs[0]) * (x1 - x0) / (x1 - xs[0]):.0f},{ym - g / 2:.0f}" for x, g in zip(xs, gx))
        bot2 = "M" + " L".join(f"{x0 + (x - xs[0]) * (x1 - x0) / (x1 - xs[0]):.0f},{ym + g / 2:.0f}" for x, g in zip(xs, gx))
        out += (f'<path d="{top2}" fill="none" stroke="{MUSTARD}" stroke-width="6" {C.kv(dash=[[0, 0], [t_open + .3, 0], [t_open + 2.6, 1]])}/>'
                f'<path d="{bot2}" fill="none" stroke="{GLOW}" stroke-width="6" {C.kv(dash=[[0, 0], [t_open + .3, 0], [t_open + 2.6, 1]])}/>'
                + kt(_r(x1 - 210, ym - 26, 200, 52, RED, rx=6, sw=0) + _t(x1 - 110, ym + 9, "GAP OPENS", 24, fill="#fff", family="Sans", weight=700), None, t_open + 2.4))
    else:
        out += kt(_r(x1 - 230, ym + 34, 220, 48, TEAL, rx=6, sw=0) + _t(x1 - 120, ym + 66, "GAP CLOSES", 22, fill="#fff", family="Sans", weight=700), None, t_draw[1] - .3)
    return out


def term_sheet(x, y, w=520, h=360, terms=(), t_terms=()):
    """A term sheet on the table: a heading and greeked lines; each sourced term in terms appears (inked) at its time."""
    out = (f'<g transform="translate({x},{y}) rotate(-2)">' + _r(-w / 2, -h / 2, w, h, PAPER, rx=4, sw=3.4)
           + _t(-w / 2 + 34, -h / 2 + 56, "TERM SHEET", 34, fill=INK, anchor="start", family="Serif", weight=700)
           + _t(-w / 2 + 34, -h / 2 + 86, "SEPTEMBER 1998 · OUR ILLUSTRATION", 14, fill="#7A6A55", anchor="start", family="Sans", weight=600, extra='letter-spacing="3"'))
    out += L._greek(-w / 2 + 34, -h / 2 + 120, w - 68, 3, gap=22, seed=4)
    for k, (txt, t) in enumerate(zip(terms, t_terms)):
        out += kt(_t(-w / 2 + 34, -h / 2 + 220 + 44 * k, txt, 30, fill=RED if k == 0 else INK, anchor="start", family="Sans", weight=700), None, t, .4)
    return out + "</g>"


# ------------------------------------------------------------------------------------------------ sets

def fund_room_1998(rows=(), head="FUND", sub="", seed=6, screens=None):
    """An open-plan trading room, 1998. Board centred at x 960 on the z .4 wall; desks at y 880 on the z .78 layer
    with a CRT on each; people stand at y 1010 behind the desks (z .74). Returns (layers, anchors)."""
    rng = random.Random(seed)
    wall = C.defs() + '<rect x="-1600" y="-900" width="5200" height="2600" fill="#D8D6CF"/>'
    wall += ('<defs><linearGradient id="sky98" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B9C4C8"/>'
             '<stop offset="1" stop-color="#E2E3DC"/></linearGradient></defs>')
    for wx in (-900, -480, 1720, 2140):                                                # tall windows on trees
        wall += f'<rect x="{wx}" y="120" width="340" height="640" fill="url(#sky98)"/>'
        for k in range(5):
            cx, r = wx + 30 + k * 70 + rng.uniform(-10, 10), rng.uniform(60, 110)
            wall += (f'<g data-swing=\'[{rng.uniform(.4, .9):.2f},{rng.uniform(.5, .9):.2f},{k},{cx:.0f},760]\'>'
                     f'<circle cx="{cx:.0f}" cy="{760 - r * 1.4:.0f}" r="{r:.0f}" fill="{rng.choice(["#6F8A5E", "#7C9468", "#5E7A50"])}" opacity=".9"/></g>')
        wall += (f'<rect x="{wx}" y="120" width="340" height="640" fill="none" stroke="#9A968C" stroke-width="14"/>'
                 f'<path d="M{wx + 170},120 L{wx + 170},760" stroke="#9A968C" stroke-width="8"/>')
    wall += f'<rect x="-1600" y="760" width="5200" height="24" fill="#B4B0A4" stroke="{INK}" stroke-width="3"/>'
    if rows:
        bw_ = 980
        wall += '<g transform="translate(960,40) scale(1.25) translate(-960,-90)">'
        wall += _r(960 - bw_ / 2, 90, bw_, 150 + 90 * len(rows), "#2A302D", rx=8, sw=5)
        wall += _t(960, 150, head, 40, fill="#F4ECDD", weight=700, family="Sans", extra='letter-spacing="5"')
        if sub:
            wall += _t(960, 190, sub, 22, fill="#B9C2BC", weight=600, family="Sans", extra='letter-spacing="4"')
        wall += board_rows_svg(960, rows, top=270, wid=bw_) + "</g>"
    light = "".join(C.shaft(x, 130, 280, 900, angle=-16, op=.12) for x in (-860, -440, 1760, 2180))
    floor = '<rect x="-1600" y="905" width="5200" height="800" fill="#7C7F80"/><rect x="-1600" y="905" width="5200" height="800" fill="url(#boards)" opacity=".08"/>'
    desks = ""
    xs = list(range(-320, 2500, 400))
    for k, dx in enumerate(xs):
        desks += _r(dx, 880, 340, 24, "#CFC7B4", rx=3, sw=3) + _r(dx + 10, 904, 320, 110, "#A9A190", sw=2.6)
        scr = (screens or {}).get(k) or _ticker_lines(184, 130, seed + k)
        desks += crt(dx + 120, 880, screen=scr, seed=k)
        desks += desk_phone(dx + 280, 880) if k % 2 else (f'<g transform="translate({dx + 270},876) rotate(-3)">' + _r(-50, -8, 100, 10, PAPER, sw=2) + "</g>")
    layers = dict(wall=(0.4, wall), light=(0.46, light), floor=(0.6, floor), desks=(0.78, desks))
    return layers, dict(feet_back=1010, board_x=960, desk_xs=xs)


def boardroom_1998(clock_path, dur, seed=8):
    """A panelled meeting room at night (not the real New York Fed room). Clock at x 1500 on the z .45 wall; the table
    top at y 860 on the z .85 layer; seated people at y 990 (z .78); the door at x -140. Returns (layers, anchors)."""
    rng = random.Random(seed)
    wall = C.defs() + '<rect x="-1600" y="-900" width="5200" height="2600" fill="#4A3A2E"/>'
    for i in range(-6, 16):                                                            # panelling
        wall += _r(i * 240 + 20, 520, 200, 330, "#56443A", rx=4, sw=2)
    for wx in (180, 700):                                                              # night windows, an invented skyline
        wall += f'<rect x="{wx}" y="80" width="420" height="400" fill="#1D2638"/>'
        x = wx
        while x < wx + 420:
            bw, bh = rng.uniform(30, 70), rng.uniform(120, 330)
            bw = min(bw, wx + 420 - x)
            wall += f'<rect x="{x:.0f}" y="{480 - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="#2E3A50"/>'
            for yy in range(int(480 - bh) + 14, 470, 26):
                for xx in range(int(x) + 6, int(x + bw) - 6, 16):
                    if rng.random() < .35:
                        wall += f'<rect x="{xx}" y="{yy}" width="7" height="10" fill="#F6D58A" opacity=".8" data-flick=\'[0.8,0.15,{xx % 7}]\'/>'
            x += bw + 3
        wall += (f'<rect x="{wx}" y="80" width="420" height="400" fill="none" stroke="#2A1E16" stroke-width="16"/>'
                 f'<path d="M{wx + 210},80 L{wx + 210},480" stroke="#2A1E16" stroke-width="10"/>')
    wall += wall_clock(1500, 250, 110, clock_path, dur, sec0=rng.randint(0, 59))
    door = (_r(-260, 200, 250, 700, "#5E3D27", sw=4) + _r(-232, 230, 194, 300, "#6B4A32", sw=2.4)
            + f'<circle cx="-40" cy="560" r="9" fill="{MUSTARD}" stroke="{INK}" stroke-width="2"/>')
    glow = (f'<circle cx="760" cy="700" r="640" fill="url(#candle)" opacity=".55"/>')
    floor = (f'<rect x="-1600" y="900" width="5200" height="700" fill="#3A2C24"/>'
             f'<ellipse cx="760" cy="1060" rx="1300" ry="130" fill="#5A2E24" opacity=".5"/>')
    table = (_r(-60, 860, 1660, 40, "#5A3420", rx=8, sw=3.6) + _r(-30, 900, 1600, 30, "#3E2416", sw=3)
             + _r(20, 930, 34, 150, "#3E2416", sw=2.6) + _r(1480, 930, 34, 150, "#3E2416", sw=2.6))
    for k, px in enumerate(range(80, 1500, 230)):                                      # papers and water glasses
        table += f'<g transform="translate({px + 60},{854}) rotate({rng.uniform(-6, 6):.1f})">' + _r(-50, -9, 100, 12, PAPER, sw=2) + "</g>"
        table += _r(px + 140, 820, 18, 36, "#CFE3E6", rx=3, sw=2)
    chairs = "".join(_r(x - 50, 760, 100, 150, "#2E2420", rx=12, sw=3) for x in range(130, 1500, 230))
    layers = dict(wall=(0.45, wall + door), glow=(0.5, glow), floor=(0.6, floor), chairs=(0.76, chairs), table=(0.85, table))
    return layers, dict(table_y=860, seat_y=990, door_x=-140, seat_xs=list(range(130, 1500, 230)))


# ------------------------------------------------------------------------------------------------ people

def fund_people(anc, dur, react_at=None, mood="concern", n=6, seed=81, phones=(), prefix="f"):
    """People between the desks, in shirtsleeves or suits; at react_at each turns to the board in turn."""
    rng = random.Random(seed)
    out = []
    for i in range(n):
        x = -150 + i * 400 + rng.uniform(-30, 30)
        d = 1 if x < anc["board_x"] else -1
        on = i in phones
        arm = dict(shF=150, elF=130) if on else {}
        keys = [[0, C.pose("relaxed", head=-8, **arm)], [.8 + .45 * i, C.pose("talk_a" if i % 2 else "talk_b", head=-6, **arm)]]
        if react_at is not None:
            keys += [[react_at + .12 * i, C.pose("relaxed", head=-16, **arm)],
                     [react_at + .5 + .12 * i, C.pose(mood if (i % 3 or on) else "point", head=-20, brow=-1, **arm)],
                     [dur, C.pose(mood, head=-14, **arm)]]
        out.append(C.actor(f"{prefix}{i}", FUND_LOOKS[i % len(FUND_LOOKS)], pos=[[0, x, anc["feet_back"] + (i % 2) * 10]], scale=1.05 + .03 * (i % 3),
                           seed=seed + i, dir=d, walk=False, pose_keys=keys, holdF=handset() if on else ""))
    return out


# ------------------------------------------------------------------------------------------------ shots

def shot_capital_hook(w, h, dur, ctx):
    """The hook (reconstruction, not LTCM's office): the board's CAPITAL row counts down as the August loss is said;
    the room turns to it. Board figures: PWG 1999 ($4.8bn on 1 Jan 1998, $4.1bn on 31 Jul, $2.3bn at the end of
    August)."""
    t_drop = min(dur - 2.2, max(1.6, word_t(ctx, 1, "one point eight")))
    t_jul = max(.8, t_drop - 1.6)
    rows = [("1 JANUARY 1998", [[0, 4.8]], 1, "$", "bn", "#F4ECDD"),
            ("CAPITAL NOW", [[0, 4.8], [t_jul - .6, 4.8], [t_jul + .4, 4.1], [t_drop, 4.1], [t_drop + 1.4, 2.3]], 1, "$", "bn", "#F6D58A")]
    layers_, anc = fund_room_1998(rows, head="FUND CAPITAL", sub="1998 · PRESIDENT'S WORKING GROUP, 1999", seed=6)
    ppl = fund_people(anc, dur, react_at=t_drop + .4, phones=(1, 4))
    layers = [lay(z, s, noblur=(k == "light")) for k, (z, s) in layers_.items() if k != "desks"]
    layers.append(lay(.74, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.78, layers_["desks"][1]))
    fg = (_r(-700, 1010, 1100, 40, "#CFC7B4", rx=4, sw=3.4) + _r(-690, 1050, 1080, 300, "#A9A190", sw=3) + crt(160, 1010, 300, 230, _ticker_lines(264, 190, 3), seed=3)
          + _r(1700, 1030, 1000, 40, "#CFC7B4", rx=4, sw=3.4) + _r(1710, 1070, 980, 300, "#A9A190", sw=3) + desk_phone(1900, 1030, color="#2A2A2E"))
    layers.append(lay(1.18, fg))
    zb = lambda x: 960 + (x - 960) / .4
    cam = [[0, 900, 600, 1.0], [t_jul - .4, 940, 560, 1.08, "inout"], [t_drop + .2, 960, 470, 1.16, "inout"], [dur, 970, 460, 1.2, "sine"]]
    over = [title("September 1998", "A fund writes to its investors", w, h, d=min(3.2, t_drop - .2)), badge("Reconstruction · not the real office", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, .74], [t_drop, .45], [dur, .5]], dof=5, shake=.3, over=over, grade="cool", vig=1.1)
    import sfx
    foley = [("flap", t_jul - .4, .35, 0), ("flap", t_drop + .1, .45, 0), ("hit", t_drop + 1.4, .45, 0, dict(pitch=110)), ("ring", .6, .12, -.5, dict(sec=.8))]
    amb = sfx.office_ambience(dur + .5, seed=98, busy=.9, phones=.4) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def _screen_shot(w, h, dur, ctx, t_draw, t_open=None, ttl=None, bdg="Our illustration · two nearly identical bonds"):
    """A trader's desk close up: a big CRT with the two yields, the trader beside it."""
    sw_, sh_ = 760, 480
    scr = yield_screen(sw_, sh_, t_draw=t_draw, t_open=t_open)
    room, anc = fund_room_1998(seed=11)
    back = [lay(z, s, noblur=(k == "light")) for k, (z, s) in room.items()]
    mon = crt(960, 900, 800, 560, scr, seed=5)
    desk = _r(300, 900, 1400, 40, "#CFC7B4", rx=4, sw=3.4) + _r(310, 940, 1380, 300, "#A9A190", sw=3) + desk_phone(1540, 900, color="#2A2A2E")
    t_tap = t_draw[1] - .6
    keys = [[0, C.pose("relaxed", head=8)], [t_tap - .5, C.pose("relaxed", head=10)], [t_tap, C.pose("point", head=8)], [t_tap + .8, C.pose("relaxed", head=4)]]
    if t_open is not None:
        keys += [[t_open + .4, C.pose("relaxed", head=6)], [t_open + 1.6, C.pose("concern", head=2, brow=-1)], [dur, C.pose("concern", head=4)]]
    else:
        keys += [[dur, C.pose("talk_b", head=6)]]
    pos = [[0, 1560, 1240]] if t_open is None else [[0, 1560, 1240], [t_open + 1.2, 1560, 1240], [t_open + 2.4, 1700, 1240, "out"]]
    trader = C.actor("tr", "shirt_1998", pos=pos, scale=1.4, seed=12, dir=-1, walk=t_open is not None, pose_keys=keys)
    layers = back + [lay(1.0, desk + mon), lay(1.04, trader["svg"])]
    cam = [[0, 960, 560, 1.0], [t_draw[0] + .4, 960, 540, 1.08, "inout"], [dur, 960, 530, 1.14, "sine"]]
    if t_open is not None:
        cam = [[0, 960, 560, 1.06], [t_open, 960, 540, 1.1, "sine"], [t_open + 1.4, 1000, 520, 1.22, "inout"], [dur, 1000, 515, 1.26, "sine"]]
    over = ([title(*ttl, w, h, d=min(3.0, dur - .6))] if ttl else []) + [badge(bdg, w, h)]
    shot = dict(dur=dur, layers=layers, actors=[trader], cam=cam, focus=[[0, 1.0]], dof=4, shake=.25, over=over, grade="cool", vig=1.0, tin=("dissolve", .35))
    import sfx
    foley = [("tick", t_tap, .3, .3)] + ([("hit", t_open + 2.4, .4, 0, dict(pitch=110))] + [("step", t, .12, .5) for t in C.footsteps(trader, dur)] if t_open is not None else [])
    amb = sfx.office_ambience(dur + .5, seed=99, busy=.5, phones=0) * .6
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_gap_close(w, h, dur, ctx):
    """Our illustration: the two yields draw across the screen with a small gap that narrows; the trader points at
    the gap as it closes. No numbers: the sourced size of the gap (about a tenth of a point) is said, not plotted."""
    a = max(.6, seg_t(ctx, 0, .2))
    b = min(dur - 1.0, max(a + 2.5, seg_t(ctx, len(ctx.get("segs") or [1]) - 1, .6)))
    return _screen_shot(w, h, dur, ctx, (a, b))


def shot_gap_open(w, h, dur, ctx):
    """After 17 August 1998 (our illustration): the same screen; the lines are already drawn and closing, then on
    'wider' the gap opens instead. Sourced in the narration (flight to quality: MacKenzie; McDonough)."""
    t_open = min(dur - 3.2, max(1.4, word_t(ctx, 2, "wider") - .4))
    return _screen_shot(w, h, dur, ctx, (.05, .6), t_open=t_open, ttl=("After August 17", "1998"))


def sit_people(anc, dur, arrive, seated=3, seed=90, prefix="b"):
    """Seated bankers along the table plus late arrivals who walk in from the door and sit (cine.sit_keys).
    arrive: list of arrival times. Returns the actors."""
    xs = anc["seat_xs"]
    out = []
    for i in range(seated):
        x = xs[2 + i * 2 % (len(xs) - 2)]
        out.append(C.actor(f"{prefix}s{i}", FED_LOOKS[i % len(FED_LOOKS)], pos=[[0, x, anc["seat_y"]]], scale=.9, seed=seed + i, dir=1 if i % 2 else -1, walk=False,
                           pose_keys=[[0, C.pose("seated", head=4)], [1.5 + i, C.pose("sit_read", head=8)], [dur, C.pose("seated", head=-4)]]))
    free = [x for k, x in enumerate(xs) if all(abs(x - a["spec"]["pos"][0][1]) > 20 for a in out)]
    for j, ta in enumerate(arrive):
        x = free[j % len(free)]
        walk_d = 1.0 + (x + 140) / 420
        t_sit = ta + walk_d + .15
        out.append(C.actor(f"{prefix}a{j}", FED_LOOKS[(j + 3) % len(FED_LOOKS)], pos=[[0, -140, anc["seat_y"]], [ta, -140, anc["seat_y"]], [ta + walk_d, x, anc["seat_y"], "out"]],
                           scale=.9, seed=seed + 20 + j, dir=1, walk=True,
                           turn=[[t_sit - .2, 1], [t_sit + .1, -1 if j % 2 else 1]],
                           pose_keys=[[0, C.pose("relaxed")], *C.sit_keys(t_sit, start="relaxed"), [dur, C.pose("seated", head=6)]]))
    return out


def shot_fed_evening(w, h, dur, ctx):
    """22 Sept 1998, evening (reconstruction): the clock runs from 7:00 to about 8:30 across the beat while bankers
    walk in and sit down at the long table (the 7 p.m. meeting of four firms, then the wider 8:30 p.m. meeting:
    McDonough 1998). Not the real room, no real person."""
    clock = [[0, 19, 0], [dur * .45, 19, 40, "inout"], [dur, 20, 30, "inout"]]
    layers_, anc = boardroom_1998(clock, dur)
    arrive = [.4, 1.4, dur * .45, dur * .45 + .9, dur * .45 + 1.8]
    ppl = sit_people(anc, dur, arrive, seated=2)
    layers = [lay(z, s, noblur=(k == "glow")) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.8, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.85, layers_["table"][1]))
    tag = kt(_r(1500 - 200, 400, 400, 64, PAPER, rx=8, sw=3) + _t(1500, 442, "7:00 TO 8:30 P.M.", 28, fill=INK, family="Sans", weight=700), None, 1.2)
    layers.insert(1, lay(.45, tag))
    zx = lambda x, z=.85: 960 + (x - 960) / z
    cam = [[0, zx(500), 560, .82], [dur * .45, zx(700), 560, .86, "sine"], [dur, zx(900), 540, .92, "sine"]]
    over = [title("New York, September 22, 1998", "A meeting at the Fed", w, h, d=min(3.4, dur - .6)), badge("Reconstruction · not the real room", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, .82]], dof=5, shake=.25, over=over, grade="dusk", vig=1.2, tin=("dissolve", .35))
    import sfx
    steps = [t for a in ppl for t in C.footsteps(a, dur) if t < dur - .2]
    foley = [("step", t, .12, -.3) for t in steps] + [("clank", t + 1.0 + (anc["seat_xs"][0] + 140) / 420, .12, 0, dict(pitch=160)) for t in arrive[:3]]
    amb = sfx.room_tone(dur + .5, seed=980, clock=True, street=.12) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_fed_deal(w, h, dur, ctx):
    """23 Sept 1998 (reconstruction): the clock near six; a term sheet is passed down the table and signed; its
    three terms rise as they are said: about $3.6bn, 14 firms, 90% of the fund (Federal Reserve History; PWG 1999)."""
    clock = [[0, 17, 52], [dur, 17, 52 + dur / 60 * 4]]
    layers_, anc = boardroom_1998(clock, dur, seed=9)
    t1 = max(1.0, word_t(ctx, 0, "three point six"))
    t2 = max(t1 + 1.0, word_t(ctx, 0, "fourteen"))
    t3 = max(t2 + 1.0, word_t(ctx, 1, "ninety"))
    xs = anc["seat_xs"]
    sign_t = [.6 + k * .9 for k in range(4)]
    def after(k, t0):                       # 18 Nov: after signing, each banker keeps living: looks along the table, nods, reads
        out, t, j = [], t0, 0
        while t < dur:
            out.append([round(t, 2), C.pose(("seated", "sit_read", "seated")[j % 3], head=(-10, 6, 12, -4)[(j + k) % 4], brow=(.4 if j % 2 else 0))])
            t += 1.1 + .25 * ((k + j) % 3)
            j += 1
        return out
    keys = {k: [[0, C.pose("seated")], [t, C.pose("sit_write", head=14)], [t + .8, C.pose("sit_write", head=12)], [t + 1.1, C.pose("seated", head=-4)], *after(k, t + 2.0)]
            for k, t in enumerate(sign_t)}
    ppl = [C.actor(f"d{k}", FED_LOOKS[k % len(FED_LOOKS)], pos=[[0, xs[k + 1], anc["seat_y"]]], scale=.9, seed=60 + k, dir=1 if k % 2 else -1, walk=False,
                   pose_keys=keys.get(k) or [[0, C.pose("seated")], *after(k, 1.0)]) for k in range(5)]
    sheets = "".join(f'<g transform="translate({xs[k + 1] + 40},{anc["table_y"] - 8}) rotate(-4)">' + _r(-44, -12, 88, 14, PAPER, sw=2)
                     + f'<path d="M-30,-6 L-12,-9 L4,-4 L26,-8" fill="none" stroke="{TEAL}" stroke-width="2.5" {C.kv(dash=[[0, 0], [t + .2, 0], [t + .9, 1]])}/></g>'
                     for k, t in enumerate(sign_t))
    sheet = term_sheet(760, 420, terms=("ABOUT $3.6BN, NEW EQUITY", "14 BANKS AND FIRMS", "90% OF THE FUND"), t_terms=(t1, t2, t3))
    big = (f'<g {C.kv(translate=[[t * .5, 0, 6 * math.sin(t * 1.3)] for t in range(int(dur * 2) + 2)])}>' + kt(sheet, None, max(.4, t1 - .8), .5) + "</g>")
    layers = [lay(z, s, noblur=(k == "glow")) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.8, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.85, layers_["table"][1] + sheets))
    layers.append(lay(.9, big))
    zx = lambda x, z=.85: 960 + (x - 960) / z
    cam = [[0, zx(560), 620, .9], [t1 - .6, zx(700), 520, 1.0, "inout"], [dur, zx(860), 490, 1.12, "sine"]]
    over = [title("September 23, 1998", "About 6 p.m.", w, h, d=min(2.8, t1 - .6)), badge("Reconstruction · terms from Federal Reserve History", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, .85], [t1, .9]], dof=4, shake=.25, over=over, grade="dusk", vig=1.2, tin=("dissolve", .35))
    import sfx
    foley = [("quill", t + .2, .3, -.3 + .2 * k, dict(sec=.7)) for k, t in enumerate(sign_t)] + [("paper", t1 - .8, .35, 0)]
    foley += [("hit", t, .35, 0, dict(pitch=p)) for t, p in ((t1 + .2, 196), (t2 + .2, 220), (t3 + .2, 247))]
    amb = sfx.room_tone(dur + .5, seed=981, clock=True, street=.1) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


SHOTS = dict(capital_hook=shot_capital_hook, gap_close=shot_gap_close, gap_open=shot_gap_open, fed_evening=shot_fed_evening, fed_deal=shot_fed_deal)


if __name__ == "__main__":
    # stills for a quick look: python3 build/cine_1998.py [name ...]
    names = sys.argv[1:] or list(SHOTS)
    work = C.OUT / "cine-1998-stills"
    work.mkdir(parents=True, exist_ok=True)
    demo = dict(segs=[("On the second of September, nineteen ninety eight, a hedge fund wrote to its investors.", .3, 4.6),
                      ("In August alone, it had lost one point eight billion dollars, and the gap got wider and wider, fourteen firms.", 4.8, 9.6),
                      ("It ended with ninety percent of the fund.", 9.8, 12.0)])
    for nm in names:
        built = SHOTS[nm](1920, 1080, 12.5, demo)
        html, total = C.film_html(built["shots"], 1920, 1080)
        print(nm, C.stills(html, [1.0, total * .4, total * .7, total - .3], work, nm))
