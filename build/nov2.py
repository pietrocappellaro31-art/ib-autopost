"""
Carousels for 19 to 25 Nov 2026: 21 decks, 3 a day (08:00, 12:30, 17:30 ET).

The 10 to 16 Nov batch (nov1.py) was the last one queued, so 17 and 18 Nov had
no carousel. Pietro, 19 Nov: "Make sure this carousel is published each day."
Same format, slots and series as nov1. Cover grounds continue the diagonal
rotation by calendar day from 10 Nov (day 1): 19 Nov is day 10, the day 1
pattern red / ink / paper; 20 Nov ink / paper / red; 21 Nov paper / red / ink.

Technicals worked before writing (illustrative inputs, stated on the slide):

ACCRUED  $10 bonus accrued, unpaid, deductible this year, 25% tax: pre-tax -10,
         tax -2.5, NI -7.5. CFS: NI -7.5, accrued liabilities +10, cash +2.5.
         BS: cash +2.5; accrued liabilities +10, retained earnings -7.5, so
         L+E +2.5. Paid next year: cash -10, accrued -10, no IS effect.
UFCF     EBIT 100, tax 25%, D&A 20, capex 30, NWC +10: UFCF 75 + 20 - 30 - 10 = 55.
         Interest 20: NI (100 - 20) x 0.75 = 60; LFCF 60 + 20 - 30 - 10 = 40 =
         55 - 20 x 0.75. UFCF at WACC gives EV; LFCF at cost of equity gives
         equity value.
TSM      10 options, strike $10, share price $20: proceeds $100 buy back 5 shares,
         net 5 new. Basic 100 becomes diluted 105. Options with a strike above
         the share price are left out.
WATERFALL Sale proceeds 500. Senior 400 recovers 400 (100%). Subordinated 200
         recovers 100 (50%). Equity 0.
ROIC     Invest 100 at ROIC 12%, WACC 10%: earns 12, capital costs 10, +2 a year;
         as a perpetuity 2 / 0.10 = 20. At ROIC 8%: -2 a year, -20.
DEFREV   $120 annual subscription paid upfront: cash +120, deferred revenue +120,
         no revenue. Revenue 10 a month, deferred revenue down 10 a month.
LBO      EBITDA 100 at 10 times = 1,000: debt 600, equity 400. Year 5 EBITDA 150 at
         10 times = 1,500; debt paid down to 300; equity 1,200. MOIC 3.0;
         3^(1/5) = 1.246, about 25%. Gain 800 = growth 50 x 10 = 500 + paydown 300.
KD       Coupon 5% bond at 90: current yield 5 / 90 = 5.6%, yield to maturity higher
         again with the pull to par. Pre-tax 6% at 25% tax: 6 x 0.75 = 4.5%.
GOODWILL $50 impairment, not deductible: NI -50; CFS add back 50, cash 0; goodwill
         -50, retained earnings -50. If deductible: tax -12.5, NI -37.5, cash +12.5.
         IFRS (IAS 36) and US GAAP for public companies (ASC 350): goodwill is
         tested for impairment, not amortised.
SOTP     A: EBITDA 50 at 8 times = 400. B: EBITDA 30 at 12 times = 360. EV 760, net
         debt 200, equity value 560.
BANK     Justified P/B = (ROE - g) / (COE - g). ROE 12%, COE 10%, g 4%: 8 / 6 = 1.33.
         ROE = COE gives 1.0.
ASSOC    Own 30% of a company earning 100: 30 of equity income, below EBITDA.
         Equity value 1,000 + debt 300 - cash 100 - associate stake 150 = EV 1,050.
NOL      100 of NOLs at 25%: at most 25 of tax saved, only as taxable income arrives.
         US federal losses from 2018 on carry forward without expiry and offset up
         to 80% of taxable income a year; section 382 caps annual use after an
         ownership change at the old company's value times the long-term
         tax-exempt rate.
COVENANT Maintenance: tested every period (often quarterly), common in bank loans.
         Incurrence: tested only when the company acts (new debt, a dividend),
         common in high-yield bonds. 4.0 times is an illustrative test level.
"""

import sys

from brand import INK, RED, TEAL, check
from nov1 import REC, TECH, build
from parts import formula, ladder, steps

DECKS = {}


def deck(fn):
    DECKS[fn.__name__.replace("_", "-")] = fn
    return fn


# ------------------------------------------------------------- Thu 19 Nov
@deck
def n2_01_accrued_bonus():
    return build(
        "n2-01-accrued-bonus", TECH, "red",
        "A $10 bonus is accrued but not paid. Walk me through it.",
        ["Income statement", "Cash flow", "Balance sheet"],
        "Three statement question where the liability side does the work.",
        "The expense is real. The cash has not moved.",
        "Watch where the $10 lands: on the <t>liability side</t>, not on cash.",
        [("Start on the income statement.", "income statement",
          ladder([("Bonus expense", "+10", RED), ("Pre-tax income", "-10", INK),
                  ("Tax at 25%", "-2.5", TEAL)], "Net income", "-7.5"),
          "The bonus is an operating expense this year. At 25% tax, net income falls by "
          "$7.50.",
          "Skipping the expense because no cash was paid.", 74),
         ("Then the cash flow statement.", "cash flow",
          ladder([("Net income", "-7.5", RED), ("Accrued liabilities up", "+10", TEAL)],
                 "Change in cash", "+2.5"),
          "An increase in a liability is added back in cash from operations. Cash ends "
          "$2.50 higher, the tax saved.",
          "Saying cash falls by $10. It falls next year, when the bonus is paid.", 74),
         ("Then the balance sheet.", "balance sheet",
          ladder([("Cash", "+2.5", TEAL), ("Accrued liabilities", "+10", RED),
                  ("Retained earnings", "-7.5", INK)]),
          "Assets rise $2.50. Liabilities rise $10 and equity falls $7.50, a net $2.50. "
          "It balances.",
          "Putting the $10 on the asset side.", 74),
         ("Next year it is paid.", "paid",
          ladder([("Cash", "-10", RED), ("Accrued liabilities", "-10", INK)],
                 "Income statement", "no change"),
          "Paying the bonus settles the liability. The expense was already booked, so net "
          "income does not move again.",
          "Expensing it a second time when the cash goes out.", 74)],
        "Accrued bonus $10", [
            ("Net income -7.5", "after 25% tax"),
            ("Cash +2.5", "liability added back"),
            ("Accrued +10, equity -7.5", "it balances"),
            ("Paid next year", "cash -10, no new expense")],
        "Expense now. Cash later.",
        ["Book the expense after tax.",
         "Add the new liability back to cash.",
         "No second expense when it is paid."])


