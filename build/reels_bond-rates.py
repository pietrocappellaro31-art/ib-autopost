"""
Reel B, 20 Nov 2026: Format D (an animated calculation) on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram. Why a bond loses value when rates rise.

A worked illustration with round numbers of our own; no issuer, market or forecast is claimed. A plain bond with a
$100 face value and a fixed 5% coupon paid once a year; "rates" means the yield on new bonds of the same risk and
the same time left. Before tax and fees.

Every number, worked:
    The bond:       one year left: it pays the last $5 coupon and the $100 back: 100 + 5 = $105, fixed.
    The new bond:   new bonds pay 10%: $100 buys 100 x 1.10 = $110 in a year.
    The price:      the old bond must also earn 10%: price x 1.10 = 105, price = 105 / 1.1 = 95.4545..., said
                    "just over ninety five dollars", shown $95.45. Check: 95.4545 x 1.1 = 105.
    Ten years left: $5 a year for 10 years, then $100, discounted at 10%:
                    sum 5 / 1.1^t (t = 1 to 10) + 100 / 1.1^10 = 30.72 + 38.55 = 69.277..., said "about sixty nine
                    dollars", shown $69 (a fall of about $31, against about $4.55 with one year left).
    The rule:       rates up, prices down; the longer the time left, the bigger the fall (for these two bonds).
    Close (asked):  rates fall to 2% instead: 105 / 1.02 = 102.94.
    Comment bonus:  two years left at 10%: 5 / 1.1 + 105 / 1.21 = 4.55 + 86.78 = 91.32.

20 Nov, from the performance data (docs/daily/quality-log.md row of 20 Nov): a short, concrete, number-led hook,
the question alone; Format D. Reel A today is Format B.

The 19 Nov next improvement: sketch._cam frames the part being explained in every beat and pulls back on the next
sentence; the price columns re-scale on their words; the see-saw tips the whole board.

    python3 build/reels_bond-rates.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "5%", GOLD, 150), (770, 560, "10%", "#3B3F48", 160),
                                              (-100, 1030, "$105", "#0F766E", 160), (770, 1120, "BOND", GOLD, 170)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-bond-rates",
    kicker="IB CALCULATION",
    mood="calm",
    cover=dict(at=("e", 0, 1, .3), lines=["A $100 bond pays 5%.", "Rates rise to 10%.", "What's it worth?"],
               hl={"5%.": GOLD, "10%.": RED, "worth?": RED}, avoid=["$95.45", "$69", "FIXED"]),
    beats=[
        dict(tag="THE PUZZLE", size=60, hold=.6, hl=["5%.", "10%.", "worth"],
             say=[("A hundred dollar bond pays five percent.", "A $100 bond pays 5%."),
                  ("Rates rise to ten percent, so what's it worth now?", "Rates rise to 10%, so what's it worth now?")],
             art=lambda t0, d, seg: picture("bd_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .7), "pop", .05), (("s", 1, .2), "tick", .04), (("s", 1, .5), "thump", .08), (("s", 1, .62), "knock", .06)]),
        dict(tag="ONE YEAR LEFT", size=56, hl=["$105.", "fixed,"],
             say=[("It has one year left, then it pays you a hundred and five.", "It has one year left, then it pays you $105."),
                  ("That payment is fixed, whatever happens to rates.", "That payment is fixed, whatever happens to rates.")],
             art=lambda t0, d, seg: picture("bd_bond", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "tick", .04), (("s", 0, .55), "thump", .07), (("s", 0, .8), "clink", .06), (("s", 1, .15), "knock", .07),
                  (("s", 1, .25), "thump", .08)]),
        dict(tag="THE NEW BOND", size=54, hl=["10%:", "$110.", "$105?"],
             say=[("But a new bond now pays ten percent: a hundred buys a hundred and ten.", "But a new bond now pays 10%: $100 buys $110."),
                  ("So who pays a hundred for your hundred and five?", "So who pays $100 for your $105?")],
             art=lambda t0, d, seg: picture("bd_rival", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "pop", .05), (("s", 0, .62), "thump", .07), (("s", 0, .8), "clink", .06), (("s", 1, .1), "thump", .07),
                  (("s", 1, .5), "pop", .05), (("s", 1, .62), "knock", .06)]),
        dict(tag="THE PRICE", size=54, hl=["10%", "$95."],
             say=[("Your price falls until it earns ten percent too.", "Your price falls until it earns 10% too."),
                  ("A hundred and five, divided by one point one, is just over ninety five dollars.",
                   "$105, divided by 1.1, is just over $95.")],
             art=lambda t0, d, seg: picture("bd_price", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "knock", .06), (("s", 0, .7), "pop", .05), (("s", 1, .05), "tick", .04), (("s", 1, .35), "tick", .04),
                  (("s", 1, .7), "thump", .08)]),
        dict(tag="TEN YEARS LEFT", size=54, hl=["$69.", "longer", "bigger"],
             say=[("With ten years left, the same jump takes it to about sixty nine dollars.",
                   "With ten years left, the same jump takes it to about $69."),
                  ("The longer the bond, the bigger the fall.", "The longer the bond, the bigger the fall.")],
             art=lambda t0, d, seg: picture("bd_long", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "clink", .04), (("s", 0, .3), "clink", .04), (("s", 0, .7), "thump", .09), (("s", 1, .15), "pop", .05),
                  (("s", 1, .55), "pop", .05)]),
        dict(tag="THE RULE", size=58, hl=["up,", "down.", "today."],
             say=[("Rates up, bond prices down.", "Rates up, bond prices down."),
                  ("The payments never change, only what they're worth today.", "The payments never change, only what they're worth today.")],
             art=lambda t0, d, seg: picture("bd_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "knock", .07), (("s", 0, .6), "thump", .08), (("s", 1, .1), "clink", .04), (("s", 1, .3), "clink", .04),
                  (("s", 1, .45), "thump", .07), (("s", 1, .55), "pop", .05)]),
    ],
    close=dict(say=[("Now say rates fall to two percent instead.", "Now say rates fall to 2% instead."),
                    ("What's the one year bond worth?", "What's the one-year bond worth?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED},
               pic=lambda t0, d: picture("bd_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
