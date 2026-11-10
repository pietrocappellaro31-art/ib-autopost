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
  10 Nov (coins, in colour): coin(...) helper, pricetag(value, tag), receipt(total, circle),
  card_tap(amount), lineup(first, others), last_coin(stamp)
  10 Nov, later (buy now, pay later): bag_later(tag), split4(total, parts), pay_dots(labels), credit_report(line),
  interest_stack(base, rate)
  10 Nov, long video (the dot-com crash): bubble(label, pop), ticker(price, change, up), server(lights),
  parcel(label, n), ballot(), payback(years, paid, label), petbowl(closed), bell(label), rocket(fall)
  youtube.py now fits every drawing to its box (the drawn part fills its half of the frame).
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
        return (f'<svg class="sk" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" style="overflow:visible" aria-hidden="true">'
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


# ---- 10 Nov scenes: coins and money in colour (Pietro: "pictures and colors and more animated")
# Generic coins of our own design: a value and a rim, no portraits or national designs.

METALS = {"copper": ("#F6C19A", "#C9703F", "#7E3B1B"), "nickel": ("#F4F6F8", "#B9C1C7", "#69737B"),
          "gold": ("#FBE7A1", "#E0A93B", "#8A5F12")}


_COIN_N = 0


def coin(p, cx, cy, r, value="1\u00a2", metal="copper", frac=0.0, flip=0, fx="pop", d=.35):
    """A shaded coin with a rim, its value in the middle and a shine. flip=N spins it N turns as it lands."""
    c0, c1, c2 = METALS[metal]
    global _COIN_N
    _COIN_N += 1
    g = f"coin{_COIN_N}"                                   # unique across every drawing on the page
    shape = (f'<defs><radialGradient id="{g}" cx="38%" cy="32%" r="78%"><stop offset="0" stop-color="{c0}"/>'
             f'<stop offset=".58" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient></defs>'
             f'<circle cx="{cx}" cy="{cy + r * .07}" r="{r}" fill="{c2}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{g})" stroke="{c2}" stroke-width="{max(r * .05, 3):.1f}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r * .83:.1f}" fill="none" stroke="{c0}" stroke-opacity=".75" stroke-width="{max(r * .03, 2):.1f}" '
             f'stroke-dasharray="{r * .06:.1f} {r * .05:.1f}"/>'
             f'<text x="{cx}" y="{cy + r * .25:.1f}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
             f'font-size="{r * .74:.1f}" fill="{c2}">{H.escape(value)}</text>'
             f'<ellipse cx="{cx - r * .38:.1f}" cy="{cy - r * .42:.1f}" rx="{r * .32:.1f}" ry="{r * .14:.1f}" fill="#fff" fill-opacity=".45" '
             f'transform="rotate(-35 {cx - r * .38:.1f} {cy - r * .42:.1f})"/>')
    if flip:
        shape = (f'<g class="a" data-fx="coinflip" data-at="{p.at(frac)}" data-d="{1.1 + .25 * flip}" data-turns="{flip}" '
                 f'style="transform-box:fill-box;transform-origin:center">{shape}</g>')
    p.fill(shape, frac, d, fx=fx)


def pricetag(p, value="1\u00a2", tag="?", **_):
    """A big coin, spinning as it lands, with a price tag swinging from a string."""
    coin(p, 300, 330, 190, value, "copper", .02, flip=3)
    p.parts.append(f'<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="9" data-w="2.6" '
                   f'style="transform-box:view-box;transform-origin:520px 170px">'
                   f'<g class="a" data-fx="pop" data-at="{p.at(.3)}" data-d=".4" style="transform-box:fill-box;transform-origin:center">'
                   f'<path d="M520 170 L600 250" stroke="{INK}" stroke-width="4"/>'
                   f'<path d="M585 235 L705 235 L760 300 L705 365 L585 365 Z" fill="{RED}" stroke="{INK}" stroke-width="5" '
                   f'transform="rotate(38 600 250)"/>'
                   f'<circle cx="603" cy="262" r="9" fill="#fff" stroke="{INK}" stroke-width="3"/>'
                   f'<text x="678" y="330" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="70" fill="#fff" '
                   f'transform="rotate(38 600 250)">{H.escape(tag)}</text></g></g>')
    p.circle(520, 170, 8, .28, .1, w=5)


def receipt(p, total="$4.97", circle=-1, **_):
    """A shop receipt printing out, the total at the bottom; circle=k rings the k-th character of the total in red."""
    zig = " ".join(f"L{170 + 20 * i} {612 if i % 2 else 600}" for i in range(1, 24))
    p.parts.append(f'<g class="a" data-fx="growYdown" data-at="{p.at(.0)}" data-d="{.5 * p.dur:.2f}">'
                   f'<path d="M170 40 H630 V600 {zig} L170 600 Z" fill="#fff" stroke="{GREY}" stroke-width="3"/></g>')
    for i, w_ in enumerate((300, 220, 260, 190)):
        p.box(215, 120 + 62 * i, w_, 20, "#DCD7CF", .12 + .06 * i, rx=10, fx="growX")
        p.box(500, 120 + 62 * i, 85, 20, "#DCD7CF", .14 + .06 * i, rx=10, fx="growX")
    p.line([(210, 400), (590, 400)], .38, .12, color=GREY, w=4, dash="10 10")
    p.text(215, 490, "TOTAL", .45, size=44, anchor="start", weight=700)
    p.text(590, 495, total, .5, size=84, anchor="end", serif=True, weight=700, color=INK)
    if circle >= 0:
        cx = 590 - (len(total) - 1 - circle) * 42 - 21
        p.circle(cx, 467, 46, .65, .3, color=RED, w=7)
    coin(p, 690, 520, 62, "5\u00a2", "nickel", .55, fx="pop")
    coin(p, 110, 540, 56, "1\u00a2", "copper", .6, fx="pop")
    p.line([(62, 492), (158, 588)], .72, .12, color=RED, w=10)
    p.line([(158, 492), (62, 588)], .76, .12, color=RED, w=10)


def card_tap(p, amount="$4.97", **_):
    """A payment card sliding onto a terminal, contactless waves, the amount on the screen."""
    p.fill(f'<rect x="420" y="120" width="300" height="470" rx="40" fill="{INK}"/>'
           f'<rect x="450" y="160" width="240" height="140" rx="16" fill="#123B37"/>'
           + "".join(f'<rect x="{462 + 78 * (k % 3)}" y="{340 + 60 * (k // 3)}" width="60" height="42" rx="10" fill="#2A2A2A"/>'
                     for k in range(9)), .02)
    p.text(570, 252, amount, .2, size=62, serif=True, weight=700, color="#7FE0CF")
    for k in range(3):
        p.parts.append(f'<g class="a" data-fx="ripple" data-at="{p.at(.5 + .12 * k)}" data-d=".9" '
                       f'style="transform-box:fill-box;transform-origin:center"><circle cx="420" cy="300" r="70" fill="none" '
                       f'stroke="{TEAL}" stroke-width="8"/></g>')
    card = (f'<defs><linearGradient id="cardg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14A08F"/>'
            f'<stop offset="1" stop-color="#0B4F49"/></linearGradient></defs>'
            f'<rect x="60" y="220" width="330" height="210" rx="22" fill="url(#cardg)" stroke="#0A3B36" stroke-width="4"/>'
            f'<rect x="100" y="280" width="62" height="48" rx="8" fill="#F2C35B"/>'
            f'<rect x="100" y="370" width="210" height="16" rx="8" fill="#fff" fill-opacity=".55"/>'
            f'<text x="350" y="265" text-anchor="end" font-family="\'Sans\',sans-serif" font-weight="600" font-size="26" fill="#fff">CARD</text>')
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.15)}" data-d="{.35 * p.dur:.2f}" data-x0="-420" data-x1="40" '
                   f'data-y0="60" data-y1="-20" data-ease="out" data-r="-8">{card}</g>')


