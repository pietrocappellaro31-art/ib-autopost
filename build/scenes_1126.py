"""
26 Nov 2026 Reel scenes (build/reels_deferred-revenue.py, build/reels_new-shares-myth.py,
build/reels_points-percent.py). Our own drawings and round numbers only; every figure is worked in the episode
docstrings. Registered into sketch.SCENES on import, so picture("dr_hook", ...) works as for any scene.

The 25 Nov next improvement, built into every scene here: each beat has a moving element from its first frame (a
loop that is already running at the swipe: a riding dot, a dropping coin, a travelling light) and a second large
move inside its longest sentence, so no beat waits for its first word to move.
"""

import math

from sketch import (SCENES, _set, _g, _life, _idle, _t, _cnt, _fr, _stamp, _pill, _ptag, _cam, _coin_shape, _nv_col,
                    _ap_cal, _ap_cal_light, INK, RED, TEAL, GREY)

GOLD = "#F2C35B"
CASH_C, REV_C, OWE_C, BUS_C, NEW_C = "#5EC8B4", "#F2C35B", "#E8836B", "#B9B4AC", "#5EC8B4"
MONTHS = "JFMAMJJASOND"


def _loop(p, a, b, period, inner, x1=0, y1=0, ease="inout", x0=0, y0=0, fo=.05):
    """A move that repeats from a to b (already running at the swipe when a is before the beat starts)."""
    n = max(1, int((b - a) / period) + 1)
    for r in range(n):
        s = a + period * r
        p.parts.append(_life(s, period, _g("slide", s, period * .9, inner, style="", x0=x0, y0=y0, x1=x1, y1=y1, ease=ease), fi=.02, fo=fo))


def _span(seg):
    return seg[0][0] - .5, seg[-1][1] + .7


def _ground(base=590, x0=30, x1=770):
    return f'<path d="M{x0} {base} H{x1}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'


def _col(x, w_, v, fill, base=590, k=3.6, label=None, size=40, dash=False, op=1.0):
    return _nv_col(x, w_, v, fill, k=k, base=base, label=label, size=size, dash=dash, op=op)


def _strip(x0, y, cw=58, ch=56, lit=None, labels=MONTHS):
    s = ""
    for j, m in enumerate(labels):
        x = x0 + j * cw
        fill = REV_C if lit is not None and j <= lit else "#F4F1EC"
        s += (f'<rect x="{x + 3}" y="{y}" width="{cw - 6}" height="{ch}" rx="8" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
              + _t(x + cw / 2, y + ch / 2 + 9, m, 26, INK, serif=False))
    return s


def _cell_light(p, x0, y, j, t, cw=58, ch=56, life=99, col=REV_C, lab=None):
    x = x0 + j * cw
    p.parts.append(_life(t, life, _g("pop", t, .22, f'<rect x="{x + 3}" y="{y}" width="{cw - 6}" height="{ch}" rx="8" fill="{col}" stroke="{INK}" stroke-width="5"/>'
                                     + _t(x + cw / 2, y + ch / 2 + 9, lab or MONTHS[j], 26, INK, serif=False)), fi=.02, fo=.05))


def _dumbbell(cx, cy, s=1.0, col=INK):
    w, h = 26 * s, 64 * s
    return (f'<rect x="{cx - 70 * s:.0f}" y="{cy - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{6 * s:.0f}" fill="{col}"/>'
            f'<rect x="{cx + 44 * s:.0f}" y="{cy - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{6 * s:.0f}" fill="{col}"/>'
            f'<rect x="{cx - 44 * s:.0f}" y="{cy - 8 * s:.0f}" width="{88 * s:.0f}" height="{16 * s:.0f}" rx="{5 * s:.0f}" fill="{col}"/>')


def _card(x, y, w_=300, h_=190, head="GYM PASS", l1="1 YEAR", l2="$120"):
    return (f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="20" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{x}" y="{y}" width="{w_}" height="54" rx="20" fill="{RED}" stroke="{INK}" stroke-width="6"/>'
            + _t(x + w_ / 2, y + 38, head, 30, "#fff", serif=False) + _t(x + w_ / 2, y + 106, l1, 34, INK, serif=False)
            + _t(x + w_ / 2, y + 168, l2, 56, INK))


# ---------------------------------------------------------------------------------------------------------------
# Reel A: deferred revenue. A gym sells a one-year membership for $120 paid up front on 1 January: cash +$120 on
# day one; revenue $10 a month as the gym delivers; end of January: revenue $10, deferred revenue (a liability)
# $110; cash $120 = $110 owed + $10 earned. Each month $10 moves from the liability to revenue; by December the
# liability is $0 and revenue $120. Close (not shown): a 6-month $60 plan paid 1 March: March revenue $10, owed $50.

DR_K = 3.6


def dr_hook(p, seg=None, **_):
    """The hook. From frame 0 the clash is on the panel: CASH IN, a full $120 teal column with coins still dropping
    into it, against REVENUE, a $10 gold slice under a dashed $120 ghost with a ? swinging on it. On the first
    sentence a JANUARY pill pops over both, the cash column presses and the $10 slice pulses; on the question a red
    bracket draws up the empty ghost and THE OTHER $110? bobs."""
    xc, xr, w_ = 80, 480, 230
    a, b = _span(seg)
    _set(p, _ground() + _col(xc, w_, 120, CASH_C, k=DR_K) + _col(xr, w_, 120, REV_C, k=DR_K, dash=True, op=.07)
         + _col(xr, w_, 10, REV_C, k=DR_K) + _t(xc + w_ / 2, 630, "CASH IN", 30, INK, serif=False)
         + _t(xr + w_ / 2, 630, "REVENUE", 30, INK, serif=False)
         + _t(xc + w_ / 2, 590 - 120 * DR_K - 22, "$120", 56, INK) + _t(xr + w_ / 2, 590 - 10 * DR_K - 20, "$10", 52, INK))
    _loop(p, a, b, .7, _coin_shape(xc + w_ / 2, 590 - 120 * DR_K + 40, 30, "$"), y0=-130, y1=60, ease="in", fo=.15)
    p.parts.append(_idle("swing", _ptag(xr + w_ / 2, 300, 150, "?", RED, "#fff", 70), 10, 2.0, style="transform-box:fill-box;transform-origin:center top"))
    for j in range(int((b - a) / .7)):
        p.parts.append(_g("ripple", a + .7 * j, .6, f'<circle cx="{xr + w_ / 2}" cy="{590 - 5 * DR_K:.0f}" r="40" fill="none" stroke="{REV_C}" stroke-width="6"/>'))
    t0 = _fr(seg, 0, .15)
    p.parts.append(_g("pop", t0, .35, _pill(400, 70, "JANUARY", INK, "#fff", 34)))
    p.parts.append(_g("press", _fr(seg, 0, .3), .4, _col(xc, w_, 120, CASH_C, k=DR_K)))
    p.parts.append(_g("press", _fr(seg, 0, .75), .4, _col(xr, w_, 10, REV_C, k=DR_K)))
    t1 = _fr(seg, 1, .05)
    top, bot = 590 - 120 * DR_K, 590 - 10 * DR_K
    p.parts.append(_g("draw", t1, .5, f'<path d="M{xr + w_ + 14} {bot:.0f} h18 V{top:.0f} h-18" stroke="{RED}" stroke-width="7" fill="none"/>', style=""))
    p.parts.append(_g("pop", t1 + .3, .35, _idle("bob", _pill(xr + w_ / 2 - 20, 420, "THE OTHER $110?", RED, "#fff", 28), 6, 1.8, style="")))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 330, 1.0), (t0 + .3, 250, 360, 1.08), (_fr(seg, 0, .7), 560, 420, 1.08), (t1 + .4, 540, 330, 1.05), (end, 400, 320, 1.0)])


