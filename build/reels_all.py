"""
The week's seven Reels, silent and read-paced.

No voiceover: Pietro uploads these by hand and adds a trending track in the
Instagram app, which the publishing API cannot do and which is worth more on
this format than anything else we control.

Every frame is short on purpose. A silent reel is read at scroll speed, so a
frame carrying more than about a dozen words is a frame nobody finishes.

Sources for the recruiting dates in r02 are in the caption file; they are
Trackr's estimates from last cycle, not bank announcements, and the reel says
so on its last frame.
"""

import sys

from reel import RED, TEAL, WHITE, build

# ---------------------------------------------------------------------------


def rows(*pairs):
    body = "".join(
        f'<div class="row"><span>{label}</span><b style="color:{colour}">{value}</b></div>'
        for label, value, colour in pairs)
    return f'<div class="card">{body}</div>'


def big(text, sub=None, size=104):
    out = f'<h1 style="font-size:{size}px">{text}</h1>'
    if sub:
        out += f'<div class="sub">{sub}</div>'
    return out


def listing(title, items, size=80):
    body = "".join(
        f'<div class="row"><span style="font-size:38px">{a}</span>'
        f'<b style="color:{TEAL};font-size:38px">{b}</b></div>' for a, b in items)
    return f'<h1 style="font-size:{size}px">{title}</h1><div class="card">{body}</div>'


REELS = {}

# --- R1 -------------------------------------------------------- Sat 21:30
REELS["w1-r01-ev-equity"] = [
    ("Enterprise value versus equity value. Get it backwards and the interview ends early.",
     big(f'Enterprise value<br>vs <span style="color:{TEAL}">equity value</span>.',
         "Get it backwards and the interview ends early.")),
    ("Equity value. What the shareholders own.",
     big("Equity value.", "What the shareholders own.<br>Price times diluted shares.")),
    ("Enterprise value. What it costs to buy the whole business.",
     big(f'<span style="color:{TEAL}">Enterprise value.</span>',
         "What it costs to buy the whole business, whoever financed it.")),
    ("The bridge. Equity value, add debt, add preferred and NCI, subtract cash.",
     '<h1 style="font-size:84px">The bridge.</h1>'
     + rows(("Equity value", "start", WHITE), ("Debt", "+", WHITE),
            ("Preferred, NCI", "+", WHITE), ("Cash", "&minus;", RED))),
    ("Why subtract cash. It comes with the company and pays down the debt you took on.",
     big(f'Why <span style="color:{TEAL}">subtract</span> cash?', size=92)
     + ""),
    ("Because it comes with the company. You use it to repay the debt you borrowed to buy it.",
     big("It comes with the company.",
         "You use it to repay the debt you borrowed to buy it.", size=86)),
    ("Adding cash is the most common slip on this question.",
     big(f'You <span style="color:{TEAL}">subtract</span> the cash'
         f'<span style="color:{RED}">.</span>',
         "Adding it is the most common slip on this question.", size=92)),
]

# --- R2 -------------------------------------------------------- Sun 21:30
REELS["w1-r02-timeline"] = [
    ("Summer 2028 applications are already open.",
     big(f'Summer 2028 is <span style="color:{TEAL}">already open</span>'
         f'<span style="color:{RED}">.</span>', size=98)),
    ("Evercore opened in September. Raine late September.",
     listing("Already open", [("Evercore", "Sept"), ("Raine Group", "late Sept"),
                              ("PMCF", "early Oct")])),
    ("November. RBC, BMO, Leerink, then LionTree and Perella Weinberg.",
     listing("November", [("RBC, BMO, Leerink", "early"),
                          ("LionTree, Perella Weinberg", "mid"),
                          ("Houlihan, Lincoln, Moelis", "late")])),
    ("December. Barclays, Deutsche Bank, Citi. JP Morgan late December.",
     listing("December", [("Barclays, Deutsche Bank", "early"),
                          ("Citi", "mid"), ("J.P. Morgan", "late")])),
    ("January. Goldman Sachs, Morgan Stanley, Bank of America.",
     listing("January", [("Goldman Sachs", "early"), ("Morgan Stanley", "early"),
                         ("Bank of America", "mid")])),
    ("If you start networking in January you are starting after the first wave has closed.",
     big("Start networking in January",
         "and you are starting after the first wave has already closed.", size=88)),
    ("These are estimates from last cycle, not announcements. Check every bank yourself.",
     big("Check every bank yourself.",
         "These are estimates from last cycle, not announcements. Dates move.",
         size=86)),
]

# --- R3 -------------------------------------------------------- Mon 21:30
REELS["w1-r03-why-banking"] = [
    ("Why investment banking? The answer that gets you dinged.",
     big(f'&ldquo;Why investment banking<span style="color:{RED}">?</span>&rdquo;',
         "The one everybody answers the same way.", size=92)),
    ("I want to learn a lot and work with smart people. Every candidate says this.",
     big("&ldquo;I want to learn, and work with smart people.&rdquo;",
         "So does everyone else in the hallway.", size=80)),
    ("Three parts. Where it started. What you did about it. Why this seat.",
     listing("Three parts", [("Where it started", "1"), ("What you did about it", "2"),
                             ("Why this seat", "3")])),
    ("Where it started has to be one specific moment, not an interest in markets.",
     big("One specific moment.",
         "A deal you followed. A company you watched get bought. Not an interest in markets.",
         size=86)),
    ("What you did about it is the part that proves the first part was true.",
     big(f'What you <span style="color:{TEAL}">did</span> about it.',
         "A club, a model you built, a pitch you wrote. This is the part that proves the first.",
         size=88)),
    ("Why this seat means why banking rather than the next closest thing.",
     big("Why this seat.",
         "Why banking rather than equity research, or consulting, or the fund down the road.",
         size=88)),
    ("If your answer would work for any other job, it is not an answer.",
     big("If it works for any other job,",
         "it is not an answer.", size=90)),
]

