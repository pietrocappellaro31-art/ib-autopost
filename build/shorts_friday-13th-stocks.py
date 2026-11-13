"""
YouTube Short: four levels on Friday the 13th and money, 13 Nov 2026 (a Friday the 13th,
the last of the three in 2026). The hook asks the last level first: do stocks do worse
on Friday the 13th?

Sources:
    [1] Our own calendar arithmetic (Python's datetime): the Fridays that fall on the 13th
        in 2026 are 13 February, 13 March and 13 November. Three.
    [2] DutchNews.nl, 12 Jun 2008, "Fewer accidents on Friday 13", reporting the Dutch
        insurance association: "fewer fires and traffic accidents on Friday 13 than on
        ordinary Fridays"; "on ordinary Fridays there are an average 7,800 road accidents,
        on Friday 13 the average is 7,500."
        https://www.dutchnews.nl/2008/06/fewer_accidents_on_friday_13/
    [3] National Geographic, Brian Handwerk, 14 Jun 2014: "It's been estimated that $800 or
        $900 million is lost in business on this day", an estimate by Donald Dossey, founder
        of the Stress Management Center and Phobia Institute in Asheville, North Carolina.
        https://www.nationalgeographic.com/culture/article/140612-friday-superstition-taboo-fear-luck-triskaidekaphobia-phobia
    [4] J. Andrew Coutts, "Friday the thirteenth and the Financial Times Industrial Ordinary
        Shares Index 1935-94", Applied Economics Letters 6(1), 1999, pp. 35-37: no evidence
        of a Friday the 13th effect; if anything, returns on Friday the 13th are higher than
        on other Fridays, in all six ten-year subsamples too.
        https://ideas.repec.org/a/taf/apeclt/v6y1999i1p35-37.html
    [5] Dumitriu and Stefanescu, "The extended Friday the 13th Effect in the US stock
        returns", MPRA Paper 95296, 2019, literature review: Kolb and Rodriguez (1987) found
        US returns on Fridays the 13th significantly lower than on other Fridays, and
        "their findings weren't confirmed by other studies".
        https://mpra.ub.uni-muenchen.de/95296/1/MPRA_paper_95296.pdf

Every answer, worked:
    L1  [1]: three (Feb, Mar, Nov 2026).
    L2  [2]: fewer, about 7,500 against 7,800 on an ordinary Friday (Dutch insurers' averages).
    L3  [3]: $800 to $900 million, and it is one phobia expert's estimate.
    L4  [5] a 1987 US study said lower; later studies did not confirm it. [4] UK shares,
        1935 to 1994 (July 1935 to December 1994, almost 60 years; the spoken line says "almost sixty years
        of UK data"): higher on Friday the 13th than on other Fridays. So: not reliably.
    The drawings are illustrations, not data: friday_bars shows equal grey bars and a
    dashed ? for the 13th.

    python3 build/shorts_friday-13th-stocks.py ISABELLA
"""

import random
import sys

from levels import make, RED, TEAL
from motion import A
from sketch import picture, cat_svg

# A colour ground per part (the penny Short standard, 10 Nov): dusk lilac for the hook, then light grounds.
DUSK, BUTTER, MINT, PEACH, ROSE, SKY = "#DCD6E8", "#F5E6B8", "#D2E9E1", "#F2D6BF", "#F6CFC3", "#D6E2F3"


def tile_svg(w, label="13", fill=RED, color="#fff"):
    h = round(w * .62)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 200 124" style="overflow:visible">'
            f'<rect x="3" y="3" width="194" height="118" rx="20" fill="{fill}" stroke="#0A0A0A" stroke-width="5"/>'
            f'<text x="100" y="86" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="72" '
            f'fill="{color}">{label}</text></svg>')


def cat(w):
    return (f'<svg width="{w}" height="{w}" viewBox="-140 -260 300 280" style="overflow:visible">{cat_svg(0, 0, 1)}</svg>')


def floaters(total):
    """Faint black cats and 13 tiles drifting at the edges, clear of the text."""
    out = ""
    spots = [(-110, 320, "cat", 220), (710, 430, "tile", 170), (-100, 900, "tile", 150), (700, 960, "cat", 200),
             (-60, 1120, "cat", 150)]
    for k, (x, y, kind, w) in enumerate(spots):
        art = cat(w) if kind == "cat" else tile_svg(w)
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.16">'
                + A(art, "float", 0, 1, amp=24, w=.5 + .1 * k, ph=k * 1.7) + "</div>")
    return out


def rain(t0, dur):
    """Black cats and 13 tiles falling in below the score, then bobbing."""
    rnd = random.Random(1313)
    out = ""
    for k in range(9):
        x, y = rnd.uniform(-20 + 80 * k, 30 + 80 * k), rnd.uniform(1030, 1110)
        art = tile_svg(rnd.uniform(110, 140), "13", rnd.choice([RED, TEAL])) if k % 2 else cat(rnd.uniform(130, 160))
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:rotate({rnd.uniform(-14, 14):.0f}deg)")
    return out