@deck
def n2_02_ufcf_lfcf():
    return build(
        "n2-02-ufcf-lfcf", TECH, "ink",
        "Unlevered or levered free cash flow?",
        ["Interest", "Discount rate", "EV or equity"],
        "The DCF question that tests whether you know who the cash belongs to.",
        "Two cash flows, two owners",
        "The difference is one line, <t>interest</t>, and it decides everything else.",
        [("Unlevered: before interest.", "before interest",
          ladder([("EBIT x (1 - 25%)", "75", INK), ("Plus D&amp;A", "+20", TEAL),
                  ("Less capex", "-30", RED), ("Less rise in NWC", "-10", RED)],
                 "Unlevered FCF", "55"),
          "Cash available to every capital provider, lenders and shareholders alike.",
          "Taking tax on EBIT after interest. Unlevered uses tax on EBIT alone.", 80),
         ("Levered: after interest.", "after interest",
          ladder([("Unlevered FCF", "55", INK), ("Interest 20 after tax", "-15", RED)],
                 "Levered FCF", "40"),
          "Cash left for shareholders once lenders are paid. Debt repaid or raised moves it "
          "too.",
          "Subtracting interest before tax. It saves tax, so take 20 x 75%.", 80),
         ("Match the discount rate.", "discount rate",
          ladder([("Unlevered FCF", "at WACC", TEAL), ("Levered FCF", "at cost of equity", TEAL)]),
          "WACC blends lenders and shareholders, so it fits unlevered. Cost of equity fits "
          "shareholders' cash.",
          "Discounting levered FCF at WACC.", 80),
         ("And what you get out.", "get out",
          ladder([("Unlevered DCF", "enterprise value", INK),
                  ("Levered DCF", "equity value", INK)]),
          "Most bank DCFs are unlevered, then bridge from EV to equity value.",
          "Calling an unlevered DCF's answer the equity value.", 84)],
        "UFCF vs LFCF", [
            ("Unlevered: before interest", "55 in the example"),
            ("Levered: after interest", "40 in the example"),
            ("UFCF at WACC", "gives EV"),
            ("LFCF at cost of equity", "gives equity value")],
        "Match the cash to its owner.",
        ["Unlevered goes to everyone.",
         "Levered goes to shareholders.",
         "Rate and output follow from that."])


@deck
def n2_03_weakness():
    return build(
        "n2-03-weakness", REC, "paper",
        "&ldquo;What is your greatest weakness?&rdquo;",
        ["Real", "Fixed", "Proof"],
        "The question everyone dreads, and the dodge everyone tries.",
        "They know the trick answers",
        "&ldquo;I work too hard&rdquo; tells them you <t>will not</t> be honest with them.",
        [("Drop the disguised strengths.", "disguised",
          ladder([("&ldquo;I'm a perfectionist&rdquo;", "heard it", RED),
                  ("&ldquo;I care too much&rdquo;", "heard it", RED),
                  ("&ldquo;I work too hard&rdquo;", "heard it", RED)]),
          "They sound safe and land badly. An interviewer hears that you will not admit a "
          "mistake on a deal.",
          "Thinking a fake weakness is the low-risk option.", 80),
         ("Pick a real one, not a core one.", "real one",
          ladder([("Real and fixable", "use it", TEAL),
                  ("Core to the job", "avoid", RED)]),
          "Speaking up in large meetings works. &ldquo;Not great with Excel&rdquo; for an "
          "analyst role does not.",
          "Naming attention to detail. It is the job.", 80),
         ("Build it in 3 beats.", "3 beats",
          steps(["The weakness, in a sentence", "When it cost you",
                 "What you changed, and where it is now"]),
          "Most of the answer is the third beat. They are listening for self-awareness and "
          "action.",
          "Spending a minute on the weakness and ten seconds on the fix.", 80),
         ("End where you are now.", "now",
          formula([("Still working on it. ", INK), ("Here is the proof.", TEAL)]),
          "Do not claim it is solved. Show the habit you use and the last time it worked.",
          "Saying it is completely gone. Nobody believes that.", 80)],
        "Greatest weakness", [
            ("No disguised strengths", "they backfire"),
            ("Real, not core to the job", "fixable"),
            ("Weakness, cost, change", "3 beats"),
            ("End on proof", "not on solved")],
        "Honest, small, and being fixed.",
        ["One real weakness.",
         "One time it cost you.",
         "What you do about it now."])


