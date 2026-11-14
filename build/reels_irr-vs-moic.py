"""
Levels #13: four interview questions on MOIC and IRR, each one harder. The hook asks the last level first.

MOIC (multiple on invested capital) = money out / money in: how much. IRR (internal rate of return) = the yearly
rate that makes the money out, discounted back, equal the money in: how fast. With one cash flow in and one out
(no interim dividends or fees), IRR = MOIC ^ (1 / years) - 1.

Every answer, worked (textbook definitions and round example numbers; no fund, deal, benchmark or "typical
return" is claimed):
    L1  MOIC stands for multiple on invested capital: what you get back divided by what you put in.
    L2  In $100, out $250: 250 / 100 = 2.5x.
    L3  IRR adds time. MOIC is the same whether the 2.5x took two years or ten; IRR is a yearly rate, so it
        falls as the holding period grows.
    L4  Deal A: 2x in 3 years. IRR = 2 ^ (1/3) - 1 = 1.259921 - 1 = 25.99%, about 26% a year.
        Deal B: 3x in 7 years. IRR = 3 ^ (1/7) - 1 = e ^ (ln 3 / 7) - 1 = e ^ 0.156945 - 1 = 1.169931 - 1
        = 16.99%, about 17% a year.
        So deal A has the higher IRR, although deal B returns the bigger multiple.
        Check: 1.26 ^ 3 = 2.0004 (about 2x); 1.17 ^ 7 = 3.0012 (about 3x).
    Bonus (comment): to match 2x in 3 years over 7 years you need 2 ^ (7/3) = 2 ^ 2.3333 = 5.0397, about 5x
        (check: 1.2599 ^ 7 = 5.04).

Spoken text writes numbers as words; the screen uses digits. "MOIC" and "IRR" are said as letters/word as the
voice reads them; any word the recogniser hears differently is checked in takes.json.

14 Nov (cinematic standard, quality-log next improvement of 13 Nov): two filmed beats in one Reel.
  - the hook is filmed (cine.py, scene family K, "a figure faces the question"): the analyst in the invented
    dusk office (cine_lib.office_today: no bank, logo or real skyline) types while his monitor draws two deals on
    one 7-year timeline (A: 2x over 3 years, B: 3x over 7), then leans back;
  - level 4's ANSWER is filmed too: the same desk, closer, the two deals build as the question is asked and each
    deal's yearly return arrives as it is said (26% a year, then 17%), A is ticked, B dims;
  - the film gets the card's motion blur through the swipes (levels.film_window).
No badge: a generic illustration, not a reconstruction of a real event; the screen shows only the worked numbers.

    python3 build/reels_irr-vs-moic.py HEART
"""

import sys

from levels import make, RED, TEAL
from sketch import picture
import cine as C
import cine_lib as CL

ART_W, ART_H = 700, 532


def office(dur, w, h, t_on, t_b, t_ans=None, t_lean=None, close=False):
    """The analyst at his desk, the two-deal monitor; shot seconds. close=True starts nearer the screen."""
    lay_, anc = CL.office_today()
    mx, my = anc["monitor"]
    mon = CL.monitor_irr(t_on=t_on, t_b=t_b, t_ans=t_ans, cx=mx, cy=my, w=480, h=290)
    typing = C.pose("seated", shF=62, elF=38, shB=56, elB=44, head=6, lean=10, eyeY=.6)
    t_lean = t_lean if t_lean is not None else t_b + 1.0
    keys = [[0, typing], [.35, dict(typing, elF=30)], [.6, typing], [.85, dict(typing, elB=36)], [1.1, typing],
            [t_lean, dict(typing, head=2, eyeY=0)],
            [t_lean + .5, C.pose("seated", shF=30, elF=70, shB=26, elB=74, head=-6, lean=-4, brow=1, mouth=2)],
            [dur, C.pose("seated", shF=28, elF=72, shB=24, elB=76, head=-8, lean=-5, brow=.8, mouth=0)]]
    analyst = C.actor("analyst", "modern_navy", pos=[[0, 330, 990]], scale=1.0, seed=5, dir=1, walk=False, pose_keys=keys)
    layers = [C.layer(z, svg, noblur=(k == "floor")) for k, (z, svg) in lay_.items() if k != "desk"]
    layers.append(C.layer(.8, analyst["svg"]))
    layers.append(C.layer(.85, lay_["desk"][1] + mon))
    gx, gy = 650, 650
    cx, cy = 960 + (gx - 960) / .85, 540 + (gy - 540) / .85
    if close:      # the answer: start on face and screen, push onto the screen as the returns arrive
        sx, sy = 960 + (mx - 960) / .85, 540 + (my - 540) / .85
        cam = [[0, cx + 30, cy - 10, 1.38], [t_ans, cx + 60, cy - 14, 1.48, "sine"], [dur, sx - 40, sy - 6, 1.9, "inout"]]
    else:
        cam = [[0, 760, 620, 1.12], [t_b, cx + 30, cy - 10, 1.38, "sine"], [dur, cx, cy, 1.6, "inout"]]
    shot = dict(dur=dur, layers=layers, actors=[analyst], cam=cam, focus=[[0, .82], [t_b, .85], [dur, .85]], dof=6, band=.3,
                shake=.4, grade="dusk", vig=.9)
    # foley tied to the picture: a soft mallet as each bar starts to draw (A higher, B lower), and with the answer
    # a ding-like high mallet as A's return lands and the tick
    fx = [("hit", t_on + .05, .32, .2, dict(pitch=330)), ("hit", t_b + .05, .32, .2, dict(pitch=220))]
    if t_ans is not None:
        fx += [("hit", t_ans + .02, .40, .25, dict(pitch=392)), ("hit", t_ans + .37, .25, .25, dict(pitch=196)),
               ("hit", t_ans + .72, .36, .25, dict(pitch=523))]
    return [shot], fx


