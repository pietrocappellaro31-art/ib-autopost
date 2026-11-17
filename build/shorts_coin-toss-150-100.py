"""
YouTube Short, Format F (a choice), 17 Nov 2026, on the story engine (build/story.py), narrator HEART (Kokoro af_heart,
en-us, 0.9), black ground. One coin toss: heads you win $150, tails you lose $100. Do you take it? On average it pays
$25 a toss, yet most people turn it down: to risk $100, most want a chance at about $200 (Kahneman). Paul Samuelson
told of a colleague who refused one toss at $200 to $100 but would take a hundred of them in a row. Over a hundred
such tosses the average total is $5,000 and the chance of ending down is under one in a thousand (our arithmetic).
The close asks the viewer to choose: one toss or a hundred.

Sources (all opened in this run, 17 Nov 2026):
    [1] LitCharts, "Thinking, Fast and Slow, Part 4, Chapter 26" (Daniel Kahneman, 2011).
        https://litcharts.com/lit/thinking-fast-and-slow/part-4-chapter-26
        The gamble: "if a coin shows tails, you lose $100. If a coin shows heads, you win $150." "To balance the
        potential loss of $100, most people require the opportunity to win about $200."
    [2] Paul A. Samuelson, "Risk and Uncertainty: A Fallacy of Large Numbers", Scientia (1963), reprinted by the
        Casualty Actuarial Society. https://www.casact.org/pubs/forum/94sforum/94sf049.pdf
        The colleague was offered a bet at $200 to $100 on a coin; he said "I won't bet because I would feel the $100
        loss more than the $200 gain. But I'll take you on if you promise to let me make 100 such bets."
    [3] Psychology Today, "Can Psychology Solve a Classic Paradox?" (The Decision Tree, June 2011).
        https://www.psychologytoday.com/us/blog/the-decision-tree/201106/can-psychology-solve-classic-paradox
        Samuelson 1963 in Scientia; the colleague "would take the gamble if Samuelson would let him repeat it 100
        times in a row"; over 100 such bets "less than 1% chance of losing money".

Our arithmetic (checked with a short script in this run):
    One toss at +$150 / -$100: 0.5 x 150 - 0.5 x 100 = +$25 on average.
    "About two to one": [1]'s $200 to balance $100 (our reading, drawn as ABOUT 2 TO 1; no ratio is claimed beyond it).
    100 tosses at +$200 / -$100 with W wins: total = 200 W - 100 (100 - W) = 300 W - 10,000. Average W = 50, so the
    average total is $5,000 (= 100 x $50). Down only if W <= 33: P = sum C(100,k)/2^100, k = 0..33 = 0.000437
    (0.044%), "under one in a thousand", drawn "< 0.1%" (consistent with [3]'s "less than 1%"). The chart in beat 5
    shows the exact binomial chance of each W from 28 to 72 (totals -$1,600 to $11,600); the rest are under one
    pixel. Fair coin assumed throughout, as in [1] and [2].

Beats, checked:
    hook     the gamble [1].
    average  +$25 a toss (our arithmetic).
    no       most people want about $200 to risk $100 [1].
    lunch    Samuelson's colleague: one toss at $200 to $100, no; a hundred, yes [2][3]. Drawn as an illustrated
             RECONSTRUCTION: a plain stick figure labelled SAMUELSON, the trader as the colleague; no likeness, no
             invented words (the bubble shows x1 NO and x100 YES, his choice, not a quote).
    hundred  average $5,000, chance of ending down under 1 in 1,000 (our arithmetic on [2]'s terms).
    close    the viewer's choice. No advice: nothing here says anyone should take any bet.

    python3 build/shorts_coin-toss-150-100.py HEART
"""

