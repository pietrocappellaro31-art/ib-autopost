"""
Reel, 27 Nov 2026 (slot B, 18:00 ET): the first full-frame animated Reel (build/reel_film.py, Pietro 26 Nov).
A story in one interview room: the superday question "depreciation goes up by $10, what happens to cash?", the
answer most candidates give (cash falls $10), why it is wrong, and the payoff (cash rises $2.50).

Narrator HEART (Kokoro af_heart, en-us, 0.9). Voice and effects only in the file: the music is a trending licensed
track Instagram attaches at posting (publish.py, Audio API). Characters, room and bank are invented.

Every number worked (the standard interview assumptions, said in the caption: a 25% tax rate, tax follows the
books, nothing else changes):
    Depreciation +10                     an expense that is not a payment
    Profit before tax: -10
    Tax at 25%: 10 x 25% = 2.50 less     (tax paid falls 2.50)
    Net income: -10 + 2.50 = -7.50
    Cash flow statement: net income -7.50, add back depreciation +10: -7.50 + 10 = +2.50
    Balance sheet check: PP&E -10, cash +2.50: assets -7.50; retained earnings -7.50: balances.
    In coins worth $2.50 each: 3 coins out (7.50), 4 coins in (10.00), net 1 coin (+2.50).
Close (asked, not answered): interest +10 instead: net income -7.50 and interest is paid in cash, so cash -7.50.

Story (26 Nov storytelling rules, docs/production/reel-film-standard.md):
    hook (said and shown in 2 s): a superday question, and on screen "An expense that ADDS cash?"
    the wrong answer most people give, struck out
    the mechanism, written on the board as it is said
    the turn: no cash left the company; the add-back
    the payoff in one number, counted up in coins and on screen
    the meaning in one line, then the question back to the viewer (comment bait that loops to the start)

    python3 build/reelf_depreciation.py            stills (fast look)
    python3 build/reelf_depreciation.py render     the Reel, its clean master and checks
"""

import json
import sys

import cine as C
import cine_lib as L
from reel_film import (W, H, lay, cam_x, cam_y, shot, hook, big_number, narration, beats, at_word, captions,
                       interview_room, marker_text, film, full_frame_check, sound, INK, RED, TEAL, MUSTARD, GREEN, _r)

SLUG = "w3-depreciation-cash"
LINES = [
    "Superday. The interviewer leans in: depreciation goes up by ten dollars. What happens to cash?",
    "Most candidates say cash falls by ten. That's wrong.",
    "Depreciation is an expense, so profit before tax falls by ten. At a twenty-five percent tax rate, "
    "the tax bill falls by two fifty, and net income falls by seven fifty.",
    "But depreciation isn't a payment. No cash left the company, so the cash flow statement adds the ten back.",
    "Minus seven fifty, plus ten. Cash goes up by two fifty.",
    "The only cash that moved is the tax you didn't pay.",
    "Your turn: interest goes up by ten instead. What happens to cash? Tell me in the comments.",
]
HOLDS = {4: .5}                    # a beat of air after the payoff

CAND, INTV = "modern_grey", "modern_navy"
BX, BY, BW, BH = 760, 220, 400, 480        # the whiteboard (layer z .55), above the two heads
BOARD = [("DEPRECIATION", "+$10", INK), ("Profit before tax", "-10", RED), ("Tax (25%)", "-2.50", TEAL),
         ("Net income", "-7.50", RED)]


def room_layers(board_svg, cand, intv, thought="", extra_near=""):
    lay_, anc = interview_room()
    z = {k: v[0] for k, v in lay_.items()}
    layers = [lay(z["wall"], lay_["wall"][1]),
              lay(.55, _board_frame() + board_svg),
              lay(z["floor"], lay_["floor"][1]), lay(z["chairs"], lay_["chairs"][1]),
              lay(.8, cand["svg"] + intv["svg"]),
              lay(.82, thought),
              lay(z["table"], lay_["table"][1] + f'<g transform="translate(900,925)">{_folder()}</g>')]
    if extra_near:
        layers.append(lay(1.2, extra_near))
    return layers, anc


def _board_frame():
    return (_r(BX, BY, BW, BH, "#FBFAF7", rx=10, sw=5)
            + f'<rect x="{BX}" y="{BY + BH - 8}" width="{BW}" height="18" rx="4" fill="#9AA0A8" stroke="{INK}" stroke-width="3"/>'
            + _r(BX + BW - 120, BY + BH - 24, 64, 14, RED, rx=4, sw=2) + _r(BX + BW - 200, BY + BH - 24, 64, 14, TEAL, rx=4, sw=2))


