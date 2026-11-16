"""
Filmed beats for YouTube #10, the salad oil swindle of 1963 (16 Nov 2026). Sets, props and shots for build/cine.py,
used by build/youtube_ep010.py as kind="cine" beats (cinematic-standard.md section 8, step 3: sets).

Sets (our own generic drawings; no real site, building, logo or person is copied; everything is badged):
  tank_farm()     an oil tank yard by the water at dusk or at night: big cylindrical tanks with ladders, catwalks and
                  painted numbers, pipes and valves between them, lamp posts, a fence, far tanks across the yard and a
                  generic far shore. One tank can be cut away to show what is inside (tank_body(cut=...)).
  chain_strip()   one long world for the receipt's journey: the yard, a field-warehouse office, a broker's desk and
                  a bank counter, side by side, so the camera can follow a paper from one to the next.
Props: warehouse_receipt() (our design, figures greeked), clipboard(), oil_level() (a liquid that rises or falls).
1963 looks (cine.LOOKS): inspector_1963 (raincoat), worker_1963 (cap and overalls), broker_1963, banker_1963.

Shots (fn(w, h, dur, ctx) -> dict(shots, foley, amb); ctx["segs"] are the beat's sentences, (text, start, end)):
  yard_hook      the hook: the yard at dusk, a slow push along the tanks; an inspector walks with a clipboard
  receipt_chain  our illustration: the tank, the warehouse company's receipt, the broker, the bank; money comes back
  tape_trick     a man on a tank lowers a tape and calls down; the inspector writes 90%; the cutaway shows the inside
  slick          the cutaway of a tank of water topped by a thin slick of oil, seen from the hatch and from the side
  pipes_night    a weekend night: oil pumped from one tank to the next, so the same oil is counted twice
  margin_calls   the dealing room, November 1963: phones ring and the board counts margin calls to $19,000,000
  exchange_close Friday 22 November 1963: the board stops at 2:07 p.m.; the Dow line shows -2.9% for the day
Facts on screen come only from the sources in youtube_ep010.py's docstring. Nobody in a shot speaks, and nobody is a
likeness: the figures are "our illustration", not portraits of De Angelis, inspectors or bankers.
"""

import math
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402
from cine_1907 import lay, badge, seg_t, word_t   # noqa: E402
from cine_1920 import title, cash_stack           # noqa: E402
from cine_1971 import kt, dealing_room, traders, desk_phone, typewriter, handset   # noqa: E402

INK, RED, TEAL, MUSTARD, PAPER = C.INK, C.RED, C.TEAL, C.MUSTARD, "#F7F5F2"
OIL, OIL2, WATER, WATER2 = "#E8B33A", "#C98F1E", "#5D8FA8", "#3F6E86"
_r, _t = L._r, L._t

C.LOOKS.update({
    "inspector_1963": dict(coat="#B8A27A", coat2="#9C8862", vest="#F1E6CF", legs="#4A4440", stock="#4A4440", shoe=INK, skin="#E5B391",
                           hair="#4A3424", hat="", style="suit", cuff="#F1E6CF", tie="#7A3B22", era="1971"),
    "worker_1963": dict(coat="#4F6A7A", coat2="#3E5664", vest="#C9A27A", legs="#3E5664", stock="#3E5664", shoe="#2A1E18", skin="#D59E7B",
                        hair="#3A2A20", hat="cap", style="suit", cuff="#D8CFC0", tie="#4F6A7A", era="1971"),
    "worker_1963b": dict(coat="#6B5A44", coat2="#55473A", vest="#D8CFC0", legs="#4A3B30", stock="#4A3B30", shoe="#2A1E18", skin="#8D5A3B",
                         hair="#14100D", hat="cap", style="suit", cuff="#D8CFC0", tie="#6B5A44", era="1971"),
    "broker_1963": dict(coat="#2F3540", coat2="#22272F", vest="#F2F2F2", legs="#2F3540", stock="#2F3540", shoe=INK, skin="#F0C7A4",
                        hair="#7A5A3A", hat="", style="suit", cuff="#F2F2F2", tie=RED, era="1971"),
    "banker_1963": dict(coat="#3A3A40", coat2="#2A2A30", vest="#F2F2F2", legs="#3A3A40", stock="#3A3A40", shoe=INK, skin="#D9A684",
                        hair="#BDB4A6", hat="", style="suit", cuff="#F2F2F2", tie=TEAL, era="1971"),
})


# ------------------------------------------------------------------------------------------------ props

def warehouse_receipt(w=220, h=140, label="WAREHOUSE RECEIPT"):
    """A generic warehouse receipt of our own design: a printed head, greeked lines (no figure is legible), a signature
    scrawl and a round seal."""
    out = _r(-w / 2, -h / 2, w, h, "#F4EEDD", rx=3, sw=2.4)
    out += f'<rect x="{-w / 2 + 7}" y="{-h / 2 + 7}" width="{w - 14}" height="{h - 14}" fill="none" stroke="#8A7A5A" stroke-width="1.6"/>'
    out += _t(0, -h / 2 + 30, label, max(11, w * .07), fill="#3A3024", family="Sans", weight=700, extra='letter-spacing="2"')
    for k in range(3):
        out += f'<path d="M{-w / 2 + 22},{-h / 2 + 52 + 20 * k} L{w / 2 - 22 - 30 * (k == 2)},{-h / 2 + 52 + 20 * k}" stroke="#B9AE9A" stroke-width="5" stroke-linecap="round"/>'
    out += f'<path d="M{-w / 2 + 24},{h / 2 - 22} q14,-16 26,-2 t24,-4 t22,2" fill="none" stroke="#2A3A5A" stroke-width="2.4"/>'
    out += f'<circle cx="{w / 2 - 36}" cy="{h / 2 - 30}" r="18" fill="none" stroke="{RED}" stroke-width="3"/>'
    return out


