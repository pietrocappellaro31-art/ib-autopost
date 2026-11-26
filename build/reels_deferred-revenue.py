"""
Reel A, 26 Nov 2026 (slot A 12:30 ET): Format C (one surprising concept) on the story engine (build/story.py),
narrator HEART (Kokoro af_heart, en-us, 0.9), black ground, -16 LUFS for Instagram.
$120 comes in, January's revenue is $10: where did the rest go? Deferred revenue.

A worked illustration with round numbers of our own and an unnamed gym; no company, price or statistic is claimed.
Assumptions, said or on screen: a one-year pass for $120 paid in full on 1 January; the gym delivers the service
evenly over the 12 months, so it books revenue evenly (accrual accounting: revenue when earned); costs left out to
keep one idea on screen.

Every number worked:
    Per month:       $120 / 12 = $10.
    1 January:       cash +$120 (all of it, day one).
    End of January:  revenue $10 (one month delivered); the other 120 - 10 = $110 is deferred revenue, a liability
                     (service still owed). Balance sheet: cash $120 = deferred revenue $110 + earned $10 (equity,
                     through retained earnings, ignoring costs and tax).
    Each month:      $10 moves from deferred revenue to revenue: $110, $100, ... , $10, $0.
    End of December: deferred revenue 110 - 11 x 10 = $0; revenue 12 x 10 = $120.
    Rule:            cash counts when it's paid, revenue when it's earned.
    Close (asked):   a 6-month pass, $60, paid 1 March: March revenue 60 / 6 = $10; still owed at the end of March
                     60 - 10 = $50 (not given).
    Comment bonus:   the $120 yearly pass, three months in: deferred revenue left 120 - 3 x 10 = $90.

Hook (24 Nov standard: five candidates, scored 1 to 5 on clash / number in the first three words / second person /
length on screen / would someone send it to a friend preparing for interviews):
    1. "$120 comes in. January's revenue: just $10. So where did the rest go?"   clash 5, number 5, you 2, 12 words 4, send 5 = 21
    2. "A gym takes $120 and books $10 of revenue. Is that fraud?"               clash 4, number 4, you 1, 11 words 4, send 4 = 17
       (the fraud angle oversells a normal rule)
    3. "You pay $120 up front. Your gym books $10. Why?"                         clash 4, number 4, you 5, 9 words 5, send 4 = 22
       (hard to show on the cover: three short lines that read as complaints, not a puzzle)
    4. "Cash $120, revenue $10, same month. Both are right."                     clash 4, number 5, you 1, 8 words 5, send 4 = 19
    5. "Answer before the year ends: when is $120 of cash not revenue?"          clash 2, number 2, you 1, 12 words 4, send 3 = 12
    Chosen: 1 (21; picked over 3 because the two numbers sit side by side on screen as two columns from frame 0, the
    shape of our best Reels: CASH IN $120 against REVENUE $10, the question last).

26 Nov, from the performance data (quality-log row of 26 Nov): plain money words in the hook (no multiple, no
acronym), the cash and three-statement family (the profit vs cash Reel, 1,145), Format C.

    python3 build/reels_deferred-revenue.py HEART
"""

import sys

import scenes_1126  # noqa: F401  (registers the dr_ scenes)
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
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "$120", "#3B3F48", 150), (770, 560, "JAN", "#0F766E", 150),
                                              (-100, 1030, "$10", "#3B3F48", 150), (770, 1120, "$", GOLD, 130)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


