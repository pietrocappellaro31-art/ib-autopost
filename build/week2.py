"""
The third daily slot: seven more carousels, 08:00 Eastern, 31 Oct to 6 Nov.

Five technical, two on recruiting, chosen so the morning slot does not read
as more of whatever ran at 12:30 the day before.

Technicals checked before writing:

COMPS    Screen on business, size and geography, not on SIC code. EV/EBITDA
         for capital-structure-neutral comparison; P/E only where leverage
         is similar. Calendarise so every company spans the same months.
PREMIUM  An acquirer pays above market because it is buying control and
         because synergies are worth more to it than to the market. The
         premium is the part of the synergies handed to the seller.
GOODWILL Purchase price less the fair value of net identifiable assets
         acquired. Sits on the balance sheet, is tested for impairment
         rather than amortised, and a writedown is a non-cash charge.
NWC      Current assets less current liabilities, excluding cash and debt.
         An increase is a use of cash: the money is sitting in receivables
         and inventory rather than in the account.
PAIRS    The numerator and the denominator must belong to the same people.
         EV pairs with EBIT, EBITDA, revenue and unlevered FCF. Equity
         value pairs with net income, EPS and levered FCF.
"""

import sys

from brand import BOOKMARK, Deck, INK, MUTE, PAPER, RED, TEAL, WHITE, check
from parts import bars, cover, cta, formula, ladder, recap, stake, steps

DECKS = {}


def deck(slug):
    def wrap(fn):
        DECKS[slug] = fn
        return fn
    return wrap


# ====================================================== 08  tell me about yourself
@deck("w1-08-about-you")
def about_you():
    d = Deck("w1-08-about-you", "Recruiting Playbook", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "&ldquo;Tell me about yourself.&rdquo;",
        ["90 seconds", "3 beats", "One thread"],
        "The first 90 seconds decide how the next 29 minutes go."))
    d.slide(INK, WHITE, inner=stake(
        "It is not an icebreaker",
        'It is the only part of the interview you can '
        '<span style="color:#5EC8B4">write in advance</span> and know you will be asked.'))

    d.qa("Ninety seconds. Three beats.", "Three beats",
         steps(["Where you started", "What you chose, and why",
                "Why you are sitting here"]),
         "Past, pivot, present. Each beat earns the next, and the whole thing lands in "
         "about 90 seconds spoken aloud.",
         "Walking the resume top to bottom. They have the resume in front of them.", 76)

    d.qa("Beat one is 20 seconds, not 60.", "20 seconds",
         ladder([("Where you are from, what you study", "15 to 20 sec", TEAL),
                 ("Every club and every job since school", "too long", RED)]),
         "Enough to place you, then move. The interviewer is waiting for the part that is "
         "about them.",
         "Spending half your time before you reach anything about finance.", 72)

    d.qa("Beat two is the only part they remember.", "only part",
         ladder([("A moment that started it", "specific", TEAL),
                 ("What you did next", "the proof", TEAL),
                 ("What that taught you", "the thread", TEAL)]),
         "One decision, what you did about it, and what it told you. This is where a person "
         "appears instead of a candidate.",
         "Listing experiences without ever saying why you chose any of them.", 68)

    d.qa("Beat three points at the door.", "points",
         formula([("which is why I want to be ", INK),
                  ("in this seat, at this bank", TEAL)]),
         "Finish on why you are in this room rather than the next one. It hands them the "
         "follow-up question you want to be asked.",
         "Ending on your resume rather than on the job.", 72)

    d.qa("Then cut it until it is 90 seconds.", "cut it",
         ladder([("Written answer", "about 220 words", MUTE),
                 ("Spoken at interview pace", "about 90 sec", TEAL),
                 ("What most people deliver", "over 3 min", RED)]),
         "Say it out loud with a timer. Anything past 2 minutes is being endured rather "
         "than heard.",
         "Rehearsing it in your head, where it is always faster than out loud.", 68)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("Ninety seconds", [
        ("Where you started", "20 seconds, no more"),
        ("One decision and what you did", "the part they remember"),
        ("What it taught you", "the thread"),
        ("Why this seat", "hands them the follow-up"),
        ("Time it out loud", "not in your head")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Write it. Then cut it in half.",
        ["3 beats, 90 seconds, one thread.",
         "Not the resume read aloud.",
         "Finish pointing at the job."],
        "Later today: how to build a comp set."))
    return d


