"""
Filmed beats for YouTube #7, the Panic of 1907 (13 Nov 2026, remade to the cinematic standard). Sets, people and
shots for build/cine.py, used by build/youtube_ep007.py as kind="cine" beats.

Sets (our own generic drawings, badged RECONSTRUCTION; no real building, interior or person is copied):
  ny_street_1907()    a lower-Manhattan street of 1907: tall office blocks behind, a stone trust-company front with
                      columns, steps and a big door, lamp posts, a paved street
  library_1907()      a private library at night: panelled walls, bookcases, green-shaded lamps, a long table, a
                      tall door with a keyhole, a wall clock at four
  exchange_1907()     a trading hall: tall windows, a post with a call-money board, brokers in bowlers

Shots (fn(w, h, dur, ctx) -> dict(shots, foley, amb), as youtube.cine_splice expects; ctx["segs"] are the beat's
sentences, (text, start, end) in beat seconds, used to time reactions to the words):
  shot_library_lock   the hook: the long table, the presidents, the door, the key turns
  shot_run            depositors gather and queue at the trust company's door
  shot_closed         the door shuts, a CLOSED notice goes up, the crowd reacts
  shot_call_money     brokers at the money post; the rate counts 9.5, 70, 100 percent; they react
  shot_pool           a clerk brings the money to the post; brokers cheer
  shot_pledges        the presidents sign, one after another; an insert of a hand signing
Facts on screen come only from the sources in youtube_ep007.py's docstring (rates, dates, the hour).
"""

import math
import pathlib
import random
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402

INK, RED, TEAL, MUSTARD, PAPER = C.INK, C.RED, C.TEAL, C.MUSTARD, "#F7F5F2"
BIG, LX, LY = 10000, -3200, -1400


def lay(z, inner, noblur=False):
    return C.layer(z, inner, x=LX, y=LY, w=BIG, h=4000, noblur=noblur)


def badge(text, w, h):
    s = min(w, h) / 1080
    return (f'<div class="badge" style="right:{int(70 * s)}px;top:{int(58 * s)}px;font-size:{int(17 * s)}px;padding:{int(7 * s)}px {int(12 * s)}px">'
            f'{text}</div>')


def title(k, h_, w, h, at=.3, d=3.4):
    s = min(w, h) / 1080
    return (f'<div class="a" data-fx="life" data-at="{at}" data-d="{d}" data-fi=".5" data-fo=".6" style="position:absolute;left:0;bottom:0;'
            f'width:{int(1100 * s)}px;height:{int(520 * s)}px;background:radial-gradient(ellipse at 0% 100%,rgba(10,8,6,.55),rgba(10,8,6,0) 70%)"></div>'
            f'<div class="title a" data-fx="life" data-at="{at}" data-d="{d}" data-fi=".5" data-fo=".6" style="left:{int(96 * s)}px;bottom:{int(170 * s)}px">'
            f'<div class="k" style="font-size:{int(24 * s)}px">{k}</div><div class="h" style="font-size:{int(84 * s)}px">{h_}</div></div>')


_r, _t = L._r, L._t


def seg_t(ctx, i, frac=0.0):
    """When sentence i of the beat starts (plus frac of its length), in beat seconds."""
    segs = ctx.get("segs") or []
    if not segs:
        return 0.5
    x, a, b = segs[min(i, len(segs) - 1)]
    return a + frac * (b - a)


def word_t(ctx, i, word):
    """Approximate time of a word inside sentence i (by character position)."""
    segs = ctx.get("segs") or []
    if not segs:
        return 1.0
    x, a, b = segs[min(i, len(segs) - 1)]
    k = x.lower().find(word.lower())
    return a + (b - a) * (max(k, 0) / max(len(x), 1))


# ------------------------------------------------------------------------------------------------ sets

