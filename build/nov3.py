"""
Carousels for 26 to 29 Nov 2026: 12 decks, 3 a day (08:00, 12:30, 17:30 ET).

Written 19 Nov 2026 in a second session that answered Pietro's "Make sure this carousel is published each day" in
parallel with the one that queued build/nov2.py. These are the decks from that session that do not repeat a nov2
topic, queued after nov2 so the queue runs to 29 Nov. Cover grounds by calendar day from 10 Nov (day 1): 26 Nov is
day 2 (ink / paper / red). The worked technicals are below.

Technicals worked before writing (illustrative inputs, stated on the slide;
25% tax throughout unless the slide says pre-tax):

WRITEDOWN Inventory -10, deductible: pre-tax -10, tax -2.5, NI -7.5. CFS: NI -7.5,
          add back 10, cash +2.5. BS: inventory -10, cash +2.5, assets -7.5,
          RE -7.5. Not deductible yet: cash tax unchanged, DTA +2.5. CFS:
          -7.5 + 10 - 2.5 = 0. BS: inventory -10, DTA +2.5, assets -7.5, RE -7.5.
TSM       10 options, strike $5, price $20. Proceeds 50, buy back 50 / 20 = 2.5,
          net new shares 7.5. Strike above price: excluded.
PPE SALE  Book value 50, sold for 60 cash. Gain 10, tax 2.5 (paid now), NI +7.5.
          CFO: 7.5 - 10 = -2.5. CFI +60. Cash +57.5. BS: cash +57.5, PP&E -50,
          assets +7.5, RE +7.5.
BANKS     Debt is the raw material (deposits, borrowing), interest is an operating
          cost, so EV and EBITDA do not fit. P/E and P/B (P/TBV). Justified
          P/B = (ROE - g) / (cost of equity - g): above 1 when ROE beats the cost
          of equity. DCF form: dividend discount model.
DEFREV    $100 cash up front for service next year. Day 1: no IS, CFO +100 via
          deferred revenue, cash +100, deferred revenue +100. On delivery (costs
          ignored, tax paid then): revenue 100, tax 25, NI 75. CFO: 75 - 100 = -25.
          BS: cash -25, deferred revenue -100, RE +75. -25 = -100 + 75.
S&U       Uses: equity purchase 400 + refinance debt 100 + fees 20 = 520.
          Sources: new debt 300 + sponsor equity 220 = 520.
CAPEX     $100 spend, 5-year life, pre-tax. Expense: EBITDA -100, CFO -100, cash
          -100. Capitalise: EBITDA 0, depreciation 20, EBIT -20, CFO -20 + 20 = 0,
          CFI -100, cash -100. FCF = CFO - capex: -100 either way.
CONVERT   $100 bond converts into 5 shares (conversion price $20). Share $25: in the
          money, if-converted: +5 shares, bond out of debt, after-tax interest
          added back to EPS numerator. Share $15: stays debt, no shares.
EQUITY    Usual presumptions (ASC 323, IAS 28): under 20% investment at fair value,
          20 to 50% significant influence, equity method, over 50% control,
          consolidate with NCI. 30% of a company earning 10: income +3, CFS -3
          (non-cash, no dividend), investment +3. EV bridge: subtract equity
          investments, add NCI.
ASSET     Asset deal: buyer picks assets and liabilities, tax basis stepped up to
          the price paid, more tax depreciation. Stock deal: buyer takes the whole
          entity, tax basis carries over. US C-corp seller in an asset deal can be
          taxed twice (corporate gain, then on distribution).
EARNOUT   Part of the price paid later if targets are met. Contingent consideration
          at fair value at closing (ASC 805, IFRS 3), remeasured through profit or
          loss when classified as a liability.
"""

import sys

from brand import check
from brand import INK, RED, TEAL
from nov1 import REC, TECH, build
from parts import formula, ladder, steps

DECKS = {}


def deck(fn):
    DECKS[fn.__name__.replace("_", "-")] = fn
    return fn