def dr_setup(p, seg=None, **_):
    """The set-up. A GYM PASS card (1 YEAR, $120) swings at the top left with a dumbbell bobbing beside it; a
    12-month calendar of $10 cells waits on the right. On the first sentence a PAID 1 JAN stamp lands and coins count
    to $120 under the card; on the second the cells light M1 to M12 and $120 / 12 = $10 pops, then a light runs round
    the cells."""
    a, b = _span(seg)
    cx, cy = 360, 390
    _set(p, _ap_cal(cx, cy, rate="$10") + _t(cx + 192, cy - 20, "12 MONTHS", 26, "#fff", serif=False))
    p.parts.append(_idle("swing", _card(40, 40), 3, 2.2, style="transform-box:fill-box;transform-origin:center top"))
    p.parts.append(_idle("bob", _dumbbell(560, 120, 1.3), 10, 1.4))
    t0 = _fr(seg, 0, .55)
    p.parts.append(_stamp(70, 250, 240, 70, "PAID 1 JAN", RED, t0, size=36, rot=-6))
    t0b = _fr(seg, 0, .25)
    for j in range(6):
        p.parts.append(_life(t0b + .12 * j, 99, _g("slide", t0b + .12 * j, .25, _coin_shape(80 + 40 * j, 560 - 0 * j, 30, "$"), style="", x0=0, y0=-200, x1=0, y1=0, ease="out"), fi=.02, fo=.01))
    p.parts.append(_life(t0b, 99, _cnt(190, 480, 0, 120, t0b, .9, size=56, color=TEAL), fi=.05, fo=.01))
    t1 = _fr(seg, 1, .05)
    gap = max(.1, (seg[1][1] - t1) * .7 / 12)
    _ap_cal_light(p, cx, cy, t1, gap, col=REV_C)
    p.parts.append(_g("pop", t1 + 12 * gap, .35, _idle("bob", _pill(550, 280, "$120 / 12 = $10", INK, "#fff", 30), 5, 1.8, style="")))
    t_run = t1 + 12 * gap + .2
    for r in range(int((b - t_run) / .25) + 1):
        j = r % 12
        x_, y_ = cx + (j % 4) * 96, cy + (j // 4) * 64
        p.parts.append(_g("press", t_run + .25 * r, .3, f'<rect x="{x_ + 4}" y="{y_ + 4}" width="88" height="56" rx="8" fill="none" stroke="{RED}" stroke-width="6"/>'))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 260, 260, 1.08), (t0 + .3, 220, 330, 1.06), (t1, 540, 440, 1.08), (t1 + 12 * gap, 520, 400, 1.04), (end, 400, 320, 1.0)])


def dr_cash(p, seg=None, **_):
    """Cash against revenue. A strip of the twelve months runs along the top (a light already travelling along it
    at the swipe); below, CASH and REVENUE columns stand dashed. On the first sentence the cash column fills to $120
    in one go on the J cell with its count (DAY 1); on the second the revenue column climbs one $10 slice per month as
    each month cell lights, its count stepping to $120."""
    a, b = _span(seg)
    k, base, x0s, y_s = 3.3, 590, 52, 50
    xc, xr, w_ = 110, 470, 220
    _set(p, _strip(x0s, y_s) + _ground(base) + _col(xc, w_, 120, CASH_C, k=k, dash=True, op=.07) + _col(xr, w_, 120, REV_C, k=k, dash=True, op=.07)
         + _t(xc + w_ / 2, base + 40, "CASH", 30, INK, serif=False) + _t(xr + w_ / 2, base + 40, "REVENUE", 30, INK, serif=False))
    _loop(p, a, _fr(seg, 1, .05), 2.2, f'<circle cx="{x0s + 29}" cy="{y_s + 74}" r="10" fill="{RED}"/>', x1=11 * 58, ease="inout")
    t0 = _fr(seg, 0, .2)
    _cell_light(p, x0s, y_s, 0, t0, col=CASH_C)
    p.parts.append(_life(t0, 99, _g("growY", t0, .5, _col(xc, w_, 120, CASH_C, k=k), style="transform-box:fill-box;transform-origin:center bottom"), fi=.01, fo=.01))
    p.parts.append(_life(t0, 99, _cnt(xc + w_ / 2, base - 120 * k - 22, 0, 120, t0, .5, size=52), fi=.05, fo=.01))
    p.parts.append(_g("pop", t0 + .5, .35, _idle("swing", _pill(xc + w_ / 2, base - 60 * k, "DAY 1", INK, "#fff", 34), 4, 1.9, style="transform-box:fill-box;transform-origin:center top")))
    t1 = _fr(seg, 1, .1)
    gap = max(.12, (seg[1][1] + .3 - t1) / 12)
    for j in range(12):
        t = t1 + gap * j
        _cell_light(p, x0s, y_s, j, t)
        p.parts.append(_life(t, 99, _g("pop", t, .22, _col(xr, w_, 10, REV_C, k=k, base=base - 10 * j * k)), fi=.02, fo=.01))
        p.parts.append(_life(t, gap if j < 11 else 99, _t(xr + w_ / 2, base - 10 * (j + 1) * k - 18, f"${10 * (j + 1)}", 48, INK), fi=.02, fo=.02))
    p.parts.append(_g("pop", t1 + 12 * gap, .35, _idle("bob", _pill(xr + w_ / 2, 300, "$10 A MONTH", TEAL, "#fff", 30), 5, 1.7, style="")))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 300, 340, 1.05), (t0 + .4, 230, 380, 1.06), (t1, 560, 330, 1.05), (t1 + 6 * gap, 480, 300, 1.03), (end, 400, 320, 1.0)])


def dr_answer(p, seg=None, **_):
    """The answer, a balance sheet to one scale. Left: CASH $120 (teal), a dot riding up and down it from the swipe.
    On the first sentence the $10 EARNED slice pops at the right's base and a red $110 block slides across from the
    cash column onto it, DEFERRED REVENUE; on the second a LIABILITY stamp lands, eleven small dumbbells (months still
    owed) pop down the block, and $120 = $110 + $10 draws along the top."""
    a, b = _span(seg)
    k, base = 3.6, 600
    xl, xr, w_ = 70, 470, 250
    _set(p, _ground(base) + _col(xl, w_, 120, CASH_C, k=k, base=base) + _col(xr, w_, 120, OWE_C, k=k, base=base, dash=True, op=.07)
         + _t(xl + w_ / 2, base - 60 * k + 14, "CASH", 40, INK, serif=False) + _t(xl + w_ / 2, base + 34, "WHAT IT HAS", 24, INK, serif=False)
         + _t(xr + w_ / 2, base + 34, "WHERE IT CAME FROM", 24, INK, serif=False))
    _loop(p, a, b, 1.6, f'<circle cx="{xl + w_ + 24}" cy="{base - 10}" r="11" fill="{INK}"/>', y1=-120 * k + 20, ease="inout")
    t0 = _fr(seg, 0, .1)
    p.parts.append(_life(t0, 99, _g("pop", t0, .3, _col(xr, w_, 10, REV_C, k=k, base=base) + _t(xr + w_ / 2, base - 5 * k + 12, "EARNED $10", 30, INK, serif=False)), fi=.02, fo=.01))
    t0b = _fr(seg, 0, .35)
    blk = _col(xr, w_, 110, OWE_C, k=k, base=base - 10 * k)
    p.parts.append(_life(t0b, 99, _g("slide", t0b, .8, blk, style="", x0=xl - xr, y0=0, x1=0, y1=0, ease="inout"), fi=.02, fo=.01))
    p.parts.append(_life(t0b + .8, 99, _pill(xr + w_ / 2, base - 120 * k - 30, "DEFERRED REVENUE $110", OWE_C, INK, 24), fi=.2, fo=.01))
    t1 = _fr(seg, 1, .05)
    for j in range(11):                       # eleven $10 months still owed, F to D, ruled into the block
        yj = base - 10 * k - 10 * k * (j + 1)
        p.parts.append(_life(t1 + .1 * j, 99, _g("pop", t1 + .1 * j, .2, f'<path d="M{xr} {yj:.0f} H{xr + w_}" stroke="{INK}" stroke-width="3"/>'
                                                  + _t(xr + 28, yj + 27, MONTHS[j + 1], 22, INK, serif=False)), fi=.02, fo=.01))
    p.parts.append(_stamp(xr + 40, base - 10 * k - 190, 200, 62, "LIABILITY", RED, t1 + 1.2, size=34, rot=-5))
    for j, (x_, lab) in enumerate(((60, "$120"), (300, "= $110"), (550, "+ $10"))):
        p.parts.append(_g("pop", _fr(seg, 1, .55) + .2 * j, .3, f'<rect x="{x_}" y="20" width="200" height="74" rx="14" fill="#fff" stroke="{INK}" stroke-width="5"/>' + _t(x_ + 100, 72, lab, 46, INK)))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 360, 1.03), (t0b, 400, 380, 1.06), (t1, 590, 300, 1.1), (t1 + 1.4, 400, 200, 1.06), (end, 400, 320, 1.0)])


