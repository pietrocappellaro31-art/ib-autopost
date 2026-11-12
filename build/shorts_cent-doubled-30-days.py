"""
YouTube Short: four levels on compound interest, 12 Nov 2026. The hook asks the
last level first: a million dollars now, or one cent doubled daily for
30 days (the riddle that keeps going round on short video).

Sources:
    [1] Corporate Finance Institute, "Rule of 72": "the Rule of 72 is a formula
        that estimates the amount of time it takes for an investment to double
        in value"; "The simple calculation is dividing 72 by the annual interest
        rate" (their example: 12% a year, about six years).
        https://corporatefinanceinstitute.com/resources/wealth-management/rule-of-72-double-investment/
    [2] Quote Investigator, 9 Sep 2019, "The Eighth Wonder of the World Is
        Compound Interest": "QI has found no substantive evidence that Albert
        Einstein, Baron Rothschild, or John D. Rockefeller employed the saying";
        the earliest attribution to Einstein QI found is a 1988 Courier-Post
        article quoting A. Michael Lipper.
        https://quoteinvestigator.com/2019/09/09/interest/

Every answer, worked:
    L1  Our own arithmetic: $100 x 1.10 = $110 after year 1; $110 x 1.10 = $121
        after year 2. Not $120: year 2 earns 10% on the $10 of interest too.
    L2  Rule of 72 [1]: 72 / 8 = 9 years. Check: 1.08^9 = 1.999, so about 9.
    L3  No evidence Einstein said it [2]; the earliest link to him that QI
        found is from 1988 [2].
    L4  The question is shown, not read again (the hook asked it). Our own arithmetic (the drawing labels day 25 = 2^24 cents = $167,772): day 1 = 1 cent, doubling each day, so day n is
        2^(n-1) cents. Day 30 = 2^29 = 536,870,912 cents = $5,368,709.12, over
        $5 million, so the cent beats $1 million. Day 20 = 2^19 = 524,288 cents
        = $5,242.88, "about five thousand". (The drawing's bars use the same
        formula, against $1 million = 400 px.)

    python3 build/shorts_cent-doubled-30-days.py MICHAEL
"""

import random
import sys

from levels import make, RED, TEAL
from motion import A
from sketch import picture, METALS

# A colour ground per part (the penny Short standard, 10 Nov): warm gold for money growing.
BUTTER, MINT, SKY, LILAC, ROSE, PEACH = "#F5E6B8", "#D2E9E1", "#D6E2F3", "#E2DAF0", "#F6CFC3", "#F2D6BF"


def coin_svg(w, label="1¢", metal="copper"):
    c0, c1, c2 = METALS[metal]
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 100 100" style="overflow:visible">'
            f'<circle cx="50" cy="53" r="46" fill="{c2}"/><circle cx="50" cy="50" r="46" fill="{c1}" stroke="{c2}" stroke-width="3"/>'
            f'<circle cx="50" cy="50" r="38" fill="none" stroke="{c0}" stroke-width="2" stroke-dasharray="3 2.5"/>'
            f'<text x="50" y="62" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="34" fill="{c2}">{label}</text></svg>')


def tile_svg(w, label="×2", fill=RED, color="#fff"):
    h = round(w * .62)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 200 124" style="overflow:visible">'
            f'<rect x="3" y="3" width="194" height="118" rx="20" fill="{fill}" stroke="#0A0A0A" stroke-width="5"/>'
            f'<text x="100" y="84" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="66" '
            f'fill="{color}">{label}</text></svg>')


def floaters(total):
    """Faint cents and x2 tiles drifting at the edges, clear of the text."""
    out = ""
    spots = [(-120, 330, "coin", 210), (700, 420, "tile", 170), (-100, 900, "tile", 150), (700, 950, "coin", 190),
             (-70, 1110, "coin", 140)]
    for k, (x, y, kind, w) in enumerate(spots):
        art = coin_svg(w) if kind == "coin" else tile_svg(w)
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.2">'
                + A(art, "float", 0, 1, amp=24, w=.5 + .1 * k, ph=k * 1.7) + "</div>")
    return out


def rain(t0, dur):
    """Cents, gold coins and x2 tiles falling in below the score, then bobbing."""
    rnd = random.Random(1230)
    out = ""
    for k in range(9):
        x, y = rnd.uniform(-20 + 80 * k, 30 + 80 * k), rnd.uniform(1030, 1110)
        if k % 3 == 1:
            art = tile_svg(rnd.uniform(110, 140), "×2", rnd.choice([RED, TEAL]))
        else:
            art = coin_svg(rnd.uniform(110, 140), *rnd.choice([("1¢", "copper"), ("$", "gold")]))
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:rotate({rnd.uniform(-16, 16):.0f}deg)")
    return out


