"""
YouTube Short: four levels on buy now, pay later, two and a half weeks before
Black Friday (27 Nov 2026) and the week Affirm reported a record quarter. The
hook asks the last level first.

Sources:
    [1] NerdWallet, "Affirm Buy Now, Pay Later Review": Pay in 4 is four
        installments "due every two weeks", the first one (one fourth of the
        price) "typically" due at checkout, 0% APR; "Monthly payments may
        charge up to 36% APR"; "Affirm doesn't charge any fees, including no
        late fees."
        https://www.nerdwallet.com/personal-loans/reviews/affirm-buy-now-pay-later
    [2] Experian plc press release, March 2025, "Affirm Expands Credit
        Reporting with Experian to Include All Pay-Over-Time Products":
        "Beginning April 1, 2025, Affirm plans to report to Experian all
        pay-over-time loan products issued from that date, including Pay in 4".
        https://www.experianplc.com/newsroom/press-releases/2025/affirm-expands-credit-reporting-with-experian-to-include-all-pay
    [3] 24/7 Wall St., 10 Nov 2026, on Affirm's fiscal Q1 ($14.4 billion of
        gross merchandise volume) and the same $1,000 at 36% example ($206 of
        interest). Context only; the number below is worked here.
        https://247wallst.com/personal-finance/2026/11/10/you-get-screwed-by-those-people-ramsey-torches-affirm-the-morning-after-its-record-14-4-billion-quarter/

Every answer, worked:
    L1  $100 in four equal payments: $25 each, the first at checkout [1].
    L2  The other three every two weeks [1]: weeks 2, 4 and 6, so the
        purchase is paid off six weeks after checkout.
    L3  Yes. Affirm reports Pay in 4 loans issued from 1 April 2025 to
        Experian [2]. (Said for Affirm only; other lenders differ.)
    L4  $1,000 repaid in 12 equal monthly payments at 36% APR (the top of
        Affirm's range [1]): monthly rate 3%, payment
        1000 x 0.03 / (1 - 1.03^-12) = $100.46; 12 x 100.46 = $1,205.55,
        so $205.55 of interest, about $206, 20.6% of the price, more than
        a fifth. Matches [3].

    python3 build/shorts_bnpl-pay-in-four.py GEORGE
"""

import random
import sys

from levels import make, RED, TEAL
from motion import A
from sketch import picture

# A colour ground per part (the penny Short standard, 10 Nov).
LILAC, GOLD, MINT, SKY, ROSE, PEACH = "#E4DAF0", "#F3E4BC", "#D2E9E1", "#D6E2F3", "#F6CFC3", "#F2D6BF"


def card_svg(w, fill="#14A08F", dark="#0B4F49"):
    h = round(w * .63)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 330 210" style="overflow:visible">'
            f'<rect x="2" y="2" width="326" height="206" rx="22" fill="{fill}" stroke="{dark}" stroke-width="5"/>'
            f'<rect x="40" y="62" width="62" height="48" rx="8" fill="#F2C35B"/>'
            f'<rect x="40" y="150" width="210" height="16" rx="8" fill="#fff" fill-opacity=".55"/></svg>')


def tile_svg(w, label="$25", fill="#F2C35B"):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 170 170" style="overflow:visible">'
            f'<rect x="3" y="3" width="164" height="164" rx="24" fill="{fill}" stroke="#0A0A0A" stroke-width="5"/>'
            f'<text x="85" y="104" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="58" '
            f'fill="#0A0A0A">{label}</text></svg>')


def floaters(total):
    """Faint cards and payment tiles drifting at the edges, clear of the text."""
    out = ""
    spots = [(-150, 330, "card", 230), (690, 430, "tile", 140), (-100, 880, "tile", 120),
             (700, 930, "card", 200), (-70, 1090, "tile", 100)]
    for k, (x, y, kind, w) in enumerate(spots):
        art = card_svg(w, "#7A6BB0", "#4A3D80") if kind == "card" else tile_svg(w, "$25")
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.18">'
                + A(art, "float", 0, 1, amp=24, w=.5 + .1 * k, ph=k * 1.7) + "</div>")
    return out


def rain(t0, dur):
    """Payment tiles and cards falling in below the score, then bobbing."""
    rnd = random.Random(11)
    out = ""
    for k in range(9):
        x, y = rnd.uniform(-20 + 80 * k, 30 + 80 * k), rnd.uniform(1030, 1110)
        art = card_svg(rnd.uniform(120, 150)) if k % 3 == 1 else tile_svg(rnd.uniform(80, 105), "$25")
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:rotate({rnd.uniform(-14, 14):.0f}deg)")
    return out


