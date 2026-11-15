"""
Filmed beats for YouTube #9, Charles Ponzi and the reply coupon (15 Nov 2026). Sets, props and shots for
build/cine.py, used by build/youtube_ep009.py as kind="cine" beats (cinematic-standard.md section 8, step 3: sets;
and the 14 Nov next improvement: quotes filmed as documents, cine_lib.document_shot).

Sets (our own generic drawings; no real building, interior, design or person is copied; everything is badged):
  boston_street_1920()  a Boston street of 1920: brick and stone office blocks, a corner sign SCHOOL ST., an office
                        door with a painted banner, lamp posts
  office_1920()         a 1920 office: plaster walls, tall windows with light, a wall clock, a long wooden counter
                        with brass grilles (three windows), a big safe; clerks behind, the public in front
  post_counters()       two post-office counters (Spain on the left, Boston on the right) with the sea between them
                        and a steamer crossing, for the coupon trade
Props: reply_coupon() (a generic coupon, not the real design), stamp_5c(), cash_stack(), promissory_note().
1920 looks (cine.LOOKS): boater_1920, boater_1920b, clerk_1920, clerk_1920b, lady_1920, lady_1920b, worker_1920.

Shots (fn(w, h, dur, ctx) -> dict(shots, foley, amb); ctx["segs"] are the beat's sentences, (text, start, end)):
  street_queue   the hook: School Street, July 1920, a line along the street to the office door
  mail_coupon    August 1919: a man at a desk opens a letter from Spain and holds up a reply coupon
  coupon_trade   the trade: 30 centavos for a coupon in Spain; across the sea; swapped for a 5-cent stamp in Boston
  office_cash    the counter: people hand in money, the clerks' stacks grow, the board counts to about $1,000,000 a week
  jars           new money into one jar, paid out of it to earlier lenders; the investments jar stays empty
  coupon_pile    our calculation: coupons pile up while the counter runs to 95,840,000
  run            late July: the crowd at the counter wants its money; the stacks go out over the counter
Facts on screen come only from the sources in youtube_ep009.py's docstring. Nobody in a shot speaks, and nobody
is drawn as a likeness: the man at the desk is "our illustration", not a portrait.
"""

import math
import pathlib
import random
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402
from cine_1907 import lay, badge, seg_t, word_t, lamps   # noqa: E402
from cine_1907 import title as _title_1907   # noqa: E402
from cine_1971 import kt     # noqa: E402

INK, RED, TEAL, MUSTARD, PAPER = C.INK, C.RED, C.TEAL, C.MUSTARD, "#F7F5F2"
_r, _t = L._r, L._t
LOOKS_PUBLIC = ["boater_1920", "lady_1920", "worker_1920", "boater_1920b", "lady_1920b", "clerk_1920b", "boater_1920", "lady_1920"]


def title(k, h_, w, h, at=.3, d=3.4):
    """The 1907 place-and-date title, raised so a two-line caption never sits on it (15 Nov: #9's first stills)."""
    s_ = min(w, h) / 1080
    return _title_1907(k, h_, w, h, at, d).replace(f"bottom:{int(170 * s_)}px", f"bottom:{int(250 * s_)}px")


# ------------------------------------------------------------------------------------------------ props

def reply_coupon(w=150, h=96, text="REPLY COUPON"):
    """A generic international reply coupon (our design: a pale card with a frame and a big blank seal)."""
    return (_r(-w / 2, -h / 2, w, h, "#E9EEDC", rx=4, sw=2.6)
            + f'<rect x="{-w / 2 + 8}" y="{-h / 2 + 8}" width="{w - 16}" height="{h - 16}" fill="none" stroke="#5E7A5A" stroke-width="2" stroke-dasharray="4 3"/>'
            + f'<circle cx="{-w / 2 + w * .2:.0f}" cy="2" r="{h * .2:.0f}" fill="#C9D6B8" stroke="#5E7A5A" stroke-width="2.4"/>'
            + _t(w * .14, -h * .06, text.split()[0], int(h * .17), fill="#3E5A3A", weight=600, family="Sans")
            + _t(w * .14, h * .2, " ".join(text.split()[1:]), int(h * .17), fill="#3E5A3A", weight=600, family="Sans"))


def stamp_5c(s=1.0):
    """A generic postage stamp with perforations and 5¢ (no real stamp's design)."""
    w, h = 90 * s, 110 * s
    perf = "".join(f'<circle cx="{-w / 2 + k * w / 8:.1f}" cy="{-h / 2}" r="{4 * s:.1f}" fill="#F7F5F2"/><circle cx="{-w / 2 + k * w / 8:.1f}" cy="{h / 2}" r="{4 * s:.1f}" fill="#F7F5F2"/>' for k in range(9))
    perf += "".join(f'<circle cx="{-w / 2}" cy="{-h / 2 + k * h / 10:.1f}" r="{4 * s:.1f}" fill="#F7F5F2"/><circle cx="{w / 2}" cy="{-h / 2 + k * h / 10:.1f}" r="{4 * s:.1f}" fill="#F7F5F2"/>' for k in range(11))
    return (_r(-w / 2, -h / 2, w, h, "#2E5670", sw=2.4) + _r(-w / 2 + 10 * s, -h / 2 + 10 * s, w - 20 * s, h - 20 * s, "#F1E6CF", sw=1.6)
            + _t(0, 18 * s, "5¢", int(44 * s), fill="#2E5670") + perf)


def cash_stack(n=4, w=120):
    """A pile of banded notes, generic green paper."""
    return "".join(f'<g transform="translate({(k % 2) * 6},{-k * 16})">' + _r(-w / 2, -14, w, 14, "#8FB08A", rx=2, sw=2)
                   + f'<rect x="-10" y="-14" width="20" height="14" fill="#E9DFC8" stroke="{INK}" stroke-width="1.5"/></g>' for k in range(n))