def clipboard(w=90, h=120, text=None, at=None):
    """A clipboard; text (sourced only) is written on it at 'at'."""
    out = _r(-w / 2, -h / 2, w, h, "#9C7A4E", rx=6, sw=2.4) + _r(-w / 2 + 8, -h / 2 + 14, w - 16, h - 22, PAPER, sw=1.6)
    out += _r(-16, -h / 2 - 6, 32, 16, "#8A8F94", rx=3, sw=1.8)
    for k in range(3):
        out += f'<path d="M{-w / 2 + 16},{-h / 2 + 34 + 14 * k} L{w / 2 - 16},{-h / 2 + 34 + 14 * k}" stroke="#CFC6B6" stroke-width="3"/>'
    if text:
        out += (f'<g {C.kv(clip=[[0, 0, 100, 0, 0], [at - .01, 0, 100, 0, 0], [at + .5, 0, 0, 0, 0]])}>'
                + _t(0, h / 2 - 16, text, 22, fill=RED, family="Serif", weight=700) + "</g>")
    return out


_CLIP = [0]


def tank_body(x, base, w, h, num="", cut=None, seed=0):
    """A vertical storage tank, front-on: shaded steel shell, a low dome, a ladder up the right side, a railing on top,
    a painted number. cut: dict(at=, water=[[t, frac]...], oil=[[t, frac]...], slick=px, tape=(t0, t1, frac)) opens
    the front of the shell from 'at' to show the inside: water and oil levels as fractions of the height."""
    rng = random.Random(seed)
    top = base - h
    _CLIP[0] += 1
    gid, cid = f"steel{_CLIP[0]}", f"tc{_CLIP[0]}"
    out = (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8E9396"/>'
           f'<stop offset=".35" stop-color="#D3D6D4"/><stop offset=".7" stop-color="#B2B7B8"/><stop offset="1" stop-color="#6E7375"/></linearGradient>'
           f'<clipPath id="{cid}"><rect x="{x - w / 2 + 6}" y="{top + 4}" width="{w - 12}" height="{h - 8}"/></clipPath></defs>')
    out += f'<ellipse cx="{x}" cy="{base + 4}" rx="{w * .56:.0f}" ry="16" fill="#000" opacity=".25"/>'
    out += f'<rect x="{x - w / 2}" y="{top}" width="{w}" height="{h}" fill="url(#{gid})" stroke="{INK}" stroke-width="4"/>'
    for k in range(1, 6):                                              # welded courses
        out += f'<path d="M{x - w / 2},{top + h * k / 6:.0f} L{x + w / 2},{top + h * k / 6:.0f}" stroke="#7E8385" stroke-width="2" opacity=".7"/>'
    for k in range(int(w / 40)):                                       # rust streaks
        sx = x - w / 2 + 20 + rng.uniform(0, w - 40)
        out += f'<path d="M{sx:.0f},{top + rng.uniform(10, 60):.0f} l{rng.uniform(-3, 3):.0f},{rng.uniform(40, 140):.0f}" stroke="#9A6A48" stroke-width="{rng.uniform(2, 5):.0f}" opacity=".35" stroke-linecap="round"/>'
    out += f'<path d="M{x - w / 2},{top} Q{x},{top - h * .09:.0f} {x + w / 2},{top} Z" fill="#B7BBBB" stroke="{INK}" stroke-width="4"/>'
    out += f'<path d="M{x - w / 2 + 10},{top - 30} L{x + w / 2 - 10},{top - 30}" stroke="{INK}" stroke-width="3"/>'
    for k in range(9):
        px = x - w / 2 + 10 + (w - 20) * k / 8
        out += f'<path d="M{px:.0f},{top - 30} L{px:.0f},{top - 2 - h * .09 * (1 - abs(2 * k / 8 - 1) ** 2) * .9:.0f}" stroke="{INK}" stroke-width="2.4"/>'
    lx = x + w / 2 - 40                                                # ladder
    out += f'<path d="M{lx},{base} L{lx},{top - 30} M{lx + 26},{base} L{lx + 26},{top - 30}" stroke="#3A3F42" stroke-width="4"/>'
    out += "".join(f'<path d="M{lx},{y} L{lx + 26},{y}" stroke="#3A3F42" stroke-width="3"/>' for y in range(int(base) - 20, int(top) - 30, -28))
    if num:
        out += _t(x - w * .12, top + h * .42, num, max(28, w * .16), fill="#F4F1EA", family="Sans", weight=700, extra='opacity=".85" letter-spacing="3"')
    if cut:
        at = cut["at"]
        inner_h = h - 8
        y0 = top + 4
        liquid = f'<rect x="{x - w / 2 + 6}" y="{y0}" width="{w - 12}" height="{inner_h}" fill="#2E2A26"/>'
        liquid += "".join(f'<path d="M{x - w / 2 + 6},{y0 + inner_h * k / 6:.0f} L{x + w / 2 - 6},{y0 + inner_h * k / 6:.0f}" stroke="#3B3632" stroke-width="2"/>' for k in range(1, 6))
        wk = cut.get("water", [[0, 0]])
        ok = cut.get("oil", [[0, 0]])
        # water: a rect from the floor up, its top at frac of the height (translate keys move it)
        wkeys = [[t, 0, inner_h * (1 - f)] for t, f in wk]
        liquid += (f'<g {C.kv(translate=wkeys)}><rect x="{x - w / 2 + 6}" y="{y0}" width="{w - 12}" height="{inner_h}" fill="{WATER}"/>'
                   + "".join(f'<path d="M{x - w / 2 + 20 + 60 * k},{y0 + 30 + 40 * (k % 3)} q20,-8 40,0" stroke="{WATER2}" stroke-width="3" fill="none" opacity=".6"/>' for k in range(int((w - 40) / 60)))
                   + "</g>")
        slick = cut.get("slick", 14)
        okeys = [[t, 0, inner_h * (1 - f) - (slick if any(v for _, v in wk) else 0)] for t, f in ok]
        if any(f for _, f in ok):
            hh = inner_h if not any(v for _, v in wk) else slick
            oa = cut.get("oil_at")
            liquid += (f'<g {C.kv(translate=okeys, **({"opacity": [[0, 0], [oa, 0], [oa + .3, 1]]} if oa is not None else {}))}><rect x="{x - w / 2 + 6}" y="{y0}" width="{w - 12}" height="{hh}" fill="{OIL}"/>'
                       f'<path d="M{x - w / 2 + 6},{y0 + 2} L{x + w / 2 - 6},{y0 + 2}" stroke="#F6D58A" stroke-width="4"/></g>')
        if cut.get("tape"):
            t0, t1, frac = cut["tape"]
            liquid += (f'<path d="M{x + w * .18:.0f},{y0} L{x + w * .18:.0f},{y0 + inner_h * frac:.0f}" stroke="#E8E1D4" stroke-width="3" stroke-dasharray="10 6" '
                       f'{C.kv(dash=[[0, 0], [t0, 0], [t1, 1]])}/>')
        out += (f'<g clip-path="url(#{cid})"><g {C.kv(opacity=[[0, 0], [at, 0], [at + .6, 1]])}>{liquid}</g></g>'
                f'<path d="M{x - w / 2 + 6},{top + 4} L{x - w / 2 + 6},{base - 4} M{x + w / 2 - 6},{top + 4} L{x + w / 2 - 6},{base - 4}" stroke="{INK}" stroke-width="5" '
                f'{C.kv(opacity=[[0, 0], [at, 0], [at + .6, 1]])}/>')
    return out


