"""
Levels #11: four interview questions on shareholders' equity, each one harder.
The hook asks the last level first; level 3 (a buyback takes equity down) is
the move level 4 needs, and the voice says so.

Shareholders' equity (book value) = total assets - total liabilities: what is
left for the owners after everything the company owes.

Every answer, worked (textbook accounting, round example numbers, no
statistic or company claimed):
    L1  Equity = assets - liabilities. Example on the drawing: assets $100,
        liabilities $80, equity $100 - $80 = $20.
    L2  A $10 dividend paid in cash: cash (an asset) -10, retained earnings
        (part of equity) -10. Equity falls by $10. Balance sheet still
        balances: assets -10 = liabilities 0 + equity -10. Net income is
        unchanged (a dividend is not an expense).
    L3  The company buys back $50 of its own shares for cash: cash -50
        (assets fall), and equity falls 50 (the shares are cancelled or held
        as treasury stock, which is deducted from equity). Both fall:
        assets -50 = equity -50.
    L4  Yes, equity can be negative. Start: assets 100, liabilities 80,
        equity 20. Borrow 50: cash +50, debt +50 -> assets 150, liabilities
        130, equity 20. Buy back 50 of shares with that cash (like level 3):
        cash -50, equity -50 -> assets 100, liabilities 130,
        equity 100 - 130 = -30. Check: 100 = 130 + (-30).
        (Years of losses can also push equity below zero, so the reason
        matters; the Reel shows the buyback route because level 3 set it up.)
    Bonus (comment): equity is $20 and the company makes a $30 loss this
        year (no dividends, no new shares). Equity = 20 - 30 = -$10.

    python3 build/reels_negative-equity.py EMMA
"""

import sys

from levels import make, RED, TEAL
from sketch import picture

ART_W, ART_H = 700, 532

EP = dict(
    slug="w2-levels-11",
    kicker="IB INTERVIEW LEVELS #11",
    hook=dict(
        say=[("Can shareholders' equity be negative?", "Can shareholders' equity be negative?")],
        sub="4 interview questions. Each one harder.",
        qsize=74,
        hl=["be negative?"],
    ),
    levels=[
        dict(tail="easy.", think=1.0, ans_min=ART_H,
             art=lambda t0, d: picture("bs_bars", t0, d, w=ART_W, h=ART_H),
             q=[("What's shareholders' equity?", "What's shareholders' equity?")],
             hl=["equity?"],
             a=[("Assets, minus liabilities.", "Assets minus liabilities.", "big"),
                ("What's left for the owners, after everything owed.", "What's left for the owners, after everything owed.")],
             bigsize=96, chip="$100 &minus; $80 = $20", chip_at=1),
        dict(tail="medium.", think=1.3, ans_min=ART_H,
             art=lambda t0, d: picture("dividend", t0, d, w=ART_W, h=ART_H),
             q=[("A company pays a ten dollar dividend, in cash.", "A company pays a $10 dividend, in cash."),
                ("What happens to equity?", "What happens to equity?")],
             hl=["to equity?"], qsize=58,
             a=[("Down ten.", "Down $10."),
                ("Cash goes out, and so do retained earnings.", "Cash goes out, and so do retained earnings.")],
             bigsize=140, chip="Cash &minus;$10 = equity &minus;$10", chip_at=1),
        dict(tail="tricky.", think=1.6, ans_min=500,
             art=lambda t0, d: picture("buyback", t0, d, w=ART_W, h=500),
             q=[("It buys back fifty dollars of its own shares, with cash.", "It buys back $50 of its own shares, with cash."),
                ("Do assets fall, or equity?", "Do assets fall, or equity?")],
             hl=["or equity?"], qsize=54,
             a=[("Both.", "Both."),
                ("Cash falls fifty, and equity falls fifty.", "Cash falls $50, and equity falls $50.")],
             bigsize=150, chip="Assets &minus;$50 = equity &minus;$50", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0, ans_min=500,
             art=lambda t0, d: picture("bs_bars", t0, d, w=ART_W, h=500, assets=100, liab=130, scale=2.6, base=430),
             q=[("Can shareholders' equity be negative?", "Can shareholders' equity be negative?")],
             hl=["be negative?"], qsize=56,
             a=[("Yes.", "Yes."),
                ("Like level three, borrow fifty, and buy back fifty.", "Like level 3, borrow $50 and buy back $50."),
                ("Equity goes from twenty, to minus thirty.", "Equity goes from $20 to minus $30.")],
             bigsize=130, chip="$100 = $130 + (&minus;$30)", chip_at=2),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comments.": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