def dr_year(p, seg=None, **_):
    """The year. The month strip on top, OWED (red, $110) and REVENUE (gold, $10) below. From the swipe a $10 slab
    lifts off OWED, travels and lands on REVENUE, once a month: OWED steps down to $0 and REVENUE up to $120 across
    both sentences, each month cell lighting as its slab lands; ALL EARNED stamps at the end."""
    a, b = _span(seg)
    k, base, x0s, y_s = 3.3, 590, 52, 50
    xo, xr, w_ = 110, 470, 220
    _set(p, _strip(x0s, y_s, lit=0) + _ground(base) + _col(xr, w_, 120, REV_C, k=k, dash=True, op=.07)
         + _t(xo + w_ / 2, base + 40, "OWED", 30, INK, serif=False) + _t(xr + w_ / 2, base + 40, "REVENUE", 30, INK, serif=False)
         + _col(xr, w_, 10, REV_C, k=k))
    t_s, t_e = seg[0][0] - .2, _fr(seg, 1, .55)
    gap = (t_e - t_s) / 11
    for j in range(11):                       # slab j leaves OWED at step j (top slab first)
        t = t_s + gap * j
        y_from = base - (110 - 10 * j) * k
        p.parts.append(_life(-1, t + 1.01, _col(xo, w_, 10, OWE_C, k=k, base=y_from + 10 * k), fi=.01, fo=.01))
        dy = (base - 10 * (j + 1) * k) - (y_from)
        p.parts.append(_life(t, gap * .8 + .02, _g("slide", t, gap * .8, _col(xo, w_, 10, OWE_C, k=k, base=y_from + 10 * k), style="", x0=0, y0=0, x1=xr - xo, y1=dy, ease="inout"), fi=.01, fo=.01))
        p.parts.append(_life(t + gap * .8, 99, _col(xr, w_, 10, REV_C, k=k, base=base - 10 * (j + 1) * k), fi=.01, fo=.01))
        _cell_light(p, x0s, y_s, j + 1, t + gap * .8)
        p.parts.append(_life(-1 if j == 0 else t, (t + gap) - (-1 if j == 0 else t), _t(xo + w_ / 2, base - (110 - 10 * j) * k - 18, f"${110 - 10 * j}", 46, RED), fi=.01, fo=.01))
        p.parts.append(_life(-1 if j == 0 else t + gap * .8 - gap, gap + (1.01 if j == 0 else 0), _t(xr + w_ / 2, base - 10 * (j + 1) * k - 18, f"${10 * (j + 1)}", 46, INK), fi=.01, fo=.01))
    p.parts.append(_life(t_e, 99, _t(xo + w_ / 2, base - 18, "$0", 52, RED) + _t(xr + w_ / 2, base - 120 * k - 18, "$120", 52, INK), fi=.05, fo=.01))
    p.parts.append(_stamp(250, 300, 300, 80, "ALL EARNED", TEAL, t_e + .2, size=40, rot=-5))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 330, 1.03), (_fr(seg, 0, .5), 360, 360, 1.06), (seg[1][0], 440, 360, 1.06), (t_e, 400, 300, 1.04), (end, 400, 320, 1.0)])


def dr_rule(p, seg=None, **_):
    """The rule at full panel height. Two tiles fill the top: CASH: WHEN PAID (teal) and REVENUE: WHEN EARNED (gold).
    Below, a chart from JAN to DEC: on the first sentence the cash line jumps to $120 in January and runs flat while
    the revenue staircase climbs $10 a month, a dot riding each; on the second the gap between them shades red,
    NOT EARNED YET, and keeps pulsing."""
    a, b = _span(seg)
    tiles = (f'<rect x="20" y="20" width="370" height="150" rx="18" fill="{CASH_C}" stroke="{INK}" stroke-width="6"/>'
             + _t(205, 82, "CASH:", 40, INK, serif=False) + _t(205, 140, "WHEN PAID", 40, INK, serif=False)
             + f'<rect x="410" y="20" width="370" height="150" rx="18" fill="{REV_C}" stroke="{INK}" stroke-width="6"/>'
             + _t(595, 82, "REVENUE:", 40, INK, serif=False) + _t(595, 140, "WHEN EARNED", 40, INK, serif=False))
    X0, X1, Y0, Y1 = 90, 750, 590, 230             # chart box: $0 at Y0, $120 at Y1
    dx = (X1 - X0) / 12
    yv = lambda v: Y0 - (Y0 - Y1) * v / 120
    axes = (f'<path d="M{X0} {Y1 - 20} V{Y0} H{X1 + 10}" stroke="{INK}" stroke-width="5" fill="none"/>'
            + "".join(_t(X0 + dx * (j + .5), Y0 + 34, m, 24, INK, serif=False) for j, m in enumerate(MONTHS))
            + _t(X0 - 12, Y1 + 8, "$120", 24, INK, serif=False, anchor="end") + _t(X0 - 12, Y0, "$0", 24, INK, serif=False, anchor="end"))
    _set(p, tiles + axes)
    cash = f'M{X0} {Y0} V{yv(120):.0f} H{X1}'
    stair = f"M{X0} {Y0}" + "".join(f" V{yv(10 * (j + 1)):.0f} H{X0 + dx * (j + 1):.0f}" for j in range(12))
    t0 = _fr(seg, 0, .05)
    p.parts.append(_g("press", t0, .4, f'<rect x="20" y="20" width="370" height="150" rx="18" fill="none" stroke="{RED}" stroke-width="8"/>'))
    p.parts.append(_g("press", _fr(seg, 0, .55), .4, f'<rect x="410" y="20" width="370" height="150" rx="18" fill="none" stroke="{RED}" stroke-width="8"/>'))
    p.parts.append(_life(t0, 99, _g("draw", t0, .6, f'<path d="{cash}" stroke="{TEAL}" stroke-width="9" fill="none" stroke-linejoin="round"/>', style=""), fi=.01, fo=.01))
    t0b = _fr(seg, 0, .45)
    p.parts.append(_life(t0b, 99, _g("draw", t0b, 1.8, f'<path d="{stair}" stroke="{GOLD}" stroke-width="9" fill="none" stroke-linejoin="round"/>', style=""), fi=.01, fo=.01))
    _loop(p, a, b, 2.4, f'<circle cx="{X0}" cy="{yv(120):.0f}" r="13" fill="{TEAL}" stroke="{INK}" stroke-width="3"/>', x1=X1 - X0)
    for r in range(int((b - t0b) / 2.4) + 1):
        s = t0b + 2.4 * r
        p.parts.append(_life(s, 2.4, _g("slide", s, 2.2, f'<circle cx="{X0}" cy="{Y0}" r="13" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>', style="", x0=0, y0=0, x1=X1 - X0, y1=yv(120) - Y0, ease="inout"), fi=.02, fo=.05))
    t1 = _fr(seg, 1, .1)
    gap_poly = f"M{X0} {yv(120):.0f} H{X1} " + "".join(f"L{X0 + dx * (12 - j):.0f} {yv(10 * (12 - j)):.0f} L{X0 + dx * (11 - j):.0f} {yv(10 * (12 - j)):.0f} " for j in range(12)) + "Z"
    p.parts.append(_life(t1, 99, f'<path d="{gap_poly}" fill="{RED}" fill-opacity=".22"/>', fi=.4, fo=.01))
    p.parts.append(_g("pop", t1 + .3, .35, _idle("bob", _pill(330, yv(95), "NOT EARNED YET", RED, "#fff", 30), 6, 1.8, style="")))
    for j in range(4):
        p.parts.append(_g("ripple", t1 + .6 + .6 * j, .55, f'<circle cx="{X0 + 2 * dx:.0f}" cy="{yv(80):.0f}" r="50" fill="none" stroke="{RED}" stroke-width="5"/>'))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 320, 1.0), (t0, 400, 200, 1.06), (t0b + .5, 420, 420, 1.06), (t1, 330, 380, 1.08), (end, 400, 320, 1.0)])


def dr_asks(p, **_):
    """The close: a 6-MONTH PASS card ($60) swinging, a strip of six months MAR to AUG with MAR pulsing, coins dropping
    into the card's corner, and two plates, MARCH REVENUE ? and STILL OWED ?, bobbing. No answer shown."""
    _set(p, _strip(40, 300, cw=120, ch=90, labels="MAMJJA") + _t(400, 284, "PAID 1 MARCH", 28, INK, serif=False))
    for r in range(30):
        j = 1 + r % 5
        p.parts.append(_g("press", p.at(0) + .45 * r, .4, f'<rect x="{40 + 120 * j + 3}" y="300" width="114" height="90" rx="8" fill="none" stroke="{TEAL}" stroke-width="6"/>'))
    for r in range(14):
        a_ = p.at(0) + 1.0 * r
        p.parts.append(_life(a_, 1.0, _g("slide", a_, .9, _coin_shape(190, 150, 30, "$"), style="", x0=0, y0=-140, x1=0, y1=40, ease="in"), fi=.02, fo=.2))
    p.parts.append(_idle("swing", _card(40, 40, 300, 190, "GYM PASS", "6 MONTHS", "$60"), 3, 2.2, style="transform-box:fill-box;transform-origin:center top"))
    p.parts.append(_idle("bob", _dumbbell(570, 140, 1.2), 10, 1.4))
    for r in range(10):
        p.parts.append(_g("press", p.at(0) + .9 * r, .45, f'<rect x="43" y="300" width="114" height="90" rx="8" fill="{REV_C}" stroke="{RED}" stroke-width="7"/>' + _t(100, 354, "M", 26, INK, serif=False)))
    for j, (x_, l1) in enumerate(((40, "MARCH REVENUE"), (420, "STILL OWED"))):
        p.parts.append(_idle("bob", f'<rect x="{x_}" y="430" width="340" height="170" rx="18" fill="#fff" stroke="{INK}" stroke-width="6"/>'
                             + _t(x_ + 170, 480, l1, 30, INK, serif=False) + _t(x_ + 170, 572, "?", 80, RED), 6, 1.8 + .3 * j, ph=j))
    for j in range(8):
        p.parts.append(_g("ripple", p.at(.1) + .9 * j, .8, f'<circle cx="100" cy="345" r="50" fill="none" stroke="{RED}" stroke-width="5"/>'))


