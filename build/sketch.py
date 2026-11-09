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
  9 Nov: wall(gap, label)  notes(left, right, lab_l, lab_r, n_left)  podium(words)
  queue(n, label)  factory(closed, label)  car(kicked)  fireworks()  rateboard(rate, sub)
  handshake(left, right)  suitcase(n)
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


# ---- 9 Nov scenes (Berlin Wall and the currency union)

def wall(p, gap=False, label="", **_):
    """A concrete wall of slabs with a rounded top; gap=True knocks the middle slabs out."""
    for i in range(8):
        x = 70 + i * 84
        if gap and i in (3, 4):
            p.fill(f'<rect x="{x + 10}" y="{470 + 18 * (i - 3)}" width="70" height="60" rx="6" fill="#C9C4BC" stroke="{INK}" stroke-width="5" '
                   f'transform="rotate({-18 + 36 * (i - 3)} {x + 45} {500})"/>', .55 + .05 * (i - 3))
            continue
        p.fill(f'<rect x="{x}" y="200" width="80" height="360" rx="4" fill="#E4E0D9" stroke="{INK}" stroke-width="5"/>'
               f'<rect x="{x - 4}" y="180" width="88" height="34" rx="17" fill="#D6D1C9" stroke="{INK}" stroke-width="5"/>', .05 + .05 * i)
    for i, (x, y) in enumerate(((120, 330), (300, 260), (560, 400), (650, 300))):
        p.line([(x, y), (x + 40, y - 20), (x + 70, y + 10)], .5 + .05 * i, .15, color=RED if i % 2 else TEAL, w=7)
    p.line([(40, 562), (760, 562)], 0, .3, w=6)
    if gap:
        figure(p, 400, 552, .9, .7, RED)
    if label:
        p.text(400, 130, label, .6, size=40, serif=True, weight=700, color=RED)


def banknote(p, x, y, label, value, color, frac, w=300, h=150):
    p.fill(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="{color}" stroke-width="7"/>'
           f'<rect x="{x + 14}" y="{y + 14}" width="{w - 28}" height="{h - 28}" rx="6" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="6 6"/>'
           f'<circle cx="{x + w - 70}" cy="{y + h / 2}" r="38" fill="none" stroke="{color}" stroke-width="5"/>', frac)
    p.text(x + 90, y + h / 2 + 26, value, frac + .05, size=74, serif=True, weight=700, color=color)
    p.text(x + w / 2, y + h + 46, label, frac + .1, size=30, weight=700, color=color)


def notes(p, left="1", right="1", lab_l="Ostmark", lab_r="D-Mark", n_left=1, **_):
    """Old notes on the left, new note on the right, an exchange arrow between."""
    for k in range(n_left):
        banknote(p, 30 + 16 * k, 150 + 22 * k, lab_l if k == n_left - 1 else "", left, GREY if k < n_left - 1 else INK, .05 + .1 * k)
    banknote(p, 470, 250, lab_r, right, TEAL, .45)
    p.line([(345, 300), (455, 300)], .35, .15, color=RED, w=9)
    p.line([(430, 280), (458, 300), (430, 320)], .4, .1, color=RED, w=9)


def podium(p, words="", **_):
    """A press conference: a lectern, a man reading a sheet, two microphones, flashes."""
    figure(p, 400, 360, 1.1, 0)
    p.fill(f'<rect x="320" y="334" width="160" height="28" rx="5" fill="#fff" stroke="{INK}" stroke-width="5" transform="rotate(-4 400 348)"/>', .2)
    p.fill(f'<path d="M260 360 H540 L510 560 H290 Z" fill="{INK}"/>', .1)
    p.line([(330, 290), (360, 345)], .15, .1, w=7)
    p.line([(470, 290), (440, 345)], .15, .1, w=7)
    p.box(345, 420, 110, 60, RED, .2, rx=6)
    for x in (360, 440):
        p.line([(x, 360), (x + (x - 400) * .4, 300)], .3, .15, w=6)
        p.fill(f'<circle cx="{x + (x - 400) * .4}" cy="296" r="12" fill="{INK}"/>', .35)
    for i, (x, y) in enumerate(((110, 120), (690, 160), (150, 420), (660, 440))):
        for a in range(0, 360, 60):
            r = math.radians(a)
            p.line([(x + 14 * math.cos(r), y + 14 * math.sin(r)), (x + 34 * math.cos(r), y + 34 * math.sin(r))], .45 + .08 * i, .08, color=RED, w=5)
    if words:
        p.box(170, 40, 460, 80, "#fff", .6)
        p.text(400, 96, words, .62, size=44, serif=True, weight=700, color=RED)
    p.line([(140, 562), (660, 562)], 0, .3, w=6)


