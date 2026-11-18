"""
YouTube #12 (18 Nov 2026): Long-Term Capital Management, 1998. A hedge fund run in part by two Nobel laureates loses
$1.8 billion in August 1998, more than half its capital since January; three weeks later fourteen banks and
securities firms, called together by the Federal Reserve Bank of New York, put in about $3.6 billion to stop it
collapsing. Why would Wall Street rescue a rival, and how do you lose half your money in a month on trades designed to
profit from tiny price gaps? Financial history, hedge funds, leverage, banking crises. Made to
docs/production/long-form-standard.md (visual plan: build/plans/ep012.md). Score: suspense.

Point of view (our reading, labelled as ours): leverage doesn't change whether a trade is right, it changes how long
you can afford to be wrong; the banks were less rescuing a rival than avoiding a fire sale of what they owned too.
Educational, not advice.

Every claim, sourced (only pages opened or returned by a search in this run):
  [PWG] President's Working Group on Financial Markets, "Hedge Funds, Leverage, and the Lessons of Long-Term Capital
      Management", April 1999 (CFTC copy): equity capital $4.8bn at 1 Jan 1998, after returning "approximately $2.7
      billion in capital to its investors" at year-end 1997; total assets $129bn at end-1997; balance-sheet leverage
      28-to-1 at end-1997; balance sheet over $125bn on 31 Aug 1998, "a balance-sheet leverage ratio of more than
      25-to-1" on the $4.8bn; end-August 1998 derivatives notional: exchange futures more than $500bn, swaps more than
      $750bn, options and other OTC more than $150bn; capital $4.1bn on 31 July ("down about fifteen percent"),
      August losses $1.8bn, capital $2.3bn at end-August; over 60,000 trades; some futures positions above 5% of open
      interest, "in a few cases well above ten percent"; top 17 counterparties' potential losses "between $3 billion
      and $5 billion in aggregate" (LTCM's estimate); Russia's devaluation and debt moratorium of 17 August; "flight
      to quality"; 14 firms invested "about $3.6 billion in new equity", "a 90 percent equity stake", operational
      control, the original owners written down to 10 percent; "LTCM appears to have received very generous credit
      terms, even though it took an exceptional degree of risk."; at year-end 1998 the five largest investment banks'
      "average leverage ratio was 27-to-1".
  [MCD] William J. McDonough, President, Federal Reserve Bank of New York, statement before the House Committee on
      Banking and Financial Services, 1 October 1998: partnership started 1994, available only to wealthy investors;
      "complex mathematical formulas to identify temporary price discrepancies"; e.g. buy corporate bonds and sell
      short Treasuries; equity positions through swaps and options; 17 Aug Russia devaluation and moratorium; "As
      markets around the world moved in the same direction at the same time, the diversification on which Long-Term
      had previously relied failed them utterly."; 2 Sept letter (52% losses through 31 Aug, seeking capital);
      Fri 18 Sept capital raising unsuccessful; Sun 20 Sept NY Fed team (Peter Fisher) with Treasury (Gary Gensler)
      at the fund's offices: "the size of these positions was much greater than market participants imagined";
      Tue 22 Sept, Goldman Sachs, Merrill Lynch, J.P. Morgan, later UBS; 7:00 p.m. four firms reviewed a draft term
      sheet, Fed officials present but not in the discussion of terms; about 8:30 p.m. a wider group of 13 firms;
      14 firms participated, two declined; "Not one penny of public money was spent or committed."; "the abrupt and
      disorderly close-out of Long-Term Capital's positions would pose unacceptable risks to the American economy."
  [FRH] Federal Reserve History, "Near Failure of Long-Term Capital Management": founded February 1994 by John
      Meriwether, former Salomon Brothers vice chairman; two Nobel laureates; returns 1994 20%, 1995 43%, 1996 41%,
      1997 17%; about $30 of debt per $1 of capital at end-1997; capital returned at end-1997 without shrinking
      positions; 44% lost in August; 23 Sept morning, a Warren Buffett-led offer of $250m for the partners plus $3.75bn
      of capital, not accepted by the 12:30 p.m. deadline (reported legal issues); agreement about 6:00 p.m.; $3.6bn
      ($3.625bn), 14 firms, 90%; no Fed funds; the last of the $3.6bn returned by the end of 1999.
  [GRN] Alan Greenspan, testimony before the House Committee on Banking and Financial Services, 1 October 1998: "a
      fire sale may be sufficiently intense and widespread that it seriously distorts markets and elevates uncertainty
      enough to impair the overall functioning of the economy."; "any time that there is public involvement that
      softens the blow of private-sector losses ... the issue of moral hazard arises."
  [MAC] Donald MacKenzie, An Engine, Not a Camera (MIT Press, 2006), ch. 8 "Arbitrage": LTCM "was run by, among
      others, Robert C. Merton and Myron Scholes"; investors pay a premium for on-the-run bonds; "short-selling newly
      issued bonds and buying their closest off-the-run counterparts"; yields "can be expected to converge"; the
      difference "was seldom much more than a tenth of a percentage point"; $550 million lost on 21 August 1998; the
      "superportfolio": "Sales by some holders ... moved prices against others, leading to a cascade of
      self-reinforcing adverse price movements."
  [NOB] Nobel Prize press release, 14 October 1997: Robert C. Merton and Myron S. Scholes, "for a new method to
      determine the value of derivatives".
  [FUR] Furfine and Remolona, "Price discovery in a market under stress: the U.S. Treasury market in fall 1998",
      Chicago Fed WP 2005-06: LTCM short on-the-run Treasuries and long swaps (background; no figure used).

Labelled as ours: the bond screens (two yields, no numbers: an illustration of the convergence trade); a tenth of a
percent of $1bn a year ($1m); at 25 to 1 a 4% fall wipes out the capital and a 1% fall takes a quarter; the balance
sheet drawn at 100 / 96; the filmed rooms (reconstructions, not LTCM's office or the New York Fed's room; nobody is a
portrait; nobody speaks); the readings in the last two chapters.
Calculations (build/plans/ep012_checks.py): 4.1 - 1.8 = 2.3; 1.8 / 4.1 = 44%; 1 - 2.3 / 4.8 = 52% ("more than
half"); 2 to 23 Sept = 21 days ("three weeks"); 0.1% of $1bn = $1m; 1 / 25 = 4%; 25 x 1% = 25%; 125 / 4.8 = 26 (more
than 25 to 1); 90 + 10 = 100.

    python build/youtube_ep012.py
"""

