"""
Levels #16 (Reel A, 17 Nov 2026): four interview questions that go from a valuation multiple to a share price, then
ask what a dividend paid with new debt does to that price. The hook asks the last level first.

Textbook comparable-company arithmetic with round example numbers; no company, deal or "typical" multiple is
claimed. Assumptions, stated here and kept on screen where they matter: the business does not change, so it keeps
the same EV/EBITDA multiple and the same enterprise value; no taxes, fees or signalling effects.

Every answer, worked:
    L1  EBITDA $50; similar companies trade at 8x EV/EBITDA. Enterprise value = 8 x 50 = $400.
    L2  Debt $100, cash $20. Equity value = EV - debt + cash = 400 - 100 + 20 = $320.
    L3  40 shares. Value per share = 320 / 40 = $8.
    L4  The company borrows $60 more and pays all of it out as a dividend. The business is the same, so EV stays
        $400. Net debt goes from 100 - 20 = 80 to 80 + 60 = 140 (the cash came in and went straight out). Equity
        value = 400 - 140 = $260; per share = 260 / 40 = $6.50. The dividend per share = 60 / 40 = $1.50, and
        8.00 - 6.50 = 1.50: the share price falls by the dividend; a shareholder holds $6.50 + $1.50 = $8, no richer
        and no poorer (before taxes).
    Hook: "$60 of new debt, paid out as a dividend: does the share price fall?" Yes, by the $1.50 a share paid out.
    Bonus (comment): same $60 of new debt, but spent buying back shares at $8. Shares bought = 60 / 8 = 7.5, so 32.5
        remain; equity value = 400 - 140 = 260; per share = 260 / 32.5 = $8. The price does not move.

Spoken text writes numbers as words; the screen uses digits.

17 Nov, from the performance data (docs/daily/performance.md, 12 Reels): 4 of the 5 Reels with 1,000+ reach opened on
concrete numbers (the $100 / $150 MOIC loop, "2x in 3 years, or 3x in 7", "1 number on that income statement is
wrong", "20x earnings buys one at 10x"); all 6 Reels at 125 to 139 reach opened on an abstract yes/no ("Can X be
negative?", "Does more debt always lower WACC?"). So the hook leads with the number: "$60 of new debt".

17 Nov, the 16 Nov Reel's next improvement: level 4 has two answer lines (the big one and one more) and a taller film
(320 px, was 232) with the camera pushing onto the share column as it falls; every level drawing keeps moving through
its answer (level 1's stack breathes in a wave, the debt slice bobs, the share tiles ripple) instead of stopping at it.
Two filmed beats: the hook (the analyst at his desk; on the monitor EV $400 that never moves, the $8 share, a red NEW
DEBT +$60 tag pulsing, an arrow to PAID OUT, a ? over the share) and level 4 (the share falls to $6.50 on the
answer, a $1.50 coin goes to PAID OUT on '$1.50', $6.50 + $1.50 = $8 lands with a tick a second later). No badge: a generic
illustration, not a reconstruction of a real event; the screens show only the worked numbers.

    python3 build/reels_dividend-recap.py HEART
"""

import sys

from levels import make, word, RED, TEAL
from sketch import level_picture, multiple_stack_fx, ev_to_equity_fx, share_grid_fx
import cine as C
import cine_lib as CL


def office(dur, w, h, t_on, t_ans=None, t_cash=None, t_sum=None, t_lean=None, close=False, wobble_until=None):
    """The analyst at his desk with the dividend monitor; shot seconds. close=True starts nearer the screen."""
    lay_, anc = CL.office_today()
    mx, my = anc["monitor"]
    mon = CL.monitor_recap(t_on=t_on, t_ans=t_ans, t_cash=t_cash, t_sum=t_sum, cx=mx, cy=my, w=480, h=290, wobble_until=wobble_until)
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
    sx, sy = 960 + (mx - 960) / .85, 540 + (my - 540) / .85
    if close:      # level 4: start on face and screen, push onto the share column as it falls
        cam = [[0, cx - 60, cy + 10, 1.25], [t_ans, cx + 60, cy - 14, 1.55, "sine"], [dur, sx - 20, sy - 4, 2.0, "inout"]]
    else:
        cam = [[0, 760, 620, 1.12], [t_on + 1.2, cx + 30, cy - 10, 1.38, "sine"], [dur, cx, cy, 1.6, "inout"]]
    shot = dict(dur=dur, layers=layers, actors=[analyst], cam=cam, focus=[[0, .82], [t_on + 1, .85], [dur, .85]], dof=6, band=.3,
                shake=.4, grade="dusk", vig=.9)
    # foley tied to the picture: a soft mallet as the share column stands; with the answer a low mallet as the
    # column falls, a clink as the coin lands in PAID OUT, a high mallet and the tick on the sum
    fx = [("hit", t_on + .1, .3, 0, dict(pitch=262))]
    if t_ans is not None:
        fx += [("hit", t_ans + .5, .34, 0, dict(pitch=165))]
    if t_cash is not None:
        fx += [("clink", t_cash + .8, .3, .3)]
    if t_sum is not None:
        fx += [("hit", t_sum + .1, .32, 0, dict(pitch=392)), ("hit", t_sum + .55, .3, 0, dict(pitch=523))]
    return [shot], fx


