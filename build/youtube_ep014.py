"""
YouTube #14 (20 Nov 2026): Silicon Valley Bank, March 2023. On 9 March 2023 depositors took more than $40 billion
out of one American bank in a single day, and most of what the bank owned was not risky loans but bonds. How does a
bank full of bonds that pay back in full go bust in two days? Banking crises, interest-rate risk (bond prices and
rates), bank accounting (held to maturity), deposit runs. Made to docs/production/long-form-standard.md and the
18 Nov decision (open on the hook, number on screen in the first frame; title and thumbnail on the same number).
Visual plan: build/plans/ep014.md. Score: suspense (style and key: score.pick's slot for the long film).

Point of view (our reading, labelled as ours): the bonds were safe from default and still lost value, because their
price moves with interest rates; the loss only had to be taken if the bank had to sell; a bank whose deposits can
leave in a day may have to sell. Educational, not advice.

Every claim, sourced (only pages opened or returned by a search in this run):
  [FED] Federal Reserve Board, Review of the Federal Reserve's Supervision and Regulation of Silicon Valley Bank
      (28 April 2023): executive summary: "On March 9, SVB lost over $40 billion in deposits, and SVBFG management
      expected to lose over $100 billion more on March 10."; the outflow "represented roughly 85 percent of the
      bank's deposit base"; for comparison "about $10 billion in outflows over 8 days" (Wachovia, 2008) and "$19
      billion over 16 days" (Washington Mutual, 2008); "Between 2019 and 2021, SVBFG tripled in size"; "SVBFG invested
      them primarily in securities with longer-term maturities"; "Rising rates impacted SVBFG in two ways: both net
      interest income and the value of long-dated securities declined"; deposits "largely uninsured"; "highly
      correlated withdrawals from SVBFG's concentrated network of VC investors and technology firms who, fueled by
      social media, withdrew uninsured deposits in a coordinated manner at an unprecedented rate"; 8 March: "SVBFG had
      sold $21 billion in available-for-sale (AFS) securities, was booking a $1.8 billion after-tax loss, ... and was
      seeking to raise $2.25 billion in capital."; "On March 10, 2023, Silicon Valley Bank (SVB) ... was closed by
      the California Department of Financial Protection and Innovation (CDFPI)"; "SVBFG's failure can be tied
      directly to the failure of the board of directors and senior management." Key takeaways: "the firm was growing
      rapidly from $71 billion to over $211 billion in assets from 2019 to 2021".
  [BAR] Michael S. Barr, Vice Chair for Supervision, testimony to the Senate Banking Committee, 28 March 2023: "To
      begin, SVB's failure is a textbook case of mismanagement."; "SVB failed because the bank's management did not
      effectively manage its interest rate and liquidity risk"; "The bank waited too long to address its problems";
      "These depositors were connected by a network of venture capital firms and other ties, and when stress began,
      they essentially acted together to generate a bank run."; "its capital levels did not have to reflect
      unrealized losses on certain securities"; "in a period of less than 24 hours".
  [10K] SVB Financial Group, Form 10-K for 2022: HTM securities at 31 Dec 2022, amortized cost $91,327m, fair value
      $76,169m, unrecognized holding loss $15,160m; HTM weighted-average duration 6.2 years; HTM weighted-average yield
      1.66%; AFS fair value $26,069m; total deposits $173,109m (2022) and $189,203m (2021); total assets $211,793m;
      total SVBFG stockholders' equity $16,004m; "estimated uninsured deposits in U.S. offices that exceed the FDIC
      insurance limit were $151.5 billion".
  [JS] Joint statement by Treasury, the Federal Reserve and the FDIC, 12 March 2023 (6:15 p.m.): resolution "in a
      manner that fully protects all depositors"; "Depositors will have access to all of their money starting
      Monday, March 13."; "No losses associated with the resolution of Silicon Valley Bank will be borne by the
      taxpayer."; "Shareholders and certain unsecured debtholders will not be protected."; "Any losses to the
      Deposit Insurance Fund to support uninsured depositors will be recovered by a special assessment on banks".
  [FDIC] FDIC press release 2023-16: closed by the California DFPI, "which appointed the Federal Deposit Insurance
      Corporation (FDIC) as receiver"; "Customers with accounts in excess of $250,000 should contact the FDIC".
  [AB] American Banker, 9 March 2023: the securities sold were "U.S. Treasury and agency securities".

Labelled as ours: the $100, 10-year, 1.5% bond and its price at 4% ($79.72, build/plans/ep014_checks.py); the filmed
rooms, the phone, the laptop, the branch and the notice (reconstructions and illustrations, nobody is a portrait,
nobody speaks); "more than half of everything it owned was bonds" is our arithmetic on [10K] (HTM 91.3 + AFS 26.1 of
211.8 = 55%); "fifteen billion against sixteen billion" is [10K]'s two figures side by side; the readings in the last
two chapters.

    python build/youtube_ep014.py
"""

