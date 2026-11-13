"""
Reusable sets and props for cine.py (13 Nov 2026). Everything is drawn here as SVG in the brand's
illustration style (ink outlines, flat fills, cream, red, teal, mustard); nothing is traced or sampled.

Sets return depth layers for a shot (cine.layer) and the anchor points a director needs (where the ground
is, where a door or a window is). Props return SVG at the origin, to place with a transform or to put in a
figure's hand (cine.actor(holdF=...)).

  Sets       street_1720(...)   a London street of 1720: sky, St Paul's on the skyline, rooftops with smoke,
                                 brick and stone fronts with sash windows, hanging signs that swing, a
                                 cobbled street, a lamp and barrels in the foreground
             study_1720(...)    a panelled study: window with a light shaft and dust, shelves, desk, candle
             parchment(...)     a full-frame sheet for charts and documents (chapter cards, data reveals)
  People     crowd(...)         independent walkers and talkers on a street, seeded
  Props      newspaper(title, lines)  letter(lines)  quill()  coin(r)  coin_stack(n)  jar(label)
             certificate(title)  candle()  cup()  ledger_book()
             phone(), card(), terminal()       modern objects for present-day stories
  Charts     price_line(points, ...)  a line chart whose stroke draws on and whose counter rides the tip,
                                       with labelled flags; data in, nothing invented
"""

import json
import math
import random

import cine as C
from cine import INK, RED, TEAL, PAPER, MUSTARD, kv, layer, motes, shaft

SW = 3.2


