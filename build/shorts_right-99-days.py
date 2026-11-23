"""
YouTube Short, Format C (one surprising concept, built up as a calculation), 23 Nov 2026, on the story engine
(build/story.py), narrator HEART (Kokoro af_heart, en-us, 0.9), black ground. Cut from YouTube #15 (22 Nov, "One
Trader Lost £827 Million. His Bank Had About £350 Million.", build/youtube_ep015.py): the film's own puzzle, its
selling-insurance example (£1 a day, 99 calm days, a £150 payout on day 100: build/plans/ep015_checks.py, labelled
in the film as ours), told here as the puzzle itself.

The puzzle: you're right 99 days out of 100, and you still lose money. How? Arithmetic, true in any country and any
currency (the film's pounds kept so the Short matches it). Our example, checked in this run (the lines below and
python3 build/plans/ep015_checks.py):
    You sell insurance against a big market move and collect £1 on each calm day.
    99 calm days: 99 x £1 = +£99.
    Day 100, the market jumps: you pay out £150.
    99 wins, 1 loss: 99 - 150 = -£51. Right 99% of the days (99 / 100), down £51.
    The rule (our reading of the arithmetic): how often you win is not enough; what you lose when you're wrong
        decides it. Here the loss is 150 times the daily win (150 / 1).
    "Selling options can work like this" is a general description of an option seller (a premium collected up front,
        a large payment if the market moves a lot); it is said as "can", and no figure rests on it.
    The close (not answered on screen): win £1 on 90 days out of 100 and lose £10 on the other 10:
        90 x 1 - 10 x 10 = 90 - 100 = -£10 (behind).

Sources. The puzzle is our own arithmetic and needs none. The film's Barings figures (Hansard 18 Jul 1995; Reserve
Bank of Australia Bulletin, Nov 1995; NLB Infopedia) are NOT used on screen, in the voice or in the description:
planned that way from the start (the 22 Nov next improvement), because this unattended run asked to re-open the three
pages first and the fetch permission was not answered. Barings is named only as the subject of our full film, a
pointer, not a claim.

Beats (as said):
    puzzle   right 99 days of 100, still lose money; how? Question first, no setup.
    bet      our own example: you sell insurance against a big move; every calm day you collect £1.
    calm     99 calm days, up £99.
    jump     day 100 the market jumps; you pay out £150.
    answer   99 wins and one loss; down £51.
    rule     how often you win isn't enough; what counts is how much you lose when you're wrong; selling options
             can work like this.
    close    win £1 on 90 days, lose £10 on the other 10: ahead or behind? (not answered). The film is the Related video.

    python3 build/shorts_right-99-days.py HEART
"""

import random
import sys

from motion import A
from sketch import picture, _ptag, rd_hook_steps
from story import make, RED

TEAL_INK, GOLD = "#5EC8B4", "#F2C35B"


def chip(label, fill, w=190, color="#fff"):
    return (f'<svg width="{w}" height="{w * .6:.0f}" viewBox="0 0 {w} {w * .6:.0f}" style="overflow:visible">'
            + _ptag(w / 2, w * .3, w * .95, label, fill, color, round(w * .2)) + "</svg>")


