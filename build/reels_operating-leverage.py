"""
Reel B, 17 Nov 2026: Format C (one surprising concept) on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram. Operating leverage: sales up 10%, profit up
60%. How? Because half of this company's costs are fixed.

A worked illustration with round numbers of our own; no company, industry average or "typical" cost split is
claimed. The cost that moves with sales is called "materials" as an everyday example of a variable cost; rent and
salaries as examples of fixed costs (over the short run this example covers).

Every number, worked:
    Base:       sales 100; costs that move with sales 40 (40% of sales); fixed costs 50; profit 100 - 40 - 50 = 10.
    Sales +10%: sales 110; moving costs 40% x 110 = 44 (+4); fixed 50; profit 110 - 44 - 50 = 16.
                Profit change (16 - 10) / 10 = +60%.
    Sales -10%: sales 90; moving costs 40% x 90 = 36; fixed 50; profit 90 - 36 - 50 = 4. Change (4 - 10) / 10 = -60%.
    Why six times: each extra $1 of sales keeps 60 cents (1 - 40%) after the moving costs; 10% of sales is $10, so
                profit moves $6 on a $10 base: 60%. The bigger the fixed costs, the thinner the profit base, the bigger
                the % swing (the degree of operating leverage here = contribution 60 / profit 10 = 6).
    Close (asked, not answered in the Reel): sales -20% gives 80 - 32 - 50 = -2, a $2 loss.
    Comment bonus: break-even sales = fixed 50 / 60% = $83.33 (83.33 - 33.33 - 50 = 0).

17 Nov, from the performance data (docs/daily/performance.md, 12 Reels): 4 of the 5 Reels with 1,000+ reach opened on
concrete numbers; all 6 at 125 to 139 reach opened on an abstract yes/no question. So the hook is two numbers: "Sales
up 10%. Profit up 60%." Every Reel so far was the Levels quiz (format A) bar one 12 s loop; B varies the format.

17 Nov, the 16 Nov Short's next improvement (beats opened on empty panels): every beat's set is on its panel at the
swipe (the four labelled columns, the fixed column with its padlock), only the action animates; and the 16 Nov Reel's:
the pictures keep moving after their last cue (the lever keeps rocking, the padlock rattles, the tiles breathe).

    python3 build/reels_operating-leverage.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "+10%", GOLD, 180), (770, 560, "+60%", "#0F766E", 190),
                                              (-100, 1030, "PROFIT", "#0F766E", 200), (770, 1120, "SALES", GOLD, 190)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-operating-leverage",
    kicker="ONE IB CONCEPT",
    mood="curious",
    cover=dict(at=("e", 0, 2, .3), lines=["Sales up 10%.", "Profit up 60%.", "How?"],
               hl={"10%.": GOLD, "60%.": TEAL_INK, "How?": RED}, avoid=["FIXED", "OPERATING LEVERAGE", "$50"]),
    beats=[
        dict(tag="SALES +10%", size=70, hold=.6, hl=["10%.", "60%."],
             say=[("Sales up ten percent.", "Sales up 10%."),
                  ("Profit up sixty percent.", "Profit up 60%."),
                  ("How is that possible?", "How is that possible?")],
             art=lambda t0, d, seg: picture("oplev_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .35), "tick", .05), (("s", 0, 1.0), "clink", .07), (("s", 1, .35), "tick", .05),
                  (("s", 1, 1.0), "thump", .12), (("s", 2, .1), "pop", .06)]),
        dict(tag="WHERE $100 GOES", size=48, hl=["$40", "fixed:", "$10"],
             say=[("Say a company sells a hundred dollars.", "Say a company sells $100."),
                  ("Forty goes on costs that grow with sales, like materials.", "$40 goes on costs that grow with sales, like materials."),
                  ("Fifty is fixed: rent and salaries.", "$50 is fixed: rent and salaries."),
                  ("That leaves ten dollars of profit.", "That leaves $10 of profit.")],
             art=lambda t0, d, seg: picture("cost_split", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .9), "knock", .08), (("s", 1, .85), "knock", .08), (("s", 1, 1.05), "clink", .05),
                  (("s", 2, .85), "knock", .08), (("s", 2, 1.05), "clink", .06), (("s", 3, .85), "clink", .07)]),
        dict(tag="SALES +10%", size=48, hl=["$110.", "don't move.", "60%."],
             say=[("Now sales rise ten percent, to a hundred and ten dollars.", "Now sales rise 10%, to $110."),
                  ("Materials rise with them, to forty four.", "Materials rise with them, to $44."),
                  ("Rent and salaries don't move.", "Rent and salaries don't move."),
                  ("So profit is sixteen dollars, up sixty percent.", "So profit is $16, up 60%.")],
             art=lambda t0, d, seg: picture("cost_grow", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .5), "tick", .04), (("s", 1, .5), "tick", .04), (("s", 2, .6), "thump", .1),
                  (("s", 3, .4), "tick", .04)] + [(("e", 3, -.05), "ding", .07)]),
        dict(tag="IT CUTS BOTH WAYS", size=54, hl=["falls 60%,"],
             say=[("It works in reverse too.", "It works in reverse too."),
                  ("Sales down ten percent, and profit falls sixty percent, to four dollars.",
                   "Sales down 10%, and profit falls 60%, to $4.")],
             art=lambda t0, d, seg: picture("cost_shrink", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "paper", .06), (("s", 1, .6), "tick", .04), (("s", 1, 2.3), "thump", .12)]),
        dict(tag="THE NAME", size=58, hl=["operating leverage.", "bigger the swing"],
             say=[("That's called operating leverage.", "That's called operating leverage."),
                  ("The more of your costs are fixed, the bigger the swing in profit.",
                   "The more of your costs are fixed, the bigger the swing in profit.")],
             art=lambda t0, d, seg: picture("lever_fixed", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "pop", .06), (("s", 1, 1.0), "knock", .08)]),
    ],
    close=dict(say=[("Now sales fall twenty percent.", "Now sales fall 20%."),
                    ("What's the profit?", "What's the profit?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED},
               pic=lambda t0, d: picture("oplev_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
