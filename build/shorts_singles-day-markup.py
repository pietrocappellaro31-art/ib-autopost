"""
YouTube Short: four levels on Singles' Day (11.11), China's shopping festival,
on the day itself, 11 Nov 2026. The hook asks the last level first: the
markup trap (a price raised 25%, then 20% off).

Sources:
    [1] Quartz, Nov 2018, "Ten years of Singles' Day, China's ridiculously huge
        shopping festival": "In 1993 a group of university students at Nanjing
        University decided to start celebrating being single on 11/11", "since
        the number 1 stands for aloneness while the date looks like four lone
        sticks"; Alibaba's first Singles' Day sale in November 2009 (Jack Ma's
        op-ed of 26 Oct 2009 came "just two weeks before the first Singles'
        Day"); "leaving only 27 participating in the shopping festival".
        https://qz.com/1450338/10-years-of-singles-day-in-china-the-shopping-festival-alibaba-invented
    [2] Benzinga, 11 Nov 2022, "Alibaba Doesn't Disclose Singles' Day Sales For
        First Time": "The FY21 sales reached 540.3 billion yuan"; Alibaba
        "decided not to disclose full sales results ... for the first time".
        https://www.benzinga.com/news/22/11/29694035/alibaba-doesnt-disclose-singles-day-sales-for-first-time
    [3] WalkTheChat, "The New Normal Double 11 2025 Report": "GMV reporting has
        been eliminated since 2022"; for 2025 "Alibaba declined to disclose
        specific GMV figures"; Taobao/Tmall ran the 2025 festival 15 Oct to 14 Nov.
        https://walkthechat.com/the-new-normal-double-11-2025-report-a-more-rational-singles-day/
    [4] Yicai Global, 2 Nov 2017, "Chinese regulators clamp down on stores
        hiking prices before Singles' Day shopping festival": the State
        Administration for Industry and Commerce said e-commerce firms "should
        not sell counterfeit goods or raise prices before discounting products".
        https://yicaiglobal.com/news/chinese-regulators-clamp-down-on-stores-hiking-prices-before-singles-day-shopping-festival

Every answer, worked:
    L1  11.11 is four 1s; a 1 "stands for aloneness" and the date "looks like
        four lone sticks" [1].
    L2  Students at Nanjing University started it in 1993 [1]; Alibaba made it
        a sale in 2009, with only 27 merchants in the first one [1].
    L3  The total: Alibaba has not published it since 2022 [2][3]. The last
        published total, for 2021, was 540.3 billion yuan [2]; said as "about
        five hundred and forty billion".
    L4  Our own arithmetic (no source needed): $100 x 1.25 = $125;
        $125 x (1 - 0.20) = $100. You save nothing: 1.25 x 0.8 = 1. This is
        the practice China's regulator told sellers not to do before the
        festival [4] (said as "a trick regulators warned about", no number).

    python3 build/shorts_singles-day-markup.py HEART
"""

import random
import sys

from levels import make, RED, TEAL
from motion import A
from sketch import picture, _ptag

# A colour ground per part (the penny Short standard, 10 Nov). Singles' Day: red and gold first.
BLUSH, GOLD, MINT, SKY, ROSE, PEACH = "#F8D9D2", "#F3E4BC", "#D2E9E1", "#D6E2F3", "#F6CFC3", "#F2D6BF"


def tag_svg(w, label, fill=RED, color="#fff", rot=0):
    h = round(w * .52)
    return (f'<svg width="{w + 20}" height="{h + 40}" viewBox="{-10} {-20} {w + 20} {h + 40}" style="overflow:visible">'
            + _ptag(w / 2, h / 2, w, label, fill, color, rot=rot) + '</svg>')


def tile_svg(w, label="11.11", fill="#fff", color=RED):
    h = round(w * .62)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 200 124" style="overflow:visible">'
            f'<rect x="3" y="3" width="194" height="118" rx="20" fill="{fill}" stroke="#0A0A0A" stroke-width="5"/>'
            f'<text x="100" y="82" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="58" '
            f'fill="{color}">{label}</text></svg>')


def floaters(total):
    """Faint price tags and 11.11 tiles drifting at the edges, clear of the text."""
    out = ""
    spots = [(-150, 330, "tag", 230, "-20%"), (690, 430, "tile", 170, "11.11"), (-110, 880, "tile", 150, "11.11"),
             (690, 930, "tag", 210, "+25%"), (-80, 1090, "tag", 150, "%")]
    for k, (x, y, kind, w, lab) in enumerate(spots):
        art = tag_svg(w, lab, "#F2C35B", "#0A0A0A") if kind == "tag" else tile_svg(w, lab)
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.2">'
                + A(art, "float", 0, 1, amp=24, w=.5 + .1 * k, ph=k * 1.7) + "</div>")
    return out


def rain(t0, dur):
    """Price tags and 11.11 tiles falling in below the score, then bobbing."""
    rnd = random.Random(1111)
    out = ""
    for k in range(9):
        x, y = rnd.uniform(-20 + 80 * k, 30 + 80 * k), rnd.uniform(1030, 1110)
        if k % 3 == 1:
            art = tile_svg(rnd.uniform(120, 150))
        else:
            art = tag_svg(rnd.uniform(110, 140), rnd.choice(["-20%", "+25%", "?"]), rnd.choice([RED, TEAL, "#F2C35B"]),
                          "#fff")
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:rotate({rnd.uniform(-16, 16):.0f}deg)")
    return out