def queue(p, n=7, label="", **_):
    """People lined up outside a bank door."""
    p.rect(600, 220, 160, 340, 0, .3, w=8)
    p.rect(640, 330, 80, 230, .15, .2, w=6)
    p.box(600, 180, 160, 40, RED, .2, rx=4)
    p.text(680, 210, label or "BANK", .25, size=26, color="#fff", weight=700)
    for i in range(n):
        x = 545 - i * 74
        figure(p, x, 555, .8, .25 + .06 * i, RED if i == 0 else None)
    p.line([(30, 562), (780, 562)], 0, .3, w=6)


def factory(p, closed=False, label="", **_):
    p.line([(90, 560), (90, 330), (230, 250), (230, 330), (370, 250), (370, 330), (510, 250), (510, 330), (650, 330), (650, 560)], 0, .5, w=8)
    p.rect(560, 120, 60, 210, .3, .2, w=8)
    for i, x in enumerate((140, 280, 420)):
        p.box(x, 400, 80, 70, INK if closed else TEAL, .4 + .04 * i, rx=4)
    if not closed:
        for i in range(3):
            p.circle(600 + 25 * i, 90 - 40 * i, 22 + 6 * i, .55 + .05 * i, .2, color=GREY, w=5)
    else:
        p.line([(150, 330), (620, 540)], .7, .12, color=RED, w=12)
        p.line([(620, 330), (150, 540)], .74, .12, color=RED, w=12)
    p.line([(40, 562), (760, 562)], 0, .3, w=6)
    if label:
        p.text(400, 612, label, .6, size=32, weight=700, color=RED if closed else INK)


def car(p, kicked=False, **_):
    """A small boxy 1960s-style two-door car (generic, no make)."""
    p.fill(f'<path d="M120 470 L150 380 Q170 340 230 330 L300 260 H520 L600 330 Q670 340 690 380 L700 470 Z" fill="#9DC7C1" stroke="{INK}" stroke-width="7"/>', 0)
    p.fill(f'<path d="M318 280 H405 V330 H270 Z" fill="#fff" stroke="{INK}" stroke-width="5"/><path d="M425 280 H505 L560 330 H425 Z" fill="#fff" stroke="{INK}" stroke-width="5"/>', .2)
    for x in (240, 580):
        p.fill(f'<circle cx="{x}" cy="480" r="52" fill="{INK}"/><circle cx="{x}" cy="480" r="20" fill="#E4E0D9"/>', .3)
    p.line([(40, 534), (760, 534)], 0, .3, w=6)
    if kicked:
        figure(p, 80, 530, .9, .5)
        for i, a in enumerate((-30, 0, 30)):
            r = math.radians(a)
            p.line([(150 + 30 * math.cos(r), 420 + 30 * math.sin(r)), (150 + 70 * math.cos(r), 420 + 70 * math.sin(r))], .7 + .03 * i, .08, color=RED, w=7)


