"""
Reel A, 25 Nov 2026 (slot A 12:30 ET): Format C (one surprising concept) on the story engine (build/story.py),
narrator HEART (Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
2% a month: is that 24% a year? The effective annual rate (interest on interest).

A worked illustration with round numbers of our own; no card, lender, product or statistic is claimed, and no
forecast. Assumptions, said or on screen: $100 owed, 2% interest a month added to the balance each month, nothing
paid back for a year, no fees.

Every number, worked:
    Month 1:        2% of $100 = $2.00, balance $102.00.
    Month 2:        2% of $102 = $2.04, balance $104.04 (the extra $0.04 is interest on month 1's interest).
    Each month:     interest 2 x 1.02^(m-1): 2.00, 2.04, 2.08, 2.12, 2.16, 2.21, 2.25, 2.30, 2.34, 2.39, 2.44, 2.49
                    (month 12: 2.487, "almost $2.50"); the twelve sum to $26.82.
    After a year:   100 x 1.02^12 = 100 x 1.268242 = $126.82; 26.8% a year.
    Simple:         12 x 2% = 24%, $124; gap $2.82.
    Rule:           effective annual rate = (1 + monthly rate)^12 - 1 = 1.268 - 1 = 26.8%.
    Close (asked):  1% a month: 1.01^12 = 1.1268, 12.7% a year, so more than 12.5% (not given).
    Comment bonus:  1% a month for two years on $100: 1.01^24 = 1.2697, about $126.97.

Hook (24 Nov standard: five candidates, scored 1 to 5 on clash / number in the first three words / second person /
length on screen / would someone send it to a friend preparing for interviews):
    1. "2% a month. That's 24% a year, right?"                          clash 4, number 5, you 2, 8 words 5, send 5 = 21
    2. "Your card charges 2% a month. Is that 24% a year?"              clash 3, number 3, you 5, 10 words 5, send 4 = 20
    3. "It's not 24%. 2% a month costs you 26.8%."                      clash 4, number 5, you 3, 9 words 5, send 3 = 20
       (gives the answer away)
    4. "12 x 2% = 24%. So why do you owe $126.82?"                       clash 5, number 5, you 4, 11 words 5, send 3 = 22
       (needs the set-up before it makes sense; the $126.82 reads as noise in the first second)
    5. "Answer before the year ends: what does 2% a month cost?"       clash 2, number 2, you 2, 11 words 5, send 3 = 14
    Chosen: 1 (the trap answer said as a fact and questioned; on screen from frame 0: 12 months of 2% lighting in
    turn beside a 24%? column and a REAL ? column).

25 Nov, from the performance data (docs/daily/quality-log.md row of 25 Nov): the rates and bonds family (bonds 1,209,
the zero coupon on 24 Nov) and the "Nope / not quite" myth-style opening; Format C.

    python3 build/reels_monthly-rate.py HEART
"""

import sys

from motion import A
from sketch import picture, _ptag
from story import make, RED

GOLD = "#F2C35B"
PIC = dict(w=752, h=640)


def chip(label, fill, w=190, color="#fff"):
    return (f'<svg width="{w}" height="{w * .6:.0f}" viewBox="0 0 {w} {w * .6:.0f}" style="overflow:visible">'
            + _ptag(w / 2, w * .3, w * .95, label, fill, color, round(w * .23)) + "</svg>")


