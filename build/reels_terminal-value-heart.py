"""
Levels #12: four interview questions on terminal value in a DCF, each one
harder. The hook asks the last level first; level 3 (an exit multiple gives
$400 at year 5) is the number level 4 discounts, and the voice says so.

Terminal value = the value, at the end of the forecast, of every cash flow
after it. A DCF is the present value of the forecast years plus the present
value of the terminal value.

Every answer, worked (textbook DCF mechanics, round example numbers, no
statistic, company or "typical share" claimed):
    L1  Terminal value is everything after the forecast period: the value at
        the last forecast year of all the cash flows beyond it.
    L2  Two ways: perpetuity growth (the last year's free cash flow grown at
        a constant rate forever: FCF x (1 + g) / (r - g)) or an exit
        multiple (the last year's EBITDA times a multiple, as if sold).
    L3  Year 5 EBITDA $50, exit multiple 8x: TV = 50 x 8 = $400, a value AT
        year 5, not today.
    L4  Free cash flow $20 a year for years 1 to 5, the $400 TV at year 5,
        discount rate 10%, end-of-year discounting.
        Forecast: 20 x (1 - 1.1^-5) / 0.10 = 20 x 3.7908 = 75.82, about $76.
        TV today: 1.1^5 = 1.61051; 400 / 1.61051 = 248.37, about $248.
        Total 75.82 + 248.37 = 324.18, about $324.
        TV share: 248.37 / 324.18 = 0.766, about 77%. So yes, terminal
        value can be most of a DCF (here about three quarters). No claim is
        made about what share is usual in practice.
    Bonus (comment): same model, but the exit multiple is 6x instead of 8x.
        TV = 50 x 6 = $300 at year 5; today 300 / 1.61051 = 186.28, about
        $186. Total 75.82 + 186.28 = 262.10, about $262. Share 186.28 /
        262.10 = 0.711, about 71%. Still most of the value.

Spoken text writes numbers as words; the screen uses digits. "D C F" and
"EBITDA" are joined back by voice_check.words, so the word check is exact.

    python3 build/reels_terminal-value.py G2

13 Nov, evening (Pietro: "Create one according to the new standards"): the same four levels remade to
docs/production (cinematic-standard, audio-standard, quality-gates section 9) as w2-levels-12-heart:
  - narrator HEART (Kokoro af_heart, 0.9), not G2;
  - the hook is FILMED (cine.py, scene family K, "a figure faces the question"): an analyst at a desk in a city
    office at dusk (cine_lib.office_today, our own invented set: no bank, logo or real skyline) types; his
    monitor builds a DCF, five small cash-flow bars, then one tall block for every year after the forecast rises
    past them; he leans back. The camera pushes from the room to the screen. No badge: it is a generic
    illustration, not a reconstruction of a real event, and no figure on the monitor is a claim (Y1 to Y5 and
    the block carry no numbers);
  - foley tied to the picture (a soft mallet as each bar lands, a lower one for the tall block);
  - a clean master (-16 LUFS) and an original-scored alternative (master.py scored).

    python3 build/reels_terminal-value-heart.py HEART
"""

import sys

from levels import make, RED, TEAL
from sketch import picture
import cine as C
import cine_lib as CL

ART_W, ART_H = 700, 532


def office_hook(dur, w, h, t_end):
    """The filmed hook (shot seconds = Reel seconds; the hook starts at 0). The bars build while the question is
    asked; the tall block rises as it ends ("most of a DCF?"); the analyst leans back as it passes the bars."""
    t_on, t_tv = .15, max(.9, t_end - 1.0)
    lay_, anc = CL.office_today()
    mx, my = anc["monitor"]
    mon = CL.monitor_dcf(t_on=t_on, t_tv=t_tv, cx=mx, cy=my, w=440, h=270)
    typing = C.pose("seated", shF=62, elF=38, shB=56, elB=44, head=6, lean=10, eyeY=.6)
    pose_keys = [[0, typing], [.35, dict(typing, elF=30)], [.6, typing], [.85, dict(typing, elB=36)], [1.1, typing],
                 [t_tv + .25, dict(typing, head=2, eyeY=0)],
                 [t_tv + .7, C.pose("seated", shF=30, elF=70, shB=26, elB=74, head=-6, lean=-4, brow=1, mouth=2)],
                 [dur, C.pose("seated", shF=28, elF=72, shB=24, elB=76, head=-8, lean=-5, brow=.8, mouth=0)]]
    analyst = C.actor("analyst", "modern_navy", pos=[[0, 330, 990]], scale=1.0, seed=5, dir=1, walk=False, pose_keys=pose_keys)
    layers = [C.layer(z, svg, noblur=(k == "floor")) for k, (z, svg) in lay_.items() if k != "desk"]
    layers.append(C.layer(.8, analyst["svg"]))
    layers.append(C.layer(.85, lay_["desk"][1] + mon))
    # end framed on the analyst's face and the screen together (world x about 330 to 1000 on the z .8 to .85 planes)
    gx, gy = 640, 660
    cx, cy = 960 + (gx - 960) / .85, 540 + (gy - 540) / .85
    cam = [[0, 760, 620, 1.12], [t_tv, cx + 30, cy - 10, 1.38, "sine"], [dur, cx, cy, 1.62, "inout"]]
    shot = dict(dur=dur, layers=layers, actors=[analyst], cam=cam, focus=[[0, .82], [t_tv, .85], [dur, .85]], dof=6, band=.3,
                shake=.4, grade="dusk", vig=.9)
    fx = [("hit", t_on + .14 * k + .18, .30, .2, dict(pitch=[262, 294, 330, 349, 392][k])) for k in range(5)]
    fx += [("hit", t_tv + .45, .55, .25, dict(pitch=131)), ("hit", t_tv + .75, .32, .25, dict(pitch=196))]
    return [shot], fx


