"""
YouTube Short, Format D (an animated calculation), 24 Nov 2026, on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground. Cut from YouTube #16 (23 Nov, "$27 Billion of Enron Was Off the Books.
Its Board Saw the Chart.", build/youtube_ep016.py): the film's own puzzle, a hedge paid in your own shares ($100
investment, $100 of the company's own shares, falls to $60 and 70%), labelled in the film as ours, not Enron's real
figures, told here as the puzzle itself.

The puzzle: your $100 investment is insured against any fall, but the insurer's only money is $100 of your own shares.
Are you safe? Arithmetic, true in any country and any currency. Our example, checked in this run
(python3 build/plans/shorts_hedge_checks.py):
    Your investment: $100. A partner promises to cover any fall; all it owns is $100 of your own shares.
    The investment falls to $60: the partner owes 100 - 60 = $40, and it has $100: covered.
    Your shares fall 70%: the partner's $100 is worth 100 x 0.3 = $30.
    It owes $40 and has $30: 40 - 30 = $10 short. It can't pay, and the $30 it has is your own stock.
    The rule (our reading of the arithmetic): a hedge is only as good as the money behind it; if that money falls
        when you fall, you're not hedged.
    The close (not answered on screen): how far can your shares fall before the partner can't pay? 100 x (1 - x) = 40
        at x = 60%, so any fall of more than 60%. The close's column stops at -50% ($50, still enough) and the break
        point is neither drawn nor said.

Sources. The puzzle is our own arithmetic and needs none. The film's Enron sources (the Senate PSI report, the Powers
report, Enron's Form 8-K of 8 Nov 2001) are NOT used on screen, in the voice or in the description: this unattended
run asked to re-open the three pages before writing (short-form-standard section 1, item 4) and each fetch came back
"permission request not answered", so the Short was planned without any Enron figure or quote from the start. Enron
is named only as the subject of our full film, a pointer, not a claim.

Hooks considered (Pietro's 24 Nov hook standard is for Reels; used here as a check, a number in the first words):
    1 "Your $100 investment is insured against any fall. But your insurer's only money is $100 of your own shares.
       Are you safe?"  (chosen: the clash on screen from frame 0, a number in the first three words)
    2 "A hedge paid in your own shares. Does it hold?"  (no number)
    3 "Insured for $100. Paid $0. How?"  (overstates: the partner has $30)
    4 "Your insurer owns only your stock. Your stock falls 70%."  (gives the twist away)
    5 "Can a hedge make you less safe?"  (vague)

Beats (as said):
    puzzle   your $100 investment insured against any fall; the insurer's only money is $100 of your own shares; safe?
    fall     our own numbers: the investment falls to $60; the partner owes $40, has $100: covered.
    twist    your own shares fall too, by 70%; the partner's $100 is now worth $30.
    answer   it owes $40 and has $30; it can't pay; and the $30 is your own stock.
    rule     a hedge is only as good as the money behind it; if that money falls when you fall, you're not hedged at
             all; the full story is in our film on Enron.
    close    how far can your shares fall before the partner can't pay? (not answered). The film is the Related video.

    python3 build/shorts_hedge-own-shares.py HEART
"""

import random
import sys

from motion import A
from sketch import picture, _ptag, hg_hook_steps
from story import make, RED

TEAL_INK, GOLD, SHARE = "#5EC8B4", "#F2C35B", "#A9C2DF"


def chip(label, fill, w=190, color="#fff"):
    return (f'<svg width="{w}" height="{w * .6:.0f}" viewBox="0 0 {w} {w * .6:.0f}" style="overflow:visible">'
            + _ptag(w / 2, w * .3, w * .95, label, fill, color, round(w * .2)) + "</svg>")


