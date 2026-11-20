"""
YouTube Short, Format C (one surprising concept), 20 Nov 2026, on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9), black ground. Cut from YouTube #13 (19 Nov, "109% of GameStop Was Sold Short. How Is
That Possible?", build/youtube_ep013.py): the film's own puzzle (chapter 3, the lending chain), with the film's source.

The puzzle: a company has 100 shares and no more exist. How can 109 of them be sold short? Arithmetic of lending, true
in any country: a lent share is sold to a buyer who can lend it again, and every lender's account still counts it.

Our illustration (Ann, Ben and Cal are not real people; the mechanism is the SEC staff's, below), checked in this run:
    Ann owns 100. She lends them to a short seller, who sells them to Ben.
        sold short 100; counted as owned 100 (Ann, still shown in her account) + 100 (Ben) = 200; shares still 100.
    Ben lends his 100, and they are sold to Cal.
        sold short 100 + 100 = 200; counted as owned 100 + 100 + 100 = 300; shares still 100.
    Short interest = shares sold short / shares outstanding (SEC p. 25): 100 / 100 = 100% after one loan, 200% after two.
    So above 100% needs only some shares lent and sold more than once: 109 of 100 is 100 + 9 lent a second time.
    The close (not answered on screen): lent and sold three times each, 300 / 100 = 300%.

Source (opened again in this run, 20 Nov 2026):
    [SEC] SEC staff, "Staff Report on Equity and Options Market Structure Conditions in Early 2021", 14 Oct 2021
        (https://www.sec.gov/files/staff-report-equity-options-market-struction-conditions-early-2021.pdf; released
        18 Oct 2021, press release 2021-212, https://www.sec.gov/news/press-release/2021-212):
        p. 25: short interest "the ratio of shares currently sold short to shares outstanding";
        pp. 25-26: GME short interest "hitting its high of 109.26% on December 31, 2020";
        p. 26: "Short interest can exceed 100%—as it did with GME—when the same shares are lent multiple times by
        successive purchasers." (quoted on screen, elided at the dash: "Short interest can exceed 100%... when the same
        shares are lent multiple times by successive purchasers.");
        p. 25 n. 74: "Short selling involves the sale of a stock that the seller does not own"; the seller "borrows the
        stock from someone else" and later covers "by purchasing it ... to give back to the lender".

Beats, checked (as said; 57.2 s):
    puzzle   100 shares, no more exist, 109 sold short: how? The question first, no setup (our round company).
    short    selling short: borrowing a share, selling it, buying one back later to return it [SEC n. 74].
    once     Ann lends her 100, sold to Ben; Ben owns them, Ann's account still shows 100; 100 sold short, 200 counted
             as owned (our illustration of SEC p. 26).
    twice    Ben lends them, sold to Cal: 200 short, 300 counted as owned, still 100 shares (same).
    gme      in 2020 GameStop's short interest hit 109% (109.26% on 31 Dec 2020, SEC pp. 25-26); staff at the market
             regulator say the same shares were lent multiple times (SEC p. 26, quoted on screen). Said "the market
             regulator" because the recogniser could not hear the letters S E C cleanly (heard "sex", "SESC", "SESE").
    rule     our reading of the arithmetic: short interest counts loans, not shares.
    close    lent and sold three times each: what's the short interest? (not answered). The film is the Related video.

    python3 build/shorts_lent-twice-109.py HEART
"""

import random
import sys

from motion import A
from sketch import picture, _ptag, ss_hook_steps, SS_SHORT_LEGS
from story import make, RED

TEAL_INK, GOLD, BLUE = "#5EC8B4", "#F2C35B", "#A9C2DF"
# 20 Nov: each picture is given its beat's own box (w 752, h = art_h): with h 640 in a shorter box the fitted
# drawing ran past the panel and its bottom was clipped (the counters on the first cuts)


