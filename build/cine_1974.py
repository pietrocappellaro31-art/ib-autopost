"""
Filmed beats for YouTube #11, Herstatt, 26 June 1974 (17 Nov 2026). Sets, props and shots for build/cine.py, used
by build/youtube_ep011.py as kind="cine" beats (cinematic-standard.md section 8, step 3: sets; step 4: data in the
world).

Sets (our own generic drawings; no real bank, building, logo or person is copied; everything is badged):
  back_office_1974()   a bank's payments room in 1974: two wall clocks (Frankfurt and New York) whose hands move,
                       a telex machine that prints, venetian blinds with afternoon light, filing cabinets, a desk
  two_cities()         one long world for a currency trade's two payments: a bank counter in Frankfurt, the sea, a
                       bank counter in New York, each with its own clock and its own window light (day in Germany
                       while it is still night in New York); an optional settlement desk in the middle (pvp)
  correspondent_1974() a New York bank's account desk: a ledger, a telephone, a cash drawer and a safe
Props: wall_clock() (hands keyed to a time path, a ticking second hand), mark_bundle() (generic blue-grey notes
marked DM, no real design), telex(), ledger_1974().
1974 looks (cine.LOOKS): banker_1974, banker_1974b, clerk_1974, clerk_1974b, dealer_1974.

Shots (fn(w, h, dur, ctx) -> dict(shots, foley, amb); ctx["segs"] are the beat's sentences, (text, start, end)):
  clocks_hook   the hook: the payments room; the Frankfurt clock reaches 3:30, the camera pans to New York at 10:30
  two_legs      our illustration: the marks paid over a Frankfurt counter in the morning while New York is dark;
                the camera crosses the sea; dollars wait on the New York counter for New York's day
  ny_suspend    New York: the phone rings, the ledger is stamped, the dollar bundle goes back in the drawer
  freeze        the dealing room re-dressed for 1974: phones ring, nobody pays; the board's index of funds moved
                falls from 100 to 40 (the BIS's estimated 60% fall, drawn as an index)
  pvp_swap      our illustration of payment versus payment: both bundles go into the settlement desk and come out
                to the other side together; then one side never pays and the other's money goes back
Facts on screen come only from the sources in youtube_ep011.py's docstring. Nobody in a shot speaks, and nobody is
a likeness: the figures are "our illustration", not portraits of anyone at Herstatt or any bank.
"""

import math
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402
from cine_1907 import lay, badge, seg_t, word_t   # noqa: E402
from cine_1920 import title                       # noqa: E402
from cine_1971 import kt, dealing_room, traders, desk_phone, typewriter, handset, dollar_bundle, _room_shot   # noqa: E402

INK, RED, TEAL, MUSTARD, PAPER = C.INK, C.RED, C.TEAL, C.MUSTARD, "#F7F5F2"
DM, DM2 = "#9FB3C4", "#7F95A8"
_r, _t = L._r, L._t

C.LOOKS.update({
    "banker_1974": dict(coat="#3B3F4A", coat2="#2B2F38", vest="#EAF0F4", legs="#3B3F4A", stock="#3B3F4A", shoe=INK, skin="#E5B391",
                        hair="#6A4A30", hat="", style="suit", cuff="#EAF0F4", tie="#8A3B22", era="1971"),
    "banker_1974b": dict(coat="#5A4632", coat2="#46362A", vest="#F1E6CF", legs="#5A4632", stock="#5A4632", shoe=INK, skin="#B97A55",
                         hair="#1E1410", hat="", style="suit", cuff="#F1E6CF", tie=MUSTARD, era="1971"),
    "clerk_1974": dict(coat="#6E7F6A", coat2="#566452", vest="#F4EFE4", legs="#4A4440", stock="#4A4440", shoe=INK, skin="#F0C7A4",
                       hair="#A0703A", hat="", style="suit", cuff="#F4EFE4", tie="#3E4F66", era="1971"),
    "clerk_1974b": dict(coat="#7A3E2E", coat2="#5E2F22", vest="#F4EFE4", legs="#3A3A40", stock="#3A3A40", shoe=INK, skin="#8D5A3B",
                        hair="#14100D", hat="", style="dress", cuff="#F4EFE4", tie=RED, era="1971"),
    "dealer_1974": dict(coat="#2F4A5A", coat2="#223845", vest="#F2F2F2", legs="#2F4A5A", stock="#2F4A5A", shoe=INK, skin="#D9A684",
                        hair="#3A2A20", hat="", style="suit", cuff="#F2F2F2", tie=TEAL, era="1971"),
})


# ------------------------------------------------------------------------------------------------ props

def _hand_keys(path, dur, per):
    """Rotation keys for a clock hand: path [[t, hours, minutes], ...] -> [[t, 0, 0, degrees]]; per = 60 (minute
    hand: 6 degrees a minute) or 720 (hour hand: 0.5 degrees a minute)."""
    out = []
    for k in path:
        t, hh, mm = k[0], k[1], k[2]
        mins = hh * 60 + mm
        deg = mins * 6 if per == 60 else mins * .5
        out.append([t, 0, 0, round(deg, 2)] + ([k[3]] if len(k) > 3 else []))
    return out