def pipe(points, w=22, color="#7E8486", flow=None):
    """A pipe along points; flow=(t0, t1) runs oil through it (a gold dash that travels)."""
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in points)
    out = (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 6}" stroke-linejoin="round"/>'
           f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"/>'
           f'<path d="{d}" fill="none" stroke="#A9AEAF" stroke-width="{w * .25:.0f}" stroke-linejoin="round" transform="translate(0,-{w * .25:.0f})" opacity=".6"/>')
    if flow:
        t0, t1 = flow
        out += (f'<path d="{d}" fill="none" stroke="{OIL}" stroke-width="{w * .55:.0f}" stroke-linejoin="round" stroke-linecap="round" '
                f'{C.kv(dash=[[0, 0], [t0, 0], [t0 + (t1 - t0) * .4, 1]], opacity=[[0, 0], [t0, 0], [t0 + .1, 1], [t1, 1], [t1 + .5, 0]])}/>')
    return out


def valve(x, y, r=26):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M{x - r * .7},{y} L{x + r * .7},{y} M{x},{y - r * .7} L{x},{y + r * .7}" stroke="{INK}" stroke-width="3"/>')


def lamp_post(x, base, h=520):
    return (f'<path d="M{x},{base} L{x},{base - h} L{x + 70},{base - h}" fill="none" stroke="#2E3236" stroke-width="10"/>'
            f'<path d="M{x + 50},{base - h} L{x + 90},{base - h} L{x + 84},{base - h + 22} L{x + 56},{base - h + 22} Z" fill="#3A3F42" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="{x + 70}" cy="{base - h + 40}" r="240" fill="url(#glowWarm)" opacity=".45" data-flick=\'[0.45,0.06,{x % 5}]\'/>')


# ------------------------------------------------------------------------------------------------ sets