def promissory_note(w=170, h=110):
    """A generic note: a title (only when big enough to read), greeked lines, a red seal."""
    big = w >= 140
    out = _r(-w / 2, -h / 2, w, h, "#F3E7CF", rx=3, sw=2.4)
    if big:
        out += _t(0, -h / 2 + 30, "NOTE", 22, fill=INK)
    y0, dy, lh = (-h / 2 + 46, 16, 6) if big else (-h / 2 + h * .22, h * .18, 4)
    out += "".join(f'<rect x="{-w / 2 + 12}" y="{y0 + dy * k:.0f}" width="{w - 24 - w * .2 * (k == 2):.0f}" height="{lh}" rx="2" fill="#B9AE9A"/>' for k in range(3))
    return out + f'<circle cx="{w / 2 - w * .14:.0f}" cy="{h / 2 - h * .2:.0f}" r="{max(5, w / 14):.0f}" fill="{RED}" stroke="{INK}" stroke-width="2"/>'


# ------------------------------------------------------------------------------------------------ sets

def boston_street_1920(seed=9, banner="THE SECURITIES EXCHANGE COMPANY"):
    """Layers and anchors for a Boston street, 1920. The office door is centred at x 960 on the z .55 layer."""
    rng = random.Random(seed)
    sky = (C.defs() + '<defs><linearGradient id="skyB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B8CBD3"/>'
           '<stop offset=".6" stop-color="#E3E4DA"/><stop offset="1" stop-color="#F0E8D6"/></linearGradient></defs>'
           '<rect x="-3000" y="-1200" width="9000" height="2600" fill="url(#skyB)"/>')
    for i in range(5):
        cx, cy = rng.uniform(-1500, 3500), rng.uniform(40, 240)
        sky += (f'<g data-drift=\'[{rng.uniform(5, 10):.1f},0,0]\'><ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rng.uniform(180, 320):.0f}" '
                f'ry="{rng.uniform(26, 44):.0f}" fill="#F6F3EC" opacity=".6"/></g>')
    far = ""
    xs = -1800
    while xs < 4200:
        bw, top = rng.uniform(200, 340), rng.uniform(140, 380)
        col = rng.choice(["#B9A08A", "#A99584", "#C4B49E", "#9E8E80"])
        far += f'<rect x="{xs:.0f}" y="{top:.0f}" width="{bw:.0f}" height="{900 - top:.0f}" fill="{col}"/>'
        for r in range(int((820 - top) / 50)):
            for c in range(int(bw / 40)):
                if rng.random() < .75:
                    far += f'<rect x="{xs + 12 + c * 40:.0f}" y="{top + 20 + r * 50:.0f}" width="18" height="26" fill="#6E7880" opacity=".5"/>'
        xs += bw + rng.uniform(10, 40)
    fronts = ""
    for x, w_, col, top in ((-1300, 620, "#A85A3C", 210), (-650, 600, "#C9B08C", 170), (1530, 600, "#8E4B35", 190), (2160, 640, "#BFA27E", 240)):
        fronts += L._front(x, w_, top, 900, col, floors=4, cols=3, lit=(), door=(1, "#2A2522"), seed=int(x) % 97,
                           brick=col in ("#A85A3C", "#8E4B35"))
    # the office block: brick, many windows, a stone ground floor with the door at x 960
    ox, ow = -40, 1560
    fronts += _r(ox, 40, ow, 860, "#9C4E36", sw=3.6)
    for r in range(5):
        for c in range(9):
            fronts += L._window(ox + 70 + c * 166, 80 + r * 92, 70, 66, lit=False, seed=r * 9 + c, glazing=(2, 2))
    fronts += _r(ox, 520, ow, 380, "#D9CFBC", sw=3.4) + _r(ox - 20, 506, ow + 40, 26, "#C4B9A4", sw=3)
    for k in range(6):
        cx = ox + 120 + k * 264
        if abs(cx - 960) > 200:
            fronts += _r(cx - 70, 600, 140, 200, "#38424A", sw=3) + f'<rect x="{cx - 62}" y="608" width="124" height="184" fill="#7E95A2" opacity=".45"/>'
    dx = 960
    fronts += _r(dx - 110, 580, 220, 300, "#3B2A20", sw=3.4) + f'<rect x="{dx - 96}" y="594" width="192" height="286" fill="#F2D394" opacity=".8"/>'
    fronts += _r(dx - 150, 556, 300, 30, "#C4B9A4", sw=2.6)
    # the painted banner over the door (wording from the company's name in the sources)
    fronts += _r(dx - 520, 452, 1040, 64, PAPER, rx=6, sw=3) + _t(dx, 496, banner, 34, fill=INK, extra='letter-spacing="5"')
    for k in range(3):
        fronts += _r(dx - 200 - 16 * k, 880 + 8 * k, 400 + 32 * k, 10, "#CFC6B5", sw=2)
    # a corner street sign on a post (the street from the sources)
    fronts += (f'<rect x="1478" y="560" width="14" height="340" fill="#1E1A18"/>' + _r(1380, 540, 210, 48, "#1F3A2E", rx=4, sw=3)
               + _t(1485, 574, "SCHOOL ST.", 26, fill="#F7F5F2", family="Sans", weight=600, extra='letter-spacing="3"'))
    fronts += f'<rect x="-2000" y="880" width="6000" height="40" fill="#B9B2A3" stroke="{INK}" stroke-width="3"/>'
    street = (f'<rect x="-2600" y="900" width="7200" height="420" fill="#8E8778"/>'
              f'<rect x="-2600" y="900" width="7200" height="22" fill="#B7AE9C" stroke="{INK}" stroke-width="3"/>'
              + "".join(f'<path d="M{x},922 L{x - 140},1320" stroke="#7A7366" stroke-width="3" opacity=".5"/>' for x in range(-2400, 4600, 220)))
    layers = dict(sky=(0.03, sky), far=(0.18, far), fronts=(0.55, fronts), street=(0.8, street))
    return layers, dict(ground_back=935, ground_main=1010, door_x=dx)


