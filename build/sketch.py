"""
Hand-drawn illustrations for the YouTube engine (8 Nov, after Pietro: "the
visuals were much better in the other YouTube videos ... as much visuals as
possible"). The earlier videos drew a scene for every beat: a clock at 9:45,
a stack of 31 bricks, falling dominoes, stick figures with magnifying
glasses, a stock chart in red marker, a rubber stamp. This module draws those
scenes as animated SVG: strokes draw themselves on (marker on paper), fills
pop in, labels fade in, all timed to the voice.

Every scene draws in a 800 x 640 box. Call scene(name, t0, dur, **opts) to get
the SVG markup; youtube.py places it. All shapes are ours (no third-party art).

Scenes (opts in brackets):
  clock(time="9:45")              bricks(n=31, red=1, label="")
  dominoes(labels=[...], fall=1)  chart(values=[...], color, label, arrow)
  bars(values=[...], labels=[...], hi=None)
  figures(n=4, hi=None, glass=False, labels=None)
  document(title, lines=5, stamp="")      stamp(text)
  tower(crack=False, floors=8, label="")  bank(label="")
  seesaw(left="", right="", tip=1)        scale(left="", right="", tip=0)
  coins(stacks=[3,5,8], labels=None)      flow(steps=[...])
  calendar(day="14", month="SEP", note="")  phone(across=True, cut=False)
  magnifier(label="")   tulip(n=1, broken=False)   ship()   book(title)
  speech(text, who="")  quote(text, who="")   bulb(text="")
  globe()  arrows(up="", down="")   house(price="")   cake(slices, hi)
"""

import html as H
import math
import random

RED, TEAL, INK, PAPER, GREY = "#D93A12", "#0F766E", "#0A0A0A", "#F7F5F2", "#9A958E"
W, Hh = 800, 640


