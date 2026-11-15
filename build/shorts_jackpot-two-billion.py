"""
YouTube Short, Format D (animated calculation), 15 Nov 2026, on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9). The record $2.04 billion jackpot, whose winner took $997.6 million in cash: not taxes,
but the time value of money. Thirty payments growing 5% a year are built up on screen, brought back to today one by
one, and added up to the cash option.

Sources (all opened in this run, 15 Nov 2026):
    [1] Powerball, "Ticket in California wins world record $2.04 billion Powerball jackpot".
        https://www.powerball.com/ticket-california-wins-world-record-204-billion-powerball-jackpot
        "$2.04 billion", "$997.6 million cash"; one ticket sold in California; the delayed Monday 7 Nov 2022 drawing,
        held the morning of 8 Nov; annuity "one immediate payment followed by 29 annual payments that increase by 5%
        each year"; odds 1 in 292.2 million.
    [2] Powerball, FAQs. https://www.powerball.com/faqs/
        Annuity: one immediate payment and 29 annual payments, increasing 5% a year ("30 increasing payments over 29
        years"); the cash value is the amount needed in the prize pool on drawing day to fund the annuity; the annuity
        factor "is made up of interest rates for securities purchased to fund prize payments"; "Both advertised prize
        options are prior to federal and jurisdictional taxes."
    [3] NPR, "Someone in California won the $2 billion Powerball jackpot", 8 Nov 2022.
        https://www.npr.org/2022/11/08/1135068822/powerball-jackpot-drawing-delayed
        $2.04 billion, $997.6 million lump sum, Joe's Service Center in Altadena; drawn 8:57 a.m. ET on the Tuesday;
        the full amount means annuity payments over 29 years.
    [4] Still the record: DraftKings Network, "What's the biggest lottery jackpot in U.S. history?", 6 Feb 2026,
        https://dknetwork.draftkings.com/2026/02/06/whats-the-biggest-lottery-jackpot-in-u-s-history/ (the $2.04
        billion Powerball of 7 Nov 2022 at the top); CBS News, updated 25 Dec 2025,
        https://www.cbsnews.com/news/powerball-mega-millions-lottery-jackpots-bigger-top-prizes/ (largest on record;
        $1.817 billion of 24 Dec 2025 second). Jackpots in November 2026 are far below it (tens of millions in the
        week's results searched in this run), so "the biggest jackpot ever" stands as of this run.

Our arithmetic (checked with a short script in this run; shown on screen as figures, the rate badged OUR ESTIMATE):
    30 payments P x 1.05^k, k = 0..29, add up to P x 66.4388 = $2.04B, so P = $30.70M (first) and the last is
    P x 1.05^29 = $126.39M. The rate r at which those 30 payments are worth $997.6M today (sum of P x 1.05^k / (1+r)^k)
    is r = 4.432%, said as "about four point four percent a year". At 4.432% the last payment is worth $35.93M today
    ("about $35.9M"). Check: at 3% they would be worth $1,234M, at 5% $921M, so higher rates mean a smaller cash
    option (the dial beat). This is our simplification (yearly discounting, payment 1 on day one); the lottery's real
    figure comes from the price of the securities it buys [2], so the rate is an estimate, not a quoted yield.
    "About half": 997.6 / 2040 = 48.9%.

Beats, checked:
    hook     [1][4] biggest jackpot ever, $2.04 billion; [1][3] $997.6 million cash, about half (48.9%).
    taxes    [2] both prize options are before tax.
    print    [1][2] 30 payments over 29 years, each 5% bigger.
    catch    general time value of money: a dollar today can earn interest (no figure).
    math     our arithmetic above (OUR MATH badge): each payment's value today; the far ones shrink the most.
    cash     [1][2][3] $997.6 million; [2] what is needed today to fund the payments.
    rate     our estimate, 4.4% a year; higher rates shrink the cash option (the arithmetic above and [2]).
    Drawings are our own generic shapes: no lottery logo, ticket, ball design or real person. The winner is not named.

    python3 build/shorts_jackpot-two-billion.py HEART
"""

import random
import sys

from motion import A
from sketch import picture, coin as _coin, _ball, Pen  # noqa: F401
from story import make, RED, TEAL

GOLDG, SAND, MINT, CREAM, SKY, TEALG, BLUSH, LILAC = ("#F6E7C8", "#EFE3D3", "#D2E9E1", "#F7EBD9", "#D6E2F3", "#D5ECE8",
                                                      "#F3DCD3", "#E2DAF0")


def ball(w, n, fill="#fff"):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 120 120" style="overflow:visible">{_ball(60, 60, 54, n, fill)}</svg>')


