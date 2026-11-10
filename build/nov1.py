"""
Carousels for 10 to 16 Nov 2026: 21 decks, 3 a day (08:00, 12:30, 17:30 ET).

Pietro raised the page to 3 carousels a day on 10 Nov 2026 and approved
building and queueing without a review round. Cover grounds follow the
diagonal rotation: day 1 red / ink / paper, day 2 ink / paper / red, day 3
paper / red / ink, then repeat.

Technicals worked before writing (illustrative inputs, stated on the slide):

DEPR     +10 depreciation, 25% tax: pre-tax -10, tax -2.5, NI -7.5. CFS: NI -7.5,
         add back 10, cash +2.5. BS: cash +2.5, PP&E -10, assets -7.5;
         retained earnings -7.5. Balances.
EV       EV = equity value + debt + preferred + NCI - cash. Issuing 100 of new
         shares: equity value +100, cash +100, EV unchanged.
ACCRETE  All-stock: buyer P/E 20 and price paid at 15 times earnings. Buyer
         gives up 1/20 = 5% earnings yield per dollar of stock, gets 1/15 = 6.7%.
         EPS rises. Reverse it and EPS falls. Cash deal: compare after-tax cost
         of debt (or forgone interest after tax) with the price-paid earnings yield.
DTL      Book depreciation 10, tax depreciation 30, 25% tax: taxable income 20
         lower, cash tax 5 lower than book tax expense, DTL +5. Reverses when tax
         depreciation falls below book. Increase in DTL is added back in CFO.
CAPSTR   After-tax cost of debt below cost of equity; more debt raises the cost
         of equity and, past a point, the cost of debt (distress). WACC is U-shaped.
TV       Gordon: FCF(n+1)/(WACC - g) = FCF(n) x (1+g)/(WACC - g). Exit:
         final-year EBITDA x multiple. TV sits at the end of year n, discounted n
         periods (end-of-year convention).
BETA     Bu = BL / (1 + (1 - t) D/E). 1.2 / (1 + 0.75 x 0.5) = 1.2 / 1.375 = 0.873.
         Relever at D/E 0.3: 0.873 x 1.225 = 1.069, about 1.07.
EBITDA   Two companies with EBITDA 100, capex 10 and 60: EBITDA less capex 90 and 40.
LIFO     Units bought at 10 then 14, one sold for 20. FIFO COGS 10, gross profit 10,
         tax at 25% 2.5. LIFO COGS 14, gross profit 6, tax 1.5. Ending inventory
         FIFO 14, LIFO 10. IFRS (IAS 2) does not permit LIFO; US GAAP does.
IRR      2^(1/5) = 1.149, 14.9%. 3^(1/5) = 1.246, 24.6%. 2^(1/3) = 1.260, 26.0%.
DIV      $10 dividend: no IS effect. CFF -10. Cash -10, retained earnings -10.
         Equity value falls by the cash paid out, EV unchanged.
LEASES   IFRS 16 and ASC 842, effective for periods from 2019: right-of-use asset
         and lease liability on the balance sheet. IFRS 16: single lessee model,
         rent replaced by depreciation and interest, EBITDA rises. ASC 842:
         operating leases keep a single straight-line lease cost in operating
         expense; finance leases split into amortisation and interest.
MIDYEAR  Discount year 1 at 0.5, year 2 at 1.5. Value rises because cash arrives
         sooner. Gordon TV discounted at n - 0.5 under mid-year; exit-multiple TV
         at n, since a multiple prices the business at a point in time.
"""

import sys

from brand import BOOKMARK, Deck, INK, MUTE, PAPER, RED, TEAL, WHITE, check
from parts import bars, cover, cta, formula, ladder, recap, stake, steps

LIGHT_TEAL = "#5EC8B4"
TECH = "Technical of the Day"
REC = "Recruiting Playbook"
TAIL = "Three of these every day."


def build(slug, series, ground, title, chips, kicker, stake_head, stake_body,
          qas, recap_title, recap_items, cta_head, cta_lines):
    total = 2 + len(qas) + 2
    d = Deck(slug, series, total)

    # Cover: the ground rotates; the stake slide never matches it.
    if ground == "red":
        d.slide(RED, WHITE, accent=WHITE, inner=cover(title, chips, kicker))
        stake_bg, stake_fg, tint = INK, WHITE, LIGHT_TEAL
    elif ground == "ink":
        d.slide(INK, WHITE, accent=RED, inner=cover(title, chips, kicker))
        stake_bg, stake_fg, tint = PAPER, INK, TEAL
    else:
        d.slide(PAPER, INK, accent=RED,
                inner=cover(title, chips, kicker, chip_bg=INK, chip_fg=WHITE))
        stake_bg, stake_fg, tint = INK, WHITE, LIGHT_TEAL

    body = stake_body.replace("<t>", f'<span style="color:{tint}">').replace("</t>", "</span>")
    d.slide(stake_bg, stake_fg, inner=stake(stake_head, body))

    for q in qas:
        d.qa(*q)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap(recap_title, recap_items))

    # CTA is red unless the cover was red.
    if ground == "red":
        d.slide(INK, WHITE, accent=RED, cue="Save", icon=BOOKMARK,
                inner=cta(cta_head, cta_lines, TAIL))
    else:
        d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK,
                inner=cta(cta_head, cta_lines, TAIL))
    return d


DECKS = {}


def deck(fn):
    DECKS[fn.__name__.replace("_", "-")] = fn
    return fn


