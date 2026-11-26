"""
Reel C, 26 Nov 2026 (slot C 21:00 ET): Format F (a choice) on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
You pay 2%, then 3%: up 1%, or up 50%? Percentage points against percent, and basis points.

A worked illustration with round numbers of our own; no rate, lender or statistic is claimed, and no forecast.
Assumptions, said or on screen: $1,000 borrowed, simple interest for one year at the stated rate.

Every number worked:
    At 2%:        1,000 x 2% = $20 of interest a year.
    At 3%:        1,000 x 3% = $30; the bill rises 30 - 20 = $10, and 10 / 20 = 50%: half as much again.
    Points:       3% - 2% = 1 percentage point.
    Percent:      (3 - 2) / 2 = 1 / 2 = 50%.
    Basis points: 1 percentage point = 100 basis points (1 bp = 0.01 percentage point).
    Rule:         subtract two percentages: points; divide the change by the starting value: percent.
    Close (asked):  a margin from 10% to 12%: 12 - 10 = 2 points = 200 basis points; (12 - 10) / 10 = 20% (not given).
    Comment bonus:  rates fall from 5% to 4%: down 1 point (100 basis points) and down (5 - 4) / 5 = 20%.

Hook (24 Nov standard: five candidates, scored 1 to 5 on clash / number in the first three words / second person /
length on screen / would someone send it to a friend preparing for interviews):
    1. "2% to 3%. Did it rise 1%, or 50%?"                     clash 5, number 5, you 1, 8 words 5, send 5 = 21
    2. "Rates went from 2% to 3%. Your bill went up 50%."      clash 4, number 3, you 4, 11 words 5, send 4 = 20
       (gives the answer away)
    3. "1% or 50%? Both numbers are real."                     clash 4, number 5, you 1, 7 words 5, send 4 = 19
       (no set-up: the viewer can't tell what rose)
    4. "You pay 2%, then 3%. So is that up 1%, or up 50%?"     clash 5, number 5, you 5, 12 words 4, send 5 = 24
    5. "Answer before the marker stops: points or percent?"    clash 2, number 1, you 1, 8 words 5, send 3 = 12
    Chosen: 4 (24: the choice between two numbers that are both true, the shape of our best Reel so far, margin vs
    markup, 1,528 reach; the ruler marker moving 2% to 3% and both answer cards are on the panel from frame 0).

26 Nov, from the performance data (quality-log row of 26 Nov): plain money words in the hook (no multiple, no
acronym), the rates family, and the two-numbers choice shape in the evening slot that reached most; Format F.

    python3 build/reels_points-percent.py HEART
"""

import sys

import scenes_1126  # noqa: F401  (registers the pp_ scenes)
from motion import A
from sketch import picture, _ptag
from story import make, RED

GOLD = "#F2C35B"
PIC = dict(w=752, h=640)


def chip(label, fill, w=190, color="#fff"):
    return (f'<svg width="{w}" height="{w * .6:.0f}" viewBox="0 0 {w} {w * .6:.0f}" style="overflow:visible">'
            + _ptag(w / 2, w * .3, w * .95, label, fill, color, round(w * .23)) + "</svg>")


def floaters(total):
    """Faint tags drifting at the edges, clear of the text (never the answer)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "2%", "#3B3F48", 150), (770, 560, "BPS", "#0F766E", 150),
                                              (-100, 1030, "3%", "#3B3F48", 150), (770, 1120, "$", GOLD, 130)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-points-vs-percent",
    kicker="IB CHOICE",
    mood="curious",
    cover=dict(at=("e", 0, 0, .2), lines=["You pay 2%, then 3%.", "Up 1%, or up 50%?"],
               hl={"2%,": GOLD, "3%.": RED, "50%?": RED}, avoid=["1 POINT", "HALF"]),
    beats=[
        dict(tag="YOUR CALL", size=58, hold=.6, hl=["2%,", "3%.", "1%,", "50%?"],
             say=[("You pay two percent, then three percent.", "You pay 2%, then 3%."),
                  ("So is that up one percent, or up fifty percent?", "So is that up 1%, or up 50%?")],
             art=lambda t0, d, seg: picture("pp_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "pop", .05), (("s", 0, .6), "pop", .05), (("s", 1, .1), "knock", .05), (("s", 1, .35), "tick", .04),
                  (("s", 1, .7), "tick", .04)]),
        dict(tag="THE SET-UP", size=56, hl=["$1,000", "2%", "$20"],
             say=[("Say you borrow a thousand dollars at two percent a year.", "Say you borrow $1,000 at 2% a year."),
                  ("That's twenty dollars of interest.", "That's $20 of interest.")],
             art=lambda t0, d, seg: picture("pp_setup", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "paper", .05), (("s", 0, .5), "paper", .05), (("s", 1, .25), "clink", .05), (("s", 1, .55), "clink", .05)]),
        dict(tag="THE RISE", size=54, hl=["3%,", "$30.", "half"],
             say=[("Now the rate goes up to three percent, and you pay thirty dollars.", "Now the rate goes up to 3%, and you pay $30."),
                  ("That extra ten dollars is half of what you paid before.", "That extra $10 is half of what you paid before.")],
             art=lambda t0, d, seg: picture("pp_rise", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "tick", .04), (("s", 0, .6), "thump", .06), (("s", 1, .1), "pop", .05), (("s", 1, .6), "thump", .07)]),
        dict(tag="THE ANSWER", size=52, hl=["Both", "point,", "50%."],
             say=[("Both are right, it rose one percentage point, and it rose fifty percent.", "Both are right: it rose 1 percentage point, and it rose 50%."),
                  ("Three minus two is one point, and one over two is fifty percent.", "3 - 2 = 1 point, and 1 / 2 = 50%.")],
             art=lambda t0, d, seg: picture("pp_answer", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "pop", .05), (("s", 0, .65), "thump", .06), (("s", 1, .05), "pop", .05), (("s", 1, .55), "pop", .05)]),
        dict(tag="BASIS POINTS", size=54, hl=["basis", "100"],
             say=[("Bankers say points, or basis points, so nobody mixes them up.", "Bankers say points, or basis points, so nobody mixes them up."),
                  ("One point is a hundred basis points.", "1 point = 100 basis points.")],
             art=lambda t0, d, seg: picture("pp_bps", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "pop", .05), (("s", 0, .55), "pop", .05), (("s", 1, .1), "tick", .04), (("s", 1, .4), "tick", .04),
                  (("e", 1, .1), "thump", .06)]),
        dict(tag="THE RULE", size=52, hl=["Subtract", "points.", "Divide", "percent."],
             say=[("Subtract two percentages, and you get points.", "Subtract two percentages, and you get points."),
                  ("Divide the change by where you started, and you get percent.", "Divide the change by where you started, and you get percent.")],
             art=lambda t0, d, seg: picture("pp_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "tick", .04), (("s", 0, .5), "tick", .04), (("s", 0, .8), "pop", .05), (("s", 1, .15), "tick", .04),
                  (("s", 1, .55), "tick", .04), (("s", 1, .9), "pop", .05)]),
    ],
    close=dict(say=[("A margin goes from ten percent to twelve percent.", "A margin goes from 10% to 12%."),
                    ("How many basis points is that, and what percent rise?", "How many basis points? What % rise?"),
                    ("Answer in the comments, and follow for tomorrow's.", "Answer in the comments, and follow for tomorrow's.")],
               cols={"comments,": RED, "follow": RED}, bar=True, art_w=720, art_h=576, size=80,
               pic=lambda t0, d: picture("pp_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]), keep_voice="--keep-voice" in sys.argv)
