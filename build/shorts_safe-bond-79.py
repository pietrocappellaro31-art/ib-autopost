"""
YouTube Short, Format D (an animated calculation), 22 Nov 2026, on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground. Cut from YouTube #14 (20 Nov, "$40 Billion Left This Bank in One Day.
It Was Full of Safe Bonds.", build/youtube_ep014.py): the film's own puzzle (its $100, 10-year, 1.5% bond, priced at
4%: $79.72, build/plans/ep014_checks.py), told here a new way: the yearly shortfall against a new bond, in today's
money.

The puzzle: a safe $100 bond pays 1.5% a year for ten years. New bonds start paying 4%. What is yours worth now?
Arithmetic of discounting, true in any country and any currency. Our example (annual coupons, no default, the buyer
wants what a new bond pays), checked in this run (python3 build/plans/ep014_checks.py and the lines below):
    It still pays $1.50 a year for 10 years and $100 at the end: $115 in all (no default).
    A new $100 bond pays $4.00 a year. Yours pays $2.50 less, every year, for 10 years: 10 x 2.50 = $25.
    Money that comes later is worth less today (at 4%): year 1's $2.50 is 2.50 / 1.04 = $2.40, year 10's
        2.50 / 1.04^10 = $1.69; all ten: 2.50 x (1 - 1.04^-10) / 0.04 = $20.28 ("about twenty dollars").
    So the price is 100 - 20.28 = $79.72, the same as discounting its own payments at 4%
        (1.50 x 8.1109 + 100 / 1.04^10 = 12.17 + 67.56 = 79.72): at that price it earns 4% a year, like a new bond.
    About a fifth of its value (20.3%) is gone, with no default.
    The rule (our reading of the arithmetic): rates up, prices down, even on a bond that is safe.
    The close (not answered on screen): new bonds at 1%: more than $100 ($104.74).

Sources. The puzzle is our own arithmetic and needs none. The film's SVB figures (10-K: HTM securities $91.3bn at
cost, $76.2bn fair value; Fed review: over $40bn of deposits out on 9 March 2023) are NOT used on screen or in the
description today: this run could not open the pages again (the fetch permission was not answered in an unattended
run; two searches returned the pages' titles and URLs only, which does not confirm a figure). The Short names the
bank only as the subject of our full film, a pointer, not a claim.

Beats (as said):
    puzzle   $100 bond, 1.5% a year for ten years; new bonds pay 4%; what's yours worth now? Question first.
    safe     it can't default (our example): $1.50 a year and the $100 back.
    gap      a new bond pays $4 a year; yours pays $2.50 less, every year, for ten years.
    today    $25 spread over ten years; worth about $20 today (the later, the less).
    answer   nobody pays $100; $79.72; at that price it earns 4%, like a new bond.
    rule     rates up, prices down, even on a safe bond.
    close    new bonds at 1%: more or less than $100? (not answered). The film is the Related video.

    python3 build/shorts_safe-bond-79.py HEART
"""

import random
import sys

from motion import A
from sketch import picture, _ptag, sb_hook_steps
from story import make, RED

TEAL_INK, GOLD, BLUE = "#5EC8B4", "#F2C35B", "#A9C2DF"


def chip(label, fill, w=190, color="#fff"):
    return (f'<svg width="{w}" height="{w * .6:.0f}" viewBox="0 0 {w} {w * .6:.0f}" style="overflow:visible">'
            + _ptag(w / 2, w * .3, w * .95, label, fill, color, round(w * .2)) + "</svg>")