# ------------------------------------------------------------- Tue 10 Nov
@deck
def n1_01_depreciation():
    return build(
        "n1-01-depreciation", TECH, "red",
        "Depreciation goes up by $10. Walk me through it.",
        ["Income statement", "Cash flow", "Balance sheet"],
        "The classic three statement question, with a tax trap in the middle.",
        "Every number has to land",
        "They are checking one thing: does your balance sheet <t>balance</t> at the end.",
        [("Start on the income statement.", "income statement",
          ladder([("Depreciation", "+10", RED), ("Pre-tax income", "-10", INK),
                  ("Tax at 25%", "-2.5", TEAL)], "Net income", "-7.5"),
          "Pre-tax income falls by $10. At a 25% tax rate, tax falls by $2.50, so net "
          "income falls by $7.50.",
          "Dropping net income by the full $10 and forgetting tax.", 74),
         ("Then the cash flow statement.", "cash flow",
          ladder([("Net income", "-7.5", RED), ("Add back depreciation", "+10", TEAL)],
                 "Change in cash", "+2.5"),
          "Depreciation is non-cash, so it is added back. Cash ends $2.50 higher, which is "
          "exactly the tax saved.",
          "Saying cash falls. No cash left the business, and less tax was paid.", 74),
         ("Then the balance sheet.", "balance sheet",
          ladder([("Cash", "+2.5", TEAL), ("PP&amp;E", "-10", RED),
                  ("Total assets", "-7.5", INK), ("Retained earnings", "-7.5", INK)]),
          "Assets fall by $7.50. Retained earnings fall by $7.50 through net income. Both "
          "sides drop by the same amount.",
          "Leaving PP&amp;E unchanged. Accumulated depreciation is what reduces it.", 74),
         ("So where did the $2.50 come from?", "$2.50",
          formula([("$10 x 25% = ", INK), ("$2.50 tax shield", TEAL)]),
          "Depreciation is deductible. The expense is non-cash, but the tax it saves is "
          "real cash.",
          "Calling depreciation a source of cash. The deduction is the source.", 70)],
        "Depreciation +10", [
            ("Net income -7.5", "tax falls by 2.5"),
            ("Cash +2.5", "add back the non-cash 10"),
            ("PP&amp;E -10, assets -7.5", "left side"),
            ("Retained earnings -7.5", "right side, it balances")],
        "Tax first. Then cash. Then balance.",
        ["Net income moves by the after-tax amount.",
         "Add the non-cash charge back.",
         "Check both sides move together."])


@deck
def n1_02_ev_bridge():
    return build(
        "n1-02-ev-bridge", TECH, "ink",
        "Equity value to enterprise value. What do you add?",
        ["Debt", "Preferred", "Minority interest", "Less cash"],
        "Get the bridge wrong and every multiple after it is wrong too.",
        "EV is not the share price",
        "Enterprise value is what the operations are worth to <t>every</t> capital provider. "
        "Shareholders are only one of them.",
        [("Start from equity value.", "equity value",
          formula([("EV = Equity value ", INK), ("+ Debt + Preferred + NCI ", RED),
                   ("- Cash", TEAL)]),
          "Add every claim that ranks alongside or ahead of shareholders, then take out "
          "the cash a buyer gets back.",
          "Treating EV as the price of the shares.", 80),
         ("Why subtract cash?", "cash",
          ladder([("Buy all the shares", "equity value", INK),
                  ("Take on the debt", "+ debt", RED),
                  ("Keep the cash inside", "- cash", TEAL)],
                 "What the operations cost", "EV"),
          "A buyer who gets the company's cash effectively pays less for the business. "
          "The cash is not part of the operations.",
          "Saying cash is subtracted because it is unproductive. It is subtracted because "
          "the buyer gets it.", 80),
         ("Why add minority interest?", "minority interest",
          ladder([("Own 80% of a subsidiary", "consolidate 100%", INK),
                  ("EBITDA in the multiple", "100%", INK),
                  ("Add the 20% you do not own", "+ NCI", TEAL)]),
          "You consolidate all of the subsidiary's EBITDA. Add the slice you do not own so "
          "the EV matches the EBITDA it is divided by.",
          "Leaving it out, then dividing a too-small EV by full EBITDA.", 76),
         ("New shares issued. Does EV change?", "EV",
          ladder([("Cash raised", "+100", TEAL), ("Equity value", "+100", INK)],
                 "Enterprise value", "no change"),
          "Equity value rises by the cash raised, cash rises by the same amount, and the "
          "two cancel in the bridge.",
          "Saying EV rises because the share count did.", 72)],
        "The bridge", [
            ("Equity value plus debt", "and preferred"),
            ("Plus minority interest", "match consolidated EBITDA"),
            ("Minus cash", "the buyer gets it back"),
            ("Raising equity leaves EV flat", "cash and equity cancel")],
        "Match every claim to the EBITDA.",
        ["Add debt, preferred and NCI.",
         "Subtract cash.",
         "Financing moves equity value, not EV."])


@deck
def n1_03_why_ib():
    return build(
        "n1-03-why-ib", REC, "paper",
        "&ldquo;Why investment banking?&rdquo;",
        ["Specific", "Proof", "The job itself"],
        "Everyone gets asked. Most answers could be about any industry.",
        "They have heard the generic one all day",
        "The answer that lands is the one only <t>you</t> could give.",
        [("Drop the lines everyone says.", "everyone",
          ladder([("&ldquo;A steep learning curve&rdquo;", "consulting too", RED),
                  ("&ldquo;Smart, driven people&rdquo;", "law too", RED),
                  ("&ldquo;I'm passionate about finance&rdquo;", "says nothing", RED)]),
          "None of these are wrong. They are just as true of other jobs, so they do not "
          "answer why banking.",
          "Opening with prestige or pay, even dressed up.", 76),
         ("Build it in 3 beats.", "3 beats",
          steps(["A moment that pulled you in", "What you did about it",
                 "Why banking is the next step"]),
          "One specific moment, proof that you acted on it, then why the work itself fits.",
          "A story with no action. Reading about deals is not acting on it.", 80),
         ("Name the work, not the industry.", "work",
          ladder([("Building the model on a live deal", "", TEAL),
                  ("Seeing a deal from pitch to close", "", TEAL),
                  ("Learning how buyers value a company", "", TEAL)]),
          "Show that you know what an analyst does day to day, and that you want that.",
          "Talking about exit options. It tells them you plan to leave.", 74),
         ("Then say it out loud.", "out loud",
          formula([("Time it. ", INK), ("Under a minute.", TEAL)]),
          "If it runs long, cut the backstory and keep the proof.",
          "Memorising it word for word, so it sounds recited.", 80)],
        "Why banking", [
            ("Skip the generic lines", "they fit any job"),
            ("Moment, action, next step", "3 beats"),
            ("Name the analyst work", "not the brand"),
            ("Say it aloud, time it", "under a minute")],
        "Make it something only you could say.",
        ["One real moment.",
         "One thing you did about it.",
         "Why this job, not just this industry."])


