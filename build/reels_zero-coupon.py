"""
Reel A, 24 Nov 2026 (slot A 12:30 ET): Format C (one surprising concept) on the story engine (build/story.py),
narrator HEART (Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
A bond that pays 0% interest, and why anyone buys it: the zero coupon bond.

A worked illustration with round numbers of our own; no issuer, fund or statistic is claimed. Assumptions, said or on
screen: the bond pays $100 back at the end of year 2 and nothing before; other bonds like it (same risk, same term)
pay 5% a year, compounded yearly; no tax, no default.

Every number, worked:
    Price today:    100 / 1.05 = 95.238 (shown $95.24); 95.238 / 1.05 = 90.703 (shown $90.70); 100 / 1.1025 = 90.70.
    Held:           90.70 x 1.05 = 95.24 (+$4.54, 5% of 90.70 = 4.535); 95.24 x 1.05 = 100.00 (+$4.76, 5% of 95.24).
    Interest:       100 - 90.70 = $9.30 over two years = 10.25% in total = 5% a year compounded (1.05 x 1.05 = 1.1025).
    Rate:           a coupon bond bought at $100 paying 5% ($5 in year 1, $105 in year 2) also yields 5% a year; the
                    zero pays it in one go, at the end.
    Rule, 2nd move: rates up to 8%: 100 / 1.08^2 = 100 / 1.1664 = $85.73: higher rates, a bigger gap.
    Close (asked):  other bonds pay 10%: 100 / 1.21 = $82.64 (not given).
    Comment bonus:  three years to go at 5%: 100 / 1.157625 = $86.38.

Hook (24 Nov standard: five candidates, scored 1 to 5 on clash / number in the first three words / second person /
length on screen / would someone send it to a friend preparing for interviews):
    1. "It pays 0% interest. So why does anyone buy this bond?"          clash 5, number 5, you 3, 11 words 5, send 5 = 23
    2. "A $100 bond that pays nothing. You'd still pay $90 for it."       clash 4, number 5, you 5, 12 words 5, send 3 = 22
       (gives the answer away)
    3. "It's not free money: a 0% bond still earns 5% a year."            clash 3, number 3, you 1, 12 words 5, send 3 = 15
    4. "You have $90.70. A bond pays you 0%. Is it a good buy?"           clash 3, number 5, you 5, 12 words 5, send 3 = 21
    5. "Answer before the bar lands: what's a 0% bond worth?"             clash 2, number 2, you 1, 9 words 5, send 3 = 13
    Chosen: 1 (the clash: an investment that pays nothing, and people buy it), on screen from frame 0.

24 Nov, from the performance data (docs/daily/quality-log.md row of 24 Nov): bonds are among our best families
(the 20 Nov bond Reel 1,205 reach, the longest average watch, 14.3 s); a short clash opening; Format C.

    python3 build/reels_zero-coupon.py HEART
"""

import sys

from motion import A
from sketch import picture, _ptag
from story import make, RED

TEAL_INK, GOLD = "#5EC8B4", "#F2C35B"
PIC = dict(w=752, h=640)


def chip(label, fill, w=190, color="#fff"):
    return (f'<svg width="{w}" height="{w * .6:.0f}" viewBox="0 0 {w} {w * .6:.0f}" style="overflow:visible">'
            + _ptag(w / 2, w * .3, w * .95, label, fill, color, round(w * .23)) + "</svg>")


