"""
The week's six remaining carousels.

Technicals checked before writing:

DCF      UFCF = EBIT(1-t) + D&A - capex - change in NWC. Discounted at WACC
         because it is the cash available to every capital provider. Gordon
         growth terminal value = FCF_n(1+g)/(WACC-g), g below long-run GDP.
WACC     E/(D+E)*Re + D/(D+E)*Rd*(1-t). Cost of debt is after tax because
         interest is deductible; there is no equivalent shield on dividends.
         Re from CAPM = rf + beta * ERP. Weights at market value, not book.
CASH     Profit is accrual, cash is not. Growth consumes working capital when
         you pay suppliers before customers pay you.
LBO      Entry, operate and deleverage, exit. Returns come from EBITDA growth,
         debt paydown and multiple expansion, in that order of reliability.
FCF      Unlevered to WACC gives enterprise value; levered to cost of equity
         gives equity value. Crossing them is the classic error.
RANGE    Precedents usually print above comps because a control premium and
         expected synergies are inside the price paid.
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


# ============================================================ C2  DCF
@deck("w1-02-dcf")
def dcf():
    d = Deck("w1-02-dcf", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "Walk me<br>through a DCF.",
        ["Project", "Discount", "Terminal value", "Bridge"],
        "Six steps. Most people fumble the fifth one."))
    d.slide(INK, WHITE, inner=stake(
        "Everyone knows it values future cash",
        'Almost nobody can say <span style="color:#5EC8B4">which</span> cash, '
        'or why it gets discounted at that particular rate.'))

    d.qa("The six steps, in order.", "six steps",
         steps(["Project UFCF", "Pick WACC", "Discount", "Terminal value",
                "Discount TV", "Bridge to equity"]),
         "Project unlevered free cash flow, discount it at WACC, add the discounted terminal "
         "value, then bridge from enterprise value to equity.",
         "Starting with the formula instead of the shape. Give the six steps first.", 76)

    d.qa("Which cash flow, and why unlevered.", "unlevered",
         formula([("EBIT(1 &minus; t)", INK), (" + D&amp;A ", MUTE), ("&minus; capex ", INK),
                  ("&minus; &Delta;NWC", TEAL)]),
         "Unlevered free cash flow is before interest, so it belongs to debt and equity "
         "together. That is why you discount it at WACC.",
         "Using levered cash flow with WACC. Levered cash flow goes to the cost of equity.", 68)

    d.qa("Terminal value is most of your answer.", "most",
         bars([("Y1", 46, TEAL), ("Y2", 60, TEAL), ("Y3", 74, TEAL), ("Y4", 88, TEAL),
               ("Y5", 102, TEAL), ("Terminal<br>value", 190, RED)],
              "typically 60 to 80 per cent of enterprise value"),
         "Gordon growth takes the final year, grows it at g, and divides by WACC minus g. "
         "Keep g below long-run GDP growth or the business outgrows the economy.",
         "Quoting a terminal growth rate of 5 per cent and not noticing what it implies.", 68)

    d.qa("Then bridge to a share price.", "bridge",
         ladder([("Enterprise value", "sum of discounted cash", INK),
                 ("Less net debt", "&minus;", RED),
                 ("Less preferred, NCI", "&minus;", RED)],
                "Equity value &divide; diluted shares", "price", TEAL),
         "A DCF produces enterprise value. The share price is three subtractions and a "
         "division away, and interviewers ask for the share price.",
         "Stopping at enterprise value and calling it the answer.", 70)

    d.qa("Say what would break it.", "break it",
         ladder([("WACC moves 1%", "value moves a lot", RED),
                 ("Terminal growth moves 0.5%", "value moves a lot", RED),
                 ("Year 4 revenue moves 5%", "value barely moves", TEAL)]),
         "The answer is dominated by two inputs you cannot observe. Naming that is what "
         "separates a candidate who has built one from a candidate who has read about one.",
         "Calling the DCF the most accurate method. It is the most assumption-heavy.", 70)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("The whole thing", [
        ("Project unlevered free cash flow", "step 1"),
        ("Discount it at WACC", "steps 2 and 3"),
        ("Add discounted terminal value", "steps 4 and 5"),
        ("Bridge to equity, divide by shares", "step 6"),
        ("Name the two inputs that drive it", "the part people skip")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Unlevered to WACC. Always.",
        ["Unlevered cash flow goes with WACC.",
         "Levered cash flow goes with cost of equity.",
         "Terminal value is most of the answer."],
        "Tomorrow: where that WACC actually comes from."))
    return d


# ============================================================ C3  WACC
@deck("w1-03-wacc")
def wacc():
    d = Deck("w1-03-wacc", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "Where does<br>WACC come from?",
        ["Cost of equity", "Cost of debt", "Market weights", "Beta"],
        "You used it in the DCF. Now justify every term."))
    d.slide(INK, WHITE, inner=stake(
        "It is one line in the model",
        'and it moves the answer more than any revenue assumption you will '
        '<span style="color:#5EC8B4">argue about for a week</span>.'))

    d.qa("The formula, and what each weight means.", "weights",
         formula([("E/(D+E) &times; R", INK), ("<sub>e</sub>", INK), ("  +  ", MUTE),
                  ("D/(D+E) &times; R", INK), ("<sub>d</sub>", INK),
                  (" &times; (1 &minus; t)", TEAL)]),
         "A blend of what equity holders demand and what lenders charge, weighted by how much "
         "of the capital structure each one funds.",
         "Weighting by book value. Use market value of equity, which is the market cap.", 66)

    d.qa("Why the cost of debt is after tax.", "after tax",
         ladder([("Interest expense", "100", INK),
                 ("Tax saved at 25%", "25", TEAL)],
                "Real cost to the company", "75", TEAL),
         "Interest is deductible, so the government pays part of it. Dividends are not "
         "deductible, which is why there is no equivalent adjustment on the equity side.",
         "Applying the same after-tax haircut to the cost of equity.", 70)

    d.qa("Cost of equity comes from CAPM.", "CAPM",
         formula([("R", INK), ("<sub>f</sub>", INK), ("  +  &beta; &times;  ", MUTE),
                  ("equity risk premium", TEAL)]),
         "The risk-free rate plus beta times the premium investors demand for holding "
         "equities rather than government bonds.",
         "Reciting CAPM without being able to say where beta came from.", 72)

    d.qa("Beta has to be unlevered first.", "unlevered",
         steps(["Take comps' betas", "Strip out their debt", "Average",
                "Re-lever at target structure"]),
         "A comparable company's beta carries its own leverage. Strip that out, average the "
         "business risk, then re-lever at the capital structure you are modelling.",
         "Pulling one beta off a screen and using it unchanged.", 66)

    d.qa("Use the yield, not the coupon.", "yield",
         ladder([("Coupon on old bonds", "4.0%", RED),
                 ("Current yield to maturity", "6.5%", TEAL)],
                "What new borrowing costs", "6.5%", TEAL),
         "WACC is forward-looking. What matters is what the company would pay to borrow "
         "today, not what it agreed to years ago.",
         "Reading the coupon off the debt schedule and calling it the cost of debt.", 72)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("Every term, justified", [
        ("Weights at market value, not book", "the most common slip"),
        ("Cost of debt after tax", "interest is deductible"),
        ("Cost of equity from CAPM", "risk free plus beta times ERP"),
        ("Beta unlevered, averaged, re-levered", "three steps, not one"),
        ("Current yield, not the old coupon", "WACC looks forward")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Market weights. After tax. Forward.",
        ["Market value of equity, not book value.",
         "Debt after tax, equity not.",
         "Today's yield, not yesterday's coupon."],
        "Tomorrow: how a profitable company runs out of cash."))
    return d


# ============================================================ C4  cash
@deck("w1-04-cash")
def cash():
    d = Deck("w1-04-cash", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "How does a profitable company run out of cash?",
        ["Receivables", "Inventory", "Capex", "Debt due"],
        "Four real answers. One of them is not bad management."))
    d.slide(INK, WHITE, inner=stake(
        "Profit is an opinion",
        'Cash is a fact. This question is checking whether you know '
        '<span style="color:#5EC8B4">the difference</span>.'))

    d.qa("Profit and cash can move in opposite directions.", "opposite",
         '<div class="card"><svg viewBox="0 0 880 250" style="width:100%;height:220px">'
         f'<line x1="30" y1="225" x2="855" y2="225" stroke="{INK}" stroke-width="3"/>'
         f'<polyline points="55,175 250,152 450,128 650,105 840,82" fill="none" '
         f'stroke="{TEAL}" stroke-width="7"/>'
         f'<polyline points="55,60 250,92 450,135 650,180 840,212" fill="none" '
         f'stroke="{RED}" stroke-width="7"/>'
         f'<text x="55" y="42" font-family="Sans" font-size="29" font-weight="600" '
         f'fill="{RED}">CASH</text>'
         f'<text x="690" y="62" font-family="Sans" font-size="29" font-weight="600" '
         f'fill="{TEAL}">PROFIT</text></svg></div>',
         "Revenue is booked when it is earned, not when it is collected. A fast-growing "
         "company books profit it has not yet been paid.",
         "Treating net income as if it were a bank balance.", 62)

    d.qa("Growth itself consumes cash.", "consumes",
         ladder([("You buy inventory", "cash out", RED),
                 ("You pay staff and suppliers", "cash out", RED),
                 ("You ship and book revenue", "profit up", TEAL),
                 ("Customer pays, 60 days later", "cash in", TEAL)],
                "The gap you have to fund", "60 days", RED),
         "Every extra unit of growth ties up more cash in receivables and inventory before "
         "any of it comes back.",
         "Saying the company grew too fast without naming the line that absorbed the cash.", 68)

    d.qa("Then the three that are not working capital.", "three",
         steps(["Heavy capex", "Debt coming due", "One-off legal or restructuring"]),
         "Spending below the operating line still drains the account. A maturity wall can "
         "empty a profitable company in a single quarter.",
         "Stopping after working capital when the interviewer wanted more than one.", 68)

    d.qa("Which statement would show it first?", "which statement",
         ladder([("Income statement", "looks fine", RED),
                 ("Balance sheet", "receivables ballooning", TEAL),
                 ("Cash flow statement", "operating cash negative", TEAL)]),
         "The income statement is the last place this shows up. Operating cash flow falling "
         "while net income rises is the signal.",
         "Not being able to say where you would look. That is the real question.", 66)

    d.qa("The sentence that ends the answer well.", "sentence",
         formula([("Profit is accrual. ", INK), ("Cash is not.", TEAL)]),
         "Name the mechanism, name the line item, name the statement you would check. Three "
         "sentences and you are finished.",
         "Answering &ldquo;bad management&rdquo;, which names nothing and ends the question.", 68)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("Four mechanisms", [
        ("Receivables and inventory build", "working capital"),
        ("Capex outruns operating cash", "below the line"),
        ("Debt matures", "the maturity wall"),
        ("One-off legal or restructuring", "non-operating"),
        ("Check operating cash flow first", "where it shows")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Name the line, not the vibe.",
        ["Profit is accrual, cash is not.",
         "Growth absorbs working capital.",
         "Operating cash flow shows it first."],
        "Tomorrow: an LBO in five steps."))
    return d


# ============================================================ C5  LBO
@deck("w1-05-lbo")
def lbo():
    d = Deck("w1-05-lbo", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "Walk me through an LBO.",
        ["Entry", "Deleverage", "Exit", "IRR"],
        "Five steps. The debt is the whole point, not a detail."))
    d.slide(INK, WHITE, inner=stake(
        "You are buying a company with its own cash flow",
        'Everything in the model follows from that '
        '<span style="color:#5EC8B4">one sentence</span>.'))

    d.qa("The five steps.", "five steps",
         steps(["Sources and uses", "Project cash flow", "Pay down debt",
                "Exit at a multiple", "Compute IRR"]),
         "Buy at a multiple of EBITDA using mostly debt, use the company's cash to repay that "
         "debt, sell in about five years, and measure what the equity returned.",
         "Describing it as buying with debt and stopping there.", 76)

    d.qa("Why use debt at all?", "debt",
         ladder([("Same business, same exit", "", MUTE),
                 ("All equity: 2.0x your money", "2.0x", MUTE),
                 ("With leverage: higher", "amplified", TEAL)],
                "Equity is a thinner slice of a bigger number", "", TEAL),
         "Debt shrinks the equity cheque, so the same gain in enterprise value is spread over "
         "less equity. Interest is deductible, and repayment imposes discipline.",
         "Saying leverage boosts returns without saying it also multiplies the downside.", 70)

    d.qa("Where the returns actually come from.", "returns",
         bars([("Debt<br>paydown", 120, TEAL), ("EBITDA<br>growth", 150, TEAL),
               ("Multiple<br>expansion", 70, RED)],
              "the third one is a hope, not a plan"),
         "Repaying debt and growing EBITDA are things the sponsor can influence. Selling at a "
         "higher multiple than you paid is a market call.",
         "Building the case on multiple expansion. Assume you exit at the entry multiple.", 68)

    d.qa("What makes a good LBO candidate?", "good",
         ladder([("Steady, predictable cash flow", "essential", TEAL),
                 ("Low existing debt", "room to lever", TEAL),
                 ("Low capex needs", "cash goes to debt", TEAL),
                 ("Cyclical or capex-heavy", "poor fit", RED)]),
         "The business has to service debt through a downturn. Predictability matters more "
         "than growth rate.",
         "Naming a fast-growing software startup. It burns cash and cannot carry debt.", 66)

    d.qa("Finish with the number they asked for.", "number",
         formula([("MoM = ", INK), ("exit equity", TEAL), (" &divide; ", MUTE),
                  ("entry equity", INK)]),
         "Exit enterprise value minus remaining net debt gives exit equity. Divide by what you "
         "put in for money-on-money, then annualise it for IRR.",
         "Quoting IRR without being able to turn it into a money-on-money multiple.", 68)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("The five steps", [
        ("Sources and uses at entry", "step 1"),
        ("Project free cash flow", "step 2"),
        ("Sweep it against the debt", "step 3"),
        ("Exit on EBITDA times a multiple", "step 4"),
        ("Exit equity over entry equity", "step 5")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Exit at the entry multiple.",
        ["Debt paydown and EBITDA growth are the plan.",
         "Multiple expansion is a hope.",
         "Predictable cash beats fast growth."],
        "Tomorrow: the four kinds of free cash flow."))
    return d


# ============================================================ C6  FCF
@deck("w1-06-fcf")
def fcf():
    d = Deck("w1-06-fcf", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "Four kinds of free cash flow.",
        ["Unlevered", "Levered", "CFO less capex", "EBITDA"],
        "Mix two of them up and your whole valuation is wrong."))
    d.slide(INK, WHITE, inner=stake(
        "Candidates say cash flow as if it meant one thing",
        'It means four, and each one gets discounted at a '
        '<span style="color:#5EC8B4">different rate</span>.'))

    d.qa("Unlevered. Before interest.", "Unlevered",
         formula([("EBIT(1 &minus; t) + D&amp;A &minus; capex &minus; &Delta;NWC", INK)]),
         "Available to every capital provider. Discount at WACC and you get enterprise value.",
         "Subtracting interest. Unlevered means before any lender is paid.", 76)

    d.qa("Levered. After the lenders.", "Levered",
         formula([("Net income + D&amp;A &minus; capex &minus; &Delta;NWC ", INK),
                  ("&minus; mandatory repayment", TEAL)]),
         "What is left for shareholders. Discount at the cost of equity and you get equity "
         "value directly, with no bridge.",
         "Discounting levered cash flow at WACC. That double-counts the capital structure.", 70)

    d.qa("The pairing that cannot be broken.", "pairing",
         ladder([("Unlevered FCF", "WACC &rarr; enterprise value", TEAL),
                 ("Levered FCF", "cost of equity &rarr; equity value", TEAL),
                 ("Unlevered FCF at cost of equity", "wrong", RED),
                 ("Levered FCF at WACC", "wrong", RED)]),
         "Match the cash flow to the people who have a claim on it, and the discount rate to "
         "the same people.",
         "Knowing both formulas and still pairing them the wrong way round.", 68)

    d.qa("The practical one, and its limit.", "practical",
         formula([("Operating cash flow ", INK), ("&minus; capex", TEAL)]),
         "The quick version you can read straight off the cash flow statement. It is levered, "
         "because operating cash flow is already after interest paid.",
         "Treating it as unlevered and feeding it into a DCF discounted at WACC.", 70)

    d.qa("And EBITDA is not cash flow.", "not cash flow",
         ladder([("Ignores capex", "", RED), ("Ignores working capital", "", RED),
                 ("Ignores cash taxes", "", RED), ("Ignores interest", "", RED)]),
         "It is a proxy for operating profitability before capital structure. Useful for "
         "multiples, not a measure of cash.",
         "Calling EBITDA a cash flow proxy without naming what it leaves out.", 68)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("Four, kept apart", [
        ("Unlevered goes with WACC", "enterprise value"),
        ("Levered goes with cost of equity", "equity value"),
        ("Operating cash flow less capex", "quick, and levered"),
        ("EBITDA is not cash flow", "four omissions"),
        ("Match the claim to the rate", "the whole rule")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Match the claim to the rate.",
        ["Unlevered to WACC, enterprise value.",
         "Levered to cost of equity, equity value.",
         "EBITDA is profitability, not cash."],
        "Tomorrow: which method prints the highest value."))
    return d


# ============================================================ C7  range
@deck("w1-07-range")
def value_range():
    d = Deck("w1-07-range", "Technical of the Day", 9)
    d.slide(RED, WHITE, accent=WHITE, inner=cover(
        "Which method gives the highest value?",
        ["Comps", "Precedents", "DCF", "LBO floor"],
        "There is a usual order, and a reason for it."))
    d.slide(INK, WHITE, inner=stake(
        "They are not asking you to rank methods",
        'They are asking whether you know what is '
        '<span style="color:#5EC8B4">inside each price</span>.'))

    d.qa("The usual order.", "usual order",
         bars([("Comps", 105, MUTE), ("Precedents", 165, TEAL),
               ("DCF", 140, RED), ("LBO", 80, MUTE)],
              "typical, not guaranteed"),
         "Precedent transactions usually print highest and an LBO lowest. Comps sit below "
         "precedents, and the DCF ranges widest of all.",
         "Stating the order as a law. Say typically, then explain why.", 64)

    d.qa("Why precedents sit above comps.", "above",
         ladder([("What a share trades at", "comps", MUTE),
                 ("Plus control premium", "+", TEAL),
                 ("Plus expected synergies", "+", TEAL)],
                "What an acquirer actually paid", "precedents", TEAL),
         "Comps price a minority stake in the open market. A precedent is what someone paid to "
         "own the whole thing and run it.",
         "Saying precedents are higher without naming the control premium.", 66)

    d.qa("Why the DCF ranges widest.", "widest",
         ladder([("WACC", "unobservable", RED),
                 ("Terminal growth", "unobservable", RED),
                 ("Year 5 margin", "a guess", RED)]),
         "Three inputs nobody can check move the answer more than anything you can observe. "
         "That is why it ranges, and why it is not the most accurate method.",
         "Calling the DCF most accurate. It is the most assumption-heavy.", 66)

    d.qa("Why the LBO sets the floor.", "floor",
         formula([("What a sponsor can pay ", INK),
                  ("and still hit its return", TEAL)]),
         "A financial buyer needs a target return, so the price is capped. A strategic buyer "
         "with synergies can pay more, which is why the floor sits below the rest.",
         "Describing the LBO as a valuation rather than a maximum price.", 64)

    d.qa("Then say what you would actually use.", "actually",
         ladder([("Public company, liquid comps", "comps anchor", TEAL),
                 ("Live sale process", "precedents anchor", TEAL),
                 ("Stable, forecastable business", "DCF carries weight", TEAL)]),
         "The right answer depends on the situation, and saying so is the answer. Nobody picks "
         "one method and ignores the rest.",
         "Picking a favourite method instead of describing the football field.", 62)

    d.slide(INK, WHITE, cue="Save", icon=BOOKMARK, inner=recap("The football field", [
        ("Precedents usually highest", "control premium and synergies"),
        ("Comps below them", "minority stake, open market"),
        ("DCF ranges widest", "three unobservable inputs"),
        ("LBO sets the floor", "a sponsor's maximum"),
        ("Say typically, then say why", "the whole answer")]))

    d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=cta(
        "Say typically. Then say why.",
        ["Precedents carry a control premium.",
         "Comps price a minority stake.",
         "The DCF is assumption-heavy, not accurate."],
        "Two of these every day."))
    return d


# ===========================================================================
if __name__ == "__main__":
    for slug in (sys.argv[1:] or list(DECKS)):
        d = DECKS[slug]()
        paths = d.render()
        problems = check(paths, 9)
        print(f"{slug}: {len(paths)} slides, "
              f"{sum(p.stat().st_size for p in paths) // 1024}KB total, "
              f"problems: {problems or 'none'}")
