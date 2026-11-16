"""
YouTube #10 (16 Nov 2026): the salad oil swindle of 1963. Lenders held warehouse receipts for 1.8 billion pounds of
vegetable oil in tanks in Bayonne, New Jersey; there were scarcely 100 million pounds. How did tanks of water and air
pass as collateral with American Express's warehouse company, two Wall Street brokers and big banks, and why did the
stock exchange end up covering a broker's debts in the week President Kennedy was shot? Financial history, scandals,
banking. Made to docs/production/long-form-standard.md (visual plan: build/plans/ep010.md). Score: suspense.

Point of view (our reading, labelled as ours): collateral is a chain of trust, and each link trusted the one before
it; the check on the oil was paid for by the borrower. Educational, not advice.

Every claim, sourced:
  [TIME65] "Crime: The Man Who Fooled Everybody", Time, 4 June 1965: De Angelis "leased 139 oil storage tanks, many as
      tall as five-story buildings"; built a refinery in Bayonne between 1958 and 1962; "Sometimes the tanks were indeed
      full" with "water, topped by a thin slick of oil"; "Usually many were empty"; "the tanks were connected by a
      jungle of pipes"; a man would climb a tank, "drop in a weighted tape measure, then shout down to an Amexco
      inspector on the ground that the tank was 90% full"; "Tino's men sometimes sneaked into the casually guarded tank
      farm on weekends, pumped oil from one tank to another"; receipts "signed by officials of American Express Co.";
      he later "forged some of his own receipts"; lenders "Instead of finding 1.8 billion lbs. of oil for which they
      held receipts ... found scarcely 100 million lbs.", the shortage worth about $130 million; by mid-1963 he had
      contracted to buy "1.2 billion lbs., worth about $120 million"; commodities margins "of 5% to 15%"; a 1 cent
      shift meant $12 million ("1c Equals $12 Million"); "At one time he had loans out on three times as much oil as
      the Bayonne tanks could hold"; loans from Ira Haupt and J. R. Williston & Beane, who took his warehouse receipts
      as collateral and used them to borrow from banks including Chase Manhattan and Continental Illinois; he paid
      American Express Warehousing "up to $20,000 a week"; "On Nov. 15 the market cracked, and so did Tino";
      "Allied Crude Vegetable Oil Refining Corp., tumbled into bankruptcy"; claims against Amexco "filed by 43
      companies, total more than $100 million"; son of poor Italian immigrants, quit high school to support his
      parents, a meat cutter in the Bronx, a $10,000 loan to open his own pork-packing plant; "had pleaded guilty to
      four federal counts of fraud and conspiracy".
  [TIME63] "Wall Street: $19 Million in the Hole", Time, 29 Nov 1963: "$19 million in margin calls"; De Angelis "was
      into Ira Haupt for at least $18 million", debts "double the firm's net worth"; the exchange ruled that neither
      firm could meet the capital requirement and barred both from trading; De Angelis "last week took refuge in
      bankruptcy".
  [TIMEAX] "Corporations: Oil, Vinegar & Sugar", Time (1965): American Express "has offered creditors $60 million in
      addition to a $20 million insurance settlement"; not legally responsible for the claims against its subsidiary;
      the stock "plummeted from $62 to $35" after the scandal broke.
  [BUNGE] Bunge Corp. v. London and Overseas Insurance Co., 394 F.2d 496 (2d Cir. 1968): "In late 1963 it was
      discovered that a massive fraud had been perpetrated by one Tino De Angelis, and that there was little or no
      oil in the tanks"; Bunge held warehouse receipts on oil in the tanks of a warehousing subsidiary of American
      Express.
  [DEANG] DeAngelis v. United States, 404 F.2d 46 (3d Cir. 1968): "convictions and sentences amounting to 20 years, as
      imposed on August 17, 1965".
  [NBER] Neil H. Jacoby and Raymond J. Saulnier, Financing Inventory on Field Warehouse Receipts (NBER, 1944): a field
      warehouse is "a special warehouse leased from, and established on the premises of, the borrowing concern";
      the warehouseman takes custody of the goods there and issues receipts that lenders accept as collateral.
  [INVNEWS] InvestmentNews, "Day JFK killed, NYSE faced massive selloff": Ira Haupt & Co. suspended from trading on
      Wednesday 20 November 1963; on 22 November "The bell rang at 2:07 p.m. The exchange closed"; "The Dow lost 21
      points, or 2.9%, that day".
  [SECHS] SEC Historical Society, The Institution of Experience, "Stress on the System: Member Firms": the threat
      "materialized in 1963 when the Ira Haupt firm failed"; "the exchange extended $12 million to cover Haupt's
      obligations" and "created a special trust to cover future brokerage firm failures".
  [PULITZER] The Pulitzer Prizes, Norman C. Miller, The Wall Street Journal: "For his comprehensive account of a
      multi-million dollar vegetable oil swindle in New Jersey."
  [FORTUNE] Stephen R. Foerster, adapted from Trailblazers, Heroes, and Crooks (Wiley, 2024), Fortune, 22 Sep 2024:
      "By June 1964, he had invested $3 million in Amex, BPL's largest single holding"; "Two-and-a-half years later,
      Amex's stock was $92.50".
  [SIPC] SIPC, History: SIPC had its origins in 1968 to 1970, when hundreds of broker-dealers merged or went out of
      business and some could not meet their obligations to customers; the Securities Investor Protection Act passed
      in 1970 and created SIPC.
Kept apart: Time's 1965 descriptions of the tricks are reported as Time's ("Time reported"); the filmed scenes are
reconstructions or our illustrations; the price per pound, the half-cent example and "one pound in eighteen" are our
own calculations from Time's figures; the chain-of-trust reading in the last chapter is ours.
Calculations (build/plans/ep010_checks.py): 100m / 1,800m = 5.6% (1 in 18); $120m / 1.2bn lb = 10 cents a pound;
1.2bn lb x $0.01 = $12m; 5% of $120m = $6m = 1.2bn lb x $0.005; 1963 + 7 = 1970; (62 - 35) / 62 = 43.5%.

    python build/youtube_ep010.py
"""