def interest_count(t):
    """Beside the level 4 answer: the interest counting up from $0 to $206 on a red tag."""
    return (f'<svg width="200" height="104" viewBox="0 0 250 130" style="overflow:visible;margin-top:8px">'
            f'<rect x="4" y="4" width="242" height="122" rx="22" fill="{RED}" stroke="#0A0A0A" stroke-width="5"/>'
            f'<text x="125" y="92" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="76" fill="#fff" '
            f'class="a" data-fx="count" data-at="{t + .2}" data-d="1.4" data-from="0" data-to="206" data-pre="+$">+$206</text></svg>')


def four_tiles(t):
    """Beside the level 1 answer: four $25 tiles, the first one lit."""
    return ('<div style="display:flex;gap:10px;margin-top:14px">'
            + "".join(A(tile_svg(78, "$25", "#F2C35B" if k == 0 else "#fff"), "pop", t + .15 + .12 * k, .4) for k in range(4))
            + "</div>")


EP = dict(
    slug="shorts-bnpl-pay-in-four",
    kicker="BUY NOW, PAY LATER",
    hook=dict(
        say=[("What's the interest on a thousand dollars at thirty six percent for a year?",
              "What's the interest on $1,000 at 36% for a year?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="Black Friday is 27 November.",
        hl=["at 36%"], qsize=74, bg=LILAC, art_w=350, art_h=280, lsize=58,
        art=lambda t0, d: picture("bag_later", t0, max(d, 2.5), w=350, tag="LATER"),
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0, bg=GOLD, ans_min=520,
             art=lambda t0, d: picture("split4", t0, d, w=650, total="$100"),
             art_after=four_tiles,
             q=[("Hundred dollar shoes, pay in four.", "$100 shoes, pay in 4."),
                ("What do you pay at checkout?", "What do you pay at checkout?")],
             hl=["at checkout?"],
             a=[("Twenty five dollars.", "$25"),
                ("The first payment is due today.", "The first payment is due today.")],
             bigsize=120),
        dict(tail="medium.", think=1.3, bg=MINT, ans_min=520,
             art=lambda t0, d: picture("pay_dots", t0, d, w=650),
             q=[("And the other three?", "And the other three?"),
                ("When are they due?", "When are they due?")],
             hl=["When are they due?"],
             a=[("Every two weeks.", "Every 2 weeks."),
                ("All paid off in six weeks.", "All paid off in 6 weeks.")],
             chip="Today &middot; wk 2 &middot; wk 4 &middot; wk 6", chip_at=1, bigsize=112),
        dict(tail="tricky.", think=1.5, bg=SKY, ans_min=520,
             art=lambda t0, d: picture("credit_report", t0, d, w=650),
             q=[("Can pay in four show up on your credit report?", "Can pay in 4 show up on your credit report?")],
             hl=["credit report?"],
             a=[("Yes, it can.", "Yes, it can."),
                ("Since April twenty twenty five, Affirm reports it to Experian.",
                 "Since April 2025, Affirm reports it to Experian.")],
             foot="Loans from 1 Apr 2025. Source: Experian, Mar 2025.", chip="All Affirm loans, Pay in 4 too", chip_at=1),
        dict(label="Last one.", tail="final boss.", think=1.8, bg=ROSE, ans_min=520,
             art=lambda t0, d: picture("interest_stack", t0, d, w=650),
             art_after=interest_count,
             q=[("What's the interest on a thousand dollars at thirty six percent for a year?",
                 "What's the interest on $1,000 at 36% for a year?")],
             hl=["at 36%"], qsize=60,
             a=[("About two hundred and six dollars.", "About $206"),
                ("More than a fifth of the price.", "More than a fifth of the price.")],
             bigsize=90, chip="12 &times; $100.46 &asymp; $1,206", chip_at=1,
             foot="12 monthly payments at 36% APR, the top of Affirm's range."),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And subscribe for one of these every day.", "And subscribe for one of these every day.")],
               cols={"comments.": RED}, bg=PEACH, art=rain),
    floaters=floaters,
    speed=1.0,
    music=False,          # Pietro adds a trending sound in the YouTube app at upload
    lufs=-14,             # YouTube loudness, without a music bed
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