def tank_farm(night=False, seed=3, cut=None, cut_index=1, nums=("7", "8", "9", "10"), xs=(180, 760, 1340, 1920), flow=None, levels=None):
    """The yard. Returns (layers, anchors). Main tanks on the z .7 layer, base y 900, 440 wide and 540 high; ground
    from y 900; the far shore and water from y 560 at z .25 and .3. cut: a cut dict for tank number cut_index."""
    rng = random.Random(seed)
    sky = ("#1E2738", "#3A4660", "#6B5A6A") if night else ("#3C4A66", "#C98A6A", "#F0B87A")
    back = (C.defs() + f'<defs><linearGradient id="ysky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky[0]}"/>'
            f'<stop offset=".6" stop-color="{sky[1]}"/><stop offset="1" stop-color="{sky[2]}"/></linearGradient></defs>'
            f'<rect x="-2600" y="-1400" width="8000" height="2100" fill="url(#ysky)"/>')
    if night:
        back += "".join(f'<circle cx="{rng.uniform(-2000, 4000):.0f}" cy="{rng.uniform(-900, 300):.0f}" r="{rng.uniform(1, 2.4):.1f}" fill="#F4F1EA" opacity="{rng.uniform(.3, .8):.2f}"/>' for _ in range(70))
    shore = ""
    x = -2400
    while x < 4600:                                                    # a generic far shore: low blocks and a few towers
        bw, bh = rng.uniform(60, 160), rng.uniform(30, 160) * (2.2 if rng.random() < .12 else 1)
        shore += f'<rect x="{x:.0f}" y="{600 - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{"#4A4F62" if not night else "#2A3042"}" opacity=".75"/>'
        if night and rng.random() < .5:
            shore += "".join(f'<rect x="{x + rng.uniform(4, bw - 8):.0f}" y="{600 - rng.uniform(8, bh):.0f}" width="4" height="4" fill="#F2C35B" opacity=".7"/>' for _ in range(3))
        x += bw + rng.uniform(4, 30)
    water = (f'<rect x="-2600" y="600" width="8000" height="140" fill="{"#5A6E80" if not night else "#232C3C"}"/>'
             + "".join(f'<path d="M{rng.uniform(-2400, 4400):.0f},{rng.uniform(612, 730):.0f} l{rng.uniform(40, 140):.0f},0" stroke="{"#E8C9A0" if not night else "#6C7A92"}" stroke-width="3" opacity=".5" '
                       f'data-drift=\'[{rng.uniform(6, 16):.1f},0,{rng.uniform(.1, .3):.2f},{k}]\'/>' for k in range(40)))
    far = ""
    for k in range(9):                                                 # far tanks across the yard
        fx = -1500 + k * 560 + rng.uniform(-40, 40)
        far += tank_body(fx, 760, 260, 230, seed=seed + 40 + k)
    ground = (f'<rect x="-2600" y="740" width="8000" height="1400" fill="{"#7A7468" if not night else "#3A3834"}"/>'
              + "".join(f'<ellipse cx="{rng.uniform(-2000, 4000):.0f}" cy="{rng.uniform(930, 1300):.0f}" rx="{rng.uniform(40, 160):.0f}" ry="{rng.uniform(6, 14):.0f}" '
                        f'fill="{"#8E8A80" if not night else "#4A4E58"}" opacity=".6"/>' for _ in range(40)))
    tanks = ""
    for k, (tx, num) in enumerate(zip(xs, nums)):
        lv = (levels or {}).get(k)
        tanks += tank_body(tx, 900, 440, 540, num=num, cut=(cut if (cut and k == cut_index) else lv), seed=seed + k)
    for a, b in zip(xs, xs[1:]):                                       # pipes and valves between tanks
        on = flow if (flow and flow[0] == xs.index(a)) else None
        tanks += pipe([(a + 220, 860), (a + 290, 860), (b - 290, 860), (b - 220, 860)], flow=(on[1], on[2]) if on else None)
        tanks += valve((a + b) / 2, 860)
    lamps = "".join(lamp_post(x, 900, 560) for x in (470, 1630, 2790, -690))
    fence = ""
    for x in range(-1800, 4200, 260):
        fence += f'<path d="M{x},1080 L{x},700" stroke="#2E3236" stroke-width="12"/>'
    fence += (f'<path d="M-1800,720 L4200,720 M-1800,1000 L4200,1000" stroke="#2E3236" stroke-width="6"/>'
              + "".join(f'<path d="M{x},720 L{x + 140},1000 M{x + 140},720 L{x},1000" stroke="#4A4F54" stroke-width="2" opacity=".55"/>' for x in range(-1800, 4200, 70)))
    layers = dict(sky=(0.12, back), shore=(0.25, shore), water=(0.3, water), far=(0.45, far), ground=(0.6, ground), tanks=(0.7, tanks + lamps), fence=(1.35, fence))
    return layers, dict(base=900, xs=list(xs), feet=960, top=900 - 540, w=440)


def chain_strip(seed=2):
    """One long world for the receipt's journey, left to right on the z .8 plane: the yard (x 0..900), the
    field-warehouse office (1300..2100), the broker's desk (2500..3300), the bank counter (3700..4500)."""
    out = C.defs() + '<rect x="-1600" y="-900" width="8000" height="2600" fill="#D9D0BC"/>'
    out += '<rect x="-1600" y="900" width="8000" height="900" fill="#8C8270"/>'
    out += '<defs><linearGradient id="cdusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3C4A66"/><stop offset="1" stop-color="#E9AD7A"/></linearGradient></defs>'
    out += '<rect x="-1600" y="-900" width="2600" height="1800" fill="url(#cdusk)"/>' + '<rect x="-1600" y="740" width="2600" height="160" fill="#7A7468"/>'
    out += tank_body(220, 900, 300, 380, num="7", seed=seed) + tank_body(640, 900, 300, 380, num="8", seed=seed + 1)
    out += pipe([(370, 870), (490, 870)])
    # field warehouse office: a hut with a sign, a desk and a filing cabinet
    out += _r(1300, 300, 800, 600, "#C9B48E", sw=4) + _r(1360, 340, 680, 90, "#2E3532", rx=6, sw=3)
    out += _t(1700, 400, "FIELD WAREHOUSE", 44, fill="#F6D58A", family="Sans", weight=600, extra='letter-spacing="5"')
    out += _r(1400, 700, 360, 24, "#6B4429", sw=3) + _r(1420, 724, 40, 176, "#5A3A22", sw=2.4) + _r(1700, 724, 40, 176, "#5A3A22", sw=2.4)
    out += _r(1880, 560, 160, 340, "#8A8F94", sw=3) + "".join(_r(1896, 580 + 80 * k, 128, 64, "#A2A7AB", sw=2) for k in range(4))
    out += _t(1700, 990, "the warehouse company", 34, fill="#3A3024", family="Sans", weight=600)
    # broker's desk: a desk, a phone, a typewriter, a window on the city
    out += _r(2500, 200, 800, 700, "#E6D9BC", sw=4) + _r(2560, 250, 300, 300, "#9DB4BE", sw=4)
    out += "".join(f'<rect x="{2570 + 40 * k}" y="{450 - 30 * (k % 4)}" width="34" height="{100 + 30 * (k % 4)}" fill="#7E878C"/>' for k in range(7))
    out += _r(2580, 700, 640, 24, "#6B4429", sw=3) + _r(2600, 724, 600, 176, "#8A5A36", sw=2.4)
    out += desk_phone(2680, 700) + typewriter(3060, 700)
    out += _t(2900, 990, "the broker", 34, fill="#3A3024", family="Sans", weight=600)
    # bank counter: columns, a counter with a grille
    out += _r(3700, 160, 800, 740, "#EFE7D6", sw=4)
    for k in range(4):
        out += _r(3740 + 200 * k, 200, 60, 500, "#DCD2BE", sw=3)
    out += _r(3700, 160, 800, 60, "#C9BEA6", sw=3) + _t(4100, 205, "BANK", 44, fill="#3A3024", weight=700)
    out += _r(3720, 700, 760, 30, "#6B4429", sw=3) + _r(3740, 730, 720, 170, "#8A5A36", sw=2.4)
    out += "".join(f'<path d="M{3900 + 22 * k},520 L{3900 + 22 * k},700" stroke="#B98A3C" stroke-width="5"/>' for k in range(19) if not 7 <= k <= 11)
    out += _t(4100, 990, "the bank", 34, fill="#3A3024", family="Sans", weight=600)
    return out, dict(stations=[(430, 760), (1580, 680), (2900, 680), (4100, 680)], desk_y=900)