def lineup(p, first="1\u00a2", others=3, **_):
    """The penny, then a row of mystery coins bobbing with question marks."""
    coin(p, 130, 320, 125, first, "copper", .02, flip=2)
    p.text(130, 500, "PENNY", .15, size=34, weight=700)
    for k in range(others):
        x = 400 + 155 * k
        p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="14" data-w="2.4" data-ph="{k * 1.3}">')
        coin(p, x, 320, 80, "?", "nickel", .3 + .12 * k)
        p.parts.append("</g>")
    p.line([(270, 320), (308, 320)], .55, .12, color=RED, w=8)
    p.line([(292, 302), (310, 320), (292, 338)], .6, .08, color=RED, w=8)
    p.text(580, 500, "WHICH ONE?", .7, size=40, serif=True, weight=700, color=RED)


def last_coin(p, value="1\u00a2", stamp="LAST ONE", **_):
    """One coin spinning down to a stop, then a red stamp across it."""
    coin(p, 400, 300, 220, value, "copper", 0, flip=4)
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{p.at(.55)}" data-d=".45" data-rot="-12" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="150" y="250" width="500" height="110" rx="14" fill="#fff" fill-opacity=".85" stroke="{RED}" stroke-width="10"/>'
                   f'<text x="400" y="330" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="70" '
                   f'letter-spacing="4" fill="{RED}">{H.escape(stamp)}</text></g>')


