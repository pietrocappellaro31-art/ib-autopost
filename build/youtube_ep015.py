"""
YouTube #15 (22 Nov 2026): Barings, February 1995. One trader in Singapore lost £827 million; his bank's recorded
capital was in the order of £350 million. How did a 233-year-old bank keep sending him the money? Banking scandals,
risk management, derivatives (futures, selling options), segregation of duties. Made to
docs/production/long-form-standard.md, the 18 Nov decision (open on the hook, the number on screen in the first
frame; title and thumbnail on the same number) and the 22 Nov decision (at least 1% better than #14, measured).
Visual plan: build/plans/ep015.md. Score: suspense (style and key: score.pick's slot for the long film).

Point of view (our reading, labelled as ours): it is told as the story of one rogue trader, but it needed a bank that
sent money without asking what it was for; a business sold as low risk was reporting large profits, and nobody who
could have checked it did. Educational, not advice.

Every claim, sourced (only pages opened or returned by a search in this run):
  [H18] Hansard, House of Commons, 18 July 1995, vol 263 cc1454-73, "Barings" (the Chancellor, Kenneth Clarke, on the
      Board of Banking Supervision's report): "By the end of 1993, the cumulative loss was more than £20 million";
      "by the end of 1994, it was more than £200 million."; "after the collapse on 26 February, the cumulative loss was
      a staggering £827 million."; "His deception was made easier as he was not only a trader but was in charge of the
      so-called back office"; "some information on the account that he used to hide his losses was available to
      London, but it was never analysed."; "The money required to fund the losses came primarily from London.";
      "Barings management in London seem generally to have believed that the money being sent to Singapore was being
      lent to clients to facilitate their trading."; "Barings management did not question why they were apparently
      lending more than £300 million to clients to trade when they had collateral of only about £31 million from
      clients for those trades."; "In 1994, Barings' internal auditors recommended that, as a trader, he should not
      have this responsibility for the back office." "Barings failed to implement that recommendation."; "No one in
      Barings accepted responsibility for Leeson's activities for the whole of 1994."
  [RBA] Reserve Bank of Australia, Bulletin, November 1995, "Implications of the Barings Collapse for Bank
      Supervisors" (a summary of the Board of Banking Supervision's report): Leeson was authorised to trade "only as
      part of a 'switching' (or arbitrage) operation between the Singaporean and Osaka futures exchanges", "viewed as
      low-risk operations by Barings management, given that they did not involve outright, open positions";
      unauthorised positions for 2 1/2 years: "long (or bought) positions in Nikkei futures", "short (or sold)
      positions in JGB futures" and "a 'short volatility' position in Nikkei exchange traded options", which required
      "for volatility in the Nikkei Index to have remained low"; "As general manager of the company, Leeson
      effectively controlled both sides of the trading operation."; "over 60 per cent of the revenues of its worldwide
      derivatives operations" from his arbitrage; the draft 1994 accounts showed "pre-tax profit of £102 million";
      "At that point, recorded Group capital was in the order of £350 million." (end December 1994); "funding to BFS
      represented twice Barings Group capital"; management "did not question, nor did it control or place limits on,
      the high, ongoing levels of funding"; "reaching £827 million by 27 February 1995"; "On 26 February 1995,
      administrators were appointed"; "virtual total failure of risk management systems and controls, and managerial
      confusion"; "clear segregation of duties is fundamental to any effective control system"; "the failings at
      Barings could not be attributed to the complexity of the business".
  [NLB] National Library Board Singapore, Infopedia, "Collapse of Barings" (Kong Yoke Mun): "Founded in 1762, Barings
      was the oldest merchant bank in Britain"; "Leeson arrived in Singapore in April 1992"; "On 3 July, Leeson
      opened an error account, 88888"; "originally opened to report error trades made by inexperienced staff";
      "appointed assistant director and general manager of BFS on 28 June 1993"; "the Nikkei plunged after an
      earthquake hit Kobe, Japan, on 17 January."; "When the Nikkei 225 dropped to 17,785 points on 23 January";
      "hoping that it would not fall below 19,000 points"; SIMEX alerted Barings in January 1995 to BFS's large
      volume of Nikkei futures and options and senior management assured SIMEX it had enough to back the trades;
      "On 23 February 1995, a senior settlements clerk on secondment from the Barings head office in London spotted
      a discrepancy"; "Leeson fled to Kuala Lumpur with his wife on the night of 23 February"; ING "completed the
      Barings takeover proceedings on 6 March, injecting £540 million to pay creditors"; "sentenced to six and a half
      years of imprisonment in Singapore for two charges of fraud and forgery" (1 December 1995).
  [H27] Hansard, House of Commons, 27 February 1995, vol 255 cc693-705: "The losses arise from contracts on the
      Singapore, Osaka and Tokyo exchanges."
  [GOV] GOV.UK, "Report into the collapse of Barings Bank", Board of Banking Supervision, 18 July 1995 (HC 673).
  [FIA] FIA MarketVoice, "25 years ago, Barings offers a hard lesson in risk controls" (26 February 2020).

Labelled as ours: the £1 a day, 99 calm days and £150 payout example (build/plans/ep015_checks.py); the filmed
rooms, the trading floor, the back office, the London room and its easel (illustrations and reconstructions: nobody
is a portrait or a likeness, nobody speaks); "more than twice its capital" is our arithmetic on [RBA]'s two figures
(827 / 350 = 2.36); "hundreds of millions still to pay" is 827 - 350; the readings in the last chapters.

    python build/youtube_ep015.py
"""

