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
  11 Nov, long video (who paid for WW1): newspaper(headline, sub, date, stamp), poster(top, big, bottom),
  ledger(names, hi), perpetual(coupon, title), shrink(years, label, last)
  youtube.py now fits every drawing to its box (the drawn part fills its half of the frame).
  11 Nov (Singles' Day Short): sale_bag(date, tag), four_ones(month), shopfront(n, banner),
  tally_board(year, total, unit, hidden), markup_tag(start, up, mid, off, end); _ptag() draws a price tag
  12 Nov (Levels #10, working capital): wc_minus(assets, liab, strike), shelf_cash(amount), prepaid(amount),
  cash_first(left, right, band)
  12 Nov (compound interest Short): cent_or_million(), coin_stacks(values), hourglass72(rate), quote_card(quote),
  doubling_bars(days, known, line); each drawn edge to edge of the 800 x 640 canvas so it fills its box
  12 Nov, long video (where money comes from): t_account(left, right, amount, destroy), keystroke(amount, pre, label),
  goldsmith(bars, notes), multiplier(start, ratio, steps), outflow(label, n), token(coin, reserve, rule, lock)
  13 Nov (Friday the 13th Short): fri13_page(), year_grid(year), road_cat(), ladder_wallet(tag), friday_bars(n, hi);
  cat_svg(x, y, s) draws a sitting black cat for floaters and the close
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
    w = max(220, 38 * len(text) + 70)        # 11 Nov: was 30 per letter, which clipped 'COVERED UP' at 52 px
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


# ---- 11 Nov scenes (Singles' Day Short): 11.11, the shops, the hidden total, the markup trap. Generic shapes of
# our own: no shop, platform or brand marks, no logos.

def _ptag(x, y, w_, label, fill=RED, color="#fff", size=None, rot=0, stroke=INK):
    """A price tag (pointed left end, a hole) centred on x, y, w_ wide."""
    h_ = w_ * .52
    x0, y0 = x - w_ / 2, y - h_ / 2
    size = size or round(h_ * .5)
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x0 + h_ * .38:.0f} {y0:.0f} L{x0 + w_:.0f} {y0:.0f} L{x0 + w_:.0f} {y0 + h_:.0f} L{x0 + h_ * .38:.0f} {y0 + h_:.0f} '
            f'L{x0:.0f} {y:.0f} Z" fill="{fill}" stroke="{stroke}" stroke-width="5" stroke-linejoin="round"/>'
            f'<circle cx="{x0 + h_ * .36:.0f}" cy="{y:.0f}" r="{h_ * .09:.0f}" fill="#fff" stroke="{stroke}" stroke-width="3"/>'
            f'<text x="{x + h_ * .18:.0f}" y="{y + size * .36:.0f}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
            f'font-size="{size}" fill="{color}">{H.escape(label)}</text></g>')


def sale_bag(p, date="11.11", tag="-20%", **_):
    """A red shopping bag with the date on it, bobbing, and a sale tag swinging from the handle."""
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="10" data-w="1.6">')
    p.fill(f'<path d="M190 240 L610 240 L650 610 L150 610 Z" fill="{RED}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
           f'<path d="M190 240 L610 240 L616 290 L184 290 Z" fill="#9E2A0D"/>'
           f'<text x="400" y="480" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="150" '
           f'fill="#fff" letter-spacing="-4">{H.escape(date)}</text>', .0)
    p.line([(290, 245), (290, 150), (330, 100), (470, 100), (510, 150), (510, 245)], .12, .3, w=12)
    p.parts.append("</g>")
    p.parts.append(f'<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="12" data-w="2.4" '
                   f'style="transform-box:view-box;transform-origin:510px 150px">'
                   f'<g class="a" data-fx="pop" data-at="{p.at(.35)}" data-d=".4" style="transform-box:fill-box;transform-origin:center">'
                   f'<path d="M510 150 L600 215" stroke="{INK}" stroke-width="4"/>'
                   + _ptag(680, 250, 230, tag, "#F2C35B", INK, 64, rot=28) + '</g></g>')


def four_ones(p, month="NOVEMBER", **_):
    """A calendar page: 11.11 at the top, then four lone stick figures, one per 1, popping in and bobbing apart."""
    p.fill(f'<rect x="110" y="20" width="580" height="610" rx="26" fill="#fff" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M110 46 Q110 20 136 20 L664 20 Q690 20 690 46 L690 120 L110 120 Z" fill="{RED}"/>', .0)
    for x in (230, 570):
        p.fill(f'<rect x="{x - 12}" y="-6" width="24" height="56" rx="12" fill="{INK}"/>', .05)
    p.text(400, 92, month, .08, size=48, weight=700, color="#fff")
    p.text(400, 270, "11.11", .15, size=150, serif=True, weight=700)
    cols = (TEAL, "#F2C35B", "#7A6BB0", RED)
    for k, x in enumerate((200, 330, 470, 600)):
        p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="9" data-w="2.1" data-ph="{k * 1.4}">')
        p.fill(f'<circle cx="{x}" cy="358" r="30" fill="{cols[k]}" stroke="{INK}" stroke-width="5"/>', .35 + .1 * k)
        p.line([(x, 390), (x, 510)], .38 + .1 * k, .18, w=9)
        p.line([(x - 34, 440), (x, 418), (x + 34, 440)], .42 + .1 * k, .14, w=8)
        p.line([(x - 28, 580), (x, 510), (x + 28, 580)], .45 + .1 * k, .14, w=8)
        p.parts.append("</g>")


def shopfront(p, n=3, banner="11.11 SALE", **_):
    """A street of little shops, striped awnings popping on, a sale banner swinging over them, a red question mark."""
    awn = (RED, TEAL, "#E0A93B")
    for k in range(n):
        x0 = 50 + 240 * k
        p.fill(f'<rect x="{x0}" y="300" width="220" height="290" fill="#FBF7F0" stroke="{INK}" stroke-width="5"/>'
               f'<rect x="{x0 + 22}" y="350" width="100" height="100" rx="6" fill="#D6E2F3" stroke="{INK}" stroke-width="4"/>'
               f'<rect x="{x0 + 142}" y="380" width="58" height="210" rx="6" fill="{awn[k]}" stroke="{INK}" stroke-width="4"/>'
               f'<circle cx="{x0 + 188}" cy="490" r="5" fill="{INK}"/>', .05 + .1 * k)
        stripes = "".join(f'<rect x="{x0 - 10 + 30 * j}" y="235" width="30" height="62" fill="{awn[k] if j % 2 == 0 else "#fff"}"/>'
                          for j in range(8))
        scal = "".join(f'<circle cx="{x0 + 5 + 30 * j}" cy="297" r="15" fill="{awn[k] if j % 2 == 0 else "#fff"}" '
                       f'stroke="{INK}" stroke-width="3"/>' for j in range(8))
        p.fill(f'<g>{scal}{stripes}<rect x="{x0 - 10}" y="235" width="240" height="62" fill="none" stroke="{INK}" stroke-width="5"/></g>',
               .15 + .1 * k, fx="growYdown")
    p.line([(30, 592), (770, 592)], .0, .3, w=7)
    p.parts.append(f'<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="3" data-w="1.8" '
                   f'style="transform-box:view-box;transform-origin:400px 40px">'
                   f'<g class="a" data-fx="pop" data-at="{p.at(.45)}" data-d=".45" style="transform-box:fill-box;transform-origin:center">'
                   f'<path d="M140 60 L400 30 L660 60" fill="none" stroke="{INK}" stroke-width="4"/>'
                   f'<path d="M120 80 L680 80 L660 125 L680 170 L120 170 L140 125 Z" fill="{RED}" stroke="{INK}" stroke-width="5" '
                   f'stroke-linejoin="round"/>'
                   f'<text x="400" y="145" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="66" '
                   f'fill="#fff">{H.escape(banner)}</text></g></g>')
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="10" data-w="2.4">')
    p.fill(f'<circle cx="720" cy="240" r="56" fill="#fff" stroke="{RED}" stroke-width="7"/>'
           f'<text x="720" y="272" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="90" fill="{RED}">?</text>',
           .7)
    p.parts.append("</g>")


