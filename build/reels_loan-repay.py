"""
Levels #15: four interview questions on a loan through the three statements, each one harder. The hook asks the
last level first.

A company borrows $100 at 10% a year; the tax rate is 25%; interest is tax deductible and paid in cash, and so is
the tax. Textbook three-statement mechanics with round example numbers; no company, deal or "typical" figure is
claimed.

Every answer, worked:
    L1  Borrowing $100 is not income: it is money the company owes back. Balance sheet: cash +100 (asset), debt
        +100 (liability). Cash flow statement: +100 in financing. The income statement does not move.
    L2  Interest = 10% x 100 = 10, an expense. Pre-tax income -10; tax falls by 10 x 25% = 2.50; net income falls
        by 10 - 2.50 = 7.50 (= 10 x (1 - 25%)).
    L3  After the year (interest and tax paid in cash, no principal repaid): cash flow from operations starts from
        net income, -7.50, with no non-cash item to add back, so cash is down 7.50. On the other side, debt is
        still 100 and retained earnings (equity) fall by the 7.50 of lower net income: assets -7.50 = liabilities
        0 + equity -7.50. It balances.
    L4  Repaying the $100 of principal is not an expense, so net income does not change (interest is the
        expense; the principal is the loan itself going back). Cash -100 and debt -100 on the balance sheet;
        -100 in financing on the cash flow statement.
    Bonus (comment): same loan, but the 10 of interest is paid in kind (added to the loan, no cash paid), still tax
        deductible. Net income still falls by 7.50; cash flow from operations adds back the 10 of non-cash
        interest: -7.50 + 10 = +2.50, so cash goes UP by 2.50 (the tax saved). Check: assets +2.50 = debt +10 +
        equity -7.50.

Spoken text writes numbers as words; the screen uses digits.

16 Nov, the 15 Nov Reel's next improvement (mean motion only just beat the day before: 1.63 vs 1.62):
  - idle life between the cues: in every drawing something keeps moving while the question is asked and the
    clock runs (notes keep travelling from the lender, the $100 sack bobs, the lender's pennant and the tags swing,
    the red interest block bobs and the tax piece breathes, the balance sways a degree around its tip, every
    question mark bobs); new motion.py fx breathe and bob;
  - every key move on its word: levels.py keeps each word's moment (m["qw"], m["aw"], the karaoke's spread) and
    passes them to scenes and to filmed windows; level 4's columns fall on 'cash' and NET INCOME lands on
    'expense' (before: a fixed offset from the answer's start);
  - action-timed sound in the drawn levels (scene_fx, laid like a film's foley): the sack lands, the stamp, the two
    tags clink, the interest block lands, the tax piece clinks, the balance clanks as it tips and levels.
Two filmed beats: the hook (the analyst at his desk; on his monitor CASH and DEBT at $100, a red REPAY arrow and
NET INCOME ?) and level 4 (closer: both columns fall to zero together, NET INCOME $0, NO CHANGE, a tick).
No badge: a generic illustration, not a reconstruction of a real event; the screens show only the worked numbers.

    python3 build/reels_loan-repay.py HEART
"""

import sys

from levels import make, word, RED, TEAL
from sketch import level_picture, loan_in_fx, interest_bite_fx, bs_tilt_fx
import cine as C
import cine_lib as CL


def office(dur, w, h, t_on, t_drop=None, t_ans=None, t_lean=None, close=False, wobble_until=None):
    """The analyst at his desk with the loan monitor; shot seconds. close=True starts nearer the screen."""
    lay_, anc = CL.office_today()
    mx, my = anc["monitor"]
    mon = CL.monitor_loan(t_on=t_on, t_drop=t_drop, t_ans=t_ans, cx=mx, cy=my, w=480, h=290, wobble_until=wobble_until)
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
    if close:      # level 4: start on face and screen, push onto the screen as the columns fall
        sx, sy = 960 + (mx - 960) / .85, 540 + (my - 540) / .85
        cam = [[0, cx + 30, cy - 10, 1.38], [t_drop, cx + 60, cy - 14, 1.5, "sine"], [dur, sx - 30, sy - 6, 1.95, "inout"]]
    else:
        cam = [[0, 760, 620, 1.12], [t_on + 1.2, cx + 30, cy - 10, 1.38, "sine"], [dur, cx, cy, 1.6, "inout"]]
    shot = dict(dur=dur, layers=layers, actors=[analyst], cam=cam, focus=[[0, .82], [t_on + 1, .85], [dur, .85]], dof=6, band=.3,
                shake=.4, grade="dusk", vig=.9)
    # foley tied to the picture: soft mallets as cash and debt stand up; with the answer, a low mallet as both
    # columns fall and a high one as NET INCOME $0 lands, then the tick
    fx = [("hit", t_on + .1, .3, -.2, dict(pitch=262)), ("hit", t_on + .35, .28, .2, dict(pitch=294))]
    if t_drop is not None:
        fx += [("hit", t_drop + .7, .34, 0, dict(pitch=165))]
    if t_ans is not None:
        fx += [("hit", t_ans + .05, .36, 0, dict(pitch=392)), ("hit", t_ans + .5, .32, 0, dict(pitch=523))]
    return [shot], fx


