"""
Levels #3: four interview questions on cash, each one harder. Written to be
read by Pietro himself (Part B of the 6 Nov recording scripts) and built on
his real voice, or on the clone.

Every answer, worked:
    L1  Cash goes back to shareholders as dividends or share buybacks.
    L2  Buying a machine for 100 cash: cash -100, PP&E +100, no expense today;
        it reaches the income statement as depreciation over its life.
    L3  Accounts receivable +20: revenue booked, cash not collected, so cash
        from operations is 20 lower than net income would suggest.
    L4  Profit is not cash: late-paying customers, bills due first, stock and
        investment can drain cash while the income statement shows a profit.

    python build/reels_levels3.py real:/path/to/memo.m4a     (or clone:/path/to/reference.wav)
"""

import sys

from levels import make, RED, TEAL

EP = dict(
    slug="w2-levels-3",
    kicker="IB INTERVIEW LEVELS #3",
    hook=dict(
        say=[("Can a profitable company go bankrupt?", "Can a profitable company go bankrupt?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="4 interview questions. Each one harder.",
        hl=["bankrupt?"],
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0,
             q=[("Name one way a company can return cash to its shareholders.",
                 "Name one way a company can return cash to its shareholders.")],
             hl=["return cash"],
             a=[("Dividends.", "Dividends."), ("Or buying back its own shares.", "Or buying back its own shares.")]),
        dict(tail="medium.", think=1.3,
             q=[("A company buys a machine for a hundred in cash.", "A company buys a machine for $100 in cash."),
                ("What happens to net income today?", "What happens to net income today?")],
             hl=["net income today?"],
             a=[("Nothing.", "Nothing."), ("It's not an expense yet.", "It's not an expense yet."),
                ("It hits the income statement as depreciation, year by year.",
                 "It hits the income statement as depreciation, year by year.")],
             chip="Cash &minus;$100 &middot; PP&amp;E +$100", chip_at=1, qsize=58),
        dict(tail="tricky.", think=1.5,
             q=[("Accounts receivable goes up by twenty.", "Accounts receivable goes up by $20."),
                ("What happens to cash from operations?", "What happens to cash from operations?")],
             hl=["cash from operations?"],
             a=[("It falls by twenty.", "&minus;$20"),
                ("You booked the sale, but the customer hasn't paid you yet.",
                 "You booked the sale, but the customer hasn't paid you yet.")],
             chip="Receivables +$20 &rarr; cash from operations &minus;$20", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0,
             q=[("Can a profitable company go bankrupt?", "Can a profitable company go bankrupt?")],
             hl=["bankrupt?"],
             a=[("Yes.", "Yes."), ("Profit isn't cash.", "Profit isn't cash."),
                ("If the customers pay late and the bills come first, the cash runs out before the profit arrives.",
                 "If the customers pay late and the bills come first, the cash runs out before the profit arrives.")],
             chip="Profit &ne; cash", chip_at=1),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Comment it below.", "Comment it below."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comment": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