def tally_board(p, year="2021", total=540.3, unit="bn yuan", hidden=("2022", "2023", "2024", "2025"), **_):
    """A sales scoreboard: one row counts up to the last published total, the rows after it stay dark with question marks."""
    p.fill(f'<rect x="70" y="30" width="660" height="590" rx="28" fill="#16302D" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="70" y="30" width="660" height="92" rx="28" fill="{TEAL}"/><rect x="70" y="96" width="660" height="26" fill="{TEAL}"/>', .0)
    p.text(400, 96, "11.11 TOTAL SALES", .05, size=44, weight=700, color="#fff")
    p.text(115, 210, year, .15, size=50, anchor="start", weight=700, color="#7FE0CF")
    p.parts.append(f'<g class="a" data-fx="fade" data-at="{p.at(.18)}" data-d=".3"><text x="690" y="212" text-anchor="end" '
                   f'font-family="\'Serif\',serif" font-weight="700" font-size="62" fill="#fff" class="a" data-fx="count" '
                   f'data-at="{p.at(.2)}" data-d="{max(.35 * p.dur, 1):.2f}" data-from="0" data-to="{total}" data-dec="1" data-show="1" '
                   f'data-suf=" {unit}">{total} {unit}</text></g>')
    p.line([(110, 250), (690, 250)], .25, .15, color="#2F5A55", w=4)
    for k, yr in enumerate(hidden):
        y = 320 + 78 * k
        p.text(115, y, yr, .4 + .08 * k, size=46, anchor="start", weight=700, color="#6E8F8B")
        p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="5" data-w="2.6" data-ph="{k}">')
        for j in range(3):
            p.fill(f'<rect x="{430 + 88 * j}" y="{y - 46}" width="70" height="62" rx="10" fill="#0B1E1C" stroke="#2F5A55" stroke-width="3"/>'
                   f'<text x="{465 + 88 * j}" y="{y + 2}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
                   f'font-size="50" fill="{RED}">?</text>', .45 + .08 * k + .03 * j)
        p.parts.append("</g>")


def markup_tag(p, start="$100", up="+25%", mid="$125", off="-20%", end="?", **_):
    """The markup trap: a $100 tag, a red arrow up to a bigger tag (+25%), then a teal arrow down to a tag with a question mark (-20%)."""
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="7" data-w="2.2">')
    p.fill(_ptag(150, 470, 240, start, TEAL, "#fff", 64, rot=-8), .02)
    p.parts.append("</g>")
    p.line([(170, 380), (210, 240), (300, 170)], .2, .25, color=RED, w=10)
    p.line([(262, 150), (306, 168), (284, 212)], .4, .08, color=RED, w=10)
    p.box(130, 175, 150, 70, "#fff", .35, rx=16)
    p.text(205, 226, up, .38, size=50, serif=True, weight=700, color=RED)
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="9" data-w="1.9" data-ph="1.2">')
    p.fill(_ptag(440, 150, 300, mid, RED, "#fff", 80, rot=6), .45)
    p.parts.append("</g>")
    p.line([(560, 230), (640, 320), (660, 400)], .6, .2, color=TEAL, w=10)
    p.line([(628, 372), (660, 410), (686, 368)], .75, .08, color=TEAL, w=10)
    p.box(680, 250, 120, 66, "#fff", .66, rx=16)
    p.text(740, 298, off, .68, size=46, serif=True, weight=700, color=TEAL)
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="11" data-w="2.6" data-ph="2.3">')
    p.fill(_ptag(610, 520, 260, end, "#F2C35B", INK, 96, rot=-6), .82)
    p.parts.append("</g>")


SCENES.update({f.__name__: f for f in (sale_bag, four_ones, shopfront, tally_board, markup_tag)})
# ---- 11 Nov (long video, Armistice Day): how the First World War was paid for. Generic shapes of our own:
# no real posters, mastheads, banknotes or emblems are copied.

def newspaper(p, headline="OVER-SUBSCRIBED", sub="AND STILL THEY POUR IN", date="1914", stamp="", **_):
    """A folded broadsheet: a made-up masthead bar, a big headline, columns of grey lines; stamp= slams a red
    verdict across it (e.g. FALSE)."""
    p.fill(f'<rect x="90" y="70" width="620" height="500" rx="8" fill="#fff" stroke="{INK}" stroke-width="6" transform="rotate(-2 400 320)"/>', 0)
    p.box(120, 95, 560, 54, INK, .06, rx=4)
    p.text(400, 134, "THE DAILY LEDGER", .1, size=34, serif=True, weight=700, color="#fff")
    p.text(670, 180, date, .14, size=26, weight=600, color=GREY, anchor="end")
    size = 64 if len(headline) <= 12 else 54 if len(headline) <= 16 else 44
    p.text(400, 255, headline, .2, size=size, serif=True, weight=700, color=INK, fx="pop")
    p.text(400, 305, sub, .3, size=28, weight=700, color=GREY)
    for c in range(3):
        for r in range(6):
            x = 130 + 185 * c
            p.line([(x, 350 + 34 * r), (x + 160 - 30 * ((r + c) % 2), 350 + 34 * r)], .35 + .02 * (r + 3 * c), .08, color=GREY, w=5, j=.8)
    if stamp:
        p.text(400, 470, stamp, .75, size=120, serif=True, weight=700, color=RED, fx="stamp")


def poster(p, top="IF YOU CANNOT FIGHT", big="INVEST", bottom="5% WAR BONDS", **_):
    """A recruiting-style poster of our own: a frame, a line on top, a huge word, a coin, a ribbon at the foot."""
    p.fill(f'<rect x="170" y="40" width="460" height="560" rx="6" fill="#F3E6CF" stroke="{INK}" stroke-width="7"/>', 0)
    p.rect(195, 65, 410, 510, .05, .3, color=RED, w=5)
    p.text(400, 140, top, .15, size=34 if len(top) < 22 else 28, weight=700, color=INK)
    p.text(400, 255, big, .25, size=104 if len(big) <= 7 else 76, serif=True, weight=700, color=RED, fx="pop")
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="8" data-w="2.0">')
    p.fill(f'<circle cx="400" cy="385" r="78" fill="#E0A93B" stroke="{INK}" stroke-width="6"/>'
           f'<circle cx="400" cy="385" r="58" fill="none" stroke="#B9822A" stroke-width="4"/>'
           f'<text x="400" y="410" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="70" fill="#fff">£</text>', .4)
    p.parts.append("</g>")
    p.box(215, 495, 370, 62, INK, .55, rx=4)
    p.text(400, 537, bottom, .6, size=32, weight=700, color="#fff")


def ledger(p, names=("A. Smith  £300", "J. Brown  £1,000", "G. Nairn  ?", "E. Harvey  ?"), hi=(2, 3), **_):
    """An open ledger: two pages of ruled lines with handwritten-looking entries; the hi rows get circled red."""
    p.fill(f'<path d="M60 120 Q230 90 400 130 Q570 90 740 120 V560 Q570 530 400 570 Q230 530 60 560 Z" fill="#FBF6EA" stroke="{INK}" stroke-width="6"/>', 0)
    p.line([(400, 130), (400, 570)], .05, .2, w=5)
    for k in range(9):
        y = 175 + 42 * k
        p.line([(90, y), (375, y)], .08 + .01 * k, .1, color="#C9C2B4", w=3, j=.5)
        p.line([(425, y), (710, y)], .08 + .01 * k, .1, color="#C9C2B4", w=3, j=.5)
    for i, n in enumerate(names[:8]):
        side, row = divmod(i, 4) if len(names) > 4 else (0, i)
        x = 105 if (i % 2 == 0 or len(names) <= 4) and side == 0 else 440
        if len(names) <= 4:
            x, row = (105, i) if i < 2 else (440, i - 2)
        y = 205 + 84 * row
        p.text(x, y, n, .2 + .1 * i, size=30, weight=600, color=INK, anchor="start", serif=True)
        if i in hi:
            p.line([(x - 15, y - 34), (x + 270, y - 34), (x + 270, y + 14), (x - 15, y + 14)], .65 + .08 * (i in hi and hi.index(i)), .2,
                   color=RED, w=6, closed=True, j=3)


