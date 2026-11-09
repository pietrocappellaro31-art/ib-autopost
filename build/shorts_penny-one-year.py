"""
YouTube Short: four levels on the end of the penny, one year after the last
circulating cent was struck (12 Nov 2025). The hook asks the last level first.

Sources:
    [1] Federal Reserve Bank of St. Louis, Page One Economics, May 2026,
        "When a Penny Costs More Than a Penny: The Economics Behind Ending the
        Cent": final circulating penny struck 12 Nov 2025, ending 232 years;
        penny still legal tender; cash totals rounded to the nearest five
        cents (final digit 1, 2, 6, 7 rounds down; 3, 4, 8, 9 rounds up);
        "no rounding for payments made electronically"; 2024 seigniorage
        pennies -$85.3 million, nickels -$17.7 million.
        https://www.stlouisfed.org/publications/page-one-economics/2026/may/penny-costs-more-than-penny-economics-behind-ending-the-cent
    [2] CoinNews, 10 Feb 2025, from the US Mint's FY2024 annual report:
        penny unit cost 3.69 cents, nickel 13.78 cents; "For the nineteenth
        consecutive year in 2024, the unit cost of producing pennies and
        nickels exceeded their face values."
        https://coinnews.net/2025/02/10/penny-costs-3-69-cents-to-make-in-2024
    [3] Coin World, 13 Nov 2025, "Final cent for circulation struck at
        Philadelphia Mint": 232-year run; the penny remains legal tender.
        https://www.coinworld.com/news/us-coins/final-cent-for-circulation-struck-at-philadelphia-mint

Every answer, worked:
    L1  A penny cost 3.69 cents to make in fiscal 2024 [2].
    L2  Cash total $4.97: final digit 7 rounds down to the nearest five
        cents, so $4.95 [1]. (Rounding rules are set by businesses and
        states; this is the common rule the St. Louis Fed describes.)
    L3  Same $4.97 by card: $4.97. No rounding on electronic payments [1].
    L4  The nickel. 13.78 - 5 = 8.78 cents lost per nickel, against
        3.69 - 1 = 2.69 cents per penny [2]. (In total the penny lost more,
        $85.3m against $17.7m [1], because far more pennies were made: the
        question is per coin, and the docstring keeps that straight.)

    python3 build/shorts_penny-one-year.py GEORGE
"""

import sys

from levels import make, RED, TEAL

EP = dict(
    slug="shorts-penny-one-year",
    kicker="THE PENNY: 1 YEAR ON",
    hook=dict(
        say=[("Which coin loses more per coin than the penny?",
              "Which coin loses more per coin than the penny?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="The last penny was struck a year ago this week.",
        hl=["than the penny?"], qsize=78,
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0,
             q=[("What did one penny cost to make?", "What did 1 penny cost to make?")],
             hl=["cost to make?"],
             a=[("Three point six nine cents.", "3.69¢"),
                ("For a one cent coin, in twenty twenty four.", "For a 1¢ coin, in 2024.")],
             bigsize=110),
        dict(tail="medium.", think=1.3,
             q=[("You pay four ninety seven in cash.", "You pay $4.97 in cash."),
                ("No pennies.", "No pennies."),
                ("What do you hand over?", "What do you hand over?")],
             hl=["hand over?"],
             a=[("Four ninety five.", "$4.95"),
                ("A seven rounds down to the nearest five cents.", "A 7 rounds down to the nearest 5¢.")],
             chip="1, 2, 6, 7 &darr; &nbsp; 3, 4, 8, 9 &uarr;", chip_at=1),
        dict(tail="tricky.", think=1.5,
             q=[("Same four ninety seven, but by card.", "Same $4.97, but by card."),
                ("What do you pay?", "What do you pay?")],
             hl=["by card."],
             a=[("Four ninety seven.", "$4.97"),
                ("Cards aren't rounded.", "Cards aren't rounded."),
                ("Only cash is.", "Only cash is.")],
             chip="Card: to the cent", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=1.8,
             q=[("Which coin loses more per coin than the penny?",
                 "Which coin loses more per coin than the penny?")],
             hl=["than the penny?"],
             a=[("The nickel.", "The nickel."),
                ("It cost almost fourteen cents to make a five cent coin.",
                 "It cost almost 14¢ to make a 5¢ coin.")],
             bigsize=104, chip="13.78 &minus; 5 = 8.78¢ lost", chip_at=1,
             foot="Per coin, FY2024. Source: US Mint annual report."),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And subscribe for one of these every day.", "And subscribe for one of these every day.")],
               cols={"comments.": RED}),
    speed=1.0,
    music=True,
    music_level=.14,          # voice about 15 dB over the bed while speaking (12 dB at the default .2)
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