import random
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
    """Faint stake tags drifting at the edges, clear of the text (never the answer, +$25: it would show on the cover)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "+$150", "#0F766E", 200), (770, 560, "−$100", RED, 190),
                                              (-100, 1030, "×100", GOLD, 180), (770, 1120, "×1", "#0F766E", 150)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


def rain(t0, dur):
    """Tags falling in under the comment ask, then bobbing."""
    rnd = random.Random(17)
    out = ""
    labs = [("×1", "#0F766E"), ("+$150", "#0F766E"), ("×100", GOLD), ("−$100", RED), ("+$25", "#0F766E")]
    for k, (lab, fill) in enumerate(labs):
        x, y = rnd.uniform(-10 + 150 * k, 10 + 150 * k), rnd.uniform(1040, 1120)
        art = chip(lab, fill, rnd.uniform(130, 160), "#0A0A0A" if fill == GOLD else "#fff")
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px")
    return out


EP = dict(
    slug="shorts-coin-toss-150-100",
    kicker="MONEY CHOICES",
    mood="curious",
    # 17 Nov (the 16 Nov next improvement): the cover is the hook's frame after YES? NO? have landed, its captions
    # hidden and the question alone laid over them; the answer (+$25, AVERAGE) must not be in the frame.
    cover=dict(at=("e", 0, 2, .5), lines=["Heads: win $150.", "Tails: lose $100.", "Do you take it?"],
               hl={"$150": TEAL_INK, "$100": RED, "take it?": RED}, avoid=["$25", "AVERAGE", "+$25"]),
    beats=[
        dict(tag="ONE COIN TOSS", size=66, hold=.75, hl=["win $150.", "lose $100."],
             say=[("Heads, you win a hundred and fifty dollars.", "Heads, you win $150."),
                  ("Tails, you lose a hundred.", "Tails, you lose $100."),
                  ("Do you take it?", "Do you take it?")],
             art=lambda t0, d, seg: picture("toss_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .05), "tick", .05), (("s", 0, 1.0), "clink", .09), (("s", 1, .05), "tick", .05),
                  (("s", 1, 1.0), "clink", .09), (("s", 2, .15), "pop", .07), (("s", 2, .35), "pop", .07)]),
        dict(tag="THE AVERAGE", hl=["$25"],
             say=[("Half the time you win a hundred and fifty, half the time you lose a hundred.",
                   "Half the time you win $150, half the time you lose $100."),
                  ("On average, that's twenty five dollars a toss.", "On average, that's $25 a toss.")],
             art=lambda t0, d, seg: picture("bet_average", t0, d, seg=seg, **PIC),
             sfx=[(("s", 1, .4), "paper", .07), (("s", 1, .95), "paper", .07)]),
        dict(tag="MOST SAY NO", hl=["say no.", "about $200."],
             say=[("Most people still say no.", "Most people still say no."),
                  ("To risk a hundred, they want a shot at about two hundred.", "To risk $100, they want a shot at about $200.")],
             art=lambda t0, d, seg: picture("loss_scale", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, 1.05), "thump", .14), (("s", 1, .3), "clink", .06)]),
        dict(tag="ONE OR A HUNDRED", badge="RECONSTRUCTION", hl=["no.", "a hundred tosses"],
             say=[("The economist Paul Samuelson offered a colleague one toss: win two hundred, lose a hundred.",
                   "The economist Paul Samuelson offered a colleague one toss: win $200, lose $100."),
                  ("He said no.", "He said no."),
                  ("But he'd take a hundred tosses in a row.", "But he'd take a hundred tosses in a row.")],
             art=lambda t0, d, seg: picture("lunch_bet", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .45), "paper", .08), (("s", 1, .05), "pop", .07), (("s", 2, .2), "pop", .07)]
             + [(("s", 2, .8 + .1 * j), "clink", .045) for j in range(7)]),
        dict(tag="A HUNDRED TOSSES", hl=["$5,000.", "under 1 in 1,000."],
             say=[("Over a hundred tosses, the average total is five thousand dollars.",
                   "Over a hundred tosses, the average total is $5,000."),
                  ("And the chance of ending down is under one in a thousand.",
                   "And the chance of ending down is under 1 in 1,000.")],
             art=lambda t0, d, seg: picture("hundred_tosses", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2 + .35 * j), "tick", .035) for j in range(7)] + [(("s", 1, .25), "paper", .06)]),
    ],
    close=dict(say=[("One toss or a hundred: which would you take?", "One toss or a hundred: which would you take?"),
                    ("Tell me in the comments.", "Tell me in the comments."),
                    ("And subscribe for more like this.", "And subscribe for more like this.")],
               cols={"comments.": RED}, art=rain,
               pic=lambda t0, d: picture("toss_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean mix is the score gate's reference; the delivered file is the scored one (17 Nov)
    lufs=-14,
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