# ------------------------------------------------------------- Thu 26 Nov (ink / paper / red)
@deck
def n3_01_writedown():
    return build(
        "n3-01-writedown", TECH, "ink",
        "Inventory is written down by $10. Walk me through it.",
        ["Income statement", "Cash flow", "Balance sheet"],
        "It walks like depreciation, until they ask about tax.",
        "Another non-cash charge",
        "No cash leaves the business. The only cash effect is the <t>tax</t>.",
        [("Start on the income statement.", "income statement",
          ladder([("Write-down", "+10", RED), ("Pre-tax income", "-10", INK),
                  ("Tax at 25%", "-2.5", TEAL)], "Net income", "-7.5"),
          "Assume the write-down is tax deductible. Pre-tax income falls by $10, tax by "
          "$2.50, net income by $7.50.",
          "Cutting net income by the full $10.", 74),
         ("Then the cash flow statement.", "cash flow",
          ladder([("Net income", "-7.5", RED), ("Add back the write-down", "+10", TEAL)],
                 "Change in cash", "+2.5"),
          "The write-down is non-cash, so it goes back in. Cash is up $2.50, the tax saved.",
          "Treating it as a cash outflow because inventory fell.", 74),
         ("Then the balance sheet.", "balance sheet",
          ladder([("Cash", "+2.5", TEAL), ("Inventory", "-10", RED),
                  ("Total assets", "-7.5", INK), ("Retained earnings", "-7.5", INK)]),
          "Assets fall by $7.50 and retained earnings fall by $7.50. It balances.",
          "Forgetting to reduce the inventory line itself.", 74),
         ("What if tax only allows it later?", "later",
          ladder([("Cash tax paid", "no change", INK),
                  ("Deferred tax asset", "+2.5", TEAL),
                  ("Change in cash", "0", INK)]),
          "Book tax still falls by $2.50, but no cash is saved yet. The difference sits "
          "in a deferred tax asset.",
          "Keeping the +2.5 of cash when no tax was actually saved.", 70)],
        "Write-down -10", [
            ("Net income -7.5", "if deductible"),
            ("Cash +2.5", "the tax saved"),
            ("Inventory -10, assets -7.5", "left side"),
            ("Not deductible yet", "DTA +2.5, cash 0")],
        "Non-cash charge, real tax.",
        ["Net income moves after tax.",
         "Add the charge back.",
         "Ask when tax gets the deduction."])


@deck
def n3_02_asset_sale():
    return build(
        "n3-02-asset-sale", TECH, "paper",
        "You sell equipment for more than book value. Walk me through it.",
        ["Gain on sale", "Cash flow", "Balance sheet"],
        "The trap is counting the cash twice.",
        "Book value 50, sold for 60",
        "The gain is profit, but the cash comes in as <t>investing</t> cash flow.",
        [("Start with the gain.", "gain",
          ladder([("Gain on sale", "+10", TEAL), ("Tax at 25%", "-2.5", RED)],
                 "Net income", "+7.5"),
          "Sale price 60 less book value 50 is a $10 gain. After tax, net income rises "
          "$7.50.",
          "Booking the whole $60 as income.", 80),
         ("Take the gain out of operations.", "operations",
          ladder([("Net income", "+7.5", INK), ("Less gain on sale", "-10", RED)],
                 "Cash from operations", "-2.5", RED),
          "The gain is not operating cash, so it is subtracted. What is left is the tax "
          "paid on it.",
          "Leaving the gain in operating cash flow.", 74),
         ("Put the proceeds in investing.", "investing",
          ladder([("Cash from operations", "-2.5", INK), ("Proceeds from sale", "+60", TEAL)],
                 "Change in cash", "+57.5"),
          "The full $60 lands in investing. Net of the tax, cash rises $57.50.",
          "Counting the $10 in operations and the $60 in investing.", 76),
         ("Then the balance sheet.", "balance sheet",
          ladder([("Cash", "+57.5", TEAL), ("PP&amp;E", "-50", RED),
                  ("Total assets", "+7.5", INK), ("Retained earnings", "+7.5", INK)]),
          "Assets rise $7.50 and retained earnings rise $7.50. It balances.",
          "Removing $60 of PP&amp;E instead of its $50 book value.", 74)],
        "Sale above book", [
            ("Gain +10, net income +7.5", "after tax"),
            ("Operations -2.5", "gain taken out"),
            ("Investing +60", "the proceeds"),
            ("Cash +57.5, PP&amp;E -50", "it balances")],
        "Gain out of operations. Cash into investing.",
        ["The gain is not operating cash.",
         "The proceeds go to investing.",
         "Remove book value, not price."])


