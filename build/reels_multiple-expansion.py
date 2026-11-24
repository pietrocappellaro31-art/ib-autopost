"""
Reel C, 24 Nov 2026 (slot C 21:00 ET): Format D (an animated calculation) on the story engine (build/story.py),
narrator HEART (Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
The company sells for 25% more and the owners make 50%: multiple expansion in a buyout, with debt.

A worked illustration with round numbers of our own; no buyer, fund, company or statistic is claimed. Assumptions,
said or on screen: EBITDA stays $10 for five years; none of the debt is repaid (the cash the business makes goes on
interest); no fees, no tax on the sale; the price is a multiple of EBITDA.

Every number, worked:
    The buy:        8 x $10 = $80, paid with $40 of debt and $40 of the owners' money.
    Five years:     EBITDA still $10; debt still $40.
    The sale:       10 x $10 = $100: 100 / 80 = 1.25, the company sells for 25% more (+$20).
    The split:      the lender gets $40 back; the owners get 100 - 40 = $60.
    The answer:     60 / 40 = 1.5x, up 50%; the $20 rise all goes to the owners: 20 / 40 = 50% against 20 / 80 = 25%.
    Rule:           a higher exit multiple on the same EBITDA is multiple expansion; with half the price in debt the
                    owners' gain (50%) is twice the company's (25%).
    Close (asked):  sold at 7x: $70; lender $40; owners $30; 30 / 40 = 0.75x, down 25% (not given).
    Comment bonus:  no debt (all $80 from the owners), sold at 10x: 100 / 80 = 1.25x, up 25%.

Hook (24 Nov standard: five candidates, scored 1 to 5 on clash / number in the first three words / second person /
length on screen / would someone send it to a friend preparing for interviews):
    1. "25% more for the company. 50% more for the owners. How?"       clash 5, number 5, you 1, 11 words 5, send 5 = 21
    2. "Bought at 8x, sold at 10x. EBITDA never grew. Owners up 50%?"    clash 4, number 4, you 1, 12 words 5, send 4 = 18
    3. "You buy at 8x and sell at 10x. Did you make 25%?"               clash 3, number 4, you 5, 12 words 5, send 4 = 21
    4. "It's not 25%: same profit, a higher multiple, and owners make 50%."  clash 3, number 3, you 1, 12 words 5, send 3 = 15
       (gives the answer away)
    5. "Answer before the bar lands: who keeps the $20?"                clash 2, number 1, you 1, 9 words 5, send 3 = 12
    Chosen: 1 (two numbers that seem to conflict, the question last and alone); both columns and both tags on screen
    from frame 0. Candidate 3 tied on points; 1 has the stronger clash, the pattern the data favours.

24 Nov, from the performance data (docs/daily/quality-log.md row of 24 Nov): buyouts are among our best families
(debt paydown 1,154 reach); a clash opening; Format D, the third buyout lever after leverage and debt paydown.

    python3 build/reels_multiple-expansion.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "8x", "#3B3F48", 140), (770, 560, "10x", GOLD, 140),
                                              (-100, 1030, "DEBT", "#3B3F48", 160), (770, 1120, "$10", "#0F766E", 140)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-multiple-expansion",
    kicker="IB BUYOUTS",
    mood="curious",
    cover=dict(at=("e", 0, 0, .1), lines=["25% more for the company.", "50% more for the owners.", "How?"],
               hl={"25%": GOLD, "50%": RED, "How?": RED}, avoid=["$60", "1.5x", "EXPANSION"]),
    beats=[
        dict(tag="THE PUZZLE", size=62, hold=.6, hl=["25%", "50%", "How?"],
             say=[("Twenty five percent more for the company.", "25% more for the company."),
                  ("Fifty percent more for the owners.", "50% more for the owners."),
                  ("How?", "How?")],
             art=lambda t0, d, seg: picture("mx_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "thump", .07), (("s", 0, .4), "tick", .04), (("s", 1, .1), "thump", .06), (("s", 1, .4), "tick", .04),
                  (("s", 2, .05), "pop", .05)]),
        dict(tag="THE BUY", size=56, hl=["8x", "$80,", "borrowed."],
             say=[("A buyer pays eight times EBITDA of ten dollars.", "A buyer pays 8x EBITDA of $10."),
                  ("So that's eighty, with forty of it borrowed.", "So that's $80, with $40 of it borrowed.")],
             art=lambda t0, d, seg: picture("mx_buy", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "pop", .05), (("s", 0, .45), "tick", .04), (("s", 0, .65), "tick", .04), (("s", 1, .3), "clink", .05),
                  (("s", 1, .65), "pop", .05)]),
        dict(tag="FIVE YEARS LATER", size=56, hl=["$10.", "$40."],
             say=[("Five years later, EBITDA is still ten dollars.", "Five years later, EBITDA is still $10."),
                  ("None of the debt is paid back, so it's still forty.", "None of the debt is paid back, so it's still $40.")],
             art=lambda t0, d, seg: picture("mx_wait", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "tick", .04), (("s", 0, .35), "tick", .04), (("s", 0, .6), "tick", .04), (("s", 1, .2), "pop", .05),
                  (("s", 1, .6), "thump", .06)]),
        dict(tag="THE SALE", size=56, hl=["10x.", "$100."],
             say=[("But the next buyer pays ten times.", "But the next buyer pays 10x."),
                  ("So the company sells for a hundred.", "So the company sells for $100.")],
             art=lambda t0, d, seg: picture("mx_sale", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "tick", .04), (("s", 0, .6), "pop", .05), (("s", 1, .1), "tick", .04), (("s", 1, .5), "clink", .05),
                  (("e", 1, .05), "thump", .06)]),
        dict(tag="WHO GETS WHAT", size=56, hl=["$40", "$60."],
             say=[("The lender gets its forty back.", "The lender gets its $40 back."),
                  ("The owners get the other sixty.", "The owners get the other $60.")],
             art=lambda t0, d, seg: picture("mx_split", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "pop", .05), (("s", 1, .2), "pop", .05), (("s", 1, .75), "clink", .05)]),
        dict(tag="THE ANSWER", size=54, hl=["50%.", "$20"],
             say=[("Forty in, sixty out: the owners are up fifty percent.", "$40 in, $60 out: the owners are up 50%."),
                  ("The whole twenty dollar rise went to them.", "The whole $20 rise went to them.")],
             art=lambda t0, d, seg: picture("mx_answer", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .35), "pop", .05), (("s", 0, .85), "thump", .07), (("s", 1, .2), "pop", .05), (("s", 1, .6), "clink", .05)]),
        dict(tag="THE RULE", size=52, hl=["multiple", "expansion.", "twice"],
             say=[("That's multiple expansion.", "That's multiple expansion."),
                  ("With half the price in debt, the owners' gain is twice the company's.",
                   "With half the price in debt, the owners' gain is twice the company's.")],
             art=lambda t0, d, seg: picture("mx_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "thump", .07), (("s", 1, .1), "pop", .05), (("s", 1, .5), "pop", .05), (("s", 1, .75), "tick", .04)]),
    ],
    close=dict(say=[("Same deal, but it sells at seven times.", "Same deal, but it sells at 7x."),
                    ("What did the owners make?", "What did the owners make?"),
                    ("Answer in the comments, and follow for tomorrow's.", "Answer in the comments, and follow for tomorrow's.")],
               cols={"comments,": RED, "follow": RED}, bar=True, art_w=720, art_h=576,
               pic=lambda t0, d: picture("mx_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",        # the grid cover (reel_cover.py) on the Reel's own ground
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
