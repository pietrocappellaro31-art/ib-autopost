"""
Levels #14: four interview questions on enterprise value and equity value, each one harder. The hook asks the last
level first.

Enterprise value (EV) is the value of the business's operations to everyone who funds it, lenders and
shareholders together. Equity value is the shareholders' part. The standard bridge, simplified to the two items
these questions use: EV = equity value + debt - cash. (The full bridge also adds preferred stock and
non-controlling interests; leaving them out does not change any answer below, and none of these companies has
them.) Textbook definitions and round example numbers; no company, deal or "typical" figure is claimed.

Every answer, worked:
    L1  Enterprise value is the value of the whole business: what it is worth to lenders and shareholders
        together (equity value is the shareholders' part only).
    L2  Equity value 100, debt 40, cash 10: EV = 100 + 40 - 10 = 130.
    L3  The company borrows 50 and keeps it as cash. Debt +50, cash +50: EV = 100 + (40 + 50) - (10 + 50)
        = 100 + 90 - 60 = 130. No change: the new debt and the new cash cancel. (Equity value is taken as
        unchanged: borrowing at a fair price swaps one claim for an equal pile of cash, so it creates no value
        for shareholders by itself.)
    L4  Can EV be lower than equity value? Yes, whenever cash is bigger than debt (net cash).
        Example: equity value 100, no debt, cash 30: EV = 100 + 0 - 30 = 70, which is lower than 100.
    Bonus (comment): can EV be negative? Yes, if cash is bigger than equity value plus debt.
        Equity value 20, no debt, cash 50: EV = 20 + 0 - 50 = -30.

Spoken text writes numbers as words; the screen uses digits. "EV" is said as letters, "E V".

15 Nov (Pietro, 14 Nov: "even more animated and with more images"; the cinematic standard):
  - a picture in every beat, through the question, the clock AND the answer: levels 1 to 3 each carry one drawing
    for the whole level (levels.py scene=, sketch.ev_whole, ev_bridge, ev_borrow) that acts the idea out on the
    words (money travels in from lenders and shareholders; the bridge builds column by column and EV counts up;
    a balance tips with the new debt and comes back level with the new cash);
  - two filmed beats: the hook (the analyst at his desk; on his monitor an EV column swings above and below
    equity: higher or lower?) and level 4 (the same desk, closer: equity grows to $100, DEBT $0 shows, a CASH
    block lifts off the top of EV, EV lands at $70 in teal, ticked, LOWER), the film's frame now blurred with the
    card at the swipes (levels.film_window);
  - written to be said: contractions, short sentences, one idea per sentence (the delivery rule of 14 Nov).
No badge: a generic illustration, not a reconstruction of a real event; the screens show only the worked numbers.

    python3 build/reels_ev-vs-equity.py HEART
"""

import sys

from levels import make, RED, TEAL
from sketch import level_picture
import cine as C
import cine_lib as CL


def office(dur, w, h, t_on, t_cash=None, t_ans=None, t_lean=None, close=False, wobble_until=None):
    """The analyst at his desk with the EV monitor; shot seconds. close=True starts nearer the screen."""
    lay_, anc = CL.office_today()
    mx, my = anc["monitor"]
    mon = CL.monitor_ev(t_on=t_on, t_cash=t_cash, t_ans=t_ans, cx=mx, cy=my, w=480, h=290, wobble_until=wobble_until)
    typing = C.pose("seated", shF=62, elF=38, shB=56, elB=44, head=6, lean=10, eyeY=.6)
    t_lean = t_lean if t_lean is not None else t_on + 2.0
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
    if close:      # the answer: start on face and screen, push onto the screen as EV lands
        sx, sy = 960 + (mx - 960) / .85, 540 + (my - 540) / .85
        cam = [[0, cx + 30, cy - 10, 1.38], [t_cash, cx + 60, cy - 14, 1.5, "sine"], [dur, sx - 30, sy - 6, 1.95, "inout"]]
    else:
        cam = [[0, 760, 620, 1.12], [t_on + 1.2, cx + 30, cy - 10, 1.38, "sine"], [dur, cx, cy, 1.6, "inout"]]
    shot = dict(dur=dur, layers=layers, actors=[analyst], cam=cam, focus=[[0, .82], [t_on + 1, .85], [dur, .85]], dof=6, band=.3,
                shake=.4, grade="dusk", vig=.9)
    # foley tied to the picture: a soft mallet as equity grows and as EV appears; with the answer, a low mallet as
    # the cash lifts off and a high one as EV lands, then the tick
    fx = [("hit", t_on + .05, .32, .2, dict(pitch=262)), ("hit", t_on + .72, .28, .2, dict(pitch=330))]
    if t_cash is not None:
        fx += [("hit", t_cash + .22, .34, .25, dict(pitch=196))]
    if t_ans is not None:
        fx += [("hit", t_ans + .02, .40, .25, dict(pitch=392)), ("hit", t_ans + .62, .36, .25, dict(pitch=523))]
    return [shot], fx