def perpetual(p, coupon="3½%", title="WAR LOAN", due="∞", **_):
    """A bond certificate of our own design: a coupon, and in the 'repayable' box an infinity sign that keeps
    drawing itself."""
    p.fill(f'<rect x="80" y="80" width="640" height="460" rx="14" fill="#EEF5F3" stroke="{TEAL}" stroke-width="8"/>', 0)
    p.rect(105, 105, 590, 410, .05, .3, color=TEAL, w=3)
    p.text(400, 185, title, .12, size=64, serif=True, weight=700, color=TEAL)
    p.text(400, 300, coupon, .25, size=110, serif=True, weight=700, color=INK, fx="pop")
    p.text(400, 345, "A YEAR, EVERY YEAR", .32, size=28, weight=700, color=GREY)
    p.box(250, 380, 300, 110, "#fff", .4, rx=10)
    p.rect(250, 380, 300, 110, .4, .2, color=INK, w=4)
    p.text(270, 410, "REPAYABLE", .45, size=20, weight=700, color=GREY, anchor="start")
    pts = [(400 + 80 * math.cos(a) / (1 + math.sin(a) ** 2), 450 + 80 * math.sin(a) * math.cos(a) / (1 + math.sin(a) ** 2))
           for a in [2 * math.pi * i / 40 for i in range(40)]]
    p.line(pts, .5, .4, color=RED, w=9, closed=True, j=.6)
    for k in range(4):
        p.fill(f'<circle cx="{150 + 500 * (k % 2)}" cy="{130 + 380 * (k // 2)}" r="12" fill="{TEAL}"/>', .1 + .05 * k)


def shrink(p, years=("1927", "", "", "2015"), label="£100", last="£1.82", **_):
    """The same banknote, smaller in each year: what inflation does to money lent at a fixed sum."""
    n = len(years)
    xs = [130 + 540 * i / max(n - 1, 1) for i in range(n)]
    for i, (x, y_) in enumerate(zip(xs, years)):
        s = 1 - .78 * i / max(n - 1, 1)
        w_, h_ = 170 * s, 96 * s
        col = RED if i == n - 1 else TEAL
        p.fill(f'<rect x="{x - w_ / 2}" y="{330 - h_ / 2}" width="{w_}" height="{h_}" rx="{8 * s}" fill="#DCEFE9" stroke="{col}" stroke-width="5"/>'
               f'<circle cx="{x}" cy="330" r="{30 * s}" fill="none" stroke="{col}" stroke-width="4"/>', .1 + .17 * i)
        p.text(x, 330 - h_ / 2 - 22, label if i < n - 1 else last, .15 + .17 * i, size=int(26 + 18 * (i == n - 1)), weight=700, color=col)
        p.text(x, 470, y_, .12 + .17 * i, size=36, weight=700, color=INK)
    p.line([(80, 420), (720, 420)], .05, .5, w=6)
    p.line([(690, 400), (722, 420), (690, 440)], .55, .1, w=6)
    p.text(400, 560, "WHAT IT BUYS", .8, size=32, weight=700, color=GREY)


SCENES.update({f.__name__: f for f in (newspaper, poster, ledger, perpetual, shrink)})


# ---- 12 Nov scenes (IG Reel, Levels #10, working capital): the mechanism of each level drawn as a diagram on
# the paper ground (teal for cash coming in, red for cash going out or owed). Generic shapes of our own.

def wc_minus(p, assets=("INVENTORY", "RECEIVABLES", "CASH"), liab=("PAYABLES",), strike="CASH", **_):
    """Current assets stacked on the left, a big minus, current liabilities on the right, and the result in a
    gold tile underneath; at the end the cash tile is struck out in red (a model leaves cash out)."""
    p.text(190, 50, "CURRENT ASSETS", .0, size=34, weight=700, color=TEAL)
    p.text(610, 50, "CURRENT LIABILITIES", .1, size=34, weight=700, color=RED)
    for k, lab in enumerate(assets):
        y = 80 + 105 * k
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.05 + .1 * k)}" data-d=".45" data-x0="-160" data-x1="0" '
                       f'data-y0="0" data-y1="0" data-ease="out">'
                       + _tile(40, y, 300, 88, "#fff", "", 10, stroke=TEAL)
                       + f'<text x="190" y="{y + 57}" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" '
                         f'font-size="38" fill="{TEAL}">{H.escape(lab)}</text></g>')
        if lab == strike:
            p.line([(30, y + 44), (350, y + 44)], .82, .25, color=RED, w=10)
    p.text(400, 240, "−", .4, size=150, serif=True, weight=700, color=INK, fx="pop")
    for k, lab in enumerate(liab):
        y = 185 + 105 * k
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.45 + .1 * k)}" data-d=".45" data-x0="160" data-x1="0" '
                       f'data-y0="0" data-y1="0" data-ease="out">'
                       + _tile(460, y, 300, 88, "#fff", "", 10, stroke=RED)
                       + f'<text x="610" y="{y + 57}" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" '
                         f'font-size="38" fill="{RED}">{H.escape(lab)}</text></g>')
    p.line([(60, 425), (740, 425)], .55, .3, w=7)
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="7" data-w="2.1">')
    p.fill(_tile(140, 460, 520, 130, "#F2C35B", "WORKING CAPITAL", 54, color=INK), .65)
    p.parts.append("</g>")


def shelf_cash(p, amount="-$30", **_):
    """Three boxes of stock drop onto a shelf one by one while the cash pile beside them shrinks, a red tag
    with the amount swinging under it."""
    p.line([(40, 330), (440, 330)], .0, .25, w=9)
    p.line([(80, 330), (80, 420)], .05, .1, w=7)
    p.line([(400, 330), (400, 420)], .05, .1, w=7)
    for k in range(3):
        x = 60 + 125 * k
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.12 + .14 * k)}" data-d=".45" data-x0="0" data-x1="0" '
                       f'data-y0="-260" data-y1="0" data-ease="out">'
                       f'<rect x="{x}" y="210" width="115" height="115" rx="8" fill="#E9C08A" stroke="{INK}" stroke-width="6"/>'
                       f'<path d="M{x} 250 L{x + 115} 250" stroke="#B8862B" stroke-width="6"/>'
                       f'<rect x="{x + 42}" y="210" width="31" height="40" fill="#B8862B"/></g>')
    p.text(240, 490, "INVENTORY", .3, size=44, weight=700)
    # the cash pile: five notes, the top three slide away towards the shelf as the boxes land
    for k in range(5):
        y = 400 - 52 * k
        note = (f'<rect x="510" y="{y}" width="230" height="44" rx="8" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>'
                f'<circle cx="625" cy="{y + 22}" r="13" fill="none" stroke="#fff" stroke-width="4"/>')
        if k >= 2:
            p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.12 + .14 * (4 - k))}" data-d=".45" data-x0="0" '
                           f'data-x1="-360" data-y0="0" data-y1="-140" data-ease="in">'
                           f'<g class="a" data-fx="life" data-at="0" data-d="{round(p.at(.12 + .14 * (4 - k)) + .4, 3)}" data-fi=".01" data-fo=".05">'
                           f'{note}</g></g>')
        else:
            p.fill(note, .0)
    p.text(625, 515, "CASH", .05, size=44, weight=700, color=TEAL)
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="8" data-w="2.3">')
    p.fill(_ptag(625, 590, 210, amount, RED, "#fff", 52), .6)
    p.parts.append("</g>")