def hook_film(dur, w, h, t_end):
    return office(dur, w, h, t_on=.35, t_lean=max(1.8, t_end - .9), wobble_until=max(2.0, t_end - .4))


def l4_film(dur, w, h, m):
    # on the words themselves (film seconds): the share falls on '$6.50', the coin leaves on '$1.50', the sum 1 s later
    t_ans = word(m, "$6.50") - .05
    t_cash = word(m, "$1.50") - .05
    t_sum = t_cash + 1.0
    return office(dur, w, h, t_on=m["q"] + .2, t_ans=t_ans, t_cash=t_cash, t_sum=t_sum, t_lean=t_ans + .4, close=True)


EP = dict(
    slug="w2-levels-16",
    kicker="IB INTERVIEW LEVELS #16",
    hook=dict(
        say=[("Sixty dollars of new debt, paid out as a dividend: does the share price fall?",
              "$60 of new debt, paid out as a dividend: does the share price fall?")],
        sub="4 interview questions. Each one harder.",
        qsize=68,
        hl=["$60", "share price fall?"],
        film=hook_film,
        film_w=754, film_h=300, foley_gain=.3, sub_gap=28,
    ),
    levels=[
        dict(tail="easy.", think=1.0, ans_min=0,
             scene=lambda m, w, h: level_picture("multiple_stack", m, w, h), scene_h=260, lock=150,
             scene_fx=multiple_stack_fx,
             q=[("A company makes fifty dollars of EBITDA.", "A company makes $50 of EBITDA."),
                ("Similar companies trade at eight times EBITDA.", "Similar companies trade at 8x EBITDA."),
                ("What's its enterprise value?", "What's its enterprise value?")],
             hl=["enterprise value?"], qsize=50,
             a=[("Four hundred dollars.", "$400.", "big"),
                ("Eight times fifty.", "8 x $50.")],
             bigsize=110),
        dict(tail="medium.", think=1.4, ans_min=0,
             scene=lambda m, w, h: level_picture("ev_to_equity", m, w, h), scene_h=290, lock=150,
             scene_fx=ev_to_equity_fx,
             q=[("It has a hundred dollars of debt and twenty of cash.", "It has $100 of debt and $20 of cash."),
                ("What's the equity value?", "What's the equity value?")],
             hl=["equity value?"], qsize=54,
             a=[("Three twenty.", "$320.", "big"),
                ("Take off the debt, add back the cash.", "Take off the debt, add back the cash.")],
             bigsize=110),
        dict(tail="tricky.", think=1.6, ans_min=0,
             scene=lambda m, w, h: level_picture("share_grid", m, w, h), scene_h=300, lock=150,
             scene_fx=share_grid_fx,
             q=[("There are forty shares.", "There are 40 shares."),
                ("What's one share worth?", "What's one share worth?")],
             hl=["worth?"], qsize=56,
             a=[("Eight dollars.", "$8.", "big"),
                ("Three twenty divided by forty.", "$320 / 40.")],
             bigsize=120),
        dict(label="Here's the last one.", tail="final boss.", think=2.0, ans_min=0,
             film=l4_film, film_w=754, film_h=320, film_gap=18, foley_gain=.3, lock=150,
             q=[("It borrows sixty more to pay a dividend.", "It borrows $60 more to pay a dividend."),
                ("What's a share worth now?", "What's a share worth now?")],
             hl=["worth now?"], qsize=50,
             # two answer lines (the 16 Nov next improvement); the filmed screen carries the working
             a=[("Six fifty.", "$6.50.", "big"),
                ("Each share got a dollar fifty.", "Each share got $1.50.")],
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