def _folder():
    return (f'<g transform="skewX(-30)">{_r(-60, -10, 140, 10, "#2E4A5A", rx=2, sw=2.4)}</g>'
            + f'<g transform="translate(30,-10) skewX(-30)">{_r(-40, -6, 100, 6, "#F7F5F2", rx=1, sw=1.6)}</g>')


def board_svg(times, circle_at=None):
    """The board's lines; times[i] = (t0, t1) shot seconds when line i is inked, None = not yet, 'done' = already."""
    out = ""
    for i, ((lab, val, col), tt) in enumerate(zip(BOARD, times)):
        if tt is None:
            continue
        t0, t1 = (0, 0) if tt == "done" else tt
        y = BY + 62 + i * 108
        big = i == 0
        out += marker_text(f"bl{i}", BX + 26, y, lab, 34 if big else 29, INK, t0, t0 + (t1 - t0) * .6, weight=700 if big else 600)
        out += marker_text(f"bv{i}", BX + BW - 26, y + (44 if not big else 50), val, 46 if not big else 58, col, t0 + (t1 - t0) * .55, t1,
                           anchor="end", family="Serif")
        if 0 < i < 3:
            out += f'<path d="M{BX + 26},{y + 66} L{BX + BW - 26},{y + 66}" stroke="#D9D3C7" stroke-width="3"/>'
    if circle_at is not None:
        y = BY + 62 + 2 * 108 + 28
        out += (f'<ellipse cx="{BX + BW - 80}" cy="{y}" rx="90" ry="46" fill="none" stroke="{RED}" stroke-width="7" '
                f'transform="rotate(-4 {BX + BW - 80} {y})" {C.kv(dash=[[0, 0], [circle_at, 0], [circle_at + .6, 1]])}/>')
    return out


_N = [0]


def people(t_talk=(), cand_pose=None, intv_pose=None, cand_seed=2, intv_seed=5):
    """26 Nov, first stills: every shot needs its own figure ids (the runtime animates the first element with an id,
    so a second shot reusing "cand" showed an empty chair)."""
    _N[0] += 1
    n = _N[0]
    seat = lambda name, **o: C.pose("seated", **{**C.POSES.get(name, {}), **o})
    ip = intv_pose or [[0, seat("talk_b", lean=10, head=4)]]
    for a, b in t_talk:                      # mouth and hands while he asks
        k = a
        while k < b:
            ip.append([round(k, 3), seat("talk_a", lean=12)])
            ip.append([round(k + .22, 3), seat("talk_b", lean=12)])
            k += .44
    ip.sort(key=lambda x: x[0])
    cp = cand_pose or [[0, seat("relaxed", head=2)]]
    cand = C.actor(f"cand{n}", CAND, pos=[[0, 760, 1060]], pose_keys=cp, dir=1, walk=False, seed=cand_seed, scale=1.0)
    intv = C.actor(f"intv{n}", INTV, pos=[[0, 1160, 1060]], pose_keys=ip, dir=-1, walk=False, seed=intv_seed, scale=1.0)
    return cand, intv


def coin_side(fill=MUSTARD):
    return (f'<ellipse cx="0" cy="10" rx="74" ry="20" fill="#B88A2E" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-74" y="0" width="148" height="10" fill="#B88A2E"/>'
            f'<ellipse cx="0" cy="0" rx="74" ry="20" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
            f'<text x="0" y="8" font-family="\'Sans\',sans-serif" font-weight="700" font-size="22" text-anchor="middle" fill="{INK}">$2.50</text>')


# ----------------------------------------------------------------------------------------------- the shots

