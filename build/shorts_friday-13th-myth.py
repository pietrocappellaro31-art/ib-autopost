"""
YouTube Short, Format E (financial myth), 13 Nov 2026, the first Short on the story engine (build/story.py) and
in the narrator HEART (af_heart, en-us, 0.9). It remakes the morning's Friday the 13th quiz
(shorts_friday-13th-stocks.py, ISABELLA) as a myth told by one recurring character, the trader.

The myth: stocks do worse on Friday the 13th. The evidence:

Sources:
    [1] Dumitriu and Stefanescu, "The extended Friday the 13th Effect in the US stock returns", MPRA Paper
        95296, 2019, literature review: Kolb and Rodriguez (1987) found US returns on Fridays the 13th
        significantly lower than on other Fridays, and "their findings weren't confirmed by other studies".
        https://mpra.ub.uni-muenchen.de/95296/1/MPRA_paper_95296.pdf
    [2] J. Andrew Coutts, "Friday the thirteenth and the Financial Times Industrial Ordinary Shares Index
        1935-94", Applied Economics Letters 6(1), 1999, pp. 35-37: daily FT 30 returns, July 1935 to December
        1994 (almost 60 years): no evidence of a Friday the 13th effect; if anything, returns on Friday the 13th
        are higher than on other Fridays, in all six ten-year subsamples too.
        https://ideas.repec.org/a/taf/apeclt/v6y1999i1p35-37.html
    [3] DutchNews.nl, 12 Jun 2008, reporting the Dutch insurance association: "fewer fires and traffic accidents
        on Friday 13 than on ordinary Fridays"; an average 7,800 road accidents on ordinary Fridays, 7,500 on
        Friday 13. https://www.dutchnews.nl/2008/06/fewer_accidents_on_friday_13/

Beats, worked:
    myth      the claim, shown as a claim ("Right?"), not as fact.
    1987      [1]: lower returns in a US study (Kolb and Rodriguez). The drawing shows the direction only and says so.
    check     [1]: other studies did not confirm it.
    evidence  [2]: almost 60 years (Jul 1935 to Dec 1994) of UK shares.
    result    [2]: if anything higher than on other Fridays. Drawing: direction only, "illustration, not to scale".
    bonus     [3]: fewer road accidents, 7,500 against 7,800 (averages).
    verdict   the curse is a myth on this evidence; "superstition isn't a strategy" is our opinion, not advice.

    python3 build/shorts_friday-13th-myth.py HEART
"""

import random
import sys

from motion import A
from sketch import picture, cat_svg
from story import make, RED, TEAL

DUSK, BUTTER, MINT, SKY, PEACH, ROSE, LILAC, SAND = ("#DCD6E8", "#F5E6B8", "#D2E9E1", "#D6E2F3", "#F2D6BF", "#F6CFC3",
                                                     "#E2DAF0", "#EDE3D1")


def tile_svg(w, label="13", fill=RED, color="#fff"):
    h = round(w * .62)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 200 124" style="overflow:visible">'
            f'<rect x="3" y="3" width="194" height="118" rx="20" fill="{fill}" stroke="#0A0A0A" stroke-width="5"/>'
            f'<text x="100" y="86" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="72" '
            f'fill="{color}">{label}</text></svg>')


def cat(w):
    return f'<svg width="{w}" height="{w}" viewBox="-140 -260 300 280" style="overflow:visible">{cat_svg(0, 0, 1)}</svg>'