def wall_clock(cx, cy, r, path, dur, label="", sec0=0, face="#F8F4EA"):
    """A station-style wall clock whose hands follow path [[t, h, m], ...] (eased between keys); a red second hand
    ticks once a second. label: a plaque under it."""
    ticks = "".join(
        f'<path d="M{cx + (r - 14) * math.sin(a):.1f},{cy - (r - 14) * math.cos(a):.1f} L{cx + (r - (30 if k % 3 == 0 else 22)) * math.sin(a):.1f},'
        f'{cy - (r - (30 if k % 3 == 0 else 22)) * math.cos(a):.1f}" stroke="{INK}" stroke-width="{7 if k % 3 == 0 else 4}" stroke-linecap="round"/>'
        for k in range(12) for a in [2 * math.pi * k / 12])
    hand = lambda ln, w_, col: f'<path d="M0,{ln * .18:.0f} L0,{-ln:.0f}" stroke="{col}" stroke-width="{w_}" stroke-linecap="round"/>'
    sec = [[t, 0, 0, (sec0 + math.floor(t)) * 6 + 6 * min(1, (t % 1) / .12)] for t in [x / 8 for x in range(int(dur * 8) + 9)]]
    out = (f'<circle cx="{cx}" cy="{cy + 8}" r="{r + 10}" fill="#000" opacity=".18"/>'
           f'<circle cx="{cx}" cy="{cy}" r="{r + 10}" fill="#2E3532" stroke="{INK}" stroke-width="4"/>'
           f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{face}" stroke="{INK}" stroke-width="3"/>' + ticks
           + f'<g transform="translate({cx},{cy})"><g {C.kv(translate=_hand_keys(path, dur, 720))}>{hand(r * .52, 12, INK)}</g></g>'
           + f'<g transform="translate({cx},{cy})"><g {C.kv(translate=_hand_keys(path, dur, 60))}>{hand(r * .8, 8, INK)}</g></g>'
           + f'<g transform="translate({cx},{cy})"><g {C.kv(translate=[[k[0], 0, 0, round(k[3], 2), "lin"] for k in sec])}>{hand(r * .86, 3, RED)}</g></g>'
           + f'<circle cx="{cx}" cy="{cy}" r="9" fill="{INK}"/>')
    if label:
        out += _r(cx - 150, cy + r + 30, 300, 58, "#2E3532", rx=6, sw=3) + _t(cx, cy + r + 70, label, 30, fill="#F6D58A", family="Sans", weight=600, extra='letter-spacing="5"')
    return out


def mark_bundle(w=150, h=64, s=1.0):
    """A banded stack of generic blue-grey notes marked DM (our design; no real note copied)."""
    out = ""
    for k in range(4):
        out += _r(-w / 2 + k * 2, -h + k * 6 - 24, w, 18, DM2 if k % 2 else DM, rx=3, sw=2)
    out += _r(-w / 2, -h + 4, w, h - 4, DM, rx=4, sw=2.6) + _r(-16, -h + 4, 32, h - 4, PAPER, sw=2)
    out += _t(-w / 4 - 4, -h / 2 + 12, "DM", 22, fill=INK, weight=700, family="Sans") + _t(w / 4 + 4, -h / 2 + 12, "DM", 22, fill=INK, weight=700, family="Sans")
    return f'<g transform="scale({s})">{out}</g>'


def usd_bundle(w=150, h=64, s=1.0):
    return dollar_bundle(w, h, label="", s=s).replace("</g>", _t(-w / 4 - 4, -h / 2 + 12, "$", 24, fill=INK, weight=700, family="Sans")
                                                       + _t(w / 4 + 4, -h / 2 + 12, "$", 24, fill=INK, weight=700, family="Sans") + "</g>", 1)


def telex(x, y, t_print=(), dur=10.0):
    """A telex machine on a stand; during each (t0, t1) in t_print the paper rises out of it (greeked lines only)."""
    rise, acc = [[0, 0, 0]], 0.0
    for a, b in t_print:
        rise += [[a, 0, -acc], [b, 0, -(acc + 60 * (b - a)), "lin"]]
        acc += 60 * (b - a)
    rise.append([dur + 1, 0, -acc])
    lines = "".join(f'<path d="M-44,{-50 + 16 * k} L{34 - 22 * (k % 3)},{-50 + 16 * k}" stroke="#A9A091" stroke-width="3"/>' for k in range(26))
    paper = (f'<g clip-path="url(#tx{x})"><g {C.kv(translate=rise)}><rect x="-56" y="-110" width="112" height="520" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
             f'{lines}</g></g>')
    return (f'<g transform="translate({x},{y})"><defs><clipPath id="tx{x}"><rect x="-80" y="-700" width="160" height="636"/></clipPath></defs>'
            + paper
            + _r(-110, -70, 220, 74, "#C9C2B0", rx=10, sw=3) + _r(-96, -40, 192, 34, "#3B3F48", rx=6, sw=2.4)
            + "".join(f'<rect x="{-88 + 14 * k}" y="-34" width="10" height="9" rx="2" fill="#E8E1D4"/>' for k in range(13))
            + _r(-70, 4, 140, 160, "#8A8F94", sw=3) + "</g>")