EP = dict(
    slug="w2-levels-12-heart",
    kicker="IB INTERVIEW LEVELS #12",
    hook=dict(
        say=[("Can terminal value be most of a DCF?", "Can terminal value be most of a DCF?")],
        sub="4 interview questions. Each one harder.",
        qsize=72,
        hl=["most of a DCF?"],
        film=lambda dur, w, h, t_end: office_hook(dur, w, h, t_end),
        film_w=754, film_h=380, foley_gain=.3, sub_gap=28,
    ),
    levels=[
        dict(tail="easy.", think=1.0, ans_min=ART_H,
             art=lambda t0, d: picture("tv_timeline", t0, d, w=ART_W, h=ART_H, seed=2),
             q=[("In a DCF, what's terminal value?", "In a DCF, what's terminal value?")],
             hl=["terminal value?"],
             a=[("Everything after the forecast.", "Everything after the forecast.", "big")],
             bigsize=96, chip="Years 1 to 5 + terminal value", chip_at=0),
        dict(tail="medium.", think=1.3, ans_min=ART_H,
             art=lambda t0, d: picture("two_ways", t0, d, w=ART_W, h=ART_H),
             q=[("Name the two ways to calculate it.", "Name the 2 ways to calculate it.")],
             hl=["two ways"], qsize=62,
             a=[("Growth, or a multiple.", "Growth, or a multiple.", "big"),
                ("Grow cash flow forever, or sell at a multiple.", "Grow cash flow forever, or sell at a multiple.")],
             bigsize=104, chip="Grow forever, or sell", chip_at=1),
        dict(tail="tricky.", think=1.6, ans_min=500,
             art=lambda t0, d: picture("exit_stack", t0, d, w=ART_W, h=500),
             q=[("Year five EBITDA is fifty dollars, exit multiple eight times.",
                 "Year 5 EBITDA is $50, exit multiple 8x."),
                ("What's terminal value?", "What's terminal value?")],
             hl=["terminal value?"], qsize=54,
             a=[("Four hundred dollars.", "$400."),
                ("Fifty times eight, but that's in year five.", "$50 times 8, but that's in year 5.")],
             bigsize=150, chip="$50 &times; 8 = $400", chip_at=1),
        dict(label="Here's the last one.", tail="final boss.", think=2.0, ans_min=500,
             art=lambda t0, d: picture("discount_shrink", t0, d, w=ART_W, h=500),
             q=[("Now twenty a year for five years, then that four hundred, at ten percent.",
                 "Now $20 a year for 5 years, then that $400, at 10%."),
                ("Is terminal value most of it?", "Is terminal value most of it?")],
             hl=["most of it?"], qsize=48,
             a=[("Yes.", "Yes."),
                ("Today, the four hundred is worth about two hundred and forty eight.", "Today, the $400 is worth about $248."),
                ("The five years add seventy six, so about seventy seven percent.", "The 5 years add $76, so about 77%.")],
             bigsize=104, chip="$248 of $324 = 77%", chip_at=2),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments.")],
               cols={"comments.": RED}),
    speed=1.0,
    # 13 Nov, measured on this Reel's stems (mix DNSMOS, -16 LUFS): as first rendered 3.05; anlmdn on the HEART
    # chain 3.08; effects at 0.6 of the first level 3.13, none 3.28; the hook foley alone costs about 0.03.
    # Kept: anlmdn, the hook foley at .3 and the effects at .7 (were .8), every effect still there.
    denoise="anlmdn=s=0.0004", fx_gain=.7, tp=-1.8,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