class Pen:
    """Collects animated SVG parts. Each stroke draws on, each fill pops."""

    def __init__(self, t0, dur, seed=1, ink=INK):
        self.t0, self.dur, self.parts, self.k, self.ink = t0, dur, [], 0, ink
        self.rng = random.Random(seed)

    def at(self, frac):
        return round(self.t0 + frac * self.dur, 3)

    def rough(self, pts, j=2.2, closed=False):
        """A slightly wobbly path through the points, like a marker line."""
        r = self.rng
        p = [(x + r.uniform(-j, j), y + r.uniform(-j, j)) for x, y in pts]
        if closed:
            p.append(p[0])
        d = f"M{p[0][0]:.1f} {p[0][1]:.1f}"
        for (x0, y0), (x1, y1) in zip(p, p[1:]):
            mx, my = (x0 + x1) / 2 + r.uniform(-j, j), (y0 + y1) / 2 + r.uniform(-j, j)
            d += f" Q{mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}"
        return d

    def line(self, pts, frac=0.0, d=0.5, color=None, w=6, closed=False, dash=None, j=2.2):
        path = self.rough(pts, j, closed)
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<g class="a" data-fx="draw" data-at="{self.at(frac)}" data-d="{d}">'
                          f'<path d="{path}" fill="none" stroke="{color or self.ink}" stroke-width="{w}" '
                          f'stroke-linecap="round" stroke-linejoin="round"{extra}/></g>')

    def circle(self, cx, cy, r, frac=0.0, d=0.5, color=None, w=6, n=28):
        pts = [(cx + r * math.cos(2 * math.pi * i / n - math.pi / 2), cy + r * math.sin(2 * math.pi * i / n - math.pi / 2))
               for i in range(n)]
        self.line(pts, frac, d, color, w, closed=True, j=1.2)

    def rect(self, x, y, w_, h_, frac=0.0, d=0.4, color=None, w=6):
        self.line([(x, y), (x + w_, y), (x + w_, y + h_), (x, y + h_)], frac, d, color, w, closed=True)

    def fill(self, shape, frac=0.0, d=0.35, fx="pop"):
        self.parts.append(f'<g class="a" data-fx="{fx}" data-at="{self.at(frac)}" data-d="{d}" '
                          f'style="transform-box:fill-box;transform-origin:center">{shape}</g>')

    def box(self, x, y, w_, h_, color, frac=0.0, rx=6, fx="pop"):
        self.fill(f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="{rx}" fill="{color}"/>', frac, fx=fx)

    def text(self, x, y, s, frac=0.0, size=34, color=None, anchor="middle", serif=False, weight=600, fx="fade"):
        fam = "'Serif',serif" if serif else "'Sans',sans-serif"
        self.parts.append(f'<g class="a" data-fx="{fx}" data-at="{self.at(frac)}" data-d="0.4">'
                          f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{weight}" '
                          f'font-size="{size}" fill="{color or self.ink}">{H.escape(str(s))}</text></g>')

    def svg(self):
        return (f'<svg viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" style="overflow:visible" aria-hidden="true">'
                + "".join(self.parts) + "</svg>")


# ---------------------------------------------------------------- scenes

def clock(p, time="9:45", **_):
    h, m = (int(x) for x in time.split(":"))
    cx, cy, r = 400, 320, 230
    p.circle(cx, cy, r, 0, .6, w=9)
    for i in range(12):
        a = 2 * math.pi * i / 12
        p.line([(cx + (r - 30) * math.sin(a), cy - (r - 30) * math.cos(a)), (cx + (r - 8) * math.sin(a), cy - (r - 8) * math.cos(a))],
               .15 + i * .015, .12, w=6)
    am = 2 * math.pi * m / 60
    ah = 2 * math.pi * ((h % 12) + m / 60) / 12
    p.line([(cx, cy), (cx + 120 * math.sin(ah), cy - 120 * math.cos(ah))], .4, .3, w=14)
    p.line([(cx, cy), (cx + 185 * math.sin(am), cy - 185 * math.cos(am))], .45, .3, color=RED, w=9)
    p.fill(f'<circle cx="{cx}" cy="{cy}" r="16" fill="{INK}"/>', .5)
    p.text(cx, cy + r + 70, time, .55, size=58, serif=True, weight=700, color=RED)


def bricks(p, n=31, red=1, label="", **_):
    cols = 4 if n > 16 else 2
    rows = math.ceil(n / cols)
    bw, bh = 120, min(36, 560 / rows - 4)
    x0 = 400 - cols * (bw + 8) / 2
    k = 0
    for r in range(rows):
        for c in range(cols):
            if k >= n:
                break
            y = 600 - (r + 1) * (bh + 4)
            color = RED if k < red else "#FFFFFF"
            p.fill(f'<rect x="{x0 + c * (bw + 8)}" y="{y}" width="{bw}" height="{bh}" rx="4" fill="{color}" stroke="{INK}" stroke-width="4"/>',
                   .05 + .6 * k / n, fx="pop")
            k += 1
    if label:
        p.text(400, 632, label, .75, size=30, color=RED)


def dominoes(p, labels=("", "", "", ""), fall=1, **_):
    n = len(labels)
    gap = 680 / n
    for i, lab in enumerate(labels):
        x = 80 + i * gap
        tilt = -55 if i < fall else 0
        p.fill(f'<g transform="rotate({tilt} {x + 30} 560)"><rect x="{x}" y="300" width="60" height="260" rx="8" fill="{RED if i == 0 else INK}"/>'
               f'<circle cx="{x + 30}" cy="370" r="9" fill="#fff"/><circle cx="{x + 30}" cy="470" r="9" fill="#fff"/></g>', .1 + .15 * i)
        if lab:
            p.text(x + 30, 610, lab, .2 + .15 * i, size=24)
    p.line([(40, 562), (760, 562)], 0, .4, w=5)


def chart(p, values=(5, 6, 5, 7, 4, 2, 1), color=RED, label="", arrow=True, **_):
    p.line([(70, 40), (70, 560), (760, 560)], 0, .35, w=6)
    lo, hi = min(values), max(values)
    pts = [(90 + i * 650 / (len(values) - 1), 520 - 440 * (v - lo) / max(hi - lo, 1e-9)) for i, v in enumerate(values)]
    p.line(pts, .2, .55, color=color, w=12, j=3)
    if arrow:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        a = math.atan2(y1 - y0, x1 - x0)
        tip = [(x1 - 34 * math.cos(a - .5), y1 - 34 * math.sin(a - .5)), (x1, y1), (x1 - 34 * math.cos(a + .5), y1 - 34 * math.sin(a + .5))]
        p.line(tip, .72, .15, color=color, w=12)
    if label:
        p.box(pts[-1][0] - 170, pts[-1][1] + (30 if pts[-1][1] < 300 else -110), 200, 70, color, .78)
        p.text(pts[-1][0] - 70, pts[-1][1] + (77 if pts[-1][1] < 300 else -63), label, .8, size=40, color="#fff", serif=True, weight=700)


def bars(p, values=(3, 5, 8), labels=None, hi=None, **_):
    n, top = len(values), max(values)
    bw = 520 / n
    p.line([(60, 560), (760, 560)], 0, .3, w=6)
    for i, v in enumerate(values):
        h = 440 * v / top
        x = 100 + i * (bw + 40)
        p.fill(f'<rect x="{x}" y="{560 - h}" width="{bw}" height="{h}" fill="{RED if i == hi else INK}"/>', .15 + .15 * i, fx="growY")
        if labels:
            p.text(x + bw / 2, 605, labels[i], .25 + .15 * i, size=26)


def figure(p, x, y, s=1.0, frac=0.0, color=None, glass=False):
    c = color or INK
    p.circle(x, y - 150 * s, 26 * s, frac, .2, color=c, w=6)
    p.line([(x, y - 124 * s), (x, y - 50 * s)], frac + .03, .15, color=c, w=7)
    p.line([(x - 40 * s, y - 100 * s), (x, y - 110 * s), (x + 40 * s, y - 95 * s)], frac + .05, .15, color=c, w=7)
    p.line([(x - 30 * s, y), (x, y - 50 * s), (x + 30 * s, y)], frac + .07, .15, color=c, w=7)
    if glass:
        p.circle(x + 62 * s, y - 108 * s, 20 * s, frac + .1, .15, color=RED, w=6)
        p.line([(x + 48 * s, y - 94 * s), (x + 38 * s, y - 84 * s)], frac + .12, .1, color=RED, w=6)


def figures(p, n=4, hi=None, glass=False, labels=None, **_):
    s = 1.3 if n <= 3 else 1.0 if n <= 6 else .7
    gap = 680 / n
    for i in range(n):
        x = 60 + gap * (i + .5)
        figure(p, x, 520, s, .05 + .08 * i, RED if i == hi else None, glass)
        if labels:
            p.text(x, 590, labels[i], .2 + .08 * i, size=26)
    p.line([(40, 524), (760, 524)], 0, .3, w=4, color=GREY)


def document(p, title="", lines=5, stamp="", **_):
    p.fill(f'<rect x="210" y="40" width="380" height="520" rx="10" fill="#fff" stroke="{INK}" stroke-width="6"/>', 0)
    if title:
        p.text(400, 120, title, .1, size=34, serif=True, weight=700)
    for i in range(lines):
        y = 190 + i * 55
        p.line([(250, y), (550 - 60 * (i % 3 == 2), y)], .15 + .07 * i, .15, color=GREY, w=8)
    if stamp:
        globals()["stamp"](p, stamp, cx=470, cy=430, frac=.6)


def stamp(p, text="", cx=400, cy=320, frac=.2, **_):
    w = max(220, 30 * len(text))
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{p.at(frac)}" data-d="0.35" data-rot="-10" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="{cx - w / 2}" y="{cy - 50}" width="{w}" height="100" rx="12" fill="none" stroke="{RED}" stroke-width="9"/>'
                   f'<text x="{cx}" y="{cy + 18}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="52" '
                   f'fill="{RED}">{H.escape(text)}</text></g>')