def ledger_1974(x, y, title_txt="ACCOUNT: HERSTATT"):
    """An open account ledger on a desk: a sourced heading, greeked rows."""
    rows = "".join(f'<path d="M{x - 150},{y - 40 + 18 * k} L{x - 30 - 30 * (k % 2)},{y - 40 + 18 * k}" stroke="#B9AE9A" stroke-width="3"/>'
                   f'<path d="M{x + 20},{y - 40 + 18 * k} L{x + 140 - 30 * (k % 3)},{y - 40 + 18 * k}" stroke="#B9AE9A" stroke-width="3"/>' for k in range(5))
    return (f'<path d="M{x - 180},{y - 90} L{x},{y - 76} L{x + 180},{y - 90} L{x + 180},{y + 60} L{x},{y + 74} L{x - 180},{y + 60} Z" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M{x},{y - 76} L{x},{y + 74}" stroke="#9A8F7C" stroke-width="3"/>' + rows
            + _t(x - 90, y - 54, title_txt, 18, fill=INK, family="Sans", weight=700))


# ------------------------------------------------------------------------------------------------ sets

def back_office_1974(fra_path, ny_path, dur, t_print=(), seed=3):
    """A payments room, 1974. Clocks centred at x 620 (Frankfurt) and 1300 (New York) on the z .5 wall; a telex at
    x 1720 on the desk layer; window with blinds on the left. Returns (layers, anchors)."""
    rng = random.Random(seed)
    wall = C.defs() + '<rect x="-1600" y="-900" width="5200" height="2600" fill="#C9CBB8"/>'
    wall += '<rect x="-1600" y="760" width="5200" height="30" fill="#A9AA96" stroke="#0A0A0A" stroke-width="3"/>'
    for k in range(40):                                                                # faint wall panels
        wall += f'<path d="M{-1600 + 140 * k},-900 L{-1600 + 140 * k},760" stroke="#BFC1AE" stroke-width="3"/>'
    # window with venetian blinds and afternoon light
    wall += _r(-560, 120, 520, 560, "#E9D9AE", sw=4) + "".join(_r(-556, 130 + 26 * k, 512, 14, "#D8C8A0", sw=1.4) for k in range(21))
    wall += _r(-580, 100, 560, 30, "#8A7F6C", sw=3)
    wall += wall_clock(620, 330, 150, fra_path, dur, label="FRANKFURT", sec0=rng.randint(0, 59))
    wall += wall_clock(1300, 330, 150, ny_path, dur, label="NEW YORK", sec0=rng.randint(0, 59))
    for k in range(3):                                                                 # filing cabinets
        wall += _r(2000 + 190 * k, 420, 170, 360, "#8D9296", sw=3) + "".join(_r(2016 + 190 * k, 440 + 84 * j, 138, 66, "#A2A7AB", sw=2) for j in range(4))
    light = (C.shaft(-560, 120, 520, 900, angle=-28, op=.2) + C.motes(-300, 200, 1400, 700, n=40, op=.5, spd=8, seed=4))
    floor = '<rect x="-1600" y="905" width="5200" height="800" fill="#6F6A5E"/><rect x="-1600" y="905" width="5200" height="800" fill="url(#boards)" opacity=".16"/>'
    desk = (_r(1500, 880, 900, 28, "#C9BBA0", rx=3, sw=3) + _r(1520, 908, 860, 120, "#A8987C", sw=2.6)
            + telex(1720, 880, t_print, dur) + desk_phone(2060, 880) + typewriter(2250, 880)
            + f'<g transform="translate(1950,872) rotate(-4)">' + _r(-60, -8, 120, 10, PAPER, sw=2) + "</g>")
    layers = dict(wall=(0.5, wall), light=(0.55, light), floor=(0.6, floor), desk=(0.8, desk))
    return layers, dict(feet=1000, clocks=(620, 1300), telex=1720)


def _counter(x0, sign, wall_col, win_col, clock_path, dur, sec0=0):
    """One bank counter (world x0 .. x0 + 1500): the back (wall, window whose light is win_col, sign, clock, grille)
    and the front (the counter itself, drawn in front of the clerk). Returns (back, front)."""
    s = f'<rect x="{x0}" y="-900" width="1500" height="2600" fill="{wall_col}"/>'
    s += _r(x0 + 90, 160, 360, 460, win_col, sw=4) + f'<path d="M{x0 + 270},160 L{x0 + 270},620 M{x0 + 90},390 L{x0 + 450},390" stroke="#6B5A44" stroke-width="10"/>'
    s += _r(x0 + 560, 110, 820, 84, "#2E3532", rx=6, sw=3) + _t(x0 + 970, 168, sign, 36, fill="#F6D58A", family="Sans", weight=600, extra='letter-spacing="5"')
    s += wall_clock(x0 + 1220, 380, 92, clock_path, dur, sec0=sec0)
    s += _r(x0 + 560, 420, 460, 24, "#B98A3C", sw=3) + "".join(
        f'<path d="M{x0 + 570 + 30 * k},444 L{x0 + 570 + 30 * k},760" stroke="#B98A3C" stroke-width="5"/>' for k in range(16) if not (5 <= k <= 10))
    front = _r(x0 + 120, 760, 1260, 30, "#6B4429", sw=3.4) + _r(x0 + 140, 790, 1220, 400, "#8A5A36", sw=3)
    return s, front


