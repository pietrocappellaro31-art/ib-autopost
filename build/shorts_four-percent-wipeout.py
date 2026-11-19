"""
YouTube Short, Format D (an animated calculation), 19 Nov 2026, on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground. Cut from YouTube #12 (18 Nov, "Two Nobel Winners Ran This Fund. It Lost
Half Its Money in a Month.", build/youtube_ep012.py): the film's sharpest number puzzle, its own line "at 25 to 1 a
4% fall wipes out the capital and a 1% fall takes a quarter" (labelled there as ours), with the film's sources.

The puzzle: you buy $100 of bonds with $4 of your own and $96 borrowed. The bonds fall 4%. What is left of your $4?
Nothing. Arithmetic, true in any country and any currency: the loan does not shrink when the bonds do.

Our arithmetic (an illustration, not LTCM's own trades; checked with a short script in this run):
    Assets $100 = debt $96 + yours $4; assets / yours = 100 / 4 = 25 ("25 to 1").
    A 4% fall: 4% x $100 = $4 lost; assets $96, debt still $96, yours $96 - $96 = $0.
    A 1% fall: $1 lost; yours $3; $1 / $4 = 25% ("a quarter").
    So at 25 to 1 every move in the assets is 25 times as large on your own money (1% x 25 = 25%).
    The close (not answered on screen): at 10 to 1 a 10% fall takes everything ($100 = $90 + $10; 10% x $100 = $10).
    The rule (the film's point of view, labelled as ours there): leverage doesn't change whether a trade is right; it
    changes how far it can go wrong before your money is gone (at no debt a 100% fall, at 25 to 1 a 4% fall).

LTCM, sources (opened again in this run, 19 Nov 2026):
    [PWG] President's Working Group on Financial Markets, "Hedge Funds, Leverage, and the Lessons of Long-Term Capital
        Management", April 1999 (CFTC copy, https://www.cftc.gov/tm/tmhedgefundreport.htm): balance sheet over $125bn
        on 31 Aug 1998, "a balance-sheet leverage ratio of more than 25-to-1" on its $4.8bn of capital at the start of
        1998; capital $4.1bn on 31 July; August losses $1.8bn, capital $2.3bn at the end of August; 14 firms invested
        "about $3.6 billion in new equity".
    [FRH] Federal Reserve History, "Near Failure of Long-Term Capital Management"
        (https://www.federalreservehistory.org/essays/ltcm-near-failure): two Nobel laureates; about $30 of debt per $1
        of capital at end-1997; 44% lost in August 1998; $3.6bn from 14 firms; no Fed money.
    [MCD] William J. McDonough, NY Fed, statement to the House Banking Committee, 1 Oct 1998
        (https://www.newyorkfed.org/newsevents/speeches/1998/mcd981001): 14 firms participated; "Not one penny of public
        money was spent or committed."
    Checks: 1.8 / 4.1 = 43.9%, said "44%" ([FRH] says 44%); 4.1 - 1.8 = 2.3.

Beats, checked:
    puzzle   $100 of bonds, $4 yours, $96 borrowed, a 4% fall (our illustration). The question first, no setup.
    answer   nothing: 4% of $100 is $4 and the loan still wants all $96.
    one      a 1% fall costs a quarter: $1 of $4.
    ratio    25 to 1: every $1 of yours carries $25 of bonds; a move hits you 25 times as hard.
    ltcm     "more than 25 to 1" [PWG: over $125bn of assets on $4.8bn]; 44% of its capital lost in August [FRH; PWG
             1.8 / 4.1]. The 4% is not said to be LTCM's own fall. (The rescue, 14 firms and $3.6bn [PWG, FRH, MCD], is
             in the description and the film, cut from the Short for length.)
    rule     the film's reading, said as a reading of the arithmetic, not a claim about any one trade.
    close    at 10 to 1, how far can prices fall? (not answered). The film is the Related video and the pinned comment.

    python3 build/shorts_four-percent-wipeout.py HEART
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
    """Faint tags drifting at the edges, clear of the text (never the answer: no $0 or WIPED OUT)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "25 TO 1", "#3B3F48", 200), (770, 560, "−4%", RED, 170),
                                              (-100, 1030, "$96", "#3B3F48", 170), (770, 1120, "$4", GOLD, 150)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


def rain(t0, dur):
    """Tags falling in under the comment ask, then bobbing (no 10%: the close's answer)."""
    rnd = random.Random(19)
    out = ""
    labs = [("25 TO 1", "#3B3F48"), ("−1%", RED), ("$4", GOLD), ("$96", "#3B3F48"), ("10 TO 1", "#0F766E")]
    for k, (lab, fill) in enumerate(labs):
        x, y = rnd.uniform(-10 + 150 * k, 10 + 150 * k), rnd.uniform(1040, 1120)
        art = chip(lab, fill, rnd.uniform(130, 160), "#0A0A0A" if fill == GOLD else "#fff")
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px")
    return out