def prepaid(p, amount="+$40", **_):
    """A gold coin drops into the cash box on the left; on the right an IOU note for next year's service
    comes up with a red LIABILITY stamp, and REVENUE $0 is written under it."""
    p.fill(_tile(40, 260, 300, 230, TEAL, "CASH", 76), .0)
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.15)}" data-d=".5" data-x0="0" data-x1="0" data-y0="-300" '
                   f'data-y1="0" data-ease="out">'
                   f'<circle cx="190" cy="150" r="78" fill="#F2C35B" stroke="{INK}" stroke-width="6"/>'
                   f'<text x="190" y="172" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="58" '
                   f'fill="{TEAL}">{H.escape(amount)}</text></g>')
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.35)}" data-d=".5" data-x0="0" data-x1="0" data-y0="160" '
                   f'data-y1="0" data-ease="out">'
                   f'<rect x="430" y="70" width="330" height="420" rx="14" fill="#fff" stroke="{INK}" stroke-width="6"/>'
                   f'<text x="595" y="140" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="34" '
                   f'fill="{INK}">WE OWE YOU</text>'
                   f'<text x="595" y="185" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="600" font-size="30" '
                   f'fill="{GREY}">NEXT YEAR\'S SERVICE</text></g>')
    for k in range(3):
        p.line([(470, 250 + 50 * k), (720, 250 + 50 * k)], .45 + .05 * k, .15, color=GREY, w=5)
    p.parts.append(f'<g class="a" data-fx="stamp" data-rot="0" data-at="{p.at(.65)}" data-d=".35" style="transform-box:fill-box;transform-origin:center">'
                   f'<g transform="rotate(-10 595 400)"><rect x="445" y="360" width="300" height="80" rx="10" fill="#fff" '
                   f'fill-opacity=".9" stroke="{RED}" stroke-width="7"/><text x="595" y="415" text-anchor="middle" '
                   f'font-family="\'Serif\',serif" font-weight="700" font-size="46" letter-spacing="2" fill="{RED}">LIABILITY</text></g></g>')
    p.text(400, 600, "REVENUE TODAY: $0", .8, size=48, weight=700, color=RED)


def cash_first(p, left="CUSTOMER PAYS", right="YOU PAY SUPPLIER", band="YOUR CASH", **_):
    """A timeline: the customer's payment lands first (teal), the supplier is paid later (red), and the gold
    band between them, the time the cash sits with you, fills in with coins bobbing on it."""
    p.line([(50, 360), (750, 360)], .0, .3, w=8)
    p.line([(715, 330), (750, 360), (715, 390)], .25, .1, w=8)
    p.box(150, 300, 500, 120, "#F2C35B", .45, rx=16, fx="growX")
    p.text(400, 378, band, .55, size=50, weight=700)
    for x, col, lab, ty, f in ((150, TEAL, left, 240, .1), (650, RED, right, 490, .3)):
        p.fill(f'<circle cx="{x}" cy="360" r="34" fill="{col}" stroke="{INK}" stroke-width="6"/>', f)
        p.text(x, ty, lab, f + .05, size=40, weight=700, color=col)
    p.text(150, 140, "FIRST", .15, size=58, serif=True, weight=700, color=TEAL)
    p.text(650, 590, "LATER", .35, size=58, serif=True, weight=700, color=RED)
    for k, x in enumerate((280, 400, 520)):
        p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="9" data-w="2.2" data-ph="{k}">')
        p.fill(f'<circle cx="{x}" cy="290" r="30" fill="#F2C35B" stroke="{INK}" stroke-width="5"/>'
               f'<text x="{x}" y="304" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="40" '
               f'fill="{TEAL}">$</text>', .65 + .08 * k)
        p.parts.append("</g>")


SCENES.update({f.__name__: f for f in (wc_minus, shelf_cash, prepaid, cash_first)})


# ---- 12 Nov (compound interest Short). Generic shapes of our own: no portraits, no real coin designs.
# Each one is drawn out to the edges of the 800 x 640 canvas, so it reads at full size in its box.

def _bag(x, y, w_, label, fill=TEAL):
    """A money sack centred on x (top at y), w_ wide, its label on the front."""
    h_ = w_ * 1.05
    return (f'<path d="M{x - w_ * .18:.0f} {y + h_ * .16:.0f} Q{x - w_ * .5:.0f} {y + h_ * .45:.0f} {x - w_ * .5:.0f} {y + h_ * .72:.0f} '
            f'Q{x - w_ * .5:.0f} {y + h_:.0f} {x:.0f} {y + h_:.0f} Q{x + w_ * .5:.0f} {y + h_:.0f} {x + w_ * .5:.0f} {y + h_ * .72:.0f} '
            f'Q{x + w_ * .5:.0f} {y + h_ * .45:.0f} {x + w_ * .18:.0f} {y + h_ * .16:.0f} Z" fill="{fill}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M{x - w_ * .2:.0f} {y + h_ * .16:.0f} L{x - w_ * .3:.0f} {y:.0f} L{x + w_ * .3:.0f} {y:.0f} L{x + w_ * .2:.0f} {y + h_ * .16:.0f} Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<rect x="{x - w_ * .24:.0f}" y="{y + h_ * .13:.0f}" width="{w_ * .48:.0f}" height="{w_ * .07:.0f}" rx="6" fill="#F2C35B" stroke="{INK}" stroke-width="4"/>'
            f'<text x="{x:.0f}" y="{y + h_ * .74:.0f}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
            f'font-size="{w_ * .3:.0f}" fill="#fff">{H.escape(label)}</text>')


def cent_or_million(p, left="1\u00a2", right="$1M", **_):
    """The riddle: a spinning cent with x2 badges popping round it, OR, and a fat money sack bobbing."""
    coin(p, 190, 330, 170, left, "copper", .02, flip=3)
    for k, (bx, by) in enumerate(((60, 120), (320, 110), (330, 540))):
        p.fill(_tile(bx - 50, by - 34, 100, 68, RED, "\u00d72", 44), .3 + .12 * k)
    p.text(408, 352, "OR", .45, size=54, serif=True, weight=700, color=INK, fx="pop")
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="10" data-w="1.8">')
    p.fill(_bag(615, 120, 330, right), .55)
    p.parts.append("</g>")


def coin_stacks(p, values=("$100", "$110", "?"), labels=("START", "YEAR 1", "YEAR 2"), **_):
    """Three stacks of coins growing left to right, each labelled; the last one ends in a question mark."""
    for k, (v, lab) in enumerate(zip(values, labels)):
        x = 140 + 260 * k
        n = 4 + 2 * k
        for j in range(n):
            y = 560 - 46 * j
            last = k == len(values) - 1 and j >= n - 2
            fill, rim = ("#F2C35B", "#8A5F12") if not last else (RED, "#7A1E08")
            p.fill(f'<ellipse cx="{x}" cy="{y + 8}" rx="105" ry="30" fill="{rim}"/>'
                   f'<ellipse cx="{x}" cy="{y}" rx="105" ry="30" fill="{fill}" stroke="{INK}" stroke-width="5"/>',
                   .05 + .22 * k + .025 * j, .25)
        top = 560 - 46 * n - 40
        p.fill(_tile(x - 95, top - 60, 190, 84, TEAL if k < len(values) - 1 else RED, v, 56), .2 + .25 * k)
        p.text(x, 630, lab, .1 + .25 * k, size=30, weight=700, color=GREY)


def hourglass72(p, rate="8%", left="\u00d71", right="\u00d72", **_):
    """An hourglass with sand running, a small coin pile on the left, a pile twice as big on the right, the rate on a tile."""
    p.parts.append('<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="4" data-w="1.4" '
                   'style="transform-box:view-box;transform-origin:400px 330px">')
    p.fill(f'<rect x="275" y="40" width="250" height="34" rx="10" fill="#B8862B" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="275" y="566" width="250" height="34" rx="10" fill="#B8862B" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M300 74 L500 74 Q500 220 410 320 Q500 420 500 566 L300 566 Q300 420 390 320 Q300 220 300 74 Z" '
           f'fill="#EAF4F8" fill-opacity=".9" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           f'<path d="M330 150 L470 150 Q460 240 400 300 Q340 240 330 150 Z" fill="#F2C35B"/>'
           f'<path d="M318 560 Q330 470 400 440 Q470 470 482 560 Z" fill="#F2C35B"/>', .0)
    p.line([(400, 300), (400, 445)], .2, .6, color="#B8862B", w=5, dash="10 9")
    p.parts.append("</g>")
    for k in range(2):
        coin(p, 120, 520 - 70 * k, 58, "$", "gold", .25 + .08 * k)
    p.fill(_tile(55, 270, 130, 76, INK, left, 44), .4)
    for k in range(4):
        coin(p, 680, 540 - 66 * k, 58, "$", "gold", .5 + .08 * k)
    p.fill(_tile(615, 160, 130, 76, RED, right, 44), .82)
    p.text(400, 634, f"AT {rate} A YEAR", .3, size=34, weight=700, color=TEAL)