# ------------------------------------------------------------- Fri 20 Nov
@deck
def n2_04_tsm():
    return build(
        "n2-04-tsm", TECH, "ink",
        "How do options change the share count?",
        ["Treasury stock method", "Diluted shares"],
        "Every equity value you calculate depends on getting this right.",
        "Basic shares undercount the owners",
        "Option holders can buy in, so the <t>diluted</t> count is the one you value on.",
        [("Only count the ones in the money.", "in the money",
          ladder([("Strike below share price", "count it", TEAL),
                  ("Strike above share price", "leave it out", RED)]),
          "Nobody exercises an option to pay $25 for a $20 share.",
          "Adding every option outstanding.", 80),
         ("Exercise, then buy back.", "buy back",
          ladder([("10 options at a $10 strike", "+10 shares", INK),
                  ("Cash raised", "$100", TEAL),
                  ("Bought back at $20", "-5 shares", RED)],
                 "Net new shares", "+5"),
          "The method assumes the company uses the exercise cash to repurchase shares at "
          "today's price.",
          "Adding all 10 shares and forgetting the buyback.", 74),
         ("So the diluted count is...", "diluted",
          formula([("100 basic ", INK), ("+ 5 net new ", TEAL), ("= 105", INK)]),
          "Equity value per share uses 105, not 100.",
          "Mixing basic shares with a diluted price.", 80),
         ("Circular? A little.", "Circular",
          formula([("Price sets dilution. ", INK), ("Dilution sets price.", TEAL)]),
          "When you are solving for an implied price, the share count moves with it. "
          "Models iterate.",
          "Fixing the share count at today's price in a valuation output.", 80)],
        "Treasury stock method", [
            ("In the money only", "strike below price"),
            ("Exercise cash buys shares back", "at today's price"),
            ("10 options become 5 shares", "in the example"),
            ("Value on diluted", "105, not 100")],
        "Exercise, buy back, count the rest.",
        ["Drop out-of-the-money options.",
         "Proceeds divided by price is the buyback.",
         "Use diluted shares for per-share value."])


@deck
def n2_05_waterfall():
    return build(
        "n2-05-waterfall", TECH, "paper",
        "A company is sold in bankruptcy. Who gets paid first?",
        ["Senior", "Subordinated", "Equity"],
        "The question behind every credit and restructuring interview.",
        "There is not enough to go around",
        "Claims are paid <t>in order</t>. Each class waits until the one above is paid in "
        "full.",
        [("Line up the claims.", "claims",
          steps(["Senior secured debt", "Subordinated debt", "Equity"]),
          "The order comes from the debt documents and bankruptcy law: secured lenders, "
          "then junior lenders, then shareholders.",
          "Thinking everyone shares the proceeds pro rata.", 84),
         ("Run the waterfall on $500.", "$500",
          ladder([("Senior debt 400", "gets 400", TEAL),
                  ("Subordinated debt 200", "gets 100", RED),
                  ("Equity", "gets 0", RED)]),
          "Senior is paid in full. The $100 left goes to subordinated lenders. Nothing "
          "reaches shareholders.",
          "Giving equity something while debt is unpaid.", 80),
         ("Recovery is the ratio.", "Recovery",
          ladder([("Senior", "400 / 400 = 100%", TEAL),
                  ("Subordinated", "100 / 200 = 50%", RED)]),
          "Recovery is what a class receives divided by its claim.",
          "Quoting recovery as a dollar amount.", 84),
         ("Why junior debt pays more.", "pays more",
          formula([("Last in line ", INK), ("= higher interest rate", TEAL)]),
          "Subordinated lenders lose first when value falls, so they charge more to lend.",
          "Assuming all debt costs the same.", 84)],
        "The waterfall", [
            ("Senior, junior, equity", "in that order"),
            ("Each class waits", "until the one above is full"),
            ("$500 against $600 of debt", "equity gets 0"),
            ("Recovery = paid / claim", "100% and 50%")],
        "Top down, until the money runs out.",
        ["Line up the claims.",
         "Fill each one before the next.",
         "Recovery is paid over claim."])


@deck
def n2_06_roic_growth():
    return build(
        "n2-06-roic-growth", TECH, "red",
        "Does growth always add value?",
        ["ROIC", "WACC", "Value"],
        "Answer before you swipe. Most people say yes.",
        "Growth costs capital",
        "It only adds value when the return beats <t>what the capital costs</t>.",
        [("Compare 2 rates.", "2 rates",
          ladder([("Return on invested capital", "ROIC", INK),
                  ("Cost of that capital", "WACC", INK)]),
          "ROIC is what the business earns on the money put in. WACC is what investors "
          "expect in return.",
          "Judging growth by revenue or EPS alone.", 84),
         ("ROIC above WACC.", "above",
          ladder([("Invest 100 at 12%", "earns 12", TEAL), ("Capital costs 10%", "-10", INK)],
                 "Value each year", "+2"),
          "Each year the investment beats its cost by 2. As a perpetuity at 10%, that is "
          "about 20 of value.",
          "Counting the whole 12 as value created.", 80),
         ("ROIC below WACC.", "below",
          ladder([("Invest 100 at 8%", "earns 8", RED), ("Capital costs 10%", "-10", INK)],
                 "Value each year", "-2", RED),
          "Revenue and profit grow, and the company is worth less for it.",
          "Calling profitable growth good growth.", 80),
         ("So in a DCF...", "DCF",
          formula([("Growth with ", INK), ("ROIC = WACC ", TEAL), ("adds nothing", INK)]),
          "Raising growth while keeping returns at the cost of capital leaves value "
          "unchanged. Check reinvestment matches growth.",
          "Raising growth with no extra capex or working capital.", 74)],
        "Growth and value", [
            ("ROIC above WACC", "growth adds value"),
            ("ROIC below WACC", "growth destroys it"),
            ("ROIC equals WACC", "growth adds nothing"),
            ("Growth needs reinvestment", "model it")],
        "Returns first. Growth second.",
        ["Compare ROIC with WACC.",
         "Only the spread creates value.",
         "Growth needs capital in the model."])


