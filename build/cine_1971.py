"""
Filmed beats for YouTube #8, the closing of the gold window (14 Nov 2026). Sets, props and shots for build/cine.py,
used by build/youtube_ep008.py as kind="cine" beats. Four new sets, the first of the 1960s and 1970s and the first
modern dealing room (cinematic-standard.md section 8, step 3: sets).

Sets (our own generic drawings; no real room, building or person is copied; everything is badged):
  living_room_1971()   a 1971 living room at night: wallpaper, a window, two armchairs side-on, a floor lamp, a
                       wall clock at nine, a wooden console television whose screen content is passed in
  vault_1971()         a gold vault: concrete walls, steel cages with stacked bars, hanging lamps with light shafts,
                       a steel counter, a round vault door
  dealing_room()       a dealing room: a split-flap price board whose rows count on cue, windows on a city, desks
                       with telephones (handsets lift when they ring) and typewriters
  lodge_1971()         a wooden lodge room: log walls, a window on swaying trees, a stone fireplace with a fire, a
                       long table and an easel

Shots (fn(w, h, dur, ctx) -> dict(shots, foley, amb); ctx["segs"] are the beat's sentences, (text, start, end)):
  tv_hook       the hook: the room, the set on; push to the screen; the quote appears on "temporarily"
  vault_window  an official brings a bundle of dollars to the counter; a clerk pushes a cart of gold to it
  vault_count   insert: $35,000,000 on the counter, bars stack, the ounce counter runs to 1,000,000 (our example)
  vault_gap     1966: the foreign-held dollars against the gold, only $3.2bn of it available (IMF figures)
  london_1960   the London board: official 35.00, market 35.00 to 40.00 on the word
  flood_1971    the week after 6 August 1971: phones ring, the board counts $3.7bn
  camp_arrive   advisers arrive at the lodge and sit
  camp_plan     a figure at the easel writes the plan's three parts as they are named
  speech        the room again: the screen lists the three measures as each is said
  market_1972   official 38 against the market's approximate 60 and 90
  wallet        the set is off; a man takes a dollar bill from his wallet, looks at it, nothing has changed
Facts on screen come only from the sources in youtube_ep008.py's docstring. No figure is a portrait: the people
named in the narration are not drawn as themselves, and nobody on screen speaks.
"""

import math
import pathlib
import random
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402
from cine_1907 import lay, badge, title, seg_t, word_t   # noqa: E402

INK, RED, TEAL, MUSTARD, PAPER = C.INK, C.RED, C.TEAL, C.MUSTARD, "#F7F5F2"
GOLD, GOLD2 = "#E2B43C", "#B98A22"
_r, _t = L._r, L._t


def kt(text, words_t, at, d=.5):
    """An SVG group that fades in at 'at' and rises a few px (for on-screen items)."""
    return f'<g {C.kv(opacity=[[0, 0], [at - .01, 0], [at + d, 1]], translate=[[0, 0, 14], [at, 0, 14], [at + d, 0, 0, "out"]])}>{text}</g>'


# ------------------------------------------------------------------------------------------------ props

def gold_bar(x, y, s=1.0, extra=""):
    """A bar seen side-on: a trapezoid with a lit top face."""
    w, h, top = 120 * s, 34 * s, 92 * s
    d = (w - top) / 2
    return (f'<g transform="translate({x:.1f},{y:.1f})" {extra}><path d="M0,0 L{w:.1f},0 L{w - d:.1f},{-h:.1f} L{d:.1f},{-h:.1f} Z" fill="{GOLD}" '
            f'stroke="{INK}" stroke-width="{2.6 * s:.1f}"/><path d="M{d + 6 * s:.1f},{-h + 6 * s:.1f} L{w - d - 6 * s:.1f},{-h + 6 * s:.1f}" stroke="#F6DC8A" '
            f'stroke-width="{4 * s:.1f}" stroke-linecap="round"/><path d="M{4 * s:.1f},{-3 * s:.1f} L{w - 4 * s:.1f},{-3 * s:.1f}" stroke="{GOLD2}" stroke-width="{3 * s:.1f}"/></g>')


def bar_stack(x, y, rows, s=.8):
    """A pyramid of bars, bottom row first."""
    out = ""
    for r, n in enumerate(rows):
        for k in range(n):
            out += gold_bar(x + (k + r * .5) * 112 * s, y - r * 32 * s, s)
    return out


def dollar_bundle(w=150, h=64, label="", s=1.0):
    """A banded stack of notes (generic green paper, no real note's design)."""
    out = ""
    for k in range(4):
        out += _r(-w / 2 + k * 2, -h + k * 6 - 24, w, 18, "#8FB08A" if k % 2 else "#A3C29C", rx=3, sw=2)
    out += _r(-w / 2, -h + 4, w, h - 4, "#9DBD95", rx=4, sw=2.6) + _r(-16, -h + 4, 32, h - 4, PAPER, sw=2)
    if label:
        out += _t(0, -h / 2 + 12, label, 22, fill=INK, weight=700, family="Sans")
    return f'<g transform="scale({s})">{out}</g>'


def dollar_bill(w=150, h=64):
    """One generic note: green paper, a border, a '1' in two corners (no real design copied)."""
    return (f'<g>{_r(-w / 2, -h / 2, w, h, "#B6CFA8", rx=4, sw=2.4)}{_r(-w / 2 + 7, -h / 2 + 7, w - 14, h - 14, "none", rx=3, sw=1.6)}'
            f'<ellipse cx="0" cy="0" rx="{h * .32:.0f}" ry="{h * .36:.0f}" fill="#9FBF92" stroke="{INK}" stroke-width="1.6"/>'
            + _t(-w / 2 + 18, -h / 2 + 24, "1", 18, fill="#2F4A2A", family="Sans") + _t(w / 2 - 18, h / 2 - 10, "1", 18, fill="#2F4A2A", family="Sans") + "</g>")


def desk_phone(x, y, ring_at=(), lift=None, color="#2A2522"):
    """A 1960s desk telephone. ring_at: times its handset jiggles (ringing); lift: (t_up, t_down) the handset goes up
    and away (somebody answered), or None."""
    jig = []
    for t in ring_at:
        jig += [[t, 0, 0, 0], [t + .05, 0, -3, -4], [t + .1, 0, 0, 3], [t + .15, 0, -3, -4], [t + .2, 0, 0, 3], [t + .25, 0, -2, -3], [t + .32, 0, 0, 0]]
    op = [[0, 1]]
    if lift:
        op = [[0, 1], [lift[0] - .01, 1], [lift[0], 0]] + ([[lift[1], 0], [lift[1] + .01, 1]] if lift[1] else [])
    tr = sorted(jig, key=lambda k: k[0]) or [[0, 0, 0, 0]]
    return (f'<g transform="translate({x},{y})">{_r(-46, -34, 92, 34, color, rx=10, sw=2.6)}'
            f'<circle cx="0" cy="-18" r="12" fill="#E8E1D4" stroke="{INK}" stroke-width="2"/>'
            f'<g {C.kv(translate=tr, opacity=op)}><path d="M-52,-40 C-50,-56 50,-56 52,-40 L40,-38 C30,-46 -30,-46 -40,-38 Z" fill="{color}" stroke="{INK}" stroke-width="2.6"/></g></g>')


def handset():
    """A handset held to the ear (for a figure on the phone)."""
    return (f'<g transform="rotate(-80)"><path d="M-8,-30 C-20,-26 -20,26 -8,30 L2,26 C-6,12 -6,-12 2,-26 Z" fill="#2A2522" stroke="{INK}" stroke-width="2.4"/></g>')


def typewriter(x, y):
    return (f'<g transform="translate({x},{y})">{_r(-60, -40, 120, 40, "#5A6068", rx=6, sw=2.6)}{_r(-50, -58, 100, 20, "#3B3F48", rx=8, sw=2.4)}'
            f'<rect x="-30" y="-96" width="60" height="44" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<path d="M-22,{-86 + 8 * k} L{18 - 10 * (k % 2)},{-86 + 8 * k}" stroke="#CFC6B6" stroke-width="2"/>' for k in range(4)) + "</g>")


# ------------------------------------------------------------------------------------------------ sets

