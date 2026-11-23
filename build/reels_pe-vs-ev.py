"""
Reel C, 23 Nov 2026 (slot C 21:00 ET): Format D (an animated calculation) on the story engine (build/story.py),
narrator HEART (Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
Same business, P/E 10x against 4x: the difference is debt, and EV / EBITDA sees through it.

A worked illustration with round numbers of our own; companies A, B and C are invented, no company or statistic is
claimed. Assumptions, said or on screen: tax left out (so earnings = operating profit - interest); no cash; the debt
is worth its face value; both businesses are worth the same, EV $400.

Every number, worked:
    Both:           EBITDA $50; depreciation $10; operating profit 50 - 10 = $40; EV $400.
    A:              no debt: equity value 400 - 0 = $400; earnings $40; P/E = 400 / 40 = 10x.
    B:              debt $300 at 5%: interest 300 x 0.05 = $15; earnings 40 - 15 = $25; equity value 400 - 300 =
                    $100; P/E = 100 / 25 = 4x.
    Catch:          EV / EBITDA = 400 / 50 = 8x for both.
    Rule:           P/E is the shares' price over the shares' earnings, both after the lenders; it mixes the business
                    with how it is funded. EV / EBITDA covers lenders and shareholders on both sides, so it compares
                    businesses with different debt.
    Close (asked):  C, same business, $200 of debt at 5%: interest $10, earnings $30, equity $200, P/E 200 / 30 =
                    6.67, about 6.7x (not given).
    Comment bonus:  B's debt at 10% instead: interest $30, earnings $10, equity $100, P/E 10x (the same as A).

23 Nov, from the performance data (docs/daily/quality-log.md row of 23 Nov): a hook that sets two numbers against
each other (10x and 4x), 14 words on screen, on the story engine; Format D, last used 22 Nov (A).

    python3 build/reels_pe-vs-ev.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "P/E", GOLD, 140), (770, 560, "DEBT", "#3B3F48", 150),
                                              (-100, 1030, "EV", "#0F766E", 130), (770, 1120, "10x", GOLD, 140)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-pe-vs-ev",
    kicker="IB CALCULATION",
    mood="curious",
    cover=dict(at=("e", 0, 2, .3), lines=["Same business.", "One trades at 10x earnings,", "the other at 4x.", "Which is cheaper?"],
               hl={"10x": GOLD, "4x.": GOLD, "cheaper?": RED}, avoid=["8x", "DEBT", "$300"]),
    beats=[
        dict(tag="THE CHOICE", size=60, hold=.6, hl=["10x", "4x.", "cheaper?"],
             say=[("Same business.", "Same business."),
                  ("One trades at ten times earnings, the other at four times.", "One trades at 10x earnings, the other at 4x."),
                  ("Which one is cheaper?", "Which one is cheaper?")],
             art=lambda t0, d, seg: picture("pe_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 1, .35), "pop", .05), (("s", 1, .8), "pop", .05), (("s", 2, .1), "thump", .07)]),
        dict(tag="THE BUSINESS", size=56, hl=["$50", "$400.", "tax"],
             say=[("Both make fifty dollars of EBITDA, and the whole business is worth four hundred.",
                   "Both make $50 of EBITDA, and the whole business is worth $400."),
                  ("We'll leave tax out.", "We'll leave tax out.")],
             art=lambda t0, d, seg: picture("pe_business", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "pop", .05), (("s", 0, .45), "pop", .05), (("s", 0, .6), "tick", .04), (("s", 1, .3), "thump", .07)]),
        dict(tag="COMPANY A", size=56, hl=["debt.", "$40.", "10x."],
             say=[("Company A has no debt.", "Company A has no debt."),
                  ("After ten of depreciation, it earns forty.", "After $10 of depreciation, it earns $40."),
                  ("Its shares are worth all four hundred, so its P E is ten times.",
                   "Its shares are worth all $400, so its P/E is 10x.")],
             art=lambda t0, d, seg: picture("pe_a", t0, d, seg=seg, **PIC),
             sfx=[(("s", 1, .4), "pop", .05), (("s", 2, .25), "tick", .04), (("s", 2, .75), "thump", .07)]),
        dict(tag="COMPANY B", size=54, hl=["$300,", "$25,", "$100.", "4x."],
             say=[("Company B owes three hundred, at five percent.", "Company B owes $300, at 5%."),
                  ("Fifteen of interest leaves it earning twenty five, and its shares are worth just a hundred.",
                   "$15 of interest leaves it earning $25, and its shares are worth just $100."),
                  ("Its P E is four times.", "Its P/E is 4x.")],
             art=lambda t0, d, seg: picture("pe_b", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "thump", .06), (("s", 1, .2), "clink", .05), (("s", 1, .75), "pop", .05), (("s", 2, .6), "thump", .07)]),
        dict(tag="THE CATCH", size=54, hl=["debt.", "8x"],
             say=[("B only looks cheap because of its debt.", "B only looks cheap because of its debt."),
                  ("Price the whole business, and both are eight times EBITDA.",
                   "Price the whole business, and both are 8x EBITDA.")],
             art=lambda t0, d, seg: picture("pe_catch", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .5), "tick", .04), (("s", 1, .15), "pop", .05), (("s", 1, .6), "pop", .05), (("s", 1, .85), "pop", .05)]),
        dict(tag="THE RULE", size=56, hl=["funded.", "EBITDA."],
             say=[("P E mixes the business with how it's funded.", "P/E mixes the business with how it's funded."),
                  ("To compare businesses, bankers use enterprise value over EBITDA.",
                   "To compare businesses, bankers use EV / EBITDA.")],
             art=lambda t0, d, seg: picture("pe_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "pop", .05), (("s", 0, .7), "pop", .05), (("s", 1, .3), "tick", .04), (("s", 1, .7), "pop", .05)]),
    ],
    close=dict(say=[("Same business, but two hundred of debt at five percent.", "Same business, but $200 of debt at 5%."),
                    ("What's its P E?", "What's its P/E?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED}, bar=True, art_w=720, art_h=576,
               pic=lambda t0, d: picture("pe_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,
    music=False,
    lufs=-16,
    theme="black",
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