def ny_street_1907(seed=7, sign="TRUST COMPANY", door_open=True):
    """Layers and anchors for a lower-Manhattan street, 1907. The trust company's door is centred at x 960."""
    rng = random.Random(seed)
    sky = (C.defs() + '<defs><linearGradient id="skyCool" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#AFC0C6"/>'
           '<stop offset=".6" stop-color="#D9DDD6"/><stop offset="1" stop-color="#ECE6D8"/></linearGradient></defs>'
           '<rect x="-3000" y="-1200" width="9000" height="2600" fill="url(#skyCool)"/>')
    for i in range(5):
        cx, cy = rng.uniform(-1500, 3500), rng.uniform(40, 260)
        sky += (f'<g data-drift=\'[{rng.uniform(5, 10):.1f},0,0]\'><ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rng.uniform(180, 320):.0f}" '
                f'ry="{rng.uniform(26, 44):.0f}" fill="#F4F1EA" opacity=".6"/></g>')
    # far: tall office blocks of 1900s New York (generic towers with many small windows), with a little steam
    far = ""
    xs = -1800
    while xs < 4200:
        bw, top = rng.uniform(160, 300), rng.uniform(40, 320)
        col = rng.choice(["#B9B3A6", "#A9A396", "#C4BCAC", "#9E998E"])
        far += f'<rect x="{xs:.0f}" y="{top:.0f}" width="{bw:.0f}" height="{900 - top:.0f}" fill="{col}"/>'
        for r in range(int((820 - top) / 46)):
            for c in range(int(bw / 34)):
                if rng.random() < .8:
                    far += f'<rect x="{xs + 10 + c * 34:.0f}" y="{top + 18 + r * 46:.0f}" width="16" height="24" fill="#7D8890" opacity=".55"/>'
        if rng.random() < .35:
            far += (f'<g data-drift=\'[10,-8,0]\'>' + "".join(
                f'<circle cx="{xs + bw * .6 + 12 * k:.0f}" cy="{top - 20 - 24 * k:.0f}" r="{16 + 7 * k}" fill="#F1EEE6" opacity="{.5 - .12 * k:.2f}"/>'
                for k in range(3)) + "</g>")
        xs += bw + rng.uniform(10, 50)
    # fronts (z .55): side buildings and the trust company in the middle (base y 900)
    fronts = ""
    for x, w_, col, top in ((-1300, 620, "#B9694A", 230), (-650, 640, "#CDB48F", 180), (1500, 600, "#8E4B35", 210), (2130, 640, "#C2A07A", 250)):
        fronts += L._front(x, w_, top, 900, col, floors=4, cols=3, lit=(), door=(1, "#2A2522"), seed=int(x) % 97,
                           brick=col in ("#B9694A", "#8E4B35"))
    # the trust company: a pale stone temple front
    tx, tw = 0, 1460
    stone, shade = "#E4DCCB", "#CFC5B0"
    fronts += _r(tx, 120, tw, 780, stone, sw=3.6)
    fronts += _r(tx - 30, 96, tw + 60, 44, shade, sw=3)                              # cornice
    fronts += _r(tx + 60, 170, tw - 120, 120, "#D9D0BC", sw=2.6)                       # frieze
    fronts += _t(tx + tw / 2, 252, sign, 62, fill=INK, weight=700, extra='letter-spacing="10"')
    for k in range(6):                                                                 # columns
        cx = tx + 140 + k * (tw - 280) / 5
        fronts += (_r(cx - 46, 300, 92, 24, shade, sw=2.4) + _r(cx - 34, 324, 68, 452, "#EDE6D7", sw=3)
                   + "".join(f'<path d="M{cx - 20 + 13 * j},{330} L{cx - 20 + 13 * j},{770}" stroke="{shade}" stroke-width="3"/>' for j in range(4))
                   + _r(cx - 46, 776, 92, 24, shade, sw=2.4))
    # the door between the middle columns (x 960 is its centre on this layer)
    dx = 960
    fronts += _r(dx - 120, 520, 240, 300, "#3B2A20", sw=3.4)
    if door_open:
        fronts += f'<rect x="{dx - 104}" y="536" width="208" height="284" fill="#F6D58A" opacity=".85"/>'
    fronts += _r(dx - 150, 490, 300, 34, shade, sw=2.6)
    for k in range(4):                                                                 # steps
        fronts += _r(tx + 260 - 18 * k, 820 + 20 * k, tw - 520 + 36 * k, 20, "#D8D0BF", sw=2.4)
    fronts += f'<rect x="-2000" y="880" width="6000" height="40" fill="#B9B2A3" stroke="{INK}" stroke-width="3"/>'
    fronts += f'<path d="M-2000,560 L4000,300 L4000,900 L-2000,900 Z" fill="#202830" opacity=".08"/>'
    street = (f'<rect x="-2600" y="900" width="7200" height="420" fill="#8E8778"/>'
              f'<rect x="-2600" y="900" width="7200" height="22" fill="#B7AE9C" stroke="{INK}" stroke-width="3"/>'
              + "".join(f'<path d="M{x},922 L{x - 140},1320" stroke="#7A7366" stroke-width="3" opacity=".5"/>' for x in range(-2400, 4600, 220))
              + f'<path d="M-2600,1150 L4600,1150" stroke="#5E574A" stroke-width="6" opacity=".35"/>')
    layers = dict(sky=(0.03, sky), far=(0.18, far), fronts=(0.55, fronts), street=(0.8, street))
    return layers, dict(ground_back=935, ground_main=1010, ground_front=1120, door_x=dx)


def lamps(x0=-1200, w=4400):
    s = ""
    for lx in (x0 + 700, x0 + 2600, x0 + 4000):
        s += (f'<rect x="{lx - 10}" y="360" width="20" height="940" fill="#1E1A18"/>'
              f'<path d="M{lx - 44},360 L{lx + 44},360 L{lx + 28},286 L{lx - 28},286 Z" fill="#2A2522" stroke="{INK}" stroke-width="3"/>'
              f'<rect x="{lx - 24}" y="290" width="48" height="66" fill="#F6E3AE" stroke="{INK}" stroke-width="3"/>')
    return s


