"""
Filmed beats for YouTube #14, Silicon Valley Bank, March 2023 (20 Nov 2026). Sets, props and shots for build/cine.py,
used by build/youtube_ep014.py as kind="cine" beats.

cinematic-standard.md section 8, step 3 (sets): the "bank office today" the build order named next, and a bank branch
front of today. Step 4 (data in the world): a wall screen whose bars are drawn to a true dollar scale as they are
said (book value against market value, then equity beside the gap), a desk monitor where a rate and a bond price
count against each other, a billboard that counts the outflow.

Sets (our own generic drawings: no real bank's name, logo, building, branch or person; everything is badged):
  bank_office_today(screen, desk_screen, desk_prop)  an open-plan bank office of today: a tall window on the city, a
                     wide wall screen that takes content (1000 x 500), a glass meeting room, a back row of desks with
                     live monitors, a front desk (top y 880, z .86) with a monitor that takes content and a paper on it
  branch_front_today(notice)  a bank branch at street level today: a stone and glass front, a blank fascia that says
                     only BANK, glass doors at x 960 with a notice slot, a cash machine, planters, towers behind
Props: bond_paper() (our example bond, $100, 10 years, 1.5%), wall_bars() (bars on a true scale that grow on cue),
rows_screen() (rows that type in and count on cue).

Shots (fn(w, h, dur, ctx) -> dict(shots, foley, amb)):
  hook_40bn     frame 0: a phone fills the frame, OVER $40BN counts from $0 by 1.4 s, IN ONE DAY lands; on the
                question the phone lowers and the camera pulls back on a branch front of today, people walking on phones
  book_gap      the bank office: the wall screen draws $91.3bn on the books, $76.2bn at market prices, the $15.2bn gap,
                then $16.0bn of equity beside it; an analyst walks to the screen and stops
  bond_1/bond_2 the puzzle, two beats (part 2 opens on part 1's end state): our example bond on the desk; the monitor's
                new-bond rate counts 1.5% to 4.0%, then the old bond's price counts $100 to $79.72
  march8        8 March 2023 at a kitchen table at night: the laptop types the announcement (sold $21bn, loss $1.8bn
                after tax, seeking $2.25bn)
  run_street    9 March: a street by day, people on their phones; the billboard counts OUT ON MARCH 9: OVER $40BN and
                EXPECTED MARCH 10: OVER $100BN on the words
  closed        10 March (reconstruction): a woman walks to the branch door, tries it, reads the notice, steps back
  growth        2019 to 2021 in the office: the wall screen draws assets $71bn to over $211bn, TRIPLED; people arrive
Facts on screen come only from the sources in youtube_ep014.py's docstring. Nobody speaks; nobody is a likeness.
"""

import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402
from cine_1907 import lay, badge, seg_t, word_t   # noqa: E402
from cine_1920 import title                       # noqa: E402
from cine_1971 import kt, board_rows_svg           # noqa: E402
from cine_2021 import (hand_phone, street_today, kitchen_2021, laptop, mini_phone, _tower, _fold, _ktf,   # noqa: E402,F401
                       STREET_LOOKS, SCREEN)

INK, RED, TEAL, MUSTARD, PAPER = C.INK, C.RED, C.TEAL, C.MUSTARD, "#F7F5F2"
_r, _t = L._r, L._t
LIGHT, DIM = "#F4F1EA", "#8FA3A8"

C.LOOKS.update({
    # 20 Nov, YouTube #14 (2023): office clothes of today, generic; nobody's likeness.
    "office_2023": dict(coat="#2F3E55", coat2="#243045", vest="#EEF1F4", legs="#2B3140", stock="#2B3140", shoe=INK, skin="#E8BC9A",
                        hair="#3A2A20", hat="", style="suit", cuff="#EEF1F4", tie="#EEF1F4", era="1971"),
    "office_2023b": dict(coat="#8A4B3A", coat2="#6E3B2E", vest="#F4EFE4", legs="#2F2F34", stock="#2F2F34", shoe=INK, skin="#9A6444",
                         hair="#14100D", hat="", style="suit", cuff="#8A4B3A", tie="#F4EFE4", era="1971"),
    "office_2023c": dict(coat="#5A6A5A", coat2="#465446", vest="#E9EEF2", legs="#33383F", stock="#33383F", shoe=INK, skin="#F1CBAA",
                         hair="#8A6A4A", hat="", style="suit", cuff="#E9EEF2", tie="#E9EEF2", era="1971"),
})


# ------------------------------------------------------------------------------------------------ props

def bond_paper(w=420, h=270, t_in=0.0):
    """Our example bond on a desk (not a real security): $100, 10 years, 1.5% a year."""
    s = (_r(0, 0, w, h, "#F4EFE2", rx=6, sw=3) + f'<rect x="12" y="12" width="{w - 24}" height="{h - 24}" fill="none" stroke="{TEAL}" stroke-width="2.4" '
         f'stroke-dasharray="7 4"/>' + _t(w / 2, 58, "BOND", 40, fill=INK, family="Serif", weight=700, extra='letter-spacing="6"')
         + _t(w / 2, 86, "OUR EXAMPLE", 16, fill="#7A7F86", family="Sans", weight=700, extra='letter-spacing="3"')
         + _t(w / 2, 150, "$100", 62, fill=RED, family="Serif", weight=700)
         + _t(w / 2, 196, "PAYS 1.5% A YEAR", 24, fill=INK, family="Sans", weight=700)
         + _t(w / 2, 230, "BACK IN FULL IN 10 YEARS", 20, fill="#4A4F55", family="Sans", weight=700, extra='letter-spacing="1"'))
    return kt(s, None, t_in, .4) if t_in > 0 else s


