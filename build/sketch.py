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
  13 Nov, long video (Newton and the South Sea Bubble): price_path(points, marks, upto, counter), apple_fall(label),
  crowd_rush(n, target), empty_pockets(label), hospital(label), scroll(title, lines, seal), letter(date, sign, hi_line)
  13 Nov (Friday the 13th Short): fri13_page(), year_grid(year), road_cat(), ladder_wallet(tag), friday_bars(n, hi);
  cat_svg(x, y, s) draws a sitting black cat for floaters and the close
  13 Nov (Levels #12, terminal value): tv_timeline(n), two_ways(left, right), exit_stack(ebitda, mult, total),
  discount_shrink(later, tv, fc, share)
  13 Nov (Friday the 13th myth Short, story engine): trader(p, x, y, s, pose) the recurring character (stand, worry,
  point, cheer, shrug, read); myth_hook(), study_1987(), not_confirmed(), uk_years(start, end), higher_bar(), myth_stamp()
  14 Nov (first cash machine Short): trader(walk=(t0, t1), turn=[(t, dir)]) walks and turns his head; bank_closed(walk_s),
  bath_idea(swap_at), cash_machine(walk_s, at_s), radio_cheque(at_s), ten_pounds(at_s), pin_six(cut_s), four_dots(),
  pin_asks(); _banknote() draws a generic note
"""

import html as H
import math
import random
import re

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
    out = p.svg()
    SOUND_LOG.append(dict(name=name, t0=t0, events=actions(out, name)))
    if HELD_LIFE and not opts.get("still"):
        out = held_life(p, out, seed)
    return out


# 17 Nov (YouTube #11, the 16 Nov next improvement): a held-life layer. Once a drawing has finished drawing itself
# it used to freeze, and the 16 Nov film had static runs of 3 to 5 s on drawn beats. Now every part of a finished
# drawing "boils" like hand-drawn animation (each stroke and fill re-drawn a little off its place, 6 times a
# second, independently), and the whole drawing sways about its base by a fraction of a degree. Both ease in over
# half a second after the drawing's last part lands, so nothing moves while it is still being drawn, and both are
# small (BOIL px in the drawing's 800 x 640 box, SWAY degrees). No sound: ambient life is silent (actions() runs on
# the drawing before the layer is added). Off with youtube ep["held_life"] = False (an exact re-render of #1 to #10).
HELD_LIFE = True
BOIL, SWAY, BOIL_FPS = 1.8, .45, 6


def held_life(p, svg, seed=1):
    ends = [float(a) + float(d) for a, d in re.findall(r'data-at="([0-9.\-]+)" data-d="([0-9.]+)"', svg)]
    if not ends:
        return svg
    end = round(max(ends) + .15, 3)
    head, body = svg.split(">", 1)
    body = body[: -len("</svg>")]
    parts = "".join(f'<g class="a" data-fx="boil" data-at="{end}" data-d=".5" data-amp="{BOIL}" data-seed="{(seed * 31 + k) % 997}" '
                    f'data-fps="{BOIL_FPS}">{part}</g>' for k, part in enumerate(p.parts)) if body == "".join(p.parts) else body
    return (head + f'><g class="a" data-fx="sway" data-at="{end}" data-d=".6" data-amp="{SWAY}" data-w="1.3" data-ph="{seed % 7}" '
            f'style="transform-box:fill-box;transform-origin:50% 100%">{parts}</g></svg>')


# 16 Nov (YouTube #10): what each drawing does and when, so the drawn beats get a sound on each action instead of one
# generic pop per visual (audio-standard.md 5). Read off the finished SVG, so drawings that append their parts
# directly are covered as well as Pen.line and Pen.fill. youtube.scenes() reads SOUND_LOG after building a visual.
SOUND_LOG = []
PAPERS = {"document", "newspaper", "letter", "scroll", "receipt", "ledger", "book", "poster", "credit_report", "perpetual",
          "quote_card", "calendar", "fri13_page", "year_grid"}
_ACT = re.compile(r'<g class="a" data-fx="([a-zA-Z]+)" data-at="([0-9.\-]+)" data-d="([0-9.]+)"([^>]*)>')
_COIN = re.compile(r'radialGradient id="coin|#E8B04A|#E2B43C|#F6C19A|#E0A93B|#B9C1C7')
_PRIORITY = {"stamp": 0, "clink": 1, "paper": 1, "hit": 1, "tock": 2, "softpop": 3, "marker": 4}


def actions(svg, name=""):
    """[(sound, seconds, gain or None, kwargs)] for one drawing: a stamp lands, a coin lands, a bar finishes growing,
    a shape pops in, a marker stroke draws (strokes close together share one sound). Ambient motion (swing, float,
    ripple, fades, camera) makes no sound. Thinned so a drawing never chatters: one per 0.12 s at most, the
    stronger sound kept, at most 3 marker passages and 3 generic pops."""
    ev, strokes = [], []
    marks = list(_ACT.finditer(svg))
    for i, m in enumerate(marks):
        fx, at, d = m.group(1), float(m.group(2)), float(m.group(3))
        body = svg[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(svg)]
        coin = bool(_COIN.search(body))
        if fx == "stamp":
            ev.append(("stamp", at + d * .85))
        elif fx == "coinflip":
            ev.append(("clink", at + d))
        elif fx in ("pop", "scale", "flipin", "slide", "move") and coin:
            ev.append(("clink", at + d * (.8 if fx != "slide" else 1)))
        elif fx in ("growY", "growYdown", "scaleY", "growX"):
            ev.append(("tock", at + d))
        elif fx in ("pop", "scale", "flipin", "slide", "move"):
            ev.append(("softpop", at + d * (.5 if fx == "pop" else 1)))
        elif fx == "press":
            ev.append(("hit", at + d * .5))
        elif fx in ("draw", "strike"):
            strokes.append((at, at + d))
    strokes.sort()
    runs = []
    for a, b in strokes:                                    # strokes within 0.3 s of each other are one passage
        if runs and a <= runs[-1][1] + .3:
            runs[-1][1] = max(runs[-1][1], b)
        else:
            runs.append([a, b])
    runs = sorted(sorted(runs, key=lambda r: r[0] - r[1])[:3])
    ev += [("marker", a, None, dict(sec=min(b - a, 1.0))) for a, b in runs]
    if name in PAPERS and (ev or strokes):
        ev.append(("paper", min(e[1] for e in ev) if ev else strokes[0][0]))
    ev = [e if len(e) == 4 else (e[0], round(e[1], 3), None, {}) for e in ev]
    ev.sort(key=lambda e: (_PRIORITY[e[0]], e[1]))
    kept, pops = [], 0
    for e in ev:                                            # stronger sounds first, then fill the gaps
        if e[0] != "marker" and any(abs(e[1] - k[1]) < .12 and k[0] != "marker" for k in kept):
            continue
        if e[0] == "softpop":
            if pops >= 3:
                continue
            pops += 1
        kept.append(e)
    return sorted(kept, key=lambda e: e[1])


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


def receipt(p, total="$4.97", circle=-1, coin_vals=("5\u00a2", "1\u00a2"), **_):
    """A shop receipt printing out, the total at the bottom; circle=k rings the k-th character of the total in red."""
    zig = " ".join(f"L{170 + 20 * i} {612 if i % 2 else 600}" for i in range(1, 24))
    p.parts.append(f'<g class="a" data-fx="growYdown" data-at="{p.at(.0)}" data-d="{.5 * p.dur:.2f}">'
                   f'<path d="M170 40 H630 V600 {zig} L170 600 Z" fill="#fff" stroke="{GREY}" stroke-width="3"/></g>')
    for i, w_ in enumerate((300, 220, 260, 190)):
        p.box(215, 120 + 62 * i, w_, 20, "#DCD7CF", .12 + .06 * i, rx=10, fx="growX")
        p.box(500, 120 + 62 * i, 85, 20, "#DCD7CF", .14 + .06 * i, rx=10, fx="growX")
    p.line([(210, 400), (590, 400)], .38, .12, color=GREY, w=4, dash="10 10")
    p.text(215, 490, "TOTAL", .45, size=44, anchor="start", weight=700)
    # 16 Nov (#10 contact sheet): a long total ("1.8bn lb") ran into TOTAL; the size now fits the 230 px it has
    fs = min(84, int(230 / (.56 * max(len(total), 1))))
    p.text(590, 495, total, .5, size=fs, anchor="end", serif=True, weight=700, color=INK)
    if circle >= 0:
        cx = 590 - (len(total) - 1 - circle) * fs / 2 - fs / 4
        p.circle(cx, 467, 46, .65, .3, color=RED, w=7)
    coin(p, 690, 520, 62, coin_vals[0], "nickel", .55, fx="pop")          # coin_vals=("", ""): no prices on a prop
    coin(p, 110, 540, 56, coin_vals[1], "copper", .6, fx="pop")
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

def newspaper(p, headline="OVER-SUBSCRIBED", sub="AND STILL THEY POUR IN", date="1914", stamp="", masthead="THE DAILY LEDGER", **_):
    """A folded broadsheet: a made-up masthead bar, a big headline, columns of grey lines; stamp= slams a red
    verdict across it (e.g. FALSE)."""
    p.fill(f'<rect x="90" y="70" width="620" height="500" rx="8" fill="#fff" stroke="{INK}" stroke-width="6" transform="rotate(-2 400 320)"/>', 0)
    p.box(120, 95, 560, 54, INK, .06, rx=4)
    # 15 Nov (#9): masthead= names the real paper when the label cites it (a made-up masthead beside "Boston Post"
    # contradicted the label); plain type, no logo
    p.text(400, 134, masthead, .1, size=34, serif=True, weight=700, color="#fff")
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
# ---- 13 Nov, long video (Newton and the South Sea Bubble): the 1720 price path with the moments marked,
# a falling apple, a crowd running in, pockets turned out, a hospital, a sealed parchment and a letter with a
# quill. Generic shapes of our own: no portrait of anyone, no company crest.

SOUTH_SEA_1720 = (("JAN", 128), ("MAR", 330), ("APR", 350), ("MAY", 550), ("JUN", 890), ("AUG", 1000), ("SEP", 150), ("DEC", 100))


def price_path(p, points=SOUTH_SEA_1720, marks=(), upto=None, unit="£", note="APPROX. PRICE, 1720", counter=True, **_):
    """A price chart in red marker drawn month by month, with a counter riding the last point. marks=[(index,
    label, colour)] pins a flag on a point ("SOLD" in teal, "BOUGHT" in red). upto=k draws only the first k
    points, the rest dashed in grey as what is still to come."""
    n = len(points)
    upto = n if upto is None else upto
    top = max(v for _, v in points)
    xy = [(110 + i * 630 / (n - 1), 520 - 400 * v / top) for i, (_, v) in enumerate(points)]
    p.line([(80, 60), (80, 540), (770, 540)], 0, .25, w=6)
    p.text(80, 40, note, .05, size=28, weight=700, color=GREY, anchor="start")
    for frac_v in (.25, .5, .75, 1):
        y = 520 - 400 * frac_v
        p.line([(80, y), (770, y)], .05, .2, color="#D9D4CC", w=2)
        p.text(70, y + 10, f"{unit}{int(top * frac_v):,}", .08, size=22, color=GREY, anchor="end", weight=600)
    for i, (m, _) in enumerate(points):
        p.text(xy[i][0], 580, m, .1 + .02 * i, size=26, weight=700, color=INK if i < upto else GREY)
    seg = .55 / max(upto - 1, 1)
    for i in range(min(upto, n) - 1):
        p.line([xy[i], xy[i + 1]], .15 + i * seg, seg * 1.05, color=RED, w=12, j=1.5)
    if upto < n:
        p.line(xy[upto - 1:], .7, .2, color=GREY, w=6, dash="4 18")
        p.text(xy[-1][0], xy[-1][1] - 40, "?", .8, size=80, serif=True, weight=700, color=RED, fx="pop")
    last = xy[upto - 1]
    if counter:                                                  # off on a thumbnail, where it would freeze on the first value
        p.parts.append(_count(last[0], last[1] - 34, points[0][1], points[upto - 1][1], p.at(.15), round(.55 * p.dur, 2),
                              size=40, color=INK, pre=unit))
    for idx, label, col in marks:
        x, y = xy[idx]
        at = .2 + idx * seg
        p.line([(x, y), (x, y + 70 if y < 300 else y - 90)], at, .12, color=col, w=5)
        fy = y + 70 if y < 300 else y - 150
        p.fill(_tile(x - 85, fy, 170, 60, col, label, 32, rx=12, stroke=col), at + .05)
        p.fill(f'<circle cx="{x}" cy="{y}" r="15" fill="{col}" stroke="#fff" stroke-width="5"/>', at)


def apple_fall(p, label="", **_):
    """A tree branch; an apple drops along a dotted arc, bounces once on the ground and settles: gravity, the
    thing he could calculate."""
    p.line([(60, 90), (330, 110), (470, 80)], 0, .3, color="#7A5230", w=14)
    for x, y in ((150, 70), (250, 120), (380, 70), (440, 120)):
        p.fill(f'<ellipse cx="{x}" cy="{y}" rx="46" ry="24" fill="{TEAL}" transform="rotate(-20 {x} {y})"/>', .15)
    p.line([(300, 130), (330, 260), (360, 400), (380, 520)], .35, .25, color=GREY, w=4, dash="6 16")
    apple = (f'<g><circle cx="380" cy="500" r="52" fill="{RED}" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M380 452 Q384 430 396 420" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
             f'<ellipse cx="410" cy="430" rx="22" ry="11" fill="{TEAL}"/><circle cx="360" cy="482" r="10" fill="#fff" opacity=".8"/></g>')
    kf = [[p.at(.3), -80, -390, .9, 1, -30], [p.at(.55), 0, 0, 1, 1, 0], [p.at(.62), 10, -60, 1, 1, 12],
          [p.at(.7), 14, 0, 1, 1, 18], [p.at(1), 14, 0, 1, 1, 18]]
    p.parts.append(f"<g class=\"a\" data-fx=\"kf\" data-at=\"{p.at(.3)}\" data-d=\"{.7 * p.dur:.2f}\" data-kf='{_json(kf)}' "
                   f'style="transform-box:fill-box;transform-origin:center">{apple}</g>')
    p.line([(60, 560), (760, 560)], 0, .3, w=6)
    if label:
        p.fill(_tile(520, 220, 240, 80, "#F2C35B", label, 40, color=INK, rx=16), .75)


def _json(x):
    import json
    return json.dumps(x)


def crowd_rush(p, n=7, target="SOUTH SEA", **_):
    """Stick figures hurrying in from the left towards a door with a sign, one after another, the last in red
    (late, near the top): the crowd, and joining it."""
    p.rect(600, 200, 170, 360, 0, .3, w=8)
    p.rect(640, 320, 90, 240, .1, .2, w=6)
    p.fill(_tile(570, 130, 230, 66, RED, target, 30, rx=10, stroke=RED), .15)
    gap, s = (84, .95) if n <= 6 else (70, .78)
    for i in range(n):
        x = 520 - i * gap
        col = RED if i == n - 1 else None
        fr = .2 + .07 * i
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(fr)}" data-d=".6" data-x0="-140" data-x1="0" data-ease="out">')
        figure(p, x, 555, s, fr, col)
        p.line([(x - 70, 470), (x - 40, 470)], fr + .02, .1, color=GREY, w=4)
        p.line([(x - 80, 500), (x - 45, 500)], fr + .03, .1, color=GREY, w=4)
        p.parts.append("</g>")
    p.line([(20, 562), (780, 562)], 0, .3, w=6)


def empty_pockets(p, label="", **_):
    """A pair of trousers with both pockets pulled inside out, and three coins dropping out and rolling away."""
    p.line([(250, 120), (550, 120), (590, 560), (430, 560), (400, 300), (370, 560), (210, 560)], 0, .45, w=8, closed=True)
    p.line([(250, 150), (550, 150)], .1, .2, w=6)
    for side in (-1, 1):
        x = 400 + side * 150
        p.fill(f'<path d="M{x - 45} 160 Q{x} 300 {x + 45} 160 Z" fill="#fff" stroke="{INK}" stroke-width="6"/>', .4)
    for k, (x, dx) in enumerate(((260, -150), (540, 160), (300, -60))):
        cid = f'<circle cx="{x}" cy="250" r="30" fill="#E0A93B" stroke="#8A5F12" stroke-width="5"/>'
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.5 + .08 * k)}" data-d=".7" data-x0="0" data-x1="{dx}" '
                       f'data-y0="0" data-y1="320" data-r="{200 * (1 if dx > 0 else -1)}" data-ease="inout" '
                       f'style="transform-box:fill-box;transform-origin:center">{cid}</g>')
    p.line([(40, 600), (760, 600)], 0, .3, w=6)
    if label:
        p.text(400, 60, label, .8, size=44, serif=True, weight=700, color=RED, fx="pop")


def hospital(p, label="HOSPITAL", **_):
    """A plain three-storey building with rows of windows that light up and a red cross over the door."""
    p.rect(150, 170, 500, 390, 0, .35, w=8)
    p.line([(130, 170), (400, 70), (670, 170)], .1, .25, w=8)
    for r in range(3):
        for c in range(5):
            if r == 2 and c == 2:
                continue
            x, y = 185 + c * 92, 200 + r * 110
            p.box(x, y, 60, 70, "#F2C35B", .3 + .03 * (r * 5 + c), rx=6)
            p.rect(x, y, 60, 70, .3 + .03 * (r * 5 + c), .1, w=4)
    p.rect(360, 430, 80, 130, .55, .2, w=6)
    p.fill(f'<g><rect x="380" y="100" width="40" height="110" rx="6" fill="{RED}"/><rect x="345" y="135" width="110" height="40" rx="6" fill="{RED}"/></g>', .7)
    p.text(400, 610, label, .8, size=38, weight=700, color=INK)
    p.line([(60, 560), (740, 560)], 0, .3, w=6)


def scroll(p, title="AN ACT", lines=4, seal="1720", **_):
    """A parchment that unrolls downwards, lines of text writing themselves on, and a red wax seal pressed at the foot."""
    p.parts.append(f'<g class="a" data-fx="growYdown" data-at="{p.at(.05)}" data-d="{.35 * p.dur:.2f}" style="transform-box:fill-box;transform-origin:top">'
                   f'<rect x="190" y="70" width="420" height="470" rx="10" fill="#F3E6C4" stroke="{INK}" stroke-width="6"/></g>')
    p.fill(f'<rect x="170" y="45" width="460" height="46" rx="23" fill="#E2CFA0" stroke="{INK}" stroke-width="6"/>', 0)
    p.fill(f'<rect x="170" y="525" width="460" height="46" rx="23" fill="#E2CFA0" stroke="{INK}" stroke-width="6"/>', .4)
    p.text(400, 160, title, .4, size=46, serif=True, weight=700)
    for i in range(lines):
        w = 300 - 40 * (i % 2)
        p.line([(400 - w / 2, 220 + i * 52), (400 + w / 2, 220 + i * 52)], .45 + .06 * i, .12, color=GREY, w=8)
    p.fill(f'<g><circle cx="530" cy="460" r="58" fill="{RED}" stroke="#8E2209" stroke-width="6"/>'
           f'<text x="530" y="472" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="34" fill="#fff">{H.escape(seal)}</text></g>',
           .78, fx="stamp")


def letter(p, date="1724", sign="I.N.", hi_line=1, **_):
    """A handwritten letter on a desk: a date, wavy lines writing on, one underlined in red, a quill that moves
    along as it writes, and initials at the foot."""
    p.box(150, 60, 500, 520, "#fff", 0, rx=10, fx="fade")
    p.rect(150, 60, 500, 520, 0, .25, w=6)
    p.text(610, 120, date, .1, size=36, serif=True, weight=700, color=GREY, anchor="end")
    for i in range(6):
        y = 180 + i * 60
        xs = [200 + k * 25 for k in range(17 - (i == 5) * 6)]
        pts = [(x, y + 8 * math.sin(k * 1.3 + i)) for k, x in enumerate(xs)]
        p.line(pts, .15 + .09 * i, .1, color=INK, w=4, j=1)
        if i == hi_line:
            p.line([(195, y + 22), (xs[-1] + 5, y + 22)], .8, .15, color=RED, w=7)
    p.text(560, 550, sign, .72, size=44, serif=True, weight=600, color=INK)
    quill = (f'<g><path d="M0 0 Q60 -120 150 -200 Q90 -90 10 4 Z" fill="#fff" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M0 0 L150 -200" stroke="{GREY}" stroke-width="3"/></g>')
    kf = [[p.at(.15), 200, 190], [p.at(.65), 600, 480], [p.at(.72), 560, 545], [p.at(1), 640, 500]]
    kf = [[t, x, y, 1, 1, 0] for t, x, y in kf]
    p.parts.append(f"<g class=\"a\" data-fx=\"kf\" data-at=\"{p.at(.1)}\" data-d=\"{.9 * p.dur:.2f}\" data-kf='{_json(kf)}'>{quill}</g>")


SCENES.update({f.__name__: f for f in (price_path, apple_fall, crowd_rush, empty_pockets, hospital, scroll, letter)})


# ---- 13 Nov (Levels #12, terminal value). Generic blocks, a signpost and stacks of our own: no company,
# no real model. Each drawn edge to edge of the 800 x 640 canvas so it fills its box.

def tv_timeline(p, n=5, **_):
    """The DCF on one baseline: five small cash flows (the forecast), then one tall block standing for every
    year after, marked with an infinity sign. The tall block is what the Reel is about."""
    base = 540
    p.line([(20, base), (780, base)], .0, .25, w=7)
    for k in range(n):
        x, h_ = 30 + 74 * k, 110 + 10 * k
        p.fill(f'<rect x="{x}" y="{base - h_}" width="58" height="{h_}" rx="8" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>',
               .08 + .07 * k)
        p.text(x + 29, base + 50, f"Y{k + 1}", .08 + .07 * k, size=34, weight=700)
    p.line([(30, 330), (30, 310), (398, 310), (398, 330)], .45, .2, w=5, color=GREY)
    p.text(214, 290, "FORECAST", .47, size=34, weight=700, color=GREY)
    _slide(p, .55, f'<rect x="440" y="40" width="330" height="{base - 40}" rx="14" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
                   f'<text x="605" y="210" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="150" '
                   f'fill="{INK}">∞</text>'
                   f'<text x="605" y="330" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="42" '
                   f'fill="{INK}">TERMINAL</text>'
                   f'<text x="605" y="384" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="42" '
                   f'fill="{INK}">VALUE</text>', y0=-120, d=.5)
    p.text(605, base + 50, "YEAR 5 ON", .7, size=34, weight=700, color=RED)


def two_ways(p, left=("GROWTH", "FOREVER"), right=("EXIT", "MULTIPLE"), **_):
    """A signpost with two arms: perpetuity growth one way, an exit multiple the other. A small figure at the
    foot looks up."""
    p.fill(f'<rect x="385" y="70" width="30" height="530" rx="8" fill="#B8862B" stroke="{INK}" stroke-width="5"/>', .0)
    p.line([(250, 600), (550, 600)], .02, .2, w=7)
    _slide(p, .12, f'<path d="M30 175 L90 110 L392 110 L392 240 L90 240 Z" fill="{TEAL}" stroke="{INK}" stroke-width="6" '
                   f'stroke-linejoin="round"/>'
                   f'<text x="245" y="168" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="46" '
                   f'fill="#fff">{left[0]}</text>'
                   f'<text x="245" y="218" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="600" font-size="32" '
                   f'fill="#fff">{left[1]}</text>', x0=60, d=.4)
    _slide(p, .42, f'<path d="M408 290 L710 290 L770 355 L710 420 L408 420 Z" fill="{RED}" stroke="{INK}" stroke-width="6" '
                   f'stroke-linejoin="round"/>'
                   f'<text x="560" y="348" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="46" '
                   f'fill="#fff">{right[0]}</text>'
                   f'<text x="560" y="398" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="600" font-size="32" '
                   f'fill="#fff">{right[1]}</text>', x0=-60, d=.4)
    p.line([(40, 400), (110, 360), (180, 335), (260, 322), (340, 315)], .25, .4, w=6, color=TEAL, dash="14 10")
    figure(p, 190, 590, .8, .6)
    p.text(285, 470, "?", .75, size=70, serif=True, weight=700, color=RED, fx="pop")


def exit_stack(p, ebitda="$50", mult=8, total="$400", **_):
    """One EBITDA block on the left, then the same block stacked eight times on the right, one by one, and a
    tag with the total."""
    base, bh = 590, 58
    p.line([(20, base), (780, base)], .0, .2, w=7)
    p.fill(f'<rect x="40" y="{base - bh}" width="220" height="{bh}" rx="8" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>'
           f'<text x="150" y="{base - bh / 2 + 15}" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" '
           f'font-size="40" fill="#fff">{ebitda}</text>', .04)
    p.text(150, base - bh - 24, "EBITDA, YEAR 5", .08, size=30, weight=700)
    p.text(345, base - 40, f"× {mult}", .2, size=84, serif=True, weight=700, color=RED, fx="pop")
    for k in range(mult):
        y = base - bh * (k + 1)
        p.fill(f'<rect x="460" y="{y}" width="220" height="{bh}" rx="8" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>'
               f'<text x="570" y="{y + bh / 2 + 13}" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" '
               f'font-size="34" fill="#fff">{ebitda}</text>', .25 + .055 * k, fx="rise")
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="7" data-w="2.2">')
    p.fill(_ptag(250, 150, 300, total, GOLD, INK, 70, rot=-6), .78)
    p.parts.append("</g>")


def discount_shrink(p, later="$400", tv="$248", fc="$76", share="77%", **_):
    """The terminal value at year 5 (tall gold block) shrinks on its way to today, where it stands under the
    five years of forecast (a small teal block). A tag shows its share of the total."""
    base = 560
    p.line([(20, base), (780, base)], .0, .2, w=7)
    p.fill(f'<rect x="30" y="{base - 400}" width="220" height="400" rx="12" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
           f'<text x="140" y="{base - 190}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="62" '
           f'fill="{INK}">{later}</text>', .03)
    p.text(140, base + 52, "YEAR 5", .05, size=34, weight=700)
    p.line([(270, 240), (380, 210), (480, 250)], .25, .3, w=7, dash="16 12")
    p.line([(455, 222), (482, 252), (446, 268)], .4, .1, w=7)
    p.text(375, 180, "÷ 1.61", .3, size=40, weight=700, color=RED)
    p.fill(f'<rect x="530" y="{base - 248}" width="240" height="248" rx="12" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
           f'<text x="650" y="{base - 104}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="58" '
           f'fill="{INK}">{tv}</text>', .48, fx="rise")
    p.fill(f'<rect x="530" y="{base - 248 - 76}" width="240" height="76" rx="12" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
           f'<text x="650" y="{base - 248 - 24}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="44" '
           f'fill="#fff">{fc}</text>', .6, fx="rise")
    p.text(650, base + 52, "TODAY", .5, size=34, weight=700, color=TEAL)
    p.parts.append('<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="7" data-w="2.2">')
    p.fill(_ptag(390, 480, 220, share, RED, "#fff", 54, rot=-5), .78)
    p.parts.append("</g>")


SCENES.update({f.__name__: f for f in (tv_timeline, two_ways, exit_stack, discount_shrink)})


# ---- 13 Nov, long video #7 (the Panic of 1907): two institutions and their reserves, a call-money gauge, a
# library with its door locked at night, a clearing-house certificate, bankers in top hats round a table.
# Generic, stylised shapes of our own: no portrait, no crest, no real building copied.

def _hat(p, x, y, s, frac, color=None):
    """A stylised top hat sitting on a figure's head at (x, y)."""
    c = color or INK
    p.fill(f'<g><rect x="{x - 22 * s:.1f}" y="{y - 52 * s:.1f}" width="{44 * s:.1f}" height="{40 * s:.1f}" rx="3" fill="{c}"/>'
           f'<rect x="{x - 34 * s:.1f}" y="{y - 16 * s:.1f}" width="{68 * s:.1f}" height="{9 * s:.1f}" rx="4" fill="{c}"/></g>', frac, d=.25)


def trust_vs_bank(p, left="NATIONAL BANK", right="TRUST COMPANY", lres=25, rres=5, **_):
    """Two buildings side by side; under each a vault gauge fills to its cash reserve (25% against 5% of
    deposits), with the percentage counting up. The trust's thin red line is the point."""
    for k, (x, lab, res, col) in enumerate(((60, left, lres, TEAL), (430, right, rres, RED))):
        f0 = .05 + .3 * k
        p.line([(x, 150), (x + 155, 70), (x + 310, 150)], f0, .2, w=7)
        p.rect(x + 10, 150, 290, 130, f0 + .03, .2, w=7)
        for c in range(4):
            p.line([(x + 50 + c * 70, 165), (x + 50 + c * 70, 265)], f0 + .06 + .02 * c, .1, w=8)
        p.text(x + 155, 310, lab, f0 + .1, size=24, weight=700)
        # the vault gauge: deposits as a tall outline, reserves as the filled part
        p.rect(x + 95, 350, 120, 230, f0 + .12, .2, w=6)
        h = 230 * res / 100
        p.parts.append(f'<g class="a" data-fx="growY" data-at="{p.at(f0 + .2)}" data-d=".6">'
                       f'<rect x="{x + 101}" y="{580 - h:.1f}" width="108" height="{h - 6:.1f}" fill="{col}"/></g>')
        p.parts.append(_count(x + 155, 480, 0, res, p.at(f0 + .2), .6, size=50, color=INK, suf="%"))
        p.text(x + 155, 620, "CASH RESERVE", f0 + .25, size=22, weight=700, color=GREY)


def rate_gauge(p, steps=((9.5, "OCT 21"), (70, "OCT 22"), (100, "OCT 24")), label="CALL MONEY, A YEAR", still=False, **_):
    """A big dial whose needle swings up step by step to each interest rate, the rate counting on the face and
    a date tile for each step; the last step in red."""
    cx, cy, r = 400, 420, 300
    pts = [(cx + r * math.cos(math.pi * (1 + i / 30)), cy + r * math.sin(math.pi * (1 + i / 30))) for i in range(31)]
    p.line(pts, 0, .3, w=10)
    for i in range(0, 11):
        a = math.pi * (1 + i / 10)
        p.line([(cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a)), (cx + r * math.cos(a), cy + r * math.sin(a))], .1, .05, w=5)
        if i % 5 == 0:
            p.text(cx + (r - 70) * math.cos(a), cy + (r - 70) * math.sin(a) + 12, f"{i * 10}%", .15, size=30, weight=700, color=GREY)
    p.fill(f'<path d="M{cx + (r - 40) * math.cos(math.pi * 1.7):.0f} {cy + (r - 40) * math.sin(math.pi * 1.7):.0f} A {r - 40} {r - 40} 0 0 1 {cx + r - 40} {cy}" '
           f'fill="none" stroke="{RED}" stroke-width="22" opacity=".35"/>', .2)
    n = len(steps)
    kf, prev = [], 0
    for k, (v, _) in enumerate(steps):
        t = p.at(.25 + .6 * k / n)
        kf += [[t, 0, 0, 1, 1, -90 + 180 * prev / 100], [round(t + .5, 3), 0, 0, 1, 1, -90 + 180 * v / 100]]
        prev = v
    needle = (f'<g><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r + 60}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
              f'<circle cx="{cx}" cy="{cy}" r="22" fill="{INK}"/></g>')
    if still:                                             # a thumbnail runs no motion: the needle at the last step
        p.parts.append(f'<g transform="rotate({-90 + 180 * steps[-1][0] / 100} {cx} {cy})">{needle}</g>')
    else:
        p.parts.append(f"<g class=\"a\" data-fx=\"kf\" data-at=\"{kf[0][0]}\" data-d=\"{p.dur:.2f}\" data-kf='{_json(kf)}' "
                       f'style="transform-box:view-box;transform-origin:{cx}px {cy}px">{needle}</g>')
    for k, (v, date) in enumerate(steps):
        f = .25 + .6 * k / n
        col = RED if k == n - 1 else INK
        if still:
            if k == n - 1:
                p.text(cx, cy + 110, f"{v:g}%", 0, size=72, color=col, serif=True, weight=700)
            p.fill(_tile(70 + k * 230, 560, 200, 60, col if k == n - 1 else "#fff", date, 30, color="#fff" if k == n - 1 else INK, rx=12), 0)
            continue
        end = p.at(.25 + .6 * (k + 1) / n) if k < n - 1 else p.t0 + p.dur + 5
        p.parts.append(f'<g class="a" data-fx="life" data-at="{p.at(f)}" data-d="{end - p.at(f):.2f}" data-fi=".05" data-fo=".05">'
                       + _count(cx, cy + 110, steps[k - 1][0] if k else 0, v, p.at(f), .5, size=72, color=col, suf="%", dec=1 if v % 1 else 0)
                       + "</g>")
        p.fill(_tile(70 + k * 230, 560, 200, 60, col if k == n - 1 else "#fff", date, 30, color="#fff" if k == n - 1 else INK, rx=12), f + .05)
    p.text(cx, 40, label, 0, size=30, weight=700, color=GREY)


def library_lock(p, clock="4:00", n=5, still=False, **_):
    """A panelled library at night: tall bookshelves, a lamp, a table with stylised bankers in top hats, a door
    on the right whose key turns in the lock, and a clock reading the hour."""
    p.box(0, 0, 800, 640, "#22303A", 0, rx=0, fx="fade")
    for k in range(3):                                    # bookshelves on the back wall
        x = 30 + k * 170
        p.rect(x, 60, 150, 380, .05 + .03 * k, .2, color="#C9A66B", w=6)
        for r in range(5):
            y = 90 + r * 70
            p.line([(x + 6, y + 50), (x + 144, y + 50)], .1 + .02 * r, .1, color="#C9A66B", w=4)
            for b in range(6):
                col = ("#D93A12", "#0F766E", "#F2C35B", "#E9E4DA")[(b + r + k) % 4]
                p.box(x + 12 + b * 22, y + 8 + (b % 3) * 4, 16, 40 - (b % 3) * 4, col, .12 + .01 * (r * 6 + b), rx=2)
    p.fill(f'<g><circle cx="300" cy="300" r="190" fill="#F2C35B" opacity=".18"/><path d="M285 200 L315 200 L330 235 L270 235 Z" fill="#F2C35B"/>'
           f'<line x1="300" y1="235" x2="300" y2="400" stroke="#C9A66B" stroke-width="6"/></g>', .2)   # the lamp's pool of light
    for i in range(n):                                    # the bankers round the table, behind it
        x = 150 + i * 85
        figure(p, x, 600, .7, .3 + .05 * i, "#E9E4DA")
        _hat(p, x, 600 - 150 * .7 - 18, .7, .32 + .05 * i, "#E9E4DA")
    p.box(100, 540, 440, 34, "#7A5230", .45, rx=6)
    p.rect(600, 160, 150, 400, .2, .25, color="#E9E4DA", w=7)       # the door
    p.fill(f'<circle cx="625" cy="370" r="10" fill="#F2C35B"/>', .3)
    key = (f'<g><circle cx="0" cy="0" r="18" fill="none" stroke="#F2C35B" stroke-width="8"/>'
           f'<path d="M18 0 H64 M50 0 V14 M62 0 V12" stroke="#F2C35B" stroke-width="8" stroke-linecap="round"/></g>')
    kf = [[p.at(.55), 700, 330, 1, 1, 0], [p.at(.62), 650, 370, 1, 1, 0], [p.at(.72), 650, 370, 1, 1, 90]]
    if still:                                             # a thumbnail runs no motion: the key turned in the lock
        p.parts.append(f'<g transform="translate(650 370) rotate(90)">{key}</g>')
    else:
        p.parts.append(f"<g class=\"a\" data-fx=\"kf\" data-at=\"{p.at(.55)}\" data-d=\"{.3 * p.dur:.2f}\" data-kf='{_json(kf)}'>{key}</g>")
    p.fill(_tile(610, 80, 130, 60, RED, "LOCKED", 26, rx=10, stroke=RED), .75, fx="stamp")
    p.fill(f'<g><circle cx="460" cy="120" r="48" fill="#E9E4DA"/><text x="460" y="132" text-anchor="middle" font-family="\'Serif\',serif" '
           f'font-weight="700" font-size="30" fill="{INK}">{H.escape(clock)}</text></g>', .8)


def scrip(p, amount="$5,000", label="CLEARING HOUSE", sub="LOAN CERTIFICATE", **_):
    """A certificate sliding in, its border drawing on, the amount counting, and a band 'IN PLACE OF CASH'."""
    body = (f'<g><rect x="90" y="120" width="620" height="360" rx="14" fill="#F3E6C4" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="115" y="145" width="570" height="310" rx="8" fill="none" stroke="#B8862B" stroke-width="4" stroke-dasharray="14 8"/>'
            f'<text x="400" y="215" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="44" fill="{INK}">{H.escape(label)}</text>'
            f'<text x="400" y="260" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="28" fill="{GREY}">{H.escape(sub)}</text>'
            f'<text x="400" y="370" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="92" fill="{TEAL}">{H.escape(amount)}</text>'
            f'<circle cx="610" cy="410" r="40" fill="{RED}" opacity=".9"/></g>')
    _slide(p, .05, body, x0=-700, d=.5)
    p.fill(_tile(160, 520, 480, 70, INK, "IN PLACE OF CASH", 38, color="#F2C35B", rx=14), .6, fx="stamp")


def bankers_table(p, n=4, pledge=True, **_):
    """Stylised bankers in top hats standing behind a table, each signing in turn: a sheet on the table gets a
    teal signature and a tick; the one at the head of the table in red."""
    for i in range(n):
        x = 160 + i * (480 / max(n - 1, 1))
        col = RED if i == 0 else None
        figure(p, x, 520, .8, .05 + .06 * i, col)
        _hat(p, x, 520 - 150 * .8 - 20, .8, .08 + .06 * i, col)
    p.box(90, 470, 620, 40, "#7A5230", .3, rx=8)
    p.line([(130, 510), (130, 610)], .32, .1, color="#7A5230", w=10)
    p.line([(670, 510), (670, 610)], .32, .1, color="#7A5230", w=10)
    if pledge:
        for i in range(n):
            x = 160 + i * (480 / max(n - 1, 1))
            f = .4 + .12 * i
            p.box(x - 48, 474, 96, 32, "#fff", f, rx=4)
            p.line([(x - 34, 496), (x - 12, 482), (x + 10, 500), (x + 32, 484)], f + .04, .12, color=TEAL, w=5)
            p.text(x, 640, "SIGNED", f + .08, size=26, weight=700, color=TEAL)


SCENES.update({f.__name__: f for f in (trust_vs_bank, rate_gauge, library_lock, scrip, bankers_table)})
# ---- 13 Nov (Friday the 13th myth Short, Format E): one recurring character, "the trader", drawn the same way
# in every scene (navy suit, red tie, round head), in five poses, plus the scenes he acts in. Our own design.

SUIT, TIE, SKIN = "#22324A", RED, "#F2D2B6"