def picture(name, t0, dur, w=752, h=None, seed=1, **opts):
    """A scene sized for the 9:16 engine (levels.py): the 800 x 640 drawing scaled to w."""
    h = h or round(w * 640 / 800)
    return scene(name, t0, dur, seed, **opts).replace(f'width="{W}" height="{Hh}"', f'width="{w}" height="{h}"', 1)


SCENES.update({f.__name__: f for f in (pricetag, receipt, card_tap, lineup, last_coin)})


# ---- 10 Nov scenes (BNPL Short): buy now, pay later (in colour). Generic shapes of our own: no shop, app or
# lender branding, no logos.

def _tile(x, y, w_, h_, fill, label, size, color="#fff", rx=22, stroke=INK):
    return (f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="5"/>'
            f'<text x="{x + w_ / 2}" y="{y + h_ / 2 + size * .36:.0f}" text-anchor="middle" font-family="\'Serif\',serif" '
            f'font-weight="700" font-size="{size}" fill="{color}">{H.escape(label)}</text>')


def bag_later(p, tag="LATER", **_):
    """A shopping bag dropping in, a card peeking out of it, a red tag swinging from the handle."""
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="10" data-w="1.6">')
    p.fill(f'<path d="M210 250 L590 250 L630 600 L170 600 Z" fill="{TEAL}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
           f'<path d="M210 250 L590 250 L600 300 L200 300 Z" fill="#0B4F49"/>', .0)
    p.line([(300, 255), (300, 160), (340, 110), (460, 110), (500, 160), (500, 255)], .12, .3, w=12)
    p.fill(f'<rect x="250" y="190" width="230" height="140" rx="16" fill="#F2C35B" stroke="{INK}" stroke-width="5" '
           f'transform="rotate(-12 365 260)"/><rect x="280" y="225" width="48" height="36" rx="6" fill="#B8862B" '
           f'transform="rotate(-12 365 260)"/>', .3)
    p.parts.append("</g>")
    p.parts.append(f'<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="12" data-w="2.4" '
                   f'style="transform-box:view-box;transform-origin:500px 160px">'
                   f'<g class="a" data-fx="pop" data-at="{p.at(.4)}" data-d=".4" style="transform-box:fill-box;transform-origin:center">'
                   f'<path d="M500 160 L560 300" stroke="{INK}" stroke-width="4"/>'
                   f'<path d="M500 300 L700 300 L750 360 L700 420 L500 420 Z" fill="{RED}" stroke="{INK}" stroke-width="5" '
                   f'transform="rotate(20 560 300)"/>'
                   f'<circle cx="525" cy="360" r="9" fill="#fff" stroke="{INK}" stroke-width="3" transform="rotate(20 560 300)"/>'
                   f'<text x="625" y="377" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="52" '
                   f'fill="#fff" transform="rotate(20 560 300)">{H.escape(tag)}</text></g></g>')


def split4(p, total="$100", parts=("TODAY", "?", "?", "?"), **_):
    """A price tag breaks into four tiles that slide out into a row; the first is marked."""
    p.fill(_tile(250, 40, 300, 150, RED, total, 96), .0)
    p.line([(400, 200), (400, 260)], .2, .1, w=6)
    for k, lab in enumerate(parts):
        x = 40 + 185 * k
        first = k == 0
        tile = _tile(x, 300, 165, 165, "#F2C35B" if first else "#fff", "?" if first else lab, 90,
                     color=INK)
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.25 + .1 * k)}" data-d=".5" data-x0="{360 - x}" data-x1="0" '
                       f'data-y0="-200" data-y1="0" data-ease="out">'
                       f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="7" data-w="2.2" data-ph="{k}">{tile}</g></g>')
        if first:
            p.text(x + 82, 530, parts[0], .7, size=40, weight=700, color=RED)


