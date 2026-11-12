"""
Viral reference proposal 1 (R2, approved by Pietro on 11 Nov): "Same $100 company. Two ways to pay."
A split-screen race with no voice, built to loop at 12 s. Effects only in the file (no music: Pietro adds
it in the app, and R2's reference carries a strong beat, about 100 BPM).

Two buyers, the same company, bought for $100 and sold for $150 (illustrative round numbers, nothing
claimed about any real deal):

    Top, all equity:    put in $100 of your own money, no debt.
                        Sold for $150 -> nothing to repay -> you get $150.
                        Multiple on your money (MOIC) = 150 / 100 = 1.5x.
    Bottom, with debt:  put in $40 of your own money, borrow $60 (40 + 60 = 100).
                        Sold for $150 -> repay the $60 debt -> you get 150 - 60 = $90.
                        MOIC = 90 / 40 = 2.25x.
    Same company, same gain of $50. The debt changes who owns the gain per dollar put in.

    The honest part, on screen: debt cuts both ways. Sold for $80 instead: top gets $80 (0.8x),
    bottom gets 80 - 60 = $20 (0.5x). Interest on the debt is left out to keep the arithmetic to
    one line; it would lower the bottom figure a little, and the caption says so.

    python3 build/reels_two-ways-to-pay.py
"""

import json
import sys

from motion import A, build, OUT
import sfx

SLUG = "w2-two-ways-to-pay"
TOTAL = 12.0
GOLD, RED, TEAL, INK = "#F2C35B", "#D93A12", "#0F766E", "#0A0A0A"
END = 11.35                                   # the "after" state fades out here and the opening frame fades back in
PX = 2.0                                      # px per $ in the bars

# panel geometry (inside the 752 x 1210 safe column)
HEAD_H, PANEL_H, GAP = 236, 452, 22
BASE = 394                                    # bar baseline inside a panel
BAR_X, BAR_W = 34, 210


def block(y_top, h, fill, label, color="#fff", dash=False, size=34):
    border = f"6px {'dashed' if dash else 'solid'} {INK}"
    return (f'<div style="position:absolute;left:{BAR_X}px;top:{y_top}px;width:{BAR_W}px;height:{h}px;box-sizing:border-box;'
            f'background:{fill};border:{border};border-radius:12px;display:flex;flex-direction:column;align-items:center;'
            f'justify-content:center;color:{color};font-weight:700;font-size:{size}px;line-height:1.1;text-align:center">{label}</div>')


def gain(y_top):
    """The $50 gain block, growing up from the top of the equity block as the company value rises."""
    h = 50 * PX
    inner = block(0, h, TEAL, "GAIN $50").replace(f"left:{BAR_X}px;top:0px", "left:0;top:0")
    return A(inner, "growY", 1.0, 2.8, style=f"position:absolute;left:{BAR_X}px;top:{y_top - h}px;width:{BAR_W}px;height:{h}px")


def amt(lbl, big):
    return f'<span style="font-size:24px;letter-spacing:.06em">{lbl}</span><span class="num" style="font-size:46px">{big}</span>'