def trader(p, x, y, s=1.0, pose="stand", frac=0.0, look=1, walk=None, turn=()):
    """The trader standing with his feet at (x, y). pose: stand, worry (hands on head), point (right arm out to
    look's side), cheer (both arms up), shrug (palms up), read (holding a sheet). His arms swing a little.
    14 Nov: walk=(t0, t1) in scene seconds gives him a walk cycle: each leg swings from its hip in opposite phase,
    the arms swing against the legs and the bob quickens, easing in and out at both ends (motion.py swing with
    data-gate). The caller moves him across the scene over the same window. turn=[(t, d), ...] turns his head:
    at t the face (eyes, mouth, hair parting) slides d (-1 left, 0 to the viewer, 1 right) over 0.35 s."""
    S = lambda v: v * s
    shoes = lambda fx_, fy: f'<ellipse cx="{fx_}" cy="{fy + S(4)}" rx="{S(22)}" ry="{S(9)}" fill="{INK}"/>'
    if walk:
        w0, w1 = walk
        legs = ""
        for k, sx in enumerate((-1, 1)):
            hip = (x + sx * S(14), y - S(120))
            legs += (f'<g class="a" data-fx="swing" data-gate="1" data-at="{w0:.2f}" data-d="{w1 - w0:.2f}" data-amp="20" '
                     f'data-w="8" data-ph="{k * 3.1416:.4f}" style="transform-box:view-box;transform-origin:{hip[0]:.1f}px {hip[1]:.1f}px">'
                     f'<path d="M{hip[0]:.1f} {hip[1]:.1f} L{x + sx * S(20):.1f} {y}" fill="none" stroke="{INK}" stroke-width="{S(16):.1f}" '
                     f'stroke-linecap="round"/>{shoes(x + sx * S(20) + look * S(10), y)}</g>')
        legs += (f'<path d="M{x - S(14)} {y - S(120)} L{x + S(14)} {y - S(120)}" stroke="{INK}" stroke-width="{S(16):.1f}" '
                 f'stroke-linecap="round"/>')
    else:
        legs = (f'<path d="M{x - S(26)} {y} L{x - S(14)} {y - S(120)} L{x + S(14)} {y - S(120)} L{x + S(26)} {y}" fill="none" '
                f'stroke="{INK}" stroke-width="{S(16):.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
                + shoes(x - S(30), y) + shoes(x + S(30), y))
    body = (f'<path d="M{x - S(46)} {y - S(118)} Q{x - S(50)} {y - S(250)} {x} {y - S(258)} Q{x + S(50)} {y - S(250)} '
            f'{x + S(46)} {y - S(118)} Z" fill="{SUIT}" stroke="{INK}" stroke-width="{S(5):.1f}"/>'
            f'<path d="M{x - S(16)} {y - S(254)} L{x} {y - S(226)} L{x + S(16)} {y - S(254)} Z" fill="#fff"/>'
            f'<path d="M{x} {y - S(236)} L{x - S(10)} {y - S(200)} L{x} {y - S(150)} L{x + S(10)} {y - S(200)} Z" fill="{TIE}"/>')
    skull = f'<circle cx="{x}" cy="{y - S(310)}" r="{S(50)}" fill="{SKIN}" stroke="{INK}" stroke-width="{S(5):.1f}"/>'
    hair = (f'<path d="M{x - S(50)} {y - S(318)} Q{x - S(40)} {y - S(372)} {x + S(6)} {y - S(364)} Q{x + S(46)} {y - S(360)} '
            f'{x + S(50)} {y - S(320)} Q{x + S(20)} {y - S(342)} {x - S(50)} {y - S(318)} Z" fill="{INK}"/>')
    eyes = f'<circle cx="{x - S(17)}" cy="{y - S(306)}" r="{S(6)}" fill="{INK}"/><circle cx="{x + S(17)}" cy="{y - S(306)}" r="{S(6)}" fill="{INK}"/>'
    mouth = {"worry": f'<path d="M{x - S(14)} {y - S(278)} Q{x} {y - S(290)} {x + S(14)} {y - S(278)}" fill="none" stroke="{INK}" stroke-width="{S(4):.1f}" stroke-linecap="round"/>',
             "shrug": f'<path d="M{x - S(14)} {y - S(282)} H{x + S(14)}" stroke="{INK}" stroke-width="{S(4):.1f}" stroke-linecap="round"/>'}.get(
        pose, f'<path d="M{x - S(16)} {y - S(286)} Q{x} {y - S(270)} {x + S(16)} {y - S(286)}" fill="none" stroke="{INK}" stroke-width="{S(4):.1f}" stroke-linecap="round"/>')
    face = eyes + mouth
    if turn or walk:
        # The face sits on its own layer so it can slide round the head; a walker looks where he is going.
        d0 = look if walk else 0
        keys, cur = [[0, d0 * S(13), 0, 1, 1]], d0
        for t, d in sorted(turn):
            keys += [[round(t, 3), cur * S(13), 0, 1, 1], [round(t + .35, 3), d * S(13), 0, 1, 1]]
            cur = d
        kf = H.escape(_json([[round(v, 2) for v in k] for k in keys]))
        face = (f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{kf}">'
                f'{eyes}{mouth}</g>')
        hair = (f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json([[k[0], round(k[1] * .5, 2), 0, 1, 1] for k in keys]))}">'
                f'{hair}</g>')
    head = skull + hair + face
    sh_l, sh_r = (x - S(42), y - S(236)), (x + S(42), y - S(236))
    hands = {"stand": ((x - S(62), y - S(130)), (x + S(62), y - S(130))),
             "worry": ((x - S(40), y - S(352)), (x + S(40), y - S(352))),
             "point": ((x - S(62), y - S(130)), (x + look * S(150), y - S(270))),
             "cheer": ((x - S(96), y - S(380)), (x + S(96), y - S(380))),
             "shrug": ((x - S(120), y - S(250)), (x + S(120), y - S(250))),
             "read": ((x - S(40), y - S(190)), (x + S(40), y - S(190)))}[pose]
    def arm(sh, hd, k):
        ex, ey = (sh[0] + hd[0]) / 2 + (-1 if k == 0 else 1) * S(22), (sh[1] + hd[1]) / 2 + S(18)
        return (f'<path d="M{sh[0]:.1f} {sh[1]:.1f} Q{ex:.1f} {ey:.1f} {hd[0]:.1f} {hd[1]:.1f}" fill="none" stroke="{SUIT}" '
                f'stroke-width="{S(20):.1f}" stroke-linecap="round"/><circle cx="{hd[0]:.1f}" cy="{hd[1]:.1f}" r="{S(13):.1f}" fill="{SKIN}" '
                f'stroke="{INK}" stroke-width="{S(4):.1f}"/>')
    def walking_arm(sh, hd, k):
        if not walk:
            return arm(sh, hd, k)
        return (f'<g class="a" data-fx="swing" data-gate="1" data-at="{walk[0]:.2f}" data-d="{walk[1] - walk[0]:.2f}" data-amp="16" '
                f'data-w="8" data-ph="{(1 - k) * 3.1416:.4f}" style="transform-box:view-box;transform-origin:{sh[0]:.1f}px {sh[1]:.1f}px">'
                f'{arm(sh, hd, k)}</g>')
    sheet = (f'<rect x="{x - S(56)}" y="{y - S(250)}" width="{S(112)}" height="{S(80)}" rx="{S(6)}" fill="#fff" stroke="{INK}" '
             f'stroke-width="{S(4):.1f}" transform="rotate(-6 {x} {y - S(210)})"/>') if pose == "read" else ""
    # the right arm swings gently on its shoulder; the whole figure bobs (a quicker, smaller bob while walking)
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="{S(5):.1f}" data-w="1.3">')
    if walk:
        p.parts.append(f'<g class="a" data-fx="swing" data-gate="1" data-at="{walk[0]:.2f}" data-d="{walk[1] - walk[0]:.2f}" '
                       f'data-amp="1.6" data-w="16" style="transform-box:view-box;transform-origin:{x}px {y}px">')
    p.fill(legs + body + walking_arm(sh_l, hands[0], 0) + head + sheet, frac, .35)
    p.parts.append(f'<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="{4 if pose in ("point", "cheer") else 2}" '
                   f'data-w="2.2" style="transform-box:view-box;transform-origin:{sh_r[0]:.0f}px {sh_r[1]:.0f}px">')
    p.fill(walking_arm(sh_r, hands[1], 1), frac + .03, .3)
    p.parts.append("</g></g>" + ("</g>" if walk else ""))


def myth_hook(p, **_):
    """The myth: the FRIDAY 13 page, the trader clutching his head, a red arrow diving past his phone screen."""
    p.fill(_page(20, 60, 330, 400, "FRIDAY", "13", RED, rot=-6, size=240), 0, .4)
    p.parts.append('<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="3" data-w="1.1" '
                   'style="transform-box:view-box;transform-origin:470px 200px">')
    p.fill(f'<rect x="370" y="60" width="200" height="290" rx="26" fill="{INK}"/><rect x="384" y="82" width="172" height="240" rx="12" fill="#1E2A2A"/>', .2)
    p.line([(400, 130), (440, 170), (470, 150), (540, 300)], .35, .4, color=RED, w=10)
    p.line([(510, 298), (542, 304), (544, 270)], .7, .1, color=RED, w=10)
    p.parts.append("</g>")
    trader(p, 690, 630, 1.0, "worry", .25)
    p.text(770, 230, "!", .8, size=110, serif=True, weight=700, color=RED, fx="pop")


def study_1987(p, **_):
    """1987: a paper whose two bars say Friday the 13th was lower (the study's direction, not its numbers), the trader reading it."""
    p.fill(f'<rect x="40" y="30" width="430" height="560" rx="14" fill="#fff" stroke="{INK}" stroke-width="7" transform="rotate(-3 255 310)"/>', 0)
    p.text(255, 105, "STUDY, 1987", .1, size=44, serif=True, weight=700, color=INK)
    p.text(255, 145, "US SHARES", .14, size=26, weight=700, color=GREY)
    p.line([(90, 470), (420, 470)], .2, .2, w=5)
    p.box(120, 230, 110, 240, TEAL, .3, rx=6, fx="growY")
    p.box(280, 330, 110, 140, RED, .45, rx=6, fx="growY")
    p.text(175, 515, "OTHER FRI", .35, size=24, weight=700, color=GREY)
    p.text(335, 515, "FRI 13", .5, size=26, weight=700, color=RED)
    p.text(335, 310, "LOWER", .6, size=34, serif=True, weight=700, color=RED, fx="pop")
    p.text(255, 565, "direction only, not to scale", .7, size=20, weight=500, color=GREY)
    trader(p, 640, 630, 1.0, "point", .2, look=-1)


def not_confirmed(p, **_):
    """Other researchers check: three papers lined up, each with a big grey ?, magnifiers hovering, the 1987 paper in front."""
    for k, (x, r) in enumerate(((60, -6), (300, 2), (540, 7))):
        p.fill(f'<g transform="rotate({r} {x + 100} 300)"><rect x="{x}" y="150" width="200" height="270" rx="10" fill="#fff" '
               f'stroke="{INK}" stroke-width="6"/><rect x="{x + 30}" y="190" width="140" height="12" rx="6" fill="{GREY}"/>'
               f'<rect x="{x + 30}" y="220" width="110" height="12" rx="6" fill="{GREY}"/>'
               f'<text x="{x + 100}" y="370" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="120" '
               f'fill="{GREY}">?</text></g>', .1 + .15 * k)
        p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="22" data-w="{.7 + .2 * k}" data-ph="{k * 1.3}">')
        p.circle(x + 160, 120, 46, .5 + .1 * k, .25, color=INK, w=9)
        p.line([(x + 192, 152), (x + 230, 192)], .6 + .1 * k, .1, color=INK, w=14)
        p.parts.append("</g>")
    p.fill(f'<rect x="150" y="470" width="500" height="110" rx="20" fill="{INK}"/>'
           f'<text x="400" y="545" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="54" fill="#fff">CONFIRMED?</text>', .75)


def uk_years(p, start=1935, end=1994, **_):
    """Almost sixty years of UK shares: a long timeline with Friday the 13th marks, a year counter running from
    1935 to 1994, and the trader walking along it."""
    p.line([(30, 470), (770, 470)], 0, .4, w=8)
    for k in range(14):
        x = 50 + k * 54
        p.box(x - 4, 440, 8, 60, RED if k % 4 == 1 else GREY, .05 + .04 * k, rx=4, fx="growY")
    p.text(60, 545, str(start), .1, size=40, serif=True, weight=700, color=INK, anchor="start")
    p.text(740, 545, str(end), .7, size=40, serif=True, weight=700, color=INK, anchor="end")
    p.fill(f'<rect x="220" y="40" width="360" height="130" rx="22" fill="#fff" stroke="{INK}" stroke-width="6"/>', .05)
    p.parts.append(_count(400, 132, start, end, p.at(.1), p.dur * .75, size=88, color=RED))
    p.text(400, 220, "UK SHARES", .15, size=34, weight=700, color=GREY)
    p.parts.append(f'<g class="a" data-fx="move" data-at="{p.at(.05)}" data-d="{p.dur * .8:.2f}" data-x="-560">')
    trader(p, 690, 460, .62, "read", .05)
    p.parts.append("</g>")


def higher_bar(p, **_):
    """The result: on the trading screen, the Friday the 13th bar grows past the other Fridays, a HIGHER tag
    pops (the direction Coutts found; the heights are an illustration, not data), the trader shrugs."""
    p.fill(f'<rect x="10" y="20" width="560" height="560" rx="28" fill="{INK}"/><rect x="32" y="42" width="516" height="516" rx="14" fill="#1E2A2A"/>', 0)
    for k in range(5):
        x = 60 + k * 96
        if k == 3:
            p.box(x, 230, 64, 260, TEAL, .35, rx=6, fx="growY")
            p.box(x - 10, 500, 84, 44, RED, .3, rx=10)
            p.text(x + 32, 532, "13", .32, size=30, serif=True, weight=700, color="#fff")
        else:
            p.box(x, 320, 64, 170, "#6F8F8B", .05 + .04 * k, rx=6, fx="growY")
            p.text(x + 32, 532, "FRI", .1, size=24, weight=700, color="#9DC7C1")
    p.fill(_tile(250, 120, 290, 90, TEAL, "HIGHER", 50), .6)
    p.text(290, 610, "illustration, not to scale", .7, size=22, weight=500, color=GREY)
    trader(p, 690, 630, .95, "shrug", .4)


def myth_stamp(p, at_s=None, **_):
    """The verdict: the FRIDAY 13 page again, a red MYTH stamp slamming across it (at_s seconds in, so a thump can
    be timed to it), the trader cheering."""
    p.fill(_page(30, 70, 330, 400, "FRIDAY", "13", RED, rot=-6, size=240), 0, .3)
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{p.t0 + at_s if at_s else p.at(.25)}" data-d="0.35" data-rot="-12" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="40" y="250" width="330" height="130" rx="16" fill="#fff" fill-opacity=".9" stroke="{RED}" stroke-width="12"/>'
                   f'<text x="205" y="345" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="92" '
                   f'fill="{RED}">MYTH</text></g>')
    trader(p, 600, 630, 1.0, "cheer", .1)


SCENES.update({f.__name__: f for f in (myth_hook, study_1987, not_confirmed, uk_years, higher_bar, myth_stamp)})


def trader_asks(p, **_):
    """The close: the trader turns to the viewer, pointing, with a speech bubble holding a red ? and a 13 tile."""
    p.fill(f'<path d="M120 60 H520 Q560 60 560 100 V300 Q560 340 520 340 H330 L280 410 L290 340 H120 Q80 340 80 300 V100 '
           f'Q80 60 120 60 Z" fill="#fff" stroke="{INK}" stroke-width="7"/>', .1)
    p.fill(_tile(130, 130, 170, 120, RED, "13", 80), .3)
    p.text(430, 280, "?", .45, size=200, serif=True, weight=700, color=RED, fx="pop")
    trader(p, 640, 630, .95, "point", .05, look=-1)


SCENES.update({f.__name__: f for f in (trader_asks,)})



# ---- 14 Nov (the first cash machine Short, Format B story): the trader plays John Shepherd-Barron in an
# illustrated reconstruction, now walking (trader(walk=...)) and turning his head (trader(turn=...)). Generic
# shapes of our own: no bank logo, no real machine's design, no banknote design.

BRICK, NOTE_G = "#B5523B", "#7FB59B"


def _banknote(x, y, w_=150, h_=72, rot=0, fill=NOTE_G):
    """A generic note: a green slip with a border and a round mark, no denomination or design."""
    return (f'<g transform="rotate({rot} {x + w_ / 2} {y + h_ / 2})"><rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="8" '
            f'fill="{fill}" stroke="{INK}" stroke-width="4"/><rect x="{x + 9}" y="{y + 9}" width="{w_ - 18}" height="{h_ - 18}" '
            f'rx="5" fill="none" stroke="#2F6B55" stroke-width="3"/><circle cx="{x + w_ / 2}" cy="{y + h_ / 2}" r="{h_ * .22:.1f}" '
            f'fill="#2F6B55" fill-opacity=".55"/></g>')


def bank_closed(p, walk_s=1.5, **_):
    """The hook: a bank front with its door shut; the man walks in from the left with a cheque, stops at the
    door, a CLOSED sign flips down on the door and he turns to the viewer. SATURDAY tag; marked illustration."""
    t0 = p.t0
    p.fill(f'<path d="M372 214 L590 84 L800 214 Z" fill="#E4D6BD" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           f'<rect x="392" y="214" width="396" height="400" fill="#EFE6D6" stroke="{INK}" stroke-width="6"/>'
           f'<text x="590" y="186" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="52" '
           f'fill="{INK}" letter-spacing="6">BANK</text>', 0, .3)
    for cx in (424, 482, 698, 756):
        p.box(cx - 17, 236, 34, 372, "#D9CBB0", .02, rx=4)
    p.fill(f'<rect x="525" y="368" width="130" height="246" rx="6" fill="#5B3A29" stroke="{INK}" stroke-width="6"/>'
           f'<circle cx="636" cy="496" r="7" fill="#F2C35B"/><rect x="372" y="612" width="428" height="26" fill="#CDBE9F" '
           f'stroke="{INK}" stroke-width="5"/>', .03)
    p.fill(_tile(0, 0, 250, 74, INK, "SATURDAY", 38), .05)
    stop = t0 + walk_s
    p.parts.append(f'<g class="a" data-fx="flipin" data-at="{stop + .05:.2f}" data-d=".45" '
                   f'style="transform-box:fill-box;transform-origin:center top">'
                   f'<path d="M560 368 L590 320 L620 368" fill="none" stroke="{INK}" stroke-width="4"/>'
                   f'<rect x="505" y="368" width="170" height="68" rx="10" fill="#fff" stroke="{RED}" stroke-width="7"/>'
                   f'<text x="590" y="416" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" '
                   f'font-size="36" fill="{RED}" letter-spacing="3">CLOSED</text></g>')
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{t0 + .05:.2f}" data-d="{walk_s - .05:.2f}" data-x0="-420" data-x1="0">')
    trader(p, 320, 630, 1.05, "read", 0, look=1, walk=(t0 + .05, stop), turn=[(stop + .55, 0)])
    p.parts.append("</g>")
    p.parts.append(f'<g class="a" data-fx="pop" data-at="{stop + .7:.2f}" data-d=".4" style="transform-box:fill-box;'
                   f'transform-origin:center"><text x="420" y="250" text-anchor="middle" font-family="\'Serif\',serif" '
                   f'font-weight="700" font-size="110" fill="{RED}">!</text></g>')
    p.text(0, 636, "our illustration", .1, size=26, weight=600, color=GREY, anchor="start")


def bath_idea(p, swap_at=None, **_):
    """That evening: the man in a bath, bubbles rising, a thought bubble where a chocolate bar becomes a note."""
    p.fill(f'<path d="M20 380 H580 V420 Q580 600 470 600 H130 Q20 600 20 420 Z" fill="#fff" stroke="{INK}" stroke-width="7"/>'
           f'<rect x="70" y="596" width="24" height="40" rx="8" fill="{INK}"/><rect x="506" y="596" width="24" height="40" rx="8" fill="{INK}"/>'
           f'<path d="M560 380 V270 Q560 240 590 240 H610" fill="none" stroke="{GREY}" stroke-width="14" stroke-linecap="round"/>', 0, .3)
    # his head and knees above the foam, the head tilting as he thinks
    p.parts.append('<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="5" data-w="1.4" '
                   'style="transform-box:view-box;transform-origin:220px 380px">')
    p.fill(f'<circle cx="220" cy="300" r="62" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M158 290 Q170 226 226 234 Q276 236 282 292 Q246 266 158 290 Z" fill="{INK}"/>'
           f'<circle cx="246" cy="304" r="7" fill="{INK}"/><circle cx="268" cy="302" r="7" fill="{INK}"/>'
           f'<path d="M238 334 Q256 346 274 332" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>', .02)
    p.parts.append("</g>")
    p.fill(f'<path d="M340 380 Q380 300 430 380" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>', .04)
    p.fill(''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#9DC7C1" stroke-width="4"/>' for x, y, r in
                   ((60, 380, 34), (120, 372, 26), (300, 384, 30), (470, 376, 36), (530, 384, 24), (400, 390, 20))), .05)
    for k in range(7):
        x = 60 + k * 76
        p.parts.append(f'<g class="a" data-fx="slide" data-at="{p.at(.05 + .1 * k)}" data-d="2.2" data-y0="0" data-y1="-260" '
                       f'data-x0="0" data-x1="{(-1) ** k * 30}"><circle cx="{x}" cy="360" r="{9 + 3 * (k % 3)}" fill="#fff" '
                       f'fill-opacity=".85" stroke="#9DC7C1" stroke-width="3"/></g>')
    # the thought: dots up to a cloud
    for k, (x, y, r) in enumerate(((330, 210, 12), (372, 168, 18))):
        p.fill(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="5"/>', .15 + .06 * k)
    p.fill(f'<path d="M430 40 Q470 0 530 24 Q580 -6 640 24 Q712 10 740 64 Q800 90 772 150 Q790 214 720 226 Q690 270 620 250 '
           f'Q560 280 510 244 Q440 254 430 196 Q380 160 418 110 Q396 60 430 40 Z" fill="#fff" stroke="{INK}" stroke-width="6"/>', .25)
    choc = ''.join(f'<rect x="{530 + 46 * c}" y="{86 + 44 * r}" width="40" height="38" rx="5" fill="#7A4A2E"/>'
                   for c in range(3) for r in range(2))
    sw = swap_at or p.at(.58)
    c0 = min(p.at(.32), sw - .8)
    p.parts.append(f'<g class="a" data-fx="life" data-at="{c0:.2f}" data-d="{sw - c0 + .1:.2f}" data-fi=".25" data-fo=".15">'
                   f'<rect x="516" y="72" width="164" height="114" rx="10" fill="#5A321E" stroke="{INK}" stroke-width="5"/>{choc}</g>')
    p.parts.append(f'<g class="a" data-fx="coinflip" data-at="{sw:.2f}" data-d="1.0" data-turns="2" '
                   f'style="transform-box:fill-box;transform-origin:center">{_banknote(508, 92, 180, 86)}</g>')
    p.parts.append(f'<g class="a" data-fx="fade" data-at="{sw + .35:.2f}" data-d=".4"><text x="598" y="226" text-anchor="middle" '
                   f'font-family="\'Sans\',sans-serif" font-weight="700" font-size="30" fill="{TEAL}">CASH</text></g>')


def cash_machine(p, walk_s=1.4, at_s=None, **_):
    """June 1967: a brick wall with a cash machine (slot, small window, a drawer), a JUNE 1967 date tag and a street
    sign; the man walks up to it, turns to it, and notes slide out of the slot."""
    t0 = p.t0
    bricks = ''.join(f'<rect x="{x + (22 if r % 2 else 0)}" y="{60 + r * 40}" width="80" height="34" rx="3" fill="{BRICK}" '
                     f'fill-opacity="{.8 + .2 * ((x * 7 + r * 3) % 5) / 5:.2f}"/>' for r in range(14) for x in range(300, 800, 88))
    p.fill(f'<rect x="300" y="54" width="500" height="580" fill="#8E3B2A"/>{bricks}', 0, .3)
    p.fill(f'<rect x="420" y="190" width="290" height="330" rx="14" fill="#C9CED3" stroke="{INK}" stroke-width="7"/>'
           f'<rect x="450" y="220" width="230" height="90" rx="8" fill="#1E2A2A"/>'
           f'<text x="565" y="276" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="30" '
           f'fill="#9DE2C9" letter-spacing="3">CASH</text>'
           f'<rect x="460" y="340" width="210" height="16" rx="8" fill="{INK}"/>'
           f'<rect x="470" y="400" width="190" height="80" rx="8" fill="#AEB4BA" stroke="{INK}" stroke-width="5"/>'
           f'<rect x="545" y="430" width="40" height="12" rx="6" fill="{INK}"/>', .05)
    p.fill(_tile(0, 0, 280, 80, RED, "JUNE 1967", 44), .1)
    p.fill(f'<rect x="20" y="104" width="240" height="56" rx="8" fill="#fff" stroke="{INK}" stroke-width="5"/>'
           f'<text x="140" y="142" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="28" '
           f'fill="{INK}" letter-spacing="2">ENFIELD</text>', .16)
    stop = t0 + walk_s
    out = (t0 + at_s) if at_s else stop + .6
    for k in range(3):
        p.parts.append(f'<g class="a" data-fx="slide" data-ease="out" data-at="{out + .18 * k:.2f}" data-d=".5" data-x0="0" '
                       f'data-x1="0" data-y0="-34" data-y1="{6 + 12 * k}"><g class="a" data-fx="fade" data-at="{out + .18 * k:.2f}" '
                       f'data-d=".1">{_banknote(500, 346, 130, 58, (-1) ** k * 4)}</g></g>')
    p.fill(f'<rect x="460" y="340" width="210" height="16" rx="8" fill="{INK}"/>', .05)       # the slot's lip over the notes
    p.parts.append(f'<g class="a" data-fx="slide" data-at="{t0 + .05:.2f}" data-d="{walk_s - .05:.2f}" data-x0="-360" data-x1="0">')
    trader(p, 330, 630, .9, "point", 0, look=1, walk=(t0 + .05, stop))
    p.parts.append("</g>")


def radio_cheque(p, at_s=None, **_):
    """How it worked: a paper cheque with a CARBON 14 label and a radiation sign glowing, sliding down into the
    machine's drawer, which shuts."""
    p.fill(f'<rect x="120" y="420" width="560" height="200" rx="18" fill="#C9CED3" stroke="{INK}" stroke-width="7"/>'
           f'<rect x="170" y="452" width="460" height="40" rx="10" fill="{INK}"/>', 0, .3)
    go = p.t0 + (at_s or p.dur * .55)
    p.parts.append(f'<g class="a" data-fx="slide" data-ease="inout" data-at="{go:.2f}" data-d=".7" data-x0="0" data-x1="0" '
                   f'data-y0="0" data-y1="140"><g class="a" data-fx="kf" data-at="0" data-d="1" '
                   f'data-kf="{H.escape(_json([[0, 0, 0, 1, 1], [round(go + .45, 2), 0, 0, 1, 1], [round(go + .7, 2), 0, 0, 1, 0]]))}">')
    p.fill(f'<rect x="140" y="40" width="520" height="300" rx="14" fill="#FFF8E6" stroke="{INK}" stroke-width="7" '
           f'transform="rotate(-3 400 190)"/>'
           f'<text x="190" y="110" font-family="\'Serif\',serif" font-weight="700" font-size="46" fill="{INK}">CHEQUE</text>'
           f'<rect x="190" y="150" width="280" height="12" rx="6" fill="{GREY}"/><rect x="190" y="186" width="220" height="12" rx="6" fill="{GREY}"/>'
           f'<rect x="190" y="252" width="250" height="44" rx="10" fill="{INK}"/>'
           f'<text x="315" y="284" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="26" '
           f'fill="#F2C35B" letter-spacing="2">CARBON 14</text>', .05)
    # a generic radiation sign: yellow disc, three black blades, pulsing
    blades = ''.join(f'<path d="M560 190 L{560 + 62 * math.cos(math.radians(a)):.1f} {190 + 62 * math.sin(math.radians(a)):.1f} '
                     f'A62 62 0 0 1 {560 + 62 * math.cos(math.radians(a + 60)):.1f} {190 + 62 * math.sin(math.radians(a + 60)):.1f} Z" '
                     f'fill="{INK}"/>' for a in (-120, 0, 120))
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="4" data-w="3">')
    p.fill(f'<circle cx="560" cy="190" r="84" fill="#F2C35B" stroke="{INK}" stroke-width="6"/>{blades}'
           f'<circle cx="560" cy="190" r="20" fill="#F2C35B" stroke="{INK}" stroke-width="6"/><circle cx="560" cy="190" r="10" fill="{INK}"/>', .2)
    p.parts.append("</g></g></g>")
    for k in range(3):
        p.parts.append(f'<g class="a" data-fx="ripple" data-at="{p.at(.25 + .1 * k)}" data-d="1.1" '
                       f'style="transform-box:fill-box;transform-origin:center"><circle cx="560" cy="190" r="46" fill="none" '
                       f'stroke="#F2C35B" stroke-width="6"/></g>')
    p.text(400, 560, "MILDLY RADIOACTIVE", .3, size=30, weight=700, color="#fff")


def ten_pounds(p, at_s=None, **_):
    """The limit: notes drop one by one onto a pile beside a counter running £0 to £10, then a MAX stamp."""
    p.fill(f'<rect x="10" y="60" width="330" height="200" rx="22" fill="#fff" stroke="{INK}" stroke-width="6"/>', 0, .3)
    p.text(175, 120, "PAID OUT", .02, size=30, weight=700, color=GREY)
    p.parts.append(_count(175, 230, 0, 10, p.t0 + .3, 2.0, size=110, color=INK, pre="£"))
    for k in range(10):
        t = p.t0 + .3 + .2 * k
        p.parts.append(f'<g class="a" data-fx="slide" data-ease="out" data-at="{t:.2f}" data-d=".35" data-x0="0" data-x1="0" '
                       f'data-y0="-380" data-y1="0"><g class="a" data-fx="fade" data-at="{t:.2f}" data-d=".08">'
                       f'{_banknote(420 + (k % 2) * 14, 560 - 30 * k, 300, 110, (-1) ** k * 3)}</g></g>')
    st = p.t0 + (at_s or 2.6)
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{st:.2f}" data-d="0.35" data-rot="-10" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="40" y="330" width="290" height="130" rx="16" fill="#fff" fill-opacity=".92" stroke="{RED}" stroke-width="12"/>'
                   f'<text x="185" y="425" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="92" '
                   f'fill="{RED}">MAX</text></g>')


def pin_six(p, cut_s=None, **_):
    """The PIN: six boxes fill with dots one by one (keypad taps); then the last two are struck out and fall, leaving
    four; a note card pins HIS WIFE'S LIMIT: 4 DIGITS (a label, not a quote) and the man turns to it and shrugs."""
    t0 = p.t0
    for k in range(6):
        x = 20 + k * 128
        fall = k >= 4
        cut = t0 + (cut_s or p.dur * .55)
        if fall:
            p.parts.append(f'<g class="a" data-fx="slide" data-ease="inout" data-at="{cut + .1 * (k - 4):.2f}" data-d=".8" '
                           f'data-x0="0" data-x1="{20 * (k - 3)}" data-y0="0" data-y1="240" data-r="{14 * (k - 3)}" style="transform-box:fill-box;transform-origin:center">'
                           f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json([[0, 0, 0, 1, 1], [round(cut + .4, 2), 0, 0, 1, 1], [round(cut + .75, 2), 0, 0, 1, 0]]))}">')
        p.fill(f'<rect x="{x}" y="40" width="112" height="140" rx="16" fill="#fff" stroke="{RED if fall else INK}" stroke-width="7"/>', .02 * k)
        p.fill(f'<circle cx="{x + 56}" cy="110" r="22" fill="{INK}"/>', 0, .2)
        p.parts[-1] = p.parts[-1].replace(f'data-at="{p.at(0)}"', f'data-at="{t0 + .25 + .22 * k:.2f}"', 1)
        if fall:
            p.parts.append(f'<g class="a" data-fx="strike" data-at="{cut - .35:.2f}" data-d=".25"><path d="M{x - 6} 50 L{x + 118} 170" '
                           f'stroke="{RED}" stroke-width="12" stroke-linecap="round"/></g></g></g>')
    p.fill(f'<rect x="420" y="262" width="370" height="170" rx="14" fill="#F2C35B" stroke="{INK}" stroke-width="6" '
           f'transform="rotate(3 605 347)"/><text x="605" y="314" text-anchor="middle" font-family="\'Sans\',sans-serif" '
           f'font-weight="700" font-size="28" fill="{INK}" letter-spacing="3" transform="rotate(3 605 347)">HIS WIFE\'S LIMIT</text>', .62)
    p.parts[-1] = p.parts[-1].replace(f'data-at="{p.at(.62)}"', f'data-at="{t0 + (cut_s or p.dur * .55) - .5:.2f}"', 1)
    p.parts.append(f'<g class="a" data-fx="fade" data-at="{t0 + (cut_s or p.dur * .55) - .3:.2f}" data-d=".3">'
                   f'<text x="605" y="396" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="64" '
                   f'fill="{RED}" transform="rotate(3 605 347)">4 DIGITS</text></g>')
    trader(p, 210, 630, .95, "shrug", .1, look=1, turn=[(t0 + (cut_s or p.dur * .55) - .2, 1)])


def four_dots(p, **_):
    """The standard: card after card and screen after screen pop in, each with four dots, around a big 4."""
    p.fill(f'<circle cx="400" cy="330" r="150" fill="{TEAL}" stroke="{INK}" stroke-width="7"/>'
           f'<text x="400" y="400" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="220" '
           f'fill="#fff">4</text>', 0, .4)
    spots = ((20, 30, -8), (290, 0, 4), (560, 30, 9), (0, 420, 6), (300, 520, -3), (570, 430, -7))
    for k, (x, y, r) in enumerate(spots):
        dots = ''.join(f'<circle cx="{x + 46 + 38 * j}" cy="{y + 70}" r="12" fill="{INK}"/>' for j in range(4))
        p.fill(f'<g transform="rotate({r} {x + 110} {y + 60})"><rect x="{x}" y="{y}" width="220" height="120" rx="16" '
               f'fill="{"#F2C35B" if k % 2 else "#fff"}" stroke="{INK}" stroke-width="6"/>{dots}</g>', .15 + .1 * k)


def pin_asks(p, **_):
    """The close: the man turns to the viewer and points, a speech bubble asking 4 OR 6?"""
    p.fill(f'<path d="M120 60 H520 Q560 60 560 100 V300 Q560 340 520 340 H330 L280 410 L290 340 H120 Q80 340 80 300 V100 '
           f'Q80 60 120 60 Z" fill="#fff" stroke="{INK}" stroke-width="7"/>', .1)
    p.text(320, 236, "4 OR 6?", .3, size=104, serif=True, weight=700, color=RED, fx="pop")
    trader(p, 700, 630, .95, "point", .05, look=-1, turn=[(p.at(.15), 0)])


SCENES.update({f.__name__: f for f in (bank_closed, bath_idea, cash_machine, radio_cheque, ten_pounds, pin_six, four_dots,
                                       pin_asks)})


# ---- 15 Nov (the $2.04 billion jackpot Short, Format D animated calculation): 30 payments that grow 5% a year,
# brought back to today. Generic shapes of our own: no lottery logo, ticket or ball design, no real person.
# Bar heights are our own arithmetic (see build/shorts_jackpot-two-billion.py): payment k = $30.7M x 1.05^k, and its
# value today at about 4.4% a year (the rate that makes the 30 add up to the $997.6M cash option).

GOLD, GOLD_D = "#F2C35B", "#8A5F12"
JP_P, JP_G, JP_R = 30.704927, 1.05, 1.0443215        # first payment $M, growth, implied yearly rate (estimate)


def _set(p, shape):
    """A piece of the set that is already there at frame 0 (15 Nov: the hook shows its drawing from the first frame,
    only the action animates)."""
    p.parts.append(f'<g class="a" data-fx="fade" data-at="-1" data-d=".05">{shape}</g>')


def _bars30(x0=60, base=560, top=380, wbar=18, gap=5.0, pv=False):
    """The 30 payments as (x, height) pairs; pv=True gives each one's value today instead."""
    scale = top / (JP_P * JP_G ** 29)
    out = []
    for k in range(30):
        v = JP_P * JP_G ** k / (JP_R ** k if pv else 1)
        out.append((x0 + k * (wbar + gap), v * scale))
    return out


def _bar(x, base, w_, h_, fill, stroke=INK):
    return f'<rect x="{x:.1f}" y="{base - h_:.1f}" width="{w_}" height="{h_:.1f}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'


