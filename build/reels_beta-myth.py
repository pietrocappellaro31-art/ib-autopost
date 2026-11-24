"""
Reel B, 24 Nov 2026 (slot B 18:00 ET): Format E (a myth) on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
Beta 2 swings twice as much as the market: does it earn twice the return? The CAPM myth.

A worked illustration with round numbers of our own; no company, index level or statistic is claimed, and no
forecast. Assumptions, said or on screen: safe government bonds pay 4% (the risk-free rate); the market is expected
to return 9%, so 5% above the safe rate (the market risk premium); the capital asset pricing model (CAPM): expected
return = safe rate + beta x (market return - safe rate). Beta measures how much a stock moves with the market.

Every number, worked:
    The myth:       2 x 9% = 18%.
    The extra:      9% - 4% = 5%; beta 2 doubles only the extra: 2 x 5% = 10%.
    The answer:     4% + 10% = 14%, not 18% (4 points lower).
    Rule, 2nd move: beta 1: 4 + 1 x 5 = 9% (the market itself); beta 0: 4 + 0 = 4% (the safe rate).
    Close (asked):  beta 0.5: 4 + 0.5 x 5 = 6.5% (not given).
    Comment bonus:  beta 1.5: 4 + 1.5 x 5 = 11.5%.
    Banking use:    CAPM's expected return is the usual cost of equity in a DCF's discount rate (WACC); said as how
                    bankers find it, not as a claim about any bank.

Hook (24 Nov standard: five candidates, scored 1 to 5 on clash / number in the first three words / second person /
length on screen / would someone send it to a friend preparing for interviews):
    1. "Beta 2 swings twice as much as the market. Does it earn double?"   clash 5, number 5, you 2, 12 words 5, send 5 = 22
       (first cut: "Beta 2: it swings ... Twice the return?", but HEART said "thee return" and the recogniser
       caught it, so the question was reworded)
    2. "Twice the risk of the market. So twice the return, right?"           clash 4, number 2, you 2, 11 words 5, send 4 = 17
    3. "It's not 18%. A beta of 2 earns 14%. Here's why."                    clash 4, number 5, you 1, 11 words 5, send 3 = 18
       (gives the answer away)
    4. "You buy a beta 2 stock. The market makes 9%. Do you make 18%?"       clash 4, number 4, you 5, 14 words 3, send 4 = 20
    5. "Answer before the bar lands: what does beta 2 earn?"                 clash 2, number 2, you 1, 9 words 5, send 3 = 13
    Chosen: 1 (two numbers in conflict, x2 risk against x2 return), the two lines moving on screen from frame 0.

24 Nov, from the performance data (docs/daily/quality-log.md row of 24 Nov): the myth format ("Buy back 10% ...
Nope.", 1,147 reach, 19 saves) and the WACC family of interview technicals; Format E, last used 22 Nov.

    python3 build/reels_beta-myth.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "BETA", "#3B3F48", 160), (770, 560, "9%", "#0F766E", 140),
                                              (-100, 1030, "4%", "#3B3F48", 140), (770, 1120, "x2", GOLD, 140)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-beta-myth",
    kicker="IB MYTH",
    mood="curious",
    cover=dict(at=("e", 0, 1, .3), lines=["Beta 2 swings twice", "as much as the market.", "Does it earn double?"],
               hl={"2": RED, "twice": GOLD, "double?": RED}, avoid=["14%", "10%"]),
    beats=[
        dict(tag="THE MYTH", size=60, hold=.6, hl=["2", "twice", "double?"],
             say=[("Beta two swings twice as much as the market.", "Beta 2 swings twice as much as the market."),
                  ("Does it earn double?", "Does it earn double?")],
             art=lambda t0, d, seg: picture("bt_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "thump", .07), (("s", 0, .35), "tick", .04), (("s", 0, .5), "pop", .05), (("s", 1, .1), "pop", .05)]),
        dict(tag="THE SET-UP", size=56, hl=["4%.", "9%."],
             say=[("Say safe government bonds pay four percent.", "Say safe government bonds pay 4%."),
                  ("And the market is expected to return nine percent.", "And the market is expected to return 9%.")],
             art=lambda t0, d, seg: picture("bt_setup", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .35), "pop", .05), (("s", 0, .6), "tick", .04), (("s", 1, .35), "pop", .05), (("s", 1, .7), "tick", .04)]),
        dict(tag="THE MYTH'S SUM", size=56, hl=["18%.", "myth."],
             say=[("Twice the market sounds like eighteen percent.", "Twice the market sounds like 18%."),
                  ("That's the myth.", "That's the myth.")],
             art=lambda t0, d, seg: picture("bt_double", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "thump", .06), (("s", 0, .55), "pop", .05), (("s", 1, .25), "thump", .07)]),
        dict(tag="ONLY THE EXTRA", size=54, hl=["above", "5%,", "10%."],
             say=[("Beta only doubles the part above the safe rate.", "Beta only doubles the part above the safe rate."),
                  ("Nine minus four is five percent, and twice five is ten.", "9% minus 4% is 5%, and twice 5% is 10%.")],
             art=lambda t0, d, seg: picture("bt_split", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .35), "pop", .05), (("s", 0, .6), "pop", .05), (("s", 1, .1), "tick", .04), (("s", 1, .65), "clink", .05),
                  (("s", 1, .85), "pop", .05)]),
        dict(tag="THE ANSWER", size=56, hl=["14%.", "18%."],
             say=[("Add back the four, and you get fourteen percent.", "Add back the 4%, and you get 14%."),
                  ("Not eighteen.", "Not 18%.")],
             art=lambda t0, d, seg: picture("bt_answer", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "pop", .05), (("s", 0, .85), "thump", .07), (("s", 1, .3), "tick", .04)]),
        dict(tag="THE RULE", size=52, hl=["safe", "beta", "extra.", "equity."],
             say=[("Expected return is the safe rate, plus beta times the market's extra.",
                   "Expected return is the safe rate, plus beta times the market's extra."),
                  ("It's how bankers find the cost of equity.", "It's how bankers find the cost of equity.")],
             art=lambda t0, d, seg: picture("bt_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "pop", .05), (("s", 0, .55), "pop", .05), (("s", 0, .8), "tick", .04), (("s", 1, .2), "tick", .04),
                  (("s", 1, .5), "tick", .04)]),
    ],
    close=dict(say=[("Now the beta is a half.", "Now the beta is 0.5."),
                    ("What return should you expect?", "What return should you expect?"),
                    ("Answer in the comments, and follow for tomorrow's.", "Answer in the comments, and follow for tomorrow's.")],
               cols={"comments,": RED, "follow": RED}, bar=True, art_w=720, art_h=576,
               pic=lambda t0, d: picture("bt_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",        # the grid cover (reel_cover.py) on the Reel's own ground
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