def library_1907(clock="4:00"):
    """A private library at night. Returns (layers, anchors). Table top at y 860 (layer z .85); door at x 1560."""
    wall = (C.defs() + f'<rect x="-1600" y="-800" width="5200" height="2400" fill="#3A2A20"/>')
    for i in range(-6, 14):                                                            # panelling
        x = i * 260
        wall += _r(x + 20, 560, 220, 300, "#46322A", rx=4, sw=2)
    rng = random.Random(5)
    for k, bx in enumerate((-620, -60, 500, 1060)):                                   # bookcases
        wall += _r(bx, 40, 500, 500, "#2A1E18", rx=4, sw=3.4)
        for row in range(4):
            y = 60 + row * 118
            wall += _r(bx + 12, y + 104, 476, 12, "#5E3D27", sw=2)
            x = bx + 18
            while x < bx + 470:
                bw_, bh = rng.uniform(16, 30), rng.uniform(70, 100)
                col = rng.choice(["#6B2E1E", "#2E4A5A", "#7A5A2A", "#3F5B45", "#8A3A24", "#4A3B30", MUSTARD])
                wall += f'<rect x="{x:.0f}" y="{y + 104 - bh:.0f}" width="{bw_:.0f}" height="{bh:.0f}" fill="{col}" stroke="{INK}" stroke-width="1.8"/>'
                x += bw_ + rng.uniform(1, 3)
    # the wall clock (it reads four) and the door, right
    wall += (f'<g transform="translate(1340,170)"><circle r="66" fill="#EFE6D3" stroke="{INK}" stroke-width="5"/>'
             + "".join(f'<path d="M{54 * math.sin(math.radians(a)):.1f},{-54 * math.cos(math.radians(a)):.1f} L{46 * math.sin(math.radians(a)):.1f},{-46 * math.cos(math.radians(a)):.1f}" stroke="{INK}" stroke-width="3"/>' for a in range(0, 360, 30))
             + f'<path d="M0,0 L{30 * math.sin(math.radians(120)):.1f},{-30 * math.cos(math.radians(120)):.1f}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
             + f'<path d="M0,0 L0,-46" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><circle r="5" fill="{INK}"/></g>')
    door = (_r(1440, 220, 260, 680, "#5E3D27", sw=4) + _r(1470, 250, 200, 280, "#6B4A32", sw=2.4) + _r(1470, 560, 200, 300, "#6B4A32", sw=2.4)
            + f'<circle cx="1490" cy="560" r="9" fill="{MUSTARD}" stroke="{INK}" stroke-width="2"/>'
            + f'<rect x="1484" y="576" width="12" height="20" rx="3" fill="#1E1410"/>')
    glow = (f'<circle cx="420" cy="760" r="520" fill="url(#candle)" opacity=".75"/>'
            f'<circle cx="1020" cy="760" r="480" fill="url(#candle)" opacity=".6"/>')
    floor = (f'<rect x="-1600" y="900" width="5200" height="700" fill="#4A2E22"/>'
             f'<rect x="-1600" y="900" width="5200" height="700" fill="url(#boards)" opacity=".35"/>'
             f'<ellipse cx="760" cy="1060" rx="1100" ry="120" fill="#6B2E1E" opacity=".55"/>')       # a rug
    table = (_r(60, 860, 1260, 36, "#5A3420", rx=6, sw=3.6) + _r(90, 896, 1200, 30, "#3E2416", sw=3)
             + _r(130, 926, 30, 150, "#3E2416", sw=2.6) + _r(1220, 926, 30, 150, "#3E2416", sw=2.6))
    for lx in (400, 1000):                                                             # green-shaded desk lamps
        table += (f'<rect x="{lx - 6}" y="790" width="12" height="70" fill="#B8862B" stroke="{INK}" stroke-width="2"/>'
                  f'<path d="M{lx - 70},790 L{lx + 70},790 L{lx + 44},748 L{lx - 44},748 Z" fill="#1F5A45" stroke="{INK}" stroke-width="3"/>'
                  f'<path d="M{lx - 66},792 L{lx + 66},792 L{lx + 160},860 L{lx - 160},860 Z" fill="#FFE3A3" opacity=".22" data-flick=\'[0.22,0.03,{lx % 7}]\'/>')
    layers = dict(wall=(0.35, wall + door), glow=(0.5, glow), floor=(0.6, floor), table=(0.85, table))
    return layers, dict(table_y=860, seat_y=990, door_x=1490, ground=1080)