def hook_film(dur, w, h, t_end):
    return office(dur, w, h, t_on=.35, t_lean=max(1.8, t_end - .9), wobble_until=max(2.0, t_end - .4))


def l4_film(dur, w, h, m):
    # the question is asked from m["q"]; equity grows as it starts, the EV column follows; on the answer's
    # second sentence ("when cash is bigger than debt") the cash lifts off, and EV lands with the third
    return office(dur, w, h, t_on=m["q"] + .2, t_cash=m["a"] + 1.0, t_ans=m["a"] + 2.6, t_lean=m["a"] + 3.4, close=True)


EP = dict(
    slug="w2-levels-14",
    kicker="IB INTERVIEW LEVELS #14",
    hook=dict(
        say=[("Can a company's enterprise value be lower than its equity value?",
              "Can enterprise value be lower than equity value?")],
        sub="4 interview questions. Each one harder.",
        qsize=72,
        hl=["equity value?"],
        film=hook_film,
        film_w=754, film_h=366, foley_gain=.3, sub_gap=28,
    ),
    levels=[
        dict(tail="easy.", think=1.0, ans_min=0,
             scene=lambda m, w, h: level_picture("ev_whole", m, w, h), scene_h=318, lock=150,
             q=[("What's enterprise value?", "What's enterprise value?")],
             hl=["enterprise value?"],
             a=[("The value of the whole business.", "The value of the whole business.", "big"),
                ("What it's worth to lenders and shareholders, together.", "What it's worth to lenders and shareholders, together.")],
             bigsize=80),
        dict(tail="medium.", think=1.4, ans_min=0,
             scene=lambda m, w, h: level_picture("ev_bridge", m, w, h), scene_h=370, lock=150,
             q=[("Equity value is a hundred.", "Equity value is $100."),
                ("Debt's forty, and cash is ten.", "Debt's $40, and cash is $10."),
                ("What's enterprise value?", "What's enterprise value?")],
             hl=["enterprise value?"], qsize=52,
             a=[("A hundred and thirty.", "$130.", "big"),
                ("A hundred, plus forty, minus ten.", "100, plus 40, minus 10.")],
             bigsize=110),
        dict(tail="tricky.", think=1.6, ans_min=0,
             scene=lambda m, w, h: level_picture("ev_borrow", m, w, h), scene_h=320, lock=150,
             q=[("The company borrows fifty and keeps it as cash.", "The company borrows $50 and keeps it as cash."),
                ("What happens to E V?", "What happens to EV?")],
             hl=["EV?"], qsize=54,
             a=[("Nothing.", "Nothing.", "big"),
                ("Debt's up fifty, and so is cash.", "Debt's up $50, and so is cash."),
                ("They cancel out.", "They cancel out.")],
             bigsize=110),
        dict(label="Here's the last one.", tail="final boss.", think=2.0, ans_min=0,
             film=l4_film, film_w=754, film_h=284, film_gap=20, foley_gain=.3, lock=150,
             q=[("Can enterprise value be lower than equity value?", "Can enterprise value be lower than equity value?")],
             hl=["equity value?"], qsize=56,
             # the filmed screen under the answer carries the working (equity $100, debt $0, cash $30 off, EV $70)
             a=[("Yes.", "Yes.", "big"),
                ("When cash is bigger than debt.", "When cash is bigger than debt."),
                ("A hundred of equity, no debt, thirty of cash, so E V is seventy.", "$100 equity, no debt, $30 cash, so EV is $70.")],
             bigsize=110),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments.")],
               cols={"comments.": RED}),
    speed=1.0,
    fx_gain=.7, tp=-1.8,          # 15 Nov: no de-noise on HEART (audio-standard 1b: the narrator chain stays natural)
)

if __name__ == "__main__":
    if "keep" in sys.argv:
        make(EP, "HEART", keep_voice=True)
    else:
        make(EP, *(sys.argv[1:2] or ["HEART"]))