# ====================================================== 09  comps
@deck("w1-09-comps")
def comps():
    d = Deck("w1-09-comps", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "How do you build a comp set?",
        ["Screen", "Pick the multiple", "Calendarise", "Apply"],
        "Everyone can define comps. Almost nobody can build one."))
    d.slide(INK, WHITE, inner=stake(
        "A comp set is an argument",
        'Every company you include is a claim that the market should value your '
        'target <span style="color:#5EC8B4">the same way</span>.'))

    d.qa("Screen on the business, not the label.", "business",
         ladder([("Same business model", "essential", TEAL),
                 ("Similar size and growth", "essential", TEAL),
                 ("Same geography and customer", "usually", TEAL),
                 ("Same industry code", "not enough", RED)]),
         "Two companies can share an industry classification and have nothing in common "
         "economically. Margin structure and growth matter more than the label.",
         "Pulling a screen by sector code and calling the output a comp set.", 68)

    d.qa("Pick the multiple the capital structure allows.", "capital structure",
         ladder([("EV / EBITDA", "ignores leverage", TEAL),
                 ("EV / EBIT", "if capex differs a lot", TEAL),
                 ("P / E", "only if leverage is similar", RED)]),
         "Enterprise value multiples let you compare companies financed differently. "
         "Price-to-earnings is after interest, so leverage contaminates it.",
         "Quoting P/E across companies with completely different debt loads.", 64)

    d.qa("Calendarise, or you are comparing different years.", "Calendarise",
         ladder([("Target year ends December", "", MUTE),
                 ("Comp year ends June", "6 months out", RED),
                 ("Adjust to a common period", "", TEAL)]),
         "Companies with different fiscal year ends have to be restated to the same twelve "
         "months before any multiple means anything.",
         "Comparing a December filer to a June filer and never mentioning it.", 66)

    d.qa("Use the median, and say why.", "median",
         ladder([("Mean", "one outlier moves it", RED),
                 ("Median", "robust to outliers", TEAL),
                 ("Quartiles", "shows the spread", TEAL)]),
         "Small comp sets have outliers. The median resists them, and the quartile range "
         "tells the reader how much to trust the number.",
         "Quoting a single average and no range at all.", 70)

    d.qa("Then explain the outliers instead of deleting them.", "outliers",
         formula([("Why does this one trade at ", INK),
                  ("twice the median", TEAL), ("?", INK)]),
         "A company far above or below the set is the most interesting thing in it. There is "
         "usually a reason, and naming it is the analysis.",
         "Quietly dropping whatever does not fit the answer you wanted.", 62)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("Building the set", [
        ("Screen on economics, not sector code", "the hard part"),
        ("EV multiples unless leverage matches", "P/E is contaminated"),
        ("Calendarise to a common period", "or nothing compares"),
        ("Median and quartiles, never the mean", "small sets have outliers"),
        ("Explain outliers, do not delete them", "that is the analysis")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "A comp set is an argument.",
        ["Screen on the business model.",
         "EV multiples unless leverage matches.",
         "Median and range, never a bare average."],
        "Tomorrow: why an acquirer pays above the market price."))
    return d


