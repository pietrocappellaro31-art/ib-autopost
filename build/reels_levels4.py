"""
Levels #4: four interview questions on LBOs and returns, each one harder.
The hook asks the last level first.

Every answer, worked:
    L1  LBOs are funded mostly with debt: less equity in, so any gain in the
        business is a bigger percentage gain on the equity (and so is a loss).
    L2  The three return drivers: grow the profits (EBITDA), sell at a higher
        multiple than you paid, pay down the debt.
    L3  MOIC = money out / money in = 200 / 100 = 2.0x.
    L4  Doubling in 3 years: 2 ** (1/3) - 1 = 0.2599, about 26% a year, so
        above 25%. (Check: 1.25 ** 3 = 1.95, just short of 2x.)

    python build/reels_levels4.py clone:L4
"""

import sys

from levels import make, RED, TEAL

EP = dict(
    slug="w2-levels-4",
    kicker="IB INTERVIEW LEVELS #4",
    hook=dict(
        say=[("You double your money in three years, is your IRR above or below twenty five percent?",
              "You double your money in 3 years. Is your IRR above or below 25%?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="4 interview questions. Each one harder.",
        hl=["25%?"],
        cols={"4.": RED, "score.": RED},
        qsize=74,
    ),
    levels=[
        dict(tail="easy.", think=1.0,
             q=[("In an LBO, does the buyer use mostly debt or mostly equity?",
                 "In an LBO, does the buyer use mostly debt or mostly equity?")],
             hl=["LBO,"],
             a=[("Mostly debt.", "Mostly debt."),
                ("Borrowed money makes the equity return bigger, if things go well.",
                 "Borrowed money makes the equity return bigger, if things go well.")],
             chip="Less equity in &rarr; bigger % return (and risk)", chip_at=1),
        dict(tail="medium.", think=1.3,
             q=[("Name one way a private equity firm makes money on a deal.",
                 "Name one way a private equity firm makes money on a deal.")],
             hl=["makes money"],
             a=[("Three ways.", "Three ways."),
                ("Grow the profits, sell at a higher multiple, or pay down the debt.",
                 "Grow the profits, sell at a higher multiple, or pay down the debt.")],
             chip="EBITDA growth &middot; multiple expansion &middot; debt paydown", chip_at=1),
        dict(tail="tricky.", think=1.5,
             q=[("You put in a hundred and take out two hundred after five years.",
                 "You put in $100 and take out $200 after 5 years."),
                ("What's the multiple on invested capital?", "What's the MOIC?")],
             hl=["MOIC?"],
             a=[("Two times.", "2.0&times;"), ("Money out, divided by money in.", "Money out, divided by money in.")],
             chip="200 &divide; 100 = 2.0&times;", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0,
             q=[("", "You double your money in 3 years."), ("Above or below twenty five percent?", "IRR above or below 25%?")],
             hl=["25%?"], qsize=58,
             a=[("Above.", "Above."),
                ("Doubling in three years is about twenty six percent a year.",
                 "Doubling in three years is about 26% a year.")],
             chip="2<sup>1/3</sup> &minus; 1 = 26%", chip_at=1),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Comment it below.", "Comment it below."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comment": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