# ------------------------------------------------------------------------------------------------ people

def inspector(dur, x0, x1=None, t_walk=(0, 0), write_at=None, look_up=None, seed=5, scale=1.0, base=960, text=None):
    """An inspector in a raincoat holding a clipboard; walks x0 -> x1 over t_walk, looks up, writes."""
    keys = [[0, C.pose("relaxed", head=-4)]]
    if look_up is not None:
        keys += [[look_up, C.pose("relaxed", head=-4)], [look_up + .5, C.pose("relaxed", head=-26, brow=.6)]]
    if write_at is not None:
        keys += [[write_at - .3, C.pose("read", head=-20)], [write_at, C.pose("sit_write" if False else "read", head=10, elF=70)],
                 [write_at + 1.0, C.pose("read", head=6)]]
    keys.append([dur, keys[-1][1]])
    keys.sort(key=lambda k: k[0])
    pos = [[0, x0, base]] if x1 is None else [[0, x0, base], [t_walk[0], x0, base], [t_walk[1], x1, base, "inout"]]
    return C.actor("insp", "inspector_1963", pos=pos, scale=scale, seed=seed, dir=1 if (x1 or x0) >= x0 else -1, walk=x1 is not None,
                   pose_keys=keys, holdF=clipboard(70, 92, text=text, at=write_at or 0), upright=True)


# ------------------------------------------------------------------------------------------------ shots