def fireworks(p, **_):
    for i, (x, y, c) in enumerate(((220, 200, RED), (520, 150, TEAL), (400, 320, "#E8B04A"), (650, 330, RED))):
        p.line([(x, 600), (x + 10, y + 40)], .05 + .12 * i, .12, color=GREY, w=4, dash="10 10")
        for a in range(0, 360, 30):
            r = math.radians(a)
            p.line([(x + 18 * math.cos(r), y + 18 * math.sin(r)), (x + 90 * math.cos(r), y + 90 * math.sin(r))], .18 + .12 * i, .12, color=c, w=6)
    p.fill(f'<path d="M40 640 V560 H120 V520 H200 V580 H300 V500 H360 V560 H460 V530 H560 V590 H640 V540 H760 V640 Z" fill="{INK}"/>', 0)


def rateboard(p, rate="1 : 1", sub="", **_):
    """A bank's exchange-rate board with flip digits."""
    p.fill(f'<rect x="120" y="120" width="560" height="380" rx="20" fill="{INK}"/>', 0)
    p.fill(f'<rect x="150" y="150" width="500" height="70" rx="8" fill="#1E1E1E"/>', .1)
    p.text(400, 200, sub or "EXCHANGE RATE", .15, size=34, color="#E8B04A", weight=700)
    p.fill(f'<rect x="170" y="260" width="460" height="190" rx="10" fill="#1E1E1E"/><line x1="170" y1="355" x2="630" y2="355" stroke="{INK}" stroke-width="5"/>', .25)
    p.text(400, 400, rate, .35, size=140, serif=True, weight=700, color="#fff", fx="pop")
    for x in (220, 580):
        p.line([(x, 500), (x, 580)], .05, .2, w=8)
    p.line([(160, 582), (640, 582)], .1, .2, w=8)


def handshake(p, left="", right="", **_):
    """Two hands meeting over a signed treaty."""
    p.fill(f'<rect x="230" y="380" width="340" height="200" rx="8" fill="#fff" stroke="{INK}" stroke-width="6"/>', 0)
    for i in range(3):
        p.line([(260, 420 + 35 * i), (540, 420 + 35 * i)], .1 + .05 * i, .1, color=GREY, w=6)
    p.line([(290, 545), (330, 530), (360, 548), (400, 528)], .3, .15, color=INK, w=5)
    p.line([(440, 545), (470, 528), (500, 548), (530, 530)], .35, .15, color=INK, w=5)
    p.fill(f'<path d="M60 250 H300 L360 230 Q400 240 380 270 L330 300 H60 Z" fill="{RED}"/>', .45)
    p.fill(f'<path d="M740 250 H500 L430 228 Q370 230 390 262 L470 300 H740 Z" fill="{TEAL}"/>', .5)
    if left:
        p.text(160, 220, left, .6, size=30, weight=700, color=RED)
    if right:
        p.text(640, 220, right, .65, size=30, weight=700, color=TEAL)


def suitcase(p, n=3, **_):
    """People leaving with suitcases, walking to the right past a sign."""
    for i in range(n):
        x = 160 + i * 190
        figure(p, x, 540, .95, .05 + .1 * i, RED if i == n - 1 else None)
        p.fill(f'<rect x="{x + 30}" y="460" width="56" height="44" rx="6" fill="#E8B04A" stroke="{INK}" stroke-width="4"/>', .12 + .1 * i)
    p.line([(700, 560), (700, 330)], .4, .15, w=7)
    p.fill(f'<path d="M640 300 H750 L780 330 L750 360 H640 Z" fill="{TEAL}"/>', .45)
    p.text(700, 340, "WEST", .5, size=26, color="#fff", weight=700)
    p.line([(40, 562), (760, 562)], 0, .3, w=6)


SCENES = {f.__name__: f for f in (clock, bricks, dominoes, chart, bars, figures, document, stamp, tower, bank, seesaw, scale,
                                  coins, flow, calendar, phone, magnifier, tulip, ship, book, speech, quote, bulb, globe,
                                  arrows, house, cake, wall, notes, podium, queue, factory, car, fireworks, rateboard,
                                  handshake, suitcase)}


def scene(name, t0, dur, seed=1, **opts):
    p = Pen(t0, dur, seed)
    SCENES[name](p, **opts)
    return p.svg()