# --- R4 -------------------------------------------------------- Tue 21:30
REELS["w1-r04-dinged"] = [
    ("Five answers that get you dinged.",
     big(f'Five answers that get you <span style="color:{RED}">dinged</span>.', size=100)),
    ("I would use a DCF because it is the most accurate.",
     big("&ldquo;A DCF, because it is the most accurate.&rdquo;",
         "It is the most assumption-heavy. Say that instead.", size=78)),
    ("You add cash in the enterprise value bridge.",
     big("&ldquo;Add cash to get enterprise value.&rdquo;",
         "You subtract it. This one ends interviews.", size=82)),
    ("Depreciation goes up by ten so net income falls by ten.",
     big("&ldquo;Depreciation up 10, net income down 10.&rdquo;",
         "Down 7.5 at a 25% rate. The tax shield is real.", size=78)),
    ("Goodwill is the premium paid. Close, but not what they asked.",
     big("&ldquo;Goodwill is the premium paid.&rdquo;",
         "It is purchase price less the fair value of net identifiable assets.", size=78)),
    ("I do not have any questions.",
     big("&ldquo;No, I think you covered everything.&rdquo;",
         "The cheapest way to look uninterested.", size=82)),
    ("Each of these has a better version that takes one extra sentence.",
     big("Every one of these",
         "has a better version that costs you one extra sentence.", size=92)),
]

# --- R5 -------------------------------------------------------- Wed 21:30
REELS["w1-r05-accretion"] = [
    ("Accretive or dilutive, in your head, in five seconds.",
     big(f'Accretive or dilutive<span style="color:{RED}">?</span>',
         "In your head. Five seconds.", size=100)),
    ("All stock deal. Compare the two P E multiples.",
     big("All-stock deal.", "Compare the two P/E multiples.", size=96)),
    ("Acquirer twenty times. Target fifteen times at the offer price.",
     '<h1 style="font-size:84px">The quick check.</h1>'
     + rows(("Acquirer P/E", "20x", TEAL), ("Target P/E", "15x", WHITE))),
    ("Acquirer trades higher than the target, so the deal is accretive.",
     big(f'<span style="color:{TEAL}">Accretive.</span>',
         "The acquirer buys earnings more cheaply than its own are valued.", size=96)),
    ("Flip it. Buying something more expensive than you is dilutive.",
     big("Flip it and it is dilutive.",
         "Paying a higher multiple than your own dilutes your earnings per share.",
         size=86)),
    ("Then say what the rule leaves out. Synergies, fees, the financing mix.",
     listing("Then name what it ignores", [("Synergies", ""), ("Fees", ""),
                                           ("Financing mix", ""), ("Writedowns", "")])),
    ("The rule gets you the direction. Naming its limits gets you the offer.",
     big("The rule gets the direction.",
         "Naming what it ignores gets you the offer.", size=90)),
]

# --- R6 -------------------------------------------------------- Thu 21:30
REELS["w1-r06-words"] = [
    ("Eight words that reveal you have not done the reading.",
     big(f'Eight words that give you <span style="color:{RED}">away</span>.', size=98)),
    ("Profit when you mean net income, EBIT or EBITDA. Say which.",
     big("&ldquo;Profit.&rdquo;", "Net income, EBIT or EBITDA. Say which one.", size=100)),
    ("Valuation when you mean enterprise value or equity value.",
     big("&ldquo;Valuation.&rdquo;",
         "Enterprise value or equity value. They are not the same number.", size=100)),
    ("Cash flow when you mean operating cash flow or free cash flow.",
     big("&ldquo;Cash flow.&rdquo;",
         "Operating, levered or unlevered free cash flow. Pick one.", size=100)),
    ("Debt when you mean gross debt or net debt.",
     big("&ldquo;Debt.&rdquo;", "Gross or net. The bridge cares.", size=100)),
    ("Multiple when you have not said of what, over what period.",
     big("&ldquo;Multiple.&rdquo;",
         "Of what, over which period, forward or trailing.", size=100)),
    ("Precision is the cheapest signal you can send in a first round.",
     big("Precision is the cheapest signal",
         "you can send in a first round.", size=92)),
]

# --- R7 -------------------------------------------------------- Fri 12:30
REELS["w1-r07-questions"] = [
    ("Do you have any questions for me?",
     big(f'&ldquo;Any questions for me<span style="color:{RED}">?</span>&rdquo;',
         "You have one shot to sound like you want the seat.", size=94)),
    ("Not what is the culture like. That answer tells you nothing.",
     big("Not &ldquo;what is the culture like?&rdquo;",
         "You will get the same answer in every interview you sit.", size=86)),
    ("What does the first six months look like for someone who does well?",
     big("&ldquo;What does the first six months look like for someone who does well?&rdquo;",
         size=72)),
    ("What is the last deal you worked on that you would want to talk about?",
     big("&ldquo;What is the last deal you would actually want to talk about?&rdquo;",
         size=74)),
    ("What separates the analyst you keep from the one you do not?",
     big("&ldquo;What separates the analyst you keep from the one you do not?&rdquo;",
         size=74)),
    ("Then one that only works if you did the reading.",
     big("Then one that only works",
         "if you actually did the reading on them.", size=92)),
    ("A question about something they did is the only one they remember.",
     big("Ask about something they did.",
         "It is the only question they remember afterwards.", size=90)),
]

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(REELS)
    for slug in wanted:
        print(slug)
        build(slug, REELS[slug])
