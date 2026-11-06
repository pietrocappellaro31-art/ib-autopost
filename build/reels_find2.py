"""
Find the error #2: the LBO that "doubled in five years at 20%".

    Entry: EV 500, debt 400, equity 100
    Exit (year 5): EV 600, debt 400, equity 200
    MOIC 200 / 100 = 2.0x                      correct
    IRR shown as 20%                           wrong: 20% is 100% / 5, no compounding
    IRR actual: 2.0 ** (1/5) - 1 = 14.9%       about 15%
    Check: 1.20 ** 5 = 2.49, "about two and a half times"
    Rule of thumb: 2x in 5 years ~ 15%; 3x in 5 years: 3 ** (1/5) - 1 = 24.6%, "about 25"

    KOKORO_DIR=/path/to/kokoro python build/reels_find2.py [voice]
"""

import sys

from findgame import make, RED, TEAL

EP = dict(
    slug="w2-find-the-error-2",
    number=2,
    title="LBO, $M",
    cols=["ENTRY", "EXIT, YR 5"],
    rows=[("Enterprise value", "500", "600"), ("Debt", "400", "400"), ("Equity", "100", "200"),
          ("Years held", "", "5"), ("MOIC", "", "2.0x"), ("IRR", "", "20%")],
    wrong=(5, 1, "20%", "14.9%"),
    hook="One number in this deal is wrong. And it looks completely right. You've got ten seconds.",
    hook_cols={"wrong.": RED, "wrong": RED, "right.": RED, "ten": RED, "seconds.": RED},
    go="Go.",
    look="Check every line.",
    # (sentence, (rows, tone) or None, caption colours, event)
    reveal=[
        [("At exit you've got two hundred of equity, from one hundred.", ([2], "n"), {}),
         ("So you doubled your money.", ([2], "t"), {"doubled": TEAL}),
         ("Two times MOIC is right.", ([4], "t"), {"moic": TEAL, "right.": TEAL})],
        [("But the IRR isn't twenty percent.", ([5], "r"), {"isn't": RED, "twenty": RED, "percent.": RED}, "pen"),
         ("Twenty percent a year for five years would be about two and a half times.", ([5], "r"), {},
          ("chip", "20% a year for 5 years &asymp; 2.5&times;")),
         ("You compound.", ([5], "r"), {"compound.": TEAL}, "strike"),
         ("Doubling in five years is about fifteen percent.", ([5], "t"), {"fifteen": TEAL, "percent.": TEAL}, "fix")],
        [("The shortcut: double in five years, about fifteen.", None, {"fifteen.": TEAL}, ("chip", "2&times; in 5 years &asymp; 15%")),
         ("Triple in five, about twenty five.", None, {"twenty": TEAL, "five.": TEAL}, ("chip", "3&times; in 5 years &asymp; 25%"))],
    ],
    close=["If you caught it, you're ready.", "If not, now you know the trick.", "Follow for two questions a day."],
    speed=.97,
)

if __name__ == "__main__":
    make(EP, *(sys.argv[1:2] or []))