def _ball(cx, cy, r, n, fill="#fff"):
    """A generic numbered ball (no game's colours or logo)."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="{max(r * .07, 3):.1f}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .55:.1f}" fill="#fff" stroke="{INK}" stroke-width="{max(r * .04, 2):.1f}"/>'
            f'<text x="{cx}" y="{cy + r * .2:.1f}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
            f'font-size="{r * .6:.1f}" fill="{INK}">{n}</text>'
            f'<ellipse cx="{cx - r * .4:.1f}" cy="{cy - r * .45:.1f}" rx="{r * .22:.1f}" ry="{r * .1:.1f}" fill="#fff" '
            f'fill-opacity=".8" transform="rotate(-35 {cx - r * .4:.1f} {cy - r * .45:.1f})"/>')


def jackpot_hook(p, half_s=None, **_):
    """The hook: a towering gold column $2.04B stands from frame 0 beside the trader; on 'about half' a teal column
    rises to half its height beside it, the missing half outlined in red dashes with a bobbing question mark, and
    the trader turns to the viewer and shrugs."""
    t0 = p.t0
    hs = t0 + (half_s or p.dur * .45)
    _set(p, f'<path d="M20 600 L780 600" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="70" y="80" width="200" height="520" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="7"/>'
            + "".join(f'<path d="M84 {120 + 52 * j} H256" stroke="{GOLD_D}" stroke-opacity=".35" stroke-width="5"/>' for j in range(9))
            + f'<rect x="58" y="10" width="224" height="70" rx="14" fill="{INK}"/>'
              f'<text x="170" y="62" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="50" fill="{GOLD}">$2.04B</text>')
    # the cash column rises to half on the words
    p.parts.append(f'<g class="a" data-fx="growY" data-at="{hs:.2f}" data-d=".8" style="transform-box:fill-box">'
                   f'<rect x="320" y="340" width="200" height="260" rx="10" fill="{TEAL}" stroke="{INK}" stroke-width="7"/></g>')
    p.parts.append(f'<g class="a" data-fx="pop" data-at="{hs + .7:.2f}" data-d=".35" style="transform-box:fill-box;transform-origin:center">'
                   f'<text x="420" y="490" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="46" fill="#fff">HALF</text></g>')
    p.parts.append(f'<g class="a" data-fx="draw" data-at="{hs + .8:.2f}" data-d=".6"><path d="M320 340 V80 H520 V340" fill="none" '
                   f'stroke="{RED}" stroke-width="7" stroke-dasharray="20 14" stroke-linejoin="round"/></g>')
    p.parts.append(f'<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="10" data-w="2.6">'
                   f'<g class="a" data-fx="pop" data-at="{hs + 1.1:.2f}" data-d=".4" style="transform-box:fill-box;transform-origin:center">'
                   f'<text x="420" y="262" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="170" fill="{RED}">?</text></g></g>')
    trader(p, 660, 600, .9, "point", (-1 - t0) / p.dur, look=-1, turn=[(hs + .9, 0)])


def before_tax(p, stamp_s=None, **_):
    """Not taxes: the two numbers hang as tags, each with a BEFORE TAX chip; a tax form slides in below and a red
    LATER stamp lands on it."""
    for k, (lab, fill) in enumerate((("$2.04B", GOLD), ("$997.6M", TEAL))):
        x = 200 + 380 * k
        p.parts.append(f'<g class="a" data-fx="swing" data-at="0" data-d="1" data-amp="5" data-w="2.2" data-ph="{k * 1.4}" '
                       f'style="transform-box:view-box;transform-origin:{x}px 20px">')
        p.fill(f'<path d="M{x} 20 L{x} 70" stroke="{INK}" stroke-width="4"/>'
               + _ptag(x, 140, 360, lab, fill=fill, color=INK if k == 0 else "#fff", size=54, rot=0), .03 + .12 * k)
        p.fill(_tile(x - 130, 240, 260, 64, INK, "BEFORE TAX", 30), .25 + .12 * k)
        p.parts.append("</g>")
    st = p.t0 + (stamp_s or p.dur * .55)
    p.parts.append(f'<g class="a" data-fx="slide" data-ease="out" data-at="{st - .75:.2f}" data-d=".6" data-x0="700" data-x1="0">'
                   f'<rect x="200" y="330" width="400" height="290" rx="12" fill="#fff" stroke="{INK}" stroke-width="6" transform="rotate(-3 400 475)"/>'
                   f'<text x="240" y="395" font-family="\'Serif\',serif" font-weight="700" font-size="48" fill="{INK}" transform="rotate(-3 400 475)">TAX</text>'
                   + "".join(f'<rect x="240" y="{420 + 34 * j}" width="{300 - 40 * (j % 2)}" height="12" rx="6" fill="#DCD7CF" '
                             f'transform="rotate(-3 400 475)"/>' for j in range(5)) + "</g>")
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{st:.2f}" data-d=".35" data-rot="-12" style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="250" y="440" width="300" height="110" rx="14" fill="#fff" fill-opacity=".9" stroke="{RED}" stroke-width="10"/>'
                   f'<text x="400" y="520" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="76" fill="{RED}">LATER</text></g>')


def thirty_bars(p, grow_s=None, five_s=None, **_):
    """The fine print: 30 gold bars rise one by one, left to right (a tick each), each 5% taller than the last; a
    total counts up to $2.04B over them; the first and last payments get their labels; on '5%' a red +5% chip
    jumps from bar to bar."""
    t0 = p.t0
    g0 = t0 + (grow_s if grow_s is not None else .2)
    base = 560
    bars = _bars30(pv=False)
    p.line([(40, base), (770, base)], 0, .3, w=6)
    step = .075
    for k, (x, h_) in enumerate(bars):
        p.parts.append(f'<g class="a" data-fx="growY" data-at="{g0 + step * k:.2f}" data-d=".3" style="transform-box:fill-box">'
                       f'{_bar(x, base, 18, h_, GOLD)}</g>')
    p.parts.append(_count(400, 90, 0, 2.04, round(g0, 2), round(step * 30 + .3, 2), size=74, color=INK, pre="$", suf="B", dec=2))
    p.text(400, 140, "30 PAYMENTS ADDED UP", .05, size=28, weight=700, color=GREY)
    p.parts.append(f'<g class="a" data-fx="fade" data-at="{g0 + .3:.2f}" data-d=".3">'
                   f'<text x="70" y="{base - bars[0][1] - 18:.0f}" font-family="\'Sans\',sans-serif" font-weight="700" font-size="28" fill="{INK}">$30.7M</text></g>')
    p.parts.append(f'<g class="a" data-fx="fade" data-at="{g0 + step * 30:.2f}" data-d=".3">'
                   f'<text x="775" y="{base - bars[-1][1] - 18:.0f}" text-anchor="end" font-family="\'Sans\',sans-serif" font-weight="700" '
                   f'font-size="28" fill="{INK}">$126.4M</text></g>')
    p.text(60, 605, "TODAY", .1, size=28, weight=700, color=GREY, anchor="start")
    p.text(775, 605, "YEAR 29", .1, size=28, weight=700, color=GREY, anchor="end")
    fs = t0 + (five_s or p.dur * .6)
    kf = [[round(fs, 2), 0, 0, .6, 0]] + [[round(fs + .25 + .18 * j, 2), 115 * j, -24 * j, 1, 1] for j in range(6)] + [[round(fs + 1.5, 2), 575, -140, 1, 1]]
    p.parts.append(f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json(kf))}" style="transform-box:fill-box;transform-origin:center">'
                   + _tile(80, 330, 120, 60, RED, "+5%", 34) + "</g>")


def dollar_today(p, grow_s=None, **_):
    """A dollar today beats a dollar later: TODAY's coin sits on a bank pile that grows coin by coin as the years
    tick on a little counter (interest); LATER's dollar arrives alone at the end, the same size it always was."""
    t0 = p.t0
    gs = t0 + (grow_s or p.dur * .45)
    p.text(200, 50, "TODAY", 0, size=40, weight=700, color=TEAL)
    p.text(600, 50, "LATER", 0, size=40, weight=700, color=RED)
    p.line([(400, 80), (400, 600)], .02, .3, color=GREY, w=4, dash="12 12")
    coin(p, 200, 470, 90, "$1", "gold", .05, flip=2)
    for j in range(5):
        p.parts.append(f'<g class="a" data-fx="slide" data-ease="out" data-at="{gs + .3 * j:.2f}" data-d=".35" data-y0="-300" data-y1="0">'
                       f'<g class="a" data-fx="fade" data-at="{gs + .3 * j:.2f}" data-d=".06">'
                       f'<ellipse cx="200" cy="{372 - 34 * j}" rx="78" ry="22" fill="{GOLD_D}"/>'
                       f'<ellipse cx="200" cy="{366 - 34 * j}" rx="78" ry="22" fill="{GOLD}" stroke="{INK}" stroke-width="4"/></g></g>')
    p.parts.append(f'<g class="a" data-fx="pop" data-at="{gs:.2f}" data-d=".35" style="transform-box:fill-box;transform-origin:center">'
                   + _tile(50, 110, 300, 64, TEAL, "+ INTEREST", 34) + "</g>")
    p.parts.append(_count(600, 220, 0, 29, round(gs - .2, 2), 1.6, size=64, color=INK, pre="YEAR "))
    p.parts.append(f'<g class="a" data-fx="slide" data-ease="out" data-at="{gs + 1.3:.2f}" data-d=".6" data-x0="260" data-x1="0">'
                   f'<g class="a" data-fx="fade" data-at="{gs + 1.3:.2f}" data-d=".1">')
    coin(p, 600, 470, 90, "$1", "nickel", 0)
    p.parts[-1] = p.parts[-1].replace(f'data-at="{p.at(0)}"', f'data-at="{gs + 1.3:.2f}"', 1)
    p.parts.append("</g></g>")
    p.parts.append(f'<g class="a" data-fx="pop" data-at="{gs + 1.9:.2f}" data-d=".3" style="transform-box:fill-box;transform-origin:center">'
                   f'<text x="600" y="345" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="34" fill="{RED}">STILL $1</text></g>')


def shrink_bars(p, shrink_s=None, **_):
    """Bring each payment back to today: the 30 gold bars stand as before, then, left to right, each shrinks to its
    value today, leaving a dashed ghost of what it was; the far ones fall the most and the row ends nearly flat.
    The last bar's two labels: $126.4M then about $35.9M today."""
    t0 = p.t0
    ss = t0 + (shrink_s or p.dur * .3)
    base = 560
    full, pv = _bars30(), _bars30(pv=True)
    p.line([(40, base), (770, base)], 0, .2, w=6)
    step = .06
    for k, ((x, h_), (_, h2)) in enumerate(zip(full, pv)):
        p.parts.append(f'<g class="a" data-fx="fade" data-at="{ss + step * k:.2f}" data-d=".2">'
                       f'<rect x="{x:.1f}" y="{base - h_:.1f}" width="18" height="{h_:.1f}" rx="4" fill="none" stroke="{GREY}" '
                       f'stroke-width="3" stroke-dasharray="6 5"/></g>')
        p.parts.append(f'<g class="a" data-fx="growY" data-at="{t0 + .02 * k:.2f}" data-d=".25" style="transform-box:fill-box">'
                       f'<g class="a" data-fx="scaleY" data-at="{ss + step * k:.2f}" data-d=".55" data-s0="1" data-s1="{h2 / h_:.4f}" '
                       f'style="transform-box:fill-box">{_bar(x, base, 18, h_, GOLD)}</g></g>')
    xl, hl = full[-1]
    p.parts.append(f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json([[0, 0, 0, 1, 1], [round(ss + step * 29, 2), 0, 0, 1, 1], [round(ss + step * 29 + .3, 2), 0, 0, 1, 0]]))}">'
                   f'<text x="775" y="{base - hl - 18:.0f}" text-anchor="end" font-family="\'Sans\',sans-serif" font-weight="700" font-size="28" fill="{INK}">$126.4M</text></g>')
    p.parts.append(f'<g class="a" data-fx="pop" data-at="{ss + step * 29 + .35:.2f}" data-d=".35" style="transform-box:fill-box;transform-origin:center">'
                   f'<text x="775" y="{base - pv[-1][1] - 18:.0f}" text-anchor="end" font-family="\'Sans\',sans-serif" font-weight="700" '
                   f'font-size="30" fill="{RED}">≈ $35.9M TODAY</text></g>')
    p.text(60, 605, "TODAY", .1, size=28, weight=700, color=GREY, anchor="start")
    p.text(775, 605, "YEAR 29", .1, size=28, weight=700, color=GREY, anchor="end")
    p.text(400, 70, "VALUE TODAY", .02, size=36, weight=700, color=GREY)


def cash_pile(p, at_s=None, **_):
    """Add them up: the 30 shrunk bars slide right one after another into one teal column that rises as they land,
    a counter running to $997.6M; then a CASH OPTION label and a check."""
    t0 = p.t0
    a = t0 + (at_s if at_s is not None else .3)
    base = 560
    pv = _bars30(x0=40, wbar=12, gap=5, top=380 * 1.0)
    pvh = [h_ / JP_R ** k for k, (_, h_) in enumerate(pv)]
    p.line([(20, base), (780, base)], 0, .2, w=6)
    step = .05
    for k, ((x, _), h2) in enumerate(zip(pv, pvh)):
        t = a + step * k
        p.parts.append(f'<g class="a" data-fx="fade" data-at="{t0 + .01 * k:.2f}" data-d=".2">'
                       f'<g class="a" data-fx="slide" data-ease="inout" data-at="{t:.2f}" data-d=".45" data-x0="0" data-x1="{640 - x:.0f}" '
                       f'data-y0="0" data-y1="-{20 + 8 * (k % 4)}"><g class="a" data-fx="kf" data-at="0" data-d="1" '
                       f'data-kf="{H.escape(_json([[0, 0, 0, 1, 1], [round(t + .35, 2), 0, 0, 1, 1], [round(t + .45, 2), 0, 0, 1, 0]]))}">'
                       f'{_bar(x, base, 12, h2 * 1.9, GOLD)}</g></g></g>')
    p.parts.append(f'<g class="a" data-fx="growY" data-at="{a + .3:.2f}" data-d="{step * 30 + .2:.2f}" style="transform-box:fill-box">'
                   f'<rect x="590" y="150" width="170" height="410" rx="10" fill="{TEAL}" stroke="{INK}" stroke-width="7"/></g>')
    p.parts.append(_count(330, 140, 0, 997.6, round(a + .3, 2), round(step * 30 + .2, 2), size=78, color=INK, pre="$", suf="M", dec=1))
    p.parts.append(f'<g class="a" data-fx="pop" data-at="{a + step * 30 + .6:.2f}" data-d=".35" style="transform-box:fill-box;transform-origin:center">'
                   + _tile(150, 200, 360, 70, TEAL, "CASH OPTION", 38) + "</g>")
    p.parts.append(f'<g class="a" data-fx="draw" data-at="{a + step * 30 + .9:.2f}" data-d=".35">'
                   f'<path d="M620 340 L665 390 L735 290" fill="none" stroke="#fff" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/></g>')


def rate_dial(p, rate_s=None, more_s=None, **_):
    """Our estimate: a dial from 0% to 10% whose needle swings up to about 4.4% as the rate is said; on 'higher
    rates' it swings on towards 7% and the teal cash column beside it sinks (an illustration of the direction,
    no figure)."""
    t0 = p.t0
    rs = t0 + (rate_s if rate_s is not None else .3)
    ms = t0 + (more_s or p.dur * .6)
    cx, cy, R = 300, 470, 250
    ang = lambda pct: 180 + 18 * pct                     # 0% left (180 deg) to 10% right (360 deg)
    pt = lambda a_, r: (cx + r * math.cos(math.radians(a_)), cy + r * math.sin(math.radians(a_)))
    arc = " ".join(f"{'M' if i == 0 else 'L'}{pt(180 + i * 6, R)[0]:.1f} {pt(180 + i * 6, R)[1]:.1f}" for i in range(31))
    p.fill(f'<path d="{arc} Z" fill="#fff" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>', 0, .3)
    for pct in range(11):
        a_ = ang(pct)
        (x1, y1), (x2, y2) = pt(a_, R - 8), pt(a_, R - (40 if pct % 5 == 0 else 24))
        p.line([(x1, y1), (x2, y2)], .03 + .01 * pct, .1, w=6 if pct % 5 == 0 else 4, j=.4)
    for pct, lab in ((0, "0%"), (5, "5%"), (10, "10%")):
        x, y = pt(ang(pct), R - 78)
        p.text(round(x), round(y + 12), lab, .1, size=30, weight=700, color=GREY)
    a1, a2 = 18 * 4.43, 18 * 7
    kf = [[0, 0, 0, 1, 1, 0], [round(rs, 2), 0, 0, 1, 1, 0], [round(rs + .9, 2), 0, 0, 1, 1, round(a1, 1)],
          [round(ms, 2), 0, 0, 1, 1, round(a1, 1)], [round(ms + .8, 2), 0, 0, 1, 1, a2]]
    p.parts.append(f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json(kf))}" '
                   f'style="transform-box:view-box;transform-origin:{cx}px {cy}px">'
                   f'<path d="M{cx} {cy - 12} L{cx - R + 50} {cy} L{cx} {cy + 12} Z" fill="{RED}" stroke="{INK}" stroke-width="4" '
                   f'stroke-linejoin="round"/></g>')
    p.fill(f'<circle cx="{cx}" cy="{cy}" r="24" fill="{INK}"/>', .05)
    p.parts.append(f'<g class="a" data-fx="pop" data-at="{rs + .9:.2f}" data-d=".35" style="transform-box:fill-box;transform-origin:center">'
                   + _tile(150, 520, 300, 80, RED, "≈ 4.4% A YEAR", 40) + "</g>")
    p.parts.append(f'<g class="a" data-fx="scaleY" data-at="{ms + .1:.2f}" data-d=".8" data-s0="1" data-s1=".72" style="transform-box:fill-box">'
                   f'<rect x="610" y="190" width="150" height="410" rx="10" fill="{TEAL}" stroke="{INK}" stroke-width="7"/></g>')
    p.text(685, 170, "CASH", .1, size=32, weight=700, color=TEAL)
    p.parts.append(f'<g class="a" data-fx="pop" data-at="{ms + .7:.2f}" data-d=".3" style="transform-box:fill-box;transform-origin:center">'
                   f'<path d="M665 300 L705 300 L705 360 L735 360 L685 420 L635 360 L665 360 Z" fill="#fff" stroke="{INK}" stroke-width="4"/></g>')


def jackpot_asks(p, **_):
    """The close: the trader turns to the viewer and points; a speech bubble asks CASH OR 30?"""
    p.fill(f'<path d="M120 60 H520 Q560 60 560 100 V300 Q560 340 520 340 H330 L280 410 L290 340 H120 Q80 340 80 300 V100 '
           f'Q80 60 120 60 Z" fill="#fff" stroke="{INK}" stroke-width="7"/>', .1)
    p.text(320, 185, "CASH", .3, size=92, serif=True, weight=700, color=TEAL, fx="pop")
    p.text(320, 290, "OR 30?", .42, size=92, serif=True, weight=700, color=RED, fx="pop")
    trader(p, 700, 630, .95, "point", .05, look=-1, turn=[(p.at(.15), 0)])


SCENES.update({f.__name__: f for f in (jackpot_hook, before_tax, thirty_bars, dollar_today, shrink_bars, cash_pile, rate_dial,
                                       jackpot_asks)})


# ---- 15 Nov scenes (Levels #14, enterprise value): one drawing per level, shown through the question, the clock
# and the answer (Pietro, 14 Nov: a picture in every beat). Each takes m, the level's moments in Reel seconds
# (levels.scene: q, qs = each question sentence (start, end), think, a, as_ = each answer sentence, end), and acts
# the idea out across them. Generic shapes of our own: no bank, company or logo. Only the episode's worked numbers.

DEBT_C, CASH_C = "#3B3F48", "#7FB59B"


def _abs(p, t):
    """A Reel time as the Pen's fraction (the Pen counts from t0 over dur)."""
    return max(0.0, (t - p.t0) / p.dur)


def _g(fx, at, d, inner, style="transform-box:fill-box;transform-origin:center", **data):
    attrs = "".join(f' data-{k}="{v}"' for k, v in data.items())
    return f'<g class="a" data-fx="{fx}" data-at="{at:.2f}" data-d="{d}"{attrs} style="{style}">{inner}</g>'


def _life(at, d, inner, fi=.2, fo=.2):
    return f'<g class="a" data-fx="life" data-at="{at:.2f}" data-d="{d:.2f}" data-fi="{fi}" data-fo="{fo}">{inner}</g>'


def _office(x, base, w_=200, h_=230):
    """A generic office block: flat roof, a grid of windows, a door."""
    s = (f'<rect x="{x}" y="{base - h_}" width="{w_}" height="{h_}" rx="6" fill="#fff" stroke="{INK}" stroke-width="6"/>'
         f'<rect x="{x - 12}" y="{base - h_ - 22}" width="{w_ + 24}" height="26" rx="5" fill="{INK}"/>')
    for r in range(3):
        for c in range(3):
            s += (f'<rect x="{x + 22 + c * (w_ - 44) / 3:.0f}" y="{base - h_ + 24 + r * 52}" width="{(w_ - 44) / 3 - 14:.0f}" height="34" '
                  f'rx="4" fill="#DCEFEA" stroke="{INK}" stroke-width="3"/>')
    return s + f'<rect x="{x + w_ / 2 - 26:.0f}" y="{base - 62}" width="52" height="62" rx="4" fill="{TEAL}" stroke="{INK}" stroke-width="4"/>'


def ev_whole(p, m=None, **_):
    """Level 1, what enterprise value is. The business stands in the middle; as the question is asked the lenders
    (a bank) arrive on the left and the shareholders on the right, and money travels from each into the business;
    a question mark bobs over it through the clock. On the answer a teal bracket spans all three and ENTERPRISE
    VALUE lands on it; on the second sentence DEBT and EQUITY tags drop onto the two sides."""
    q0 = m["qs"][0][0]
    base = 560
    p.parts.append(_g("fade", p.t0, .3, f'<path d="M20 {base} L780 {base}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                      + _office(300, base, 200, 250)))
    # the lenders: a small bank, from the left
    bank_ = (f'<path d="M30 352 L130 300 L230 352 Z" fill="{INK}"/>'
             + "".join(f'<rect x="{48 + 46 * k}" y="362" width="22" height="160" fill="#E8E4DE" stroke="{INK}" stroke-width="4"/>' for k in range(4))
             + f'<rect x="26" y="522" width="208" height="38" fill="{INK}"/>')
    _slide(p, _abs(p, q0 + .15), bank_ + f'<text x="130" y="285" text-anchor="middle" font-family="\'Sans\',sans-serif" '
           f'font-weight="700" font-size="30" fill="{INK}">LENDERS</text>', x0=-320, d=.55)
    # the shareholders, from the right
    folks = ""
    for k in range(3):
        x, s = 600 + 72 * k, .78
        c = TEAL if k == 1 else INK
        folks += (f'<circle cx="{x}" cy="{base - 150 * s:.0f}" r="{26 * s:.0f}" fill="#fff" stroke="{c}" stroke-width="6"/>'
                  f'<path d="M{x} {base - 124 * s:.0f} L{x} {base - 50 * s:.0f} M{x - 40 * s:.0f} {base - 100 * s:.0f} L{x} {base - 110 * s:.0f} '
                  f'L{x + 40 * s:.0f} {base - 95 * s:.0f} M{x - 30 * s:.0f} {base} L{x} {base - 50 * s:.0f} L{x + 30 * s:.0f} {base}" '
                  f'fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    _slide(p, _abs(p, q0 + .55), folks + f'<text x="672" y="395" text-anchor="middle" font-family="\'Sans\',sans-serif" '
           f'font-weight="700" font-size="30" fill="{INK}">SHAREHOLDERS</text>', x0=320, d=.55)
    # money from each side into the business, on a loop through the question and the clock
    t = q0 + 1.0
    k = 0
    while t < m["a"] - .2:
        side = k % 2
        x0 = 150 if side == 0 else 600
        note = _note(x0 - 50, 420, 100, 46)
        dx = 330 - x0 if side == 0 else 420 - x0
        p.parts.append(_life(t, .9, _g("slide", t, .8, note, style="", x0=0, x1=dx, y0=0, y1=10, ease="inout"), fi=.12, fo=.15))
        t += .55
        k += 1
    # the question mark over the business
    p.parts.append(_life(m["think"] - .1, m["a"] - m["think"] + .15,
                         '<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="8" data-w="3">'
                         f'<text x="400" y="230" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="120" '
                         f'fill="{RED}">?</text></g>'))
    # the answer: a bracket over all three, ENTERPRISE VALUE
    a = m["a"]
    p.line([(30, 250), (30, 214), (770, 214), (770, 250)], _abs(p, a + .02), .45, color=TEAL, w=9)
    p.parts.append(_g("pop", a + .3, .4, _tile(170, 120, 460, 78, TEAL, "ENTERPRISE VALUE", 44)))
    if len(m["as_"]) > 1:
        a1 = m["as_"][1][0]
        p.parts.append(_g("pop", a1 + .1, .35, _ptag(140, 470, 170, "DEBT", DEBT_C, "#fff", 34)))
        p.parts.append(_g("pop", a1 + .55, .35, _ptag(680, 500, 190, "EQUITY", GOLD, INK, 34)))


def ev_bridge(p, m=None, eq=100, debt=40, cash=10, **_):
    """Level 2, the bridge. EQUITY grows to $100 on the first sentence; on the second DEBT drops onto it (+$40)
    and CASH comes off the top (-$10); on 'what's enterprise value' a dashed EV column waits with a question mark;
    on the answer the EV column fills teal to the same height and counts to $130."""
    base, k = 548, 2.9
    ev = eq + debt - cash
    qs = m["qs"]
    t_eq = qs[0][0] + .15
    t_debt = qs[1][0] + .1 if len(qs) > 1 else t_eq + 1
    t_cash = (qs[1][0] + qs[1][1]) / 2 + .1 if len(qs) > 1 else t_debt + .8
    t_ask = qs[-1][0] + .1
    a = m["a"]
    xs = [20, 215, 410, 610]
    cw = 170
    p.parts.append(_g("fade", p.t0, .3, f'<path d="M0 {base} L800 {base}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'))

    def lab(x, txt, at, col=INK):
        p.parts.append(_g("fade", at, .3, f'<text x="{x + cw / 2}" y="{base + 46}" text-anchor="middle" font-family="\'Sans\',sans-serif" '
                                          f'font-weight="700" font-size="32" fill="{col}">{H.escape(txt)}</text>'))

    def val(x, y, txt, at, col="#fff", size=46):
        p.parts.append(_g("pop", at, .3, f'<text x="{x + cw / 2}" y="{y}" text-anchor="middle" font-family="\'Serif\',serif" '
                                         f'font-weight="700" font-size="{size}" fill="{col}">{H.escape(txt)}</text>'))
    # equity grows from the ground
    he = eq * k
    p.parts.append(_g("growY", t_eq, .6, f'<rect x="{xs[0]}" y="{base - he:.0f}" width="{cw}" height="{he:.0f}" rx="8" fill="{GOLD}" '
                                         f'stroke="{INK}" stroke-width="6"/>', style="transform-box:fill-box"))
    val(xs[0], base - he / 2 + 16, f"${eq}", t_eq + .45, INK)
    lab(xs[0], "EQUITY", t_eq)
    # debt drops onto the top of equity's level
    hd = debt * k
    _slide(p, _abs(p, t_debt), f'<rect x="{xs[1]}" y="{base - he - hd:.0f}" width="{cw}" height="{hd:.0f}" rx="8" fill="{DEBT_C}" '
                               f'stroke="{INK}" stroke-width="6"/>'
                               f'<text x="{xs[1] + cw / 2}" y="{base - he - hd / 2 + 16:.0f}" text-anchor="middle" font-family="\'Serif\',serif" '
                               f'font-weight="700" font-size="46" fill="#fff">+${debt}</text>', y0=-260, d=.5)
    p.parts.append(_g("draw", t_debt + .3, .3, f'<path d="M{xs[0] + cw} {base - he:.0f} L{xs[1]} {base - he:.0f}" stroke="{INK}" '
                                               f'stroke-width="4" stroke-dasharray="10 8" fill="none"/>', style=""))
    lab(xs[1], "+ DEBT", t_debt)
    # cash hangs down from the top of debt, then is lifted out
    hc = cash * k
    top = base - he - hd
    p.parts.append(_g("growYdown", t_cash, .45, f'<rect x="{xs[2]}" y="{top:.0f}" width="{cw}" height="{hc:.0f}" rx="6" fill="{CASH_C}" '
                                                 f'stroke="{INK}" stroke-width="6"/>', style="transform-box:fill-box"))
    p.parts.append(_g("pop", t_cash + .3, .3, f'<text x="{xs[2] + cw / 2}" y="{top + hc + 52:.0f}" text-anchor="middle" '
                                              f'font-family="\'Serif\',serif" font-weight="700" font-size="46" fill="{INK}">&#8722;${cash}</text>'))
    p.parts.append(_g("draw", t_cash + .1, .3, f'<path d="M{xs[1] + cw} {top:.0f} L{xs[2]} {top:.0f}" stroke="{INK}" stroke-width="4" '
                                               f'stroke-dasharray="10 8" fill="none"/>', style=""))
    lab(xs[2], "− CASH", t_cash)
    # the EV column: dashed and empty on the ask, filled on the answer
    hv = ev * k
    p.parts.append(_life(t_ask, a - t_ask + .25,
                         f'<rect x="{xs[3]}" y="{base - hv:.0f}" width="{cw}" height="{hv:.0f}" rx="8" fill="none" stroke="{TEAL}" '
                         f'stroke-width="6" stroke-dasharray="16 12"/>'
                         '<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="7" data-w="3">'
                         f'<text x="{xs[3] + cw / 2}" y="{base - hv / 2 + 40:.0f}" text-anchor="middle" font-family="\'Serif\',serif" '
                         f'font-weight="700" font-size="120" fill="{TEAL}">?</text></g>', fi=.2, fo=.15))
    p.parts.append(_g("draw", t_cash + .5, .3, f'<path d="M{xs[2] + cw} {base - hv:.0f} L{xs[3]} {base - hv:.0f}" stroke="{INK}" '
                                               f'stroke-width="4" stroke-dasharray="10 8" fill="none"/>', style=""))
    lab(xs[3], "= EV", t_ask, TEAL)
    p.parts.append(_g("growY", a + .05, .6, f'<rect x="{xs[3]}" y="{base - hv:.0f}" width="{cw}" height="{hv:.0f}" rx="8" fill="{TEAL}" '
                                            f'stroke="{INK}" stroke-width="6"/>', style="transform-box:fill-box"))
    p.parts.append(_count(xs[3] + cw / 2, round(base - hv / 2 + 18), 0, ev, round(a + .1, 2), .8, size=54, color="#fff", pre="$"))
    # the second answer sentence walks the sum: each column pulses in turn
    if len(m["as_"]) > 1:
        s0, s1 = m["as_"][1]
        for j, x in enumerate(xs[:3]):
            hh = (he, hd, hc)[j]
            y = (base - he, base - he - hd, top)[j]
            tb = s0 + (s1 - s0) * (.05 + .3 * j)
            ring = (f'<rect x="{x - 9}" y="{y - 9:.0f}" width="{cw + 18}" height="{hh + 18:.0f}" rx="12" fill="none" '
                    f'stroke="{TEAL}" stroke-width="7"/>')
            p.parts.append(_life(tb, .75, _g("pop", tb, .3, ring), fi=.08, fo=.25))


def ev_borrow(p, m=None, amount=50, ev=130, **_):
    """Level 3, borrow and keep it as cash. A balance: EV $130 sits on the pivot. On 'borrows fifty' a DEBT +$50
    weight drops on the left pan and the beam tips; on 'keeps it as cash' a CASH +$50 weight drops on the right pan
    and the beam comes back level; a question mark over EV through the clock; on 'Nothing.' EV is ticked and NO
    CHANGE lands beside it; on 'they cancel out' the two weights pulse together."""
    qs, a = m["qs"], m["a"]
    s0, s1 = qs[0]
    t_debt = s0 + .25
    t_cash = s0 + (s1 - s0) * .62
    cx, cy, half = 400, 330, 290
    rot = 7.0
    dy = round(half * math.sin(math.radians(rot)), 1)
    # stand and EV on top, there from the start
    p.parts.append(_g("fade", p.t0, .3,
                      f'<path d="M{cx} {cy} L{cx - 70} 560 L{cx + 70} 560 Z" fill="{INK}"/>'
                      f'<path d="M80 560 L720 560" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                      + _tile(cx - 130, 130, 260, 120, TEAL, "", 10)
                      + f'<text x="{cx}" y="178" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="34" fill="#fff">EV</text>'
                      f'<text x="{cx}" y="232" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="56" fill="#fff">${ev}</text>'))
    keys = [[0, 0, 0, 1, 1, 0], [round(t_debt + .3, 2), 0, 0, 1, 1, 0], [round(t_debt + .9, 2), 0, 0, 1, 1, -rot],
            [round(t_cash + .3, 2), 0, 0, 1, 1, -rot], [round(t_cash + 1.0, 2), 0, 0, 1, 1, 0]]
    p.parts.append(f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json(keys))}" '
                   f'style="transform-box:view-box;transform-origin:{cx}px {cy}px">'
                   f'<rect x="{cx - half - 20}" y="{cy - 10}" width="{2 * half + 40}" height="20" rx="10" fill="{INK}"/>'
                   f'<circle cx="{cx}" cy="{cy}" r="18" fill="{GOLD}" stroke="{INK}" stroke-width="5"/></g>')

    def pan(x, sign, weight, t_drop):
        k_ = [[0, 0, 0], [round(t_debt + .3, 2), 0, 0], [round(t_debt + .9, 2), 0, sign * dy], [round(t_cash + .3, 2), 0, sign * dy],
              [round(t_cash + 1.0, 2), 0, 0]]
        kk = [[t, x_, y_, 1, 1, 0] for t, x_, y_ in k_]
        inner = (f'<path d="M{x} {cy} L{x - 90} 470 M{x} {cy} L{x + 90} 470" stroke="{INK}" stroke-width="4"/>'
                 f'<path d="M{x - 110} 470 L{x + 110} 470 Q{x} 520 {x - 110} 470 Z" fill="#E8E1D4" stroke="{INK}" stroke-width="5"/>')
        # the weight falls from just above the pan (a first cut dropped it from the question card's height, over its words)
        inner += _g("fade", t_drop, .15, _g("slide", t_drop, .4, weight, style="", x0=0, x1=0, y0=-170, y1=0, ease="out"), style="")
        p.parts.append(f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json(kk))}">{inner}</g>')
    w_debt = (f'<rect x="{cx - half - 95}" y="382" width="190" height="88" rx="10" fill="{DEBT_C}" stroke="{INK}" stroke-width="5"/>'
              f'<text x="{cx - half}" y="418" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="28" fill="#fff">DEBT</text>'
              f'<text x="{cx - half}" y="458" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="38" fill="#fff">+${amount}</text>')
    w_cash = (f'<rect x="{cx + half - 95}" y="382" width="190" height="88" rx="10" fill="{CASH_C}" stroke="{INK}" stroke-width="5"/>'
              f'<text x="{cx + half}" y="418" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="28" fill="{INK}">CASH</text>'
              f'<text x="{cx + half}" y="458" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="38" fill="{INK}">+${amount}</text>')
    pan(cx - half, 1, w_debt, t_debt)
    pan(cx + half, -1, w_cash, t_cash)
    # the question over EV
    p.parts.append(_life(m["think"] - .1, a - m["think"] + .15,
                         '<g class="a" data-fx="float" data-at="0" data-d="1" data-amp="7" data-w="3">'
                         f'<text x="{cx + 175}" y="225" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="110" '
                         f'fill="{RED}">?</text></g>'))
    # the answer
    p.parts.append(_g("pop", a + .1, .35, f'<circle cx="{cx + 150}" cy="140" r="30" fill="#fff" stroke="{INK}" stroke-width="5"/>'
                                          f'<path d="M{cx + 136} 141 l10 11 l20 -22" fill="none" stroke="{TEAL}" stroke-width="8" '
                                          f'stroke-linecap="round" stroke-linejoin="round"/>'))
    p.parts.append(_g("pop", a + .35, .35, _ptag(668, 272, 230, "NO CHANGE", TEAL, "#fff", 30, rot=-3)))
    if len(m["as_"]) > 1:
        t_c = m["as_"][-1][0]
        p.parts.append(_g("pop", t_c + .05, .3, f'<text x="{cx}" y="455" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
                                                f'font-size="80" fill="#fff">=</text>'))


SCENES.update({f.__name__: f for f in (ev_whole, ev_bridge, ev_borrow)})


def level_picture(name, m, w, h, seed=1, **opts):
    """15 Nov: a level-long scene (levels.py scene=) sized to its box; t0 and dur span the whole level."""
    p = Pen(m["start"] + .2, max(m["end"] - m["start"], .5), seed)
    SCENES[name](p, m=m, **opts)
    return p.svg().replace(f'width="{W}" height="{Hh}"', f'width="{w}" height="{h}"', 1)


# ---- 16 Nov (the 50% puzzle Short, Format C, one surprising concept): a $100 bar that falls 50% and rises 50% and
# ends at $75; why the rise must be 100%; the same $50 measured from two bases; the loss-to-gain ladder; the
# 2007 to 2013 S&P 500 round trip. One bar scale throughout (4 px a dollar, $100 = 400 px), so the same $50 is the
# same height in every drawing. Generic shapes of our own: no index provider's logo or chart, no real person.

PX = 4                                    # pixels a dollar, every 50% drawing
B50 = 580                                 # their baseline