def office_1920(board=None, seed=5, dusk=False, cal=("AUG", "1919")):
    """A 1920 office with a long counter. Returns (layers, anchors). board: SVG drawn on the wall board (x 640..1280,
    y 120..330 on the wall layer). The counter top is at y 800 (z .8); clerks stand behind it at y 960 (z .66); the
    public stands in front at y 1040 (z .9)."""
    rng = random.Random(seed)
    wall = C.defs() + f'<rect x="-1600" y="-900" width="5200" height="2600" fill="{"#CDBE9E" if dusk else "#E6D9BC"}"/>'
    wall += f'<rect x="-1600" y="600" width="5200" height="320" fill="#8A6A48" stroke="{INK}" stroke-width="3"/>'
    for x in range(-1600, 3600, 180):
        wall += f'<path d="M{x},600 L{x},920" stroke="#6E5236" stroke-width="3"/>'
    for wx in (-560, 1660, 2300):
        wall += _r(wx, 40, 300, 480, "#9DB4BE" if not dusk else "#3E4A5E", sw=4) + f'<path d="M{wx + 150},40 L{wx + 150},520 M{wx},280 L{wx + 300},280" stroke="{INK}" stroke-width="5"/>'
        if not dusk:
            wall += C.shaft(wx + 20, 60, 260, 900, angle=-16, op=.22)
    wall += (f'<g transform="translate(380,170)"><circle r="62" fill="#F7F1E4" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M0,0 L0,-40 M0,0 L28,10" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>')
    if board is not None:
        wall += f'<g transform="translate(0,120)">' + _r(640, 120, 640, 210, "#24302A", rx=8, sw=4) + board + "</g>"
    else:                                                               # a wall calendar for the month in the title
        wall += f'<g transform="translate(-330,230)">' + (_r(860, 110, 200, 240, PAPER, rx=4, sw=3) + _r(860, 110, 200, 60, RED, rx=4, sw=3)
                 + _t(960, 152, cal[0], 30, fill="#F7F5F2", family="Sans", weight=600, extra='letter-spacing="3"')
                 + _t(960, 250, cal[1], 64, fill=INK) + "".join(f'<rect x="{880 + 32 * (k % 5)}" y="{280 + 18 * (k // 5)}" width="22" height="8" fill="#CFC6B6"/>' for k in range(10))) + "</g>"
    safe = (_r(-200, 380, 300, 420, "#3E4A46", rx=10, sw=4) + f'<circle cx="-50" cy="560" r="46" fill="#55625D" stroke="{INK}" stroke-width="4"/>'
            + f'<g data-swing=\'[3,0.5,0,-50,560]\'><path d="M-50,560 L-50,524" stroke="#E2C27A" stroke-width="6"/></g>')
    wall += safe + C.motes(-600, 100, 3200, 700, n=34, op=.5, spd=4, seed=seed)
    clerks_floor = f'<rect x="-1600" y="900" width="5200" height="700" fill="#7A5236"/>'
    counter = (_r(-700, 790, 3320, 26, "#6B4429", rx=3, sw=3.4) + _r(-680, 816, 3280, 300, "#8A5A36", sw=3)
               + "".join(_r(x, 840, 150, 240, "#7A4E2F", sw=2.4) for x in range(-640, 2600, 210)))
    grilles = ""
    for gx in (520, 960, 1400):                                         # three windows with brass bars
        grilles += _r(gx - 170, 470, 340, 24, "#B98A3C", sw=3) + "".join(
            f'<path d="M{gx - 160 + 24 * k},494 L{gx - 160 + 24 * k},790" stroke="#B98A3C" stroke-width="5"/>' for k in range(14) if not (5 <= k <= 8))
        grilles += _r(gx - 60, 700, 120, 90, "none", sw=3)
    floor = f'<rect x="-1600" y="1000" width="5200" height="700" fill="#9C7A55"/>' + "".join(
        f'<path d="M{x},1000 L{x - 260},1700" stroke="#86664A" stroke-width="3"/>' for x in range(-1600, 3600, 200))
    layers = dict(wall=(0.42, wall), clerks_floor=(0.6, clerks_floor), counter=(0.8, counter), grilles=(0.8, grilles), floor=(0.9, floor))
    return layers, dict(counter_y=790, clerk_y=960, public_y=1060, windows=(520, 960, 1400))


def post_counter(x0, sign, wall_col, seed=0):
    """One post-office counter (world x0 .. x0 + 1500)."""
    s = f'<rect x="{x0}" y="-900" width="1500" height="2600" fill="{wall_col}"/>'
    s += _r(x0 + 300, 120, 900, 90, "#2E3532", rx=6, sw=3) + _t(x0 + 750, 180, sign, 40, fill="#F6D58A", family="Sans", weight=600, extra='letter-spacing="5"')
    s += _r(x0 + 120, 760, 1260, 30, "#6B4429", sw=3.4) + _r(x0 + 140, 790, 1220, 400, "#8A5A36", sw=3)
    s += _r(x0 + 520, 420, 460, 24, "#B98A3C", sw=3) + "".join(
        f'<path d="M{x0 + 530 + 30 * k},444 L{x0 + 530 + 30 * k},760" stroke="#B98A3C" stroke-width="5"/>' for k in range(16) if not (5 <= k <= 10))
    for k in range(4):                                                  # pigeonholes
        s += _r(x0 + 1080 + 0 * k, 260 + 40 * k, 220, 40, "#C9B48E", sw=2)
    return s


# ------------------------------------------------------------------------------------------------ people

