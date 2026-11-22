"""
Reel B, 22 Nov 2026: Format E (a myth) on the story engine (build/story.py), narrator HEART (Kokoro af_heart,
en-us, 0.9), black ground, -16 LUFS for Instagram. The myth: a stock split makes shareholders richer.

A worked illustration with round numbers of our own; no company or market reaction is claimed. Mechanically, a
2-for-1 split gives every holder two shares for each one held and the share price is adjusted to half; the company,
its profit and its cash do not change. Before tax and trading costs; no claim about how prices move after splits.

Every number, worked:
    Before:         100 shares x $50 = $5,000.
    The split:      2 for 1: 100 x 2 = 200 shares; each is half as much of the company, so 50 / 2 = $25.
    After:          200 x 25 = $5,000 (unchanged).
    Per share:      EPS $2.50 becomes 2.50 / 2 = $1.25; the multiple 50 / 2.50 = 20x and 25 / 1.25 = 20x.
    The dividend:   $1 a share on 100 shares = $100; after, 50 cents on 200 shares = $100.
    Close (asked):  a 1-for-5 reverse split of 100 shares at $4: 100 / 5 = 20 shares at 4 x 5 = $20 ($400 either
                    way; not given).
    Comment bonus:  a 3-for-2 split of 100 shares at $60: 150 shares at $40 ($6,000 either way).

22 Nov, from the performance data (docs/daily/quality-log.md row of 22 Nov): a hook of 12 words, a number and a
yes/no question, on the story engine. Format E (a myth), last used 19 Nov; Reel A today is Format D.

    python3 build/reels_stock-split.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "2:1", GOLD, 150), (770, 560, "SHARE", "#3B3F48", 170),
                                              (-100, 1030, "$50", "#0F766E", 150), (770, 1120, "x2", GOLD, 140)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-stock-split",
    kicker="IB MYTH",
    mood="playful",
    cover=dict(at=("e", 0, 1, .3), lines=["A 2-for-1 split", "doubles your shares.", "Are you richer?"],
               hl={"2-for-1": GOLD, "doubles": GOLD, "richer?": RED}, avoid=["$5,000", "$25", "SAME"]),
    beats=[
        dict(tag="THE MYTH", size=60, hold=.6, hl=["2-for-1", "doubles", "richer?"],
             say=[("A two for one split doubles your shares.", "A 2-for-1 split doubles your shares."),
                  ("So are you any richer?", "So are you any richer?")],
             art=lambda t0, d, seg: picture("sp_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "tick", .04), (("s", 0, .45), "paper", .06), (("s", 0, .62), "pop", .05), (("s", 1, .2), "pop", .05),
                  (("s", 1, .5), "clink", .05)]),
        dict(tag="YOUR SHARES", size=56, hl=["$50", "$5,000.", "200."],
             say=[("You own a hundred shares at fifty dollars each, so five thousand.", "You own 100 shares at $50 each, so $5,000."),
                  ("Split them, and now you own two hundred.", "Split them, and now you own 200.")],
             art=lambda t0, d, seg: picture("sp_shares", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "tick", .04), (("s", 0, .45), "pop", .05), (("s", 0, .5), "tick", .04), (("s", 0, .85), "clink", .05),
                  (("s", 1, .1), "paper", .06), (("s", 1, .55), "pop", .05)]),
        dict(tag="THE PRICE", size=54, hl=["half", "$25.", "$5,000."],
             say=[("But each share is now half as much of the company, so the price halves to twenty five.",
                   "But each share is now half as much of the company, so the price halves to $25."),
                  ("Two hundred times twenty five: still five thousand.", "200 times $25: still $5,000.")],
             art=lambda t0, d, seg: picture("sp_price", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .35), "tick", .04), (("s", 0, .55), "tick", .04), (("s", 0, .8), "knock", .06), (("s", 1, .3), "thump", .07),
                  (("s", 1, .8), "pop", .05)]),
        dict(tag="THE COMPANY", size=54, hl=["same", "$1.25,", "20x."],
             say=[("The company hasn't changed: same profit, same cash.", "The company hasn't changed: same profit, same cash."),
                  ("Earnings per share fall to a dollar twenty five, so it still trades at twenty times.",
                   "Earnings per share fall to $1.25, so it still trades at 20x.")],
             art=lambda t0, d, seg: picture("sp_company", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "pop", .05), (("s", 0, .5), "pop", .05), (("s", 0, .7), "pop", .05), (("s", 1, .2), "tick", .04),
                  (("s", 1, .6), "pop", .05), (("s", 1, .85), "clink", .05)]),
        dict(tag="THE TRUTH", size=56, hl=["same", "slices."],
             say=[("A split just cuts the same pie into more slices.", "A split just cuts the same pie into more slices."),
                  ("Your piece of the company is exactly the same size.", "Your piece of the company is exactly the same size.")],
             art=lambda t0, d, seg: picture("sp_myth", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .45), "tick", .04), (("s", 0, .65), "tick", .04), (("s", 1, .15), "paper", .05), (("s", 1, .6), "thump", .07)]),
        dict(tag="EVEN THE DIVIDEND", size=54, hl=["price", "value", "50", "cents,"],
             say=[("It changes the price of a share, not the value of the company.", "It changes the price of a share, not the value of the company."),
                  ("A dollar dividend becomes fifty cents, on twice the shares.", "A $1 dividend becomes 50 cents, on twice the shares.")],
             art=lambda t0, d, seg: picture("sp_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "knock", .06), (("s", 0, .7), "pop", .05), (("s", 1, .2), "clink", .05), (("s", 1, .5), "clink", .05),
                  (("s", 1, .85), "pop", .05)]),
    ],
    close=dict(say=[("Now a one for five reverse split, on a hundred shares at four dollars.", "Now a 1-for-5 reverse split, on 100 shares at $4."),
                    ("How many shares do you hold, and at what price?", "How many shares do you hold, and at what price?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED},
               pic=lambda t0, d: picture("sp_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",        # the grid cover (reel_cover.py) on the Reel's own ground
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