EP = dict(
    slug="w2-deferred-revenue",
    kicker="IB CONCEPT",
    mood="curious",
    cover=dict(at=("e", 0, 0, .2), lines=["$120 comes in.", "January's revenue: $10.", "Where did the rest go?"],
               hl={"$120": GOLD, "$10.": RED, "rest": RED}, avoid=["$110", "LIABILITY"]),
    beats=[
        dict(tag="THE CLASH", size=58, hold=.6, hl=["$120", "$10.", "rest"],
             say=[("A hundred and twenty dollars comes in, and January's revenue is just ten.", "$120 comes in. January's revenue: just $10."),
                  ("So where did the rest go?", "So where did the rest go?")],
             art=lambda t0, d, seg: picture("dr_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "thump", .07), (("s", 0, .3), "clink", .05), (("s", 0, .75), "pop", .05), (("s", 1, .1), "tick", .04),
                  (("s", 1, .4), "pop", .05)]),
        dict(tag="THE SET-UP", size=54, hl=["$120,", "$10"],
             say=[("A gym sells a year's pass for a hundred and twenty dollars, paid on January first.", "A gym sells a year's pass for $120, paid on 1 January."),
                  ("That's ten dollars a month.", "That's $10 a month.")],
             art=lambda t0, d, seg: picture("dr_setup", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "clink", .05), (("s", 0, .55), "thump", .06), (("s", 1, .05), "tick", .04), (("s", 1, .4), "tick", .04),
                  (("s", 1, .8), "pop", .05)]),
        dict(tag="CASH OR REVENUE", size=54, hl=["$120", "delivers:", "month."],
             say=[("All the money arrives on day one.", "All $120 arrives on day one."),
                  ("But revenue only counts as the gym delivers, ten dollars a month.", "But revenue only counts as the gym delivers: $10 a month.")],
             art=lambda t0, d, seg: picture("dr_cash", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "clink", .05), (("s", 0, .3), "thump", .06), (("s", 1, .1), "tick", .04), (("s", 1, .5), "tick", .04),
                  (("e", 1, .1), "pop", .05)]),
        dict(tag="THE ANSWER", size=54, hl=["$110", "deferred", "liability:"],
             say=[("The other hundred and ten goes on the balance sheet as deferred revenue.", "The other $110 goes on the balance sheet as deferred revenue."),
                  ("It's a liability, gym time it still owes.", "It's a liability: gym time it still owes.")],
             art=lambda t0, d, seg: picture("dr_answer", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .1), "pop", .05), (("s", 0, .4), "paper", .05), (("s", 1, .05), "thump", .07), (("s", 1, .55), "pop", .05),
                  (("s", 1, .75), "pop", .05)]),
        dict(tag="THE YEAR", size=54, hl=["$10", "$0,", "$120."],
             say=[("Each month, ten dollars moves from that liability to revenue.", "Each month, $10 moves from that liability to revenue."),
                  ("By December it owes nothing, and revenue's a hundred and twenty.", "By December it owes $0, and revenue's $120.")],
             art=lambda t0, d, seg: picture("dr_year", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .2), "tick", .04), (("s", 0, .5), "tick", .04), (("s", 0, .8), "tick", .04), (("s", 1, .2), "tick", .04),
                  (("s", 1, .6), "thump", .07)]),
        dict(tag="THE RULE", size=52, hl=["paid,", "earned.", "hasn't"],
             say=[("Cash counts when it's paid, and revenue counts when it's earned.", "Cash counts when it's paid, and revenue counts when it's earned."),
                  ("So a company can hold cash it hasn't earned.", "So a company can hold cash it hasn't earned.")],
             art=lambda t0, d, seg: picture("dr_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .05), "pop", .05), (("s", 0, .5), "pop", .05), (("s", 1, .1), "knock", .05), (("s", 1, .35), "pop", .05)]),
    ],
    close=dict(say=[("Six months for sixty dollars, paid March first.", "6 months for $60, paid 1 March."),
                    ("What's March revenue, and what's still owed?", "March revenue? Still owed?"),
                    ("Answer in the comments, and follow for tomorrow's.", "Answer in the comments, and follow for tomorrow's.")],
               cols={"comments,": RED, "follow": RED}, bar=True, art_w=720, art_h=576, size=80,
               pic=lambda t0, d: picture("dr_asks", t0, d, w=720, h=576)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean master; the posted file is the scored master made from it (master.py scored)
    lufs=-16,
    theme="black",
    room=.0003,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]), keep_voice="--keep-voice" in sys.argv)