def figure(mode_at, cheer):
    """A stick figure, arms down; at mode_at it either cheers (arms up, bouncing) or shrugs (palms up)."""
    body = ('<circle cx="60" cy="34" r="24" fill="#fff" stroke="#0A0A0A" stroke-width="6"/>'
            '<path d="M60 58 L60 128 M60 128 L32 186 M60 128 L88 186" stroke="#0A0A0A" stroke-width="7" stroke-linecap="round" fill="none"/>')
    down = '<path d="M60 78 L30 122 M60 78 L90 122" stroke="#0A0A0A" stroke-width="7" stroke-linecap="round" fill="none"/>'
    up = (f'<path d="M60 78 L24 22 M60 78 L96 22" stroke="{TEAL}" stroke-width="8" stroke-linecap="round" fill="none"/>'
          if cheer else
          '<path d="M60 80 L22 90 L12 70 M60 80 L98 90 L108 70" stroke="#0A0A0A" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
    face = ('<path d="M48 40 Q60 52 72 40" stroke="#0A0A0A" stroke-width="4" fill="none" stroke-linecap="round"/>' if cheer else
            '<path d="M48 46 L72 46" stroke="#0A0A0A" stroke-width="4" fill="none" stroke-linecap="round"/>')
    svg = lambda inner: f'<svg viewBox="0 0 120 200" width="120" height="200" style="position:absolute;left:0;top:0;overflow:visible">{inner}</svg>'
    arms_down = A(svg(down), "life", -1, mode_at + 1, fi=.01, fo=.08)
    arms_mode = A(svg(up + face), "life", mode_at, END - mode_at, fi=.08, fo=.3)
    arms_back = A(svg(down), "life", END, 2, fi=.4, fo=.01)
    inner = svg(body) + arms_down + arms_mode + arms_back
    if cheer:
        inner = A(inner, "beat", mode_at, 1, n=3, style="position:absolute;left:0;top:0;width:120px;height:200px;transform-origin:center bottom")
    return f'<div style="position:absolute;right:26px;bottom:34px;width:120px;height:200px">{inner}</div>'


def panel(top, kind):
    """kind 'equity' (all equity) or 'debt' ($40 equity + $60 debt)."""
    debt = kind == "debt"
    eq_in = 40 if debt else 100
    out_v = 90 if debt else 150
    moic = 2.25 if debt else 1.5
    chip_txt = "$40 EQUITY + $60 DEBT" if debt else "ALL EQUITY"
    chip_col = RED if debt else TEAL
    h = ""
    h += (f'<div style="position:absolute;left:30px;top:24px;padding:8px 18px;border-radius:14px;background:{chip_col};color:#fff;'
          f'font-size:28px;font-weight:700;letter-spacing:.04em">{chip_txt}</div>')
    h += f'<div style="position:absolute;left:24px;right:24px;top:{BASE}px;height:6px;border-radius:3px;background:{INK}"></div>'
    # the opening bars (also the closing frame, so the loop seam is invisible)
    if debt:
        d_h, e_h = 60 * PX, 40 * PX
        start = block(BASE - d_h, d_h, RED, "DEBT $60") + block(BASE - d_h - e_h, e_h, GOLD, "YOU $40", INK)
        # during the play: the debt block leaves at the sale, the equity and the gain drop down by its height
        play = (A(A(block(BASE - d_h, d_h, RED, "DEBT $60"), "slide", 4.9, .55, x0=0, x1=520, y0=0, y1=0, ease="in"),
                  "life", -1, 6.4, fi=.01, fo=.15)
                + A(A(block(BASE - d_h - e_h, e_h, GOLD, "YOU $40", INK)
                      + gain(BASE - d_h - e_h),
                      "slide", 5.5, .5, x0=0, x1=0, y0=0, y1=d_h, ease="out"),
                    "life", -1, END + 1, fi=.01, fo=.4))
        repaid = A('<div style="font-size:30px;font-weight:700;color:#D93A12;white-space:nowrap">&minus;$60 to the bank</div>',
                   "life", 5.0, END - 5.0, fi=.2, fo=.3, style=f"position:absolute;left:{BAR_X + 4}px;top:{BASE + 12}px")
    else:
        e_h = 100 * PX
        start = block(BASE - e_h, e_h, GOLD, "YOU $100", INK)
        play = A(block(BASE - e_h, e_h, GOLD, "YOU $100", INK)
                 + gain(BASE - e_h),
                 "life", -1, END + 1, fi=.01, fo=.4)
        repaid = A('<div style="font-size:30px;font-weight:700;opacity:.55;white-space:nowrap">no debt to repay</div>',
                   "life", 5.0, END - 5.0, fi=.2, fo=.3, style=f"position:absolute;left:{BAR_X + 4}px;top:{BASE + 12}px")
    h += play + A(start, "life", END, 2, fi=.45, fo=.01, style="position:absolute;inset:0")
    h += repaid
    # the numbers column
    col = 280
    row = lambda y, inner: f'<div style="position:absolute;left:{col}px;top:{y}px;display:flex;flex-direction:column;line-height:1.05">{inner}</div>'
    value = A('$100', "count", 1.0, 2.8, cls="num", style="font-size:46px", **{"from": 100, "to": 150, "pre": "$", "lin": 1, "show": 1})
    value = (A(value, "life", -1, END + 1, fi=.01, fo=.4, style="position:absolute;left:0;top:0")
             + A('<span class="num" style="font-size:46px">$100</span>', "life", END + .05, 2, fi=.4, fo=.01, style="position:absolute;left:0;top:0"))
    h += row(78, '<span style="font-size:24px;letter-spacing:.06em;opacity:.65">COMPANY</span>'
             + f'<div style="position:relative;height:50px;width:200px">{value}</div>')
    h += row(160, amt('<span style="opacity:.65">YOU PUT IN</span>', f"${eq_in}"))
    out = A("$0", "count", 5.9, 1.0, cls="num", style=f"font-size:46px;color:{TEAL if not debt else INK}",
            **{"from": 0, "to": out_v, "pre": "$"})
    h += A(row(242, '<span style="font-size:24px;letter-spacing:.06em;opacity:.65">YOU GET</span>' + out),
           "life", 5.8, END - 5.8, fi=.2, fo=.35, style="position:absolute;inset:0")
    big = A("1.0x", "count", 7.0, 1.0, cls="num", style=f"font-size:{80 if debt else 74}px;color:{RED if debt else INK}",
            **{"from": 1, "to": moic, "dec": 2 if debt else 1, "suf": "x"})
    h += A(f'<div style="position:absolute;left:{col}px;top:318px;line-height:1">{big}</div>',
           "life", 6.95, END - 6.95, fi=.1, fo=.35, style="position:absolute;inset:0")
    # the sale stamp
    h += A(f'<div style="position:absolute;right:30px;top:22px;transform:rotate(-8deg);border:5px solid {RED};color:{RED};'
           f'border-radius:10px;padding:4px 14px;font-size:34px;font-weight:700;background:rgba(255,255,255,.85)">SOLD $150</div>',
           "life", 4.2, END - 4.2, fi=.01, fo=.3, style="position:absolute;inset:0")
    h += f'<div style="position:absolute;inset:0">{figure(7.9, cheer=debt)}</div>'
    card = (f'<div style="position:absolute;left:0;right:0;top:{top}px;height:{PANEL_H}px;background:#fff;border-radius:28px;'
            f'box-shadow:0 22px 50px rgba(10,10,10,.13),0 2px 6px rgba(10,10,10,.08);overflow:hidden">{h}</div>')
    return card


def headline():
    a = ('<div style="font-family:\'Serif\',serif;font-weight:700;font-size:78px;line-height:1.02;letter-spacing:-.03em">Same $100 company.</div>'
         f'<div class="it" style="font-size:66px;color:{TEAL};margin-top:8px">Two ways to pay.</div>')
    b = ('<div style="font-family:\'Serif\',serif;font-weight:700;font-size:56px;line-height:1.04;letter-spacing:-.03em;white-space:nowrap">Same company. More debt.</div>'
         f'<div class="it" style="font-size:52px;color:{RED};margin-top:6px">Bigger multiple on your money.</div>'
         '<div style="font-size:27px;font-weight:500;opacity:.7;margin-top:12px;line-height:1.25">Debt cuts both ways: sell for $80 and it\'s 0.5x, not 0.8x.</div>')
    box = "position:absolute;left:0;right:0;top:0"
    return (A(a, "life", -1, 10.3, fi=.01, fo=.3, style=box)
            + A(b, "life", 9.0, END - 9.0, fi=.35, fo=.35, style=box)
            + A(a, "life", END + .1, 2, fi=.4, fo=.01, style=box))


def scene():
    html = (f'<div style="position:relative;width:752px;height:{HEAD_H + 2 * PANEL_H + 2 * GAP}px">'
            + headline()
            + panel(HEAD_H + GAP, "equity")
            + panel(HEAD_H + 2 * GAP + PANEL_H, "debt")
            + "</div>")
    return [dict(dur=TOTAL, push=0, html=html)]


def sounds():
    ev = [("pop", 1.0), ("pop", 1.05, .2)]
    ev += [("tick", 1.0 + .233 * k, .18) for k in range(13)]          # the company value ticking 100 -> 150
    ev += [("thump", 4.2), ("pop", 4.22, .25)]                        # SOLD
    ev += [("pop", 4.95, .3), ("thump", 5.5, .3)]                     # the debt leaves, the blocks drop
    ev += [("tick", 5.9 + .1 * k, .16) for k in range(10)]            # what you get, counting
    ev += [("tick", 7.0 + .125 * k, .2) for k in range(8)]            # the multiples
    ev += [("ding", 8.0, .16), ("pop", 7.9, .3), ("pop", 8.15, .22), ("pop", 8.4, .18)]   # the cheer bounces
    ev += [("pop", 9.0, .3), ("pop", 9.5, .18)]                       # the moral
    return ev


if __name__ == "__main__":
    mp4, cover, problems = build(SLUG, scene(), theme="paper", cover_at=.5, crf=20)
    buf = sfx.track(sounds(), TOTAL + .6)
    final = OUT / SLUG / f"{SLUG}.mp4"
    tmp = mp4.with_name(SLUG + "-fx.mp4")
    sfx.mux(mp4, buf, tmp)                        # effects only, -24 LUFS: the music Pietro adds carries it
    tmp.replace(final)
    (OUT / SLUG / "cover.jpg").write_bytes(cover.read_bytes())
    print("problems:", problems)