def s0(b, d):
    t_ten = at_word(b, 0, "ten", 0)
    t_cash = at_word(b, 0, "cash?", 0)
    cand, intv = people(t_talk=[(at_word(b, 0, "depreciation", 0), t_cash + .4)])
    layers, anc = room_layers(board_svg([(t_ten - .9, t_ten + .5), None, None, None]), cand, intv)
    # open close on the interviewer as he leans in, pull back to the room as the board is written on
    cam = [[0, cam_x(1130, .8), cam_y(760, .8), 1.75], [max(1.0, t_ten - 1.1), cam_x(1110, .8), cam_y(740, .8), 1.6, "sine"],
           [t_ten + .2, cam_x(960, .8), cam_y(730, .8), 1.02, "inout"], [d, cam_x(960, .8), cam_y(720, .8), 1.06, "sine"]]
    over = [hook([[("An expense", False)], [("that ", False), ("ADDS", True)], [("cash?", True)]], at=0, d=max(2.4, t_ten - 1.1), top=230, size=120)]
    fx = [("marker", t_ten - .9, .5, .2, dict(sec=1.3)), ("hit", t_cash, .3, 0, dict(pitch=262))]
    return shot(d, layers, [cand, intv], cam, over, tin=("cut", 0)), fx


def s1(b, d):
    t_falls = at_word(b, 1, "falls", 1)
    t_wrong = at_word(b, 1, "wrong.", 1)
    seat = lambda name, **o: C.pose("seated", **{**C.POSES.get(name, {}), **o})
    cp = [[0, seat("relaxed", head=0, mouth=1, brow=.6)], [t_falls, seat("shrug", mouth=1, brow=.8)],
          [t_wrong, seat("concern")], [d, seat("concern", head=8)]]
    cand, intv = people(cand_pose=cp)
    # the thought over his head: CASH -$10, then struck out
    tx, ty = 800, 590
    thought = (f'<g {C.kv(opacity=[[0, 0], [t_falls - .1, 0], [t_falls + .2, 1]], translate=[[0, tx, ty + 20, 0, .42], [t_falls - .1, tx, ty + 20, 0, .42], [t_falls + .35, tx, ty, 0, .6, "out"]])}>'
               f'<circle cx="40" cy="190" r="12" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="20" cy="150" r="20" fill="#fff" stroke="{INK}" stroke-width="4"/>'
               f'<rect x="-190" y="-90" width="380" height="200" rx="90" fill="#fff" stroke="{INK}" stroke-width="5"/>'
               f'<text x="0" y="-12" font-family="\'Sans\',sans-serif" font-weight="700" font-size="40" letter-spacing="4" text-anchor="middle" fill="{INK}">CASH</text>'
               f'<text x="0" y="74" font-family="\'Serif\',serif" font-weight="700" font-size="92" text-anchor="middle" fill="{INK}">-$10</text>'
               f'<path d="M-160,40 L160,0" stroke="{RED}" stroke-width="16" stroke-linecap="round" {C.kv(dash=[[0, 0], [t_wrong, 0], [t_wrong + .3, 1]])}/></g>')
    layers, anc = room_layers(board_svg(["done", None, None, None]), cand, intv, thought)
    cam = [[0, cam_x(780, .8), cam_y(720, .8), 2.0], [d, cam_x(785, .8), cam_y(715, .8), 2.12, "sine"]]
    from motion import A
    over = [A(A(f'<div style="font-family:Serif,serif;font-weight:700;font-size:150px;color:{RED};text-shadow:0 0 4px #000,0 6px 24px rgba(0,0,0,.7)">WRONG</div>',
                "stamp", t_wrong, .35, rot=-8), "life", 0, d, style="position:absolute;left:0;right:0;top:760px;text-align:center", fi=.01, fo=.2)]
    fx = [("paper", t_falls, .25, -.3, dict(sec=.3, crisp=.6)), ("stamp", t_wrong, .55, 0), ("quill", t_wrong, .3, 0, dict(sec=.3, rate=4))]
    return shot(d, layers, [cand, intv], cam, over, tin=("cut", 0)), fx


def s2(b, d):
    t_pre = at_word(b, 2, "profit", 2)
    t_tax = at_word(b, 2, "bill", 2) - .5
    t_net = at_word(b, 2, "net", 2)
    times = ["done", (t_pre, t_pre + 1.2), (t_tax, t_tax + 1.2), (t_net, t_net + 1.2)]
    cand, intv = people()
    layers, anc = room_layers(board_svg(times), cand, intv)
    bcx, bcy = BX + BW / 2, BY + BH / 2
    # 26 Nov: the board's top at about screen y 60 and its bottom above the caption band
    cam = [[0, cam_x(bcx - 14, .55), cam_y(560, .55), 1.8], [d * .5, cam_x(bcx + 6, .55), cam_y(584, .55), 1.88, "sine"],
           [d, cam_x(bcx + 16, .55), cam_y(600, .55), 1.95, "sine"]]
    fx = [("marker", t, .55, .1, dict(sec=1.1)) for t in (t_pre, t_tax, t_net)]
    return shot(d, layers, [cand, intv], cam, [], tin=("cut", 0), shake=.15), fx