# ====================================================== 10  premium
@deck("w1-10-premium")
def premium():
    d = Deck("w1-10-premium", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "Why pay more than the market price?",
        ["Control", "Synergies", "Scarcity"],
        "The market already priced it. An acquirer pays above that anyway."))
    d.slide(INK, WHITE, inner=stake(
        "Every premium has to be justified to somebody",
        'Usually to shareholders who can see the share price '
        '<span style="color:#5EC8B4">the day before</span>.'))

    d.qa("Three reasons, and only one is financial.", "Three reasons",
         steps(["Control", "Synergies", "Scarcity"]),
         "Control, because a majority lets you set strategy and cash. Synergies, because the "
         "business is worth more inside the acquirer. Scarcity, because there may be no "
         "second asset like it.",
         "Answering &ldquo;synergies&rdquo; and stopping, when control is the first reason.", 70)

    d.qa("Control is worth paying for on its own.", "Control",
         ladder([("Buy 2% of the shares", "no say in anything", MUTE),
                 ("Buy 51%", "set strategy, appoint the board", TEAL),
                 ("Buy 100%", "direct the cash", TEAL)]),
         "A traded share price is what a minority stake costs. Control over strategy, capital "
         "allocation and the board is a different thing and it is not in that price.",
         "Treating the market price as the value of the whole company.", 68)

    d.qa("Synergies split into two kinds.", "two kinds",
         ladder([("Cost: overlapping functions, sites", "credible", TEAL),
                 ("Revenue: cross-sell, new markets", "rarely delivered", RED)]),
         "Cost synergies can be counted and are usually delivered. Revenue synergies are "
         "forecast and frequently are not. Buyers are discounted accordingly.",
         "Quoting a synergy number without saying which kind it is.", 66)

    d.qa("The premium is the part handed to the seller.", "handed",
         bars([("Standalone<br>value", 110, MUTE), ("Synergies", 70, TEAL),
               ("Premium<br>paid", 55, RED)],
              "whatever the buyer keeps is the deal's value to the buyer"),
         "If the acquirer pays away the entire synergy value, the deal makes sense for the "
         "seller and does nothing for the buyer.",
         "Not being able to say who captures the value. That is the whole question.", 66)

    d.qa("So what makes a premium too high?", "too high",
         formula([("Premium paid ", RED), (" &gt; ", MUTE),
                  ("synergies you can actually deliver", TEAL)]),
         "Above that line the acquirer has transferred value to the target's shareholders. "
         "This is why most large acquisitions disappoint.",
         "Calling a deal good because it closed. Closing is not the test.", 64)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("The premium", [
        ("Control is not in the share price", "reason one"),
        ("Cost synergies are credible", "reason two"),
        ("Revenue synergies usually are not", "the discount"),
        ("Scarcity, when there is no second asset", "reason three"),
        ("Who captures the value", "the real question")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Who captures the value?",
        ["Control is not in the traded price.",
         "Cost synergies land, revenue synergies often do not.",
         "Pay away all the synergies and you gained nothing."],
        "Tomorrow: goodwill, and what happens when it is written down."))
    return d