def floaters(total):
    """Faint tags drifting at the edges, clear of the text (never the answer)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "2%", "#3B3F48", 150), (770, 560, "x12", "#0F766E", 150),
                                              (-100, 1030, "M1", "#3B3F48", 140), (770, 1120, "%", GOLD, 130)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-monthly-rate",
    kicker="IB CONCEPT",
    mood="curious",
    cover=dict(at=("e", 0, 1, .3), lines=["2% a month.", "That's 24% a year,", "right?"],
               hl={"2%": RED, "24%": GOLD, "right?": RED}, avoid=["26.8%", "126.82"]),
    beats=[
        dict(tag="THE TRAP", size=64, hold=.6, hl=["2%", "24%", "right?"],
             say=[("Two percent a month.", "2% a month."),
                  ("That's twenty four percent a year, right?", "That's 24% a year, right?")],
             art=lambda t0, d, seg: picture("ap_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "thump", .07), (("s", 0, .3), "tick", .04), (("s", 0, .6), "tick", .04), (("s", 0, .9), "tick", .04),
                  (("s", 1, .1), "pop", .05), (("s", 1, .6), "tick", .04)]),
        dict(tag="THE SET-UP", size=56, hl=["$100", "2%", "cent"],
             say=[("Say you owe a hundred dollars on a card, at two percent a month.", "Say you owe $100 on a card, at 2% a month."),
                  ("And you don't pay a cent back for twelve months.", "And you don't pay a cent back for 12 months.")],
             art=lambda t0, d, seg: picture("ap_setup", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "pop", .05), (("s", 0, .75), "pop", .05), (("s", 1, .1), "paper", .05), (("s", 1, .5), "paper", .05),
                  (("s", 1, .95), "thump", .07)]),
        dict(tag="MONTH BY MONTH", size=54, hl=["$2,", "$102.", "$102."],
             say=[("Month one adds two dollars, so you owe a hundred and two.", "Month 1 adds $2, so you owe $102."),
                  ("Month two charges two percent on the hundred and two.", "Month 2 charges 2% on the $102.")],
             art=lambda t0, d, seg: picture("ap_month", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "thump", .05), (("s", 0, .4), "clink", .04), (("s", 1, .1), "knock", .05), (("s", 1, .5), "thump", .05),
                  (("s", 1, .8), "pop", .05)]),
        dict(tag="IT SNOWBALLS", size=56, hl=["bigger", "$2.50."],
             say=[("So every month's interest is a little bigger than the last.", "So every month's interest is a little bigger than the last."),
                  ("By month twelve, it's almost two fifty.", "By month 12, it's almost $2.50.")],
             art=lambda t0, d, seg: picture("ap_snowball", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "tick", .04), (("s", 0, .35), "tick", .04), (("s", 0, .6), "tick", .04), (("s", 0, .85), "tick", .04),
                  (("s", 1, .2), "pop", .05)]),
        dict(tag="THE ANSWER", size=54, hl=["$126.82.", "26.8%,", "24%."],
             say=[("After a year, you owe a hundred and twenty six dollars and eighty two cents.", "After a year, you owe $126.82."),
                  ("That's twenty six point eight percent, not twenty four.", "That's 26.8%, not 24%.")],
             art=lambda t0, d, seg: picture("ap_answer", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "tick", .04), (("s", 0, .5), "tick", .04), (("s", 0, .85), "pop", .05), (("s", 1, .15), "thump", .07),
                  (("s", 1, .7), "knock", .05)]),
        dict(tag="THE RULE", size=52, hl=["interest", "12", "effective", "rate."],
             say=[("Interest on interest is why the yearly cost beats twelve times the monthly rate.",
                   "Interest on interest is why the yearly cost beats 12 times the monthly rate."),
                  ("That's the effective annual rate.", "That's the effective annual rate.")],
             art=lambda t0, d, seg: picture("ap_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "tick", .04), (("s", 0, .4), "tick", .04), (("s", 0, .7), "tick", .04), (("s", 0, .95), "pop", .05),
                  (("s", 1, .5), "thump", .07)]),
    ],
    close=dict(say=[("Now it's one percent a month.", "Now it's 1% a month."),
                    ("Is that more or less than twelve and a half percent a year?", "More or less than 12.5% a year?"),
                    ("Answer in the comments, and follow for tomorrow's.", "Answer in the comments, and follow for tomorrow's.")],
               cols={"comments,": RED, "follow": RED}, bar=True, art_w=720, art_h=576,
               pic=lambda t0, d: picture("ap_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
