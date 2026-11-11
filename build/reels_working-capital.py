"""
Levels #10: four interview questions on working capital, each one harder.
The hook asks the last level first; level 3 (cash before revenue) is the
idea level 4 needs, and the voice says so.

Net working capital = current assets - current liabilities. In a DCF the
operating version leaves out cash and debt (they sit in net debt), and an
increase in working capital is a use of cash.

Every answer, worked (textbook accounting, round example numbers, no
statistic or company claimed):
    L1  Current assets minus current liabilities. In a model, cash and debt
        are left out of it (operating working capital), because they are
        counted in net debt.
    L2  Inventory up by $30, paid in cash: an increase in an operating asset
        is a use of cash. Cash from operations falls by $30
        (inventory +30, cash -30; no expense yet, so net income is unchanged).
    L3  A customer pays $40 up front for next year's service. Revenue is only
        recognised when the service is delivered, so revenue today is $0.
        Cash +40, deferred revenue (a current liability) +40; the balance
        sheet balances: assets +40 = liabilities +40.
    L4  Yes, negative working capital can be a good sign: it means current
        liabilities (money owed to suppliers, cash collected before the
        service, like level 3) exceed current assets, i.e. customers pay
        before suppliers are paid. As such a business grows, working capital
        gets more negative, and a fall in working capital is a source of
        cash: growth brings cash in instead of using it. (It can also signal
        trouble paying bills, so the reason matters; the Reel says "can be".)
    Bonus (comment): accounts payable up by $15. An increase in an operating
        liability is a source of cash: cash from operations rises by $15.

    python3 build/reels_working-capital.py BELLA
"""

import sys

from levels import make, RED, TEAL
from sketch import picture

# 12 Nov: the drawings come up to the Short's size (600 x 480 on Levels #9): the art box is 700 x 532 and the
# answer zone is as tall as the box, so the diagram is the biggest thing on the card while the question is read.
ART_W, ART_H = 700, 532

EP = dict(
    slug="w2-levels-10",
    kicker="IB INTERVIEW LEVELS #10",
    hook=dict(
        say=[("Can negative working capital be a good sign?", "Can negative working capital be a good sign?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="4 interview questions. Each one harder.",
        qsize=74,
        hl=["good sign?"],
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0, ans_min=ART_H,
             art=lambda t0, d: picture("wc_minus", t0, d, w=ART_W, h=ART_H),
             q=[("What's net working capital?", "What's net working capital?")],
             hl=["working capital?"],
             a=[("Current assets, minus current liabilities.", "Current assets minus current liabilities.", "big"),
                ("In a model, leave out cash and debt.", "In a model, leave out cash and debt.")],
             bigsize=84),
        dict(tail="medium.", think=1.3, ans_min=ART_H,
             art=lambda t0, d: picture("shelf_cash", t0, d, w=ART_W, h=ART_H),
             q=[("Inventory goes up by thirty, paid in cash.", "Inventory goes up by $30, paid in cash."),
                ("What happens to cash flow?", "What happens to cash flow?")],
             hl=["cash flow?"], qsize=58,
             a=[("Down thirty.", "Down $30."),
                ("The cash is sitting on a shelf until it sells.", "The cash is sitting on a shelf until it sells.")],
             bigsize=140, chip="Inventory +$30 &rarr; cash &minus;$30", chip_at=1),
        dict(tail="tricky.", think=1.6,
             art=lambda t0, d: picture("prepaid", t0, d, w=ART_W, h=500),
             q=[("A customer pays forty up front, for next year's service.", "A customer pays $40 up front, for next year's service."),
                ("How much revenue today?", "How much revenue today?")],
             hl=["revenue today?"], qsize=52, ans_min=500,
             a=[("None.", "None."),
                ("Cash goes up forty, and so does deferred revenue, a liability.",
                 "Cash goes up $40, and so does deferred revenue, a liability.")],
             bigsize=150, chip="Cash +$40 = deferred revenue +$40", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0, ans_min=500,
             art=lambda t0, d: picture("cash_first", t0, d, w=ART_W, h=500),
             q=[("Can negative working capital be a good sign?", "Can negative working capital be a good sign?")],
             hl=["good sign?"], qsize=56,
             a=[("Yes.", "Yes."),
                ("Like level three, customers pay you first.", "Like level 3, customers pay you first."),
                ("You pay suppliers later, so growth brings cash in.",
                 "You pay suppliers later, so growth brings cash in.")],
             bigsize=130, chip="Paid first, pay later", chip_at=2),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comments.": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