# ------------------------------------------------------------- Wed 11 Nov
@deck
def n1_04_accretion():
    return build(
        "n1-04-accretion", TECH, "ink",
        "All-stock deal. Accretive or dilutive?",
        ["Buyer P/E", "Price paid", "EPS"],
        "You can answer it in one line once you see what the P/E really is.",
        "It is a pricing question",
        "The buyer pays with its own shares. The question is whether it buys "
        "<t>more earnings</t> than it gives away.",
        [("Compare the P/Es.", "P/Es",
          ladder([("Buyer trades at", "20 times", INK),
                  ("Price paid for target", "15 times", TEAL)], "EPS", "accretive"),
          "The buyer pays with shares priced at 20 times earnings and buys earnings priced "
          "at 15 times. It gets more earnings per share issued.",
          "Using the target's market P/E. Use the price actually paid, premium in.", 84),
         ("Now flip it.", "flip",
          ladder([("Buyer trades at", "15 times", INK),
                  ("Price paid for target", "20 times", RED)], "EPS", "dilutive", RED),
          "Cheap currency buying expensive earnings. Each new share brings in less profit "
          "than the existing shares earn.",
          "Forgetting that the premium raises the P/E you are paying.", 84),
         ("What about a cash deal?", "cash",
          formula([("After-tax cost of cash ", RED), ("vs ", INK),
                   ("1 / price-paid P/E", TEAL)]),
          "Compare the after-tax cost of the debt or cash used with the earnings yield of "
          "the price paid. At 20 times, the yield is 5%.",
          "Treating cash as free. It gives up interest, after tax.", 80),
         ("Is accretive the same as good?", "good",
          formula([("Accretion is arithmetic. ", INK), ("Value is judgement.", TEAL)]),
          "No. A deal can lift EPS and still destroy value if the buyer overpaid.",
          "Ending your answer at accretive.", 78)],
        "Accretion in one line", [
            ("Buyer P/E above price paid", "accretive"),
            ("Buyer P/E below price paid", "dilutive"),
            ("Cash: cost after tax vs yield", "yield is 1 over P/E"),
            ("Accretive is not value", "overpaying still hurts")],
        "Compare what you pay with what you get.",
        ["Use the P/E including the premium.",
         "Earnings yield is 1 over the P/E.",
         "Say what accretion does not tell you."])


@deck
def n1_05_dtl():
    return build(
        "n1-05-dtl", TECH, "paper",
        "Where does a deferred tax liability come from?",
        ["Book", "Tax", "Timing"],
        "Two sets of books, one timing gap, and a liability nobody borrowed.",
        "Nobody lent this money",
        "A DTL is tax the company has <t>postponed</t>, not tax it has avoided.",
        [("There are two sets of books.", "two sets",
          ladder([("Shareholder books", "GAAP or IFRS", INK),
                  ("Tax return", "tax rules", INK),
                  ("Depreciation for tax", "often faster", TEAL)]),
          "Companies report to investors under accounting rules and to the tax authority "
          "under tax rules. Both are legal.",
          "Implying the company is hiding something.", 80),
         ("Faster tax depreciation means less tax now.", "less tax now",
          ladder([("Book depreciation", "10", INK), ("Tax depreciation", "30", INK),
                  ("Taxable income lower by", "20", INK)], "DTL at 25%", "5"),
          "Cash tax is 5 below the tax expense on the income statement. That 5 is owed "
          "later, so it is a liability.",
          "Booking it as an asset. Pay less now, more later, is a liability.", 62),
         ("Then it reverses.", "reverses",
          steps(["Tax depreciation runs ahead", "It runs out first",
                 "Cash tax rises above book", "DTL unwinds to 0"]),
          "In later years tax depreciation falls below book depreciation, and the gap "
          "closes.",
          "Calling it a permanent saving.", 84),
         ("Where is it on the cash flow statement?", "cash flow",
          ladder([("Increase in DTL", "+ add back", TEAL)]),
          "Tax expense was recorded but not paid in cash, so the increase is added back in "
          "cash from operations.",
          "Leaving it out and understating operating cash flow.", 68)],
        "Deferred tax liability", [
            ("Book and tax books differ", "both legal"),
            ("Faster tax depreciation", "less cash tax now"),
            ("The gap reverses", "DTL goes back to 0"),
            ("Increase is added back", "cash from operations")],
        "Postponed, not avoided.",
        ["Tax depreciation runs ahead of book.",
         "The difference times the rate is the DTL.",
         "It reverses as the asset ages."])


@deck
def n1_06_all_debt():
    return build(
        "n1-06-all-debt", TECH, "red",
        "Debt is cheaper than equity. So why not borrow it all?",
        ["Tax shield", "Risk", "WACC"],
        "Put your answer in the comments before you swipe.",
        "Cheap until it is not",
        "Every turn of debt changes the price of <t>everything else</t> in the capital "
        "structure.",
        [("Why debt is cheaper.", "cheaper",
          ladder([("Lenders are paid first", "less risk", TEAL),
                  ("Interest is deductible", "tax shield", TEAL)]),
          "Lenders rank ahead of shareholders and interest cuts tax, so the after-tax cost "
          "of debt sits below the cost of equity.",
          "Forgetting the tax shield, the second half of the answer.", 84),
         ("More debt makes equity riskier.", "riskier",
          steps(["More fixed claims", "Equity returns swing more",
                 "Cost of equity rises"]),
          "Shareholders sit behind a bigger pile of debt, so they demand more.",
          "Holding the cost of equity flat while adding debt.", 82),
         ("Then lenders charge more.", "lenders",
          steps(["Default gets likelier", "Rates on new debt rise",
                 "Shield needs profit"]),
          "Past a point, distress risk lifts the cost of debt. The tax shield is worth "
          "nothing if there is no profit to shield.",
          "Assuming the interest rate stays the same at any leverage.", 84),
         ("So WACC is shaped like a U.", "U",
          bars([("No debt", 8, INK), ("Some debt", 6, TEAL), ("Too much", 9, RED)],
               "Illustrative shape, not data"),
          "WACC falls as cheaper debt comes in, then rises as distress costs take over. "
          "The target structure sits near the bottom.",
          "Saying more debt is always better because it is cheaper.", 80)],
        "Why not all debt", [
            ("Debt is cheaper", "seniority and tax shield"),
            ("Equity gets riskier", "cost of equity rises"),
            ("Distress costs arrive", "cost of debt rises"),
            ("WACC is a U", "aim for the bottom")],
        "Cheap debt makes everything else dearer.",
        ["Name the tax shield.",
         "Name the rising cost of equity.",
         "Name distress, then draw the U."])