EP = dict(
    slug="shorts-four-percent-wipeout",
    kicker="MONEY MATHS",
    mood="tense",
    cover=dict(at=("e", 0, 3, .3), lines=["$100 of bonds.", "$4 of your own.", "They fall 4%.", "What's left?"],
               hl={"$100": TEAL_INK, "$4": GOLD, "4%.": RED, "left?": RED}, avoid=["$0", "WIPED", "Nothing"]),
    beats=[
        dict(tag="THE PUZZLE", size=58, hold=.45, art_h=540, hl=["$100 of bonds", "$4", "$96", "fall 4%."],
             say=[("You buy a hundred dollars of bonds with four dollars of your own.",
                   "You buy $100 of bonds with $4 of your own."),
                  ("You borrow the other ninety six.", "You borrow the other $96."),
                  ("The bonds fall four percent.", "The bonds fall 4%."),
                  ("What's left of your four?", "What's left of your $4?")],
             art=lambda t0, d, seg: picture("lv_hook", t0, d, seg=seg, **PIC),
             # bonds land, the $4 sliver lands, the loan grows and lands, the 4% slice drops away, the ring closes
             sfx=[(("s", 0, 1.3), "thump", .12), (("s", 0, 2.55), "clink", .07), (("s", 1, .25), "paper", .06),
                  (("s", 1, 1.15), "thump", .1), (("s", 2, .9), "knock", .08), (("s", 3, .15), "pop", .06)]),
        dict(tag="THE ANSWER", hl=["Nothing.", "$4.", "all $96"],
             say=[("Nothing.", "Nothing."),
                  ("Four percent of a hundred is four dollars.", "4% of $100 is $4."),
                  ("And the loan still wants all ninety six back.", "And the loan still wants all $96 back.")],
             art=lambda t0, d, seg: picture("lv_zero", t0, d, seg=seg, **PIC),
             # the WIPED OUT stamp, the 4% tag, the OWED ring, the = lands
             sfx=[(("s", 0, .3), "thump", .14), (("s", 1, .66), "pop", .06), (("s", 2, .3), "paper", .06), (("s", 2, 1.8), "pop", .06)]),
        dict(tag="JUST 1%", hl=["1%", "a quarter", "$1 out of $4."],
             say=[("Even a one percent fall costs you a quarter of your money.",
                   "Even a 1% fall costs you a quarter of your money."),
                  ("One dollar out of four.", "$1 out of $4.")],
             art=lambda t0, d, seg: picture("lv_one", t0, d, seg=seg, **PIC),
             # the -1% tag, the red coin lands on the ground, the 1 OF 4 tag
             sfx=[(("s", 0, .66), "pop", .06), (("s", 0, 2.95), "clink", .08), (("s", 1, .85), "tick", .04)]),
        dict(tag="THE RATIO", size=58, art_h=600, hl=["25 to 1.", "$25", "25 times"],
             say=[("That's twenty five to one.", "That's 25 to 1."),
                  ("Every dollar of yours carries twenty five dollars of bonds.", "Every $1 of yours carries $25 of bonds."),
                  ("So every move hits you twenty five times as hard.", "So every move hits you 25 times as hard.")],
             art=lambda t0, d, seg: picture("lv_ratio", t0, d, seg=seg, **PIC),
             # the 25 TO 1 tag, the tiles filling (a tick every fifth), the -1% chip, the ring on the coin
             sfx=[(("s", 0, .3), "pop", .07)] + [(("s", 1, .8 + 1.92 * j / 4), "tick", .03) for j in range(5)]
                 + [(("s", 2, .6), "pop", .06), (("s", 2, 1.8), "thump", .1)]),
        dict(tag="IT HAPPENED", size=58, art_h=600, hl=["more than 25 to 1.", "44%"],
             say=[("In nineteen ninety eight, the hedge fund LTCM ran at more than twenty five to one.",
                   "In 1998, the hedge fund LTCM ran at more than 25 to 1."),
                  ("In August alone, it lost forty four percent of its capital.", "In August alone, it lost 44% of its capital.")],
             art=lambda t0, d, seg: picture("lv_ltcm", t0, d, seg=seg, **PIC),
             # the gold capital sliver lands, the 25 TO 1 tag, the AUGUST ribbon, the 44% lifts away, the -44% tag
             sfx=[(("s", 0, 3.3), "clink", .07), (("s", 0, 4.1), "pop", .06), (("s", 1, .36), "paper", .06),
                  (("s", 1, 1.9), "knock", .07), (("s", 1, 2.7), "pop", .06)]),
        dict(tag="THE RULE", size=58, art_h=600, hl=["right.", "gone."],
             say=[("Leverage doesn't change whether a trade is right.", "Leverage doesn't change whether a trade is right."),
                  ("It changes how far it can go wrong before your money's gone.",
                   "It changes how far it can go wrong before your money's gone.")],
             art=lambda t0, d, seg: picture("lv_rule", t0, d, seg=seg, **PIC),
             # the two ticks, the SAME tag, the 4% ring
             sfx=[(("s", 0, .7), "paper", .05), (("s", 0, .95), "paper", .05), (("s", 0, 1.9), "pop", .06),
                  (("s", 1, 2.5), "thump", .1)]),
    ],
    close=dict(say=[("At ten to one, how far can prices fall before you're wiped out?",
                     "At 10 to 1, how far can prices fall before you're wiped out?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED}, art=rain,
               pic=lambda t0, d: picture("lv_asks", t0, d, w=520, h=416)),
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