SCENES.update({f.__name__: f for f in (dr_hook, dr_setup, dr_cash, dr_answer, dr_year, dr_rule, dr_asks)})


# ---------------------------------------------------------------------------------------------------------------
# Reel B: new shares at a fair price. Company worth $1,000, 100 shares at $10; you hold 10 (10%, $100). It sells 25
# new shares at $10 for $250: worth $1,250, 125 shares, still $10 a share; your 10 are 8% and still $100. Sold at
# $6 instead: $150 in, $1,150 / 125 = $9.20 a share, your 10 = $92. Close (not shown): sold at $14: $1,350 / 125 =
# $10.80, your 10 = $108.

def _wedge(cx, cy, r, a0, a1, fill, op=1.0):
    p0 = (cx + r * math.sin(math.radians(a0)), cy - r * math.cos(math.radians(a0)))
    p1 = (cx + r * math.sin(math.radians(a1)), cy - r * math.cos(math.radians(a1)))
    large = 1 if a1 - a0 > 180 else 0
    return (f'<path d="M{cx} {cy} L{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 {large} 1 {p1[0]:.1f} {p1[1]:.1f} Z" fill="{fill}" fill-opacity="{op}" '
            f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')


def _pie(cx, cy, r, you, new=0.0):
    """A pie for the company: grey for the others, gold for your slice (you, a share of 1), teal for new shares."""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BUS_C}" stroke="{INK}" stroke-width="6"/>'
    if new:
        s += _wedge(cx, cy, r, 360 * (1 - new), 360, NEW_C)
    return s + _wedge(cx, cy, r, 0, 360 * you, GOLD)


def _share(x, y, s=44, fill=BUS_C, lab=None):
    out = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="7" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
    if lab:
        out += _t(x + s / 2, y + s / 2 + 7, lab, 18, INK, serif=False)
    return out


def ns_hook(p, seg=None, **_):
    """The hook. From frame 0: the company as a pie with your 10% gold slice (left) and a bigger pie with your slice
    at 8% and new teal shares (right), 10% and 8% under them; a dot rides from one pie to the other for ever. On the
    first sentence the left slice presses, then the right one; on the question LOST? and a red down arrow pop and a ?
    swings."""
    a, b = _span(seg)
    r1, r2 = 150, 168
    _set(p, _pie(200, 300, r1, .10) + _pie(590, 300, r2, .08, new=.2)
         + _t(200, 530, "10%", 80, INK) + _t(590, 530, "8%", 80, RED) + _t(200, 590, "YOUR SLICE", 26, INK, serif=False) + _t(590, 590, "AFTER NEW SHARES", 26, INK, serif=False))
    _loop(p, a, b, 1.5, f'<circle cx="250" cy="120" r="12" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>', x1=380, y1=0, ease="inout")
    p.parts.append(_idle("breathe", _wedge(200, 300, r1, 0, 36, GOLD), .04, 1.6))
    p.parts.append(_idle("breathe", _wedge(590, 300, r2, 0, 28.8, GOLD), .04, 1.6, ph=1))
    t0 = _fr(seg, 0, .15)
    p.parts.append(_g("press", t0, .45, _t(200, 530, "10%", 80, INK)))
    p.parts.append(_g("press", _fr(seg, 0, .7), .45, _t(590, 530, "8%", 80, RED)))
    for j in range(3):
        p.parts.append(_g("ripple", _fr(seg, 0, .7) + .4 * j, .5, f'<circle cx="590" cy="500" r="60" fill="none" stroke="{RED}" stroke-width="5"/>'))
    t1 = _fr(seg, 1, .05)
    p.parts.append(_g("pop", t1, .35, _idle("bob", _pill(400, 60, "LOST MONEY?", RED, "#fff", 34), 6, 1.8, style="")))
    p.parts.append(_g("pop", t1 + .3, .4, _idle("swing", _ptag(720, 140, 110, "?", RED, "#fff", 60), 10, 2.0, style="transform-box:fill-box;transform-origin:center top")))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 330, 1.0), (t0, 240, 350, 1.08), (_fr(seg, 0, .7), 560, 380, 1.08), (t1 + .3, 400, 280, 1.04), (end, 400, 320, 1.0)])


def ns_setup(p, seg=None, **_):
    """The set-up. A 10 x 10 grid of share tiles (dashed until they build), a $10 A SHARE tag swinging on the right
    from the swipe. On the first sentence the rows build top to bottom with 100 SHARES and $1,000 counting; on the
    second your top row turns gold, YOU: 10 = 10% pops and a light runs along your row."""
    a, b = _span(seg)
    s, g = 46, 6
    x0, y0 = 40, 60
    ghost = "".join(f'<rect x="{x0 + c * (s + g)}" y="{y0 + r * (s + g)}" width="{s}" height="{s}" rx="7" fill="none" stroke="{GREY}" stroke-width="2" stroke-dasharray="6 5"/>' for r in range(10) for c in range(10))
    _set(p, ghost + f'<rect x="580" y="290" width="190" height="120" rx="16" fill="#fff" stroke="{INK}" stroke-width="6"/>' + _t(675, 326, "COMPANY", 22, GREY, serif=False)
         + f'<rect x="580" y="430" width="190" height="120" rx="16" fill="#fff" stroke="{INK}" stroke-width="6"/>' + _t(675, 466, "SHARES", 22, GREY, serif=False))
    p.parts.append(_idle("swing", _ptag(670, 130, 190, "$10", INK, "#fff", 56), 8, 2.0, style="transform-box:fill-box;transform-origin:center top"))
    p.parts.append(_idle("bob", _t(675, 230, "A SHARE", 28, INK, serif=False), 5, 1.6))
    t0 = _fr(seg, 0, .15)
    gap = max(.08, (seg[0][1] - t0) * .75 / 10)
    for r in range(10):
        row = "".join(_share(x0 + c * (s + g), y0 + r * (s + g), s) for c in range(10))
        p.parts.append(_life(t0 + gap * r, 99, _g("pop", t0 + gap * r, .25, row, style="transform-box:fill-box;transform-origin:center"), fi=.02, fo=.01))
    p.parts.append(_life(t0, 99, _cnt(675, 390, 0, 1000, t0, gap * 10, size=46), fi=.05, fo=.01))
    p.parts.append(_life(t0, 99, _cnt(675, 530, 0, 100, t0, gap * 10, size=46, pre=""), fi=.05, fo=.01))
    t1 = _fr(seg, 1, .1)
    you = "".join(_share(x0 + c * (s + g), y0, s, GOLD) for c in range(10))
    p.parts.append(_life(t1, 99, _g("pop", t1, .35, you), fi=.02, fo=.01))
    p.parts.append(_g("pop", t1 + .4, .35, _idle("bob", _pill(290, 30 + 0, "YOU: 10 SHARES = 10%", GOLD, INK, 26), 4, 1.7, style="")))
    p.parts.append(_g("pop", _fr(seg, 1, .7), .35, _pill(675, 600, "YOURS: $100", TEAL, "#fff", 26)))
    for r in range(int((b - t1) / .2) + 1):
        c = r % 10
        p.parts.append(_g("press", t1 + .5 + .2 * r, .25, f'<rect x="{x0 + c * (s + g) - 3}" y="{y0 - 3}" width="{s + 6}" height="{s + 6}" rx="8" fill="none" stroke="{RED}" stroke-width="5"/>'))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 320, 1.03), (t0 + .4, 300, 360, 1.05), (t1, 300, 200, 1.08), (t1 + 1.0, 420, 300, 1.04), (end, 400, 320, 1.0)])