# ------------------------------------------------------------- Thu 12 Nov
@deck
def n1_07_terminal():
    return build(
        "n1-07-terminal", TECH, "paper",
        "Terminal value: growth or exit multiple?",
        ["Gordon growth", "Exit multiple", "Cross-check"],
        "It is usually the biggest single number in a DCF, so it gets pushed hardest.",
        "Know both, then test one against the other",
        "The strongest answer uses each method to <t>sanity check</t> the other.",
        [("Perpetuity growth.", "growth",
          formula([("TV = ", INK), ("FCF x (1 + g) ", TEAL), ("/ (WACC - g)", INK)]),
          "Next year's cash flow over the discount rate minus growth. Keep g below "
          "long-run economic growth, or the company outgrows the economy.",
          "Using this year's FCF instead of next year's.", 90),
         ("Exit multiple.", "multiple",
          formula([("TV = ", INK), ("Final-year EBITDA ", TEAL), ("x multiple", INK)]),
          "Apply a multiple drawn from today's comps to the last forecast year.",
          "Picking a multiple with no comps behind it.", 90),
         ("Cross-check them.", "Cross-check",
          ladder([("Your growth rate", "implies a multiple", INK),
                  ("Your exit multiple", "implies a growth rate", INK),
                  ("One looks absurd?", "fix the input", RED)]),
          "Back out what each method implies about the other. If one looks wrong, the "
          "assumption behind it is.",
          "Running one method and stopping there.", 90),
         ("Then discount it.", "discount",
          formula([("TV at end of year 5 ", INK), ("/ (1 + WACC)^5", TEAL)]),
          "The terminal value sits at the end of the final forecast year, so discount it "
          "back that many years.",
          "Adding it to the present value undiscounted.", 90)],
        "Terminal value", [
            ("Gordon: next year's FCF", "over WACC minus g"),
            ("Exit: final EBITDA x multiple", "from comps"),
            ("Cross-check the two", "implied multiple, implied g"),
            ("Discount it back", "same years as the forecast")],
        "Two methods, one sanity check.",
        ["Growth below the economy's.",
         "Multiple backed by comps.",
         "Discount the TV like any cash flow."])


@deck
def n1_08_beta():
    return build(
        "n1-08-beta", TECH, "red",
        "Unlever the beta. Then relever it.",
        ["Comps", "Strip the debt", "Relever"],
        "The 4 step answer to where your cost of equity comes from.",
        "A comp's beta carries its own debt",
        "Strip out the leverage and what is left is <t>business risk</t> you can compare.",
        [("Why unlever at all?", "unlever",
          ladder([("Levered beta", "business + debt", RED),
                  ("Unlevered beta", "business only", TEAL)]),
          "Each comp has a different debt load. Unlevering puts them on the same footing.",
          "Averaging the comps' levered betas straight off a screen.", 90),
         ("Unlever each comp.", "Unlever",
          formula([("&beta;u = &beta;L / (1 + (1 - t) x D/E)", INK)]),
          "Levered beta 1.2, D/E 0.5, tax 25%: 1.2 divided by 1.375 is about 0.87.",
          "Using book D/E. Use market values.", 90),
         ("Take the median, then relever.", "relever",
          formula([("&beta;L = &beta;u x (1 + (1 - t) x D/E)", INK)]),
          "Relever at the target's own D/E. At 0.87 and a D/E of 0.3, that is about 1.07.",
          "Relevering at the comps' average structure, not the target's.", 80),
         ("Then it goes into CAPM.", "CAPM",
          formula([("Cost of equity = r", INK), ("f", INK), (" + ", INK),
                   ("&beta; x ERP", TEAL)]),
          "The relevered beta is the one that belongs in the target's cost of equity.",
          "Plugging in the unlevered beta.", 90)],
        "Beta in 4 steps", [
            ("Pull the comps' levered betas", "from the market"),
            ("Unlever each one", "market D/E, their tax rate"),
            ("Take the median", "business risk"),
            ("Relever at the target", "then CAPM")],
        "Unlever. Median. Relever.",
        ["Market value D/E, not book.",
         "The target's structure, not the comps'.",
         "Relevered beta into CAPM."])


@deck
def n1_09_your_questions():
    return build(
        "n1-09-your-questions", REC, "ink",
        "&ldquo;Do you have any questions for me?&rdquo;",
        ["Them", "The group", "The close"],
        "The last 5 minutes are still part of the interview.",
        "It is not a formality",
        "Your questions show what you <t>listened</t> to and what you care about.",
        [("Ask about their work.", "their work",
          ladder([("&ldquo;Which deal taught you the most?&rdquo;", "", TEAL),
                  ("&ldquo;How has the group's work changed?&rdquo;", "", TEAL)]),
          "Ask what only they can answer. It gets them talking about something they know.",
          "Asking what a typical day looks like. It is on every website.", 90),
         ("Ask about the group.", "group",
          ladder([("&ldquo;What separates analysts who do well here?&rdquo;", "", TEAL)]),
          "It tells you what they reward, and tells them you are thinking about doing well.",
          "Asking about pay, hours or bonus in a first round.", 90),
         ("Close the loop.", "loop",
          ladder([("&ldquo;Anything in my background I can clarify?&rdquo;", "", TEAL)]),
          "One last chance to fix a weak answer before they write their notes.",
          "Saying you think they covered everything.", 90),
         ("Two is enough.", "Two",
          formula([("Prepare 4. ", INK), ("Ask 2.", TEAL)]),
          "Drop any they already answered, and react to what they said earlier.",
          "Reading a list off your phone.", 90)],
        "Your questions", [
            ("Ask about their work", "only they can answer"),
            ("Ask what the group rewards", "not pay or hours"),
            ("Close the loop", "fix a weak answer"),
            ("Prepare 4, ask 2", "skip the answered ones")],
        "End on a question only they can answer.",
        ["One about their work.",
         "One about the group.",
         "Then offer to clarify."])


