"""
Levels #6: four interview questions on the balance sheet, each one harder.
The hook asks the last level first; level 3 sets up what level 4 turns over.

Every answer, worked:
    L1  Assets = liabilities + equity.
    L2  Buying inventory for 50 in cash: cash -50, inventory +50, total
        assets unchanged.
    L3  Goodwill = purchase price - fair value of the target's identifiable
        net assets = 500 - 300 = 200.
    L4  Negative goodwill is not carried on the balance sheet: when the price
        is below the fair value of the net assets, the buyer books the
        difference as a gain straight away, a bargain purchase (US GAAP
        ASC 805 and IFRS 3, after reassessing the values).

    python build/reels_levels6.py G2
"""

import sys

from levels import make, RED, TEAL

EP = dict(
    slug="w2-levels-6",
    kicker="IB INTERVIEW LEVELS #6",
    hook=dict(
        say=[("Can goodwill ever be negative?", "Can goodwill ever be negative?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="4 interview questions. Each one harder.",
        hl=["negative?"],
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0,
             q=[("What's the basic accounting equation?", "What's the basic accounting equation?")],
             hl=["accounting equation?"],
             a=[("Assets equal liabilities plus equity.", "Assets = liabilities + equity", "big")],
             bigsize=74),
        dict(tail="medium.", think=1.3,
             q=[("A company buys inventory for fifty in cash.", "A company buys inventory for $50 in cash."),
                ("What happens to total assets?", "What happens to total assets?")],
             hl=["total assets?"],
             a=[("Nothing.", "Nothing."), ("Cash goes down fifty, inventory goes up fifty.", "Cash goes down $50, inventory goes up $50.")],
             chip="Cash &minus;$50 &middot; Inventory +$50", chip_at=1),
        dict(tail="tricky.", think=1.5,
             q=[("A company buys another for five hundred.", "A company buys another for $500."),
                ("Its net assets are worth three hundred at fair value.", "Its net assets are worth $300 at fair value."),
                ("What's the goodwill?", "What's the goodwill?")],
             hl=["goodwill?"], qsize=56,
             a=[("Two hundred.", "$200"), ("It's the price paid above the fair value of what you buy.",
                                             "It's the price paid above the fair value of what you buy.")],
             chip="500 &minus; 300 = 200", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0,
             q=[("Can goodwill ever be negative?", "Can goodwill ever be negative?")],
             hl=["negative?"],
             a=[("Not on the balance sheet.", "Not on the balance sheet."),
                ("If you pay less than the net assets are worth, you book the difference as a gain straight away.",
                 "If you pay less than the net assets are worth, you book the difference as a gain straight away."),
                ("It's called a bargain purchase.", "It's called a bargain purchase.")],
             bigsize=88, chip="Price &lt; fair value &rarr; gain, not negative goodwill", chip_at=1),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comments.": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
