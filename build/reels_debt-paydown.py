"""
Reel A, 19 Nov 2026: Format C (one surprising concept) on the story engine (build/story.py), narrator HEART (Kokoro
af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram. The debt paydown in a buyout: a company bought for $100
and sold five years later for $100, yet the owners double their money.

A worked illustration with round numbers of our own; no deal, fund or company is claimed. No fees, no cash left in
the company, the sale price equals the purchase price, and the company's cash after interest and tax is $8 a year
(an assumption of the example, said as "the company's cash pays down eight dollars of debt").

Every number, worked:
    Purchase:   price $100 = owners' equity $40 + debt $60.
    Five years: $8 a year of the company's cash repays debt: 5 x 8 = $40; debt 60 - 40 = $20 (60, 52, 44, 36, 28, 20).
    Sale:       price $100 (the same as paid): the lender is repaid $20; the owners get 100 - 20 = $80.
    Return:     $80 / $40 = 2.0x (MOIC). One cash flow in at year 0 and one out at year 5: IRR = 2^(1/5) - 1 =
                0.1487, said "about fifteen percent a year".
    No growth:  the price is $100 in year 0 and in year 5 (0% growth, the same multiple; nothing else changed).
    The lever:  the debt repaid moves $40 of the company's value from the lenders (60 to 20) to the owners (40 to 80).
                The standard buyout value bridge splits returns into earnings growth, a higher exit multiple and debt
                paydown (free cash flow); said as "one of the three classic buyout levers", no figure attached.
    Close (asked): the same deal sold for $120: owners get 120 - 20 = $100, $100 / $40 = 2.5x.
    Comment bonus: sold for $100 with none of the $60 repaid: owners get 100 - 60 = $40, $40 / $40 = 1.0x.

19 Nov, from the performance data (docs/daily/quality-log.md row of 19 Nov): the hook is the puzzle alone, number-led
and short; Format C. Reel B today is Format E (a myth).

    python3 build/reels_debt-paydown.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "$100", GOLD, 160), (770, 560, "$60", "#3B3F48", 160),
                                              (-100, 1030, "$40", GOLD, 150), (770, 1120, "5Y", "#0F766E", 150)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-debt-paydown",
    kicker="IB CONCEPT",
    mood="calm",
    cover=dict(at=("e", 0, 1, .3), lines=["Bought for $100.", "Sold for $100.", "How did they make 2x?"],
               hl={"$100.": GOLD, "2x?": RED}, avoid=["$80", "DEBT", "$20"]),
    beats=[
        dict(tag="THE PUZZLE", size=60, hold=.6, hl=["$100,", "$100.", "double their money?"],
             say=[("Bought for a hundred dollars, sold five years later for a hundred dollars.",
                   "Bought for $100, sold five years later for $100."),
                  ("So how did the owners double their money?", "So how did the owners double their money?")],
             art=lambda t0, d, seg: picture("dp_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "thump", .08), (("s", 0, 2.6), "thump", .08), (("s", 1, .4), "pop", .05), (("s", 1, 1.6), "pop", .05)]),
        dict(tag="THE DEAL", size=58, hl=["$40", "$60."],
             say=[("They paid forty dollars of their own, and borrowed sixty.", "They paid $40 of their own, and borrowed $60."),
                  ("The loan sits on the company, not on them.", "The loan sits on the company, not on them.")],
             art=lambda t0, d, seg: picture("dp_deal", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .4), "thump", .08), (("s", 0, 2.2), "knock", .07), (("s", 1, .3), "pop", .05), (("s", 1, 1.5), "pop", .05)]),
        dict(tag="FIVE YEARS", size=56, hl=["$8", "$20."],
             say=[("Every year, the company's cash pays down eight dollars of debt.",
                   "Every year, the company's cash pays down $8 of debt."),
                  ("Five years later, sixty has become twenty.", "Five years later, $60 has become $20.")],
             art=lambda t0, d, seg: picture("dp_years", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .6), "clink", .07), (("s", 1, .7), "clink", .06), (("s", 1, 1.1), "clink", .06),
                  (("s", 1, 1.5), "clink", .06), (("s", 1, 1.9), "clink", .06)]),
        dict(tag="THE SALE", size=56, hl=["$100,", "$80"],
             say=[("They sell for a hundred dollars, the same price they paid.", "They sell for $100, the same price they paid."),
                  ("The lender takes its twenty, and eighty dollars is left for them.",
                   "The lender takes its $20, and $80 is left for them.")],
             art=lambda t0, d, seg: picture("dp_sale", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "ding", .05), (("s", 1, 1.2), "knock", .07), (("e", 1, -.4), "pop", .06)]),
        dict(tag="THE RETURN", size=58, hl=["2x", "15%"],
             say=[("Forty in, eighty out, so that's two times their money.", "$40 in, $80 out, so that's 2x their money."),
                  ("About fifteen percent a year, with no growth at all.", "About 15% a year, with no growth at all.")],
             art=lambda t0, d, seg: picture("dp_return", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "tick", .04), (("s", 0, 1.2), "tick", .04), (("s", 0, 2.2), "thump", .09), (("s", 1, .4), "pop", .06)]),
        dict(tag="THE LEVER", size=54, hl=["lenders", "owners.", "three"],
             say=[("Paying down debt moves value from the lenders to the owners.",
                   "Paying down debt moves value from the lenders to the owners."),
                  ("It's one of the three classic buyout levers, with growth and a higher multiple.",
                   "It's one of the three classic buyout levers, with growth and a higher multiple.")],
             art=lambda t0, d, seg: picture("dp_lever", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .5), "tick", .04), (("s", 0, 1.1), "tick", .04), (("s", 0, 1.7), "tick", .04),
                  (("s", 1, .2), "pop", .06), (("s", 1, 2.4), "pop", .05), (("s", 1, 3.3), "pop", .05)]),
    ],
    close=dict(say=[("Same deal, but it sells for a hundred and twenty.", "Same deal, but it sells for $120."),
                    ("What's the multiple on their money?", "What's the multiple on their money?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED},
               pic=lambda t0, d: picture("dp_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