def two_cities(dur, fra_path, ny_path, ny_light, pvp=False):
    """Frankfurt counter at x -300..1200, the sea 1200..2200, New York counter 2200..3700 (z .75). Returns (back,
    front): the counters' fronts are drawn over the clerks. ny_light: keys [[t, opacity of the day light]] for New
    York's window (dark before its day starts). pvp: a settlement desk on a platform in the middle (x 1700)."""
    fra, fra_f = _counter(-300, "BANK · FRANKFURT", "#E4D6B8", "#F3E7BF", fra_path, dur, sec0=12)
    ny, ny_f = _counter(2200, "BANK · NEW YORK", "#CCD6DA", "#2A3550", ny_path, dur, sec0=40)
    ny += f'<g {C.kv(opacity=ny_light)}>' + _r(2290, 160, 360, 460, "#F3E7BF", sw=4) + f'<path d="M2470,160 L2470,620 M2290,390 L2650,390" stroke="#6B5A44" stroke-width="10"/></g>'
    sea = (f'<rect x="1200" y="-900" width="1000" height="2600" fill="#BFD3D6"/>'
           + "".join(f'<path d="M{x},{y} q30,-14 60,0 t60,0" fill="none" stroke="#7FA2AA" stroke-width="4" data-drift=\'[{-6 - (y % 5)},0,0]\'/>'
                     for x in range(1220, 2160, 180) for y in range(560, 1100, 90))
           + f'<rect x="1200" y="420" width="1000" height="20" fill="#9FBCC2"/>'
           + _t(1450, 330, "GERMANY", 30, fill="#4C6A70", family="Sans", weight=600, extra='letter-spacing="6"')
           + _t(1950, 330, "USA", 30, fill="#4C6A70", family="Sans", weight=600, extra='letter-spacing="6"'))
    front = fra_f + ny_f
    if pvp:
        front += (_r(1460, 760, 480, 30, "#6B4429", sw=3) + _r(1480, 790, 440, 400, "#8A5A36", sw=3))
        sea += (_r(1500, 380, 400, 260, "#2E3532", rx=10, sw=4) + _t(1700, 450, "SETTLEMENT", 34, fill="#F6D58A", family="Sans", weight=600, extra='letter-spacing="5"')
                + _t(1700, 500, "BOTH LEGS AT ONCE", 24, fill="#E8E1D4", family="Sans", weight=600, extra='letter-spacing="3"'))
    return sea + fra + ny, front


# ------------------------------------------------------------------------------------------------ shots