def tv_screen(items=(), quote=None, off=False):
    """What the set shows, in screen coordinates of the console (screen 1380..1700 x 670..900). items: [(t, text)]
    appear one under another; quote: (t, lines) a quote card; off: the set is dark."""
    x0, y0, w, h = 1380, 670, 320, 230
    clip = f'<clipPath id="scr"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="26"/></clipPath>'
    if off:
        return (f'<defs>{clip}</defs><rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="26" fill="#2B2F2E" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M{x0 + 30},{y0 + 30} Q{x0 + 90},{y0 + 10} {x0 + 150},{y0 + 26}" stroke="#55605C" stroke-width="6" fill="none" opacity=".6"/>')
    g = (f'<defs>{clip}<linearGradient id="scrg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9DB3B8"/>'
         f'<stop offset="1" stop-color="#6F878D"/></linearGradient><pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
         f'<rect width="4" height="2" fill="#000" opacity=".12"/></pattern></defs>'
         f'<g clip-path="url(#scr)"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#scrg)"/>')
    # a generic broadcast set: drapes, a desk, a seated speaker as a soft silhouette (nobody's likeness)
    g += (f'<rect x="{x0}" y="{y0}" width="44" height="{h}" fill="#5D6F74"/><rect x="{x0 + w - 44}" y="{y0}" width="44" height="{h}" fill="#5D6F74"/>'
          f'<path d="M{x0 + 112},{y0 + 196} C{x0 + 112},{y0 + 140} {x0 + 208},{y0 + 140} {x0 + 208},{y0 + 196} Z" fill="#2E3A3E"/>'
          f'<circle cx="{x0 + 160}" cy="{y0 + 118}" r="24" fill="#2E3A3E"/>'
          f'<rect x="{x0 + 60}" y="{y0 + 188}" width="200" height="42" fill="#3E4C50"/>')
    g += (f'<rect x="{x0}" y="{y0 + 12}" width="{w}" height="24" fill="#1E2A2E" opacity=".75"/>'
          + _t(x0 + w / 2, y0 + 30, "ADDRESS TO THE NATION", 14, fill="#F4ECDD", weight=600, family="Sans", extra='letter-spacing="3"'))
    if quote:
        qt, lines = quote
        card = (f'<rect x="{x0 + 18}" y="{y0 + 52}" width="{w - 36}" height="{24 + 22 * len(lines)}" rx="6" fill="#F4ECDD" stroke="{INK}" stroke-width="2"/>'
                + "".join(_t(x0 + 32, y0 + 76 + 22 * k, ln, 15, fill=INK, anchor="start", weight=600, family="Sans") for k, ln in enumerate(lines)))
        g += kt(card, None, qt, .4)
    for k, (t, text) in enumerate(items):
        card = (f'<rect x="{x0 + 18}" y="{y0 + 48 + 44 * k}" width="{w - 36}" height="38" rx="6" fill="#F4ECDD" stroke="{INK}" stroke-width="2"/>'
                f'<rect x="{x0 + 18}" y="{y0 + 48 + 44 * k}" width="38" height="38" rx="6" fill="{RED}" stroke="{INK}" stroke-width="2"/>'
                + _t(x0 + 37, y0 + 74 + 44 * k, str(k + 1), 20, fill="#fff", family="Sans")
                + _t(x0 + 66, y0 + 73 + 44 * k, text, 15, fill=INK, anchor="start", weight=700, family="Sans"))
        g += kt(card, None, t, .35)
    g += (f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#scan)"/>'
          f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#DDEFF2" data-flick=\'[0.06,0.05,3]\'/></g>'
          f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="26" fill="none" stroke="{INK}" stroke-width="5"/>'
          f'<path d="M{x0 + 24},{y0 + 30} Q{x0 + 90},{y0 + 8} {x0 + 160},{y0 + 22}" stroke="#fff" stroke-width="6" fill="none" opacity=".25"/>')
    return g


