"""
Reel A, 22 Nov 2026: Format D (an animated calculation) on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram. Minority (noncontrolling) interest in
enterprise value: why you add it.

A worked illustration with round numbers of our own; no company is claimed. The accounting it rests on: a parent
that controls a subsidiary (usually more than half the votes) consolidates it, so 100% of the subsidiary's revenue,
costs and EBITDA sit in the parent's figures (IFRS 10; US GAAP ASC 810), and the part owned by outsiders is shown as
noncontrolling interest. The enterprise value bridge adds it so that EV and EBITDA cover the same owners (the usual
interview answer). An equity-method stake (say 30%) puts none of its EBITDA in yours, so it is subtracted (the
close; not given).

Every number, worked:
    Ownership:      you own 80% of the subsidiary; outsiders own 20%.
    EBITDA:         your own business $40 + all of the subsidiary's $10 = $50 consolidated.
    Equity value:   your market value $300; it pays only for your 80% of the subsidiary.
    Minority:       the subsidiary's equity is worth $100, so the outside 20% is 0.2 x 100 = $20.
    EV:             300 + 100 debt - 20 cash + 20 minority interest = $400.
    Multiple:       400 / 50 = 8.0x. Leave minority out: 380 / 50 = 7.6x (looks cheaper than it is).
    Close (asked):  a 30% stake with no control (its EBITDA is not in yours): add or subtract? (subtract; not given)
    Comment bonus:  the same company plus a 30% stake worth $15: 400 - 15 = $385.

22 Nov, from the performance data (docs/daily/quality-log.md row of 22 Nov): a hook of 13 words, two facts that
seem to clash and a why (the paradox opening of the 1,100+ Reels), on the story engine (average watch 12 to 15 s,
against 7 to 10 s on Levels). Format D, the week's second; Reel B today is Format E.

The 20 Nov next improvement: the camera keys are re-solved inside each drawing's fitted view (motion.js fitSvg),
so a zoom can no longer cut labels at the edge; the multiple beat changes state with a full-panel wipe.

    python3 build/reels_minority-interest.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "80%", GOLD, 150), (770, 560, "EV", "#3B3F48", 150),
                                              (-100, 1030, "EBITDA", "#0F766E", 180), (770, 1120, "20%", GOLD, 150)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-minority-interest",
    kicker="IB CALCULATION",
    mood="curious",
    cover=dict(at=("e", 0, 1, .3), lines=["You own 80%.", "Why is all its EBITDA", "in yours?"],
               hl={"80%.": GOLD, "all": RED, "yours?": RED}, avoid=["$400", "8.0x", "MINORITY", "CONTROL"]),
    beats=[
        dict(tag="THE PUZZLE", size=60, hold=.6, hl=["80%", "all", "yours?"],
             say=[("You own eighty percent of a company.", "You own 80% of a company."),
                  ("Why is all of its EBITDA in yours?", "Why is all of its EBITDA in yours?")],
             art=lambda t0, d, seg: picture("mi_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "pop", .05), (("s", 0, .55), "pop", .05), (("s", 1, .2), "tick", .04), (("s", 1, .55), "thump", .08),
                  (("s", 1, .7), "pop", .05)]),
        dict(tag="CONTROL", size=56, hl=["control", "all", "$50."],
             say=[("Own more than half, and you control it, so you report all of it.", "Own more than half, and you control it, so you report all of it."),
                  ("Your forty of EBITDA, plus all of its ten, makes fifty.", "Your $40 of EBITDA, plus all of its $10, makes $50.")],
             art=lambda t0, d, seg: picture("mi_control", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "tick", .04), (("s", 0, .45), "knock", .08), (("s", 1, .12), "pop", .05), (("s", 1, .52), "thump", .08),
                  (("s", 1, .8), "clink", .05)]),
        dict(tag="WHO YOU PAY FOR", size=54, hl=["80%.", "$20,", "else."],
             say=[("But your share price only pays for your eighty percent.", "But your share price only pays for your 80%."),
                  ("The other twenty percent, worth twenty dollars, belongs to someone else.", "The other 20%, worth $20, belongs to someone else.")],
             art=lambda t0, d, seg: picture("mi_owners", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "pop", .05), (("s", 0, .25), "tick", .04), (("s", 0, .75), "pop", .05), (("s", 1, .15), "knock", .06),
                  (("s", 1, .45), "pop", .05), (("s", 1, .75), "thump", .07)]),
        dict(tag="THE BRIDGE", size=52, hl=["$300", "$100", "$20", "minority", "$400."],
             say=[("Enterprise value: three hundred of equity, plus a hundred of debt, minus twenty of cash.",
                   "Enterprise value: $300 of equity, plus $100 of debt, minus $20 of cash."),
                  ("Then add the twenty of minority interest: four hundred.", "Then add the $20 of minority interest: $400.")],
             art=lambda t0, d, seg: picture("mi_bridge", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .12), "thump", .07), (("s", 0, .45), "thump", .07), (("s", 0, .78), "knock", .06), (("s", 1, .25), "thump", .08),
                  (("s", 1, .45), "pop", .05), (("s", 1, .7), "clink", .05)]),
        dict(tag="THE MULTIPLE", size=54, hl=["8x", "7.6x:", "cheaper"],
             say=[("Four hundred over fifty is eight times EBITDA.", "$400 over $50 is 8x EBITDA."),
                  ("Leave it out and you get seven point six: it looks cheaper than it is.", "Leave it out and you get 7.6x: it looks cheaper than it is.")],
             art=lambda t0, d, seg: picture("mi_multiple", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "tick", .04), (("s", 0, .5), "tick", .04), (("s", 0, .7), "tick", .04), (("s", 0, .9), "pop", .05),
                  (("s", 1, .08), "paper", .05), (("s", 1, .6), "knock", .08)]),
        dict(tag="THE RULE", size=58, hl=["same", "owners", "in."],
             say=[("Enterprise value and EBITDA must cover the same owners.", "Enterprise value and EBITDA must cover the same owners."),
                  ("If all the EBITDA is in, all the owners are in.", "If all the EBITDA is in, all the owners are in.")],
             art=lambda t0, d, seg: picture("mi_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .6), "thump", .07), (("s", 0, .85), "clink", .05), (("s", 1, .2), "pop", .05), (("s", 1, .45), "pop", .05)]),
    ],
    close=dict(say=[("Now flip it: a thirty percent stake, with no control.", "Now flip it: a 30% stake, with no control."),
                    ("Do you add that stake to enterprise value, or take it away?", "Do you add that stake to enterprise value, or take it away?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED},
               pic=lambda t0, d: picture("mi_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",        # the grid cover (reel_cover.py) on the Reel's own ground
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