def _r(x, y, w, h, fill, rx=0, sw=SW, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" {extra}/>'


def _t(x, y, text, size, fill=INK, anchor="middle", weight=700, family="Serif", extra=""):
    fam = "'Serif',serif" if family == "Serif" else "'Sans',sans-serif"
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="{weight}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{text}</text>')


# ------------------------------------------------------------------------------------------------ props

def newspaper(title="COURSE OF THE EXCHANGE", sub="LONDON, JUNE 1720", rows=(("South Sea", "890"), ("Bank", None), ("East India", None)),
              w=230, h=300, hi=0):
    """A folded broadsheet held up or read. rows: (name, price) lines in the price list; hi highlights one.
    13 Nov: a price of None is drawn as an illegible pen mark, so a prop never shows an unsourced number (only the
    South Sea price of early June 1720, about 890, is sourced for the proof of concept)."""
    x0, y0 = -w / 2, -h
    s = _r(x0, y0, w, h, "#F4ECDD", rx=3)
    s += f'<path d="M{x0 + 6},{y0 + 6} L{x0 + w - 6},{y0 + 6}" stroke="{INK}" stroke-width="1.4"/>'
    s += _t(0, y0 + 30, title, 15, extra='letter-spacing="1"')
    s += f'<path d="M{x0 + 10},{y0 + 40} L{x0 + w - 10},{y0 + 40}" stroke="{INK}" stroke-width="2"/>'
    s += _t(0, y0 + 56, sub, 10, weight=600, family="Sans", extra='letter-spacing="1.5"')
    for i, (name, price) in enumerate(rows):
        y = y0 + 88 + i * 30
        if i == hi:
            s += f'<rect x="{x0 + 8}" y="{y - 18}" width="{w - 16}" height="26" fill="{MUSTARD}" opacity=".55"/>'
        s += _t(x0 + 14, y, name, 15, anchor="start", weight=600, family="Sans")
        if price is None:
            s += f'<path d="M{x0 + w - 62},{y - 6} q8,-6 16,0 t16,0 t16,0" fill="none" stroke="#6F655A" stroke-width="2.4" stroke-linecap="round"/>'
        else:
            s += _t(x0 + w - 14, y, price, 17, anchor="end")
    for i in range(6):
        y = y0 + 190 + i * 16
        s += f'<path d="M{x0 + 14},{y} L{x0 + w - 14 - (i % 3) * 22},{y}" stroke="#9A8F7E" stroke-width="3" stroke-linecap="round"/>'
    s += f'<path d="M0,{y0 + 4} L0,{y0 + h - 4}" stroke="#CFC4B0" stroke-width="1.5"/>'
    return s


def letter(lines=("Sell the bonds.", "Buy South Sea."), w=330, h=230, reveal=None):
    """A sheet on a desk with handwriting. reveal: [(t0, t1), ...] per line: the ink appears left to right."""
    s = _r(-w / 2, -h / 2, w, h, "#F6EFE0", rx=3) + f'<rect x="{-w / 2 + 3}" y="{-h / 2 + 3}" width="{w - 6}" height="{h - 6}" fill="url(#paperlines)" opacity=".5"/>'
    for i, line in enumerate(lines):
        y = -h / 2 + 70 + i * 52
        clip = ""
        if reveal:
            a, b = reveal[i]
            clip = kv(clip=[[0, 0, 100, 0, 0], [a, 0, 100, 0, 0], [b, 0, 0, 0, 0, "lin"]])
        s += (f'<g {clip}><text x="{-w / 2 + 26}" y="{y}" font-family="\'Serif\',serif" font-style="italic" font-weight="400" '
              f'font-size="34" fill="#2A2018">{line}</text></g>')
    return s


def quill(len_=150):
    return (f'<g><path d="M0,0 C20,-40 60,-110 {len_ * .55},-{len_}" fill="none" stroke="{INK}" stroke-width="2.6"/>'
            f'<path d="M14,-30 C30,-70 70,-130 {len_ * .55},-{len_} C{len_ * .3},-{len_ * .8} 30,-60 14,-30 Z" fill="#F7F5F2" stroke="{INK}" stroke-width="2.4"/>'
            f'<path d="M24,-52 C40,-80 60,-112 {len_ * .5},-{len_ * .92}" fill="none" stroke="#CFC6B6" stroke-width="1.6"/></g>')


def coin(r=16, fill=MUSTARD, mark="£"):
    return (f'<g><ellipse cx="0" cy="0" rx="{r}" ry="{r * .42}" fill="{fill}" stroke="{INK}" stroke-width="2.4"/>'
            f'<ellipse cx="0" cy="-3" rx="{r}" ry="{r * .42}" fill="#F7D978" stroke="{INK}" stroke-width="2.4"/></g>')


def coin_stack(n, r=18):
    return "".join(f'<g transform="translate(0,{-i * 7})">{coin(r)}</g>' for i in range(n))


def jar(label="BONDS", w=150, h=170, color=TEAL):
    return (f'<g>{_r(-w / 2, -h, w, h, "rgba(255,255,255,.35)", rx=18)}'
            f'<rect x="{-w / 2 + 8}" y="{-h - 16}" width="{w - 16}" height="20" rx="6" fill="{color}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<rect x="{-w / 2 + 16}" y="{-h * .58}" width="{w - 32}" height="40" rx="4" fill="#F4ECDD" stroke="{INK}" stroke-width="2"/>'
            + _t(0, -h * .58 + 28, label, 19, weight=600, family="Sans", extra='letter-spacing="1"') + "</g>")


def certificate(title="SOUTH SEA STOCK", w=260, h=180):
    return (_r(-w / 2, -h / 2, w, h, "#F3E7CF", rx=4) + _r(-w / 2 + 10, -h / 2 + 10, w - 20, h - 20, "none", rx=3, sw=1.6)
            + _t(0, -h / 2 + 46, title, 20) + _t(0, -h / 2 + 76, "ONE SHARE", 12, weight=600, family="Sans")
            + f'<circle cx="{w / 2 - 44}" cy="{h / 2 - 40}" r="20" fill="{RED}" stroke="{INK}" stroke-width="2.4"/>')


def candle(lit=True):
    s = (f'<ellipse cx="0" cy="0" rx="34" ry="9" fill="#B08A4E" stroke="{INK}" stroke-width="{SW}"/>'
         + _r(-12, -70, 24, 70, "#F4ECDD", rx=4)
         + f'<path d="M0,-70 L0,-80" stroke="{INK}" stroke-width="2"/>')
    if lit:
        s += (f'<circle cx="0" cy="-92" r="120" fill="url(#candle)" data-flick=\'[0.85,0.12,4]\'/>'
              f'<path d="M0,-80 C-9,-92 -5,-104 0,-114 C5,-104 9,-92 0,-80 Z" fill="#FFC14D" stroke="{INK}" stroke-width="2" data-flick=\'[0.95,0.06,9]\'/>')
    return s


def cup():
    steam = "".join(f'<path d="M{-6 + 6 * i},-30 C{-14 + 6 * i},-44 {2 + 6 * i},-52 {-6 + 6 * i},-66" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>' for i in range(3))
    return (f'<g data-steam="1">{steam}</g>' + _r(-18, -30, 36, 30, "#F7F5F2", rx=6)
            + f'<path d="M18,-24 C30,-24 30,-8 18,-8" fill="none" stroke="{INK}" stroke-width="{SW}"/>'
            + f'<ellipse cx="0" cy="0" rx="30" ry="6" fill="#E6DCCB" stroke="{INK}" stroke-width="2.4"/>')


def ledger_book(w=200, h=40, color="#6B2E1E"):
    return _r(-w / 2, -h, w, h, color, rx=4) + f'<path d="M{-w / 2 + 8},{-h + 8} L{w / 2 - 8},{-h + 8}" stroke="{MUSTARD}" stroke-width="2"/>'


def phone(w=120, h=230, screen=TEAL):
    return (_r(-w / 2, -h / 2, w, h, INK, rx=20) + f'<rect x="{-w / 2 + 8}" y="{-h / 2 + 14}" width="{w - 16}" height="{h - 28}" rx="10" fill="{screen}"/>')


def card(w=200, h=126, color=RED):
    return (_r(-w / 2, -h / 2, w, h, color, rx=14) + f'<rect x="{-w / 2 + 22}" y="{-h / 2 + 34}" width="34" height="26" rx="5" fill="{MUSTARD}" stroke="{INK}" stroke-width="2"/>'
            + f'<path d="M{-w / 2 + 22},{h / 2 - 28} L{w / 2 - 60},{h / 2 - 28}" stroke="#F7F5F2" stroke-width="5" stroke-linecap="round"/>')


def terminal(w=170, h=250):
    return (_r(-w / 2, -h / 2, w, h, "#2A2A2A", rx=18) + f'<rect x="{-w / 2 + 16}" y="{-h / 2 + 18}" width="{w - 32}" height="90" rx="8" fill="#BFE3D6"/>'
            + "".join(f'<rect x="{-w / 2 + 22 + (k % 3) * 44}" y="{-h / 2 + 128 + (k // 3) * 32}" width="34" height="22" rx="5" fill="#555"/>' for k in range(9)))


# ------------------------------------------------------------------------------------------------ charts

def price_line(points, x0, y0, w, h, vmax, upto=None, color=RED, draw=(0, 2), flags=(), counter=None, months=None,
               label_size=22, stroke=7, dashed_after=None, ticks=None, xspan=None, money="£"):
    """A line chart drawn in a box (x0, y0 top-left, w x h). points: [(label, value), ...]. draw=(t0, t1): the
    line draws on over those shot seconds. flags: [(index, text, colour, t)] pins on points. counter: (t0, t1)
    shows a number riding the tip. Returns SVG."""
    n = len(points)
    # a point may carry its own x (months, years): (label, value, x); ticks then label the axis, so a month
    # with no sourced price keeps its place and gets no invented point
    if xspan:
        xs = [x0 + w * (p[2] - xspan[0]) / (xspan[1] - xspan[0]) for p in points]
    else:
        xs = [x0 + w * i / (n - 1) for i in range(n)]
    ys = [y0 + h - h * p[1] / vmax for p in points]
    last = n - 1 if upto is None else upto
    solid = " ".join(("M" if i == 0 else "L") + f"{xs[i]:.1f},{ys[i]:.1f}" for i in range(last + 1))
    s = f'<path d="M{x0},{y0 + h} L{x0 + w},{y0 + h}" stroke="{INK}" stroke-width="3"/>'
    for frac in (.25, .5, .75, 1):
        yy = y0 + h - h * frac
        s += f'<path d="M{x0},{yy:.1f} L{x0 + w},{yy:.1f}" stroke="{INK}" stroke-width="1.2" opacity=".18"/>'
        s += _t(x0 - 14, yy + 7, f"{money}{int(vmax * frac):,}", label_size - 4, anchor="end", weight=600, family="Sans", extra='opacity=".6"')
    if ticks and xspan:
        for tx, lab in ticks:
            px = x0 + w * (tx - xspan[0]) / (xspan[1] - xspan[0])
            s += f'<path d="M{px:.1f},{y0 + h} L{px:.1f},{y0 + h + 10}" stroke="{INK}" stroke-width="2"/>'
            s += _t(px, y0 + h + 40, lab, label_size, weight=600, family="Sans", extra='opacity=".7"')
    else:
        for i, p in enumerate(points):
            s += _t(xs[i], y0 + h + 34, p[0], label_size, weight=600, family="Sans", extra='opacity=".7"')
    a, b = draw
    s += (f'<path d="{solid}" fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round" '
          f'{kv(dash=[[0, 0], [a, 0], [b, 1, "inout"]])}/>')
    if dashed_after is not None and last < n - 1:
        rest = " ".join(("M" if i == last else "L") + f"{xs[i]:.1f},{ys[i]:.1f}" for i in range(last, n))
        ta, tb = dashed_after
        s += (f'<path d="{rest}" fill="none" stroke="{color}" stroke-width="{stroke - 2}" stroke-dasharray="4 14" stroke-linecap="round" '
              f'{kv(opacity=[[0, 0], [ta, 0], [tb, .8]])}/>')
    for idx, text, col, t in flags:
        fx, fy = xs[idx], ys[idx]
        s += (f'<g {kv(opacity=[[0, 0], [t, 0], [t + .3, 1]], translate=[[0, 0, -30], [t, 0, -30], [t + .45, 0, 0, "out"]])}>'
              f'<circle cx="{fx}" cy="{fy}" r="13" fill="{col}" stroke="{INK}" stroke-width="3"/>'
              f'<path d="M{fx},{fy - 14} L{fx},{fy - 76}" stroke="{INK}" stroke-width="3"/>'
              f'<rect x="{fx - 6}" y="{fy - 120}" width="{len(text) * 15 + 30}" height="44" rx="8" fill="{col}" stroke="{INK}" stroke-width="3"/>'
              + _t(fx + 9, fy - 90, text, 22, fill="#fff", anchor="start", weight=600, family="Sans", extra='letter-spacing="1"') + "</g>")
    if counter:
        ta, tb = counter
        keys = []
        # ride along the line: position and value keyed per point over the draw time
        for i in range(last + 1):
            ti = a + (b - a) * (i / max(last, 1))
            keys.append((ti, xs[i], ys[i], points[i][1]))
        tr = [[0, xs[0], ys[0] - 40]] + [[k[0], k[1], k[2] - 40, "lin"] for k in keys]
        cnt = [[0, points[0][1]]] + [[k[0], k[3], "lin"] for k in keys]
        s += (f'<g {kv(translate=tr, opacity=[[0, 0], [ta, 0], [ta + .3, 1], [tb - .3, 1], [tb, 0]])}>'
              f'<rect x="-62" y="-40" width="124" height="52" rx="10" fill="{INK}"/>'
              f'<text x="0" y="-3" font-family="\'Serif\',serif" font-weight="700" font-size="34" fill="#fff" text-anchor="middle" '
              f'data-pre="{money}" {kv(count=cnt)}>{money}{points[0][1]}</text></g>')
    return s


# ------------------------------------------------------------------------------------------------ sets

def _window(x, y, w, h, lit=False, seed=0, glazing=(3, 4)):
    s = _r(x - 8, y - 8, w + 16, h + 16, "#EFE6D3", sw=2.6)
    glass = "#F6D58A" if lit else "#3D4A52"
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{glass}" stroke="{INK}" stroke-width="2.6"/>'
    if lit:
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFF1C2" data-flick=\'[0.35,0.08,{seed}]\'/>'
    else:
        s += f'<path d="M{x + 4},{y + h - 6} L{x + w * .6},{y + 6}" stroke="#7E8C94" stroke-width="5" opacity=".5"/>'
    cx, cy = glazing
    for i in range(1, cx):
        s += f'<path d="M{x + w * i / cx},{y} L{x + w * i / cx},{y + h}" stroke="#EFE6D3" stroke-width="3.4"/>'
    for j in range(1, cy):
        s += f'<path d="M{x},{y + h * j / cy} L{x + w},{y + h * j / cy}" stroke="#EFE6D3" stroke-width="3.4"/>'
    s += f'<rect x="{x - 12}" y="{y + h + 8}" width="{w + 24}" height="10" fill="#E3D7BF" stroke="{INK}" stroke-width="2"/>'
    return s


def _front(x, w, top, base, color, floors=3, cols=3, lit=(), door=None, seed=0, brick=True):
    s = _r(x, top, w, base - top, color, sw=3.4)
    if brick:
        rng = random.Random(seed)
        for k in range(int((base - top) * w / 2600)):
            bx, by = x + rng.uniform(10, w - 40), top + rng.uniform(20, base - top - 20)
            s += f'<rect x="{bx:.0f}" y="{by:.0f}" width="26" height="9" fill="#000" opacity=".07"/>'
    s += _r(x - 10, top - 18, w + 20, 22, "#E8DCC4", sw=2.6) + _r(x - 4, top - 30, w + 8, 14, "#D8CAB0", sw=2.2)
    fh = (base - top - 150) / floors
    ww, wh = w / cols * .46, fh * .62
    k = 0
    for f in range(floors):
        for c in range(cols):
            if door and f == floors - 1 and c == door[0]:
                continue
            wx = x + w / cols * (c + .5) - ww / 2
            wy = top + 40 + f * fh
            s += _window(wx, wy, ww, wh, lit=(k in lit), seed=seed * 10 + k)
            k += 1
    if door:
        c = door[0]
        dx = x + w / cols * (c + .5) - 46
        s += _r(dx - 10, base - 210, 112, 210, "#E8DCC4", sw=2.6)
        s += _r(dx, base - 196, 92, 196, door[1] if len(door) > 1 else "#3B2A20", sw=3)
        s += f'<path d="M{dx},{base - 196} A46,40 0 0 1 {dx + 92},{base - 196}" fill="#F6D58A" stroke="{INK}" stroke-width="3"/>'
        s += f'<circle cx="{dx + 74}" cy="{base - 96}" r="5" fill="{MUSTARD}" stroke="{INK}" stroke-width="2"/>'
    return s


def _sign(x, y, lines, w=230, h=118, color=TEAL, seed=0):
    """A painted board hanging from an iron bracket; it swings a little."""
    s = f'<path d="M{x},{y} L{x + w * .62},{y} M{x + 12},{y} L{x + 36},{y + 34}" stroke="{INK}" stroke-width="5" fill="none"/>'
    hx = x + w * .6
    board = (f'<path d="M{hx - w / 2 + 30},{y} L{hx - w / 2 + 30},{y + 22} M{hx + w / 2 - 30},{y} L{hx + w / 2 - 30},{y + 22}" stroke="{INK}" stroke-width="2.6"/>'
             + _r(hx - w / 2, y + 22, w, h, color, rx=8, sw=3.4) + _r(hx - w / 2 + 8, y + 30, w - 16, h - 16, "none", rx=5, sw=1.6))
    for i, line in enumerate(lines):
        size = 30 if i == 0 else 17
        board += _t(hx, y + 22 + (h / 2) + (-6 if len(lines) > 1 else 10) + i * 34 - (6 if i == 0 and len(lines) > 1 else 0),
                    line, size, fill="#F7F5F2", weight=700 if i == 0 else 600, family="Serif" if i == 0 else "Sans",
                    extra='letter-spacing="1"')
    return s + f'<g data-swing=\'[2.2,1.3,{seed},{hx},{y}]\'>{board}</g>'


def street_1720(w=4400, x0=-1200, sign_a=("JONATHAN'S", "COFFEE HOUSE"), sign_b=("GARRAWAY'S", "COFFEE HOUSE"), seed=4,
                sign_xa=560, sign_xb=1500, alley_x=180, board_x=1000):
    """Layers for a London street of 1720 (Exchange Alley is the default dressing). Returns (layers, anchors).
    anchors: ground lines and key x positions per depth, for placing actors and aiming the camera."""
    rng = random.Random(seed)
    sky = C.defs() + f'<rect x="{x0 - 2000}" y="-1200" width="{w + 6000}" height="2600" fill="url(#skyWarm)"/>'
    sky += f'<circle cx="1500" cy="250" r="420" fill="url(#glowWarm)" opacity=".8"/>'
    for i in range(6):
        cx, cy = rng.uniform(x0, x0 + w), rng.uniform(60, 330)
        sky += (f'<g data-drift=\'[{rng.uniform(4, 9):.1f},0,0]\'><ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rng.uniform(160, 300):.0f}" ry="{rng.uniform(26, 46):.0f}" '
                f'fill="#FFF8E8" opacity=".55"/></g>')
    # far skyline with St Paul's (completed 1710) and church spires
    far = ""
    base = 700
    xs = x0
    while xs < x0 + w:
        bw = rng.uniform(90, 220)
        bh = rng.uniform(70, 170)
        far += f'<rect x="{xs:.0f}" y="{base - bh:.0f}" width="{bw:.0f}" height="{bh + 300:.0f}" fill="#CDB997"/>'
        xs += bw
    dome_x = 1250
    far += (f'<rect x="{dome_x - 170}" y="{base - 220}" width="340" height="230" fill="#BFA982"/>'
            f'<rect x="{dome_x - 110}" y="{base - 300}" width="220" height="90" fill="#BFA982"/>'
            f'<path d="M{dome_x - 120},{base - 300} C{dome_x - 120},{base - 470} {dome_x + 120},{base - 470} {dome_x + 120},{base - 300} Z" fill="#B49D76"/>'
            f'<rect x="{dome_x - 18}" y="{base - 520}" width="36" height="70" fill="#B49D76"/>'
            f'<path d="M{dome_x - 10},{base - 520} L{dome_x},{base - 566} L{dome_x + 10},{base - 520} Z" fill="#B49D76"/>')
    for sx in (dome_x - 700, dome_x + 620, dome_x + 1500, dome_x - 1500):
        far += (f'<rect x="{sx - 26}" y="{base - 300}" width="52" height="300" fill="#C3AE89"/>'
                f'<path d="M{sx - 26},{base - 300} L{sx},{base - 440} L{sx + 26},{base - 300} Z" fill="#C3AE89"/>')
    # mid rooftops with chimneys and smoke
    mid = ""
    xs = x0 - 200
    while xs < x0 + w + 200:
        bw = rng.uniform(160, 300)
        top = rng.uniform(330, 430)
        mid += f'<path d="M{xs:.0f},{top + 60:.0f} L{xs + bw * .5:.0f},{top:.0f} L{xs + bw:.0f},{top + 60:.0f} L{xs + bw:.0f},1200 L{xs:.0f},1200 Z" fill="#A98E6C" stroke="#8C7356" stroke-width="2"/>'
        if rng.random() < .7:
            cx = xs + bw * rng.uniform(.2, .7)
            mid += f'<rect x="{cx:.0f}" y="{top - 30:.0f}" width="34" height="70" fill="#8F7357" stroke="#6E5841" stroke-width="2"/>'
            if rng.random() < .6:
                mid += (f'<g data-drift=\'[14,-9,0]\'>'
                        + "".join(f'<circle cx="{cx + 17 + 12 * k:.0f}" cy="{top - 44 - 22 * k:.0f}" r="{14 + 6 * k}" fill="#E8DECB" opacity="{.45 - .1 * k:.2f}"/>' for k in range(3))
                        + "</g>")
        xs += bw
    # street fronts (z .55): base at y 900
    fronts = ""
    xs = x0 + 150
    palette = ["#A9583C", "#CDB48F", "#8E4B35", "#D8C3A0", "#B9694A", "#C2A07A", "#97553D"]
    anchors = dict(signs={}, doors=[])
    k = 0
    while xs < x0 + w - 300:
        bw = rng.choice([520, 560, 600, 640])
        top = rng.choice([300, 330, 360, 390])
        col = palette[k % len(palette)]
        lit = set(rng.sample(range(9), 3))
        door = (rng.choice([0, 1, 2]), rng.choice(["#3B2A20", TEAL, "#6B2E1E", INK]))
        fronts += _front(xs, bw, top, 900, col, floors=3, cols=3, lit=lit, door=door, seed=k, brick=col not in ("#CDB48F", "#D8C3A0", "#C2A07A"))
        anchors["doors"].append(xs + bw / 3 * (door[0] + .5))
        xs += bw + rng.choice([0, 0, 40])
        k += 1
    # dressing at fixed places near the action: two coffee-house signs, the alley's name, a notice board
    fronts += _sign(sign_xa - 140, 560, sign_a, color=TEAL, seed=1)
    fronts += _sign(sign_xb - 140, 545, sign_b, color=RED, seed=2.4)
    anchors["signs"] = dict(a=sign_xa, b=sign_xb)
    fronts += (_r(alley_x - 75, 650, 150, 48, "#F4ECDD", rx=4, sw=2.4)
               + _t(alley_x, 682, "EXCHANGE ALLEY", 15, weight=600, family="Sans", extra='letter-spacing="1"'))
    fronts += _r(board_x - 85, 700, 170, 130, "#6B4A32", rx=4)
    for j in range(4):
        bx, by = board_x - 73 + (j % 2) * 78, 712 + (j // 2) * 58
        fronts += _r(bx, by, 68, 50, "#F4ECDD", sw=1.8) + _t(bx + 34, by + 20, "NEW", 11, weight=600, family="Sans") \
            + _t(bx + 34, by + 36, "SUBSCRIPTION", 7.5, weight=600, family="Sans")
    # late-afternoon light: the sun is low on the right; the lower storeys sit in shade, a band of sun crosses
    fronts += (f'<path d="M{x0 - 400},560 L{x0 + w + 400},300 L{x0 + w + 400},900 L{x0 - 400},900 Z" fill="#3A2416" opacity=".16"/>'
               f'<rect x="{x0 - 400}" y="840" width="{w + 800}" height="60" fill="#2A1A10" opacity=".14"/>')
    fronts += f'<rect x="{x0 - 400}" y="880" width="{w + 800}" height="40" fill="#C9B79B" stroke="{INK}" stroke-width="3"/>'
    # the street itself (z .8): pavement edge, cobbles, gutter
    street = (f'<rect x="{x0 - 800}" y="900" width="{w + 1600}" height="420" fill="url(#cobble)"/>'
              f'<rect x="{x0 - 800}" y="900" width="{w + 1600}" height="420" fill="#3A2A1C" opacity=".08"/>'
              f'<rect x="{x0 - 800}" y="898" width="{w + 1600}" height="22" fill="#B7A385" stroke="{INK}" stroke-width="3"/>'
              f'<path d="M{x0 - 800},1150 L{x0 + w + 800},1150" stroke="#5E4B3A" stroke-width="6" opacity=".35"/>'
              f'<path d="M{x0 - 800},1000 L{x0 + w + 800},940 L{x0 + w + 800},1060 L{x0 - 800},1120 Z" fill="#FFE2A6" opacity=".22"/>')
    layers = dict(sky=(0.03, sky), far=(0.14, far), mid=(0.3, mid), fronts=(0.55, fronts), street=(0.8, street))
    anchors.update(ground_back=930, ground_main=1010, ground_front=1120)
    return layers, anchors


def foreground_1720(x0=-1200, w=4400, seed=9):
    """Near objects (z ~1.3), to be blurred by depth of field: lamp posts, barrels, a cart wheel."""
    rng = random.Random(seed)
    s = ""
    for lx in (x0 + 900, x0 + 2500, x0 + 3900):
        s += (f'<rect x="{lx - 9}" y="380" width="18" height="900" fill="#1E1A18"/>'
              f'<path d="M{lx - 46},380 L{lx + 46},380 L{lx + 30},300 L{lx - 30},300 Z" fill="#2A2522" stroke="{INK}" stroke-width="3"/>'
              f'<rect x="{lx - 26}" y="304" width="52" height="72" fill="#F6D58A" stroke="{INK}" stroke-width="3" data-flick=\'[0.9,0.08,{lx % 9}]\'/>'
              f'<circle cx="{lx}" cy="340" r="150" fill="url(#candle)" opacity=".55"/>')
    for bx in (x0 + 1700, x0 + 3200):
        s += (f'<path d="M{bx - 70},1240 C{bx - 84},1150 {bx - 84},1080 {bx - 70},1000 L{bx + 70},1000 C{bx + 84},1080 {bx + 84},1150 {bx + 70},1240 Z" fill="#8A5A36" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M{bx - 80},1040 L{bx + 80},1040 M{bx - 82},1190 L{bx + 82},1190" stroke="#3A2A1C" stroke-width="10"/>')
    return s


def crowd(n, x_range, ground, scale, z_seed=1, looks=None, speed=(55, 95), dirs=(1, -1), dur=8.0, talkers=0, prefix="c"):
    """n independent people on a street line. Walkers cross at their own pace and direction; talkers stand
    in pairs and gesture. Returns (svg, specs, actors)."""
    rng = random.Random(z_seed)
    looks = looks or ["gent_teal", "gent_ink", "gent_mus", "gent_brown", "trader_cap", "lady_blue", "gent_ink", "gent_brown",
                      "trader_cap", "gent_teal", "gent_red", "lady_red"]
    actors = []
    for i in range(n):
        look = looks[(i * 5 + z_seed) % len(looks)]
        d = rng.choice(dirs)
        x = x_range[0] + (x_range[1] - x_range[0]) * (i + rng.uniform(.15, .85)) / n
        v = rng.uniform(*speed) * d
        y = ground + rng.uniform(-8, 8)
        a = C.actor(f"{prefix}{i}", look, pos=[[0, x, y], [dur, x + v * dur, y, "lin"]], scale=scale * rng.uniform(.94, 1.04),
                    seed=z_seed * 10 + i, dir=d, amp=rng.uniform(20, 26))
        a["spec"]["ph"] = rng.uniform(0, 6.28)
        actors.append(a)
    for j in range(talkers):
        x = x_range[0] + (x_range[1] - x_range[0]) * (j + .5) / max(talkers, 1) + rng.uniform(-60, 60)
        y = ground + rng.uniform(-4, 4)
        for side, (dx, dr) in enumerate(((0, 1), (165 * scale, -1))):
            look = looks[(j * 3 + side * 7 + z_seed) % len(looks)]
            keys, t, flip = [], 0.0, side
            while t < dur + 1:
                keys.append([t, C.pose("talk_a" if (flip % 2 == 0) else "talk_b")])
                t += rng.uniform(.5, 1.1)
                flip += 1
            actors.append(C.actor(f"{prefix}t{j}{side}", look, pos=[[0, x + dx, y]], pose_keys=keys, scale=scale, seed=z_seed * 7 + j * 2 + side,
                                  dir=dr, walk=False))
    return "".join(a["svg"] for a in actors), actors


def study_1720():
    """A panelled study: back wall with shelves and a tall window (light shaft, dust), a desk, a candle.
    Returns (layers, anchors). The desk top is at y 860 on the z .85 layer; the chair seat at y 900."""
    wall = C.defs() + f'<rect x="-1400" y="-800" width="4800" height="2400" fill="#8A6446"/>'
    for i in range(-6, 14):                                   # panelling
        x = i * 260
        wall += _r(x + 20, 120, 220, 380, "#94704F", rx=4, sw=2.4) + _r(x + 20, 540, 220, 380, "#94704F", rx=4, sw=2.4)
    wall += f'<rect x="-1400" y="500" width="4800" height="22" fill="#6E4B32" stroke="{INK}" stroke-width="3"/>'
    # window, left
    wall += (_r(-240, 40, 460, 700, "#E9DCC2", sw=4) + f'<rect x="-210" y="70" width="400" height="640" fill="#F8EBCB"/>'
             + "".join(f'<path d="M{-210 + 400 * k / 3},70 L{-210 + 400 * k / 3},710" stroke="#E9DCC2" stroke-width="10"/>' for k in (1, 2))
             + "".join(f'<path d="M-210,{70 + 640 * k / 4} L190,{70 + 640 * k / 4}" stroke="#E9DCC2" stroke-width="10"/>' for k in (1, 2, 3))
             + f'<path d="M-260,30 C-160,120 -120,500 -200,760 L-260,760 Z" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
             + f'<path d="M240,30 C140,120 120,500 200,760 L260,760 Z" fill="{RED}" stroke="{INK}" stroke-width="3"/>')
    # shelves, right
    shelves = ""
    rng = random.Random(3)
    for row in range(4):
        y = 150 + row * 170
        shelves += _r(980, y + 140, 720, 18, "#5E3D27", sw=2.6)
        x = 1000
        while x < 1680:
            bw = rng.uniform(22, 44)
            bh = rng.uniform(100, 136)
            col = rng.choice(["#6B2E1E", "#2E4A5A", "#7A5A2A", "#3B3B3B", "#8A3A24", "#3F5B45", MUSTARD])
            tilt = rng.choice([0, 0, 0, 6]) if x > 1600 else 0
            shelves += f'<rect x="{x:.0f}" y="{y + 140 - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{col}" stroke="{INK}" stroke-width="2.2" transform="rotate({tilt},{x:.0f},{y + 140:.0f})"/>'
            shelves += f'<rect x="{x + 4:.0f}" y="{y + 160 - bh:.0f}" width="{bw - 8:.0f}" height="6" fill="{MUSTARD}" opacity=".7"/>'
            x += bw + rng.uniform(1, 4)
    shelves = _r(960, 120, 760, 720, "#6E4B32", rx=4, sw=3.4) + shelves
    wall += shelves
    # a plain framed print between window and shelves (no copied artwork: a ship drawn in a few lines)
    wall += (_r(470, 180, 300, 220, "#C9A27A", sw=3.4) + _r(490, 200, 260, 180, "#EFE3CC", sw=2)
             + f'<path d="M540,330 L700,330 L680,350 L560,350 Z M620,330 L620,240 M620,240 L670,320 M620,250 L580,320" fill="none" stroke="{INK}" stroke-width="3"/>')
    floor = f'<rect x="-1400" y="900" width="4800" height="700" fill="url(#boards)"/><rect x="-1400" y="900" width="4800" height="700" fill="#000" opacity=".12"/>'
    light = (shaft(-170, 120, 330, 1400, angle=-32, op=.32) + motes(-120, 160, 900, 760, n=46, op=.8, spd=8, seed=5))
    desk = (_r(380, 860, 980, 40, "#6B4A32", rx=6, sw=3.6) + _r(400, 900, 940, 180, "#5A3D29", rx=4, sw=3.4)
            + _r(430, 930, 260, 60, "#6B4A32", rx=4, sw=2.4) + _r(1050, 930, 260, 60, "#6B4A32", rx=4, sw=2.4)
            + f'<circle cx="560" cy="960" r="6" fill="{MUSTARD}" stroke="{INK}" stroke-width="2"/><circle cx="1180" cy="960" r="6" fill="{MUSTARD}" stroke="{INK}" stroke-width="2"/>')
    chair = (_r(150, 900, 150, 20, "#4E3322", rx=6, sw=3) + _r(156, 720, 24, 190, "#4E3322", rx=8, sw=3)
             + _r(160, 918, 16, 170, "#4E3322", sw=2.6) + _r(276, 918, 16, 170, "#4E3322", sw=2.6))
    layers = dict(wall=(0.35, wall), light=(0.5, light), floor=(0.6, floor), chair=(0.72, chair), desk=(0.85, desk))
    return layers, dict(desk_y=860, seat_y=900, seat_x=230, ground=1060)


def parchment(w=2400, h=1400, x0=-240, y0=-160):
    s = C.defs() + f'<rect x="{x0 - 400}" y="{y0 - 400}" width="{w + 800}" height="{h + 800}" fill="#2A2018"/>'
    s += (f'<path d="M{x0},{y0 + 30} Q{x0 + w / 2},{y0 - 10} {x0 + w},{y0 + 30} L{x0 + w - 20},{y0 + h - 30} Q{x0 + w / 2},{y0 + h + 10} {x0 + 20},{y0 + h - 30} Z" '
          f'fill="#F3E7CF" stroke="{INK}" stroke-width="4"/>')
    rng = random.Random(2)
    for _ in range(40):
        s += f'<circle cx="{rng.uniform(x0, x0 + w):.0f}" cy="{rng.uniform(y0, y0 + h):.0f}" r="{rng.uniform(20, 90):.0f}" fill="#C9A87A" opacity=".06"/>'
    return s


# ------------------------------------------------------------------------------------------------ 13 Nov: today
# The first present-day set (cinematic-standard.md section 8, step 3: "a bank office"). Generic: no bank, logo,
# real skyline or real firm. Built for the IB Reels' filmed hooks (scene-library K: a figure faces the question).

def office_today(seed=6, dusk=True):
    """An analyst's desk in a city office at dusk: a tall window with an invented skyline whose windows flicker on,
    a shelf of binders, a plant, a desk lamp with a warm pool of light, a chair. Returns (layers, anchors) like
    study_1720: the desk top is at y 860 on the z .85 layer, the chair seat at y 900, the monitor centre at
    (780, 640) on the z .85 layer (monitor_dcf(cx=780, cy=640, w=440, h=270))."""
    rng = random.Random(seed)
    sky_top, sky_bot = ("#2E3550", "#D98A5A") if dusk else ("#BFD3DE", "#EEF2F2")
    wall = C.defs() + (f'<defs><linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky_top}"/>'
                       f'<stop offset=".75" stop-color="{sky_bot}"/></linearGradient></defs>')
    wall += f'<rect x="-1400" y="-800" width="4800" height="2400" fill="#D8CFC2"/>'
    # the window: two tall panes, an invented skyline, lit windows that come on one by one (flicker)
    wx, wy, ww, wh = -160, 60, 1060, 760
    sky = f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="url(#dusk)"/>'
    x = wx - 20
    while x < wx + ww:
        bw, bh = rng.uniform(70, 150), rng.uniform(180, 520)
        col = rng.choice(["#283048", "#323A55", "#3B4360", "#2B2F44"])
        sky += f'<rect x="{x:.0f}" y="{wy + wh - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{col}"/>'
        for r in range(int(bh // 34)):
            for c in range(int(bw // 26)):
                if rng.random() < .33:
                    op = rng.uniform(.5, .95)
                    sky += (f'<rect x="{x + 8 + c * 26:.0f}" y="{wy + wh - bh + 12 + r * 34:.0f}" width="12" height="16" fill="{MUSTARD}" '
                            f'opacity="{op:.2f}" data-flick=\'[{op:.2f},0.06,{rng.randint(0, 9)}]\'/>')
        x += bw + rng.uniform(4, 18)
    wall += (sky + f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#4A4F5C" stroke-width="22"/>'
             + f'<path d="M{wx + ww / 2},{wy} L{wx + ww / 2},{wy + wh}" stroke="#4A4F5C" stroke-width="14"/>'
             + f'<rect x="{wx - 30}" y="{wy + wh}" width="{ww + 60}" height="26" fill="#BDB3A5" stroke="{INK}" stroke-width="3"/>')
    # shelves with binders, right
    sh = _r(1180, 160, 560, 640, "#B9AC9A", rx=4, sw=3.2)
    for row in range(3):
        y = 200 + row * 200
        sh += _r(1196, y + 160, 528, 16, "#8F8270", sw=2.4)
        bx = 1212
        while bx < 1690:
            bw_ = rng.uniform(30, 52)
            col = rng.choice([TEAL, "#2E4A5A", "#E8E1D4", RED, "#3B3B3B", "#E8E1D4"])
            sh += (f'<rect x="{bx:.0f}" y="{y + 20:.0f}" width="{bw_:.0f}" height="140" rx="3" fill="{col}" stroke="{INK}" stroke-width="2.2"/>'
                   f'<rect x="{bx + bw_ / 2 - 7:.0f}" y="{y + 40:.0f}" width="14" height="40" rx="2" fill="#F7F5F2" opacity=".8"/>')
            bx += bw_ + rng.uniform(2, 6)
    wall += sh
    # a plant in the corner, its leaves sway
    plant = (f'<g transform="translate(1040,860)">' + _r(-56, -120, 112, 120, "#C4704A", rx=10)
             + "".join(f'<g data-swing=\'[{1.4 + k * .3:.1f},{2.0 + k * .2:.1f},{k},0,-110]\'><path d="M0,-110 C{-80 + k * 40},{-220 - k * 20} {-40 + k * 30},{-300} {-10 + k * 25},{-330 + k * 10} '
                       f'C{20 + k * 10},{-260} {10},{-180} 0,-110 Z" fill="{TEAL if k % 2 else "#3F7A5A"}" stroke="{INK}" stroke-width="3"/></g>' for k in range(4))
             + "</g>")
    floor = f'<rect x="-1400" y="900" width="4800" height="700" fill="#8E8579"/><rect x="-1400" y="900" width="4800" height="700" fill="#000" opacity=".1"/>'
    chair = (_r(150, 900, 160, 22, "#2B2F3A", rx=8, sw=3) + _r(156, 700, 30, 210, "#2B2F3A", rx=12, sw=3)
             + _r(222, 922, 16, 120, "#5A5F6A", sw=2.4) + f'<path d="M170,1050 L290,1050" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    lamp_glow = f'<ellipse cx="1260" cy="860" rx="360" ry="120" fill="url(#glowWarm)" opacity=".55"/>'
    desk = (lamp_glow + _r(380, 860, 1000, 36, "#E8E1D4", rx=6, sw=3.6) + _r(420, 896, 24, 180, "#5A5F6A", sw=2.6)
            + _r(1316, 896, 24, 180, "#5A5F6A", sw=2.6)
            # the lamp
            + f'<path d="M1250,860 L1250,840 M1250,840 L1210,700 L1300,620" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
            + f'<path d="M1262,598 L1350,640 L1320,690 L1240,650 Z" fill="{RED}" stroke="{INK}" stroke-width="3.2"/>'
            + _r(1215, 846, 70, 16, INK, rx=6, sw=0)
            # keyboard and a notepad
            + _r(470, 838, 250, 22, "#3B3F48", rx=6, sw=2.6) + f'<g transform="translate(1040,848) rotate(-4)">{_r(-70, -10, 140, 14, "#F7F5F2", rx=2, sw=2)}</g>'
            + f'<g transform="translate(1150,860)">{cup()}</g>')
    layers = dict(wall=(0.35, wall), floor=(0.6, floor), plant=(0.62, plant), chair=(0.72, chair), desk=(0.85, desk))
    return layers, dict(desk_y=860, seat_y=900, seat_x=230, ground=1060, monitor=(780, 640))


def monitor_dcf(t_on=.2, t_tv=1.6, bars=5, cx=900, cy=600, w=560, h=340, tv_label="TERMINAL VALUE"):
    """A monitor on the desk showing a DCF timeline: five small cash flows rise one by one, then one tall block
    for every year after the forecast rises past them (the idea the Reel asks about). Shot seconds. The screen
    glows onto the desk."""
    x0, y0 = cx - w / 2, cy - h / 2
    s = (f'<ellipse cx="{cx}" cy="{cy + 40}" rx="{w * .75:.0f}" ry="{h * .7:.0f}" fill="#BFE3D6" opacity=".14"/>'
         + _r(cx - 18, y0 + h, 36, 860 - (y0 + h), "#3B3F48", sw=2.6) + _r(cx - 90, 846, 180, 16, "#3B3F48", rx=6, sw=2.6)
         + _r(x0 - 16, y0 - 16, w + 32, h + 32, "#1E2128", rx=14, sw=3.6)
         + f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#F4EFE6"/>')
    base = y0 + h - 46
    s += f'<path d="M{x0 + 24},{base} L{x0 + w - 24},{base}" stroke="{INK}" stroke-width="4"/>'
    s += _t(x0 + 26, y0 + 34, "DCF", 22, INK, anchor="start", weight=600, family="Sans", extra='letter-spacing="3"')
    step = (w - 60) * .58 / bars                      # the forecast takes about 58% of the width, the block the rest
    bw = step * .72
    for k in range(bars):
        bx, bh = x0 + 30 + k * step, (h - 110) * (.24 + .03 * k)
        t = t_on + .14 * k
        s += (f'<g {kv(clip=[[0, 100, 0, 0, 0], [t, 100, 0, 0, 0], [t + .3, 0, 0, 0, 0, "out"]])}>'
              f'<rect x="{bx:.1f}" y="{base - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="5" fill="{TEAL}" stroke="{INK}" stroke-width="2.6"/></g>'
              + f'<g {kv(opacity=[[0, 0], [t, 0], [t + .3, 1]])}>' + _t(round(bx + bw / 2, 1), base + 26, f"Y{k + 1}", 17, INK, weight=600, family="Sans") + "</g>")
    tx = x0 + 30 + bars * step + 14
    tw, th = x0 + w - 24 - tx, h - 100
    s += (f'<g {kv(clip=[[0, 100, 0, 0, 0], [t_tv, 100, 0, 0, 0], [t_tv + .7, 0, 0, 0, 0, "out"]])}>'
          f'<rect x="{tx:.1f}" y="{base - th}" width="{tw:.1f}" height="{th}" rx="8" fill="{MUSTARD}" stroke="{INK}" stroke-width="3"/>'
          + _t(round(tx + tw / 2, 1), base - th / 2 - 8, "\u221e", 56, INK)
          + "".join(_t(round(tx + tw / 2, 1), base - th / 2 + 30 + 20 * i, part, 15, INK, weight=700, family="Sans")
                    for i, part in enumerate(tv_label.split())) + "</g>"
          + f'<g {kv(opacity=[[0, 0], [t_tv + .5, 0], [t_tv + .8, 1]])}>' + _t(round(tx + tw / 2, 1), base + 26, "YEAR 5 ON", 15, RED, weight=700, family="Sans") + "</g>")
    return s