def pay_dots(p, labels=("TODAY", "?", "?", "?"), **_):
    """A timeline with four payment dots: the first paid and ticked, the rest waiting with question marks."""
    p.line([(70, 330), (730, 330)], .0, .35, w=8)
    for k, lab in enumerate(labels):
        x = 100 + 200 * k
        paid = k == 0
        p.fill(f'<circle cx="{x}" cy="330" r="62" fill="{TEAL if paid else "#fff"}" stroke="{INK}" stroke-width="6"/>', .15 + .12 * k)
        if paid:
            p.line([(x - 26, 332), (x - 6, 352), (x + 30, 308)], .3, .15, color="#fff", w=11)
        else:
            p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="8" data-w="2.6" data-ph="{k}">')
            p.text(x, 358, "?", .2 + .12 * k, size=80, serif=True, weight=700, color=RED)
            p.parts.append("</g>")
        p.text(x, 450, lab, .3 + .12 * k, size=34, weight=700, color=RED if paid else INK)
        p.box(x - 52, 175, 104, 64, "#F2C35B", .35 + .12 * k, rx=14)
        p.text(x, 220, "$25", .4 + .12 * k, size=38, serif=True, weight=700)


def credit_report(p, line="PAY IN 4", **_):
    """A credit report sliding up, rows filling in, a magnifier gliding over one row with a red question mark."""
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(0)}" data-d="{.3 * p.dur:.2f}" data-x0="0" data-x1="0" '
                   f'data-y0="260" data-y1="0" data-ease="out">'
                   f'<rect x="170" y="30" width="460" height="590" rx="18" fill="#fff" stroke="{INK}" stroke-width="6"/>'
                   f'<rect x="170" y="30" width="460" height="96" rx="18" fill="{TEAL}"/>'
                   f'<rect x="170" y="100" width="460" height="26" fill="{TEAL}"/>'
                   f'<text x="400" y="92" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="40" '
                   f'letter-spacing="3" fill="#fff">CREDIT REPORT</text></g>')
    for i, w_ in enumerate((300, 240, 280, 0, 220)):
        y = 175 + 80 * i
        if w_:
            p.box(215, y, w_, 22, "#DCD7CF", .25 + .07 * i, rx=11, fx="growX")
            p.box(530, y, 55, 22, "#BFE3DB", .27 + .07 * i, rx=11, fx="growX")
    p.text(215, 437, line, .5, size=40, anchor="start", weight=700, color=RED)
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.55)}" data-d=".9" data-x0="260" data-x1="0" data-y0="140" data-y1="0" '
                   f'data-ease="out"><g class="a" data-fx="float" data-at="0" data-d="1" data-amp="10" data-w="1.8">'
                   f'<circle cx="560" cy="420" r="92" fill="#fff" fill-opacity=".35" stroke="{INK}" stroke-width="14"/>'
                   f'<path d="M626 486 L730 590" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>'
                   f'<text x="560" y="452" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="96" '
                   f'fill="{RED}">?</text></g></g>')


def interest_stack(p, base="$1,000", rate="36%", **_):
    """A tall stack of notes for the loan, then a red stack growing on top of it with a question mark, a 36% tag swinging."""
    for k in range(9):
        y = 560 - 34 * k
        p.fill(f'<rect x="110" y="{y}" width="300" height="56" rx="8" fill="#BFE3DB" stroke="#0B4F49" stroke-width="4"/>'
               f'<circle cx="260" cy="{y + 28}" r="16" fill="none" stroke="#0B4F49" stroke-width="4"/>', .02 + .035 * k)
    p.text(260, 630, base, .35, size=48, serif=True, weight=700)
    p.parts.append(f'<g class="a" data-fx="growY" data-at="{p.at(.45)}" data-d="{.35 * p.dur:.2f}">'
                   + "".join(f'<rect x="480" y="{560 - 34 * k}" width="220" height="56" rx="8" fill="#F6CFC3" stroke="{RED}" stroke-width="4"/>'
                             for k in range(5)) + '</g>')
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="9" data-w="2.2">')
    p.text(590, 360, "+ ?", .6, size=96, serif=True, weight=700, color=RED)
    p.parts.append("</g>")
    p.parts.append(f'<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="10" data-w="2.3" '
                   f'style="transform-box:view-box;transform-origin:600px 40px">'
                   f'<g class="a" data-fx="pop" data-at="{p.at(.25)}" data-d=".4" style="transform-box:fill-box;transform-origin:center">'
                   f'<path d="M600 40 L600 110" stroke="{INK}" stroke-width="4"/>'
                   f'<rect x="500" y="110" width="200" height="110" rx="18" fill="{RED}" stroke="{INK}" stroke-width="5"/>'
                   f'<text x="600" y="190" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="70" '
                   f'fill="#fff">{H.escape(rate)}</text></g></g>')
    p.circle(600, 40, 8, .22, .1, w=5)