# ------------------------------------------------------------- Fri 13 Nov
@deck
def n1_10_ebitda():
    return build(
        "n1-10-ebitda", TECH, "red",
        "Why does everyone use EBITDA?",
        ["Capital structure", "Non-cash", "Blind spots"],
        "Know why it is useful, and the one thing it cannot see.",
        "Useful, not cash",
        "EBITDA is a <t>comparison</t> tool. It is not the cash a business generates.",
        [("It ignores how the company is financed.", "financed",
          ladder([("Before interest", "debt-neutral", TEAL),
                  ("Pairs with", "enterprise value", TEAL)]),
          "Two companies with different debt loads can be compared, which is why it sits "
          "under EV.",
          "Pairing EBITDA with equity value.", 74),
         ("It strips out non-cash charges.", "non-cash",
          ladder([("Depreciation", "past purchases", INK),
                  ("Amortisation", "accounting choices", INK)]),
          "D&amp;A depends on what was bought years ago and how it is written off. EBITDA "
          "gets closer to operating profit before those choices.",
          "Saying D&amp;A does not matter. The assets still need replacing.", 74),
         ("Its blind spot is capex.", "capex",
          ladder([("Company A: EBITDA 100, capex 10", "90", TEAL),
                  ("Company B: EBITDA 100, capex 60", "40", RED)]),
          "Same EBITDA, very different cash once the business reinvests to keep running.",
          "Calling EBITDA cash flow.", 80),
         ("It also misses working capital and tax.", "working capital",
          steps(["Sales grow", "Receivables build", "EBITDA up, cash down"]),
          "A growing business can show rising EBITDA while cash gets tied up in "
          "receivables and inventory.",
          "Valuing a capital-heavy business on EBITDA alone.", 70)],
        "EBITDA", [
            ("Before interest", "pairs with EV"),
            ("Before D&amp;A", "removes accounting choices"),
            ("Blind to capex", "same EBITDA, different cash"),
            ("Blind to NWC and tax", "growth can eat cash")],
        "A comparison tool, not cash.",
        ["Say why it pairs with EV.",
         "Say what it removes.",
         "Name capex as the blind spot."])


@deck
def n1_11_lifo_fifo():
    return build(
        "n1-11-lifo-fifo", TECH, "ink",
        "Prices are rising. LIFO or FIFO?",
        ["COGS", "Profit", "Tax"],
        "Same unit sold, two different profits. Here is the arithmetic.",
        "The order you expense inventory matters",
        "When costs rise, the method you pick changes profit, tax and "
        "<t>the balance sheet</t>.",
        [("Same unit, two costs.", "two costs",
          ladder([("Bought first", "10", INK), ("Bought second", "14", INK),
                  ("Sold one for", "20", INK)]),
          "FIFO expenses the oldest cost, 10. LIFO expenses the newest, 14.",
          "Assuming the method changes the physical goods sold. It changes the cost.", 90),
         ("LIFO: lower profit, lower tax.", "lower tax",
          ladder([("FIFO gross profit", "10", INK), ("LIFO gross profit", "6", INK),
                  ("Tax at 25%: FIFO vs LIFO", "2.5 vs 1.5", TEAL)]),
          "Higher cost of goods means lower profit and less tax, so LIFO keeps more cash "
          "when prices rise.",
          "Saying LIFO makes the company less valuable. It saves cash tax.", 84),
         ("FIFO: a truer balance sheet.", "truer",
          ladder([("FIFO ending inventory", "14", TEAL),
                  ("LIFO ending inventory", "10", RED)]),
          "FIFO leaves the newer, higher cost on the balance sheet, closer to what it "
          "would cost to replace.",
          "Forgetting the balance sheet side of the answer.", 84),
         ("IFRS does not allow LIFO.", "IFRS",
          ladder([("US GAAP", "LIFO allowed", INK), ("IFRS", "LIFO not allowed", RED)]),
          "Comparing a US company on LIFO with a peer reporting under IFRS means adjusting "
          "first.",
          "Comparing margins across them as if they were like for like.", 84)],
        "LIFO vs FIFO, prices rising", [
            ("LIFO: newest cost in COGS", "lower profit, lower tax"),
            ("FIFO: oldest cost in COGS", "higher profit"),
            ("FIFO inventory is closer to today", "balance sheet"),
            ("No LIFO under IFRS", "adjust before comparing")],
        "LIFO saves tax. FIFO shows the balance sheet.",
        ["Work the numbers out loud.",
         "Cover profit, tax and inventory.",
         "Mention IFRS."])


@deck
def n1_12_why_us():
    return build(
        "n1-12-why-us", REC, "paper",
        "&ldquo;Why our bank?&rdquo;",
        ["The group", "The people", "One deal"],
        "Swap the bank's name and if your answer still works, it is not an answer.",
        "The swap test",
        "A good answer breaks if you put a <t>different bank's</t> name in it.",
        [("Name the group, not the brand.", "group",
          ladder([("&ldquo;A leading global franchise&rdquo;", "fits anyone", RED),
                  ("The group and what it covers", "fits only them", TEAL)]),
          "Talk about the team you would join and the work it does.",
          "Quoting rankings or reputation. Every bank on your list has a version of that.",
          84),
         ("Use a real conversation.", "real conversation",
          steps(["Who you spoke to", "What they told you", "Why it stuck"]),
          "One person and one thing they said is worth more than a paragraph of research.",
          "Name-dropping someone you barely spoke to. They may check.", 84),
         ("Mention one deal, carefully.", "one deal",
          formula([("One deal. ", INK), ("One reason it interested you.", TEAL)]),
          "Show you understand why it mattered, not just that it happened.",
          "Reciting a list of deals off their website.", 84),
         ("Make it fit you.", "you",
          formula([("Their way of working ", INK), ("+ what you've done", TEAL)]),
          "End on why your background fits how this team works.",
          "Ending on what the bank can do for your career.", 90)],
        "Why us", [
            ("Pass the swap test", "it only fits them"),
            ("Name the group", "not the brand"),
            ("One person, one deal", "specific, not a list"),
            ("Tie it back to you", "fit, not flattery")],
        "If it fits any bank, rewrite it.",
        ["The group you would join.",
         "One real conversation.",
         "Why it fits what you have done."])