def quote_card(p, quote=("COMPOUND INTEREST", "IS THE 8TH WONDER", "OF THE WORLD"), by="SAID BY ?", **_):
    """A framed quotation card, tilted, with big quote marks, three lines and an unknown speaker, a magnifier hovering over it."""
    p.fill(f'<rect x="30" y="60" width="740" height="470" rx="26" fill="#fff" stroke="{INK}" stroke-width="7" transform="rotate(-3 400 300)"/>', 0)
    p.text(95, 220, "\u201c", .05, size=230, serif=True, weight=700, color=RED, fx="pop")
    for k, line in enumerate(quote):
        p.text(420, 210 + 78 * k, line, .15 + .12 * k, size=50, serif=True, weight=700, color=INK)
    p.box(240, 445, 330, 64, TEAL, .55, rx=14)
    p.text(405, 489, by, .58, size=36, weight=700, color="#fff")
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="14" data-w="1.7" data-ph=".8">')
    p.circle(660, 470, 78, .7, .3, color=INK, w=12)
    p.line([(715, 528), (780, 600)], .8, .12, color=INK, w=20)
    p.parts.append("</g>")


def doubling_bars(p, days=30, known=25, line="$1 MILLION", **_):
    """A cent doubling every day: 30 bars, flat for weeks, then shooting up; the last days are dashed boxes with a ?,
    and a dashed line marks a million dollars. Heights are 2^(day-1) cents against $1M = 400 px (our arithmetic)."""
    x0, base, top, bw = 30, 580, 400, 24.6
    p.line([(x0 - 10, base), (790, base)], 0, .2, w=6)
    for d in range(1, days + 1):
        x = x0 + (d - 1) * 25.4
        cents = 2 ** (d - 1)
        h_ = max(4, top * cents / 1e8)
        if d <= known:
            p.box(round(x, 1), round(base - h_, 1), bw - 4, round(h_, 1), RED if d == known else TEAL, .05 + .02 * d, rx=3, fx="growY")
        else:
            p.line([(x, base), (x, base - 520), (x + bw - 4, base - 520), (x + bw - 4, base)], .65 + .03 * (d - known), .12,
                   color=GREY, w=3, dash="7 6")
    p.line([(x0 - 10, base - top), (790, base - top)], .55, .3, color=RED, w=5, dash="16 10")
    p.box(30, base - top - 70, 300, 56, "#fff", .6, rx=12)
    p.text(180, base - top - 30, line, .62, size=36, serif=True, weight=700, color=RED)
    p.text(690, 120, "?", .85, size=120, serif=True, weight=700, color=RED, fx="pop")
    coin(p, 95, 470, 62, "1\u00a2", "copper", .02, flip=2)                     # day 1: one cent
    p.box(170, 438, 250, 62, "#fff", .1, rx=12)
    p.text(295, 482, "DAY 1: 1\u00a2", .12, size=36, serif=True, weight=700, color=TEAL)
    kx = x0 + (known - 1) * 25.4 + 10                                              # day `known`, still under $1M
    p.line([(kx, base - top * 2 ** (known - 1) / 1e8 - 10), (kx - 60, 300)], .5, .15, color=RED, w=4)
    p.box(kx - 330, 250, 290, 62, "#fff", .52, rx=12)
    p.text(kx - 185, 294, f"DAY {known}: ${2 ** (known - 1) / 100:,.0f}", .54, size=34, serif=True, weight=700, color=RED)
    for d in (1, 10, 20, 30):
        p.text(x0 + (d - 1) * 25.4 + 10, 624, f"DAY {d}" if d in (1, 30) else str(d), .1, size=24, weight=700, color=GREY,
               anchor="middle")


SCENES.update({f.__name__: f for f in (cent_or_million, coin_stacks, hourglass72, quote_card, doubling_bars)})
# ---- 12 Nov scenes (YouTube #5, where money comes from): a bank's books, a keystroke, a goldsmith's notes, the
# textbook multiplier, a run, and a fully backed token. Generic shapes of our own: no bank, app or coin branding.

def _count(x, y, frm, to, at, d, size=60, color=INK, pre="", suf="", dec=0, anchor="middle"):
    """A number that counts up inside the drawing (motion.py 'count' on an SVG text)."""
    return (f'<text class="a" data-fx="count" data-at="{at}" data-d="{d}" data-from="{frm}" data-to="{to}" data-dec="{dec}" '
            f'data-pre="{H.escape(pre)}" data-suf="{H.escape(suf)}" x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-family="\'Serif\',serif" font-weight="700" font-size="{size}" fill="{color}">{H.escape(pre)}{frm}{H.escape(suf)}</text>')


def t_account(p, left="LOAN", right="DEPOSIT", amount="+£100", destroy=False, title="THE BANK'S BOOKS", **_):
    """A bank's balance sheet as a T: ASSETS on the left, LIABILITIES on the right. The loan and the deposit
    pop in at the same instant, joined by a gold bracket ('created together'). destroy=True: both are then
    struck out in red as the loan is repaid, and the money is gone."""
    p.text(400, 50, title, .0, size=36, weight=700, color=GREY)
    p.line([(60, 120), (740, 120)], .02, .3, w=9)
    p.line([(400, 120), (400, 560)], .1, .3, w=9)
    p.text(230, 100, "ASSETS", .15, size=40, weight=700, color=TEAL)
    p.text(570, 100, "LIABILITIES", .15, size=40, weight=700, color=RED)
    for x, lab, col in ((85, left, TEAL), (425, right, RED)):
        p.fill(f'<rect x="{x}" y="200" width="290" height="190" rx="18" fill="#fff" stroke="{col}" stroke-width="7"/>'
               f'<text x="{x + 145}" y="270" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="40" fill="{col}">{H.escape(lab)}</text>'
               f'<text x="{x + 145}" y="350" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="64" fill="{INK}">{H.escape(amount)}</text>',
               .38, d=.4)
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="6" data-w="2">')
    p.line([(230, 420), (230, 460), (570, 460), (570, 420)], .55, .3, color="#B8862B", w=8)
    p.fill(_tile(240, 480, 320, 70, "#F2C35B", "SAME MOMENT", 36, color=INK, rx=16), .62)
    p.parts.append("</g>")
    if destroy:
        for x in (85, 425):
            p.line([(x - 10, 300), (x + 300, 290)], .78, .2, color=RED, w=12)
        p.text(400, 620, "REPAID: THE MONEY IS GONE", .85, size=40, weight=700, color=RED)


def keystroke(p, amount=10000, pre="£", label="YOUR ACCOUNT", key="ENTER", **_):
    """A screen with an account balance counting up from 0 after a key is pressed: a loan typed into being."""
    p.rect(110, 40, 580, 360, .0, .35, w=8)
    p.box(130, 60, 540, 320, "#fff", .05, rx=8, fx="fade")
    p.line([(360, 400), (320, 470), (480, 470), (440, 400)], .1, .2, w=7)
    p.text(400, 140, label, .15, size=38, weight=700, color=GREY)
    p.text(400, 205, "BALANCE", .18, size=32, weight=600, color=GREY)
    n = len(pre + f"{amount:,}")                                    # shrink long amounts so they fit the screen
    p.parts.append(_count(400, 320, 0, amount, p.at(.5), round(.3 * p.dur, 2), size=min(96, int(900 / max(n, 1))), color=TEAL, pre=pre))
    # the key, pressed once just before the count starts
    p.parts.append(f'<g class="a" data-fx="press" data-at="{p.at(.4)}" data-d=".25" style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="250" y="500" width="300" height="110" rx="20" fill="{PAPER}" stroke="{INK}" stroke-width="7"/>'
                   f'<rect x="262" y="510" width="276" height="80" rx="14" fill="#fff" stroke="{GREY}" stroke-width="3"/>'
                   f'<text x="400" y="566" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="44" fill="{INK}">{H.escape(key)}</text></g>')
    p.fill(f'<circle cx="590" cy="520" r="18" fill="{RED}"/>', .42)
    p.parts.append(f'<g class="a" data-fx="ripple" data-at="{p.at(.42)}" data-d=".6" style="transform-box:fill-box;transform-origin:center">'
                   f'<circle cx="400" cy="555" r="90" fill="none" stroke="{RED}" stroke-width="6"/></g>')


