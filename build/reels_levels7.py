"""
Levels #7: four interview questions on share count and dilution, each one
harder. The hook asks the last level first; level 3 teaches the treasury
stock method that level 4 turns over.

Every answer, worked:
    L1  Equity value (market cap) = share price x diluted shares outstanding.
    L2  Diluted EPS = net income / diluted shares = 110 / 55 = $2.00.
        (Basic EPS would be 110 / 50 = $2.20; the question asks for diluted.)
    L3  Treasury stock method: 10 options, strike $10, share price $20.
        Exercise: 10 new shares issued, the company receives 10 x $10 = $100.
        It uses the $100 to buy back shares at $20: 100 / 20 = 5 shares.
        Net new shares = 10 - 5 = 5.
    L4  Out-of-the-money options (strike above the share price) are left out
        of diluted shares: nobody would pay the strike for a share worth less.
        Run through level 3's method, e.g. 10 options, strike $30, price $20:
        issue 10, proceeds $300 buy back 300 / 20 = 15, net -5, so they would
        reduce the count. They are anti-dilutive and are counted as zero.

    python build/reels_levels7.py BELLA
"""

import sys

from levels import make, RED, TEAL

EP = dict(
    slug="w2-levels-7",
    kicker="IB INTERVIEW LEVELS #7",
    hook=dict(
        say=[("Do out of the money options dilute?",
              "Do out of the money options dilute?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="4 interview questions. Each one harder.",
        hl=["dilute?"],
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0,
             q=[("How do you get equity value from the share price?",
                 "How do you get equity value from the share price?")],
             hl=["equity value"],
             a=[("Share price times diluted shares.", "Share price × diluted shares", "big")],
             bigsize=74),
        dict(tail="medium.", think=1.3,
             q=[("Net income is a hundred and ten.", "Net income is $110."),
                ("Diluted shares are fifty five.", "Diluted shares are 55."),
                ("What's diluted earnings per share?", "What's diluted earnings per share?")],
             hl=["earnings per share?"],
             a=[("Two dollars.", "$2.00"), ("A hundred and ten, divided by fifty five.",
                                           "$110 divided by 55 shares.")],
             chip="110 / 55 = $2.00", chip_at=1),
        dict(tail="tricky.", think=1.6,
             q=[("There are ten options with a strike of ten dollars.",
                 "There are 10 options with a $10 strike."),
                ("The share price is twenty.", "The share price is $20."),
                ("Using the treasury stock method, how many new shares?",
                 "Treasury stock method: how many new shares?")],
             hl=["new shares?"], qsize=56,
             a=[("Five.", "5"),
                ("Ten shares are issued, and the hundred dollars they bring in buys back five.",
                 "10 shares are issued, and the $100 they bring in buys back 5.")],
             chip="10 &minus; 100 / 20 = 5", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=2.0,
             q=[("Do out of the money options dilute?",
                 "Do out of the money options dilute?")],
             hl=["dilute?"],
             a=[("No.", "No."),
                ("Nobody pays a strike above the share price.",
                 "Nobody pays a strike above the share price."),
                ("Run level three and you'd buy back more shares than you issue, so it's zero.",
                 "Run level 3: you'd buy back more shares than you issue, so it's 0.")],
             bigsize=88, chip="Strike &gt; price &rarr; 0 new shares", chip_at=1),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comments.": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
