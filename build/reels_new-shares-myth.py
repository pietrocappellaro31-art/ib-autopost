"""
Reel B, 26 Nov 2026 (slot B 18:00 ET): Format E (a myth) on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
10% of a company, then just 8%: did you lose money? New shares sold at a fair price.

A worked illustration with round numbers of our own; no company, share price or statistic is claimed, and no
forecast. Assumptions, said or on screen: the company is worth $1,000 before the new shares (100 shares at $10);
the new shares are sold for cash, and the cash raised adds its own amount to the company's value (no fees, no news,
nothing else changes); "worth" means value per share = company value / shares.

Every number worked:
    Before:       $1,000 / 100 shares = $10 a share; you hold 10 shares: 10 / 100 = 10%, 10 x $10 = $100.
    New shares:   25 sold at $10 = $250 cash; shares 100 + 25 = 125; your stake 10 / 125 = 8%.
    After:        value 1,000 + 250 = $1,250; per share 1,250 / 125 = $10; your 10 shares 10 x 10 = $100: the same.
    The catch:    sold at $6 instead: 25 x 6 = $150; value 1,000 + 150 = $1,150; per share 1,150 / 125 = $9.20;
                  your 10 shares 10 x 9.20 = $92 (an $8 loss), the value handed to the new buyers.
    Rule:         a smaller slice of a bigger pie can be worth the same (8% x $1,250 = $100 = 10% x $1,000);
                  what matters is the price the new shares sell for.
    Close (asked):  sold at $14: 25 x 14 = $350; 1,350 / 125 = $10.80; your 10 shares $108 (not given).
    Comment bonus:  100 new shares at $10: stake 10 / 200 = 5%, value 2,000 / 200 = $10 a share, still $100.

Hook (24 Nov standard: five candidates, scored 1 to 5 on clash / number in the first three words / second person /
length on screen / would someone send it to a friend preparing for interviews):
    1. "10% of a company. Then just 8%. Did you just lose money?"   clash 5, number 5, you 4, 12 words 4, send 5 = 23
    2. "Your stake drops from 10% to 8%. Did you lose money?"         clash 5, number 3, you 5, 11 words 5, send 5 = 23
    3. "New shares mean dilution, so you lose. Nope."                  clash 3, number 1, you 2, 8 words 5, send 3 = 14
    4. "The company sold 25 new shares. Are you poorer?"               clash 3, number 3, you 4, 9 words 5, send 4 = 19
    5. "Answer before the pie grows: is a smaller slice less money?"   clash 3, number 1, you 2, 11 words 5, send 4 = 15
    Chosen: 1 (tied with 2 at 23; the standard's number in the first three words breaks the tie, and both pies sit
    on the panel from frame 0, 10% against 8%, the question last).

26 Nov, from the performance data (quality-log row of 26 Nov): plain money words in the hook (no multiple, no
acronym), the equity family and the myth format (the buyback myth, 1,152 reach and 19 saves), Format E.

    python3 build/reels_new-shares-myth.py HEART
"""

import sys

import scenes_1126  # noqa: F401  (registers the ns_ scenes)
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "10%", "#3B3F48", 150), (770, 560, "NEW", "#0F766E", 150),
                                              (-100, 1030, "8%", "#3B3F48", 150), (770, 1120, "$", GOLD, 130)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-new-shares-myth",
    kicker="IB MYTH",
    mood="curious",
    cover=dict(at=("e", 0, 0, .2), lines=["10% of a company.", "Then just 8%.", "Did you lose money?"],
               hl={"10%": GOLD, "8%.": RED, "money?": RED}, avoid=["SAME", "$1,250"]),
    beats=[
        dict(tag="THE MYTH", size=58, hold=.6, hl=["10%", "8%.", "money?"],
             say=[("Ten percent of a company, and then just eight percent.", "10% of a company. Then just 8%."),
                  ("Did you just lose money?", "Did you just lose money?")],
             art=lambda t0, d, seg: picture("ns_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "thump", .07), (("s", 0, .7), "knock", .05), (("s", 1, .05), "pop", .05), (("s", 1, .3), "tick", .04)]),
        dict(tag="THE SET-UP", size=54, hl=["$1,000:", "$10.", "10%,", "$100."],
             say=[("A company's worth a thousand dollars, a hundred shares at ten each.", "A company's worth $1,000: 100 shares at $10."),
                  ("You hold ten, so ten percent, worth a hundred dollars.", "You hold 10: 10%, worth $100.")],
             art=lambda t0, d, seg: picture("ns_setup", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "tick", .04), (("s", 0, .45), "tick", .04), (("s", 0, .75), "tick", .04), (("s", 1, .1), "pop", .05),
                  (("s", 1, .7), "clink", .05)]),
        dict(tag="NEW SHARES", size=54, hl=["25", "$250", "8%."],
             say=[("It sells twenty five new shares at ten dollars, for two hundred and fifty.", "It sells 25 new shares at $10: $250 in."),
                  ("That makes a hundred and twenty five shares, and your ten are eight percent.", "That's 125 shares, and your 10 are 8%.")],
             art=lambda t0, d, seg: picture("ns_new", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "clink", .05), (("s", 0, .5), "clink", .05), (("s", 0, .75), "clink", .05), (("s", 1, .1), "pop", .05),
                  (("s", 1, .55), "pop", .05)]),
        dict(tag="THE ANSWER", size=54, hl=["$1,250:", "$10", "$100."],
             say=[("But the company's now worth twelve hundred and fifty, still ten dollars a share.", "But it's now worth $1,250: still $10 a share."),
                  ("So your ten shares are still worth a hundred.", "So your 10 shares are still worth $100.")],
             art=lambda t0, d, seg: picture("ns_answer", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "pop", .05), (("s", 0, .45), "pop", .05), (("s", 0, .65), "pop", .05), (("s", 1, .05), "tick", .04),
                  (("s", 1, .6), "thump", .07)]),
        dict(tag="THE CATCH", size=54, hl=["cheap.", "$6", "$92."],
             say=[("It only hurts if the new shares go too cheap.", "It only hurts if the new shares go too cheap."),
                  ("At six dollars each, your ten shares fall to ninety two dollars.", "At $6 each, your 10 shares fall to $92.")],
             art=lambda t0, d, seg: picture("ns_catch", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .4), "pop", .05), (("s", 1, .05), "paper", .05), (("s", 1, .35), "clink", .05), (("s", 1, .6), "knock", .05),
                  (("s", 1, .85), "thump", .06)]),
        dict(tag="THE RULE", size=52, hl=["smaller", "bigger", "price"],
             say=[("A smaller slice of a bigger pie can be worth the same.", "A smaller slice of a bigger pie can be worth the same."),
                  ("What matters is the price the new shares sell for.", "What matters is the price the new shares sell for.")],
             art=lambda t0, d, seg: picture("ns_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .5), "pop", .05), (("s", 1, .1), "tick", .04), (("s", 1, .45), "tick", .04), (("s", 1, .8), "tick", .04)]),
    ],
    close=dict(say=[("Same twenty five shares, sold at fourteen dollars.", "Same 25 shares, sold at $14."),
                    ("What are your ten shares worth now?", "What are your 10 shares worth now?"),
                    ("Answer in the comments, and follow for tomorrow's.", "Answer in the comments, and follow for tomorrow's.")],
               cols={"comments,": RED, "follow": RED}, bar=True, art_w=720, art_h=576,
               pic=lambda t0, d: picture("ns_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]), keep_voice="--keep-voice" in sys.argv)
