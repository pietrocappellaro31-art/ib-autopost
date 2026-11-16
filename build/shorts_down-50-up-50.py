"""
YouTube Short, Format C (one surprising concept), 16 Nov 2026, on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9). A $100 stock falls 50% and then rises 50%: it is at $75, not $100. The rise is
measured from a smaller number, so getting back from a 50% fall takes a 100% gain; the bigger the fall, the faster
the gain needed grows (10% needs about 11%, 80% needs 400%). The real case: the S&P 500 from its October 2007 high
to the March 2009 low and back, which needed about 131% and took until March 2013.

Sources (all opened in this run, 16 Nov 2026):
    [1] Exceljet, "Required recovery rate". https://exceljet.net/formulas/required-recovery-rate
        Gain needed = 1 / (1 - loss) - 1; "A 50% loss does not require a 50% gain to recover the loss"; 10% loss
        needs 11.1%, 20% needs 25%, 50% needs 100%, 80% needs 400%.
    [2] Wikipedia, "United States bear market of 2007-2009".
        https://en.wikipedia.org/wiki/United_States_bear_market_of_2007%E2%80%932009
        S&P 500 closing high 1,565.15 on 9 Oct 2007, closing low 676.53 on 9 Mar 2009, peak to bottom -56.78%.
    [3] NPR, "1,569: S&P 500 Closes At All-Time High, Rising Above Oct. 2007 Mark", 28 Mar 2013.
        https://www.npr.org/sections/thetwo-way/2013/03/28/175610809/1-569-s-p-closes-at-all-time-high-rising-above-oct-2007-mark
        Closed at 1,569 on 28 Mar 2013, "an all-time high that erased the record set on Oct. 9, 2007".

Our arithmetic (checked with a short script in this run):
    100 x 0.5 = 50; 50 x 1.5 = 75. 50 -> 100 is +100%. Gain needed g = 1 / (1 - L) - 1: L = 10% -> 11.1% ("about
    eleven"), 25% -> 33.3%, 50% -> 100%, 80% -> 400%. S&P 500: 676.53 / 1,565.15 - 1 = -56.8% ("about fifty seven
    percent"); 1,565.15 / 676.53 - 1 = +131.4% ("about a hundred and thirty one percent"), on closing prices. The
    chart in beat 6 shows only the three real closes (1,565, 677 and the 28 Mar 2013 record); the line between them
    is drawn smooth and labelled PATH SIMPLIFIED. Index levels exclude dividends; the Short says nothing about total
    return. "The financial crisis" names the 2007 to 2009 bear market of [2].

Beats, checked:
    hook      the puzzle (illustrative $100; no real stock).
    no        $75 (our arithmetic); the rise is 50% of $50.
    double    50 back to 100 is +100% [1].
    same      the same $50 is 50% of $100 and 100% of $50 (our arithmetic).
    ladder    10% -> about 11%, 80% -> 400% [1]; 25% and 50% drawn too; one scale for losses and gains.
    crisis    [2] about 57% fall, Oct 2007 high to Mar 2009 low; about 131% back (our arithmetic on [2]); [3] March 2013.
    No advice, no prediction, no claim about any investor's returns. Drawings are our own shapes: no index
    provider's logo or chart.

    python3 build/shorts_down-50-up-50.py HEART
"""

import random
import sys

from motion import A
from sketch import picture, _ptag, GREY   # noqa: F401
from story import make, RED, TEAL

CREAM, MINT, SKY, SAND, BLUSH, GOLDG, LILAC = ("#F7EBD9", "#D2E9E1", "#D6E2F3", "#EFE3D3", "#F3DCD3", "#F6E7C8", "#E2DAF0")
PIC = dict(w=752, h=640)


def chip(label, fill, w=190):
    return (f'<svg width="{w}" height="{w * .6:.0f}" viewBox="0 0 {w} {w * .6:.0f}" style="overflow:visible">'
            + _ptag(w / 2, w * .3, w * .95, label, fill, "#fff", round(w * .23)) + "</svg>")


