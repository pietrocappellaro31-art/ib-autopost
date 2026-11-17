"""
YouTube #11 (17 Nov 2026): Herstatt, 26 June 1974. A German bank is shut at half past three in the afternoon; banks
that had already paid it Deutsche marks for dollars due later that day in New York never get their dollars. How do
you lose the whole amount of a trade that went exactly as agreed, and why is more than a trillion dollars a day still
exposed to the same gap fifty years later? Banking crises, financial history, how markets settle. Made to
docs/production/long-form-standard.md (visual plan: build/plans/ep011.md). Score: suspense.

Point of view (our reading, labelled as ours): a currency trade carries two risks, the price and the clock; Herstatt
was a clock failure, and the cure was not a better forecast but making both payments happen at once. Educational,
not advice.

Every claim, sourced (only pages opened or returned by a search in this run):
  [BIS26] Drehmann, McGuire, Shirakami, Conway and Lovell, "Uncovering FX settlement risk: new measures from the 2025
      BIS Triennial Survey", BIS Quarterly Review, 15 June 2026: "On the afternoon of 26 June 1974, the German
      authorities ordered Bankhaus Herstatt into liquidation"; "The bank was closed at 3.30 pm Frankfurt time, after
      which its New York correspondent bank ... suspended all outgoing US dollar payments from Herstatt's account";
      this "left Herstatt's counterparties exposed for the full value of the Deutsche marks ... they had already paid
      in Frankfurt earlier in the day to settle US dollar-Deutsche mark foreign exchange (FX) trades"; Herstatt risk
      "occurs when one party to an FX trade fulfils its obligation to deliver currency but does not receive the
      corresponding currency in return"; "Market participants began to delay payments until they had received
      confirmation of their counterparties' payments", bringing cross-border payments and FX trades "to a halt";
      "The turmoil subsided only after major central banks signalled their readiness to provide sufficient
      liquidity"; the BCBS "was established at the end of 1974"; the CPSS created in 1990. April 2025: "More than
      $14 trillion worth of gross financial obligations were settled on an average day"; "$5.2 trillion" (just over
      a third, 36%) via payment versus payment (PvP); "More than $1.4 trillion (10%) were settled on a gross
      bilateral basis, which is fully exposed to settlement risk"; the other methods: pre-settlement netting,
      intragroup settlement, settlement over accounts with timing controls; gross bilateral "from 32% of the average
      daily settlement in 2006 to 15% in 2025" (like for like: the 2006 survey left out intragroup settlement);
      settlement fails "only 0.01%" of obligations.
  [GALATI] Gabriele Galati, "Settlement risk in foreign exchange markets and CLS Bank", BIS Quarterly Review, December
      2002: "On 26 June 1974, at 15:30 CET, the German authorities closed Bankhaus Herstatt"; counterparties "had
      irrevocably paid large amounts of Deutsche marks to the bank but not yet received dollars in exchange"; "The
      value of transactions to be settled for Bankhaus Herstatt was estimated at $200 million"; some forward trades
      not yet due "had to be replaced"; in the multilateral net settlement system used in New York, gross funds
      transferred fell by an estimated 60% over the next three days; limited overlap in operating hours between
      time zones; PvP: "the two legs of a transaction are settled simultaneously, and in such a way that the one
      cannot occur without the other"; payments to CLS Bank "between 07:00 and 12:00 CET"; seven currencies (US
      dollar, euro, yen, pound sterling, Swiss franc, Canadian dollar, Australian dollar); "In September 2002, CLS
      Bank went into operation".
  [NORMAN] Ben Norman, "BoE archives reveal little known lesson from the 1974 failure of Herstatt Bank", Bank
      Underground (Bank of England staff blog), 24 June 2015: Herstatt "was the country's 35th biggest bank"; it had
      "sizeable losses in foreign exchange (fx) trading"; its licence was withdrawn on 26 June 1974, after close of
      banking business in Germany but still during the business day in the US; Charles Coombs (Federal Reserve Bank
      of New York), at the BIS in early July 1974: New York banks' first reaction was to hold up out payments, and
      "This had the effect of virtually freezing up the clearing process, which on two or three consecutive days ran
      until 1am".
  [BCBS] BIS, History of the Basel Committee: established "by the central bank Governors of the Group of Ten
      countries at the end of 1974", after disturbances in currency and banking markets "(notably the failure of
      Bankhaus Herstatt in West Germany)"; first meeting February 1975; first named the "Committee on Banking
      Regulations and Supervisory Practices".
  [FINVIA] Nils Wischmeyer, finvia blog: "Cologne-based Herstatt Bank" (the city only; its loss figures disagree
      with each other, so none are used).
  [CLS24] CLS, CLSSettlement for corporate treasurers (Rev Q1/0224): "18 of the most actively traded currencies".
  [TRI25] BIS press release, 30 September 2025: global FX trading hit $9.6 trillion a day in April 2025.

Labelled as ours: the New York clock time (3:30 p.m. CET, UTC+1, West Germany had no summer time in 1974, is
14:30 UTC; New York was on daylight time all year in 1974, UTC-4, so 10:30 a.m.: a five-hour gap); the working-day
bars (illustrative hours); the index of New York funds moved (100 to 40 is the BIS's estimated 60% fall drawn as an
index, not a measured series); the filmed scenes (reconstructions, nobody a portrait, nobody speaks); the reading in
the last chapter. No price, rate or loss figure for Herstatt is given: the sources do not agree on one.
Calculations (build/plans/ep011_checks.py): 15:30 at UTC+1 = 10:30 at UTC-4; 5.2 / 14 = 37% ("just over a third";
BIS rounds the share to 36% on its unrounded totals); 1.4 / 14 = 10%; 32% to 15% is "more than halved"; 2026 - 1974
= 52 ("more than fifty years"); 100 x (1 - 0.6) = 40.

    python build/youtube_ep011.py
"""