@deck
def n3_03_teamwork():
    return build(
        "n3-03-teamwork", REC, "red",
        "&ldquo;Tell me about a time you worked in a team.&rdquo;",
        ["Your part", "Friction", "Result"],
        "Deal teams are small. They want to know what you are like in one.",
        "&ldquo;We&rdquo; hides you",
        "They are hiring you, not the group. Say what <t>you</t> did.",
        [("Pick a team with stakes.", "stakes",
          ladder([("A class project with no deadline", "low stakes", RED),
                  ("A deadline that could be missed", "real pressure", TEAL)]),
          "Choose a story where something could have gone wrong.",
          "A story where everything went smoothly.", 80),
         ("Say what your part was.", "your part",
          steps(["The goal", "Your role", "What you did, in the first person"]),
          "Use &ldquo;I&rdquo; for your actions and &ldquo;we&rdquo; only for the outcome.",
          "Saying &ldquo;we&rdquo; the whole way through.", 80),
         ("Include the friction.", "friction",
          ladder([("A missed handoff", "", INK), ("A disagreement on approach", "", INK),
                  ("Someone falling behind", "", INK)]),
          "Show how you handled it without making anyone the villain.",
          "Blaming a teammate.", 84),
         ("Finish on the result.", "result",
          formula([("What happened, ", INK), ("and what you'd repeat.", TEAL)]),
          "Give the outcome and 1 thing you learned about working with others.",
          "Ending on the problem instead of the result.", 84)],
        "Teamwork", [
            ("Real stakes", "something could go wrong"),
            ("Your part", "in the first person"),
            ("The friction", "no villains"),
            ("The result", "and what you'd repeat")],
        "Your part, under pressure.",
        ["Pick a story with stakes.",
         "Say I, not we.",
         "Handle the friction fairly."])


# ------------------------------------------------------------- Fri 27 Nov (paper / red / ink)
@deck
def n3_04_capitalise():
    return build(
        "n3-04-capitalise", TECH, "paper",
        "Capitalise or expense $100. What changes?",
        ["EBITDA", "Cash flow", "Free cash flow"],
        "Same cash out of the door. Very different-looking numbers.",
        "Same spend, two treatments",
        "Pre-tax, year 1, a 5-year life. The cash is the same. <t>Where it shows</t> is not.",
        [("Expense it.", "Expense",
          ladder([("EBITDA", "-100", RED), ("Cash from operations", "-100", RED),
                  ("Cash from investing", "0", INK)]),
          "The whole $100 hits operating profit and operating cash flow this year.",
          "Thinking expensing is the cheaper option in cash.", 84),
         ("Capitalise it.", "Capitalise",
          ladder([("EBITDA", "0", TEAL), ("Depreciation", "-20", INK),
                  ("Cash from operations", "-20 + 20 = 0", TEAL),
                  ("Cash from investing", "-100", RED)]),
          "It becomes an asset, depreciated $20 a year. EBITDA and operating cash flow "
          "do not see it.",
          "Forgetting the capex in investing.", 84),
         ("So which looks better?", "better",
          formula([("Capitalised: ", INK), ("higher EBITDA and CFO", TEAL)]),
          "Capitalising flatters EBITDA and operating cash flow. That is why it gets "
          "scrutinised.",
          "Calling it free money. Total cash out is the same.", 84),
         ("What doesn't change?", "change",
          formula([("FCF = CFO - capex = ", INK), ("-100 both ways", TEAL)]),
          "Free cash flow nets the capex back out, so it is the same either way.",
          "Comparing EBITDA across companies with different policies.", 80)],
        "Capitalise vs expense", [
            ("Expense", "EBITDA -100, CFO -100"),
            ("Capitalise", "EBITDA 0, investing -100"),
            ("Capitalising flatters", "EBITDA and CFO"),
            ("Free cash flow", "-100 either way")],
        "Look at free cash flow.",
        ["Expensing hits EBITDA.",
         "Capitalising moves it to investing.",
         "FCF does not care."])