def ns_new(p, seg=None, **_):
    """The new shares. The 100-share grid (your row gold) with dashed places for 25 more under it and a cash jar on
    the right with a NEW SHARES $10 tag swinging from the swipe. On the first sentence the 25 teal tiles slide in one
    after another and coins drop into the jar counting to $250; on the second the share count steps 100 to 125 and
    your stake counts 10% down to 8%."""
    a, b = _span(seg)
    s, g = 38, 5
    x0, y0 = 30, 40
    old = "".join(_share(x0 + c * (s + g), y0 + r * (s + g), s, GOLD if r == 0 else BUS_C) for r in range(10) for c in range(10))
    ghost = "".join(f'<rect x="{x0 + (j % 10) * (s + g)}" y="{y0 + (10 + j // 10) * (s + g)}" width="{s}" height="{s}" rx="7" fill="none" stroke="{GREY}" stroke-width="2" stroke-dasharray="6 5"/>' for j in range(25))
    jar = (f'<path d="M520 250 V420 Q520 460 560 460 H720 Q760 460 760 420 V250" fill="#EAF6F3" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="506" y="226" width="268" height="30" rx="10" fill="{INK}"/>' + _t(640, 490, "CASH IN", 24, INK, serif=False))
    _set(p, old + ghost + jar)
    p.parts.append(_idle("swing", _pill(630, 90, "NEW: $10 EACH", NEW_C, INK, 26), 5, 2.0, style="transform-box:fill-box;transform-origin:center top"))
    _loop(p, a, _fr(seg, 0, .2), .6, _coin_shape(640, 200, 22, "$"), y0=-40, y1=200, ease="in", fo=.1)
    t0 = _fr(seg, 0, .2)
    gap = max(.05, (seg[0][1] - t0) * .8 / 25)
    for j in range(25):
        t = t0 + gap * j
        p.parts.append(_life(t, 99, _g("slide", t, .3, _share(x0 + (j % 10) * (s + g), y0 + (10 + j // 10) * (s + g), s, NEW_C), style="", x0=500, y0=0, x1=0, y1=0, ease="out"), fi=.02, fo=.01))
        if j % 5 == 0:
            p.parts.append(_life(t, 99, _g("slide", t, .3, _coin_shape(560 + 40 * (j // 5), 430, 20, "$"), style="", x0=0, y0=-220, x1=0, y1=0, ease="out"), fi=.02, fo=.01))
    p.parts.append(_life(t0, 99, _cnt(640, 330, 0, 250, t0, gap * 25, size=56, color=TEAL), fi=.05, fo=.01))
    t1 = _fr(seg, 1, .1)
    p.parts.append(_g("pop", t1, .3, f'<rect x="500" y="510" width="130" height="110" rx="16" fill="#fff" stroke="{INK}" stroke-width="6"/>' + _t(565, 540, "SHARES", 20, GREY, serif=False)))
    p.parts.append(_life(t1, 99, _cnt(565, 600, 100, 125, t1, .8, size=46, pre=""), fi=.05, fo=.01))
    t1b = _fr(seg, 1, .55)
    p.parts.append(_g("pop", t1b, .3, f'<rect x="645" y="510" width="135" height="110" rx="16" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>' + _t(712, 540, "YOUR 10", 20, INK, serif=False)))
    p.parts.append(_life(t1b, 99, _cnt(712, 604, 10, 8, t1b + .1, .7, size=52, pre="", suf="%", color=RED), fi=.05, fo=.01))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 320, 1.03), (t0 + .3, 300, 420, 1.06), (t1, 400, 480, 1.06), (t1b + .4, 560, 420, 1.06), (end, 400, 320, 1.0)])


def ns_answer(p, seg=None, **_):
    """The answer, three rows at full height. From the swipe a dot rides along the top row. On the first sentence
    $1,000 + $250 = $1,250 lights tile by tile, then $1,250 / 125 = $10 below it; on the second your ten share tiles
    each get a $10 tag, count to $100 and SAME STILL $100 stamps."""
    a, b = _span(seg)
    row = lambda y, labs, w=230: "".join(f'<rect x="{20 + j * 260}" y="{y}" width="{w}" height="120" rx="16" fill="#fff" stroke="{INK}" stroke-width="6"/>' for j in range(len(labs)))
    _set(p, row(30, "abc") + row(190, "abc") + _t(255, 105, "+", 50, RED) + _t(515, 105, "=", 50, RED) + _t(255, 265, "/", 50, RED) + _t(515, 265, "=", 50, RED)
         + "".join(_share(40 + 52 * c, 380, 46, GOLD) for c in range(10)) + _t(300, 462, "YOUR 10 SHARES", 26, INK, serif=False))
    _loop(p, a, b, 1.8, f'<circle cx="40" cy="160" r="10" fill="{RED}"/>', x1=720)
    t0 = _fr(seg, 0, .1)
    for j, lab in enumerate(("$1,000", "$250", "$1,250")):
        p.parts.append(_life(t0 + .35 * j, 99, _g("pop", t0 + .35 * j, .3, _t(135 + 260 * j, 110, lab, 50, TEAL if j == 2 else INK)), fi=.02, fo=.01))
    t0b = _fr(seg, 0, .6)
    for j, lab in enumerate(("$1,250", "125", "$10")):
        p.parts.append(_life(t0b + .3 * j, 99, _g("pop", t0b + .3 * j, .3, _t(135 + 260 * j, 270, lab, 50, TEAL if j == 2 else INK)), fi=.02, fo=.01))
    t1 = _fr(seg, 1, .05)
    for c in range(10):
        p.parts.append(_life(t1 + .1 * c, 99, _g("pop", t1 + .1 * c, .2, _t(63 + 52 * c, 412, "$10", 18, INK, serif=False)), fi=.02, fo=.01))
    p.parts.append(_life(t1, 99, _cnt(300, 560, 0, 100, t1, 1.0, size=72), fi=.05, fo=.01))
    p.parts.append(_stamp(560, 490, 220, 100, "SAME", TEAL, _fr(seg, 1, .6), size=56, rot=-6))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 160, 1.06), (t0b, 400, 240, 1.06), (t1, 330, 470, 1.08), (t1 + 1.2, 420, 420, 1.04), (end, 400, 320, 1.0)])


def ns_catch(p, seg=None, **_):
    """The catch. Left, a NEW SHARE price tag swinging from the swipe, $10; right, YOUR 10 SHARES as a $100 column
    (gold) with a riding dot. On the first sentence CHEAP? pops and the tag's $10 is crossed; on the second the tag
    turns to $6, a CASH IN plate counts $150 (not $250), $9.20 A SHARE pops and the top $8 of your column breaks off
    and falls, the count stepping $100 to $92."""
    a, b = _span(seg)
    k, base, xc, w_ = 4.4, 600, 470, 240
    _set(p, _ground(base, 420, 770) + _t(xc + w_ / 2, base + 34, "YOUR 10 SHARES", 24, INK, serif=False)
         + _col(xc, w_, 100, GOLD, k=k, base=base, dash=True, op=.07) + _col(xc, w_, 92, GOLD, k=k, base=base))
    p.parts.append(_life(-1, _fr(seg, 1, .6) + 1, _col(xc, w_, 8, GOLD, k=k, base=base - 92 * k), fi=.01, fo=.01))
    p.parts.append(_life(-1, _fr(seg, 1, .6) + .9, _t(xc + w_ / 2, base - 100 * k - 20, "$100", 52, INK), fi=.01, fo=.05))
    p.parts.append(_idle("swing", _ptag(200, 130, 260, "$10", NEW_C, INK, 70), 8, 2.0, style="transform-box:fill-box;transform-origin:center top"))
    p.parts.append(_idle("bob", _t(200, 260, "NEW SHARE", 28, INK, serif=False), 5, 1.7))
    _loop(p, a, b, 1.6, f'<circle cx="{xc - 26}" cy="{base - 10}" r="11" fill="{INK}"/>', y1=-92 * k + 20)
    t0 = _fr(seg, 0, .4)
    p.parts.append(_g("pop", t0, .35, _idle("bob", _pill(200, 330, "TOO CHEAP?", RED, "#fff", 30), 5, 1.8, style="")))
    t1 = _fr(seg, 1, .05)
    p.parts.append(_g("draw", t1, .3, f'<path d="M110 90 L300 170" stroke="{RED}" stroke-width="12" stroke-linecap="round"/>', style=""))
    p.parts.append(_g("pop", t1 + .3, .35, _ptag(200, 130, 200, "$6", RED, "#fff", 70, rot=-8)))
    p.parts.append(_g("pop", t1 + .4, .3, f'<rect x="50" y="400" width="300" height="200" rx="16" fill="#fff" stroke="{INK}" stroke-width="6"/>' + _t(200, 440, "25 x $6", 30, GREY, serif=False)))
    p.parts.append(_life(t1 + .4, 99, _cnt(200, 510, 0, 150, t1 + .45, .7, size=60, color=TEAL), fi=.05, fo=.01))
    p.parts.append(_life(t1 + .6, 99, _t(200, 570, "NOT $250", 30, RED, serif=False), fi=.2, fo=.01))
    t1b = _fr(seg, 1, .6)
    p.parts.append(_life(t1b, 99, _g("slide", t1b, .7, _col(xc, w_, 8, RED, k=k, base=base - 92 * k), style="", x0=0, y0=0, x1=120, y1=420, ease="in"), fi=.01, fo=.3))
    p.parts.append(_life(t1b + .5, 99, _t(xc + w_ / 2, base - 92 * k - 20, "$92", 56, RED), fi=.05, fo=.01))
    p.parts.append(_g("pop", t1b + .2, .35, _pill(xc + w_ / 2, 120, "$9.20 A SHARE", RED, "#fff", 28)))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 300, 300, 1.05), (t0, 220, 260, 1.08), (t1 + .4, 260, 400, 1.06), (t1b, 560, 300, 1.06), (end, 400, 320, 1.0)])


def ns_rule(p, seg=None, **_):
    """The rule at full panel height. Top: the small pie with its 10% slice and the bigger pie with its 8% slice, the
    small slice lifting off and sliding onto the big one, again and again, = $100 between them. Bottom, from the
    second sentence: two result rows, SOLD AT $10: YOURS $100 (teal) and SOLD AT $6: YOURS $92 (red), lighting in
    turn with a frame running between them."""
    a, b = _span(seg)
    _set(p, _pie(170, 235, 125, .10) + _pie(610, 235, 140, .08, new=.2) + _t(170, 400, "10% OF $1,000", 28, INK, serif=False)
         + _t(610, 405, "8% OF $1,250", 28, INK, serif=False)
         + f'<rect x="30" y="430" width="740" height="80" rx="14" fill="#fff" stroke="{INK}" stroke-width="5"/>'
         + f'<rect x="30" y="530" width="740" height="80" rx="14" fill="#fff" stroke="{INK}" stroke-width="5"/>'
         + _t(400, 484, "SOLD AT $10: YOURS STAY $100", 36, INK, serif=False) + _t(400, 584, "SOLD AT $6: YOURS FALL TO $92", 36, INK, serif=False))
    _loop(p, a, b, 2.0, _wedge(170, 235, 125, 0, 36, GOLD), x1=440, y1=0, ease="inout")
    t0 = _fr(seg, 0, .5)
    p.parts.append(_g("pop", t0, .35, _idle("bob", _pill(390, 50, "BOTH ARE $100", TEAL, "#fff", 30), 5, 1.8, style="")))
    t1 = _fr(seg, 1, .1)
    for r in range(int((b - t1) / 1.2) + 1):
        y_ = 430 if r % 2 == 0 else 530
        col = TEAL if r % 2 == 0 else RED
        p.parts.append(_g("press", t1 + 1.2 * r, .5, f'<rect x="30" y="{y_}" width="740" height="80" rx="14" fill="{col}" fill-opacity=".25" stroke="{col}" stroke-width="8"/>'))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 220, 1.06), (t0, 400, 240, 1.04), (t1, 400, 500, 1.08), (t1 + 1.5, 400, 450, 1.04), (end, 400, 320, 1.0)])