def tower(p, crack=False, floors=8, label="", **_):
    top = 560 - floors * 58
    p.rect(270, top, 260, 560 - top, 0, .5, w=7)
    for f in range(floors):
        for c in range(3):
            p.box(298 + c * 76, top + 16 + f * 58, 50, 30, RED if (f + c) % 5 == 0 else INK, .2 + .03 * f, rx=3)
    p.line([(200, 562), (600, 562)], 0, .3, w=6)
    if crack:
        p.line([(400, top), (380, top + 90), (420, top + 170), (385, top + 260), (410, 560)], .7, .3, color=RED, w=9, j=4)
    if label:
        p.text(400, top - 30, label, .5, size=36, serif=True, weight=700)


def bank(p, label="", **_):
    p.line([(180, 200), (400, 70), (620, 200)], 0, .35, w=8, closed=True)
    for i in range(5):
        x = 225 + i * 88
        p.rect(x, 230, 34, 260, .25 + .05 * i, .2, w=6)
    p.rect(170, 495, 460, 40, .5, .2, w=7)
    p.line([(140, 562), (660, 562)], .55, .2, w=7)
    if label:
        p.text(400, 172, label, .6, size=30, serif=True, weight=700)


def seesaw(p, left="", right="", tip=1, **_):
    a = -14 * tip
    p.fill(f'<path d="M370 560 L400 470 L430 560 Z" fill="{INK}"/>', 0)
    p.fill(f'<g transform="rotate({a} 400 465)"><rect x="110" y="455" width="580" height="18" rx="8" fill="{INK}"/>'
           f'<rect x="130" y="375" width="120" height="80" rx="8" fill="{RED}"/><rect x="560" y="400" width="90" height="55" rx="8" fill="{TEAL}"/>'
           f'<text x="190" y="430" text-anchor="middle" font-family="\'Sans\'" font-weight="700" font-size="28" fill="#fff">{H.escape(left)}</text>'
           f'<text x="605" y="438" text-anchor="middle" font-family="\'Sans\'" font-weight="700" font-size="24" fill="#fff">{H.escape(right)}</text></g>', .3)