@deck
def n3_05_convertible():
    return build(
        "n3-05-convertible", TECH, "red",
        "How do you treat a convertible bond?",
        ["Debt", "Shares", "Diluted EPS"],
        "It is debt or it is shares. Never both.",
        "It depends on the share price",
        "A $100 bond that converts into 5 shares is worth converting only above "
        "<t>$20</t> a share.",
        [("Find the conversion price.", "conversion price",
          formula([("$100 / 5 shares = ", INK), ("$20", TEAL)]),
          "Face value divided by the shares it converts into.",
          "Comparing the share price with the bond's face value.", 78),
         ("Share price $25: in the money.", "in the money",
          ladder([("Diluted shares", "+5", INK), ("Debt", "-100", TEAL)]),
          "Holders would convert. Add the 5 shares and take the bond out of debt.",
          "Adding the shares and keeping the debt too.", 78),
         ("Share price $15: out of the money.", "out of the money",
          ladder([("Diluted shares", "no change", INK), ("Debt", "$100 stays", INK)]),
          "Holders keep the bond. It stays as debt in the EV bridge.",
          "Counting shares nobody would convert into.", 76),
         ("What about diluted EPS?", "diluted EPS",
          formula([("Add back after-tax interest, ", TEAL), ("add the shares", INK)]),
          "The if-converted method: if the bond converts, its interest stops, so the "
          "numerator rises too.",
          "Adding the shares but leaving the interest cost in.", 78)],
        "Convertible bond", [
            ("Conversion price", "$100 / 5 = $20"),
            ("Above $20", "shares in, debt out"),
            ("Below $20", "stays as debt"),
            ("Diluted EPS", "interest added back")],
        "Debt or shares. Pick one.",
        ["Find the conversion price.",
         "In the money: count the shares.",
         "Never count it twice."])


@deck
def n3_06_five_years():
    return build(
        "n3-06-five-years", REC, "ink",
        "&ldquo;Where do you see yourself in 5 years?&rdquo;",
        ["Honest", "Grounded", "Short"],
        "Say the wrong thing and they hear that you are leaving.",
        "They are checking 1 thing",
        "Will you <t>stay</t> long enough, and work hard enough, to be worth training?",
        [("Start with the next 2 years.", "2 years",
          steps(["Learn the modelling", "Get on live deals", "Be trusted with more"]),
          "Show you have thought about the analyst years themselves.",
          "Skipping straight past the job you are interviewing for.", 80),
         ("Leave exit options out.", "exit options",
          ladder([("&ldquo;Private equity in 2 years&rdquo;", "you plan to leave", RED),
                  ("&ldquo;Growing into the associate role&rdquo;", "you plan to build", TEAL)]),
          "Even if you are unsure, lead with growth in the job in front of you.",
          "Naming the fund you want to join.", 78),
         ("Make it about skills.", "skills",
          formula([("Judgement on deals, ", INK), ("not a title.", TEAL)]),
          "Talk about what you want to be good at, not where you want to sit.",
          "Promising a managing director title in 5 years.", 84),
         ("Keep it short.", "short",
          formula([("3 sentences. ", INK), ("Then stop.", TEAL)]),
          "It is a quick check, not a life plan.",
          "Over-planning it, which sounds rehearsed.", 84)],
        "5 years", [
            ("The analyst years first", "learn, deals, trust"),
            ("No exit plan", "growth in the job"),
            ("Skills, not titles", "judgement on deals"),
            ("3 sentences", "then stop")],
        "Grow here first.",
        ["Start with the analyst years.",
         "Leave exits out.",
         "Talk skills, not titles."])