def goldsmith(p, bars=3, notes=6, **_):
    """A goldsmith's strongbox with a few gold bars in it, and paper notes ('promise to pay') flying out of it
    one after another, more notes than bars; the extra ones are outlined in red."""
    p.rect(60, 300, 300, 260, .0, .35, w=8)
    p.line([(60, 300), (100, 240), (400, 240), (360, 300)], .08, .25, w=8)
    p.line([(360, 560), (400, 500), (400, 240)], .12, .2, w=8)
    for k in range(bars):
        x, y = 95 + 85 * (k % 3), 470 - 60 * (k // 3)
        p.fill(f'<path d="M{x} {y + 50} L{x + 15} {y} L{x + 65} {y} L{x + 80} {y + 50} Z" fill="#F2C35B" stroke="{INK}" stroke-width="5"/>', .15 + .05 * k)
    p.text(210, 610, f"{bars} BARS OF GOLD", .3, size=36, weight=700)
    for k in range(notes):
        col = INK if k < bars else RED
        # 12 Nov fix: the notes sit in a two-column grid beside the box (they had piled up on top of each other)
        x0, y0 = 425 + 190 * (k % 2), 60 + 135 * (k // 2)
        rot = (-6, 4, -3, 5, -5, 3)[k % 6]
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.35 + .08 * k)}" data-d=".45" data-x0="{220 - x0}" data-x1="0" '
                       f'data-y0="{420 - y0}" data-y1="0" data-ease="out">'
                       f'<g transform="rotate({rot} {x0 + 85} {y0 + 45})"><rect x="{x0}" y="{y0}" width="170" height="90" rx="8" fill="#fff" '
                       f'stroke="{col}" stroke-width="6"/><text x="{x0 + 85}" y="{y0 + 40}" text-anchor="middle" font-family="\'Serif\',serif" '
                       f'font-style="italic" font-weight="600" font-size="22" fill="{col}">I promise to pay</text>'
                       f'<path d="M{x0 + 25} {y0 + 64} H{x0 + 145}" stroke="{GREY}" stroke-width="4"/></g></g>')
    p.text(610, 610, f"{notes} NOTES", .35 + .08 * notes, size=36, weight=700, color=RED if notes > bars else INK)


def multiplier(p, start=100, ratio=.9, steps=5, stamp_text="TEXTBOOK", **_):
    """The textbook money multiplier: a deposit is lent on, re-deposited and lent again, each bar a little
    shorter, in a cascade down to the right; then a red stamp over it."""
    v = float(start)
    for k in range(steps):
        x, y = 50 + 140 * k, 80 + 90 * k
        w_ = 120
        h_ = 360 * v / start
        p.box(x, 560 - h_, w_, h_, TEAL if k == 0 else "#BFD9D5", .05 + .12 * k, rx=8, fx="growY")
        p.text(x + w_ / 2, 545 - h_, f"{v:.0f}", .1 + .12 * k, size=40, serif=True, weight=700)
        if k < steps - 1:
            p.line([(x + w_ - 10, 590), (x + 150, 590)], .1 + .12 * k, .15, color=RED, w=5)
        v *= ratio
    p.line([(30, 560), (770, 560)], .0, .3, w=8)
    p.text(400, 625, "deposit, lend 90%, re-deposit, lend again", .2, size=32, weight=600, color=GREY)
    if not stamp_text:
        return
    p.parts.append(f'<g class="a" data-fx="stamp" data-rot="0" data-at="{p.at(.75)}" data-d=".35" style="transform-box:fill-box;transform-origin:center">'
                   f'<g transform="rotate(-12 470 170)"><rect x="270" y="115" width="400" height="110" rx="12" fill="#fff" fill-opacity=".9" '
                   f'stroke="{RED}" stroke-width="9"/><text x="470" y="192" text-anchor="middle" font-family="\'Serif\',serif" '
                   f'font-weight="700" font-size="64" letter-spacing="3" fill="{RED}">{H.escape(stamp_text)}</text></g></g>')


def outflow(p, label="$40bn+ OUT", n=7, **_):
    """A bank with phones around it, and coins streaming out of its door towards each phone: a run, by app."""
    p.line([(260, 200), (400, 110), (540, 200)], .0, .3, w=8)
    p.rect(270, 200, 260, 220, .05, .3, w=8)
    for k in range(4):
        p.line([(300 + 60 * k, 220), (300 + 60 * k, 400)], .1 + .03 * k, .15, w=6)
    p.box(370, 340, 60, 80, INK, .2, rx=4)
    p.line([(220, 420), (580, 420)], .1, .2, w=8)
    spots = [(90, 140), (80, 330), (130, 520), (400, 560), (670, 520), (720, 330), (710, 140)][:n]
    for k, (x, y) in enumerate(spots):
        p.fill(f'<rect x="{x - 32}" y="{y - 52}" width="64" height="104" rx="12" fill="#fff" stroke="{INK}" stroke-width="5"/>'
               f'<rect x="{x - 22}" y="{y - 38}" width="44" height="66" rx="4" fill="#E8E4DE"/>', .2 + .05 * k)
        for j in range(2):
            p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.45 + .05 * k + .12 * j)}" data-d=".55" data-x0="0" '
                           f'data-x1="{x - 400}" data-y0="0" data-y1="{y - 380}" data-ease="out">'
                           f'<g class="a" data-fx="life" data-at="{p.at(.45 + .05 * k + .12 * j)}" data-d=".6" data-fi=".05" data-fo=".2">'
                           f'<circle cx="400" cy="380" r="20" fill="#F2C35B" stroke="{INK}" stroke-width="4"/></g></g>')
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="6" data-w="2.4">')
    p.fill(_ptag(400, 40, 300, label, RED, "#fff", 40), .7)
    p.parts.append("</g>")


def token(p, coin="$1", reserve="$1", rule="1 : 1", lock="NO LENDING", **_):
    """A fully backed token: a coin on the left, a reserve box with one note for it on the right, an equals
    sign between, and a padlock under the reserve that says it is not lent on."""
    p.fill(f'<circle cx="190" cy="250" r="130" fill="#BFD9D5" stroke="{INK}" stroke-width="7"/>'
           f'<circle cx="190" cy="250" r="100" fill="none" stroke="{TEAL}" stroke-width="5" stroke-dasharray="14 10"/>'
           f'<text x="190" y="278" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="84" fill="{TEAL}">{H.escape(coin)}</text>', .0)
    p.text(190, 440, "TOKEN", .1, size=40, weight=700, color=TEAL)
    p.text(400, 280, "=", .25, size=120, serif=True, weight=700, fx="pop")
    p.rect(480, 120, 260, 260, .3, .3, w=8)
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.4)}" data-d=".45" data-x0="0" data-x1="0" data-y0="-200" data-y1="0" data-ease="out">'
                   f'<rect x="510" y="220" width="200" height="90" rx="8" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>'
                   f'<text x="610" y="282" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="54" fill="#fff">{H.escape(reserve)}</text></g>')
    p.text(610, 440, "RESERVE", .45, size=40, weight=700)
    p.fill(_tile(270, 500, 260, 80, "#F2C35B", rule, 52, color=INK, rx=16), .55)
    # padlock
    p.line([(585, 520), (585, 495), (635, 495), (635, 520)], .65, .2, color=RED, w=7)
    p.box(570, 520, 80, 60, RED, .7, rx=8)
    p.text(610, 625, lock, .75, size=34, weight=700, color=RED)


SCENES.update({f.__name__: f for f in (t_account, keystroke, goldsmith, multiplier, outflow, token)})


# ---- 12 Nov scenes (Levels #11, shareholders' equity). Generic boxes, notes and certificates of our own:
# no company, logo or real balance sheet.

GOLD = "#F2C35B"


def _note(x, y, w_=150, h_=64):
    return (f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="9" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{x + w_ / 2}" cy="{y + h_ / 2}" r="{h_ * .26:.0f}" fill="none" stroke="#fff" stroke-width="4"/>')


def _cert(x, y, w_=150, h_=104, label="SHARE"):
    return (f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="6" fill="#FFF8E6" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x + 10}" y="{y + 10}" width="{w_ - 20}" height="{h_ - 20}" rx="3" fill="none" stroke="#B8862B" stroke-width="3"/>'
            f'<text x="{x + w_ / 2}" y="{y + h_ / 2 + 11}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
            f'font-size="30" fill="{INK}">{label}</text>')


