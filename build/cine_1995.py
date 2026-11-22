"""
Filmed beats for YouTube #15, Barings, February 1995 (22 Nov 2026). Sets, props and shots for build/cine.py, used by
build/youtube_ep015.py as kind="cine" beats.

cinematic-standard.md section 8. Step 4 (data in the world), the 20 Nov "next improvement": a balance sheet that
rearranges as a filmed beat (balance_board: the bank's capital and the hidden losses drawn on one true scale; the
losses grow as they are said, then slide across onto the capital and eat it, the rest hanging below zero). Step 3
(sets): a trading floor, the next set the build order names (a futures pit of 1995: stepped rings, traders in
coloured jackets whose arms signal all the time, a price board that takes content, booths with phones and CRTs,
clocks); a back office of 1995 in Singapore (a big CRT that takes content, a fax, filing cabinets, a ceiling fan, a
window at dusk); London at night reuses cine_1998's panelled room with a new easel that takes content.

Sets (our own generic drawings: no exchange's or bank's name, logo, building or person; everything is badged):
  pit_1995(board, clock_path, dur)  a futures trading floor: the board 1300 x 430 at x 310..1610, y 60..490 (z .4)
                     takes content; three clocks; booths left and right; the pit's rings (z .6); feet 905 (back
                     row, z .66) and 1000 (front row, z .74); a rail in front (z .9)
  back_office_1995(screen)  an office at dusk: a CRT whose screen (664 x 440) takes content, centred at x 700 on a
                     desk at y 880 (z .86); a seat at (1240, 1010)
  easel(content)     a flip-chart easel, its board 900 x 600; content drawn in the board's box
Props: balance_board() (capital against losses on a true scale, rearranging), pit_board() (rows that count).
People: pit_traders() (arms that signal on their own rhythm; at react_at they turn to the board and slump or point).

Shots (fn(w, h, dur, ctx) -> dict(shots, foley, amb)):
  hook_827      frame 0: the board fills the frame and LOST BY ONE TRADER counts from £0 to £827M by 1.4 s; THE
                BANK'S CAPITAL ABOUT £350M lands; on the question the camera pulls back onto the pit, traders
                signalling
  pit_floor     1992 (reconstruction): a trader in a blue jacket crosses the floor and steps into the pit; the board
                lists NIKKEI 225 FUTURES, SINGAPORE and OSAKA (no prices: illegible ticks)
  acct_88888    the back office: the CRT types NEW ACCOUNT 88888, OPENED 3 JULY 1992, FOR ERROR TRADES
  hidden_1/2    London at night: the CRT draws the losses in 88888 (end 1993 over £20M, end 1994 over £200M), then
                the draft 1994 accounts' pre-tax profit, £102M, beside them (a scene across two beats)
  tally_1/2     our example of selling insurance: £1 a day for 99 calm days (+£99), then day 100 pays out £150
                (-£51); the CRT counts days and pounds on the words
  funding_1/2   London at night, the easel: "lent to clients" more than £300M against clients' collateral about
                £31M, then funding to Singapore twice the group's capital
  kobe_fall     January 1995: the board reads EARTHQUAKE AT KOBE, 17 JANUARY; NIKKEI 225 counts down to 17,785
                (23 January) past HIS LINE 19,000; the pit slumps
  capital_1/2   the balance sheet that rearranges (the 20 Nov next improvement): capital about £350M on the
                right; the losses grow on the left (£20M, £200M, £827M); part 2 slides them onto the capital
Facts on screen come only from the sources in youtube_ep015.py's docstring. Nobody speaks; nobody is a likeness.
"""

import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402
from cine_1907 import lay, badge, seg_t, word_t   # noqa: E402,F401
from cine_1920 import title                       # noqa: E402
from cine_1971 import kt, desk_phone, handset      # noqa: E402,F401
from cine_1974 import wall_clock                  # noqa: E402
from cine_1998 import crt, boardroom_1998, _ticker_lines   # noqa: E402
from cine_2021 import _fold, _ktf                 # noqa: E402
from cine_2023 import find_t, _alive, rows_screen  # noqa: E402

INK, RED, TEAL, MUSTARD, PAPER = C.INK, C.RED, C.TEAL, C.MUSTARD, "#F7F5F2"
_r, _t = L._r, L._t
LIGHT, DIM = "#F4F1EA", "#8FA3A8"
BOARD = "#14181C"
SCREEN95 = "#0F2A24"                                                             # cine_1998.SCREEN

C.LOOKS.update({
    # 22 Nov, YouTube #15 (1995): exchange trading jackets in plain colours (generic; no badge, no exchange's colours),
    # one red jacket in the crowd at most; office clothes of 1995.
    "pit_95_blue": dict(coat="#3A5DA8", coat2="#2C4884", vest="#F2F2F2", legs="#2B2F3A", stock="#2B2F3A", shoe=INK, skin="#EBC2A0",
                        hair="#6A4A30", hat="", style="suit", cuff="#3A5DA8", tie="#2C4884", era="1971"),
    "pit_95_teal": dict(coat=TEAL, coat2="#0B5A54", vest="#F2F2F2", legs="#2B2F3A", stock="#2B2F3A", shoe=INK, skin="#C98E68",
                        hair="#14100D", hat="", style="suit", cuff=TEAL, tie="#0B5A54", era="1971"),
    "pit_95_mus": dict(coat="#D9A83A", coat2="#B88A28", vest="#F2F2F2", legs="#33363E", stock="#33363E", shoe=INK, skin="#E8BC9A",
                       hair="#2A1E18", hat="", style="suit", cuff="#D9A83A", tie="#B88A28", era="1971"),
    "pit_95_green": dict(coat="#3F7A5A", coat2="#2F6048", vest="#F2F2F2", legs="#2B2F3A", stock="#2B2F3A", shoe=INK, skin="#9A6444",
                         hair="#14100D", hat="", style="suit", cuff="#3F7A5A", tie="#2F6048", era="1971"),
    "pit_95_grey": dict(coat="#7A8088", coat2="#61666D", vest="#F2F2F2", legs="#2B2F3A", stock="#2B2F3A", shoe=INK, skin="#F0C7A4",
                        hair="#8A6A4A", hat="", style="suit", cuff="#7A8088", tie="#61666D", era="1971"),
    "pit_95_red": dict(coat=RED, coat2="#A92C0D", vest="#F2F2F2", legs="#2B2F3A", stock="#2B2F3A", shoe=INK, skin="#E5B391",
                       hair="#3A2A20", hat="", style="suit", cuff=RED, tie="#A92C0D", era="1971"),
    "office_1995": dict(coat="#2E3442", coat2="#222733", vest="#EEF1F4", legs="#2E3442", stock="#2E3442", shoe=INK, skin="#E8BC9A",
                        hair="#5A3A28", hat="", style="suit", cuff="#EEF1F4", tie="#7A2E1C", era="1971"),
    "office_1995b": dict(coat="#5B4636", coat2="#46362A", vest="#F4EFE4", legs="#3A332E", stock="#3A332E", shoe=INK, skin="#C98E68",
                         hair="#14100D", hat="", style="suit", cuff="#F4EFE4", tie=TEAL, era="1971"),
    "clerk_1995": dict(coat="#E9E4DA", coat2="#D2CCBF", vest="#F7F5F2", legs="#3B3F4A", stock="#3B3F4A", shoe=INK, skin="#D9A684",
                       hair="#14100D", hat="", style="suit", cuff="#F7F5F2", tie="#3E4F66", era="1971"),
})
PIT_LOOKS = ("pit_95_teal", "pit_95_mus", "pit_95_green", "pit_95_grey", "pit_95_mus", "pit_95_teal", "pit_95_grey", "pit_95_green",
             "pit_95_red", "pit_95_teal")


# ------------------------------------------------------------------------------------------------ props

def pit_board(rows, x0=60, y0=150, step=96, wid=1180, size=40):
    """Board rows that light up and count at their times: (label, value text or None, colour, t, count keys or None,
    (dec, pre, suf))."""
    return rows_screen(rows, x0=x0, y0=y0, step=step, wid=wid, size=size)