SCENES.update({f.__name__: f for f in (bag_later, split4, pay_dots, credit_report, interest_stack)})


# ---- 10 Nov (long video) scenes: the dot-com crash. All generic shapes of our own (no logos, no products, no mascots).

def bubble(p, label="", pop=False, **_):
    """A soap bubble with a shine, swelling over a ground line; pop=True bursts it into shards."""
    cx, cy = 400, 300
    if not pop:
        p.parts.append(f'<g class="a" data-fx="scale" data-at="{p.at(0)}" data-d="{.9 * p.dur:.2f}" data-s0=".55" data-s1="1.06" '
                       f'style="transform-box:fill-box;transform-origin:center bottom">'
                       f'<circle cx="{cx}" cy="{cy}" r="230" fill="#D8EEEA" fill-opacity=".55" stroke="{TEAL}" stroke-width="7"/>'
                       f'<path d="M260 230 Q290 150 370 120" fill="none" stroke="#fff" stroke-width="18" stroke-linecap="round"/>'
                       f'<circle cx="250" cy="275" r="11" fill="#fff"/></g>')
        if label:
            p.text(cx, cy + 25, label, .35, size=74, serif=True, weight=700, color=INK, fx="pop")
    else:
        p.circle(cx, cy, 230, 0, .15, color=GREY, w=4)
        for k in range(12):
            a = 2 * math.pi * k / 12 + .2
            r0, r1 = 120 + 20 * (k % 3), 230 + 50 * (k % 2)
            p.line([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))], .2 + .02 * k, .12, color=RED, w=8)
        p.text(cx, cy + 30, label or "POP", .35, size=110, serif=True, weight=700, color=RED, fx="stamp")
    p.line([(80, 580), (720, 580)], 0, .3, w=6)


def ticker(p, price="$80.06", change="-90%", up=False, **_):
    """A trading screen: a price, a change chip and a little line chart."""
    col = TEAL if up else RED
    p.fill(f'<rect x="70" y="90" width="660" height="440" rx="26" fill="{INK}"/>', 0)
    p.fill(f'<rect x="100" y="120" width="600" height="380" rx="14" fill="#141414"/>', .05)
    vals = (2, 3, 2.6, 4, 5.5, 5, 7, 6.6) if up else (6.8, 7.4, 6, 4.5, 4.9, 3, 2, 1.4)
    pts = [(130 + 540 * i / (len(vals) - 1), 470 - 30 * v) for i, v in enumerate(vals)]
    p.line(pts, .15, .45, color=col, w=9, j=1.5)
    p.text(130, 200, price, .3, size=88, serif=True, weight=700, color="#fff", anchor="start", fx="pop")
    p.box(500, 150, 175, 66, col, .45, rx=33)
    p.text(587, 196, change, .5, size=40, weight=700, color="#fff")
    p.line([(330, 530), (300, 600), (500, 600), (470, 530)], .1, .2, w=8)


def server(p, lights=True, **_):
    """A rack of network boxes with blinking lights and cables: the kit the internet ran on."""
    p.fill(f'<rect x="230" y="60" width="340" height="520" rx="18" fill="#2A2A2A" stroke="{INK}" stroke-width="6"/>', 0)
    for i in range(6):
        y = 90 + 80 * i
        p.box(255, y, 290, 60, "#3A3A3A", .08 + .05 * i, rx=8)
        for k in range(5):
            c = TEAL if (i + k) % 3 else "#E8B04A"
            p.parts.append(f'<g class="a" data-fx="{"beat" if lights else "fade"}" data-at="{p.at(.4 + .03 * k)}" data-d="0.4" data-n="40" '
                           f'style="transform-box:fill-box;transform-origin:center"><circle cx="{285 + 28 * k}" cy="{y + 30}" r="9" fill="{c}"/></g>')
        p.box(440, y + 22, 85, 16, "#555", .12 + .05 * i, rx=4)
    for k, (x0, c) in enumerate(((570, RED), (570, TEAL), (230, INK))):
        y0 = 150 + 140 * k
        x1 = 760 if x0 > 400 else 40
        p.line([(x0, y0), ((x0 + x1) / 2, y0 + 60), (x1, y0 + 30)], .5 + .06 * k, .25, color=c, w=8)
    p.line([(160, 590), (640, 590)], 0, .3, w=6)