def four_sticks(t):
    """Beside the level 1 answer: four lone 1s popping in one by one."""
    return ('<div style="display:flex;gap:14px;margin-top:14px">'
            + "".join(A(f'<div style="width:34px;height:150px;border-radius:17px;background:{c};border:5px solid #0A0A0A"></div>',
                        "pop", t + .15 + .14 * k, .4)
                      for k, c in enumerate((TEAL, "#F2C35B", "#7A6BB0", RED))) + "</div>")


def count_tag(frm, to, pre="", suf="", fill=RED, w=210):
    """A tag whose number counts from frm to to as the answer lands."""
    def art(t):
        return (f'<svg width="{w}" height="{round(w * .52)}" viewBox="0 0 250 130" style="overflow:visible;margin-top:8px">'
                f'<rect x="4" y="4" width="242" height="122" rx="22" fill="{fill}" stroke="#0A0A0A" stroke-width="5"/>'
                f'<text x="125" y="92" text-anchor="middle" font-family="\'Serif\',serif" font-weight="700" font-size="72" fill="#fff" '
                f'class="a" data-fx="count" data-at="{t + .2}" data-d="1.4" data-from="{frm}" data-to="{to}" data-pre="{pre}" '
                f'data-suf="{suf}">{pre}{to}{suf}</text></svg>')
    return art


ART_W, ART_H = 700, 532          # 11 Nov: drawings a little bigger in the answer zone (650 x 520 on the penny Short)

EP = dict(
    slug="shorts-singles-day-markup",
    kicker="SINGLES' DAY: 11.11",
    hook=dict(
        say=[("A price goes up twenty five percent, then twenty percent off: what do you save?",
              "A price goes up 25%, then 20% off: what do you save?"),
             ("That's level four.", "That's level 4."), ("Keep score.", "Keep score.")],
        sub="Today is 11.11, Singles' Day in China.",
        hl=["what do you save?"], qsize=74, bg=BLUSH, art_w=360, art_h=290, lsize=58,
        art=lambda t0, d: picture("sale_bag", t0, max(d, 2.5), w=360),
        cols={"4.": RED, "score.": RED},
    ),
    levels=[
        dict(tail="easy.", think=1.0, bg=GOLD, ans_min=ART_H,
             art=lambda t0, d: picture("four_ones", t0, d, w=ART_W, h=ART_H),
             art_after=four_sticks,
             q=[("Why is November the eleventh called Singles' Day?", "Why is 11.11 called Singles' Day?")],
             hl=["11.11?"],
             a=[("It's four ones.", "Four 1s."),
                ("Four lone sticks, like four single people.", "Four lone sticks, like four single people.")],
             bigsize=120),
        dict(tail="medium.", think=1.3, bg=MINT, ans_min=ART_H,
             art=lambda t0, d: picture("shopfront", t0, d, w=ART_W, h=ART_H),
             art_after=count_tag(0, 27, fill=TEAL, w=170),
             q=[("Students started it in nineteen ninety three.", "Students started it in 1993."),
                ("Who turned it into a sale?", "Who turned it into a sale?")],
             hl=["into a sale?"],
             a=[("Alibaba, in two thousand nine.", "Alibaba."),
                ("Only twenty seven shops joined the first one.", "Only 27 shops joined the first one.")],
             bigsize=108, chip="1993 students &rarr; 2009 sale", chip_at=1),
        dict(tail="tricky.", think=1.5, bg=SKY, ans_min=ART_H,
             art=lambda t0, d: picture("tally_board", t0, d, w=ART_W, h=ART_H),
             q=[("Since twenty twenty two, what has Alibaba stopped publishing?",
                 "Since 2022, what has Alibaba stopped publishing?")],
             hl=["stopped publishing?"],
             a=[("The total sales.", "The total sales."),
                ("The last, for twenty twenty one, was about five hundred and forty billion yuan.",
                 "The last, for 2021, was about 540 billion yuan.")],
             bigsize=108, chip="2021: 540.3 bn yuan", chip_at=1,
             foot="Sources: Benzinga, Nov 2022; WalkTheChat, 2025."),
        dict(label="Last one.", tail="final boss.", think=1.8, bg=ROSE, ans_min=ART_H,
             art=lambda t0, d: picture("markup_tag", t0, d, w=ART_W, h=ART_H),
             art_after=count_tag(125, 100, pre="$", fill=RED),
             q=[("A price goes up twenty five percent, then twenty percent off: what do you save?",
                 "A price goes up 25%, then 20% off: what do you save?")],
             hl=["what do you save?"], qsize=60,
             a=[("Nothing at all.", "Nothing."),
                ("A hundred becomes a hundred and twenty five, and twenty percent off that is a hundred again.",
                 "$100 becomes $125, and 20% off that is $100 again.")],
             bigsize=112, chip="$100 &times; 1.25 &times; 0.8 = $100", chip_at=1,
             foot="China's regulator told sellers not to do this (2017)."),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments."),
                    ("And subscribe for one of these every day.", "And subscribe for one of these every day.")],
               cols={"comments.": RED}, bg=PEACH, art=rain),
    floaters=floaters,
    speed=1.0,
    music=False,          # Pietro adds a trending sound in the YouTube app at upload
    lufs=-14,             # YouTube loudness, without a music bed
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
