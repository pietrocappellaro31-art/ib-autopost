"""
Levels #8: four interview questions on unlevered free cash flow, each one
harder. The hook asks the last level first; level 2 builds the formula that
level 4 turns over.

Unlevered free cash flow (UFCF) = EBIT x (1 - tax rate) + D&A - capex
- increase in net working capital. Standard definition used in a DCF.

Every answer, worked:
    L1  UFCF is before interest: it is the cash available to everyone who
        funds the company, lenders and shareholders, so it is discounted at
        WACC. (Levered FCF is after interest, for shareholders only.)
    L2  EBIT 100, tax rate 25%, D&A 20, capex 30, working capital flat:
        100 x (1 - 25%) = 75; 75 + 20 - 30 - 0 = 65.
    L3  Same company, net working capital rises by 10 (cash tied up in
        stock or in customers who have not paid yet): 65 - 10 = 55.
        Free cash flow falls by 10.
    L4  Depreciation up 10 on level 2, everything else the same (capex
        unchanged, depreciation deductible for tax):
        EBIT 90, after tax 90 x 75% = 67.5; 67.5 + 30 - 30 = 67.5.
        67.5 - 65 = +2.5. Yes: depreciation is not cash, but it cuts tax by
        10 x 25% = 2.5 (the tax shield), so UFCF rises by 2.5.
    Bonus (comment): level 2 again with a 30% tax rate:
        100 x 70% = 70; 70 + 20 - 30 = 60.

    python build/reels_levels8.py EMMA
"""

import sys

from levels import make, RED, TEAL

EP = dict(
    slug="w2-levels-8",
    kicker="IB INTERVIEW LEVELS #8",
    hook=dict(
        say=[("Can more depreciation raise free cash flow?",
              "Can more depreciation raise free cash flow?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="4 interview questions. Each one harder.",
        qsize=70,
        hl=["free cash flow?"],
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0,
             q=[("Is unlevered free cash flow before or after interest?",
                 "Is unlevered free cash flow before or after interest?")],
             hl=["interest?"],
             a=[("Before interest is paid.", "Before interest is paid.", "big"),
                ("It's cash for lenders and shareholders.",
                 "It's cash for lenders and shareholders.")],
             bigsize=92),
        dict(tail="medium.", think=1.4,
             q=[("EBIT is a hundred, taxed at twenty five percent.",
                 "EBIT is 100, taxed at 25%."),
                ("Depreciation twenty, capex thirty, working capital flat.",
                 "Depreciation 20, capex 30, working capital flat."),
                ("What's unlevered free cash flow?", "What's unlevered free cash flow?")],
             hl=["free cash flow?"], qsize=54,
             a=[("Sixty five.", "65"),
                ("Seventy five after tax, plus twenty, minus thirty.",
                 "75 after tax, plus 20, minus 30.")],
             chip="100 &times; 75% + 20 &minus; 30 = 65", chip_at=1),
        dict(tail="tricky.", think=1.6,
             q=[("Now working capital rises by ten.",
                 "Now working capital rises by 10."),
                ("What happens to free cash flow?", "What happens to free cash flow?")],
             hl=["free cash flow?"], qsize=58,
             a=[("It falls by ten.", "It falls by 10."),
                ("That cash is stuck in inventory and unpaid bills.",
                 "That cash is stuck in inventory and unpaid bills.")],
             bigsize=96, chip="65 &minus; 10 = 55", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0,
             q=[("Can more depreciation raise free cash flow?",
                 "Can more depreciation raise free cash flow?")],
             hl=["free cash flow?"],
             a=[("Yes.", "Yes."),
                ("Depreciation isn't cash, but it's deductible.",
                 "Depreciation isn't cash, but it's deductible."),
                ("Ten more in level two cuts tax by two and a half.",
                 "10 more in level 2 cuts tax by 2.5.")],
             bigsize=110, chip="10 &times; 25% = 2.5 more cash", chip_at=1),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comments.": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