def shot_yard_hook(w, h, dur, ctx):
    """Bayonne, 1963: the yard at dusk; the camera travels along the tanks and pushes in on one; an inspector walks
    along the bases with a clipboard; a worker on top of tank 8 waits by the hatch."""
    layers_, anc = tank_farm(night=False)
    t_push = max(1.5, seg_t(ctx, 1, .1) if len(ctx.get("segs") or []) > 1 else dur * .5)
    insp = inspector(dur, -200, 900, t_walk=(.3, min(dur - .5, t_push + 2.5)), seed=5, scale=.86, base=anc["feet"], look_up=min(dur - .8, t_push + 2.6))
    worker = C.actor("w", "worker_1963", pos=[[0, 860, anc["top"] - 28]], scale=.62, seed=8, dir=-1, walk=False,
                     pose_keys=[[0, C.pose("relaxed", head=6)], [dur * .6, C.pose("point", head=-10)], [dur, C.pose("relaxed", head=-4)]])
    layers = [lay(z, s, noblur=(k == "sky")) for k, (z, s) in layers_.items() if k != "fence"]
    layers.insert(5, lay(.7, worker["svg"]))
    layers.append(lay(.72, insp["svg"]))
    layers.append(lay(layers_["fence"][0], layers_["fence"][1]))
    tx = 960 + (760 - 960) / .7
    cam = [[0, -300, 520, 1.0], [t_push, 400, 520, 1.04, "sine"], [dur, tx + 60, 470, 1.32, "inout"]]
    over = [title("Bayonne, New Jersey", "1963", w, h, d=min(3.4, dur - .6)), badge("Reconstruction · not the real yard", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[insp, worker], cam=cam, focus=[[0, .45], [t_push, .7], [dur, .7]], dof=7, shake=.35, over=over, grade="dusk", vig=1.15)
    import sfx
    steps = [t for t in C.footsteps(insp, dur) if t < dur - .3]
    foley = [("step", t, .18, -.2) for t in steps] + [("clank", dur * .6, .12, .3, dict(pitch=170))]
    amb = sfx.yard_ambience(dur + .5, seed=61) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_receipt_chain(w, h, dur, ctx):
    """Our illustration of field warehousing: a receipt is made at the warehouse office for the oil in the tanks, goes
    to the broker, then to the bank; loans come back the other way. The camera follows the paper."""
    world, anc = chain_strip()
    st = anc["stations"]
    n = len(ctx.get("segs") or [1])
    t1 = max(1.2, seg_t(ctx, min(1, n - 1), .1))
    t2 = max(t1 + 1.6, seg_t(ctx, min(2, n - 1), .1))
    t3 = max(t2 + 1.6, min(dur - 3.0, seg_t(ctx, min(3, n - 1), .1)))
    t_back = min(dur - 1.6, t3 + 1.6)
    P = [(x + 150, 655) for x, _ in st]
    rc = (f'<g {C.kv(translate=[[0, P[1][0], P[1][1], -4, .2], [.6, P[1][0], P[1][1], -4, .2], [1.1, P[1][0], P[1][1], -4, 1.0, "out"],
                                [t2 - .9, P[1][0], P[1][1], -4, 1.0], [t2, P[2][0], P[2][1], 3, 1.0, "inout"],
                                [t3 - .9, P[2][0], P[2][1], 3, 1.0], [t3, P[3][0], P[3][1], -2, 1.0, "inout"]],
                     opacity=[[0, 0], [.6, 0], [.8, 1]])}>{warehouse_receipt(180, 115)}</g>')
    money = (f'<g {C.kv(translate=[[0, P[3][0] - 260, 690], [t_back, P[3][0] - 260, 690], [dur, P[3][0] - 1100, 640, "inout"]],
                        opacity=[[0, 0], [t_back - .2, 0], [t_back, 1]])}>{cash_stack(3, 130)}</g>')
    ppl = [C.actor("clerk", "inspector_1963", pos=[[0, 1580, 900]], scale=.95, seed=3, dir=1, walk=False,
                   pose_keys=[[0, C.pose("relaxed")], [.6, C.pose("reach", shF=60, elF=20)], [1.4, C.pose("relaxed", head=-6)], [dur, C.pose("relaxed")]]),
           C.actor("broker", "broker_1963", pos=[[0, 2760, 900]], scale=.95, seed=4, dir=1, walk=False,
                   pose_keys=[[0, C.pose("relaxed")], [t2, C.pose("reach", shF=70, elF=18)], [t2 + .6, C.pose("read", head=8)], [t3 - .6, C.pose("relaxed")], [dur, C.pose("relaxed")]]),
           C.actor("banker", "banker_1963", pos=[[0, 4300, 900]], scale=.95, seed=6, dir=-1, walk=False,
                   pose_keys=[[0, C.pose("relaxed")], [t3, C.pose("reach", shF=70, elF=18)], [t3 + .6, C.pose("read", head=8)], [t_back, C.pose("hold_up")], [dur, C.pose("relaxed")]])]
    z = .8
    aim = lambda px: 960 + (px - 960) / z
    cam = [[0, aim(st[0][0] + 300), 520, 1.12], [.9, aim(st[1][0]), 520, 1.18, "inout"], [t2 - .9, aim(st[1][0] + 60), 520, 1.18, "sine"],
           [t2, aim(st[2][0]), 520, 1.18, "inout"], [t3 - .9, aim(st[2][0] + 60), 520, 1.18, "sine"], [t3, aim(st[3][0]), 520, 1.18, "inout"],
           [dur, aim(st[3][0] - 380), 530, 1.08, "inout"]]
    layers = [lay(z, world), lay(z + .02, "".join(a["svg"] for a in ppl)), lay(z + .04, rc + money)]
    over = [badge("Our illustration · how field warehousing worked", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, z + .04]], dof=3, shake=.25, over=over, grade="warm", tin=("dissolve", .35))
    import sfx
    foley = [("paper", .7, .35, -.2), ("stamp", 1.2, .3, -.2), ("paper", t2 - .1, .3, 0), ("paper", t3 - .1, .3, .2), ("paper", t_back, .3, .3)]
    amb = sfx.office_ambience(dur + .5, seed=62, busy=.5, phones=0) * .55
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_tape_trick(w, h, dur, ctx):
    """As Time described it in 1965: a man climbs on top of a tank, lowers a weighted tape, and calls down that the
    tank is 90% full; the inspector below writes it down. On 'empty' the cutaway opens: there is almost nothing in it."""
    n = len(ctx.get("segs") or [1])
    t_tape = max(1.0, seg_t(ctx, 0, .45))
    t_write = max(t_tape + 1.2, seg_t(ctx, min(1, n - 1), .3))
    t_cut = max(t_write + 1.2, seg_t(ctx, min(2, n - 1), .05))
    cut = dict(at=t_cut, water=[[0, 0]], oil=[[0, .06]], slick=0, tape=(t_tape, t_tape + 1.2, .95))
    layers_, anc = tank_farm(night=False, cut=cut, cut_index=1, seed=4)
    worker = C.actor("w", "worker_1963", pos=[[0, 700, anc["top"] - 28]], scale=.66, seed=8, dir=1, walk=False,
                     pose_keys=[[0, C.pose("relaxed")], [t_tape - .2, C.pose("reach", shF=40, elF=10, head=20)], [t_tape + 1.3, C.pose("reach", shF=40, elF=10, head=24)],
                                [t_tape + 1.6, C.pose("talk_a", head=30, mouth=2)], [t_write, C.pose("point", head=30)], [dur, C.pose("relaxed", head=20)]])
    insp = inspector(dur, 1080, base=anc["feet"] - 40, write_at=t_write, look_up=t_tape + 1.4, seed=6, scale=.9, text="90%")
    layers = [lay(z, s, noblur=(k == "sky")) for k, (z, s) in layers_.items() if k not in ("fence", "shore")]
    layers.insert(4, lay(.7, worker["svg"] + kt(_t(760, 640, "almost empty", 52, fill="#F4F1EA", family="Sans", weight=700, extra='letter-spacing="3"'), None, t_cut + .7)))
    layers.append(lay(.72, insp["svg"]))
    tx = 960 + (760 - 960) / .7
    cam = [[0, tx, 330, 1.5], [t_tape + 1.2, tx + 20, 360, 1.55, "sine"], [t_write - .3, tx + 200, 640, 1.7, "inout"], [t_cut - .2, tx, 520, 1.22, "inout"], [dur, tx, 520, 1.28, "sine"]]
    over = [badge("Reconstruction · as Time described it in 1965", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[worker, insp], cam=cam, focus=[[0, .7]], dof=5, shake=.3, over=over, grade="dusk", tin=("dissolve", .35))
    import sfx
    foley = [("clank", t_tape - .1, .2, -.1, dict(pitch=200)), ("marker", t_write, .18, .3, dict(sec=.7)), ("hit", t_cut + .3, .35, 0, dict(pitch=131))]
    amb = sfx.yard_ambience(dur + .5, seed=63, horn=False) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_slick(w, h, dur, ctx):
    """A tank of water topped by a thin slick of oil: the cutaway fills with water, then the gold slick settles on top;
    the camera rises to the hatch, where only the gold shows."""
    n = len(ctx.get("segs") or [1])
    t_w = max(.8, seg_t(ctx, 0, .3))
    t_o = max(t_w + 1.6, seg_t(ctx, 0, .75))
    t_up = max(t_o + 1.2, seg_t(ctx, min(1, n - 1), .1))
    cut = dict(at=.3, water=[[0, 0], [t_w, 0], [t_w + 1.4, .93]], oil=[[0, .93]], oil_at=t_o, slick=16)
    layers_, anc = tank_farm(night=False, cut=cut, cut_index=1, seed=5)
    tx = 960 + (760 - 960) / .7
    pill = lambda x, y, wd: f'<rect x="{x - wd / 2}" y="{y - 46}" width="{wd}" height="62" rx="10" fill="#1E1A16" opacity=".75"/>'
    labels = (kt(_t(760, 700, "WATER", 54, fill="#F4F1EA", family="Sans", weight=700, extra='letter-spacing="6"'), None, t_w + 1.0)
              + kt(pill(760, 262, 400) + _t(760, 262, "a thin slick of oil", 40, fill=OIL, family="Serif", weight=700), None, t_o + .4))
    layers = [lay(z, s, noblur=(k == "sky")) for k, (z, s) in layers_.items() if k not in ("fence",)]
    layers.append(lay(.7, labels))
    cam = [[0, tx, 520, 1.2], [t_o, tx, 500, 1.3, "inout"], [t_up, tx, 400, 1.42, "inout"], [dur, tx, 330, 1.7, "inout"]]
    over = [badge("Reconstruction · Time, 1965: water, topped by a thin slick of oil", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[], cam=cam, focus=[[0, .7]], dof=5, shake=.25, over=over, grade="dusk", tin=("dissolve", .35))
    import sfx
    foley = [("pump", t_w, .25, 0, dict(sec=1.5)), ("hit", t_o + .2, .3, 0, dict(pitch=196))]
    amb = sfx.yard_ambience(dur + .5, seed=64, horn=False) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_pipes_night(w, h, dur, ctx):
    """A weekend night: the yard is dark and lightly guarded; a pump sends oil along the pipe from tank 8 into tank 9,
    whose level rises as 8's falls, so the same oil can be counted again; a clipboard tick on each."""
    n = len(ctx.get("segs") or [1])
    t_f = max(1.0, seg_t(ctx, 0, .4))
    t_e = min(dur - 1.2, t_f + 3.0)
    lv = {1: dict(at=.2, water=[[0, 0]], oil=[[0, .8], [t_f + .6, .8], [t_e, .1]], slick=0),
          2: dict(at=.2, water=[[0, 0]], oil=[[0, .1], [t_f + .6, .1], [t_e, .8]], slick=0)}
    layers_, anc = tank_farm(night=True, cut=None, levels=lv, flow=(1, t_f, t_e), seed=6)
    xs = anc["xs"]
    men = [C.actor(f"m{k}", ("worker_1963", "worker_1963b")[k], pos=[[0, (300, 1610)[k], anc["feet"] - 30]], scale=.82, seed=20 + k, dir=1 if k else -1, walk=False,
                   pose_keys=[[0, C.pose("relaxed", head=-6)], [t_f - .3, C.pose("reach", shF=50, elF=20)], [t_f + .4, C.pose("relaxed", head=-12)], [dur, C.pose("concern" if k else "relaxed", head=-8)]])
           for k in range(2)]
    tags = (kt(_t(xs[1], 270, "counted", 40, fill="#F4F1EA", family="Sans", weight=600), None, .6)
            + kt(_t(xs[2], 270, "counted again", 40, fill=OIL, family="Sans", weight=700), None, t_e + .2))
    layers = [lay(z, s, noblur=(k == "sky")) for k, (z, s) in layers_.items() if k != "fence"]
    layers.append(lay(.72, "".join(a["svg"] for a in men) + tags))
    layers.append(lay(layers_["fence"][0], layers_["fence"][1]))
    mx = 960 + ((xs[1] + xs[2]) / 2 - 960) / .7
    cam = [[0, mx - 120, 520, 1.0], [t_f, mx, 520, 1.06, "sine"], [dur, mx + 40, 500, 1.12, "sine"]]
    over = [title("Bayonne", "A weekend night", w, h, d=min(2.8, dur - .6)), badge("Reconstruction · as Time described it in 1965", w, h)]
    shot = dict(dur=dur, layers=layers, actors=men, cam=cam, focus=[[0, .7]], dof=5, shake=.3, over=over, grade="cool", vig=1.3, tin=("dissolve", .35))
    import sfx
    foley = [("clank", t_f - .2, .25, -.2, dict(pitch=150)), ("pump", t_f, .3, 0, dict(sec=t_e - t_f)), ("hit", t_e + .2, .3, .3, dict(pitch=196))]
    amb = sfx.yard_ambience(dur + .5, seed=65, wind=.7, horn=False) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def _room(head, sub, rows, dur, react_at, mood, ring, phones, cam, ttl, bdg, grade="warm", seed=5, tin=("cut", 0), w=1920, h=1080):
    layers_, anc = dealing_room(head=head, sub=sub, rows=rows, ring=ring, lifts=[], seed=seed)
    tr = traders(anc, dur, react_at=react_at, mood=mood, phones=phones, seed=seed + 60)
    layers = [lay(z, s, noblur=(k == "light")) for k, (z, s) in layers_.items() if k != "desks"]
    layers.append(lay(.74, "".join(a["svg"] for a in tr)))
    layers.append(lay(.78, layers_["desks"][1]))
    fg = (_r(-700, 1010, 1000, 40, "#C9BBA0", rx=4, sw=3.4) + _r(-690, 1050, 980, 300, "#A8987C", sw=3) + desk_phone(140, 1010, color="#3B2F27")
          + _r(1720, 1030, 1000, 40, "#C9BBA0", rx=4, sw=3.4) + _r(1730, 1070, 980, 300, "#A8987C", sw=3) + typewriter(1880, 1030))
    layers.append(lay(1.18, fg))
    over = ([title(*ttl, w=w, h=h, d=min(3.0, dur - .6))] if ttl else []) + [badge(bdg, w, h)]
    return dict(dur=dur, layers=layers, actors=tr, cam=cam, focus=[[0, .74], [dur, .7]], dof=6, shake=.35, over=over, grade=grade, tin=tin)


def shot_margin_calls(w, h, dur, ctx):
    """Mid November 1963: phones ring across the room; the board counts the margin calls to $19,000,000 (Time,
    29 Nov 1963) as the figure is said."""
    n = len(ctx.get("segs") or [1])
    t0 = max(1.0, word_t(ctx, n - 1, "nineteen") - .6)
    t1 = min(dur - .8, t0 + 1.8)
    rows = [("MARGIN CALLS", [[0, 0], [t0, 0], [t1, 19000000, "out"]], 0, "$", "", "#F6D58A")]
    ring = [(k % 7, .3 + .5 * k) for k in range(int(dur / .5))]
    cam = [[0, 760, 450, 1.0], [t0, 960, 440, 1.06, "inout"], [dur, 990, 430, 1.1, "sine"]]
    shot = _room("VEGETABLE OIL FUTURES", "NOVEMBER 1963", rows, dur, t1, "concern", ring, (0, 2, 4), cam, ("New York", "November 1963"),
                 "Reconstruction · figure from Time, 29 November 1963", grade="cool", seed=9, tin=("dissolve", .35), w=w, h=h)
    import sfx
    foley = [("ring", t, .12, (-.6, .6)[k % 2], dict(sec=.5)) for k, (_, t) in enumerate(ring[::3])] + [("flap", t0, .4, 0), ("hit", t1, .45, 0, dict(pitch=147))]
    amb = sfx.office_ambience(dur + .5, seed=66, busy=1.6, phones=1.5) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_exchange_close(w, h, dur, ctx):
    """Friday 22 November 1963: on the stock exchange board the Dow's change for the day counts down to -2.9%; then
    CLOSED 2:07 P.M. drops across the board; the room goes still."""
    n = len(ctx.get("segs") or [1])
    t_close = max(1.2, word_t(ctx, min(1, n - 1), "two oh seven") if n > 1 else dur * .4)
    t_dow = max(t_close + .8, min(dur - 1.0, seg_t(ctx, min(2, n - 1), .4)))
    rows = [("DOW, NOV 22", [[0, 0], [t_dow - .8, 0], [t_dow, -2.9, "out"]], 1, "", "%", "#F6D58A")]
    cam = [[0, 900, 450, 1.0], [t_close - .3, 960, 440, 1.06, "inout"], [dur, 970, 430, 1.1, "sine"]]
    shot = _room("NEW YORK STOCK EXCHANGE", "FRIDAY, NOVEMBER 22, 1963", rows, dur, t_close, "concern", [], (1,), cam, None,
                 "Reconstruction · times and figure from InvestmentNews", grade="cool", seed=13, tin=("dissolve", .35), w=w, h=h)
    by = 540 + (260 - 540) / .38
    closed = (f'<g {C.kv(translate=[[0, 960, -300, -4], [t_close, 960, -300, -4], [t_close + .45, 960, 500, -3, "out"]])}>'
              + _r(-360, -60, 720, 120, RED, rx=8, sw=4) + _t(0, 22, "CLOSED 2:07 P.M.", 62, fill="#F7F5F2", family="Sans", weight=700, extra='letter-spacing="4"') + "</g>")
    shot["layers"].insert(1, lay(.38, closed))
    import sfx
    foley = [("ring", .4, .1, -.5, dict(sec=.6)), ("stamp", t_close + .45, .35, 0), ("flap", .6, .3, 0), ("hit", t_dow, .35, 0, dict(pitch=131))]
    amb = sfx.office_ambience(dur + .5, seed=67, busy=1.0, phones=.3) * .6
    return dict(shots=[shot], foley=foley, amb=amb)


SHOTS = dict(yard_hook=shot_yard_hook, receipt_chain=shot_receipt_chain, tape_trick=shot_tape_trick, slick=shot_slick,
             pipes_night=shot_pipes_night, margin_calls=shot_margin_calls, exchange_close=shot_exchange_close)