def floaters(total):
    """Faint black cats and 13 tiles drifting at the edges, clear of the text."""
    out = ""
    for k, (x, y, kind, w) in enumerate([(-120, 330, "cat", 200), (720, 520, "tile", 150), (-110, 980, "tile", 140),
                                         (720, 1100, "cat", 180)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.13">'
                + A(cat(w) if kind == "cat" else tile_svg(w), "float", 0, 1, amp=24, w=.5 + .1 * k, ph=k * 1.7) + "</div>")
    return out


def rain(t0, dur):
    """Black cats and 13 tiles falling in under the comment ask, then bobbing."""
    rnd = random.Random(1313)
    out = ""
    for k in range(9):
        x, y = rnd.uniform(-20 + 80 * k, 30 + 80 * k), rnd.uniform(1030, 1110)
        art = tile_svg(rnd.uniform(110, 140), "13", rnd.choice([RED, TEAL])) if k % 2 else cat(rnd.uniform(130, 160))
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:rotate({rnd.uniform(-14, 14):.0f}deg)")
    return out


def accidents(t0, d):
    """Under the road: the two averages, 7,800 counting down to 7,500 as the line lands."""
    return A(f'<div style="display:flex;gap:18px;justify-content:center;margin-top:18px;font-family:\'Serif\',serif;font-weight:700">'
             f'<div style="background:#fff;border:4px solid #0A0A0A;border-radius:18px;padding:10px 22px;font-size:40px">'
             f'<span style="font-family:Sans;font-size:22px;letter-spacing:.12em;opacity:.6;display:block">OTHER FRIDAYS</span>7,800</div>'
             f'<div style="background:{TEAL};color:#fff;border:4px solid #0A0A0A;border-radius:18px;padding:10px 22px;font-size:40px">'
             f'<span style="font-family:Sans;font-size:22px;letter-spacing:.12em;opacity:.8;display:block">FRIDAY 13</span>'
             f'<span class="a" data-fx="count" data-at="{t0 + 1.2:.2f}" data-d="1.4" data-from="7800" data-to="7500" data-sep="1">7,500</span>'
             f'</div></div>', "pop", round(t0 + .9, 2), .4)


STAMP_AT = 1.1                     # seconds into the verdict beat: the MYTH stamp lands, with a thump

EP = dict(
    slug="shorts-friday-13th-myth",
    kicker="MYTH CHECK",
    mood="playful",
    cover_at=2.9,
    beats=[
        dict(tag="THE MYTH", bg=DUSK, size=72, hl=["Friday the 13th."],
             say=[("Stocks do worse on Friday the thirteenth.", "Stocks do worse on Friday the 13th."),
                  ("Everyone knows that, right?", "Everyone knows that, right?")],
             art=lambda t0, d: picture("myth_hook", t0, 2.2, w=752, h=640),
             sfx=[(1.0, "pop", .08)]),
        dict(tag="1987", bg=BUTTER, hl=["lower returns"],
             say=[("In nineteen eighty seven, an American study found lower returns on Fridays the thirteenth.",
                   "In 1987, an American study found lower returns on Fridays the 13th.")],
             art=lambda t0, d: picture("study_1987", t0, d, w=752, h=640),
             sfx=[(1.4, "pop", .08), (2.2, "pop", .08)]),
        dict(tag="THE CHECK", bg=MINT, hl=["couldn't confirm it."],
             say=[("But other studies couldn't confirm it.", "But other studies couldn't confirm it.")],
             art=lambda t0, d: picture("not_confirmed", t0, d, w=752, h=640),
             sfx=[(.3, "pop", .07), (.6, "pop", .07), (.9, "pop", .07)]),
        dict(tag="THE EVIDENCE", bg=SKY, hl=["almost 60 years"],
             say=[("A British study checked almost sixty years of UK shares.",
                   "A British study checked almost 60 years of UK shares.")],
             art=lambda t0, d: picture("uk_years", t0, d, w=752, h=640),
             sfx=[(.15 + .25 * j, "tick", .06) for j in range(12)]),
        dict(tag="THE RESULT", bg=PEACH, hl=["higher"],
             say=[("On Friday the thirteenth, returns were, if anything, higher than on other Fridays.",
                   "On Friday the 13th, returns were, if anything, higher than on other Fridays.")],
             art=lambda t0, d: picture("higher_bar", t0, d, w=752, h=640),
             sfx=[(1.6, "ding", .06)]),
        dict(tag="BONUS", bg=SAND, hl=["fewer road accidents"],
             say=[("And Dutch insurers counted fewer road accidents that day, not more.",
                   "And Dutch insurers counted fewer road accidents that day, not more.")],
             art=lambda t0, d: picture("road_cat", t0, d, w=700, h=520), art_w=700, art_h=520,
             over=accidents, sfx=[(1.2 + .2 * j, "tick", .05) for j in range(7)]),
        dict(tag="THE VERDICT", bg=ROSE, hl=["a myth."],
             say=[("So the Friday the thirteenth curse is a myth.", "So the Friday the 13th curse is a myth."),
                  ("Superstition isn't a strategy.", "Superstition isn't a strategy.")],
             art=lambda t0, d: picture("myth_stamp", t0, d, w=752, h=640, at_s=STAMP_AT),
             sfx=[(STAMP_AT, "thump", .2)]),
    ],
    close=dict(say=[("Would you trade on Friday the thirteenth?", "Would you trade on Friday the 13th?"),
                    ("Tell me in the comments.", "Tell me in the comments."),
                    ("And subscribe for more like this.", "And subscribe for more like this.")],
               cols={"comments.": RED}, bg=LILAC, art=rain,
               pic=lambda t0, d: picture("trader_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # clean master: Pietro adds a sound in the YouTube app
    lufs=-14,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