# ------------------------------------------------------------- Sat 21 Nov
@deck
def n2_07_deferred_revenue():
    return build(
        "n2-07-deferred-revenue", TECH, "paper",
        "A customer pays $120 upfront for a year. Is it revenue?",
        ["Cash", "Deferred revenue", "Revenue"],
        "Subscription businesses live on this line. So do interview questions.",
        "Paid is not earned",
        "Revenue is recognised as the service is <t>delivered</t>, not when the cash "
        "arrives.",
        [("Day 1: no revenue.", "no revenue",
          ladder([("Cash", "+120", TEAL), ("Deferred revenue", "+120", INK)],
                 "Revenue", "0"),
          "The company owes a year of service, so the cash comes with a liability.",
          "Booking $120 of revenue on day 1.", 84),
         ("Each month, $10 is earned.", "earned",
          ladder([("Deferred revenue", "-10", INK), ("Revenue", "+10", TEAL)]),
          "As each month of service is delivered, $10 moves from the liability to revenue.",
          "Reducing cash each month. The cash came in once.", 84),
         ("Where is it on cash flow?", "cash flow",
          ladder([("Increase in deferred revenue", "+ add back", TEAL)]),
          "Cash arrived before revenue, so the increase is added in cash from operations.",
          "Missing it, so operating cash flow looks lower than it is.", 84),
         ("Is it debt?", "debt",
          formula([("Settled by service, ", INK), ("not by cash.", TEAL)]),
          "Usually it sits in working capital, not in the EV bridge. Customers fund the "
          "business in advance.",
          "Adding it to net debt like a loan.", 84)],
        "Deferred revenue", [
            ("Cash first, revenue later", "a liability in between"),
            ("$10 a month", "moves to revenue"),
            ("Increase adds to cash", "from operations"),
            ("Working capital, not debt", "settled by service")],
        "Paid is not earned.",
        ["Cash in, liability up.",
         "Earn it as you deliver.",
         "The increase helps operating cash."])


@deck
def n2_08_matching_rule():
    return build(
        "n2-08-matching-rule", TECH, "red",
        "Why is EV / net income the wrong multiple?",
        ["Numerator", "Denominator", "Interest"],
        "One rule fixes every multiple question you will get.",
        "The top and bottom must agree",
        "If the numerator is for everyone, the denominator must be <t>before</t> anyone is "
        "paid.",
        [("EV belongs to every investor.", "every investor",
          ladder([("EV / Revenue", "works", TEAL), ("EV / EBITDA", "works", TEAL),
                  ("EV / EBIT", "works", TEAL)]),
          "These are all before interest, so lenders and shareholders still share them.",
          "Pairing EV with anything after interest.", 84),
         ("Equity value belongs to shareholders.", "shareholders",
          ladder([("Price / Earnings", "works", TEAL), ("Price / Book", "works", TEAL),
                  ("Equity value / Levered FCF", "works", TEAL)]),
          "These are after interest, what is left for shareholders.",
          "Pairing equity value with EBITDA.", 76),
         ("So EV / net income fails.", "fails",
          ladder([("EV", "for everyone", INK), ("Net income", "after lenders", RED)],
                 "Result", "mismatch", RED),
          "Two companies with the same EBITDA but different debt get different multiples "
          "for no operating reason.",
          "Thinking it is just unusual. It is inconsistent.", 80),
         ("The 1-line test.", "1-line",
          formula([("Is interest in the denominator? ", INK), ("Then use equity value.", TEAL)]),
          "Before interest goes with EV. After interest goes with equity value.",
          "Memorising a list instead of the rule.", 74)],
        "The matching rule", [
            ("EV pairs with", "revenue, EBITDA, EBIT"),
            ("Equity value pairs with", "earnings, book, levered FCF"),
            ("EV / net income", "mismatch"),
            ("Ask about interest", "before or after")],
        "Match who the number belongs to.",
        ["EV with pre-interest metrics.",
         "Equity value with post-interest.",
         "Test any multiple with that."])


@deck
def n2_09_dont_know():
    return build(
        "n2-09-dont-know", REC, "ink",
        "You get a technical you cannot answer. Now what?",
        ["Reason", "Honest", "Recover"],
        "It will happen. What you do next is the part they grade.",
        "They are watching how you think",
        "A blank stare costs more than a <t>wrong first step</t> reasoned out loud.",
        [("Do not bluff.", "bluff",
          ladder([("Confident and wrong", "worst", RED),
                  ("Silent", "bad", RED),
                  ("Honest and reasoning", "best", TEAL)]),
          "Interviewers ask follow-ups. A bluff falls apart on the second question.",
          "Inventing a term or a number to fill the gap.", 84),
         ("Say what you do know.", "do know",
          steps(["Restate the question", "Name the concept it touches",
                 "Work from first principles"]),
          "Most technicals connect to the three statements or to valuation. Start from the "
          "piece you know.",
          "Jumping to a final answer without the steps.", 84),
         ("Think out loud.", "out loud",
          formula([("&ldquo;My instinct is X, ", INK), ("because Y.&rdquo;", TEAL)]),
          "Saying your reasoning lets them correct you, and a corrected path still scores.",
          "Thinking in silence for 30 seconds.", 84),
         ("Then close the loop.", "close the loop",
          formula([("Look it up that night. ", INK), ("Mention it in your thank-you.", TEAL)]),
          "It shows you follow through, which is what they want in an analyst.",
          "Pretending it never happened.", 76)],
        "When you do not know", [
            ("Never bluff", "follow-ups expose it"),
            ("Start from what you know", "statements or valuation"),
            ("Reason out loud", "let them guide you"),
            ("Follow up after", "in the thank-you note")],
        "Honest, then reasoned.",
        ["Say what you know.",
         "Think out loud.",
         "Close the loop afterwards."])