import cine_1998 as F
from cine_lib import document_shot
from youtube import make

S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)
SS = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: SC(art, txt, **opts)      # the drawing alone, its line as the heading
CINE = lambda name: dict(kind="cine", shot=F.SHOTS[name])
DOC = lambda **kw: dict(kind="cine", shot=document_shot(**kw))

EP = dict(
    slug="yt-012-ltcm",
    title="Two Nobel Winners Ran This Fund. It Lost Half Its Money in a Month.",
    score="suspense",
    fx="action",
    held_life=True,
    text_life=True,
    thumb=dict(film_a=dict(shot=F.SHOTS["capital_hook"], dur=12.0, t=10.5, pos="78% 22%",
                           segs=[("On the second of September, nineteen ninety eight, a hedge fund wrote to its investors.", .3, 4.6),
                                 ("In August alone, it had lost one point eight billion dollars.", 4.8, 8.4)]),
               film_b=dict(shot=F.SHOTS["fed_deal"], dur=12.0, t=11.0, pos="50% 45%",
                           segs=[("At around six that evening, fourteen banks and securities firms agreed to put in about three point six billion dollars of new equity.", .3, 6.0),
                                 ("In return they got ninety percent of the fund, and control of it.", 6.2, 9.6)]),
               big_a="Two Nobel winners. Half the money gone in <span style='color:#D93A12'>a month</span>.", size_a=80,
               big="Wall Street paid <span style='color:#D93A12'>$3.6bn</span> to save a rival.", size=84,
               small="September 1998"),
    chapters=[
        dict(title="Half in a month", art=("bars", dict(values=[4.8, 2.3], labels=["JAN", "AUG"], hi=1)), beats=[
            dict(say="On the second of September, nineteen ninety eight, a hedge fund wrote to its investors. In August alone, it had lost one point eight billion dollars. Since January, more than half its capital was gone.",
                 show=CINE("capital_hook")),
            dict(say="Among the people who ran it were Robert Merton and Myron Scholes. They'd won the Nobel prize in economics the year before, for a new way to value derivatives.",
                 shows=[S("book", "Two Nobel laureates.", "Economics, 1997", ["Nobel"], 100, title="1997"),
                        SS("document", "A new way to value derivatives.", "Nobel Prize press release, 1997", ["value"], 96, flip=True, title="NOBEL 1997", lines=3, stamp="DERIVATIVES")]),
            dict(say="Three weeks after that letter, fourteen banks and securities firms put in about three point six billion dollars to stop it collapsing. They'd been called together by the Federal Reserve Bank of New York.",
                 shows=[
                        dict(kind="number", value=3.6, dec=1, pre="$", suf="bn", label="of new equity, September 23, 1998 · Federal Reserve History"),
                        S("bank", "Called together by the New York Fed.", "September 1998", ["New"], 96, flip=True, label="NEW YORK FED")]),
            dict(say="Why would Wall Street rescue a rival? And how do some of the best minds in finance lose half their money in a month, on trades designed to profit from tiny price gaps?",
                 shows=[S("handshake", "Why rescue a rival?", "", ["rival?"], 110, left="BANKS", right="FUND"),
                        SC("seesaw", "Half the money, in a month, on tiny gaps", left="TINY GAPS", right="HALF GONE", tip=1)]),
        ]),
        dict(title="The fund", art=("tower", dict(floors=6, label="LTCM")), beats=[
            dict(say="The fund was Long-Term Capital Management. John Meriwether, a former vice chairman of Salomon Brothers, started it in February nineteen ninety four. It was open only to wealthy investors.",
                 shows=[S("tower", "Long-Term Capital Management.", "Founded February 1994", ["Long-Term"], 92, floors=6, label="LTCM"),
                        SS("calendar", "February 1994.", "Federal Reserve History", ["February"], 100, flip=True, day="1994", month="FEB", note="FOUNDED"),
                        S("bricks", "Only for the wealthy.", "McDonough, 1998", ["wealthy."], 100, n=31, red=3)]),
            dict(say="Its returns were remarkable. Twenty percent in its first year, then forty three percent, then forty one, then seventeen percent in nineteen ninety seven.",
                 shows=[SC("bars", "Return each year, % (Federal Reserve History)", values=[20, 43, 41, 17], labels=["1994", "1995", "1996", "1997"], hi=1),
                        S("rocket", "Remarkable.", "", ["Remarkable."], 120)]),
            dict(say="At the end of nineteen ninety seven, it gave about two point seven billion dollars back to its investors. But it didn't shrink its positions. So the same bets now sat on less money: four point eight billion dollars of capital.",
                 shows=[S("coins", "About $2.7bn given back.", "End of 1997 · PWG, 1999", ["back"], 100, stacks=[6, 4, 2]),
                        SS("tower", "Same bets, less money.", "Federal Reserve History", ["less"], 100, flip=True, floors=8, label="SAME SIZE"),
                        dict(kind="compare", left=("Given back, end 1997", "$2.7bn"), right=("Capital, January 1998", "$4.8bn"), note="President's Working Group, 1999")]),
        ]),
        dict(title="A tenth of a percent", art=("seesaw", dict(left="NEW", right="OLD", tip=0)), beats=[
            dict(say="Here's one kind of trade it made, as the sociologist Donald MacKenzie describes it. Take two US Treasury bonds that are almost the same: a new one, and one issued a little earlier. Investors pay extra for the newest, because it's the easiest to trade. So it yields a little less.",
                 show=CINE("gap_close")),
            dict(say="The difference was seldom much more than a tenth of a percentage point. The fund would sell the new bond short and buy the older one. As the new bond aged, the two yields could be expected to come together, and the gap would pay.",
                 shows=[dict(kind="number", value=0.1, start=0.1, dec=1, suf="%", label="the gap, seldom much more · MacKenzie, 2006"),
                        S("two_ways", "Sell the new, buy the old.", "MacKenzie, 2006", ["Sell"], 96, left=("NEW BOND", "SELL"), right=("OLDER BOND", "BUY")),
                        SS("handshake", "The yields come together.", "Our illustration", ["together,"], 100, flip=True, left="NEW", right="OLD")]),
            dict(say="That's tiny. On a billion dollars of bonds, a tenth of a percent is about a million dollars a year. To make it worth doing, you have to do it in enormous size, with borrowed money.",
                 shows=[S("magnifier", "Tiny.", "", ["Tiny."], 130, label="0.1%"),
                        dict(kind="compare", left=("Bonds", "$1bn"), right=("A tenth of a percent", "$1m"), note="A year, roughly · our arithmetic"),
                        SS("tower", "Enormous size, borrowed money.", "", ["borrowed"], 96, flip=True, floors=10, label="BORROWED")]),
            dict(say="It ran the same idea across many markets. It bought corporate bonds and sold Treasuries short, used interest rate swaps, and took big positions in stocks through derivatives.",
                 shows=[dict(kind="flow", title="The same idea, many markets (McDonough, 1998)", items=[("doc", "Corporate bonds vs Treasuries"), ("scales", "Interest rate swaps"), ("coin", "Stocks, via derivatives")]),
                        SS("globe", "Many markets, one idea.", "McDonough, 1998", ["one"], 100, flip=True)]),
        ]),
        dict(title="Twenty five to one", art=("bs_bars", dict(assets=100, liab=96, scale=3.2)), beats=[
            dict(say="At the end of nineteen ninety seven, the fund held about a hundred and twenty nine billion dollars of assets. The President's Working Group on Financial Markets later put its leverage at twenty eight to one.",
                 shows=[dict(kind="number", value=129, pre="$", suf="bn", label="of assets, end of 1997 · President's Working Group, 1999"),
                        S("seesaw", "Twenty eight to one.", "PWG, 1999", ["eight"], 100, flip=True, left="DEBT", right="CAPITAL", tip=0)]),
            dict(say="By the end of August, it still had more than a hundred and twenty five billion dollars of assets, on the four point eight billion of capital it started the year with. That's more than twenty five to one.",
                 shows=[SC("bars", "End of August 1998, $ billion (PWG, 1999)", values=[125, 4.8], labels=["ASSETS", "CAPITAL, JAN"], hi=1),
                        S("bricks", "More than 25 to 1.", "Our drawing: 1 red brick of capital", ["25"], 100, n=26, red=1, label="25 TO 1")]),
            dict(say="Here's what that means, in our own arithmetic. At twenty five to one, if the assets fall by just four percent, the whole of the capital is gone. A fall of one percent takes a quarter of it.",
                 shows=[SC("bs_bars", "Our arithmetic: 100 of assets, 96 borrowed, 4 of capital", assets=100, liab=96, scale=3.2),
                        dict(kind="number", value=4, suf="%", label="fall in assets that wipes out the capital, at 25 to 1 · our arithmetic"),
                        S("empty_pockets", "1% takes a quarter.", "Our arithmetic", ["quarter."], 100, flip=True, label="25%")]),
            dict(say="And that's only the balance sheet. At the end of August, its futures had a face value of more than five hundred billion dollars, its swaps more than seven hundred and fifty billion, and its options and other contracts more than a hundred and fifty billion. Face value isn't money at risk. But it shows the size of the footprint.",
                 shows=[S("scale", "Only the balance sheet.", "", ["balance"], 100, left="ASSETS", right="DEBT", tip=0),
                        SC("bars", "Derivatives, face value, end of August 1998, more than $ billion (PWG, 1999)", values=[500, 750, 150], labels=["FUTURES", "SWAPS", "OPTIONS, OTHER"], hi=1),
                        S("magnifier", "Not money at risk.", "Face value only", ["risk."], 100, label="FACE VALUE"),
                        SS("dominoes", "The size of the footprint.", "Our reading", ["footprint."], 96, flip=True, labels=["$500BN", "$750BN", "$150BN", ""], fall=0)]),
            dict(say="It had more than sixty thousand trades on its books. In a few futures markets, it held well above ten percent of all the open contracts. Selling that much in a hurry would move the price against it.",
                 shows=[S("ledger", "60,000 trades.", "PWG, 1999", ["60,000"], 110, names=("Trade 1", "Trade 2", "...", "Trade 60,000"), hi=(3,)),
                        SS("queue", "Over 10% of some markets.", "In a few futures markets · PWG, 1999", ["10%"], 96, flip=True, n=10, label="OPEN CONTRACTS"),
                        S("scale", "Selling would move the price.", "Our reading", ["move"], 96, left="SELL", right="PRICE", tip=1)]),
        ]),
        dict(title="August the seventeenth", art=("calendar", dict(day="17", month="AUG", note="1998")), beats=[
            dict(say="Then, on the seventeenth of August, nineteen ninety eight, Russia devalued its currency and declared a moratorium on its debt. Investors ran for whatever was safest and easiest to sell. The gaps the fund was betting would close got wider instead.",
                 show=CINE("gap_open")),
            dict(say="On the twenty first of August, it lost five hundred and fifty million dollars in a single day. Over the month it lost one point eight billion, and its capital fell from four point one billion at the end of July to two point three billion.",
                 shows=[dict(kind="number", value=550, pre="$", suf="m", label="lost on August 21, 1998 · MacKenzie, 2006"),
                        SC("bars", "Capital, 1998, $ billion (PWG, 1999)", values=[4.8, 4.1, 2.3], labels=["JAN 1", "JUL 31", "AUG 31"], hi=2)]),
            dict(say="Its trades were spread across many markets, so they were supposed to protect each other. They didn't. In the words of the New York Fed's president, William McDonough, as markets around the world moved in the same direction at the same time, the diversification on which Long-Term had previously relied failed them utterly.",
                 show=DOC(style="opinion", head="FEDERAL RESERVE BANK OF NEW YORK", sub="STATEMENT TO CONGRESS, OCTOBER 1, 1998",
                          quote="As markets around the world moved in the same direction at the same time, the diversification on which Long-Term had previously relied failed them utterly.",
                          hl=("same direction", "failed them utterly"), start=(2, "as markets"), wrap=40,
                          source="William J. McDonough, statement before the House Banking Committee, 1998", badge_text="Quoted from the statement", seed=21)),
            dict(say="MacKenzie points to another reason. Other firms held similar trades. When some of them sold, prices moved against the others, and that led to more selling. In his words, a cascade of self-reinforcing adverse price movements.",
                 shows=[S("book", "Another reason.", "MacKenzie, 2006", ["Another"], 110, title="2006"),
                        SS("figures", "Others held similar trades.", "MacKenzie, 2006", ["similar"], 96, flip=True, n=4, hi=0),
                        S("dominoes", "Selling led to more selling.", "MacKenzie, 2006", ["more"], 96, labels=["SELL", "SELL", "SELL", "SELL"], fall=1),
                        dict(kind="term", term="A cascade", text="of self-reinforcing adverse price movements. Donald MacKenzie, 2006")]),
        ]),
        dict(title="Four days in September", art=("clock", dict(time="8:30")), beats=[
            dict(say="On the second of September, the fund told its investors about the losses and asked for new capital. By Friday the eighteenth, it still had none. On Sunday the twentieth, a team from the New York Fed, with an official from the Treasury, went to look at the fund's positions.",
                 shows=[S("document", "A letter, and a request.", "September 2 · McDonough, 1998", ["request."], 96, title="TO INVESTORS", lines=4, stamp="SEPT 2"),
                        SS("calendar", "Friday 18: no new capital.", "McDonough, 1998", ["no"], 96, flip=True, day="18", month="SEP", note="NOTHING"),
                        S("magnifier", "Sunday 20: the Fed takes a look.", "McDonough, 1998", ["look."], 96, label="SEPT 20")]),
            dict(say="What they learned, McDonough later told Congress, was that the size of these positions was much greater than market participants imagined. The fund's own estimate was that its seventeen biggest counterparties could lose between three and five billion dollars between them.",
                 shows=[S("tower", "Bigger than anyone imagined.", "McDonough, 1998", ["imagined."], 96, floors=12, label="POSITIONS"),
                        dict(kind="compare", left=("Low estimate", "$3bn"), right=("High estimate", "$5bn"), note="Possible losses, top 17 counterparties, LTCM's estimate · PWG, 1999")]),
            dict(say="On Tuesday the twenty second, Fed officials met Goldman Sachs, Merrill Lynch and JPMorgan, and later UBS. At seven that evening, those firms looked at a draft term sheet. At about half past eight, thirteen firms sat down together. The Fed's officials were in the room, but didn't take part in the talks on terms.",
                 show=CINE("fed_evening")),
            dict(say="The next morning, an investor group led by Warren Buffett made a rival offer: two hundred and fifty million dollars for the partners' stake, and three point seven five billion of new capital. It wasn't accepted by its deadline of half past twelve, reportedly for legal reasons.",
                 shows=[dict(kind="compare", left=("For the partners", "$250m"), right=("New capital", "$3.75bn"), note="Offer of September 23 · Federal Reserve History"),
                        SS("clock", "Not accepted by 12:30.", "Federal Reserve History", ["12:30."], 100, flip=True, time="12:30")]),
            dict(say="At around six that evening, fourteen banks and securities firms agreed to put in about three point six billion dollars of new equity. In return they got ninety percent of the fund, and control of it. The original owners were left with ten percent.",
                 show=CINE("fed_deal")),
            dict(say="Two firms that were asked chose not to take part. And McDonough was clear on one point: not one penny of public money was spent or committed.",
                 shows=[S("figures", "Two firms said no.", "McDonough, 1998", ["no."], 100, n=2, hi=1),
                        SC("stamp", "Not one penny of public money (McDonough, 1998)", text="NO PUBLIC MONEY")]),
        ]),
        dict(title="Why rescue a rival?", art=("dominoes", dict(labels=["FUND", "BANK", "BANK", "MARKET"], fall=1)), beats=[
            dict(say="So why did the Fed get involved at all? McDonough's answer was that the abrupt and disorderly close-out of Long-Term Capital's positions would pose unacceptable risks to the American economy.",
                 show=DOC(style="notice", head="FEDERAL RESERVE BANK OF NEW YORK", sub="STATEMENT TO CONGRESS, OCTOBER 1, 1998",
                          quote="the abrupt and disorderly close-out of Long-Term Capital's positions would pose unacceptable risks to the American economy.",
                          hl=("abrupt and disorderly", "unacceptable risks"), start=(1, "the abrupt"), wrap=40,
                          source="William J. McDonough, statement before the House Banking Committee, 1998", badge_text="Quoted from the statement", seed=22)),
            dict(say="Alan Greenspan put it in terms of a fire sale. He told Congress that a fire sale may be sufficiently intense and widespread that it seriously distorts markets and elevates uncertainty enough to impair the overall functioning of the economy.",
                 show=DOC(style="opinion", head="BOARD OF GOVERNORS OF THE FEDERAL RESERVE", sub="TESTIMONY, OCTOBER 1, 1998",
                          quote="a fire sale may be sufficiently intense and widespread that it seriously distorts markets and elevates uncertainty enough to impair the overall functioning of the economy.",
                          hl=("fire sale", "seriously distorts"), start=(1, "a fire sale"), wrap=42,
                          source="Alan Greenspan, testimony before the House Banking Committee, 1998", badge_text="Quoted from the testimony", seed=23)),
            dict(say="Our reading is that the banks weren't really rescuing a rival. They were its lenders and its counterparties. A forced sale would have pushed down the prices of things they owned too. Putting in fresh money was the cheaper way out.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 120, text="?"),
                        SS("handshake", "Lenders and counterparties.", "Our reading", ["Lenders"], 100, flip=True, left="BANKS", right="FUND"),
                        S("dominoes", "A forced sale hits them too.", "Our reading", ["too."], 96, labels=["FUND", "BANK", "BANK", "BANK"], fall=1),
                        SS("scale", "The cheaper way out.", "Our reading", ["cheaper"], 100, flip=True, left="RESCUE", right="FIRE SALE", tip=1)]),
            dict(say="The President's Working Group later found that the fund appears to have received very generous credit terms, even though it took an exceptional degree of risk.",
                 show=DOC(style="flyer", head="PRESIDENT'S WORKING GROUP ON FINANCIAL MARKETS", sub="REPORT, APRIL 1999",
                          quote="LTCM appears to have received very generous credit terms, even though it took an exceptional degree of risk.",
                          hl=("generous credit terms", "exceptional degree of risk"), start=(0, "appears"), wrap=40,
                          source="Hedge Funds, Leverage, and the Lessons of Long-Term Capital Management, 1999", badge_text="Quoted from the report", seed=24)),
            dict(say="And there's a cost: Greenspan himself warned that whenever public involvement softens the blow of private losses, the issue of moral hazard arises. If the biggest players expect to be rescued, they may take more risk.",
                 shows=[S("scale", "Moral hazard.", "Greenspan, 1998", ["hazard."], 110, left="RISK", right="RESCUE", tip=0),
                        SS("bank", "Expect a rescue, take more risk.", "Our reading", ["more"], 96, flip=True, label="RESCUE?")]),
        ]),
        dict(title="Right, but not in time", art=("hourglass72", dict(rate="25:1", left="GAP", right="TIME")), beats=[
            dict(say="Under its new owners, the fund sold off most of its positions. By the end of nineteen ninety nine, the last of the three point six billion dollars had been returned to the firms.",
                 shows=[S("document", "Positions sold off.", "Federal Reserve History", ["sold"], 100, title="WIND-DOWN", lines=4, stamp="SOLD"),
                        SS("calendar", "Repaid by the end of 1999.", "Federal Reserve History", ["Repaid"], 100, flip=True, day="1999", month="DEC", note="REPAID")]),
            dict(say="And the lesson wasn't only about hedge funds. The same report found that at the end of nineteen ninety eight, the five largest investment banks had average leverage of twenty seven to one.",
                 shows=[S("bank", "Not only hedge funds.", "PWG, 1999", ["only"], 100, label="BANKS"),
                        dict(kind="compare", left=("The fund, August 1998", "25:1+"), right=("Top 5 investment banks, end 1998", "27:1"), note="Average leverage · President's Working Group, 1999")]),
            dict(say="Here's our reading. A trade can be right in the end and still ruin you on the way there. A gap that should close can get wider first. And with twenty five dollars of assets on every dollar of capital, you may not last long enough to see it close.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 120, text="!"),
                        SS("hourglass72", "Right in the end.", "Our reading", ["end"], 100, flip=True, rate="TIME", left="GAP", right="CLOSED"),
                        S("seesaw", "Wider first.", "Our illustration", ["Wider"], 110, left="GAP", right="TIME", tip=0),
                        SS("empty_pockets", "Gone before it closes.", "Our reading", ["Gone"], 100, flip=True, label="25:1")]),
            dict(say="Leverage doesn't change whether you're right. It changes how long you can afford to be wrong.",
                 shows=[dict(kind="statement", text="Leverage doesn't change whether you're right. It changes how long you can afford to be wrong.", hl=["long"], size=100)]),
            dict(say="If an interviewer asks you what LTCM teaches, here's a short answer. Small, steady gaps can hide big risks when they're bought with borrowed money, when everyone holds the same trade, and when there's no time to wait. This is education, not financial advice.",
                 shows=[S("document", "What does LTCM teach?", "Interview prep", ["LTCM"], 100, title="Q: LTCM?", lines=3, stamp="1998"),
                        dict(kind="list", title="The short answer", items=["Borrowed money", "Everyone in the same trade", "No time to wait"]),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. Should the Fed have brought the banks together, or let the fund fail? Tell us in the comments.",
                 shows=[S("bulb", "Our question for you.", "", ["question"], 110, text="?"),
                        SC("seesaw", "Bring the banks together, or let it fail?", left="RESCUE", right="LET IT FAIL", tip=0),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "September 1998. A hedge fund run in part by two Nobel laureates tells its investors it's lost $1.8 billion in August alo"
        "ne. That's more than half its capital since January. Three weeks later, fourteen banks and securities firms, called toge"
        'ther by the Federal Reserve Bank of New York, put in about $3.6 billion to stop it collapsing.\n\nSo why would Wall Street'
        " rescue a rival? We'll show you the trade Long-Term Capital Management was known for: two almost identical Treasury bond"
        "s, and a gap of about a tenth of a percentage point. You'll see why it only paid with borrowed money, what 25 to 1 lever"
        "age does when prices move the wrong way, how Russia's default in August 1998 made the gaps wider instead of narrower, an"
        'd the four days in September that ended in a room at the Fed.\n\nThen the hard part. Why did the Fed get involved, with no'
        " public money? What did Greenspan and McDonough tell Congress? We'll look at the moral hazard it raised and give you our"
        ' reading of the lesson. Should the Fed have let it fail? Tell us below.'),
    sources=[
        ("President's Working Group on Financial Markets, Hedge Funds, Leverage, and the Lessons of Long-Term Capital Management (April 1999)", "https://www.cftc.gov/tm/tmhedgefundreport.htm"),
        ("William J. McDonough, Statement before the House Committee on Banking and Financial Services, 1 October 1998", "https://www.newyorkfed.org/newsevents/speeches/1998/mcd981001"),
        ("Alan Greenspan, Testimony on the private-sector refinancing of Long-Term Capital Management, 1 October 1998", "https://www.federalreserve.gov/boarddocs/testimony/1998/19981001.htm"),
        ("Federal Reserve History, Near Failure of Long-Term Capital Management", "https://www.federalreservehistory.org/essays/ltcm-near-failure"),
        ("Donald MacKenzie, An Engine, Not a Camera, ch. 8 (MIT Press, 2006)", "https://personal.lse.ac.uk/robert49/teaching/ph232/pdf/MacKenzie-Ch8.pdf"),
        ("Nobel Prize press release, Economic Sciences 1997", "https://www.nobelprize.org/prizes/economic-sciences/1997/press-release/"),
        ("Furfine and Remolona, Price discovery in a market under stress: the U.S. Treasury market in fall 1998 (Chicago Fed WP 2005-06)", "https://www.chicagofed.org/-/media/publications/working-papers/2005/wp2005-06-pdf.pdf"),
    ],
    source_note="We drew the filmed scenes ourselves. They're stylised reconstructions, not the fund's office or the New York Fed's "
                "meeting room, nobody in them is a portrait, and nobody speaks. The bond screens are our illustration and carry no "
                "numbers. The million dollars a year, the 4% and the balance sheet drawn at 100 and 96 are our own arithmetic. The "
                "readings in the last two chapters are ours, so feel free to disagree with them. This channel is educational and isn't "
                "affiliated with, or endorsed by, any bank, fund or institution named in it.",
    hashtags=["FinanceHistory", "HedgeFunds", "Leverage"],
    tags=["LTCM", "Long-Term Capital Management", "LTCM 1998", "hedge fund collapse", "leverage explained", "convergence trade",
          "Federal Reserve 1998 rescue", "Russia default 1998", "Merton Scholes", "moral hazard", "financial history",
          "investment banking interview", "fire sale", "on the run off the run"],
)

if __name__ == "__main__":
    make(EP)