def floaters(total):
    """Faint tags drifting at the edges, clear of the text (never the answer, -£51, nor the close's)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "99%", "#0F766E", 170), (770, 560, "DAY 100", RED, 180),
                                              (-100, 1030, "£1", "#3B3F48", 150), (770, 1120, "?", GOLD, 120)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


def rain(t0, dur):
    """Tags falling in under the comment ask, then bobbing (no answer)."""
    rnd = random.Random(23)
    out = ""
    labs = [("+£1", "#0F766E"), ("90", "#3B3F48"), ("-£10", RED), ("10", "#3B3F48"), ("?", GOLD)]
    for k, (lab, fill) in enumerate(labs):
        x, y = rnd.uniform(-10 + 150 * k, 10 + 150 * k), rnd.uniform(1040, 1120)
        art = chip(lab, fill, rnd.uniform(130, 160), "#0A0A0A" if fill == GOLD else "#fff")
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px")
    return out


F = lambda j, f: (lambda s: s[j][0] + f * (s[j][1] - s[j][0]))       # a moment f of the way through sentence j
STEPS = lambda j, a, b, n=10: [(lambda s, i=i: s[j][0] + (a + (b - a) * i / (n - 1)) * (s[j][1] - s[j][0])) for i in range(n)]

# the hook: a tick per row of calm days, the red day (thump), the bar falling (knock), the ? (pop)
HOOK_SFX = ([((lambda seg, i=i: rd_hook_steps(seg)[i] + .05), "tick", .035) for i in range(10)]
            + [((lambda s: F(1, .1)(s)), "thump", .09),
               ((lambda s: F(1, .1)(s) + .35), "knock", .05),
               ((lambda s: F(2, .05)(s)), "pop", .06)])

EP = dict(
    slug="shorts-right-99-days",
    kicker="MONEY MATHS",
    mood="tense",
    cover=dict(at=("e", 0, 1, .3), lines=["Right 99 days out of 100.", "Still losing money.", "How?"],
               hl={"99": TEAL_INK, "100.": TEAL_INK, "losing": RED, "How?": RED}, avoid=["51", "150"]),
    beats=[
        dict(tag="THE PUZZLE", size=64, hold=.5, art_h=560, hl=["right 99 days", "out of 100.", "lose money.", "How?"],
             say=[("You're right ninety nine days out of a hundred.", "You're right 99 days out of 100."),
                  ("And you still lose money.", "And you still lose money."),
                  ("How?", "How?")],
             art=lambda t0, d, seg: picture("rd_hook", t0, d, seg=seg, w=752, h=560),
             sfx=HOOK_SFX),
        dict(tag="OUR EXAMPLE", size=56, art_h=540, hl=["sell insurance", "big market move,", "£1."],
             say=[("Here's our own example.", "Here's our own example."),
                  ("You sell insurance against a big market move, and every calm day, you collect one pound.",
                   "You sell insurance against a big market move, and every calm day, you collect £1.")],
             art=lambda t0, d, seg: picture("rd_bet", t0, d, seg=seg, w=752, h=540),
             sfx=[((lambda s: F(0, .2)(s) + .05), "thump", .07)]
                 + [((lambda s, i=i: s[1][0] + (.03 + .87 * (i + .6) / 9) * (s[1][1] - s[1][0]) + .25), "clink", .03) for i in range(9)]),
        dict(tag="99 CALM DAYS", size=62, art_h=560, hl=["99 calm days,", "up £99."],
             say=[("Ninety nine calm days, and you're up ninety nine pounds.", "99 calm days, and you're up £99.")],
             art=lambda t0, d, seg: picture("rd_calm", t0, d, seg=seg, w=752, h=560),
             sfx=[((lambda s, f=f: f(s) + .45), "clink", .03) for f in STEPS(0, .03, .7, 11)]
                 + [((lambda s: F(0, .8)(s)), "thump", .08)]),
        dict(tag="DAY 100", size=62, art_h=560, hl=["day 100,", "jumps.", "£150."],
             say=[("Then on day one hundred, the market jumps.", "Then on day 100, the market jumps."),
                  ("You pay out a hundred and fifty pounds.", "You pay out £150.")],
             art=lambda t0, d, seg: picture("rd_jump", t0, d, seg=seg, w=752, h=560),
             sfx=[((lambda s: F(0, .25)(s) + .05), "paper", .05),
                  ((lambda s: F(0, .6)(s) + .3), "thump", .1)]
                 + [((lambda s, f=f: f(s)), "tick", .03) for f in STEPS(1, .05, .85, 8)]),
        dict(tag="THE ANSWER", size=62, art_h=560, hl=["99 wins", "one loss.", "down £51."],
             say=[("Ninety nine wins, and one loss.", "99 wins, and one loss."),
                  ("And you're down fifty one pounds.", "And you're down £51.")],
             art=lambda t0, d, seg: picture("rd_answer", t0, d, seg=seg, w=752, h=560),
             sfx=[((lambda s, f=f: f(s) + .2), "tick", .03) for f in STEPS(0, .03, .62, 6)]
                 + [((lambda s: F(0, .7)(s) + .4), "thump", .1),
                    ((lambda s: F(1, .15)(s) + .5), "knock", .05),
                    ((lambda s: F(1, .75)(s) + .1), "thump", .1)]),
        dict(tag="THE RULE", size=52, art_h=470, hold=.9, hl=["isn't enough.", "how much you lose", "Selling options"],
             say=[("How often you win isn't enough.", "How often you win isn't enough."),
                  ("What counts is how much you lose when you're wrong.", "What counts is how much you lose when you're wrong."),
                  ("Selling options can work just like this.", "Selling options can work just like this.")],
             art=lambda t0, d, seg: picture("rd_rule", t0, d, seg=seg, w=752, h=470),
             sfx=[((lambda s: F(0, .8)(s) + .1), "thump", .08),
                  ((lambda s: F(1, .05)(s) + .1), "clink", .04),
                  ((lambda s: F(1, .85)(s) + .3), "pop", .05),
                  ((lambda s: F(2, .9)(s) - .2), "knock", .06)]),
    ],
    close=dict(say=[("Win a pound on ninety days out of a hundred, and lose ten pounds on the other ten.",
                     "Win £1 on 90 days out of 100, and lose £10 on the other 10."),
                    ("Ahead, or behind?", "Ahead, or behind?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED}, art=rain,
               pic=lambda t0, d: picture("rd_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean mix is the score gate's reference; the delivered file is the scored one (17 Nov)
    lufs=-14,
    room=.0003,
)

if __name__ == "__main__":
    if "remix" in sys.argv:
        from story import remix
        remix(EP, "HEART")
    else:
        make(EP, *(sys.argv[1:2] or ["HEART"]))