def queue_people(anc, dur, n=11, arrivals=3, seed=11):
    """A line along the pavement to the office door (facing it), people hurrying to join, passers-by behind."""
    rng = random.Random(seed)
    q = []
    for i in range(n):
        x = anc["door_x"] - 150 - i * 96
        keys = [[0, C.pose("relaxed", head=rng.uniform(-6, 6))], [dur * .5, C.pose("relaxed" if i % 3 else "hold_up", head=rng.uniform(-8, 8))],
                [dur, C.pose("relaxed", head=rng.uniform(-6, 6))]]
        q.append(C.actor(f"q{i}", LOOKS_PUBLIC[i % len(LOOKS_PUBLIC)], pos=[[0, x, anc["ground_main"] - 4 + (i % 2) * 6]], scale=.82, seed=seed + i,
                         dir=1, walk=False, pose_keys=keys, holdF=promissory_note(70, 46) if i % 3 == 0 else "", upright=True))
    walkers = []
    for j in range(arrivals):
        end_x = anc["door_x"] - 150 - (n + j) * 96
        start = end_x - rng.uniform(700, 1000)
        t_arrive = min(dur - .4, rng.uniform(1.8, dur * .8))
        walkers.append(C.actor(f"w{j}", LOOKS_PUBLIC[(j * 3 + 1) % len(LOOKS_PUBLIC)], pos=[[0, start, anc["ground_main"] + 4], [t_arrive, end_x, anc["ground_main"] + 4, "out"]],
                               scale=.84, seed=seed + 30 + j, dir=1, amp=24))
    bsvg, back = L.crowd(6, (-900, 2700), anc["ground_back"], .55, z_seed=seed, dur=dur + 1, talkers=1, prefix="b", looks=LOOKS_PUBLIC)
    return q, walkers, (bsvg, back)


def public_at_counter(anc, dur, react_at=None, mood="hold_up", n=7, seed=21, hold=None, prefix="p", gap=190, x0=300):
    """People in front of the counter, backs to the camera's left side, facing the windows."""
    rng = random.Random(seed)
    out = []
    for i in range(n):
        x = x0 + i * gap + rng.uniform(-20, 20)
        keys = [[0, C.pose("relaxed", head=rng.uniform(-6, 6))]]
        if react_at is not None:
            keys += [[react_at + .12 * i, C.pose("relaxed")], [react_at + .4 + .12 * i, C.pose(mood if i % 2 == 0 else "reach", brow=-1 if mood == "concern" else .5, head=-10)],
                     [dur, C.pose(mood if i % 2 == 0 else "concern", head=-6)]]
        out.append(C.actor(f"{prefix}{i}", LOOKS_PUBLIC[(i + seed) % len(LOOKS_PUBLIC)], pos=[[0, x, anc["public_y"] + (i % 2) * 10]], scale=1.0, seed=seed + i,
                           dir=1 if i % 2 else -1, walk=False, pose_keys=keys, holdF=hold if hold and i % 2 == 0 else "", upright=True))
    return out


def clerks(anc, dur, act_at=(), n=3, seed=41, prefix="k"):
    """One clerk behind each window; act_at: times they reach across the counter (alternating)."""
    out = []
    for i, wx in enumerate(anc["windows"][:n]):
        keys = [[0, C.pose("relaxed", head=-4)]]
        for k, t in enumerate(act_at):
            if k % n == i:
                keys += [[t - .3, C.pose("relaxed")], [t, C.pose("reach", shF=70, elF=14)], [t + .5, C.pose("relaxed", head=4)]]
        keys.append([dur, C.pose("relaxed", head=-2)])
        keys.sort(key=lambda k: k[0])
        out.append(C.actor(f"{prefix}{i}", ("clerk_1920", "clerk_1920b", "clerk_1920")[i], pos=[[0, wx, anc["clerk_y"]]], scale=.86, seed=seed + i,
                           dir=-1 if i == 2 else 1, walk=False, pose_keys=keys))
    return out


# ------------------------------------------------------------------------------------------------ shots

def shot_street_queue(w, h, dur, ctx):
    """School Street, July 1920: the line along the pavement to the office; latecomers hurry to join it."""
    layers_, anc = boston_street_1920()
    q, walkers, (bsvg, back) = queue_people(anc, dur)
    layers = [lay(z, s, noblur=(k == "sky")) for k, (z, s) in layers_.items()]
    layers.insert(3, lay(.5, bsvg))
    layers.append(lay(.8, "".join(a["svg"] for a in q + walkers)))
    layers.append(lay(1.3, lamps()))
    t_line = max(1.5, seg_t(ctx, 1, .2))
    bx = 960 + (960 - 960) / .55
    cam = [[0, bx + 120, 610, 1.18], [max(1.0, t_line - .8), bx, 640, 1.1, "sine"], [dur, -60, 660, 1.0, "inout"]]
    over = [title("Boston", "July 1920", w, h, d=min(3.4, dur - .6)), badge("Reconstruction", w, h)]
    shot = dict(dur=dur, layers=layers, actors=q + walkers + back, cam=cam, focus=[[0, .55], [t_line, .8], [dur, .8]], dof=8, shake=.4, over=over, grade="warm")
    import sfx
    steps = sorted(set(sum((C.footsteps(a, dur) for a in walkers[:2]), [])))
    foley = [("step", t, .3, (-.3, .3)[i % 2]) for i, t in enumerate(steps) if t < dur - .3]
    amb = sfx.street_ambience(dur + .5, seed=15, crowd=1.6)
    return dict(shots=[shot], foley=foley, amb=amb * .55)