def exchange_1907(rate_keys=None):
    """A trading hall with a call-money post. rate_keys: [(t_on, t_off, from, to, decimals), ...], one figure at a time."""
    wall = (C.defs() + f'<rect x="-1600" y="-800" width="5200" height="2400" fill="#D9CDB4"/>')
    for k in range(-3, 8):                                                             # tall arched windows, light shafts
        x = k * 420
        wall += (_r(x, 60, 240, 560, "#EFE6D3", sw=3.4) + f'<rect x="{x + 18}" y="78" width="204" height="524" fill="#F8F1DF"/>'
                 + f'<path d="M{x},60 A120,90 0 0 1 {x + 240},60" fill="#EFE6D3" stroke="{INK}" stroke-width="3"/>'
                 + "".join(f'<path d="M{x + 18},{78 + 131 * j} L{x + 222},{78 + 131 * j}" stroke="#D9CDB4" stroke-width="6"/>' for j in (1, 2, 3)))
    wall += f'<rect x="-1600" y="640" width="5200" height="28" fill="#B8A889" stroke="{INK}" stroke-width="3"/>'
    light = "".join(C.shaft(x + 40, 90, 160, 1100, angle=-20, op=.22) for x in range(-1260, 3000, 840)) + C.motes(-200, 100, 2400, 800, n=50, op=.6, spd=6, seed=8)
    floor = f'<rect x="-1600" y="900" width="5200" height="700" fill="#8A7A62"/><rect x="-1600" y="900" width="5200" height="700" fill="url(#boards)" opacity=".25"/>'
    # the money post: a pillar with a slate board (the call-money rate counts on it)
    px = 960
    post = (_r(px - 60, 120, 120, 800, "#6B4A32", sw=3.6) + _r(px - 250, 220, 500, 300, "#2A3A33", rx=8, sw=5)
            + _r(px - 236, 234, 472, 272, "none", rx=5, sw=2)
            + _t(px, 296, "CALL MONEY", 44, fill="#F4ECDD", weight=700, family="Sans", extra='letter-spacing="6"')
            + _t(px, 340, "RATE, A YEAR", 24, fill="#C9C3B2", weight=600, family="Sans", extra='letter-spacing="4"'))
    for t_on, t_off, v0, v1, dec in (rate_keys or []):        # one figure at a time, each counting from the last
        post += (f'<text x="{px}" y="470" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="120" fill="#F6D58A" '
                 f'{C.kv(count=[[0, v0], [t_on, v0], [t_on + .6, v1]], opacity=[[0, 0], [t_on - .01, 0], [t_on, 1], [t_off - .01, 1], [t_off, 0]])} '
                 f'data-suf="%" data-dec="{dec}">{v0}%</text>')
    layers = dict(wall=(0.35, wall), light=(0.45, light), floor=(0.6, floor), post=(0.7, post))
    return layers, dict(ground=1020, post_x=px)


# ------------------------------------------------------------------------------------------------ people

def presidents(n, x0, gap, seat_y, scale=.9, prefix="p", base_pose="seated", looks=("banker_1907", "banker_1907b", "banker_1907c"),
               keys=None, dur=8.0):
    """Seated trust company presidents along the far side of the table, facing the camera's right in turn."""
    out = []
    for i in range(n):
        pk = (keys or {}).get(i) or [[0, C.pose(base_pose, head=4 * ((i % 3) - 1))], [dur, C.pose(base_pose, head=-3 * ((i % 3) - 1))]]
        out.append(C.actor(f"{prefix}{i}", looks[i % len(looks)], pos=[[0, x0 + i * gap, seat_y]], scale=scale, seed=40 + i,
                           dir=1 if i % 2 == 0 else -1, walk=False, pose_keys=pk))
    return out


# ------------------------------------------------------------------------------------------------ shots