def floaters(total):
    """Faint -50% and +50% tags drifting at the edges, clear of the text."""
    out = ""
    for k, (x, y, lab, w) in enumerate([(-90, 330, "−50%", 200), (770, 560, "+50%", 180), (-100, 1030, "+100%", 190),
                                        (770, 1120, "−50%", 190)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.12">'
                + A(chip(lab, RED if lab.startswith("−") else TEAL, w), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7) + "</div>")
    return out


def rain(t0, dur):
    """Tags falling in under the comment ask, then bobbing."""
    rnd = random.Random(16)
    out = ""
    labs = ["−50%", "+100%", "−80%", "+400%", "+50%"]
    for k, lab in enumerate(labs):
        x, y = rnd.uniform(-10 + 150 * k, 10 + 150 * k), rnd.uniform(1040, 1120)
        art = chip(lab, RED if lab.startswith("−") else TEAL, rnd.uniform(130, 160))
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px")
    return out


EP = dict(
    slug="shorts-down-50-up-50",
    kicker="MONEY MATHS",
    mood="curious",
    cover_at=4.6,      # after the rise stops short and the question mark lands
    beats=[
        dict(tag="THE PUZZLE", bg=CREAM, size=66, hl=["falls 50%.", "rises 50%."],
             say=[("A hundred dollar stock falls fifty percent.", "A $100 stock falls 50%."),
                  ("Then it rises fifty percent.", "Then it rises 50%."),
                  ("Are you back to a hundred?", "Are you back to $100?")],
             art=lambda t0, d, seg: picture("half_hook", t0, d, fall=seg[0][0] + 1.25, rise=seg[1][0] + .45, **PIC),
             sfx=[(("s", 0, 1.25 + .7), "thump", .14), (("s", 1, .45 + .1), "pop", .08), (("s", 1, .45 + 1.0), "knock", .06)]),
        dict(tag="THE ANSWER", bg=MINT, hl=["$75."],
             say=[("No, it's at seventy five.", "No, it's at $75."),
                  ("The rise is fifty percent of a smaller number.", "The rise is 50% of a smaller number.")],
             art=lambda t0, d, seg: picture("seventy_five", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .05 + .3), "thump", .14), (("s", 0, .35 + .45), "clink", .07),
                  (("s", 1, .15 + .4), "paper", .07), (("s", 1, 1.05 + .4), "paper", .07)]),
        dict(tag="THE WAY BACK", bg=SKY, hl=["double.", "100%"],
             say=[("To get back to a hundred, it has to double.", "To get back to $100, it has to double."),
                  ("That's a hundred percent gain, not fifty.", "That's a 100% gain, not 50%.")],
             art=lambda t0, d, seg: picture("doubles", t0, d, seg=seg, lift=seg[0][0] + 1.5, **PIC),
             sfx=[(("s", 0, 1.5 + .7), "clink", .08), (("s", 1, .3), "pop", .07), (("s", 1, 1.2), "paper", .08)]),
        dict(tag="WHY", bg=SAND, hl=["the same", "50%.", "100%."],
             say=[("The dollars are the same both ways.", "The dollars are the same both ways."),
                  ("Fifty down is fifty percent.", "$50 down is 50%."),
                  ("Fifty back up is a hundred percent.", "$50 back up is 100%.")],
             art=lambda t0, d, seg: picture("same_dollars", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .4 + .05), "tick", .05), (("s", 1, .2), "pop", .07), (("s", 2, .3), "pop", .07)]),
        dict(tag="THE BIGGER THE FALL", bg=BLUSH, hl=["about 11%.", "400%."],
             say=[("And the further it falls, the worse it gets.", "And the further it falls, the worse it gets."),
                  ("Down ten percent needs about eleven.", "Down 10% needs about 11%."),
                  ("Down eighty needs four hundred.", "Down 80% needs 400%.")],
             art=lambda t0, d, seg: picture("ladder", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2 + .3 * j), "tick", .04) for j in range(4)] + [(("s", 1, .35), "pop", .06),
                                                                              (("s", 2, .55 + .6), "thump", .15)]),
        dict(tag="IT HAPPENED", bg=GOLDG, hl=["about 57%.", "about 131%.", "March 2013."],
             say=[("In the financial crisis, the S and P five hundred fell about fifty seven percent.",
                   "In the financial crisis, the S&P 500 fell about 57%."),
                  ("Getting back needed a gain of about a hundred and thirty one percent.",
                   "Getting back needed a gain of about 131%."),
                  ("It took until March twenty thirteen.", "It took until March 2013.")],
             art=lambda t0, d, seg: picture("crisis_path", t0, d, seg=seg, **PIC)),
    ],
    close=dict(say=[("Did you think fifty would get you back?", "Did you think 50% would get you back?"),
                    ("Tell me in the comments.", "Tell me in the comments."),
                    ("And subscribe for more like this.", "And subscribe for more like this.")],
               cols={"comments.": RED}, bg=LILAC, art=rain,
               pic=lambda t0, d: picture("fifty_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # clean master: Pietro adds a sound in the YouTube app
    lufs=-14,
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