import cine_2023 as F
from cine_lib import document_shot
from youtube import make

S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)
SS = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: SC(art, txt, **opts)
CINE = lambda name: dict(kind="cine", shot=F.SHOTS[name])
DOC = lambda **kw: dict(kind="cine", shot=document_shot(**kw))
FED = "Federal Reserve review, 2023"
TENK = "SVB Form 10-K, 2022"

EP = dict(
    slug="yt-014-svb-40-billion",
    title="$40 Billion Left This Bank in One Day. It Was Full of Safe Bonds.",
    score="suspense",
    hook_first=True,
    fx="action",
    held_life=True,
    text_life=True,
    thumb=dict(film_a=dict(shot=F.SHOTS["hook_40bn"], dur=12.0, t=2.6, pos="70% 40%",
                           segs=[("On the ninth of March, twenty twenty three, depositors took more than forty billion dollars out of one American bank, in a single day.", .3, 5.0),
                                 ("Most of what it owned wasn't risky loans. It was bonds.", 5.2, 7.6),
                                 ("So how does a bank full of bonds go bust in two days?", 7.8, 10.4)]),
               film_b=dict(shot=F.SHOTS["run_street"], dur=15.0, t=13.5, pos="50% 25%",
                           segs=[("The Fed's review says social media fuelled the withdrawals.", .3, 4.5),
                                 ("On Thursday the ninth, over forty billion dollars left.", 4.7, 8.0),
                                 ("Management expected over a hundred billion more the next day.", 8.2, 11.5)]),
               big_a="<span style='color:#D93A12'>$40 billion</span> in one day", size_a=104,
               big="<span style='color:#D93A12'>$40bn</span> gone. Safe bonds?", size=100,
               small="Silicon Valley Bank, 2023"),
    chapters=[
        dict(title="Forty billion in a day", art=("outflow", dict(label="$40bn+ OUT", n=7)), beats=[
            dict(say="On the ninth of March, twenty twenty three, depositors took more than forty billion dollars out of one American bank, in a single day. Most of what it owned wasn't risky loans. It was bonds. So how does a bank full of bonds go bust in two days?",
                 show=CINE("hook_40bn")),
            dict(say="The bank was Silicon Valley Bank, in California. Its bonds weren't going to default. But at the end of twenty twenty two, they were worth about fifteen billion dollars less than the price on its books. And all of its equity came to sixteen billion.",
                 show=CINE("book_gap")),
            dict(say="This film follows the money. Where the deposits came from, how a bond can lose value without missing a payment, and the two days that ended it.",
                 shows=[S("magnifier", "Follow the money.", "", ["money."], 104, label="$"),
                        dict(kind="list", title="In this film", items=["Where the deposits came from", "A bond that loses a fifth", "Two days in March"])]),
        ]),
        dict(title="Money pouring in", art=("coin_stacks", dict(values=("$71bn", "$211bn", "$212bn"), labels=("2019", "2021", "FAILED"))), beats=[
            dict(say="Silicon Valley Bank was the bank of young tech companies, and of the venture capital firms that fund them. Between twenty nineteen and twenty twenty one, it tripled in size, from seventy one billion dollars of assets to over two hundred and eleven billion.",
                 show=CINE("growth")),
            dict(say="Much of that money arrived as deposits. By the end of twenty twenty two, the bank held a hundred and seventy three billion dollars of them.",
                 shows=[S("coins", "Deposits pouring in.", "", ["Deposits"], 100),
                        dict(kind="number", value=173, pre="$", suf="bn", label="deposits, December 31, 2022 · SVB Form 10-K")]),
            dict(say="In the US, deposit insurance covers up to two hundred and fifty thousand dollars per depositor at a bank, in most cases. SVB estimated that a hundred and fifty one and a half billion dollars of its US deposits were above that limit.",
                 shows=[S("document", "Insured up to $250,000.", "FDIC", ["$250,000."], 96, title="INSURED", lines=3, stamp="$250K"),
                        dict(kind="compare", left=("All deposits, end of 2022", "$173bn"), right=("Estimated above the limit (US)", "$151.5bn"), note="SVB Form 10-K, 2022")]),
            dict(say="A bank doesn't keep deposits in a vault. It lends them out, or invests them. SVB put much of the money into bonds with long maturities, to earn more on it. By the end of twenty twenty two, more than half of everything it owned was bonds.",
                 shows=[S("bank", "Not in a vault.", "", ["vault."], 100, label="BANK"),
                        SS("t_account", "Lent out, or invested.", left="LOANS, BONDS", right="DEPOSITS", amount="$", title="THE BANK'S BOOKS"),
                        SS("hourglass72", "Long bonds, to earn more.", "", (), 96, flip=True, rate="LONG", left="DEPOSITS", right="BONDS"),
                        SC("bars", "End of 2022, $ billion: bonds against everything it owned (SVB Form 10-K; our sum)", values=[117.4, 211.8], labels=["BONDS $117.4BN", "ALL ASSETS $211.8BN"], hi=0)]),
        ]),
        dict(title="The bond that loses a fifth", art=("seesaw", dict(left="RATES", right="PRICE", tip=0)), beats=[
            dict(say="Here's the puzzle, with our own round numbers. You buy a ten year bond for a hundred dollars. It pays one and a half percent a year, and it pays back the hundred in full. Then interest rates rise, and new ten year bonds pay four percent.",
                 show=CINE("bond_1")),
            dict(say="Nobody will pay you a hundred dollars for a bond paying one and a half percent, when a hundred dollars buys one paying four percent. To sell yours, you'd have to cut the price until the buyer earns four percent too. That price is about seventy nine dollars and seventy cents.",
                 show=CINE("bond_2")),
            dict(say="Your bond hasn't missed a payment. It will still pay back a hundred at the end. But if you need the cash today, about a fifth of it is gone.",
                 shows=[S("stamp", "No missed payment.", "Our example", ["payment."], 100, text="PAID"),
                        dict(kind="compare", left=("Paid back in 10 years", "$100"), right=("If you sell today", "$79.72"), note="Our example: 1.5% a year, new bonds at 4%"),
                        S("empty_pockets", "A fifth, gone today.", "", ["today."], 96, flip=True, label="-20%")]),
            dict(say="It works the other way too. If new bonds paid just one percent, your bond would be worth more than a hundred: about a hundred and four dollars and seventy four cents.",
                 shows=[SS("seesaw", "Rates down, price up.", "", (), 96, left="RATES", right="PRICE", tip=1),
                        dict(kind="number", value=104.74, dec=2, pre="$", label="our $100 bond at 1.5%, if new bonds paid 1% · our example")]),
            dict(say="Bankers measure this with duration. Roughly, it's the percentage a bond's price falls when rates rise by one point. Our bond's duration is a little over nine. Take rates from one and a half percent to two and a half, and its price falls about nine percent, to ninety one dollars and twenty five cents.",
                 shows=[S("magnifier", "Duration.", "", ["Duration."], 104, label="%"),
                        dict(kind="term", term="Duration", text="roughly, the % a bond's price falls when rates rise one percentage point."),
                        dict(kind="number", value=9.2, dec=1, label="our 10-year bond's duration, at 1.5% · our example"),
                        SC("bars", "Our example: rates from 1.5% to 2.5%, price in $", values=[100, 91.25], labels=["AT 1.5%: $100", "AT 2.5%: $91.25"], hi=1)]),
            dict(say="And the longer the bond, the further it falls. SVB's bonds held to maturity had a weighted average duration of six point two years. On average, they yielded just one point six six percent.",
                 shows=[SC("bars", "Our example at 4%: a 1.5% bond worth, $ (6 years against 10)", values=[86.89, 79.72], labels=["6 YEARS: $86.89", "10 YEARS: $79.72"], hi=1),
                        dict(kind="number", value=6.2, dec=1, suf=" years", label="average duration, held-to-maturity bonds, end of 2022 · SVB Form 10-K"),
                        dict(kind="number", value=1.66, dec=2, suf="%", label="their average yield · SVB Form 10-K, 2022")]),
        ]),
        dict(title="Two kinds of books", art=("scale", dict(left="AT COST", right="AT MARKET", tip=0)), beats=[
            dict(say="Banks can label their bonds in two ways. Bonds available for sale are shown at market prices. Bonds held to maturity are shown at what they cost, because the bank means to keep them until they pay back.",
                 shows=[S("document", "Two labels.", "", ["labels."], 104, title="BONDS", lines=4, stamp="2"),
                        dict(kind="split", left=("doc", "Available for sale", "At market"), right=("scales", "Held to maturity", "At cost")),
                        S("hourglass72", "Kept until they pay back.", "", ["pay"], 96, flip=True, rate="HTM", left="BUY", right="REPAID")]),
            dict(say="At the end of twenty twenty two, SVB held ninety one billion dollars of bonds labelled held to maturity. At market prices, they were worth seventy six billion.",
                 shows=[SC("bars", "Held to maturity, end of 2022, $ billion (SVB Form 10-K)", values=[91.3, 76.2], labels=["ON ITS BOOKS $91.3BN", "AT MARKET $76.2BN"], hi=1)]),
            dict(say="Its bonds available for sale were smaller: twenty six billion dollars at market prices, after two and a half billion of losses that already showed.",
                 shows=[S("document", "Available for sale: $26bn.", "SVB Form 10-K, 2022", ["$26bn."], 96, title="AFS", lines=3, stamp="-$2.5bn")]),
            dict(say="Fifteen billion dollars of loss, against sixteen billion of equity. And under the rules for a bank of its size, its capital didn't have to reflect those losses.",
                 shows=[S("seesaw", "Fifteen against sixteen.", "SVB Form 10-K, 2022", ["sixteen."], 96, left="$15.2bn LOSS", right="$16.0bn EQUITY", tip=1),
                        dict(kind="term", term="Unrealized losses", text="its capital levels did not have to reflect unrealized losses on certain securities. Michael Barr, 2023")]),
            dict(say="The loss only had to be taken if the bank sold the bonds. And a bank has to sell when depositors want their money back faster than the cash comes in.",
                 shows=[S("bulb", "Only if it sells.", "Our reading", ["sells."], 110, text="?"),
                        SS("queue", "When depositors want it back.", "", (), 96, flip=True, n=6, label="WITHDRAW")]),
        ]),
        dict(title="Rates go up", art=("arrows", dict(up="RATES", down="BOND PRICES")), beats=[
            dict(say="In twenty twenty two, interest rates in America rose. In the Fed's review, rising rates hit SVB in two ways. Its interest income fell, and so did the value of its long bonds.",
                 shows=[S("rocket", "Rates rose.", "", ["rose."], 100),
                        SS("magnifier", "The Fed's review.", "", (), 96, flip=True, label="2023"),
                        dict(kind="flow", title="Rising rates hit it twice", items=[("coin", "Interest income down"), ("doc", "Long bonds worth less"), ("scales", "Pressure on earnings")])]),
            dict(say="Its deposits started to fall too, from a hundred and eighty nine billion dollars at the end of twenty twenty one, to a hundred and seventy three billion a year later.",
                 shows=[SC("bars", "Deposits, $ billion (SVB Form 10-K)", values=[189.2, 173.1], labels=["END 2021: $189.2BN", "END 2022: $173.1BN"], hi=1),
]),
            dict(say="Its depositors were concentrated: technology firms and the venture capital investors behind them. In the words of the Fed's vice chair for supervision, Michael Barr, when stress began, they essentially acted together.",
                 shows=[S("handshake", "Tech firms and their investors.", "Barr testimony, 2023", ["investors."], 96, left="FUND", right="START-UP"),
                        dict(kind="quote", text="These depositors were connected by a network of venture capital firms and other ties, and when stress began, they essentially acted together.",
                             hl=["connected", "acted together."], who="Michael Barr, Senate testimony, March 28, 2023", size=72)]),
            dict(say="When a deposit leaves, a bank pays it from its cash, or borrows, or sells something. Every bond sold at a lower price than it cost turns a loss on paper into a real one.",
                 shows=[dict(kind="flow", title="A deposit leaves", items=[("coin", "Pay from cash"), ("doc", "Borrow"), ("scales", "Sell bonds")]),
                        S("stamp", "A paper loss, made real.", "Our reading", ["real."], 96, flip=True, text="SOLD")]),
        ]),
        dict(title="Wednesday to Friday", art=("calendar", dict(day="8", month="MAR", note="2023")), beats=[
            dict(say="On Wednesday the eighth of March, SVB announced it had sold twenty one billion dollars of its bonds available for sale, booking a loss of one point eight billion dollars after tax. And it planned to raise two point two five billion dollars of new capital.",
                 show=CINE("march8")),
            dict(say="In our reading, that announcement told every depositor two things at once. The bond losses were real. And the bank needed money.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 110, text="!"),
                        SS("stamp", "The losses were real.", "", (), 96, text="REAL"),
                        S("empty_pockets", "The bank needed money.", "", ["money."], 96, flip=True, label="CAPITAL")]),
            dict(say="The Fed's review says social media fuelled the withdrawals. On Thursday the ninth, over forty billion dollars left. Management expected over a hundred billion more the next day.",
                 show=CINE("run_street")),
            dict(say="Together, that was about eighty five percent of the bank's deposits. For comparison, in two thousand and eight, Washington Mutual lost nineteen billion dollars over sixteen days, and Wachovia about ten billion over eight.",
                 shows=[dict(kind="number", value=85, suf="%", label="of the deposit base, March 9 and the outflow expected on March 10 · Federal Reserve review"),
                        SC("bars", "Deposits out, $ billion (Federal Reserve review, 2023)", values=[10, 19, 40], labels=["WACHOVIA ~$10BN, 8 DAYS", "WAMU $19BN, 16 DAYS", "SVB OVER $40BN, 1 DAY"], hi=2)]),
            dict(say="On Friday the tenth of March, the California regulator closed the bank, and named the FDIC, the deposit insurer, as receiver.",
                 show=CINE("closed")),
        ]),
        dict(title="Sunday night", art=("clock", dict(time="6:15")), beats=[
            dict(say="On Sunday evening, the Treasury, the Fed and the FDIC said that every depositor would be protected, insured or not. They would have access to all of their money from Monday.",
                 shows=[S("document", "Every depositor protected.", "Joint statement, March 12, 2023", ["Every"], 96, title="MARCH 12", lines=4, stamp="ALL"),
                        dict(kind="timeline", title="Three days (Federal Reserve; FDIC; joint statement)", items=[("FRI 10", "Bank closed"), ("SUN 12", "All depositors protected"), ("MON 13", "Access to all of it")], hi=1)]),
            dict(say="Shareholders and certain unsecured debtholders were not protected. And any losses to the deposit insurance fund would be recovered by a special assessment on banks. The statement said no losses would be borne by the taxpayer.",
                 shows=[SS("empty_pockets", "Shareholders: not protected.", "", (), 96, label="SHARES"),
                        S("scale", "A charge on banks.", "Joint statement, 2023", ["banks."], 96, flip=True, left="BANKS", right="TAXPAYER", tip=0),
                        dict(kind="term", term="The taxpayer", text="No losses associated with the resolution of Silicon Valley Bank will be borne by the taxpayer. Joint statement, 2023")]),
            dict(say="The same Sunday, the Federal Reserve said it would make additional funding available to eligible banks.",
                 shows=[S("bank", "Additional funding for banks.", "Federal Reserve, March 12, 2023", ["funding"], 96, label="FED")]),
        ]),
        dict(title="Why it failed", art=("magnifier", dict(label="WHY?")), beats=[
            dict(say="Barr told Congress how he saw it. SVB's failure is a textbook case of mismanagement.",
                 show=DOC(style="opinion", head="BOARD OF GOVERNORS OF THE FEDERAL RESERVE SYSTEM", sub="TESTIMONY, MARCH 28, 2023",
                          quote="To begin, SVB's failure is a textbook case of mismanagement.",
                          hl=("textbook case", "mismanagement"), start=(0, "To begin"), wrap=36,
                          source="Michael S. Barr, Vice Chair for Supervision, before the Senate Banking Committee", badge_text="Quoted from the testimony", seed=41)),
            dict(say="He said the bank's management did not effectively manage its interest rate and liquidity risk, and waited too long to address its problems. The Fed's review tied the failure directly to the board and senior management.",
                 shows=[S("tower", "Rate risk and liquidity risk.", "Barr testimony, 2023", ["liquidity"], 96, crack=True, floors=6, label="SVB"),
                        dict(kind="term", term="The review", text="the failure can be tied directly to the board of directors and senior management. Federal Reserve, 2023")]),
            dict(say="It's often said the bank failed because it bought risky assets. Our reading is different: the bonds were safe from default. The risk wasn't whether they would pay, but what they were worth on the day the bank had to sell.",
                 shows=[S("myth_stamp", "Risky assets?", "", ["Risky"], 100),
                        SS("seesaw", "Safe from default, not from rates.", "", (), 96, flip=True, left="DEFAULT", right="RATES", tip=1),
                        dict(kind="statement", text="The risk wasn't whether they'd pay. It was what they were worth on the day it had to sell.", hl=["worth"], size=72)]),
            dict(say="Long bonds, paid for with deposits that could leave in a day: bankers call that a mismatch. SVB's ran in the worst direction at the worst time.",
                 shows=[SC("scale", "Long bonds against money that could leave in a day", left="10-YEAR BONDS", right="DEPOSITS: 1 DAY", tip=1),
                        S("dominoes", "A mismatch.", "", ["mismatch."], 100, labels=("RATES", "BONDS", "SALE", "RUN"))]),
        ]),
        dict(title="Safe, and still a loss", art=("handshake", dict(left="SAFE", right="LOSS")), beats=[
            dict(say="Here's our reading of the whole story. A bond can be safe and still lose value. Whether that loss matters depends on whether you can wait.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 120, text="?"),
                        dict(kind="number", value=79.72, dec=2, pre="$", label="what our $100 bond fetches when new bonds pay 4%: no default needed"),
                        S("hourglass72", "Can you wait?", "", ["wait?"], 96, flip=True, rate="TIME", left="SELL NOW", right="WAIT")]),
            dict(say="If an interviewer asks why rising rates can sink a bank, here's a short answer. Bond prices fall when rates rise, and long bonds fall the most. A bank that funds long bonds with deposits that can leave quickly may have to sell them at a loss. This is education, not financial advice.",
                 shows=[S("document", "Why can rates sink a bank?", "Interview prep", ["sink"], 100, title="Q: RATES?", lines=3, stamp="2023"),
                        SS("seesaw", "Rates up, prices down.", "", (), 96, flip=True, left="RATES", right="PRICES", tip=0),
                        dict(kind="list", title="The short answer", items=["Rates up, bond prices down", "Long bonds fall the most", "Fast deposits can force a sale"]),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. Should banks have to show every bond at its market price? Tell us in the comments.",
                 shows=[S("bulb", "Our question for you.", "", ["question"], 110, text="?"),
                        SC("seesaw", "At cost, or at market price?", left="AT COST", right="AT MARKET", tip=1),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "On March 9, 2023, depositors took more than $40 billion out of Silicon Valley Bank in a single day. Most of what "
        "the bank owned wasn't risky loans. It was bonds. So how does a bank full of bonds go bust in two days?\n\n"
        "We start with the puzzle at the centre of it: a $100 bond that pays 1.5% a year, and what it's worth once new "
        "bonds pay 4%. It never misses a payment, and it still loses about a fifth of its price. Then we look at how SVB "
        "grew, why its $15 billion of losses on bonds held to maturity sat next to $16 billion of equity, and the "
        "announcement on March 8 that set off the run. We finish with the Sunday night decision to protect every "
        "depositor, what the Fed's own review said went wrong, and our reading of the lesson. Should banks have to show "
        "every bond at its market price? Tell us below."),
    sources=[
        ("Federal Reserve Board, Review of the Federal Reserve's Supervision and Regulation of Silicon Valley Bank, executive summary (April 2023)",
         "https://www.federalreserve.gov/publications/2023-April-SVB-Executive-Summary.htm"),
        ("Federal Reserve Board, the same review, key takeaways (April 2023)",
         "https://www.federalreserve.gov/publications/2023-April-SVB-Key-Takeaways.htm"),
        ("Michael S. Barr, testimony to the Senate Banking Committee, March 28, 2023",
         "https://www.federalreserve.gov/newsevents/testimony/barr20230328a.htm"),
        ("SVB Financial Group, Form 10-K for 2022 (SEC EDGAR)",
         "https://www.sec.gov/Archives/edgar/data/719739/000071973923000021/sivb-20221231.htm"),
        ("Joint statement by the Treasury, the Federal Reserve and the FDIC, March 12, 2023",
         "https://www.federalreserve.gov/newsevents/pressreleases/monetary20230312b.htm"),
        ("FDIC press release 2023-16, Silicon Valley Bank closed, FDIC appointed receiver",
         "https://www.fdic.gov/news/press-releases/2023/pr23016.html"),
        ("American Banker, SVB Financial sells securities at a $1.8B loss, launches capital raise (March 9, 2023)",
         "https://www.americanbanker.com/news/svb-financial-sells-securities-at-a-1-8b-loss-launches-capital-raise"),
    ],
    source_note="We drew the filmed scenes ourselves. The phone, the laptop, the office, the branch and the notice on its door are "
                "our illustrations and stylised reconstructions, not the real bank or its staff. Nobody in them is a portrait, and "
                "nobody speaks. The $100 bond at 1.5% and its price of $79.72 once new bonds pay 4% are our own example, worked "
                "out in full. \"More than half of everything it owned was bonds\" is our sum from the 10-K ($91.3 billion held to "
                "maturity plus $26.1 billion available for sale, of $211.8 billion). The readings in the last chapters are ours, "
                "so feel free to disagree with them. This channel is educational and isn't affiliated with, or endorsed by, any "
                "bank, regulator or company named in it.",
    hashtags=["SiliconValleyBank", "BankRun", "FinanceHistory"],
    tags=["Silicon Valley Bank", "SVB collapse", "SVB bank run 2023", "why did SVB fail", "bond prices and interest rates",
          "held to maturity", "unrealized losses", "duration risk", "bank run explained", "FDIC deposit insurance",
          "March 2023 banking crisis", "interest rate risk", "investment banking interview", "financial history"],
)

if __name__ == "__main__":
    make(EP)