def shot_library_lock(w, h, dur, ctx):
    """The hook: wide on the long table, the presidents waiting; the camera drifts to the door, where a banker
    (our illustration, not a portrait) turns the key; push on the lock as the narration says 'locked'."""
    layers_, anc = library_1907()
    t_lock = min(dur - 1.2, max(1.6, word_t(ctx, 1, "locked")))
    pres = presidents(5, 250, 210, anc["seat_y"], dur=dur,
                      keys={2: [[0, C.pose("seated", head=6)], [t_lock - .2, C.pose("seated", head=6)], [t_lock + .3, C.pose("seated", head=-14, brow=1, mouth=2)], [dur, C.pose("seated", head=-10, brow=.6)]],
                            4: [[0, C.pose("seated")], [t_lock + .1, C.pose("seated")], [t_lock + .5, C.pose("seated", head=-16, brow=1)], [dur, C.pose("seated", head=-12)]]})
    key = '<g transform="rotate(0)"><circle r="12" fill="none" stroke="#C99A3B" stroke-width="6"/><path d="M12,0 H44 M34,0 V10 M42,0 V8" stroke="#C99A3B" stroke-width="6" stroke-linecap="round"/></g>'
    # the host stands at the door, on the wall's depth so he lines up with it (first stills: on z .9 he floated
    # far in front of the door the camera was pushing into)
    host = C.actor("host", "banker_1907", pos=[[0, 1760, 905], [max(.8, t_lock - 1.4), 1590, 905], [dur, 1590, 905]],
                   scale=1.45, seed=3, dir=-1, holdF=key,
                   pose_keys=[[0, C.pose("relaxed")], [max(.9, t_lock - 1.2), C.pose("reach", shF=78, elF=10)], [t_lock - .2, C.pose("reach", shF=80, elF=6)],
                              [t_lock + .5, C.pose("reach", shF=80, elF=6, head=8)], [dur, C.pose("relaxed", head=-6)]])
    layers = [lay(z, s, noblur=(k == "glow")) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.78, "".join(a["svg"] for a in pres)))
    layers.append(lay(.85, layers_["table"][1]))
    layers.insert(1, lay(.36, host["svg"]))
    # the door's keyhole on the z .35 layer at (1490, 586) -> camera point
    kx, ky = 960 + (1490 - 960) / .35, 540 + (586 - 540) / .35
    tx, ty = 960 + (760 - 960) / .8, 540 + (760 - 540) / .8
    cam = [[0, tx, ty, 1.0], [max(1.0, t_lock - 1.6), tx + 220, ty - 20, 1.08, "sine"], [t_lock, kx * .55 + tx * .45, 560, 1.5, "inout"],
           [dur, kx * .6 + tx * .4, 560, 1.62, "sine"]]
    over = [title("New York", "November 1907", w, h, d=min(3.4, dur - .6)), badge("Reconstruction", w, h)]
    shot = dict(dur=dur, layers=layers, actors=pres + [host], cam=cam, focus=[[0, .8], [t_lock, .9], [dur, .9]], dof=7, shake=.35,
                over=over, grade="dusk", vig=1.2)
    import sfx
    foley = [("tick", t, .25, .35) for t in np.arange(.4, dur, 1.0)] + [("hit", t_lock, .5, .4, dict(pitch=110)), ("paper", t_lock + .4, .25, -.3)]
    amb = sfx.room_tone(dur + .5, seed=9, clock=False, street=.08)
    return dict(shots=[shot], foley=foley, amb=amb * .7)


def _street_people(anc, dur, queue_n=9, arrivals=4, closed_at=None, seed=11):
    """A queue up the steps to the door, people hurrying in to join it, passers-by in the far plane."""
    rng = random.Random(seed)
    looks = ["clerk_1907", "lady_1907", "worker_1907", "clerk_1907b", "banker_1907b", "lady_1907b", "clerk_1907c", "worker_1907"]
    q = []
    for i in range(queue_n):                                       # the line, facing the door (to the right)
        x = anc["door_x"] - 120 - i * 92
        y = anc["ground_main"] - 4 + (i % 2) * 6
        keys = [[0, C.pose("relaxed", head=rng.uniform(-6, 6))], [dur * .5, C.pose("relaxed", head=rng.uniform(-8, 8))]]
        if closed_at is not None:
            keys = [[0, C.pose("relaxed")], [closed_at + .2 + .07 * i, C.pose("relaxed")],
                    [closed_at + .5 + .07 * i, C.pose(("concern", "shrug", "point")[i % 3], brow=-1 if i % 3 == 0 else 1)],
                    [dur, C.pose(("concern", "shrug", "concern")[i % 3])]]
        a = C.actor(f"q{i}", looks[i % len(looks)], pos=[[0, x, y]], scale=.82, seed=seed + i, dir=1, walk=False, pose_keys=keys)
        q.append(a)
    walkers = []
    for j in range(arrivals):                                      # people hurrying in from the left to join the line
        end_x = anc["door_x"] - 120 - (queue_n + j) * 92
        start = end_x - rng.uniform(700, 1100)
        t_arrive = min(dur - .4, rng.uniform(1.6, dur * .8))
        walkers.append(C.actor(f"w{j}", looks[(j * 3 + 1) % len(looks)], pos=[[0, start, anc["ground_main"] + 4], [t_arrive, end_x, anc["ground_main"] + 4, "out"]],
                               scale=.84, seed=seed + 30 + j, dir=1, amp=24))
    back = L.crowd(6, (-900, 2700), anc["ground_back"], .55, z_seed=seed, dur=dur + 1, talkers=1, prefix="b",
                   looks=["clerk_1907", "lady_1907", "clerk_1907b", "worker_1907", "banker_1907c", "lady_1907b"])
    return q, walkers, back


