"""
Reel B, 18 Nov 2026: Format F (a choice the viewer reasons through) on the story engine (build/story.py), narrator
HEART (Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram. FIFO or LIFO with rising prices: you buy
one unit at $10, then one at $12, and sell one for $20. Is your profit $8 or $10? Both: it depends on the inventory
method.

A worked illustration with round numbers of our own; no company or industry is claimed. One sale, no other costs.

Every number, worked:
    Purchases:  unit 1 at $10 (first in), unit 2 at $12 (last in). One unit sold for $20.
    FIFO:       cost of goods sold = the first unit, $10; profit 20 - 10 = $10; the $12 unit stays in inventory.
    LIFO:       cost of goods sold = the last unit, $12; profit 20 - 12 = $8; the $10 unit stays in inventory.
    Tax:        at 25%, FIFO tax 25% x 10 = $2.50, LIFO 25% x 8 = $2.00: $0.50 less tax under LIFO on this one sale
                (rising prices only; in the US a company using LIFO for tax must also use it in its own reports, the
                LIFO conformity rule, not said).
    Rules:      US GAAP allows LIFO (ASC 330; KPMG, "Inventory accounting: IFRS Standards vs US GAAP"); IFRS does not:
                IAS 2 permits FIFO or weighted average cost, LIFO was removed in the 2003 revision (IAS Plus, IAS 2).
                Said as "American rules allow it. International rules don't."
    Close (asked): prices fall, $10 then $8, sold for $20: FIFO cost $10, profit $10; LIFO cost $8, profit $12. LIFO
                shows more profit when prices fall.
    Comment bonus: weighted average on the $10 and $12 units: cost (10 + 12) / 2 = $11, profit $9.

18 Nov, from the performance data: number-led hook (4 of the top 5 Reels opened on concrete numbers). Format F, the
first Reel as a choice; A today is format D.

    python3 build/reels_fifo-lifo.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "$10", GOLD, 150), (770, 560, "$20", "#0F766E", 170),
                                              (-100, 1030, "$12", "#0F766E", 150), (770, 1120, "$10", GOLD, 170)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-fifo-lifo",
    kicker="IB CHOICE",
    mood="tense",
    cover=dict(at=("e", 0, 2, .3), lines=["Bought at $10, then $12.", "Sold one for $20.", "Profit $8 or $10?"],
               hl={"$10,": TEAL_INK, "$12.": GOLD, "$20.": GOLD, "$10?": RED}, avoid=["BOTH", "FIFO", "LIFO"]),
    beats=[
        dict(tag="YOUR CALL", size=58, hold=.6, hl=["$10,", "$12.", "$20.", "$8, or $10?"],
             say=[("You buy one unit for ten dollars, then one for twelve.", "You buy one unit for $10, then one for $12."),
                  ("You sell one for twenty.", "You sell one for $20."),
                  ("Is your profit eight dollars, or ten?", "Is your profit $8, or $10?")],
             art=lambda t0, d, seg: picture("fl_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "thump", .08), (("s", 0, 1.9), "thump", .08), (("s", 1, .9), "clink", .07),
                  (("s", 2, .5), "pop", .05), (("s", 2, 1.1), "pop", .05)]),
        dict(tag="BOTH", size=58, hl=["Both,", "inventory method."],
             say=[("Both, depending on which unit you say you sold.", "Both, depending on which unit you say you sold."),
                  ("That's your inventory method.", "That's your inventory method.")],
             art=lambda t0, d, seg: picture("fl_both", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .05), "knock", .08), (("s", 1, .3), "pop", .06)]),
        dict(tag="FIFO", size=52, hl=["First in, first out:", "$10 of profit."],
             say=[("First in, first out: the ten dollar unit goes first.", "First in, first out: the $10 unit goes first."),
                  ("Twenty minus ten is ten dollars of profit.", "$20 minus $10 is $10 of profit."),
                  ("The twelve dollar unit stays in inventory.", "The $12 unit stays in inventory.")],
             art=lambda t0, d, seg: picture("fl_fifo", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, 1.6), "paper", .06), (("s", 1, .3), "tick", .04), (("s", 1, 1.6), "clink", .07),
                  (("s", 2, .6), "thump", .08)]),
        dict(tag="LIFO", size=52, hl=["Last in, first out:", "$8 of profit."],
             say=[("Last in, first out: the twelve dollar unit goes first.", "Last in, first out: the $12 unit goes first."),
                  ("Twenty minus twelve is eight dollars of profit.", "$20 minus $12 is $8 of profit."),
                  ("The ten dollar unit stays.", "The $10 unit stays.")],
             art=lambda t0, d, seg: picture("fl_lifo", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, 1.6), "paper", .06), (("s", 1, .3), "tick", .04), (("s", 1, 1.6), "clink", .07),
                  (("s", 2, .3), "knock", .06)]),
        dict(tag="RISING PRICES", size=52, hl=["less tax.", "50 cents"],
             say=[("When prices rise, last in, first out shows less profit, so less tax.",
                   "When prices rise, last in, first out shows less profit, so less tax."),
                  ("At a twenty five percent rate, that's fifty cents less, on one sale.",
                   "At a 25% rate, that's 50 cents less, on one sale.")],
             art=lambda t0, d, seg: picture("fl_tax", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .4), "tick", .04), (("s", 0, 2.4), "pop", .06), (("s", 1, 2.2), "clink", .08)]),
        dict(tag="THE RULES", size=60, hl=["allow it,", "do not."],
             say=[("American rules allow it, but international rules do not.", "American rules allow it, but international rules do not.")],
             art=lambda t0, d, seg: picture("fl_rules", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "thump", .09), (("d", .52), "thump", .09)]),
    ],
    close=dict(say=[("Now prices fall: ten, then eight.", "Now prices fall: $10, then $8."),
                    ("Which method shows more profit?", "Which method shows more profit?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED},
               pic=lambda t0, d: picture("fl_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