def chip(label, fill, w=190, color="#fff"):
    return (f'<svg width="{w}" height="{w * .6:.0f}" viewBox="0 0 {w} {w * .6:.0f}" style="overflow:visible">'
            + _ptag(w / 2, w * .3, w * .95, label, fill, color, round(w * .2)) + "</svg>")


def floaters(total):
    """Faint tags drifting at the edges, clear of the text (never the hook's answer, LENT, nor the close's, 300%)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "SHORT", "#3B3F48", 180), (770, 560, "109%", RED, 180),
                                              (-100, 1030, "100 SHARES", "#3B3F48", 220), (770, 1120, "?", GOLD, 120)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill == GOLD else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


def rain(t0, dur):
    """Tags falling in under the comment ask, then bobbing (no 300%)."""
    rnd = random.Random(20)
    out = ""
    labs = [("LENT", "#3B3F48"), ("109%", RED), ("SOLD", GOLD), ("100", "#2E4F7A"), ("OWES", "#0F766E")]
    for k, (lab, fill) in enumerate(labs):
        x, y = rnd.uniform(-10 + 150 * k, 10 + 150 * k), rnd.uniform(1040, 1120)
        art = chip(lab, fill, rnd.uniform(130, 160), "#0A0A0A" if fill == GOLD else "#fff")
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px")
    return out


# the hook's eleven steps: a tick on each, a thump when the column crosses ALL 100, a knock on the ninth ghost share
HOOK_SFX = ([((lambda seg, i=i: ss_hook_steps(seg)[i] + .25), "tick", .035) for i in range(11)]
            + [((lambda seg: ss_hook_steps(seg)[9] + .3), "thump", .1), ((lambda seg: ss_hook_steps(seg)[10] + .45), "knock", .07)])

EP = dict(
    slug="shorts-lent-twice-109",
    kicker="MONEY MATHS",
    mood="tense",
    cover=dict(at=("e", 0, 2, .2), lines=["100 shares exist.", "109 are sold short.", "How?"],
               hl={"100": TEAL_INK, "109": RED, "How?": RED}, avoid=["LENT", "LOAN", "OWES"]),
    beats=[
        dict(tag="THE PUZZLE", size=62, hold=.45, art_h=560, hl=["100 shares.", "109", "How?"],
             say=[("A company has a hundred shares.", "A company has 100 shares."),
                  ("No more exist.", "No more exist."),
                  ("Yet a hundred and nine are sold short.", "Yet 109 are sold short."),
                  ("How?", "How?")],
             art=lambda t0, d, seg: picture("ss_hook", t0, d, seg=seg, w=752, h=560),
             sfx=HOOK_SFX + [(("s", 3, .1), "pop", .06)]),
        dict(tag="SHORT SELLING", hl=["borrowing", "selling it,", "return it."],
             say=[("Selling short means borrowing a share, selling it, and buying one back later to return it.",
                   "Selling short means borrowing a share, selling it, and buying one back later to return it.")],
             art=lambda t0, d, seg: picture("ss_short", t0, d, seg=seg, w=752, h=640),
             # the four legs land: borrow, sell, buy back (paper), return (a clink on the lender's hand)
             sfx=[((lambda s, f=f: s[0][0] + f * (s[0][1] - s[0][0]) + .5), "paper", .05) for f in SS_SHORT_LEGS[:3]]
                 + [((lambda s: s[0][0] + SS_SHORT_LEGS[3] * (s[0][1] - s[0][0]) + .55), "clink", .06)]),
        dict(tag="LENT ONCE", size=50, art_h=470, hl=["Ben.", "still shows", "her 100.", "100 sold short,", "200"],
             say=[("Ann lends her hundred shares to a short seller, who sells them to Ben.",
                   "Ann lends her 100 shares to a short seller, who sells them to Ben."),
                  ("Ben owns them now, but Ann's account still shows her hundred.",
                   "Ben owns them now, but Ann's account still shows her 100."),
                  ("A hundred sold short, two hundred counted as owned.", "100 sold short, 200 counted as owned.")],
             art=lambda t0, d, seg: picture("ss_once", t0, d, seg=seg, w=752, h=470),
             # the bundle's legs take 0.9 s (ss_once): the paper and the clink on their landings
             sfx=[((lambda s: s[0][0] + .3 * (s[0][1] - s[0][0]) + .85), "paper", .05),
                  ((lambda s: s[0][0] + .75 * (s[0][1] - s[0][0]) + .85), "clink", .06),
                  ((lambda s: s[2][0] + .12 * (s[2][1] - s[2][0])), "knock", .06),
                  ((lambda s: s[2][0] + .62 * (s[2][1] - s[2][0])), "knock", .06)]),
        dict(tag="LENT AGAIN", size=54, art_h=520, hl=["Cal.", "200 sold short,", "300", "only 100"],
             say=[("Then Ben lends them as well, and they're sold to Cal.",
                   "Then Ben lends them as well, and they're sold to Cal."),
                  ("Two hundred sold short, three hundred counted as owned.", "200 sold short, 300 counted as owned."),
                  ("Still only a hundred shares.", "Still only 100 shares.")],
             art=lambda t0, d, seg: picture("ss_twice", t0, d, seg=seg, w=752, h=520),
             sfx=[((lambda s: s[0][0] + .25 * (s[0][1] - s[0][0]) + .55), "paper", .05),
                  ((lambda s: s[0][0] + .75 * (s[0][1] - s[0][0]) + .55), "clink", .06),
                  ((lambda s: s[1][0] + .1 * (s[1][1] - s[1][0])), "knock", .06),
                  ((lambda s: s[1][0] + .6 * (s[1][1] - s[1][0])), "knock", .06),
                  ((lambda s: s[2][0] + .15 * (s[2][1] - s[2][0]) + .2), "thump", .1)]),
        dict(tag="IT HAPPENED", size=54, art_h=560, hl=["109%.", "lent multiple times."],
             say=[("In twenty twenty, GameStop's short interest hit a hundred and nine percent.",
                   "In 2020, GameStop's short interest hit 109%."),
                  ("Staff at the market regulator say the same shares were lent multiple times.",
                   "Staff at the market regulator say the same shares were lent multiple times.")],
             art=lambda t0, d, seg: picture("ss_gme", t0, d, seg=seg, w=752, h=560),
             # the shares bar lands (1.2 s), the short bar lands and +9.26 pops (2.1 s), the quote starts wiping in
             sfx=[((lambda s: s[0][0] + .08 * (s[0][1] - s[0][0]) + 1.2), "thump", .08),
                  ((lambda s: s[0][0] + .45 * (s[0][1] - s[0][0]) + 2.1), "pop", .06),
                  ((lambda s: s[1][0] + .05 * (s[1][1] - s[1][0])), "paper", .06)]),
        dict(tag="THE READING", size=64, art_h=600, hold=1.1, hl=["loans,", "shares."],
             say=[("So short interest counts loans, not shares.", "So short interest counts loans, not shares.")],
             art=lambda t0, d, seg: picture("ss_rule", t0, d, seg=seg, w=752, h=600),
             sfx=[((lambda s: s[0][0] + .8 * (s[0][1] - s[0][0]) + .2), "paper", .05)]
                 + [((lambda s, j=j: s[0][1] - .2 + 1.0 * j / 3 + .1), "tick", .04) for j in range(4)]),
    ],
    close=dict(say=[("If every share is lent and sold three times, what's the short interest?",
                     "If every share is lent and sold three times, what's the short interest?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED}, art=rain,
               pic=lambda t0, d: picture("ss_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean mix is the score gate's reference; the delivered file is the scored one (17 Nov)
    lufs=-14,
    room=.0003,
)

if __name__ == "__main__":
    if "remix" in sys.argv:
        from story import remix
        remix(EP, "HEART")
    else:
        make(EP, *(sys.argv[1:2] or ["HEART"]))
