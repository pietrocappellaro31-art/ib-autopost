"""
Levels #1: four interview questions, each one harder. The hook asks the last
level first ("Can enterprise value be negative?") and the Reel closes the loop.

Every answer, worked:
    L1  Income statement, balance sheet, cash flow statement.
    L2  Depreciation +10 at a 25% tax rate: profit before tax -10, tax -2.5,
        net income -10 x (1 - 25%) = -7.5.
    L3  Borrow 100, hold it as cash: EV = equity + debt - cash;
        debt +100, cash +100, equity unchanged, so EV unchanged.
    L4  EV = equity + debt - cash, so EV < 0 when cash > equity + debt.

    KOKORO_DIR=/path/to/kokoro python build/reels_levels1.py [voice]
"""

import sys

from levels import make, RED, TEAL

EP = dict(
    slug="w2-levels-1",
    kicker="IB INTERVIEW LEVELS",
    hook=dict(
        say=[("Can enterprise value be negative?", "Can enterprise value be negative?"),
             ("That's level four.", "That's level 4."),
             ("Let's see if you make it.", "Let's see if you make it.")],
        sub="4 interview questions. Each one harder.",
        hl=["negative?"],
        cols={"4.": RED, "make": RED, "it.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0,
             q=[("Name the three financial statements.", "Name the three financial statements.")],
             hl=["three"],
             a=[("Income statement, balance sheet, cash flow statement.",
                 "Income statement, | Balance sheet, | Cash flow statement.", "big")],
             bigsize=74),
        dict(tail="medium.", think=1.3,
             q=[("Depreciation goes up ten, at a twenty five percent tax rate.", "Depreciation goes up $10, at a 25% tax rate."),
                ("What happens to net income?", "What happens to net income?")],
             hl=["net income?"],
             a=[("Down seven and a half.", "Down $7.5"),
                ("That's ten, minus the tax you save.", "That's $10, minus the tax you save.")],
             chip="10 &times; (1 &minus; 25%) = 7.5", chip_at=1),
        dict(tail="tricky.", think=1.5,
             q=[("A company borrows a hundred and holds it as cash.", "A company borrows $100 and holds it as cash."),
                ("What happens to enterprise value?", "What happens to enterprise value?")],
             hl=["enterprise value?"],
             a=[("Nothing.", "Nothing."), ("Debt and cash both go up a hundred.", "Debt and cash both go up $100."),
                ("They cancel out.", "They cancel out.")],
             chip="EV = equity + debt &minus; cash", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0,
             q=[("Can enterprise value be negative?", "Can enterprise value be negative?")],
             hl=["negative?"],
             a=[("Yes.", "Yes."), ("Remember level three.", "Remember level 3."),
                ("When cash is more than equity plus debt, it goes below zero.",
                 "When cash is more than equity plus debt, it goes below zero.")],
             acols={"3.": RED, "zero.": TEAL}, chip="EV = equity + debt &minus; cash", chip_at=1),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Comment it below.", "Comment it below."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comment": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