def shot_mail_coupon(w, h, dur, ctx):
    """August 1919: a man at a desk opens a letter from Spain; a reply coupon is inside; he holds it up to look."""
    layers_, anc = office_1920(dusk=True)
    t_open = max(1.2, seg_t(ctx, 0, .45))
    t_hold = min(dur - 1.0, max(t_open + 1.4, word_t(ctx, 1, "coupon")))
    desk = (_r(560, 860, 820, 30, "#6B4429", sw=3.4) + _r(600, 890, 60, 210, "#5A3A22", sw=3) + _r(1280, 890, 60, 210, "#5A3A22", sw=3)
            + f'<g transform="translate(1180,860)">{L.candle(False) if False else ""}</g>'
            + f'<g transform="translate(1250,858)"><path d="M0,0 L-30,-130 L30,-130 Z" fill="none" stroke="{INK}" stroke-width="5"/>'
              f'<path d="M-60,-130 L60,-130 L30,-190 L-30,-190 Z" fill="#2F5A3E" stroke="{INK}" stroke-width="4"/></g>'
            + f'<circle cx="1250" cy="-60" r="1" fill="none"/>'
            + f'<circle cx="1250" cy="700" r="420" fill="url(#glowWarm)" opacity=".55" data-flick=\'[0.55,0.03,5]\'/>')
    env = (f'<g {C.kv(opacity=[[0, 1], [t_open + .3, 1], [t_open + .6, .35]])} transform="translate(960,846)">'
           + _r(-90, -50, 180, 100, "#F1E6CF", rx=3, sw=2.4) + f'<path d="M-90,-50 L0,8 L90,-50" fill="none" stroke="{INK}" stroke-width="2.4"/>'
           + _t(30, 30, "ESPAÑA", 16, fill="#6A5F50", family="Sans", weight=600) + "</g>")
    coup = f'<g {C.kv(opacity=[[0, 0], [t_hold - .4, 0], [t_hold - .1, 1]])}>{reply_coupon(110, 70)}</g>'
    man = C.actor("man", "clerk_1920b", pos=[[0, 780, 1010]], scale=1.25, seed=7, dir=1, walk=False, holdF=coup, upright=True,
                  pose_keys=[[0, C.pose("sit_read", head=10)], [t_open, C.pose("sit_read", head=14)], [t_open + .5, C.pose("sit_write", head=14)],
                             [t_hold - .2, C.pose("seated", shF=10, elF=60, head=6)],
                             [t_hold + .4, C.pose("seated", shF=110, elF=34, head=-10, brow=1, mouth=1)],
                             [dur, C.pose("seated", shF=112, elF=30, head=-6, brow=.6)]])
    chair = _r(640, 900, 150, 24, "#5A3A22", sw=3) + _r(640, 760, 22, 340, "#5A3A22", sw=3)
    layers = [lay(.42, layers_["wall"][1]), lay(.6, layers_["clerks_floor"][1]), lay(.86, chair + "".join([man["svg"]])), lay(.88, desk + env)]
    cx, cy = 960 + (880 - 960) / .87, 540 + (740 - 540) / .87
    cam = [[0, cx - 60, cy + 30, 1.38], [t_open, cx, cy + 20, 1.5, "sine"], [t_hold, cx - 20, cy - 60, 1.72, "inout"], [dur, cx - 10, cy - 70, 1.8, "sine"]]
    over = [title("Boston", "August 1919", w, h, d=min(3.0, dur - .6)), badge("Our illustration · not a portrait", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[man], cam=cam, focus=[[0, .87]], dof=6, shake=.3, over=over, grade="dusk", vig=1.25)
    import sfx
    foley = [("paper", t_open, .5, 0), ("paper", t_hold - .2, .3, .1)]
    amb = sfx.room_tone(dur + .5, seed=51, clock=True, street=.12) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_coupon_trade(w, h, dur, ctx):
    """Spain: 30 centavos pushed under the grille, a coupon comes back; the camera follows it across the sea (a
    steamer); Boston: the coupon goes under the grille, a 5-cent stamp comes back; then the comparison."""
    t_es = max(1.0, seg_t(ctx, 1, .2))
    t_sea = max(t_es + 1.6, seg_t(ctx, 2, 0))
    t_us = max(t_sea + 2.4, word_t(ctx, 2, "stamp") - .2)
    t_cmp = max(t_us + 1.2, seg_t(ctx, 3, .15))
    back = (post_counter(-300, "POST OFFICE · SPAIN", "#E2C79A") + post_counter(3500, "POST OFFICE · BOSTON", "#CFD8D2"))
    sea = (f'<rect x="1200" y="-900" width="2300" height="2600" fill="#BFD3D6"/>'
           + "".join(f'<path d="M{x},{y} q30,-14 60,0 t60,0" fill="none" stroke="#7FA2AA" stroke-width="4" data-drift=\'[{-6 - (y % 5)},0,0]\'/>'
                     for x in range(1220, 3460, 180) for y in range(560, 1100, 90))
           + f'<rect x="1200" y="420" width="2300" height="20" fill="#9FBCC2"/>')
    ship = (f'<g {C.kv(translate=[[0, 1300, 0], [t_sea, 1300, 0], [t_us - .2, 3100, 0, "inout"], [dur, 3200, 0]])}>'
            + f'<path d="M-180,560 L180,560 L140,640 L-150,640 Z" fill="#2A2522" stroke="{INK}" stroke-width="3"/>'
            + _r(-90, 490, 170, 70, "#F1E6CF", sw=3) + _r(-30, 410, 40, 80, RED, sw=3)
            + f'<g transform="translate(-10,404)"><g data-steam="2"><circle r="18" fill="#F4F1EA"/><circle r="18" fill="#F4F1EA"/><circle r="18" fill="#F4F1EA"/></g></g></g>')
    coins = (f'<g {C.kv(translate=[[0, 380, 740], [t_es - .1, 380, 740], [t_es + .5, 700, 740, "out"]], opacity=[[0, 1], [t_es + .7, 1], [t_es + .9, 0]])}>'
             + "".join(f'<g transform="translate({k * 60},0)">{L.coin_stack(2, r=26)}</g>' for k in range(3))
             + _t(60, -60, "30 centavos", 44, fill=INK, family="Sans", weight=600) + "</g>")
    coupon_es = (f'<g {C.kv(translate=[[0, 640, 720, -6], [t_es + .6, 640, 720, -6], [t_es + 1.2, 420, 700, 4, "out"], [t_sea - .1, 420, 700, 4],
                                        [t_sea + .5, 1500, 470, 0, "inout"], [t_us - .5, 3500, 470, -4, "lin"], [t_us, 4250, 720, 0, "out"],
                                        [t_us + .6, 4250, 730, 0]],
                             opacity=[[0, 0], [t_es + .55, 0], [t_es + .7, 1], [t_us + .5, 1], [t_us + .7, 0]])}>{reply_coupon(170, 108)}</g>')
    stamp = (f'<g {C.kv(translate=[[0, 4250, 720], [t_us + .6, 4250, 720], [t_us + 1.2, 4020, 680, 0, 1.6, "out"], [dur, 4010, 670, 0, 1.65]],
                         opacity=[[0, 0], [t_us + .55, 0], [t_us + .75, 1]])}>{stamp_5c(1.1)}</g>')
    cmp_ = kt(_r(3480, 230, 1000, 150, PAPER, rx=10, sw=3)
              + _t(3980, 292, "30 centavos cost less than 5¢", 40, fill=INK, family="Sans", weight=600)
              + _t(3980, 346, "because the peseta had fallen", 28, fill="#6A5F50", family="Sans", weight=500), None, t_cmp)
    world = back + sea
    layers = [lay(.7, world, noblur=True), lay(.72, ship), lay(.75, coins + coupon_es + stamp + cmp_)]
    zx = lambda x: 960 + (x - 960) / .75
    cam = [[0, zx(560), 560, 1.0], [t_es, zx(560), 600, 1.12, "sine"], [t_sea + .5, zx(1500), 560, 1.05, "inout"], [t_us - .5, zx(3500), 560, 1.05, "lin"], [t_us, zx(4100), 600, 1.08, "out"],
           [t_us + .8, zx(4060), 600, 1.14, "out"], [t_cmp, zx(3980), 520, 1.08, "inout"], [dur, zx(3980), 520, 1.12, "sine"]]
    over = [badge("Our illustration · prices from Smithsonian Magazine", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[], cam=cam, focus=[[0, .75]], dof=4, shake=.25, over=over, grade="warm", tin=("dissolve", .35))
    import sfx
    foley = ([("clink", t_es + .05 + .08 * k, .35, -.2) for k in range(3)] + [("paper", t_es + .7, .35, -.2), ("paper", t_us + .1, .35, .2),
             ("paper", t_us + .7, .3, .2), ("hit", t_cmp + .1, .35, 0, dict(pitch=196))])
    amb = sfx.room_tone(dur + .5, seed=52, clock=False, street=.18) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def _board_count(label, keys, pre="$", suf="", sub=""):
    return (_t(960, 170, label, 30, fill="#B9C2BC", family="Sans", weight=600, extra='letter-spacing="4"')
            + f'<g {C.kv(opacity=[[0, 0], [keys[1][0] - .25, 0], [keys[1][0], 1]])}>'
              f'<text x="960" y="272" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="82" fill="#F6D58A" '
              f'{C.kv(count=keys)} data-dec="0" data-pre="{pre}" data-suf="{suf}">{pre}0</text></g>'
            + (_t(960, 316, sub, 22, fill="#B9C2BC", family="Sans", weight=500) if sub else ""))


def shot_office_cash(w, h, dur, ctx):
    """By July 1920: people hand money in at the windows; the clerks' stacks grow; the board counts to about $1,000,000
    a week on the words."""
    t_c0 = max(1.0, seg_t(ctx, 2, .05))
    t_c1 = min(dur - .6, max(t_c0 + 1.5, seg_t(ctx, 2, .95)))
    board = _board_count("TAKEN IN, A WEEK (ABOUT)", [[0, 0], [t_c0, 0], [t_c1, 1000000, "out"]], sub="By July 1, 1920 · Supreme Court opinion")
    layers_, anc = office_1920(board=board)
    hands = [.8 + 1.1 * k for k in range(int((dur - 1) / 1.1))]
    ck = clerks(anc, dur, act_at=hands)
    pub = public_at_counter(anc, dur, react_at=None, n=7, hold=cash_stack(2, 70))
    stacks = ""
    for i, wx in enumerate(anc["windows"]):
        for k in range(6):
            at = .9 + 1.1 * (k * 3 + i)
            if at < dur - .2:
                stacks += f'<g {C.kv(opacity=[[0, 0], [at, 0], [at + .2, 1]], translate=[[0, wx + 120, 785 - 18 * k], [at, wx + 60, 770 - 18 * k], [at + .3, wx + 120, 785 - 18 * k, "out"]])}>{cash_stack(1, 110)}</g>'
    layers = [lay(.42, layers_["wall"][1]), lay(.6, layers_["clerks_floor"][1]), lay(.66, "".join(a["svg"] for a in ck)),
              lay(.8, layers_["counter"][1] + stacks + layers_["grilles"][1]), lay(.9, layers_["floor"][1]), lay(.92, "".join(a["svg"] for a in pub))]
    bx, by = 960 + (960 - 960) / .42, 540 + (225 - 540) / .42
    cam = [[0, 900, 640, 1.04], [max(.8, t_c0 - .6), 960, 600, 1.1, "sine"], [t_c0 + .4, 960, 470, 1.26, "inout"], [dur, 980, 460, 1.3, "sine"]]
    over = [title("27 School Street", "Spring and summer 1920", w, h, d=min(3.0, dur - .6)), badge("Reconstruction · not the real office", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ck + pub, cam=cam, focus=[[0, .8], [t_c0, .42], [dur, .42]], dof=6, shake=.35, over=over, grade="warm")
    import sfx
    foley = [("paper", t + .05, .22, (-.3, 0, .3)[k % 3]) for k, t in enumerate(hands) if t < dur - .3] + [("flap", t_c0 + .1, .2, 0), ("hit", t_c1, .4, 0, dict(pitch=147))]
    amb = sfx.street_ambience(dur + .5, seed=16, crowd=1.0) * .4 + sfx.room_tone(dur + .5, seed=17, clock=False, street=0) * .4
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_jars(w, h, dur, ctx):
    """Three jars on a counter at night: new lenders' money pours into MONEY IN; out of it, coins go to PAID TO EARLIER
    LENDERS; INVESTMENTS stays empty, then a NONE tag drops onto it on 'no investments'."""
    t_none = max(1.0, word_t(ctx, 1, "no investments") if len(ctx.get("segs") or []) > 1 else 1.5)
    t_flow = max(t_none + 1.0, seg_t(ctx, 2, .1))
    xs = dict(inv=470, mid=960, out=1450)
    base = 860
    jars = (f'<g transform="translate({xs["inv"]},{base}) scale(1.5)">{L.jar("INVESTMENTS", 220, 260, color="#5E6663")}</g>'
            f'<g transform="translate({xs["mid"]},{base}) scale(1.5)">{L.jar("MONEY IN", 220, 260, color=TEAL)}</g>'
            f'<g transform="translate({xs["out"]},{base}) scale(1.5)">{L.jar("PAID OUT", 220, 260, color=RED)}</g>')
    falls, outs = "", ""
    for k in range(14):                                             # new money falls into the middle jar from above
        at = .4 + k * (dur - 1.2) / 14
        falls += (f'<g {C.kv(translate=[[0, xs["mid"] + (k % 3 - 1) * 40, -120], [at, xs["mid"] + (k % 3 - 1) * 40, -120], [at + .5, xs["mid"] + (k % 3 - 1) * 40, base - 40 - 9 * min(k, 8), "in"]],
                               opacity=[[0, 0], [at, 0], [at + .05, 1]])}>{L.coin(26)}</g>')
    for k in range(10):                                             # and out of it, across to the paid-out jar
        at = t_flow + k * max(.25, (dur - t_flow - .8) / 10)
        if at > dur - .4:
            break
        outs += (f'<g {C.kv(translate=[[0, xs["mid"], base - 120], [at, xs["mid"], base - 120], [at + .35, (xs["mid"] + xs["out"]) / 2, base - 470, "out"],
                                       [at + .7, xs["out"] + (k % 3 - 1) * 40, base - 40 - 9 * min(k, 8), "in"]],
                              opacity=[[0, 0], [at, 0], [at + .05, 1]])}>{L.coin(26)}</g>')
    none_tag = (f'<g {C.kv(translate=[[0, xs["inv"], -200, -8], [t_none, xs["inv"], -200, -8], [t_none + .45, xs["inv"], base - 430, -6, "out"]])}>'
                + _r(-110, -36, 220, 72, PAPER, rx=6, sw=3) + _t(0, 14, "NONE", 40, fill=RED, family="Sans", weight=600, extra='letter-spacing="5"') + "</g>")
    labels = (_t(xs["mid"], base + 60, "from new lenders", 34, fill="#F1E6CF", family="Sans", weight=500)
              + _t(xs["out"], base + 60, "to earlier lenders", 34, fill="#F1E6CF", family="Sans", weight=500))
    room = (C.defs() + f'<rect x="-1600" y="-900" width="5200" height="2600" fill="#2C2A2E"/>'
            + f'<circle cx="960" cy="420" r="900" fill="url(#glowWarm)" opacity=".35" data-flick=\'[0.35,0.03,2]\'/>'
            + _r(-400, 820, 2700, 40, "#6B4429", sw=3.4) + _r(-400, 860, 2700, 500, "#4E321F", sw=3) + C.motes(100, 0, 1700, 800, n=26, op=.4, spd=3))
    layers = [lay(.6, room, noblur=True), lay(.8, jars + falls + outs + none_tag + labels)]
    cam = [[0, 960, 600, 1.04], [t_none, 960 + (xs["inv"] - 960) / .8 * .5, 560, 1.16, "inout"], [t_flow, 980, 560, 1.06, "inout"], [dur, 1060, 560, 1.1, "sine"]]
    over = [badge("Our illustration · from the Supreme Court's findings", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[], cam=cam, focus=[[0, .8]], dof=4, shake=.25, over=over, grade="dusk", vig=1.2, tin=("dissolve", .35))
    import sfx
    foley = ([("clink", .4 + k * (dur - 1.2) / 14 + .5, .22, 0, dict(glass=True)) for k in range(14)]
             + [("clink", t_flow + k * max(.25, (dur - t_flow - .8) / 10) + .7, .22, .4, dict(glass=True)) for k in range(10) if t_flow + k * max(.25, (dur - t_flow - .8) / 10) < dur - .4]
             + [("paper", t_none + .4, .4, -.4)])
    amb = sfx.room_tone(dur + .5, seed=53, clock=True, street=.05) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_coupon_pile(w, h, dur, ctx):
    """Our calculation. First one coupon priced at nothing, and the 5-cent stamp it can become at most; then coupons
    rain onto the counter in stacks while the board runs to 95,840,000 as the narration reaches the number."""
    t_free = .5
    t_stamp = max(1.2, seg_t(ctx, 1, .05))
    t0 = max(t_stamp + 1.2, word_t(ctx, 1, "he'd need") - .3)
    t1 = min(dur - .8, max(t0 + 2.0, word_t(ctx, 1, "and then")))
    board = (_r(560, 90, 800, 240, "#2E3532", rx=10, sw=4)
             + _board_count("COUPONS NEEDED, AT LEAST", [[0, 0], [t0, 0], [t1, 95840000, "out"]], pre="", sub="$4,792,000 ÷ 5¢ a coupon · our calculation"))
    one = (f'<g {C.kv(opacity=[[0, 0], [t_free, 0], [t_free + .3, 1], [t0, 1], [t0 + .4, 0]], translate=[[0, 760, 600, -4, 1.0], [t_free, 760, 600, -4, 1.0], [t_free + .4, 760, 560, -4, 1.1, "out"]])}>'
           + reply_coupon(260, 168) + _r(-60, 100, 120, 50, PAPER, rx=6, sw=2.6) + _t(0, 136, "COST: 0", 26, fill=RED, family="Sans", weight=600) + "</g>"
           + f'<g {C.kv(opacity=[[0, 0], [t_stamp, 0], [t_stamp + .3, 1], [t0, 1], [t0 + .4, 0]], translate=[[0, 1180, 600, 6, 1.6], [t_stamp, 1180, 600, 6, 1.6], [t_stamp + .4, 1180, 560, 4, 1.9, "out"]])}>'
           + stamp_5c(1.0) + "</g>"
           + kt(_t(1180, 720, "at most", 36, fill=INK, family="Sans", weight=600), None, t_stamp + .3)
           + f'<g {C.kv(opacity=[[0, 1], [t0, 1], [t0 + .3, 0]])}>' + kt(_t(970, 580, "→", 90, fill=RED), None, t_stamp + .2) + "</g>")
    piles = ""
    rng = random.Random(4)
    n = 35
    for k in range(n):
        at = t0 + (t1 - t0) * k / n
        x = 380 + (k % 7) * 195 + rng.uniform(-20, 20)
        y = 760 - (k // 7) * 52
        piles += (f'<g {C.kv(opacity=[[0, 0], [at - .01, 0], [at, 1]], translate=[[0, x, y - 300, rng.uniform(-20, 20)], [at, x, y - 300, rng.uniform(-20, 20)], [at + .35, x, y, rng.uniform(-6, 6), "in"]])}>'
                  + "".join(f'<g transform="translate({j * 3},{-j * 7})">{reply_coupon(170, 106)}</g>' for j in range(3)) + "</g>")
    desk = (C.defs() + f'<rect x="-1600" y="-900" width="5200" height="2600" fill="#5E6663"/>' + C.shaft(700, -100, 400, 1100, angle=0, op=.2, color="255,236,190")
            + _r(-300, 800, 2600, 50, "#8A5A36", sw=4) + _r(-300, 850, 2600, 500, "#6B4429", sw=3))
    layers = [lay(.6, desk, noblur=True), lay(.7, board), lay(.75, one + piles)]
    cam = [[0, 960, 520, 1.06], [t0, 960, 540, 1.02, "inout"], [dur, 960, 520, 1.08, "sine"]]
    over = [badge("Our calculation · not a historical scene", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[], cam=cam, focus=[[0, .7]], dof=4, shake=.2, over=over, grade="cool", tin=("dissolve", .35))
    import sfx
    foley = ([("paper", t_free + .1, .3, -.2), ("paper", t_stamp + .1, .3, .2)] + [("paper", t0 + (t1 - t0) * k / n + .3, .16, ((k % 7) - 3) / 4) for k in range(0, n, 2)]
             + [("hit", t1, .4, 0, dict(pitch=147))])
    amb = sfx.room_tone(dur + .5, seed=54, clock=False, street=0) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_run(w, h, dur, ctx):
    """Late July 1920: the crowd presses to the windows holding up notes; the clerks push cash out across the counter;
    the stacks behind the grilles go down."""
    t_rush = max(1.0, seg_t(ctx, 1, .1))
    board = _board_count("PAID OUT IN ONE DAY", [[0, 0], [max(1, seg_t(ctx, 2, .2)), 0], [min(dur - .5, seg_t(ctx, 2, .95)), 1000000, "out"]],
                         suf="+", sub="As the Boston Post reported · via Smithsonian")
    layers_, anc = office_1920(board=board)
    gives = [t_rush + .6 + .9 * k for k in range(int((dur - t_rush - 1) / .9))]
    ck = clerks(anc, dur, act_at=gives)
    pub = public_at_counter(anc, dur, react_at=t_rush - .3, mood="hold_up", n=9, gap=160, x0=180, hold=promissory_note(80, 52), seed=27)
    back = public_at_counter(dict(anc, public_y=1000), dur, react_at=t_rush, mood="concern", n=6, gap=260, x0=60, seed=33, prefix="r")
    stacks = ""
    for i, wx in enumerate(anc["windows"]):
        for k in range(5):
            gone = t_rush + .6 + .9 * (k * 3 + i)
            stacks += f'<g {C.kv(opacity=[[0, 1], [gone, 1], [gone + .25, 0]], translate=[[0, wx + 100, 785 - 18 * k], [gone, wx + 100, 785 - 18 * k], [gone + .3, wx - 40, 800 - 18 * k, "out"]])}>{cash_stack(1, 110)}</g>'
    layers = [lay(.42, layers_["wall"][1]), lay(.6, layers_["clerks_floor"][1]), lay(.66, "".join(a["svg"] for a in ck)),
              lay(.8, layers_["counter"][1] + stacks + layers_["grilles"][1]), lay(.86, "".join(a["svg"] for a in back)), lay(.9, layers_["floor"][1]),
              lay(.94, "".join(a["svg"] for a in pub))]
    bx, by = 960, 540 + (225 - 540) / .42
    cam = [[0, 960, 620, 1.04], [t_rush, 1000, 640, 1.14, "inout"], [max(t_rush + 1, seg_t(ctx, 2, .1)), 960, 470, 1.26, "inout"], [dur, 940, 460, 1.3, "sine"]]
    over = [title("School Street", "Late July 1920", w, h, d=min(3.0, dur - .6)), badge("Reconstruction · not the real office", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ck + pub + back, cam=cam, focus=[[0, .8], [dur, .7]], dof=6, shake=.5, over=over, grade="cool")
    import sfx
    foley = [("paper", t + .05, .25, (-.3, 0, .3)[k % 3]) for k, t in enumerate(gives) if t < dur - .3]
    amb = sfx.street_ambience(dur + .5, seed=18, crowd=2.2) * .55
    return dict(shots=[shot], foley=foley, amb=amb)


SHOTS = dict(street_queue=shot_street_queue, mail_coupon=shot_mail_coupon, coupon_trade=shot_coupon_trade, office_cash=shot_office_cash,
             jars=shot_jars, coupon_pile=shot_coupon_pile, run=shot_run)
