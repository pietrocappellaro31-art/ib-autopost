"""
Levels #9: four interview questions on WACC, each one harder. The hook asks
the last level first; level 1 (why debt is cheaper) and level 4 (does more
debt always help) are the two halves of the same idea.

WACC = E/V x cost of equity + D/V x cost of debt x (1 - tax rate), the
standard weighted average cost of capital used to discount unlevered free
cash flow in a DCF.

Every answer, worked:
    L1  Debt is cheaper than equity for two reasons: lenders are paid
        before shareholders (interest and principal come first, and rank
        ahead in a bankruptcy), so they take less risk and ask for less;
        and interest is tax deductible, so the after-tax cost is lower
        still. Textbook, no number claimed.
    L2  Pre-tax cost of debt 8%, tax rate 25%:
        8% x (1 - 25%) = 8% x 75% = 6%.
    L3  60% equity at a 10% cost of equity, 40% debt at the 6% after-tax
        cost from level 2:
        60% x 10% = 6.0%; 40% x 6% = 2.4%; 6.0% + 2.4% = 8.4%.
    L4  No. Adding debt swaps expensive equity for cheaper debt, but it
        also makes the remaining equity riskier, so the cost of equity
        rises; past a point the risk of financial distress pushes the
        cost of debt up as well, and WACC rises again (the trade-off view
        taught in corporate finance: WACC falls, then rises, as debt
        grows). No optimal ratio or number is claimed.
    Bonus (comment): level 3 with a 50 / 50 mix, both costs held the same:
        50% x 10% + 50% x 6% = 5% + 3% = 8%.

Spoken text spells WACC as "whack", the way bankers say it: Pocket TTS (G2)
read the letters ("way C C") on the first render.

    python3 build/reels_wacc-more-debt.py G2
"""

import sys

from levels import make, RED, TEAL
from sketch import picture

ART = 600     # drawing width in the answer zone (the paper ground stays: Reels keep the brand ground)

EP = dict(
    slug="w2-levels-9",
    kicker="IB INTERVIEW LEVELS #9",
    hook=dict(
        say=[("Does more debt always lower whack?", "Does more debt always lower WACC?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="4 interview questions. Each one harder.",
        qsize=76,
        hl=["lower WACC?"],
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0, ans_min=480,
             art=lambda t0, d: picture("capital_stack", t0, d, w=ART),
             q=[("Why is debt cheaper than equity?", "Why is debt cheaper than equity?")],
             hl=["cheaper"],
             a=[("Lenders get paid first.", "Lenders get paid first.", "big"),
                ("And interest is tax deductible.", "And interest is tax deductible.")],
             bigsize=92),
        dict(tail="medium.", think=1.4, ans_min=480,
             art=lambda t0, d: picture("tax_cut", t0, d, w=ART),
             q=[("Debt costs eight percent before tax.", "Debt costs 8% before tax."),
                ("The tax rate is twenty five percent.", "The tax rate is 25%."),
                ("What's the after tax cost of debt?", "What's the after-tax cost of debt?")],
             hl=["after-tax cost"], qsize=56,
             a=[("Six percent.", "6%"),
                ("Eight percent, times seventy five percent.", "8%, times 75%.")],
             bigsize=150, chip="8% &times; (1 &minus; 25%) = 6%", chip_at=1),
        dict(tail="tricky.", think=1.6, ans_min=480,
             art=lambda t0, d: picture("mix_bar", t0, d, w=ART),
             q=[("Sixty percent equity, costing ten percent.", "60% equity, costing 10%."),
                ("Forty percent debt, at that six percent.", "40% debt, at that 6%."),
                ("What's whack?", "What's WACC?")],
             hl=["WACC?"], qsize=56,
             a=[("Eight point four percent.", "8.4%"),
                ("Six from equity, plus two point four from debt.", "6 from equity, plus 2.4 from debt.")],
             bigsize=150, chip="60% &times; 10% + 40% &times; 6% = 8.4%", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0, ans_min=480,
             art=lambda t0, d: picture("wacc_curve", t0, d, w=ART),
             q=[("Does more debt always lower whack?", "Does more debt always lower WACC?")],
             hl=["lower WACC?"],
             a=[("No.", "No."),
                ("More debt makes the equity riskier, so it costs more.",
                 "More debt makes the equity riskier, so it costs more."),
                ("Past a point, debt costs more too, and whack rises.",
                 "Past a point, debt costs more too, and WACC rises.")],
             bigsize=130, chip="WACC falls, then rises", chip_at=2),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comments.": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