def scale(p, left="", right="", tip=0, **_):
    p.line([(400, 120), (400, 540)], 0, .3, w=8)
    p.line([(300, 560), (500, 560)], .1, .2, w=8)
    dy = 30 * tip
    p.line([(160, 160 + dy), (640, 160 - dy)], .3, .3, w=8)
    for x, y, lab, c in ((160, 160 + dy, left, RED), (640, 160 - dy, right, TEAL)):
        p.line([(x, y), (x - 70, y + 160), (x + 70, y + 160), (x, y)], .45, .25, w=5)
        p.fill(f'<path d="M{x - 90} {y + 160} Q{x} {y + 220} {x + 90} {y + 160} Z" fill="{c}"/>', .55)
        p.text(x, y + 270, lab, .6, size=34, color=c, weight=700)


def coins(p, stacks=(3, 5, 8), labels=None, **_):
    n = len(stacks)
    for i, k in enumerate(stacks):
        x = 400 + (i - (n - 1) / 2) * 220
        for j in range(k):
            y = 540 - j * 34
            p.fill(f'<ellipse cx="{x}" cy="{y}" rx="80" ry="22" fill="#E8B04A" stroke="{INK}" stroke-width="5"/>', .1 + .3 * i / n + .02 * j)
        if labels:
            p.text(x, 610, labels[i], .5 + .1 * i, size=30, weight=700)


def flow(p, steps=("A", "B", "C"), **_):
    n = len(steps)
    h = 520 / n
    for i, s in enumerate(steps):
        y = 60 + i * h
        p.box(170, y, 460, h - 60, RED if i == n - 1 else INK, .1 + .25 * i)
        p.text(400, y + (h - 60) / 2 + 14, s, .15 + .25 * i, size=38, color="#fff", weight=600)
        if i < n - 1:
            p.line([(400, y + h - 55), (400, y + h - 8)], .2 + .25 * i, .12, w=7)
            p.line([(382, y + h - 26), (400, y + h - 6), (418, y + h - 26)], .25 + .25 * i, .08, w=7)


def calendar(p, day="14", month="SEP", note="", **_):
    p.fill(f'<rect x="230" y="90" width="340" height="400" rx="20" fill="#fff" stroke="{INK}" stroke-width="7"/>', 0)
    p.box(230, 90, 340, 110, RED, .1, rx=18)
    p.text(400, 168, month, .2, size=56, color="#fff", weight=700)
    p.text(400, 410, day, .3, size=190, serif=True, weight=700)
    for x in (300, 500):
        p.line([(x, 60), (x, 120)], .05, .15, w=10)
    if note:
        p.text(400, 570, note, .5, size=34, color=RED, weight=700)