def hook_film(dur, w, h, t_end):
    return office(dur, w, h, t_on=.35, t_b=max(1.2, t_end * .45), t_lean=max(1.6, t_end - .9))


def l4_film(dur, w, h, m):
    # the question "Two times in three years, or three times in seven." starts at m["q"]; A draws as it begins,
    # B about a second and a half in; the returns arrive with the answer
    return office(dur, w, h, t_on=m["q"] + .2, t_b=m["q"] + 1.5, t_ans=m["a"] + 1.4, t_lean=m["a"] + 2.6, close=True)


EP = dict(
    slug="w2-levels-13",
    kicker="IB INTERVIEW LEVELS #13",
    hook=dict(
        say=[("Two times in three years, or three times in seven: which has the higher IRR?",
              "2x in 3 years, or 3x in 7: which has the higher IRR?")],
        sub="4 interview questions. Each one harder.",
        qsize=68,
        hl=["higher IRR?"],
        film=hook_film,
        film_w=754, film_h=380, foley_gain=.3, sub_gap=28,
    ),
    levels=[
        dict(tail="easy.", think=1.0, ans_min=ART_H,
             art=lambda t0, d: picture("flow", t0, d, w=ART_W, h=ART_H, steps=("MONEY IN", "WAIT", "MONEY OUT")),
             q=[("What does MOIC stand for?", "What does MOIC stand for?")],
             hl=["MOIC"],
             a=[("Multiple on invested capital.", "Multiple on invested capital.", "big"),
                ("What you get back, divided by what you put in.", "What you get back, divided by what you put in.")],
             bigsize=96, chip="MOIC = money out &divide; money in", chip_at=1),
        dict(tail="medium.", think=1.3, ans_min=ART_H,
             art=lambda t0, d: picture("coins", t0, d, w=ART_W, h=ART_H, stacks=(2, 5), labels=("$100", "$250")),
             q=[("You put in a hundred dollars and get back two hundred and fifty.", "You put in $100 and get back $250."),
                ("What's the MOIC?", "What's the MOIC?")],
             hl=["MOIC?"], qsize=56,
             a=[("Two point five times.", "2.5x.", "big"),
                ("Two fifty divided by a hundred.", "$250 divided by $100.")],
             bigsize=150, chip="$250 &divide; $100 = 2.5x", chip_at=1),
        dict(tail="tricky.", think=1.6, ans_min=ART_H,
             art=lambda t0, d: picture("clock", t0, d, w=ART_W, h=ART_H),
             q=[("What does IRR tell you that MOIC doesn't?", "What does IRR tell you that MOIC doesn't?")],
             hl=["IRR"], qsize=60,
             a=[("Time.", "Time.", "big"),
                ("IRR is a yearly return.", "IRR is a yearly return."),
                ("MOIC ignores how long it took.", "MOIC ignores how long it took.")],
             bigsize=150, chip="MOIC: how much. IRR: how fast.", chip_at=1),
        dict(label="Here's the last one.", tail="final boss.", think=2.0, ans_min=0,
             film=l4_film, film_w=754, film_h=300, film_gap=24, foley_gain=.3,
             q=[("Two times in three years, or three times in seven.", "2x in 3 years, or 3x in 7."),
                ("Which has the higher IRR?", "Which has the higher IRR?")],
             hl=["higher IRR?"], qsize=50,
             # 14 Nov: no chip on this level; the filmed screen under the answer carries the working (26% a year,
             # 17% a year, A ticked), and the card stays inside the safe area
             a=[("Two times in three years.", "2x in 3 years.", "big"),
                ("About twenty six percent a year, against seventeen percent.", "About 26% a year, against 17%.")],
             bigsize=96),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments.")],
               cols={"comments.": RED}),
    speed=1.0,
    denoise="anlmdn=s=0.0004", fx_gain=.7, tp=-1.8,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