def desk_world(t_rows, coin_events, counter, gain_at=None):
    """A close shot on the table: the cash flow statement on a sheet, and the company's cash as a stack of coins."""
    wood = ('<rect x="-2600" y="-1600" width="7200" height="4200" fill="#8A6446"/>'
            + "".join(f'<path d="M-2600,{-1600 + k * 46} C-800,{-1580 + k * 46} 1200,{-1630 + k * 46} 4600,{-1600 + k * 46}" fill="none" '
                      f'stroke="#7A5639" stroke-width="{2 + (k % 3)}" opacity=".7"/>' for k in range(90)))
    sx, sy = 680, 50
    sheet = (f'<g transform="rotate(-3 {sx + 280} {sy + 300})">'
             + f'<rect x="{sx + 10}" y="{sy + 12}" width="560" height="390" fill="#000" opacity=".25"/>'
             + _r(sx, sy, 560, 390, "#FBFAF7", rx=4, sw=3)
             + f'<text x="{sx + 34}" y="{sy + 70}" font-family="\'Sans\',sans-serif" font-weight="700" font-size="34" letter-spacing="3" fill="{INK}">CASH FLOW STATEMENT</text>'
             + f'<path d="M{sx + 34},{sy + 96} L{sx + 526},{sy + 96}" stroke="{INK}" stroke-width="3"/>')
    rows = [("Net income", "-7.50", RED), ("+ Depreciation", "+10.00", GREEN)]
    for i, ((lab, val, col), tt) in enumerate(zip(rows, t_rows)):
        if tt is None:
            continue
        t0, t1 = (-2, -2) if tt == "done" else tt
        y = sy + 190 + i * 120
        sheet += marker_text(f"cr{i}", sx + 34, y, lab, 40, INK, t0, t0 + .5, family="Sans", weight=600)
        sheet += marker_text(f"cv{i}", sx + 526, y, val, 52, col, t0 + .3, t1, anchor="end", family="Serif")
        if i == 1:
            sheet += f'<path d="M{sx + 300},{y + 36} L{sx + 526},{y + 36}" stroke="{INK}" stroke-width="3" {C.kv(opacity=[[0, 0], [t1, 0], [t1 + .2, 1]])}/>'
    sheet += "</g>"
    # 26 Nov: the cash sits beside its label, not under it, so the band above the captions stays wood
    base_x, base_y = 1095, 700
    coins = ""
    top = 6
    for k in range(6):
        y = base_y - k * 24
        ev = [e for e in coin_events if e[0] == "out" and e[2] == k]
        if ev:
            t = ev[0][1]
            coins += f'<g {C.kv(translate=[[0, base_x, y, 0, 1.15], [t, base_x, y, 0, 1.15], [t + .55, base_x + 700, y - 420, 30, 1.15, "in"]])}>{coin_side()}</g>'
        else:
            coins += f'<g transform="translate({base_x},{y}) scale(1.15)">{coin_side()}</g>'
    n_out = sum(1 for e in coin_events if e[0] == "out")
    for j, e in enumerate([e for e in coin_events if e[0] == "in"]):
        t = e[1]
        y = base_y - (top - n_out + j) * 24
        coins += f'<g {C.kv(translate=[[0, base_x + 40, y - 900, 0, 1.15], [t, base_x + 40, y - 900, 0, 1.15], [t + .45, base_x, y, 0, 1.15, "out"]], opacity=[[0, 0], [t, 0], [t + .05, 1]])}>{coin_side()}</g>'
    lx = 850
    lab = (f'<text x="{lx}" y="{520}" font-family="\'Sans\',sans-serif" font-weight="700" font-size="30" letter-spacing="3" text-anchor="middle" fill="#F7F5F2">THE COMPANY\'S</text>'
           f'<text x="{lx}" y="{556}" font-family="\'Sans\',sans-serif" font-weight="700" font-size="30" letter-spacing="3" text-anchor="middle" fill="#F7F5F2">CASH</text>')
    c0, c1, ta = counter
    lab += (f'<text x="{lx}" y="{636}" font-family="\'Serif\',serif" font-weight="700" font-size="68" text-anchor="middle" '
            f'fill="{MUSTARD}" data-pre="$" data-dec="2" {C.kv(count=[[0, c0], [ta, c0], [ta + 1.0, c1]])}>${c0:.2f}</text>')
    if gain_at is not None:
        lab += (f'<g {C.kv(opacity=[[0, 0], [gain_at, 0], [gain_at + .15, 1]], translate=[[0, lx, 730, 0, .6], [gain_at, lx, 730, 0, .6], [gain_at + .35, lx, 730, 0, 1, "out"]])}>'
                f'<text x="0" y="0" font-family="\'Serif\',serif" font-weight="700" font-size="84" text-anchor="middle" fill="#7BE08F" '
                f'stroke="{INK}" stroke-width="3" paint-order="stroke">+$2.50</text></g>')
    return [lay(.5, wood), lay(.8, sheet), lay(.9, coins + lab)]