def phone(p, across=True, cut=False, **_):
    for x in (130, 670):
        p.fill(f'<rect x="{x - 55}" y="200" width="110" height="200" rx="18" fill="{INK}"/><rect x="{x - 42}" y="222" width="84" height="140" rx="6" fill="#E5F0EE"/>', 0)
    p.line([(185, 300), (300, 200), (400, 300), (500, 200), (615, 300)], .2, .4, color=RED, w=7, dash="16 14")
    if cut:
        p.line([(360, 210), (440, 390)], .7, .1, w=8)
        p.line([(440, 210), (360, 390)], .72, .1, w=8)


def magnifier(p, label="", **_):
    p.circle(340, 260, 170, 0, .5, w=14)
    p.line([(462, 382), (640, 560)], .4, .25, w=26)
    if label:
        p.text(340, 278, label, .5, size=56, serif=True, weight=700, color=RED)


def tulip(p, n=1, broken=False, **_):
    for i in range(n):
        x = 400 + (i - (n - 1) / 2) * 200
        p.line([(x, 560), (x - 6, 420), (x, 300)], .05 + .1 * i, .3, color=TEAL, w=10)
        p.fill(f'<path d="M{x - 30} {390} Q{x - 110} {370} {x - 60} {460} Z" fill="{TEAL}"/>', .2 + .1 * i)
        p.fill(f'<path d="M{x - 70} 300 Q{x - 80} 190 {x - 40} 170 L{x - 20} 230 L{x} 160 L{x + 20} 230 L{x + 40} 170 Q{x + 80} 190 {x + 70} 300 Q{x} 350 {x - 70} 300 Z" '
               f'fill="{RED}"/>', .35 + .1 * i)
        if broken:
            for k in (-40, -10, 20, 48):
                p.line([(x + k, 200), (x + k + 6, 300)], .55 + .1 * i, .15, color="#fff", w=8)
    p.line([(150, 562), (650, 562)], 0, .3, w=6)


def ship(p, **_):
    p.line([(140, 430), (660, 430), (590, 530), (210, 530)], 0, .45, w=8, closed=True)
    p.line([(400, 430), (400, 110)], .3, .2, w=8)
    p.fill(f'<path d="M408 130 L600 400 L408 400 Z" fill="#fff" stroke="{INK}" stroke-width="6"/>', .45)
    p.fill(f'<path d="M392 160 L240 400 L392 400 Z" fill="{RED}"/>', .5)
    p.line([(60, 575), (160, 555), (260, 580), (360, 555), (460, 580), (560, 555), (660, 580), (760, 560)], .6, .3, color=TEAL, w=7)


def book(p, title="", **_):
    p.fill(f'<path d="M140 140 Q270 100 400 150 L400 540 Q270 490 140 530 Z" fill="#fff" stroke="{INK}" stroke-width="7"/>'
           f'<path d="M660 140 Q530 100 400 150 L400 540 Q530 490 660 530 Z" fill="#fff" stroke="{INK}" stroke-width="7"/>', 0)
    for i in range(5):
        p.line([(180, 220 + 55 * i), (360, 225 + 55 * i)], .2 + .05 * i, .1, color=GREY, w=7)
        p.line([(440, 225 + 55 * i), (620, 220 + 55 * i)], .25 + .05 * i, .1, color=GREY, w=7)
    if title:
        p.text(400, 610, title, .55, size=34, serif=True, weight=700, color=RED)


def speech(p, text="", who="", **_):
    p.fill(f'<path d="M110 80 H690 Q720 80 720 110 V360 Q720 390 690 390 H330 L250 470 L265 390 H110 Q80 390 80 360 V110 Q80 80 110 80 Z" '
           f'fill="#fff" stroke="{INK}" stroke-width="7"/>', 0)
    words, line, lines = text.split(), "", []
    for w_ in words:
        if len(line + " " + w_) > 22:
            lines.append(line)
            line = w_
        else:
            line = (line + " " + w_).strip()
    lines.append(line)
    for i, l in enumerate(lines[:4]):
        p.text(400, 170 + i * 62, l, .15 + .08 * i, size=46, serif=True, weight=700)
    figure(p, 250, 620, .8, .3)
    if who:
        p.text(330, 620, who, .5, size=28, anchor="start", color=RED, weight=700)


def quote(p, text="", who="", **_):
    p.text(120, 210, "“", 0, size=260, serif=True, weight=700, color=RED, anchor="start")
    speech_lines(p, text, 140, 300, .15)
    if who:
        p.text(140, 590, "— " + who if False else who, .6, size=32, anchor="start", color=GREY, weight=600)