def shot_run(w, h, dur, ctx):
    """October 18: depositors gather; the line grows up the steps of the trust company."""
    layers_, anc = ny_street_1907()
    q, walkers, (bsvg, back) = _street_people(anc, dur)
    layers = [lay(z, s, noblur=(k == "sky")) for k, (z, s) in layers_.items()]
    layers.insert(3, lay(.5, bsvg))
    layers.append(lay(.8, "".join(a["svg"] for a in q + walkers)))
    layers.append(lay(1.3, lamps()))
    cam = [[0, 520, 600, 1.05], [dur, 860, 580, 1.22, "sine"]]
    over = [title("New York", "October 18, 1907", w, h, d=min(3.2, dur - .6)), badge("Reconstruction", w, h)]
    shot = dict(dur=dur, layers=layers, actors=q + walkers + back, cam=cam, focus=[[0, .8], [dur, .8]], dof=9, shake=.4, over=over, grade="cool")
    import sfx
    steps = sorted(set(sum((C.footsteps(a, dur) for a in walkers[:2]), [])))
    foley = [("step", t, .35, (-.3, .3)[i % 2]) for i, t in enumerate(steps) if t < dur - .3]
    amb = sfx.street_ambience(dur + .5, seed=5, crowd=1.3)
    return dict(shots=[shot], foley=foley, amb=amb * .55)


def shot_closed(w, h, dur, ctx):
    """October 22, shortly after noon: the door shuts, a CLOSED notice goes up, the line turns to each other."""
    layers_, anc = ny_street_1907(door_open=True)          # lit and open until it shuts on "shut"
    t_shut = min(dur - 1.0, max(1.0, word_t(ctx, 1, "shut")))
    q, walkers, (bsvg, back) = _street_people(anc, dur, queue_n=11, arrivals=0, closed_at=t_shut, seed=21)
    dx = anc["door_x"]
    door = (f'<g {C.kv(opacity=[[0, 0], [t_shut - .25, 0], [t_shut, 1]])}>' + _r(dx - 104, 536, 208, 284, "#3B2A20", sw=3) + "</g>"
            + f'<g {C.kv(opacity=[[0, 0], [t_shut + .25, 0], [t_shut + .45, 1]], translate=[[0, dx, 640, -8, .6], [t_shut + .25, dx, 640, -8, .6], [t_shut + .55, dx, 640, -3, 1, "out"]])}>'
            + _r(-110, -40, 220, 80, PAPER, rx=6, sw=3) + _t(0, 16, "CLOSED", 40, fill=RED, weight=700, family="Sans", extra='letter-spacing="4"') + "</g>")
    layers = [lay(z, s, noblur=(k == "sky")) for k, (z, s) in layers_.items()]
    layers.insert(3, lay(.5, bsvg))
    layers.append(lay(.55, door))
    layers.append(lay(.8, "".join(a["svg"] for a in q)))
    layers.append(lay(1.3, lamps()))
    cx = 960 + (dx - 960) / .55
    cam = [[0, 700, 600, 1.12], [max(.5, t_shut - .6), cx, 560, 1.45, "inout"], [dur, cx - 40, 560, 1.38, "sine"]]
    over = [title("October 22, 1907", "Shortly after noon", w, h, d=min(3.0, dur - .6)), badge("Reconstruction", w, h)]
    shot = dict(dur=dur, layers=layers, actors=q + back, cam=cam, focus=[[0, .8], [t_shut, .6], [dur, .7]], dof=8, shake=.35, over=over,
                grade="cool", tin=("dissolve", .4))
    import sfx
    foley = [("hit", t_shut, .7, 0, dict(pitch=82)), ("paper", t_shut + .4, .45, .1)]
    amb = sfx.street_ambience(dur + .5, seed=8, crowd=1.6)
    return dict(shots=[shot], foley=foley, amb=amb * .55)