def hook_film(dur, w, h, t_end):
    return office(dur, w, h, t_on=.35, t_lean=max(1.8, t_end - .9), wobble_until=max(2.0, t_end - .4))


def l4_film(dur, w, h, m):
    # 16 Nov: on the words themselves (film seconds): NET INCOME $0 lands on 'expense', both columns fall on 'cash'
    t_ans = word(m, "expense") - .05
    t_drop = word(m, "cash") - .05
    return office(dur, w, h, t_on=m["q"] + .2, t_drop=t_drop, t_ans=t_ans, t_lean=t_ans + .4, close=True)


EP = dict(
    slug="w2-levels-15",
    kicker="IB INTERVIEW LEVELS #15",
    hook=dict(
        say=[("Does paying back a loan lower net income?", "Does paying back a loan lower net income?")],
        sub="4 interview questions. Each one harder.",
        qsize=72,
        hl=["net income?"],
        film=hook_film,
        film_w=754, film_h=366, foley_gain=.3, sub_gap=28,
    ),
    levels=[
        dict(tail="easy.", think=1.0, ans_min=0,
             scene=lambda m, w, h: level_picture("loan_in", m, w, h), scene_h=296, lock=150,
             scene_fx=loan_in_fx,
             q=[("A company borrows a hundred dollars.", "A company borrows $100."),
                ("Is that income?", "Is that income?")],
             hl=["income?"], qsize=56,
             a=[("No.", "No.", "big"),
                ("Cash and debt both go up a hundred.", "Cash and debt both go up $100."),
                ("The income statement doesn't move.", "The income statement doesn't move.")],
             bigsize=110),
        dict(tail="medium.", think=1.4, ans_min=0,
             scene=lambda m, w, h: level_picture("interest_bite", m, w, h), scene_h=340, lock=150,
             scene_fx=interest_bite_fx,
             q=[("The loan costs ten percent a year.", "The loan costs 10% a year."),
                ("Tax is twenty-five percent.", "Tax is 25%."),
                ("How much does net income fall?", "How much does net income fall?")],
             hl=["fall?"], qsize=52,
             a=[("Seven fifty.", "$7.50.", "big"),
                ("Ten of interest, but tax falls by two fifty.", "$10 of interest, but tax falls by $2.50.")],
             bigsize=110),
        dict(tail="tricky.", think=1.6, ans_min=0,
             scene=lambda m, w, h: level_picture("bs_tilt", m, w, h), scene_h=330, lock=150,
             scene_fx=bs_tilt_fx,
             q=[("After a year, cash is down seven fifty.", "After a year, cash is down $7.50."),
                ("What else falls, so it still balances?", "What else falls, so it still balances?")],
             hl=["balances?"], qsize=54,
             a=[("Equity.", "Equity.", "big"),
                ("Retained earnings drop by the same seven fifty.", "Retained earnings drop by the same $7.50.")],
             bigsize=110),
        dict(label="Here's the last one.", tail="final boss.", think=2.0, ans_min=0,
             film=l4_film, film_w=754, film_h=232, film_gap=18, foley_gain=.3, lock=150,
             q=[("Then it pays the hundred back.", "Then it pays the $100 back."),
                ("Does net income fall?", "Does net income fall?")],
             hl=["fall?"], qsize=52,
             # the filmed screen under the answer carries the working (cash and debt -$100, net income $0)
             a=[("No.", "No.", "big"),
                ("Paying back the loan isn't an expense.", "Paying back the loan isn't an expense."),
                ("Cash and debt both drop a hundred.", "Cash and debt both drop $100.")],
             bigsize=110),
    ],
    close=dict(say=[("What's your score out of four?", "What's your score out of 4?"),
                    ("Put it in the comments.", "Put it in the comments.")],
               cols={"comments.": RED}),
    speed=1.0,
    fx_gain=.7, tp=-1.8,          # no de-noise on HEART (audio-standard 1b: the narrator chain stays natural)
)

if __name__ == "__main__":
    if "keep" in sys.argv:
        make(EP, "HEART", keep_voice=True)
    else:
        make(EP, *(sys.argv[1:2] or ["HEART"]))