def floaters(total):
    """Faint tags drifting at the edges, clear of the text (never the hook's answer, $79.72, nor the close's)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "BOND", "#3B3F48", 170), (770, 560, "4%", RED, 150),
                                              (-100, 1030, "1.5%", "#2E4F7A", 170), (770, 1120, "?", GOLD, 120)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


def rain(t0, dur):
    """Tags falling in under the comment ask, then bobbing (no answer)."""
    rnd = random.Random(22)
    out = ""
    labs = [("1%", RED), ("BOND", "#3B3F48"), ("$100", GOLD), ("RATES", "#2E4F7A"), ("?", "#0F766E")]
    for k, (lab, fill) in enumerate(labs):
        x, y = rnd.uniform(-10 + 150 * k, 10 + 150 * k), rnd.uniform(1040, 1120)
        art = chip(lab, fill, rnd.uniform(130, 160), "#0A0A0A" if fill == GOLD else "#fff")
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px")
    return out


F = lambda j, f: (lambda s: s[j][0] + f * (s[j][1] - s[j][0]))       # a moment f of the way through sentence j
STEPS = lambda j, a, b, n=10: [(lambda s, i=i: s[j][0] + (a + (b - a) * i / (n - 1)) * (s[j][1] - s[j][0])) for i in range(n)]

# the hook: a coin on each year (clink), the $100 lands (thump), the gauge climbs (ticks), the $ ? (pop)
HOOK_SFX = ([((lambda seg, i=i: sb_hook_steps(seg)[i] + .25), "clink", .035) for i in range(10)]
            + [((lambda seg: sb_hook_steps(seg)[9] + .6), "thump", .08)]
            + [((lambda s, i=i: s[1][0] + (.05 + .85 * i / 4) * (s[1][1] - s[1][0])), "tick", .035) for i in range(5)]
            + [((lambda s: F(2, .1)(s) + .05), "pop", .06)])

EP = dict(
    slug="shorts-safe-bond-79",
    kicker="MONEY MATHS",
    mood="tense",
    cover=dict(at=("e", 0, 2, .2), lines=["A safe $100 bond pays 1.5%.", "New bonds pay 4%.", "What's yours worth?"],
               hl={"$100": TEAL_INK, "1.5%": TEAL_INK, "4%.": RED, "worth?": RED}, avoid=["79", "20.28", "$25"]),
    beats=[
        dict(tag="THE PUZZLE", size=60, hold=.45, art_h=560, hl=["$100 bond", "1.5%", "4%.", "worth now?"],
             say=[("A safe hundred dollar bond pays one and a half percent a year, for ten years.",
                   "A safe $100 bond pays 1.5% a year, for ten years."),
                  ("Then new bonds start paying four percent.", "Then new bonds start paying 4%."),
                  ("What's yours worth now?", "What's yours worth now?")],
             art=lambda t0, d, seg: picture("sb_hook", t0, d, seg=seg, w=752, h=560),
             sfx=HOOK_SFX),
        dict(tag="IT'S SAFE", size=60, art_h=560, hl=["can't default.", "$1.50 a year,", "$100 back."],
             say=[("It can't default.", "It can't default."),
                  ("You still get a dollar fifty a year, and your hundred back.",
                   "You still get $1.50 a year, and your $100 back.")],
             art=lambda t0, d, seg: picture("sb_safe", t0, d, seg=seg, w=752, h=560),
             sfx=[((lambda s: F(0, .2)(s) + .35), "thump", .08)]
                 + [((lambda s, f=f: f(s) + .55), "clink", .03) for f in STEPS(1, .05, .75)]
                 + [((lambda s: F(1, .8)(s) + .45), "thump", .08)]),
        dict(tag="THE GAP", size=56, art_h=520, hl=["$4 a year.", "$2.50 less,", "ten years."],
             say=[("But a new bond pays four dollars a year.", "But a new bond pays $4 a year."),
                  ("Yours pays two fifty less, every year, for ten years.",
                   "Yours pays $2.50 less, every year, for ten years.")],
             art=lambda t0, d, seg: picture("sb_gap", t0, d, seg=seg, w=752, h=520),
             sfx=[((lambda s: F(0, .1)(s) + .4), "paper", .05)]
                 + [((lambda s, f=f: f(s) + .45), "knock", .04) for f in STEPS(1, .05, .85)]),
        dict(tag="IN TODAY'S MONEY", size=54, art_h=520, hl=["$25,", "worth less today,", "about $20"],
             say=[("That's twenty five dollars, spread over ten years.", "That's $25, spread over ten years."),
                  ("Money that comes later is worth less today, so the gap is worth about twenty dollars now.",
                   "Money that comes later is worth less today, so the gap is worth about $20 now.")],
             art=lambda t0, d, seg: picture("sb_today", t0, d, seg=seg, w=752, h=520),
             sfx=[((lambda s, f=f: f(s) + .2), "tick", .03) for f in STEPS(0, .05, .8)]
                 + [((lambda s, f=f: f(s) + .3), "tick", .03) for f in STEPS(1, .2, .92)]),
        dict(tag="THE ANSWER", size=56, art_h=560, hl=["a hundred", "$79.72.", "4%,"],
             say=[("So nobody pays a hundred for it.", "So nobody pays a hundred for it."),
                  ("It's worth seventy nine dollars and seventy two cents.", "It's worth $79.72."),
                  ("At that price, it earns four percent, just like a new bond.",
                   "At that price, it earns 4%, just like a new bond.")],
             art=lambda t0, d, seg: picture("sb_answer", t0, d, seg=seg, w=752, h=560),
             sfx=[((lambda s: F(0, .15)(s) + .1), "paper", .05),
                  ((lambda s: F(1, .1)(s) + .5), "paper", .05),
                  ((lambda s: F(1, .7)(s) + .1), "thump", .1)]
                 + [((lambda s, i=i: s[2][0] + (.05 + .65 * i / 10) * (s[2][1] - s[2][0]) + .05), "clink", .025) for i in range(0, 11, 2)]
                 + [((lambda s: F(2, .75)(s) + .05), "pop", .05)]),
        dict(tag="THE RULE", size=64, art_h=600, hold=1.1, hl=["Rates up,", "prices down,", "perfectly safe."],
             say=[("Rates up, prices down, even on a bond that's perfectly safe.",
                   "Rates up, prices down, even on a bond that's perfectly safe.")],
             art=lambda t0, d, seg: picture("sb_rule", t0, d, seg=seg, w=752, h=600),
             sfx=[((lambda s, f=f: f(s)), "tick", .03) for f in STEPS(0, .05, .5, 6)]
                 + [((lambda s: F(0, .62)(s) + .35), "thump", .08)]),
    ],
    close=dict(say=[("If new bonds paid one percent instead, would yours be worth more or less than a hundred?",
                     "If new bonds paid 1% instead, would yours be worth more or less than $100?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED}, art=rain,
               pic=lambda t0, d: picture("sb_asks", t0, d, w=520, h=416)),
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