def ns_asks(p, **_):
    """The close: the 100-share grid with your gold row; 25 new tiles tagged $14 keep sliding in and fading, a $14
    tag swings, and YOUR 10: ? bobs. No answer shown."""
    s, g = 38, 5
    x0, y0 = 30, 40
    old = "".join(_share(x0 + c * (s + g), y0 + r * (s + g), s, GOLD if r == 0 else BUS_C) for r in range(10) for c in range(10))
    _set(p, old)
    for r in range(8):
        t = p.at(0) + 2.0 * r
        new = "".join(_share(x0 + (j % 10) * (s + g), y0 + (10 + j // 10) * (s + g), s, NEW_C) for j in range(25))
        p.parts.append(_life(t, 2.0, _g("slide", t, .6, new, style="", x0=500, y0=0, x1=0, y1=0, ease="out"), fi=.05, fo=.3))
    p.parts.append(_idle("swing", _ptag(640, 130, 240, "NEW: $14", NEW_C, INK, 44), 8, 2.0, style="transform-box:fill-box;transform-origin:center top"))
    p.parts.append(_idle("bob", f'<rect x="510" y="330" width="260" height="200" rx="18" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>'
                         + _t(640, 380, "YOUR 10", 30, INK, serif=False) + _t(640, 490, "?", 96, RED), 6, 1.9))
    for j in range(8):
        p.parts.append(_g("ripple", p.at(.1) + .9 * j, .8, f'<circle cx="640" cy="460" r="60" fill="none" stroke="{RED}" stroke-width="5"/>'))


SCENES.update({f.__name__: f for f in (ns_hook, ns_setup, ns_new, ns_answer, ns_catch, ns_rule, ns_asks)})


# ---------------------------------------------------------------------------------------------------------------
# Reel C: percentage points against percent. A rate from 2% to 3%: up 3 - 2 = 1 percentage point (100 basis
# points), and up (3 - 2) / 2 = 50%. On $1,000: interest $20 to $30, +$10, half as much again. Close (not shown):
# a margin from 10% to 12%: 200 basis points, a 20% rise.

PP_X0, PP_DX = 80, 128            # the 0% to 5% ruler: x of 0% and px per point


def _ruler(y, x0=PP_X0, dx=PP_DX, n=5, lab=True):
    s = f'<path d="M{x0} {y} H{x0 + n * dx}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    for j in range(n + 1):
        s += f'<path d="M{x0 + j * dx} {y - 18} V{y + 18}" stroke="{INK}" stroke-width="5"/>'
        if lab:
            s += _t(x0 + j * dx, y + 58, f"{j}%", 34, INK, serif=False)
    for j in range(n * 4):
        if j % 4:
            s += f'<path d="M{x0 + j * dx / 4:.0f} {y - 9} V{y + 9}" stroke="{GREY}" stroke-width="3"/>'
    return s


def _marker(x, y, col=RED, lab=None):
    s = f'<path d="M{x} {y - 22} L{x - 22} {y - 62} H{x + 22} Z" fill="{col}" stroke="{INK}" stroke-width="4"/>'
    if lab:
        s += _t(x, y - 76, lab, 34, col)
    return s


def pp_hook(p, seg=None, **_):
    """The hook. From frame 0 a 0% to 5% ruler with a marker sliding from 2% to 3% and back for ever (a grey ghost
    marker left at 2%), and two answer cards below, +1% (teal) and +50% (gold), with OR between them. On the first
    sentence 2% and 3% pills pop on the ruler; on the question the cards press in turn and a ? swings over them."""
    a, b = _span(seg)
    y = 220
    _set(p, _ruler(y) + _marker(PP_X0 + 2 * PP_DX, y, GREY)
         + f'<rect x="40" y="380" width="320" height="200" rx="22" fill="{CASH_C}" stroke="{INK}" stroke-width="7"/>' + _t(200, 515, "+1%", 100, INK)
         + f'<rect x="440" y="380" width="320" height="200" rx="22" fill="{GOLD}" stroke="{INK}" stroke-width="7"/>' + _t(600, 515, "+50%", 100, INK)
         + _t(400, 500, "OR", 40, "#fff", serif=False))
    _loop(p, a, b, 1.6, _marker(PP_X0 + 2 * PP_DX, y), x1=PP_DX, ease="inout")
    t0 = _fr(seg, 0, .1)
    p.parts.append(_g("pop", t0, .3, _pill(PP_X0 + 2 * PP_DX, 80, "2%", INK, "#fff", 40)))
    p.parts.append(_g("pop", _fr(seg, 0, .6), .3, _pill(PP_X0 + 3 * PP_DX, 80, "3%", RED, "#fff", 40)))
    t1 = _fr(seg, 1, .1)
    for r in range(int((b - t1) / .8) + 1):
        x_ = 40 if r % 2 == 0 else 440
        p.parts.append(_g("press", t1 + .8 * r, .5, f'<rect x="{x_}" y="380" width="320" height="200" rx="22" fill="none" stroke="{RED}" stroke-width="10"/>'))
    p.parts.append(_g("pop", t1 + .2, .4, _idle("swing", _ptag(400, 330, 110, "?", RED, "#fff", 60), 10, 2.0, style="transform-box:fill-box;transform-origin:center top")))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 300, 1.0), (t0, 400, 180, 1.08), (t1, 400, 460, 1.06), (t1 + 1.2, 400, 380, 1.03), (end, 400, 320, 1.0)])


def _notes(x, y, n=10, w_=230, h_=26):
    return "".join(f'<rect x="{x}" y="{y - (j + 1) * (h_ + 4)}" width="{w_}" height="{h_}" rx="6" fill="#9ED3A8" stroke="{INK}" stroke-width="3"/>'
                   + _t(x + w_ / 2, y - (j + 1) * (h_ + 4) + 20, "$100", 18, INK, serif=False) for j in range(n))