def _money_bar(x, w_, dollars, fill=GOLD, dash=False, col=INK):
    h_ = dollars * PX
    if dash:
        return (f'<rect x="{x}" y="{B50 - h_}" width="{w_}" height="{h_}" rx="10" fill="none" stroke="{col}" stroke-width="6" '
                f'stroke-dasharray="18 12"/>')
    return (f'<rect x="{x}" y="{B50 - h_}" width="{w_}" height="{h_}" rx="10" fill="{fill}" stroke="{INK}" stroke-width="7"/>'
            + "".join(f'<path d="M{x + 14} {B50 - h_ + 40 + 50 * j} H{x + w_ - 14}" stroke="{GOLD_D}" stroke-opacity=".3" '
                      f'stroke-width="5"/>' for j in range(int((h_ - 40) // 50))))


def _t(x, y, s, size=40, col=INK, serif=True, anchor="middle", weight=700):
    fam = "'Serif',serif" if serif else "'Sans',sans-serif"
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{H.escape(fam)}" font-weight="{weight}" font-size="{size}" '
            f'fill="{col}">{H.escape(s)}</text>')


def _arrow(x, y0, y1, col, w=16):
    """A thick marker arrow from y0 to y1 (down if y1 > y0), drawn on."""
    sgn = 1 if y1 > y0 else -1
    head = f"M{x - 34} {y1 - sgn * 40} L{x} {y1} L{x + 34} {y1 - sgn * 40}"
    return (f'<path d="M{x} {y0} L{x} {y1 - sgn * 6}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>',
            f'<path d="{head}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def half_hook(p, fall=None, rise=None, **_):
    """The hook. A $100 gold bar stands from frame 0 under a dashed START line, the trader beside it. On 'falls
    fifty percent' the bar sinks to half (a red -50% tag drops in, a thump as it lands, the counter runs 100 to 50);
    on 'rises fifty percent' it grows back by half of what is left (a teal +50% tag, the counter 50 to 75) and stops
    short: the gap to START is outlined in red with a bobbing question mark, and the trader turns to the viewer."""
    t0 = p.t0
    f0 = fall if fall is not None else t0 + .6
    r0 = rise if rise is not None else f0 + 1.8
    x, w_ = 110, 230
    _set(p, f'<path d="M20 {B50} L780 {B50}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M60 {B50 - 400} H600" stroke="{GREY}" stroke-width="5" stroke-dasharray="14 12"/>'
            + _t(600, B50 - 412, "START", 28, GREY, serif=False, anchor="end"))
    # the bar: fall to 0.5, then rise by half of that (0.75 of the start), nested so each move is its own ease
    p.parts.append(f'<g class="a" data-fx="fade" data-at="-1" data-d=".05">'
                   + _g("scaleY", f0, .7, _g("scaleY", r0, .8, _money_bar(x, w_, 100), style="transform-box:fill-box", s0=1, s1=1.5),
                        style="transform-box:fill-box", s0=1, s1=.5) + "</g>")
    # the counter inside the bar, near its foot: $100, then 100 to 50, then 50 to 75
    p.parts.append(_life(-1, f0 + 1.04, _t(x + w_ / 2, B50 - 40, "$100", 64, INK), fi=.01, fo=.05))
    p.parts.append(_life(f0, r0 - f0 + .05, _count(x + w_ / 2, B50 - 40, 100, 50, round(f0, 2), .7, size=64, pre="$"), fi=.05, fo=.05))
    p.parts.append(_life(r0, 99, _count(x + w_ / 2, B50 - 40, 50, 75, round(r0, 2), .8, size=64, pre="$"), fi=.05, fo=.01))
    # the two moves, as tags beside the bar
    p.parts.append(_g("slide", f0 - .05, .45, _g("fade", f0 - .05, .1, _ptag(440, B50 - 300, 190, "−50%", RED, "#fff", 46), style=""),
                      style="", y0=-160, y1=0, ease="out"))
    a1, a2 = _arrow(430, B50 - 230, B50 - 120, RED, 12)
    p.parts.append(_g("draw", f0 + .25, .4, a1, style=""))
    p.parts.append(_g("draw", f0 + .55, .2, a2, style=""))
    p.parts.append(_g("pop", r0 + .05, .4, _ptag(440, B50 - 60, 190, "+50%", TEAL, "#fff", 46)))
    # stops short of START: the gap and the question
    p.parts.append(_g("draw", r0 + .8, .5, f'<path d="M{x} {B50 - 300} V{B50 - 400} H{x + w_} V{B50 - 300}" fill="none" stroke="{RED}" '
                                         f'stroke-width="7" stroke-dasharray="18 12" stroke-linejoin="round"/>', style=""))
    p.parts.append(_g("float", 0, 1, _g("pop", r0 + 1.0, .4, _t(x + w_ / 2, B50 - 312, "?", 120, RED)), style="", amp=8, w=2.6))
    trader(p, 670, B50, .88, "point", (-1 - t0) / p.dur, look=-1, turn=[(r0 + .9, 0)])


def seventy_five(p, seg=None, **_):
    """No, $75. The bar stands at $50 with the dashed $100 START line above; on 'No' a red NO stamp; the $25 rise
    drops onto the bar as a teal block, '+$25' on it, the counter $75; the missing $25 to START outlined in red.
    On the second sentence two sums write themselves out on the right: 50% of $100 = $50 (the fall, red), 50% of
    $50 = $25 (the rise, teal), the two bases ringed."""
    s0, s1 = seg[0][0], seg[1][0]
    x, w_ = 70, 230
    p.parts.append(_g("fade", p.t0, .25, f'<path d="M20 {B50} L780 {B50}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                                         f'<path d="M40 {B50 - 400} H330" stroke="{GREY}" stroke-width="5" stroke-dasharray="14 12"/>'
                      + _t(330, B50 - 412, "START $100", 26, GREY, serif=False, anchor="end") + _money_bar(x, w_, 50), style=""))
    p.parts.append(_g("fade", p.t0, .25, _t(x + w_ / 2, B50 - 50, "$50", 56), style=""))
    # +$25 drops on
    blk = (f'<rect x="{x}" y="{B50 - 300}" width="{w_}" height="100" rx="10" fill="{TEAL}" stroke="{INK}" stroke-width="7"/>'
           + _t(x + w_ / 2, B50 - 233, "+$25", 50, "#fff"))
    p.parts.append(_g("slide", s0 + .35, .45, _g("fade", s0 + .35, .08, blk, style=""), style="", y0=-260, y1=0, ease="out"))
    p.parts.append(_g("draw", s0 + .95, .45, f'<path d="M{x} {B50 - 300} V{B50 - 400} H{x + w_} V{B50 - 300}" fill="none" stroke="{RED}" '
                                            f'stroke-width="7" stroke-dasharray="18 12" stroke-linejoin="round"/>', style=""))
    p.parts.append(_g("pop", s0 + 1.1, .35, _t(x + w_ / 2, B50 - 335, "−$25", 44, RED)))
    # the stamp: NO, $75
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{s0 + .05:.2f}" data-d=".35" data-rot="-8" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="420" y="40" width="330" height="140" rx="16" fill="#fff" fill-opacity=".9" stroke="{RED}" stroke-width="10"/>'
                   + _t(585, 140, "$75", 100, RED) + "</g>")
    # the two sums, written out on the words
    rows = [("50% OF", "$100", "= $50", RED, "THE FALL"), ("50% OF", "$50", "= $25", TEAL, "THE RISE")]
    for j, (a_, b_, c_, col, lab) in enumerate(rows):
        y = 300 + 150 * j
        t = s1 + .15 + .9 * j
        p.parts.append(_g("fade", t, .3, _t(400, y - 52, lab, 26, col, serif=False, anchor="start"), style=""))
        txt = (f'<text x="400" y="{y}" font-family="\'Serif\',serif" font-weight="700" font-size="46" fill="{INK}">'
               f'{H.escape(a_)} <tspan fill="{col}" text-decoration="underline">{H.escape(b_)}</tspan> {H.escape(c_)}</text>')
        p.parts.append(_g("wipe", t, .55, txt, style=""))


def doubles(p, seg=None, lift=None, **_):
    """To get back it has to double. The $50 bar; on 'double' a second $50 block lifts off it and stacks on top,
    a x2 tag swings in, the counter runs $50 to $100 and the START line turns teal with a tick. On the second
    sentence a big teal +100% tag lands and a +50% tag beside it is struck through in red."""
    s0, s1 = seg[0][0], seg[1][0]
    d0 = lift if lift is not None else s0 + (seg[0][1] - s0) * .55
    x, w_ = 90, 230
    p.parts.append(_g("fade", p.t0, .25, f'<path d="M20 {B50} L780 {B50}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                      + _money_bar(x, w_, 50), style=""))
    line = f'<path d="M50 {B50 - 400} H380" stroke-width="6" stroke-dasharray="14 12" stroke="%s"/>'
    p.parts.append(_life(p.t0, d0 + .8 - p.t0, line % GREY + _t(380, B50 - 414, "START $100", 26, GREY, serif=False, anchor="end"), fi=.2, fo=.1))
    p.parts.append(_life(d0 + .7, 99, line % TEAL + _t(380, B50 - 414, "BACK TO $100", 26, TEAL, serif=False, anchor="end"), fi=.15, fo=.1))
    # the copy lifts off and stacks
    copy = _money_bar(x, w_, 50).replace(f'y="{B50 - 200}"', f'y="{B50 - 200}"', 1)
    p.parts.append(_g("slide", d0, .7, _g("fade", d0, .1, copy, style=""), style="", y0=0, y1=-200, ease="inout"))
    p.parts.append(_life(p.t0, d0 + .05 - p.t0, _t(x + w_ / 2, B50 - 50, "$50", 56), fi=.2, fo=.05))
    p.parts.append(_life(d0, 99, _count(x + w_ / 2, B50 - 50, 50, 100, round(d0, 2), .7, size=56, pre="$"), fi=.05, fo=.01))
    p.parts.append(_g("swing", 0, 1, _g("pop", d0 + .3, .4, _ptag(470, B50 - 300, 170, "×2", INK, "#fff", 58)),
                      style="transform-box:view-box;transform-origin:470px 230px", amp=5, w=2.2))
    p.parts.append(_g("pop", d0 + .8, .35, f'<circle cx="420" cy="{B50 - 400}" r="28" fill="#fff" stroke="{INK}" stroke-width="5"/>'
                                          f'<path d="M406 {B50 - 399} l10 11 l20 -22" fill="none" stroke="{TEAL}" stroke-width="8" '
                                          f'stroke-linecap="round" stroke-linejoin="round"/>'))
    # the verdict
    p.parts.append(_g("pop", s1 + .3, .4, _tile(410, 350, 330, 120, TEAL, "+100%", 80)))
    p.parts.append(_g("fade", s1 + .9, .3, _tile(470, 488, 210, 74, "#fff", "+50%", 46, color=GREY), style=""))
    p.parts.append(_g("strike", s1 + 1.2, .3, f'<path d="M455 528 L695 523" stroke="{RED}" stroke-width="10" stroke-linecap="round"/>',
                      style="transform-box:fill-box"))


def same_dollars(p, seg=None, **_):
    """The same $50, two bases. Left: a $100 bar; right: a $50 bar, side by side on one floor. On 'the same both
    ways' a red arrow runs down the left bar's top half and a teal arrow up from the right bar's top to $100, both
    the same length, each with a $50 brace label and an = between them. On 'fifty percent' the left one gets
    '$50 of $100 = 50%'; on 'a hundred percent' the right one gets '$50 of $50 = 100%', each base pulsing."""
    s0, s1, s2 = seg[0][0], seg[1][0], seg[2][0]
    xl, xr, w_ = 60, 450, 220
    p.parts.append(_g("fade", p.t0, .25, f'<path d="M20 {B50} L780 {B50}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>', style=""))
    p.parts.append(_g("growY", p.t0 + .05, .5, _money_bar(xl, w_, 100, fill="#FBE7A1"), style="transform-box:fill-box"))
    p.parts.append(_g("growY", p.t0 + .2, .5, _money_bar(xr, w_, 50), style="transform-box:fill-box"))
    p.parts.append(_g("draw", p.t0 + .3, .4, f'<path d="M{xr} {B50 - 400} H{xr + w_}" stroke="{TEAL}" stroke-width="6" stroke-dasharray="14 12" fill="none"/>', style=""))
    # the left bar's top half fades to a ghost as the arrow runs down it
    a = s0 + .4
    p.parts.append(_g("fade", a + .2, .4, f'<rect x="{xl}" y="{B50 - 400}" width="{w_}" height="200" rx="10" fill="#FFF8EE" '
                                         f'stroke="{RED}" stroke-width="6" stroke-dasharray="18 12"/>', style=""))
    for (x, y0, y1, col) in ((xl + w_ / 2, B50 - 390, B50 - 210, RED), (xr + w_ / 2, B50 - 210, B50 - 390, TEAL)):
        b1, b2 = _arrow(x, y0, y1, col, 16)
        p.parts.append(_g("draw", a, .5, b1, style=""))
        p.parts.append(_g("draw", a + .45, .2, b2, style=""))
    for x in (xl + w_ + 20, xr - 20):
        side = 1 if x < 400 else -1
        p.parts.append(_g("draw", a + .55, .3, f'<path d="M{x} {B50 - 400} q{side * 22} 0 {side * 22} 22 v56 q0 22 {side * 22} 22 '
                                              f'q{-side * 22} 0 {-side * 22} 22 v56 q0 22 {-side * 22} 22" fill="none" stroke="{INK}" '
                                              f'stroke-width="5"/>', style=""))
    p.parts.append(_g("pop", a + .75, .35, _t(400, B50 - 280, "$50", 46) + _t(400, B50 - 330, "=", 60, GREY)))
    # the two readings
    p.parts.append(_g("pop", s1 + .2, .4, _tile(xl - 10, 10, w_ + 20, 100, RED, "50%", 68)))
    p.parts.append(_g("fade", s1 + .5, .3, _t(xl + w_ / 2, 150, "$50 OF $100", 32, RED, serif=False), style=""))
    p.parts.append(_g("pop", s2 + .3, .4, _tile(xr - 10, 10, w_ + 20, 100, TEAL, "100%", 68)))
    p.parts.append(_g("fade", s2 + .6, .3, _t(xr + w_ / 2, 150, "$50 OF $50", 32, TEAL, serif=False), style=""))
    for t, x, h_, col in ((s1 + .6, xl, 400, RED), (s2 + .7, xr, 200, TEAL)):
        p.parts.append(_life(t, .9, _g("pop", t, .3, f'<rect x="{x - 10}" y="{B50 - h_ - 10}" width="{w_ + 20}" height="{h_ + 10}" '
                                                      f'rx="14" fill="none" stroke="{col}" stroke-width="7"/>'), fi=.08, fo=.3))


LADDER = ((10, 100 / 9), (25, 100 / 3), (50, 100.0), (80, 400.0))   # loss, gain needed = 1 / (1 - loss) - 1


def ladder(p, seg=None, **_):
    """The loss-to-gain ladder: four pairs on one honest scale (0.92 px a percentage point, losses and gains alike). On 'the deeper the fall' the
    four red losses drop below the line one after another (10, 25, 50, 80); on 'down ten' the first teal gain
    grows to about 11%; the next two follow on the gap; on 'down eighty' the last one shoots up to 400%, a thump,
    and its label lands at the top."""
    s0, s1, s2 = seg[0][0], seg[1][0], seg[2][0]
    base, k = 450, .92
    xs = (110, 300, 490, 680)
    p.parts.append(_g("fade", p.t0, .25, f'<path d="M20 {base} L780 {base}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                      + _t(30, base + 150, "LOSS", 28, RED, serif=False, anchor="start")
                      + _t(30, 40, "GAIN NEEDED TO GET BACK", 28, TEAL, serif=False, anchor="start"), style=""))
    times = (s1 + .35, seg[1][1] - .1, seg[1][1] + .25, s2 + .55)
    for j, ((loss, gain), x) in enumerate(zip(LADDER, xs)):
        tl = s0 + .2 + .3 * j
        hl = loss * k
        p.parts.append(_g("growYdown", tl, .4, f'<rect x="{x - 62}" y="{base}" width="56" height="{hl:.0f}" rx="6" fill="{RED}" '
                                               f'stroke="{INK}" stroke-width="5"/>', style="transform-box:fill-box"))
        p.parts.append(_g("fade", tl + .3, .3, _t(x - 34, base + hl + 44, f"−{loss}%", 34, RED), style=""))
        hg = gain * k
        tg = times[j]
        p.parts.append(_g("growY", tg, .45 if j < 3 else .7, f'<rect x="{x + 6}" y="{base - hg:.0f}" width="56" height="{hg:.0f}" rx="6" '
                                                           f'fill="{TEAL}" stroke="{INK}" stroke-width="5"/>', style="transform-box:fill-box"))
        lab = f"+{gain:.0f}%" if j != 0 else "+11%"
        p.parts.append(_g("pop", tg + (.35 if j < 3 else .65), .3, _t(x + 34, base - hg - 16, lab, 36 if j < 3 else 46, TEAL)))


def _crisis_y(v):
    return 560 - (v - 600) / 1100 * 400


def crisis_path(p, seg=None, **_):
    """The 2007 to 2013 round trip of the S&P 500 (three real closes; the path between them is drawn smooth, not
    data). On the first sentence the red line falls from the October 2007 high (1,565) to the March 2009 low (677)
    and -57% counts on; on the second a dashed record line runs across at 1,565 and the teal line climbs back from
    the low as +131% counts; on 'March 2013' it reaches the line, a calendar tag drops on the point and ticks."""
    s0, s1, s2 = seg[0][0], seg[1][0], seg[2][0]
    yrs = lambda y: 90 + y * 620 / 5.47
    P0, P1, P2 = (yrs(0), _crisis_y(1565)), (yrs(1.42), _crisis_y(677)), (yrs(5.47), _crisis_y(1569))
    p.parts.append(_g("fade", p.t0, .25, f'<path d="M40 600 L780 600" stroke="{INK}" stroke-width="5"/>'
                      + _t(40, 630, "S&P 500 CLOSES (WIKIPEDIA, NPR), PATH SIMPLIFIED", 24, GREY, serif=False, anchor="start", weight=600), style=""))
    # fall
    down = (f'M{P0[0]:.0f} {P0[1]:.0f} C{P0[0] + 50:.0f} {P0[1] + 30:.0f}, {P0[0] + 70:.0f} {P0[1] + 120:.0f}, '
            f'{P0[0] + 100:.0f} {P0[1] + 170:.0f} S{P1[0] - 20:.0f} {P1[1] - 10:.0f}, {P1[0]:.0f} {P1[1]:.0f}')
    p.parts.append(_g("draw", s0 + .3, 1.6, f'<path d="{down}" fill="none" stroke="{RED}" stroke-width="10" stroke-linecap="round"/>', style=""))
    p.parts.append(_g("pop", s0 + .1, .3, f'<circle cx="{P0[0]:.0f}" cy="{P0[1]:.0f}" r="13" fill="{INK}"/>'
                      + _t(P0[0] - 10, P0[1] - 60, "OCT 2007", 26, GREY, serif=False, anchor="start")
                      + _t(P0[0] - 10, P0[1] - 24, "1,565", 36, INK, anchor="start")))
    p.parts.append(_g("pop", s0 + 1.9, .3, f'<circle cx="{P1[0]:.0f}" cy="{P1[1]:.0f}" r="13" fill="{RED}"/>'
                      + _t(P1[0], P1[1] + 46, "MAR 2009 · 677", 26, GREY, serif=False)))
    p.parts.append(_life(s0 + 1.0, 99, _count(P1[0] - 150, P1[1] - 40, 0, -57, round(s0 + 1.0, 2), 1.0, size=64, color=RED, suf="%"),
                         fi=.1, fo=.01))
    # the record line and the climb back
    p.parts.append(_g("draw", s1 + .1, .6, f'<path d="M{P0[0]:.0f} {P0[1]:.0f} H{P2[0] + 20:.0f}" fill="none" stroke="{TEAL}" '
                                          f'stroke-width="5" stroke-dasharray="14 12"/>', style=""))
    up = (f'M{P1[0]:.0f} {P1[1]:.0f} C{P1[0] + 60:.0f} {P1[1] - 20:.0f}, {P1[0] + 90:.0f} {P1[1] - 130:.0f}, {P1[0] + 170:.0f} '
          f'{P1[1] - 150:.0f} S{P1[0] + 260:.0f} {P1[1] - 200:.0f}, {P1[0] + 330:.0f} {P1[1] - 250:.0f} S{P2[0] - 40:.0f} '
          f'{P2[1] + 30:.0f}, {P2[0]:.0f} {P2[1]:.0f}')
    climb = max(s2 + .3 - (s1 + .4), 2.2)                  # reaches the record as 'March 2013' is said
    p.parts.append(_g("draw", s1 + .4, climb, f'<path d="{up}" fill="none" stroke="{TEAL}" stroke-width="10" stroke-linecap="round"/>',
                      style="", lin=1))
    p.parts.append(_life(s1 + .6, 99, _count(P2[0] - 70, P1[1] - 20, 0, 131, round(s1 + .6, 2), climb - .4, size=64, color=TEAL,
                                             pre="+", suf="%"), fi=.1, fo=.01))
    # March 2013: the tag lands where the line meets the record
    tag_t = s1 + .4 + climb
    p.parts.append(_g("slide", tag_t, .4, _g("fade", tag_t, .08,
                                              f'<rect x="{P2[0] - 160:.0f}" y="{P2[1] - 120:.0f}" width="170" height="86" rx="12" fill="#fff" '
                                              f'stroke="{INK}" stroke-width="5"/><rect x="{P2[0] - 160:.0f}" y="{P2[1] - 120:.0f}" width="170" '
                                              f'height="28" rx="10" fill="{TEAL}"/>'
                                              + _t(P2[0] - 75, P2[1] - 50, "MAR 2013", 30, INK), style=""),
                      style="", y0=-120, y1=0, ease="out"))
    p.parts.append(_g("pop", tag_t + .35, .3, f'<circle cx="{P2[0]:.0f}" cy="{P2[1]:.0f}" r="22" fill="#fff" stroke="{INK}" stroke-width="5"/>'
                                            f'<path d="M{P2[0] - 11:.0f} {P2[1]:.0f} l8 9 l16 -18" fill="none" stroke="{TEAL}" stroke-width="7" '
                                            f'stroke-linecap="round" stroke-linejoin="round"/>'))


def fifty_asks(p, **_):
    """The close: the trader points; the bubble reads -50% +50% = $100? with the $100 struck to $75."""
    p.fill(f'<path d="M110 60 H540 Q580 60 580 100 V300 Q580 340 540 340 H340 L290 410 L300 340 H110 Q70 340 70 300 V100 '
           f'Q70 60 110 60 Z" fill="#fff" stroke="{INK}" stroke-width="7"/>', .1)
    p.text(325, 175, "−50% +50%", .25, size=70, serif=True, weight=700, color=INK, fx="pop")
    p.text(325, 290, "= $75", .45, size=96, serif=True, weight=700, color=RED, fx="pop")
    trader(p, 700, 630, .95, "point", .05, look=-1, turn=[(p.at(.15), 0)])


SCENES.update({f.__name__: f for f in (half_hook, seventy_five, doubles, same_dollars, ladder, crisis_path, fifty_asks)})


# ---- 16 Nov scenes (Levels #15, a loan through the three statements). The 15 Nov Reel's next improvement: each
# drawing keeps an idle life between its cues (notes keep travelling, the bag bobs, the beam sways a degree, the
# question mark bobs, tags swing), and every key move is placed on its word (m["qw"], m["aw"]: the word moments
# levels.py now keeps, the same spread as the karaoke). Generic shapes of our own: no bank, company or logo. Only
# the episode's worked numbers ($100 loan, 10% interest, 25% tax, $7.50, $2.50).

def _wt(m, w, which="aw", sent=None, default=None, after=0.0):
    """The moment of a word in the level (see levels.word); default if it is not there."""
    rows = m.get(which) or []
    rows = rows if sent is None else rows[sent:sent + 1]
    for row in rows:
        for x, t in row:
            if x == w.lower() and t >= after:
                return t
    if default is None:
        raise KeyError(f"word {w!r} not in {which}")
    return default


def _idle(fx, inner, amp, w, ph=0.0, style="transform-box:fill-box;transform-origin:center"):
    """A drawing part that never stops moving (motion.py float, swing, breathe, bob), for the gaps between cues."""
    return f'<g class="a" data-fx="{fx}" data-at="0" data-d="1" data-amp="{amp}" data-w="{w}" data-ph="{ph}" style="{style}">{inner}</g>'


def _small_bank(x, base, label="LENDER"):
    """A small columned bank front, x its left edge (208 wide), standing on base; a pennant on the roof."""
    s = (f'<path d="M{x + 4} {base - 208} L{x + 104} {base - 262} L{x + 204} {base - 208} Z" fill="{INK}"/>'
         + "".join(f'<rect x="{x + 22 + 46 * k}" y="{base - 198}" width="22" height="160" fill="#E8E4DE" stroke="{INK}" stroke-width="4"/>'
                   for k in range(4))
         + f'<rect x="{x}" y="{base - 38}" width="208" height="38" fill="{INK}"/>'
         + f'<path d="M{x + 104} {base - 262} L{x + 104} {base - 312}" stroke="{INK}" stroke-width="5"/>')
    flag = _idle("swing", f'<path d="M{x + 106} {base - 312} L{x + 160} {base - 298} L{x + 106} {base - 284} Z" fill="{RED}" stroke="{INK}" '
                          f'stroke-width="3"/>', 14, 3.4, style=f"transform-box:view-box;transform-origin:{x + 106}px {base - 298}px")
    return s + flag + _t(x + 104, base - 9, label, 26, "#fff", serif=False)


def _page_is(x, y, w_=230, h_=270, title="INCOME", sub="STATEMENT"):
    """An income statement page: a title, five greeked lines (no legible figures)."""
    s = (f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="8" fill="#FFFDF7" stroke="{INK}" stroke-width="6"/>'
         + _t(x + w_ / 2, y + 44, title, 30, INK, serif=False) + _t(x + w_ / 2, y + 76, sub, 22, INK, serif=False, weight=600))
    for k in range(5):
        s += (f'<path d="M{x + 24} {y + 112 + 30 * k} L{x + w_ - 80 + (k % 2) * 20} {y + 112 + 30 * k}" stroke="{INK}" stroke-opacity=".28" '
              f'stroke-width="7" stroke-linecap="round"/>')
    return s


def loan_in(p, m=None, amount=100, **_):
    """Level 1, is a loan income? A lender stands on the left, the company in the middle. On 'borrows' the lender
    slides in; on '$100' a $100 sack travels to the company and waits there, bobbing, while notes keep moving
    across through the question and the clock. On 'income?' an INCOME STATEMENT page slides in on the right with a
    question mark bobbing over it. On 'No.' a NOT INCOME stamp lands on the page; on 'cash' a CASH +$100 tag drops
    onto the company and on 'debt' a DEBT +$100 tag beside it (both swing a little after); on 'doesn't move' the
    page gets a teal $0 and a tick."""
    base = 560
    t_b = _wt(m, "borrows", "qw", default=m["qs"][0][0] + .3)
    t_100 = _wt(m, f"${amount}", "qw", default=t_b + .6)
    t_inc = _wt(m, "income", "qw", default=m["qs"][-1][0] + .3)
    a = m["a"]
    p.parts.append(_g("fade", p.t0, .3, f'<path d="M0 {base} L960 {base}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                      + _office(250, base, 200, 250) + _t(350, base - 253, "COMPANY", 22, "#fff", serif=False)))
    _slide(p, _abs(p, t_b - .1), _small_bank(10, base), x0=-300, d=.55)
    # the sack: from the lender to the company's door, then bobbing beside it until the answer
    sack = _bag(0, 0, 120, f"${amount}", fill=TEAL)
    p.parts.append(_life(t_100 - .05, a + .6 - t_100,
                         _g("slide", t_100, .7, _idle("bob", f'<g transform="translate(114 380)">{sack}</g>', 14, 2.8, style=""),
                            style="", x0=0, x1=150, y0=0, y1=8, ease="inout"), fi=.12, fo=.25))
    # notes keep travelling from the lender to the company through the question and the clock (idle life)
    t, k = t_100 + .8, 0
    while t < a - .3:
        note = _note(150, 330 + 18 * (k % 3), 90, 42)
        p.parts.append(_life(t, .95, _g("slide", t, .85, note, style="", x0=0, x1=150, y0=0, y1=-6, ease="inout"), fi=.12, fo=.18))
        t += .4
        k += 1
    # the income statement page and its question
    page = _idle("swing", _page_is(480, 250, 210, 270), 3.5, 2.0, style="transform-box:view-box;transform-origin:585px 250px")
    _slide(p, _abs(p, t_inc - .25), page, x0=300, d=.5)
    p.parts.append(_life(t_inc + .2, a - t_inc - .05, _idle("bob", _t(585, 440, "?", 120, RED), 16, 3.2, style="")))
    # the answer
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{a + .05:.2f}" data-d="0.35" data-rot="-10" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="485" y="330" width="200" height="84" rx="10" fill="#FFFDF7" fill-opacity=".85" stroke="{RED}" stroke-width="8"/>'
                   + _t(585, 366, "NOT", 34, RED) + _t(585, 402, "INCOME", 34, RED) + '</g>')
    t_cash = _wt(m, "cash", default=a + 1.2)
    t_debt = _wt(m, "debt", default=t_cash + .5)
    for tt, y, lab, fill, col in ((t_cash, 330, "CASH", CASH_C, INK), (t_debt, 460, "DEBT", DEBT_C, "#fff")):
        x = 840
        tag = _idle("swing", _ptag(x, y, 240, f"{lab} +${amount}", fill, col, 30), 6, 2.4, ph=y / 90,
                    style=f"transform-box:view-box;transform-origin:{x - 120}px {y}px")
        p.parts.append(_g("fade", tt - .02, .12, _g("slide", tt - .02, .4, tag, style="", x0=0, x1=0, y0=-120, y1=0, ease="out"), style=""))
    t_mv = _wt(m, "move", default=m["as_"][-1][0] + .6) if len(m["as_"]) > 2 else m["end"] - .8
    p.parts.append(_g("pop", t_mv - .1, .35, f'<circle cx="676" cy="266" r="30" fill="#fff" stroke="{INK}" stroke-width="5"/>'
                                             f'<path d="M662 267 l10 11 l20 -22" fill="none" stroke="{TEAL}" stroke-width="8" '
                                             f'stroke-linecap="round" stroke-linejoin="round"/>'))
    p.parts.append(_g("pop", t_mv - .25, .35, _t(585, 500, "$0", 56, TEAL)))


def loan_in_fx(m, amount=100):
    """The sounds of loan_in, on the same words: the sack lands (a soft mallet), the stamp (a hit), the tags (clinks)."""
    t_100 = _wt(m, f"${amount}", "qw", default=m["qs"][0][0] + .9)
    t_cash, t_debt = _wt(m, "cash", default=m["a"] + 1.2), _wt(m, "debt", default=m["a"] + 1.7)
    return [("hit", t_100 + .68, .25, 0, dict(pitch=220)), ("hit", m["a"] + .12, .32, 0, dict(pitch=147)),
            ("clink", t_cash + .32, .22, -.3), ("clink", t_debt + .32, .22, .3)]


def interest_bite(p, m=None, rate=10, tax=25, **_):
    """Level 2, how much does net income fall? A tall NET INCOME bar. On '10%' the top $10 of it turns red and slides
    out to the right as INTEREST -$10 (a dashed outline left behind). On '25%' a teal $2.50 piece (TAX SAVED) comes
    back off the red block onto the bar. Through 'how much ... fall?' and the clock a bracket shows the gap with a
    bobbing question mark; the red block bobs and the teal piece breathes. On the answer the gap fills red and counts
    to -$7.50; on '$10' and '$2.50' the two pieces are ringed in turn. Scale: 12 px a dollar of the change."""
    k = 12
    base, top, x, cw = 545, 120, 70, 220
    bite, back = rate * k, round(rate * tax / 100 * k)
    t_r = _wt(m, f"{rate}%", "qw", default=m["qs"][0][0] + .6)
    t_t = _wt(m, f"{tax}%", "qw", default=(m["qs"][1][0] + .4) if len(m["qs"]) > 1 else t_r + 1.2)
    t_f = _wt(m, "fall", "qw", default=m["qs"][-1][0] + .6)
    a = m["a"]
    p.parts.append(_g("fade", p.t0, .3, f'<path d="M0 {base} L800 {base}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'))
    # the bar below the bite, there from the start (it breathes a little until the bite)
    p.parts.append(_g("growY", p.t0 + .1, .55, f'<rect x="{x}" y="{top + bite}" width="{cw}" height="{base - top - bite}" rx="8" fill="{GOLD}" '
                                              f'stroke="{INK}" stroke-width="6"/>', style="transform-box:fill-box"))
    p.parts.append(_g("fade", p.t0 + .5, .3, _t(x + cw / 2, base - 70, "NET", 36, INK, serif=False) + _t(x + cw / 2, base - 28, "INCOME", 36, INK, serif=False)))
    # the top $10: gold until the rate is said, then red and out to the right
    gold_top = f'<rect x="{x}" y="{top}" width="{cw}" height="{bite}" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
    p.parts.append(_life(p.t0 + .1, t_r + .2 - p.t0, _g("growY", p.t0 + .1, .55, gold_top, style="transform-box:fill-box"), fi=.05, fo=.1))
    p.parts.append(_g("draw", t_r + .15, .4, f'<path d="M{x} {top} L{x + cw} {top} L{x + cw} {top + bite} L{x} {top + bite} Z" fill="none" '
                                             f'stroke="{INK}" stroke-width="4" stroke-dasharray="12 9"/>', style=""))
    red = (f'<rect x="{x}" y="{top}" width="{cw}" height="{bite}" rx="8" fill="{RED}" stroke="{INK}" stroke-width="6"/>'
           + _t(x + cw / 2, top + bite / 2 + 15, f"−${rate}", 44, "#fff"))
    mv = 400
    p.parts.append(_g("fade", t_r - .05, .15, _g("slide", t_r + .1, .7, _idle("bob", red, 12, 2.5, style=""), style="", x0=0, x1=mv, y0=0, y1=-10,
                                                ease="inout"), style=""))
    p.parts.append(_g("fade", t_r + .6, .3, _t(x + mv + cw / 2, top - 30, "INTEREST", 38, RED, serif=False)))
    # the tax saved: a teal piece leaves the red block and settles back on the bar
    piece = (f'<rect x="{x + mv}" y="{top + bite - back}" width="{cw}" height="{back}" rx="5" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>')
    p.parts.append(_g("fade", t_t - .1, .15, _g("slide", t_t, .8, _idle("breathe", piece, .09, 3.4), style="", x0=0, x1=-mv, y0=0, y1=0,
                                                 ease="inout"), style=""))
    p.parts.append(_g("pop", t_t + .7, .3, _ptag(x + cw + 150, top + bite + 70, 270, "TAX +$2.50", TEAL, "#fff", 34)))
    # the question: a bracket on the gap, a bobbing ?
    gy0, gy1 = top, top + bite - back
    p.parts.append(_life(t_f - .1, a - t_f + .3,
                         f'<path d="M{x + cw + 18} {gy0} L{x + cw + 40} {gy0} L{x + cw + 40} {gy1} L{x + cw + 18} {gy1}" fill="none" stroke="{RED}" '
                         f'stroke-width="7" stroke-linecap="round"/>'
                         + _idle("bob", _t(x + cw + 90, (gy0 + gy1) / 2 + 40, "?", 110, RED), 16, 3.2, style="")))
    # the answer: the gap fills red and counts to -$7.50
    p.parts.append(_g("growYdown", a + .05, .5, f'<rect x="{x}" y="{gy0}" width="{cw}" height="{gy1 - gy0}" rx="8" fill="{RED}" fill-opacity=".22" '
                                                f'stroke="{RED}" stroke-width="6"/>', style="transform-box:fill-box"))
    p.parts.append(_count(x + cw / 2, round((gy0 + gy1) / 2 + 20), 0, 7.5, round(a + .1, 2), .8, size=56, color=RED, pre="−$", dec=2))
    if len(m["as_"]) > 1:
        t10 = _wt(m, f"${rate}", sent=1, default=m["as_"][1][0] + .1)
        t25 = _wt(m, "$2.50", sent=1, default=m["as_"][1][1] - .4)
        for tt, y, h_, xx in ((t10, top - 10, bite + 20, x + mv - 10), (t25, top + bite - back - 10, back + 20, x - 10)):
            ring = f'<rect x="{xx}" y="{y}" width="{cw + 20}" height="{h_}" rx="12" fill="none" stroke="{TEAL}" stroke-width="7"/>'
            p.parts.append(_life(tt - .05, .85, _g("pop", tt - .05, .3, ring), fi=.08, fo=.25))


def interest_bite_fx(m, rate=10, tax=25):
    t_r = _wt(m, f"{rate}%", "qw", default=m["qs"][0][0] + .6)
    t_t = _wt(m, f"{tax}%", "qw", default=t_r + 1.2)
    return [("hit", t_r + .75, .26, 0, dict(pitch=175)), ("clink", t_t + .78, .2, -.2), ("hit", m["a"] + .1, .28, 0, dict(pitch=262))]


def bs_tilt(p, m=None, amt="$7.50", **_):
    """Level 3, what balances the drop in cash? A balance sheet as a balance: ASSETS on the left pan (a CASH block),
    LIABILITIES + EQUITY on the right (DEBT under EQUITY). On 'down' the cash block shrinks by the $7.50 and the
    beam tips (the left side lighter); through the question and the clock it sways about a degree around the tip
    and a question mark bobs over the equity block. On 'Equity.' the equity block glows; on 'drop' it shrinks by
    the same $7.50 and the beam comes back level; a = lands between the pans."""
    qs, a = m["qs"], m["a"]
    t_dn = _wt(m, "down", "qw", default=qs[0][0] + (qs[0][1] - qs[0][0]) * .7)
    t_dr = _wt(m, "drop", default=(m["as_"][1][0] + .5) if len(m["as_"]) > 1 else a + 1.0)
    cx, cy, half = 400, 300, 280
    rot = 6.0
    p.parts.append(_g("fade", p.t0, .3,
                      f'<path d="M{cx} {cy} L{cx - 64} 590 L{cx + 64} 590 Z" fill="{INK}"/>'
                      f'<path d="M60 590 L740 590" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                      + _t(cx - half, 130, "ASSETS", 32, INK, serif=False) + _t(cx + half, 112, "LIABILITIES", 28, INK, serif=False)
                      + _t(cx + half, 146, "+ EQUITY", 28, INK, serif=False)))
    # the beam's angle through the level: level, tip on 'down', sway a degree while waiting, level again on 'drop'
    ang = [(0, 0), (t_dn + .2, 0), (t_dn + .9, rot)]
    t, j = t_dn + 1.5, 0
    while t < t_dr - .2:
        ang.append((round(t, 2), rot + (2.2 if j % 2 == 0 else -2.2)))
        t += .6
        j += 1
    ang += [(round(t_dr + .2, 2), rot), (round(t_dr + 1.0, 2), 0)]
    t, j = t_dr + 1.6, 0
    while t < m["end"] + .3:                      # and after, a slow settle
        ang.append((round(t, 2), 1.4 if j % 2 == 0 else -1.4))
        t += 1.1
        j += 1
    keys = [[round(t_, 2), 0, 0, 1, 1, r] for t_, r in ang]
    p.parts.append(f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json(keys))}" '
                   f'style="transform-box:view-box;transform-origin:{cx}px {cy}px">'
                   f'<rect x="{cx - half - 20}" y="{cy - 10}" width="{2 * half + 40}" height="20" rx="10" fill="{INK}"/>'
                   f'<circle cx="{cx}" cy="{cy}" r="18" fill="{GOLD}" stroke="{INK}" stroke-width="5"/></g>')
    k_ = 2.0            # px per $ of the blocks; the $7.50 shown as 15 px x 4 (made visible: a schematic, not to scale)
    drop = 60

    def pan(x, sign, inner):
        kk = [[t_, 0, round(sign * half * math.sin(math.radians(r)), 1), 1, 1, 0] for t_, r in ang]
        body = (f'<path d="M{x} {cy} L{x - 100} 460 M{x} {cy} L{x + 100} 460" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M{x - 120} 460 L{x + 120} 460 Q{x} 510 {x - 120} 460 Z" fill="#E8E1D4" stroke="{INK}" stroke-width="5"/>' + inner)
        p.parts.append(f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json(kk))}">{body}</g>')
    # left: CASH, shrinks on 'down'
    lx, rx = cx - half, cx + half
    cash_h = 170
    cash = (f'<g class="a" data-fx="scaleY" data-at="{t_dn:.2f}" data-d="0.6" data-s0="1" data-s1="{(cash_h - drop) / cash_h:.3f}" '
            f'style="transform-box:fill-box;transform-origin:center bottom">'
            f'<rect x="{lx - 85}" y="{460 - cash_h}" width="170" height="{cash_h}" rx="8" fill="{CASH_C}" stroke="{INK}" stroke-width="5"/></g>'
            + _g("fade", p.t0 + .3, .3, _t(lx, 445, "CASH", 30, INK, serif=False)))
    cash += _g("pop", t_dn + .4, .3, _ptag(lx + 10, 460 - cash_h - 10, 180, f"−{amt}", RED, "#fff", 28))
    pan(lx, -1, cash)
    # right: DEBT (stays) under EQUITY (shrinks on 'drop')
    debt_h, eq_h = 90, 110
    eq_top = 460 - debt_h - eq_h
    right = (f'<rect x="{rx - 85}" y="{460 - debt_h}" width="170" height="{debt_h}" rx="8" fill="{DEBT_C}" stroke="{INK}" stroke-width="5"/>'
             + _t(rx, 460 - debt_h / 2 + 11, "DEBT", 30, "#fff", serif=False)
             + f'<g class="a" data-fx="scaleY" data-at="{t_dr:.2f}" data-d="0.6" data-s0="1" data-s1="{(eq_h - drop) / eq_h:.3f}" '
               f'style="transform-box:fill-box;transform-origin:center bottom">'
               f'<rect x="{rx - 85}" y="{eq_top}" width="170" height="{eq_h}" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="5"/></g>'
             + _g("fade", p.t0 + .3, .3, _t(rx, 460 - debt_h - 18, "EQUITY", 28, INK, serif=False)))
    right += _life(a, t_dr - a + .1, _g("pop", a, .3, f'<rect x="{rx - 95}" y="{eq_top - 10}" width="190" height="{eq_h + 20}" rx="12" '
                                                    f'fill="none" stroke="{TEAL}" stroke-width="8"/>'), fi=.06, fo=.2)
    right += _g("pop", t_dr + .4, .3, _ptag(rx + 10, eq_top - 40, 180, f"−{amt}", RED, "#fff", 28))
    right += _life(m["think"] - .3, a - m["think"] + .3, _idle("bob", _t(rx, eq_top - 40, "?", 110, RED), 16, 3.2, style=""))
    pan(rx, 1, right)
    p.parts.append(_g("pop", t_dr + 1.0, .35, _t(cx, 250, "=", 90, TEAL)))


def bs_tilt_fx(m):
    t_dn = _wt(m, "down", "qw", default=m["qs"][0][0] + 1.0)
    t_dr = _wt(m, "drop", default=m["a"] + 1.0)
    return [("clank", t_dn + .85, .16, -.3), ("hit", t_dn + .45, .2, -.3, dict(pitch=196)), ("hit", t_dr + .45, .22, .3, dict(pitch=196)),
            ("clank", t_dr + .95, .14, 0)]


SCENES.update({f.__name__: f for f in (loan_in, interest_bite, bs_tilt)})


# ---- 17 Nov (the coin toss Short, Format F, a choice): heads win $150, tails lose $100; the average of +$25 a toss;
# why most people still say no (Kahneman: to risk $100 most want a chance at about $200); Samuelson's colleague, who
# refused one toss at $200 to $100 but would take a hundred; what a hundred tosses look like (our binomial
# arithmetic). Generic shapes of our own: no coin design of any country, no real person's likeness (Samuelson is a
# plain stick figure in a labelled reconstruction).

BET_SCALE = 1.9                           # px a dollar in the average drawing


def _coin_shape(cx, cy, r, value="$", metal="gold"):
    """coin()'s shaded coin as a plain SVG string (no animation of its own)."""
    class _P:
        parts = []

        def at(self, f):
            return 0

        def fill(self, shape, *a, **k):
            self.shape = shape
    q = _P()
    coin(q, cx, cy, r, value, metal)
    return q.shape


def _toss(cx, cy, r, t, h=240, d=.9, turns=4, value="$"):
    """A coin tossed at t: it flies up h px and lands again over d s, spinning turns times on its axis."""
    kf = H.escape(_json([[round(t, 2), 0, 0, 1, 1], [round(t + d * .45, 2), 0, -h, 1, 1], [round(t + d, 2), 0, 0, 1, 1]]))
    spin = (f'<g class="a" data-fx="coinflip" data-at="{t:.2f}" data-d="{d}" data-turns="{turns}" '
            f'style="transform-box:fill-box;transform-origin:center">{_coin_shape(cx, cy, r, value)}</g>')
    return f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{kf}">{spin}</g>'


def _bet_tiles(heads_x=40, tails_x=500, y=60, w_=260, h_=150, size=72):
    return (_t(heads_x + w_ / 2, y - 26, "HEADS", 30, TEAL, serif=False)
            + _tile(heads_x, y, w_, h_, TEAL, "+$150", size)
            + _t(tails_x + w_ / 2, y - 26, "TAILS", 30, RED, serif=False)
            + _tile(tails_x, y, w_, h_, RED, "−$100", size))


def toss_hook(p, seg=None, **_):
    """The hook. From frame 0: HEADS +$150 and TAILS -$100 tiles, a gold coin on the floor, the trader beside it.
    On 'Heads' the coin is tossed (up, spinning) and lands as the HEADS tile presses with a teal ring; on 'Tails' it
    is tossed again and lands as the TAILS tile presses with a red ring; on 'Do you take it?' the trader turns to the
    viewer, palms up, and YES? and NO? chips pop either side of the coin, the ? bobbing."""
    s0, s1, s2 = seg[0][0], seg[1][0], seg[2][0]
    _set(p, f'<path d="M20 590 L780 590" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' + _bet_tiles())
    cx, cy, r = 400, 510, 72
    t1, t2, d = s0 + .05, s1 + .05, .95
    kf = lambda t: H.escape(_json([[round(t, 2), 0, 0, 1, 1], [round(t + d * .45, 2), 0, -240, 1, 1], [round(t + d, 2), 0, 0, 1, 1]]))
    spin = lambda t: (f'<g class="a" data-fx="coinflip" data-at="{t:.2f}" data-d="{d}" data-turns="5" '
                      f'style="transform-box:fill-box;transform-origin:center">{_coin_shape(cx, cy, r, "$")}</g>')
    # one coin: still on the floor from frame 0, spinning up and down on each toss (coinflip hides a coin before its
    # start, so each toss has its own copy, handed over the moment the next one starts)
    coin_ = (_life(-1, t1 + 1.01, _coin_shape(cx, cy, r, "$"), fi=.01, fo=.01) + _life(t1, t2 - t1 + .01, spin(t1), fi=.01, fo=.01)
             + _life(t2, 99, spin(t2), fi=.01, fo=.01))
    p.parts.append(f'<ellipse cx="{cx}" cy="584" rx="64" ry="10" fill="{INK}" fill-opacity=".18"/>'
                   f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{kf(t2)}">'
                   f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{kf(t1)}">{coin_}</g></g>')
    # each landing presses its tile and rings it
    for t, x, col in ((t1 + d, 40, TEAL), (t2 + d, 500, RED)):
        p.parts.append(_g("draw", t, .45, f'<rect x="{x - 12}" y="48" width="284" height="174" rx="30" fill="none" stroke="{col}" '
                                        f'stroke-width="9"/>', style=""))
    # the question: YES? NO?
    p.parts.append(_g("pop", s2 + .15, .35, _tile(110, 300, 150, 92, "#fff", "YES", 46, color=TEAL)))
    p.parts.append(_g("pop", s2 + .35, .35, _tile(520, 300, 150, 92, "#fff", "NO", 46, color=RED)))
    p.parts.append(_g("float", 0, 1, _g("pop", s2 + .55, .4, _t(cx, 300, "?", 120, RED)), style="", amp=8, w=2.6))
    trader(p, 720, 590, .62, "shrug", (-1 - p.t0) / p.dur, look=-1, turn=[(s2 + .1, 0)])


def bet_average(p, seg=None, **_):
    """The average. A zero line; on 'win a hundred and fifty' a teal bar grows up to +$150, on 'lose a hundred' a red
    bar grows down to -$100 (one scale, 1.9 px a dollar). On the second sentence both halve (x1/2 tags, counters 150
    to 75 and 100 to 50) and the sums wipe on at the right: 1/2 of $150 = $75, 1/2 of $100 = $50, then $25 A TOSS
    lands as a stamp on 'twenty five'."""
    s0, e0, s1, e1 = seg[0][0], seg[0][1], seg[1][0], seg[1][1]
    z, k = 330, BET_SCALE
    xt, xr, w_ = 50, 200, 120
    g_up, g_dn = s0 + .25, s0 + (e0 - s0) * .55
    half = s1 + .1
    p.parts.append(_g("fade", p.t0, .25, f'<path d="M30 {z} H360" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                      + _t(30, z - 14, "$0", 26, GREY, serif=False, anchor="start"), style=""))
    up = f'<rect x="{xt}" y="{z - 150 * k}" width="{w_}" height="{150 * k}" rx="10" fill="{TEAL}" stroke="{INK}" stroke-width="7"/>'
    dn = f'<rect x="{xr}" y="{z - 100 * k}" width="{w_}" height="{100 * k}" rx="10" fill="{RED}" stroke="{INK}" stroke-width="7"/>'
    grow = lambda t, inner, s1_: _g("scaleY", t, .6, _g("scaleY", half, .7, inner, style="transform-box:fill-box", s0=1, s1=.5),
                                     style="transform-box:fill-box", s0=.001, s1=1)
    p.parts.append(grow(g_up, up, 1))
    p.parts.append(f'<g transform="translate(0 {2 * z}) scale(1 -1)">{grow(g_dn, dn, 1)}</g>')
    p.parts.append(_life(g_up + .3, half - g_up - .25, _t(xt + w_ / 2, z - 30, "+$150", 40, "#fff"), fi=.2, fo=.05))
    p.parts.append(_life(half, 99, _count(xt + w_ / 2, z - 30, 150, 75, round(half, 2), .7, size=40, color="#fff", pre="+$"), fi=.05, fo=.01))
    p.parts.append(_life(g_dn + .3, half - g_dn - .25, _t(xr + w_ / 2, z + 55, "−$100", 40, "#fff"), fi=.2, fo=.05))
    p.parts.append(_life(half, 99, _count(xr + w_ / 2, z + 55, 100, 50, round(half, 2), .7, size=40, color="#fff", pre="−$"), fi=.05, fo=.01))
    for x, y in ((260, z - 180), (110, z + 110)):
        p.parts.append(_g("pop", half + .05, .35, _ptag(x, y, 110, "½", INK, "#fff", 44)))
    rows = [("½ of $150", "= $75", TEAL), ("½ of $100", "= $50", RED)]
    for j, (a_, b_, col) in enumerate(rows):
        y = 150 + 110 * j
        txt = (f'<text x="385" y="{y}" font-family="\'Serif\',serif" font-weight="700" font-size="44" fill="{INK}">'
               f'{H.escape(a_)} <tspan fill="{col}">{H.escape(b_)}</tspan></text>')
        p.parts.append(_g("wipe", half + .3 + .55 * j, .5, txt, style=""))
    p.parts.append(_g("draw", half + 1.3, .35, '<path d="M385 300 H770" stroke="#0A0A0A" stroke-width="6" stroke-linecap="round"/>', style=""))
    land = s1 + (e1 - s1) * .55
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{land:.2f}" data-d=".35" data-rot="-6" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="425" y="340" width="340" height="180" rx="18" fill="#fff" stroke="{TEAL}" stroke-width="10"/>'
                   + _t(595, 445, "+$25", 96, TEAL) + _t(595, 495, "A TOSS, ON AVERAGE", 24, TEAL, serif=False) + "</g>")


def loss_scale(p, seg=None, **_):
    """Most people say no. A balance: the red -$100 weight on the left pan, the teal +$150 on the right. On 'say no'
    the beam tips the loss side down (10 degrees; the pans drop and rise 45 px) and a red NO stamp lands. On the
    second sentence the teal weight grows to +$200 (counter 150 to 200) and on 'two hundred' the beam comes back
    level, a teal tick on the post. The beam sways a degree whenever it is still."""
    s0, s1, e1 = seg[0][0], seg[1][0], seg[1][1]
    px_, py_ = 400, 170
    tip0, tip1 = s0 + .35, s0 + 1.15
    lev0 = s1 + (e1 - s1) * .72
    _set(p, f'<path d="M260 600 H540" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M{px_} 600 V{py_}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="M{px_ - 40} 600 L{px_} 540 L{px_ + 40} 600 Z" fill="{INK}"/>')
    ang = lambda a: [[0, 0, 0, 1, 1, 0], [round(tip0, 2), 0, 0, 1, 1, 0], [round(tip1, 2), 0, 0, 1, 1, a],
                     [round(lev0, 2), 0, 0, 1, 1, a], [round(lev0 + .8, 2), 0, 0, 1, 1, 0]]
    dy = lambda d: [[0, 0, 0], [round(tip0, 2), 0, 0], [round(tip1, 2), 0, d], [round(lev0, 2), 0, d], [round(lev0 + .8, 2), 0, 0]]
    beam = (f'<path d="M{px_ - 270} {py_} H{px_ + 270}" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
            f'<circle cx="{px_}" cy="{py_}" r="16" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>')
    p.parts.append(_idle("swing", f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json(ang(-10)))}" '
                                  f'style="transform-box:view-box;transform-origin:{px_}px {py_}px">{beam}</g>', 1, 1.4,
                         style=f"transform-box:view-box;transform-origin:{px_}px {py_}px"))

    def pan(x, weight):
        return (f'<path d="M{x} {py_} L{x - 90} {py_ + 170} M{x} {py_} L{x + 90} {py_ + 170}" stroke="{GREY}" stroke-width="4"/>'
                f'<path d="M{x - 110} {py_ + 170} Q{x} {py_ + 230} {x + 110} {py_ + 170} Z" fill="#fff" stroke="{INK}" stroke-width="7"/>'
                + weight)
    wl = f'<rect x="{px_ - 270 - 70}" y="{py_ + 70}" width="140" height="100" rx="12" fill="{RED}" stroke="{INK}" stroke-width="6"/>' \
         + _t(px_ - 270, py_ + 138, "−$100", 40, "#fff")
    grow_at = s1 + .3
    wr_block = f'<rect x="{px_ + 270 - 70}" y="{py_ + 70}" width="140" height="100" rx="12" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
    wr = (_g("scaleY", grow_at, .7, wr_block, style="transform-box:fill-box", s0=1, s1=1.35)
          + _life(-1, grow_at + 1.05, _t(px_ + 270, py_ + 138, "+$150", 40, "#fff"), fi=.01, fo=.05)
          + _life(grow_at, 99, _count(px_ + 270, py_ + 138, 150, 200, round(grow_at, 2), .7, size=40, color="#fff", pre="+$"), fi=.05, fo=.01))
    for x, w, d in ((px_ - 270, wl, 45), (px_ + 270, wr, -45)):
        p.parts.append(f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json(dy(d)))}">{pan(x, w)}</g>')
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{tip1 - .1:.2f}" data-d=".35" data-rot="-10" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="40" y="10" width="200" height="110" rx="16" fill="#fff" fill-opacity=".92" stroke="{RED}" stroke-width="10"/>'
                   + _t(140, 90, "NO", 76, RED) + "</g>")
    p.parts.append(_g("pop", lev0 + .8, .35, f'<circle cx="{px_}" cy="470" r="34" fill="#fff" stroke="{INK}" stroke-width="5"/>'
                                            f'<path d="M{px_ - 16} 471 l12 13 l24 -26" fill="none" stroke="{TEAL}" stroke-width="9" '
                                            f'stroke-linecap="round" stroke-linejoin="round"/>'))
    p.parts.append(_g("fade", lev0 + .9, .4, _t(px_, 535, "ABOUT 2 TO 1", 30, TEAL, serif=False), style=""))


def lunch_bet(p, seg=None, **_):
    """Samuelson's colleague (an illustrated reconstruction). A lunch table: a plain stick figure on the left (the
    economist, labelled), the trader on the right (the colleague). On the first sentence a card slides across the
    table: WIN $200 / LOSE $100, a coin beside it. On 'He said no' a bubble over the trader: x1 and a red NO. On the
    last sentence the bubble swaps to x100 and a teal YES, and a stack of coins rises on the table, counting 1 to 100."""
    s0, s1, s2, e2 = seg[0][0], seg[1][0], seg[2][0], seg[2][1]
    _set(p, f'<path d="M150 470 H650" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M190 470 V600 M610 470 V600" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M20 600 H780" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    figure(p, 110, 600, 1.75, (p.t0 + .05 - p.t0) / p.dur)
    p.parts.append(_g("fade", p.t0 + .4, .3, _t(20, 628, "SAMUELSON, OUR ILLUSTRATION", 24, GREY, serif=False, anchor="start"), style=""))
    trader(p, 690, 600, .72, "stand", .05, look=-1, turn=[(s1 - .2, -1)])
    card = (f'<rect x="250" y="330" width="250" height="130" rx="12" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            + _t(375, 385, "WIN $200", 38, TEAL) + _t(375, 435, "LOSE $100", 38, RED))
    p.parts.append(_g("slide", s0 + .4, .6, _g("fade", s0 + .4, .1, card, style=""), style="", x0=-200, x1=0, ease="out"))
    bub = lambda inner: (f'<path d="M430 40 H760 Q790 40 790 70 V190 Q790 220 760 220 H700 L680 270 L660 220 H430 Q400 220 400 190 V70 '
                         f'Q400 40 430 40 Z" fill="#fff" stroke="{INK}" stroke-width="6"/>' + inner)
    no = bub(_t(510, 160, "×1", 70, INK) + _t(670, 160, "NO", 76, RED))
    yes = bub(_t(530, 160, "×100", 70, INK) + _t(700, 160, "YES", 62, TEAL))
    p.parts.append(_life(s1 + .05, s2 - s1 + .05, _g("pop", s1 + .05, .35, no), fi=.05, fo=.15))
    p.parts.append(_life(s2 + .2, 99, _g("pop", s2 + .2, .35, yes), fi=.05, fo=.01))
    # a stack of coins rising on the table while he says it
    stack_at = s2 + .5
    n_c = 7
    for j in range(n_c):
        y = 452 - 16 * j
        p.parts.append(_g("slide", stack_at + .1 * j, .3, _g("fade", stack_at + .1 * j, .08,
                          f'<ellipse cx="560" cy="{y}" rx="40" ry="13" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="4"/>', style=""),
                          style="", y0=-60, y1=0, ease="out"))
    p.parts.append(_life(stack_at, 99, _count(560, 300, 1, 100, round(stack_at, 2), max(e2 - stack_at, .8), size=40, pre="×"), fi=.1, fo=.01))


def hundred_tosses(p, seg=None, **_):
    """A hundred tosses at $200 to $100. Top left a small coin spins through 100 tosses (counter 1 to 100) while the
    chart grows: every possible total after 100 tosses (34 or more wins ends up, 33 or fewer ends down), each bar its
    exact binomial chance, drawn left to right. On 'average' the middle bar ($5,000, 50 wins) is ringed with a
    counter. On the second sentence the red zone left of $0 is shaded and labelled: ENDING DOWN, UNDER 0.1%
    (our arithmetic: 0.044%); the teal side: OVER 99.9%."""
    from math import comb
    s0, e0, s1, e1 = seg[0][0], seg[0][1], seg[1][0], seg[1][1]
    base, top = 520, 210
    ws = list(range(28, 73))
    pmf = {w: comb(100, w) / 2 ** 100 for w in ws}
    peak = max(pmf.values())
    x0, bw = 50, 15.5
    xof = lambda w: x0 + (w - ws[0]) * bw
    zero_x = xof(100 / 3)                                  # 300 W - 10,000 = 0 at W = 33.3
    p.parts.append(_g("fade", p.t0, .25, f'<path d="M30 {base} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>', style=""))
    grow0, grow_d = s0 + .2, max(e0 - s0 - .4, 1.2)
    for w in ws:
        h_ = (base - top) * pmf[w] / peak
        if h_ < .5:
            continue
        t = grow0 + grow_d * (w - ws[0]) / len(ws)
        col = RED if w <= 33 else TEAL
        bar = f'<rect x="{xof(w) + 1.5:.1f}" y="{base - h_:.1f}" width="{bw - 3:.1f}" height="{h_:.1f}" rx="3" fill="{col}"/>'
        p.parts.append(_g("scaleY", t, .35, bar, style="transform-box:fill-box", s0=.001, s1=1))
    for w, lab in ((50, "$5,000"), (72, "$11,600")):            # $0 is marked by the red line (17 Nov: a -$1,600 label crowded it)
        p.parts.append(_g("fade", grow0 + grow_d * (w - ws[0]) / len(ws), .3,
                          _t(xof(w) + bw / 2, base + 44, lab, 28, GREY if w != 50 else INK, serif=False), style=""))
    # the spinning coin and the toss counter
    p.parts.append(_g("fade", p.t0, .2, _g("coinflip", s0, max(e0 - s0, 1.2), _coin_shape(690, 110, 52, "$"), turns=40), style=""))
    p.parts.append(_g("fade", p.t0, .2, _count(690, 210, 1, 100, round(s0, 2), max(e0 - s0, 1.2), size=34, pre="TOSS "), style=""))
    av = s0 + (e0 - s0) * .7
    xm = xof(50) + bw / 2
    p.parts.append(_g("draw", av, .4, f'<path d="M{xm} {top - 20} V{base}" stroke="{INK}" stroke-width="4" stroke-dasharray="10 8"/>', style=""))
    p.parts.append(_g("pop", av + .2, .35, f'<rect x="{xm - 150}" y="50" width="300" height="130" rx="22" fill="#fff" stroke="{INK}" '
                                          f'stroke-width="6"/>' + _t(xm, 95, "AVERAGE", 26, GREY, serif=False)))
    p.parts.append(_life(av + .25, 99, _count(xm, 160, 0, 5000, round(av + .3, 2), .8, size=52, color=TEAL, pre="+$").replace("data-dec", 'data-sep="1" data-dec', 1), fi=.05, fo=.01))
    # the red zone and its share
    z0 = s1 + .2
    p.parts.append(_g("wipe", z0, .5, f'<rect x="30" y="{top - 40}" width="{zero_x - 30:.1f}" height="{base - top + 40}" fill="{RED}" '
                                    f'fill-opacity=".16"/>', style=""))
    p.parts.append(_g("draw", z0, .4, f'<path d="M{zero_x:.1f} {top - 40} V{base + 10}" stroke="{RED}" stroke-width="6" '
                                    f'stroke-dasharray="12 9"/>', style=""))
    p.parts.append(_g("fade", z0 + .1, .3, _t(zero_x, base + 44, "$0", 28, RED, serif=False), style=""))
    lab_at = s1 + (e1 - s1) * .6
    p.parts.append(_g("pop", lab_at, .4, _ptag(215, 330, 250, "< 0.1%", RED, "#fff", 46)))
    p.parts.append(_g("fade", lab_at + .1, .3, _t(95, 250, "ENDING DOWN", 26, RED, serif=False, anchor="start"), style=""))


def toss_asks(p, **_):
    """The close: x1 and x100 tiles either side of a bobbing ?, the trader pointing at the viewer."""
    p.fill(_tile(40, 120, 220, 150, TEAL, "×1", 90), .1)
    p.fill(_tile(330, 120, 260, 150, GOLD, "×100", 84, color=INK), .25)
    p.parts.append(_g("float", 0, 1, _g("pop", p.at(.4), .4, _t(300, 420, "?", 160, RED)), style="", amp=10, w=2.4))
    trader(p, 690, 630, .9, "point", .05, look=-1, turn=[(p.at(.15), 0)])
    p.parts.append(_idle("bob", _coin_shape(150, 470, 60, "$"), 10, 2.0))


SCENES.update({f.__name__: f for f in (toss_hook, bet_average, loss_scale, lunch_bet, hundred_tosses, toss_asks)})

# ---- 17 Nov, long video #11 (Herstatt, 1974): two banking days five hours apart, on one clock (German time).
# The hours of each banking day are illustrative (labelled so); the five-hour gap and 15:30 are the sourced facts.

def day_bars(p, upto=3, gap=5, closed="15:30", **_):
    """upto 1: Frankfurt's banking day; 2: + New York's, shifted by gap hours, with the gap bracketed; 3: + marks
    paid in the morning, the 15:30 closing line, dollars due in New York's day; 4: the cure, one window in which both
    legs settle together."""
    X = lambda hr: 70 + (hr - 6) * 660 / 18
    p.line([(X(6), 520), (X(24), 520)], 0, .3, w=5)
    for hr in range(6, 25, 3):
        p.line([(X(hr), 508), (X(hr), 532)], .05 + hr * .004, .08, w=4)
        p.text(X(hr), 572, f"{hr:02d}:00", .08 + hr * .004, size=24, color=GREY)
    p.text(400, 618, "GERMAN TIME (CET) · CLS WINDOW, 2002" if upto >= 4 else "GERMAN TIME · ILLUSTRATIVE HOURS", .12, size=22, color=GREY, weight=600)
    if upto >= 4:                                          # the CLS window of 2002: 07:00 to 12:00 CET (Galati, BIS)
        w0, w1 = X(7), X(12)
        p.fill(f'<rect x="{w0:.0f}" y="150" width="{w1 - w0:.0f}" height="300" rx="22" fill="{TEAL}" fill-opacity=".16" stroke="{TEAL}" stroke-width="6"/>', .1)
        p.text((w0 + w1) / 2, 132, "07:00 TO 12:00", .15, size=28, color=TEAL, weight=700)
        for k, (lab, y, metal) in enumerate((("DM", 230, "nickel"), ("$", 370, "gold"))):
            coin(p, (w0 + w1) / 2, y, 44, lab, metal, .25 + .08 * k)
        p.line([(w1 + 30, 200), (w1 + 60, 200), (w1 + 60, 400), (w1 + 30, 400)], .45, .3, color=RED, w=8)
        p.fill(f'<g><rect x="{w1 + 80}" y="282" width="56" height="46" rx="8" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
               f'<path d="M{w1 + 92} 282 v-14 a16 16 0 0 1 32 0 v14" fill="none" stroke="{INK}" stroke-width="7"/></g>', .6)
        p.text(w1 + 160, 260, "BOTH LEGS", .7, size=44, anchor="start", weight=700)
        p.text(w1 + 160, 314, "TOGETHER,", .76, size=44, anchor="start", weight=700)
        p.text(w1 + 160, 368, "OR NEITHER", .82, size=44, anchor="start", weight=700, color=RED)
        return
    fx0, fx1 = X(8), X(15)
    p.text(30, 186, "FRANKFURT", 0, size=28, anchor="start", weight=700)
    p.fill(f'<rect x="{fx0:.0f}" y="210" width="{fx1 - fx0:.0f}" height="70" rx="14" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>', .1, fx="growX")
    if upto < 3:
        p.text(fx1 - 20, 256, "BANKS OPEN", .2, size=26, color="#fff", weight=700, anchor="end")
    if upto >= 2:
        nx0, nx1 = X(9 + gap), X(17 + gap)
        p.text(30, 346, "NEW YORK", .3, size=28, anchor="start", weight=700)
        p.fill(f'<rect x="{nx0:.0f}" y="370" width="{nx1 - nx0:.0f}" height="70" rx="14" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>', .35, fx="growX")
        if upto < 3:
            p.text(nx1 - 20, 416, "BANKS OPEN", .45, size=26, color=INK, weight=700, anchor="end")
        p.line([(X(9), 470), (X(9 + gap), 470)], .5, .2, color=RED, w=6)
        p.line([(X(9), 456), (X(9), 484)], .5, .05, color=RED, w=6)
        p.line([(X(9 + gap), 456), (X(9 + gap), 484)], .55, .05, color=RED, w=6)
        p.text((X(9) + X(9 + gap)) / 2, 500, f"{gap} HOURS", .6, size=26, color=RED, weight=700)
    if upto >= 3:
        coin(p, X(9.2), 245, 28, "DM", "nickel", .62)
        p.text(X(9.2), 316, "MARKS PAID", .66, size=22, weight=700)
        h_, m_ = (int(x) for x in closed.split(":"))
        xc = X(h_ + m_ / 60)
        p.line([(xc, 150), (xc, 450)], .7, .2, color=RED, w=7, dash="16 12")
        p.text(xc, 136, f"{closed} CLOSED", .74, size=30, color=RED, weight=700)
        coin(p, X(18.5), 405, 28, "$", "gold", .82)
        p.text(X(18.5), 358, "DOLLARS DUE", .86, size=22, weight=700)


SCENES.update({f.__name__: f for f in (day_bars,)})


# ---- 17 Nov (Reel, Levels #16: from a multiple to a share price, then a dividend paid with new debt). One money scale
# through the three drawn levels (0.8 px a dollar, so EV $400 = 320 px, the equity $320 = 256 px, $50 of EBITDA =
# 40 px); generic shapes of our own (an office block, a lender's front, share tiles): no company, logo or index.
# 17 Nov (the 16 Nov Reel's next improvement): every drawing keeps moving THROUGH the answer, not only until it.

K16 = .8                      # px a dollar
B16 = 560                     # baseline


def _blk(x, y, w_, h_, fill=GOLD, label="", size=26, col=INK, rx=6):
    s = f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
    return s + (_t(x + w_ / 2, y + h_ / 2 + size * .36, label, size, col) if label else "")


def multiple_stack(p, m=None, ebitda=50, mult=8, **_):
    """Level 1, EV from a multiple. The company's office on the left. On '$50' a gold EBITDA $50 block lands beside
    it. On 'similar' three peer tags reading 8x drop in above it and keep swinging. On '8x' eight copies of the block
    fly one by one into a stack on the right (a rising mallet each). On 'enterprise' a bracket with a bobbing ? stands
    beside the stack. On the answer the bracket turns teal and counts to $400; on '8' a ring goes round one block and
    a x8 tag pops. The stack's blocks keep breathing in a wave after the answer. Drawn flatter than the other levels
    (0.6 px a dollar, the stack 240 px) so it fits its wide box without the fit step cropping it (17 Nov: the first
    cut at 0.8 px a dollar was 1.34 times too tall for its box and ran into the answer)."""
    base, bh = B16, ebitda * .6
    t50 = _wt(m, f"${ebitda}", "qw", default=m["qs"][0][0] + .8)
    tsim = _wt(m, "similar", "qw", default=m["qs"][1][0] + .1)
    t8 = _wt(m, f"{mult}x", "qw", default=tsim + 1.0)
    tev = _wt(m, "enterprise", "qw", default=m["qs"][-1][0] + .3)
    a = m["a"]
    p.parts.append(_g("fade", p.t0, .3, f'<path d="M0 {base} L800 {base}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
                      + _office(20, base, 170, 200) + _t(105, base - 222, "COMPANY", 20, "#fff", serif=False), style=""))
    blk = _blk(212, base - bh, 130, bh, GOLD, f"${ebitda}", 24)
    p.parts.append(_g("fade", t50 - .05, .1, _g("slide", t50 - .05, .45, _idle("breathe", blk, .05, 2.6), style="", y0=-140, y1=0, ease="out"),
                      style=""))
    p.parts.append(_g("fade", t50 + .2, .3, _t(277, base - bh - 14, "EBITDA", 22, INK, serif=False), style=""))
    for j, x in enumerate((80, 200, 320)):
        tag = _idle("swing", _ptag(x, 290, 104, f"{mult}x", GREY, "#fff", 30), 7, 2.2, ph=j * 1.3,
                    style=f"transform-box:view-box;transform-origin:{x - 52}px 290px")
        p.parts.append(_g("fade", tsim + .12 * j, .12, _g("slide", tsim + .12 * j, .4, tag, style="", y0=-90, y1=0, ease="out"), style=""))
    p.parts.append(_g("fade", tsim + .5, .3, _t(200, 240, "SIMILAR COMPANIES", 22, GREY, serif=False), style=""))
    sx = 480
    for k in range(mult):
        y = base - bh * (k + 1)
        t = t8 + .14 * k
        inner = _idle("breathe", _blk(sx, y, 150, bh, GOLD, f"${ebitda}", 20), .04, 2.4, ph=k * .7)
        p.parts.append(_g("fade", t, .08, _g("slide", t, .42, inner, style="", x0=212 - sx, y0=(base - bh) - y, x1=0, y1=0, ease="inout"),
                          style=""))
    top = base - bh * mult
    br = (f'<path d="M{sx + 168} {top} L{sx + 188} {top} L{sx + 188} {base} L{sx + 168} {base}" fill="none" stroke="{{c}}" '
          f'stroke-width="7" stroke-linecap="round"/>')
    p.parts.append(_life(tev - .1, a - tev + .25, br.format(c=RED) + _idle("bob", _t(sx + 250, (top + base) / 2 + 40, "?", 110, RED), 16, 3.2,
                                                                                style="")))
    p.parts.append(_g("draw", a + .05, .4, br.format(c=TEAL), style=""))
    p.parts.append(_g("fade", a + .05, .25, _t(sx + 255, (top + base) / 2 - 24, "EV", 40, TEAL, serif=False), style=""))
    p.parts.append(_count(sx + 255, round((top + base) / 2 + 34), 0, ebitda * mult, round(a + .1, 2), .8, size=48, color=TEAL, pre="$"))
    if len(m["as_"]) > 1:
        tm = _wt(m, str(mult), sent=1, default=m["as_"][1][0] + .1)
        ring = f'<rect x="{sx - 12}" y="{base - bh - 10}" width="174" height="{bh + 20}" rx="10" fill="none" stroke="{TEAL}" stroke-width="7"/>'
        p.parts.append(_life(tm - .05, 1.2, _g("pop", tm - .05, .3, ring), fi=.08, fo=.3))
        p.parts.append(_g("pop", tm + .2, .35, _ptag(sx - 80, base - 120, 120, f"×{mult}", TEAL, "#fff", 36)))


def multiple_stack_fx(m, ebitda=50, mult=8):
    t50 = _wt(m, f"${ebitda}", "qw", default=m["qs"][0][0] + .8)
    tsim = _wt(m, "similar", "qw", default=m["qs"][1][0] + .1)
    t8 = _wt(m, f"{mult}x", "qw", default=tsim + 1.0)
    return ([("hit", t50 + .4, .24, -.3, dict(pitch=220))] + [("clink", tsim + .12 * j + .35, .12, -.2 + .2 * j) for j in range(3)]
            + [("hit", t8 + .14 * k + .4, .12, .3, dict(pitch=330 + 20 * k)) for k in range(mult)] + [("hit", m["a"] + .1, .26, .3, dict(pitch=330))])


def ev_to_equity(p, m=None, ev=400, debt=100, cash=20, **_):
    """Level 2, EV to equity value. The $400 EV column from level 1 stands from the first frame. On 'debt' its top
    $100 turns red and slides out towards the lenders' front on the right (it bobs there). On 'cash' a teal $20
    block comes up from a coin pile onto the column. On 'equity' a bracket with a bobbing ? measures what is left.
    On the answer it counts to $320 in teal; on 'debt' and 'cash' in the second answer line each piece is ringed.
    The column, the debt slice and the cash block keep moving through the answer."""
    base = B16
    hev, hd, hc = ev * K16, debt * K16, cash * K16
    x, cw = 70, 170
    tdb = _wt(m, f"${debt}", "qw", default=m["qs"][0][0] + .8)
    tca = _wt(m, f"${cash}", "qw", default=tdb + 1.0)
    teq = _wt(m, "equity", "qw", default=m["qs"][-1][0] + .3)
    a = m["a"]
    _set(p, f'<path d="M0 {base} L800 {base}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            + _small_bank(570, base, "LENDERS"))
    # the column: the part that stays, and the top $100 that leaves
    stay = _blk(x, base - hev + hd, cw, hev - hd, GOLD) + "".join(
        f'<path d="M{x + 12} {base - 40 * j} H{x + cw - 12}" stroke="{GOLD_D}" stroke-opacity=".35" stroke-width="4"/>' for j in range(1, 6))
    p.parts.append(_g("fade", -1, .05, _idle("breathe", stay, .02, 3.0, style="transform-box:fill-box;transform-origin:center bottom"), style=""))
    p.parts.append(_life(-1, tdb + .1 + 1, _blk(x, base - hev, cw, hd, GOLD), fi=.01, fo=.05))
    p.parts.append(_life(-1, tdb + .1 + 1, _t(x + cw / 2, base - hev / 2 + 14, f"EV ${ev}", 38, INK), fi=.01, fo=.1))
    red = _blk(x, base - hev, cw, hd, RED, f"−${debt}", 34, "#fff")
    p.parts.append(_g("fade", tdb - .05, .1, _g("slide", tdb + .1, .8, _idle("bob", red, 10, 2.4, style=""), style="", x0=0, x1=330, y0=0, y1=0,
                                                 ease="inout"), style=""))
    p.parts.append(_g("fade", tdb + .7, .3, _t(x + 330 + cw / 2, base - hev - 16, "DEBT", 28, RED, serif=False), style=""))
    p.parts.append(_g("draw", tdb + .3, .4, f'<path d="M{x} {base - hev} H{x + cw} V{base - hev + hd} H{x} Z" fill="none" stroke="{INK}" '
                                           f'stroke-width="4" stroke-dasharray="12 9"/>', style=""))
    # the cash: a coin pile, and a teal block that rises onto the column
    for j in range(4):
        p.parts.append(_g("pop", tdb + .5 + .06 * j, .25, _coin_shape(300 + 18 * (j % 2), base - 22 - 26 * j, 40, "$")))
    cy = base - hev + hd - hc
    blk = _blk(x, cy, cw, hc, TEAL)
    p.parts.append(_g("fade", tca - .05, .1, _g("slide", tca, .7, _idle("breathe", blk, .06, 2.2), style="", x0=230, x1=0, y0=(base - 60) - cy,
                                                 y1=0, ease="inout"), style=""))
    p.parts.append(_g("pop", tca + .55, .3, _ptag(x + cw + 90, cy + 66, 140, f"+${cash}", TEAL, "#fff", 32)))
    # the question, then the answer
    eq_top = cy
    br = (f'<path d="M{x - 18} {eq_top} L{x - 38} {eq_top} L{x - 38} {base} L{x - 18} {base}" fill="none" stroke="{{c}}" stroke-width="7" '
          f'stroke-linecap="round"/>')
    p.parts.append(_life(teq - .1, a - teq + .25, br.format(c=RED)))
    p.parts.append(_life(teq - .1, a - teq + .25, _idle("bob", _t(x + cw / 2, base - 90, "?", 110, RED), 16, 3.2, style="")))
    p.parts.append(_g("draw", a + .05, .4, br.format(c=TEAL), style=""))
    p.parts.append(_count(x + cw / 2, base - 120, 0, ev - debt + cash, round(a + .1, 2), .8, size=52, color=INK, pre="$"))
    p.parts.append(_g("fade", a + .3, .3, _t(x + cw / 2, base - 70, "EQUITY", 30, INK, serif=False), style=""))
    if len(m["as_"]) > 1:
        td = _wt(m, "debt", sent=1, default=m["as_"][1][0] + .3)
        tc = _wt(m, "cash", sent=1, default=m["as_"][1][1] - .4)
        for tt, (rx, ry, rw, rh) in ((td, (x + 318, base - hev - 12, cw + 24, hd + 24)), (tc, (x - 12, cy - 12, cw + 24, hc + 24))):
            ring = f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="12" fill="none" stroke="{TEAL}" stroke-width="7"/>'
            p.parts.append(_life(tt - .05, 1.0, _g("pop", tt - .05, .3, ring), fi=.08, fo=.3))


def ev_to_equity_fx(m, ev=400, debt=100, cash=20):
    tdb = _wt(m, f"${debt}", "qw", default=m["qs"][0][0] + .8)
    tca = _wt(m, f"${cash}", "qw", default=tdb + 1.0)
    return [("hit", tdb + .85, .24, .3, dict(pitch=165)), ("clink", tdb + .55, .14, -.2), ("clink", tca + .7, .2, -.3),
            ("hit", m["a"] + .1, .26, 0, dict(pitch=294))]


def share_grid(p, m=None, eq=320, n=40, **_):
    """Level 3, one share. The $320 equity column stands from the first frame. On '40' it breaks into forty share
    tiles that fly out into a 10 x 4 grid on the right (a tick every few). On 'worth' a ? bobs where the column was
    and the first tile wobbles. On the answer that tile flies to the left, turns teal, a 1 SHARE tag lands over it
    and $8 counts up under it; on '$320' the grid gets = $320 beside its label, on '40' a teal frame and a ÷ 40 tag.
    The tiles keep rippling through the answer. (17 Nov: laid out flat after the first cut ran 1.45 times too tall
    for its wide box and over the answer.)"""
    base = B16
    he = eq * K16
    x, cw = 50, 170
    t40 = _wt(m, str(n), "qw", default=m["qs"][0][0] + .6)
    tw = _wt(m, "worth", "qw", default=m["qs"][-1][0] + .5)
    a = m["a"]
    _set(p, f'<path d="M0 {base} L800 {base}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    col = _blk(x, base - he, cw, he, GOLD, f"${eq}", 44)
    p.parts.append(_life(-1, t40 + .6 + 1, col, fi=.01, fo=.3))
    p.parts.append(_life(-1, t40 + .6 + 1, _t(x + cw / 2, base - he - 18, "EQUITY", 28, INK, serif=False), fi=.01, fo=.3))
    cols_, rows_ = 10, n // 10
    tw_, th_, gx, gy = 44, 40, 52, 50
    gx0, gy0 = 262, base - rows_ * gy + 6
    first = None
    for k in range(n):
        r, c = divmod(k, cols_)
        tx, ty = gx0 + c * gx, gy0 + r * gy
        sx, sy = x + cw / 2 - tw_ / 2, base - he + (k + .5) * he / n - th_ / 2
        t = t40 + .25 + .025 * k
        tile = _blk(tx, ty, tw_, th_, GOLD, rx=5)
        inner = _idle("breathe", tile, .05, 2.2, ph=(r + c) * .5)
        if k == 0:
            first = (tx, ty)
            inner = _life(-1, a + .05 + 1, _idle("swing", tile, 5, 3.0, style="transform-box:fill-box;transform-origin:center"), fi=.01, fo=.05)
        p.parts.append(_g("fade", t, .08, _g("slide", t, .5, inner, style="", x0=round(sx - tx), y0=round(sy - ty), x1=0, y1=0, ease="inout"),
                          style=""))
    p.parts.append(_g("fade", t40 + .9, .3, _t(gx0 + 4, gy0 - 20, f"{n} SHARES", 28, INK, serif=False, anchor="start"), style=""))
    p.parts.append(_life(tw - .1, a - tw + .2, _idle("bob", _t(x + cw / 2, base - 60, "?", 120, RED), 14, 3.2, style="")))
    # the answer: the first tile flies to where the column stood and turns teal, a tag over it, $8 under it
    fx_, fy_ = first
    lx, ly = x + cw / 2 - 40, base - 220
    lifted = _blk(fx_, fy_, tw_, th_, TEAL, rx=5)
    p.parts.append(_g("fade", a, .1, _g("slide", a + .05, .45, _idle("bob", f'<g transform="translate({fx_} {fy_}) scale(1.8) translate({-fx_} {-fy_})">'
                                                                     f'{lifted}</g>', 8, 2.4, style=""), style="",
                                         x0=0, x1=lx - fx_, y0=0, y1=ly - fy_, ease="out"), style=""))
    p.parts.append(_g("pop", a + .4, .35, _ptag(x + cw / 2 + 10, base - 292, 190, "1 SHARE", INK, "#fff", 28)))
    p.parts.append(_life(a + .45, 99, _count(x + cw / 2, base - 40, 0, eq / n, round(a + .5, 2), .6, size=72, color=TEAL, pre="$"), fi=.05, fo=.01))
    if len(m["as_"]) > 1:
        te = _wt(m, f"${eq}", sent=1, default=m["as_"][1][0] + .1)
        tn = _wt(m, str(n), sent=1, default=m["as_"][1][1] - .3)
        frame = (f'<rect x="{gx0 - 12}" y="{gy0 - 12}" width="{cols_ * gx + 14}" height="{rows_ * gy + 12}" rx="14" fill="none" '
                 f'stroke="{TEAL}" stroke-width="7"/>')
        p.parts.append(_g("fade", te, .3, _t(gx0 + 230, gy0 - 20, f"= ${eq}", 28, TEAL, serif=False, anchor="start"), style=""))
        p.parts.append(_life(tn - .05, 99, _g("pop", tn - .05, .3, frame), fi=.08, fo=.01))
        p.parts.append(_g("pop", tn + .15, .35, _ptag(gx0 + cols_ * gx - 60, gy0 - 34, 130, f"÷ {n}", TEAL, "#fff", 32)))


def share_grid_fx(m, eq=320, n=40):
    t40 = _wt(m, str(n), "qw", default=m["qs"][0][0] + .6)
    return [("tick", t40 + .3 + .25 * j, .08, -.3 + .1 * j) for j in range(5)] + [("hit", m["a"] + .4, .26, -.2, dict(pitch=392))]


SCENES.update({f.__name__: f for f in (multiple_stack, ev_to_equity, share_grid)})


# ---- 17 Nov (Reel B, Format C, one surprising concept: operating leverage). Sales $100, costs that move with sales
# $40, fixed costs $50, profit $10; sales +10% gives profit $16 (+60%), sales -10% gives $4 (-60%). One money scale
# for every column (3.2 px a dollar: $100 = 320 px), always SALES - MOVING - FIXED = PROFIT in four columns on one
# baseline, so the eye can see that only the fixed column refuses to move. 17 Nov (the 16 Nov Short's next
# improvement): every beat's set is on its panel at the swipe (_set), only the action animates.

K17, B17 = 3.2, 580
OL_X = (20, 215, 410, 605)                    # SALES, MOVING, FIXED, PROFIT
OL_W = 160
MOVE_C = "#E9A23B"


def _ol_col(i, dollars, fill, label="", col=INK, size=40):
    x, h_ = OL_X[i], dollars * K17
    s = f'<rect x="{x}" y="{B17 - h_:.1f}" width="{OL_W}" height="{h_:.1f}" rx="8" fill="{fill}" stroke="{INK}" stroke-width="6"/>'
    return s + (_t(x + OL_W / 2, B17 - h_ / 2 + size * .36, label, size, col) if label and h_ > size + 6 else "")


def _ol_ground(names=("SALES", "MOVING", "FIXED", "PROFIT"), signs=True):
    s = f'<path d="M0 {B17} L800 {B17}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    for x, n in zip(OL_X, names):
        s += _t(x + OL_W / 2, B17 + 44, n, 28, INK, serif=False)
    if signs:
        for x, sg in zip(OL_X[1:], ("−", "−", "=")):
            s += _t(x - 18, B17 - 30, sg, 50, GREY)
    return s


def _lock(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-22 -10 V-30 A22 22 0 0 1 22 -30 V-10" fill="none" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="-34" y="-12" width="68" height="54" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="0" cy="12" r="7" fill="{INK}"/></g>')


def _crate(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-34" y="-30" width="68" height="60" rx="5" fill="#C98A4B" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-34 -30 L34 30 M34 -30 L-34 30" stroke="{INK}" stroke-width="4"/></g>')


def oplev_hook(p, seg=None, **_):
    """The hook. Two tiles from frame 0: SALES $100 and PROFIT $10, each on a baseline. On 'Sales up 10%' a short
    arrow draws up from SALES (6 px a percent) and its counter runs to $110 with a +10% tag; on 'Profit up 60%' a
    long arrow shoots up from PROFIT (the same 6 px a percent, so six times the length) and the counter runs to $16
    with a +60% stamp; on the question a ? bobs between them and both tiles keep breathing."""
    s0, s1, s2 = seg[0][0], seg[1][0], seg[2][0]
    base, k = 590, 6.0
    xs, xp = 200, 600
    _set(p, f'<path d="M30 {base} H770" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            + _t(xs, base + 44, "SALES", 30, INK, serif=False) + _t(xp, base + 44, "PROFIT", 30, INK, serif=False))
    for x, frm, to, t, fill in ((xs, 100, 110, s0 + .3, GOLD), (xp, 10, 16, s1 + .3, TEAL)):
        tile = f'<rect x="{x - 110}" y="{base - 120}" width="220" height="110" rx="14" fill="{fill}" stroke="{INK}" stroke-width="6"/>'
        p.parts.append(_g("fade", -1, .05, _idle("breathe", tile, .03, 2.6, ph=x / 300), style=""))
        p.parts.append(_life(-1, t + 1.0, _t(x, base - 46, f"${frm}", 60, INK if fill == GOLD else "#fff"), fi=.01, fo=.05))
        p.parts.append(_life(t, 99, _count(x, base - 46, frm, to, round(t, 2), .8, size=60, color=INK if fill == GOLD else "#fff", pre="$"),
                             fi=.05, fo=.01))
    for x, pct, t, col in ((xs, 10, s0 + .3, GOLD_D), (xp, 60, s1 + .3, TEAL)):
        y0, y1 = base - 140, base - 140 - pct * k
        a1, a2 = _arrow(x, y0, y1, col, 18)
        p.parts.append(_g("draw", t, .5 + pct / 150, a1, style=""))
        p.parts.append(_g("draw", t + .45 + pct / 150, .2, a2, style=""))
    p.parts.append(_g("pop", s0 + .9, .35, _ptag(xs + 150, base - 230, 150, "+10%", GOLD, INK, 40)))
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{s1 + 1.0:.2f}" data-d=".35" data-rot="-8" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="{xp - 300}" y="40" width="210" height="110" rx="16" fill="#fff" stroke="{TEAL}" stroke-width="9"/>'
                   + _t(xp - 195, 118, "+60%", 70, TEAL) + "</g>")
    p.parts.append(_life(s2 - .05, 99, _idle("bob", _t(400, 330, "?", 150, RED), 16, 3.0, style=""), fi=.15, fo=.01))


def cost_split(p, seg=None, **_):
    """Where the $100 goes. The four labelled slots (SALES - MOVING - FIXED = PROFIT) are there at the swipe. On the
    first sentence the SALES bar grows to $100. On '$40' the bottom $40 (amber) slides out of it into MOVING, a
    crate bobbing on top; on '$50' the next $50 (slate) slides into FIXED and a padlock lands on it; on the last
    sentence the top $10 (teal) slides into PROFIT and its counter runs to $10. The sales bar stays whole (sales are
    still $100): the pieces are copies that show where it goes."""
    s0, s1, s2, s3 = (x[0] for x in seg[:4])
    _set(p, _ol_ground())
    p.parts.append(_g("growY", s0 + .3, .7, _ol_col(0, 100, GOLD), style="transform-box:fill-box;transform-origin:center bottom"))
    p.parts.append(_g("fade", s0 + .9, .3, _t(OL_X[0] + OL_W / 2, B17 - 320 - 18, "$100", 44, INK), style=""))
    # copies leave the sales bar: moving (its bottom 40), fixed (the next 50), profit (the top 10)
    pieces = [(1, 40, 0, MOVE_C, "$40", INK, s1 + .2), (2, 50, 40, DEBT_C, "$50", "#fff", s2 + .2), (3, 10, 90, TEAL, "", "#fff", s3 + .2)]
    for i, d, below, fill, lab, col, t in pieces:
        h_ = d * K17
        y_src = B17 - (below + d) * K17
        y_dst = B17 - h_
        x = OL_X[i]
        blk = f'<rect x="{x}" y="{y_dst:.1f}" width="{OL_W}" height="{h_:.1f}" rx="8" fill="{fill}" stroke="{INK}" stroke-width="6"/>'
        if lab:
            blk += _t(x + OL_W / 2, y_dst + h_ / 2 + 15, lab, 42, col)
        p.parts.append(_g("fade", t - .05, .1, _g("slide", t, .7, _idle("breathe", blk, .02, 2.8, ph=i,
                                                                         style="transform-box:fill-box;transform-origin:center bottom"),
                                                  style="", x0=OL_X[0] - x, x1=0, y0=round(y_src - y_dst, 1), y1=0, ease="inout"), style=""))
        # the piece's place in the sales bar shows its share
        p.parts.append(_life(t, 1.3, f'<rect x="{OL_X[0] + 6}" y="{y_src + 3:.1f}" width="{OL_W - 12}" height="{h_ - 6:.1f}" rx="6" fill="none" '
                                     f'stroke="{fill if fill != DEBT_C else INK}" stroke-width="8"/>', fi=.1, fo=.3))
    p.parts.append(_g("fade", s1 + .75, .2, _g("slide", s1 + .75, .4, _idle("bob", _crate(OL_X[1] + OL_W / 2, B17 - 128 - 50), 8, 2.4, style=""),
                                                style="", y0=-80, y1=0, ease="out"), style=""))
    p.parts.append(_g("fade", s2 + .75, .2, _g("slide", s2 + .75, .4, _idle("swing", _lock(OL_X[2] + OL_W / 2, B17 - 160 - 58), 6, 2.0,
                                                                         style=f"transform-box:view-box;transform-origin:{OL_X[2] + OL_W / 2}px {B17 - 160 - 88}px"),
                                                style="", y0=-80, y1=0, ease="out"), style=""))
    p.parts.append(_life(s3 + .7, 99, _count(OL_X[3] + OL_W / 2, B17 - 32 - 24, 0, 10, round(s3 + .7, 2), .5, size=56, color=TEAL, pre="$"),
                         fi=.05, fo=.01))


def _ol_state(p, sales=100, move=40, fixed=50, profit=10):
    """The four columns at their starting values, on the panel from the swipe."""
    _set(p, _ol_ground())
    _set(p, _ol_col(0, sales, GOLD) + _t(OL_X[0] + OL_W / 2, B17 - sales * K17 - 18, f"${sales}", 44, "#fff"))
    _set(p, _ol_col(2, fixed, DEBT_C, f"${fixed}", "#fff", 42) + _lock(OL_X[2] + OL_W / 2, B17 - fixed * K17 - 58))


def _ol_change(p, i, frm, to, t, fill, col=INK, size=42, d=.7, tag=None, tag_fill=None):
    """Column i goes from frm to to dollars at t (nested scaleY from the baseline), with a counter inside."""
    h_ = frm * K17
    rect = f'<rect x="{OL_X[i]}" y="{B17 - h_:.1f}" width="{OL_W}" height="{h_:.1f}" rx="8" fill="{fill}" stroke="{INK}" stroke-width="6"/>'
    p.parts.append(_g("fade", -1, .05, _g("scaleY", t, d, rect, style="transform-box:fill-box;transform-origin:center bottom", s0=1,
                                          s1=round(to / frm, 4)), style=""))
    y = B17 - min(frm, to) * K17 / 2 + size * .36 if min(frm, to) * K17 > size + 10 else B17 - max(frm, to) * K17 - 20
    c = col if min(frm, to) * K17 > size + 10 else (TEAL if to > frm else RED)
    p.parts.append(_life(-1, t + 1.05, _t(OL_X[i] + OL_W / 2, round(y), f"${frm}", size, c), fi=.01, fo=.05))
    p.parts.append(_life(t, 99, _count(OL_X[i] + OL_W / 2, round(y), frm, to, round(t, 2), d + .1, size=size, color=c, pre="$"), fi=.05, fo=.01))
    if tag:
        p.parts.append(_g("pop", t + d, .35, _ptag(OL_X[i] + OL_W / 2 + 10, B17 - max(frm, to) * K17 - 90, 150, tag, tag_fill, "#fff", 36)))


def cost_grow(p, seg=None, **_):
    """Sales up 10%. The four columns from the last beat stand at the swipe. On the first sentence SALES grows to $110
    (+10%); on the second MOVING grows $40 to $44 (+$4); on the third the FIXED column's padlock gives a small rattle
    and a NO CHANGE tag lands; on the last PROFIT grows $10 to $16 and a +60% stamp lands. One scale throughout."""
    s0, s1, s2, s3 = (x[0] for x in seg[:4])
    _set(p, _ol_ground())
    _ol_change(p, 0, 100, 110, s0 + .5, GOLD, "#fff" if False else INK, tag="+10%", tag_fill=GOLD_D)
    _ol_change(p, 1, 40, 44, s1 + .5, MOVE_C, tag="+$4", tag_fill=GOLD_D)
    _set(p, _ol_col(2, 50, DEBT_C, "$50", "#fff", 42))
    lock = _lock(OL_X[2] + OL_W / 2, B17 - 160 - 58)
    p.parts.append(_g("fade", -1, .05, _idle("swing", lock, 4, 1.6, style=f"transform-box:view-box;transform-origin:{OL_X[2] + OL_W / 2}px {B17 - 248}px"),
                      style=""))
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{s2 + .6:.2f}" data-d=".35" data-rot="-6" style="transform-box:fill-box;transform-origin:center">'
                   + _ptag(OL_X[2] + OL_W / 2, B17 - 330, 180, "NO CHANGE", INK, "#fff", 24) + "</g>")
    _ol_change(p, 3, 10, 16, s3 + .4, TEAL, "#fff")
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{seg[3][0] + (seg[3][1] - seg[3][0]) * .6:.2f}" data-d=".35" data-rot="-8" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="{OL_X[3] - 20}" y="130" width="200" height="104" rx="16" fill="#fff" stroke="{TEAL}" stroke-width="9"/>'
                   + _t(OL_X[3] + 80, 205, "+60%", 64, TEAL) + "</g>")


def cost_shrink(p, seg=None, **_):
    """It cuts both ways. The four columns at $100 / $40 / $50 / $10 stand at the swipe. On the first sentence a red
    REVERSE arrow curls over them. On the second SALES falls to $90 (-10%), MOVING to $36, FIXED holds (the padlock
    rattles), and PROFIT falls $10 to $4 with a red -60% stamp."""
    s0, s1, e1 = seg[0][0], seg[1][0], seg[1][1]
    _set(p, _ol_ground())
    _set(p, _ol_col(2, 50, DEBT_C, "$50", "#fff", 42))
    p.parts.append(_g("fade", -1, .05, _idle("swing", _lock(OL_X[2] + OL_W / 2, B17 - 160 - 58), 4, 1.6,
                                             style=f"transform-box:view-box;transform-origin:{OL_X[2] + OL_W / 2}px {B17 - 248}px"), style=""))
    arc = f'<path d="M640 120 Q400 20 160 120" fill="none" stroke="{RED}" stroke-width="12" stroke-linecap="round"/>'
    head = f'<path d="M200 80 L160 120 L214 140" fill="none" stroke="{RED}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
    p.parts.append(_g("draw", s0 + .2, .6, arc, style=""))
    p.parts.append(_g("draw", s0 + .75, .2, head, style=""))
    mid = s1 + (e1 - s1) * .2
    _ol_change(p, 0, 100, 90, mid, GOLD, tag="−10%", tag_fill=RED)
    _ol_change(p, 1, 40, 36, mid + .3, MOVE_C)
    _ol_change(p, 3, 10, 4, s1 + (e1 - s1) * .55, TEAL, "#fff")
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{s1 + (e1 - s1) * .72:.2f}" data-d=".35" data-rot="-8" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="{OL_X[3] - 20}" y="250" width="200" height="104" rx="16" fill="#fff" stroke="{RED}" stroke-width="9"/>'
                   + _t(OL_X[3] + 80, 325, "−60%", 64, RED) + "</g>")


def lever_fixed(p, seg=None, **_):
    """The name. A lever on a fulcrum labelled FIXED COSTS: a short SALES arm on the left, a long PROFIT arm on the
    right. It rocks from the first sentence: the sales end dips a little, the profit end swings a lot. On 'fixed' in
    the second sentence the fulcrum slides further left (more of the costs fixed) and the same small push now swings
    the profit end further. Tags: +10% on the sales end, PROFIT on the long end."""
    s0, s1, e1 = seg[0][0], seg[1][0], seg[1][1]
    t_mv = s1 + (e1 - s1) * .3
    y = 330
    _set(p, f'<path d="M40 560 H760" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    p.parts.append(_g("pop", s0 + .2, .4, _t(400, 70, "OPERATING LEVERAGE", 44, INK, serif=False)))

    def lever(fx_, ang, t_on, t_off):
        rocks, t, j = [[0, 0, 0, 1, 1, 0]], t_on, 0
        while t < t_off + 12:
            rocks.append([round(t, 2), 0, 0, 1, 1, -ang if j % 2 == 0 else ang * .35])
            t += .9
            j += 1
        beam = (f'<rect x="60" y="{y - 14}" width="680" height="28" rx="12" fill="{INK}"/>'
                f'<rect x="64" y="{y - 92}" width="120" height="78" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
                + _t(124, y - 42, "SALES", 26, INK, serif=False)
                + f'<rect x="600" y="{y - 92}" width="136" height="78" rx="10" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                + _t(668, y - 42, "PROFIT", 26, "#fff", serif=False))
        rock = (f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json(rocks))}" '
                f'style="transform-box:view-box;transform-origin:{fx_}px {y}px">{beam}</g>')
        post = (f'<path d="M{fx_ - 70} 560 L{fx_} {y + 14} L{fx_ + 70} 560 Z" fill="{DEBT_C}" stroke="{INK}" stroke-width="6"/>'
                + _t(fx_, 520, "FIXED", 24, "#fff", serif=False))
        return rock + post

    p.parts.append(_life(-1, t_mv + 1.2, lever(330, 6, s0 + .3, t_mv), fi=.01, fo=.2))
    p.parts.append(_life(t_mv + .1, 99, lever(220, 9, t_mv + .3, 99), fi=.2, fo=.01))
    p.parts.append(_g("pop", t_mv + .4, .4, _ptag(420, 210, 230, "MORE FIXED", DEBT_C, "#fff", 30)))
    p.parts.append(_g("draw", t_mv + .3, .4, f'<path d="M320 600 L240 600" stroke="{RED}" stroke-width="8" stroke-linecap="round"/>'
                                            f'<path d="M260 584 L236 600 L260 616" fill="none" stroke="{RED}" stroke-width="8" stroke-linecap="round"/>',
                      style=""))


def oplev_asks(p, **_):
    """The close: SALES with a -20% tag and a dashed $80 outline, PROFIT as a ? that bobs."""
    _set(p, f'<path d="M30 560 H770" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="80" y="{560 - 320}" width="200" height="320" rx="10" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
            + _t(180, 600, "SALES", 30, INK, serif=False) + _t(600, 600, "PROFIT", 30, INK, serif=False))
    p.parts.append(_g("draw", p.at(.25), .4, f'<rect x="80" y="{560 - 256}" width="200" height="256" rx="10" fill="none" stroke="{RED}" '
                                           f'stroke-width="7" stroke-dasharray="16 10"/>', style=""))
    p.fill(_ptag(380, 230, 170, "−20%", RED, "#fff", 46), .35)
    p.parts.append(_g("float", 0, 1, _g("pop", p.at(.5), .4, _t(600, 470, "?", 220, RED)), style="", amp=12, w=2.2))


SCENES.update({f.__name__: f for f in (oplev_hook, cost_split, cost_grow, cost_shrink, lever_fixed, oplev_asks)})


# ---- 18 Nov (the tax bracket Short, Format E, a myth): a $1,000 raise that crosses into the 22% bracket. US federal
# income tax, single filer, 2026 brackets (IRS, Rev. Proc. 2025-32): 10% to $12,400, 12% to $50,400, 22% above.
# Generic shapes of our own: no agency seal, form or logo, no real person. Every beat's set is on the panel at the
# swipe (the 17 Nov next improvement), drawn with _set or a pre-drawn trader, so only the action animates, and every
# beat starts an action on its first spoken word.

TB_BASE = 600
TB_K = 440 / 51400                       # pixels a dollar in the to-scale column ($51,400 = 440 px)
L10_C, L12_C, L22_C = CASH_C, GOLD, RED


def _pre(p):
    """A Pen fraction that puts a pen-drawn piece (a stroke, the trader) fully on the panel before the swipe."""
    return (-2 - p.t0) / p.dur


def _trader_poses(p, x, y, s, poses, look=1, end=99):
    """15 Nov's trader in a sequence of poses: poses=[(t, pose), ...], the first from the swipe. Each pose is a
    whole drawn trader shown for its window and cross-faded (0.12 s) into the next, so he reacts on the words."""
    for j, (t, pose) in enumerate(poses):
        q = Pen(p.t0, p.dur, p.seed if hasattr(p, "seed") else 1)
        trader(q, x, y, s, pose, _pre(q), look=look)
        t_on = -1 if j == 0 else t
        t_off = poses[j + 1][0] + .12 if j + 1 < len(poses) else end
        p.parts.append(_life(t_on, t_off - t_on, "".join(q.parts), fi=.01 if j == 0 else .12, fo=.12))


def _cnt(x, y, frm, to, at, d, size=48, color=INK, pre="$", suf="", dec=0, anchor="middle"):
    """_count with thousands separators from 1,000 (motion.py data-sep)."""
    return _count(x, y, frm, to, round(at, 2), d, size=size, color=color, pre=pre, suf=suf, dec=dec,
                  anchor=anchor).replace('data-fx="count"', 'data-fx="count" data-sep="1"', 1)


def _fr(seg, j, f):
    """A moment a fraction f of the way through sentence j (the captions light by characters the same way)."""
    a, b = seg[j]
    return a + f * (b - a)


def _stripes(x, y0, y1, w_, col=GOLD_D, gap=46):
    return "".join(f'<path d="M{x + 14} {y} H{x + w_ - 14}" stroke="{col}" stroke-opacity=".3" stroke-width="5"/>'
                   for y in range(int(y1) - 40, int(y0) + 20, -gap))


def _pay_col(x, top, w_=180, label="$50,400", fill=GOLD):
    return (f'<rect x="{x}" y="{top}" width="{w_}" height="{TB_BASE - top}" rx="10" fill="{fill}" stroke="{INK}" stroke-width="7"/>'
            + _stripes(x, top, TB_BASE, w_) + _t(x + w_ / 2, TB_BASE - 26, label, 36, INK))


def _wallet(cx, cy, s=1.0):
    S = lambda v: v * s
    return (f'<rect x="{cx - S(70)}" y="{cy - S(48)}" width="{S(140)}" height="{S(96)}" rx="{S(14)}" fill="#8A5F12" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{cx + S(18)}" y="{cy - S(20)}" width="{S(56)}" height="{S(40)}" rx="{S(10)}" fill="#B8862B" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{cx + S(40)}" cy="{cy}" r="{S(7)}" fill="{INK}"/>')


def tb_hook(p, seg=None, **_):
    """The hook. From the swipe: a gold pay column ($50,400) standing just under a dashed 22% line, the trader beside
    it. On 'raise' a teal +$1,000 block drops onto the column and lands above the line; the line turns solid red and a
    22% tag pops on '22%'. On the question the trader puts his hands on his head, a ? bobs over him and a wallet with
    a red LESS? tag drops in on the right. Not to scale (the +$1,000 is drawn big; beat 3 shows it to scale)."""
    s0, s1 = seg[0][0], seg[1][0]
    x, w_, top, line = 300, 180, 300, 300
    _set(p, f'<path d="M20 {TB_BASE} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            + _t(30, 632, "NOT TO SCALE", 20, GREY, serif=False, anchor="start"))
    p.parts.append(_g("fade", -1, .05, _idle("breathe", _pay_col(x, top), .015, 2.8,
                                             style="transform-box:fill-box;transform-origin:center bottom"), style=""))
    dash = f'<path d="M230 {line} H560" stroke="{RED}" stroke-width="6" stroke-dasharray="18 12" stroke-linecap="round"/>'
    _set(p, dash + _t(570, line + 10, "22% LINE", 28, RED, serif=False, anchor="start"))
    t_drop = _fr(seg, 0, .1)
    blk = (f'<rect x="{x}" y="{line - 70}" width="{w_}" height="70" rx="10" fill="{TEAL}" stroke="{INK}" stroke-width="7"/>'
           + _t(x + w_ / 2, line - 22, "+$1,000", 40, "#fff"))
    p.parts.append(_g("fade", t_drop, .08, _g("slide", t_drop, .55, _idle("bob", blk, 3, 2.2), style="", y0=-260, y1=0, ease="out"),
                      style=""))
    t22 = _fr(seg, 0, .62)
    p.parts.append(_g("draw", t_drop + .55, .35, f'<path d="M230 {line} H560" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>',
                      style=""))
    p.parts.append(_g("pop", t22, .35, _ptag(650, 200, 150, "22%", RED, "#fff", 48)))
    p.parts.append(_life(t22 + .1, 1.0, _g("pop", t22 + .1, .3, f'<rect x="{x - 12}" y="{line - 82}" width="{w_ + 24}" height="94" rx="14" '
                                                             f'fill="none" stroke="{RED}" stroke-width="7"/>'), fi=.05, fo=.3))
    _trader_poses(p, 130, TB_BASE, .72, [(0, "stand"), (s1 + .05, "worry")], look=1)
    p.parts.append(_life(s1 + .1, 99, _idle("bob", _t(130, 300, "?", 120, RED), 14, 2.8, style=""), fi=.15, fo=.01))
    t_w = s1 + .35
    p.parts.append(_g("fade", t_w, .1, _g("slide", t_w, .45, _idle("swing", _wallet(660, 470, .9) + _ptag(660, 380, 150, "LESS?", RED, "#fff", 36),
                                                                   5, 2.4, style="transform-box:view-box;transform-origin:660px 360px"),
                                          style="", y0=-120, y1=0, ease="out"), style=""))


def tb_myth(p, seg=None, **_):
    """The myth. From the swipe: the column with its +$1,000 on top ($51,400), the dashed 22% line, the trader. On the
    first sentence a red wash rises through the whole column and a 22% ON ALL OF IT? tag hangs over it; on 'It
    doesn't.' a MYTH stamp lands, the wash drains away and only the +$1,000 above the line stays red."""
    s0, s1 = seg[0][0], seg[1][0]
    x, w_, line = 300, 180, 300
    _set(p, f'<path d="M20 {TB_BASE} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    p.parts.append(_g("fade", -1, .05, _idle("breathe", _pay_col(x, line, label="$51,400")
                                             + f'<rect x="{x}" y="{line - 70}" width="{w_}" height="70" rx="10" fill="{TEAL}" stroke="{INK}" stroke-width="7"/>'
                                             + _t(x + w_ / 2, line - 22, "+$1,000", 40, "#fff"), .012, 2.8,
                                             style="transform-box:fill-box;transform-origin:center bottom"), style=""))
    _set(p, f'<path d="M230 {line} H560" stroke="{RED}" stroke-width="6" stroke-dasharray="18 12" stroke-linecap="round"/>'
            + _t(570, line + 10, "22% LINE", 28, RED, serif=False, anchor="start"))
    _trader_poses(p, 130, TB_BASE, .72, [(0, "read"), (s1 + .05, "shrug")], look=1)
    t_w = _fr(seg, 0, .25)
    wash = f'<rect x="{x + 4}" y="{line - 66}" width="{w_ - 8}" height="{TB_BASE - line + 62}" rx="8" fill="{RED}" fill-opacity=".72"/>'
    p.parts.append(_life(t_w, s1 + .5 - t_w, _g("growY", t_w, 1.1, wash, style="transform-box:fill-box;transform-origin:center bottom"),
                         fi=.01, fo=.35))
    p.parts.append(_life(t_w + .6, s1 + .4 - t_w - .6, _g("pop", t_w + .6, .35, _ptag(400, 150, 420, "22% ON ALL OF IT?", RED, "#fff", 36)),
                         fi=.05, fo=.25))
    p.parts.append(_life(s1 + .3, 99, f'<rect x="{x + 4}" y="{line - 66}" width="{w_ - 8}" height="62" rx="8" fill="{RED}" fill-opacity=".8"/>'
                         + _t(x + w_ / 2, line - 22, "22%", 40, "#fff"), fi=.3, fo=.01))
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{s1 + .05:.2f}" data-d=".35" data-rot="-10" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="520" y="380" width="240" height="120" rx="16" fill="#fff" stroke="{RED}" stroke-width="10"/>'
                   + _t(640, 465, "MYTH", 76, RED) + "</g>")


def tb_layers(p, seg=None, **_):
    """The layers, to scale ($51,400 = 440 px). From the swipe: the empty column outline, $0 at its foot, the source
    line. On 'layers' its two dividers draw in. On '10%' the bottom layer ($12,400) fills light green with 10% and its
    $12,400 mark; on '12%' (same sentence) the middle layer (to $50,400) fills gold; on '22%' the thin red top ($1,000, 8.6 px) fills
    and a magnifier pops out of it with 22% ON THIS $1,000; the $51,400 total lands on top."""
    x, w_ = 250, 200
    h10, h12, h22 = 12400 * TB_K, 38000 * TB_K, 1000 * TB_K
    y10, y12, y22 = TB_BASE - h10, TB_BASE - h10 - h12, TB_BASE - h10 - h12 - h22
    _set(p, f'<path d="M20 {TB_BASE} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="{x}" y="{y22:.1f}" width="{w_}" height="{TB_BASE - y22:.1f}" rx="6" fill="none" stroke="{INK}" stroke-width="5" '
            f'stroke-dasharray="16 12"/>'
            + _t(x - 14, TB_BASE - 4, "$0", 28, GREY, serif=False, anchor="end")
            + _t(24, 34, "TAXABLE INCOME, TO SCALE", 24, GREY, serif=False, anchor="start")
            + _t(400, 634, "US FEDERAL, SINGLE FILER, 2026 (IRS)", 22, GREY, serif=False))
    # 18 Nov: the set at the swipe is the column already marked in its three layers, faintly tinted, so the panel
    # opens on the thing being explained; each layer then fills solid on its own words
    _set(p, "".join(f'<rect x="{x}" y="{y:.1f}" width="{w_}" height="{h_:.1f}" fill="{c}" fill-opacity=".28"/>'
                    for y, h_, c in ((y10, h10, L10_C), (y12, h12, L12_C), (y22, h22, L22_C)))
            + _t(x + w_ + 18, y10 + h10 / 2 + 10, "?", 34, GREY, anchor="start")
            + _t(x + w_ + 18, y12 + h12 / 2 + 10, "?", 34, GREY, anchor="start"))
    t_lay = _fr(seg, 0, .55)
    for j, y in enumerate((y10, y12)):
        p.parts.append(_g("draw", t_lay + .12 * j, .4, f'<path d="M{x - 30} {y:.1f} H{x + w_ + 30}" stroke="{INK}" stroke-width="5" '
                                                       f'stroke-dasharray="10 8"/>', style=""))
    layer = lambda y, h_, fill: f'<rect x="{x}" y="{y:.1f}" width="{w_}" height="{h_:.1f}" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
    grow = "transform-box:fill-box;transform-origin:center bottom"
    t10 = _fr(seg, 1, .04)
    p.parts.append(_g("growY", t10, .6, layer(y10, h10, L10_C), style=grow))
    p.parts.append(_g("pop", t10 + .4, .3, _t(x + w_ / 2, y10 + h10 / 2 + 18, "10%", 50, INK)))
    p.parts.append(_g("fade", t10 + .6, .3, _t(x - 14, y10 + 10, "$12,400", 30, INK, serif=False, anchor="end"), style=""))
    t12 = _fr(seg, 1, .5)
    p.parts.append(_g("growY", t12, .8, _idle("breathe", layer(y12, h12, L12_C) + _stripes(x, y12, y10, w_), .01, 3.0, style=grow),
                      style=grow))
    p.parts.append(_g("pop", t12 + .6, .3, _t(x + w_ / 2, y12 + h12 / 2 + 18, "12%", 50, INK)))
    p.parts.append(_g("fade", _fr(seg, 1, .85), .3, _t(x - 14, y12 + 10, "$50,400", 30, INK, serif=False, anchor="end"), style=""))
    t22 = _fr(seg, 2, .05)
    p.parts.append(_g("fade", t22, .2, layer(y22, h22, L22_C), style=""))
    # the magnifier: a ring on the sliver, a leader, and the zoomed $1,000 in red
    mx, my, r = 640, 240, 105
    mag = (f'<circle cx="{x + w_ - 24}" cy="{y22 + h22 / 2:.1f}" r="22" fill="none" stroke="{RED}" stroke-width="6"/>'
           f'<path d="M{x + w_ - 4} {y22 + h22 / 2 - 8:.1f} L{mx - r + 8} {my - 20}" stroke="{RED}" stroke-width="6" stroke-linecap="round"/>'
           f'<circle cx="{mx}" cy="{my}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="7"/>'
           f'<rect x="{mx - 78}" y="{my - 56}" width="156" height="60" fill="{L22_C}" stroke="{INK}" stroke-width="5"/>'
           f'<rect x="{mx - 78}" y="{my + 4}" width="156" height="44" fill="{L12_C}" stroke="{INK}" stroke-width="5"/>'
           + _t(mx, my - 12, "22%", 42, "#fff") + _t(mx, my + r + 34, "ONLY THIS $1,000", 24, RED, serif=False))
    p.parts.append(_g("pop", t22 + .2, .4, _idle("bob", mag, 4, 2.6, style="")))
    p.parts.append(_g("fade", t22 + .5, .3, _t(x + w_ / 2, y22 - 16, "$51,400", 34, INK), style=""))


def tb_raise(p, seg=None, **_):
    """The raise, worked (magnified: the top of the column). From the swipe: the gold slab below $50,400, the dashed
    red 22% line on its top edge, an empty TAX tray on the right, the income counter at $50,400. On the first
    sentence a teal +$1,000 block drops onto the slab above the line and the counter runs to $51,400. On '22%' the
    top 22% of the block turns red and counts $220, then slides into the tray; on 'You keep' what is left is $780
    in teal with a YOU KEEP tag, and three coins drop on it."""
    s0, s1, s2 = seg[0][0], seg[1][0], seg[2][0]
    x, w_, line, bh = 90, 300, 420, 160
    sl = bh * .22
    _set(p, f'<path d="M20 {TB_BASE} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="{x}" y="{line}" width="{w_}" height="{TB_BASE - line}" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="7"/>'
            + _stripes(x, line, TB_BASE, w_) + _t(x + w_ / 2, 530, "THE FIRST $50,400", 30, INK, serif=False)
            + f'<path d="M40 {line} H440" stroke="{RED}" stroke-width="6" stroke-dasharray="18 12" stroke-linecap="round"/>'
            + _t(240, line + 40, "SAME TAX AS BEFORE", 22, INK, serif=False)
            + f'<rect x="470" y="380" width="300" height="220" rx="16" fill="#fff" stroke="{INK}" stroke-width="7"/>'
            + _t(620, 430, "TAX", 40, INK, serif=False)
            + _t(240, 50, "INCOME", 26, GREY, serif=False))
    t_c = _fr(seg, 0, .55)
    p.parts.append(_life(-1, t_c + 1.01, _t(240, 110, "$50,400", 60, INK), fi=.01, fo=.01))
    p.parts.append(_life(t_c, 99, _cnt(240, 110, 50400, 51400, t_c, .9, size=60), fi=.01, fo=.01))
    t_drop = _fr(seg, 0, .08)
    top = line - bh
    t22 = _fr(seg, 1, .55)
    t_go = _fr(seg, 1, .9)
    body = f'<rect x="{x}" y="{top}" width="{w_}" height="{bh}" rx="8" fill="{TEAL}" stroke="{INK}" stroke-width="7"/>'
    p.parts.append(_g("fade", t_drop, .08, _g("slide", t_drop, .55, body + _life(-1, t22 + .2 + 1, _t(x + w_ / 2, top + bh / 2 + 18, "+$1,000", 52, "#fff"),
                                                                                 fi=.01, fo=.15),
                                              style="", y0=-300, y1=0, ease="out"), style=""))
    p.parts.append(_life(_fr(seg, 1, .05), t22 - _fr(seg, 1, .05) + .2,
                         f'<rect x="{x - 10}" y="{top - 10}" width="{w_ + 20}" height="{bh + 20}" rx="14" fill="none" stroke="{RED}" stroke-width="7"/>',
                         fi=.15, fo=.2))
    # the 22% slice: red on the block, counting $220, then into the tray (same size: x +390, y down to the tray floor)
    dx, dy = 475 - x, (TB_BASE - 14 - sl) - top
    slice_ = (f'<rect x="{x}" y="{top}" width="{w_}" height="{sl:.1f}" rx="8" fill="{RED}" stroke="{INK}" stroke-width="6"/>'
              + _cnt(x + w_ / 2, top + sl / 2 + 13, 0, 220, t22 + .1, .6, size=36, color="#fff"))
    p.parts.append(_life(t22, 99, _g("slide", t_go, .7, slice_, style="", x0=0, y0=0, x1=dx - 0, y1=round(dy, 1), ease="inout"), fi=.1, fo=.01))
    p.parts.append(_g("pop", t_go + .75, .3, _t(620, 500, "+$220", 40, RED)))
    p.parts.append(_life(t_go + .3, 99, f'<rect x="{x}" y="{top}" width="{w_}" height="{sl:.1f}" rx="8" fill="#fff" fill-opacity=".85" '
                                        f'stroke="{INK}" stroke-width="4" stroke-dasharray="10 8"/>', fi=.3, fo=.01))
    tk = s2 + .15
    p.parts.append(_life(tk, 99, _t(x + w_ / 2, top + sl + (bh - sl) / 2 + 20, "$780", 60, "#fff"), fi=.15, fo=.01))
    p.parts.append(_g("pop", tk + .2, .35, _ptag(x + w_ / 2, top - 50, 200, "YOU KEEP", TEAL, "#fff", 34)))
    for j in range(3):
        p.parts.append(_g("fade", tk + .45 + .15 * j, .05, _g("slide", tk + .45 + .15 * j, .3,
                          f'<ellipse cx="{x + w_ + 40}" cy="{line - 12 - 16 * j}" rx="34" ry="11" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="4"/>',
                          style="", y0=-80, y1=0, ease="out"), style=""))


def _receipt(x, y, w_, h_, head, inc):
    return (f'<path d="M{x} {y} H{x + w_} V{y + h_} ' + " ".join(f"L{x + w_ - (k + .5) * w_ / 10:.1f} {y + h_ - (14 if k % 2 == 0 else 0)}"
                                                                  for k in range(10))
            + f' L{x} {y + h_} Z" fill="#fff" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            + _t(x + w_ / 2, y + 44, head, 30, GREY, serif=False) + _t(x + w_ / 2, y + 90, inc, 36, INK))


def tb_total(p, seg=None, **_):
    """The whole bill. From the swipe: two receipts, BEFORE ($50,400) and AFTER ($51,400), and an empty rate dial
    (0 to 25%, marks at 12% and 22%). On the first sentence both receipts print the same two rows (10% $1,240, 12%
    $4,560) together, the AFTER one adds 22% $220, then the totals count: $5,800 and $5,800 to $6,020 with a +$220
    tag. On the last sentence the needle sweeps to 11.7% and the reading counts with it, under the 12% mark."""
    s0, s1 = seg[0][0], seg[1][0]
    _set(p, _receipt(40, 20, 330, 330, "BEFORE", "$50,400") + _receipt(430, 20, 330, 330, "AFTER", "$51,400"))
    cx, cy, R = 400, 600, 190
    ang = lambda pct: math.pi * (1 - pct / 25)
    pt = lambda pct, r: (cx + r * math.cos(ang(pct)), cy - r * math.sin(ang(pct)))
    arc = f'<path d="M{cx - R} {cy} A{R} {R} 0 0 1 {cx + R} {cy}" fill="none" stroke="{INK}" stroke-width="8"/>'
    ticks = ""
    for pct, lab, col in ((0, "0%", GREY), (12, "12%", INK), (22, "22%", RED), (25, "25%", GREY)):
        (ax, ay), (bx, by), (tx, ty) = pt(pct, R - 16), pt(pct, R + 16), pt(pct, R + 44)
        ticks += (f'<path d="M{ax:.1f} {ay:.1f} L{bx:.1f} {by:.1f}" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'
                  + _t(tx, ty + 10, lab, 24, col, serif=False))
    _set(p, arc + ticks + f'<circle cx="{cx}" cy="{cy}" r="14" fill="{INK}"/>')
    rows = [("10%", "$1,240"), ("12%", "$4,560")]
    t_r = _fr(seg, 0, .12)
    for k, (x, _) in enumerate(((40, 0), (430, 0))):
        for j, (rate, amt) in enumerate(rows):
            y = 150 + 40 * j
            p.parts.append(_g("fade", t_r + .25 * j, .25, _t(x + 30, y, rate, 28, INK, serif=False, anchor="start")
                              + _t(x + 300, y, amt, 28, INK, serif=False, anchor="end"), style=""))
    p.parts.append(_g("fade", t_r + .6, .25, _t(460, 230, "22%", 28, RED, serif=False, anchor="start")
                      + _t(730, 230, "$220", 28, RED, serif=False, anchor="end"), style=""))
    for x in (40, 430):
        p.parts.append(_g("draw", t_r + .8, .3, f'<path d="M{x + 30} 250 H{x + 300}" stroke="{INK}" stroke-width="4"/>', style=""))
    t_a = _fr(seg, 0, .55)
    p.parts.append(_life(t_a, 99, _cnt(205, 300, 0, 5800, t_a, .6, size=44), fi=.01, fo=.01))
    t_b = _fr(seg, 0, .82)
    p.parts.append(_life(t_a, t_b - t_a + .01, _cnt(595, 300, 0, 5800, t_a, .6, size=44), fi=.01, fo=.01))
    p.parts.append(_life(t_b, 99, _cnt(595, 300, 5800, 6020, t_b, .6, size=44, color=RED), fi=.01, fo=.01))
    p.parts.append(_g("pop", t_b + .6, .3, _ptag(680, 380, 130, "+$220", RED, "#fff", 30)))
    # the needle: 0 to 11.7% on the last sentence (rotate about the hub; 25% = 180 degrees)
    t_n = s1 + .1
    deg = 11.712 / 25 * 180
    kf = H.escape(_json([[0, 0, 0, 1, 1, 0], [round(t_n, 2), 0, 0, 1, 1, 0], [round(t_n + 1.1, 2), 0, 0, 1, 1, round(deg, 2)]]))
    needle = f'<path d="M{cx} {cy} L{cx - R + 34} {cy}" stroke="{TEAL}" stroke-width="10" stroke-linecap="round"/>'
    p.parts.append(f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{kf}" style="transform-box:view-box;'
                   f'transform-origin:{cx}px {cy}px">{needle}</g>')
    p.parts.append(_life(t_n, 99, _cnt(cx - 105, cy - 45, 0, 11.7, t_n, 1.1, size=50, color=TEAL, pre="", suf="%", dec=1), fi=.05, fo=.01))
    p.parts.append(_g("fade", t_n + .9, .3, _t(cx - 105, cy - 12, "OF YOUR INCOME", 18, INK, serif=False), style=""))


def tb_rule(p, seg=None, **_):
    """The reading. From the swipe: two pay bars to scale ($50,400 and $51,400, 0.0078 px a dollar), the trader
    reading beside them. On 'So' each bar's tax drops off its top in red (to scale: $5,800 and $6,020) and on
    'brackets' the dashed $50,400 line draws across; on 'raise' what is left counts as take-home ($44,600 and
    $45,380), a +$780 tag pops on the taller one and the trader cheers. One sentence."""
    k = 400 / 51400
    bars = [(110, 50400, 5800, "BEFORE"), (330, 51400, 6020, "AFTER")]
    _set(p, f'<path d="M20 {TB_BASE} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    for x, pay, tax, lab in bars:
        top = TB_BASE - pay * k
        _set(p, f'<rect x="{x}" y="{top:.1f}" width="170" height="{pay * k:.1f}" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="7"/>'
                + _stripes(x, top, TB_BASE, 170) + _t(x + 85, TB_BASE + 30, lab, 24, GREY, serif=False))
    t_line = _fr(seg, 0, .3)
    y50 = TB_BASE - 50400 * k
    p.parts.append(_g("draw", t_line, .5, f'<path d="M80 {y50:.1f} H540" stroke="{RED}" stroke-width="6" stroke-dasharray="18 12"/>', style=""))
    t_tax = _fr(seg, 0, .1)
    for j, (x, pay, tax, lab) in enumerate(bars):
        top = TB_BASE - pay * k
        red = f'<rect x="{x}" y="{top:.1f}" width="170" height="{tax * k:.1f}" rx="8" fill="{RED}" stroke="{INK}" stroke-width="6"/>'
        p.parts.append(_g("growYdown", t_tax + .2 * j, .5, red, style="transform-box:fill-box;transform-origin:center top"))
        p.parts.append(_g("fade", t_tax + .3 + .2 * j, .3, _t(x + 85, top - 14, f"TAX ${tax:,}", 26, RED, serif=False), style=""))
    t_keep = _fr(seg, 0, .55)
    for j, (x, pay, tax, lab) in enumerate(bars):
        p.parts.append(_life(t_keep + .2 * j, 99, _cnt(x + 85, TB_BASE - 60, 0, pay - tax, t_keep + .2 * j, .7, size=36), fi=.05, fo=.01))
    p.parts.append(_g("fade", t_keep, .3, _t(280, TB_BASE - 110, "TAKE-HOME", 22, INK, serif=False), style=""))
    p.parts.append(_g("pop", t_keep + 1.0, .35, _ptag(415, 70, 160, "+$780", TEAL, "#fff", 40)))
    _trader_poses(p, 650, TB_BASE, .72, [(0, "read"), (t_keep + 1.0, "cheer")], look=-1)


def tb_asks(p, **_):
    """The close, all on the panel from frame 0: a 22% tile and an 11.7% tile either side of a bobbing ?, the trader
    pointing at the viewer."""
    _set(p, _tile(30, 110, 200, 140, RED, "22%", 80) + _tile(270, 110, 230, 140, TEAL, "11.7%", 70))
    p.parts.append(_g("float", 0, 1, _t(260, 420, "?", 160, RED), style="", amp=10, w=2.4))
    _trader_poses(p, 690, 630, .9, [(0, "point")], look=-1)
    p.parts.append(_idle("bob", _wallet(130, 500, .9), 8, 2.2))


SCENES.update({f.__name__: f for f in (tb_hook, tb_myth, tb_layers, tb_raise, tb_total, tb_rule, tb_asks)})


# ---- 18 Nov Reel A: accretion / dilution in an all-stock deal (build/reels_accretion-dilution.py) ----
# 18 Nov (the 17 Nov Reel next improvement): every scene's set is on the panel at the swipe and the first action
# starts on the first spoken word of every sentence (_fr(seg, j, .05)), with a second action on its second number.

AD_BASE, AD_K = 590, 3.0                  # earnings column: 3 px a dollar
AD_GX, AD_TW, AD_GAP = 320, 32, 40        # share grid: left edge, tile, pitch (10 x 10 = 100 shares)


def _ad_tile_xy(k):
    r, c = divmod(k, 10)
    return AD_GX + c * AD_GAP, AD_BASE - (r + 1) * AD_GAP


def _ad_grid(p, n_old=100, new=None, t_old=None):
    """The buyer's shares: n_old gold tiles (on the panel from the swipe, or filling row by row from t_old), plus
    new=(n, colour, t) tiles that fly in from the right one by one, each with a tick."""
    for k in range(n_old):
        x, y = _ad_tile_xy(k)
        tile = _blk(x, y, AD_TW, AD_TW, GOLD, rx=4)
        r, c = divmod(k, 10)
        inner = _idle("breathe", tile, .04, 2.4, ph=(r + c) * .4)
        if t_old is None:
            p.parts.append(_g("fade", -1, .05, inner, style=""))
        else:
            p.parts.append(_g("pop", t_old + .07 * r + .01 * c, .25, inner))
    if new:
        n, fill, t = new
        for j in range(n):
            x, y = _ad_tile_xy(n_old + j)
            inner = _idle("bob", _blk(x, y, AD_TW, AD_TW, fill, rx=4), 3, 2.0, ph=j * .7)
            tj = t + .08 * j
            p.parts.append(_g("fade", tj, .08, _g("slide", tj, .45, inner, style="", x0=round(780 - x), y0=-60, x1=0, y1=0, ease="out"),
                              style=""))


def _ad_col(p, earn=100, t_grow=None, add=None):
    """The earnings column (gold), from the swipe or growing at t_grow; add=(dollars, colour, t, label) drops a block
    on top of it. The label above counts to the new total."""
    x, w_ = 50, 170
    h_ = earn * AD_K
    col = f'<rect x="{x}" y="{AD_BASE - h_:.0f}" width="{w_}" height="{h_:.0f}" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
    lab = _t(x + w_ / 2, AD_BASE + 40, "EARNINGS", 26, INK, serif=False)
    _set(p, lab)
    grow = "transform-box:fill-box;transform-origin:center bottom"
    if t_grow is None:
        p.parts.append(_g("fade", -1, .05, _idle("breathe", col, .01, 3.0, style=grow), style=""))
    else:
        p.parts.append(_g("growY", t_grow, .7, col, style=grow))
    top = AD_BASE - h_
    if add:
        d, fill, t, tot = add
        hb = d * AD_K
        blk = (f'<rect x="{x}" y="{top - hb:.0f}" width="{w_}" height="{hb:.0f}" rx="6" fill="{fill}" stroke="{INK}" stroke-width="6"/>')
        p.parts.append(_g("fade", t, .08, _g("slide", t, .5, blk, style="", y0=-200, y1=0, ease="out"), style=""))
        p.parts.append(_life(-1 if t_grow is None else t_grow + .6, t + .5 - (-1 if t_grow is None else t_grow + .6),
                             _t(x + w_ / 2, top - 22, f"${earn}", 44, INK), fi=.05, fo=.05))
        p.parts.append(_life(t + .45, 99, _count(x + w_ / 2, round(top - hb - 22), earn, tot, round(t + .45, 2), .4, size=44, color=INK,
                                                 pre="$"), fi=.05, fo=.01))
    elif t_grow is None:
        _set(p, _t(x + w_ / 2, top - 22, f"${earn}", 44, INK))
    else:
        p.parts.append(_g("fade", t_grow + .6, .3, _t(x + w_ / 2, top - 22, f"${earn}", 44, INK), style=""))


def _ad_eps(p, frm, to, t, x=520, y=60, col=INK, d=.8):
    """The EPS readout at the top right of the grid: a white plate, EPS, and a counter in dollars and cents."""
    _set(p, f'<rect x="{x - 210}" y="{y - 56}" width="420" height="92" rx="16" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            + _t(x - 120, y + 14, "EPS", 40, GREY, serif=False))
    p.parts.append(_life(-1, t + .05 - (-1), _t(x + 70, y + 18, f"${frm:.2f}", 56, INK), fi=.01, fo=.05))
    p.parts.append(_life(t, 99, _count(x + 70, y + 18, frm, to, round(t, 2), d, size=56, color=col, pre="$", dec=2), fi=.05, fo=.01))


def _stamp(x, y, w_, h_, label, col, t, size=60, rot=-8):
    return (f'<g class="a" data-fx="stamp" data-at="{t:.2f}" data-d=".35" data-rot="{rot}" style="transform-box:fill-box;transform-origin:center">'
            f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="16" fill="#fff" stroke="{col}" stroke-width="9"/>'
            + _t(x + w_ / 2, y + h_ / 2 + size * .36, label, size, col) + "</g>")


def ad_hook(p, seg=None, **_):
    """The hook. From the swipe: the buyer (a big office) and the target (a small one) on one street. On the first
    sentence a gold 20x tag drops onto the buyer; on the second a teal 10x tag onto the target, then five share
    tiles fly from the buyer to the target (paying in shares) and the target slides toward the buyer. On the question
    an EPS plate pops between them with a ? that bobs, a teal up arrow and a red down arrow drawn either side."""
    base = 600
    _set(p, f'<path d="M20 {base} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            + _t(190, base + 34, "YOUR COMPANY", 24, INK, serif=False) + _t(640, base + 34, "TARGET", 24, INK, serif=False))
    p.parts.append(_g("fade", -1, .05, _idle("breathe", _office(60, base, 260, 300), .01, 3.2,
                                             style="transform-box:fill-box;transform-origin:center bottom"), style=""))
    t_slide = _fr(seg, 1, .75)
    tgt = _idle("breathe", _office(560, base, 160, 190), .015, 2.6, style="transform-box:fill-box;transform-origin:center bottom")
    p.parts.append(_life(-1, t_slide + .1 + 1, tgt, fi=.01, fo=.05))
    p.parts.append(_life(t_slide + .1, 99, _g("slide", t_slide + .1, .6, tgt, style="", x0=0, x1=-150, y0=0, y1=0, ease="inout"),
                         fi=.01, fo=.01))
    t20 = _fr(seg, 0, .05)
    p.parts.append(_g("fade", t20, .08, _g("slide", t20, .45, _idle("swing", _ptag(190, 230, 170, "20x", GOLD, INK, 56), 4, 2.6,
                                                                    style="transform-box:fill-box;transform-origin:center top"),
                                           style="", y0=-160, y1=0, ease="out"), style=""))
    t10 = _fr(seg, 1, .05)
    p.parts.append(_life(t10, t_slide + .1 - t10, _g("slide", t10, .45, _ptag(640, 360, 150, "10x", TEAL, "#fff", 50),
                                                     style="", y0=-160, y1=0, ease="out"), fi=.08, fo=.05))
    p.parts.append(_life(t_slide + .1, 99, _g("slide", t_slide + .1, .6, _ptag(640, 360, 150, "10x", TEAL, "#fff", 50),
                                              style="", x0=0, x1=-150, y0=0, y1=0, ease="inout"), fi=.01, fo=.01))
    t_pay = _fr(seg, 1, .45)
    for j in range(5):
        tj = t_pay + .07 * j
        tile = _blk(270 + 30 * j, 330, 34, 34, GOLD, rx=4)
        p.parts.append(_life(tj, t_slide - tj + .1, _g("slide", tj, .5, tile, style="", x0=-60, y0=40, x1=300 - 30 * j, y1=60, ease="inout"),
                             fi=.05, fo=.15))
    s2 = seg[2][0] + .05
    p.parts.append(_g("pop", s2, .35, f'<rect x="250" y="60" width="300" height="110" rx="18" fill="#fff" stroke="{INK}" stroke-width="7"/>'
                                       + _t(360, 136, "EPS", 52, INK, serif=False)))
    p.parts.append(_life(s2 + .2, 99, _idle("bob", _t(490, 140, "?", 90, RED), 10, 2.6, style=""), fi=.1, fo=.01))
    for x, y0, y1, col, t in ((190, 170, 70, TEAL, s2 + .25), (610, 70, 170, RED, s2 + .45)):
        a1, a2 = _arrow(x, y0, y1, col, 14)
        p.parts.append(_g("draw", t, .3, a1, style=""))
        p.parts.append(_g("draw", t + .25, .15, a2, style=""))


def ad_buyer(p, seg=None, **_):
    """The buyer. From the swipe: the faint outline of a 10 x 10 share grid and an empty dashed earnings column, the
    EPS plate at $0.00. On '$100' the gold earnings column grows to $100; on '100 shares' the grid fills row by row;
    on '$1 a share' EPS counts to $1.00. On '20x' a 20x tag pops and one share tile lifts out, swings, and a $20
    price lands on it (20 x $1)."""
    _set(p, f'<path d="M20 {AD_BASE} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="50" y="{AD_BASE - 300}" width="170" height="300" rx="8" fill="none" stroke="{GREY}" '
            f'stroke-width="5" stroke-dasharray="14 10"/>'
            + "".join(f'<rect x="{_ad_tile_xy(k)[0]}" y="{_ad_tile_xy(k)[1]}" width="{AD_TW}" height="{AD_TW}" rx="4" fill="none" '
                      f'stroke="{GREY}" stroke-width="3"/>' for k in range(100)))
    _ad_col(p, 100, t_grow=_fr(seg, 0, .05))
    _ad_grid(p, 100, t_old=_fr(seg, 0, .42))
    p.parts.append(_g("fade", _fr(seg, 0, .5), .3, _t(AD_GX + 2, AD_BASE + 40, "100 SHARES", 26, INK, serif=False, anchor="start"), style=""))
    _ad_eps(p, 0, 1.0, _fr(seg, 0, .82))
    t20 = _fr(seg, 1, .05)
    p.parts.append(_g("pop", t20, .35, _ptag(135, 170, 150, "20x", GOLD, INK, 50)))
    x, y = _ad_tile_xy(99)
    big = (f'<g transform="translate({x + 18} {y + 18}) scale(2.6) translate({-x - 18} {-y - 18})">'
           + _blk(x, y, AD_TW, AD_TW, GOLD, rx=4) + "</g>")
    t_up = _fr(seg, 1, .4)
    p.parts.append(_g("fade", t_up, .1, _g("slide", t_up, .45, _idle("swing", big, 5, 2.4), style="", x0=0, y0=0, x1=-180, y1=170, ease="out"),
                      style=""))
    p.parts.append(_g("pop", _fr(seg, 1, .8), .35, _t(x + 16 - 180, y + 170 + 30, "$20", 40, INK)))


def ad_target(p, seg=None, **_):
    """The target. From the swipe: the small target office on the left, an empty price tray on the right. On '$10' a
    teal $10 earnings block drops beside the office; on '10x' a price tag swings in and counts $0 to $100 (10 x
    $10); on '5 new shares' five teal share tiles fly into the tray one by one, each marked $20, and a 5 x $20 =
    $100 line wipes on under them."""
    base = 600
    _set(p, f'<path d="M20 {base} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            + _t(150, base + 34, "TARGET", 24, INK, serif=False)
            + f'<rect x="300" y="420" width="470" height="150" rx="14" fill="none" stroke="{GREY}" stroke-width="5" '
              f'stroke-dasharray="14 10"/>' + _t(535, 604 + 30, "NEW SHARES", 24, INK, serif=False))
    p.parts.append(_g("fade", -1, .05, _idle("breathe", _office(60, base, 180, 210), .015, 2.8,
                                             style="transform-box:fill-box;transform-origin:center bottom"), style=""))
    t0 = _fr(seg, 0, .05)
    blk = (f'<rect x="250" y="{base - 90}" width="120" height="90" rx="8" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
           + _t(310, base - 32, "$10", 40, "#fff"))
    p.parts.append(_g("fade", t0, .08, _g("slide", t0, .45, _idle("bob", blk, 3, 2.4), style="", y0=-220, y1=0, ease="out"), style=""))
    t1 = _fr(seg, 0, .45)
    tag = (f'<rect x="330" y="100" width="300" height="130" rx="18" fill="#fff" stroke="{INK}" stroke-width="7"/>'
           + _t(400, 180, "PRICE", 28, GREY, serif=False))
    p.parts.append(_g("fade", t1, .08, _g("slide", t1, .4, _idle("swing", tag, 3, 2.6, style="transform-box:fill-box;transform-origin:center top"),
                                          style="", y0=-200, y1=0, ease="out"), style=""))
    t_cnt = _fr(seg, 0, .72)
    p.parts.append(_life(t_cnt, 99, _count(540, 190, 0, 100, round(t_cnt, 2), .6, size=64, color=INK, pre="$"), fi=.05, fo=.01))
    p.parts.append(_g("pop", _fr(seg, 0, .68), .3, _ptag(700, 250, 120, "10x", TEAL, "#fff", 40)))
    t2 = _fr(seg, 1, .05)
    for j in range(5):
        tj = t2 + .22 * j
        x = 322 + 90 * j
        tile = _blk(x, 446, 76, 76, GOLD, "$20", 26, rx=6)
        p.parts.append(_g("fade", tj, .08, _g("slide", tj, .4, _idle("bob", tile, 3, 2.2, ph=j), style="", x0=-260 - 90 * j + 322, y0=-300,
                                              x1=0, y1=0, ease="out"), style=""))
    p.parts.append(_g("wipe", _fr(seg, 1, .75), .5, _t(535, 556, "5 x $20 = $100", 34, INK), style=""))


def _ad_rings(p, t_col, t_grid, n_rows, col=RED):
    """18 Nov (the lowest motion window was the division sentence): a ring pulses round the earnings column as its
    dollars are said, then round the whole share grid as its share count is said."""
    top = AD_BASE - n_rows * AD_GAP
    p.parts.append(_life(t_col, 1.3, _g("pop", t_col, .3, f'<rect x="38" y="{AD_BASE - 352}" width="194" height="364" rx="14" fill="none" '
                                                      f'stroke="{col}" stroke-width="8"/>'), fi=.05, fo=.3))
    p.parts.append(_life(t_grid, 1.5, _g("pop", t_grid, .3, f'<rect x="{AD_GX - 12}" y="{top - 8}" width="{10 * AD_GAP + 16}" '
                                                        f'height="{AD_BASE - top + 16}" rx="14" fill="none" stroke="{col}" stroke-width="8"/>'),
                         fi=.05, fo=.3))


def ad_accrete(p, seg=None, **_):
    """The answer at 10x. From the swipe: the buyer's $100 column, the 100 gold tiles, EPS $1.00. On '$110' the
    target's teal $10 drops on the column and its label counts to $110; on '105 shares' five teal tiles fly into the
    grid; on 'about $1.05' EPS counts $1.00 to $1.05 in teal; on 'Accretive' a teal up arrow and an ACCRETIVE stamp."""
    _set(p, f'<path d="M20 {AD_BASE} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    _ad_col(p, 100, add=(10, TEAL, _fr(seg, 0, .1), 110))
    _ad_grid(p, 100, new=(5, TEAL, _fr(seg, 0, .55)))
    p.parts.append(_life(-1, _fr(seg, 0, .6) + 1, _t(AD_GX + 2, AD_BASE + 40, "100 SHARES", 26, INK, serif=False, anchor="start"), fi=.01, fo=.1))
    p.parts.append(_life(_fr(seg, 0, .6), 99, _t(AD_GX + 2, AD_BASE + 40, "105 SHARES", 26, TEAL, serif=False, anchor="start"), fi=.1, fo=.01))
    _ad_rings(p, _fr(seg, 0, .2), _fr(seg, 0, .62), 11, TEAL)
    _ad_eps(p, 1.0, 1.05, _fr(seg, 1, .2), col=TEAL)
    t2 = seg[2][0] + .05
    a1, a2 = _arrow(745, 160, 60, TEAL, 14)
    p.parts.append(_g("draw", t2, .3, a1, style=""))
    p.parts.append(_g("draw", t2 + .25, .15, a2, style=""))
    p.parts.append(_stamp(370, 200, 330, 100, "ACCRETIVE", TEAL, _fr(seg, 2, .5), size=54))


def ad_dilute(p, seg=None, **_):
    """The answer at 30x. From the swipe: the $110 column, the 100 gold tiles, EPS $1.00. On '30x' a red 30x tag
    swings in over the grid; on '15 shares' fifteen red tiles fly into the grid (a row and a half); on 'about 96
    cents' EPS counts $1.00 down to $0.96 in red; on 'Dilutive' a red down arrow and a DILUTIVE stamp."""
    _set(p, f'<path d="M20 {AD_BASE} H780" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    x, w_ = 50, 170
    _set(p, f'<rect x="{x}" y="{AD_BASE - 330}" width="{w_}" height="300" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{x}" y="{AD_BASE - 330}" width="{w_}" height="30" rx="6" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
            + _t(x + w_ / 2, AD_BASE - 352, "$110", 44, INK) + _t(x + w_ / 2, AD_BASE + 40, "EARNINGS", 26, INK, serif=False))
    _ad_grid(p, 100, new=(15, RED, _fr(seg, 0, .55)))
    p.parts.append(_life(-1, _fr(seg, 0, .7) + 1, _t(AD_GX + 2, AD_BASE + 40, "100 SHARES", 26, INK, serif=False, anchor="start"), fi=.01, fo=.1))
    p.parts.append(_life(_fr(seg, 0, .7), 99, _t(AD_GX + 2, AD_BASE + 40, "115 SHARES", 26, RED, serif=False, anchor="start"), fi=.1, fo=.01))
    t0 = _fr(seg, 0, .05)
    p.parts.append(_g("fade", t0, .08, _g("slide", t0, .4, _idle("swing", _ptag(135, 150, 150, "30x", RED, "#fff", 50), 4, 2.4,
                                                                 style="transform-box:fill-box;transform-origin:center top"),
                                          style="", y0=-160, y1=0, ease="out"), style=""))
    _ad_rings(p, _fr(seg, 1, .05), _fr(seg, 1, .4), 12)
    _ad_eps(p, 1.0, .96, _fr(seg, 1, .7), x=520, col=RED)
    t2 = seg[2][0] + .05
    a1, a2 = _arrow(745, 200, 300, RED, 14)
    p.parts.append(_g("draw", t2, .3, a1, style=""))
    p.parts.append(_g("draw", t2 + .25, .15, a2, style=""))
    p.parts.append(_stamp(380, 210, 310, 100, "DILUTIVE", RED, _fr(seg, 2, .5), size=58))


def ad_rule(p, seg=None, **_):
    """The rule. From the swipe: a price-to-earnings scale from 0x to 40x with YOUR 20x marked, the caveat line. On the
    first sentence a pointer drops onto 20x; on 'lower multiple' it slides to 10x, the left half fills teal and EPS UP
    pops; on 'higher one' it slides to 30x, the right half fills red and EPS DOWN pops. The pointer keeps bobbing."""
    y, x0, x1 = 360, 60, 740
    xv = lambda m: x0 + (x1 - x0) * m / 40
    s = f'<path d="M{x0} {y} H{x1}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    for m in (0, 10, 20, 30, 40):
        s += f'<path d="M{xv(m)} {y - 16} V{y + 16}" stroke="{INK}" stroke-width="6"/>' + _t(xv(m), y + 60, f"{m}x", 34, INK, serif=False)
    s += (f'<rect x="{xv(20) - 90}" y="{y + 84}" width="180" height="56" rx="12" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>'
          + _t(xv(20), y + 124, "YOU: 20x", 28, INK, serif=False)
          + _t(400, 620, "ALL-STOCK DEAL, BEFORE SYNERGIES AND FEES", 22, GREY, serif=False)
          + _t(400, 60, "PRICE PAID, TIMES EARNINGS", 26, GREY, serif=False))
    _set(p, s)
    t1, t2 = _fr(seg, 0, .4), _fr(seg, 1, .3)
    for a, b, fill, t, lab, lx in ((0, 20, TEAL, t1, "EPS UP", 10), (20, 40, RED, t2, "EPS DOWN", 30)):
        zone = f'<rect x="{xv(a)}" y="{y - 12}" width="{xv(b) - xv(a)}" height="24" rx="10" fill="{fill}"/>'
        p.parts.append(_g("growX", t, .5, zone, style="transform-box:fill-box;transform-origin:left center" if a == 0 else
                          "transform-box:fill-box;transform-origin:left center"))
        p.parts.append(_g("pop", t + .4, .35, _ptag(xv(lx), 160, 210, lab, fill, "#fff", 34)))
    ptr = (f'<path d="M-34 -70 L34 -70 L0 -20 Z" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>')
    kf = [[0, 0, 0, 1, 1, 0], [round(t1, 2), 0, 0, 1, 1, 0], [round(t1 + .5, 2), xv(10) - xv(20), 0, 1, 1, 0],
          [round(t2, 2), xv(10) - xv(20), 0, 1, 1, 0], [round(t2 + .6, 2), xv(30) - xv(20), 0, 1, 1, 0]]
    mover = (f'<g class="a" data-fx="kf" data-at="0" data-d="1" data-kf="{H.escape(_json(kf))}" style="transform-box:view-box">'
             f'<g transform="translate({xv(20)} {y})">{_idle("bob", ptr, 8, 2.2, style="")}</g></g>')
    p.parts.append(_g("fade", _fr(seg, 0, .05), .1, _g("slide", _fr(seg, 0, .05), .45, mover, style="", y0=-200, y1=0, ease="out"), style=""))


def ad_asks(p, **_):
    """The close: a price tag with $? swinging, an equals sign, and EPS $1.00 on a plate."""
    _set(p, f'<rect x="440" y="250" width="320" height="130" rx="18" fill="#fff" stroke="{INK}" stroke-width="7"/>'
            + _t(530, 334, "EPS", 40, GREY, serif=False) + _t(660, 338, "$1.00", 54, INK) + _t(380, 340, "=", 80, INK))
    p.parts.append(_g("pop", p.at(.15), .4, _idle("swing", _ptag(180, 300, 240, "PAY $?", RED, "#fff", 54), 6, 2.4,
                                                     style="transform-box:fill-box;transform-origin:center top")))
    p.parts.append(_g("float", 0, 1, _g("pop", p.at(.45), .4, _t(400, 190, "?", 160, RED)), style="", amp=12, w=2.2))


TEAL_L = "#5EC8B4"
SCENES.update({f.__name__: f for f in (ad_hook, ad_buyer, ad_target, ad_accrete, ad_dilute, ad_rule, ad_asks)})


# ---- 18 Nov Reel B: FIFO or LIFO with rising prices (build/reels_fifo-lifo.py) ----
# The same rule as Reel A: the set is on the panel at the swipe; an action on the first word of every sentence.

FL_BASE = 560                              # the shelf
FL_X, FL_W, FL_H = 90, 240, 160           # the stack: left edge, unit width and height


def _unit(x, y, price, fill, label=None):
    """One unit of stock: a crate with a price tag on its front."""
    s = (f'<rect x="{x}" y="{y}" width="{FL_W}" height="{FL_H}" rx="8" fill="#C98A4B" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M{x} {y + 30} H{x + FL_W} M{x} {y + FL_H - 30} H{x + FL_W}" stroke="{INK}" stroke-width="4"/>'
         + _ptag(x + FL_W / 2, y + FL_H / 2, 150, price, fill, INK if fill == GOLD else "#fff", 54))
    if label:
        s += _t(x - 16, y + FL_H / 2 + 10, label, 22, GREY, serif=False, anchor="end")
    return s


def _pill(x, y, label, fill=INK, color="#fff", size=28):
    """A rounded label sized to its text (18 Nov: long labels on a price tag ran under its hole)."""
    w_ = len(label) * size * .66 + 44
    h_ = size * 1.7
    return (f'<rect x="{x - w_ / 2:.0f}" y="{y - h_ / 2:.0f}" width="{w_:.0f}" height="{h_:.0f}" rx="{h_ / 2:.0f}" fill="{fill}" '
            f'stroke="{INK}" stroke-width="5"/>' + _t(x, y + size * .36, label, size, color, serif=False))


def _fl_shelf(p, register=True):
    _set(p, f'<path d="M30 {FL_BASE} H770" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M60 {FL_BASE} V{FL_BASE + 50} M360 {FL_BASE} V{FL_BASE + 50}" stroke="{INK}" stroke-width="7"/>'
            + _t(210, FL_BASE + 50, "INVENTORY", 24, INK, serif=False))
    if register:
        _set(p, f'<rect x="500" y="{FL_BASE - 170}" width="260" height="170" rx="14" fill="{DEBT_C}" stroke="{INK}" stroke-width="6"/>'
                f'<rect x="525" y="{FL_BASE - 150}" width="210" height="76" rx="8" fill="#DCEFEA" stroke="{INK}" stroke-width="4"/>'
                + _t(630, FL_BASE - 92, "$20", 56, INK) + _t(630, FL_BASE + 50, "SOLD FOR", 24, INK, serif=False))


Y_LO, Y_HI = FL_BASE - FL_H, FL_BASE - 2 * FL_H - 6       # bottom unit (first in), top unit (last in)


def _drop(p, t, inner, dy=-260):
    p.parts.append(_g("fade", t, .08, _g("slide", t, .45, inner, style="", y0=dy, y1=0, ease="out"), style=""))


def fl_hook(p, seg=None, **_):
    """The hook. From the swipe: the empty shelf with two dashed slots and the till. On '$10' the first unit drops
    into the bottom slot; on '$12' (same sentence) the second lands on top of it. On 'sell one for $20' the till
    flashes $20 and a unit outline marked ? hovers over it. On the question two tags swing in, $8? and $10?."""
    _fl_shelf(p, register=False)
    _set(p, "".join(f'<rect x="{FL_X}" y="{y}" width="{FL_W}" height="{FL_H}" rx="8" fill="none" stroke="{GREY}" stroke-width="5" '
                    f'stroke-dasharray="14 10"/>' for y in (Y_LO, Y_HI)))
    _drop(p, _fr(seg, 0, .1), _idle("breathe", _unit(FL_X, Y_LO, "$10", TEAL, "1ST"), .01, 3.0))
    _drop(p, _fr(seg, 0, .62), _idle("breathe", _unit(FL_X, Y_HI, "$12", GOLD, "2ND"), .01, 2.6, ph=1))
    t1 = _fr(seg, 1, .05)
    till = (f'<rect x="500" y="{FL_BASE - 170}" width="260" height="170" rx="14" fill="{DEBT_C}" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="525" y="{FL_BASE - 150}" width="210" height="76" rx="8" fill="#DCEFEA" stroke="{INK}" stroke-width="4"/>')
    _set(p, till + _t(630, FL_BASE + 50, "SALE", 24, INK, serif=False))
    p.parts.append(_g("pop", _fr(seg, 1, .6), .35, _t(630, FL_BASE - 92, "$20", 56, INK)))
    ghost = (f'<rect x="510" y="{FL_BASE - 190 - FL_H}" width="{FL_W}" height="{FL_H}" rx="8" fill="#fff" fill-opacity=".6" stroke="{INK}" '
             f'stroke-width="5" stroke-dasharray="12 8"/>' + _t(510 + FL_W / 2, FL_BASE - 190 - FL_H / 2 + 30, "?", 90, RED))
    p.parts.append(_g("fade", t1, .2, _idle("bob", ghost, 8, 2.4, style=""), style=""))
    t2 = _fr(seg, 2, .3)
    for x, lab, fill, dt in ((470, "$8?", RED, 0), (660, "$10?", TEAL, .5)):
        p.parts.append(_g("fade", t2 + dt, .08, _g("slide", t2 + dt, .4, _idle("swing", _ptag(x, 70, 150, lab, fill, "#fff", 44), 6, 2.2,
                                                                               style="transform-box:fill-box;transform-origin:center top"),
                                                   style="", y0=-120, y1=0, ease="out"), style=""))


def fl_both(p, seg=None, **_):
    """The answer is 'both'. From the swipe: the two units stacked, the till at $20. On 'Both' a BOTH stamp lands; on
    'which unit' a red ring pulses round the top unit, then the bottom one, back and forth. On 'inventory method' a
    tag drops between them with two arrows, FIFO pointing at the bottom and LIFO at the top."""
    _fl_shelf(p)
    p.parts.append(_g("fade", -1, .05, _idle("breathe", _unit(FL_X, Y_LO, "$10", TEAL, "1ST"), .01, 3.0), style=""))
    p.parts.append(_g("fade", -1, .05, _idle("breathe", _unit(FL_X, Y_HI, "$12", GOLD, "2ND"), .01, 2.6, ph=1), style=""))
    p.parts.append(_stamp(450, 40, 260, 110, "BOTH", TEAL, _fr(seg, 0, .03), size=70))
    t = _fr(seg, 0, .4)
    k = 0
    while t < seg[-1][1] + 3:
        y = Y_HI if k % 2 == 0 else Y_LO
        ring = f'<rect x="{FL_X - 12}" y="{y - 12}" width="{FL_W + 24}" height="{FL_H + 24}" rx="14" fill="none" stroke="{RED}" stroke-width="8"/>'
        p.parts.append(_life(t, .7, ring, fi=.12, fo=.15))
        t += .8
        k += 1
    t1 = _fr(seg, 1, .2)
    p.parts.append(_g("pop", t1, .35, _pill(560, 280, "INVENTORY METHOD", INK, "#fff", 30)))


def _fl_sale(p, seg, out_y, out_price, out_fill, stay_y, stay_price, stay_fill, method, rule, profit, pfill):
    """One method worked. From the swipe: both units, the till at $20, the method's name and rule over the stack. On
    the first word the unit that goes first gets an arrow, then slides across into the till; on the second sentence
    the sum $20 - cost = profit wipes on under the till and the profit counts up; on the third the unit that stays
    settles onto the shelf (if it was on top) and a STAYS IN INVENTORY tag lands on it."""
    _fl_shelf(p)
    _set(p, _t(210, 44, method, 50, INK) + _t(210, 86, rule, 28, GREY, serif=False))
    t0 = _fr(seg, 0, .05)
    a1, a2 = (f'<path d="M{FL_X - 70} {out_y + FL_H / 2} H{FL_X - 18}" stroke="{RED}" stroke-width="10" stroke-linecap="round"/>',
              f'<path d="M{FL_X - 44} {out_y + FL_H / 2 - 22} L{FL_X - 18} {out_y + FL_H / 2} L{FL_X - 44} {out_y + FL_H / 2 + 22}" fill="none" '
              f'stroke="{RED}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    p.parts.append(_life(t0, 2.0, _g("draw", t0, .3, a1 + a2, style=""), fi=.05, fo=.3))
    t_go = _fr(seg, 0, .55)
    unit_out = _unit(FL_X, out_y, out_price, out_fill)
    # 18 Nov (contact sheet): the sold unit slides into the till and fades there; the one left on top settles at once
    p.parts.append(_life(-1, t_go + .7 + .5 + 1, _g("slide", t_go, .7, unit_out, style="", x0=0, y0=0, x1=510 - FL_X,
                                                     y1=FL_BASE - 130 - FL_H - out_y, ease="inout"), fi=.01, fo=.5))
    t_set = t_go + .6
    t_tag = _fr(seg, 2, .2)
    unit_stay = _idle("breathe", _unit(FL_X, stay_y, stay_price, stay_fill), .01, 2.6)
    if stay_y == Y_HI:
        p.parts.append(_g("fade", -1, .05, _g("slide", t_set, .45, unit_stay, style="", y0=0, y1=Y_LO - Y_HI, x0=0, x1=0, ease="out"), style=""))
    else:
        p.parts.append(_g("fade", -1, .05, unit_stay, style=""))
    t1 = _fr(seg, 1, .1)
    p.parts.append(_g("wipe", t1, .5, _t(640, 150, f"$20 − {out_price}", 50, INK), style=""))
    p.parts.append(_g("draw", t1 + .4, .2, f'<path d="M520 180 H760" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>', style=""))
    t_p = _fr(seg, 1, .7)
    p.parts.append(_g("pop", t_p, .3, _t(560, 240, "=", 50, INK)))
    p.parts.append(_life(t_p, 99, _count(670, 244, 0, profit, round(t_p, 2), .5, size=62, color=pfill, pre="$"), fi=.05, fo=.01))
    p.parts.append(_g("pop", t_p + .4, .3, _t(640, 290, "PROFIT", 26, pfill, serif=False)))
    p.parts.append(_g("pop", t_tag, .35, _pill(FL_X + FL_W / 2 + 90, Y_LO - 40, "STAYS IN INVENTORY", INK, "#fff", 26)))


def fl_fifo(p, seg=None, **_):
    """First in, first out: the $10 unit (bottom) goes to the till, profit $10, the $12 unit settles and stays."""
    _fl_sale(p, seg, Y_LO, "$10", TEAL, Y_HI, "$12", GOLD, "FIFO", "FIRST IN, FIRST OUT", 10, TEAL)


def fl_lifo(p, seg=None, **_):
    """Last in, first out: the $12 unit (top) goes to the till, profit $8, the $10 unit stays."""
    _fl_sale(p, seg, Y_HI, "$12", GOLD, Y_LO, "$10", TEAL, "LIFO", "LAST IN, FIRST OUT", 8, RED)


def fl_tax(p, seg=None, **_):
    """Rising prices: less profit, less tax. From the swipe: two profit columns to scale (30 px a dollar), FIFO $10 and
    LIFO $8. On the first sentence a red 25% tax cap grows on top of each ($2.50 and $2.00 by the second sentence's
    numbers) and LESS TAX lands on LIFO; on '50 cents' a gold coin marked 50c rises out of the gap between the caps and
    lands beside LIFO with a KEPT tag, and keeps bobbing."""
    base, k = 560, 30
    cols = ((150, 10, "FIFO", TEAL), (470, 8, "LIFO", RED))
    s = f'<path d="M40 {base} H760" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    for x, v, n, c in cols:
        s += (f'<rect x="{x}" y="{base - v * k}" width="180" height="{v * k}" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
              + _t(x + 90, base + 40, n, 30, INK, serif=False) + _t(x + 90, base - v * k / 2 + 40, f"${v}", 48, INK))
    _set(p, s + _t(400, 620, "PROFIT BEFORE TAX, ONE SALE, 25% TAX", 22, GREY, serif=False))
    t0 = _fr(seg, 0, .05)
    for j, (x, v, n, c) in enumerate(cols):
        cap = f'<rect x="{x + 10}" y="{base - v * k + 6}" width="160" height="{v * k * .25:.0f}" rx="6" fill="{RED}" fill-opacity=".85"/>'
        p.parts.append(_g("growYdown", t0 + .3 * j, .6, _idle("breathe", cap, .03, 2.0, ph=j), style="transform-box:fill-box;transform-origin:center top"))
    # 18 Nov (the lowest 6 s window of the first cut, 0.74, was this beat's long first sentence): on "less profit" the
    # $2 that LIFO lacks draws in as a dashed outline over its column with a -$2 pill, and the FIFO column gives a nod
    t_gap = _fr(seg, 0, .55)
    p.parts.append(_g("draw", t_gap, .5, f'<rect x="470" y="{base - 10 * k}" width="180" height="{2 * k}" rx="8" fill="none" stroke="{RED}" '
                                         f'stroke-width="6" stroke-dasharray="14 9"/>', style=""))
    p.parts.append(_g("pop", t_gap + .35, .3, _idle("bob", _pill(560, base - 10 * k - 40, "−$2 PROFIT", RED, "#fff", 26), 5, 2.2, style="")))
    p.parts.append(_life(_fr(seg, 0, .3), 1.1, _g("press", _fr(seg, 0, .3), .5, f'<rect x="140" y="{base - 10 * k - 10}" width="200" '
                                                                         f'height="{10 * k + 10}" rx="10" fill="none" stroke="{TEAL}" stroke-width="8"/>'),
                         fi=.1, fo=.3))
    t1 = _fr(seg, 1, .05)
    for x, v, lab in ((150, 10, "$2.50"), (470, 8, "$2.00")):
        p.parts.append(_g("pop", t1 + (.0 if v == 10 else .35), .3, _t(x + 90, base - v * k + 6 + v * k * .125 + 14, lab, 36, "#fff")))
    p.parts.append(_g("pop", _fr(seg, 0, .85), .35, _ptag(560, 120, 200, "LESS TAX", RED, "#fff", 32)))
    t_c = _fr(seg, 1, .6)
    coin = (f'<circle cx="0" cy="0" r="48" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>' + _t(0, 14, "50¢", 36, INK))
    p.parts.append(_g("fade", t_c, .1, _g("slide", t_c, .55, f'<g transform="translate(720 300)">{_idle("bob", coin, 8, 2.2, style="")}</g>',
                                          style="", x0=-330, y0=120, x1=0, y1=0, ease="out"), style=""))
    p.parts.append(_g("pop", t_c + .5, .3, _ptag(720, 380, 120, "KEPT", TEAL, "#fff", 28)))


def fl_rules(p, seg=None, **_):
    """Who allows it. From the swipe: two rule books standing on the shelf, US GAAP and IFRS, each with a LIFO tag. On
    the first sentence a teal tick stamps onto US GAAP; on the second a red cross stamps onto IFRS. Both books keep
    breathing."""
    base = 560
    _set(p, f'<path d="M40 {base} H760" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    for x, name, col in ((90, "US GAAP", "#1D4E89"), (450, "IFRS", "#5B3A7A")):
        book = (f'<rect x="{x}" y="{base - 360}" width="260" height="360" rx="12" fill="{col}" stroke="{INK}" stroke-width="7"/>'
                f'<rect x="{x + 20}" y="{base - 340}" width="18" height="320" fill="#fff" fill-opacity=".35"/>'
                + _t(x + 140, base - 260, name, 44, "#fff", serif=False) + _ptag(x + 140, base - 160, 150, "LIFO", GOLD, INK, 40))
        p.parts.append(_g("fade", -1, .05, _idle("breathe", book, .012, 2.8 + x / 400, style="transform-box:fill-box;transform-origin:center bottom"),
                          style=""))
    tick = f'<path d="M150 470 L205 520 L300 400" fill="none" stroke="{TEAL}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>'
    cross = f'<path d="M520 400 L640 520 M640 400 L520 520" fill="none" stroke="{RED}" stroke-width="22" stroke-linecap="round"/>'
    # 18 Nov: said as one sentence ("American rules allow it, but international rules don't."): the tick on its first
    # word, the cross on "international"
    ta, tb = (_fr(seg, 0, .05), _fr(seg, 0, .52)) if len(seg) == 1 else (_fr(seg, 0, .1), _fr(seg, 1, .1))
    p.parts.append(_g("draw", ta, .4, f'<circle cx="220" cy="460" r="95" fill="#fff" stroke="{TEAL}" stroke-width="10"/>' + tick, style=""))
    p.parts.append(_g("draw", tb, .4, f'<circle cx="580" cy="460" r="95" fill="#fff" stroke="{RED}" stroke-width="10"/>' + cross, style=""))
    p.parts.append(_g("pop", ta + .1, .3, _t(220, 600, "ALLOWED", 26, TEAL, serif=False)))
    p.parts.append(_g("pop", tb + .1, .3, _t(580, 600, "NOT ALLOWED", 26, RED, serif=False)))


def fl_asks(p, **_):
    """The close: prices falling. A $10 unit with an $8 unit on top, a red down arrow beside them, FIFO or LIFO? over
    the till and a ? that bobs."""
    _set(p, f'<path d="M30 {FL_BASE} H770" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
            + _unit(FL_X, Y_LO, "$10", TEAL) + _unit(FL_X, Y_HI, "$8", RED))
    a1, a2 = _arrow(395, 200, 500, RED, 16)
    p.parts.append(_g("draw", p.at(.1), .4, a1, style=""))
    p.parts.append(_g("draw", p.at(.2), .2, a2, style=""))
    p.fill(_pill(590, 230, "FIFO OR LIFO?", INK, "#fff", 36), .35)
    p.parts.append(_g("float", 0, 1, _g("pop", p.at(.5), .4, _t(600, 470, "?", 200, RED)), style="", amp=12, w=2.2))


SCENES.update({f.__name__: f for f in (fl_hook, fl_both, fl_fifo, fl_lifo, fl_tax, fl_rules, fl_asks)})


# ---- 19 Nov (the leverage Short, Format D, an animated calculation, cut from YouTube #12, LTCM 1998): $100 of bonds
# bought with $4 of your own and $96 borrowed (25 to 1); a 4% fall takes all $4, a 1% fall takes a quarter. Then
# LTCM's own figures (PWG 1999, Federal Reserve History). Generic shapes of our own: no fund logo, no real person.
# Every beat's set is on the panel at the swipe (entry_check), and every sentence longer than about 2.5 s carries a
# second action on its second number or its last words (the 18 Nov next improvement: no quiet 6 s window).

LV_BASE, LV_K = 590, 4.2                  # ground line; pixels a dollar ($100 = 420 px) in the to-scale columns
BOND_C, BOND_D = "#A9C2DF", "#2E4F7A"
LV_BX, LV_RX, LV_W = 90, 410, 210         # the bonds column and the paid-for-by column (debt under yours)


def _lv_ground():
    return f'<path d="M30 {LV_BASE} H770" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'


def _lv_bonds(x, top, w_=LV_W, label=True):
    h_ = LV_BASE - top
    s = (f'<rect x="{x}" y="{top:.1f}" width="{w_}" height="{h_:.1f}" rx="8" fill="{BOND_C}" stroke="{INK}" stroke-width="7"/>'
         + "".join(f'<path d="M{x + 22} {y:.1f} H{x + w_ - 22}" stroke="{BOND_D}" stroke-opacity=".35" stroke-width="5"/>'
                   for y in [top + 34 + 40 * k for k in range(int((h_ - 60) // 40))]))
    return s + (_t(x + w_ / 2, LV_BASE - 26, "BONDS", 30, BOND_D, serif=False) if label else "")


def _lv_debt(x, top, w_=LV_W):
    return (f'<rect x="{x}" y="{top:.1f}" width="{w_}" height="{LV_BASE - top:.1f}" rx="8" fill="{DEBT_C}" stroke="{INK}" stroke-width="7"/>'
            + _t(x + w_ / 2, LV_BASE - 26, "BORROWED", 28, "#fff", serif=False))


def _lv_yours(x, top, h_, w_=LV_W):
    return f'<rect x="{x}" y="{top:.1f}" width="{w_}" height="{h_:.1f}" rx="4" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>'


def _lv_swap(p, t, x, y, a, b, size=60, color=INK, pre="$", suf="", d=.6, dec=0):
    """A label that reads a until t, then counts to b."""
    p.parts.append(_life(-1, t + 1.01, _t(x, y, f"{pre}{a}{suf}", size, color), fi=.01, fo=.01))
    p.parts.append(_life(t, 99, _cnt(x, y, a, b, t, d, size=size, color=color, pre=pre, suf=suf, dec=dec), fi=.01, fo=.01))


def _push(p, at, d, s1=1.04, ox=400, oy=400):
    """19 Nov: a slow push-in on the whole drawing over a long stretch (the hook, a long first sentence), so the
    panel is never still while the voice explains; the actions still land on their words."""
    p.parts.insert(0, f'<g class="a" data-fx="scale" data-at="{at:.2f}" data-d="{d:.2f}" data-s0="1" data-s1="{s1}" '
                      f'style="transform-box:view-box;transform-origin:{ox}px {oy}px">')
    p.parts.append("</g>")


def lv_hook(p, seg=None, **_):
    """The puzzle, to scale ($100 = 420 px). From the swipe: the ground, two dashed column outlines (WHAT YOU OWN,
    PAID FOR BY) and TO SCALE. On 'buy' the bonds column grows and counts to $100; on 'own' a thin gold $4 sliver
    lands on top of the right column with a $4 YOURS tag. On 'borrow' the dark BORROWED block grows under it and
    counts to $96. On 'fall' the bonds' top 4% turns red and drops away (the column counts to $96) with a -4% tag;
    on 'What's left' a red ring closes on the sliver and a ? bobs over it."""
    top, ytop = LV_BASE - 100 * LV_K, LV_BASE - 100 * LV_K
    ydeb = LV_BASE - 96 * LV_K
    _set(p, _lv_ground()
            + f'<rect x="{LV_BX}" y="{top}" width="{LV_W}" height="{100 * LV_K}" rx="8" fill="none" stroke="{GREY}" stroke-width="5" stroke-dasharray="16 12"/>'
            + f'<rect x="{LV_RX}" y="{top}" width="{LV_W}" height="{100 * LV_K}" rx="8" fill="none" stroke="{GREY}" stroke-width="5" stroke-dasharray="16 12"/>'
            + _t(LV_BX + LV_W / 2, top - 22, "WHAT YOU OWN", 26, GREY, serif=False)
            + _t(LV_RX + LV_W / 2, top - 22, "PAID FOR BY", 26, GREY, serif=False)
            + _t(30, 630, "TO SCALE", 20, GREY, serif=False, anchor="start")
            # 19 Nov: the three blocks faintly tinted from the first frame, so the hook opens on the thing explained
            + f'<rect x="{LV_BX}" y="{top}" width="{LV_W}" height="{100 * LV_K}" rx="8" fill="{BOND_C}" fill-opacity=".3"/>'
            + f'<rect x="{LV_RX}" y="{ydeb}" width="{LV_W}" height="{96 * LV_K}" rx="8" fill="{DEBT_C}" fill-opacity=".22"/>'
            + f'<rect x="{LV_RX}" y="{ytop}" width="{LV_W}" height="{4 * LV_K}" rx="4" fill="{GOLD}" fill-opacity=".5"/>'
            + _t(LV_BX + LV_W / 2, 330, "?", 60, GREY) + _t(LV_RX + LV_W / 2, 330, "?", 60, GREY))
    grow = "transform-box:fill-box;transform-origin:center bottom"
    tb = _fr(seg, 0, .06)
    p.parts.append(_g("ripple", tb + 1.0, .7, f'<circle cx="{LV_BX + LV_W / 2}" cy="{LV_BASE}" r="45" fill="none" stroke="{BOND_D}" stroke-width="6"/>'))
    p.parts.append(_g("growY", tb, 1.1, _idle("breathe", _lv_bonds(LV_BX, top), .008, 3.1, style=grow), style=grow))
    t_fall = _fr(seg, 2, .3)
    p.parts.append(_life(tb + .2, t_fall + .35 - tb - .2 + .01, _cnt(LV_BX + LV_W / 2, 330, 0, 100, tb + .2, 1.4, size=60), fi=.05, fo=.01))
    p.parts.append(_life(t_fall + .35, 99, _cnt(LV_BX + LV_W / 2, 330, 100, 96, t_fall + .35, .5, size=60), fi=.01, fo=.01))
    ty = _fr(seg, 0, .62)
    p.parts.append(_g("fade", ty, .08, _g("slide", ty, .45, _lv_yours(LV_RX, ytop, 4 * LV_K), style="", y0=-140, y1=0, ease="out"), style=""))
    p.parts.append(_g("pop", ty + .35, .35, _idle("swing", _ptag(665, 110, 190, "$4 YOURS", GOLD, INK, 30), 6, 2.2,
                                                  style="transform-box:view-box;transform-origin:575px 110px")))
    p.parts.append(_g("draw", ty + .5, .4, f'<path d="M585 140 Q585 {ytop:.0f} {LV_RX + LV_W - 10} {ytop + 4:.0f}" fill="none" stroke="{GOLD_D}" '
                                           f'stroke-width="4" stroke-dasharray="8 7"/>', style=""))
    td = _fr(seg, 1, .08)
    p.parts.append(_g("growY", td, 1.0, _lv_debt(LV_RX, ydeb), style=grow))
    p.parts.append(_g("ripple", td + 1.0, .7, f'<circle cx="{LV_RX + LV_W / 2}" cy="{LV_BASE}" r="45" fill="none" stroke="{INK}" stroke-width="6"/>'))
    p.parts.append(_life(td + .4, 99, _cnt(LV_RX + LV_W / 2, 330, 0, 96, td + .4, .7, size=60, color="#fff"), fi=.05, fo=.01))
    # the fall: the top 4% ($4, 16.8 px) of the bonds turns red, then drops off to the left and fades
    sl = (f'<rect x="{LV_BX}" y="{top:.1f}" width="{LV_W}" height="{4 * LV_K:.1f}" rx="4" fill="{RED}" stroke="{INK}" stroke-width="5"/>')
    p.parts.append(_life(t_fall, 1.6, _g("slide", t_fall + .4, 1.0, sl, style="", x0=0, y0=0, x1=-60, y1=120, ease="inout"), fi=.08, fo=.4))
    p.parts.append(_life(t_fall + .5, 99, f'<rect x="{LV_BX}" y="{top:.1f}" width="{LV_W}" height="{4 * LV_K:.1f}" rx="4" fill="none" '
                                          f'stroke="{RED}" stroke-width="4" stroke-dasharray="10 8"/>', fi=.3, fo=.01))
    p.parts.append(_g("pop", t_fall + .1, .35, _idle("bob", _ptag(LV_BX + LV_W / 2, 88, 130, "−4%", RED, "#fff", 36), 4, 2.2, style="")))
    tq = _fr(seg, 3, .1)
    p.parts.append(_g("pop", tq, .35, f'<rect x="{LV_RX - 12}" y="{ytop - 14}" width="{LV_W + 24}" height="{4 * LV_K + 28}" rx="10" fill="none" '
                                      f'stroke="{RED}" stroke-width="7"/>'))
    p.parts.append(_life(tq + .15, 99, _idle("bob", _t(LV_RX + LV_W / 2, ytop - 50, "?", 110, RED), 12, 2.6, style=""), fi=.15, fo=.01))
    _push(p, 0, seg[3][1] + .5, 1.045, 400, 420)


def lv_zero(p, seg=None, **_):
    """The answer. From the swipe: the state after the fall, to scale: bonds at $96 with the lost $4 dashed in red
    above them, BORROWED $96, the gold $4 sliver still on top. On 'Nothing.' the sliver squashes flat, a YOURS $0 tag
    replaces it and a WIPED OUT stamp lands over the right column. On the second sentence the lost slice glows, a
    4% x $100 = $4 tag pops over it and the bonds' figure counts $100 to $96 on '$4'. On the third a teal ring
    closes on BORROWED with an OWED tag, then an = lands between the columns (what you own pays what you owe)."""
    top, y96 = LV_BASE - 100 * LV_K, LV_BASE - 96 * LV_K
    _set(p, _lv_ground() + _lv_bonds(LV_BX, y96) + _lv_debt(LV_RX, y96)
            + f'<rect x="{LV_BX}" y="{top:.1f}" width="{LV_W}" height="{4 * LV_K:.1f}" rx="4" fill="none" stroke="{RED}" stroke-width="4" stroke-dasharray="10 8"/>'
            + _t(LV_RX + LV_W / 2, 330, "$96", 60, "#fff")
            + _t(30, 630, "TO SCALE", 20, GREY, serif=False, anchor="start"))
    t0 = _fr(seg, 0, .1)
    p.parts.append(f'<g class="a" data-fx="scaleY" data-at="{t0:.2f}" data-d="0.45" data-s0="1" data-s1="0.05" '
                   f'style="transform-box:fill-box;transform-origin:center bottom">{_lv_yours(LV_RX, top, 4 * LV_K)}</g>')
    p.parts.append(_life(-1, t0 + 1.01, _ptag(665, 250, 190, "$4 YOURS", GOLD, INK, 30), fi=.01, fo=.2))
    p.parts.append(_g("pop", t0 + .3, .35, _idle("bob", _ptag(665, 250, 190, "$0 YOURS", RED, "#fff", 30), 4, 2.4, style="")))
    p.parts.append(f'<g class="a" data-fx="stamp" data-at="{t0 + .2:.2f}" data-d=".35" data-rot="-8" '
                   f'style="transform-box:fill-box;transform-origin:center">'
                   f'<rect x="{LV_RX - 10}" y="40" width="{LV_W + 120}" height="92" rx="14" fill="#fff" stroke="{RED}" stroke-width="9"/>'
                   + _t(LV_RX + LV_W / 2 + 50, 104, "WIPED OUT", 50, RED) + "</g>")
    t1 = _fr(seg, 1, .08)
    p.parts.append(_life(t1, 99, _g("pop", t1, .3, f'<rect x="{LV_BX}" y="{top:.1f}" width="{LV_W}" height="{4 * LV_K:.1f}" rx="4" fill="{RED}" '
                                                   f'fill-opacity=".85"/>'), fi=.05, fo=.01))
    p.parts.append(_g("pop", _fr(seg, 1, .3), .35, _idle("bob", _ptag(LV_BX + LV_W / 2 + 10, 92, 280, "4% × $100", RED, "#fff", 40), 4, 2.3, style="")))
    _lv_swap(p, _fr(seg, 1, .78), LV_BX + LV_W / 2, 330, 100, 96, size=60)
    p.parts.append(_g("pop", _fr(seg, 1, .8), .3, _t(LV_BX + LV_W / 2, top - 6, "= $4", 30, RED, serif=False)))
    t2 = _fr(seg, 2, .12)
    p.parts.append(_g("pop", t2, .35, f'<rect x="{LV_RX - 12}" y="{y96 - 12:.1f}" width="{LV_W + 24}" height="{LV_BASE - y96 + 24:.1f}" rx="14" '
                                      f'fill="none" stroke="{TEAL}" stroke-width="8"/>'))
    p.parts.append(_g("pop", _fr(seg, 2, .4), .35, _idle("bob", _ptag(LV_RX + LV_W / 2, 440, 190, "OWED", TEAL, "#fff", 34), 4, 2.5, style="")))
    p.parts.append(_g("pop", _fr(seg, 2, .75), .4, _t((LV_BX + LV_W + LV_RX) / 2, 400, "=", 100, TEAL)))


def lv_one(p, seg=None, **_):
    """One percent. From the swipe: the $100 bonds column on the left, your $4 as four gold $1 coins stacked on the
    right under YOURS $4. On '1%' a -1% tag pops over the bonds and their figure counts to $99; on 'quarter' the
    top coin turns red and slides off the stack to the ground with a -25% tag, the stack's figure counting $4 to $3
    on the second sentence while a 1/4 tag lands by the fallen coin."""
    top = LV_BASE - 100 * LV_K
    _set(p, _lv_ground() + _lv_bonds(80, top, 220) + _t(500, 250, "YOURS", 30, GREY, serif=False))
    p.parts.append(_g("fade", -1, .05, _idle("breathe", _lv_bonds(80, top, 220), .006, 3.0,
                                             style="transform-box:fill-box;transform-origin:center bottom"), style=""))
    coin = lambda cx, cy, fill=GOLD, lab="$1", col=INK: (
        f'<ellipse cx="{cx}" cy="{cy + 14}" rx="80" ry="24" fill="{GOLD_D if fill == GOLD else "#8E2408"}" stroke="{INK}" stroke-width="5"/>'
        f'<rect x="{cx - 80}" y="{cy - 6}" width="160" height="20" fill="{GOLD_D if fill == GOLD else "#8E2408"}"/>'
        f'<ellipse cx="{cx}" cy="{cy - 6}" rx="80" ry="24" fill="{fill}" stroke="{INK}" stroke-width="5"/>' + _t(cx, cy + 6, lab, 30, col))
    ys = [LV_BASE - 40 - 52 * k for k in range(4)]
    for y in ys[:3]:
        _set(p, coin(500, y))
    t1 = _fr(seg, 0, .22)
    _lv_swap(p, t1 + .2, 190, 330, 100, 99, size=60)
    p.parts.append(_g("pop", t1, .35, _idle("bob", _ptag(190, top - 70, 150, "−1%", RED, "#fff", 40), 4, 2.2, style="")))
    tq = _fr(seg, 0, .62)
    p.parts.append(_life(-1, tq + 1.01, coin(500, ys[3]), fi=.01, fo=.01))
    p.parts.append(_life(tq, 99, _g("slide", tq + .25, .75, coin(500, ys[3], RED, "$1", "#fff"), style="", x0=0, y0=0, x1=200,
                                    y1=ys[0] - ys[3], ease="inout"), fi=.08, fo=.01))
    p.parts.append(_g("pop", tq + .95, .35, _idle("bob", _ptag(700, 380, 150, "−25%", RED, "#fff", 40), 4, 2.4, style="")))
    t2 = _fr(seg, 1, .15)
    _lv_swap(p, t2, 500, 330, 4, 3, size=64)
    p.parts.append(_g("pop", _fr(seg, 1, .6), .35, _t(700, 470, "1 OF 4", 30, RED, serif=False)))


def lv_ratio(p, seg=None, **_):
    """The ratio. From the swipe: one gold $1 coin (YOURS) on the left and an empty 5 x 5 grid of bond tiles on the
    right. On '25 to 1' a 25 TO 1 tag pops at the top. On the second sentence the 25 tiles fill one after another
    and a counter beside the coin runs $0 to $25 of bonds with them. On the third a -1% chip pops on the grid and,
    on '25 times', a -25% tag lands on the coin with a red ring."""
    gx, gy, ts, gap = 350, 198, 72, 8
    grid = "".join(f'<rect x="{gx + c * (ts + gap)}" y="{gy + r * (ts + gap)}" width="{ts}" height="{ts}" rx="8" fill="{BOND_C}" fill-opacity=".3" stroke="{GREY}" '
                   f'stroke-width="4" stroke-dasharray="10 8"/>' for r in range(5) for c in range(5))
    cx, cy = 140, 480
    coin = (f'<circle cx="{cx}" cy="{cy}" r="82" fill="{GOLD}" stroke="{INK}" stroke-width="7"/>'
            f'<circle cx="{cx}" cy="{cy}" r="62" fill="none" stroke="{GOLD_D}" stroke-width="4"/>' + _t(cx, cy + 18, "$1", 52, INK))
    _set(p, grid + _t(cx, 610, "YOURS", 26, GREY, serif=False) + _t(546, 620, "BONDS", 26, GREY, serif=False))
    p.parts.append(_g("fade", -1, .05, _idle("bob", coin, 5, 2.4, style=""), style=""))
    p.parts.append(_g("pop", _fr(seg, 0, .2), .4, _idle("bob", _ptag(400, 100, 340, "25 TO 1", INK, "#fff", 56), 4, 2.6, style="")))
    a, b = _fr(seg, 1, .25), _fr(seg, 1, .85)
    for k in range(25):
        r, c = divmod(k, 5)
        x, y = gx + c * (ts + gap), gy + (4 - r) * (ts + gap)
        tile = (f'<rect x="{x}" y="{y}" width="{ts}" height="{ts}" rx="8" fill="{BOND_C}" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M{x + 14} {y + 28} H{x + ts - 14} M{x + 14} {y + 46} H{x + ts - 24}" stroke="{BOND_D}" stroke-opacity=".45" stroke-width="4"/>')
        p.parts.append(_g("pop", a + (b - a) * k / 24, .25, tile))
    p.parts.append(_life(a, 99, _cnt(cx, 300, 0, 25, a, b - a + .1, size=60, color=BOND_D), fi=.1, fo=.01))
    p.parts.append(_g("fade", a + .2, .3, _t(cx, 345, "OF BONDS", 24, BOND_D, serif=False), style=""))
    t3 = _fr(seg, 2, .2)
    p.parts.append(_g("pop", t3, .35, _idle("bob", _ptag(700, 175, 140, "−1%", RED, "#fff", 38), 4, 2.2, style="")))
    t4 = _fr(seg, 2, .6)
    p.parts.append(_g("pop", t4, .35, f'<circle cx="{cx}" cy="{cy}" r="98" fill="none" stroke="{RED}" stroke-width="8"/>'))
    p.parts.append(_g("pop", t4 + .15, .35, _idle("bob", _ptag(cx + 105, 405, 150, "−25%", RED, "#fff", 40), 4, 2.4, style="")))


def _mini_bank(x, y, s=1.0):
    S = lambda v: v * s
    return (f'<path d="M{x - S(26)} {y - S(30)} L{x} {y - S(48)} L{x + S(26)} {y - S(30)} Z" fill="{INK}"/>'
            f'<rect x="{x - S(22)}" y="{y - S(30)}" width="{S(44)}" height="{S(34)}" fill="#E8E4DE" stroke="{INK}" stroke-width="3"/>'
            + "".join(f'<rect x="{x - S(16) + S(12) * k}" y="{y - S(26)}" width="{S(7)}" height="{S(26)}" fill="{GREY}"/>' for k in range(3))
            + f'<rect x="{x - S(28)}" y="{y + S(4)}" width="{S(56)}" height="{S(7)}" fill="{INK}"/>')


def lv_ltcm(p, seg=None, **_):
    """It happened: LTCM, 1998 (PWG 1999; Federal Reserve History). From the swipe: a 1998 LTCM card, an empty CAPITAL
    outline sized to $4.1bn (31 July 1998) on the left, and on the right two dashed outlines, ASSETS and FUNDING, to
    one scale ($125bn = 360 px). On the first sentence the ASSETS column grows (over $125bn), then the FUNDING column
    grows dark (borrowed) with a 14 px gold sliver on top ($4.8bn of capital), and on '25 to 1' a MORE THAN 25 TO 1
    tag pops. On the second an AUGUST ribbon lands under the card, the capital bar fills gold, its top 44% turns red
    and lifts away while the figure counts $4.1bn to $2.3bn, and a -44% tag pops."""
    k = 80                          # px a billion, the capital bar
    x, w_ = 90, 220
    top, y23 = LV_BASE - 4.1 * k, LV_BASE - 2.3 * k
    ka = 360 / 125                  # px a billion, the balance sheet
    ax, fx_, cw = 430, 615, 160
    atop = LV_BASE - 125 * ka
    cap = 4.8 * ka
    _set(p, _lv_ground()
            + f'<rect x="{x}" y="{top:.1f}" width="{w_}" height="{4.1 * k:.1f}" rx="8" fill="none" stroke="{GREY}" stroke-width="5" stroke-dasharray="16 12"/>'
            + f'<rect x="{x}" y="40" width="{w_}" height="110" rx="14" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            + f'<rect x="{x}" y="40" width="{w_}" height="34" rx="8" fill="{RED}"/>' + _t(x + w_ / 2, 66, "LTCM", 26, "#fff", serif=False)
            + _t(x + w_ / 2, 138, "1998", 56, INK)
            + f'<rect x="{x}" y="{top:.1f}" width="{w_}" height="{4.1 * k:.1f}" rx="8" fill="{GOLD}" fill-opacity=".3"/>'
            + "".join(f'<rect x="{xx}" y="{atop:.1f}" width="{cw}" height="{125 * ka:.1f}" rx="8" fill="{fc}" fill-opacity=".25" stroke="{GREY}" stroke-width="4" '
                      f'stroke-dasharray="14 10"/>' for xx, fc in ((ax, BOND_C), (fx_, DEBT_C)))
            + _t(ax + cw / 2, LV_BASE + 32, "ASSETS", 22, GREY, serif=False) + _t(fx_ + cw / 2, LV_BASE + 32, "FUNDING", 22, GREY, serif=False)
            + _t(400, 636, "SOURCES: PWG REPORT 1999, FEDERAL RESERVE HISTORY", 17, GREY, serif=False))
    grow = "transform-box:fill-box;transform-origin:center bottom"
    t_a = _fr(seg, 0, .12)
    p.parts.append(_g("growY", t_a, .8, _idle("breathe", _lv_bonds(ax, atop, cw, label=False), .006, 3.2, style=grow), style=grow))
    p.parts.append(_g("fade", t_a + .6, .3, _t(ax + cw / 2, 330, "OVER", 26, BOND_D, serif=False) + _t(ax + cw / 2, 372, "$125BN", 38, BOND_D),
                      style=""))
    t_f = _fr(seg, 0, .45)
    p.parts.append(_g("growY", t_f, .7, f'<rect x="{fx_}" y="{atop + cap:.1f}" width="{cw}" height="{125 * ka - cap:.1f}" rx="8" fill="{DEBT_C}" '
                                       f'stroke="{INK}" stroke-width="6"/>' + _t(fx_ + cw / 2, 372, "BORROWED", 24, "#fff", serif=False), style=grow))
    p.parts.append(_g("fade", t_f + .6, .08, _g("slide", t_f + .6, .4, f'<rect x="{fx_}" y="{atop:.1f}" width="{cw}" height="{cap:.1f}" rx="3" '
                                                                       f'fill="{GOLD}" stroke="{INK}" stroke-width="4"/>', style="", y0=-90, y1=0,
                                                ease="out"), style=""))
    p.parts.append(_g("fade", t_f + .9, .3, _t(fx_ + cw / 2, atop - 14, "$4.8BN CAPITAL", 20, INK, serif=False), style=""))
    p.parts.append(_g("pop", _fr(seg, 0, .8), .4, _idle("bob", _ptag(560, 112, 300, "OVER 25 TO 1", INK, "#fff", 32), 4, 2.6, style="")))
    t_g = _fr(seg, 1, .05)
    p.parts.append(_g("growY", t_g, .5, f'<rect x="{x}" y="{y23:.1f}" width="{w_}" height="{2.3 * k:.1f}" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="7"/>',
                      style=grow))
    t_l = _fr(seg, 1, .45)
    gtop = (f'<rect x="{x}" y="{top:.1f}" width="{w_}" height="{1.8 * k:.1f}" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="7"/>')
    p.parts.append(_life(t_g + .1, t_l - t_g - .1 + .01, _g("growY", t_g + .1, .5, gtop, style=grow), fi=.01, fo=.01))
    red = f'<rect x="{x}" y="{top:.1f}" width="{w_}" height="{1.8 * k:.1f}" rx="8" fill="{RED}" stroke="{INK}" stroke-width="7"/>'
    p.parts.append(_life(t_l, 2.0, _g("slide", t_l + .3, 1.0, red, style="", x0=0, y0=0, x1=0, y1=-50, ease="inout"), fi=.01, fo=.6))
    p.parts.append(_life(t_l + .6, 99, f'<rect x="{x}" y="{top:.1f}" width="{w_}" height="{1.8 * k:.1f}" rx="8" fill="none" stroke="{RED}" '
                                       f'stroke-width="4" stroke-dasharray="10 8"/>', fi=.3, fo=.01))
    p.parts.append(_g("fade", t_g + .3, .3, _t(x + w_ / 2, LV_BASE - 26, "CAPITAL", 28, INK, serif=False), style=""))
    p.parts.append(_life(t_g + .3, t_l + .3 - t_g - .3, _t(x + w_ / 2, LV_BASE - 90, "$4.1BN", 46, INK), fi=.2, fo=.01))
    p.parts.append(_life(t_l + .3, 99, _cnt(x + w_ / 2, LV_BASE - 90, 4.1, 2.3, t_l + .3, .9, size=46, pre="$", suf="BN", dec=1), fi=.01, fo=.01))
    p.parts.append(_g("pop", _fr(seg, 1, .1), .35, _ptag(x + w_ / 2 + 20, 196, 210, "AUGUST", RED, "#fff", 34)))
    p.parts.append(_g("pop", t_l + 1.1, .35, _idle("bob", _ptag(x + w_ / 2 + 30, top + 60, 150, "−44%", RED, "#fff", 40), 4, 2.3, style="")))


def lv_rule(p, seg=None, **_):
    """The rule. From the swipe: two lanes, NO DEBT and 25 TO 1, each with the same trade ticket, and two empty
    ROOM TO FALL gauges on the ground. On the first sentence the same teal tick draws onto both tickets and a SAME
    TRADE tag pops between them. On the second the left gauge grows to 100% ('far'), then the right one shows only 4%
    in red, with a ring and a 4% tag ('gone')."""
    _set(p, _lv_ground())
    for cx, head in ((210, "NO DEBT"), (590, "25 TO 1")):
        tk = (f'<rect x="{cx - 130}" y="40" width="260" height="140" rx="14" fill="#fff" stroke="{INK}" stroke-width="6"/>'
              + _t(cx - 110, 80, "THE TRADE", 22, GREY, serif=False, anchor="start")
              + f'<path d="M{cx - 110} 110 H{cx - 10} M{cx - 110} 140 H{cx - 40}" stroke="{GREY}" stroke-width="6" stroke-linecap="round"/>')
        p.parts.append(_g("fade", -1, .05, _idle("bob", tk, 3, 2.6 + cx / 900, style=""), style=""))
        _set(p, _t(cx, 236, head, 34, INK, serif=False)
                + f'<rect x="{cx - 60}" y="{LV_BASE - 300}" width="120" height="300" rx="8" fill="none" stroke="{GREY}" stroke-width="4" stroke-dasharray="12 9"/>')
    _set(p, _t(400, 628, "HOW FAR PRICES CAN FALL BEFORE YOUR MONEY IS GONE", 19, GREY, serif=False))
    t0 = _fr(seg, 0, .25)
    for j, cx in enumerate((210, 590)):
        p.parts.append(_g("draw", t0 + .25 * j, .4, f'<path d="M{cx + 20} 120 L{cx + 50} 150 L{cx + 105} 75" fill="none" stroke="{TEAL}" '
                                                    f'stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>', style=""))
    for j, cx in enumerate((210, 590)):
        p.parts.append(_g("press", _fr(seg, 0, .02) + .15 * j, .5, f'<rect x="{cx - 136}" y="34" width="272" height="152" rx="18" fill="none" '
                                                                 f'stroke="{TEAL}" stroke-width="6"/>'))
    p.parts.append(_g("draw", _fr(seg, 0, .55), .5, f'<path d="M352 200 H448 M362 190 L350 200 L362 210 M438 190 L450 200 L438 210" fill="none" '
                                                    f'stroke="{TEAL}" stroke-width="6" stroke-linecap="round"/>', style=""))
    p.parts.append(_g("pop", _fr(seg, 0, .7), .35, _ptag(400, 112, 130, "SAME", TEAL, "#fff", 30)))
    grow = "transform-box:fill-box;transform-origin:center bottom"
    t1 = _fr(seg, 1, .3)
    p.parts.append(_g("growY", t1, .8, f'<rect x="150" y="{LV_BASE - 300}" width="120" height="300" rx="8" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>',
                      style=grow))
    p.parts.append(_g("pop", t1 + .6, .3, _t(210, LV_BASE - 140, "100%", 44, "#fff")))
    t2 = _fr(seg, 1, .7)
    p.parts.append(_g("growY", t2, .4, f'<rect x="530" y="{LV_BASE - 12}" width="120" height="12" rx="3" fill="{RED}" stroke="{INK}" stroke-width="4"/>',
                      style=grow))
    p.parts.append(_g("pop", t2 + .25, .35, f'<rect x="516" y="{LV_BASE - 30}" width="148" height="44" rx="12" fill="none" stroke="{RED}" stroke-width="7"/>'))
    p.parts.append(_g("pop", t2 + .35, .35, _idle("bob", _ptag(600, LV_BASE - 90, 150, "4%", RED, "#fff", 44), 4, 2.3, style="")))
    _push(p, seg[0][0], seg[1][1] - seg[0][0], 1.04, 400, 420)


def lv_asks(p, **_):
    """The close, all on the panel from frame 0: a 10 TO 1 tag over a bonds column with a dashed line across it, a
    bobbing ? beside the line, the trader pointing at the viewer. The answer (10%) is not shown."""
    top = LV_BASE - 100 * LV_K
    _set(p, _lv_ground() + _lv_bonds(90, top, 220)
            + f'<path d="M60 {top + 60} H340" stroke="{RED}" stroke-width="6" stroke-dasharray="16 12"/>')
    p.parts.append(_g("fade", -1, .05, _idle("bob", _ptag(200, top - 60, 230, "10 TO 1", INK, "#fff", 44), 4, 2.4, style=""), style=""))
    p.parts.append(_g("float", 0, 1, _t(420, top + 110, "?", 160, RED), style="", amp=10, w=2.4))
    _trader_poses(p, 650, LV_BASE + 30, .9, [(0, "point")], look=-1)


SCENES.update({f.__name__: f for f in (lv_hook, lv_zero, lv_one, lv_ratio, lv_ltcm, lv_rule, lv_asks)})