# ====================================================== 11  goodwill
@deck("w1-11-goodwill")
def goodwill():
    d = Deck("w1-11-goodwill", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "What exactly is goodwill?",
        ["Not the premium", "A plug", "Impairment"],
        "The most commonly half-right answer in accounting."))
    d.slide(INK, WHITE, inner=stake(
        "Almost everyone says the premium paid",
        'It is close enough to sound right and wrong enough to '
        '<span style="color:#5EC8B4">cost you the question</span>.'))

    d.qa("The definition, precisely.", "precisely",
         formula([("Purchase price ", INK), ("&minus; fair value of net identifiable "
                                             "assets acquired", TEAL)]),
         "Not price less book value. The acquired assets are first written up or down to "
         "fair value, and goodwill is whatever is left over after that.",
         "Saying &ldquo;the premium over book value&rdquo;. Fair value comes first.", 66)

    d.qa("Where the step-up happens.", "step-up",
         ladder([("Book value of net assets", "600", MUTE),
                 ("Written up to fair value", "750", TEAL),
                 ("Purchase price", "1,000", INK)],
                "Goodwill", "250", RED),
         "Property, brands and customer relationships get revalued, and some intangibles "
         "get recognised for the first time. Goodwill is the residual after all of it.",
         "Jumping straight from 600 to 1,000 and calling 400 goodwill.", 70)

    d.qa("It is not amortised. It is tested.", "tested",
         ladder([("Finite-life intangibles", "amortised", TEAL),
                 ("Goodwill", "tested for impairment", TEAL),
                 ("Goodwill amortised over 10 years", "wrong", RED)]),
         "Under US GAAP and IFRS goodwill sits on the balance sheet indefinitely and is "
         "tested at least annually for impairment.",
         "Amortising it. That was the old rule and it has not applied for years.", 66)

    d.qa("What a writedown does to the statements.", "writedown",
         ladder([("Income statement", "non-cash charge", RED),
                 ("Cash flow statement", "added back, cash unchanged", TEAL),
                 ("Balance sheet", "goodwill down, equity down", RED)]),
         "It hits reported earnings and equity but costs nothing in cash. It is an admission "
         "that the acquisition was worth less than was paid.",
         "Saying it reduces cash. Nothing leaves the building.", 64)

    d.qa("Why it matters beyond the accounting.", "beyond",
         formula([("A large impairment is ", INK),
                  ("the buyer admitting it overpaid", TEAL)]),
         "Goodwill on the balance sheet is the record of what was paid above identifiable "
         "value. An impairment is that record being corrected in public.",
         "Treating it as a bookkeeping entry with no information in it.", 66)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("Goodwill", [
        ("Price less fair value of net assets", "not book value"),
        ("Assets are stepped up first", "then the residual"),
        ("Tested, never amortised", "the old rule is gone"),
        ("A writedown is non-cash", "earnings and equity only"),
        ("It is an admission of overpaying", "the information in it")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Fair value first. Residual second.",
        ["Price minus fair value of net identifiable assets.",
         "Tested for impairment, not amortised.",
         "A writedown costs earnings, not cash."],
        "Tomorrow: net working capital, and why growth eats it."))
    return d


# ====================================================== 12  working capital
@deck("w1-12-nwc")
def nwc():
    d = Deck("w1-12-nwc", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "Net working capital.",
        ["What is in it", "What is not", "Why it eats cash"],
        "An increase is a use of cash. Know why before you are asked."))
    d.slide(INK, WHITE, inner=stake(
        "It is the line that turns profit into cash",
        'or <span style="color:#5EC8B4">stops it</span>, which is why it sits in every '
        'cash flow forecast you will ever build.'))

    d.qa("What goes in, and what is excluded.", "excluded",
         ladder([("Receivables, inventory, prepaid", "in", TEAL),
                 ("Payables, accrued expenses", "in", TEAL),
                 ("Cash", "out", RED),
                 ("Short-term debt", "out", RED)]),
         "Operating current assets less operating current liabilities. Cash and debt are "
         "financing, so they are stripped out.",
         "Using textbook current assets minus current liabilities, which includes both.", 62)

    d.qa("Why an increase is a use of cash.", "use of cash",
         ladder([("Receivables up 50", "cash out", RED),
                 ("Inventory up 30", "cash out", RED),
                 ("Payables up 20", "cash in", TEAL)],
                "Change in NWC", "60 used", RED),
         "Money sitting in receivables and inventory is money not in the account. Paying "
         "suppliers later is an interest-free loan in the other direction.",
         "Getting the sign backwards, which inverts the whole cash flow forecast.", 66)

    d.qa("The cash conversion cycle, in days.", "in days",
         formula([("DSO + DIO ", INK), ("&minus; DPO", TEAL)]),
         "Days to collect, plus days of inventory, minus days you take to pay. The result is "
         "how long your cash is tied up before it comes back.",
         "Knowing the three ratios and not being able to combine them.", 72)

    d.qa("Some businesses run it negative.", "negative",
         ladder([("Supermarket: customers pay instantly", "cash first", TEAL),
                 ("Pays suppliers in 45 days", "cash later", TEAL)],
                "Growth funds itself", "negative NWC", TEAL),
         "Collect before you pay and growth generates cash instead of consuming it. It is "
         "why retail and subscription models can expand without financing.",
         "Assuming working capital always rises with revenue.", 64)

    d.qa("Which is why it belongs in the DCF.", "DCF",
         formula([("EBIT(1 &minus; t) + D&amp;A &minus; capex ", INK),
                  ("&minus; &Delta;NWC", TEAL)]),
         "Free cash flow is after the working capital the growth required. Leave it out and "
         "you have valued a company that never funds its own expansion.",
         "Dropping the term because it is small this year. It scales with growth.", 62)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("Working capital", [
        ("Operating items only", "cash and debt excluded"),
        ("An increase uses cash", "get the sign right"),
        ("DSO plus DIO minus DPO", "the cycle in days"),
        ("Negative is possible and powerful", "growth funds itself"),
        ("It sits inside free cash flow", "not an afterthought")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "An increase is a use of cash.",
        ["Operating items only, no cash, no debt.",
         "DSO plus DIO minus DPO.",
         "It scales with growth, so it stays in the model."],
        "Tomorrow: which multiple pairs with which number."))
    return d