def shot_clocks_hook(w, h, dur, ctx):
    """26 June 1974: a bank's payments room. The Frankfurt clock's hands reach 3:30 as the time is said; the telex
    prints; the camera pans to the New York clock at 10:30 on the second sentence (our calculation). A clerk reads
    the telex paper. Nobody is a portrait; the room is not Herstatt's."""
    t_330 = min(dur * .45, max(1.6, word_t(ctx, 0, "half past three") + .6))
    t_ny = max(t_330 + 2.0, seg_t(ctx, 1, .05))
    fra = [[0, 15, 26], [t_330, 15, 30, "out"], [dur, 15, 30 + dur / 60]]
    ny = [[0, 10, 26], [t_330, 10, 30, "out"], [dur, 10, 30 + dur / 60]]
    layers_, anc = back_office_1974(fra, ny, dur, t_print=[(.4, 2.4), (t_ny + .3, t_ny + 2.0)])
    clerk = C.actor("ck", "clerk_1974", pos=[[0, 1560, anc["feet"]]], scale=.95, seed=7, dir=1, walk=False,
                    pose_keys=[[0, C.pose("read", head=6)], [t_330 - .3, C.pose("read", head=8)], [t_330 + .3, C.pose("relaxed", head=-24, brow=.6)],
                               [t_ny + .5, C.pose("relaxed", head=-22)], [t_ny + 1.4, C.pose("concern", head=-10)], [dur, C.pose("concern", head=-8)]])
    walker = C.actor("wk", "banker_1974", pos=[[0, 2700, anc["feet"] + 20], [min(dur - .5, t_330 + 1.5), 2100, anc["feet"] + 20, "out"]], scale=1.0, seed=9, dir=-1,
                     pose_keys=[[0, C.pose("relaxed")], [dur, C.pose("relaxed", head=-12)]])
    layers = [lay(z, s, noblur=(k == "light")) for k, (z, s) in layers_.items() if k != "desk"]
    layers.append(lay(.76, clerk["svg"] + walker["svg"]))
    layers.append(lay(.8, layers_["desk"][1]))
    zx = lambda x, z=.5: 960 + (x - 960) / z
    cam = [[0, zx(1000), 600, .94], [max(.8, t_330 - 1.2), zx(800), 520, 1.12, "inout"], [t_330 + .6, zx(640), 470, 1.34, "out"],
           [t_ny - .2, zx(660), 470, 1.36, "sine"], [t_ny + 1.0, zx(1290), 480, 1.34, "inout"], [dur, zx(1300), 490, 1.4, "sine"]]
    ny_lab = kt(_r(1300 - 240, 600, 480, 70, PAPER, rx=8, sw=3) + _t(1300, 646, "10:30 A.M. · OUR CALCULATION", 26, fill=INK, family="Sans", weight=700), None, t_ny + .6)
    fra_lab = kt(_r(620 - 240, 600, 480, 70, PAPER, rx=8, sw=3) + _t(620, 646, "3:30 P.M. · BANK CLOSED", 26, fill=RED, family="Sans", weight=700), None, t_330 + .2)
    layers.insert(1, lay(.5, ny_lab + fra_lab))
    lamp = (f'<g data-swing=\'[1.2,1.1,0,980,-200]\'><path d="M980,-200 L980,140" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M900,200 L1060,200 L1020,140 L940,140 Z" fill="#2E5A4E" stroke="{INK}" stroke-width="4"/>'
            f'<ellipse cx="980" cy="204" rx="60" ry="10" fill="#FFF1C9"/></g>')
    fg = (_r(-400, 1040, 1300, 40, "#C9BBA0", rx=4, sw=3.4) + _r(-390, 1080, 1280, 300, "#A8987C", sw=3) + desk_phone(560, 1040, color="#3B2F27")
          + f'<g transform="translate(250,1034) rotate(-5)">' + _r(-90, -10, 180, 12, PAPER, sw=2) + "</g>")
    layers.append(lay(1.1, lamp))
    layers.append(lay(1.2, fg))
    over = [title("June 26, 1974", "3:30 p.m., German time", w, h, d=min(3.2, t_ny - .4)), badge("Reconstruction · not the real bank", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[clerk, walker], cam=cam, focus=[[0, .6], [t_330, .5], [dur, .5]], dof=6, shake=.3, over=over, grade="warm", vig=1.1)
    import sfx
    steps = [t for t in C.footsteps(walker, dur) if t < dur - .2]
    foley = ([("step", t, .15, .4) for t in steps] + [("telex", .4, .35, .4, dict(sec=2.0)), ("telex", t_ny + .3, .35, .4, dict(sec=1.7)),
             ("hit", t_330, .45, -.2, dict(pitch=147)), ("hit", t_ny + 1.0, .35, .2, dict(pitch=196))])
    amb = sfx.room_tone(dur + .5, seed=74, clock=True, street=.2) * .8
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_two_legs(w, h, dur, ctx):
    """Our illustration of a currency trade's two payments. Frankfurt, morning: a bank's man pushes a bundle of marks
    under the grille and the clerk takes it in (New York's window is still dark). The camera crosses the sea; New
    York's day begins and a bundle of dollars sits ready on the counter there. On the last sentence the camera pulls
    back to show both counters, the marks paid and the dollars still waiting."""
    t_dm = max(1.0, seg_t(ctx, 1, .25))
    t_sea = max(t_dm + 1.8, seg_t(ctx, 2, 0))
    t_ny = max(t_sea + 2.2, seg_t(ctx, 2, .75))
    t_wide = max(t_ny + 1.0, seg_t(ctx, 3, 0))
    fra = [[0, 9, 0], [dur, 9, dur / 6]]
    ny = [[0, 3, 55], [t_ny, 4, 0], [t_ny + 1.2, 9, 0, "inout"], [dur, 9, 2]]                # New York's clock runs on to its day
    light = [[0, 0], [t_ny, 0], [t_ny + 1.2, 1]]
    world, front = two_cities(dur, fra, ny, light)
    marks = (f'<g {C.kv(translate=[[0, 380, 740], [t_dm - .3, 380, 740], [t_dm + .6, 700, 740, "out"], [t_dm + 1.0, 820, 700, "out"]],
                        opacity=[[0, 1], [t_dm + .8, 1], [t_dm + 1.1, 0]])}>{mark_bundle(150, 64)}</g>')
    dollars = f'<g {C.kv(translate=[[0, 2960, 740]], opacity=[[0, 0], [t_ny + .9, 0], [t_ny + 1.3, 1]])}>{usd_bundle(150, 64)}</g>'
    lab_fra = kt(_r(100, 860, 900, 120, PAPER, rx=10, sw=3) + _t(550, 916, "MARKS: PAID IN GERMANY", 40, fill=INK, family="Sans", weight=700)
                 + _t(550, 958, "in Germany's banking day", 26, fill="#6A5F50", family="Sans", weight=500), None, t_dm + .9)
    lab_ny = kt(_r(2600, 860, 900, 120, PAPER, rx=10, sw=3) + _t(3050, 916, "DOLLARS: PAID IN THE US", 40, fill=INK, family="Sans", weight=700)
                + _t(3050, 958, "in New York's banking day", 26, fill="#6A5F50", family="Sans", weight=500), None, t_ny + 1.2)
    ppl = [C.actor("fb", "banker_1974", pos=[[0, 240, 1000]], scale=1.0, seed=3, dir=1, walk=False,
                   pose_keys=[[0, C.pose("relaxed")], [t_dm - .3, C.pose("reach", shF=60, elF=16)], [t_dm + .9, C.pose("relaxed", head=-6)], [dur, C.pose("relaxed")]]),
           C.actor("fc", "clerk_1974", pos=[[0, 920, 860]], scale=.86, seed=4, dir=-1, walk=False,
                   pose_keys=[[0, C.pose("relaxed")], [t_dm + .5, C.pose("reach", shF=64, elF=14)], [t_dm + 1.2, C.pose("read", head=8)], [dur, C.pose("relaxed")]]),
           C.actor("nc", "clerk_1974b", pos=[[0, 3120, 860]], scale=.86, seed=6, dir=-1, walk=False,
                   pose_keys=[[0, C.pose("relaxed", head=8)], [t_ny + .9, C.pose("reach", shF=60, elF=18)], [t_ny + 1.6, C.pose("relaxed", head=-8)], [dur, C.pose("relaxed")]])]
    z = .75
    zx = lambda x: 960 + (x - 960) / z
    cam = [[0, zx(600), 560, 1.04], [t_dm, zx(620), 600, 1.14, "sine"], [t_sea - .2, zx(700), 560, 1.1, "inout"], [t_ny - .4, zx(2400), 560, 1.06, "inout"],
           [t_ny + .6, zx(2800), 580, 1.12, "out"], [t_wide - .2, zx(2800), 560, 1.12, "sine"], [t_wide + 1.6, zx(1700), 600, .5, "inout"], [dur, zx(1700), 600, .48, "sine"]]
    shopper = [a for a in ppl if a["spec"]["id"] == "fb"]
    clerks_ = [a for a in ppl if a["spec"]["id"] != "fb"]
    layers = [lay(z, world, noblur=True), lay(z + .01, "".join(a["svg"] for a in clerks_)), lay(z + .02, front + marks + dollars + lab_fra + lab_ny),
              lay(z + .03, "".join(a["svg"] for a in shopper))]
    over = [badge("Our illustration · how a currency trade settles", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl, cam=cam, focus=[[0, z + .02]], dof=3, shake=.25, over=over, grade="warm", tin=("dissolve", .35))
    import sfx
    foley = [("paper", t_dm + .1, .4, -.3), ("paper", t_dm + .9, .3, -.2), ("hit", t_dm + .95, .3, -.2, dict(pitch=196)),
             ("paper", t_ny + 1.0, .35, .3), ("hit", t_ny + 1.3, .3, .3, dict(pitch=220))]
    amb = sfx.room_tone(dur + .5, seed=75, clock=True, street=.15) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def correspondent_1974(dur, ring=(), lift=None, seed=5):
    """A New York bank's account desk: wall with a clock at 10:3x, a counter with a ledger and a phone, a cash
    drawer and a safe behind. Returns (layers, anchors)."""
    wall = C.defs() + '<rect x="-1600" y="-900" width="5200" height="2600" fill="#CCD6DA"/>'
    wall += "".join(f'<path d="M{-1600 + 160 * k},-900 L{-1600 + 160 * k},760" stroke="#BEC9CE" stroke-width="3"/>' for k in range(36))
    wall += _r(140, 110, 1640, 84, "#2E3532", rx=6, sw=3) + _t(960, 168, "BANK · NEW YORK · FOREIGN ACCOUNTS", 36, fill="#F6D58A", family="Sans", weight=600, extra='letter-spacing="5"')
    wall += wall_clock(1560, 400, 110, [[0, 10, 33], [dur, 10, 33 + dur / 60]], dur, sec0=17)
    wall += _r(-500, 240, 520, 440, "#F3E7BF", sw=4) + '<path d="M-240,240 L-240,680 M-500,460 L20,460" stroke="#6B5A44" stroke-width="10"/>'
    # the safe, behind the counter
    wall += (_r(2100, 360, 360, 420, "#5E666C", rx=12, sw=4) + '<circle cx="2280" cy="560" r="70" fill="#7A838A" stroke="#0A0A0A" stroke-width="4"/>'
             + "".join(f'<path d="M2280,560 L{2280 + 60 * math.cos(a):.0f},{560 + 60 * math.sin(a):.0f}" stroke="#0A0A0A" stroke-width="5"/>' for a in [k * math.pi / 3 for k in range(6)]))
    floor = '<rect x="-1600" y="905" width="5200" height="800" fill="#6F6A5E"/>'
    counter = (_r(300, 760, 1500, 30, "#6B4429", sw=3.4) + _r(320, 790, 1460, 400, "#8A5A36", sw=3)
               + ledger_1974(820, 740) + desk_phone(1280, 760, ring_at=ring, lift=lift))
    return dict(wall=(0.5, wall), floor=(0.6, floor), counter=(0.8, counter)), dict(feet_back=905, counter_y=760)


def shot_ny_suspend(w, h, dur, ctx):
    """New York, mid-morning, 26 June 1974 (reconstruction): the phone rings and the clerk answers; on 'stopped' a
    red SUSPENDED stamp lands on the account's ledger; on the second sentence the bundle of dollars goes back into the
    drawer, and the messenger waiting at the counter is left with nothing."""
    t_ring = .5
    t_up = 1.3
    t_stop = min(dur - 3.0, max(t_up + 1.0, word_t(ctx, 0, "stopped")))
    t_back = max(t_stop + 1.2, seg_t(ctx, 1, .1))
    layers_, anc = correspondent_1974(dur, ring=(t_ring, t_ring + .45), lift=(t_up, None))
    clerk = C.actor("cl", "clerk_1974", pos=[[0, 1360, 860]], scale=.9, seed=8, dir=-1, walk=False, holdF=handset(),
                    pose_keys=[[0, C.pose("relaxed", head=6)], [t_up, C.pose("relaxed", shF=150, elF=130, head=-6)],
                               [t_stop - .4, C.pose("relaxed", shF=150, elF=130, head=4, brow=-1)], [t_stop, C.pose("reach", shF=60, elF=20, brow=-1)],
                               [t_back, C.pose("reach", shF=40, elF=20)], [t_back + 1.0, C.pose("concern", head=4)], [dur, C.pose("concern", head=6)]])
    messenger = C.actor("ms", "banker_1974b", pos=[[0, 200, 1010]], scale=1.0, seed=10, dir=1, walk=False,
                        pose_keys=[[0, C.pose("relaxed", head=-4)], [t_back - .2, C.pose("relaxed", head=-6)], [t_back + .4, C.pose("reach", shF=55, elF=20)],
                                   [t_back + 1.3, C.pose("shrug")], [dur, C.pose("concern", head=4)]])
    bundle = (f'<g {C.kv(translate=[[0, 1060, 752], [t_back, 1060, 752], [t_back + 1.0, 1700, 700, 0, .7, "inout"], [t_back + 1.3, 1700, 700, 0, .7]],
                         opacity=[[0, 1], [t_back + 1.0, 1], [t_back + 1.3, 0]])}>{usd_bundle(170, 70)}</g>')
    stamp = (f'<g transform="translate(820,700)"><g {C.kv(translate=[[0, 0, -60, -8, 2.2], [t_stop - .01, 0, -60, -8, 2.2], [t_stop + .25, 0, 0, -8, 1, "out"]],
                                                       opacity=[[0, 0], [t_stop - .01, 0], [t_stop + .05, 1]])}>'
             + _r(-150, -34, 300, 68, "none", rx=8, sw=0, extra=f'stroke="{RED}" stroke-width="7"') + _t(0, 14, "SUSPENDED", 40, fill=RED, weight=700, family="Sans", extra='letter-spacing="4"')
             + "</g></g>")
    layers = [lay(z, s) for k, (z, s) in layers_.items()]
    layers.insert(2, lay(.74, clerk["svg"]))
    layers.append(lay(.82, bundle + stamp))
    layers.append(lay(.9, messenger["svg"]))
    zx = lambda x, z=.8: 960 + (x - 960) / z
    cam = [[0, zx(1100), 540, 1.0], [t_up + .2, zx(1250), 520, 1.16, "inout"], [t_stop - .3, zx(950), 600, 1.3, "inout"], [t_stop + .6, zx(850), 640, 1.42, "out"],
           [t_back - .2, zx(900), 620, 1.36, "sine"], [t_back + 1.2, zx(1150), 560, 1.12, "inout"], [dur, zx(1100), 560, 1.08, "sine"]]
    over = [title("New York", "Mid-morning, June 26, 1974", w, h, d=min(3.0, t_stop - .3)), badge("Reconstruction · not the real bank", w, h)]
    shot = dict(dur=dur, layers=layers, actors=[clerk, messenger], cam=cam, focus=[[0, .8]], dof=5, shake=.3, over=over, grade="cool", tin=("dissolve", .35))
    import sfx
    foley = [("ring", t_ring, .2, .2, dict(sec=.9)), ("clank", t_up, .12, .2, dict(pitch=200)), ("hit", t_stop + .2, .6, 0, dict(pitch=110)),
             ("paper", t_back + .1, .35, .1), ("clank", t_back + 1.1, .2, .4, dict(pitch=150))]
    amb = sfx.office_ambience(dur + .5, seed=76, busy=.6, phones=0) * .6
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_freeze(w, h, dur, ctx):
    """New York, the days after: the dealing room re-dressed for 1974. Phones ring and nobody pays first; on 'sixty'
    the board's index of the money moved through the city's settlement system falls from 100 to 40 (the BIS's
    estimated 60% fall over three days, drawn as an index, not a measured series)."""
    t60 = min(dur - 1.6, max(2.0, word_t(ctx, 3, "sixty")))
    rows = [("FUNDS MOVED, INDEX", [[0, 100], [t60 - 1.4, 100], [t60 + .4, 40]], 0, "", "", "#F6D58A")]
    ring = [(k % 7, .3 + .5 * k) for k in range(int(dur / .5))]
    cam = [[0, 700, 560, 1.04], [seg_t(ctx, 1, 0), 880, 520, 1.1, "sine"], [t60 - 1.2, 960, 440, 1.16, "inout"], [dur, 980, 430, 1.2, "sine"]]
    shot, anc = _room_shot("NEW YORK SETTLEMENT", "THE NEXT THREE DAYS · BIS ESTIMATE", rows, dur, seg_t(ctx, 1, .2), "concern", ring=ring, lifts=[],
                           phones=(0, 2, 3, 5), cam=cam, ttl=("New York", "The next three days"),
                           bdg="Reconstruction · BIS estimate, as an index", grade="cool", seed=17, tin=("dissolve", .35))
    import sfx
    foley = [("ring", t, .12, (-.6, .6)[k % 2], dict(sec=.5)) for k, (_, t) in enumerate(ring[::3])] + [("flap", t60 - 1.2, .4, 0), ("hit", t60 + .4, .45, 0, dict(pitch=110))]
    amb = sfx.office_ambience(dur + .5, seed=77, busy=1.4, phones=1.8) * .7
    return dict(shots=[shot], foley=foley, amb=amb)