def _ticks(x0, y0, n, wid, seed=0):
    """Illegible flickering price ticks (no number is shown that is not sourced)."""
    rng = random.Random(seed)
    s = ""
    for k in range(n):
        y = y0 + k * 34
        s += "".join(f'<rect x="{x0 + j * 46}" y="{y}" width="34" height="18" fill="#6FD3A8" opacity=".5" '
                     f'data-flick=\'[0.5,0.35,{(k * 7 + j) % 11}]\'/>' for j in range(int(wid / 46)) if rng.random() < .8)
    return s


def balance_board(t_cap, t_loss, t_move=None, w=900, h=600, scale=.30, part=1):
    """The balance sheet that rearranges (cinematic-standard step 4). One true scale, £m to px (scale): the group's
    recorded capital, about £350M (RBA: 'in the order of £350 million', end Dec 1994), stands on the right as a teal
    block on the zero line; the losses hidden in 88888 grow as a red block on the left, keyed as said:
    t_loss = [(t, £m, label), ...] (Hansard: more than £20M end 1993, more than £200M end 1994; RBA: £827M by
    27 Feb 1995). At t_move (part 2) the red block slides across onto the capital: the capital block shrinks to
    nothing as the loss covers it, and the part of the loss larger than the capital hangs below the zero line,
    labelled with what the sources support (more than twice the capital), not an invented figure."""
    zero = 430                                                                       # the zero line, board px
    cap_h = 350 * scale
    lx, rx, bw = 120, 560, 220
    gone = -9.0
    s = (_t(40, 52, "BARINGS GROUP · £ MILLION · ONE SCALE", 24, fill=INK, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
         + _t(40, 80, "CAPITAL: RBA SUMMARY OF THE OFFICIAL REPORT · LOSSES: HANSARD, RBA", 13, fill="#6A6F76", anchor="start", family="Sans",
              weight=600, extra='letter-spacing="1.5"')
         + f'<path d="M30,{zero} L{w - 30},{zero}" stroke="{INK}" stroke-width="4"/>'
         + _t(w - 34, zero - 10, "ZERO", 15, fill="#6A6F76", anchor="end", family="Sans", weight=700, extra='letter-spacing="2"'))
    # the capital block (right), which part 2 eats from the top down
    cap_keys = [[0, cap_h]] if part == 2 or t_cap <= 0 else [[0, 0], [t_cap, 0], [t_cap + .9, cap_h, "out"]]
    ycap = [[0, zero - cap_h]] if part == 2 or t_cap <= 0 else [[0, zero], [t_cap, zero], [t_cap + .9, zero - cap_h, "out"]]
    if t_move is not None:
        cap_keys = _fold(cap_keys + [[t_move + .9, cap_h], [t_move + 2.4, 0, "inout"]])
        ycap = _fold(ycap + [[t_move + .9, zero - cap_h], [t_move + 2.4, zero, "inout"]])
    s += f'<rect x="{rx}" width="{bw}" fill="{TEAL}" stroke="{INK}" stroke-width="3" {C.kv(height=cap_keys, y=ycap)}/>'
    cap_op = [[0, 1]] if t_move is None else _fold([[-20, 1], [t_move + 2.2, 1], [t_move + 2.6, 0]])
    s += f'<g {C.kv(opacity=cap_op)}>' + _ktf(_t(rx + bw / 2, 112, "RECORDED CAPITAL", 20, fill=TEAL, family="Sans", weight=700, extra='letter-spacing="2"')
              + _t(rx + bw / 2, 144, "ABOUT £350M", 32, fill=INK, family="Sans", weight=700)
              + _t(rx + bw / 2, 166, "END OF 1994", 14, fill="#6A6F76", family="Sans", weight=700, extra='letter-spacing="2"'),
              t_cap if part == 1 else 0) + "</g>"
    # the loss block (left): its height follows the losses as said; part 2 moves it across and down
    hk = [[-20, 0]]
    for t, v, lab in t_loss:
        hk += [[t, hk[-1][1]], [t + .9, v * scale, "out"]]
    hk = _fold(hk)
    yk = [[k[0], zero - k[1]] + k[2:] for k in hk]
    full = t_loss[-1][1] * scale
    move = []
    if t_move is not None:                                                           # slide across over the capital, then sink through zero
        move = _fold([[-20, 0, 0], [t_move, 0, 0], [t_move + .9, rx - lx, 0, "inout"]])
        hk = _fold([[-20, full], [t_move + .9, full], [t_move + 2.4, full - cap_h, "inout"]])
        yk = _fold([[-20, zero - full], [t_move + .9, zero - full], [t_move + 2.4, zero, "inout"]])
    s += (f'<g {C.kv(translate=move) if move else ""}>'
          f'<rect x="{lx}" width="{bw}" fill="{RED}" stroke="{INK}" stroke-width="3" opacity=".88" {C.kv(height=hk, y=yk)}/>'
          + "</g>")
    # the loss's running label (left column); part 1 counts, part 2 keeps the last value
    last = t_loss[-1]
    ck = [[-20, 0]]
    for t, v, lab in t_loss:
        ck += [[t, ck[-1][1]], [t + .9, v, "out"]]
    ck = _fold(ck)
    lab_op = [[0, 1]] if t_move is None else _fold([[0, 1], [t_move, 1], [t_move + .5, 0]])
    s += (f'<g {C.kv(opacity=lab_op)}>'
          + _ktf(_t(lx + bw / 2, 112, "HIDDEN IN 88888", 20, fill=RED, family="Sans", weight=700, extra='letter-spacing="2"'), t_loss[0][0] if part == 1 else 0)
          + f'<text x="{lx + bw / 2}" y="146" text-anchor="middle" font-family="\'Sans\',sans-serif" font-weight="700" font-size="34" fill="{INK}" '
            f'{C.kv(count=ck)} data-dec="0" data-pre="£" data-suf="M">£{ck[0][1]:.0f}M</text>'
          + "".join(_ktf(f'<g {C.kv(opacity=[[0, 0], [t - .01, 0], [t + .3, 1], [t_loss[k + 1][0] if k + 1 < len(t_loss) else 999, 1], [(t_loss[k + 1][0] + .3) if k + 1 < len(t_loss) else 999, 0]])}>'
                         + _t(lx + bw / 2, 168, lab, 14, fill="#6A6F76", family="Sans", weight=700, extra='letter-spacing="2"') + "</g>", 0)
                    for k, (t, v, lab) in enumerate(t_loss))
          + "</g>")
    if t_move is not None:
        below = (full - cap_h)
        s += _ktf(_r(rx - 40, zero - 70, bw + 80, 44, "#FBFAF6", rx=6, sw=2.4)
                  + _t(rx + bw / 2, zero - 40, "CAPITAL: GONE", 22, fill=RED, family="Sans", weight=700, extra='letter-spacing="2"'), t_move + 2.5)
        s += _ktf(_t(rx - 30, zero + 90, "STILL TO PAY", 26, fill=RED, anchor="end", family="Sans", weight=700, extra='letter-spacing="2"')
                  + _t(rx - 30, zero + 120, "THE LOSSES WERE MORE", 17, fill="#4A4F55", anchor="end", family="Sans", weight=700)
                  + _t(rx - 30, zero + 142, "THAN TWICE THE CAPITAL", 17, fill="#4A4F55", anchor="end", family="Sans", weight=700),
                  t_move + 2.9)
    return s


def easel(x, y, content="", w=900, h=600):
    """A flip-chart easel standing on the floor at x (centre), its board's top at y; content in the board box."""
    legs = (f'<path d="M{x - w * .42},{y + h + 330} L{x - 30},{y - 30} M{x + w * .42},{y + h + 330} L{x + 30},{y - 30} '
            f'M{x},{y - 30} L{x},{y + h + 330}" stroke="#5A3A24" stroke-width="16" stroke-linecap="round"/>')
    return (legs + _r(x - w / 2 - 14, y - 14, w + 28, h + 28, "#3E2A1C", rx=6, sw=3)
            + f'<g transform="translate({x - w / 2},{y})"><rect width="{w}" height="{h}" fill="#FBFAF6"/>{content}</g>'
            + _r(x - w / 2 - 30, y + h + 6, w + 60, 22, "#5A3A24", rx=4, sw=3))


# ------------------------------------------------------------------------------------------------ sets

def pit_1995(board="", clock_path=None, dur=10.0, seed=95, board_tint=0.0):
    """A futures trading floor of 1995 (generic: no exchange's name or logo). Layers (z): hall .4 (the board, clocks,
    booth fronts), pit .6 (three stepped rings), people at .66 (feet 905) and .74 (feet 1000), rail .9.
    Returns (layers, anchors)."""
    rng = random.Random(seed)
    hall = C.defs() + '<rect x="-1800" y="-900" width="5600" height="2600" fill="#2A2E35"/>'
    hall += "".join(_r(-1700 + k * 360, -60, 260, 30, "#E9ECEF", rx=6, sw=0) for k in range(15))        # ceiling lights
    hall += "".join(C.shaft(-1500 + k * 720, -40, 260, 900, angle=0, op=.06) for k in range(8))
    # the board
    hall += (f'<g transform="translate(310,60)">' + _r(-22, -22, 1344, 474, "#0B0E11", rx=8, sw=5)
             + f'<rect width="1300" height="430" fill="{BOARD}"/>{board}'
             + f'<rect width="1300" height="430" fill="#6FD3A8" opacity=".03" data-flick=\'[0.03,0.02,4]\'/></g>')
    # clocks either side of the board
    if clock_path:
        for cx, lab, off in ((40, "TOKYO", 1), (1880, "LONDON", -8)):
            pth = [[k[0], (k[1] + off) % 24] + k[2:] for k in clock_path]
            hall += wall_clock(cx, 210, 90, pth, dur, label=lab, sec0=rng.randint(0, 59))
    # booth fronts: counters with phones and screens, left and right
    for bx in list(range(-1700, 160, 300)) + list(range(1760, 3600, 300)):
        hall += (_r(bx, 640, 260, 150, "#4A4F58", sw=3) + _r(bx + 10, 560, 240, 80, "#1B2228", sw=2.4)
                 + _ticks(bx + 22, 572, 2, 216, seed=bx) + _r(bx, 790, 260, 22, "#6B717A", sw=2.4))
    pit = '<rect x="-1800" y="780" width="5600" height="900" fill="#55524E"/>'
    for k, (y, wd, col) in enumerate(((800, 2900, "#6E665C"), (850, 2400, "#7C7366"), (900, 1900, "#8A8072"))):
        pit += (f'<path d="M{960 - wd / 2},{y} L{960 + wd / 2},{y} L{960 + wd / 2 + 60},{y + 50} L{960 - wd / 2 - 60},{y + 50} Z" fill="{col}" '
                f'stroke="{INK}" stroke-width="3"/>')
    pit += '<rect x="-1800" y="950" width="5600" height="700" fill="#4E4A45"/>'
    slips = "".join(f'<g transform="translate({rng.uniform(-900, 2800):.0f},{rng.uniform(1040, 1180):.0f}) rotate({rng.uniform(-40, 40):.0f})">'
                    + _r(-16, -10, 32, 20, "#F4EFE2", sw=1.4) + "</g>" for _ in range(40))
    rail = (f'<rect x="-1800" y="1110" width="5600" height="16" fill="#9A9284" stroke="{INK}" stroke-width="3"/>'
            + "".join(_r(x, 1126, 14, 160, "#8A8274", sw=2) for x in range(-1800, 3800, 220)))
    layers = dict(hall=(0.4, hall), pit=(0.6, pit), slips=(0.8, slips), rail=(0.92, rail))
    return layers, dict(feet_back=905, feet_front=1000, board=(960, 275), board_tl=(310, 60))


def back_office_1995(screen="", seed=97, dusk=True):
    """A back office of 1995 at dusk (generic). Layers (z): wall .45 (a window on a city with palms, filing
    cabinets, a wall clock face without hands, a ceiling fan whose blades turn), floor .6, desk .86 (top y 880 from
    x 60 to 1160; a CRT centred at x 640 whose screen 664 x 440 takes content; a fax machine; trays). Seat (1240,
    1010). Returns (layers, anchors)."""
    rng = random.Random(seed)
    wall = C.defs() + '<rect x="-1800" y="-900" width="5600" height="2600" fill="#D8D1C2"/>'
    top, bot = ("#3E4A6A", "#E59A62") if dusk else ("#AFC6D6", "#E6ECEC")
    wx, wy, ww, wh = 1300, 90, 900, 560
    wall += (f'<defs><linearGradient id="bo95{seed}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
             f'<stop offset="1" stop-color="{bot}"/></linearGradient></defs><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="url(#bo95{seed})"/>')
    x = wx
    while x < wx + ww:
        bw, bh = rng.uniform(60, 140), rng.uniform(160, 420)
        bw = min(bw, wx + ww - x)
        wall += f'<rect x="{x:.0f}" y="{wy + wh - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="#3A3F52" opacity=".85"/>'
        for yy in range(int(wy + wh - bh) + 12, wy + wh - 10, 24):
            for xx in range(int(x) + 6, int(x + bw) - 8, 16):
                if rng.random() < .3:
                    wall += f'<rect x="{xx}" y="{yy}" width="7" height="10" fill="#F6D58A" opacity=".8" data-flick=\'[0.8,0.15,{xx % 7}]\'/>'
        x += bw + 5
    for px_ in (wx + 120, wx + 700):                                                  # palms in silhouette, swaying
        wall += (f'<path d="M{px_},{wy + wh} C{px_ + 10},{wy + wh - 160} {px_ - 6},{wy + wh - 260} {px_ + 14},{wy + wh - 330}" stroke="#2A2E2A" '
                 f'stroke-width="14" fill="none"/><g data-swing=\'[1.2,0.4,{px_ % 5},{px_ + 14},{wy + wh - 330}]\'>'
                 + "".join(f'<path d="M{px_ + 14},{wy + wh - 330} q{dx * .5:.0f},-40 {dx:.0f},{20 + abs(dx) * .2:.0f}" stroke="#2A2E2A" stroke-width="10" '
                           f'fill="none" stroke-linecap="round"/>' for dx in (-130, -80, 70, 120, 150)) + "</g>")
    wall += (f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#7A6F5E" stroke-width="16"/>'
             f'<path d="M{wx + ww / 2},{wy} L{wx + ww / 2},{wy + wh}" stroke="#7A6F5E" stroke-width="10"/>')
    for k in range(4):                                                                # filing cabinets
        fx = -700 + k * 190
        wall += _r(fx, 420, 170, 420, "#9AA0A6", sw=3) + "".join(_r(fx + 14, 440 + d * 100, 142, 86, "#AEB4BA", sw=2) + _r(fx + 60, 474 + d * 100, 50, 12, "#6A7076", rx=4, sw=1.6)
                                                                  for d in range(4))
    wall += _r(-100, 140, 620, 300, "#F4F3EE", rx=4, sw=3) + "".join(                  # a pinned notice board, illegible
        f'<g transform="translate({-60 + c * 150},{170 + r * 130}) rotate({rng.uniform(-5, 5):.1f})">' + _r(0, 0, 110, 100, rng.choice(["#FBFAF6", "#F6E7B0", "#DDEBE6"]), sw=1.8)
        + "".join(f'<path d="M12,{24 + j * 16} l{rng.uniform(50, 86):.0f},0" stroke="#9A9284" stroke-width="3"/>' for j in range(4)) + "</g>" for r in range(2) for c in range(4))
    fan = (f'<path d="M960,-200 L960,40" stroke="#5A5248" stroke-width="10"/><circle cx="960" cy="44" r="26" fill="#6A6056" stroke="{INK}" stroke-width="3"/>'
           f'<g transform="translate(960,48)"><g data-spin=\'[0.9]\'>' + "".join(
               f'<g transform="rotate({a})"><ellipse cx="150" cy="0" rx="130" ry="20" fill="#8A7D6C" stroke="{INK}" stroke-width="2.4"/></g>' for a in (0, 120, 240))
           + "</g></g>")
    floor = '<rect x="-1800" y="860" width="5600" height="900" fill="#8E8576"/>' + "".join(
        f'<path d="M-1800,{y} L3800,{y}" stroke="#7F7769" stroke-width="3"/>' for y in range(900, 1700, 70))
    mw, mh = 700, 480
    front = (_r(60, 880, 1100, 34, "#C9B994", rx=4, sw=3.6) + _r(90, 914, 1040, 260, "#A8987C", sw=3)
             + crt(640, 880, mw, mh, screen=screen, seed=seed)
             + _r(1000, 820, 150, 60, "#D6D0C2", rx=6, sw=3) + _r(1016, 800, 118, 24, "#BDB6A6", rx=4, sw=2)          # a fax
             + f'<g transform="translate(1040,810) rotate(-4)">' + _r(0, -60, 80, 60, PAPER, sw=1.8) + "</g>"
             + _r(150, 846, 160, 34, "#8A7D6C", rx=3, sw=2.4) + _r(160, 826, 140, 22, PAPER, sw=1.8))
    layers = dict(wall=(0.45, wall + fan), floor=(0.6, floor), front=(0.86, front))
    return layers, dict(seat=(1300, 1010), desk_y=880, screen=(640, 880 - mh / 2 - 34), screen_wh=(mw - 36, mh - 40), feet=990)


# ------------------------------------------------------------------------------------------------ people

def pit_traders(dur, n=10, seed=11, react_at=None, mood="concern", skip=(), looks=PIT_LOOKS, prefix="pt"):
    """Traders on the pit's steps, arms signalling on their own rhythm (palms out, a hand up, a point), heads turning;
    at react_at each turns to the board in turn and takes mood. Returns actors; [i] has x and z in its spec."""
    rng = random.Random(seed)
    out = []
    for i in range(n):
        if i in skip:
            continue
        front = i % 2 == 1
        x = -520 + i * (3000 / max(n, 1)) + rng.uniform(-40, 40)
        feet = 1000 if front else 905
        d = 1 if x < 960 else -1
        keys, t = [], rng.uniform(0, .4)
        while t < dur + .5:
            if react_at is not None and react_at - .2 < t < react_at + 1.2:
                t = react_at + 1.2
                continue
            if react_at is not None and t >= react_at + 1.2 and mood in ("concern", "shrug"):
                kind = rng.choice(["concern", "shrug", "relaxed"])
                keys.append([round(t, 2), C.pose(kind, head=rng.uniform(-18, -6), brow=-1, mouth=-1)])
                t += rng.uniform(1.1, 1.8)
                continue
            kind = rng.choice(["hold_up", "hold_up", "point", "cheer", "talk_a", "reach"])
            over = dict(head=rng.uniform(-14, 10), mouth=rng.choice([0, 1, 2]))
            if kind == "hold_up":
                over.update(shF=rng.uniform(110, 160), elF=rng.uniform(10, 60))
            keys.append([round(t, 2), C.pose(kind, **over)])
            t += rng.uniform(.45, .95)
        if react_at is not None:
            keys.append([round(react_at + .08 * i, 2), C.pose("relaxed", head=-16)])
            keys.append([round(react_at + .45 + .08 * i, 2), C.pose(mood if i % 3 else "point", head=-20, brow=-1)])
            keys.sort(key=lambda k: k[0])
        a = C.actor(f"{prefix}{i}", looks[i % len(looks)], pos=[[0, x, feet]], scale=.84 if not front else .92, seed=seed + i, dir=d,
                    walk=False, pose_keys=keys)
        a["front"] = front
        out.append(a)
    return out


def _pit_layers(layers_, traders, extra_back="", extra_front=""):
    layers = [lay(layers_["hall"][0], layers_["hall"][1]), lay(layers_["pit"][0], layers_["pit"][1])]
    layers.append(lay(.66, "".join(a["svg"] for a in traders if not a["front"]) + extra_back))
    layers.append(lay(.74, "".join(a["svg"] for a in traders if a["front"]) + extra_front))
    layers.append(lay(layers_["slips"][0], layers_["slips"][1]))
    layers.append(lay(layers_["rail"][0], layers_["rail"][1]))
    return layers


def _pit_amb(dur, seed):
    import sfx
    return (sfx.street_ambience(dur + .5, seed=seed, crowd=1.6) * .55 + sfx.office_ambience(dur + .5, seed=seed + 1, busy=1.4, phones=2) * .35)


# ------------------------------------------------------------------------------------------------ shots

def _bx(x, z=.4):
    return 960 + (x - 960) / z


def shot_hook_827(w, h, dur, ctx):
    """The hook. Frame 0: the board fills the frame and LOST BY ONE TRADER counts from £0 to £827M by 1.4 s (RBA:
    '£827 million by 27 February 1995'; Hansard 18 July 1995); THE BANK'S CAPITAL ABOUT £350M lands with its sentence
    (RBA: 'in the order of £350 million'). On the question the camera pulls back onto the pit, traders signalling."""
    n = len(ctx.get("segs") or [0])
    t_cap = max(2.2, seg_t(ctx, 1, 0.0) if n > 1 else 3.0)
    t_q = min(dur - 3.0, max(t_cap + 1.6, seg_t(ctx, n - 1, 0.0) - .4))
    rows = [("LOST BY ONE TRADER", None, RED, .0, [[0, 0], [.1, 0], [1.4, 827, "out"]], (0, "£", "M")),
            ("THE BANK'S RECORDED CAPITAL", None, "#6FD3A8", t_cap, [[0, 350]], (0, "ABOUT £", "M"))]
    board = (_t(60, 80, "SINGAPORE · FEBRUARY 1995", 34, fill=LIGHT, anchor="start", family="Sans", weight=700, extra='letter-spacing="4"')
             + _t(1240, 80, "OUR ILLUSTRATION", 18, fill=DIM, anchor="end", family="Sans", weight=600, extra='letter-spacing="3"')
             + pit_board(rows, y0=210, step=130, size=46)
             + _t(60, 400, "SOURCES: RESERVE BANK OF AUSTRALIA, 1995 · HANSARD, 1995", 18, fill=DIM, anchor="start", family="Sans", weight=600,
                  extra='letter-spacing="2"'))
    layers_, anc = pit_1995(board=board, clock_path=[[0, 14, 5], [dur, 14, 6]], dur=dur)
    tr = pit_traders(dur, n=16, seed=31)
    layers = _pit_layers(layers_, tr)
    bx, by = anc["board"]
    cam = [[0, _bx(bx), 540 + (by - 540) / .4 + 10, 2.25], [.9, _bx(bx), 540 + (by - 540) / .4, 2.3, "sine"],
           [t_q, _bx(bx + 10), 540 + (by - 540) / .4, 2.36, "sine"], [t_q + 2.0, 960, 560, 1.0, "inout"], [dur, 980, 570, .96, "sine"]]
    over = [badge("Our illustration · figures from the RBA and Hansard", w, h)]
    shot = dict(dur=dur, layers=layers, actors=tr, cam=cam, focus=[[0, .4], [t_q + .5, .4], [t_q + 1.8, .7]], dof=4, shake=.3, over=over,
                grade="cool", vig=1.1)
    foley = [("flap", .05, .35, 0), ("flap", 1.3, .3, 0), ("flap", t_cap + .05, .3, .1)]
    return dict(shots=[shot], foley=foley, amb=_pit_amb(dur, 950))


def shot_pit_floor(w, h, dur, ctx):
    """1992 (reconstruction, not a likeness): a trader in a blue jacket crosses the floor from the left, steps into the
    pit and joins the signalling; the board lists what was traded (NLB, RBA: Nikkei 225 futures on SIMEX and Osaka)
    with illegible ticks only. Sentences: 0 the trader, 1 the bank, 2 more than twice its capital."""
    n = len(ctx.get("segs") or [0])
    t_b = max(1.0, seg_t(ctx, 1, .1))
    t_c = max(t_b + 1.5, seg_t(ctx, n - 1, .1))
    board = (_t(60, 70, "NIKKEI 225 FUTURES", 34, fill=LIGHT, anchor="start", family="Sans", weight=700, extra='letter-spacing="4"')
             + _t(1240, 70, "SINGAPORE · OSAKA", 22, fill=DIM, anchor="end", family="Sans", weight=600, extra='letter-spacing="3"')
             + _ticks(60, 120, 7, 1180, seed=5)
             + _ktf(_r(60, 330, 760, 70, "#2A1512", rx=6, sw=0) + _t(80, 378, "LOSSES: MORE THAN TWICE THE CAPITAL", 30, fill="#F08A6A", anchor="start",
                                                                  family="Sans", weight=700), t_c))
    layers_, anc = pit_1995(board=board, clock_path=[[0, 10, 30], [dur, 10, 31]], dur=dur, seed=96)
    tr = pit_traders(dur, n=16, seed=41, skip=(9,))
    feet = anc["feet_front"]
    t_in = .2
    t_arr = t_in + 3.4
    keys = [[0, C.pose("relaxed", head=-4)], [t_arr, C.pose("relaxed", head=-10)], [t_arr + .4, C.pose("hold_up", shF=140, elF=30, head=-12)]]
    t = t_arr + 1.0
    rng = random.Random(7)
    while t < dur:
        keys.append([round(t, 2), C.pose(rng.choice(["hold_up", "point", "cheer"]), head=rng.uniform(-14, 6))])
        t += rng.uniform(.5, .9)
    hero = C.actor("pf_hero", "pit_95_blue", pos=[[0, -700, feet + 10], [t_in, -700, feet + 10], [t_arr, 1010, feet + 10, "out"], [dur, 1010, feet + 10]],
                   scale=1.0, seed=77, dir=1, pose_keys=keys)
    hero["front"] = True
    tr.append(hero)
    layers = _pit_layers(layers_, tr)
    zx = lambda x, z=.74: 960 + (x - 960) / z
    cam = [[0, zx(200), 600, .98], [t_arr, zx(980), 590, 1.12, "inout"], [t_c - .3, zx(980), 560, 1.14, "sine"],
           [t_c + 1.0, _bx(820), 540 + (330 - 540) / .4 * .55, 1.35, "inout"], [dur, _bx(840), 540 + (330 - 540) / .4 * .55, 1.38, "sine"]]
    over = [title("Singapore, 1992", "A trading floor", w, h, d=min(3.0, t_b + .4)), badge("Reconstruction · not a likeness, not the real exchange", w, h)]
    shot = dict(dur=dur, layers=layers, actors=tr, cam=cam, focus=[[0, .74], [t_c + .4, .74], [t_c + 1.0, .5]], dof=4, shake=.3, over=over,
                grade="warm", vig=1.1, tin=("dissolve", .35))
    foley = [("step", t, .06, -.3) for t in C.footsteps(hero, dur)][:12] + [("flap", t_c + .1, .3, 0)]
    return dict(shots=[shot], foley=foley, amb=_pit_amb(dur, 960))


def _office_shot(w, h, dur, scr, cam_keys, ttl, bdg, seed=97, sitter_keys=None, dusk=True, look="clerk_1995", foley=(), tin=("dissolve", .35)):
    layers_, anc = back_office_1995(screen=scr, seed=seed, dusk=dusk)
    sx, sy = anc["seat"]
    an = C.actor(f"bo{seed}", look, pos=[[0, sx, sy]], scale=1.0, seed=seed + 3, dir=-1, walk=False,
                 pose_keys=_alive(sitter_keys or [[0, C.pose("seated", head=10, eyeY=1)], [dur, C.pose("seated", head=8)]], dur, t0=.9, every=1.9))
    layers = [lay(z, s) for k, (z, s) in layers_.items() if k != "front"]
    layers.append(lay(.82, an["svg"]))
    layers.append(lay(.86, layers_["front"][1]))
    zx = lambda x, z=.86: 960 + (x - 960) / z
    zy = lambda y, z=.86: 540 + (y - 540) / z
    mx, my = anc["screen"]
    cam = [[k[0], zx(mx + k[1]), zy(my + k[2]), k[3]] + k[4:] for k in cam_keys]
    shot = dict(dur=dur, layers=layers, actors=[an], cam=cam, focus=[[0, .86]], dof=4, shake=.2, over=([title(*ttl, w, h, d=2.6)] if ttl else []) + [badge(bdg, w, h)],
                grade="warm" if dusk else "cool", vig=1.12, tin=tin)
    import sfx
    amb = sfx.room_tone(dur + .5, seed=seed * 3, clock=True, street=.2) * .8
    return dict(shots=[shot], foley=list(foley), amb=amb)


def shot_acct_88888(w, h, dur, ctx):
    """The back office (our illustration): the CRT types the new account as it is said (NLB: opened 3 July 1992, error
    account 88888, originally for error trades by inexperienced staff). Sentences: 0 arrived April 1992, 1 opened it."""
    t_open = max(1.4, find_t(ctx, "opened") - .2)
    t_num = max(t_open + .8, find_t(ctx, "number") - .1)
    digits = "88888"
    sw_, sh_ = 664, 440
    typed = "".join(_ktf(_t(40 + k * 92, 250, d_, 110, fill="#F6D58A", anchor="start", family="Sans", weight=700), t_num + .35 * k, .12) for k, d_ in enumerate(digits))
    scr = (_t(30, 46, "BARINGS FUTURES (SINGAPORE) · ACCOUNTS", 20, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + _t(30, 72, "OUR ILLUSTRATION · FACTS FROM SINGAPORE'S NATIONAL LIBRARY", 13, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
           + _ktf(_t(30, 130, "NEW ACCOUNT", 30, fill=LIGHT, anchor="start", family="Sans", weight=700, extra='letter-spacing="3"'), t_open)
           + typed
           + _ktf(_t(30, 320, "OPENED 3 JULY 1992", 28, fill="#C9D4D6", anchor="start", family="Sans", weight=700), t_num + 2.0)
           + _ktf(_r(30, 350, 600, 50, "#5E3A1A", rx=6, sw=0) + _t(46, 384, "FOR: ERROR TRADES", 28, fill="#F6D58A", anchor="start", family="Sans", weight=700),
                  t_num + 2.6))
    keys = [[0, C.pose("seated", head=10, eyeY=1)], [t_open, C.pose("sit_write", head=14)], [t_num + 2.0, C.pose("sit_write", head=12)],
            [t_num + 2.6, C.pose("seated", head=6, lean=-2)], [dur, C.pose("seated", head=6)]]
    cam = [[0, 300, 120, .92], [t_open - .3, 0, 20, 1.35, "inout"], [t_num + 2.2, 0, 40, 1.45, "sine"], [dur, 60, 60, 1.25, "inout"]]
    fol = [("tick", t_num + .35 * k, .3, 0) for k in range(5)] + [("tick", t_open, .25, 0), ("tick", t_num + 2.0, .25, 0), ("hit", t_num + 2.6, .3, 0, dict(pitch=160))]
    return _office_shot(w, h, dur, scr, cam, ("Singapore, July 1992", "The back office"), "Our illustration · not the real office", sitter_keys=keys, foley=fol)


def _hidden(w, h, dur, ctx, part):
    """London at night (our illustration): part 1 draws the losses in 88888 (Hansard 18 July 1995: more than £20M by
    the end of 1993, more than £200M by the end of 1994); part 2 adds what the draft 1994 accounts showed, a pre-tax
    profit of £102M (RBA), and ON THE BOOKS: NONE OF IT beside the losses."""
    gone = -9.0
    if part == 1:
        t93 = max(1.4, find_t(ctx, "twenty million") - .2)
        t94 = max(t93 + 1.2, find_t(ctx, "two hundred") - .2)
        t_none, t_prof = dur + 99, dur + 99
    else:
        t93, t94 = gone, gone + .5
        t_none = .8
        t_prof = max(1.6, find_t(ctx, "hundred and two") - .2)
    rows = [("LOSSES IN 88888, END OF 1993", None, "#F08A6A", t93 - .3 if part == 1 else gone, _fold([[gone - 1, 0], [t93, 0], [t93 + .8, 20, "out"]]), (0, "OVER £", "M")),
            ("LOSSES IN 88888, END OF 1994", None, RED, t94 - .3 if part == 1 else gone, _fold([[gone - 1, 0], [t94, 0], [t94 + .9, 200, "out"]]), (0, "OVER £", "M"))]
    if part == 2:
        rows.append(("1994 PRE-TAX PROFIT, DRAFT ACCOUNTS", None, "#6FD3A8", t_prof - .3, [[0, 0], [t_prof, 0], [t_prof + .9, 102, "out"]], (0, "£", "M")))
    rows = [r[:3] + (max(r[3], 0) if r[3] > -5 else 0,) + r[4:] for r in rows]
    scr = (_t(30, 46, "THE GROUP'S NUMBERS · £ MILLION", 20, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + _t(30, 72, "OUR ILLUSTRATION · HANSARD 1995, RESERVE BANK OF AUSTRALIA 1995", 13, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
           + rows_screen(rows, x0=30, y0=150, step=90, wid=600, size=20)
           + (_ktf(_r(30, 330, 600, 44, "#5E1A12", rx=6, sw=0) + _t(46, 361, "LOSSES ON THE BOOKS: NONE", 24, fill="#F6D58A", anchor="start", family="Sans", weight=700),
                   t_none) if part == 2 else ""))
    if part == 1:
        keys = [[0, C.pose("seated", head=10, eyeY=1)], [t93, C.pose("seated", head=12, lean=8, eyeY=1)], [t94 + .6, C.pose("seated", head=4, lean=-2, brow=.8)],
                [dur, C.pose("seated", head=6, brow=.4)]]
        cam = [[0, 320, 100, .9], [t93 - .4, 0, 20, 1.4, "inout"], [t94 + 1.2, 0, 30, 1.46, "sine"], [dur, 10, 30, 1.48, "sine"]]
    else:
        keys = [[0, C.pose("seated", head=6, brow=.4)], [t_prof, C.pose("seated", head=12, lean=10, eyeY=1)], [t_prof + 1.2, C.pose("seated", shF=30, elF=110, head=4, brow=-1)],
                [dur, C.pose("seated", shF=30, elF=110, head=2, brow=-1)]]
        cam = [[0, 10, 30, 1.48], [t_prof - .3, 0, 60, 1.55, "inout"], [t_prof + 1.6, 260, 140, 1.02, "inout"], [dur, 280, 140, 1.0, "sine"]]
    fol = [("tick", t, .3, 0) for t in (t93, t94, t_prof) if 0 < t < dur] + ([("hit", t_prof + .9, .3, 0, dict(pitch=150))] if part == 2 else [])
    return _office_shot(w, h, dur, "".join(scr), cam, ("London, 1995", "The numbers") if part == 1 else None,
                        "Our illustration · figures from Hansard and the RBA", seed=98, sitter_keys=keys, look="office_1995", dusk=False, foley=fol,
                        tin=("dissolve", .35) if part == 1 else ("cut", 0))


def shot_hidden_1(w, h, dur, ctx):
    return _hidden(w, h, dur, ctx, 1)


def shot_hidden_2(w, h, dur, ctx):
    return _hidden(w, h, dur, ctx, 2)


def _tally(w, h, dur, ctx, part):
    """Our example (not Barings' numbers): selling insurance on a market. Part 1: the CRT counts CALM DAYS 0 to 99 and
    FEES COLLECTED £0 to £99 as they are said; part 2: DAY 100 PAYS OUT £150 and TOTAL counts +£99 to -£51 (99 - 150 =
    -51, build/plans/ep015_checks.py)."""
    gone = -9.0
    if part == 1:
        t_d = max(1.6, find_t(ctx, "one pound") - .2)
        t_99 = max(t_d + 1.5, find_t(ctx, "ninety nine") - .4)
        t_pay, t_tot = dur + 99, dur + 99
    else:
        t_d, t_99 = gone, gone + .5
        t_pay = max(.9, find_t(ctx, "hundred and fifty") - .3)
        t_tot = max(t_pay + 1.2, find_t(ctx, "fifty one") - .4)
    days = _fold([[gone - 1, 0], [t_d, 0], [t_99, 99, "inout"]] + ([[t_pay - .2, 99], [t_pay, 100, "out"]] if part == 2 else []))
    fees = _fold([[gone - 1, 0], [t_d, 0], [t_99, 99, "inout"]])
    rows = [("DAYS", None, "#C9D4D6", 0 if part == 2 else .4, days, (0, "", "")),
            ("FEES COLLECTED", None, "#6FD3A8", 0 if part == 2 else .7, fees, (0, "+£", ""))]
    if part == 2:
        rows += [("DAY 100: THE MARKET JUMPS, YOU PAY", None, RED, t_pay - .3, [[0, 0], [t_pay, 0], [t_pay + .8, 150, "out"]], (0, "-£", "")),
                 ("YOUR TOTAL", None, "#F6D58A", t_tot - .3, [[0, 99], [t_tot, 99], [t_tot + .7, 0, "in"], [t_tot + .71, 0], [99, 0]], (0, "+£", ""))]
    scr = (_t(30, 46, "OUR EXAMPLE · SELLING INSURANCE ON A MARKET", 20, fill="#C9D4D6", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
           + _t(30, 72, "NOT BARINGS' NUMBERS", 13, fill=DIM, anchor="start", family="Sans", weight=600, extra='letter-spacing="2"')
           + rows_screen(rows, x0=30, y0=140, step=78, wid=600, size=22))
    if part == 2:                                                                      # the total crosses zero: +£99 counts down, then -£51 counts up
        scr += (f'<rect x="440" y="{140 + 78 * 3 - 40}" width="200" height="52" fill="{SCREEN95}" {C.kv(opacity=[[0, 0], [t_tot + .7, 0], [t_tot + .71, 1]])}/>'
                f'<text x="630" y="{140 + 78 * 3}" text-anchor="end" font-family="\'Sans\',sans-serif" font-weight="700" font-size="34" fill="{RED}" '
                f'{C.kv(opacity=[[0, 0], [t_tot + .7, 0], [t_tot + .71, 1]], count=[[0, 0], [t_tot + .7, 0], [t_tot + 1.3, 51, "out"]])} data-dec="0" data-pre="-£" data-suf="">-£0</text>')
    if part == 1:
        keys = [[0, C.pose("seated", head=10, eyeY=1)], [t_99, C.pose("seated", head=8, lean=-4, mouth=1, brow=.4)], [dur, C.pose("seated", head=6, mouth=1)]]
        cam = [[0, 200, 80, 1.0], [t_d - .4, 0, 30, 1.42, "inout"], [dur, 10, 40, 1.5, "sine"]]
    else:
        keys = [[0, C.pose("seated", head=6, mouth=1)], [t_pay, C.pose("seated", head=12, lean=10, brow=1)], [t_tot + 1.0, C.pose("seated", shF=30, elF=110, head=2, brow=-1, mouth=-1)],
                [dur, C.pose("seated", shF=30, elF=110, head=2, brow=-1)]]
        cam = [[0, 10, 40, 1.5], [t_pay - .2, 0, 60, 1.6, "inout"], [t_tot + 1.4, 240, 120, 1.06, "inout"], [dur, 250, 120, 1.04, "sine"]]
    fol = [("tick", t, .3, 0) for t in (t_d, t_99) if 0 < t < dur] + ([("hit", t_pay + .1, .35, 0, dict(pitch=140)), ("tick", t_tot + 1.2, .3, 0)] if part == 2 else [])
    return _office_shot(w, h, dur, scr, cam, None, "Our example · not Barings' numbers", seed=99, sitter_keys=keys, look="office_1995b", foley=fol,
                        tin=("dissolve", .35) if part == 1 else ("cut", 0))


def shot_tally_1(w, h, dur, ctx):
    return _tally(w, h, dur, ctx, 1)


def shot_tally_2(w, h, dur, ctx):
    return _tally(w, h, dur, ctx, 2)


def _london_room(w, h, dur, board, cam, ttl, bdg, react_at, seed=8, tin=("dissolve", .35), foley=(), stander=True, walk_in=None):
    """walk_in=(t0, t1): the standing banker walks in from the left (x 400) to his place by the easel between t0 and
    t1 (22 Nov: capital_1 measured 12 static seconds with everyone seated and the board still between its cues)."""
    clock = [[0, 21, 10], [dur, 21, 12]]
    layers_, anc = boardroom_1998(clock, dur, seed=seed)
    ppl = []
    for i, x in enumerate(anc["seat_xs"][:4]):
        keys = [[0, C.pose("seated", head=6 + 3 * i)], [1.2 + .5 * i, C.pose("sit_read", head=10)]]
        if react_at:
            keys += [[react_at + .2 * i, C.pose("seated", head=-14, brow=.8)], [react_at + 1.6 + .2 * i, C.pose("seated", shF=30, elF=110, head=-8, brow=-1)],
                     [dur, C.pose("seated", shF=30, elF=110, head=-6, brow=-1)]]
        ppl.append(C.actor(f"lr{seed}_{i}", ("office_1995", "office_1995b", "suit_1998c", "lady_1998")[i], pos=[[0, x, anc["seat_y"]]], scale=.95,
                           seed=seed * 10 + i, dir=1, walk=False, pose_keys=_alive(keys, dur, t0=.7 + .3 * i)))
    st_pos = [[0, 2560, 1010]] if not walk_in else [[0, 300, 1010], [walk_in[0], 300, 1010], [walk_in[1], 2560, 1010, "inout"], [dur, 2560, 1010]]
    stand = C.actor(f"lr{seed}_s", "office_1995", pos=st_pos, scale=1.02, seed=seed * 10 + 9, dir=1 if walk_in else -1, walk=bool(walk_in),
                    turn=[[walk_in[1], 1], [walk_in[1] + .3, -1]] if walk_in else None,
                    pose_keys=_alive([[0, C.pose("relaxed", head=-4)], [max(.5, (react_at or 2) - .6), C.pose("point", head=-6)],
                                      [max(1.2, (react_at or 2) + .6), C.pose("relaxed", head=8)], [dur, C.pose("concern", head=6)]], dur, t0=1.0))
    layers = [lay(z, s, noblur=(k == "glow")) for k, (z, s) in layers_.items() if k != "table"]
    layers.append(lay(.8, "".join(a["svg"] for a in ppl)))
    layers.append(lay(.85, layers_["table"][1]))
    layers.append(lay(.88, easel(1960, 300, board) + (stand["svg"] if stander else "")))
    zx = lambda x, z=.88: 960 + (x - 960) / z
    zy = lambda y, z=.88: 540 + (y - 540) / z
    cam_ = [[k[0], zx(k[1]), zy(k[2]), k[3]] + k[4:] for k in cam]
    over = ([title(*ttl, w, h, d=2.6)] if ttl else []) + [badge(bdg, w, h)]
    shot = dict(dur=dur, layers=layers, actors=ppl + ([stand] if stander else []), cam=cam_, focus=[[0, .88]], dof=4, shake=.22, over=over, grade="dusk", vig=1.18, tin=tin)
    import sfx
    amb = sfx.room_tone(dur + .5, seed=seed * 7, clock=True, street=.1) * .8
    foley = list(foley) + ([("step", t, .08, -.2) for t in C.footsteps(stand, dur)][:14] if walk_in else [])
    return dict(shots=[shot], foley=foley, amb=amb)


def _funding(w, h, dur, ctx, part):
    """London at night (our illustration): the easel. Part 1 (margin; London believed it was lent to clients): FUNDING
    FROM LONDON with an arrow to SINGAPORE and the label LONDON'S BELIEF: LENT TO CLIENTS. Part 2: the Chancellor's
    two figures (Hansard 18 July 1995): lent to clients more than £300M, clients' collateral about £31M, drawn as bars
    on one scale."""
    gone = -9.0
    sc = 2.2                                                                           # px per £m
    if part == 1:
        t_mg = max(1.0, find_t(ctx, "margin") - .2)
        t_ldn = max(t_mg + 1.4, find_t(ctx, "London") - .2)
        t_bel = max(t_ldn + 1.2, find_t(ctx, "believed") - .2)
        t_300, t_31 = dur + 99, dur + 99
    else:
        t_mg, t_ldn, t_bel = gone, gone, gone
        t_300 = max(1.2, find_t(ctx, "three hundred") - .2)
        t_31 = max(t_300 + 1.2, find_t(ctx, "thirty one") - .2)
    b = (_t(40, 56, "WHERE THE MONEY WENT · 1994 TO 1995", 26, fill=INK, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
         + _t(40, 84, "OUR ILLUSTRATION · FROM THE CHANCELLOR'S STATEMENT, JULY 18, 1995", 14, fill="#6A6F76", anchor="start", family="Sans", weight=600, extra='letter-spacing="1.5"')
         + _ktf(_r(40, 120, 230, 80, "#2E3442", rx=8, sw=2.4) + _t(155, 172, "LONDON", 32, fill="#fff", family="Sans", weight=700), max(t_mg, 0) if part == 1 else 0)
         + _ktf(_r(630, 120, 230, 80, TEAL, rx=8, sw=2.4) + _t(745, 172, "SINGAPORE", 30, fill="#fff", family="Sans", weight=700), max(t_mg, 0) + .2 if part == 1 else 0)
         + (f'<path d="M290,160 L610,160" stroke="{RED}" stroke-width="10" stroke-linecap="round" {C.kv(dash=_fold([[gone - 1, 0], [t_ldn, 0], [t_ldn + 1.0, 1, "out"]]))}/>'
            + _ktf(f'<path d="M590,140 L616,160 L590,180" fill="none" stroke="{RED}" stroke-width="10" stroke-linejoin="round"/>'
                   + _t(450, 140, "CASH FOR MARGIN", 18, fill=RED, family="Sans", weight=700, extra='letter-spacing="2"'), max(t_ldn + .9, 0) if part == 1 else 0))
         + _ktf(_r(40, 230, 820, 56, "#F6E7B0", rx=6, sw=2) + _t(60, 268, "WHAT LONDON BELIEVED: IT WAS LENT TO CLIENTS", 22, fill=INK, anchor="start", family="Sans", weight=700),
                max(t_bel, 0) if part == 1 else 0))
    if part == 2:
        b += (_ktf(_t(40, 340, "LENT TO CLIENTS, APPARENTLY", 18, fill="#6A6F76", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"'), t_300 - .2)
              + f'<rect x="40" y="352" height="64" fill="{RED}" stroke="{INK}" stroke-width="2.4" {C.kv(width=[[0, 0], [t_300, 0], [t_300 + 1.0, 300 * sc, "out"]])}/>'
              + _ktf(_t(40 + 300 * sc + 14, 398, "OVER £300M", 30, fill=INK, anchor="start", family="Sans", weight=700), t_300 + .8)
              + _ktf(_t(40, 460, "CLIENTS' COLLATERAL FOR THOSE TRADES", 18, fill="#6A6F76", anchor="start", family="Sans", weight=700, extra='letter-spacing="2"'), t_31 - .2)
              + f'<rect x="40" y="472" height="64" fill="{TEAL}" stroke="{INK}" stroke-width="2.4" {C.kv(width=[[0, 0], [t_31, 0], [t_31 + .8, 31 * sc, "out"]])}/>'
              + _ktf(_t(40 + 31 * sc + 14, 518, "ABOUT £31M", 30, fill=INK, anchor="start", family="Sans", weight=700), t_31 + .7)
              + _t(860, 580, "ONE SCALE", 13, fill="#6A6F76", anchor="end", family="Sans", weight=700, extra='letter-spacing="2"'))
    if part == 1:
        cam = [[0, 1100, 640, .9], [max(.6, t_mg - .3), 1700, 560, 1.18, "inout"], [dur, 1760, 560, 1.22, "sine"]]
        react = None
    else:
        cam = [[0, 1760, 560, 1.22], [t_300 - .3, 1880, 660, 1.28, "inout"], [t_31 + 1.4, 1500, 600, 1.0, "inout"], [dur, 1460, 600, .98, "sine"]]
        react = t_31 + .9
    fol = [("tick", t, .3, 0) for t in (t_ldn, t_bel, t_300, t_31) if 0 < t < dur] + ([("hit", t_31 + .8, .3, 0, dict(pitch=150))] if part == 2 else [])
    return _london_room(w, h, dur, b, cam, ("London, 1994", "Cash for Singapore") if part == 1 else None,
                        "Our illustration · not the real office", react, seed=8 if part == 1 else 9,
                        tin=("dissolve", .35) if part == 1 else ("cut", 0), foley=fol, stander=False)


def shot_funding_1(w, h, dur, ctx):
    return _funding(w, h, dur, ctx, 1)


def shot_funding_2(w, h, dur, ctx):
    return _funding(w, h, dur, ctx, 2)


def shot_kobe_fall(w, h, dur, ctx):
    """January 1995 (our illustration): the board reads EARTHQUAKE AT KOBE · 17 JANUARY (NLB), then NIKKEI 225 ON 23
    JANUARY counts to 17,785 (NLB) under HIS LINE: 19,000 (NLB: 'hoping that it would not fall below 19,000 points').
    The count starts at the line, not at an unsourced level: the board says only that the index was below it. The
    traders stop signalling and turn to the board. Sentences: 0 the quake, 1 the Nikkei fell, 2 17,785 on 23 Jan."""
    t_q = max(.9, find_t(ctx, "earthquake") - .2)
    t_fell = max(t_q + 1.4, find_t(ctx, "fell") - .2)
    t_lvl = max(t_fell + 1.4, find_t(ctx, "seventeen thousand") - .3)
    board = (_ktf(_r(60, 30, 1180, 84, "#3A1A12", rx=6, sw=0) + _t(84, 88, "EARTHQUAKE AT KOBE · 17 JANUARY 1995", 40, fill="#F6D58A", anchor="start",
                                                                  family="Sans", weight=700, extra='letter-spacing="2"'), t_q)
             + _ktf(_t(60, 170, "NIKKEI 225 · POINTS", 26, fill=DIM, anchor="start", family="Sans", weight=700, extra='letter-spacing="3"'), t_fell - .3)
             + _ktf(_r(60, 196, 1180, 4, "#F6D58A", sw=0) + _t(1240, 236, "HIS LINE: 19,000", 26, fill="#F6D58A", anchor="end", family="Sans", weight=700,
                                                         extra='letter-spacing="2"'), t_fell)
             + _ktf(_t(60, 320, "23 JANUARY", 40, fill=LIGHT, anchor="start", family="Sans", weight=700, extra='letter-spacing="2"')
                    + f'<text x="1240" y="330" text-anchor="end" font-family="\'Sans\',sans-serif" font-weight="700" font-size="96" fill="{RED}" '
                      f'{C.kv(count=[[0, 19000], [t_lvl, 19000], [t_lvl + 1.4, 17785, "out"]])} data-dec="0" data-pre="" data-suf="">19,000</text>', t_lvl - .4)
             + _ktf(_t(60, 400, "SINGAPORE'S NATIONAL LIBRARY, INFOPEDIA · OUR ILLUSTRATION", 18, fill=DIM, anchor="start", family="Sans", weight=600,
                       extra='letter-spacing="2"'), t_lvl))
    layers_, anc = pit_1995(board=board, clock_path=[[0, 9, 0], [dur, 9, 1]], dur=dur, seed=97)
    tr = pit_traders(dur, n=16, seed=51, react_at=t_q + .2, mood="concern")
    layers = _pit_layers(layers_, tr)
    bx, by = anc["board"]
    cam = [[0, 960, 600, .98], [t_q + .4, _bx(bx) * .5 + 480, 380, 1.3, "inout"], [t_lvl - .2, _bx(bx), 540 + (by - 540) / .4 * .8, 1.7, "inout"],
           [t_lvl + 2.2, _bx(bx + 60), 540 + (by - 540) / .4 * .8, 1.78, "sine"], [dur, 960, 580, 1.0, "inout"]]
    over = [title("January 1995", "After the earthquake", w, h, d=min(2.6, t_q + .8)), badge("Our illustration · not the real exchange", w, h)]
    shot = dict(dur=dur, layers=layers, actors=tr, cam=cam, focus=[[0, .7], [t_q + .2, .7], [t_q + 1.0, .4], [dur - 1, .4], [dur, .7]], dof=4, shake=.35,
                over=over, grade="cool", vig=1.15, tin=("dissolve", .35))
    foley = [("flap", t_q + .05, .35, 0), ("flap", t_fell + .05, .3, 0), ("hit", t_lvl + 1.4, .35, 0, dict(pitch=120))]
    import sfx
    amb = _pit_amb(dur, 970)
    k = int((t_q + 1.2) * sfx.FSR) if hasattr(sfx, "FSR") else 0
    if k:
        amb[k:] *= .5                                                                   # the floor goes quieter as they turn to the board
    return dict(shots=[shot], foley=foley, amb=amb)


def _capital(w, h, dur, ctx, part):
    """The balance sheet that rearranges (the 20 Nov next improvement), on the London easel on the weekend of 25 and
    26 February 1995 (our illustration). Part 1: capital about £350M rises on its sentence; the losses grow on the
    left as said (over £20M end 1993, over £200M end 1994, £827M by 27 Feb). Part 2: the losses slide across onto the
    capital: the capital goes to nothing and the rest of the loss hangs below zero (more than twice the capital)."""
    if part == 1:
        t827 = max(1.4, find_t(ctx, "eight hundred and twenty seven") - .3)
        t_cap = max(t827 + 2.0, find_t(ctx, "three hundred and fifty") - .4)
        t_loss = [(.6, 20, "END OF 1993: OVER £20M"), (t827 - 1.2, 200, "END OF 1994: OVER £200M"), (t827, 827, "27 FEBRUARY 1995")]
        t_move = None
    else:
        t_cap = 0
        t_loss = [(-9, 827, "27 FEBRUARY 1995")]
        t_move = max(.6, find_t(ctx, "books") - .4)
    b = balance_board(t_cap, t_loss, t_move=t_move, part=part)
    if part == 1:
        cam = [[0, 1500, 600, .96], [.5, 1940, 640, 1.42, "inout"], [t827 + 1.2, 1880, 600, 1.5, "inout"],
               [t_cap - .3, 2060, 600, 1.48, "inout"], [t_cap + 1.6, 2040, 660, 1.4, "inout"], [dur, 1900, 680, 1.3, "sine"]]
        react = t827 + .6
    else:
        cam = [[0, 1960, 640, 1.46], [t_move + 2.6, 1980, 720, 1.4, "inout"], [dur, 1760, 640, 1.18, "inout"]]
        react = t_move + 2.4
    fol = ([("tick", t, .3, 0) for t, v, l in t_loss if 0 < t < dur] + ([("tick", t_cap, .3, .1)] if part == 1 else [])
           + ([("paper", t_move, .3, 0), ("hit", t_move + 2.4, .4, 0, dict(pitch=110))] if part == 2 else []))
    return _london_room(w, h, dur, b, cam, ("London, February 1995", "The weekend") if part == 1 else None,
                        "Our illustration · figures from Hansard and the RBA", react, seed=10 if part == 1 else 11,
                        tin=("dissolve", .35) if part == 1 else ("cut", 0), foley=fol, walk_in=(t827 + 1.4, t_cap - .4) if part == 1 else None)


def shot_capital_1(w, h, dur, ctx):
    return _capital(w, h, dur, ctx, 1)


def shot_capital_2(w, h, dur, ctx):
    return _capital(w, h, dur, ctx, 2)


SHOTS = dict(hook_827=shot_hook_827, pit_floor=shot_pit_floor, acct_88888=shot_acct_88888, hidden_1=shot_hidden_1, hidden_2=shot_hidden_2,
             tally_1=shot_tally_1, tally_2=shot_tally_2, funding_1=shot_funding_1, funding_2=shot_funding_2, kobe_fall=shot_kobe_fall,
             capital_1=shot_capital_1, capital_2=shot_capital_2)


if __name__ == "__main__":
    # stills for a quick look: python3 build/cine_1995.py [name ...]
    names = sys.argv[1:] or list(SHOTS)
    work = C.OUT / "cine-1995-stills"
    work.mkdir(parents=True, exist_ok=True)
    demo = dict(segs=[("One trader lost eight hundred and twenty seven million, an earthquake, he opened it, one pound a day, futures exchanges ask for margin.", .3, 4.6),
                      ("By the end of nineteen ninety three, more than twenty million, the Nikkei fell, number eight eight, money came from London.", 4.8, 8.6),
                      ("Two hundred million, seventeen thousand, ninety nine pounds, put the losses on the books, believed, three hundred million.", 8.8, 12.0),
                      ("A hundred and two million, three hundred and fifty, hundred and fifty, fifty one, thirty one million.", 12.2, 15.0)])
    for nm in names:
        built = SHOTS[nm](1920, 1080, 15.0, demo)
        html, total = C.film_html(built["shots"], 1920, 1080)
        print(nm, [p.name for p in C.stills(html, [0.2, 1.6, total * .4, total * .7, total - .3], work, nm)])