# ====================================================== 13  pairs
@deck("w1-13-multiples")
def multiples():
    d = Deck("w1-13-multiples", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "Why is there no P / EBITDA?",
        ["Numerator", "Denominator", "Same people"],
        "One rule explains every multiple you will ever be asked about."))
    d.slide(INK, WHITE, inner=stake(
        "Multiples are not a list to memorise",
        'They follow one rule, and once you can say it you can derive '
        '<span style="color:#5EC8B4">any of them</span>.'))

    d.qa("The rule.", "rule",
         formula([("The numerator and the denominator ", INK),
                  ("must belong to the same people", TEAL)]),
         "If the value in the numerator belongs to everyone who financed the business, the "
         "flow underneath it has to belong to them too.",
         "Memorising which multiples exist instead of why they exist.", 70)

    d.qa("What enterprise value pairs with.", "Enterprise value",
         ladder([("EV / Revenue", "before everyone", TEAL),
                 ("EV / EBITDA", "before interest and tax", TEAL),
                 ("EV / EBIT", "before interest and tax", TEAL),
                 ("EV / unlevered FCF", "before lenders", TEAL)]),
         "Enterprise value is the whole business, so it pairs with anything measured before "
         "lenders are paid.",
         "Pairing enterprise value with net income, which is after interest.", 66)

    d.qa("What equity value pairs with.", "Equity value",
         ladder([("P / E", "after interest and tax", TEAL),
                 ("Price / book", "shareholders' stake", TEAL),
                 ("P / levered FCF", "after lenders", TEAL),
                 ("P / EBITDA", "mismatched", RED)]),
         "Equity value is the shareholders' slice, so it pairs with what is left after the "
         "lenders have been paid.",
         "Price over EBITDA. The price is after debt, EBITDA is before it.", 66)

    d.qa("Why EV over EBITDA is the workhorse.", "workhorse",
         ladder([("Company A, no debt", "P/E 20", MUTE),
                 ("Company B, heavy debt", "P/E 12", MUTE),
                 ("Same EV / EBITDA", "identical businesses", TEAL)]),
         "Two identical businesses financed differently show completely different P/E ratios "
         "and the same EV/EBITDA. That is the whole reason it dominates.",
         "Concluding B is cheaper when the only difference is leverage.", 62)

    d.qa("Then name what EBITDA hides.", "hides",
         ladder([("Capex", "ignored", RED), ("Working capital", "ignored", RED),
                 ("Cash taxes", "ignored", RED)]),
         "Capital-structure-neutral is not the same as complete. For a capital-intensive "
         "business, EV/EBIT is often the fairer comparison.",
         "Defending EBITDA as if it had no weaknesses at all.", 66)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("One rule", [
        ("Numerator and denominator, same claim", "the whole rule"),
        ("EV with revenue, EBITDA, EBIT, UFCF", "before lenders"),
        ("Equity with net income, EPS, LFCF", "after lenders"),
        ("EV / EBITDA ignores leverage", "why it dominates"),
        ("It also ignores capex and taxes", "say so")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Same people, top and bottom.",
        ["Enterprise value with pre-interest flows.",
         "Equity value with post-interest flows.",
         "There is no P / EBITDA, and now you know why."],
        "Tomorrow: the 15-minute networking call."))
    return d