# ------------------------------------------------------------- Sat 14 Nov
@deck
def n1_13_irr():
    return build(
        "n1-13-irr", TECH, "ink",
        "2 times your money in 5 years. What is the IRR?",
        ["MOIC", "IRR", "Time"],
        "The shortcuts every LBO question expects you to know cold.",
        "Same multiple, different return",
        "The multiple tells you how much. The IRR tells you <t>how fast</t>.",
        [("MOIC is a ratio.", "ratio",
          formula([("MOIC = ", INK), ("Exit equity ", TEAL), ("/ Entry equity", INK)]),
          "Put in 100, take out 200, and the MOIC is 2 times. It ignores how long it took.",
          "Treating MOIC as an annual return.", 90),
         ("IRR adds time.", "time",
          ladder([("2 times in 3 years", "about 26%", TEAL),
                  ("2 times in 5 years", "about 15%", INK)]),
          "The same multiple earned more slowly is a lower annual return.",
          "Dividing the gain by the years. 100% over 5 years is not 20% a year.", 90),
         ("The ones to memorise.", "memorise",
          ladder([("2 times in 5 years", "about 15%", INK),
                  ("3 times in 5 years", "about 25%", INK),
                  ("2 times in 3 years", "about 26%", INK)]),
          "IRR is the multiple to the power of 1 over the years, minus 1. 2 to the 1/5 is "
          "about 1.149.",
          "Freezing on the maths. Know these three and estimate from them.", 90),
         ("Why funds report both.", "both",
          steps(["IRR rewards speed", "MOIC rewards size", "A quick flip can mislead"]),
          "A fast exit can post a high IRR on a small gain, so investors look at both.",
          "Quoting one number on its own.", 90)],
        "MOIC and IRR", [
            ("MOIC: exit over entry", "how much"),
            ("IRR: per year", "how fast"),
            ("2 times, 5 years", "about 15%"),
            ("3 times, 5 years", "about 25%")],
        "Say the multiple, then the speed.",
        ["MOIC ignores time.",
         "IRR is the multiple's root, minus 1.",
         "Know 15% and 25% cold."])


@deck
def n1_14_dividend():
    return build(
        "n1-14-dividend", TECH, "paper",
        "A company pays a $10 dividend. Walk it through.",
        ["Income statement", "Cash flow", "Balance sheet"],
        "The trick is the statement where nothing happens.",
        "Start with what does not move",
        "A dividend is a distribution of profit, not an <t>expense</t>.",
        [("The income statement.", "income statement",
          ladder([("Revenue, costs, tax", "no change", INK)], "Net income", "no change"),
          "Dividends are paid out of profit after it is earned, so they never touch the "
          "income statement.",
          "Deducting the dividend from net income.", 90),
         ("The cash flow statement.", "cash flow",
          ladder([("Cash from financing", "-10", RED)], "Change in cash", "-10", RED),
          "It sits in financing, next to debt repaid and shares bought back.",
          "Putting it in operating cash flow under US GAAP.", 90),
         ("The balance sheet.", "balance sheet",
          ladder([("Cash", "-10", RED), ("Retained earnings", "-10", RED)]),
          "Cash falls by $10 and retained earnings fall by $10. Both sides drop together.",
          "Reducing a liability instead of equity.", 90),
         ("And enterprise value?", "enterprise value",
          ladder([("Equity value", "-10", INK), ("Cash", "-10", INK)],
                 "Enterprise value", "no change"),
          "Shareholders take $10 out, so equity value falls by about that, and so does "
          "cash. The operations are untouched.",
          "Saying EV falls because the company has less cash.", 90)],
        "A $10 dividend", [
            ("Income statement", "nothing"),
            ("Cash flow: financing", "-10"),
            ("Cash and retained earnings", "both -10"),
            ("Enterprise value", "unchanged")],
        "Not an expense. A distribution.",
        ["Skip the income statement.",
         "Financing outflow of 10.",
         "Cash and equity fall together."])


@deck
def n1_15_revenue_worth():
    return build(
        "n1-15-revenue-worth", TECH, "red",
        "100 of revenue at a software company or a grocer. Which is worth more?",
        ["Margins", "Growth", "Recurring"],
        "Pick one in the comments, then swipe for the reasoning.",
        "Revenue is not value",
        "A buyer pays for the <t>cash</t> the revenue turns into, and for how long it lasts.",
        [("Revenue is not profit.", "profit",
          ladder([("Grocer", "thin margins", RED), ("Software", "high margins", TEAL)]),
          "The same 100 of sales turns into very different profit depending on the "
          "business.",
          "Comparing companies on revenue alone.", 90),
         ("Growth changes the multiple.", "Growth",
          steps(["Faster growth", "More future cash", "Higher multiple today"]),
          "A buyer pays now for cash that arrives later, so faster growth earns a higher "
          "multiple.",
          "Forgetting that growth has to be paid for with reinvestment.", 84),
         ("Recurring beats one-off.", "Recurring",
          ladder([("Subscription renewals", "predictable", TEAL),
                  ("One-off sales", "earned again each year", INK)]),
          "Revenue that renews is easier to forecast, and that lowers the risk a buyer "
          "prices in.",
          "Treating all revenue as the same quality.", 84),
         ("So the answer is: it depends. Then say on what.", "it depends",
          formula([("Margin ", TEAL), ("x growth ", TEAL), ("x durability", TEAL)]),
          "Usually the software company, because of margins, growth and recurring revenue. "
          "A slow, unprofitable one can be worth less.",
          "Saying 'it depends' and stopping.", 64)],
        "Which 100 is worth more", [
            ("Margins", "how much becomes profit"),
            ("Growth", "how much more is coming"),
            ("Recurring revenue", "how sure you can be"),
            ("It depends, then explain", "name all three")],
        "Value the cash, not the sales.",
        ["Margin first.",
         "Then growth.",
         "Then how durable it is."])