# ------------------------------------------------------------- Sun 22 Nov
@deck
def n2_10_paper_lbo():
    return build(
        "n2-10-paper-lbo", TECH, "red",
        "Paper LBO: what is the return?",
        ["Entry", "Exit", "MOIC", "IRR"],
        "No Excel. A pen, 5 numbers and a minute.",
        "Every number fits on a napkin",
        "Find the equity going in and the equity coming out. The rest is <t>one ratio</t>.",
        [("Entry.", "Entry",
          ladder([("EBITDA 100 at 10 times", "EV 1,000", INK), ("Debt", "600", RED),
                  ("Sponsor equity", "400", TEAL)]),
          "The sponsor buys at 10 times EBITDA and funds 60% with debt. Fees ignored.",
          "Computing the return on the full 1,000.", 84),
         ("Exit in year 5.", "Exit",
          ladder([("EBITDA 150 at 10 times", "EV 1,500", INK), ("Debt left", "300", RED)],
                 "Equity at exit", "1,200"),
          "EBITDA grows to 150, the multiple holds and cash flow pays debt down to 300.",
          "Forgetting to subtract the debt still owed.", 84),
         ("The return.", "return",
          ladder([("1,200 / 400", "3.0 times", TEAL), ("3 times in 5 years", "about 25%", TEAL)]),
          "MOIC is 3.0. Tripling over 5 years is an IRR of about 25%.",
          "Dividing the 800 gain by 5 and calling it 40% a year.", 84),
         ("Where did the 800 come from?", "800",
          ladder([("EBITDA growth: 50 x 10", "500", TEAL), ("Debt paydown", "300", TEAL),
                  ("Multiple change", "0", INK)]),
          "Growth, paydown and multiple are the 3 levers. Here, growth did most of it.",
          "Crediting all of it to leverage.", 84)],
        "Paper LBO", [
            ("Equity in", "400"),
            ("Equity out", "1,200"),
            ("MOIC 3.0", "IRR about 25%"),
            ("Growth 500, paydown 300", "multiple 0")],
        "Equity in, equity out, one ratio.",
        ["Subtract debt at both ends.",
         "3 times in 5 years is about 25%.",
         "Split the gain into its 3 levers."])


@deck
def n2_11_cost_of_debt():
    return build(
        "n2-11-cost-of-debt", TECH, "ink",
        "What is the cost of debt in WACC?",
        ["Coupon", "Yield", "After tax"],
        "The coupon is the wrong answer more often than not.",
        "The coupon was set years ago",
        "WACC needs what lenders want <t>today</t>, not what they agreed to then.",
        [("Use the yield, not the coupon.", "yield",
          ladder([("Coupon", "5%", INK), ("Bond price", "90", RED),
                  ("Current yield 5 / 90", "5.6%", TEAL)]),
          "A bond below par yields more than its coupon. Yield to maturity is higher still, "
          "because it is repaid at 100.",
          "Plugging in the coupon rate.", 84),
         ("Then take tax off.", "tax",
          formula([("6% x (1 - 25%) ", INK), ("= 4.5%", TEAL)]),
          "Interest is deductible, so the cost to the company is after tax.",
          "Using the pre-tax rate in WACC.", 84),
         ("No traded bonds?", "No traded",
          steps(["Find the credit rating", "Find yields on similar debt",
                 "Or add a spread to the risk-free rate"]),
          "For private or unrated companies, borrow the yield of comparable credit.",
          "Using interest expense over book debt.", 84),
         ("Why not interest / debt?", "interest / debt",
          formula([("History, ", INK), ("not the market.", TEAL)]),
          "Book interest reflects old loans at old rates. WACC is forward-looking.",
          "Thinking a historical average is close enough.", 84)],
        "Cost of debt", [
            ("Yield, not coupon", "what lenders want now"),
            ("After tax", "6% becomes 4.5%"),
            ("No bonds", "use comparable credit"),
            ("Not interest over debt", "that is history")],
        "Today's yield, after tax.",
        ["Yield to maturity, not the coupon.",
         "Multiply by 1 minus the tax rate.",
         "Borrow a yield if there is none."])


@deck
def n2_12_deal_discussion():
    return build(
        "n2-12-deal-discussion", REC, "paper",
        "&ldquo;Tell me about a deal you have followed.&rdquo;",
        ["What", "Why", "Your view"],
        "Every interviewer asks it. Most candidates recite a headline.",
        "They want analysis, not news",
        "A headline anyone can read. What they want is <t>your view</t> on it.",
        [("Pick one deal and know it cold.", "one deal",
          steps(["Buyer and target", "Price and how it was paid",
                 "Where it stands now"]),
          "Choose a deal you can discuss for 10 minutes, ideally in the group you are "
          "interviewing for.",
          "Picking the biggest deal of the year and knowing only the headline.", 80),
         ("Explain the logic.", "logic",
          ladder([("Why the buyer wanted it", "strategy", TEAL),
                  ("Why the seller sold", "the other side", TEAL),
                  ("Why now", "timing", TEAL)]),
          "Most candidates explain only the buyer. Covering the seller and the timing is "
          "what stands out.",
          "Repeating the press release's language.", 84),
         ("Have a number ready.", "number",
          formula([("The multiple paid, ", INK), ("against peers.", TEAL)]),
          "Know what was paid and how it compares, from the filing or announcement, not "
          "from memory of a headline.",
          "Quoting a number you cannot source.", 84),
         ("Then give your view.", "view",
          formula([("Good deal or bad? ", INK), ("Say which, and why.", TEAL)]),
          "Name the biggest risk too. A view with a risk attached sounds like an analyst.",
          "Sitting on the fence.", 84)],
        "Deal discussion", [
            ("One deal, known cold", "10 minutes deep"),
            ("Buyer, seller, timing", "the logic"),
            ("A sourced number", "multiple vs peers"),
            ("A view and a risk", "not a summary")],
        "Know it. Explain it. Judge it.",
        ["One deal you can defend.",
         "The logic from both sides.",
         "Your view, with the risk."])