def parcel(p, label="", n=3, **_):
    """Cardboard boxes stacked up, taped, a delivery arrow: online shopping (no brand)."""
    xs = [(250, 400, 260, 170), (420, 400, 240, 170), (330, 240, 240, 160)][:max(1, min(n, 3))]
    for i, (x, y, w_, h_) in enumerate(xs):
        p.fill(f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="6" fill="#D9B27C" stroke="{INK}" stroke-width="6"/>'
               f'<rect x="{x + w_ / 2 - 22}" y="{y}" width="44" height="{h_}" fill="#C79A5E"/>'
               f'<rect x="{x + 20}" y="{y + h_ - 50}" width="70" height="30" fill="#fff" stroke="{INK}" stroke-width="3"/>', .1 + .15 * i, fx="pop")
    p.line([(70, 330), (190, 330)], .6, .15, color=RED, w=10)
    p.line([(165, 305), (192, 330), (165, 355)], .66, .1, color=RED, w=10)
    p.line([(120, 572), (720, 572)], 0, .3, w=6)
    if label:
        p.text(470, 625, label, .7, size=36, weight=700, color=RED)


def ballot(p, **_):
    """Benjamin Graham's line as a picture: a ballot box (voting machine) beside a weighing scale."""
    p.fill(f'<rect x="70" y="300" width="270" height="230" rx="12" fill="#fff" stroke="{INK}" stroke-width="7"/>'
           f'<rect x="150" y="296" width="110" height="16" rx="6" fill="{INK}"/>', 0)
    for k in range(3):
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.1 + .12 * k)}" data-d=".35" data-x0="{-40 + 40 * k}" data-x1="0" '
                       f'data-y0="-160" data-y1="0" data-ease="out">'
                       f'<rect x="{165 + 8 * k}" y="{230}" width="70" height="90" rx="4" fill="#fff" stroke="{GREY}" stroke-width="4" transform="rotate({-10 + 10 * k} 200 275)"/></g>')
    p.text(205, 590, "SHORT TERM", .4, size=30, weight=700, color=RED)
    p.line([(590, 200), (590, 520)], .3, .2, w=8)
    p.line([(470, 520), (710, 520)], .35, .15, w=8)
    p.line([(460, 230), (720, 230)], .4, .2, w=8)
    for x in (480, 700):
        p.line([(x, 230), (x - 50, 340), (x + 50, 340)], .5, .15, w=6, closed=True)
    p.fill(f'<rect x="450" y="290" width="60" height="44" rx="6" fill="{TEAL}"/>', .62)
    p.text(590, 590, "LONG TERM", .7, size=30, weight=700, color=TEAL)


def payback(p, years=10, paid=10, label="", **_):
    """Years in a row, each filling with a coin as it is 'paid back'; the last one lands in red."""
    n = years
    cols = min(n, 5)
    rows = math.ceil(n / cols)
    for k in range(n):
        r, c = divmod(k, cols)
        x, y = 110 + c * 120, 140 + r * 200
        p.rect(x, y, 100, 150, .02 + .02 * k, .15, color=GREY, w=4)
        p.text(x + 50, y + 185, f"Y{k + 1}", .05 + .02 * k, size=26, weight=600, color=GREY)
        if k < paid:
            p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.25 + .055 * k)}" data-d=".3" data-y0="-90" data-y1="0" data-ease="out">'
                           f'<circle cx="{x + 50}" cy="{y + 75}" r="38" fill="{RED if k == n - 1 else "#E0A93B"}" stroke="{INK}" stroke-width="5"/>'
                           f'<text x="{x + 50}" y="{y + 88}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="34" fill="#fff">$</text></g>')
    if label:
        p.text(400, 60, label, .1, size=40, serif=True, weight=700, color=INK)


def petbowl(p, closed=True, **_):
    """A pet food bowl, and a shop sign flipped to CLOSED."""
    p.fill(f'<path d="M180 470 Q200 560 400 560 Q600 560 620 470 Z" fill="{RED}" stroke="{INK}" stroke-width="7"/>'
           f'<ellipse cx="400" cy="470" rx="220" ry="34" fill="#B82F0E" stroke="{INK}" stroke-width="6"/>', 0)
    for k in range(7):
        p.fill(f'<circle cx="{290 + 36 * k}" cy="{462 - 10 * (k % 2)}" r="14" fill="#8A5A2B"/>', .15 + .02 * k)
    p.line([(400, 90), (300, 200)], .3, .1, w=5)
    p.line([(400, 90), (500, 200)], .32, .1, w=5)
    p.fill(f'<circle cx="400" cy="88" r="10" fill="{INK}"/>', .3)
    p.parts.append(f'<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="5" data-w="2.2" style="transform-origin:400px 90px">'
                   f'<rect x="250" y="200" width="300" height="120" rx="12" fill="#fff" stroke="{INK}" stroke-width="7"/>'
                   f'<text x="400" y="280" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="62" fill="{RED if closed else TEAL}">'
                   f'{"CLOSED" if closed else "OPEN"}</text></g>')
    p.line([(120, 562), (680, 562)], 0, .3, w=6)