# ------------------------------------------------------------- Sun 15 Nov
@deck
def n1_16_leases():
    return build(
        "n1-16-leases", TECH, "paper",
        "How do leases change EBITDA?",
        ["IFRS 16", "ASC 842", "EV"],
        "The answer depends on where the company reports.",
        "Same lease, two answers",
        "Both standards put leases on the balance sheet. Only one <t>moves EBITDA</t>.",
        [("Leases are on the balance sheet.", "balance sheet",
          ladder([("Right-of-use asset", "asset", INK), ("Lease liability", "liability", INK)]),
          "Since 2019 for listed companies, IFRS 16 and US GAAP's ASC 842 both record most leases as an asset "
          "and a matching liability.",
          "Saying operating leases are still off balance sheet.", 80),
         ("Under IFRS 16, EBITDA rises.", "rises",
          steps(["Rent leaves opex", "Depreciation below EBITDA", "Interest below EBITDA"]),
          "The lease cost is split into depreciation and interest, both below EBITDA.",
          "Assuming the company got more profitable. Only the line moved.", 80),
         ("Under US GAAP, operating leases do not move it.", "do not",
          ladder([("Operating lease", "one cost in opex", INK),
                  ("Finance lease", "split, like IFRS", INK)]),
          "An operating lease keeps a single straight-line cost in operating expenses.",
          "Treating US and IFRS EBITDA as comparable without checking.", 70),
         ("So match EV and EBITDA.", "match",
          formula([("EBITDA before lease cost ", INK), ("needs EV with lease debt", TEAL)]),
          "If lease costs sit below EBITDA, the lease liability belongs in EV. Keep every "
          "comp consistent.",
          "Mixing IFRS and US comps in one multiple without adjusting.", 84)],
        "Leases", [
            ("Both standards: on balance sheet", "since 2019"),
            ("IFRS 16", "EBITDA goes up"),
            ("ASC 842 operating", "EBITDA unchanged"),
            ("Match the numerator", "lease debt in EV if needed")],
        "Check where it reports before you compare.",
        ["Asset and liability under both.",
         "IFRS moves EBITDA up.",
         "Keep EV and EBITDA consistent."])


@deck
def n1_17_synergies():
    return build(
        "n1-17-synergies", TECH, "red",
        "Cost synergies or revenue synergies?",
        ["Cut", "Sell", "Credibility"],
        "Why buyers trust one kind far more than the other.",
        "Synergies justify the premium",
        "Which kind you count decides how much a buyer can <t>defend</t> paying.",
        [("Cost synergies: what you can cut.", "cut",
          ladder([("Duplicate head office", "", TEAL), ("Overlapping systems", "", TEAL),
                  ("Combined purchasing", "", TEAL)]),
          "These sit inside management's control once the deal closes.",
          "Listing cuts the combined company cannot actually make.", 80),
         ("Revenue synergies: what you hope to sell.", "hope",
          ladder([("Cross-selling to new customers", "", INK),
                  ("New markets", "", INK)]),
          "These depend on customers doing something they have not done yet.",
          "Treating them as as certain as cost cuts.", 74),
         ("Why buyers trust costs more.", "costs",
          formula([("In your control ", TEAL), ("vs ", INK), ("in the customer's", RED)]),
          "Cost synergies are easier to plan, measure and deliver, so lenders and boards "
          "weight them more.",
          "Pricing a deal on revenue synergies alone.", 84),
         ("They cost money first.", "cost money",
          steps(["Integration costs", "Phase in over years", "Then the run-rate"]),
          "Synergies take time to arrive and cost money to achieve.",
          "Counting the full run-rate from day 1.", 90)],
        "Synergies", [
            ("Cost synergies", "in management's control"),
            ("Revenue synergies", "depend on customers"),
            ("Boards weight costs more", "easier to deliver"),
            ("Phase them in", "integration costs first")],
        "Count what you control.",
        ["Name a cost synergy.",
         "Discount revenue synergies.",
         "Phase in, net of costs."])


@deck
def n1_18_failure():
    return build(
        "n1-18-failure", REC, "ink",
        "&ldquo;Tell me about a time you failed.&rdquo;",
        ["Real", "Owned", "Changed"],
        "They are not testing the failure. They are testing what you did next.",
        "A fake failure is the real failure",
        "&ldquo;I worked too hard&rdquo; tells them you will not <t>own</t> a mistake on a "
        "deal.",
        [("Pick a real one.", "real",
          ladder([("Something that mattered", "", TEAL), ("Your fault, at least partly", "", TEAL),
                  ("Not a disaster", "", TEAL)]),
          "A real setback with real stakes, small enough that it did not end anything.",
          "A strength in disguise. They hear that answer all day.", 90),
         ("Own your part.", "Own",
          formula([("&ldquo;I&rdquo; ", TEAL), ("not &ldquo;we&rdquo;", RED)]),
          "Say what you did wrong in one plain sentence. No blaming the team.",
          "Spending half the answer on context.", 90),
         ("Then what you did.", "did",
          steps(["What went wrong", "What you did about it", "What changed after"]),
          "Most of the answer goes here: the fix, and the habit you kept.",
          "Ending on the failure itself.", 90),
         ("Show it stuck.", "stuck",
          formula([("A later moment ", INK), ("where you did it right.", TEAL)]),
          "One example of the lesson working later proves you learned it.",
          "Saying you learned a lot, with nothing to show it.", 90)],
        "The failure answer", [
            ("Real, not a disguised strength", "with stakes"),
            ("Own it in 1 sentence", "I, not we"),
            ("Most time on the fix", "what you did"),
            ("Show it stuck", "a later example")],
        "Own it. Fix it. Prove it stuck.",
        ["A real failure.",
         "Your part, said plainly.",
         "The habit it gave you."])