# ------------------------------------------------------------- Mon 23 Nov
@deck
def n2_13_goodwill_impairment():
    return build(
        "n2-13-goodwill-impairment", TECH, "ink",
        "Goodwill is impaired by $50. Walk me through it.",
        ["Income statement", "Cash flow", "Balance sheet"],
        "Three statement question with a tax assumption to state first.",
        "Ask about tax first",
        "The answer changes with one assumption: is the impairment <t>deductible</t>?",
        [("Assume it is not deductible.", "not deductible",
          ladder([("Impairment", "+50", RED), ("Tax effect", "0", INK)],
                 "Net income", "-50"),
          "Book impairments of goodwill often give no tax deduction, so net income falls "
          "by the full $50.",
          "Applying the 25% tax shield without asking.", 80),
         ("Cash flow statement.", "Cash flow",
          ladder([("Net income", "-50", RED), ("Add back impairment", "+50", TEAL)],
                 "Change in cash", "0"),
          "It is non-cash, so it is added back. With no tax saved, cash does not move.",
          "Saying cash falls by $50.", 84),
         ("Balance sheet.", "Balance sheet",
          ladder([("Goodwill", "-50", RED), ("Retained earnings", "-50", INK)]),
          "Assets fall $50 and equity falls $50. It balances.",
          "Forgetting to reduce goodwill itself.", 84),
         ("If it were deductible.", "deductible",
          ladder([("Tax at 25%", "-12.5", TEAL), ("Net income", "-37.5", INK)],
                 "Change in cash", "+12.5"),
          "Then it works like depreciation: the tax saved is real cash. State the "
          "assumption out loud.",
          "Not saying which case you are answering.", 84)],
        "Goodwill impairment $50", [
            ("Not deductible", "net income -50"),
            ("Add back on cash flow", "cash 0"),
            ("Goodwill -50", "equity -50"),
            ("If deductible", "cash +12.5")],
        "State the tax assumption first.",
        ["Not deductible: cash unchanged.",
         "Deductible: cash rises by the tax saved.",
         "Goodwill and equity fall together."])


@deck
def n2_14_sotp():
    return build(
        "n2-14-sotp", TECH, "paper",
        "How do you value a company with 2 different businesses?",
        ["Sum of the parts", "Multiples", "Net debt"],
        "One multiple for a conglomerate is the wrong multiple for both halves.",
        "One multiple cannot fit both",
        "Value each division against <t>its own</t> peers, then add them up.",
        [("Value each part.", "each part",
          ladder([("Division A: EBITDA 50 at 8 times", "400", INK),
                  ("Division B: EBITDA 30 at 12 times", "360", INK)],
                 "Enterprise value", "760"),
          "Each division gets the multiple its own comparable companies trade at.",
          "Applying the group's blended multiple to both.", 74),
         ("Then bridge to equity.", "equity",
          ladder([("Enterprise value", "760", INK), ("Net debt", "-200", RED)],
                 "Equity value", "560"),
          "Debt and cash usually sit at the group level, so take them off once at the end.",
          "Subtracting net debt from each division.", 84),
         ("Why it matters.", "matters",
          formula([("Market value below 760? ", INK), ("Conglomerate discount.", TEAL)]),
          "If the group trades below the sum of its parts, a breakup or spin-off may unlock "
          "value.",
          "Assuming the market always prices the sum.", 80),
         ("What else to subtract?", "subtract",
          ladder([("Head office costs", "capitalise and subtract", RED),
                  ("Taxes on a breakup", "if relevant", RED)]),
          "Central costs belong to no division, so value them separately and take them off.",
          "Leaving corporate costs out entirely.", 84)],
        "Sum of the parts", [
            ("Each division, own peers", "400 + 360"),
            ("EV 760", "less net debt 200"),
            ("Equity value 560", "in the example"),
            ("Subtract central costs", "they belong to no one")],
        "Value the parts, then add.",
        ["One multiple per division.",
         "Net debt once, at the end.",
         "Head office costs come off."])


@deck
def n2_15_bank_valuation():
    return build(
        "n2-15-bank-valuation", TECH, "red",
        "Why can't you value a bank on EV / EBITDA?",
        ["Debt", "P/B", "ROE"],
        "The FIG question that catches generalists every time.",
        "For a bank, debt is inventory",
        "Deposits and borrowing are <t>raw material</t>, not financing. Interest is the "
        "cost of sales.",
        [("Why EV breaks.", "EV",
          ladder([("Debt", "part of operations", RED), ("Interest", "an operating cost", RED)],
                 "EV / EBITDA", "meaningless", RED),
          "You cannot separate operating from financing, so EV and EBITDA have no clean "
          "meaning.",
          "Netting deposits like normal debt.", 84),
         ("Use equity multiples.", "equity",
          ladder([("Price / Earnings", "P/E", TEAL), ("Price / Book", "P/B", TEAL),
                  ("Price / Tangible book", "P/TBV", TEAL)]),
          "Value the equity directly. A dividend discount model is the intrinsic version.",
          "Running an unlevered DCF on a bank.", 84),
         ("What drives P/B?", "P/B",
          formula([("P/B = ", INK), ("(ROE - g) / (COE - g)", TEAL)]),
          "A bank earning more than its cost of equity trades above book. At ROE 12%, cost "
          "of equity 10% and growth 4%, P/B is about 1.33.",
          "Treating a low P/B as cheap without checking ROE.", 80),
         ("The 1-line version.", "1-line",
          formula([("ROE = cost of equity ", INK), ("&rarr; P/B of 1.0", TEAL)]),
          "Returns equal to what shareholders require make the equity worth its book value.",
          "Forgetting the link between ROE and P/B.", 80)],
        "Valuing a bank", [
            ("Debt is raw material", "EV does not work"),
            ("P/E, P/B, P/TBV", "equity multiples"),
            ("P/B from ROE", "(ROE - g) / (COE - g)"),
            ("ROE = COE", "P/B of 1.0")],
        "Value the equity, not the enterprise.",
        ["Debt is operations for a bank.",
         "Use P/E and P/B.",
         "ROE explains P/B."])


