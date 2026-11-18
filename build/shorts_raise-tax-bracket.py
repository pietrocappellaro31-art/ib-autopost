"""
YouTube Short, Format E (a myth), 18 Nov 2026, on the story engine (build/story.py), narrator HEART (Kokoro af_heart,
en-us, 0.9), black ground. The myth: a raise that pushes you into a higher tax bracket can leave you with less. The
evidence: US federal income tax comes in layers, and the higher rate applies only to the dollars in the new bracket.
Worked with the 2026 single-filer brackets: a $1,000 raise from $50,400 to $51,400 of taxable income adds $220 of
tax and leaves $780 more after federal income tax; the whole bill is still about 11.7% of income. The correct
reading: the brackets alone cannot make a raise cost you.

Sources (all opened in this run, 18 Nov 2026):
    [1] IRS, "IRS releases tax inflation adjustments for tax year 2026, including amendments from the One, Big,
        Beautiful Bill" (Rev. Proc. 2025-32).
        https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill
        Single filers, 2026: 10% for $12,400 or less; 12% over $12,400; 22% over $50,400; 24% over $105,700; 32% over
        $201,775; 35% over $256,225; 37% over $640,600. (Standard deduction $16,100: not used; we speak of taxable
        income throughout.)
    [2] Tax Foundation, "2026 Tax Brackets" (Table 1). https://taxfoundation.org/data/all/federal/2026-tax-brackets/
        Single: 10% $0 to $12,400; 12% $12,401 to $50,400; 22% $50,401 to $105,700 (agrees with [1]).
    [3] IRS, "Federal income tax rates and brackets". https://www.irs.gov/filing/federal-income-tax-rates-and-brackets
        "When your income jumps to a higher tax bracket, you don't pay the higher rate on your entire income. You pay
        the higher rate only on the part that's in the new tax bracket."

Our arithmetic (2026, single filer, taxable income, federal income tax only; checked with a short script in this run):
    Tax on $50,400 = 10% x 12,400 + 12% x (50,400 - 12,400) = 1,240 + 4,560 = $5,800.
    Tax on $51,400 = 5,800 + 22% x 1,000 = 5,800 + 220 = $6,020.
    The raise: +$1,000 of income, +$220 of tax, +$780 after federal income tax.
    Average rate after the raise: 6,020 / 51,400 = 11.71%, "still under 12%", drawn 11.7%.
    Take-home after federal income tax only: 50,400 - 5,800 = $44,600; 51,400 - 6,020 = $45,380 (+$780).
    Scope (on screen and in the description): federal income tax brackets only; payroll and state taxes, credits and
    benefits with income limits are not part of this and are not claimed either way.

Beats, checked:
    hook     a $1,000 raise into the 22% bracket ([1]: 22% starts over $50,400).
    myth     the belief that the higher rate hits all your pay; [3] says it doesn't.
    layers   10% to $12,400, 12% to $50,400, 22% above ([1], [2]); the column is drawn to scale.
    raise    $50,400 to $51,400: only the last $1,000 at 22% = $220; $780 kept (our arithmetic on [1]).
    total    $5,800 to $6,020, 11.7% of income (our arithmetic).
    rule     so the brackets alone can't make a raise cost you (follows from [3]: the higher rate touches only the
             dollars above the line, so the added tax is a share, under 100%, of the added income).
    close    the viewer's own belief. No advice.

    python3 build/shorts_raise-tax-bracket.py HEART
"""

import random
import sys

from motion import A
from sketch import picture, _ptag
from story import make, RED

TEAL_INK, GOLD = "#5EC8B4", "#F2C35B"
PIC = dict(w=752, h=640)


def chip(label, fill, w=190, color="#fff"):
    return (f'<svg width="{w}" height="{w * .6:.0f}" viewBox="0 0 {w} {w * .6:.0f}" style="overflow:visible">'
            + _ptag(w / 2, w * .3, w * .95, label, fill, color, round(w * .23)) + "</svg>")


def floaters(total):
    """Faint bracket tags drifting at the edges, clear of the text (never the answer: no $780, $220 or 11.7%)."""
    out = ""
    for k, (x, y, lab, fill, w) in enumerate([(-90, 330, "10%", "#7FB59B", 170), (770, 560, "22%", RED, 170),
                                              (-100, 1030, "12%", GOLD, 170), (770, 1120, "$1,000", "#0F766E", 200)]):
        out += (f'<div style="position:absolute;left:{x}px;top:{y}px;opacity:.14">'
                + A(chip(lab, fill, w, "#0A0A0A" if fill in (GOLD, "#7FB59B") else "#fff"), "float", 0, 1, amp=20, w=.5 + .1 * k, ph=k * 1.7)
                + "</div>")
    return out