# ------------------------------------------------------------- Mon 16 Nov
@deck
def n1_19_circular():
    return build(
        "n1-19-circular", TECH, "red",
        "Why does an LBO model have a circular reference?",
        ["Interest", "Cash", "Debt"],
        "Every modelling test gets here eventually.",
        "The model chases its own tail",
        "Interest depends on debt, and debt depends on the cash left <t>after</t> interest.",
        [("Follow the loop.", "loop",
          steps(["Interest", "Net income", "Cash to repay", "Debt balance", "Interest"]),
          "Interest on average debt needs this year's ending balance, which needs the cash "
          "left after this year's interest.",
          "Saying it is a modelling error. It is the logic of the business.", 90),
         ("Fix 1: iterate.", "iterate",
          formula([("Turn on ", INK), ("iterative calculation", TEAL)]),
          "Let the spreadsheet loop until the numbers settle.",
          "Iterating without a switch to break the loop when it errors.", 90),
         ("Fix 2: a circuit breaker.", "circuit breaker",
          ladder([("Switch on", "average balance", INK), ("Switch off", "interest = 0", INK)]),
          "A toggle that cuts the loop, so one error cannot spread through the model.",
          "Having no way to reset the model when it blows up.", 84),
         ("Fix 3: use the opening balance.", "opening balance",
          formula([("Interest = ", INK), ("opening debt ", TEAL), ("x rate", INK)]),
          "No loop at all. Slightly less precise when debt is paid down fast.",
          "Not saying what you give up by doing it.", 80)],
        "The circular reference", [
            ("Interest, cash, debt, interest", "the loop"),
            ("Iterate", "let it settle"),
            ("Circuit breaker", "a toggle to cut it"),
            ("Opening balance", "no loop, less precise")],
        "Explain the loop. Then break it.",
        ["Name the loop.",
         "Give a fix.",
         "Say what the fix costs."])


@deck
def n1_20_sbc():
    return build(
        "n1-20-sbc", TECH, "ink",
        "Is stock-based compensation a real expense?",
        ["Non-cash", "Dilution", "Valuation"],
        "It gets added back. That does not make it free.",
        "Paid in shares is still paid",
        "Employees get shares instead of cash, and <t>existing shareholders</t> pay for it.",
        [("Why it is added back.", "added back",
          ladder([("Expensed on the income statement", "yes", INK),
                  ("Cash paid out", "no", INK)], "Cash flow statement", "add back"),
          "No cash leaves the business, so it is added back in cash from operations.",
          "Stopping there and calling it a free expense.", 90),
         ("The cost is dilution.", "dilution",
          steps(["Shares issued to staff", "Share count rises", "Each share owns less"]),
          "Shareholders pay with a smaller slice of the company instead of with cash.",
          "Forgetting it shows up in the diluted share count.", 90),
         ("Do not count it twice.", "twice",
          ladder([("Treat SBC as a cash cost", "lower FCF", INK),
                  ("Or count future dilution", "higher share count", INK)]),
          "Pick one: treat it as a cost in cash flow, or capture it in the share count.",
          "Adding it back and also ignoring future dilution.", 90),
         ("So what do you say?", "say",
          formula([("Non-cash, ", INK), ("but a real cost.", TEAL)]),
          "It is non-cash for the cash flow statement and a real cost for shareholders.",
          "Picking one side of that sentence.", 90)],
        "Stock-based compensation", [
            ("Added back on cash flow", "non-cash"),
            ("Paid for through dilution", "share count rises"),
            ("Count it once", "cost or dilution"),
            ("Non-cash, but real", "the one-line answer")],
        "Non-cash is not free.",
        ["Add it back on cash flow.",
         "Then name the dilution.",
         "Count it once in valuation."])


@deck
def n1_21_mid_year():
    return build(
        "n1-21-mid-year", TECH, "paper",
        "What is the mid-year convention?",
        ["Timing", "Discount", "Terminal value"],
        "A small switch in the DCF with a question hiding behind it.",
        "Cash does not arrive on 31 December",
        "It comes in <t>through the year</t>, so discounting a full year is too harsh.",
        [("Discount half a year earlier.", "half a year",
          ladder([("Year 1", "0.5", TEAL), ("Year 2", "1.5", TEAL), ("Year 3", "2.5", TEAL)]),
          "Each year's cash flow is treated as arriving in the middle of that year.",
          "Using 0.5 for year 1 and then 2 for year 2.", 84),
         ("Value goes up.", "up",
          formula([("Earlier cash ", INK), ("= higher present value", TEAL)]),
          "Every period is discounted half a year less, so the DCF value rises.",
          "Saying it lowers value.", 90),
         ("Perpetuity growth TV moves too.", "moves",
          formula([("Discount at ", INK), ("n - 0.5", TEAL)]),
          "The Gordon growth value extends the same mid-year cash flows, so it shifts "
          "with them.",
          "Applying mid-year to the forecast and not to the growth TV.", 80),
         ("Exit multiple TV does not.", "does not",
          formula([("Discount at ", INK), ("n", TEAL)]),
          "A multiple prices the business at a point in time, the end of the forecast, so "
          "it stays at year n.",
          "Moving the exit value to n - 0.5 as well.", 90)],
        "Mid-year convention", [
            ("Cash arrives mid-year", "0.5, 1.5, 2.5"),
            ("Value rises", "less discounting"),
            ("Gordon TV", "n - 0.5"),
            ("Exit multiple TV", "stays at n")],
        "Half a year earlier. Except the exit.",
        ["0.5, 1.5, 2.5.",
         "Value goes up.",
         "Exit multiple TV stays at n."])


# ===========================================================================
if __name__ == "__main__":
    for slug in (sys.argv[1:] or list(DECKS)):
        d = DECKS[slug]()
        paths = d.render()
        problems = check(paths, d.total)
        print(f"{slug}: {len(paths)} slides, "
              f"{sum(p.stat().st_size for p in paths) // 1024}KB, problems: {problems or 'none'}")