# ------------------------------------------------------------- Sat 28 Nov (red / ink / paper)
@deck
def n3_07_no_profit():
    return build(
        "n3-07-no-profit", TECH, "red",
        "How do you value a company that loses money?",
        ["P/E", "Revenue multiples", "DCF"],
        "The usual multiples stop working. The question is what replaces them.",
        "Negative earnings break P/E",
        "A price divided by a loss <t>means nothing</t>, so you move up the income statement.",
        [("Move up the income statement.", "income statement",
          ladder([("P/E", "negative, no use", RED), ("EV/EBITDA", "if EBITDA is positive", INK),
                  ("EV/Revenue", "if it is not", TEAL)]),
          "Use the highest line that is still positive and comparable.",
          "Quoting a negative P/E.", 80),
         ("Use forward numbers.", "forward",
          formula([("Next year's or later ", TEAL), ("estimates", INK)]),
          "If the company is expected to turn profitable, value it on those later years.",
          "Using only the latest year's loss.", 84),
         ("Stretch the DCF.", "DCF",
          steps(["Longer forecast", "Until margins settle", "Then terminal value"]),
          "Forecast far enough that the business reaches steady margins before the "
          "terminal value.",
          "A 5-year forecast that ends while it is still losing money.", 84),
         ("Check the funding.", "funding",
          formula([("Cash burn ", RED), ("vs cash on hand", INK)]),
          "A loss-making company may need to raise money, which dilutes existing owners.",
          "Ignoring the dilution from future fundraising.", 84)],
        "Loss-making company", [
            ("P/E fails", "move up the statement"),
            ("Forward multiples", "on future profit"),
            ("Longer DCF", "until margins settle"),
            ("Funding needs", "future dilution")],
        "Move up the income statement.",
        ["Revenue or EBITDA multiples.",
         "Value the profitable years.",
         "Watch the cash burn."])


@deck
def n3_08_lbo_candidate():
    return build(
        "n3-08-lbo-candidate", TECH, "ink",
        "What makes a good LBO candidate?",
        ["Cash flow", "Capex", "Exit"],
        "Every trait comes back to 1 thing: paying down the debt.",
        "The debt has to be serviced",
        "A buyout loads the company with debt, so the business must <t>generate cash</t> "
        "every year.",
        [("Stable, predictable cash flow.", "predictable",
          ladder([("Recurring revenue, steady margins", "good", TEAL),
                  ("Cyclical, lumpy results", "risky", RED)]),
          "Lenders lend against cash flow they can count on.",
          "Picking a fast grower that burns cash.", 84),
         ("Low capital needs.", "capital",
          formula([("Less capex ", INK), ("= more cash for debt", TEAL)]),
          "Every dollar not spent on capex can repay debt.",
          "Ignoring how much the business must reinvest.", 84),
         ("Room to improve.", "improve",
          steps(["Costs to cut", "Assets to sell", "Margins to raise"]),
          "The sponsor needs a plan to grow EBITDA, not just ride it.",
          "Assuming multiple expansion will make the return.", 84),
         ("A clear way out.", "way out",
          ladder([("Sale to a strategic buyer", "", TEAL), ("Sale to another sponsor", "", TEAL),
                  ("IPO", "", TEAL)]),
          "The return only exists once the stake is sold.",
          "Forgetting the exit entirely.", 84)],
        "LBO candidate", [
            ("Predictable cash flow", "lenders can count on it"),
            ("Low capex", "more cash for debt"),
            ("Room to improve", "costs, assets, margins"),
            ("A clear exit", "strategic, sponsor or IPO")],
        "Cash to pay the debt, then a way out.",
        ["Steady cash flow.",
         "Little reinvestment needed.",
         "A buyer at the end."])