def _brokers(anc, dur, react_at, n=7, mood="concern", seed=31, prefix="k"):
    rng = random.Random(seed)
    looks = ["clerk_1907", "clerk_1907b", "clerk_1907c", "banker_1907c", "clerk_1907", "worker_1907", "clerk_1907b"]
    out = []
    for i in range(n):
        side = -1 if i % 2 == 0 else 1
        x = anc["post_x"] + side * (300 + (i // 2) * 170) + rng.uniform(-30, 30)
        d = 1 if x < anc["post_x"] else -1
        keys = [[0, C.pose("relaxed", head=-10)], [0.6 + .3 * i, C.pose("talk_a" if i % 2 else "talk_b", head=-12)],
                [react_at + .1 * i, C.pose("relaxed", head=-14)], [react_at + .35 + .1 * i, C.pose(mood if i % 3 else "point", brow=1 if mood == "cheer" else -1, head=-16)],
                [dur, C.pose(mood, head=-12)]]
        out.append(C.actor(f"{prefix}{i}", looks[i % len(looks)], pos=[[0, x, anc["ground"] + (i % 3) * 14]], scale=.92 + .04 * (i % 3), seed=seed + i,
                           dir=d, walk=False, pose_keys=keys))
    return out


def shot_call_money(w, h, dur, ctx):
    """The money post: the board counts 9.5, then 70, then 100 percent as the narration says each; brokers react."""
    t70 = max(1.0, word_t(ctx, 0, "seventy"))
    t100 = max(t70 + 1.2, word_t(ctx, 1, "hundred"))
    keys = [(0, t70 - .3, 9.5, 9.5, 1), (t70 - .3, t100 - .3, 9.5, 70, 0), (t100 - .3, dur + 1, 70, 100, 0)]
    layers_, anc = exchange_1907(rate_keys=keys)
    brokers = _brokers(anc, dur, t70, mood="concern")
    layers = [lay(z, s, noblur=(k == "light")) for k, (z, s) in layers_.items()]
    layers.append(lay(.82, "".join(a["svg"] for a in brokers)))
    pcx, pcy = 960 + (960 - 960) / .7, 540 + (380 - 540) / .7
    cam = [[0, pcx, 600, 1.0], [t70, pcx, 520, 1.22, "inout"], [t100, pcx, pcy, 1.55, "inout"], [dur, pcx, pcy, 1.6, "sine"]]
    over = [badge("Reconstruction · rates from Federal Reserve History", w, h)]
    shot = dict(dur=dur, layers=layers, actors=brokers, cam=cam, focus=[[0, .75], [t100, .7], [dur, .7]], dof=6, shake=.4, over=over, grade="warm")
    import sfx
    foley = [("hit", t70 + .1, .45, 0, dict(pitch=196)), ("hit", t100 + .1, .55, 0, dict(pitch=147)), ("paper", .5, .2, -.4)]
    amb = sfx.street_ambience(dur + .5, seed=12, crowd=2.0) * .5
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_pool(w, h, dur, ctx):
    """A clerk carries the money to the post (a bag, then a stack of notes on the counter); brokers cheer."""
    t_arrive = min(dur - 1.0, max(1.6, seg_t(ctx, 0, .7)))
    layers_, anc = exchange_1907(rate_keys=[(0, dur + 1, 100, 100, 0)])
    brokers = _brokers(anc, dur, t_arrive, mood="cheer", seed=51, prefix="c")
    bag = (f'<g><path d="M-30,-6 C-40,-50 40,-50 30,-6 Q34,30 0,32 Q-34,30 -30,-6 Z" fill="#B8862B" stroke="{INK}" stroke-width="3"/>'
           f'<text x="0" y="16" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="26" fill="{INK}">$</text></g>')
    clerk = C.actor("clerk", "clerk_1907", pos=[[0, -300, anc["ground"] + 30], [t_arrive, anc["post_x"] - 150, anc["ground"] + 30, "out"], [dur, anc["post_x"] - 150, anc["ground"] + 30]],
                    scale=1.0, seed=8, dir=1, holdF=bag, upright=True,
                    pose_keys=[[0, C.pose("relaxed", shF=40, elF=50)], [t_arrive, C.pose("hold_up", shF=110)], [dur, C.pose("hold_up", shF=126, mouth=1)]])
    layers = [lay(z, s, noblur=(k == "light")) for k, (z, s) in layers_.items()]
    layers.append(lay(.82, "".join(a["svg"] for a in brokers)))
    layers.append(lay(.9, clerk["svg"]))
    cam = [[0, 500, 600, 1.15], [t_arrive, 900, 580, 1.2, "inout"], [dur, 940, 560, 1.28, "sine"]]
    over = [badge("Reconstruction", w, h)]
    shot = dict(dur=dur, layers=layers, actors=brokers + [clerk], cam=cam, focus=[[0, .9], [dur, .85]], dof=6, shake=.4, over=over, grade="warm",
                tin=("dissolve", .4))
    import sfx
    steps = [t for t in C.footsteps(clerk, dur) if t < t_arrive]
    foley = [("step", t, .4, -.2) for t in steps] + [("clink", t_arrive + .05, .5, 0), ("clink", t_arrive + .2, .4, .1)]
    amb = sfx.street_ambience(dur + .5, seed=14, crowd=2.0) * .5
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_pledges(w, h, dur, ctx):
    """Just after four: the presidents sign in turn (a pen stroke and a page lifted each), then an insert of a hand
    signing a pledge whose sum is left blank (no amount per bank is sourced)."""
    layers_, anc = library_1907()
    d1 = dur * .62
    n = 5
    sign_t = [.5 + k * (d1 - 1.2) / n for k in range(n)]
    keys = {k: [[0, C.pose("seated")], [t, C.pose("sit_write", head=14)], [t + .9, C.pose("sit_write", head=12)], [t + 1.2, C.pose("seated", head=-4, mouth=0)],
                [d1, C.pose("seated", head=-6)]] for k, t in enumerate(sign_t)}
    pres = presidents(n, 250, 210, anc["seat_y"], dur=d1, keys=keys)
    sheets = "".join(f'<g transform="translate({250 + 210 * k + 40},{anc["table_y"] - 6}) rotate(-4)">' + _r(-40, -12, 80, 14, PAPER, sw=2)
                     + f'<path d="M-28,-6 L-10,-9 L6,-4 L24,-8" fill="none" stroke="{TEAL}" stroke-width="2.5" {C.kv(dash=[[0, 0], [t + .2, 0], [t + .9, 1]])}/></g>'
                     for k, t in enumerate(sign_t))
    layers = [lay(z, s, noblur=(k == "glow")) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.78, "".join(a["svg"] for a in pres)))
    layers.append(lay(.85, layers_["table"][1] + sheets))
    tx, ty = 960 + (760 - 960) / .8, 540 + (800 - 540) / .8
    cam = [[0, tx - 260, ty, 1.35], [d1, tx + 300, ty - 10, 1.4, "sine"]]
    shot1 = dict(dur=d1, layers=layers, actors=pres, cam=cam, focus=[[0, .8]], dof=6, shake=.3, grade="dusk", vig=1.2,
                 over=[title("Sunday, November 3", "Just after 4 a.m.", w, h, d=min(3.0, d1 - .6)), badge("Reconstruction", w, h)])
    # insert: a hand signs a pledge (the sum is a blank line: no per-bank amount is sourced)
    d2 = dur - d1
    t_sig = .5
    sheet = (f'<g transform="translate(960,560) rotate(-2)"><rect x="-560" y="-330" width="1120" height="660" rx="4" fill="#F6EFE0" stroke="{INK}" stroke-width="5"/>'
             f'<text x="-500" y="-230" font-family="\'Serif\',serif" font-weight="700" font-size="54" fill="{INK}">Pledge</text>'
             f'<text x="-500" y="-170" font-family="\'Sans\',sans-serif" font-weight="600" font-size="22" letter-spacing="4" fill="#7A6A55">NEW YORK, NOVEMBER 3, 1907</text>'
             + "".join(f'<rect x="-500" y="{-110 + 46 * j}" width="{900 - 140 * (j % 2)}" height="8" fill="#CFC6B6"/>' for j in range(4))
             + f'<text x="-500" y="150" font-family="\'Sans\',sans-serif" font-weight="600" font-size="26" fill="#7A6A55">SUM: $ ______________</text>'
             f'<path d="M-500,250 L500,250" stroke="{INK}" stroke-width="3"/></g>')
    ink = (f'<path d="M560,800 C620,760 660,830 720,790 C780,750 800,820 860,790 C920,760 960,800 1040,780 C1100,770 1160,800 1240,770" fill="none" '
           f'stroke="#1E2A3A" stroke-width="7" stroke-linecap="round" {C.kv(dash=[[0, 0], [t_sig, 0], [t_sig + 1.4, 1]])}/>')
    pen = (f'<g {C.kv(translate=[[0, 560, 800], [t_sig, 560, 800], [t_sig + 1.4, 1240, 770, "lin"], [d2, 1400, 900]])}>'
           f'<g transform="rotate(-60)"><rect x="0" y="-8" width="300" height="16" rx="8" fill="#1E1A18" stroke="{INK}" stroke-width="3"/>'
           f'<path d="M0,-8 L-28,0 L0,8 Z" fill="#C99A3B" stroke="{INK}" stroke-width="2"/></g></g>')
    desk = (C.defs() + f'<rect x="-1000" y="-800" width="4000" height="2800" fill="#4A2E22"/>'
            f'<circle cx="1400" cy="200" r="700" fill="url(#candle)" opacity=".5"/>' + sheet + ink + pen)
    shot2 = dict(dur=d2, layers=[lay(1.0, desk)], actors=[], cam=[[0, 900, 580, 1.08], [d2, 940, 600, 1.16, "sine"]], dof=0, shake=.25,
                 grade="dusk", vig=1.0, over=[badge("Reconstruction", w, h)], tin=("cut", 0))
    import sfx
    foley = [("quill", t + .2, .35, -.3 + .15 * k, dict(sec=.7)) for k, t in enumerate(sign_t)] + [("quill", d1 + t_sig, .55, .1, dict(sec=1.4))]
    foley += [("tick", t, .2, .35) for t in np.arange(.3, d1, 1.0)]
    amb = sfx.room_tone(dur + .5, seed=4, clock=False, street=.05)
    return dict(shots=[shot1, shot2], foley=foley, amb=amb * .7)


SHOTS = dict(library_lock=shot_library_lock, run=shot_run, closed=shot_closed, call_money=shot_call_money, pool=shot_pool, pledges=shot_pledges)


if __name__ == "__main__":
    # stills for a quick look: python3 build/cine_1907.py [name ...]
    names = sys.argv[1:] or list(SHOTS)
    work = C.OUT / "cine-1907-stills"
    work.mkdir(parents=True, exist_ok=True)
    demo = dict(segs=[("It is just after four in the morning, on a Sunday.", .3, 3.6), ("The front doors have been quietly locked.", 3.8, 6.4)])
    for nm in names:
        built = SHOTS[nm](1920, 1080, 7.0, demo)
        html, total = C.film_html(built["shots"], 1920, 1080)
        print(nm, C.stills(html, [1.0, total * .5, total - .3], work, nm))