def _slide(p, frac, inner, x0=0, y0=0, x1=0, y1=0, d=.45, ease="out"):
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(frac)}" data-d="{d}" data-x0="{x0}" data-x1="{x1}" '
                   f'data-y0="{y0}" data-y1="{y1}" data-ease="{ease}">{inner}</g>')


def bs_bars(p, assets=100, liab=80, scale=3.2, base=470, **_):
    """The balance sheet as two columns on one baseline: assets on the left, liabilities and equity stacked on
    the right, an equals sign between. Equity is whatever is left. When liabilities are bigger than assets the
    equity block hangs below the baseline in red, dashed: negative equity."""
    eq = assets - liab
    ha, hl, he = assets * scale, liab * scale, abs(eq) * scale

    def col(x, y, h_, fill, label, amount, frac, color="#fff", dash=False):
        st = f'stroke-dasharray="14 10"' if dash else ""
        lab = (f'<text x="{x + 130}" y="{y + h_ / 2 - 6:.0f}" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" '
               f'font-size="34" fill="{color}">{label}</text>'
               f'<text x="{x + 130}" y="{y + h_ / 2 + 44:.0f}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
               f'font-size="50" fill="{color}">{amount}</text>') if h_ >= 110 else (
               f'<text x="{x + 130}" y="{y + h_ / 2 + 13:.0f}" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" '
               f'font-size="34" fill="{color}">{label} {amount}</text>')
        _slide(p, frac, f'<rect x="{x}" y="{y:.0f}" width="260" height="{h_:.0f}" rx="12" fill="{fill}" stroke="{INK}" '
                        f'stroke-width="6" {st}/>' + lab, y0=60 if y < base else -60)

    p.line([(30, base), (770, base)], .0, .3, w=7)
    col(60, base - ha, ha, TEAL, "ASSETS", f"${assets}", .08)
    col(480, base - hl, hl, RED, "LIABILITIES", f"${liab}", .3)
    if eq > 0:
        col(480, base - hl - he, he, GOLD, "EQUITY", f"${eq}", .52, color=INK)
    else:
        col(480, base, he, "#FDE7DF", "EQUITY", f"−${-eq}", .52, color=RED, dash=True)
    p.text(400, base - ha / 2 + 30, "=", .45, size=110, serif=True, weight=700, fx="pop")
    if eq < 0:
        p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="6" data-w="2.2">')
        p.fill(_ptag(250, base + 80, 250, "BELOW 0", RED, "#fff", 40, rot=-6), .75)
        p.parts.append("</g>")


def dividend(p, amount="\u2212$10", **_):
    """A cash pile on the left; the top notes fly across to three shareholders, who cheer; underneath, the
    retained earnings tile takes a red tag for the same amount."""
    for k in range(4):
        y = 300 - 70 * k
        note = _note(60, y)
        if k == 3:
            _slide(p, .2, f'<g class="a" data-fx="life" data-at="0" data-d="{round(p.at(.2) + .55, 3)}" data-fi=".01" data-fo=".05">{note}</g>',
                   x1=470, y1=-40, d=.6, ease="inout")
        else:
            p.fill(note, .02 + .04 * k)
    p.text(135, 420, "CASH", .05, size=40, weight=700, color=TEAL)
    p.line([(250, 170), (520, 170)], .1, .3, w=7, dash="16 12")
    p.line([(495, 150), (520, 170), (495, 190)], .2, .1, w=7)
    for k in range(3):
        figure(p, 580 + 75 * k, 330, .8, .3 + .06 * k, TEAL if k == 1 else None)
    p.fill(_note(560, 100, 120, 52), .45)
    p.text(655, 420, "SHAREHOLDERS", .3, size=34, weight=700)
    p.fill(_tile(70, 480, 470, 110, GOLD, "", 10, color=INK), .55)
    p.text(305, 548, "RETAINED EARNINGS", .55, size=34, weight=700)
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="7" data-w="2.4">')
    p.fill(_ptag(660, 535, 220, amount, RED, "#fff", 50, rot=-5), .7)
    p.parts.append("</g>")


def buyback(p, amount="\u2212$50", **_):
    """The company (a block with columns) on the left, shareholders on the right. Cash notes travel right on the
    top track, share certificates travel back left on the bottom track and are stamped CANCELLED; equity takes a
    red tag."""
    p.fill(f'<path d="M40 210 L210 120 L380 210 Z" fill="{INK}"/>'
           f'<rect x="60" y="210" width="300" height="230" fill="#fff" stroke="{INK}" stroke-width="6"/>'
           + "".join(f'<rect x="{85 + 70 * k}" y="235" width="40" height="180" fill="#E8E4DE" stroke="{INK}" stroke-width="4"/>' for k in range(4))
           + f'<rect x="40" y="440" width="340" height="24" fill="{INK}"/>', .0)
    p.text(210, 95, "COMPANY", .05, size=36, weight=700)
    for k in range(3):
        figure(p, 560 + 80 * k, 440, .8, .1 + .05 * k)
    p.text(640, 500, "SHAREHOLDERS", .15, size=34, weight=700)
    for k in range(2):                                  # cash out, to the right, high
        _slide(p, .2 + .12 * k, f'<g class="a" data-fx="life" data-at="0" data-d="{round(p.at(.2 + .12 * k) + .55, 3)}" '
                                f'data-fi=".01" data-fo=".05">{_note(260, 60)}</g>', x1=300, y1=0, d=.55, ease="inout")
    p.text(470, 150, "CASH OUT", .2, size=30, weight=700, color=TEAL)
    _slide(p, .45, _cert(330, 470, 200, 130, label="SHARES"), x0=300, x1=-230, d=.6)
    p.fill(f'<g transform="rotate(-12 200 560)"><rect x="60" y="527" width="280" height="66" rx="8" fill="#fff" fill-opacity=".85" stroke="{RED}" '
           f'stroke-width="6"/><text x="200" y="574" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" '
           f'font-size="40" fill="{RED}">CANCELLED</text></g>', .66, fx="stamp")
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="7" data-w="2.2">')
    p.text(520, 600, "EQUITY", .72, size=40, weight=700, color=RED)
    p.fill(_ptag(705, 588, 170, amount, RED, "#fff", 46, rot=-4), .75)
    p.parts.append("</g>")


SCENES.update({f.__name__: f for f in (bs_bars, dividend, buyback)})


# ---- 13 Nov scenes (Friday the 13th Short): a calendar page with a black cat, a year of 13ths under a
# magnifier, a road with a cat crossing, a ladder and an open wallet, Fridays on a trading screen. Our own
# generic shapes: no film, brand or character.

def cat_svg(x, y, s=1.0, eyes="#F2C35B"):
    """A black cat sitting, seen from the side-front, its tail curled up; (x, y) is where it sits, s scales it."""
    t = f'translate({x} {y}) scale({s})'
    return (f'<g transform="{t}">'
            f'<path d="M58 -14 Q130 -10 118 -70 Q112 -102 136 -112" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M-62 0 Q-74 -96 -30 -138 L30 -138 Q74 -96 62 0 Z" fill="{INK}"/>'
            f'<circle cx="0" cy="-168" r="52" fill="{INK}"/>'
            f'<path d="M-48 -190 L-40 -248 L-8 -212 Z M48 -190 L40 -248 L8 -212 Z" fill="{INK}"/>'
            f'<ellipse cx="-20" cy="-172" rx="10" ry="13" fill="{eyes}"/><ellipse cx="20" cy="-172" rx="10" ry="13" fill="{eyes}"/>'
            f'<rect x="-22" y="-182" width="4" height="20" rx="2" fill="{INK}"/><rect x="18" y="-182" width="4" height="20" rx="2" fill="{INK}"/>'
            f'</g>')


def _page(x, y, w_, h_, month, day, head=RED, rot=0, size=None):
    size = size or h_ * .5
    return (f'<g transform="rotate({rot} {x + w_ / 2} {y + h_ / 2})">'
            f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="{w_ * .07:.0f}" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{x}" y="{y}" width="{w_}" height="{h_ * .27:.0f}" rx="{w_ * .07:.0f}" fill="{head}" stroke="{INK}" stroke-width="6"/>'
            f'<text x="{x + w_ / 2}" y="{y + h_ * .2:.0f}" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" '
            f'font-size="{h_ * .15:.0f}" fill="#fff" letter-spacing="2">{H.escape(month)}</text>'
            f'<text x="{x + w_ / 2}" y="{y + h_ * .86:.0f}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
            f'font-size="{size:.0f}" fill="{INK}">{H.escape(day)}</text></g>')