def bell(p, label="", **_):
    """A bell that nobody rings: drawn, hanging still, a red cross through the sound lines."""
    p.line([(400, 60), (400, 130)], 0, .15, w=8)
    p.fill(f'<path d="M260 430 Q270 240 330 190 Q400 130 470 190 Q530 240 540 430 Q560 450 580 470 H220 Q240 450 260 430 Z" fill="#E8B04A" stroke="{INK}" stroke-width="7"/>'
           f'<circle cx="400" cy="495" r="30" fill="{INK}"/>', .1)
    for k, s in enumerate((-1, 1)):
        for j in range(2):
            x = 400 + s * (220 + 45 * j)
            p.line([(x, 260), (x + s * 25, 320), (x, 380)], .4 + .05 * j, .12, color=GREY, w=6)
    p.line([(120, 200), (680, 460)], .65, .15, color=RED, w=12)
    if label:
        p.text(400, 600, label, .7, size=36, weight=700, color=RED)


def rocket(p, fall=False, **_):
    """A little rocket climbing a dotted path; fall=True tips it over at the top and drops it."""
    path = [(110, 560), (260, 470), (390, 330), (500, 190), (560, 110)]
    p.line(path, 0, .5, color=GREY, w=5, dash="12 14")
    body = (f'<g transform="scale(1.8)"><path d="M-30 40 L0 -70 L30 40 Z" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="0" cy="-10" r="12" fill="{TEAL}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-30 40 L-50 70 L-20 46 Z M30 40 L50 70 L20 46 Z" fill="{RED}"/>'
            f'<path d="M-14 46 Q0 90 14 46 Z" fill="#E8B04A"/></g>')
    if not fall:
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.1)}" data-d="{.6 * p.dur:.2f}" data-x0="0" data-x1="420" '
                       f'data-y0="0" data-y1="-420" data-ease="inout"><g transform="translate(130 560) rotate(40)">{body}</g></g>')
    else:
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.2)}" data-d="{.55 * p.dur:.2f}" data-x0="0" data-x1="60" '
                       f'data-y0="0" data-y1="430" data-ease="inout" data-r="150"><g transform="translate(560 120) rotate(40)">{body}</g></g>')
        p.line([(560, 560), (620, 520), (680, 570)], .8, .1, color=RED, w=8)
    p.line([(60, 590), (740, 590)], 0, .3, w=6)


SCENES.update({f.__name__: f for f in (bubble, ticker, server, parcel, ballot, payback, petbowl, bell, rocket)})


# ---- 11 Nov scenes (IG Reel, Levels #9, WACC): the capital structure, drawn as diagrams of the mechanism
# on the paper ground (red for the risky or costly part, teal for the cheap one). Generic shapes of our own.

def capital_stack(p, top="EQUITY", bottom="DEBT", **_):
    """Two blocks stacked like a balance sheet's right side: debt at the bottom, paid first (a coin drops on
    it with a 1), equity on top, paid last (a red 2), a dashed arrow climbing the order of payment."""
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(0)}" data-d=".5" data-x0="0" data-x1="0" data-y0="120" data-y1="0" data-ease="out">'
                   f'<rect x="150" y="360" width="420" height="230" rx="18" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                   f'<text x="360" y="500" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="76" fill="#fff">{H.escape(bottom)}</text></g>')
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.15)}" data-d=".5" data-x0="0" data-x1="0" data-y0="-200" data-y1="0" data-ease="out">'
                   f'<rect x="150" y="60" width="420" height="280" rx="18" fill="#fff" stroke="{RED}" stroke-width="7"/>'
                   f'<text x="360" y="225" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="76" fill="{RED}">{H.escape(top)}</text></g>')
    for k, (y, n, col) in enumerate(((475, "1", TEAL), (200, "2", RED))):
        p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="8" data-w="2.2" data-ph="{k}">')
        p.fill(f'<circle cx="680" cy="{y}" r="58" fill="#F2C35B" stroke="{INK}" stroke-width="6"/>'
               f'<text x="680" y="{y + 26}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="74" fill="{col}">{n}</text>',
               .4 + .2 * k)
        p.parts.append("</g>")
    p.line([(70, 570), (70, 90)], .45, .5, w=6, dash="16 14")
    p.line([(48, 120), (70, 84), (92, 120)], .7, .15, w=6)


