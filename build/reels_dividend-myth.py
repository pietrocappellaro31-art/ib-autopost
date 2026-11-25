"""
Reel B, 25 Nov 2026 (slot B 18:00 ET): Format E (a myth) on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
A $1 dividend lands and your $50 share drops to $49: did you get paid? The dividend myth.

A worked illustration with round numbers of our own; no company, share price or statistic is claimed, and no
forecast. Assumptions, said or on screen: a share worth $50, part of it cash; a $1 cash dividend; in theory, all
else equal (no news, no market move), the price falls by about the dividend on the ex-dividend day (the first day a
buyer no longer gets it). Tax: whether and how much depends on the holder; we only say "if it's taxed".

Every number, worked:
    Before:         one share worth $50.
    Paid out:       $1 of the company's cash goes to you; the company is worth $1 a share less: 50 - 1 = $49.
    You:            $49 share + $1 cash = $50, the same as before.
    Tax:            if the $1 is taxed at any rate above 0, you keep less than $1: under $50 in total.
    Rule:           price before = price after + dividend (50 = 49 + 1): the dividend moves value, it doesn't make it.
    Close (asked):  $80 share, $5 dividend: about 80 - 5 = $75 right after (not given).
    Comment bonus:  the same cash spent on a buyback at $50 a share instead: in this simple case the price of the
                    shares left stays about $50 (cash and share count fall in proportion).

Hook (24 Nov standard: five candidates, scored 1 to 5 on clash / number in the first three words / second person /
length on screen / would someone send it to a friend preparing for interviews):
    1. "A $1 dividend lands. Your $50 share drops to $49. So did you get paid?"   clash 5, number 5, you 5, 14 words 3, send 5 = 23
    2. "Dividends are free money. Nope."                                          clash 3, number 1, you 1, 5 words 5, send 3 = 13
    3. "$1 dividend, $1 price drop. Who paid you?"                                clash 4, number 5, you 3, 8 words 5, send 4 = 21
    4. "You got $1 in dividends and you're no richer. Here's why."                clash 3, number 3, you 5, 11 words 5, send 3 = 19
       (gives the answer away)
    5. "Answer before the price drops: is a dividend free money?"                clash 2, number 1, you 1, 10 words 5, send 3 = 12
    Chosen: 1 (the two moves you can see on a statement, +$1 and -$1, and the question last; 13 words on screen
    with the question, the coin and the price tag both moving from frame 0).

25 Nov, from the performance data (docs/daily/quality-log.md row of 25 Nov): the myth format ("Buy back 10% ...
Nope.", 1,148 reach, 19 saves) and the equity family (shareholders' equity, our best share count); Format E.

    python3 build/reels_dividend-myth.py HEART
"""

import sys

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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "$1", "#3B3F48", 150), (770, 560, "$50", "#0F766E", 150),
                                              (-100, 1030, "DIV", "#3B3F48", 150), (770, 1120, "$", GOLD, 130)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-dividend-myth",
    kicker="IB MYTH",
    mood="curious",
    cover=dict(at=("e", 0, 1, .3), lines=["A $1 dividend lands.", "Your $50 share drops to $49.", "So did you get paid?"],
               hl={"$1": GOLD, "$49.": RED, "paid?": RED}, avoid=["SAME", "$50 total"]),
    beats=[
        dict(tag="THE MYTH", size=58, hold=.6, hl=["$1", "$49.", "paid?"],
             say=[("A one dollar dividend lands, and your fifty dollar share drops to forty nine.", "A $1 dividend lands. Your $50 share drops to $49."),
                  ("So did you get paid?", "So did you get paid?")],
             art=lambda t0, d, seg: picture("dv_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "thump", .07), (("s", 0, .35), "clink", .05), (("s", 0, .6), "tick", .04), (("s", 1, .1), "pop", .05)]),
        dict(tag="THE SET-UP", size=56, hl=["$50", "cash.", "$1"],
             say=[("Say a share is worth fifty dollars, and part of that is the company's cash.", "Say a share is worth $50, and part of that is the company's cash."),
                  ("It pays one dollar of that cash out to you.", "It pays $1 of that cash out to you.")],
             art=lambda t0, d, seg: picture("dv_setup", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "pop", .05), (("s", 0, .7), "pop", .05), (("s", 1, .4), "pop", .05), (("s", 1, .9), "clink", .05)]),
        dict(tag="THE DROP", size=54, hl=["less,", "less.", "$49"],
             say=[("The company now holds a dollar less, so each share is worth a dollar less.", "The company now holds $1 less, so each share is worth $1 less."),
                  ("In theory, the price drops to about forty nine on the ex-dividend day.", "In theory, it drops to about $49 on the ex-dividend day.")],
             art=lambda t0, d, seg: picture("dv_drop", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .3), "knock", .05), (("s", 0, .4), "pop", .05), (("s", 1, .05), "tick", .04), (("s", 1, .4), "tick", .04),
                  (("s", 1, .55), "pop", .05)]),
        dict(tag="THE ANSWER", size=56, hl=["$49", "$1", "$50,"],
             say=[("You now hold a forty nine dollar share and one dollar of cash.", "You now hold a $49 share and $1 of cash."),
                  ("That's fifty, the same as before.", "That's $50, the same as before.")],
             art=lambda t0, d, seg: picture("dv_answer", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "thump", .05), (("s", 0, .5), "clink", .05), (("s", 1, .05), "pop", .05), (("s", 1, .35), "pop", .05),
                  (("s", 1, .6), "thump", .07)]),
        dict(tag="THE CATCH", size=56, hl=["pocket", "taxed,", "behind."],
             say=[("It's like moving cash from one pocket to the other.", "It's like moving cash from one pocket to the other."),
                  ("And if that dollar's taxed, you end up a little behind.", "And if that $1 is taxed, you end up a little behind.")],
             art=lambda t0, d, seg: picture("dv_tax", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "clink", .04), (("s", 0, .5), "clink", .04), (("s", 1, .1), "pop", .05), (("s", 1, .3), "knock", .05),
                  (("s", 1, .6), "pop", .05)]),
        dict(tag="THE RULE", size=52, hl=["moves", "before", "after,", "dividend."],
             say=[("A dividend doesn't create value, it just moves it from the company to you.", "A dividend doesn't create value, it just moves it from the company to you."),
                  ("Price before equals price after, plus the dividend.", "Price before = price after + the dividend.")],
             art=lambda t0, d, seg: picture("dv_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "pop", .05), (("s", 0, .75), "thump", .07), (("s", 1, .05), "tick", .04), (("s", 1, .35), "tick", .04),
                  (("s", 1, .65), "tick", .04)]),
    ],
    close=dict(say=[("An eighty dollar share pays a five dollar dividend.", "$80 share, $5 dividend."),
                    ("What should it be worth right after?", "What should it be worth right after?"),
                    ("Answer in the comments, and follow for tomorrow's.", "Answer in the comments, and follow for tomorrow's.")],
               cols={"comments,": RED, "follow": RED}, bar=True, art_w=720, art_h=576,
               pic=lambda t0, d: picture("dv_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
