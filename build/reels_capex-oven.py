"""
Reel A, 20 Nov 2026: Format B (a short financial story) on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram. Capitalise, then depreciate: a baker spends
$100 on an oven, and her profit does not fall by $100.

A worked illustration with round numbers of our own; no company, person or tax rule is claimed. Before tax; the oven
is paid in cash on day one, lasts five years, has no scrap value and is depreciated in equal amounts (straight line,
the usual default for a long-lived asset: it is capitalised as property, plant and equipment, then depreciated over
its useful life; IAS 16 and US GAAP ASC 360 both work this way). Sales, costs and cash are the same every year apart
from the oven; no working capital.

Every number, worked:
    A normal year:  sales $150 - costs (flour, wages, rent) $100 = profit $50 (before tax).
    The trap:       expensing the whole oven in year 1: 50 - 100 = -$50.
    Spread it:      $100 / 5 years = $20 a year of depreciation; year 1 profit 50 - 20 = $30.
    Cash, year 1:   the business brings in 150 - 100 = $50 of cash, and the oven costs $100 in cash today:
                    50 - 100 = -$50 ("cash is down fifty, while profit says thirty").
    Five years:     profit 5 x 30 = $150; cash -50 + 4 x 50 = $150 (equal: same money, different timing).
    Close (asked):  the same oven lasting 10 years: $100 / 10 = $10 a year; year 1 profit 50 - 10 = $40.
    Comment bonus:  after 2 years of $20 the oven's book value is 100 - 40 = $60.

20 Nov, from the performance data (docs/daily/quality-log.md row of 20 Nov): a short, concrete hook (11 words, a
number and a yes/no question), the pattern of the four Reels since 14 Nov that reached 1,000+; Format B, not used this
week. Reel B today is Format D.

The 19 Nov next improvement: every beat has one large move, sketch._cam, a camera that frames the part being
explained and pulls back on the next sentence (zoom 1.2 to 1.3), on top of the columns re-scaling through zero.

    python3 build/reels_capex-oven.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "$100", GOLD, 160), (770, 560, "OVEN", "#3B3F48", 170),
                                              (-100, 1030, "5Y", "#0F766E", 150), (770, 1120, "$150", GOLD, 160)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-capex-oven",
    kicker="IB CONCEPT",
    mood="calm",
    cover=dict(at=("e", 0, 1, .3), lines=["$100 on an oven.", "Does profit fall", "by $100?"],
               hl={"$100": GOLD, "$100?": RED}, avoid=["$20", "$30", "DEPRECIATION"]),
    beats=[
        dict(tag="THE PUZZLE", size=60, hold=.6, hl=["$100", "$100?"],
             say=[("She spends a hundred dollars on a new oven.", "She spends $100 on a new oven."),
                  ("Does her profit fall by a hundred dollars?", "Does her profit fall by $100?")],
             art=lambda t0, d, seg: picture("ov_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "clink", .06), (("s", 0, .55), "thump", .08), (("s", 1, .25), "thump", .08), (("s", 1, .8), "pop", .05)]),
        dict(tag="A NORMAL YEAR", size=56, hl=["$150", "$50."],
             say=[("Her bakery sells a hundred and fifty dollars of bread a year.", "Her bakery sells $150 of bread a year."),
                  ("Flour, wages and rent cost a hundred, so profit is fifty.", "Flour, wages and rent cost $100, so profit is $50.")],
             art=lambda t0, d, seg: picture("ov_year", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "thump", .07), (("s", 1, .02), "knock", .06), (("s", 1, .2), "knock", .06), (("s", 1, .38), "knock", .06),
                  (("s", 1, .62), "pop", .05), (("s", 1, .85), "ding", .04)]),
        dict(tag="THE TRAP", size=56, hl=["-$50.", "five"],
             say=[("Count the whole oven this year, and profit is minus fifty.", "Count the whole oven this year, and profit is -$50."),
                  ("But the oven bakes for five years, not one.", "But the oven bakes for five years, not one.")],
             art=lambda t0, d, seg: picture("ov_trap", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "thump", .09), (("s", 0, .5), "knock", .07), (("s", 1, .2), "tick", .04), (("s", 1, .34), "tick", .04),
                  (("s", 1, .48), "tick", .04), (("s", 1, .62), "tick", .04), (("s", 1, .75), "tick", .04)]),
        dict(tag="SPREAD IT", size=56, hl=["$20", "depreciation,", "$30."],
             say=[("So accountants spread it: twenty dollars a year, for five years.", "So accountants spread it: $20 a year, for five years."),
                  ("That's depreciation, and this year's profit is thirty.", "That's depreciation, and this year's profit is $30.")],
             art=lambda t0, d, seg: picture("ov_spread", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .35), "pop", .05), (("s", 0, .5), "clink", .05), (("s", 0, .65), "clink", .05), (("s", 0, .8), "clink", .05),
                  (("s", 1, .1), "thump", .08), (("s", 1, .6), "knock", .06)]),
        dict(tag="THE CASH", size=56, hl=["$100", "-$50,", "$30."],
             say=[("Cash is different: the hundred dollars left her account today.", "Cash is different: the $100 left her account today."),
                  ("So this year, cash is down fifty, while profit says thirty.", "So this year, cash is down $50, while profit says $30.")],
             art=lambda t0, d, seg: picture("ov_cash", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "clink", .06), (("s", 0, .4), "clink", .05), (("s", 0, .55), "thump", .08), (("s", 1, .25), "pop", .05),
                  (("s", 1, .7), "pop", .05)]),
        dict(tag="FIVE YEARS", size=54, hl=["$150.", "timing."],
             say=[("Over five years, both add up to a hundred and fifty.", "Over five years, both add up to $150."),
                  ("Same money, different timing, and that's why bankers look at both.", "Same money, different timing, and that's why bankers look at both.")],
             art=lambda t0, d, seg: picture("ov_total", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "tick", .04), (("s", 0, .25), "tick", .04), (("s", 0, .5), "tick", .04), (("s", 0, .7), "tick", .04),
                  (("s", 0, .95), "ding", .04), (("s", 1, .3), "pop", .05), (("s", 1, .85), "pop", .05)]),
    ],
    close=dict(say=[("Same oven, but it lasts ten years.", "Same oven, but it lasts 10 years."),
                    ("What's her profit in year one?", "What's her profit in year 1?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED},
               pic=lambda t0, d: picture("ov_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