def pp_setup(p, seg=None, **_):
    """The set-up. A stack of ten $100 notes on the left (dashed until it builds) and an INTEREST jar on the right,
    a 2% A YEAR tag swinging from the swipe and a coin already dropping. On the first sentence the notes stack up
    with the count to $1,000; on the second two $10 coins drop into the jar and its count reads $20."""
    a, b = _span(seg)
    base = 580
    jar = (f'<path d="M460 300 V540 Q460 580 500 580 H680 Q720 580 720 540 V300" fill="#EAF6F3" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="446" y="276" width="288" height="30" rx="10" fill="{INK}"/>' + _t(590, 625, "INTEREST", 28, INK, serif=False))
    _set(p, f'<rect x="60" y="{base - 300}" width="230" height="300" rx="8" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="10 8"/>' + jar
         + _t(175, base + 45, "YOU BORROW", 28, INK, serif=False))
    p.parts.append(_idle("swing", _pill(590, 120, "2% A YEAR", INK, "#fff", 40), 5, 2.0, style="transform-box:fill-box;transform-origin:center top"))
    _loop(p, a, _fr(seg, 1, .2), .9, _coin_shape(590, 330, 24, "$"), y0=-80, y1=60, ease="in", fo=.2)
    t0 = _fr(seg, 0, .15)
    gap = max(.08, (seg[0][1] - t0) * .7 / 10)
    for j in range(10):
        p.parts.append(_life(t0 + gap * j, 99, _g("slide", t0 + gap * j, .25, _notes(60, base - j * 30, 1), style="", x0=0, y0=-200, x1=0, y1=0, ease="out"), fi=.02, fo=.01))
    p.parts.append(_life(t0, 99, _cnt(175, base - 330, 0, 1000, t0, gap * 10, size=56), fi=.05, fo=.01))
    t1 = _fr(seg, 1, .2)
    for j in range(2):
        p.parts.append(_life(t1 + .4 * j, 99, _g("slide", t1 + .4 * j, .35, _coin_shape(540 + 100 * j, 530, 42, "$10"), style="", x0=0, y0=-260, x1=0, y1=0, ease="out"), fi=.02, fo=.01))
    p.parts.append(_life(t1 + .5, 99, _cnt(590, 420, 0, 20, t1 + .5, .5, size=64, color=RED), fi=.05, fo=.01))
    for j in range(3):
        p.parts.append(_g("ripple", t1 + 1.0 + .5 * j, .5, f'<circle cx="590" cy="500" r="70" fill="none" stroke="{RED}" stroke-width="5"/>'))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 320, 1.03), (t0 + .3, 220, 380, 1.08), (t1, 590, 420, 1.08), (t1 + 1.2, 500, 380, 1.04), (end, 400, 320, 1.0)])


def pp_rise(p, seg=None, **_):
    """The rise. Left, a RATE thermometer 0% to 5% (a bubble bobbing from the swipe) at 2%; right, the INTEREST
    column, $20 in gold. On the first sentence the thermometer rises to 3% and a red $10 slab drops onto the column,
    the count stepping $20 to $30; on the second a bracket marks the $10 against the $20 below (HALF OF $20) and
    +50% stamps."""
    a, b = _span(seg)
    k, base, xc, w_ = 9.0, 590, 430, 240
    tb_x, tb_y0, tb_y1 = 120, 560, 120                         # thermometer: 0% at y0, 5% at y1
    ty = lambda v: tb_y0 - (tb_y0 - tb_y1) * v / 5
    _set(p, f'<rect x="{tb_x}" y="{tb_y1 - 20}" width="80" height="{tb_y0 - tb_y1 + 40}" rx="40" fill="#fff" stroke="{INK}" stroke-width="6"/>'
         + "".join(f'<path d="M{tb_x + 80} {ty(j):.0f} h24" stroke="{INK}" stroke-width="4"/>' + _t(tb_x + 150, ty(j) + 12, f"{j}%", 30, INK, serif=False) for j in range(6))
         + f'<rect x="{tb_x + 18}" y="{ty(2):.0f}" width="44" height="{tb_y0 - ty(2):.0f}" rx="16" fill="{RED}"/>'
         + _ground(base, 400, 770) + _col(xc, w_, 30, GOLD, k=k, base=base, dash=True, op=.07) + _col(xc, w_, 20, GOLD, k=k, base=base)
         + _t(xc + w_ / 2, base + 36, "INTEREST", 26, INK, serif=False) + _t(xc + w_ / 2, base - 10 * k + 14, "$20", 44, INK))
    p.parts.append(_idle("bob", f'<circle cx="{tb_x + 40}" cy="{tb_y0 + 10}" r="46" fill="{RED}" stroke="{INK}" stroke-width="6"/>', 4, 1.3))
    _loop(p, a, b, 1.4, f'<circle cx="{tb_x + 40}" cy="{tb_y0 - 20}" r="8" fill="#fff"/>', y1=-(tb_y0 - ty(2)) + 40, ease="in")
    t0 = _fr(seg, 0, .2)
    p.parts.append(_life(t0, 99, _g("growY", t0, .6, f'<rect x="{tb_x + 18}" y="{ty(3):.0f}" width="44" height="{ty(2) - ty(3) + 4:.0f}" rx="10" fill="{RED}"/>', style="transform-box:fill-box;transform-origin:center bottom"), fi=.01, fo=.01))
    p.parts.append(_g("pop", t0 + .5, .3, _pill(tb_x + 40, ty(3) - 70, "3%", RED, "#fff", 40)))
    t0b = _fr(seg, 0, .6)
    p.parts.append(_life(t0b, 99, _g("slide", t0b, .4, _col(xc, w_, 10, RED, k=k, base=base - 20 * k) + _t(xc + w_ / 2, base - 25 * k + 14, "+$10", 44, "#fff"), style="", x0=0, y0=-300, x1=0, y1=0, ease="out"), fi=.02, fo=.01))
    p.parts.append(_life(t0b + .3, 99, _cnt(xc + w_ / 2, base - 30 * k - 24, 20, 30, t0b + .3, .5, size=56), fi=.05, fo=.01))
    t1 = _fr(seg, 1, .05)
    p.parts.append(_g("draw", t1, .4, f'<path d="M{xc - 16} {base - 20 * k:.0f} h-18 V{base - 30 * k:.0f} h18" stroke="{RED}" stroke-width="7" fill="none"/>', style=""))
    p.parts.append(_g("draw", t1 + .3, .4, f'<path d="M{xc - 16} {base:.0f} h-30 V{base - 20 * k:.0f} h30" stroke="{INK}" stroke-width="6" fill="none"/>', style=""))
    p.parts.append(_g("pop", t1 + .5, .35, _idle("bob", _pill(xc + w_ / 2, 140, "HALF OF $20", INK, "#fff", 30), 5, 1.8, style="")))
    p.parts.append(_stamp(xc + 10, 20, 220, 80, "+50%", TEAL, _fr(seg, 1, .6), size=52, rot=-6))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 320, 1.03), (t0, 250, 300, 1.08), (t0b, 560, 380, 1.06), (t1 + .4, 520, 260, 1.06), (end, 400, 320, 1.0)])


def pp_answer(p, seg=None, **_):
    """The answer, two rows at full height. POINTS: the ruler with a marker riding 2% to 3% from the swipe and a
    bracket 1 POINT over the step; PERCENT: two gold blocks (the 2%) and one red block (the extra 1%) beside them,
    1 / 2 = 50%. On the first sentence both rows light, 1 POINT then 50%; on the second the two sums draw in tiles,
    3 - 2 = 1 and 1 / 2 = 50%."""
    a, b = _span(seg)
    y = 200
    blocks = "".join(f'<rect x="{90 + 130 * j}" y="380" width="110" height="110" rx="12" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>' + _t(145 + 130 * j, 450, "1%", 34, INK) for j in range(2))
    _set(p, _ruler(y) + _t(30, 40, "POINTS", 30, INK, serif=False, anchor="start") + _t(30, 350, "PERCENT", 30, INK, serif=False, anchor="start") + blocks
         + f'<rect x="370" y="380" width="110" height="110" rx="12" fill="{RED}" fill-opacity=".12" stroke="{GREY}" stroke-width="4" stroke-dasharray="10 8"/>')
    _loop(p, a, b, 1.6, _marker(PP_X0 + 2 * PP_DX, y), x1=PP_DX)
    t0 = _fr(seg, 0, .2)
    x2, x3 = PP_X0 + 2 * PP_DX, PP_X0 + 3 * PP_DX
    p.parts.append(_g("draw", t0, .4, f'<path d="M{x2} {y - 80} v-18 H{x3} v18" stroke="{TEAL}" stroke-width="8" fill="none"/>', style=""))
    p.parts.append(_g("pop", t0 + .3, .35, _pill((x2 + x3) / 2, y - 130, "1 POINT", TEAL, "#fff", 34)))
    t0b = _fr(seg, 0, .65)
    p.parts.append(_life(t0b, 99, _g("slide", t0b, .4, f'<rect x="370" y="380" width="110" height="110" rx="12" fill="{RED}" stroke="{INK}" stroke-width="5"/>' + _t(425, 450, "+1%", 34, "#fff"), style="", x0=0, y0=-200, x1=0, y1=0, ease="out"), fi=.02, fo=.01))
    p.parts.append(_g("draw", t0b + .4, .4, f'<path d="M90 510 v18 H350 v-18" stroke="{INK}" stroke-width="6" fill="none"/>', style=""))
    p.parts.append(_g("pop", t0b + .6, .35, _idle("bob", _pill(620, 435, "HALF: 50%", GOLD, INK, 34), 5, 1.7, style="")))
    t1 = _fr(seg, 1, .05)
    for j, (x_, lab) in enumerate(((40, "3 - 2 = 1 POINT"), (420, "1 / 2 = 50%"))):
        p.parts.append(_g("pop", t1 + .6 * j, .35, f'<rect x="{x_}" y="560" width="340" height="76" rx="14" fill="#fff" stroke="{INK}" stroke-width="5"/>' + _t(x_ + 170, 612, lab, 36, INK, serif=False)))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 300, 1.03), (t0, 400, 160, 1.08), (t0b, 400, 430, 1.08), (t1, 400, 560, 1.06), (end, 400, 320, 1.0)])