@deck
def n3_09_why_hire():
    return build(
        "n3-09-why-hire", REC, "paper",
        "&ldquo;Why should we hire you?&rdquo;",
        ["Proof", "The job", "Short"],
        "The question everyone dreads is the easiest one to prepare.",
        "Adjectives are not proof",
        "&ldquo;Hard-working and detail-oriented&rdquo; is what everyone says. "
        "<t>Evidence</t> is what they remember.",
        [("Match it to the job.", "job",
          ladder([("Long hours, tight deadlines", "work ethic", INK),
                  ("Models that must be right", "accuracy", INK),
                  ("Learning fast", "curiosity", INK)]),
          "Pick the traits the analyst job actually needs.",
          "Listing traits that have nothing to do with banking.", 84),
         ("Back each with a fact.", "fact",
          steps(["The trait", "A time you showed it", "What happened"]),
          "One short example per trait, from your own experience.",
          "Adjectives with nothing behind them.", 84),
         ("Keep it to 3.", "3",
          formula([("3 reasons. ", INK), ("Each with proof.", TEAL)]),
          "More than 3 and none of them stick.",
          "A list of 7 strengths.", 84),
         ("Close on the fit.", "fit",
          formula([("Why this team, ", INK), ("right now.", TEAL)]),
          "End with 1 line on why you want this role at this firm.",
          "Ending on a list instead of a reason.", 84)],
        "Why hire you", [
            ("Traits the job needs", "work ethic, accuracy, curiosity"),
            ("1 fact each", "a time you showed it"),
            ("3 at most", "so they stick"),
            ("Close on fit", "this team, right now")],
        "Proof, not adjectives.",
        ["Match traits to the job.",
         "Back each with a fact.",
         "Stop at 3."])


# ------------------------------------------------------------- Sun 29 Nov (ink / paper / red)
@deck
def n3_10_asset_stock():
    return build(
        "n3-10-asset-stock", TECH, "ink",
        "Asset deal or stock deal. What's the difference?",
        ["Liabilities", "Tax basis", "Who prefers which"],
        "Same company, same price. Very different tax bill.",
        "What exactly are you buying?",
        "In a stock deal you buy the <t>whole entity</t>. In an asset deal you pick what "
        "you take.",
        [("What comes with it?", "comes with",
          ladder([("Stock deal", "every liability, known or not", RED),
                  ("Asset deal", "only what you choose", TEAL)]),
          "Buying the shares means inheriting the company's history, lawsuits included.",
          "Thinking the buyer can leave liabilities behind in a stock deal.", 84),
         ("What happens to the tax basis?", "tax basis",
          ladder([("Stock deal", "carries over", INK),
                  ("Asset deal", "stepped up to the price paid", TEAL)]),
          "A step-up means more tax depreciation and amortisation, so lower cash tax for "
          "years.",
          "Saying the step-up changes book depreciation only.", 80),
         ("Which does the buyer prefer?", "buyer",
          formula([("Asset deal: ", INK), ("fewer risks, tax step-up", TEAL)]),
          "Both features favour the buyer.",
          "Forgetting that the step-up has a real cash value.", 84),
         ("Which does the seller prefer?", "seller",
          formula([("Stock deal: ", INK), ("taxed once, clean exit", TEAL)]),
          "In the US, a C-corp selling assets can be taxed twice: on the gain, then when "
          "the cash is paid out.",
          "Assuming both sides want the same structure.", 80)],
        "Asset vs stock", [
            ("Stock deal", "all liabilities, basis carries over"),
            ("Asset deal", "chosen liabilities, step-up"),
            ("Buyer", "prefers assets"),
            ("Seller", "prefers stock")],
        "Liabilities and tax decide it.",
        ["Stock deal: you take everything.",
         "Asset deal: the basis steps up.",
         "Buyer and seller want opposite things."])