import cine_1974 as F
from cine_lib import document_shot
from youtube import make

S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)
SS = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: SC(art, txt, **opts)      # the drawing alone, its line as the heading
CINE = lambda name: dict(kind="cine", shot=F.SHOTS[name])
DOC = lambda **kw: dict(kind="cine", shot=document_shot(**kw))

EP = dict(
    slug="yt-011-herstatt",
    title="A Bank Shut at 3:30. The Banks That Had Already Paid It Never Got Their Dollars.",
    score="suspense",
    fx="action",
    held_life=True,
    thumb=dict(film_a=dict(shot=F.SHOTS["clocks_hook"], dur=12.0, t=8.5, pos="50% 45%",
                           segs=[("On the twenty sixth of June, nineteen seventy four, at half past three in the afternoon, German time, the authorities shut a bank.", .3, 7.5),
                                 ("In New York, it was half past ten in the morning.", 7.8, 11.4)]),
               film_b=dict(shot=F.SHOTS["ny_suspend"], dur=11.0, t=9.6, pos="50% 50%",
                           segs=[("In New York, the bank that held Herstatt's dollars stopped every payment out of its account.", .3, 5.4),
                                 ("The dollars stayed where they were.", 5.7, 9.0)]),
               big_a="Paid in the morning. Shut at <span style='color:#D93A12'>3:30</span>.", size_a=84,
               big="Paid in marks. <span style='color:#D93A12'>Never</span> paid in dollars.", size=84,
               small="Germany, June 26, 1974"),
    chapters=[
        dict(title="Half past three", art=("clock", dict(time="3:30")), beats=[
            dict(say="On the twenty sixth of June, nineteen seventy four, at half past three in the afternoon, German time, the authorities shut a bank in Cologne called Bankhaus Herstatt. In New York, it was half past ten in the morning.",
                 show=CINE("clocks_hook")),
            dict(say="Earlier that day, banks had paid Herstatt in Deutsche marks, for trades where Herstatt owed them dollars. The dollars were due later that day, in New York. They never came.",
                 shows=[S("notes", "Marks paid in Frankfurt.", "Earlier that day · BIS", ["marks"], 100, left="DM", right="$", lab_l="PAID", lab_r="DUE"),
                        SS("day_bars", "Dollars due later, in New York.", "Illustrative hours", ["later,"], 96, flip=True, upto=3),
                        SC("stamp", "The dollars never came", text="UNPAID")]),
            dict(say="Nobody had misjudged the price. They'd traded with a licensed bank, at the rate they'd agreed. So how do you lose the whole amount of a trade that went exactly as agreed? And why is more than a trillion dollars a day still exposed to the same gap, half a century later?",
                 shows=[S("magnifier", "Nobody misjudged the price.", "", ["price."], 100, label="RATE OK"),
                        S("handshake", "A licensed bank, the agreed rate.", "", ["agreed"], 96, flip=True, left="DM", right="$"),
                        SS("scale", "So how do you lose it all?", "", ["all?"], 100, left="PAID", right="RECEIVED", tip=0),
                        SC("bars", "Settled a day, April 2025, $ trillion: all, and with no protection (BIS, 2026)", values=[14, 1.4], labels=["ALL", "UNPROTECTED"], hi=1)]),
        ]),
        dict(title="Two payments, not one", art=("notes", dict(left="DM", right="$", lab_l="", lab_r="")), beats=[
            dict(say="A currency trade looks like one deal. You sell Deutsche marks, you buy dollars, at a rate you both agree.",
                 shows=[S("notes", "One deal.", "Sell marks, buy dollars", ["deal."], 120, left="DM", right="$", lab_l="SELL", lab_r="BUY"),
                        S("handshake", "At a rate you both agree.", "", ["agree."], 100, flip=True, left="DM", right="$")]),
            dict(say="But it settles as two separate payments. The marks move through the banking system in Germany. The dollars move through the banking system in the United States. Each currency is paid at home, in its own working day.",
                 show=CINE("two_legs")),
            dict(say="A German bank can't pay dollars in Germany. It keeps them in an account at an American bank, called its correspondent, and tells that bank when to pay them out. Herstatt's correspondent was in New York.",
                 shows=[S("bank", "Dollars live in America.", "", ["America."], 100, label="NEW YORK"),
                        S("phone", "The correspondent pays them out.", "On instruction", ["correspondent"], 96, flip=True, across=True),
                        SS("globe", "Herstatt's was in New York.", "BIS, 2026", ["New"], 100)]),
            dict(say="Frankfurt and New York were five hours apart, and their banking days barely overlapped. So the marks were paid hours before the dollars could be.",
                 shows=[SC("day_bars", "Two banking days, five hours apart (illustrative hours)", upto=2),
                        SS("hourglass72", "Hours of waiting.", "Our illustration", ["waiting."], 100, flip=True, rate="5 HRS", left="DM", right="$")]),
            dict(say="For those hours, a bank that had paid was simply trusting that the other side would pay too. That gap has a name. The BIS defines it like this: it occurs when one party to an FX trade fulfils its obligation to deliver currency but does not receive the corresponding currency in return.",
                 show=DOC(style="opinion", head="BANK FOR INTERNATIONAL SETTLEMENTS", sub="QUARTERLY REVIEW, JUNE 2026",
                          quote="occurs when one party to an FX trade fulfils its obligation to deliver currency but does not receive the corresponding currency in return",
                          hl=("fulfils its obligation", "does not receive the"), start=(2, "occurs"), wrap=40, source="Herstatt risk, as defined in BIS Quarterly Review, June 2026",
                          badge_text="Quoted from the review", seed=11)),
            dict(say="Here's an example of our own. Say a bank sells ten million marks for dollars, and pays its marks in the morning. Until the dollars arrive, what it can lose isn't a few percent on the rate. It's the whole ten million marks.",
                 shows=[S("bulb", "Our own example.", "", ["example."], 120, text="10M"),
                        S("notes", "10 million marks, paid.", "Our illustration", ["paid."], 100, flip=True, left="10M", right="$", lab_l="PAID", lab_r="WAITING"),
                        S("seesaw", "Not a few percent.", "", ["percent."], 100, left="RATE", right="ALL", tip=1),
                        SS("empty_pockets", "All 10 million.", "Our illustration", ["10"], 100, flip=True, label="DM")]),
        ]),
        dict(title="The thirty fifth biggest bank", art=("bank", dict(label="HERSTATT")), beats=[
            dict(say="Herstatt wasn't a giant. A Bank of England economist, writing in twenty fifteen, called it the country's thirty fifth biggest bank. But it had made sizeable losses trading currencies.",
                 shows=[S("bank", "Not a giant.", "", ["giant."], 110, label="HERSTATT"),
                        SS("bars", "The 35th biggest in Germany.", "Bank Underground, 2015", ["35th"], 96, flip=True, values=[9, 7, 5, 3, 2], labels=["", "", "", "", "35th"], hi=4),
                        S("tower", "Sizeable losses on currencies.", "No figure: the accounts differ", ["losses"], 96, crack=True, floors=6, label="FX")]),
            dict(say="On the twenty sixth of June, Germany's authorities withdrew its licence and ordered it into liquidation. They acted after banking business had closed in Germany, while the business day in the United States was still running.",
                 shows=[SC("stamp", "Licence withdrawn, June 26, 1974", text="CLOSED"),
                        SC("day_bars", "Closed after Germany's banking day, during New York's (illustrative hours)", upto=3)]),
            dict(say="The BIS later put the value of the trades still to be settled with Herstatt at around two hundred million dollars. That's an estimate, and it doesn't say how much of it was lost.",
                 shows=[dict(kind="number", value=200, pre="$", suf="m", label="of trades still to be settled with Herstatt, an estimate · BIS, 2002"),
                        S("magnifier", "An estimate, not a loss.", "Galati, BIS, 2002", ["estimate,"], 100, flip=True, label="~$200M")]),
        ]),
        dict(title="Mid-morning in New York", art=("phone", dict(across=True, cut=True)), beats=[
            dict(say="In New York, Herstatt's correspondent stopped every dollar payment out of Herstatt's account. The dollars stayed where they were.",
                 show=CINE("ny_suspend")),
            dict(say="So the banks that had paid their marks in Frankfurt that morning were exposed for the full value. Not for a move in the exchange rate. For everything they'd paid.",
                 shows=[S("scale", "Exposed for the full value.", "BIS, 2026", ["full"], 100, left="PAID", right="RECEIVED", tip=0),
                        SS("seesaw", "Not a move in the rate.", "", ["rate."], 100, flip=True, left="DM", right="$", tip=1),
                        dict(kind="compare", left=("If the rate moves", "Part"), right=("If they never pay", "All"), note="Our illustration: what is at risk in each case")]),
            dict(say="Some banks also had trades with Herstatt that weren't due yet. Those had to be replaced, with someone else, at whatever the market rate was by then.",
                 shows=[S("calendar", "Trades not yet due.", "Galati, BIS, 2002", ["due."], 100, day="27", month="JUN", note="1974"),
                        SS("two_ways", "Replaced, at the new rate.", "Galati, BIS, 2002", ["Replaced,"], 96, flip=True, left=("OLD TRADE", "GONE"), right=("NEW TRADE", "NEW RATE"))]),
            dict(say="Think of a bank that traded with Herstatt that morning. It had done everything right, and paid on time. Now its dollars were just a claim on a bank in liquidation.",
                 shows=[S("figures", "A bank that did everything right.", "Our illustration", ["right,"], 96, n=1, hi=0),
                        S("document", "Paid on time.", "", ["time."], 100, flip=True, title="PAID", lines=3, stamp="ON TIME"),
                        SS("ledger", "Now, a claim.", "On a bank in liquidation", ["claim"], 96, names=("Claim: $ due", "", "", ""), hi=(0,))]),
        ]),
        dict(title="Nobody pays first", art=("dominoes", dict(labels=["PAY", "WAIT", "WAIT", "WAIT"], fall=1)), beats=[
            dict(say="Then the fear spread. Banks began to hold back their own payments until they'd seen the other side's money arrive. If everyone waits to be paid first, nobody pays. In the system New York banks used to settle with each other, the money moving through it fell by an estimated sixty percent over the next three days.",
                 show=CINE("freeze")),
            dict(say="At the BIS in early July, Charles Coombs of the Federal Reserve Bank of New York described it to other central bankers. In his words, this had the effect of virtually freezing up the clearing process, which on two or three consecutive days ran until one in the morning.",
                 show=DOC(style="notice", head="BANK OF ENGLAND ARCHIVE, VIA BANK UNDERGROUND", sub="BIS, BASEL, EARLY JULY 1974",
                          quote="This had the effect of virtually freezing up the clearing process, which on two or three consecutive days ran until 1am.",
                          hl=("virtually freezing", "until 1am"), start=(1, "this had"), source="Charles Coombs, Federal Reserve Bank of New York, as quoted by B. Norman, 2015",
                          badge_text="Quoted from the archive", seed=12)),
            dict(say="A Bank of England economist who went through the archives drew a lesson from it. When one bank fails, the banks that survive may hold back their payments to each other too. One failure becomes a traffic jam for everyone.",
                 shows=[S("book", "From the archives.", "Bank Underground, 2015", ["archives."], 100, title="1974"),
                        S("queue", "Survivors hold back too.", "Norman, 2015", ["back"], 96, flip=True, n=7, label="PAYMENTS"),
                        SS("car", "A traffic jam for everyone.", "Our reading", ["jam"], 100, kicked=False)]),
            dict(say="According to the BIS, the turmoil only calmed after the major central banks signalled they were ready to provide enough liquidity. One small bank's failure had nearly stopped the world's currency payments.",
                 shows=[S("bank", "Calm, once central banks stepped in.", "BIS, 2026", ["Calm,"], 96, label="CENTRAL BANKS"),
                        SS("dominoes", "One small bank, a whole market.", "Our reading", ["whole"], 96, flip=True, labels=["HERSTATT", "BANK", "BANK", "BANK"], fall=1)]),
        ]),
        dict(title="A committee in Basel", art=("book", dict(title="BASEL")), beats=[
            dict(say="Central bankers moved within months. At the end of nineteen seventy four, the central bank governors of the Group of Ten set up a committee in Basel. It first met in February nineteen seventy five. Today it's called the Basel Committee on Banking Supervision.",
                 shows=[S("bell", "Within months.", "", ["months."], 110, label="1974"),
                        S("globe", "The Group of Ten acts.", "End of 1974 · BIS", ["Ten"], 100),
                        SS("calendar", "First meeting: February 1975.", "BIS, History of the Basel Committee", ["February"], 96, flip=True, day="1975", month="FEB", note="BASEL"),
                        S("book", "Now the Basel Committee.", "On Banking Supervision", ["Basel"], 100, title="BCBS")]),
            dict(say="But the gap in the clock took far longer to close. In nineteen ninety, central banks set up a committee on payment systems. And in September two thousand and two, a bank called CLS went into operation.",
                 shows=[S("hourglass72", "Decades to close the gap.", "", ["Decades"], 100, rate="28 YRS", left="1974", right="2002"),
                        dict(kind="timeline", title="Closing the gap", items=[("1974", "Herstatt"), ("1975", "Basel Committee meets"), ("1990", "Payments committee"), ("2002", "CLS opens")], hi=3),
                        SS("document", "2002: CLS opens.", "Galati, BIS, 2002", ["CLS"], 100, flip=True, title="CLS BANK", lines=3, stamp="2002")]),
        ]),
        dict(title="Both or neither", art=("scale", dict(left="DM", right="$", tip=0)), beats=[
            dict(say="CLS settles both legs at once. As a BIS review put it, the two legs of a transaction are settled simultaneously, and in such a way that the one cannot occur without the other.",
                 show=CINE("pvp_swap")),
            dict(say="This is called payment versus payment. If one side doesn't pay, the other side's money isn't released. Both, or neither.",
                 shows=[S("handshake", "Payment versus payment.", "PvP", ["versus"], 100, left="DM", right="$"),
                        SS("scale", "No payment, no release.", "", ["release."], 100, flip=True, left="DM", right="$", tip=0),
                        SC("stamp", "Both, or neither", text="BOTH OR NEITHER")]),
            dict(say="Each bank pays in only what it owes overall, after its trades are netted. But every trade is still settled in full, on CLS's own books.",
                 shows=[S("coins", "Pay in only the net.", "Galati, BIS, 2002", ["net"], 100, stacks=[2, 4, 6]),
                        S("ledger", "Every trade settled in full.", "On CLS's books · Galati, BIS, 2002", ["full,"], 96, flip=True, names=("DM / $  settled", "$ / ¥  settled", "£ / $  settled", "€ / $  settled"), hi=(0,))]),
            dict(say="It runs in one window each day. When it started, payments to CLS were made between seven in the morning and noon, Central European time, in seven currencies. Today it lists eighteen.",
                 shows=[SC("day_bars", "One window a day for both legs (BIS, 2002)", upto=4),
                        dict(kind="timeline", title="Payments to CLS, Central European time (BIS, 2002)", items=[("7:00", "Window opens"), ("12:00", "Window closes")], hi=1),
                        dict(kind="compare", left=("Currencies, 2002", "7"), right=("Currencies, today", "18"), note="BIS, 2002 · CLS, 2024")]),
        ]),
        dict(title="Fifty years later", art=("bars", dict(values=[14, 5.2, 1.4], labels=["ALL", "PVP", "EXPOSED"], hi=2)), beats=[
            dict(say="So is the problem solved? Not quite. In June twenty twenty six, the BIS published new measures. In April twenty twenty five, more than fourteen trillion dollars of foreign exchange payments were settled on an average day.",
                 shows=[S("magnifier", "Solved?", "", ["Solved?"], 130, label="?"),
                        S("bulb", "Not quite.", "", ["quite."], 120, flip=True, text="!"),
                        SS("document", "New measures, June 2026.", "BIS Quarterly Review", ["2026."], 96, title="BIS 2026", lines=3, stamp="NEW"),
                        SC("coins", "More than $14 trillion of FX payments settled a day, April 2025 (BIS, 2026)", stacks=[4, 6, 8])]),
            dict(say="Just over a third, five point two trillion, settled payment versus payment. But ten percent, more than one point four trillion dollars a day, was settled one payment at a time, with nothing to cover the gap. That's fully exposed to Herstatt risk.",
                 shows=[SC("bars", "Settled on an average day, April 2025, $ trillion (BIS, 2026)", values=[14, 5.2], labels=["ALL", "BOTH AT ONCE"], hi=1),
                        SC("bars", "Settled on an average day, April 2025, $ trillion (BIS, 2026)", values=[14, 5.2, 1.4], labels=["ALL", "BOTH AT ONCE", "FULLY EXPOSED"], hi=2),
                        dict(kind="number", value=1.4, dec=1, pre="$", suf="tn", label="a day fully exposed to settlement risk · BIS, 2026")]),
            dict(say="The rest was made safer in other ways: by netting trades against each other first, by settling inside the same banking group, or with controls on when payments go out.",
                 shows=[SC("ledger", "The other ways (BIS, 2026)", names=("Netting", "Same group", "Timing", ""), hi=(0, 1, 2))]),
            dict(say="And there's progress. Leaving out payments inside the same group, the share settled one payment at a time has more than halved, from thirty two percent of the total in two thousand and six, to fifteen percent in twenty twenty five.",
                 shows=[S("rocket", "Progress.", "", ["Progress."], 120),
                        SC("bars", "Settled one payment at a time, share, like for like (BIS, 2026)", values=[32, 15], labels=["2006: 32%", "2025: 15%"], hi=1)]),
            dict(say="Most days, nothing goes wrong. Failed settlements were about one hundredth of one percent of the total. The danger isn't how often it happens. It's how much is riding on the day it does.",
                 shows=[S("bricks", "Most days, nothing goes wrong.", "", ["nothing"], 100, n=31, red=0),
                        dict(kind="number", value=0.01, dec=2, suf="%", label="of obligations failed to settle, April 2025 · BIS, 2026"),
                        SS("dominoes", "Not how often.", "Our reading", ["often."], 100, flip=True, labels=["", "", "", ""], fall=0),
                        S("scale", "How much rides on the day.", "Our reading", ["rides"], 96, left="ODDS", right="AMOUNT", tip=1)]),
        ]),
        dict(title="A clock, not a forecast", art=("clock", dict(time="10:30")), beats=[
            dict(say="Here's our reading. A currency trade carries two risks. One is the price: the rate moves against you, and you lose the difference. The other is the clock: you've paid, they haven't, and in that gap you can lose the whole amount.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 130, text="2"),
                        SS("notes", "Two risks in one trade.", "", ["Two"], 100, flip=True, left="DM", right="$", lab_l="", lab_r=""),
                        S("seesaw", "Risk one: the price.", "You lose the difference", ["price."], 96, left="DM", right="$", tip=1),
                        S("clock", "Risk two: the clock.", "You can lose it all", ["clock."], 96, flip=True, time="3:30")]),
            dict(say="That's why the cure for Herstatt wasn't a better forecast. It was a better clock: making both payments happen at the same moment.",
                 shows=[S("magnifier", "Not a better forecast.", "", ["forecast."], 100, label="RATE?"),
                        SS("day_bars", "A better clock.", "Our reading", ["clock:"], 96, flip=True, upto=4)]),
            dict(say="It's tempting to file settlement risk under the back office, as plumbing. Herstatt is the reminder that when the plumbing stops, the whole market stops with it.",
                 shows=[S("server", "Just plumbing?", "", ["plumbing."], 100, lights=False),
                        SS("wall", "When it stops, everything stops.", "Our reading", ["stops"], 96, flip=True, gap=False, label="PAYMENTS")]),
            dict(say="If an interviewer asks you what Herstatt risk is, here's a short answer. It's paying your side of a currency trade and not receiving theirs, because the two payments settle at different times. This is education, not financial advice.",
                 shows=[S("document", "What is Herstatt risk?", "Interview prep", ["Herstatt"], 100, title="Q: HERSTATT?", lines=3, stamp="2 LEGS"),
                        dict(kind="list", title="The short answer", items=["You pay your side", "Theirs never arrives", "Two payments, two times"]),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. If you had to choose, would you rather pay first and trust, or wait to be paid and risk losing the deal? Tell us in the comments.",
                 shows=[S("bulb", "Our question for you.", "", ["question"], 110, text="?"),
                        SC("seesaw", "Pay first, or wait?", left="PAY FIRST", right="WAIT", tip=0),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "26 June 1974, half past three in the afternoon in Germany. The authorities shut Bankhaus Herstatt. Earlier that day, banks "
        "around the world had paid it Deutsche marks for dollars it was due to pay them later that day in New York. The dollars never came.\n\n"
        "Nobody had misjudged a price. So how do you lose the whole amount of a trade that went exactly as agreed? We'll show why a "
        "currency trade settles as two payments in two countries, why five hours between Frankfurt and New York mattered, what happened "
        "when Herstatt's New York correspondent stopped its payments, and how fear nearly froze New York's clearing for days. Then the fix: the "
        "Basel Committee, and decades later CLS and payment versus payment, both legs at once or neither.\n\n"
        "And the twist: the BIS's 2026 figures show more than $1.4 trillion a day still settled one payment at a time, fully exposed to "
        "the same risk. We'll end with our reading: a trade has two risks, the price and the clock. Would you rather pay first or wait? Tell us below."),
    sources=[
        ("BIS Quarterly Review, June 2026: Uncovering FX settlement risk (Drehmann, McGuire, Shirakami, Conway, Lovell)", "https://www.bis.org/publ/qtrpdf/r_qt2606c.htm"),
        ("BIS Quarterly Review, December 2002: Settlement risk in foreign exchange markets and CLS Bank (Galati)", "https://www.bis.org/publ/qtrpdf/r_qt0212f.pdf"),
        ("Bank Underground (Bank of England staff blog), BoE archives reveal little known lesson from the 1974 failure of Herstatt Bank (Norman, 2015)", "https://bankunderground.co.uk/2015/06/24/boe-archives-reveal-little-known-lesson-from-the-1974-failure-of-herstatt-bank/"),
        ("BIS, History of the Basel Committee", "https://www.bis.org/bcbs/history.htm"),
        ("BIS CPSS, Settlement risk in foreign exchange transactions (1996)", "https://www.bis.org/cpmi/publ/d17.htm"),
        ("BIS press release, Global FX trading hits $9.6 trillion a day in April 2025", "https://www.bis.org/press/p250930.htm"),
        ("CLS, CLSSettlement for corporate treasurers (2024)", "https://www.cls-group.com/media/mzmerdhw/clssettlement_corporate_treasurers_feb2024_v1ind.pdf"),
        ("finvia, The death of a bank that almost ruined Cologne (Wischmeyer)", "https://finvia.fo/en/knowledge/blog/article/der-tod-einer-bank-der-fast-ganz-koln-ins-verderben-sturzte"),
    ],
    source_note="We drew the filmed scenes ourselves. They're stylised reconstructions, not the real banks or anyone's portrait, and "
                "nobody in them speaks. The New York clock time (10:30 a.m.) is our calculation from the 3:30 p.m. German closing time; "
                "the working-day bars use illustrative hours; the falling index on the dealing-room board draws the BIS's estimated 60% "
                "fall, not a measured series. We give no loss figure for Herstatt because the accounts we found don't agree on one. The "
                "reading in the last chapter is ours, so feel free to disagree with it.",
    hashtags=["FinanceHistory", "Banking", "Forex"],
    tags=["Herstatt", "Herstatt risk", "Bankhaus Herstatt 1974", "settlement risk", "FX settlement risk", "CLS Bank",
          "payment versus payment", "Basel Committee history", "foreign exchange explained", "banking crisis 1974",
          "BIS triennial survey", "financial history", "investment banking interview", "how FX trades settle"],
)

if __name__ == "__main__":
    make(EP)