def speech_lines(p, text, x, y, frac, size=48, width=24):
    words, line, lines = text.split(), "", []
    for w_ in words:
        if len(line + " " + w_) > width:
            lines.append(line)
            line = w_
        else:
            line = (line + " " + w_).strip()
    lines.append(line)
    for i, l in enumerate(lines[:5]):
        p.text(x, y + i * 62, l, frac + .08 * i, size=size, serif=True, weight=700, anchor="start")


def bulb(p, text="", **_):
    p.fill(f'<path d="M400 90 C290 90 230 170 230 250 C230 330 300 370 320 440 H480 C500 370 570 330 570 250 C570 170 510 90 400 90 Z" fill="#FFE07A" stroke="{INK}" stroke-width="7"/>', 0)
    for i, y in enumerate((470, 505, 540)):
        p.line([(330, y), (470, y)], .2 + .05 * i, .1, w=10)
    for a in range(-60, 61, 30):
        r = math.radians(a)
        p.line([(400 + 210 * math.sin(r), 250 - 210 * math.cos(r)), (400 + 260 * math.sin(r), 250 - 260 * math.cos(r))], .3, .15, color=RED, w=8)
    if text:
        p.text(400, 270, text, .45, size=52, serif=True, weight=700)


def globe(p, **_):
    p.circle(400, 320, 240, 0, .5, w=8)
    p.line([(160, 320), (640, 320)], .2, .2, w=5)
    for rx in (90, 180):
        pts = [(400 + rx * math.sin(2 * math.pi * i / 30), 320 - 240 * math.cos(2 * math.pi * i / 30)) for i in range(30)]
        p.line(pts, .3, .3, w=5, closed=True, j=1)
    p.fill('<circle cx="470" cy="250" r="16" fill="#D93A12"/>', .6)


def arrows(p, up="", down="", **_):
    p.fill(f'<path d="M230 520 V260 H160 L280 100 L400 260 H330 V520 Z" fill="{TEAL}"/>', .1)
    p.fill(f'<path d="M470 120 V380 H400 L520 540 L640 380 H570 V120 Z" fill="{RED}"/>', .35)
    if up:
        p.text(280, 590, up, .3, size=32, weight=700, color=TEAL)
    if down:
        p.text(520, 30 + 40, down, .5, size=32, weight=700, color=RED)


def house(p, price="", **_):
    p.line([(180, 300), (400, 120), (620, 300)], 0, .35, w=9)
    p.rect(220, 300, 360, 250, .2, .35, w=8)
    p.rect(360, 420, 80, 130, .4, .2, w=7)
    p.box(260, 340, 70, 60, TEAL, .5)
    p.box(470, 340, 70, 60, TEAL, .5)
    if price:
        p.box(470, 90, 260, 80, RED, .6)
        p.text(600, 145, price, .62, size=42, color="#fff", serif=True, weight=700)


def cake(p, slices=8, hi=1, **_):
    cx, cy, r = 400, 320, 240
    for i in range(slices):
        a0, a1 = 2 * math.pi * i / slices - math.pi / 2, 2 * math.pi * (i + 1) / slices - math.pi / 2
        off = 30 if i < hi else 0
        mx, my = off * math.cos((a0 + a1) / 2), off * math.sin((a0 + a1) / 2)
        p.fill(f'<path d="M{cx + mx} {cy + my} L{cx + mx + r * math.cos(a0):.1f} {cy + my + r * math.sin(a0):.1f} '
               f'A{r} {r} 0 0 1 {cx + mx + r * math.cos(a1):.1f} {cy + my + r * math.sin(a1):.1f} Z" '
               f'fill="{RED if i < hi else "#fff"}" stroke="{INK}" stroke-width="6"/>', .05 + .06 * i)


SCENES = {f.__name__: f for f in (clock, bricks, dominoes, chart, bars, figures, document, stamp, tower, bank, seesaw, scale,
                                  coins, flow, calendar, phone, magnifier, tulip, ship, book, speech, quote, bulb, globe,
                                  arrows, house, cake)}


def scene(name, t0, dur, seed=1, **opts):
    p = Pen(t0, dur, seed)
    SCENES[name](p, **opts)
    return p.svg()