@deck
def n3_11_cash_or_stock():
    return build(
        "n3-11-cash-or-stock", TECH, "paper",
        "Should the buyer pay in cash or stock?",
        ["Cost", "Risk", "Control"],
        "There is no single right answer. There is a right way to reason.",
        "Paying in stock shares the deal",
        "With stock, the seller becomes an owner and <t>shares the risk</t> of the deal "
        "working.",
        [("When does cash make sense?", "cash",
          ladder([("Plenty of cash or cheap debt", "", TEAL),
                  ("Confident in the target", "keep all the upside", TEAL)]),
          "Cash keeps every share's claim on the upside for the buyer's own shareholders.",
          "Ignoring what the cash or the debt costs.", 84),
         ("When does stock make sense?", "stock",
          ladder([("Shares look richly valued", "cheap currency", TEAL),
                  ("Very large deal", "too big for cash", TEAL),
                  ("Unsure about the target", "share the risk", TEAL)]),
          "Stock spreads the risk and saves cash, at the cost of dilution.",
          "Forgetting that new shares dilute existing owners.", 80),
         ("What does the seller want?", "seller",
          ladder([("Cash", "certain value", INK),
                  ("Stock", "a share of the upside", INK)]),
          "Cash is certain. Stock lets the seller share in what comes next, and in some "
          "structures defers tax.",
          "Assuming sellers always want cash.", 84),
         ("How do you tie it together?", "together",
          formula([("Compare costs, ", INK), ("then who carries the risk.", TEAL)]),
          "Cost of debt after tax against the cost of issuing shares, then who should "
          "bear the risk of the deal.",
          "Answering with one factor only.", 80)],
        "Cash or stock", [
            ("Cash", "confident buyer, keeps upside"),
            ("Stock", "expensive shares, big deal"),
            ("Seller", "certainty or upside"),
            ("The answer", "cost, then risk")],
        "Cost first. Then risk.",
        ["Cash keeps the upside.",
         "Stock shares the risk.",
         "Ask what the seller wants."])


@deck
def n3_12_earnout():
    return build(
        "n3-12-earnout", TECH, "red",
        "What is an earn-out, and why use one?",
        ["Valuation gap", "Contingent", "Risks"],
        "A way to agree on price when buyer and seller cannot.",
        "Pay part of the price later",
        "Some of the price is paid only <t>if targets are met</t> after the deal closes.",
        [("Why would anyone agree to it?", "agree",
          ladder([("Seller", "believes the forecast", INK),
                  ("Buyer", "doubts the forecast", INK),
                  ("Earn-out", "pays if it comes true", TEAL)]),
          "It bridges a gap in valuation by tying part of the price to results.",
          "Calling it a discount. The seller can earn the full price.", 84),
         ("What is it tied to?", "tied",
          formula([("Revenue or EBITDA ", TEAL), ("over a set period", INK)]),
          "A clear metric, a target and a time window, all written into the agreement.",
          "Vague targets, which lead to disputes.", 84),
         ("How is it accounted for?", "accounted",
          formula([("Fair value at closing, ", INK), ("remeasured later", TEAL)]),
          "It is recorded as contingent consideration, and changes in value usually go "
          "through profit and loss.",
          "Recording nothing until it is paid.", 80),
         ("What can go wrong?", "wrong",
          ladder([("Disputes over the numbers", "", RED),
                  ("Seller loses control after closing", "", RED),
                  ("Short-term targets over long-term value", "", RED)]),
          "The seller can no longer run the business but is paid on its results.",
          "Thinking it removes the disagreement. It often delays it.", 80)],
        "Earn-out", [
            ("Price paid later", "if targets are met"),
            ("Bridges a valuation gap", "buyer vs seller"),
            ("Fair value at closing", "remeasured later"),
            ("Risk of disputes", "over the numbers")],
        "Agree now, pay on results.",
        ["It bridges a price gap.",
         "Tie it to a clear metric.",
         "Expect arguments about the numbers."])


# ===========================================================================
if __name__ == "__main__":
    for slug in (sys.argv[1:] or list(DECKS)):
        d = DECKS[slug]()
        paths = d.render()
        problems = check(paths, d.total)
        print(f"{slug}: {len(paths)} slides, "
              f"{sum(p.stat().st_size for p in paths) // 1024}KB, problems: {problems or 'none'}")
