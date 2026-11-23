"""
Reel B, 23 Nov 2026 (slot B 18:00 ET): Format B (a short financial story) on the story engine (build/story.py),
narrator HEART (Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
Profit is not cash: a print shop's $30 profit and $70 less cash in the same month (a receivable).

A worked illustration with round numbers of our own; Mia and her shop are invented, no company or statistic is
claimed. Accrual basis: revenue is counted when the work is done (the job is delivered), not when the cash arrives
(the principle of ASC 606 / IFRS 15, not named on screen). Before tax; no other jobs or costs that month.

Every number, worked:
    The job:        posters worth $100, delivered this month; the client pays in 60 days.
    Costs:          $70 of paper and ink, paid today in cash.
    Profit:         revenue 100 - costs 70 = $30 (before tax).
    Cash:           in 0, out 70: 0 - 70 = -$70 this month.
    The gap:        the $100 owed is a receivable (an asset: money she's owed). 30 - (-70) = 100: the whole gap.
    Paid:           two months later (day 60) cash +100: -70 + 100 = +$30, the same $30 as the profit.
    Rule:           profit counts what's earned, cash what's come in; growing on credit, each job here adds $30
                    of profit and takes $70 of cash until it is paid (5 jobs: +$150 profit, -$350 cash).
    Close (asked):  next month three jobs like this, none paid yet that month: profit 3 x 30 = $90, cash 3 x -70 =
                    -$210 (not given).
    Comment bonus:  the client never pays: the $100 receivable is written off as a $100 bad-debt expense, so the
                    job ends as 30 - 100 = a $70 loss (the $70 she paid out).

23 Nov, from the performance data (docs/daily/quality-log.md row of 23 Nov): the paradox opening (two facts that seem
to clash, then the question), 12 words on screen, on the story engine; Format B, last used 20 Nov.

    python3 build/reels_profit-cash.py HEART
"""

import sys

from motion import A
from sketch import picture, _ptag
from story import make, RED

TEAL_INK, GOLD = "#5EC8B4", "#F2C35B"
PIC = dict(w=752, h=640)


def chip(label, fill, w=190, color="#fff"):
    return (f'<svg width="{w}" height="{w * .6:.0f}" viewBox="0 0 {w} {w * .6:.0f}" style="overflow:visible">'
            + _ptag(w / 2, w * .3, w * .95, label, fill, color, round(w * .23)) + "</svg>")


def floaters(total):
    """Faint tags drifting at the edges, clear of the text (never the answer)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "PROFIT", GOLD, 170), (770, 560, "CASH", "#3B3F48", 150),
                                              (-100, 1030, "60 DAYS", "#0F766E", 170), (770, 1120, "$100", GOLD, 150)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-profit-cash",
    kicker="IB STORY",
    mood="calm",
    cover=dict(at=("e", 0, 1, .3), lines=["A $30 profit this month.", "So why is her cash", "down $70?"],
               hl={"$30": TEAL_INK, "profit": TEAL_INK, "$70?": RED}, avoid=["RECEIVABLE", "OWED", "INVOICE"]),
    beats=[
        dict(tag="THE PUZZLE", size=62, hold=.6, hl=["$30", "profit", "$70?"],
             say=[("A thirty dollar profit this month.", "A $30 profit this month."),
                  ("So why is her cash down seventy?", "So why is her cash down $70?")],
             art=lambda t0, d, seg: picture("pc_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "tick", .04), (("s", 0, .6), "pop", .05), (("s", 1, .2), "thump", .07), (("s", 1, .7), "pop", .05)]),
        dict(tag="THE JOB", size=56, hl=["$100", "60", "$70"],
             say=[("Mia prints a hundred dollars of posters for a client, who will pay in sixty days.",
                   "Mia prints $100 of posters for a client, who will pay in 60 days."),
                  ("She pays seventy dollars for paper and ink today.", "She pays $70 for paper and ink today.")],
             art=lambda t0, d, seg: picture("pc_job", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "paper", .05), (("s", 0, .37), "paper", .05), (("s", 0, .62), "paper", .05), (("s", 1, .25), "paper", .05),
                  (("s", 1, .75), "pop", .05)]),
        dict(tag="THE PROFIT", size=56, hl=["done,", "$100", "$70", "$30."],
             say=[("The sale counts when the work is done, so this month shows a hundred of revenue and seventy of costs.",
                   "The sale counts when the work is done, so this month shows $100 of revenue and $70 of costs."),
                  ("Profit: thirty dollars.", "Profit: $30.")],
             art=lambda t0, d, seg: picture("pc_profit", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "thump", .07), (("s", 0, .45), "tick", .04), (("s", 0, .8), "pop", .05), (("s", 1, .3), "clink", .05)]),
        dict(tag="THE CASH", size=56, hl=["yet,", "$70", "down"],
             say=[("But no money has come in yet, and seventy dollars has gone out.",
                   "But no money has come in yet, and $70 has gone out."),
                  ("Cash: down seventy.", "Cash: down $70.")],
             art=lambda t0, d, seg: picture("pc_cash", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "clink", .04), (("s", 0, .65), "tick", .04), (("s", 1, .2), "pop", .05), (("s", 1, .8), "thump", .07)]),
        dict(tag="THE GAP", size=54, hl=["receivable:", "owed.", "$30"],
             say=[("The missing hundred sits on her balance sheet as a receivable: money she's owed.",
                   "The missing $100 sits on her balance sheet as a receivable: money she's owed."),
                  ("Two months later the client pays, and her cash ends up thirty dollars higher.",
                   "Two months later the client pays, and her cash ends up $30 higher.")],
             art=lambda t0, d, seg: picture("pc_gap", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .4), "paper", .05), (("s", 0, .78), "pop", .05), (("s", 1, .5), "clink", .05), (("s", 1, .6), "thump", .06)]),
        dict(tag="THE RULE", size=56, hl=["earned.", "in.", "cash."],
             say=[("Profit counts what you've earned.", "Profit counts what you've earned."),
                  ("Cash counts what's come in.", "Cash counts what's come in."),
                  ("Grow fast on credit, and you can be profitable and still run out of cash.",
                   "Grow fast on credit, and you can be profitable and still run out of cash.")],
             art=lambda t0, d, seg: picture("pc_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "pop", .05), (("s", 1, .2), "pop", .05), (("s", 2, .1), "tick", .04), (("e", 2, .1), "thump", .07)]),
    ],
    close=dict(say=[("Next month she takes three jobs like this one.", "Next month she takes three jobs like this one."),
                    ("What's her profit, and her cash?", "What's her profit, and her cash?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED}, bar=True, art_w=720, art_h=576,
               pic=lambda t0, d: picture("pc_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,
    music=False,
    lufs=-16,
    theme="black",
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