def count_tag(frm, to, pre="", suf="", fill=RED, w=210, dec=0, size=72):
    """A tile whose number counts from frm to to as the answer lands."""
    def art(t):
        return (f'<svg width="{w}" height="{round(w * .52)}" viewBox="0 0 250 130" style="overflow:visible;margin-top:8px">'
                f'<rect x="4" y="4" width="242" height="122" rx="22" fill="{fill}" stroke="#0A0A0A" stroke-width="5"/>'
                f'<text x="125" y="{65 + size * .34:.0f}" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" '
                f'font-size="{size}" fill="#fff" class="a" data-fx="count" data-at="{t + .2}" data-d="1.4" data-from="{frm}" '
                f'data-to="{to}" data-dec="{dec}" data-pre="{pre}" data-suf="{suf}">{pre}{to:.{dec}f}{suf}</text></svg>')
    return art


def stamp_tile(label, fill=RED):
    """Beside the level 3 answer: a stamp that slams in."""
    def art(t):
        return A(f'<div style="margin-top:12px;display:inline-block;padding:10px 22px;border:7px solid {fill};border-radius:14px;'
                 f'color:{fill};font-family:\'Serif\',serif;font-weight:700;font-size:40px;letter-spacing:.04em;'
                 f'transform:rotate(-8deg);background:rgba(255,255,255,.7)">{label}</div>', "pop", t + .2, .4)
    return art


ART_W, ART_H = 700, 532          # the answer-zone size from 11 Nov; today's drawings reach the canvas edges
HOOK_W, HOOK_H = 420, 336        # 12 Nov: hook art 420 px (360 on 11 Nov), lines smaller so both fit the 752 px column

EP = dict(
    slug="shorts-cent-doubled-30-days",
    kicker="COMPOUND INTEREST",
    hook=dict(
        say=[("A million dollars now, or one cent doubled daily for thirty days?",
              "$1 million now, or 1¢ doubled daily for 30 days?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="Four questions on how money grows.",
        hl=["for 30 days?"], qsize=74, bg=BUTTER, art_w=HOOK_W, art_h=HOOK_H, lsize=50,
        art=lambda t0, d: picture("cent_or_million", t0, max(d, 2.5), w=HOOK_W, h=HOOK_H),
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0, bg=MINT, ans_min=ART_H,
             art=lambda t0, d: picture("coin_stacks", t0, d, w=ART_W, h=ART_H),
             art_after=count_tag(100, 121, pre="$", fill=TEAL, w=190),
             q=[("A hundred dollars earns ten percent a year.", "$100 earns 10% a year."),
                ("What do you have after two years?", "What do you have after 2 years?")],
             hl=["after 2 years?"], qsize=60,
             a=[("A hundred and twenty one dollars.", "$121."),
                ("Not a hundred and twenty: the interest earns interest.",
                 "Not $120: the interest earns interest.")],
             bigsize=120, chip="$100 &times; 1.1 &times; 1.1 = $121", chip_at=1),
        dict(tail="medium.", think=1.3, bg=SKY, ans_min=ART_H,
             art=lambda t0, d: picture("hourglass72", t0, d, w=ART_W, h=ART_H),
             art_after=count_tag(0, 9, suf=" yrs", fill=TEAL, w=190, size=64),
             q=[("Rule of seventy two: at eight percent a year, when does your money double?",
                 "Rule of 72: at 8% a year, when does your money double?")],
             hl=["money double?"], qsize=60,
             a=[("About nine years.", "9 years."),
                ("Seventy two divided by eight.", "72 divided by 8.")],
             bigsize=104, chip="72 &divide; 8% = 9 years", chip_at=1,
             foot="Source: Corporate Finance Institute, Rule of 72."),
        dict(tail="tricky.", think=1.5, bg=LILAC, ans_min=ART_H - 20,
             art=lambda t0, d: picture("quote_card", t0, d, w=ART_W, h=ART_H - 20),
             art_after=stamp_tile("NO PROOF"),
             q=[("Did Einstein call compound interest the eighth wonder of the world?",
                 "Did Einstein call compound interest the 8th wonder of the world?")],
             hl=["8th wonder"], qsize=56,
             a=[("There's no proof he did.", "No proof."),
                ("The earliest known link to him is from nineteen eighty eight.",
                 "The earliest known link to him is from 1988.")],
             bigsize=100, foot="Source: Quote Investigator, 2019."),
        dict(label="Last one.", tail="final boss.", think=1.8, bg=ROSE, ans_min=ART_H - 40,
             art=lambda t0, d: picture("doubling_bars", t0, d, w=ART_W, h=ART_H - 40),
             art_after=count_tag(0, 5.37, pre="$", suf="M", fill=RED, dec=2, size=64),
             q=[("", "$1 million now, or 1¢ doubled daily for 30 days?"),
                ("Which one would you take?", "Which one would you take?")],
             hl=["which one would you take?"], qsize=52,
             a=[("The penny, by far.", "The penny."),
                ("Day thirty: over five million dollars.", "Day 30: over $5 million."),
                ("Day twenty: only about five thousand.", "Day 20: only about $5,000.")],
             bigsize=100, chip="1&cent; &times; 2<sup>29</sup> = $5,368,709", chip_at=1),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And subscribe for one of these every day.", "And subscribe for one of these every day.")],
               cols={"comments.": RED}, bg=PEACH, art=rain),
    floaters=floaters,
    speed=1.0,
    music=False,          # Pietro adds a trending sound in the YouTube app at upload
    lufs=-14,             # YouTube loudness, without a music bed; two-stage master from 12 Nov
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
