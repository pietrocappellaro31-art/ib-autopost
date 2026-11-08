"""
Levels #5: four interview questions on discounting, each one harder. The
hook asks the last level first; level 3 sets up the formula level 4 needs.

Every answer, worked:
    L1  Equity usually costs more than debt: shareholders are paid last, so
        they need a higher expected return (and interest is tax deductible).
    L2  A higher discount rate (WACC) means every future cash flow is divided
        by a bigger number, so the DCF value falls.
    L3  Perpetuity of 100 a year from next year at 10%: 100 / 0.10 = 1,000.
    L4  Growing perpetuity, 100 next year, growing 2% a year, at 10%:
        100 / (0.10 - 0.02) = 100 / 0.08 = 1,250.

    python build/reels_levels5.py clone:L4
"""

import sys

from levels import make, RED, TEAL

EP = dict(
    slug="w2-levels-5",
    kicker="IB INTERVIEW LEVELS #5",
    hook=dict(
        say=[("A hundred a year, growing two percent forever, at a ten percent discount rate, what's it worth today?",
              "$100 a year, growing 2% forever, at a 10% discount rate. What's it worth today?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="4 interview questions. Each one harder.",
        hl=["worth today?"],
        cols={"4.": RED, "score.": RED},
        qsize=64,
    ),
    levels=[
        dict(tail="easy.", think=1.0,
             q=[("Which usually costs a company more, debt or equity?",
                 "Which usually costs a company more: debt or equity?")],
             hl=["costs"],
             a=[("Equity.", "Equity."),
                ("Shareholders get paid after everyone else, so they want more.",
                 "Shareholders get paid after everyone else, so they want more.")],
             chip="Lenders get paid first, shareholders last", chip_at=1),
        dict(tail="medium.", think=1.3,
             q=[("The discount rate goes up.", "The discount rate goes up."),
                ("What happens to a DCF value?", "What happens to a DCF value?")],
             hl=["DCF value?"],
             a=[("It falls.", "It falls."),
                ("Future cash flows are worth less today.", "Future cash flows are worth less today.")],
             chip="Higher discount rate &rarr; lower value", chip_at=1),
        dict(tail="tricky.", think=1.5,
             q=[("A company pays you a hundred a year, forever, starting next year.",
                 "A company pays you $100 a year, forever, starting next year."),
                ("The discount rate is ten percent.", "The discount rate is 10%."),
                ("What's it worth today?", "What's it worth today?")],
             hl=["worth today?"], qsize=56,
             a=[("A thousand.", "$1,000"), ("Divide the cash flow by the rate.", "Divide the cash flow by the rate.")],
             chip="100 &divide; 10% = 1,000", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0,
             q=[("", "$100 a year, growing 2% forever, at a 10% discount rate."),
                ("What's it worth today?", "What's it worth today?")],
             hl=["worth today?"], qsize=56,
             a=[("Twelve hundred and fifty.", "$1,250"),
                ("Same as level three, but divide by the rate minus the growth.",
                 "Same as level 3, but divide by the rate minus the growth."),
                ("A hundred over eight percent.", "100 over 8%.")],
             acols={"3": RED}, chip="100 &divide; (10% &minus; 2%) = 1,250", chip_at=1),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comments.": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