def tax_cut(p, before="8%", after="6%", rate="25%", **_):
    """A tall teal bar for the cost of debt before tax; a red dashed slice across its top is the tax saved,
    and it falls away, leaving the after-tax bar with a question mark."""
    p.line([(120, 600), (680, 600)], .0, .25, w=6)
    p.box(260, 160, 280, 440, TEAL, .08, rx=12, fx="growY")
    p.text(400, 410, before, .2, size=96, serif=True, weight=700, color="#fff")
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.5)}" data-d=".7" data-x0="0" data-x1="170" data-y0="0" data-y1="-60" data-ease="in">'
                   f'<rect x="260" y="160" width="280" height="110" rx="12" fill="#F6CFC3" stroke="{RED}" stroke-width="6" stroke-dasharray="18 12"/>'
                   f'<text x="400" y="232" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="44" fill="{RED}">TAX {H.escape(rate)}</text></g>')
    p.line([(230, 270), (570, 270)], .4, .2, color=RED, w=7, dash="20 12")
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="9" data-w="2.4">')
    p.text(640, 470, "?", .75, size=130, serif=True, weight=700, color=RED)
    p.parts.append("</g>")


def mix_bar(p, left="EQUITY 60%", right="DEBT 40%", lcost="10%", rcost="6%", split=.6, **_):
    """One bar of the company's funding split into its two parts, each with its cost on a tag above it,
    and a scale weighing them underneath."""
    x0, x1, y = 60, 740, 250
    xm = x0 + (x1 - x0) * split
    p.box(x0, y, xm - x0, 170, "#fff", .05, rx=14, fx="growX")
    p.rect(x0, y, xm - x0, 170, .05, .4, color=RED, w=7)
    p.box(xm + 10, y, x1 - xm - 10, 170, TEAL, .25, rx=14, fx="growX")
    p.text((x0 + xm) / 2, y + 108, left, .3, size=46, weight=700, color=RED)
    p.text((xm + 10 + x1) / 2, y + 108, right, .45, size=46, weight=700, color="#fff")
    for k, (cx, s, col) in enumerate((((x0 + xm) / 2, lcost, RED), ((xm + 10 + x1) / 2, rcost, TEAL))):
        p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="7" data-w="2.1" data-ph="{k}">')
        p.box(cx - 90, 70, 180, 110, "#F2C35B", .55 + .12 * k, rx=18)
        p.text(cx, 147, s, .6 + .12 * k, size=72, serif=True, weight=700, color=col)
        p.parts.append("</g>")
    p.line([(400, 470), (400, 560)], .7, .2, w=6)
    p.line([(250, 600), (550, 600)], .75, .2, w=8)
    p.text(400, 640, "WEIGHTED", .8, size=34, weight=700)


def wacc_curve(p, **_):
    """WACC against debt: a marker U-curve drawn left to right, a dot rolling down it and then up past the
    bottom, a red question mark at the high right end."""
    p.line([(90, 40), (90, 560), (740, 560)], .0, .35, w=7)
    p.text(115, 60, "WACC", .1, size=40, weight=700, anchor="start", fx="fade")
    p.text(560, 615, "MORE DEBT", .15, size=38, weight=700)
    p.line([(700, 595), (740, 560), (700, 525)], .3, .1, w=6)
    pts = [(x, 470 - .0028 * (x - 400) ** 2) for x in range(130, 731, 12)]
    p.line(pts, .2, .55, color=RED, w=9, j=1.0)
    lo = max(pts, key=lambda q: q[1])
    p.line([(lo[0], lo[1] + 20), (lo[0], 560)], .7, .2, color=TEAL, w=5, dash="12 10")
    p.parts.append(f'<g class="a" data-fx="pop" data-at="{p.at(.75)}" data-d=".35" style="transform-box:fill-box;transform-origin:center">'
                   f'<circle cx="{lo[0]}" cy="{lo[1]}" r="20" fill="{TEAL}" stroke="{INK}" stroke-width="5"/></g>')
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="10" data-w="2.3">')
    p.text(pts[-1][0] - 10, pts[-1][1] - 30, "?", .85, size=110, serif=True, weight=700, color=RED)
    p.parts.append("</g>")


SCENES.update({f.__name__: f for f in (capital_stack, tax_cut, mix_bar, wacc_curve)})