def count_tag(frm, to, pre="", suf="", fill=RED, w=210, dec=0, size=72, sep=False):
    """A tile whose number counts from frm to to as the answer lands."""
    def art(t):
        return (f'<svg width="{w}" height="{round(w * .52)}" viewBox="0 0 250 130" style="overflow:visible;margin-top:8px">'
                f'<rect x="4" y="4" width="242" height="122" rx="22" fill="{fill}" stroke="#0A0A0A" stroke-width="5"/>'
                f'<text x="125" y="{65 + size * .34:.0f}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
                f'font-size="{size}" fill="#fff" class="a" data-fx="count" data-at="{t + .2}" data-d="1.4" data-from="{frm}" '
                f'data-to="{to}" data-dec="{dec}" data-pre="{pre}" data-suf="{suf}"' + (' data-sep="1"' if sep else '')
                + f'>{pre}{to:,.{dec}f}{suf}</text></svg>')
    return art


def stamp_tile(label, fill=RED, size=40):
    """Beside an answer: a stamp that slams in."""
    def art(t):
        return A(f'<div style="margin-top:12px;display:inline-block;padding:10px 22px;border:7px solid {fill};border-radius:14px;'
                 f'color:{fill};font-family:\'Serif\',serif;font-weight:700;font-size:{size}px;letter-spacing:.04em;white-space:nowrap;'
                 f'transform:rotate(-8deg);background:rgba(255,255,255,.7)">{label}</div>', "pop", t + .2, .4)
    return art


ART_W, ART_H = 700, 532          # the answer-zone size from 11 Nov
HOOK_W, HOOK_H = 540, 432        # 13 Nov: the hook is the question alone, so its drawing sits centred and bigger (420 x 336 on 12 Nov);
                                 # 600 x 480 ran 66 px under the 1440 line with the question on 3 lines, 560 x 448 still 6 px

EP = dict(
    slug="shorts-friday-13th-stocks",
    kicker="FRIDAY THE 13TH",
    mood="playful",
    hook=dict(
        say=[("Do shares do worse on Friday the thirteenth?", "Do shares do worse on Friday the 13th?")],
        sub="Four questions on the unluckiest day for money.",
        hl=["Friday the 13th?"], qsize=72, bg=DUSK, art_w=HOOK_W, art_h=HOOK_H,
        art=lambda t0, d: picture("fri13_page", t0, max(d, 2.5), w=HOOK_W, h=HOOK_H),
    ),
    levels=[
        dict(tail="easy.", think=1.0, bg=BUTTER, ans_min=ART_H,
             art=lambda t0, d: picture("year_grid", t0, d, w=ART_W, h=ART_H),
             art_after=count_tag(0, 3, fill=TEAL, w=170),
             q=[("How many Friday the thirteenths are there in twenty twenty six?",
                 "How many Friday the 13ths are there in 2026?")],
             hl=["in 2026?"], qsize=60,
             a=[("Three.", "Three."),
                ("February, March and November.", "February, March and November.")],
             bigsize=120, chip="Feb 13 &middot; Mar 13 &middot; Nov 13", chip_at=1),
        dict(tail="medium.", think=1.3, bg=MINT, ans_min=ART_H - 40,
             art=lambda t0, d: picture("road_cat", t0, d, w=ART_W, h=ART_H - 40),
             art_after=count_tag(7800, 7500, fill=TEAL, w=200, size=58, sep=True),
             q=[("Dutch insurers counted road accidents.", "Dutch insurers counted road accidents."),
                ("More on Friday the thirteenth, or fewer?", "More on Friday the 13th, or fewer?")],
             hl=["or fewer?"], qsize=54,
             a=[("Fewer.", "Fewer."),
                ("Seventy five hundred, against seventy eight hundred normally.",
                 "7,500, against 7,800 normally.")],
             bigsize=120, foot="Source: Dutch insurers, via DutchNews, 2008."),
        dict(tail="tricky.", think=1.5, bg=PEACH, ans_min=ART_H - 20,
             art=lambda t0, d: picture("ladder_wallet", t0, d, w=ART_W, h=ART_H - 20),
             art_after=stamp_tile("ESTIMATE"),
             q=[("How much business is said to be lost on every Friday the thirteenth?",
                 "How much business is said to be lost on every Friday the 13th?")],
             hl=["lost"], qsize=58,
             a=[("Eight hundred to nine hundred million dollars.", "$800 to | $900 million."),
                ("But that's one phobia expert's estimate.", "But that's one phobia expert's estimate.")],
             bigsize=96, foot="Source: National Geographic, 2014."),
        dict(label="And the last one.", tail="final boss.", think=1.8, bg=ROSE, ans_min=ART_H - 40,
             art=lambda t0, d: picture("friday_bars", t0, d, w=ART_W, h=ART_H - 40),
             art_after=stamp_tile("NOT LOWER", size=30),
             q=[("", "Do shares do worse on Friday the 13th?"),
                ("What does the data say?", "What does the data say?")],
             hl=["what does the data say?"], qsize=56,
             a=[("Not reliably.", "Not reliably."),
                ("An American study in nineteen eighty seven said yes.", "A 1987 US study said yes."),
                ("But in almost sixty years of UK data, they did better.",
                 "But in almost 60 years of UK data, they did better.")],
             bigsize=104, foot="Sources: Kolb and Rodriguez, 1987; Coutts, 1999."),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And subscribe for one of these every day.", "And subscribe for one of these every day.")],
               cols={"comments.": RED}, bg=SKY, art=rain),
    floaters=floaters,
    speed=1.0,            # the voice's own trial pace (0.89 for ISABELLA) comes from voices.json
    music=False,          # Pietro adds a trending sound in the YouTube app at upload
    lufs=-14,             # YouTube loudness, two-stage master
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