# ------------------------------------------------------------- Tue 24 Nov
@deck
def n2_16_equity_investments():
    return build(
        "n2-16-equity-investments", TECH, "paper",
        "A company owns 30% of another. What happens in the EV bridge?",
        ["Equity method", "EBITDA", "Subtract"],
        "The mirror image of minority interest, and just as often asked.",
        "The earnings are not in EBITDA",
        "A 30% stake shows up as one line <t>below</t> operating profit.",
        [("How it is booked.", "booked",
          ladder([("Associate earns", "100", INK), ("30% share", "30", TEAL)],
                 "Equity income", "below EBITDA"),
          "Under the equity method, the company books its share of the profit, not the "
          "associate's revenue or EBITDA.",
          "Consolidating it like a subsidiary.", 84),
         ("So subtract it from EV.", "subtract",
          ladder([("Equity value", "1,000", INK), ("Plus debt", "+300", RED),
                  ("Less cash", "-100", TEAL), ("Less 30% stake", "-150", TEAL)],
                 "Enterprise value", "1,050"),
          "EBITDA excludes the stake's earnings, so EV must exclude its value too.",
          "Adding it, as you would minority interest.", 74),
         ("Compare minority interest.", "minority interest",
          ladder([("Own 80%, consolidate 100%", "add NCI", INK),
                  ("Own 30%, consolidate 0%", "subtract stake", INK)]),
          "Both fix the same problem: making EV match the EBITDA it is divided by.",
          "Memorising signs without the reason.", 84),
         ("The rule.", "rule",
          formula([("In EBITDA? Keep it in EV. ", INK), ("Not in EBITDA? Take it out.", TEAL)]),
          "Every bridge item follows from what the denominator includes.",
          "Treating the bridge as a list to memorise.", 74)],
        "Equity investments", [
            ("30% stake", "equity method"),
            ("Earnings below EBITDA", "not in the multiple"),
            ("Subtract from EV", "1,050 in the example"),
            ("Mirror of NCI", "same logic, other sign")],
        "Match EV to EBITDA.",
        ["Equity income sits below EBITDA.",
         "So subtract the stake's value.",
         "Add NCI, subtract associates."])


@deck
def n2_17_nols():
    return build(
        "n2-17-nols", TECH, "red",
        "Why would a buyer pay for a target's past losses?",
        ["NOLs", "Tax", "Timing"],
        "Losses can be an asset. Whether they are depends on 1 question.",
        "Old losses can cut future tax",
        "Net operating losses offset <t>future</t> taxable income, so they save real cash.",
        [("What they are worth at most.", "at most",
          formula([("100 of NOLs x 25% ", INK), ("= up to 25 of tax saved", TEAL)]),
          "That ceiling is only reached if the company earns enough taxable income to use "
          "them.",
          "Valuing them at the full 25 today.", 80),
         ("Timing matters.", "Timing",
          steps(["Forecast taxable income", "Apply the yearly limit",
                 "Discount the tax saved each year"]),
          "Value is the present value of the tax actually saved, year by year.",
          "Ignoring when the company turns profitable.", 84),
         ("The US limits.", "limits",
          ladder([("Losses from 2018 on", "no expiry", TEAL),
                  ("Yearly use", "up to 80% of taxable income", INK)]),
          "Federal losses from 2018 can be carried forward without expiry, but each year "
          "they offset at most 80% of taxable income.",
          "Assuming losses wipe out all tax in year 1.", 80),
         ("And after an acquisition.", "acquisition",
          formula([("Section 382 ", RED), ("caps yearly use.", INK)]),
          "After an ownership change, annual use is limited to the old company's value times "
          "a long-term tax-exempt rate.",
          "Paying for NOLs the buyer cannot use for years.", 80)],
        "NOLs in a deal", [
            ("Worth up to NOLs x tax rate", "25 on 100"),
            ("Only with taxable income", "timing drives value"),
            ("US: 80% yearly limit", "losses from 2018"),
            ("Section 382", "caps use after a deal")],
        "Worth the tax saved, when it is saved.",
        ["Multiply by the tax rate for the ceiling.",
         "Discount by when they are used.",
         "Check the limits after a deal."])


@deck
def n2_18_cold_email():
    return build(
        "n2-18-cold-email", REC, "ink",
        "How do you write a cold email to a banker?",
        ["Short", "Specific", "One ask"],
        "Bankers read email on their phones between calls. Write for that.",
        "They read it between calls",
        "Make the ask clear before the <t>first scroll</t>.",
        [("Subject line first.", "Subject",
          formula([("Shared school + ", INK), ("a specific ask", TEAL)]),
          "A connection in the subject, such as your shared university, gets the email "
          "opened.",
          "&ldquo;Quick question&rdquo; or &ldquo;Hello&rdquo;.", 84),
         ("4 sentences, no more.", "4 sentences",
          steps(["Who you are", "Why them, specifically", "One ask: a 15-minute call",
                 "When you are free"]),
          "Keep it readable on one phone screen.",
          "A paragraph on your life story.", 84),
         ("Make the ask small.", "small",
          ladder([("&ldquo;Can you refer me?&rdquo;", "too big", RED),
                  ("&ldquo;15 minutes this week?&rdquo;", "easy yes", TEAL)]),
          "A short call is easy to agree to. Referrals come later, after a real "
          "conversation.",
          "Asking for a job in the first email.", 84),
         ("Follow up once.", "once",
          formula([("No reply in a week? ", INK), ("One short nudge.", TEAL)]),
          "Reply in the same thread so the context is there. Then move on.",
          "Sending 4 follow-ups.", 84)],
        "Cold email", [
            ("Subject with a connection", "gets it opened"),
            ("4 sentences", "one phone screen"),
            ("Ask for 15 minutes", "not a referral"),
            ("One follow-up", "same thread")],
        "Short, specific, one small ask.",
        ["A connection in the subject.",
         "4 sentences.",
         "One follow-up, then move on."])


