"""
Reel B, 19 Nov 2026: Format E (a myth, then the truth) on the story engine (build/story.py), narrator HEART (Kokoro
af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram. The buyback myth: "buy back 10% of your shares and EPS
rises 10%". With idle cash it rises about 11%; once the interest the cash was earning is counted, about 3%.

A worked illustration with round numbers of our own; no company is claimed. One year of earnings, a 25% tax rate,
cash earning 5% before tax, shares bought at the market price (no premium, no fees).

Every number, worked:
    Company:    earnings $100, 100 shares: EPS 100 / 100 = $1.00. At 20x earnings: price 20 x $1 = $20 a share.
    Buyback:    10% of the shares = 10 shares x $20 = $200 of cash; shares 100 - 10 = 90.
    Idle cash:  EPS 100 / 90 = 1.1111, said "about one dollar and eleven cents"; +11.1%, said "up eleven percent,
                not ten" (1 / 0.9 - 1 = 11.1%).
    The catch:  the $200 earned 5% = $10 a year before tax; after 25% tax 10 x 0.75 = $7.50 of earnings lost.
    Real EPS:   (100 - 7.50) / 90 = 92.50 / 90 = 1.0278, said "about one dollar and three cents"; +2.8%, said "up about
                three percent".
    The rule:   at 20x each share earns 1 / 20 = 5% of its price (the earnings yield); the cash earned 5% x 0.75 =
                3.75% after tax; 5% > 3.75%, so the buyback adds to EPS.
    Close (asked): at 40x, price $40, 10 shares cost $400, lost interest 400 x 5% x 0.75 = $15; EPS (100 - 15) / 90 =
                0.944: it falls (earnings yield 2.5% < 3.75%).
    Comment bonus: at 20x, $300 of cash buys 15 shares; if the cash earned nothing, EPS 100 / 85 = $1.18 (about 17.6% up).

19 Nov, from the performance data: number-led hook, Format E (the first Reel told as a myth); Reel A today is C.

    python3 build/reels_buyback-eps.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "EPS", GOLD, 160), (770, 560, "$20", "#0F766E", 160),
                                              (-100, 1030, "10%", GOLD, 150), (770, 1120, "$1", "#0F766E", 150)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-buyback-eps",
    kicker="IB MYTH",
    mood="playful",
    cover=dict(at=("e", 0, 0, .3), lines=["Buy back 10% of your shares.", "EPS goes up 10%?"],
               hl={"10%": GOLD, "10%?": RED}, avoid=["$1.11", "$1.03", "11%", "3%"]),
    beats=[
        dict(tag="THE MYTH", size=58, hold=.4, hl=["10%", "10%, right?"],
             say=[("Buy back ten percent of your shares, and earnings per share go up ten percent, right?",
                   "Buy back 10% of your shares, and earnings per share go up 10%, right?")],
             art=lambda t0, d, seg: picture("bb_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "pop", .05), (("s", 0, .8), "pop", .05), (("s", 0, 3.0), "thump", .08), (("e", 0, -.3), "knock", .07)]),
        dict(tag="THE COMPANY", hold=.35, size=56, hl=["$100", "$1 each.", "$20."],
             say=[("A company earns a hundred dollars on a hundred shares: one dollar each.",
                   "A company earns $100 on 100 shares: $1 each."),
                  ("At twenty times, a share costs twenty dollars.",
                   "At 20x, a share costs $20.")],
             art=lambda t0, d, seg: picture("ad_buyer", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "thump", .08), (("s", 0, 1.6), "tick", .04), (("e", 0, -.6), "ding", .05), (("s", 1, .3), "pop", .06)]),
        dict(tag="THE BUYBACK", hold=.35, size=52, hl=["$200", "$1.11.", "11%,"],
             say=[("It spends two hundred dollars of cash buying back ten shares.",
                   "It spends $200 of cash buying back 10 shares."),
                  ("A hundred dollars over ninety shares is about one dollar and eleven cents.",
                   "$100 over 90 shares is about $1.11."),
                  ("Up eleven percent, not ten.", "Up 11%, not 10.")],
             art=lambda t0, d, seg: picture("bb_buyback", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .4), "clink", .07), (("s", 0, 1.9), "pop", .04), (("s", 1, .3), "tick", .04), (("s", 1, 1.4), "tick", .04),
                  (("e", 1, -.5), "ding", .05), (("s", 2, .2), "pop", .06)]),
        dict(tag="THE CATCH", hold=.35, size=52, hl=["5%,", "$10", "$7.50"],
             say=[("But that cash was earning five percent, or ten dollars a year.",
                   "But that cash was earning 5%, or $10 a year."),
                  ("After a twenty five percent tax, seven dollars and fifty cents is gone.",
                   "After a 25% tax, $7.50 is gone.")],
             art=lambda t0, d, seg: picture("bb_catch", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "clink", .05), (("s", 0, 1.0), "pop", .05), (("e", 0, -.6), "tick", .04),
                  (("s", 1, .4), "knock", .07), (("e", 1, -.5), "thump", .09)]),
        dict(tag="THE REAL NUMBER", hold=.35, size=52, hl=["$1.03.", "3%,"],
             say=[("Ninety two dollars and fifty cents, over ninety shares, is about one dollar and three cents.",
                   "$92.50, over 90 shares, is about $1.03."),
                  ("Up about three percent, not ten.", "Up about 3%, not 10.")],
             art=lambda t0, d, seg: picture("bb_real", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "paper", .06), (("s", 0, 2.0), "tick", .04), (("e", 0, -.6), "ding", .05), (("s", 1, 1.0), "thump", .09)]),
        dict(tag="THE RULE", hold=.35, size=52, hl=["5%", "3.75%"],
             say=[("Each share earns five percent of its price.",
                   "Each share earns 5% of its price."),
                  ("The cash earned three point seven five percent after tax, so the buyback wins.",
                   "The cash earned 3.75% after tax, so the buyback wins.")],
             art=lambda t0, d, seg: picture("bb_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "clink", .06), (("e", 0, -.8), "pop", .05), (("s", 1, .6), "tick", .04), (("e", 1, -.4), "ding", .05)]),
    ],
    close=dict(say=[("At forty times, does the same buyback still lift earnings per share?",
                     "At 40x, does the same buyback still lift earnings per share?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED},
               pic=lambda t0, d: picture("bb_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