# ====================================================== 14  networking call
@deck("w1-14-call")
def call():
    d = Deck("w1-14-call", "Recruiting Playbook", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "The 15-minute networking call.",
        ["Open", "Ask", "Close"],
        "They gave you 15 minutes. Most people waste 11 of them."))
    d.slide(INK, WHITE, inner=stake(
        "Nobody takes this call to hear your resume",
        'They took it because someone once took one for '
        '<span style="color:#5EC8B4">them</span>. Make it easy to be glad they did.'))

    d.qa("The first 60 seconds.", "60 seconds",
         ladder([("Thank them, name the referrer", "10 sec", TEAL),
                 ("Two lines on you", "30 sec", TEAL),
                 ("Why you asked for this call", "20 sec", TEAL)]),
         "Short, warm, and specific about why them. Then stop talking and let them run it.",
         "Opening with a 3-minute version of your background.", 70)

    d.qa("Ask about them, not about the industry.", "about them",
         ladder([("What is banking like?", "generic", RED),
                 ("How did you end up in this group?", "personal", TEAL),
                 ("What surprised you in year one?", "specific", TEAL)]),
         "Anything they could answer from a brochure wastes the call. Questions only they "
         "can answer are the ones that build a relationship.",
         "Asking what you could have found on the website in 30 seconds.", 66)

    d.qa("Show the reading without performing it.", "reading",
         formula([("I saw you worked on ", INK), ("[deal]", TEAL),
                  (". What was hard about it?", INK)]),
         "One specific reference proves you prepared. It also hands them something they "
         "actually enjoy talking about.",
         "Listing three of their deals, which reads as research rather than interest.", 62)

    d.qa("The close is the whole point.", "close",
         steps(["Thank them", "Ask who else", "Ask what to do next"]),
         "Two questions at minute 13. Is there anyone else in the group worth speaking to, "
         "and is there anything you should be doing now. Both are easy to say yes to.",
         "Ending with thanks and no ask, which ends the thread.", 68)

    d.qa("Then the follow-up, within 24 hours.", "24 hours",
         ladder([("Same day thank-you note", "", TEAL),
                 ("One line on something they said", "", TEAL),
                 ("Update when something changes", "", TEAL)]),
         "Reference one specific thing from the conversation so it is clearly not a template. "
         "Then update them when you have news worth sending.",
         "A generic thank-you, and then silence for 4 months.", 66)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("Fifteen minutes", [
        ("60 seconds on you, then stop", "the open"),
        ("Questions only they can answer", "not the industry"),
        ("One specific deal reference", "proves the prep"),
        ("Who else, and what next", "minute 13"),
        ("Follow up within 24 hours", "with a detail")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Minute 13 is the whole call.",
        ["Open in 60 seconds, then listen.",
         "Ask what only they can answer.",
         "Always ask who else and what next."],
        "Two of these every day."))
    return d


# ===========================================================================
if __name__ == "__main__":
    for slug in (sys.argv[1:] or list(DECKS)):
        d = DECKS[slug]()
        paths = d.render()
        problems = check(paths, 9)
        print(f"{slug}: {len(paths)} slides, "
              f"{sum(p.stat().st_size for p in paths) // 1024}KB, "
              f"problems: {problems or 'none'}")