# ------------------------------------------------------------- Wed 25 Nov
@deck
def n2_19_merger_model():
    return build(
        "n2-19-merger-model", TECH, "red",
        "Walk me through a merger model.",
        ["Price", "Funding", "Pro forma EPS"],
        "5 steps. Get them in order and the follow-ups get easier.",
        "It answers one question",
        "Does the buyer's <t>EPS</t> go up or down after the deal?",
        [("Set the price.", "price",
          steps(["Target share price", "Plus a premium", "Times diluted shares"]),
          "The offer price times the target's diluted shares is the equity purchase price.",
          "Using basic shares for the target.", 84),
         ("Decide how it is paid.", "paid",
          ladder([("Cash", "forgone interest", INK), ("New debt", "new interest", RED),
                  ("New stock", "more shares", TEAL)]),
          "Each source has a cost: lost interest on cash, new interest on debt, or new "
          "shares.",
          "Treating cash on hand as free.", 84),
         ("Combine the income statements.", "Combine",
          steps(["Buyer net income + target net income",
                 "Plus synergies, after tax",
                 "Less funding costs and new D&amp;A, after tax"]),
          "Write-ups from the purchase price allocation add depreciation and amortisation.",
          "Adding synergies before tax.", 74),
         ("Compare EPS.", "EPS",
          formula([("Pro forma net income / new share count ", INK), ("vs standalone EPS", TEAL)]),
          "Higher is accretive, lower is dilutive. Then say what it means for value.",
          "Stopping at accretive.", 74)],
        "Merger model", [
            ("Price", "premium on diluted shares"),
            ("Funding", "cash, debt, stock"),
            ("Combine", "plus synergies, less costs"),
            ("EPS", "accretive or dilutive")],
        "Price, fund, combine, compare.",
        ["Diluted shares for the target.",
         "Every funding source has a cost.",
         "Everything after tax."])


@deck
def n2_20_covenants():
    return build(
        "n2-20-covenants", TECH, "ink",
        "Maintenance or incurrence covenant?",
        ["Bank loans", "Bonds", "Tests"],
        "Leveraged finance asks it. Most candidates know one of the two.",
        "Both protect lenders",
        "The difference is <t>when</t> the test is run.",
        [("Maintenance: tested every period.", "every period",
          formula([("e.g. Debt / EBITDA ", INK), ("at most 4.0 times", TEAL)]),
          "The ratio must hold every test date, often each quarter, whatever the company "
          "does. Common in bank loans.",
          "Thinking it only applies when borrowing more.", 80),
         ("Incurrence: tested on action.", "on action",
          ladder([("Raising new debt", "test runs", TEAL),
                  ("Paying a dividend", "test runs", TEAL),
                  ("Doing nothing", "no test", INK)]),
          "The company is only tested when it wants to take an action. Common in high-yield "
          "bonds.",
          "Saying a falling EBITDA alone breaches it.", 80),
         ("What happens on a breach?", "breach",
          steps(["Technical default", "Waiver or amendment", "Usually a fee or higher rate"]),
          "Lenders rarely want the keys. They usually negotiate, at a price.",
          "Assuming a breach means bankruptcy.", 84),
         ("And covenant-lite?", "covenant-lite",
          formula([("No maintenance tests, ", INK), ("incurrence only.", TEAL)]),
          "A covenant-lite loan behaves more like a bond for the borrower.",
          "Thinking it means no covenants at all.", 84)],
        "Covenants", [
            ("Maintenance", "tested every period"),
            ("Incurrence", "tested when the company acts"),
            ("Breach", "waiver, amendment, fee"),
            ("Covenant-lite", "no maintenance tests")],
        "When the test runs is the answer.",
        ["Maintenance: every period.",
         "Incurrence: on an action.",
         "Breach usually means a negotiation."])


@deck
def n2_21_thank_you():
    return build(
        "n2-21-thank-you", REC, "paper",
        "What goes in an interview thank-you note?",
        ["Fast", "Specific", "Short"],
        "Most are generic. A specific one gets remembered.",
        "It is your last impression",
        "One <t>specific detail</t> from the conversation does more than three paragraphs.",
        [("Send it the same day.", "same day",
          formula([("Within 24 hours, ", INK), ("while they remember you.", TEAL)]),
          "Email is fine. Speed matters more than format.",
          "Waiting until the weekend.", 84),
         ("One email per interviewer.", "per interviewer",
          ladder([("Group email", "generic", RED), ("One each, personalised", "remembered", TEAL)]),
          "Each note should mention something only that person said.",
          "Copy-pasting the same note to everyone.", 84),
         ("Use this shape.", "shape",
          steps(["Thank them for their time", "One detail you discussed",
                 "Why it confirmed your interest"]),
          "3 sentences is enough. They read it on a phone.",
          "Re-pitching your whole story.", 84),
         ("Check it twice.", "twice",
          formula([("Right name, right bank, ", INK), ("no typos.", TEAL)]),
          "A wrong name in a thank-you note undoes the interview.",
          "Sending it from a template with the last bank's name.", 84)],
        "Thank-you note", [
            ("Same day", "within 24 hours"),
            ("One per interviewer", "personalised"),
            ("Thanks, detail, interest", "3 sentences"),
            ("Check names", "and the bank")],
        "Fast, specific, short.",
        ["Send it the same day.",
         "One detail per person.",
         "Proofread the names."])


# ===========================================================================
if __name__ == "__main__":
    for slug in (sys.argv[1:] or list(DECKS)):
        d = DECKS[slug]()
        paths = d.render()
        problems = check(paths, d.total)
        print(f"{slug}: {len(paths)} slides, "
              f"{sum(p.stat().st_size for p in paths) // 1024}KB, problems: {problems or 'none'}")