def s3(b, d):
    t_cfs = at_word(b, 3, "flow", 3) - .2
    t_back = at_word(b, 3, "adds", 3)
    t_no = at_word(b, 3, "no", 3)
    layers = desk_world([(t_cfs, t_cfs + .9), (t_back, t_back + .8)], [], (15.0, 15.0, d))
    # "No cash left": a red cross over an arrow leaving the stack
    from motion import A
    cross = (f'<svg width="1080" height="400" viewBox="0 0 1080 400" style="position:absolute;left:0;top:1010px">'
             f'<path d="M800,190 L1020,110" stroke="#fff" stroke-width="14" stroke-linecap="round" {C.kv(dash=[[0, 0], [t_no, 0], [t_no + .35, 1]])}/>'
             f'<path d="M986,92 L1030,106 L1000,142" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" {C.kv(opacity=[[0, 0], [t_no + .3, 0], [t_no + .4, 1]])}/>'
             f'<g {C.kv(opacity=[[0, 0], [t_no + .5, 0], [t_no + .6, 1]])}><path d="M850,80 L970,200 M970,80 L850,200" stroke="{RED}" stroke-width="22" stroke-linecap="round"/></g></svg>')
    over = [A(cross, "life", 0, d, fi=.01, fo=.2)]
    cam = [[0, cam_x(930, .8), cam_y(500, .8), 1.0], [d, cam_x(985, .8), cam_y(560, .8), 1.13, "sine"]]
    fx = [("paper", .05, .3, 0, dict(sec=.5, crisp=.8)), ("marker", t_cfs, .5, -.1, dict(sec=.9)), ("hit", t_no + .5, .35, -.2, dict(pitch=131)),
          ("marker", t_back, .5, -.1, dict(sec=.8))]
    return shot(d, layers, [], cam, over, tin=("cut", 0), shake=.15, vig=.3), fx


def s4(b, d):
    t_minus = at_word(b, 4, "minus", 4)
    t_plus = at_word(b, 4, "plus", 4)
    t_up = at_word(b, 4, "up", 4)
    outs = [("out", t_minus + .15 + k * .22, 5 - k) for k in range(3)]
    ins = [("in", t_plus + .1 + k * .22, None) for k in range(4)]
    layers = desk_world(["done", "done"], outs + ins, (15.0, 17.5, t_up), gain_at=t_up + .2)
    over = []
    cam = [[0, cam_x(985, .8), cam_y(560, .8), 1.13], [t_up, cam_x(930, .9), cam_y(640, .9), 1.42, "inout"], [d, cam_x(935, .9), cam_y(645, .9), 1.46, "sine"]]
    fx = [("clink", t, .5, -.3, dict(glass=False)) for _, t, _ in outs] + [("clink", t + .45, .55, .2, dict(glass=False)) for _, t, _ in ins]
    fx += [("hit", t_up, .5, 0, dict(pitch=330))]
    return shot(d, layers, [], cam, over, tin=("cut", 0), shake=.15, vig=.3), fx


def s5(b, d):
    t_tax = at_word(b, 5, "tax", 5)
    seat = lambda name, **o: C.pose("seated", **{**C.POSES.get(name, {}), **o})
    cp = [[0, seat("relaxed", mouth=1, brow=.5, head=-2)], [d, seat("relaxed", mouth=1, brow=.6, head=-4)]]
    ip = [[0, seat("relaxed", head=4)], [t_tax, seat("relaxed", head=12, mouth=1)], [t_tax + .35, seat("relaxed", head=0, mouth=1)],
          [t_tax + .7, seat("relaxed", head=12, mouth=1)], [d, seat("relaxed", head=2, mouth=1)]]
    cand, intv = people(cand_pose=cp, intv_pose=ip)
    layers, anc = room_layers(board_svg(["done"] * 4, circle_at=t_tax - .2), cand, intv)
    cam = [[0, cam_x(960, .8), cam_y(750, .8), 1.0], [d, cam_x(960, .8), cam_y(740, .8), 1.08, "sine"]]
    fx = [("marker", t_tax - .2, .45, .2, dict(sec=.6))]
    return shot(d, layers, [cand, intv], cam, [], tin=("cut", 0)), fx


