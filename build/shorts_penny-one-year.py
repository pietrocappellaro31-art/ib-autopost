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
from motion import A
from sketch import picture, Pen, coin

# Colour and pictures (10 Nov, Pietro: "make the video more engaging with pictures and colors
# and more animated"): a colour ground per part, a drawing in the answer zone of every level,
# coins drifting behind, and a shower of coins at the score.
COPPER, MINT, SKY, ROSE, GOLD = "#F2D6BF", "#D2E9E1", "#D6E2F3", "#F6CFC3", "#F3E4BC"


def coin_svg(value, metal, r, t0, flip=0, fx="pop"):
    p = Pen(t0, 1)
    coin(p, r + 6, r + 6, r, value, metal, 0, flip=flip, fx=fx)
    return f'<svg width="{2 * r + 12}" height="{2 * r + 22}" style="overflow:visible">{"".join(p.parts)}</svg>'


def floaters(total):
    """Faint coins drifting slowly at the edges, clear of the header, the text and the footer."""
    out = ""
    spots = [(-120, 330, 95, "copper"), (650, 420, 70, "nickel"), (-110, 860, 70, "nickel"),
             (670, 900, 95, "copper"), (-60, 1080, 55, "copper")]
    for k, (x, y, r, m) in enumerate(spots):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.2">'
                + A(coin_svg("", m, r, -1), "float", 0, 1, amp=24, w=.5 + .1 * k, ph=k * 1.7) + "</div>")
    return out


def rain(t0, dur):
    """Coins falling in below the score, then bobbing."""
    import random
    rnd = random.Random(7)
    out = ""
    spots = [(rnd.uniform(-20 + 80 * k, 40 + 80 * k), rnd.uniform(1030, 1110)) for k in range(9)]
    for k, (x, y) in enumerate(spots):
        m = rnd.choice(["copper", "copper", "nickel"])
        r = rnd.uniform(38, 60)
        out += A(A(coin_svg("1\u00a2" if m == "copper" else "5\u00a2", m, r, -1), "float", 0, 1, amp=8, w=1.4, ph=k),
                 "move", t0 + .1 + .07 * k, .9, y=-1700, style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px")
    return out


EP = dict(
    slug="shorts-penny-one-year",
    kicker="THE PENNY: 1 YEAR ON",
    hook=dict(
        say=[("Which coin loses more per coin than the penny?",
              "Which coin loses more per coin than the penny?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="The last penny was struck a year ago this week.",
        hl=["than the penny?"], qsize=78, bg=COPPER, art_w=250, art_h=200,
        art=lambda t0, d: picture("last_coin", t0, max(d, 2.5), w=250, stamp="LAST ONE"),
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0, bg=COPPER, ans_min=520,
             art=lambda t0, d: picture("pricetag", t0, d, w=650, value="1\u00a2", tag="?\u00a2"),
             q=[("What did one penny cost to make?", "What did 1 penny cost to make?")],
             hl=["cost to make?"],
             a=[("Three point six nine cents.", "3.69¢"),
                ("For a one cent coin, in twenty twenty four.", "For a 1¢ coin, in 2024.")],
             bigsize=110),
        dict(tail="medium.", think=1.3, bg=MINT, ans_min=520,
             art=lambda t0, d: picture("receipt", t0, d, w=650, total="$4.97", circle=4),
             q=[("You pay four ninety seven in cash.", "You pay $4.97 in cash."),
                ("No pennies.", "No pennies."),
                ("What do you hand over?", "What do you hand over?")],
             hl=["hand over?"],
             a=[("Four ninety five.", "$4.95"),
                ("A seven rounds down to the nearest five cents.", "A 7 rounds down to the nearest 5¢.")],
             chip="1, 2, 6, 7 &darr; &nbsp; 3, 4, 8, 9 &uarr;", chip_at=1),
        dict(tail="tricky.", think=1.5, bg=SKY, ans_min=520,
             art=lambda t0, d: picture("card_tap", t0, d, w=650, amount="$4.97"),
             q=[("Same four ninety seven, but by card.", "Same $4.97, but by card."),
                ("What do you pay?", "What do you pay?")],
             hl=["by card."],
             a=[("Four ninety seven.", "$4.97"),
                ("Cards aren't rounded.", "Cards aren't rounded."),
                ("Only cash is.", "Only cash is.")],
             chip="Card: to the cent", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=1.8, bg=ROSE, ans_min=520,
             art=lambda t0, d: picture("lineup", t0, d, w=650),
             art_after=lambda t: coin_svg("5\u00a2", "nickel", 95, t, flip=3),
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
               cols={"comments.": RED}, bg=GOLD, art=rain),
    floaters=floaters,
    speed=1.0,
    music=True,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