def floaters(total):
    """Faint numbered balls drifting at the edges, clear of the text."""
    out = ""
    for k, (x, y, n, w) in enumerate([(-100, 330, 7, 170), (760, 560, 29, 150), (-110, 1010, 30, 150), (760, 1110, 5, 170)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.13">'
                + A(ball(w, n, "#F2C35B" if k % 2 else "#fff"), "float", 0, 1, amp=22, w=.5 + .1 * k, ph=k * 1.7) + "</div>")
    return out


def rain(t0, dur):
    """Numbered balls falling in under the comment ask, then bobbing."""
    rnd = random.Random(2022)
    out = ""
    for k in range(9):
        x, y = rnd.uniform(-20 + 80 * k, 30 + 80 * k), rnd.uniform(1030, 1110)
        art = ball(rnd.uniform(110, 140), rnd.randint(1, 69), "#F2C35B" if k % 3 == 0 else "#fff")
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px")
    return out


PIC = dict(w=752, h=640)

EP = dict(
    slug="shorts-jackpot-two-billion",
    kicker="MONEY MATHS",
    mood="playful",
    cover_at=6.8,      # 15 Nov: after the half column and the question mark land
    beats=[
        dict(tag="THE RECORD", bg=GOLDG, size=66, hl=["about half."],
             say=[("The biggest jackpot ever was two point oh four billion dollars.",
                   "The biggest jackpot ever was $2.04 billion."),
                  ("The winner took about half.", "The winner took about half."),
                  ("So where did the rest go?", "So where did the rest go?")],
             art=lambda t0, d, seg: picture("jackpot_hook", t0, d, half_s=seg[1][0] + .9 - t0, **PIC),
             sfx=[(("s", 1, 1.0), "thump", .14), (("s", 1, 1.9), "pop", .08)]),
        dict(tag="NOT TAXES", bg=SAND, hl=["before tax."],
             say=[("It wasn't taxes.", "It wasn't taxes."),
                  ("Both numbers come before tax.", "Both numbers come before tax.")],
             art=lambda t0, d, seg: picture("before_tax", t0, d, stamp_s=seg[1][1] - .2 - t0, **PIC),
             sfx=[(.08, "pop", .06), (.2, "pop", .06), (("e", 1, -.9), "paper", .1), (("e", 1, -.2), "thump", .15)]),
        dict(tag="THE FINE PRINT", bg=CREAM, hl=["thirty payments,", "5% bigger"],
             say=[("That two billion is thirty payments, spread over twenty nine years.",
                   "That $2 billion is 30 payments, spread over 29 years."),
                  ("Each one's five percent bigger than the last.", "Each one's 5% bigger than the last.")],
             art=lambda t0, d, seg: picture("thirty_bars", t0, d, grow_s=seg[0][0] + .6 - t0, five_s=seg[1][0] + .4 - t0, **PIC),
             sfx=[(("s", 0, .6 + .075 * k), "tick", .03) for k in range(0, 30, 2)] + [(("s", 1, .45), "pop", .07)]),
        dict(tag="THE CATCH", bg=MINT, hl=["beats a dollar later."],
             say=[("But a dollar today beats a dollar later.", "But a dollar today beats a dollar later."),
                  ("Today's dollar can earn interest while you wait.", "Today's dollar can earn interest while you wait.")],
             art=lambda t0, d, seg: picture("dollar_today", t0, d, grow_s=seg[1][0] + .3 - t0, **PIC),
             sfx=[(("s", 1, .55 + .3 * j), "clink", .07) for j in range(5)] + [(("s", 1, 2.05), "clink", .05)]),
        dict(tag="THE MATH", badge="OUR MATH", bg=SKY, hl=["it shrinks.", "shrink most."],
             say=[("So bring each payment back to today, and it shrinks.",
                   "So bring each payment back to today, and it shrinks."),
                  ("And the furthest ones shrink most.", "And the furthest ones shrink most.")],
             art=lambda t0, d, seg: picture("shrink_bars", t0, d, shrink_s=seg[0][1] - 1.0 - t0, **PIC),
             sfx=[(("e", 0, -1.0 + .06 * k), "tick", .025) for k in range(0, 30, 3)] + [(("e", 0, -1.0 + 2.1), "pop", .07)]),
        dict(tag="THE CASH OPTION", bg=TEALG, hl=["$997.6 million."],
             say=[("Add them up, and you get nine hundred and ninety seven point six million.",
                   "Add them up, and you get $997.6 million."),
                  ("That's what it costs today to fund all thirty payments.",
                   "That's what it costs today to fund all 30 payments.")],
             art=lambda t0, d, seg: picture("cash_pile", t0, d, at_s=seg[0][0] + .5 - t0, **PIC),
             sfx=[(("s", 0, .5 + .05 * k + .4), "clink", .035) for k in range(0, 30, 5)]
                 + [(("s", 0, .5 + 2.1), "ding", .06)]),
        dict(tag="THE RATE", badge="OUR ESTIMATE", bg=BLUSH, hl=["4.4 percent a year."],
             say=[("Work it backwards, and that's about four point four percent a year.",
                   "Work it backwards, and that's about 4.4 percent a year."),
                  ("Higher rates shrink it even more.", "Higher rates shrink it even more.")],
             art=lambda t0, d, seg: picture("rate_dial", t0, d, rate_s=seg[0][0] + .8 - t0, more_s=seg[1][0] + .2 - t0, **PIC),
             sfx=[(("s", 0, .8 + .9), "knock", .12), (("s", 1, 1.0), "thump", .14)]),
    ],
    close=dict(say=[("Cash now, or thirty payments?", "Cash now, or 30 payments?"),
                    ("Which would you take?", "Which would you take?"),
                    ("Tell me in the comments.", "Tell me in the comments."),
                    ("And subscribe for more like this.", "And subscribe for more like this.")],
               cols={"comments.": RED}, bg=LILAC, art=rain,
               pic=lambda t0, d: picture("jackpot_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # clean master: Pietro adds a sound in the YouTube app
    lufs=-14,
    room=.0003,           # 15 Nov: half the default room tone; mix 3.22 to 3.24 OVRL against 3.17 (remix test in qa.md)
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
