"""
YouTube Short, Format B (financial story), 14 Nov 2026, on the story engine (build/story.py), narrator HEART
(Kokoro af_heart, en-us, 0.9). A Saturday: the cash machine was born because a bank closed on a Saturday.
One recurring character, the trader, plays John Shepherd-Barron in an illustrated reconstruction (marked
"illustration" on the first drawing); today he walks (legs alternating) and turns his head.

Story: beginning (the bank shut on a Saturday), conflict (no cash), turning point (the bath, the idea),
conclusion (the 1967 machine, the cheque, the limit, the four-digit PIN).

Sources (all opened in this run, 14 Nov 2026):
    [1] Barclays, "From the archives: the ATM is 50", 2017. https://home.barclays/news/2017/06/from-the-archives-the-atm-is-50
        The first ATM unveiled 27 June 1967 at a Barclays branch in Enfield, north London; Reg Varney made the first
        withdrawal; Shepherd-Barron (De La Rue) was "unable to cash his cheques after his bank closed on a Saturday
        morning", inspired by chocolate vending machines while in the bath that evening; customers put a cheque
        impregnated with carbon 14 ("a mildly radioactive substance") into a drawer and entered a PIN; £10 at a time;
        four digits because his wife could not remember more than four.
    [2] BBC News, "The man who invented the cash machine", 25 June 2007 (archived copy, docketalarm exhibit 1025).
        https://www.docketalarm.com/cases/PTAB/IPR2018-00150/Inter_Partes_Review_of_U.S._Pat._9559852/11-03-2017-Petitioner/Exhibit-1025-25-The_Man_Who_Invented_The_Cash_Machine,_BBC_NEWS_June_25,_2007/
        "I hit upon the idea of a chocolate bar dispenser, but replacing chocolate with cash"; cheques "impregnated
        with carbon 14, a mildly radioactive substance"; "a maximum of £10 a time"; he could remember his six-figure
        army number, "she said she could only remember four figures, so because of her, four figures became the world
        standard."
    [3] Wikipedia, "John Shepherd-Barron". https://en.wikipedia.org/wiki/John_Shepherd-Barron
        After closing time, unable to withdraw money; the idea in the bath; first machine June 1967 outside the
        Enfield branch of Barclays; withdrawals capped at £10; six digits proposed, his wife could remember four.
        Also: James Goodfellow's card-and-PIN system is cited as prior art and was closer to modern ATMs, so the
        script says "his cash machine" and "Barclays opened", not "he invented the ATM" as an absolute claim.

Beats, checked:
    hook      [1] closed on a Saturday (morning); "couldn't cash his cheque" is [1]'s "unable to cash his cheques".
    idea      [1][2] the bath, that evening; chocolate bar dispenser with cash.
    1967      [1][3] June 1967, Barclays, Enfield, north London.
    cheque    [1][2] paper cheque with carbon 14, mildly radioactive.
    limit     [2][3] £10 a time at most.
    PIN       [1][2][3] six digits wanted, his wife could remember four.
    standard  [2] "four figures became the world standard" (his account, via the BBC); the script says "the
              standard". Not every PIN today is four digits; the line states what happened then, as sourced.
    The drawings are illustrations: the bank, the machine, the notes and the radiation sign are generic shapes of
    our own (no bank logo, no real machine design, no note design).

    python3 build/shorts_first-cash-machine.py HEART
"""

import random
import sys

from motion import A
from sketch import picture, _banknote
from story import make, RED, TEAL

STONE, BATH, BRICKG, CHEQUE, MINT, LILAC, SKY, BUTTER = ("#E8E0D2", "#D6E8EE", "#F2D6BF", "#F5E6B8", "#D2E9E1",
                                                         "#E2DAF0", "#D6E2F3", "#F6E7C8")

WALK = 1.5        # seconds the man walks to the bank door (hook)
WALK2 = 1.4       # to the machine (1967)
STEP = .39        # one step: half a gait cycle at 8 rad/s (sketch.trader)


def note(w):
    h = round(w * .48)
    return f'<svg width="{w}" height="{h}" viewBox="0 0 150 72" style="overflow:visible">{_banknote(0, 0)}</svg>'


def dots(w):
    return (f'<svg width="{w}" height="{w * .45:.0f}" viewBox="0 0 200 90" style="overflow:visible">'
            f'<rect x="3" y="3" width="194" height="84" rx="18" fill="#fff" stroke="#0A0A0A" stroke-width="5"/>'
            + "".join(f'<circle cx="{40 + 40 * j}" cy="45" r="11" fill="#0A0A0A"/>' for j in range(4)) + "</svg>")


