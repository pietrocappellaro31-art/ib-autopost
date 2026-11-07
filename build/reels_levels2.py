"""
Levels #2: four interview questions on multiples and M&A, each one harder,
in Pietro's cloned voice. The hook asks the last level first.

Every answer, worked:
    L1  P/E = share price / EPS = equity value / net income. Net income is
        after interest, so it belongs to shareholders: equity value.
    L2  EBITDA is before interest, so it is available to lenders and
        shareholders alike: enterprise value.
    L3  Equity 100, net debt 50, EV 150. Share price doubles, share count the
        same: equity 200, net debt still 50, EV 250 (not 300).
    L4  Acquirer at 20x earnings pays in stock for a target bought at 10x:
        acquirer E 100 on 100 shares at $20 (EPS $1.00); target E 50 bought
        for 500 = 25 new shares; combined 150 / 125 = $1.20. Accretive, before
        fees and synergies. A higher P/E buying a lower P/E all in stock is
        always accretive on these assumptions.
    Bonus (comment): 10x buying 20x all in stock is dilutive.

    python build/reels_levels2.py clone:/path/to/reference.wav
"""

import sys

from levels import make, RED, TEAL

Q4 = ("A company at twenty times earnings buys one at ten times, all in stock, accretive or dilutive?",
      "A company at 20&times; earnings buys one at 10&times;, all in stock. Accretive or dilutive?")

EP = dict(
    slug="w2-levels-2",
    kicker="IB INTERVIEW LEVELS #2",
    hook=dict(
        say=[Q4, ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="4 interview questions. Each one harder.",
        hl=["Accretive or dilutive?"],
        cols={"4.": RED, "score.": RED},
        qsize=66,
    ),
    levels=[
        dict(tail="easy.", think=1.0,
             q=[("Price to earnings, enterprise value or equity value?",
                 "Price to earnings: enterprise value or equity value?")],
             hl=["earnings:"],
             a=[("Equity value.", "Equity value."),
                ("Earnings belong to shareholders, so you match them with equity.",
                 "Earnings belong to shareholders, so you match them with equity.")],
             chip="P/E = equity value &divide; net income", chip_at=1),
        dict(tail="medium.", think=1.3,
             q=[("And EBITDA, enterprise value or equity value?",
                 "And EBITDA: enterprise value or equity value?")],
             hl=["EBITDA:"],
             a=[("Enterprise value.", "Enterprise value."),
                ("EBITDA comes before interest, so it belongs to lenders and shareholders.",
                 "EBITDA comes before interest, so it belongs to lenders and shareholders.")],
             chip="Before interest &rarr; EV &middot; after interest &rarr; equity", chip_at=1, bigsize=86),
        dict(tail="tricky.", think=1.5,
             q=[("A company has a hundred of equity value and fifty of net debt.",
                 "A company has $100 of equity value and $50 of net debt."),
                ("The share price doubles.", "The share price doubles."),
                ("What's the new enterprise value?", "What's the new enterprise value?")],
             hl=["new enterprise value?"], qsize=54,
             a=[("Two hundred and fifty.", "$250"),
                ("Only the equity doubles, to two hundred.", "Only the equity doubles, to $200."),
                ("The debt stays at fifty.", "The debt stays at $50.")],
             chip="200 + 50 = 250, not 300", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0,
             q=[("", Q4[1].replace(" Accretive or dilutive?", "")), ("Accretive or dilutive?", "Accretive or dilutive?")],
             hl=["Accretive or dilutive?"], qsize=50,
             a=[("Accretive.", "Accretive."), ("It pays with expensive shares for cheaper earnings.",
                                               "It pays with expensive shares for cheaper earnings.")],
             chip="Higher P/E buys lower P/E in stock &rarr; EPS up", foot="Before fees and synergies.", chip_at=1),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Comment it below.", "Comment it below."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comment": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
