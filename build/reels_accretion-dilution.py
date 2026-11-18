"""
Reel A, 18 Nov 2026: Format D (an animated calculation) on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram. Accretion and dilution in an all-stock deal:
your company trades at 20x earnings; you buy a target at 10x, paying in new shares. Does your EPS go up?

A worked illustration with round numbers of our own; no real company, deal or "typical" multiple is claimed. The
simplification is said on screen: an all-stock deal, before synergies, fees, financing costs and deal accounting.

Every number, worked:
    Buyer:      earnings $100, 100 shares, EPS 100 / 100 = $1.00. At 20x earnings the share price is 20 x $1 = $20
                (market value 100 x $20 = $2,000, not said).
    Target:     earnings $10. At 10x it costs 10 x $10 = $100. Paid in buyer shares at $20: 100 / 20 = 5 new shares.
    Combined:   earnings 100 + 10 = $110; shares 100 + 5 = 105; EPS 110 / 105 = 1.0476..., "about $1.05" (+4.8%).
                EPS rises: accretive.
    At 30x:     price 30 x $10 = $300; 300 / 20 = 15 new shares; EPS 110 / 115 = 0.9565..., "about 96 cents" (-4.3%).
                EPS falls: dilutive.
    The rule:   all stock, the buyer gives up earnings yield 1/20 = 5% on the shares it issues and gets the target's
                1/(price multiple). Paying a lower multiple than its own P/E (10x < 20x: 10% > 5%) raises EPS, a higher one
                (30x: 3.3% < 5%) lowers it. Before synergies and fees.
    Close (asked, answered in the comment bonus by the viewers): break-even price: EPS stays $1.00 when 110 / (100 + n)
                = 1, n = 10 shares = $200 = 20x, the buyer's own multiple.
    Comment bonus: same $300 price (15 shares), target earnings $15: 115 / 115 = $1.00, break-even.

18 Nov, from the performance data (docs/daily/performance.md, unchanged since 17 Nov 17:35 UTC: the 17 Nov Reels are
not yet in it): 4 of the 5 Reels with 1,000+ reach opened on concrete numbers, all 6 at 125 to 139 opened on an
abstract yes/no. So the hook leads with the two multiples. Format D varies the week (A on 17 Nov, C on 17 Nov).

18 Nov, the 17 Nov Reel next improvement: no beat over 3 sentences, every drawing acts on the first spoken word of
each sentence and again on its second number.

    python3 build/reels_accretion-dilution.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "20x", GOLD, 170), (770, 560, "EPS", "#0F766E", 170),
                                              (-100, 1030, "SHARES", "#0F766E", 210), (770, 1120, "10x", GOLD, 170)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-accretion-dilution",
    kicker="IB CALCULATION",
    mood="curious",
    cover=dict(at=("e", 0, 2, .3), lines=["You trade at 20x.", "You buy at 10x,", "in shares.", "EPS up or down?"],
               hl={"20x.": GOLD, "10x,": TEAL_INK, "down?": RED}, avoid=["ACCRETIVE", "DILUTIVE", "$1.05"]),
    beats=[
        dict(tag="ALL-STOCK DEAL", size=62, hold=.6, hl=["20x", "10x,", "go up?"],
             say=[("Your company trades at twenty times earnings.", "Your company trades at 20x earnings."),
                  ("You buy another at ten times, paying in shares.", "You buy another at 10x, paying in shares."),
                  ("Do your earnings per share go up?", "Do your earnings per share go up?")],
             art=lambda t0, d, seg: picture("ad_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "clink", .07), (("s", 1, .3), "clink", .07), (("s", 1, 1.3), "tick", .05),
                  (("s", 2, .1), "pop", .06)]),
        dict(tag="YOUR COMPANY", size=52, hl=["$1 a share.", "$20."],
             say=[("You earn a hundred dollars, on a hundred shares: a dollar a share.",
                   "You earn $100, on 100 shares: $1 a share."),
                  ("At twenty times, each share is worth twenty dollars.", "At 20x, each share is worth $20.")],
             art=lambda t0, d, seg: picture("ad_buyer", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "knock", .07), (("s", 0, 1.6), "tick", .04), (("s", 0, 2.3), "tick", .04),
                  (("e", 0, -.3), "clink", .06), (("s", 1, .1), "pop", .06), (("e", 1, -.4), "clink", .06)]),
        dict(tag="THE TARGET", size=52, hl=["$100.", "5 new shares,"],
             say=[("The target earns ten dollars, so at ten times it costs a hundred.", "The target earns $10, so at 10x it costs $100."),
                  ("You pay with five new shares, at twenty dollars each.", "You pay with 5 new shares, at $20 each.")],
             art=lambda t0, d, seg: picture("ad_target", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .5), "thump", .08), (("s", 0, 1.9), "paper", .06), (("s", 1, .2), "clink", .05),
                  (("s", 1, .6), "clink", .05), (("s", 1, 1.0), "clink", .05)]),
        dict(tag="AT 10x", size=52, hl=["$110,", "105 shares.", "$1.05", "accretive."],
             say=[("Now you earn a hundred and ten dollars, on a hundred and five shares.",
                   "Now you earn $110, on 105 shares."),
                  ("That's about a dollar and five cents a share.", "That's about $1.05 a share."),
                  ("So it goes up, and that's accretive.", "So it goes up, and that's accretive.")],
             art=lambda t0, d, seg: picture("ad_accrete", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .6), "thump", .1), (("s", 0, 2.2), "tick", .04), (("s", 1, .5), "tick", .04),
                  (("e", 2, -.5), "ding", .07)]),
        dict(tag="AT 30x", size=52, hl=["30x", "15 shares.", "96 cents.", "dilutive."],
             say=[("Pay thirty times instead, and you issue fifteen shares.", "Pay 30x instead, and you issue 15 shares."),
                  ("A hundred and ten dollars over a hundred and fifteen shares is about ninety six cents.",
                   "$110 over 115 shares is about 96 cents."),
                  ("So it falls, and that's dilutive.", "So it falls, and that's dilutive.")],
             art=lambda t0, d, seg: picture("ad_dilute", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "paper", .06), (("s", 0, 1.7), "tick", .04), (("s", 1, 2.0), "tick", .04),
                  (("e", 2, -.5), "thump", .12)]),
        dict(tag="THE RULE", size=56, hl=["lower multiple", "higher one,"],
             say=[("The rule: pay a lower multiple than your own, and it rises.", "The rule: pay a lower multiple than your own, and it rises."),
                  ("Pay a higher one, and it falls.", "Pay a higher one, and it falls.")],
             art=lambda t0, d, seg: picture("ad_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "knock", .07), (("s", 0, 1.6), "pop", .06), (("s", 1, .7), "pop", .06)]),
    ],
    close=dict(say=[("So what price makes it break even?", "So what price makes it break even?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED},
               pic=lambda t0, d: picture("ad_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