import cine_1963 as F
from cine_lib import document_shot
from youtube import make

S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)
CINE = lambda name: dict(kind="cine", shot=F.SHOTS[name])
DOC = lambda **kw: dict(kind="cine", shot=document_shot(**kw))

EP = dict(
    slug="yt-010-salad-oil",
    title="Wall Street Lent Against Tanks of Salad Oil. Most of the Oil Wasn't There.",
    score="suspense",
    fx="action",
    thumb=dict(film_a=dict(shot=F.SHOTS["yard_hook"], dur=11.0, t=10.6, pos="55% 50%",
                           segs=[("In nineteen sixty three, a company leased storage tanks.", .3, 5.0), ("On paper they held a fortune in vegetable oil.", 5.3, 10.6)]),
               film_b=dict(shot=F.SHOTS["slick"], dur=9.0, t=7.4, pos="50% 55%",
                           segs=[("Sometimes the tanks were full, Time said, with water topped by a thin slick of oil.", .3, 5.0),
                                 ("Look in from the top, and all you see is the oil.", 5.3, 8.6)]),
               big_a="1.8 billion pounds of oil. <span style='color:#D93A12'>Most</span> wasn't there.", size_a=80,
               big="Tanks of <span style='color:#D93A12'>water</span>. Loans of millions.", size=84,
               small="New Jersey, 1963"),
    chapters=[
        dict(title="A yard full of tanks", art=("tower", dict(floors=6, label="OIL?")), beats=[
            dict(say="In Bayonne, New Jersey, a businessman named Tino De Angelis leased a hundred and thirty nine oil storage tanks, many as tall as five story buildings. By nineteen sixty three, on paper, they held a fortune in vegetable oil.",
                 show=CINE("yard_hook")),
            dict(say="Lenders held receipts for one point eight billion pounds of it. When the tanks were finally checked, they found scarcely a hundred million pounds.",
                 shows=[S("receipt", "1.8 billion pounds on paper.", "Time, 1965", ["1.8"], 100, total="1.8bn lb", circle=0, coin_vals=("", "")),
                        dict(kind="compare", left=("Oil on the receipts", "1.8bn lb"), right=("Oil found in the tanks", "~100m lb"), note="Time, 4 June 1965")]),
            dict(say="Most of the oil had never existed. So how do you borrow against tanks of water and air, from some of the biggest names in American finance? And why did it end with the stock exchange covering a broker's debts, in the week President Kennedy was shot?",
                 shows=[SC("stamp", "Most of the oil never existed", text="MISSING"),
                        S("magnifier", "Borrowing against water and air?", "", ["water"], 100, flip=True, label="OIL?"),
                        SC("calendar", "The week of November 22, 1963", day="22", month="NOV", note="1963")]),
        ]),
        dict(title="The meat cutter from the Bronx", art=("factory", dict(label="REFINERY")), beats=[
            dict(say="Tino De Angelis was the son of poor Italian immigrants. He quit high school to support his parents, and started out as a meat cutter in the Bronx. A ten thousand dollar loan let him open his own pork packing plant.",
                 shows=[S("figures", "The son of immigrants.", "Our drawing, not a portrait", ["immigrants."], 100, n=1, hi=0),
                        S("house", "A meat cutter in the Bronx.", "Time, 1965", ["Bronx."], 96, flip=True, price="NY"),
                        S("pricetag", "A $10,000 loan.", "His own pork plant", ["$10,000"], 100, value="$10k", tag="LOAN")]),
            dict(say="Then he moved into vegetable oil. Between nineteen fifty eight and nineteen sixty two, he built a refinery in Bayonne, and his company was called Allied Crude Vegetable Oil Refining.",
                 shows=[SC("ship", "Then, vegetable oil"),
                        SC("factory", "A refinery in Bayonne, built 1958 to 1962", label="ALLIED")]),
            dict(say="To grow fast, he borrowed huge sums, and the collateral was the oil in his tanks.",
                 shows=[S("scale", "Borrowing against the oil.", "Time, 1965", ["oil."], 100, flip=True, left="LOANS", right="OIL", tip=0)]),
        ]),
        dict(title="A receipt for oil", art=("document", dict(title="RECEIPT", lines=3, stamp="OIL")), beats=[
            dict(say="Lending against stored goods was an old idea. A study published in nineteen forty four by the National Bureau of Economic Research described the field warehouse. In its words, a special warehouse leased from, and established on the premises of, the borrowing concern.",
                 show=DOC(style="opinion", head="NATIONAL BUREAU OF ECONOMIC RESEARCH", sub="FINANCING INVENTORY ON FIELD WAREHOUSE RECEIPTS (1944)",
                          quote="a special warehouse leased from, and established on the premises of, the borrowing concern",
                          hl=("leased from", "borrowing concern"), start=(2, "a special"), source="Jacoby and Saulnier, NBER, 1944",
                          badge_text="Quoted from the study", seed=3)),
            dict(say="Here's how it worked. A warehouse company takes charge of the goods right where they sit. It issues a receipt saying how much is there. A lender takes that receipt as collateral, and lends against it. And the lender can use the same receipt to borrow from a bank in turn.",
                 show=CINE("receipt_chain")),
            dict(say="In Bayonne, the warehouse company was a subsidiary of American Express. Its officials signed De Angelis's receipts, and he paid it up to twenty thousand dollars a week.",
                 shows=[S("bank", "A subsidiary of American Express.", "Its warehousing company", ["American"], 92, label="WAREHOUSING"),
                        S("receipt", "Up to $20,000 a week.", "Paid by De Angelis · Time, 1965", ["$20,000"], 100, flip=True, total="$20,000", circle=-1, coin_vals=("", ""))]),
            dict(say="His lenders included two old Wall Street brokers, Ira Haupt and Williston and Beane. They took his receipts as collateral, and used them to borrow from big banks, including Chase Manhattan and Continental Illinois.",
                 shows=[S("handshake", "Two Wall Street brokers.", "Ira Haupt · J. R. Williston & Beane", ["brokers."], 96, left="Haupt", right="Williston"),
                        dict(kind="flow", items=[("lock", "Receipts as collateral"), ("hand", "Brokers lend"), ("coin", "Banks lend to brokers")])]),
            dict(say="And the brokers had their own reason to keep him happy. They also handled his futures trading, and Time reported commissions of up to a hundred thousand dollars a month.",
                 shows=[S("bulb", "A reason to keep him happy.", "Our reading", ["happy."], 100, text="$"),
                        S("coins", "Up to $100,000 a month.", "Commissions on his futures · Time, 1965", ["$100,000"], 96, flip=True, stacks=[3, 5, 7])]),
        ]),
        dict(title="Ninety percent full", art=("magnifier", dict(label="90%")), beats=[
            dict(say="Time magazine later described how the inspectors were fooled. One of De Angelis's men would climb on top of a tank and drop in a weighted tape measure. Then he'd shout down to the inspector on the ground that the tank was ninety percent full. Usually, many of the tanks were empty.",
                 show=CINE("tape_trick")),
            dict(say="Sometimes the tanks really were full, with water, topped by a thin slick of oil.",
                 show=CINE("slick")),
            dict(say="Oil floats on water. So look in from the hatch at the top, and all you'd see is the oil.",
                 shows=[SC("magnifier", "Oil floats on water", label="OIL"),
                        S("arrows", "From the top, only oil.", "Our illustration", ["only"], 100, flip=True, up="OIL", down="WATER")]),
            dict(say="And on weekends, his men sneaked into the casually guarded yard and pumped oil from one tank to another, so the same oil could be counted again.",
                 show=CINE("pipes_night")),
            dict(say="Later, he didn't bother fooling the inspectors at all, and forged some receipts himself. At one point he had loans out on three times as much oil as the Bayonne tanks could even hold.",
                 shows=[S("document", "Then he forged receipts.", "Time, 1965", ["forged"], 100, title="RECEIPT", lines=3, stamp="FORGED"),
                        SC("bars", "Loans on three times as much oil as the tanks could hold (Time, 1965)", values=[1, 3], labels=["TANK SPACE", "LOANS ON"], hi=1)]),
        ]),
        dict(title="A bet on a cent", art=("coins", dict(stacks=[2, 4, 6])), beats=[
            dict(say="The money went into something riskier. By the middle of nineteen sixty three, De Angelis had contracted to buy one point two billion pounds of oil in the futures market, worth about a hundred and twenty million dollars. By November, Time reported, he'd bought a hundred and fifty million dollars' worth of futures.",
                 shows=[SC("handshake", "Futures: a deal now to buy later", left="Buy", right="Sell"),
                        dict(kind="compare", left=("Oil contracted, mid 1963", "1.2bn lb"), right=("Worth about", "$120m"), note="Time, 4 June 1965"),
                        dict(kind="number", value=150, pre="$", suf="m", label="of vegetable oil futures bought by November · Time, 29 Nov 1963")]),
            dict(say="Futures traded on small deposits, called margin, of five to fifteen percent. So a small move in the price was a big move in his money. Every cent a pound was twelve million dollars.",
                 shows=[S("pricetag", "Margin: 5% to 15% down.", "Time, 1965", ["Margin:"], 100, value="5%", tag="DOWN"),
                        S("seesaw", "A small move, a big swing.", "", ["big"], 100, flip=True, left="Price", right="Money", tip=1),
                        dict(kind="number", value=12000000, pre="$", label="for every 1¢ a pound · Time, 1965")]),
            dict(say="Here's our own arithmetic. A hundred and twenty million dollars for one point two billion pounds is about ten cents a pound. So a fall of just half a cent wipes out a five percent deposit.",
                 shows=[S("bulb", "Our arithmetic.", "", ["arithmetic."], 120, text="10¢"),
                        S("pricetag", "About 10 cents a pound.", "$120m ÷ 1.2bn lb", ["10"], 100, flip=True, value="10¢", tag="PER LB"),
                        SC("bars", "Our calculation: a 5% deposit is $6m, and half a cent a pound on 1.2bn lb is $6m", values=[6, 6], labels=["5% DEPOSIT", "½¢ FALL"], hi=1)]),
            dict(say="Then the price broke. On November the fifteenth, Time wrote, the market cracked, and so did Tino. The margin calls came to nineteen million dollars.",
                 show=CINE("margin_calls")),
        ]),
        dict(title="Four days in November", art=("calendar", dict(day="22", month="NOV", note="1963")), beats=[
            dict(say="Within days, his company was in bankruptcy. He owed Ira Haupt at least eighteen million dollars, about double the firm's net worth.",
                 shows=[S("bank_closed", "Bankrupt.", "Allied, November 1963", ["Bankrupt."], 120),
                        S("scale", "$18 million owed to Haupt.", "About double its net worth · Time, 1963", ["$18"], 96, flip=True, left="OWED", right="WORTH", tip=1)]),
            dict(say="Haupt was responsible for his futures contracts, and it tried to cover them, borrowing some thirty million dollars from American and British banks. When the market didn't recover, Haupt went under. The other broker, Williston and Beane, raised the money it needed in two days and was let back in.",
                 shows=[S("interest_stack", "About $30 million borrowed.", "From US and British banks · Time, 1965", ["$30"], 96, base="$30m", rate="TO COVER"),
                        SC("tower", "Haupt went under", crack=True, floors=6, label="HAUPT"),
                        S("document", "Williston raised the money.", "Back after two days · Time, 1963", ["Williston"], 96, flip=True, title="REINSTATED", lines=3, stamp="BACK")]),
            dict(say="On Wednesday, November the twentieth, Ira Haupt was suspended from trading. It no longer had the capital the exchange's rules required.",
                 shows=[SC("stamp", "Ira Haupt suspended, 20 November 1963", text="SUSPENDED"),
                        SC("bricks", "Not enough capital (Time, 29 November 1963)", n=12, red=0, label="CAPITAL")]),
            dict(say="Two days later, on Friday, November the twenty second, President Kennedy was shot in Dallas. In New York, the stock exchange closed at two oh seven in the afternoon. The Dow ended the day down two point nine percent.",
                 show=CINE("exchange_close")),
            dict(say="With a broker frozen and a market shaken, the exchange stepped in. It extended twelve million dollars to cover Haupt's obligations, and set up a special trust to cover future brokerage failures.",
                 shows=[S("handshake", "The exchange stepped in.", "SEC Historical Society", ["stepped"], 100, left="NYSE", right="Haupt"),
                        S("document", "$12 million, and a trust.", "For future brokerage failures", ["trust."], 100, flip=True, title="TRUST", lines=3, stamp="$12M")]),
        ]),
        dict(title="How big was the hole?", art=("receipt", dict(total="1.8bn", circle=-1, coin_vals=("", ""))), beats=[
            dict(say="Years later, a federal appeals court summed it up. In its words, in late nineteen sixty three it was discovered that a massive fraud had been perpetrated by one Tino De Angelis, and that there was little or no oil in the tanks.",
                 show=DOC(style="opinion", head="UNITED STATES COURT OF APPEALS, SECOND CIRCUIT", sub="BUNGE CORP. v. LONDON AND OVERSEAS INSURANCE CO. (1968)",
                          quote="In late 1963 it was discovered that a massive fraud had been perpetrated by one Tino De Angelis, and that there was little or no oil in the tanks.",
                          hl=("massive fraud", "no oil in the tanks"), start=(1, "in late"), source="394 F.2d 496 (2d Cir. 1968)",
                          badge_text="Quoted from the opinion", seed=4)),
            dict(say="Put the two numbers on one honest scale. Receipts for one point eight billion pounds, against about a hundred million found. Roughly one pound in eighteen was real.",
                 shows=[SC("bars", "Pounds of oil, millions: on the receipts and found (Time, 1965)", values=[1800, 100], labels=["RECEIPTS", "FOUND"], hi=1),
                        S("receipt", "1,800 million on paper.", "Time, 1965", ["1,800"], 100, flip=True, total="1.8bn lb", circle=0, coin_vals=("", "")),
                        S("pricetag", "About 1 pound in 18.", "Our calculation", ["18."], 100, value="1/18", tag="REAL")]),
            dict(say="Time put the shortage at about a hundred and thirty million dollars. Forty three companies filed claims of more than a hundred million against American Express.",
                 shows=[S("empty_pockets", "About $130 million short.", "Time, 1965", ["$130"], 100, label="OIL"),
                        S("figures", "43 companies, over $100 million.", "Claims against American Express · Time", ["43"], 96, flip=True, n=6, hi=0)]),
            dict(say="The fight over who would pay went on for years. The Haupt firm faced claims of thirty eight million dollars, and it sued American Express for fifty two million.",
                 shows=[SC("stamp", "Years of claims", text="CLAIMS"),
                        S("ledger", "Claims and counterclaims.", "Time, 1965", ["counterclaims."], 96, flip=True, names=("Claims on Haupt  $38m", "Haupt v. AmEx  $52m", "", ""), hi=(0, 1))]),
            dict(say="Time reported that American Express wasn't legally responsible for those claims. It offered creditors sixty million dollars anyway, on top of a twenty million dollar insurance settlement. Its shares fell from sixty two dollars to thirty five.",
                 shows=[S("scroll", "Not legally responsible.", "Time", ["Not"], 100, title="CLAIMS", seal="1964"),
                        dict(kind="compare", left=("Offered to creditors", "$60m"), right=("Plus insurance", "$20m"), note="Time"),
                        SC("bars", "American Express shares, dollars: before and after (Time)", values=[62, 35], labels=["BEFORE $62", "LOW $35"], hi=1)]),
        ]),
        dict(title="Twenty years", art=("scroll", dict(title="20 YEARS", seal="1965")), beats=[
            dict(say="De Angelis pleaded guilty to four federal counts of fraud and conspiracy. An appeals court later recorded the result: convictions and sentences amounting to twenty years, as imposed on August the seventeenth, nineteen sixty five.",
                 show=DOC(style="opinion", head="UNITED STATES COURT OF APPEALS, THIRD CIRCUIT", sub="DeANGELIS v. UNITED STATES (1968)",
                          quote="convictions and sentences amounting to 20 years, as imposed on August 17, 1965",
                          hl=("20 years", "August 17, 1965"), start=(1, "convictions"), wrap=34, source="404 F.2d 46 (3d Cir. 1968)",
                          badge_text="Quoted from the opinion", seed=5)),
            dict(say="A Wall Street Journal reporter, Norman Miller, won a Pulitzer Prize for covering it. The citation reads: for his comprehensive account of a multi million dollar vegetable oil swindle in New Jersey.",
                 show=DOC(style="notice", head="THE PULITZER PRIZES", sub="NORMAN C. MILLER · THE WALL STREET JOURNAL",
                          quote="For his comprehensive account of a multi-million dollar vegetable oil swindle in New Jersey.",
                          hl=("comprehensive account", "vegetable oil swindle"), start=(1, "for his"), source="Prize citation, pulitzer.org",
                          badge_text="Quoted from the citation", seed=6)),
            dict(say="And one investor bought while others ran. By June nineteen sixty four, Warren Buffett's partnership had put about three million dollars into American Express, its largest holding. Two and a half years later, the shares were at ninety two dollars and fifty cents.",
                 shows=[S("magnifier", "One investor bought.", "", ["bought."], 110, label="AMEX"),
                        S("coins", "About $3 million in.", "By June 1964 · Foerster, in Fortune", ["$3"], 100, flip=True, stacks=[2, 4, 6]),
                        SC("rocket", "$92.50, two and a half years later (Foerster, in Fortune)")]),
        ]),
        dict(title="A chain of trust", art=("dominoes", dict(labels=["BANK", "BROKER", "RECEIPT", "TANK"], fall=1)), beats=[
            dict(say="Here's our reading. Every link in the chain trusted the link before it. The banks trusted the brokers' collateral. The brokers trusted the receipts. The receipts trusted the inspectors, and the inspectors trusted a man on a ladder.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 130, text="1"),
                        SC("dominoes", "Each link trusted the one before it", labels=["BANK", "BROKER", "RECEIPT", "TANK"], fall=1),
                        S("bank", "Banks trusted the collateral.", "", ["collateral."], 96, label="BANK"),
                        S("document", "Brokers trusted the receipts.", "", ["receipts."], 96, flip=True, title="RECEIPT", lines=3, stamp="OK"),
                        S("tower", "And a man on a ladder.", "Time, 1965: '90% full'", ["ladder."], 96, floors=5, label="90%")]),
            dict(say="A receipt is only as good as the last time somebody really looked in the tank. And the man paying the warehouse company to look was the borrower himself.",
                 shows=[S("magnifier", "Only as good as the last look.", "Our reading", ["last"], 100, label="TANK"),
                        S("seesaw", "The borrower paid the checker.", "Up to $20,000 a week · Time", ["borrower"], 96, flip=True, left="Borrower", right="Checker", tip=1)]),
            dict(say="Seven years later, after a wave of broker failures, Congress passed the Securities Investor Protection Act, which created a corporation to protect brokerage customers.",
                 shows=[S("document", "1970: a law for broker failures.", "SIPC, History", ["1970:"], 96, title="SIPA 1970", lines=3, stamp="LAW")]),
            dict(say="If an interviewer asks what makes collateral good, think of Bayonne. Ask who checks it, who pays the checker, and what happens if it isn't there. This is education, not financial advice.",
                 shows=[S("document", "What makes collateral good?", "Interview prep", ["good?"], 100, title="Q: COLLATERAL?", lines=3, stamp="CHECK"),
                        dict(kind="list", title="The Bayonne test", items=["Who checks it?", "Who pays the checker?", "What if it isn't there?"]),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. What's the biggest thing you've ever trusted because of a piece of paper? Tell us in the comments.",
                 shows=[SC("magnifier", "Our question for you", label="YOU?"),
                        S("receipt", "Trusted because of a paper?", "Your turn", ["paper?"], 92, flip=True, total="?", circle=0, coin_vals=("", "")),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "Bayonne, New Jersey, 1963. Tino De Angelis leases 139 storage tanks, and lenders hold warehouse receipts for 1.8 billion "
        "pounds of vegetable oil in them. When somebody finally checks the tanks, there's scarcely 100 million pounds.\n\n"
        "How do you borrow against tanks of water and air from American Express's warehouse company, two Wall Street brokers and big "
        "banks? We'll follow a warehouse receipt from the tank to the bank, then the tricks Time magazine described in 1965: a weighted tape "
        "and a shout of \"90% full\", water topped by a thin slick of oil, oil pumped from tank to tank on weekends, and finally forged "
        "receipts. Then the futures bet (every cent a pound was $12 million), the crash of 15 November, $19 million in margin calls, and "
        "the week of 22 November, when the stock exchange covered a broker's debts as the country reeled from President Kennedy's "
        "assassination.\n\n"
        "We'll end with our own reading: collateral is a chain of trust, and here the borrower paid for the check. What's the biggest thing "
        "you've ever trusted because of a piece of paper? Tell us below."),
    sources=[
        ("Time, Crime: The Man Who Fooled Everybody (4 June 1965)", "https://time.com/archive/6833300/crime-the-man-who-fooled-everybody"),
        ("Time, Wall Street: $19 Million in the Hole (29 Nov 1963)", "https://time.com/archive/6813130/wall-street-19-million-in-the-hole"),
        ("Time, Corporations: Oil, Vinegar & Sugar", "https://time.com/archive/6636164/corporations-oil-vinegar-sugar"),
        ("Bunge Corp. v. London and Overseas Insurance Co., 394 F.2d 496 (2d Cir. 1968)", "https://www.leagle.com/decision/1968890394f2d4961759"),
        ("DeAngelis v. United States, 404 F.2d 46 (3d Cir. 1968)", "https://www.leagle.com/decision/1968450404f2d461432"),
        ("Jacoby and Saulnier, Financing Inventory on Field Warehouse Receipts (NBER, 1944)", "https://www.nber.org/system/files/chapters/c4016/c4016.pdf"),
        ("InvestmentNews, Day JFK killed, NYSE faced massive selloff", "https://www.investmentnews.com/industry-news/day-jfk-killed-nyse-faced-massive-selloff/55145"),
        ("SEC Historical Society, Stress on the System: Member Firms", "https://sechistorical.org/exhibition/the-institution-of-experience-self-regulatory-organizations-in-the-securities-industry-1792-2010/evolution-of-the-perfect-institution/stress-on-the-system-member-firms/"),
        ("The Pulitzer Prizes, Norman C. Miller, The Wall Street Journal", "https://www.pulitzer.org/winners/norman-c-miller"),
        ("Stephen R. Foerster in Fortune, Warren Buffett and the American Express scandal (22 Sep 2024)", "https://www.fortune.com/2024/09/22/warren-buffett-investing-strategy-american-express-stock-scandal"),
        ("SIPC, History", "https://www.sipc.org/about-sipc/history"),
    ],
    source_note="We drew the filmed scenes ourselves. They're stylised reconstructions, not the real yard or anyone's portrait, and "
                "nobody in them speaks. The warehouse receipt is our own design. The price per pound, the half-cent example and \"one pound "
                "in eighteen\" are our own calculations from Time's figures, and the reading in the last chapter is ours, so feel free "
                "to disagree with it.",
    hashtags=["FinanceHistory", "Fraud", "WallStreet"],
    tags=["salad oil scandal", "salad oil swindle", "Tino De Angelis", "American Express 1963", "warehouse receipts", "field warehousing",
          "collateral fraud", "Ira Haupt", "Bayonne tanks", "commodity futures margin", "financial history", "Wall Street scandals",
          "Warren Buffett American Express", "investment banking interview"],
)

if __name__ == "__main__":
    make(EP)
