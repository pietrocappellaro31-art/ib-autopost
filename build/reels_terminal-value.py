"""
Levels #12: four interview questions on terminal value in a DCF, each one
harder. The hook asks the last level first; level 3 (an exit multiple gives
$400 at year 5) is the number level 4 discounts, and the voice says so.

Terminal value = the value, at the end of the forecast, of every cash flow
after it. A DCF is the present value of the forecast years plus the present
value of the terminal value.

Every answer, worked (textbook DCF mechanics, round example numbers, no
statistic, company or "typical share" claimed):
    L1  Terminal value is everything after the forecast period: the value at
        the last forecast year of all the cash flows beyond it.
    L2  Two ways: perpetuity growth (the last year's free cash flow grown at
        a constant rate forever: FCF x (1 + g) / (r - g)) or an exit
        multiple (the last year's EBITDA times a multiple, as if sold).
    L3  Year 5 EBITDA $50, exit multiple 8x: TV = 50 x 8 = $400, a value AT
        year 5, not today.
    L4  Free cash flow $20 a year for years 1 to 5, the $400 TV at year 5,
        discount rate 10%, end-of-year discounting.
        Forecast: 20 x (1 - 1.1^-5) / 0.10 = 20 x 3.7908 = 75.82, about $76.
        TV today: 1.1^5 = 1.61051; 400 / 1.61051 = 248.37, about $248.
        Total 75.82 + 248.37 = 324.18, about $324.
        TV share: 248.37 / 324.18 = 0.766, about 77%. So yes, terminal
        value can be most of a DCF (here about three quarters). No claim is
        made about what share is usual in practice.
    Bonus (comment): same model, but the exit multiple is 6x instead of 8x.
        TV = 50 x 6 = $300 at year 5; today 300 / 1.61051 = 186.28, about
        $186. Total 75.82 + 186.28 = 262.10, about $262. Share 186.28 /
        262.10 = 0.711, about 71%. Still most of the value.

Spoken text writes numbers as words; the screen uses digits. "D C F" and
"EBITDA" are joined back by voice_check.words, so the word check is exact.

    python3 build/reels_terminal-value.py G2
"""

import sys

from levels import make, RED, TEAL
from sketch import picture

ART_W, ART_H = 700, 532

EP = dict(
    slug="w2-levels-12",
    kicker="IB INTERVIEW LEVELS #12",
    hook=dict(
        say=[("Can terminal value be most of a DCF?", "Can terminal value be most of a DCF?")],
        sub="4 interview questions. Each one harder.",
        qsize=80,
        hl=["most of a DCF?"],
        art=lambda t0, d: picture("tv_timeline", t0, d, w=400, h=320),
        art_w=400, art_h=320,
    ),
    levels=[
        dict(tail="easy.", think=1.0, ans_min=ART_H,
             art=lambda t0, d: picture("tv_timeline", t0, d, w=ART_W, h=ART_H, seed=2),
             q=[("In a DCF, what's terminal value?", "In a DCF, what's terminal value?")],
             hl=["terminal value?"],
             a=[("Everything after the forecast.", "Everything after the forecast.", "big"),
                ("All the years you don't model one by one.", "All the years you don't model one by one.")],
             bigsize=96, chip="Years 1 to 5 + terminal value", chip_at=1),
        dict(tail="medium.", think=1.3, ans_min=ART_H,
             art=lambda t0, d: picture("two_ways", t0, d, w=ART_W, h=ART_H),
             q=[("Name the two ways to calculate it.", "Name the 2 ways to calculate it.")],
             hl=["two ways"], qsize=62,
             a=[("Growth, or a multiple.", "Growth, or a multiple.", "big"),
                ("Grow the last cash flow forever, or sell at a multiple of EBITDA.",
                 "Grow the last cash flow forever, or sell at a multiple of EBITDA.")],
             bigsize=104, chip="Grow forever, or sell", chip_at=1),
        dict(tail="tricky.", think=1.6, ans_min=500,
             art=lambda t0, d: picture("exit_stack", t0, d, w=ART_W, h=500),
             q=[("Year five EBITDA is fifty dollars, exit multiple eight times.",
                 "Year 5 EBITDA is $50, exit multiple 8x."),
                ("What's terminal value?", "What's terminal value?")],
             hl=["terminal value?"], qsize=54,
             a=[("Four hundred dollars.", "$400."),
                ("Fifty times eight, but that's in year five.", "$50 times 8, but that's in year 5.")],
             bigsize=150, chip="$50 &times; 8 = $400", chip_at=1),
        dict(label="Here's the last one.", tail="final boss.", think=2.0, ans_min=500,
             art=lambda t0, d: picture("discount_shrink", t0, d, w=ART_W, h=500),
             q=[("Twenty a year for five years, then the four hundred from level three, at ten percent.",
                 "$20 a year for 5 years, then the $400 from level 3, at 10%."),
                ("Is terminal value most of it?", "Is terminal value most of it?")],
             hl=["most of it?"], qsize=48,
             a=[("Yes.", "Yes."),
                ("Discounted, the four hundred is about two hundred and forty eight.", "Discounted, the $400 is about $248."),
                ("The five years add seventy six, so about seventy seven percent.", "The 5 years add $76, so about 77%.")],
             bigsize=104, chip="$248 of $324 = 77%", chip_at=2),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And follow for two questions a day.", "And follow for two questions a day.")],
               cols={"comments.": RED}),
    speed=1.0,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