def living_room_1971(screen=None, off=False, seed=3):
    """A living room on a summer night in 1971. Returns (layers, anchors). The console's screen is centred at
    (1540, 785) on the z .78 layer; the armchairs' occupants sit with their feet at y 1000 (z .72)."""
    rng = random.Random(seed)
    wall = C.defs() + f'<rect x="-1600" y="-900" width="5200" height="2600" fill="#C9A46A"/>'
    for x in range(-1600, 3600, 64):                                                   # wallpaper stripes
        wall += f'<rect x="{x}" y="-900" width="22" height="1800" fill="#BD9659" opacity=".55"/>'
    for x in range(-1600, 3600, 128):
        wall += "".join(f'<circle cx="{x + 43}" cy="{y}" r="9" fill="none" stroke="#A8824A" stroke-width="3" opacity=".6"/>' for y in range(-60, 880, 120))
    # the window: night, an invented street with lit windows and a lamp glow
    wx, wy, ww, wh = 40, 170, 480, 470
    win = (f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="#1C2642"/>'
           f'<circle cx="{wx + 380}" cy="{wy + 300}" r="120" fill="url(#glowWarm)" opacity=".45"/>')
    bx = wx
    while bx < wx + ww:
        bw, bh = rng.uniform(60, 120), rng.uniform(120, 300)
        win += f'<rect x="{bx:.0f}" y="{wy + wh - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="#2A3352"/>'
        for r_ in range(int(bh // 40)):
            for c_ in range(int(bw // 28)):
                if rng.random() < .3:
                    win += f'<rect x="{bx + 8 + c_ * 28:.0f}" y="{wy + wh - bh + 12 + r_ * 40:.0f}" width="12" height="16" fill="{MUSTARD}" opacity=".8" data-flick=\'[0.8,0.08,{rng.randint(0, 9)}]\'/>'
        bx += bw + 6
    win += (f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#F1E6CF" stroke-width="16"/>'
            f'<path d="M{wx + ww / 2},{wy} L{wx + ww / 2},{wy + wh} M{wx},{wy + wh / 2} L{wx + ww},{wy + wh / 2}" stroke="#F1E6CF" stroke-width="10"/>')
    for side, x in ((1, wx - 70), (-1, wx + ww - 10)):                                # curtains that stir
        win += (f'<g data-swing=\'[1.2,{0.9 + .2 * side:.1f},{side},{x + 40},{wy - 40}]\'><path d="M{x},{wy - 40} L{x + 80},{wy - 40} C{x + 70},{wy + 200} {x + 96},{wy + 380} {x + 80},{wy + wh + 60} '
                f'L{x},{wy + wh + 60} Z" fill="#B5552E" stroke="{INK}" stroke-width="3"/>'
                + "".join(f'<path d="M{x + 16 + 16 * k},{wy - 30} C{x + 10 + 16 * k},{wy + 200} {x + 24 + 16 * k},{wy + 400} {x + 14 + 16 * k},{wy + wh + 50}" stroke="#97441F" stroke-width="3" fill="none"/>' for k in range(4))
                + "</g>")
    wall += win + _r(-1600, wy - 56, 2400, 18, "#8A5A36", sw=2.4)
    # a picture and the clock at nine
    wall += (_r(700, 250, 260, 170, "#7A4E2E", sw=4) + f'<rect x="716" y="266" width="228" height="138" fill="#E9D3A0"/>'
             f'<path d="M716,370 C780,320 840,350 944,300 L944,404 L716,404 Z" fill="#6E8F5E"/><circle cx="890" cy="300" r="22" fill="{RED}" opacity=".8"/>')
    cx_, cy_ = 1180, 250
    wall += (f'<g transform="translate({cx_},{cy_})"><circle r="62" fill="#F4ECDD" stroke="{INK}" stroke-width="5"/>'
             + "".join(f'<path d="M{50 * math.sin(math.radians(a)):.1f},{-50 * math.cos(math.radians(a)):.1f} L{42 * math.sin(math.radians(a)):.1f},{-42 * math.cos(math.radians(a)):.1f}" stroke="{INK}" stroke-width="3"/>' for a in range(0, 360, 30))
             + f'<path d="M0,0 L-30,0" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M0,0 L0,-44" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><circle r="5" fill="{INK}"/></g>')
    wall += f'<rect x="-1600" y="880" width="5200" height="30" fill="#8A5A36" stroke="{INK}" stroke-width="3"/>'
    floor = (f'<rect x="-1600" y="905" width="5200" height="800" fill="#7A4E2E"/>'
             + "".join(f'<path d="M{x},{905 + (x * 7) % 60} l6,-10" stroke="#8E5E38" stroke-width="3"/>' for x in range(-1600, 3600, 23))
             + f'<ellipse cx="900" cy="1040" rx="900" ry="90" fill="#9C6A3A" opacity=".5"/>')
    # two armchairs side-on (back to the left, the occupant faces the set on the right), a lamp, a low table
    chairs = ""
    for ax in (420, 820):
        chairs += (_r(ax - 130, 930, 200, 50, "#3F6E5A", rx=16, sw=3.2) + _r(ax - 150, 730, 50, 250, "#3F6E5A", rx=22, sw=3.2)
                   + _r(ax - 136, 980, 14, 26, "#3A2A20", sw=2) + _r(ax + 50, 980, 14, 26, "#3A2A20", sw=2)
                   + _r(ax - 112, 912, 170, 26, "#4E8068", rx=12, sw=2.6))
    lamp = (f'<rect x="1106" y="560" width="10" height="440" fill="#3A2A20"/><ellipse cx="1111" cy="1000" rx="50" ry="10" fill="#3A2A20"/>'
            f'<path d="M1050,560 L1172,560 L1150,470 L1072,470 Z" fill="#F1D59A" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="1111" cy="600" r="260" fill="url(#glowWarm)" opacity=".5" data-flick=\'[0.5,0.02,4]\'/>')
    tbl = _r(560, 900, 140, 18, "#6B4A32", rx=4, sw=2.6) + _r(574, 918, 12, 80, "#4A3226", sw=2) + _r(674, 918, 12, 80, "#4A3226", sw=2)
    # the console television
    tv = (_r(1330, 640, 470, 300, "#7A4E2E", rx=12, sw=4) + _r(1350, 920, 18, 80, "#4A3226", sw=2.4) + _r(1762, 920, 18, 80, "#4A3226", sw=2.4)
          + "".join(f'<path d="M1720,{680 + 18 * k} L1780,{680 + 18 * k}" stroke="#5A3826" stroke-width="5"/>' for k in range(10))
          + f'<circle cx="1750" cy="880" r="12" fill="#C99A3B" stroke="{INK}" stroke-width="2"/>'
          + (tv_screen(off=True) if off else (screen or tv_screen())))
    glow = "" if off else (f'<path d="M1380,680 L560,1040 L1380,1040 Z" fill="#BFE3F0" opacity=".10" data-flick=\'[0.10,0.05,6]\'/>'
                           f'<ellipse cx="1540" cy="785" rx="330" ry="250" fill="#CFEFF7" opacity=".14" data-flick=\'[0.14,0.06,2]\'/>')
    layers = dict(wall=(0.4, wall), floor=(0.6, floor), chairs=(0.72, chairs + tbl), lamp=(0.74, lamp), tv=(0.78, tv), glow=(0.79, glow))
    return layers, dict(feet=1000, chairs=(420, 820), screen=(1540, 785), tv_z=.78)


def vault_1971(cages=7, seed=4):
    """A gold vault. Returns (layers, anchors). Counter top at y 860 on the z .8 layer, x 700..1300."""
    rng = random.Random(seed)
    wall = C.defs() + (f'<defs><pattern id="mesh" width="26" height="26" patternUnits="userSpaceOnUse">'
                       f'<path d="M0,0 L26,26 M26,0 L0,26" stroke="#7E8784" stroke-width="2.4"/></pattern></defs>'
                       f'<rect x="-1600" y="-900" width="5200" height="2600" fill="#8D948C"/>')
    for x in range(-1600, 3600, 300):
        wall += f'<path d="M{x},-900 L{x},900" stroke="#7A817A" stroke-width="3"/>'
    for y in range(-900, 900, 180):
        wall += f'<path d="M-1600,{y} L3600,{y}" stroke="#7A817A" stroke-width="3"/>'
    for k in range(cages):                                                             # steel cages with bars
        x = -700 + k * 420
        wall += _r(x, 230, 380, 640, "#5E6663", sw=3.4)
        rows = [rng.choice([5, 6]), 5, rng.choice([3, 4, 5]), rng.choice([2, 3])][: rng.choice([3, 4])]
        wall += bar_stack(x + 26, 860, rows, s=.62) + bar_stack(x + 26, 560, [5, 4][: rng.choice([1, 2])], s=.62)
        wall += _r(x + 6, 556, 368, 10, "#4A514E", sw=2)
        wall += f'<rect x="{x}" y="230" width="380" height="640" fill="url(#mesh)" opacity=".55"/>'
        wall += _r(x + 150, 250, 80, 34, "#E8E1D4", rx=4, sw=2)                         # a blank tag
    wall += f'<rect x="-1600" y="870" width="5200" height="40" fill="#6E7570" stroke="{INK}" stroke-width="3"/>'
    lamps = ""
    for lx in range(-400, 2600, 600):
        lamps += (f'<path d="M{lx},-200 L{lx},120" stroke="{INK}" stroke-width="4"/>'
                  f'<path d="M{lx - 70},170 L{lx + 70},170 L{lx + 36},120 L{lx - 36},120 Z" fill="#2E3532" stroke="{INK}" stroke-width="3"/>'
                  + C.shaft(lx - 60, 170, 120, 760, angle=0, op=.16, color="255,236,190"))
    lamps += C.motes(-400, 150, 2800, 700, n=40, op=.5, spd=4, seed=seed)
    door = (f'<g transform="translate(-260,560)"><circle r="300" fill="#9AA29C" stroke="{INK}" stroke-width="6"/><circle r="250" fill="#B4BBB5" stroke="{INK}" stroke-width="4"/>'
            + "".join(f'<circle cx="{270 * math.cos(math.radians(a)):.0f}" cy="{270 * math.sin(math.radians(a)):.0f}" r="10" fill="#7A817A" stroke="{INK}" stroke-width="2"/>' for a in range(0, 360, 30))
            + f'<g data-swing=\'[4,0.4,0,0,0]\'><circle r="56" fill="#7A817A" stroke="{INK}" stroke-width="4"/>'
            + "".join(f'<path d="M0,0 L{110 * math.cos(math.radians(a)):.0f},{110 * math.sin(math.radians(a)):.0f}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>' for a in (0, 120, 240))
            + "</g></g>")
    floor = (f'<rect x="-1600" y="905" width="5200" height="800" fill="#6F7672"/>'
             f'<rect x="-1600" y="905" width="5200" height="800" fill="#fff" opacity=".04"/>'
             + "".join(f'<path d="M{x},905 L{x - 300},1700" stroke="#636A66" stroke-width="3"/>' for x in range(-1600, 3600, 260)))
    counter = (_r(700, 860, 600, 30, "#A9B0AB", rx=4, sw=3.4) + _r(730, 890, 540, 150, "#8E9590", sw=3)
               + _r(700, 856, 600, 6, "#D5DAD6", sw=0))
    plaque = (_r(820, 120, 360, 70, "#2E3532", rx=6, sw=3) + _t(1000, 166, "$35 AN OUNCE", 34, fill="#F6D58A", family="Sans", extra='letter-spacing="4"'))
    layers = dict(wall=(0.35, wall + plaque), lamps=(0.42, lamps), door=(0.5, door), floor=(0.6, floor), counter=(0.8, counter))
    return layers, dict(counter_y=860, counter=(700, 1300), ground=1030)


def board_rows_svg(px, rows, top=250, wid=860):
    """Rows on a split-flap board: (label, keys [[t, v], ...], dec, pre, suf, color). The value counts between keys."""
    out = ""
    for k, (label, keys, dec, pre, suf, col) in enumerate(rows):
        y = top + 90 * k
        out += _r(px - wid / 2 + 20, y - 52, wid - 40, 72, "#1E2422", rx=4, sw=2)
        for j in range(int((wid - 60) / 34)):                                          # flap cells
            out += f'<path d="M{px - wid / 2 + 30 + 34 * j},{y - 16} l28,0" stroke="#2E3633" stroke-width="2"/>'
        out += _t(px - wid / 2 + 44, y, label, 30, fill="#E8E1D4", anchor="start", weight=600, family="Sans", extra='letter-spacing="3"')
        v0 = keys[0][1]
        out += (f'<text x="{px + wid / 2 - 44}" y="{y + 4}" text-anchor="end" font-family="\'Sans\',sans-serif" font-weight="700" font-size="46" fill="{col}" '
                f'{C.kv(count=keys)} data-dec="{dec}" data-pre="{pre}" data-suf="{suf}">{pre}{v0:.{dec}f}{suf}</text>')
    return out


def dealing_room(head="", sub="", rows=(), ring=(), lifts=(), city="day", seed=5):
    """A dealing room. Returns (layers, anchors). The board is centred at x 960 on the z .38 layer; desks at y 880
    on the z .78 layer, feet at y 1010 behind them (z .74) and y 1090 in front (z .9)."""
    rng = random.Random(seed)
    wall = C.defs() + f'<rect x="-1600" y="-900" width="5200" height="2600" fill="#D9D0BC"/>'
    sky = ("#AFC0C6", "#E4E2D8") if city == "day" else ("#3A4560", "#C98A5A")
    wall += (f'<defs><linearGradient id="dsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky[0]}"/>'
             f'<stop offset="1" stop-color="{sky[1]}"/></linearGradient></defs>')
    for wx in (-760, -360, 1700, 2100):                                                # tall windows on an invented city
        wall += f'<rect x="{wx}" y="140" width="300" height="600" fill="url(#dsky)"/>'
        x = wx
        while x < wx + 300:
            bw, bh = rng.uniform(40, 90), rng.uniform(160, 420)
            wall += f'<rect x="{x:.0f}" y="{740 - bh:.0f}" width="{min(bw, wx + 300 - x):.0f}" height="{bh:.0f}" fill="#8D9498" opacity=".8"/>'
            x += bw + 4
        wall += (f'<rect x="{wx}" y="140" width="300" height="600" fill="none" stroke="#8A7F6C" stroke-width="14"/>'
                 f'<path d="M{wx + 150},140 L{wx + 150},740" stroke="#8A7F6C" stroke-width="8"/>')
    wall += f'<rect x="-1600" y="760" width="5200" height="24" fill="#B8A889" stroke="{INK}" stroke-width="3"/>'
    # the board
    bw_ = 900
    wall += '<g transform="translate(960,70) scale(1.3) translate(-960,-90)">'
    wall += _r(960 - bw_ / 2, 90, bw_, 150 + 90 * max(len(rows), 1), "#2A302D", rx=8, sw=5)
    wall += _t(960, 150, head, 40, fill="#F4ECDD", weight=700, family="Sans", extra='letter-spacing="5"')
    if sub:
        wall += _t(960, 190, sub, 22, fill="#B9C2BC", weight=600, family="Sans", extra='letter-spacing="4"')
    wall += board_rows_svg(960, rows, top=270, wid=bw_) + "</g>"
    light = "".join(C.shaft(x, 150, 240, 900, angle=-18, op=.16) for x in (-700, -300, 1760, 2160))
    floor = f'<rect x="-1600" y="905" width="5200" height="800" fill="#7E7462"/><rect x="-1600" y="905" width="5200" height="800" fill="url(#boards)" opacity=".18"/>'
    desks = ""
    ph = 0
    for k, dx in enumerate(range(-300, 2400, 380)):
        desks += _r(dx, 880, 320, 26, "#C9BBA0", rx=3, sw=3) + _r(dx + 10, 906, 300, 110, "#A8987C", sw=2.6)
        rt = [t for (i, t) in ring if i == k]
        lf = next((l for (i, *l) in lifts if i == k), None)
        desks += desk_phone(dx + 70, 880, ring_at=rt, lift=lf)
        desks += typewriter(dx + 230, 880) if k % 2 else (f'<g transform="translate({dx + 220},876) rotate(-3)">' + _r(-60, -8, 120, 10, PAPER, sw=2) + "</g>")
        ph += 1
    layers = dict(wall=(0.38, wall), light=(0.45, light), floor=(0.6, floor), desks=(0.78, desks))
    return layers, dict(feet_back=1010, feet_front=1095, board_x=960, desk_xs=list(range(-300, 2400, 380)))


def lodge_1971(easel_items=(), seed=8):
    """A wooden lodge room. Returns (layers, anchors). Table top at y 860 (z .85), seated feet at y 990 (z .78);
    the easel paper is centred at (1560, 640) on the z .8 layer."""
    rng = random.Random(seed)
    wall = C.defs() + f'<rect x="-1600" y="-900" width="5200" height="2600" fill="#8A5A36"/>'
    for y in range(-900, 900, 46):                                                     # logs
        wall += (f'<rect x="-1600" y="{y}" width="5200" height="44" rx="20" fill="#9A6A42" stroke="#5E3D27" stroke-width="3"/>'
                 f'<path d="M-1600,{y + 30} L3600,{y + 30}" stroke="#7E5434" stroke-width="2" opacity=".6"/>')
    # a wide window on trees
    wx, wy, ww, wh = -200, 160, 900, 520
    win = f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="#CFE0D8"/>'
    for k in range(9):
        tx = wx + 40 + k * 100 + rng.uniform(-20, 20)
        th = rng.uniform(260, 420)
        win += (f'<g data-swing=\'[{rng.uniform(.8, 1.6):.1f},{rng.uniform(.5, .9):.2f},{k},{tx:.0f},{wy + wh}]\'>'
                f'<path d="M{tx - 70},{wy + wh} L{tx},{wy + wh - th} L{tx + 70},{wy + wh} Z" fill="{["#3F6E4A", "#4E7F56", "#335C3E"][k % 3]}" stroke="{INK}" stroke-width="2.4"/></g>')
    win += (f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#5E3D27" stroke-width="18"/>'
            + "".join(f'<path d="M{wx + ww * k / 3},{wy} L{wx + ww * k / 3},{wy + wh}" stroke="#5E3D27" stroke-width="10"/>' for k in (1, 2)))
    wall += win
    # a stone fireplace with a fire
    fx = 2050
    fire = (_r(fx - 260, 300, 520, 600, "#9C9488", sw=4)
            + "".join(_r(fx - 260 + (j % 2) * 40 + 80 * i, 300 + 60 * j, 80, 60, "#A9A194", sw=2) for j in range(10) for i in range(6) if fx - 260 + (j % 2) * 40 + 80 * i < fx + 220)
            + _r(fx - 150, 640, 300, 260, "#2A1E18", rx=10, sw=3) + _r(fx - 300, 600, 600, 40, "#6B4A32", sw=3))
    for k in range(5):
        fire += (f'<g data-swing=\'[{6 + k},{3 + k * .7:.1f},{k},{fx - 80 + 40 * k},880]\'><path d="M{fx - 110 + 44 * k},880 C{fx - 130 + 44 * k},{820 - 10 * k} {fx - 80 + 44 * k},{780 - 20 * (k % 3)} '
                 f'{fx - 90 + 44 * k},{740 - 20 * (k % 2)} C{fx - 60 + 44 * k},{790} {fx - 50 + 44 * k},{830} {fx - 70 + 44 * k},880 Z" fill="{["#F2C35B", "#E8862F", "#D93A12"][k % 3]}" '
                 f'stroke="{INK}" stroke-width="2" data-flick=\'[0.9,0.1,{k}]\'/></g>')
    glow = f'<circle cx="{fx}" cy="800" r="520" fill="url(#candle)" opacity=".55" data-flick=\'[0.55,0.08,7]\'/>'
    floor = f'<rect x="-1600" y="905" width="5200" height="800" fill="#5E3D27"/><rect x="-1600" y="905" width="5200" height="800" fill="url(#boards)" opacity=".4"/>'
    table = (_r(60, 860, 1260, 36, "#6B4A32", rx=6, sw=3.6) + _r(90, 896, 1200, 30, "#4A3226", sw=3)
             + _r(130, 926, 30, 150, "#4A3226", sw=2.6) + _r(1220, 926, 30, 150, "#4A3226", sw=2.6)
             + "".join(f'<g transform="translate({200 + 200 * k},854) rotate({(-3, 2, -2, 4, -1, 3)[k]})">' + _r(-44, -8, 88, 10, PAPER, sw=2) + "</g>" for k in range(6))
             + "".join(f'<g transform="translate({300 + 300 * k},852)">' + L.cup() + "</g>" for k in range(3)))
    # the easel: a paper pad on which the plan is written item by item
    ex, ey = 1560, 640
    easel = (f'<path d="M{ex - 150},{ey + 480} L{ex - 40},{ey - 260} M{ex + 150},{ey + 480} L{ex + 40},{ey - 260} M{ex},{ey - 260} L{ex},{ey + 500}" stroke="#4A3226" stroke-width="16" stroke-linecap="round"/>'
             + _r(ex - 210, ey - 260, 420, 440, PAPER, rx=4, sw=4) + _r(ex - 220, ey - 274, 440, 24, "#4A3226", sw=3))
    for k, (t, text) in enumerate(easel_items):
        ln = _t(ex - 180, ey - 170 + 110 * k, f"{k + 1}  {text}", 44, fill=INK if k else RED, anchor="start", weight=700, family="Serif")
        ul = f'<path d="M{ex - 182},{ey - 156 + 110 * k} L{ex + 170},{ey - 156 + 110 * k}" stroke="{TEAL}" stroke-width="5" {C.kv(dash=[[0, 0], [t + .2, 0], [t + .9, 1]])}/>'
        easel += f'<g {C.kv(clip=[[0, 0, 100, 0, 0], [t - .01, 0, 100, 0, 0], [t + .7, 0, 0, 0, 0]])}>{ln}</g>' + ul
    layers = dict(wall=(0.35, wall + fire), glow=(0.5, glow), floor=(0.6, floor), easel=(0.8, easel), table=(0.85, table))
    return layers, dict(table_y=860, seat_y=990, easel=(ex, ey), stand_y=1040)


# ------------------------------------------------------------------------------------------------ people

def armchair_people(dur, lean_at=None, react="concern"):
    """A man and a woman in the armchairs facing the set; lean_at: they lean in and react."""
    keys_m = [[0, C.pose("seated", head=-4)], [dur, C.pose("seated", head=-2)]]
    keys_w = [[0, C.pose("seated", head=2)], [dur, C.pose("seated", head=0)]]
    if lean_at:
        keys_m = [[0, C.pose("seated", head=-4)], [lean_at, C.pose("seated", head=-4)], [lean_at + .5, C.pose("seated", lean=14, head=6, brow=1, mouth=2)],
                  [dur, C.pose("seated", lean=12, head=4, brow=.6)]]
        keys_w = [[0, C.pose("seated")], [lean_at + .3, C.pose("seated")], [lean_at + .8, C.pose("seated", head=-18, brow=1)],
                  [lean_at + 1.6, C.pose("seated", head=-16, brow=1, mouth=2)], [dur, C.pose("seated", head=-6, brow=.4)]]
    m = C.actor("man", "home_1971", pos=[[0, 340, 1000]], scale=.95, seed=5, dir=1, walk=False, pose_keys=keys_m)
    w_ = C.actor("wife", "lady_1971", pos=[[0, 740, 1000]], scale=.92, seed=9, dir=1, walk=False, pose_keys=keys_w)
    return [m, w_]


def advisers(n, x0, gap, seat_y, dur, keys=None, prefix="a", scale=.9):
    looks = ("suit_1971", "suit_1971b", "suit_1971c", "suit_1971d")
    out = []
    for i in range(n):
        pk = (keys or {}).get(i) or [[0, C.pose("seated", head=3 * ((i % 3) - 1))], [dur, C.pose("seated", head=-3 * ((i % 3) - 1))]]
        out.append(C.actor(f"{prefix}{i}", looks[i % len(looks)], pos=[[0, x0 + i * gap, seat_y]], scale=scale, seed=60 + i,
                           dir=1 if i % 2 == 0 else -1, walk=False, pose_keys=pk))
    return out


def traders(anc, dur, react_at=None, mood="concern", n=6, seed=71, phones=(), prefix="t"):
    """Traders standing between the desks; phones: indices holding a handset to the ear."""
    rng = random.Random(seed)
    looks = ("suit_1971b", "suit_1971", "suit_1971d", "suit_1971c")
    out = []
    for i in range(n):
        x = -140 + i * 380 + rng.uniform(-30, 30)
        d = 1 if x < anc["board_x"] else -1
        on_phone = i in phones
        base = dict(shF=150, elF=130, head=-6) if on_phone else dict()
        keys = [[0, C.pose("relaxed", head=-12, **({k: v for k, v in base.items() if k != "head"}))],
                [0.8 + .4 * i, C.pose("talk_a" if i % 2 else "talk_b", head=-10, **({k: v for k, v in base.items() if k != "head"}))]]
        if react_at is not None:
            keys += [[react_at + .1 * i, C.pose("relaxed", head=-16, **({k: v for k, v in base.items() if k != "head"}))],
                     [react_at + .4 + .1 * i, C.pose(mood if (i % 3 or on_phone) else "point", brow=1 if mood == "cheer" else -1, head=-18,
                                                     **({k: v for k, v in base.items() if k != "head"}))],
                     [dur, C.pose(mood, head=-14, **({k: v for k, v in base.items() if k != "head"}))]]
        out.append(C.actor(f"{prefix}{i}", looks[i % len(looks)], pos=[[0, x, anc["feet_back"] + (i % 2) * 10]], scale=.9 + .03 * (i % 3),
                           seed=seed + i, dir=d, walk=False, pose_keys=keys, holdF=handset() if on_phone else ""))
    return out


# ------------------------------------------------------------------------------------------------ shots

def shot_tv_hook(w, h, dur, ctx):
    """Sunday 15 August 1971, 9 p.m.: wide on the room, the set on; push to the screen; the quote card appears on
    'temporarily' (a verbatim line from the address, the American Presidency Project text)."""
    t_q = min(dur - 1.5, max(1.5, word_t(ctx, 1, "suspend")))
    scr = tv_screen(quote=(t_q, ["“I have directed Secretary Connally", "to suspend temporarily the", "convertibility of the dollar", "into gold”"]))
    layers_, anc = living_room_1971(screen=scr)
    ppl = armchair_people(dur, lean_at=t_q)
    layers = [lay(z, s, noblur=(k in ("glow", "lamp"))) for k, (z, s) in layers_.items() if k not in ("tv", "glow")]
    layers.append(lay(.72, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.78, layers_["tv"][1]))
    layers.append(lay(.79, layers_["glow"][1], noblur=True))
    sx, sy = anc["screen"]
    kx, ky = 960 + (sx - 960) / .78, 540 + (sy - 540) / .78
    cam = [[0, 980, 600, 1.0], [max(1.2, t_q - 1.2), 1180, 610, 1.18, "sine"], [t_q + .8, kx, ky, 4.4, "inout"], [dur, kx, ky, 4.7, "sine"]]
    over = [title("Sunday, August 15, 1971", "9 p.m.", w, h, d=min(3.4, t_q - .6)), badge("Reconstruction · not a portrait", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, .74], [t_q, .78], [dur, .78]], dof=6, shake=.3, over=over, grade="dusk", vig=1.25)
    import sfx
    foley = [("tick", t, .2, .3) for t in np.arange(.4, dur, 1.0)] + [("hit", t_q, .5, .2, dict(pitch=110))]
    amb = sfx.room_tone(dur + .5, seed=21, clock=False, street=.04)
    return dict(shots=[shot], foley=foley, amb=amb * .7)


def shot_speech(w, h, dur, ctx):
    """The address, the three measures: the screen lists each as the narration names it (sentences 2, 3 and 4)."""
    # each item lands on the sentence that names it ("First, ...", "Second, ...", "Third, ..."), found by its first
    # word, not by its index: the first render put item 2 on the sentence after "First" (caught in the motion sheet)
    segs = ctx.get("segs") or []
    def at(word, k):
        for i, (x, a, b) in enumerate(segs):
            if x.strip().lower().startswith(word):
                return a + .15 * (b - a)
        return seg_t(ctx, k, .15)
    items = [(at("first", 1), "GOLD WINDOW CLOSED"), (at("second", 2), "90-DAY FREEZE: PRICES, WAGES"), (at("third", 3), "EXTRA 10% TAX ON IMPORTS")]
    layers_, anc = living_room_1971(screen=tv_screen(items=items))
    ppl = armchair_people(dur, lean_at=items[0][0])
    layers = [lay(z, s, noblur=(k in ("glow", "lamp"))) for k, (z, s) in layers_.items() if k not in ("tv", "glow")]
    layers.append(lay(.72, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.78, layers_["tv"][1]))
    layers.append(lay(.79, layers_["glow"][1], noblur=True))
    sx, sy = anc["screen"]
    kx, ky = 960 + (sx - 960) / .78, 540 + (sy - 540) / .78
    t1 = items[0][0]
    cam = [[0, 1300, 640, 1.45], [max(.8, t1 - .6), 1420, 660, 1.6, "sine"], [t1 + .4, kx, ky + 10, 4.4, "inout"], [dur, kx, ky + 4, 4.6, "sine"]]
    over = [badge("Reconstruction · the three measures as announced", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, .76], [dur, .78]], dof=6, shake=.25, over=over, grade="dusk", vig=1.2,
                tin=("dissolve", .4))
    import sfx
    foley = [("hit", t + .05, .4, .2, dict(pitch=196 - 20 * k)) for k, (t, _) in enumerate(items)]
    amb = sfx.room_tone(dur + .5, seed=22, clock=False, street=.04)
    return dict(shots=[shot], foley=foley, amb=amb * .7)


def shot_wallet(w, h, dur, ctx):
    """The set is off. A man stands by his chair, takes a dollar bill from his wallet, looks at it; nothing about it
    has changed (our illustration of the point in the narration)."""
    layers_, anc = living_room_1971(off=True)
    t_up = min(dur - 1.6, max(1.0, seg_t(ctx, 1, .1)))
    bill = f'<g {C.kv(opacity=[[0, 0], [t_up - .4, 0], [t_up - .2, 1]])}>{dollar_bill(110, 48)}</g>'
    man = C.actor("man", "home_1971", pos=[[0, 540, 1000]], scale=1.0, seed=5, dir=-1, walk=False, holdF=bill, upright=True,
                  pose_keys=[[0, C.pose("relaxed", head=-6)], [t_up - .6, C.pose("reach", shF=40, elF=60, head=10)], [t_up + .3, C.pose("read", head=12, brow=.4)],
                             [t_up + 2.2, C.pose("read", head=10, brow=1)], [dur, C.pose("shrug", head=2)]])
    wife = C.actor("wife", "lady_1971", pos=[[0, 740, 1000]], scale=.92, seed=9, dir=-1, walk=False,
                   pose_keys=[[0, C.pose("seated", head=4)], [dur, C.pose("seated", head=8, mouth=1)]])
    layers = [lay(z, s, noblur=(k in ("glow", "lamp"))) for k, (z, s) in layers_.items() if k not in ("tv", "glow")]
    layers.append(lay(.72, wife["svg"]))
    layers.append(lay(.76, man["svg"]))
    layers.append(lay(.78, layers_["tv"][1]))
    cx = 960 + (600 - 960) / .76
    cam = [[0, cx + 200, 560, 1.25], [dur, cx, 500, 1.6, "sine"]]
    over = [badge("Our illustration", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[wife, man], cam=cam, focus=[[0, .76]], dof=6, shake=.3, over=over, grade="dusk", vig=1.2)
    import sfx
    foley = [("paper", t_up - .3, .35, -.2)]
    amb = sfx.room_tone(dur + .5, seed=23, clock=True, street=.05)
    return dict(shots=[shot], foley=foley, amb=amb * .6)


def shot_vault_window(w, h, dur, ctx):
    """An official walks to the counter with a bundle of dollars and sets it down; a clerk pushes a cart of bars to
    the other side of the counter (the gold window, a metaphor, shown as our illustration)."""
    layers_, anc = vault_1971()
    t_put = min(dur - 2.2, max(1.8, seg_t(ctx, 1, .35)))
    t_cart = min(dur - .6, t_put + 1.6)
    g = anc["ground"]
    held = f'<g {C.kv(opacity=[[0, 1], [t_put - .01, 1], [t_put, 0]])}>{dollar_bundle(120, 50)}</g>'
    official = C.actor("off", "suit_1971b", pos=[[0, 120, g], [t_put - .5, 760, g, "out"], [dur, 760, g]], scale=1.0, seed=12, dir=1, holdF=held, upright=True,
                       pose_keys=[[0, C.pose("relaxed", shF=40, elF=50)], [t_put - .5, C.pose("reach", shF=60, elF=30)], [t_put + .3, C.pose("relaxed", head=-4)],
                                  [dur, C.pose("relaxed", head=4, brow=.4)]])
    clerk = C.actor("clerk", "suit_1971d", pos=[[0, 1900, g], [t_put, 1900, g], [t_cart, 1420, g, "out"], [dur, 1420, g]], scale=1.0, seed=14, dir=-1,
                    pose_keys=[[0, C.pose("relaxed")], [t_put + .1, C.pose("reach", shF=70, elF=10)], [t_cart, C.pose("reach", shF=66, elF=14)], [dur, C.pose("relaxed", head=-6)]])
    bundle_on = f'<g {C.kv(opacity=[[0, 0], [t_put - .01, 0], [t_put, 1]])} transform="translate(840,856)">{dollar_bundle(120, 50)}</g>'
    cart = (f'<g {C.kv(translate=[[0, 1700, 0], [t_put, 1700, 0], [t_cart, 1220, 0, "out"], [dur, 1220, 0]])}>'
            + _r(-170, 900, 340, 24, "#6E7570", rx=4, sw=3) + bar_stack(-150, 898, [5, 4, 3], s=.6)
            + "".join(f'<circle cx="{cx_}" cy="944" r="20" fill="#2A2522" stroke="{INK}" stroke-width="3"/>' for cx_ in (-120, 120)) + "</g>")
    layers = [lay(z, s, noblur=(k == "lamps")) for k, (z, s) in layers_.items() if k != "counter"]
    layers.append(lay(.8, layers_["counter"][1] + bundle_on))
    layers.append(lay(.84, cart + "".join(a["svg"] for a in (official, clerk))))
    cam = [[0, 560, 700, 1.08], [t_put, 960, 690, 1.16, "inout"], [dur, 1080, 680, 1.22, "sine"]]
    over = [title("The gold window", "Our illustration", w, h, d=min(3.0, dur - .6)), badge("Reconstruction · not a real vault", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[official, clerk], cam=cam, focus=[[0, .84], [dur, .82]], dof=6, shake=.3, over=over, grade="cool", vig=1.15)
    import sfx
    steps = [t for t in C.footsteps(official, dur) if t < t_put] + [t for t in C.footsteps(clerk, dur) if t_put < t < t_cart]
    foley = [("step", t, .3, -.2) for t in steps] + [("paper", t_put, .4, 0), ("clank", t_cart, .5, .3, dict(pitch=150))]
    amb = sfx.room_tone(dur + .5, seed=31, clock=False, street=0) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_vault_count(w, h, dur, ctx):
    """Our example on the counter: $35,000,000 at $35 an ounce; bars stack up and the ounces count to 1,000,000."""
    t0 = max(.8, seg_t(ctx, 1, .1))
    t1 = min(dur - .8, max(t0 + 1.5, seg_t(ctx, 1, .95)))
    n = 15
    rows = [5, 4, 3, 2, 1]
    bars, k = "", 0
    for r, cnt in enumerate(rows):
        for j in range(cnt):
            at = t0 + (t1 - t0) * k / n
            bars += f'<g {C.kv(opacity=[[0, 0], [at - .01, 0], [at, 1]], translate=[[0, 0, -40], [at, 0, -40], [at + .25, 0, 0, "out"]])}>' + gold_bar(1010 + (j + r * .5) * 128, 840 - r * 38, 1.1) + "</g>"
            k += 1
    desk = (C.defs() + f'<rect x="-1000" y="-800" width="4000" height="2800" fill="#5E6663"/>'
            + C.shaft(700, -100, 300, 1000, angle=0, op=.2, color="255,236,190")
            + _r(-200, 850, 2400, 60, "#A9B0AB", sw=4) + _r(-200, 910, 2400, 400, "#8E9590", sw=3)
            + f'<g transform="translate(560,850)">{dollar_bundle(300, 110, label="$35,000,000", s=1.2)}</g>' + bars)
    board = (_r(560, 120, 800, 220, "#2E3532", rx=10, sw=4)
             + _t(960, 186, "OUNCES OF GOLD", 34, fill="#B9C2BC", weight=600, family="Sans", extra='letter-spacing="6"')
             + f'<text x="960" y="300" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="104" fill="#F6D58A" '
               f'{C.kv(count=[[0, 0], [t0, 0], [t1, 1000000]])} data-dec="0">0</text>')
    eq = kt(_r(500, 380, 920, 70, PAPER, rx=8, sw=3) + _t(960, 428, "$35,000,000 ÷ $35 an ounce = 1,000,000 oz", 34, fill=INK, family="Sans"), None, t1 - .2)
    layers = [lay(.6, desk), lay(.7, board + eq)]
    cam = [[0, 900, 560, 1.0], [dur, 960, 540, 1.1, "sine"]]
    over = [badge("Our example, not a real transaction", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[], cam=cam, focus=[[0, .65]], dof=4, shake=.25, over=over, grade="cool", tin=("dissolve", .35))
    import sfx
    foley = [("clank", t0 + (t1 - t0) * k / n + .2, .25, .2, dict(pitch=170 + 7 * k)) for k in range(n)] + [("hit", t1, .4, 0, dict(pitch=147))]
    amb = sfx.room_tone(dur + .5, seed=32, clock=False, street=0) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_vault_gap(w, h, dur, ctx):
    """1966, IMF figures, one honest scale (40 px a billion dollars): foreign official dollar holdings (over $14bn)
    rise as a column of bundles; the gold ($13.2bn) rises beside it; all but $3.2bn of it dims (needed at home);
    on 'a quarter', a quarter of the dollars is marked against the $3.2bn."""
    S = 40.0
    base = 820                     # 14 Nov: was 900, the axis labels sat under the captions
    ta = max(.6, seg_t(ctx, 0, .45))
    tb = max(ta + 1.0, seg_t(ctx, 0, .75))
    tc = max(tb + 1.0, seg_t(ctx, 1, .2))
    tq = max(tc + 1.0, word_t(ctx, 2, "quarter"))
    hx, gx = 620, 1220
    usd = (f'<g {C.kv(clip=[[0, 100, 0, 0, 0], [ta - .01, 100, 0, 0, 0], [ta + 1.4, 0, 0, 0, 0, "out"]])}>'
           + "".join(f'<g transform="translate({hx},{base - k * 28})">{dollar_bundle(260, 28)}</g>' for k in range(20)) + "</g>")
    usd_h = 14 * S
    usd = (f'<g {C.kv(clip=[[0, 100, 0, 0, 0], [ta - .01, 100, 0, 0, 0], [ta + 1.4, 0, 0, 0, 0, "out"]])}>'
           + _r(hx - 130, base - usd_h, 260, usd_h, "#9DBD95", sw=3)
           + "".join(f'<path d="M{hx - 130},{base - k * 20} L{hx + 130},{base - k * 20}" stroke="#7FA078" stroke-width="2"/>' for k in range(1, int(usd_h / 20)))
           + _r(hx - 18, base - usd_h, 36, usd_h, PAPER, sw=2) + "</g>")
    gold_h, avail_h = 13.2 * S, 3.2 * S
    gold = (f'<g {C.kv(clip=[[0, 100, 0, 0, 0], [tb - .01, 100, 0, 0, 0], [tb + 1.4, 0, 0, 0, 0, "out"]])}>'
            + _r(gx - 130, base - gold_h, 260, gold_h, GOLD, sw=3)
            + "".join(f'<path d="M{gx - 130},{base - k * 22} L{gx + 130},{base - k * 22}" stroke="{GOLD2}" stroke-width="2"/>' for k in range(1, int(gold_h / 22)))
            + "</g>")
    dim = (f'<g {C.kv(opacity=[[0, 0], [tc - .01, 0], [tc + .6, 1]])}>' + _r(gx - 130, base - gold_h, 260, gold_h - avail_h, "#2E3532", sw=3, extra='opacity=".72"')
           + _t(gx + 160, base - gold_h + 60, "NEEDED AT HOME", 26, fill="#F4ECDD", anchor="start", family="Sans", weight=700)
           + _t(gx + 160, base - avail_h / 2 + 12, "$3.2bn AVAILABLE", 30, fill="#F6D58A", anchor="start", family="Sans", weight=700)
           + _r(gx - 136, base - avail_h, 272, avail_h, "none", sw=6, extra=f'stroke="{TEAL}"') + "</g>")
    q_h = usd_h / 4
    quarter = (f'<g {C.kv(opacity=[[0, 0], [tq - .01, 0], [tq + .5, 1]])}>' + _r(hx - 136, base - q_h, 272, q_h, "none", sw=6, extra=f'stroke="{RED}"')
               + _t(hx - 160, base - q_h / 2 + 12, "A QUARTER: $3.5bn+", 30, fill="#F7C9B8", anchor="end", family="Sans", weight=700)
               + f'<path d="M{hx + 140},{base - q_h} L{gx - 140},{base - avail_h}" stroke="{RED}" stroke-width="5" stroke-dasharray="14 10"/></g>')
    labels = (kt(_t(hx, base - usd_h - 30, "$14bn+", 50, fill="#F4ECDD", family="Serif"), None, ta + 1.2)
              + kt(_t(gx, base - gold_h - 30, "$13.2bn", 50, fill="#F6D58A", family="Serif"), None, tb + 1.2)
              + _t(hx, base + 60, "DOLLARS HELD BY FOREIGN", 24, fill="#D9DED9", family="Sans", weight=600)
              + _t(hx, base + 92, "CENTRAL BANKS AND GOVERNMENTS", 24, fill="#D9DED9", family="Sans", weight=600)
              + _t(gx, base + 60, "US GOLD", 24, fill="#D9DED9", family="Sans", weight=600)
              + _t(330, 300, "1966", 72, fill="#F4ECDD", family="Serif"))
    layers_, anc = vault_1971()
    layers = [lay(z, s, noblur=(k == "lamps")) for k, (z, s) in layers_.items() if k in ("wall", "lamps", "floor")]
    layers.append(lay(.9, f'<rect x="-1000" y="-600" width="4000" height="2400" fill="#1E2422" opacity=".55"/>'
                      + _r(300, base, 1320, 8, "#D9DED9", sw=0) + usd + gold + dim + quarter + labels, noblur=True))
    cam = [[0, 960, 600, 1.0], [tq, 960, 560, 1.04, "sine"], [dur, 900, 560, 1.08, "sine"]]
    over = [badge("Data: IMF, for 1966 · one scale, $1bn = 40 px", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[], cam=cam, focus=[[0, .9]], dof=5, shake=.2, over=over, grade="cool", tin=("dissolve", .35))
    import sfx
    foley = [("paper", ta + .2, .3, -.3), ("clank", tb + .3, .4, .3, dict(pitch=160)), ("hit", tc + .1, .4, .3, dict(pitch=110)), ("hit", tq + .1, .45, -.3, dict(pitch=147))]
    amb = sfx.room_tone(dur + .5, seed=33, clock=False, street=0) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def _room_shot(head, sub, rows, dur, react_at, mood, ring, lifts, phones, cam, ttl, bdg, grade="warm", seed=5, tin=("cut", 0)):
    layers_, anc = dealing_room(head=head, sub=sub, rows=rows, ring=ring, lifts=lifts, seed=seed)
    tr = traders(anc, dur, react_at=react_at, mood=mood, phones=phones, seed=seed + 60)
    layers = [lay(z, s, noblur=(k == "light")) for k, (z, s) in layers_.items() if k != "desks"]
    layers.append(lay(.74, "".join(a["svg"] for a in tr)))
    layers.append(lay(.78, layers_["desks"][1]))
    fg = (_r(-700, 1010, 1000, 40, "#C9BBA0", rx=4, sw=3.4) + _r(-690, 1050, 980, 300, "#A8987C", sw=3) + desk_phone(140, 1010, color="#3B2F27")
          + _r(1720, 1030, 1000, 40, "#C9BBA0", rx=4, sw=3.4) + _r(1730, 1070, 980, 300, "#A8987C", sw=3) + typewriter(1880, 1030))
    layers.append(lay(1.18, fg))
    over = ([title(*ttl, w=1920, h=1080, d=min(3.0, dur - .6))] if ttl else []) + [badge(bdg, 1920, 1080)]
    return dict(dur=dur, layers=layers, actors=tr, cam=cam, focus=[[0, .74], [dur, .7]], dof=6, shake=.35, over=over, grade=grade, tin=tin), anc


def shot_london_1960(w, h, dur, ctx):
    """London, 20 October 1960: the market price counts from 35 to 40 dollars on the board as 'forty' is said."""
    t40 = min(dur - 1.0, max(1.5, word_t(ctx, 0, "forty")))
    rows = [("OFFICIAL PRICE", [[0, 35]], 2, "$", "", "#F4ECDD"), ("LONDON MARKET", [[0, 35], [t40 - .6, 35], [t40 + .3, 40]], 2, "$", "", "#F6D58A")]
    by = 540 + (330 - 540) / .38
    cam = [[0, 900, 620, 1.0], [t40 - .3, 960, 520, 1.16, "inout"], [dur, 980, 510, 1.2, "sine"]]
    shot, anc = _room_shot("GOLD", "US DOLLARS AN OUNCE", rows, dur, t40, "concern", ring=[(1, .6), (3, 1.4), (4, t40 + .4)], lifts=[], phones=(2,), cam=cam,
                           ttl=("London", "October 20, 1960"), bdg="Reconstruction · prices from Federal Reserve History", grade="warm", seed=5)
    import sfx
    foley = [("flap", t40 - .5, .45, 0), ("hit", t40 + .3, .4, 0, dict(pitch=196)), ("ring", .6, .15, -.5, dict(sec=.9)), ("ring", 1.4, .12, .6, dict(sec=.9))]
    amb = sfx.office_ambience(dur + .5, seed=41, busy=.8, phones=0) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_flood_1971(w, h, dur, ctx):
    """The week after 6 August 1971: phones ring, the board counts the dollars into central banks to $3.7bn."""
    t0 = max(1.0, word_t(ctx, 1, "three")) - .4
    t1 = min(dur - .6, t0 + 2.2)
    rows = [("DOLLARS INTO CENTRAL BANKS", [[0, 0], [t0, 0], [t1, 3.7]], 1, "$", "bn", "#F6D58A")]
    ring = [(k % 7, .3 + .55 * k) for k in range(int(dur / .55))]
    by = 540 + (330 - 540) / .38
    cam = [[0, 760, 600, 1.08], [t0, 960, 520, 1.16, "inout"], [dur, 990, 510, 1.22, "sine"]]
    shot, anc = _room_shot("THE WEEK AFTER AUGUST 6, 1971", "FEDERAL RESERVE BANK OF NEW YORK", rows, dur, t1, "concern", ring=ring, lifts=[], phones=(0, 2, 4), cam=cam,
                           ttl=("August 1971", "The flood"), bdg="Reconstruction · figure from the New York Fed", grade="cool", seed=9, tin=("dissolve", .35))
    import sfx
    foley = [("ring", t, .12, (-.6, .6)[k % 2], dict(sec=.5)) for k, (_, t) in enumerate(ring[::3])] + [("flap", t0, .4, 0), ("hit", t1, .45, 0, dict(pitch=147))]
    amb = sfx.office_ambience(dur + .5, seed=42, busy=1.6, phones=1.5) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_market_1972(w, h, dur, ctx):
    """Official 38 against the market's approximate 60 (mid 1972) and 90 (early 1973), each on its word."""
    t60 = min(dur - 2.0, max(1.2, word_t(ctx, 1, "sixty")))
    t90 = min(dur - .8, max(t60 + 1.2, word_t(ctx, 1, "ninety")))
    rows = [("OFFICIAL PRICE", [[0, 38]], 0, "$", "", "#F4ECDD"),
            ("MARKET, APPROX.", [[0, 38], [t60 - .5, 38], [t60 + .3, 60], [t90 - .5, 60], [t90 + .3, 90]], 0, "$", "", "#F6D58A")]
    by = 540 + (330 - 540) / .38
    cam = [[0, 1040, 600, 1.06], [t60 - .2, 960, 520, 1.16, "inout"], [dur, 940, 510, 1.22, "sine"]]
    shot, anc = _room_shot("GOLD", "US DOLLARS AN OUNCE, 1972 TO 1973", rows, dur, t60, "shrug", ring=[(2, t90 + .2)], lifts=[], phones=(), cam=cam,
                           ttl=None, bdg="Reconstruction · approximate market prices, Federal Reserve History", grade="warm", seed=13, tin=("dissolve", .35))
    import sfx
    foley = [("flap", t60 - .4, .4, 0), ("flap", t90 - .4, .4, 0), ("hit", t60 + .3, .35, 0, dict(pitch=196)), ("hit", t90 + .3, .4, 0, dict(pitch=147))]
    amb = sfx.office_ambience(dur + .5, seed=43, busy=1.0, phones=.5) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_camp_arrive(w, h, dur, ctx):
    """Camp David, Friday 13 August 1971: advisers walk in and sit at the long table. Nobody is a portrait."""
    layers_, anc = lodge_1971()
    n = 6
    seated = advisers(4, 250, 300, anc["seat_y"], dur)
    walk_in = []
    for j in range(2):
        tx = 250 + (4 + j) * 210 - 60
        t_sit = min(dur - 1.0, 1.6 + j * 1.4)
        walk_in.append(C.actor(f"w{j}", ("suit_1971c", "suit_1971d")[j], pos=[[0, 2200 + 200 * j, anc["seat_y"]], [t_sit, tx, anc["seat_y"], "out"], [dur, tx, anc["seat_y"]]],
                               scale=.9, seed=80 + j, dir=-1,
                               pose_keys=[[0, C.pose("relaxed")], [t_sit - .1, C.pose("relaxed")], [t_sit + .5, C.pose("seated", head=-4)], [dur, C.pose("seated", head=2)]]))
    layers = [lay(z, s, noblur=(k == "glow")) for k, (z, s) in layers_.items() if k not in ("table", "easel")]
    layers.append(lay(.8, layers_["easel"][1]))
    layers.append(lay(.78, "".join(a["svg"] for a in seated + walk_in)))
    layers.append(lay(.85, layers_["table"][1]))
    tx_, ty_ = 960 + (760 - 960) / .8, 540 + (780 - 540) / .8
    cam = [[0, tx_ + 500, ty_ - 20, 1.15], [dur, tx_ + 60, ty_, 1.2, "sine"]]
    over = [title("Camp David", "Friday, August 13, 1971", w, h, d=min(3.4, dur - .6)), badge("Reconstruction · not portraits", w, h)]
    shot = dict(dur=dur, layers=layers, actors=seated + walk_in, cam=cam, focus=[[0, .8]], dof=6, shake=.3, over=over, grade="warm", vig=1.15)
    import sfx
    steps = sorted(t for a in walk_in for t in C.footsteps(a, dur) if t < dur - 1)
    foley = [("step", t, .3, .3) for t in steps]
    amb = sfx.room_tone(dur + .5, seed=51, clock=False, street=0) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_camp_plan(w, h, dur, ctx):
    """A figure at the easel writes the three parts as the narration names them; the others turn to watch."""
    t_g = max(1.0, word_t(ctx, 0, "gold"))
    t_p = max(t_g + .9, word_t(ctx, 0, "prices"))
    t_i = max(t_p + .9, word_t(ctx, 0, "imports"))
    items = [(t_g - .2, "GOLD"), (t_p - .2, "PRICES, WAGES"), (t_i - .2, "IMPORTS")]
    layers_, anc = lodge_1971(easel_items=items)
    ex, ey = anc["easel"]
    pen = '<g><rect x="0" y="-5" width="60" height="10" rx="5" fill="#1E1A18" stroke="#0A0A0A" stroke-width="2"/></g>'
    writer = C.actor("writer", "suit_1971", pos=[[0, ex - 330, anc["stand_y"]]], scale=1.05, seed=90, dir=1, walk=False, holdF=pen,
                     pose_keys=sum(([[t - .3, C.pose("point", shF=96, elF=20, head=-6)], [t + .5, C.pose("point", shF=88, elF=24, head=-4)]] for t, _ in items),
                                   [[0, C.pose("relaxed", head=-4)]]) + [[dur, C.pose("relaxed", head=-10)]])
    keys = {i: [[0, C.pose("seated")], [t_g + .2 * i, C.pose("seated")], [t_g + .5 + .2 * i, C.pose("seated", head=-14 if i % 2 == 0 else 14, brow=.6)],
                [dur, C.pose("seated", head=-10 if i % 2 == 0 else 10)]] for i in range(5)}
    seated = advisers(5, 250, 230, anc["seat_y"], dur, keys=keys)
    layers = [lay(z, s, noblur=(k == "glow")) for k, (z, s) in layers_.items() if k not in ("table", "easel")]
    layers.append(lay(.78, "".join(a["svg"] for a in seated)))
    layers.append(lay(.8, layers_["easel"][1] + writer["svg"]))
    layers.append(lay(.85, layers_["table"][1]))
    kx, ky = 960 + (ex - 960) / .8, 540 + (ey - 540) / .8
    cam = [[0, kx - 520, ky + 60, 1.2], [t_g, kx - 200, ky, 1.4, "inout"], [dur, kx - 140, ky - 10, 1.5, "sine"]]
    over = [badge("Reconstruction · the plan's three parts", w, h)]
    shot = dict(dur=dur, layers=layers, actors=seated + [writer], cam=cam, focus=[[0, .8]], dof=6, shake=.3, over=over, grade="warm", vig=1.15,
                tin=("dissolve", .35))
    import sfx
    foley = [("quill", t, .4, .3, dict(sec=.8, rate=6.0)) for t, _ in items]
    amb = sfx.room_tone(dur + .5, seed=52, clock=False, street=0) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


SHOTS = dict(tv_hook=shot_tv_hook, speech=shot_speech, wallet=shot_wallet, vault_window=shot_vault_window, vault_count=shot_vault_count,
             vault_gap=shot_vault_gap, london_1960=shot_london_1960, flood_1971=shot_flood_1971, market_1972=shot_market_1972,
             camp_arrive=shot_camp_arrive, camp_plan=shot_camp_plan)


if __name__ == "__main__":
    # stills for a quick look: python3 build/cine_1971.py [name ...]
    names = sys.argv[1:] or list(SHOTS)
    work = C.OUT / "cine-1971-stills"
    work.mkdir(parents=True, exist_ok=True)
    demo = dict(segs=[("On a Sunday evening in August, at nine o'clock, television cut to the President, gold forty three point seven sixty.", .3, 4.0),
                      ("He said he would suspend temporarily the convertibility, three point seven, gold, prices and imports, sixty and ninety, a quarter.", 4.2, 9.0),
                      ("Second, a freeze.", 9.2, 11.0), ("Third, an extra tax.", 11.2, 13.0)])
    for nm in names:
        built = SHOTS[nm](1920, 1080, 13.5, demo)
        html, total = C.film_html(built["shots"], 1920, 1080)
        print(nm, [p.name for p in C.stills(html, [1.0, total * .45, total - .4], work, nm)])
