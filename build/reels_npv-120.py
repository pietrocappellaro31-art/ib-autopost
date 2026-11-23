"""
Reel A, 23 Nov 2026 (slot A 12:30 ET): Format C (one surprising concept) on the story engine (build/story.py),
narrator HEART (Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
$100 in, $120 back two years later, and it can still be a bad deal: net present value.

A worked illustration with round numbers of our own; no company, fund or statistic is claimed. Assumptions, said or
on screen: the same money could earn 10% a year elsewhere at the same risk (the discount rate), compounded yearly; one
payment back at the end of year 2; no tax, no fees.

Every number, worked:
    The deal:        pay $100 today, get $120 back at the end of year 2.
    Other option:    $100 x 1.1 = $110 after one year; $110 x 1.1 = $121 after two (year 2 earns 10% of $110 = $11,
                     $1 more than year 1's $10: interest on the interest).
    Verdict:         $120 against $121: the deal leaves you $1 behind.
    Today's money:   120 / 1.1 = 109.0909 (shown $109.09); 109.0909 / 1.1 = 99.1736 (shown $99.17); 120 / 1.21 = 99.17.
    NPV:             99.17 - 100 = -0.83 (negative). Net present value = value today of what comes back - cost today.
    Close (asked):   the $120 after one year: 120 / 1.1 = 109.09, NPV +9.09, a good deal (not given).
    Comment bonus:   $120 in two years when the other option earns 8%: 120 / 1.08^2 = 120 / 1.1664 = 102.88,
                     NPV +2.88, a good deal.

23 Nov, from the performance data (docs/daily/quality-log.md row of 23 Nov): the paradox opening on the story engine
(two facts that seem to clash, then the question), 12 words on screen; Format C, last used 19 Nov.

    python3 build/reels_npv-120.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "$100", GOLD, 150), (770, 560, "10%", "#3B3F48", 140),
                                              (-100, 1030, "2 YRS", "#0F766E", 160), (770, 1120, "$120", GOLD, 150)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-npv-120",
    kicker="IB CONCEPT",
    mood="curious",
    cover=dict(at=("e", 0, 2, .3), lines=["$100 in.", "$120 back two years later.", "Can that be a bad deal?"],
               hl={"$100": GOLD, "$120": GOLD, "bad": RED, "deal?": RED}, avoid=["$121", "$99.17", "NPV", "BEHIND"]),
    beats=[
        dict(tag="THE PUZZLE", size=62, hold=.6, hl=["$100", "$120", "bad"],
             say=[("A hundred dollars in.", "$100 in."), ("A hundred and twenty back, two years later.", "$120 back, two years later."),
                  ("Can that still be a bad deal?", "Can that still be a bad deal?")],
             art=lambda t0, d, seg: picture("nv_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "thump", .07), (("s", 1, .0), "tick", .04), (("s", 1, .25), "tick", .04), (("s", 1, .5), "pop", .05),
                  (("s", 2, .25), "pop", .05), (("s", 2, .45), "pop", .05)]),
        dict(tag="THE OTHER OPTION", size=56, hl=["10%", "risk.", "$110."],
             say=[("Say your money could earn ten percent a year elsewhere, at the same risk.",
                   "Say your money could earn 10% a year elsewhere, at the same risk."),
                  ("After one year, that's a hundred and ten.", "After one year, that's $110.")],
             art=lambda t0, d, seg: picture("nv_alt", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "pop", .05), (("s", 0, .4), "pop", .05), (("s", 1, .1), "tick", .04), (("s", 1, .55), "clink", .05)]),
        dict(tag="YEAR TWO", size=56, hl=["$110,", "$11.", "$121."],
             say=[("In year two, you earn ten percent of a hundred and ten, which is eleven dollars.",
                   "In year two, you earn 10% of $110, which is $11."),
                  ("That's a hundred and twenty one.", "That's $121.")],
             art=lambda t0, d, seg: picture("nv_year2", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .4), "pop", .05), (("s", 0, .8), "clink", .05), (("s", 1, .35), "thump", .07)]),
        dict(tag="THE VERDICT", size=56, hl=["$120", "$121.", "$1"],
             say=[("So it's a hundred and twenty against a hundred and twenty one.",
                   "So it's $120 against $121."),
                  ("You'd be a dollar behind.", "You'd be $1 behind.")],
             art=lambda t0, d, seg: picture("nv_verdict", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "tick", .04), (("s", 0, .7), "tick", .04), (("s", 1, .1), "pop", .05), (("s", 1, .5), "thump", .07)]),
        dict(tag="BACK TO TODAY", size=54, hl=["today?", "1.1,", "$99.17."],
             say=[("Bankers flip it: what's the hundred and twenty worth today?",
                   "Bankers flip it: what's the $120 worth today?"),
                  ("Divide it by one point one, twice, and you get about ninety nine dollars and seventeen cents.",
                   "Divide it by 1.1, twice, and you get about $99.17.")],
             art=lambda t0, d, seg: picture("nv_today", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .6), "pop", .05), (("s", 1, .12), "pop", .05), (("s", 1, .5), "pop", .05), (("e", 1, .2), "tick", .04)]),
        dict(tag="THE RULE", size=54, hl=["negative.", "enough.", "beat"],
             say=[("Pay a hundred for it, and the net present value is negative.",
                   "Pay $100 for it, and the net present value is negative."),
                  ("Getting more back isn't enough.", "Getting more back isn't enough."),
                  ("It has to beat your other option.", "It has to beat your other option.")],
             art=lambda t0, d, seg: picture("nv_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "pop", .05), (("s", 0, .25), "pop", .05), (("s", 0, .65), "tick", .04), (("s", 0, .95), "thump", .07),
                  (("s", 1, .3), "pop", .05), (("s", 2, .5), "thump", .06)]),
    ],
    close=dict(say=[("Now the hundred and twenty comes back after one year.", "Now the $120 comes back after one year."),
                    ("Good deal or bad?", "Good deal or bad?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED}, bar=True, art_w=720, art_h=576,
               pic=lambda t0, d: picture("nv_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",        # the grid cover (reel_cover.py) on the Reel's own ground
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
