"""
Reel C, 25 Nov 2026 (slot C 21:00 ET): Format B (a short financial story) on the story engine (build/story.py),
narrator HEART (Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
$10 of inventory written off and profit falls $7.50: so why is cash up $2.50? A write-down through the three
statements, the classic interview walk-through.

A worked illustration with round numbers of our own and an invented shop (Leo's, said so in the caption); no company
or statistic is claimed. Assumptions, said or on screen: a 25% tax rate, and the write-down cuts taxable income (our
example's assumption; real tax rules on write-downs vary by country). "Cash up $2.50" means compared with no
write-down: the jackets were paid for earlier, so no cash moves on the day; the gain is the tax not paid.

Every number, worked:
    Income statement:   write-down -$10 before tax; tax 25% x 10 = $2.50 less; net income -10 + 2.50 = -$7.50.
    Cash flow:          start from net income -7.50, add back the $10 non-cash write-down: +$2.50.
    Balance sheet:      inventory -10, cash +2.50: assets -7.50; retained earnings (equity) -7.50: balances.
    Rule:               the cash effect is the tax saved: $10 x 25% = $2.50.
    Close (asked):      a $40 write-down: cash +40 x 25% = +$10 (net income -$30) (not given).
    Comment bonus:      $10 write-down at a 30% tax rate: net income -$7, cash +$3.

Hook (24 Nov standard: five candidates, scored 1 to 5 on clash / number in the first three words / second person /
length on screen / would someone send it to a friend preparing for interviews):
    1. "$10 of inventory written off. Profit falls $7.50. So why is cash up $2.50?"
                                                                             clash 5, number 5, you 1, 13 words 4, send 5 = 20
    2. "Write off $10 of jackets. Your cash goes UP. How?"                   clash 4, number 4, you 3, 10 words 5, send 4 = 20
       (three shouted words is a tell; "goes up" with no number is vaguer)
    3. "Profit down $7.50, cash up $2.50, same event. Walk me through it."   clash 5, number 4, you 2, 12 words 4, send 4 = 19
    4. "Your shop writes off $10 of stock. What happens to cash?"            clash 2, number 3, you 5, 11 words 5, send 4 = 19
    5. "Answer before the stamp lands: what does a $10 write-down do to cash?" clash 2, number 2, you 1, 13 words 4, send 3 = 12
    Chosen: 1 (two numbers moving in opposite directions, the question last; on screen from frame 0: the rack and
    its tag, a PROFIT plate with a falling arrow and a CASH plate with a rising one).

25 Nov, from the performance data (docs/daily/quality-log.md row of 25 Nov): the cash family (profit vs cash, debt
paydown, the loan through the three statements) and the evening slot, our strongest (1,522 and 1,210); Format B.

    python3 build/reels_writedown.py HEART
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "-$10", "#3B3F48", 170), (770, 560, "+$2.50", "#0F766E", 170),
                                              (-100, 1030, "TAX", "#3B3F48", 150), (770, 1120, "$", GOLD, 130)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-writedown-cash",
    kicker="IB TECHNICAL",
    mood="curious",
    cover=dict(at=("e", 0, 1, .3), lines=["$10 of inventory written off.", "Profit falls $7.50.", "So why is cash up $2.50?"],
               hl={"$10": GOLD, "$7.50.": RED, "$2.50?": RED}, avoid=["TAX NOT PAID", "BALANCES"]),
    beats=[
        dict(tag="THE PUZZLE", size=56, hold=.6, hl=["$10", "$7.50.", "$2.50?"],
             say=[("Ten dollars of inventory written off, and profit falls seven fifty.", "$10 of inventory written off. Profit falls $7.50."),
                  ("So why is cash up two fifty?", "So why is cash up $2.50?")],
             art=lambda t0, d, seg: picture("iw_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "thump", .07), (("s", 0, .2), "knock", .05), (("s", 0, .6), "tick", .04), (("s", 1, .2), "pop", .05),
                  (("s", 1, .45), "tick", .04)]),
        dict(tag="LEO'S SHOP", size=56, hl=["$10", "zero."],
             say=[("Leo's shop has ten dollars of winter jackets nobody will buy.", "Leo's shop has $10 of winter jackets nobody will buy."),
                  ("He writes them down to zero.", "He writes them down to $0.")],
             art=lambda t0, d, seg: picture("iw_shop", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .15), "paper", .05), (("s", 0, .6), "pop", .05), (("s", 1, .2), "tick", .04), (("s", 1, .45), "tick", .04),
                  (("s", 1, .6), "thump", .07)]),
        dict(tag="PROFIT", size=54, hl=["$10", "25%", "$7.50."],
             say=[("That's a ten dollar expense, so profit before tax falls ten.", "That's a $10 expense, so profit before tax falls $10."),
                  ("With tax at twenty five percent, profit only falls seven fifty.", "With tax at 25%, profit only falls $7.50.")],
             art=lambda t0, d, seg: picture("iw_income", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "thump", .05), (("s", 1, .05), "pop", .05), (("s", 1, .3), "clink", .05), (("s", 1, .55), "pop", .05)]),
        dict(tag="CASH", size=54, hl=["no", "back", "$2.50", "higher."],
             say=[("No cash left his shop, since he paid for them long ago.", "No cash left his shop: he paid for them long ago."),
                  ("Add back the ten, and cash ends up two fifty higher.", "Add back the $10, and cash ends up $2.50 higher.")],
             art=lambda t0, d, seg: picture("iw_cash", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "pop", .05), (("s", 0, .6), "paper", .05), (("s", 1, .1), "thump", .05), (("s", 1, .35), "pop", .05),
                  (("s", 1, .7), "clink", .05)]),
        dict(tag="BALANCE SHEET", size=56, hl=["$7.50.", "same", "balances."],
             say=[("On the balance sheet, assets fall seven fifty.", "On the balance sheet, assets fall $7.50."),
                  ("Equity falls by the same seven fifty, so it balances.", "Equity falls by the same $7.50, so it balances.")],
             art=lambda t0, d, seg: picture("iw_bs", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "paper", .05), (("s", 0, .5), "clink", .05), (("s", 0, .8), "pop", .05), (("s", 1, .2), "paper", .05),
                  (("s", 1, .6), "thump", .07)]),
        dict(tag="THE RULE", size=52, hl=["no", "tax", "$2.50", "25%."],
             say=[("A write-down costs no cash, but it cuts the tax bill.", "A write-down costs no cash, but it cuts the tax bill."),
                  ("Ten dollars times twenty five percent is the two fifty.", "$10 x 25% is the $2.50.")],
             art=lambda t0, d, seg: picture("iw_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "paper", .05), (("s", 0, .5), "pop", .05), (("s", 1, .05), "tick", .04), (("s", 1, .3), "tick", .04),
                  (("s", 1, .55), "tick", .04), (("s", 1, .8), "clink", .05)]),
    ],
    close=dict(say=[("Now Leo writes off forty dollars.", "Leo writes off $40."),
                    ("What happens to his cash?", "What happens to his cash?"),
                    ("Answer in the comments, and follow for tomorrow's.", "Answer in the comments, and follow for tomorrow's.")],
               cols={"comments,": RED, "follow": RED}, bar=True, art_w=720, art_h=576,
               pic=lambda t0, d: picture("iw_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