def wall_bars(x0, y0, bars, scale, bar_h=64, gap=40, size=26):
    """Horizontal bars on a true scale (scale px per unit) that grow on cue. bars: (label, value, colour, t, text)."""
    s = ""
    for k, (lab, v, col, t, txt) in enumerate(bars):
        y = y0 + k * (bar_h + gap)
        wpx = v * scale
        s += _ktf(_t(x0, y - 10, lab, size - 6, fill=DIM, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"'), t, .3)
        s += (f'<rect x="{x0}" y="{y}" width="{wpx:.0f}" height="{bar_h}" fill="{col}" '
              f'{C.kv(width=[[0, 0], [t - .01, 0], [t + .9, round(wpx), "out"]]) if t > 0 else ""}/>')
        s += _ktf(_t(x0 + wpx + 16, y + bar_h * .72, txt, size + 6, fill=LIGHT, anchor="start", family="Sans", weight=700), t + .7, .3)
    return s


def rows_screen(rows, x0=40, y0=150, step=78, wid=820, size=28):
    """Rows that type in at their times: (label, value text or None, colour, t, count keys or None, (dec, pre, suf))."""
    s = ""
    for k, (lab, val, col, t, keys, fmt) in enumerate(rows):
        y = y0 + step * k
        row = _t(x0, y, lab, size, fill="#C9D4D6", anchor="start", family="Sans", weight=600)
        if keys:
            dec, pre, suf = fmt
            row += (f'<text x="{x0 + wid}" y="{y}" text-anchor="end" font-family="\'Sans\',sans-serif" font-weight="700" font-size="{size + 12}" '
                    f'fill="{col}" {C.kv(count=keys)} data-dec="{dec}" data-pre="{pre}" data-suf="{suf}">{pre}{keys[0][1]:.{dec}f}{suf}</text>')
        else:
            row += _t(x0 + wid, y, val, size + 12, fill=col, anchor="end", family="Sans", weight=700)
        s += _ktf(row, t, .25)
    return s


# ------------------------------------------------------------------------------------------------ sets

def bank_office_today(screen="", desk_screen="", desk_prop="", seed=51, dusk=False, front_monitor=True):
    """An open-plan bank office of today. Layers (z): wall .4 (window on the city at x -760..420, the wall screen
    1000 x 500 at x 520..1520, y 120..620, a glass meeting room from x 1700), back desks .62 (a row at y 840 with
    live monitors), floor .6, front desk .86 (top y 880 from x 80 to 1100: a monitor 640 x 380 centred at x 560 whose
    screen takes desk_screen, and desk_prop drawn at (700, 880) as its bottom left). People: feet 960 behind the back
    row (z .7), a seat at (1240, 1010) by the front desk (z .82). Returns (layers, anchors)."""
    rng = random.Random(seed)
    wall = C.defs() + '<rect x="-1800" y="-900" width="5600" height="2600" fill="#D9DCDD"/>'
    wall += "".join(_r(-1700 + k * 420, -40, 300, 26, "#F6F7F2", rx=6, sw=0) for k in range(13))          # ceiling light panels
    wx, wy, ww, wh = -760, 90, 1180, 690
    top, bot = ("#2E3550", "#D98A5A") if dusk else ("#AFC6D6", "#E6ECEC")
    wall += (f'<defs><linearGradient id="bo23{seed}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
             f'<stop offset="1" stop-color="{bot}"/></linearGradient></defs>'
             f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="url(#bo23{seed})"/>')
    x = wx
    while x < wx + ww:
        bw, bh = rng.uniform(70, 170), rng.uniform(220, 600)
        bw = min(bw, wx + ww - x)
        wall += _tower(x, bw, wy + wh - bh, wy + wh, rng.choice(["#8E9CAA", "#A3AFBA", "#7F8D9B"]) if not dusk else "#2A3246",
                       .05 if not dusk else .35, rng, cols=2, glass=True)
        x += bw + 6
    for k in range(1, 4):
        wall += f'<path d="M{wx + ww * k / 4:.0f},{wy} L{wx + ww * k / 4:.0f},{wy + wh}" stroke="#5A6068" stroke-width="10"/>'
    wall += f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#5A6068" stroke-width="18"/>'
    # the wall screen
    wall += (f'<g transform="translate(520,120)">' + _r(-18, -18, 1036, 536, "#22262C", rx=10, sw=4)
             + f'<rect width="1000" height="500" rx="4" fill="{SCREEN}"/>{screen}'
             + '<rect width="1000" height="500" fill="#9FE0D2" opacity=".04" data-flick=\'[0.04,0.02,3]\'/></g>')
    # a glass meeting room, right: frames, a table, a plant
    gx = 1700
    wall += (f'<rect x="{gx}" y="60" width="900" height="760" fill="#BFD3DE" opacity=".35"/>'
             + "".join(f'<path d="M{gx + k * 180},60 L{gx + k * 180},820" stroke="#7A8590" stroke-width="8"/>' for k in range(6))
             + f'<path d="M{gx},60 L{gx + 900},60 M{gx},820 L{gx + 900},820" stroke="#7A8590" stroke-width="10"/>'
             + _r(gx + 160, 640, 560, 26, "#6B5A4A", rx=6, sw=3) + _r(gx + 420, 666, 30, 150, "#5A4A3C", sw=2)
             + f'<rect x="{gx + 40}" y="420" width="820" height="12" fill="#F6F7F2" opacity=".5"/>')
    pl = 1560                                                                           # a tall plant between screen and glass
    wall += (_r(pl - 46, 700, 92, 120, "#B9AC9A", rx=8, sw=3)
             + f'<g data-swing=\'[0.8,0.5,3,{pl},700]\'>' + "".join(
                 f'<path d="M{pl},700 C{pl + dx * .4:.0f},{600 - k * 20} {pl + dx:.0f},{560 - k * 26} {pl + dx * 1.2:.0f},{520 - k * 30}" '
                 f'stroke="#3F6B4A" stroke-width="16" fill="none" stroke-linecap="round"/>' for k, dx in enumerate((-90, -40, 20, 70, 110))) + "</g>")
    floor = '<rect x="-1800" y="840" width="5600" height="900" fill="#8C8F92"/>' + "".join(
        f'<path d="M{x},840 L{x - 300},1700" stroke="#7F8285" stroke-width="3"/>' for x in range(-1800, 3800, 240))
    back = ""
    for k, bx in enumerate(range(-600, 1700, 520)):                                    # the back row of desks with live monitors
        back += (_r(bx, 820, 420, 24, "#C9C4BA", rx=4, sw=3) + _r(bx + 20, 844, 380, 110, "#A9A39A", sw=2.4)
                 + _r(bx + 120, 690, 180, 112, "#22262C", rx=6, sw=2.6) + _r(bx + 196, 802, 28, 20, "#22262C", sw=2)
                 + f'<rect x="{bx + 132}" y="702" width="156" height="88" fill="#1B2A30"/>'
                 + "".join(f'<rect x="{bx + 142}" y="{712 + r * 14}" width="{rng.uniform(50, 130):.0f}" height="6" fill="#9FE0D2" '
                           f'opacity=".55" data-flick=\'[0.55,0.25,{(k * 5 + r) % 9}]\'/>' for r in range(5)))
    mon_w, mon_h = 640, 380
    front = (_r(80, 880, 1020, 34, "#E3DED4", rx=4, sw=3.6) + _r(110, 914, 960, 260, "#B8B2A8", sw=3)
             + (f'<g transform="translate({560 - mon_w / 2 - 18},{880 - mon_h - 104})">' + _r(0, 0, mon_w + 36, mon_h + 36, "#22262C", rx=12, sw=3.4)
             + f'<g transform="translate(18,18)"><rect width="{mon_w}" height="{mon_h}" fill="{SCREEN}"/>{desk_screen}'
             + f'<rect width="{mon_w}" height="{mon_h}" fill="#9FE0D2" opacity=".04" data-flick=\'[0.04,0.02,6]\'/></g>'
             + _r(mon_w / 2 - 12, mon_h + 36, 60, 46, "#22262C", sw=2.6) + _r(mon_w / 2 - 92, mon_h + 78, 220, 18, "#22262C", rx=6, sw=2.6) + "</g>" if front_monitor else "")
             + f'<g transform="translate(260,880)">{L.cup()}</g>'
             + (f'<g transform="translate(930,{880 - 6}) rotate(-4) scale(.62)" ><g transform="translate(0,-270)">{desk_prop}</g></g>' if desk_prop else ""))
    layers = dict(wall=(0.4, wall), floor=(0.6, floor), back=(0.62, back), front=(0.86, front))
    return layers, dict(feet=960, seat=(1240, 1010), desk_y=880, wall_screen=(1020, 370), monitor=(560, 880 - mon_h / 2 - 86), paper=(1060, 800))


def branch_front_today(notice="", seed=61, morning=True):
    """A bank branch at street level today (generic: the fascia says only BANK). Layers (z): sky .15, towers .3, the
    branch front .5 (glass doors centred at x 960, y 560..1010; the notice slot 220 x 280 drawn at (850, 640) on the
    left door), pavement .6, furniture .7 (a cash machine at x 1450, planters, a lamp). Feet at 1010.
    Returns (layers, anchors)."""
    rng = random.Random(seed)
    top, bot = ("#C9D6E0", "#F1E6D4") if morning else ("#AFC6D6", "#E6ECEC")
    sky = C.defs() + (f'<defs><linearGradient id="bf23{seed}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
                      f'<stop offset="1" stop-color="{bot}"/></linearGradient></defs>'
                      f'<rect x="-2400" y="-1200" width="7200" height="2600" fill="url(#bf23{seed})"/>')
    far = ""
    x = -2200
    while x < 4400:
        bw, bh = rng.uniform(180, 340), rng.uniform(500, 1000)
        far += _tower(x, bw, 700 - bh, 720, rng.choice(["#8E9CAA", "#A3AFBA", "#7F8D9B", "#9AA6B0"]), .04, rng, glass=True)
        x += bw + rng.uniform(10, 50)
    front = ""
    # neighbours either side: brick and render, with shop windows
    for nx, nw, col in ((-1500, 900, "#9A948C"), (-600, 860, "#B8735A"), (2120, 900, "#C4A07E"), (3020, 900, "#8A939E")):
        front += (_r(nx, 120, nw, 780, col, sw=3) + _r(nx + 40, 700, nw - 80, 200, "#1E2228", sw=3)
                  + f'<rect x="{nx + 54}" y="714" width="{nw - 108}" height="150" fill="#D6E2F3" opacity=".9"/>'
                  + "".join(_r(nx + 60 + c * (nw - 120) / 4, 200 + r * 150, (nw - 120) / 4 - 30, 100, "#6E7C88", sw=2) for r in range(3) for c in range(4)))
    # the branch: pale stone, a dark fascia with BANK, a glass front, two glass doors in the middle
    front += (_r(260, 80, 1860, 820, "#E4DED2", sw=3.4)
              + "".join(_r(300 + c * 360, 140, 300, 220, "#7F8D9B", sw=2.4) for c in range(5))
              + _r(300, 400, 1780, 110, "#1F2A36", rx=4, sw=3) + _t(1190, 478, "BANK", 64, fill="#E8E4DC", family="Serif", weight=700, extra='letter-spacing="18"')
              + _r(320, 540, 1740, 360, "#2A3440", sw=3))
    for gx in (340, 560, 1360, 1580, 1800):                                             # glass panes with reflections
        front += (f'<rect x="{gx}" y="556" width="200" height="330" fill="#A9C1CF" opacity=".85"/>'
                  f'<path d="M{gx + 30},866 L{gx + 150},576" stroke="#F4F7F8" stroke-width="16" opacity=".35"/>')
    front += (f'<rect x="800" y="556" width="160" height="454" fill="#B5CAD6" opacity=".92" stroke="#4A5560" stroke-width="6"/>'
              f'<rect x="960" y="556" width="160" height="454" fill="#B5CAD6" opacity=".92" stroke="#4A5560" stroke-width="6"/>'
              + _r(930, 760, 14, 80, "#C9CED2", rx=6, sw=2) + _r(976, 760, 14, 80, "#C9CED2", rx=6, sw=2)
              + f'<path d="M830,990 L930,580" stroke="#F4F7F8" stroke-width="12" opacity=".3"/>'
              + f'<g transform="translate(814,640)">{notice}</g>')
    pave = ('<rect x="-2400" y="900" width="7200" height="160" fill="#B3AEA4"/>'
            f'<rect x="-2400" y="1060" width="7200" height="18" fill="#C9C4BA" stroke="{INK}" stroke-width="3"/>'
            '<rect x="-2400" y="1078" width="7200" height="600" fill="#5A5D62"/>'
            + "".join(f'<path d="M{x},900 L{x - 40},1060" stroke="#9E998F" stroke-width="3"/>' for x in range(-2400, 4800, 180)))
    furn = (_r(1430, 600, 180, 330, "#3A4450", rx=10, sw=3) + _r(1452, 630, 136, 96, "#1B2A30", rx=4, sw=2)
            + f'<rect x="1462" y="640" width="116" height="76" fill="#9FE0D2" opacity=".5" data-flick=\'[0.5,0.15,2]\'/>'
            + _r(1470, 750, 100, 50, "#5A6470", rx=4, sw=2) + _r(1470, 820, 100, 14, "#1F2428", rx=4, sw=2))
    for px_ in (420, 1880):
        furn += (_r(px_ - 70, 920, 140, 90, "#6B6058", rx=6, sw=3)
                 + f'<g data-swing=\'[0.7,0.6,{px_ % 5},{px_},920]\'>' + "".join(
                     f'<circle cx="{px_ + dx}" cy="{900 - abs(dx) * .3:.0f}" r="{40 - abs(dx) * .2:.0f}" fill="#3F6B4A" stroke="{INK}" stroke-width="2.4"/>'
                     for dx in (-50, 0, 50)) + "</g>")
    layers = dict(sky=(0.15, sky), far=(0.3, far), front=(0.5, front), pave=(0.6, pave), furn=(0.7, furn))
    return layers, dict(feet=1010, door=(960, 800), notice=(924, 800))


def _readers(cr, looks, every=2):
    """Rebuild every other walker of a crowd with a phone in hand and a reading pose."""
    out = []
    for i, a in enumerate(cr):
        if i % every == 0:
            sp = a["spec"]
            a = C.actor(sp["id"], looks[i % len(looks)], pos=sp["pos"], scale=sp["scale"], seed=sp["seed"], dir=sp["dir"],
                        pose_keys=[[0, C.pose("relaxed", shF=70, elF=95, head=14, eyeY=1)]], holdF=mini_phone())
        out.append(a)
    return out


def _alive(keys, dur, t0=1.0, every=2.1, amp=6):
    """Small head turns between a figure's actions so nobody holds still."""
    t = t0
    while t < dur:
        if all(abs(t - k[0]) > .8 for k in keys):
            base = dict(max((k for k in keys if k[0] <= t), key=lambda k: k[0])[1])
            base["head"] = base.get("head", 0) + (amp if int(t) % 2 else -amp)
            keys.append([round(t, 2), base])
        t += every
    keys.sort(key=lambda k: k[0])
    return keys


def find_t(ctx, word, default=1.0):
    """When a word is said in the beat, searching every sentence (the first sentence that has it)."""
    for i, (x, a, b) in enumerate(ctx.get("segs") or []):
        if word.lower() in x.lower():
            return word_t(ctx, i, word)
    return default


# ------------------------------------------------------------------------------------------------ shots

def shot_hook_40bn(w, h, dur, ctx):
    """The hook. Frame 0: a phone fills the frame and OVER $40BN counts up from $0 within 1.4 s (deposits that left
    Silicon Valley Bank on 9 March 2023: Fed review, April 2023, "over $40 billion"); IN ONE DAY lands at 1.6 s. On the
    question the phone lowers and the camera pulls back onto a generic branch front of today, people on their phones."""
    t_q = min(dur - 3.0, max(3.5, seg_t(ctx, len(ctx.get("segs") or [0]) - 1, 0.0) - .4))   # the question is the last sentence
    W = 560
    body = (_t(W * .12, W * .62, "DEPOSITS OUT", 40, fill=DIM, anchor="start", family="Sans", weight=700, extra='letter-spacing="3"')
            + _t(W * .12, W * .74, "OVER", 44, fill=LIGHT, anchor="start", family="Sans", weight=700)
            + f'<text x="{W * .1:.0f}" y="{W * 1.02:.0f}" font-family="\'Serif\',serif" font-weight="700" font-size="150" fill="{RED}" '
              f'{C.kv(count=[[0, 0], [.1, 0], [1.4, 40, "out"]])} data-dec="0" data-pre="$" data-suf="BN">$40BN</text>'
            + kt(_t(W * .12, W * 1.18, "IN ONE DAY", 46, fill=MUSTARD, anchor="start", family="Sans", weight=700), None, 1.6, .4)
            + _t(W * .12, W * 1.28, "MARCH 9, 2023", 30, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
            + f'<path d="M{W * .12:.0f},{W * 1.45:.0f} L{W * .88:.0f},{W * 1.45:.0f}" stroke="#2E3A40" stroke-width="3"/>'
            + _t(W * .12, W * 1.54, "FROM ONE BANK:", 34, fill=LIGHT, anchor="start", family="Sans", weight=600)
            + kt(_t(W * .12, W * 1.64, "SILICON VALLEY BANK", 34, fill=LIGHT, anchor="start", family="Sans", weight=700), None, 2.4, .4)
            + _t(W * .12, W * 1.77, "FEDERAL RESERVE REVIEW, 2023", 22, fill="#5E7378", anchor="start", family="Sans", weight=600, extra='letter-spacing="2"'))
    hp = hand_phone(W, 1080, body=body, head="NEWS", sub="OUR ILLUSTRATION", skin="#C98E68", sleeve="#2F3E55")
    ph = (f'<g {C.kv(translate=[[0, 712, 40, -2], [t_q, 712, 50, -1], [t_q + 1.4, 780, 1500, 8, "inout"], [dur, 780, 1500, 8]])}>'
          f'<g transform="scale(.88)">{hp}</g></g>')
    layers_, anc = branch_front_today(seed=61)
    _, cr = L.crowd(8, (-500, 2500), anc["feet"], .95, z_seed=7, looks=STREET_LOOKS, speed=(45, 80), dur=dur + 1, talkers=0, prefix="hb")
    ppl = _readers(cr, STREET_LOOKS)
    stand = C.actor("hb_atm", "office_2023b", pos=[[0, 1300, anc["feet"]]], scale=1.0, seed=79, dir=1, walk=False, holdF=mini_phone(),
                    pose_keys=[[0, C.pose("relaxed", shF=70, elF=95, head=16, eyeY=1)], [t_q + 1.6, C.pose("relaxed", shF=70, elF=95, head=16, eyeY=1)],
                               [t_q + 2.1, C.pose("relaxed", shF=70, elF=95, head=-8, brow=.8)], [dur, C.pose("relaxed", shF=70, elF=95, head=6, eyeY=1)]])
    ppl.append(stand)
    layers = [lay(z, s, noblur=(k == "sky")) for k, (z, s) in layers_.items()]
    layers.insert(len(layers) - 1, lay(.76, "".join(a["svg"] for a in ppl)))
    layers.append(lay(1.0, ph))
    cam = [[0, 960, 560, 1.0], [t_q, 960, 545, 1.03, "sine"], [t_q + 1.6, 960, 560, .86, "inout"], [dur, 990, 560, .82, "sine"]]
    over = [badge("Our illustration · not the real bank", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, 1.0], [t_q + .6, 1.0], [t_q + 1.6, .76]], dof=6, shake=.35, over=over,
                grade="cool", vig=1.1)
    import sfx
    foley = [("tap", .12, .5, .1), ("tap", 1.45, .35, .1), ("buzz", t_q - .9, .25, .2)] + [("step", t, .05, -.2) for a in ppl[:3] for t in C.footsteps(a, dur)][:18]
    amb = sfx.city_ambience(dur + .5, seed=230, night=False, traffic=.6) * .65
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_book_gap(w, h, dur, ctx):
    """The bank office today (our illustration). The wall screen draws SVB's held-to-maturity bonds at 31 Dec 2022 on a
    true scale (10-K: amortized cost $91.3bn, fair value $76.2bn), the gap ($15.2bn) and, beside it, total equity
    ($16.0bn). Sentences: 0 the bank, 1 not going to default, 2 fifteen billion less, 3 equity sixteen billion. An
    analyst walks from the window to the screen and stops; the two at the back desks look up."""
    n = len(ctx.get("segs") or [])
    S = lambda i, f=0.0: seg_t(ctx, min(i, max(n - 1, 0)), f)
    t_book = max(1.2, S(1, .1))
    t_mkt = max(t_book + 1.0, find_t(ctx, "fifteen") - .3)
    t_gap = t_mkt + 1.0
    t_eq = max(t_gap + .9, S(3, .2))
    sc = 8.2                                                                             # px per $bn on the wall screen
    scr = (_t(40, 56, "BONDS HELD TO MATURITY · DECEMBER 31, 2022", 24, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + _t(40, 84, "SILICON VALLEY BANK · $ BILLION · FORM 10-K", 16, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
           + wall_bars(40, 150, [("ON ITS BOOKS (WHAT IT PAID)", 91.3, "#5E7378", t_book, "$91.3BN"),
                                 ("AT MARKET PRICES", 76.2, TEAL, t_mkt, "$76.2BN")], sc, bar_h=60, gap=58)
           + _ktf(f'<rect x="{40 + 76.2 * sc:.0f}" y="268" width="{15.1 * sc:.0f}" height="60" fill="none" stroke="{RED}" stroke-width="4" stroke-dasharray="8 6"/>'
                  + f'<text x="{40 + 83.7 * sc:.0f}" y="372" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="34" fill="{RED}" '
                    f'{C.kv(count=[[0, 0], [t_gap, 0], [t_gap + .8, 15.2, "out"]])} data-dec="1" data-pre="-$" data-suf="BN">-$15.2BN</text>', t_gap, .3)
           + wall_bars(40, 420, [("ALL OF ITS EQUITY", 16.0, MUSTARD, t_eq, "$16.0BN")], sc, bar_h=44, gap=0, size=22)
           )
    layers_, anc = bank_office_today(screen=scr, seed=51, front_monitor=False)
    feet = anc["feet"]
    walker = C.actor("bg_a", "office_2023", pos=[[0, -260, feet], [t_book - .2, -260, feet], [t_book + 2.4, 420, feet, "inout"], [dur, 440, feet]],
                     scale=1.0, seed=101, dir=1,
                     pose_keys=_alive([[0, C.pose("relaxed", head=-4)], [t_book + 2.5, C.pose("relaxed", head=-14, eyeY=-1)],
                                       [t_gap, C.pose("point", head=-16)], [t_gap + 1.2, C.pose("relaxed", head=-14)],
                                       [t_eq + .3, C.pose("concern", head=-12)], [dur, C.pose("concern", head=-10)]], dur, t0=t_eq + 1.2))
    sitters = []
    for i, (x, look) in enumerate(((60, "office_2023b"), (1420, "office_2023c"))):
        keys = _alive([[0, C.pose("seated", head=10, eyeY=1)], [t_mkt + .2 * i, C.pose("seated", head=10, eyeY=1)],
                       [t_mkt + .5 + .2 * i, C.pose("seated", head=-12, lean=-4, brow=.6)], [dur, C.pose("seated", head=-10)]], dur, t0=.6 + i)
        sitters.append(C.actor(f"bg_s{i}", look, pos=[[0, x, 1000]], scale=.92, seed=110 + i, dir=1 if i == 0 else -1, walk=False, pose_keys=keys))
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k not in ("back", "front")]
    layers.append(lay(.62, layers_["back"][1]))
    layers.append(lay(.7, "".join(a["svg"] for a in [walker] + sitters)))
    layers.append(lay(.86, layers_["front"][1]))
    zx = lambda x, z=.4: 960 + (x - 960) / z
    zy = lambda y, z=.4: 540 + (y - 540) / z
    sx, sy = anc["wall_screen"]
    cam = [[0, 900, 560, .9], [t_book - .3, 960, 520, 1.0, "inout"], [t_mkt - .2, 1010, 470, 1.18, "inout"], [t_eq + .2, 1020, 460, 1.24, "sine"],
           [dur, 1030, 460, 1.28, "sine"]]
    over = [title("Silicon Valley Bank, 2022", "Its bonds, on its books", w, h, d=min(2.8, t_book + .6)), badge("Our illustration · figures from the bank's 10-K", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[walker] + sitters, cam=cam, focus=[[0, .55]], dof=3, shake=.2, over=over, grade="cool", vig=1.05,
                tin=("dissolve", .35))
    import sfx
    foley = [("tick", t_book + .1, .3, 0), ("tick", t_mkt + .1, .3, 0), ("hit", t_gap + .1, .35, .1, dict(pitch=150)), ("tick", t_eq + .1, .3, .1)]
    foley += [("step", t, .05, -.3) for t in C.footsteps(walker, dur)][:10]
    amb = sfx.room_tone(dur + .5, seed=261, clock=False, street=.12) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_bond(w, h, dur, ctx, part=1):
    """The puzzle in two beats (our example, not a real bond). Part 1 sentences: 0 our numbers, 1 you buy a ten year
    bond for $100, 2 it pays 1.5% and pays back the 100, 3 rates rise, new bonds pay 4%. Part 2: 0 nobody pays 100,
    1 cut the price until the buyer earns 4%, 2 that price is about $79.70. On the desk monitor: NEW 10-YEAR BONDS
    PAY 1.5% -> 4.0% (part 1, on 'four percent'), YOUR BOND'S PRICE $100.00 -> $79.72 (part 2, on 'seventy nine');
    the price is the sum of the bond's payments discounted at 4% (build/plans/ep014_checks.py)."""
    n = len(ctx.get("segs") or [])
    S = lambda i, f=0.0: seg_t(ctx, min(i, max(n - 1, 0)), f)
    gone = -9.0
    if part == 1:
        t_paper = max(.8, S(1, .2))
        t_rate = max(t_paper + 1.5, find_t(ctx, "four percent") - .2)
        t_price, t_earn = dur + 99, dur + 99
    else:
        t_paper, t_rate = gone, gone + .5
        t_price = max(1.2, find_t(ctx, "seventy nine") - .3)
        t_earn = max(.8, S(1, .5))
    rows = [("NEW 10-YEAR BONDS PAY", None, MUSTARD, .3 if part == 1 else gone, _fold([[gone - 1, 1.5], [t_rate, 1.5], [t_rate + 1.0, 4.0, "out"]]), (1, "", "%")),
            ("YOUR BOND PAYS", "1.5%", "#C9D4D6", .6 if part == 1 else gone, None, None)]
    if part == 2:
        rows.append(("YOUR BOND'S PRICE TODAY", None, RED, .3, [[0, 100], [t_price, 100], [t_price + 1.2, 79.72, "out"]], (2, "$", "")))
    rows = [r[:4] + ([k for k in r[4] if k[0] < dur + 50] if r[4] else None, r[5]) for r in rows]
    dscr = (_t(36, 50, "OUR EXAMPLE · A $100 BOND, 10 YEARS", 20, fill=DIM, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
            + rows_screen(rows, x0=36, y0=120, step=86, wid=570, size=26)
            + (_ktf(_r(36, 312, 570, 44, TEAL, rx=6, sw=0) + _t(321, 342, "PRICED SO A BUYER EARNS 4% A YEAR", 20, fill="#fff", family="Sans", weight=700), t_earn, .3)
               if part == 2 else ""))
    layers_, anc = bank_office_today(desk_screen=dscr, desk_prop=bond_paper(t_in=t_paper if part == 1 else 0), seed=52)
    sx, sy = anc["seat"]
    keys = [[gone - 1, C.pose("seated", head=12, eyeY=1, lean=8)]]
    if part == 1:
        keys += [[t_paper - .2, C.pose("seated", head=16, eyeY=1.4, lean=12)], [t_rate, C.pose("seated", head=10, lean=8)],
                 [t_rate + .6, C.pose("seated", head=6, lean=2, brow=.6)], [dur, C.pose("seated", head=8, lean=4, brow=.3)]]
    else:
        keys += [[t_price, C.pose("seated", head=10, lean=10, eyeY=1)], [t_price + 1.3, C.pose("seated", head=-4, lean=-6, brow=1, mouth=2)],
                 [t_price + 2.6, C.pose("seated", shF=30, elF=110, head=4, brow=-1)], [dur, C.pose("seated", shF=30, elF=110, head=2, brow=-1)]]
    keys = _alive(_fold(keys), dur, t0=.9, every=1.9)
    an = C.actor("bd", "office_2023c", pos=[[0, sx, sy]], scale=1.0, seed=121, dir=-1, walk=False, pose_keys=keys)
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k != "front"]
    layers.append(lay(.82, an["svg"]))
    layers.append(lay(.86, layers_["front"][1]))
    zx = lambda x, z=.86: 960 + (x - 960) / z
    zy = lambda y, z=.86: 540 + (y - 540) / z
    mx, my = anc["monitor"]
    px, py = anc["paper"]
    if part == 1:
        cam = [[0, zx(760), zy(640), 1.05], [t_paper - .2, zx(px), zy(py), 1.55, "inout"], [t_rate - .6, zx(mx), zy(my), 1.45, "inout"],
               [dur, zx(mx + 10), zy(my), 1.5, "sine"]]
    else:
        cam = [[0, zx(mx + 10), zy(my), 1.5], [t_price - .3, zx(mx), zy(my + 20), 1.6, "inout"], [t_price + 1.6, zx(820), zy(650), 1.12, "inout"],
               [dur, zx(840), zy(650), 1.1, "sine"]]
    over = [badge("Our example · not a real bond", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[an], cam=cam, focus=[[0, .86]], dof=4, shake=.2, over=over, grade="cool", vig=1.1,
                tin=("dissolve", .35) if part == 1 else ("cut", 0))
    import sfx
    foley = [(nm, t, g, 0, *rest) for nm, t, g, *rest in (("paper", t_paper, .4), ("tick", t_rate, .3), ("tick", t_rate + .5, .25),
                                                          ("tick", t_price, .3), ("hit", t_price + 1.2, .35, dict(pitch=140)), ("tick", t_earn, .25)) if 0 < t < dur]
    amb = sfx.room_tone(dur + .5, seed=270 + part, clock=False, street=.12) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_bond_2(w, h, dur, ctx):
    return shot_bond(w, h, dur, ctx, part=2)


def shot_march8(w, h, dur, ctx):
    """8 March 2023 at a kitchen table at night (our illustration). The laptop types the announcement as it is said
    (Fed review, executive summary: sold $21bn of AFS securities, a $1.8bn after-tax loss, seeking $2.25bn of
    capital). Sentences: 0 sold and booked the loss, 1 planned to raise capital."""
    t_sold = max(1.0, find_t(ctx, "twenty one") - .2)
    t_loss = max(t_sold + 1.0, find_t(ctx, "one point eight") - .2)
    t_cap = max(t_loss + 1.0, find_t(ctx, "two point two five") - .2)
    sw_, sh_ = 620, 380
    scr = (_t(24, 44, "MARCH 8, 2023 · THE BANK ANNOUNCES", 20, fill=LIGHT, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + _t(24, 70, "OUR ILLUSTRATION · FIGURES FROM THE FED'S REVIEW", 13, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
           + rows_screen([("BONDS SOLD", None, "#C9D4D6", t_sold - .2, [[0, 0], [t_sold, 0], [t_sold + .7, 21, "out"]], (0, "$", "BN")),
                          ("LOSS, AFTER TAX", None, RED, t_loss - .2, [[0, 0], [t_loss, 0], [t_loss + .7, 1.8, "out"]], (1, "$", "BN")),
                          ("NEW CAPITAL SOUGHT", None, MUSTARD, t_cap - .2, [[0, 0], [t_cap, 0], [t_cap + .8, 2.25, "out"]], (2, "$", "BN"))],
                         x0=24, y0=140, step=82, wid=560, size=24))
    layers_, anc = kitchen_2021(night=True, seed=33, screen=scr)
    sx, sy = anc["seat"]
    viewer = C.actor("m8", "office_2023b", pos=[[0, sx, sy]], scale=1.0, seed=131, dir=-1, walk=False,
                     pose_keys=_alive([[0, C.pose("seated", head=10, eyeY=1)], [t_sold - .3, C.pose("seated", head=12, lean=10, eyeY=1)],
                                       [t_loss + .4, C.pose("seated", head=-4, lean=-4, brow=1, mouth=2)], [t_cap + .6, C.pose("seated", shF=30, elF=110, head=6, brow=-1)],
                                       [dur, C.pose("seated", shF=30, elF=110, head=4, brow=-1)]], dur, t0=.8))
    layers = [lay(z, s, noblur=(k in ("glow",))) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.82, viewer["svg"]))
    layers.append(lay(.85, layers_["table"][1]))
    zx = lambda x, z=.85: 960 + (x - 960) / z
    zy = lambda y, z=.85: 540 + (y - 540) / z
    lx, ly = anc["laptop"]
    cam = [[0, zx(900), zy(640), .95], [t_sold - .4, zx(lx), zy(ly - 240), 1.5, "inout"], [t_cap + .6, zx(lx + 20), zy(ly - 240), 1.6, "sine"],
           [dur, zx(900), zy(620), 1.15, "inout"]]
    over = [title("March 8, 2023", "An announcement", w, h, d=min(2.6, t_sold - .3)), badge("Our illustration · figures from the Federal Reserve's review", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[viewer], cam=cam, focus=[[0, .85]], dof=4, shake=.25, over=over, grade="warm", vig=1.15, tin=("dissolve", .35))
    import sfx
    foley = [("tick", t, .3, 0) for t in (t_sold, t_loss, t_cap)] + [("hit", t_loss + .2, .3, 0, dict(pitch=160))]
    amb = sfx.room_tone(dur + .5, seed=281, clock=False, street=.2) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_run_street(w, h, dur, ctx):
    """9 March 2023: a street by day, people walking with their phones. The billboard counts OUT ON MARCH 9: OVER $40BN
    and EXPECTED MARCH 10: OVER $100BN on the words (Fed review: "over $40 billion", "over $100 billion more").
    Sentences: 0 connected depositors, 1 the Fed's words, 2 over forty billion left, 3 over a hundred billion more."""
    n = len(ctx.get("segs") or [])
    t40 = max(1.0, find_t(ctx, "forty") - .2)
    t100 = max(t40 + 1.5, find_t(ctx, "hundred") - .2)
    rows = [("OUT ON MARCH 9", [[0, 0], [t40, 0], [t40 + 1.0, 40, "out"]], 0, "OVER $", "BN", "#F08A6A"),
            ("EXPECTED MARCH 10", [[0, 0], [t100, 0], [t100 + 1.0, 100, "out"]], 0, "OVER $", "BN", "#F6D58A")]
    bb = ('<g transform="translate(450,30) scale(.86)">' + _t(0, 40, "SILICON VALLEY BANK · DEPOSITS", 30, fill=LIGHT, family="Sans", weight=700, extra='letter-spacing="3"')
          + board_rows_svg(0, rows, top=130, wid=880) + "</g>"
          + _t(450, 350, "FEDERAL RESERVE REVIEW, APRIL 2023", 18, fill=DIM, family="Sans", weight=600, extra='letter-spacing="2"'))
    layers_, anc = street_today(night=False, seed=23, billboard=bb)
    _, cr = L.crowd(9, (-600, 2600), anc["feet"], .95, z_seed=11, looks=STREET_LOOKS, speed=(60, 110), dur=dur + 1, talkers=0, prefix="rs")
    ppl = _readers(cr, STREET_LOOKS, every=1)
    layers = [lay(z, s, noblur=(k in ("light", "sky"))) for k, (z, s) in layers_.items()]
    layers.insert(len(layers) - 1, lay(.76, "".join(a["svg"] for a in ppl)))
    cam = [[0, 960, 600, .86], [t40 - .3, 960, 470, 1.0, "inout"], [t100 + 1.2, 960, 480, 1.02, "sine"], [dur, 980, 560, .9, "inout"]]
    over = [badge("Our illustration · Fed review figures", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, .5], [t100 + 1.4, .5], [dur, .76]], dof=4, shake=.3, over=over, grade="cool",
                vig=1.05, tin=("dissolve", .35))
    import sfx
    foley = [("flap", t40 + .1, .35, 0), ("flap", t100 + .1, .35, 0), ("buzz", .6, .2, -.3), ("buzz", t40 + 1.4, .2, .4)]
    foley += [("step", t, .05, -.2) for a in ppl[:3] for t in C.footsteps(a, dur)][:18]
    amb = sfx.city_ambience(dur + .5, seed=291, night=False, traffic=.7) * .6
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_closed(w, h, dur, ctx):
    """Friday 10 March 2023 (reconstruction, not the real branch). A woman walks to the branch door, pushes it (it does
    not open), reads the notice on the glass and steps back. The notice is our illustration of what the record says:
    closed on 10 March by the California regulator, the FDIC appointed receiver (Fed review; FDIC press release)."""
    t_arrive = 2.4
    t_push = t_arrive + .3
    t_read = t_push + 1.0
    notice = (_r(0, 0, 220, 280, "#FBFAF6", rx=2, sw=2.4) + _t(110, 40, "NOTICE", 26, fill=INK, family="Serif", weight=700, extra='letter-spacing="3"')
              + _t(110, 78, "THIS BANK WAS", 15, fill=INK, family="Sans", weight=700) + _t(110, 100, "CLOSED ON", 15, fill=INK, family="Sans", weight=700)
              + _t(110, 130, "MARCH 10, 2023", 20, fill=RED, family="Sans", weight=700)
              + _t(110, 160, "BY THE CALIFORNIA", 13, fill=INK, family="Sans", weight=600) + _t(110, 178, "REGULATOR", 13, fill=INK, family="Sans", weight=600)
              + _t(110, 210, "FDIC APPOINTED", 14, fill=TEAL, family="Sans", weight=700) + _t(110, 230, "RECEIVER", 14, fill=TEAL, family="Sans", weight=700)
              + _t(110, 264, "OUR ILLUSTRATION", 10, fill="#7A7F86", family="Sans", weight=600, extra='letter-spacing="2"'))
    layers_, anc = branch_front_today(notice=notice, seed=62)
    feet = anc["feet"]
    dx, _ = anc["door"]
    wom = C.actor("cl", "lady_2021b", pos=[[0, 120, feet], [t_arrive, dx - 270, feet, "out"], [t_read + 2.6, dx - 270, feet], [t_read + 3.4, dx - 330, feet, "inout"],
                                          [dur, dx - 340, feet]], scale=1.06, seed=141, dir=1,
                  pose_keys=_alive([[0, C.pose("relaxed", head=2)], [t_arrive, C.pose("relaxed", head=0)], [t_push, C.pose("reach", head=2)],
                                    [t_push + .25, C.pose("reach", shF=58, head=2)], [t_push + .5, C.pose("reach", head=2)],
                                    [t_read, C.pose("read", shF=10, elF=20, shB=6, elB=20, head=-8, eyeY=-.6)], [t_read + 2.4, C.pose("concern", head=-6)],
                                    [t_read + 3.4, C.pose("concern", head=-2, brow=-1)], [dur, C.pose("hold_up", head=-8, brow=-1)]], dur, t0=t_read + 3.6, amp=4))
    _, cr = L.crowd(2, (1500, 2600), feet + 40, 1.0, z_seed=13, looks=STREET_LOOKS, speed=(50, 80), dirs=(1,), dur=dur + 1, talkers=0, prefix="cc")
    ppl = _readers(cr, STREET_LOOKS)
    layers = [lay(z, s, noblur=(k == "sky")) for k, (z, s) in layers_.items()]
    layers.insert(len(layers) - 1, lay(.74, wom["svg"]))
    layers.insert(len(layers) - 1, lay(.8, "".join(a["svg"] for a in ppl)))
    zx = lambda x, z=.5: 960 + (x - 960) / z
    zy = lambda y, z=.5: 540 + (y - 540) / z
    nx, ny = anc["notice"]
    cam = [[0, 900, 560, .86], [t_arrive, 940, 560, .95, "inout"], [t_read - .2, zx(nx - 40), zy(ny), 1.9, "inout"], [t_read + 2.4, zx(nx - 40), zy(ny + 6), 2.0, "sine"],
           [t_read + 3.6, 930, 560, 1.0, "inout"], [dur, 920, 560, .96, "sine"]]
    over = [title("Friday, March 10, 2023", "The branch door", w, h, d=2.2), badge("Reconstruction · not the real branch", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[wom] + ppl, cam=cam, focus=[[0, .74]], dof=4, shake=.25, over=over, grade="cool", vig=1.1,
                tin=("dissolve", .35))
    import sfx
    foley = [("clank", t_push + .05, .35, 0, dict(pitch=220)), ("clank", t_push + .3, .25, 0, dict(pitch=200)), ("paper", t_read, .2, 0)]
    foley += [("step", t, .06, -.1) for t in C.footsteps(wom, dur)][:12]
    amb = sfx.city_ambience(dur + .5, seed=301, night=False, traffic=.5) * .55
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_growth(w, h, dur, ctx):
    """2019 to 2021 in the bank office by day (our illustration): the wall screen draws total assets on a true scale as
    they are said (Fed review, key takeaways: "$71 billion to over $211 billion in assets from 2019 to 2021"), and a
    TRIPLED tag lands; people come in and cross the floor, a seated banker turns to watch. 20 Nov: filmed so the
    opening minute has no static second (yt_preview's new opening gate failed 49 to 59 s on the drawn version).
    Sentences: 0 the bank of young tech companies, 1 tripled, $71bn to over $211bn."""
    t71 = max(1.2, find_t(ctx, "seventy one") - .2)
    t211 = max(t71 + 1.0, find_t(ctx, "two hundred and eleven") - .2)
    t3 = max(.8, find_t(ctx, "tripled") - .1)
    sc = 3.0                                                                             # px per $bn
    scr = (_t(40, 56, "SILICON VALLEY BANK · TOTAL ASSETS", 24, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + _t(40, 84, "$ BILLION · FEDERAL RESERVE REVIEW, 2023", 16, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
           + wall_bars(40, 170, [("2019", 71, "#5E7378", t71, "$71BN"), ("2021", 211, TEAL, t211, "OVER $211BN")], sc, bar_h=70, gap=70, size=26)
           + _ktf(_r(700, 40, 250, 56, RED, rx=28, sw=0) + _t(825, 78, "TRIPLED", 28, fill="#fff", family="Sans", weight=700, extra='letter-spacing="3"'),
                  max(t3, t211 + .9), .3))
    layers_, anc = bank_office_today(screen=scr, seed=53, front_monitor=False)
    feet = anc["feet"]
    looks = ["office_2023", "lady_2021", "jacket_2021", "office_2023c", "tee_2021"]
    ppl = []
    for i in range(5):                                                                   # people arriving, at their own pace
        t0 = .3 + i * (dur / 5.5)
        x0, x1 = (-700, 1900) if i % 2 == 0 else (2600, 200)
        v = 150 if i % 2 == 0 else -140
        xa = x0
        pos = [[0, x0, feet + (i % 3) * 14], [t0, x0, feet + (i % 3) * 14], [dur + 1, x0 + v * (dur + 1 - t0), feet + (i % 3) * 14, "lin"]]
        ppl.append(C.actor(f"gw{i}", looks[i], pos=pos, scale=.95, seed=150 + i, dir=1 if v > 0 else -1, amp=22))
    sit = C.actor("gw_s", "office_2023b", pos=[[0, 1420, 1000]], scale=.92, seed=160, dir=-1, walk=False,
                  pose_keys=_alive([[0, C.pose("seated", head=10, eyeY=1)], [t211, C.pose("seated", head=10, eyeY=1)],
                                    [t211 + .4, C.pose("seated", head=-14, lean=-4, brow=.8)], [dur, C.pose("seated", head=-10)]], dur, t0=.6))
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k not in ("back", "front")]
    layers.append(lay(.62, layers_["back"][1]))
    layers.append(lay(.7, "".join(a["svg"] for a in ppl + [sit])))
    layers.append(lay(.86, layers_["front"][1]))
    cam = [[0, 880, 600, .92], [t71 - .3, 980, 500, 1.1, "inout"], [t211 + 1.0, 1010, 470, 1.2, "sine"], [dur, 990, 520, 1.08, "inout"]]
    over = [title("2019 to 2021", "A bank of young tech companies", w, h, d=min(2.8, t71 - .2)), badge("Our illustration · figures from the Fed's review", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl + [sit], cam=cam, focus=[[0, .55]], dof=3, shake=.2, over=over, grade="warm", vig=1.05,
                tin=("dissolve", .35))
    import sfx
    foley = [("tick", t71 + .1, .3, 0), ("tick", t211 + .1, .3, 0), ("hit", max(t3, t211 + .9) + .1, .3, .1, dict(pitch=170))]
    foley += [("step", t, .05, -.2) for a in ppl[:3] for t in C.footsteps(a, dur)][:18]
    amb = sfx.room_tone(dur + .5, seed=311, clock=False, street=.15) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


SHOTS = dict(growth=shot_growth, hook_40bn=shot_hook_40bn, book_gap=shot_book_gap, bond_1=shot_bond, bond_2=shot_bond_2, march8=shot_march8,
             run_street=shot_run_street, closed=shot_closed)


if __name__ == "__main__":
    # stills for a quick look: python3 build/cine_2023.py [name ...]
    names = sys.argv[1:] or list(SHOTS)
    work = C.OUT / "cine-2023-stills"
    work.mkdir(parents=True, exist_ok=True)
    demo = dict(segs=[("The bank was Silicon Valley Bank, our numbers, twenty one billion.", .3, 3.6),
                      ("Its bonds weren't going to default, you buy a ten year bond, one point eight, two point two five, nobody, cut the price.", 3.8, 7.6),
                      ("But they were worth fifteen billion less, forty billion left, seventy nine dollars.", 7.8, 11.0),
                      ("Its equity was sixteen billion, new bonds pay four percent, a hundred billion more.", 11.2, 14.0)])
    for nm in names:
        built = SHOTS[nm](1920, 1080, 15.0, demo)
        html, total = C.film_html(built["shots"], 1920, 1080)
        print(nm, [p.name for p in C.stills(html, [0.2, 1.6, total * .4, total * .7, total - .3], work, nm)])