def shot_pvp_swap(w, h, dur, ctx):
    """Our illustration of payment versus payment. Both bundles travel to the settlement desk in the middle at the
    same time, a latch closes, and both come out to the other side together. Then, on 'cannot occur without the
    other', a second try: the marks arrive but no dollars do, and the marks go back where they came from."""
    t_go = max(.8, seg_t(ctx, 0, .2))
    t_in = t_go + 1.6
    t_swap = t_in + .6
    t_out = t_swap + 1.6
    t_try = max(t_out + 1.0, word_t(ctx, 1, "cannot") - .6)
    t_try = min(t_try, dur - 3.2)
    fra = [[0, 9, 0], [dur, 9, dur / 6]]
    ny = [[0, 9, 0], [dur, 9, dur / 6]]
    world, front = two_cities(dur, [[0, 8, 0], [dur, 8, dur / 6]], [[0, 9, 0], [dur, 9, dur / 6]], [[0, 1]], pvp=True)   # illustrative clocks
    cx = 1700
    dm = (f'<g {C.kv(translate=[[0, 820, 700], [t_go, 820, 700], [t_in, cx - 90, 610, 0, 1, "inout"], [t_swap, cx - 90, 610], [t_swap + .5, cx + 90, 610, 0, 1, "inout"],
                                [t_out - .4, cx + 90, 610], [t_out + .6, 2900, 700, 0, 1, "inout"], [dur, 2900, 700]],
                     opacity=[[0, 1]])}>{mark_bundle(140, 60, 1.4)}</g>')
    usd = (f'<g {C.kv(translate=[[0, 2900, 640], [t_go, 2900, 640], [t_in, cx + 90, 560, 0, 1, "inout"], [t_swap, cx + 90, 560], [t_swap + .5, cx - 90, 560, 0, 1, "inout"],
                                 [t_out - .4, cx - 90, 560], [t_out + .6, 820, 640, 0, 1, "inout"], [dur, 820, 640]],
                      opacity=[[0, 1]])}>{usd_bundle(140, 60, 1.4)}</g>')
    dm2 = (f'<g {C.kv(translate=[[0, 820, 760], [t_try, 820, 760], [t_try + 1.2, cx - 90, 690, 0, 1, "inout"], [t_try + 2.0, cx - 90, 690], [t_try + 3.0, 820, 760, 0, 1, "inout"]],
                      opacity=[[0, 0], [t_try - .3, 0], [t_try, 1]])}>{mark_bundle(140, 60, 1.4)}</g>')
    latch = (f'<g transform="translate({cx},640)"><g {C.kv(opacity=[[0, 0], [t_in - .1, 0], [t_in, 1], [t_out - .5, 1], [t_out - .3, 0]])}>'
             + _r(-30, -26, 60, 46, RED, rx=6, sw=3) + f'<path d="M-18,-26 v-14 a18 18 0 0 1 36 0 v14" fill="none" stroke="{INK}" stroke-width="6"/></g></g>')
    tag = kt(_r(cx - 330, 180, 660, 100, PAPER, rx=10, sw=3) + _t(cx, 244, "BOTH, OR NEITHER", 46, fill=RED, family="Sans", weight=700), None, t_out)
    no_usd = kt(_r(cx + 160, 720, 360, 70, PAPER, rx=8, sw=3) + _t(cx + 340, 766, "NO DOLLARS", 30, fill=RED, family="Sans", weight=700), None, t_try + 1.0)
    z = .75
    zx = lambda x: 960 + (x - 960) / z
    cam = [[0, zx(cx), 580, .5], [t_go, zx(cx), 580, .52, "sine"], [t_in, zx(cx), 540, .86, "inout"], [t_out + .4, zx(cx), 540, .9, "sine"],
           [t_out + 1.0, zx(cx), 580, .5, "inout"], [t_try + 1.0, zx(cx - 300), 580, .66, "inout"], [dur, zx(cx - 300), 580, .64, "sine"]]
    ck = [C.actor("pf", "clerk_1974", pos=[[0, 600, 860]], scale=.86, seed=21, dir=1, walk=False,
                  pose_keys=[[0, C.pose("relaxed")], [t_go - .2, C.pose("reach", shF=64, elF=14)], [t_go + .8, C.pose("relaxed", head=-8)],
                             [t_out + .4, C.pose("reach", shF=60, elF=18)], [t_out + 1.2, C.pose("cheer")], [t_try + 2.6, C.pose("concern")], [dur, C.pose("relaxed")]]),
          C.actor("pn", "clerk_1974b", pos=[[0, 3100, 860]], scale=.86, seed=22, dir=-1, walk=False,
                  pose_keys=[[0, C.pose("relaxed")], [t_go - .2, C.pose("reach", shF=64, elF=14)], [t_go + .8, C.pose("relaxed", head=-8)],
                             [t_out + .4, C.pose("reach", shF=60, elF=18)], [t_out + 1.2, C.pose("cheer")], [t_try + 1.2, C.pose("shrug")], [dur, C.pose("relaxed")]])]
    layers = [lay(z, world, noblur=True), lay(z + .01, "".join(a["svg"] for a in ck)), lay(z + .02, front), lay(z + .04, dm + usd + dm2 + latch + tag + no_usd)]
    over = [badge("Our illustration · payment versus payment", w, h)]
    shot = dict(dur=dur, layers=layers, actors=ck, cam=cam, focus=[[0, z + .02]], dof=2, shake=.2, over=over, grade="warm", tin=("dissolve", .35))
    import sfx
    foley = [("paper", t_go, .3, -.4), ("paper", t_go + .05, .3, .4), ("clank", t_in, .3, 0, dict(pitch=220)), ("hit", t_swap + .5, .4, 0, dict(pitch=196)),
             ("clank", t_out - .4, .25, 0, dict(pitch=180)), ("paper", t_try, .3, -.3), ("hit", t_try + 1.4, .35, 0, dict(pitch=110)), ("paper", t_try + 2.2, .3, -.3)]
    amb = sfx.room_tone(dur + .5, seed=78, clock=False, street=.12) * .6
    return dict(shots=[shot], foley=foley, amb=amb)


SHOTS = dict(clocks_hook=shot_clocks_hook, two_legs=shot_two_legs, ny_suspend=shot_ny_suspend, freeze=shot_freeze, pvp_swap=shot_pvp_swap)