def s6(b, d):
    t_int = at_word(b, 6, "interest", 6)
    t_q = at_word(b, 6, "what", 6)
    seat = lambda name, **o: C.pose("seated", **{**C.POSES.get(name, {}), **o})
    ip = [[0, seat("relaxed", head=0)], [t_int - .2, seat("point", lean=8, head=-4, brow=.6)], [d, seat("point", lean=8, head=-6, brow=.6)]]
    cand, intv = people(intv_pose=ip)
    # the board is wiped and the next question written on it
    wipe = (f'<rect x="{BX + 6}" y="{BY + 6}" width="{BW - 12}" height="{BH - 30}" fill="#FBFAF7" '
            f'{C.kv(clip=[[0, 0, 100, 0, 0], [.1, 0, 100, 0, 0], [.7, 0, 0, 0, 0, "inout"]])}/>')
    nxt = (marker_text("ni0", BX + 26, BY + 120, "INTEREST", 44, INK, t_int, t_int + .5, weight=700)
           + marker_text("ni1", BX + BW - 26, BY + 200, "+$10", 72, RED, t_int + .4, t_int + .9, anchor="end", family="Serif")
           + marker_text("ni2", BX + 26, BY + 330, "CASH?", 72, TEAL, t_q, t_q + .6, family="Serif"))
    layers, anc = room_layers(board_svg(["done"] * 4) + wipe + nxt, cand, intv)
    cam = [[0, cam_x(1030, .8), cam_y(700, .8), 1.15], [d, cam_x(1040, .8), cam_y(690, .8), 1.28, "sine"]]
    over = []
    fx = [("paper", .1, .3, .1, dict(sec=.6, crisp=.4)), ("marker", t_int, .5, .1, dict(sec=.9)), ("marker", t_q, .5, .1, dict(sec=.6))]
    return shot(d, layers, [cand, intv], cam, over, tin=("cut", 0)), fx


def build():
    work = C.OUT / SLUG
    work.mkdir(parents=True, exist_ok=True)
    voice = narration(LINES, work)
    b = beats(voice, HOLDS)
    shots, events = [], []
    for i, fn in enumerate((s0, s1, s2, s3, s4, s5, s6)):
        s, fx = fn(b, b["durs"][i])
        shots.append(s)
        events += [(e[0], round(e[1] + b["shot_starts"][i], 3), *e[2:]) for e in fx]
    html, total = film(shots, captions(voice, b))
    json.dump(dict(beats=b, voice=[dict(text=m["text"], heard=m["heard"], wer=m["wer"], dur=m["dur"]) for m in voice]),
              open(work / "cues.json", "w"), indent=1)
    return html, total, work, voice, b, events


if __name__ == "__main__":
    html, total, work, voice, b, events = build()
    print(f"total {total:.1f} s; lines wer: {[round(m['wer'], 3) for m in voice]}")
    mids = [round(s + d * k, 2) for s, d in zip(b["shot_starts"], b["durs"]) for k in (.15, .8)]
    if "render" not in sys.argv:
        pngs = C.stills(html, mids, work, "still", W, H)
        print(json.dumps(full_frame_check(pngs), indent=0))
    else:
        mp4, secs = C.render(html, total, work, SLUG, W, H, fps=30, workers=4)
        rep = sound(work, SLUG, voice, b, events)
        pngs = C.stills(html, mids, work, "still", W, H)
        rep["full_frame"] = full_frame_check(pngs)
        rep["render_seconds"] = round(secs, 1)
        json.dump(rep, open(work / "report.json", "w"), indent=1, default=str)
        m = rep["masters"]["clean"]
        print({k: m.get(k) for k in ("file", "lufs", "true_peak", "clipped_samples", "dnsmos", "wer_of_master")})
        print("full frame:", all(x["ok"] for x in rep["full_frame"]))