def floaters(total):
    """Faint notes and four-dot PIN slips drifting at the edges, clear of the text."""
    out = ""
    for k, (x, y, kind, w) in enumerate([(-110, 330, "note", 200), (730, 560, "dots", 170), (-120, 1010, "dots", 160),
                                         (730, 1120, "note", 190)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(note(w) if kind == "note" else dots(w), "float", 0, 1, amp=22, w=.5 + .1 * k, ph=k * 1.7) + "</div>")
    return out


def rain(t0, dur):
    """Notes and PIN slips falling in under the comment ask, then bobbing."""
    rnd = random.Random(1967)
    out = ""
    for k in range(9):
        x, y = rnd.uniform(-20 + 80 * k, 30 + 80 * k), rnd.uniform(1030, 1110)
        art = dots(rnd.uniform(120, 150)) if k % 2 else note(rnd.uniform(140, 170))
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:rotate({rnd.uniform(-14, 14):.0f}deg)")
    return out


def bath(t0, d, seg):
    swap = seg[1][1] - .5                    # the note turns over as "cash" is said
    return picture("bath_idea", t0, d, w=752, h=640, swap_at=swap)


EP = dict(
    slug="shorts-first-cash-machine",
    kicker="MONEY STORIES",
    mood="playful",
    cover_at=2.5,
    beats=[
        dict(tag="ONE SATURDAY", badge="RECONSTRUCTION", bg=STONE, size=70, hl=["after it had closed."],
             say=[("One Saturday, a man got to his bank after it had closed.",
                   "One Saturday, a man got to his bank after it had closed."),
                  ("He couldn't cash his cheque.", "He couldn't cash his cheque.")],
             art=lambda t0, d: picture("bank_closed", t0, d, w=752, h=640, walk_s=WALK),
             sfx=[(.05 + .25 + STEP * j, "step", .5) for j in range(4)]
                 + [(.05 + WALK + .08, "knock", .16), (.05 + WALK + .72, "pop", .08)]),
        dict(tag="THAT EVENING", badge="RECONSTRUCTION", bg=BATH, size=58, hl=["had an idea."],
             say=[("That evening, in the bath, John Shepherd-Barron had an idea.",
                   "That evening, in the bath, John Shepherd-Barron had an idea."),
                  ("A chocolate bar machine, but with cash.", "A chocolate bar machine, but with cash.")],
             art=bath,
             sfx=[(1.0, "pop", .06), (("e", 1, -.5), "ding", .06)]),
        dict(tag="JUNE 1967", badge="RECONSTRUCTION", bg=BRICKG, hl=["Enfield, north London."],
             say=[("In June nineteen sixty seven, Barclays opened his cash machine in Enfield, north London.",
                   "In June 1967, Barclays opened his cash machine in Enfield, north London.")],
             art=lambda t0, d, seg: picture("cash_machine", t0, d, w=752, h=640, walk_s=WALK2, at_s=seg[0][1] - .5 - t0),
             sfx=[(.05 + .2 + STEP * j, "step", .45) for j in range(3)]
                 + [(("e", 0, -.5 + .18 * k), "paper", .12) for k in range(3)]),
        dict(tag="HOW IT WORKED", badge="RECONSTRUCTION", bg=CHEQUE, hl=["mildly radioactive"],
             say=[("You fed in a paper cheque, laced with mildly radioactive carbon fourteen.",
                   "You fed in a paper cheque, laced with mildly radioactive carbon 14.")],
             art=lambda t0, d, seg: picture("radio_cheque", t0, d, w=752, h=640, at_s=seg[0][1] - .3 - t0),
             sfx=[(("e", 0, -.3), "paper", .14), (("e", 0, .42), "knock", .18)]),
        dict(tag="THE LIMIT", badge="RECONSTRUCTION", bg=MINT, hl=["at most."],
             say=[("It paid out ten pounds at a time, at most.", "It paid out £10 at a time, at most.")],
             art=lambda t0, d, seg: picture("ten_pounds", t0, d, w=752, h=640, at_s=max(seg[0][1] - .25 - t0, 2.45)),
             sfx=[(.05 + .3 + .2 * j, "tick", .05) for j in range(10)] + [(("e", 0, -.25), "thump", .2)]),
        dict(tag="THE PIN", badge="RECONSTRUCTION", split=True, bg=SKY, hl=["remember four."],
             say=[("He wanted a six digit PIN.", "He wanted a six-digit PIN."),
                  ("But his wife said she could only remember four.", "But his wife said she could only remember four.")],
             art=lambda t0, d, seg: picture("pin_six", t0, d, w=752, h=640, cut_s=seg[1][1] - .1 - t0),
             sfx=[(.05 + .25 + .22 * j, "tick", .07) for j in range(6)]
                 + [(("e", 1, -.6), "pop", .07), (("e", 1, .5), "knock", .14)]),
        dict(tag="THE ENDING", bg=BUTTER, hl=["the standard."],
             say=[("So four digits became the standard.", "So four digits became the standard.")],
             art=lambda t0, d: picture("four_dots", t0, d, w=752, h=640),
             sfx=[(("d", .15 + .2 * k), "pop", .06) for k in range(3)]),
    ],
    close=dict(say=[("Four digits or six, which would you pick?", "Four digits or six: which would you pick?"),
                    ("Tell me in the comments.", "Tell me in the comments."),
                    ("And subscribe for more like this.", "And subscribe for more like this.")],
               cols={"comments.": RED}, bg=LILAC, art=rain,
               pic=lambda t0, d: picture("pin_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # clean master: Pietro adds a sound in the YouTube app
    lufs=-14,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or ["HEART"]))