def floaters(total):
    """Faint tags drifting at the edges, clear of the text (never the answer)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "0%", "#3B3F48", 140), (770, 560, "$100", GOLD, 150),
                                              (-100, 1030, "2 YRS", "#0F766E", 160), (770, 1120, "5%", "#3B3F48", 140)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-zero-coupon",
    kicker="IB CONCEPT",
    mood="curious",
    cover=dict(at=("e", 0, 1, .3), lines=["It pays 0% interest.", "So why does anyone", "buy this bond?"],
               hl={"0%": RED, "buy": GOLD, "bond?": GOLD}, avoid=["$90.70", "$9.30", "BELOW FACE"]),
    beats=[
        dict(tag="THE PUZZLE", size=62, hold=.6, hl=["0%", "buy"],
             say=[("It pays zero percent interest.", "It pays 0% interest."),
                  ("So why does anyone buy this bond?", "So why does anyone buy this bond?")],
             art=lambda t0, d, seg: picture("zc_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "thump", .07), (("s", 0, .3), "tick", .04), (("s", 0, .5), "tick", .04), (("s", 0, .8), "thump", .06),
                  (("s", 1, .2), "pop", .05), (("s", 1, .6), "pop", .05)]),
        dict(tag="THE CATCH", size=56, hl=["$100", "years.", "don't"],
             say=[("It pays a hundred dollars back in two years.", "It pays $100 back in two years."),
                  ("But you don't pay a hundred for it.", "But you don't pay $100 for it.")],
             art=lambda t0, d, seg: picture("zc_catch", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .35), "pop", .05), (("s", 0, .6), "clink", .05), (("s", 1, .1), "pop", .05), (("s", 1, .45), "tick", .04),
                  (("s", 1, .7), "pop", .05)]),
        dict(tag="THE PRICE", size=56, hl=["5%", "$90.70."],
             say=[("Say other bonds like it pay five percent a year.", "Say other bonds like it pay 5% a year."),
                  ("Then it sells for about ninety dollars and seventy cents.", "Then it sells for about $90.70.")],
             art=lambda t0, d, seg: picture("zc_price", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .35), "pop", .05), (("s", 0, .55), "pop", .05), (("s", 1, .1), "tick", .04), (("s", 1, .6), "tick", .04),
                  (("e", 1, .1), "thump", .06)]),
        dict(tag="THE INTEREST", size=56, hl=["$100.", "$9.30", "interest."],
             say=[("Hold it for two years, and that ninety seventy becomes a hundred.",
                   "Hold it for two years, and that $90.70 becomes $100."),
                  ("The nine dollars and thirty cents in between is your interest.",
                   "The $9.30 in between is your interest.")],
             art=lambda t0, d, seg: picture("zc_grow", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .4), "pop", .05), (("s", 0, .75), "pop", .05), (("s", 1, .1), "tick", .04), (("s", 1, .45), "thump", .07)]),
        dict(tag="SAME 5%", size=56, hl=["5%", "end."],
             say=[("That's still five percent a year, like the other bonds.", "That's still 5% a year, like the other bonds."),
                  ("It's just paid in one go, at the end.", "It's just paid in one go, at the end.")],
             art=lambda t0, d, seg: picture("zc_rate", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "pop", .05), (("s", 0, .4), "pop", .05), (("s", 1, .1), "clink", .05), (("s", 1, .3), "clink", .05),
                  (("s", 1, .6), "thump", .07)]),
        dict(tag="THE RULE", size=54, hl=["below", "gap", "interest.", "higher"],
             say=[("A zero coupon bond sells below its face value.", "A zero coupon bond sells below its face value."),
                  ("The gap is your interest.", "The gap is your interest."),
                  ("And the higher rates go, the bigger the gap.", "And the higher rates go, the bigger the gap.")],
             art=lambda t0, d, seg: picture("zc_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "pop", .05), (("s", 0, .8), "thump", .06), (("s", 1, .2), "tick", .04), (("s", 2, .3), "pop", .05),
                  (("s", 2, .7), "tick", .04)]),
    ],
    close=dict(say=[("Now other bonds pay ten percent.", "Now other bonds pay 10%."),
                    ("What's it worth now?", "What's it worth now?"),
                    ("Answer in the comments, and follow for tomorrow's.", "Answer in the comments, and follow for tomorrow's.")],
               cols={"comments,": RED, "follow": RED}, bar=True, art_w=720, art_h=576,
               pic=lambda t0, d: picture("zc_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",        # the grid cover (reel_cover.py) on the Reel's own ground
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