def pp_bps(p, seg=None, **_):
    """Basis points. Top: the ruler with the 2% to 3% step boxed and a magnifier bobbing over it from the swipe;
    below, the step blown up: 100 small ticks in a row of ten groups. On the first sentence POINTS and BASIS POINTS
    pills pop; on the second the hundred ticks light group by group with a count to 100 BPS and 1 POINT = 100 BPS
    stamps."""
    a, b = _span(seg)
    y = 120
    x2, x3 = PP_X0 + 2 * PP_DX, PP_X0 + 3 * PP_DX
    gx0, gx1, gy = 40, 760, 360
    ticks = "".join(f'<path d="M{gx0 + (gx1 - gx0) * j / 100:.1f} {gy - (40 if j % 10 == 0 else 20)} V{gy + (40 if j % 10 == 0 else 20)}" stroke="{GREY}" stroke-width="{4 if j % 10 == 0 else 2}"/>' for j in range(101))
    _set(p, _ruler(y) + f'<rect x="{x2 - 6}" y="{y - 34}" width="{x3 - x2 + 12}" height="68" rx="10" fill="none" stroke="{RED}" stroke-width="5"/>'
         + f'<path d="M{x2} {y + 40} L{gx0} {gy - 60} M{x3} {y + 40} L{gx1} {gy - 60}" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 8"/>'
         + f'<path d="M{gx0} {gy} H{gx1}" stroke="{INK}" stroke-width="5"/>' + ticks
         + _t(gx0, gy + 80, "2%", 32, INK, serif=False) + _t(gx1, gy + 80, "3%", 32, INK, serif=False))
    p.parts.append(_idle("bob", f'<circle cx="{(x2 + x3) / 2}" cy="{y}" r="58" fill="none" stroke="{INK}" stroke-width="7"/><path d="M{(x2 + x3) / 2 + 42} {y + 42} l40 40" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>', 8, 1.5))
    _loop(p, a, b, 2.0, f'<circle cx="{gx0}" cy="{gy}" r="10" fill="{RED}"/>', x1=gx1 - gx0)
    t0 = _fr(seg, 0, .15)
    p.parts.append(_g("pop", t0, .3, _pill(230, 250, "POINTS", TEAL, "#fff", 32)))
    p.parts.append(_g("pop", _fr(seg, 0, .55), .3, _pill(560, 250, "BASIS POINTS", GOLD, INK, 32)))
    t1 = _fr(seg, 1, .05)
    gap = max(.08, (seg[1][1] - t1) * .8 / 10)
    for g in range(10):
        xa = gx0 + (gx1 - gx0) * g / 10
        p.parts.append(_life(t1 + gap * g, 99, _g("pop", t1 + gap * g, .2, f'<rect x="{xa + 2:.0f}" y="{gy - 26}" width="{(gx1 - gx0) / 10 - 4:.0f}" height="52" rx="6" fill="{GOLD}" fill-opacity=".7" stroke="{INK}" stroke-width="3"/>'), fi=.02, fo=.01))
    p.parts.append(_life(t1, 99, _cnt(400, 480, 0, 100, t1, gap * 10, size=60, pre="", suf=" BPS", color=RED), fi=.05, fo=.01))
    p.parts.append(_stamp(170, 530, 460, 80, "1 POINT = 100 BPS", RED, t1 + gap * 10 + .1, size=40, rot=-4))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 260, 1.04), (t0, 400, 400, 1.06), (t1, 300, 360, 1.08), (t1 + gap * 8, 520, 330, 1.06), (end, 400, 320, 1.0)])


def pp_rule(p, seg=None, **_):
    """The rule at full panel height: two rows of big tiles, 3% - 2% = 1 POINT and (3 - 2) / 2 = 50%, with SUBTRACT
    and DIVIDE pills at their left; from the swipe a frame travels along the top row. On the first sentence the top
    row lights tile by tile; on the second the frame moves to the bottom row and its tiles light in turn, the = signs
    pulsing."""
    a, b = _span(seg)
    tw, th = 220, 150
    xs = (20, 290, 560)
    _set(p, "".join(f'<rect x="{x}" y="110" width="{tw}" height="{th}" rx="18" fill="#fff" stroke="{INK}" stroke-width="6"/>' for x in (xs[0], xs[2]))
         + "".join(f'<rect x="{x}" y="400" width="{tw}" height="{th}" rx="18" fill="#fff" stroke="{INK}" stroke-width="6"/>' for x in (xs[0], xs[2]))
         + _t(xs[0] + tw / 2, 205, "3% - 2%", 48, INK) + _t(xs[2] + tw / 2, 205, "1 POINT", 46, TEAL)
         + _t(xs[0] + tw / 2, 495, "1 / 2", 52, INK) + _t(xs[2] + tw / 2, 495, "50%", 64, RED)
         + _t(xs[1] + tw / 2, 205, "=", 70, RED) + _t(xs[1] + tw / 2, 495, "=", 70, RED)
         + _pill(150, 60, "SUBTRACT", TEAL, "#fff", 32) + _pill(190, 345, "DIVIDE BY THE START", RED, "#fff", 28)
         + _t(xs[0] + tw / 2, 590, "(3 - 2) / 2", 34, INK, serif=False))
    t1 = _fr(seg, 1, 0)
    for r in range(int((b - a) / .5) + 1):
        t = a + .5 * r
        yy = 110 if t < t1 else 400
        x = xs[0] if r % 2 == 0 else xs[2]
        p.parts.append(_g("press", t, .45, f'<rect x="{x - 6}" y="{yy - 6}" width="{tw + 12}" height="{th + 12}" rx="22" fill="none" stroke="{RED if yy == 400 else TEAL}" stroke-width="7"/>'))
    t0 = _fr(seg, 0, .2)
    for j, x in enumerate(xs):
        p.parts.append(_g("press", t0 + .4 * j, .4, f'<rect x="{x}" y="110" width="{tw}" height="{th}" rx="18" fill="{CASH_C}" fill-opacity=".5" stroke="{INK}" stroke-width="6"/>'))
    for j, x in enumerate(xs):
        p.parts.append(_g("press", _fr(seg, 1, .15) + .4 * j, .4, f'<rect x="{x}" y="400" width="{tw}" height="{th}" rx="18" fill="{GOLD}" fill-opacity=".5" stroke="{INK}" stroke-width="6"/>'))
    end = seg[-1][1] + .4
    _cam(p, [(seg[0][0] - .4, 400, 200, 1.06), (t0 + 1.0, 400, 220, 1.04), (t1, 400, 440, 1.06), (t1 + 1.4, 400, 420, 1.04), (end, 400, 320, 1.0)])


def pp_asks(p, **_):
    """The close: a MARGIN ruler from 0% to 15% with a marker sliding 10% to 12% and back for ever, and two cards,
    ? BPS and ? % RISE, pressing in turn. No answer shown."""
    y, x0, dx = 220, 70, 44
    s = f'<path d="M{x0} {y} H{x0 + 15 * dx}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    for j in range(16):
        s += f'<path d="M{x0 + j * dx} {y - (18 if j % 5 == 0 else 10)} V{y + (18 if j % 5 == 0 else 10)}" stroke="{INK}" stroke-width="{5 if j % 5 == 0 else 3}"/>'
        if j % 5 == 0 or j == 12:
            s += _t(x0 + j * dx, y + 58, f"{j}%", 32, INK, serif=False)
    _set(p, s + _t(400, 90, "MARGIN", 34, INK, serif=False) + _marker(x0 + 10 * dx, y, GREY)
         + f'<rect x="40" y="380" width="320" height="200" rx="22" fill="#fff" stroke="{INK}" stroke-width="7"/>' + _t(200, 450, "BASIS POINTS", 30, INK, serif=False) + _t(200, 545, "?", 90, RED)
         + f'<rect x="440" y="380" width="320" height="200" rx="22" fill="#fff" stroke="{INK}" stroke-width="7"/>' + _t(600, 450, "% RISE", 30, INK, serif=False) + _t(600, 545, "?", 90, RED))
    for r in range(12):
        t = p.at(0) + 1.6 * r
        p.parts.append(_life(t, 1.6, _g("slide", t, 1.45, _marker(x0 + 10 * dx, y), style="", x0=0, y0=0, x1=2 * dx, y1=0, ease="inout"), fi=.02, fo=.05))
        p.parts.append(_g("press", t, .6, f'<rect x="{40 if r % 2 == 0 else 440}" y="380" width="320" height="200" rx="22" fill="none" stroke="{RED}" stroke-width="10"/>'))


SCENES.update({f.__name__: f for f in (pp_hook, pp_setup, pp_rise, pp_answer, pp_bps, pp_rule, pp_asks)})