def fri13_page(p, **_):
    """The hook: a tilted calendar page FRIDAY / 13 dropping in, a black cat beside it with a swinging tail,
    and a little falling arrow over a ? (does the market fall?)."""
    p.fill(_page(40, 70, 420, 500, "FRIDAY", "13", RED, rot=-5, size=300), 0, .4)
    p.line([(140, 40), (140, 110)], .08, .12, w=12)
    p.line([(360, 22), (360, 92)], .1, .12, w=12)
    p.parts.append('<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="3" data-w="1.6" '
                   'style="transform-box:view-box;transform-origin:640px 620px">')
    p.fill(cat_svg(640, 620, 1.55), .3, .4)
    p.parts.append("</g>")
    p.line([(520, 60), (590, 130), (630, 100), (740, 220)], .55, .35, color=RED, w=12)
    p.line([(700, 222), (744, 224), (740, 180)], .8, .12, color=RED, w=12)
    p.text(770, 110, "?", .85, size=110, serif=True, weight=700, color=RED, fx="pop")


def year_grid(p, year="2026", **_):
    """Twelve small calendar pages for the year, every one on the 13th, with a magnifier gliding over them."""
    months = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
    p.text(400, 52, year, 0, size=54, serif=True, weight=700, color=INK)
    for k, m in enumerate(months):
        cx, cy = 20 + (k % 4) * 195, 84 + (k // 4) * 182
        p.fill(_page(cx, cy, 175, 165, m, "13", TEAL if k % 2 else RED, rot=(-3, 2, -1, 3)[k % 4], size=86), .05 + .045 * k, .3)
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="70" data-w=".55" data-ph=".4">')
    p.circle(470, 360, 92, .7, .3, color=INK, w=14)
    p.fill(f'<circle cx="470" cy="360" r="84" fill="#fff" fill-opacity=".35"/>', .72)
    p.line([(536, 426), (612, 506)], .8, .14, color=INK, w=24)
    p.parts.append("</g>")


def road_cat(p, **_):
    """A road with a dashed centre line, a little car coming, a black cat crossing in front, a warning sign with 13 and a ?."""
    p.fill(f'<path d="M0 420 H800 V600 H0 Z" fill="#5E5A55"/>', 0)
    for x in range(10, 800, 120):
        p.box(x, 502, 70, 14, "#F7F5F2", .05 + x / 4000, rx=4)
    p.parts.append('<g class="a" data-fx="move" data-at="{}" data-d="1.4" data-x="-260">'.format(p.at(.1)))
    p.fill(f'<path d="M430 520 L452 462 Q462 440 492 436 L530 398 H640 L690 436 Q730 442 740 466 L748 520 Z" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M542 408 H582 V436 H516 Z M600 408 H636 L668 436 H600 Z" fill="#EAF4F8" stroke="{INK}" stroke-width="4"/>'
           f'<circle cx="490" cy="526" r="32" fill="{INK}"/><circle cx="490" cy="526" r="12" fill="#E4E0D9"/>'
           f'<circle cx="690" cy="526" r="32" fill="{INK}"/><circle cx="690" cy="526" r="12" fill="#E4E0D9"/>'
           f'<path d="M742 470 h18" stroke="#F2C35B" stroke-width="10" stroke-linecap="round"/>', .1)
    p.parts.append("</g>")
    p.parts.append('<g class="a" data-fx="move" data-at="{}" data-d="1.2" data-x="-200">'.format(p.at(.3)))
    p.fill(cat_svg(250, 560, .95), .3)
    p.parts.append("</g>")
    p.line([(130, 400), (130, 230)], .2, .2, w=10)
    p.parts.append('<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="5" data-w="2" '
                   'style="transform-box:view-box;transform-origin:130px 250px">')
    p.fill(f'<path d="M130 40 L240 240 L20 240 Z" fill="#F2C35B" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
           f'<text x="130" y="214" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="96" fill="{INK}">13</text>', .25)
    p.parts.append("</g>")
    p.text(720, 300, "?", .75, size=150, serif=True, weight=700, color=RED, fx="pop")


def ladder_wallet(p, tag="$?", **_):
    """An open wallet under a leaning ladder, banknotes fluttering out of it, a red price tag swinging: money lost."""
    p.line([(70, 600), (330, 40)], 0, .3, w=12, color="#8A5F12")
    p.line([(190, 610), (440, 70)], .05, .3, w=12, color="#8A5F12")
    for k in range(7):
        f = .14 + .12 * k
        x0, y0 = 70 + 260 * f, 600 - 560 * f
        p.line([(x0, y0), (x0 + 118, y0 + 8)], .1 + .03 * k, .1, w=9, color="#8A5F12")
    p.fill(f'<path d="M260 470 L660 470 L640 610 L280 610 Z" fill="#7E3B1B" stroke="{INK}" stroke-width="7"/>'
           f'<path d="M260 470 L300 400 L620 400 L660 470 Z" fill="#A0522D" stroke="{INK}" stroke-width="7"/>'
           f'<circle cx="600" cy="540" r="16" fill="#F2C35B" stroke="{INK}" stroke-width="5"/>', .3)
    for k, (x, y, r) in enumerate(((330, 300, -18), (450, 230, 12), (560, 150, -8), (680, 260, 20))):
        p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="16" data-w="{1.1 + .3 * k}" data-ph="{k}">')
        p.fill(f'<g transform="rotate({r} {x} {y})"><rect x="{x - 80}" y="{y - 40}" width="160" height="80" rx="8" fill="#9DC7C1" '
               f'stroke="{INK}" stroke-width="5"/><circle cx="{x}" cy="{y}" r="22" fill="none" stroke="{INK}" stroke-width="4"/>'
               f'<text x="{x}" y="{y + 11}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="30" fill="{INK}">$</text></g>',
               .4 + .1 * k)
        p.parts.append("</g>")
    p.parts.append('<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="8" data-w="2.4" '
                   'style="transform-box:view-box;transform-origin:700px 380px">')
    p.line([(700, 380), (700, 430)], .75, .1, w=4)
    p.fill(_tile(610, 430, 180, 100, RED, tag, 62), .78)
    p.parts.append("</g>")


def friday_bars(p, n=9, hi=5, **_):
    """A trading screen: a row of Fridays as equal grey bars (no data, an illustration), one marked 13 drawn only
    as a dashed outline with a red ? over it: higher or lower?"""
    p.fill(f'<rect x="10" y="20" width="780" height="600" rx="30" fill="{INK}"/>'
           f'<rect x="34" y="44" width="732" height="552" rx="16" fill="#1E2A2A"/>', 0)
    for k in range(5):
        p.line([(60, 120 + 100 * k), (740, 120 + 100 * k)], .05, .2, color="#35504D", w=2)
    p.text(80, 98, "FRIDAYS", .1, size=34, weight=700, color="#9DC7C1", anchor="start")
    bw = 60
    for k in range(n):
        x = 70 + k * 76
        if k == hi:
            p.line([(x, 520), (x, 250), (x + bw, 250), (x + bw, 520)], .5, .25, color=RED, w=5, dash="12 9")
            p.text(x + bw / 2, 225, "?", .8, size=110, serif=True, weight=700, color=RED, fx="pop")
            p.box(x - 8, 532, bw + 16, 50, RED, .55, rx=10)
            p.text(x + bw / 2, 568, "13", .58, size=34, serif=True, weight=700, color="#fff")
        else:
            p.box(x, 340, bw, 180, "#6F8F8B", .1 + .04 * k, rx=6, fx="growY")
            p.text(x + bw / 2, 568, "FRI", .15 + .04 * k, size=24, weight=700, color="#9DC7C1")
    p.line([(60, 520), (740, 520)], .05, .2, color="#9DC7C1", w=4)


SCENES.update({f.__name__: f for f in (fri13_page, year_grid, road_cat, ladder_wallet, friday_bars)})
