"""
Reel C, 22 Nov 2026 (the first slot C: Pietro, 22 Nov, three Reels a day this week): Format F (a choice) on the
story engine (build/story.py), narrator HEART (Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
Margin or markup: the same $25 of profit is 25% or 33% depending on what you divide it by.

A worked illustration with round numbers of our own; no company or statistic is claimed. Definitions: margin =
profit / price (revenue); markup = profit / cost. Gross, EBITDA and net margin are each that profit line over revenue.

Every number, worked:
    The deal:       cost $75, price $100, profit 100 - 75 = $25.
    Margin:         25 / 100 = 25%.
    Markup:         25 / 75 = 0.3333 = 33% (shown 33%; $25 fits into $75 three times).
    The trap:       cost $100 with a 50% markup: price 100 x 1.5 = $150, profit $50, margin 50 / 150 = 33%.
                    A 100% markup: price $200, profit $100, margin 100 / 200 = 50% ("keep half of every sale").
    Markup > margin whenever there is a profit, because cost is smaller than price.
    Close (asked):  a 25% markup: on $100 of cost, price $125, margin 25 / 125 = 20% (not given).
    Comment bonus:  the price for a 40% margin on a $60 cost: 60 / (1 - 0.4) = $100 (check: 40 / 100 = 40%).

22 Nov, from the performance data (docs/daily/quality-log.md row of 22 Nov): a hook that sets two numbers against
each other (the paradox opening), 15 words, on the story engine; Format F (a choice), not used since 18 Nov.

    python3 build/reels_margin-markup.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "$75", GOLD, 150), (770, 560, "COST", "#3B3F48", 160),
                                              (-100, 1030, "PRICE", "#0F766E", 170), (770, 1120, "$100", GOLD, 150)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-margin-markup",
    kicker="IB CHOICE",
    mood="curious",
    cover=dict(at=("e", 0, 1, .3), lines=["Buy for $75,", "sell for $100.", "Margin 25% or 33%?"],
               hl={"$75,": GOLD, "$100.": GOLD, "25%": RED, "33%?": RED}, avoid=["MARKUP", "REVENUE"]),
    beats=[
        dict(tag="THE CHOICE", size=60, hold=.6, hl=["$75", "$100.", "25%,", "33%?"],
             say=[("You buy it for seventy five dollars and sell it for a hundred.", "You buy it for $75 and sell it for $100."),
                  ("Is your margin twenty five percent, or thirty three?", "Is your margin 25%, or 33%?")],
             art=lambda t0, d, seg: picture("mk_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "thump", .07), (("s", 0, .72), "thump", .07), (("s", 0, .8), "pop", .05), (("s", 1, .3), "pop", .05),
                  (("s", 1, .5), "pop", .05)]),
        dict(tag="THE PROFIT", size=56, hl=["$25.", "divide"],
             say=[("Either way, the profit is twenty five dollars.", "Either way, the profit is $25."),
                  ("The question is what you divide it by.", "The question is what you divide it by.")],
             art=lambda t0, d, seg: picture("mk_profit", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .55), "pop", .05), (("s", 0, .9), "clink", .05), (("s", 1, .3), "tick", .04), (("s", 1, .6), "tick", .04)]),
        dict(tag="MARGIN", size=54, hl=["price:", "25%.", "keep."],
             say=[("Margin divides by the price: twenty five over a hundred is twenty five percent.",
                   "Margin divides by the price: $25 over $100 is 25%."),
                  ("It's the share of every sale you keep.", "It's the share of every sale you keep.")],
             art=lambda t0, d, seg: picture("mk_margin", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "tick", .04), (("s", 0, .55), "pop", .05), (("s", 0, .8), "clink", .05), (("s", 1, .2), "clink", .04),
                  (("s", 1, .5), "clink", .04)]),
        dict(tag="MARKUP", size=54, hl=["cost:", "33%.", "bigger"],
             say=[("Markup divides by the cost: twenty five over seventy five is thirty three percent.",
                   "Markup divides by the cost: $25 over $75 is 33%."),
                  ("Same deal, bigger number.", "Same deal, bigger number.")],
             art=lambda t0, d, seg: picture("mk_markup", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "tick", .04), (("s", 0, .5), "thump", .06), (("s", 0, .65), "thump", .06), (("s", 0, .8), "thump", .06),
                  (("s", 1, .2), "pop", .05)]),
        dict(tag="THE TRAP", size=54, hl=["50%", "33%", "100%"],
             say=[("So a fifty percent markup is only a thirty three percent margin.", "So a 50% markup is only a 33% margin."),
                  ("To keep half of every sale, you'd need a one hundred percent markup.", "To keep half of every sale, you'd need a 100% markup.")],
             art=lambda t0, d, seg: picture("mk_trap", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "thump", .07), (("s", 0, .6), "tick", .04), (("s", 1, .05), "paper", .05), (("s", 1, .6), "pop", .05)]),
        dict(tag="THE RULE", size=56, hl=["revenue.", "cost,", "bigger."],
             say=[("Every margin in a model is over revenue.", "Every margin in a model is over revenue."),
                  ("Markup is over cost, so it always looks bigger.", "Markup is over cost, so it always looks bigger.")],
             art=lambda t0, d, seg: picture("mk_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "pop", .05), (("s", 0, .5), "pop", .05), (("s", 0, .75), "pop", .05), (("s", 1, .2), "thump", .06),
                  (("s", 1, .5), "thump", .06)]),
    ],
    close=dict(say=[("Now it's a twenty five percent markup.", "Now it's a 25% markup."),
                    ("What's the margin?", "What's the margin?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED},
               pic=lambda t0, d: picture("mk_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",        # the grid cover (reel_cover.py) on the Reel's own ground
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