def rain(t0, dur):
    """Tags falling in under the comment ask, then bobbing."""
    rnd = random.Random(18)
    out = ""
    labs = [("10%", "#7FB59B"), ("12%", GOLD), ("22%", RED), ("+$780", "#0F766E"), ("$1,000", GOLD)]
    for k, (lab, fill) in enumerate(labs):
        x, y = rnd.uniform(-10 + 150 * k, 10 + 150 * k), rnd.uniform(1040, 1120)
        art = chip(lab, fill, rnd.uniform(130, 160), "#0A0A0A" if fill in (GOLD, "#7FB59B") else "#fff")
        out += A(A(art, "float", 0, 1, amp=8, w=1.4, ph=k), "move", t0 + .1 + .07 * k, .9, y=-1700,
                 style=f"position:absolute;left:{x:.0f}px;top:{y:.0f}px")
    return out


EP = dict(
    slug="shorts-raise-tax-bracket",
    kicker="MONEY MYTHS",
    mood="curious",
    cover=dict(at=("e", 0, 1, .4), lines=["A $1,000 raise.", "Into the 22% bracket.", "Take home less?"],
               hl={"$1,000": TEAL_INK, "22%": RED, "less?": RED}, avoid=["$780", "$220", "11.7%"]),     # not "MYTH": the kicker reads MONEY MYTHS
    beats=[
        dict(tag="THE RAISE", size=66, hold=.75, hl=["$1,000 raise", "22% bracket."],
             say=[("A thousand dollar raise pushes you into the twenty two percent bracket.",
                   "A $1,000 raise pushes you into the 22% bracket."),
                  ("Could you take home less?", "Could you take home less?")],
             art=lambda t0, d, seg: picture("tb_hook", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .92), "thump", .12), (("s", 1, .85), "clink", .07)]),       # block lands; wallet lands
        dict(tag="THE MYTH", hl=["all your pay.", "It doesn't."],
             say=[("Many think the higher rate hits all your pay.",
                   "Many think the higher rate hits all your pay."),
                  ("It doesn't.", "It doesn't.")],
             art=lambda t0, d, seg: picture("tb_myth", t0, d, seg=seg, **PIC),
             sfx=[(("s", 1, .3), "thump", .14)]),                                         # the MYTH stamp lands
        dict(tag="THE LAYERS", hl=["layers.", "10%", "12%", "22%"],
             say=[("Tax comes in layers.", "Tax comes in layers."),
                  ("Ten percent on the first twelve thousand four hundred, twelve percent up to fifty thousand four hundred.",
                   "10% on the first $12,400, 12% up to $50,400."),
                  ("Twenty two percent above that.", "22% above that.")],
             art=lambda t0, d, seg: picture("tb_layers", t0, d, seg=seg, **PIC),
             sfx=[(("s", 1, .25), "paper", .06), (("s", 1, 2.96), "paper", .06), (("s", 2, .35), "pop", .06)]),
        dict(tag="THE RAISE, WORKED", hl=["$220.", "$780."],
             say=[("Say you go from fifty thousand four hundred to fifty one thousand four hundred.",
                   "Say you go from $50,400 to $51,400."),
                  ("Only that last thousand pays twenty two percent: two hundred and twenty dollars.",
                   "Only that last $1,000 pays 22%: $220."),
                  ("You keep seven hundred and eighty.", "You keep $780.")],
             art=lambda t0, d, seg: picture("tb_raise", t0, d, seg=seg, **PIC),
             # the block lands, the $220 slice drops into the tray, three coins land on what you keep
             sfx=[(("s", 0, .91), "thump", .1), (("s", 1, 5.1), "knock", .06), (("s", 2, .9), "clink", .06),
                  (("s", 2, 1.05), "clink", .06), (("s", 2, 1.2), "clink", .06)]),
        dict(tag="THE WHOLE BILL", hl=["$6,020.", "under 12%"],
             say=[("Your total tax goes from five thousand eight hundred to six thousand and twenty.",
                   "Your total tax goes from $5,800 to $6,020."),
                  ("That's still under twelve percent of your income.", "That's still under 12% of your income.")],
             art=lambda t0, d, seg: picture("tb_total", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .57), "paper", .07)] + [(("s", 1, .1 + .15 * j), "tick", .035) for j in range(7)]),
        dict(tag="THE RULE", hl=["can't"],
             say=[("So the brackets alone can't make a raise cost you.", "So the brackets alone can't make a raise cost you.")],
             art=lambda t0, d, seg: picture("tb_rule", t0, d, seg=seg, **PIC),
             sfx=[(("s", 0, .25), "paper", .06), (("s", 0, .45), "paper", .06), (("s", 0, 2.53), "pop", .07)]),
    ],
    close=dict(say=[("Did you think a raise could cost you?", "Did you think a raise could cost you?"),
                    ("Tell me in the comments.", "Tell me in the comments.")],
               cols={"comments.": RED}, art=rain,
               pic=lambda t0, d: picture("tb_asks", t0, d, w=520, h=416)),
    floaters=floaters,
    speed=1.0,            # HEART's own pace, 0.9, comes from voices.json
    music=False,          # the clean mix is the score gate's reference; the delivered file is the scored one (17 Nov)
    lufs=-14,
    room=.0003,
)

if __name__ == "__main__":
    if "remix" in sys.argv:            # effects moved onto their actions: same picture, same takes
        from story import remix
        remix(EP, "HEART")
    else:
        make(EP, *(sys.argv[1:2] or ["HEART"]))