def floaters(total):
    """Faint tags drifting at the edges, clear of the text (never the answer, $30 or $10 short, nor the close's)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "$100", "#0F766E", 170), (770, 560, "HEDGE", "#2E4F7A", 180),
                                              (-100, 1030, "IOU", "#3B3F48", 150), (770, 1120, "?", GOLD, 120)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


def rain(t0, dur):
    """Tags falling in under the comment ask, then bobbing (no answer)."""
    rnd = random.Random(24)
    out = ""
    labs = [("-10%", RED), ("-30%", RED), ("$40", "#3B3F48"), ("-50%", RED), ("?", GOLD)]
    for k, (lab, fill) in enumerate(labs):
        x, y = rnd.uniform(-10 + 150 * k, 10 + 150 * k), rnd.uniform(1150, 1190)   # 24 Nov: under the comment bar
        art = chip(lab, fill, rnd.uniform(130, 160), "#0A0A0A" if fill == GOLD else "#fff")
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px")
    return out


F = lambda j, f: (lambda s: s[j][0] + f * (s[j][1] - s[j][0]))       # a moment f of the way through sentence j
STEPS = lambda j, a, b, n=10: [(lambda s, i=i: s[j][0] + (a + (b - a) * i / (n - 1)) * (s[j][1] - s[j][0])) for i in range(n)]

# the hook: a clink per cash slice, a tick per share slice, the shield (thump), the ? (pop)
HOOK_SFX = ([((lambda seg, i=i: hg_hook_steps(seg)[0][i] + .05), "clink", .03) for i in range(10)]
            + [((lambda s: F(0, .72)(s)), "thump", .08)]
            + [((lambda seg, i=i: hg_hook_steps(seg)[1][i] + .05), "tick", .03) for i in range(10)]
            + [((lambda s: F(2, .05)(s)), "pop", .06)])

EP = dict(
    slug="shorts-hedge-own-shares",
    kicker="MONEY MATHS",
    mood="tense",
    cover=dict(at=("e", 0, 1, .4), lines=["Insured by $100", "of your own shares.", "Are you safe?"],
               hl={"$100": TEAL_INK, "own": RED, "shares.": RED, "safe?": RED}, avoid=["30", "CAN'T", "SHORT", "60"]),
    beats=[
        dict(tag="THE PUZZLE", size=60, hold=.5, art_h=560, hl=["$100 investment", "any fall.", "your own shares.", "safe?"],
             say=[("Your hundred dollar investment is insured against any fall.", "Your $100 investment is insured against any fall."),
                  ("But your insurer's only money is a hundred dollars of your own shares.", "But your insurer's only money is $100 of your own shares."),
                  ("Are you safe?", "Are you safe?")],
             art=lambda t0, d, seg: picture("hg_hook", t0, d, seg=seg, w=752, h=560),
             sfx=HOOK_SFX),
        dict(tag="OUR EXAMPLE", size=56, art_h=540, hl=["falls to $60.", "owes you $40,", "covered."],
             say=[("Here are our own numbers.", "Here are our own numbers."),
                  ("Your investment falls to sixty dollars.", "Your investment falls to $60."),
                  ("The partner owes you forty, and it has a hundred, so you're covered.",
                   "The partner owes you $40, and it has $100, so you're covered.")],
             art=lambda t0, d, seg: picture("hg_fall", t0, d, seg=seg, w=752, h=540),
             sfx=[((lambda s: F(0, .2)(s) + .05), "thump", .07)]
                 + [((lambda s, f=f: f(s)), "knock", .04) for f in STEPS(1, .1, .8, 4)]
                 + [((lambda s: F(2, .05)(s)), "paper", .05),
                    ((lambda s: F(2, .7)(s) + .1), "clink", .04),
                    ((lambda s: F(2, .85)(s)), "thump", .08)]),
        dict(tag="THE TWIST", size=62, art_h=560, hl=["shares fall too,", "70%.", "$30."],
             say=[("Now your own shares fall too, by seventy percent.", "Now your own shares fall too, by 70%."),
                  ("The partner's hundred dollars is now worth thirty.", "The partner's $100 is now worth $30.")],
             art=lambda t0, d, seg: picture("hg_twist", t0, d, seg=seg, w=752, h=560),
             sfx=[((lambda s, f=f: f(s)), "tick", .03) for f in STEPS(0, .2, .9, 7)]
                 + [((lambda s, f=f: f(s)), "knock", .035) for f in STEPS(1, .1, .8, 7)]
                 + [((lambda s: F(1, .88)(s)), "thump", .09)]),
        dict(tag="THE ANSWER", size=62, art_h=560, hl=["owes you $40,", "has $30.", "can't pay.", "your own stock."],
             say=[("It owes you forty, and it has thirty.", "It owes you $40, and it has $30."),
                  ("It can't pay.", "It can't pay."),
                  ("And the thirty it does have is your own stock.", "And the $30 it does have is your own stock.")],
             art=lambda t0, d, seg: picture("hg_answer", t0, d, seg=seg, w=752, h=560),
             sfx=[((lambda s, f=f: f(s)), "tick", .03) for f in STEPS(0, .05, .85, 4)]
                 + [((lambda s: F(1, .45)(s)), "thump", .1),
                    ((lambda s: F(2, .1)(s)), "paper", .05)]
                 + [((lambda s, j=j: F(2, .1 + .75 * (.35 + .3 * j))(s)), "knock", .045) for j in range(3)]),
        dict(tag="THE RULE", size=54, art_h=500, hold=.9, hl=["only as good", "money behind it.", "not hedged", "film on Enron."],
             say=[("A hedge is only as good as the money behind it.", "A hedge is only as good as the money behind it."),
                  ("If that money falls when you fall, you're not hedged at all.", "If that money falls when you fall, you're not hedged at all."),
                  ("The full story is in our film on Enron.", "The full story is in our film on Enron.")],
             art=lambda t0, d, seg: picture("hg_rule", t0, d, seg=seg, w=752, h=500),
             sfx=[((lambda s, f=f: f(s) + .1), "clink", .03) for f in STEPS(0, .05, .8, 5)]
                 + [((lambda s: F(1, .9)(s)), "thump", .09),
                    ((lambda s: F(2, .2)(s)), "pop", .05)]),
    ],
    close=dict(say=[("How far can your shares fall, before the partner can't pay?",
                     "How far can your shares fall before the partner can't pay?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               size=64, bar=True, art_w=700, art_h=560,
               cols={"comments.": RED}, art=rain,
               pic=lambda t0, d: picture("hg_asks", t0, d, w=700, h=560)),
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