import cine_1995 as F
from cine_lib import document_shot
from youtube import make

S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)
SS = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: SC(art, txt, **opts)
CINE = lambda name: dict(kind="cine", shot=F.SHOTS[name])
DOC = lambda **kw: dict(kind="cine", shot=document_shot(**kw))
HAN = "Hansard, July 18, 1995"
RBA = "Reserve Bank of Australia, 1995"

EP = dict(
    slug="yt-015-barings-827-million",
    title="One Trader Lost £827 Million. His Bank Had About £350 Million.",
    score="suspense",
    score_key="G",            # 22 Nov: the Short of the same day drew E in parallel (score.pick reserves per session); G is in none of the last three and no other video of today
    hook_first=True,
    fx="action",
    held_life=True,
    text_life=True,
    thumb=dict(film_a=dict(shot=F.SHOTS["hook_827"], dur=12.0, t=11.4, pos="60% 55%",
                           segs=[("One trader in Singapore lost eight hundred and twenty seven million pounds.", .3, 4.2),
                                 ("His bank's capital was about three hundred and fifty million.", 4.4, 7.4),
                                 ("So how did a bank two hundred and thirty three years old keep sending him the money?", 7.6, 11.6)]),
               film_b=dict(shot=F.SHOTS["capital_2"], dur=12.0, t=6.5, pos="70% 45%",
                           segs=[("Put the losses on the books, and the capital is gone, with hundreds of millions still to pay.", .3, 5.5)]),
               big_a="<span style='color:#D93A12'>£827M</span> lost by one trader", size_a=104,
               big="<span style='color:#D93A12'>£827M</span>. Capital gone.", size=100,
               small="Barings, 1995"),
    chapters=[
        dict(title="One trader, one bank", art=("tower", dict(crack=True, floors=7, label="1762")), beats=[
            dict(say="One trader in Singapore lost eight hundred and twenty seven million pounds. His bank's capital was about three hundred and fifty million. So how did a bank two hundred and thirty three years old keep sending him the money?",
                 show=CINE("hook_827")),
            dict(say="The trader was Nick Leeson. The bank was Barings, founded in seventeen sixty two, the oldest merchant bank in Britain. By the end, his losses were more than twice its capital.",
                 show=CINE("pit_floor")),
            dict(say="This film follows the money from London to Singapore. An account nobody read, a bet that won small and lost big, and the earthquake that ended it.",
                 shows=[S("magnifier", "Follow the money.", "", ["money."], 104, label="£"),
                        dict(kind="list", title="In this film", items=["An account nobody read", "Win small, lose big", "The earthquake, and the weekend"])]),
        ]),
        dict(title="The error account", art=("calendar", dict(day="3", month="JUL", note="1992")), beats=[
            dict(say="Leeson arrived in Singapore in April nineteen ninety two, to work for Barings on the futures exchange. On the third of July, he opened an error account, number eight eight eight eight eight.",
                 show=CINE("acct_88888")),
            dict(say="An error account is for mistakes. If a trade goes wrong, say a buy that should have been a sell, it's parked there until it's put right. This one was opened for errors made by inexperienced staff.",
                 shows=[S("document", "For mistakes.", "", ["mistakes."], 104, title="ERRORS", lines=4, stamp="88888"),
                        dict(kind="term", term="Error account", text="where wrong trades are parked until they're put right."),
                        SS("stamp", "Opened for inexperienced staff's errors", text="ERROR")]),
            dict(say="Barings let him trade, but only one kind of business: switching between the Singapore and Osaka exchanges. Buy where it's a little cheaper, sell where it's a little dearer, and hold no open bet. Management saw it as low risk.",
                 shows=[SC("seesaw", "Switching: the same contract on two exchanges", left="SINGAPORE", right="OSAKA", tip=1),
                        dict(kind="flow", title="Switching, as Barings saw it", items=[("coin", "Buy a little cheaper"), ("doc", "Sell a little dearer"), ("scales", "No open bet")]),
                        S("scale", "Seen as low risk.", RBA, ["low"], 96, flip=True, left="RISK", right="PROFIT", tip=1)]),
        ]),
        dict(title="Two jobs", art=("handshake", dict(left="TRADES", right="CHECKS")), beats=[
            dict(say="In June nineteen ninety three, he was made general manager of the Singapore futures company. He ran the trading. And he also ran the back office, the people who record and check the trades.",
                 shows=[S("figures", "General manager.", "June 1993", ["manager."], 100, n=4, hi=0),
                        dict(kind="split", left=("doc", "Front office", "Makes the trades"), right=("scales", "Back office", "Records and checks them")),
                        SS("handshake", "One person, both sides.", left="TRADES", right="CHECKS")]),
            dict(say="A trader who checks his own trades can hide what he likes. The Chancellor later told Parliament what happened. In nineteen ninety four, Barings' internal auditors recommended that, as a trader, he should not have this responsibility for the back office. Barings failed to implement that recommendation.",
                 show=DOC(style="opinion", head="HOUSE OF COMMONS", sub="THE CHANCELLOR'S STATEMENT, JULY 18, 1995",
                          quote="In 1994, Barings' internal auditors recommended that, as a trader, he should not have this responsibility for the back office. Barings failed to implement that recommendation.",
                          hl=("not have this responsibility", "failed to implement"), start=(2, None), wrap=40,
                          source="Kenneth Clarke, Chancellor of the Exchequer, Hansard vol 263", badge_text="Quoted from Hansard", seed=51)),
            dict(say="So until the end, one man still made the trades. And he kept the records of them.",
                 shows=[S("stamp", "Not implemented.", HAN, ["implemented."], 104, text="1994"),
                        S("tower", "Both sides, one man.", "", ["one"], 96, flip=True, crack=True, floors=5, label="BFS")]),
        ]),
        dict(title="The account nobody read", art=("ledger", dict(names=("88888  1993  £20M+", "88888  1994  £200M+", "PROFIT  1994  £102M", "?"), hi=(0, 1))), beats=[
            dict(say="He used the account to hide losses. By the end of nineteen ninety three, the losses in it came to more than twenty million pounds. By the end of nineteen ninety four, more than two hundred million.",
                 show=CINE("hidden_1")),
            dict(say="None of it was in Barings' accounts. The draft accounts for nineteen ninety four showed a pre tax profit of a hundred and two million pounds. And his business was credited with over sixty percent of the revenue of Barings' derivatives operations worldwide.",
                 show=CINE("hidden_2")),
            dict(say="Some information on the account was available to London. In the Chancellor's words, it was never analysed.",
                 shows=[S("document", "Available to London.", HAN, ["London."], 100, title="88888", lines=5, stamp="UNREAD"),
                        SS("magnifier", "Never analysed", label="?")]),
            dict(say="In our reading, that was the warning. A business sold as low risk was reporting very large profits. Low risk and large profits rarely come together.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 110, text="!"),
                        SS("seesaw", "Low risk, large profits?", "", (), 96, flip=True, left="LOW RISK", right="BIG PROFIT", tip=1),
                        dict(kind="statement", text="Low risk and large profits rarely come together.", hl=["rarely"], size=76)]),
        ]),
        dict(title="Win small, lose big", art=("seesaw", dict(left="99 DAYS", right="DAY 100", tip=1)), beats=[
            dict(say="So what was he actually doing? The Reserve Bank of Australia's summary of the official report lists three big positions: he'd bought Nikkei futures, sold Japanese government bond futures, and sold options on the Nikkei.",
                 shows=[SS("magnifier", "Three positions (RBA summary, 1995)", label="3"),
                        dict(kind="list", title="His unauthorised positions", items=["Bought Nikkei futures", "Sold Japanese government bond futures", "Sold options on the Nikkei"])]),
            dict(say="A future is a deal to buy or sell later at a price fixed today. His Nikkei futures made money if Japanese shares rose, and lost money if they fell.",
                 shows=[S("handshake", "A price fixed today.", "", ["today."], 100, left="NOW", right="LATER"),
                        SC("arrows", "His bought Nikkei futures", up="SHARES UP: GAIN", down="SHARES DOWN: LOSS")]),
            dict(say="The options were different. Selling an option is a bit like selling insurance. Here's our own example. You collect one pound a day, as long as the market stays calm. After ninety nine calm days, you're up ninety nine pounds.",
                 show=CINE("tally_1")),
            dict(say="On day one hundred, the market jumps, and you have to pay out a hundred and fifty. You were right ninety nine days out of a hundred, and you're down fifty one pounds.",
                 show=CINE("tally_2")),
            dict(say="That's the shape of the bet. Most days it pays a little. Once in a while, it costs far more than all the little payments put together.",
                 shows=[SC("seesaw", "Our example: the shape of the bet", left="MANY SMALL WINS", right="ONE BIG LOSS", tip=1)]),
            dict(say="The Reserve Bank calls his options a short volatility position. It needed the Nikkei to stay calm. And his futures needed it not to fall.",
                 shows=[dict(kind="term", term="Short volatility", text="a bet that a market stays calm. Win small, often. Lose big, once."),
                        SS("seesaw", "Calm days win; one jump loses", left="99 CALM DAYS", right="1 JUMP", tip=1),
                        S("dominoes", "And not falling.", "", ["falling."], 96, flip=True, labels=("CALM", "FLAT", "UP", "?"))]),
        ]),
        dict(title="London pays", art=("bank", dict(label="LONDON")), beats=[
            dict(say="Futures exchanges ask for cash, called margin, to cover losses as they happen. The money to fund Leeson's losses came primarily from London. Barings' management there seems to have believed it was being lent to clients.",
                 show=CINE("funding_1")),
            dict(say="Here's how margin works. Each day, the exchange works out who gained and who lost on every contract, and the losers pay in cash. So a bet that loses a lot needs a lot of cash, quickly.",
                 shows=[S("calendar", "Every day.", "", ["day."], 100, day="1", month="DAY", note="SETTLED"),
                        dict(kind="flow", title="Margin, day by day", items=[("doc", "Every contract valued"), ("scales", "Gains and losses worked out"), ("coin", "Losers pay in cash")]),
                        S("coins", "A lot of cash, quickly.", "", ["quickly."], 96, flip=True)]),
            dict(say="In the Chancellor's account, they did not question why they were apparently lending more than three hundred million pounds to clients, who had put up collateral of only about thirty one million.",
                 show=CINE("funding_2")),
            dict(say="Nobody put limits on the funding. Just before the collapse, the money sent to the Singapore company was twice the capital of the whole Barings group.",
                 shows=[SS("coins", "No limits on the funding (RBA, 1995)"),
                        SC("bars", "Funding to the Singapore company against group capital (RBA, 1995; capital = 1)", values=[2, 1], labels=["FUNDING TO SINGAPORE: 2x", "GROUP CAPITAL: 1x"], hi=0)]),
            dict(say="And for the whole of nineteen ninety four, the Chancellor told Parliament, no one in Barings accepted responsibility for Leeson's activities.",
                 show=DOC(style="opinion", head="HOUSE OF COMMONS", sub="THE CHANCELLOR'S STATEMENT, JULY 18, 1995",
                          quote="No one in Barings accepted responsibility for Leeson's activities for the whole of 1994.",
                          hl=("No one", "responsibility"), start=(0, "no one"), wrap=36,
                          source="Kenneth Clarke, Chancellor of the Exchequer, Hansard vol 263", badge_text="Quoted from Hansard", seed=52)),
        ]),
        dict(title="Kobe", art=("calendar", dict(day="17", month="JAN", note="1995")), beats=[
            dict(say="On the seventeenth of January, nineteen ninety five, an earthquake hit Kobe, in Japan. The Nikkei fell. On the twenty third of January, it was at seventeen thousand, seven hundred and eighty five points.",
                 show=CINE("kobe_fall")),
            dict(say="Leeson kept betting, hoping it would not fall below nineteen thousand. In our reading, every fall cost his futures money, and his options too, because the market was no longer calm.",
                 shows=[SC("dominoes", "Our reading: one move, two losses", labels=("QUAKE", "NIKKEI DOWN", "FUTURES LOSE", "OPTIONS LOSE")),
                        S("ticker", "Below nineteen thousand.", "Singapore's National Library", ["nineteen"], 96, flip=True, price="17,785", change="23 JAN", up=False)]),
            dict(say="That month, the Singapore exchange, SIMEX, alerted Barings to the size of its trading in Nikkei futures and options. Barings' senior management assured the exchange it had enough to back the trades.",
                 shows=[SS("bell", "January 1995: the exchange asked", label="SIMEX"),
                        S("handshake", "Enough to back the trades.", "Singapore's National Library", ["back"], 96, flip=True, left="SIMEX", right="BARINGS")]),
        ]),
        dict(title="The weekend", art=("calendar", dict(day="26", month="FEB", note="1995")), beats=[
            dict(say="On the twenty third of February, a settlements clerk from Barings' London office spotted a discrepancy. That night, Leeson left for Kuala Lumpur with his wife.",
                 shows=[S("magnifier", "A discrepancy.", "February 23, 1995", ["discrepancy."], 104, label="?"),
                        SS("suitcase", "That night, he left", n=2)]),
            dict(say="By the twenty seventh of February, the hidden losses had reached eight hundred and twenty seven million pounds. At the end of nineteen ninety four, Barings' recorded capital had been in the order of three hundred and fifty million.",
                 show=CINE("capital_1")),
            dict(say="Put the losses on the books, and the capital is gone, with hundreds of millions still to pay.",
                 show=CINE("capital_2")),
            dict(say="When the Chancellor spoke to the House of Commons on the twenty seventh, he said that deposits at Barings were, for the moment, frozen.",
                 shows=[S("bank", "Deposits frozen.", "Hansard, February 27, 1995", ["frozen."], 104, label="FROZEN")]),
            dict(say="On Sunday the twenty sixth of February, administrators were appointed. In March, the Dutch bank ING completed a takeover, putting in five hundred and forty million pounds to pay creditors.",
                 shows=[dict(kind="timeline", title="Three dates (Singapore's National Library; RBA)", items=[("23 FEB", "A discrepancy"), ("26 FEB", "Administrators"), ("6 MAR", "ING takes over")], hi=1),
                        dict(kind="number", value=540, pre="£", suf="m", label="put in by ING to pay creditors · Singapore's National Library")]),
        ]),
        dict(title="Why it happened", art=("magnifier", dict(label="WHY?")), beats=[
            dict(say="The Board of Banking Supervision reported in July nineteen ninety five. In the Reserve Bank's summary, its answer was a virtual total failure of risk management systems and controls, and managerial confusion.",
                 shows=[S("document", "The official report.", "July 1995", ["report."], 100, title="REPORT", lines=5, stamp="1995"),
                        dict(kind="term", term="The finding", text="virtual total failure of risk management systems and controls, and managerial confusion. RBA summary, 1995")]),
            dict(say="The failings, it found, could not be blamed on the complexity of the business. And one of its lessons was simple. Clear segregation of duties is fundamental to any effective control system.",
                 shows=[S("tower", "Not the complexity.", RBA, ["complexity."], 96, crack=True, floors=6, label="BARINGS"),
                        SS("scale", "Separate the duties.", "", (), 96, flip=True, left="TRADE", right="CHECK", tip=0),
                        dict(kind="statement", text="Clear segregation of duties is fundamental to any effective control system.", hl=["segregation"], size=70)]),
            dict(say="Leeson pleaded guilty in Singapore to two charges, of fraud and forgery. In December nineteen ninety five, he was sentenced to six and a half years in prison.",
                 shows=[S("stamp", "Six and a half years.", "Singapore's National Library", ["years."], 104, text="1995"),
                        dict(kind="number", value=6.5, dec=1, suf=" years", label="the sentence, Singapore, December 1, 1995 · Singapore's National Library")]),
            dict(say="In July, the Chancellor told the House that the collapse had led to loss for a number of investors in Barings.",
                 shows=[S("empty_pockets", "Loss for investors.", HAN, ["investors."], 100, label="INVESTORS")]),
            dict(say="It's often told as the story of one rogue trader. Our reading is that it also needed a bank that sent money without asking what it was for. One person did the trading, and many people didn't check it.",
                 shows=[S("myth_stamp", "One rogue trader?", "", ["rogue"], 100),
                        SS("figures", "Many people didn't check.", "Our reading", (), 96, flip=True, n=6, hi=0),
                        dict(kind="statement", text="One person did the trading. Many people didn't check it.", hl=["check"], size=76)]),
        ]),
        dict(title="Who checks the checker", art=("scale", dict(left="TRADES", right="CHECKS", tip=0)), beats=[
            dict(say="If an interviewer asks why segregation of duties matters, here's a short answer. The person who makes a trade should never be the one who records it, settles it, or pays for it. Otherwise one mistake, or one lie, can grow for years. This is education, not financial advice.",
                 shows=[S("document", "Why separate the duties?", "Interview prep", ["separate"], 100, title="Q: DUTIES?", lines=3, stamp="1995"),
                        dict(kind="list", title="The short answer", items=["The trader trades", "Someone else records and settles", "Someone else pays"]),
                        SS("dominoes", "Or one lie grows for years.", "", (), 96, flip=True, labels=("1992", "1993", "1994", "1995")),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. If one desk is making most of a bank's profit, what would you check first? Tell us in the comments.",
                 shows=[S("bulb", "Our question for you.", "", ["question"], 110, text="?"),
                        SC("seesaw", "One desk, most of the profit", left="ONE DESK", right="THE REST", tip=0),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "One trader in Singapore lost £827 million. His bank's recorded capital was about £350 million. So how did "
        "Barings, the oldest merchant bank in Britain, keep sending him the money?\n\n"
        "We'll follow it from the error account Nick Leeson opened in July 1992, account 88888, to the weekend in "
        "February 1995 when the losses wiped out the bank's capital. On the way, you'll see why a trader who also ran the back office could "
        "hide what he liked, how a business sold as low risk reported large profits, what selling options has in common "
        "with selling insurance (win small, often; lose big, once), why London kept paying, and what the earthquake at "
        "Kobe did to his bets. We'll finish with what the official inquiry found and our reading of the lesson. If one desk "
        "is making most of a bank's profit, what would you check first? Tell us below."),
    sources=[
        ("Hansard, House of Commons, 18 July 1995, Barings (the Chancellor's statement on the Board of Banking Supervision report)",
         "https://api.parliament.uk/historic-hansard/commons/1995/jul/18/barings"),
        ("Reserve Bank of Australia, Bulletin, November 1995, Implications of the Barings Collapse for Bank Supervisors",
         "https://www.rba.gov.au/publications/bulletin/1995/nov/1.html"),
        ("National Library Board Singapore, Infopedia, Collapse of Barings",
         "https://eresources.nlb.gov.sg/infopedia/articles/SIP_1531_2009-06-11.html"),
        ("Hansard, House of Commons, 27 February 1995, Barings",
         "https://api.parliament.uk/historic-hansard/commons/1995/feb/27/barings"),
        ("GOV.UK, Report into the collapse of Barings Bank (Board of Banking Supervision, 18 July 1995)",
         "https://www.gov.uk/government/publications/report-into-the-collapse-of-barings-bank"),
        ("FIA MarketVoice, 25 years ago, Barings offers a hard lesson in risk controls (26 February 2020)",
         "https://www.fia.org/marketvoice/articles/25-years-ago-barings-offers-hard-lesson-risk-controls"),
    ],
    source_note="We drew the filmed scenes ourselves. The trading floor, the back office, the London room and the screens and "
                "easel in them are our illustrations and stylised reconstructions. They aren't the real exchange, offices or "
                "people, nobody in them is a portrait or a likeness, and nobody speaks. The £1 a day insurance example is ours, "
                "it isn't Barings' numbers. \"More than twice its capital\" is our arithmetic on the Reserve Bank of Australia's two "
                "figures (£827 million against capital in the order of £350 million). The readings in the last chapters are "
                "ours, so feel free to disagree with them. This channel is educational and isn't affiliated with, or endorsed "
                "by, any bank, exchange, regulator or company named in it.",
    hashtags=["Barings", "NickLeeson", "FinanceHistory"],
    tags=["Barings Bank", "Nick Leeson", "Barings collapse 1995", "rogue trader", "account 88888", "Nikkei futures",
          "Kobe earthquake 1995", "short volatility", "selling options explained", "segregation of duties",
          "risk management", "SIMEX", "investment banking interview", "financial history"],
)

if __name__ == "__main__":
    make(EP)
