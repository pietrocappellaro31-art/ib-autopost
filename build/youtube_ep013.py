"""
YouTube #13 (19 Nov 2026): GameStop, January 2021. On 31 December 2020 the shares of GameStop sold short came to
109% of all the shares the company had. Within four weeks the price went from a little under $20 to an intraday
high of $483, and on that day some trading apps stopped their customers buying it. How can more than all of a
company be sold short, and why did a 5:11 a.m. notice switch off the buy button? Financial markets, short selling,
market plumbing (clearing and settlement), behavioural finance. Made to docs/production/long-form-standard.md and
the 18 Nov decision (open on the hook, number on screen in the first frame; title and thumbnail on the same number).
Visual plan: build/plans/ep013.md. Score: suspense (style and key: see EP below).

Point of view (our reading, labelled as ours): 109% is what lending a lent share produces, not an error; the buy
button went grey over a clearing deposit sized to the risk of unsettled trades; the SEC staff found the rally was
sustained by buyers who wanted the stock more than by short sellers forced to cover. Educational, not advice.

Every claim, sourced (only pages opened or returned by a search in this run):
  [SEC] SEC Staff Report on Equity and Options Market Structure Conditions in Early 2021 (October 2021): GME short
      interest "hitting its high of 109.26% on December 31, 2020" (p. 26; short interest over shares outstanding,
      p. 25); "Short interest can exceed 100%—as it did with GME—when the same shares are lent multiple times by
      successive purchasers." (p. 26); "Short selling involves the sale of a stock that the seller does not own."
      (p. 25, n. 74); GME discussed on "the subreddit WallStreetBets", "had already started to receive attention on
      Reddit in 2019" (pp. 18-19); "By the end of 2020, GME traded for a little under $20 per share." (p. 18); 2020
      average daily volume about 6.7 million shares (p. 18, n. 55); 22 Jan 2021 "the price of GME rose from $43 to
      $72 ... in approximately three hours" (p. 19), volume 197.2 million shares that day (p. 20); 27 Jan close "a
      high of $347.51" (p. 19); unique accounts trading GME "nearly 900,000" by 27 Jan (p. 21); 40 LULD trading pauses
      in January 2021 against one in 2020 (p. 40, Table 1); "some funds had closed out their short positions in meme
      stocks, realizing significant losses" (p. 23); 27 Jan NSCC "intraday margin calls from 36 clearing members
      totaling $6.9 billion" (p. 32); ECP waived for all members on 28 Jan (p. 32); one broker-dealer restricted all
      new customer purchases in eight securities, "position-closing-only" (p. 35; some investors could only sell,
      n. 88); 28 Jan intraday high $483.00 (p. 19), open $265.00 and close $193.60 (p. 36); "By February 3, GME's price
      was below $100 per share, and fell as low as $40.59 by February 19" (p. 22); buying to cover "likely contributed
      to increases in GME's price" in some periods but "such buying was a small fraction of overall buy volume" and
      "it was the positive sentiment, not the buying-to-cover, that sustained the weeks-long price appreciation of
      GameStop stock." (pp. 26-27); "the price of GME rose as the short interest decreased" 22-27 Jan (p. 27);
      "One method to mitigate the systemic risk posed by such entities ... is to shorten the settlement cycle."
      (p. 45); T+2 defined (p. 5).
  [TEN] Vlad Tenev, Robinhood, written testimony to the House Financial Services Committee, 18 February 2021:
      automated NSCC notice at "approximately 5:11 a.m. EST on January 28"; deficit "approximately $3 billion"; VaR
      charge "nearly $1.3 billion (up from $696 million)" plus an "excess capital premium charge" of "over $2.2
      billion", triggered because "the amount of the NSCC VaR charge exceeded the amount of net capital"; restrictions
      decided "Between 6:30 and 7:30 am EST"; NSCC cut the premium, then shortly after 9:00 a.m. waived it for the
      day: revised requirement "approximately $1.4 billion", met with "approximately $737 million" deposited on top of
      the $696 million already on deposit; T+2 settlement period and collateral.
  [T1] SEC press release 2023-29, 15 February 2023: the standard settlement cycle shortened from two business days to
      one (T+1); compliance date 28 May 2024; Chair Gensler: one of the areas staff recommended "in response to the
      meme stock events of 2021".
  [FOX] Fox Business, 1 February 2021, "Melvin Capital, hedge fund that bet against GameStop, lost 53% in January"
      (from "a source familiar with the matter"; the WSJ first reported it); Citadel and Point72 pledged $2.75 billion.

Labelled as ours: the $20 / $10 / $50 short sale; the company with 100 shares and the lending chain (the mechanism is
[SEC] p. 26; the people are our illustration); the app on screen (no real app); the filmed rooms (reconstructions,
nobody is a portrait, nobody speaks); "fewer days of trades to cover" (our reading of [SEC] p. 45); the readings in
chapters 6 and 8. "29 times the average day" is our arithmetic.
Calculations (build/plans/ep013_checks.py): 197.2 / 6.7 = 29.4 ("about 29 times"); 483 / 20 = 24.15 (from a little
under $20); 696 + 737 = 1,433 (about $1.4bn); 1.3 + 2.2 = 3.5 (with ~0.7 on deposit: a shortfall of about 3);
20 - 10 = 10, 50 - 20 = 30; 100 lent and sold twice = 200 short, 300 counted as owned; 72 / 43 = 1.67.

    python build/youtube_ep013.py
"""

import cine_2021 as F
from cine_lib import document_shot
from youtube import make

S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)
SS = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: SC(art, txt, **opts)      # the drawing alone, its line as the heading
CINE = lambda name: dict(kind="cine", shot=F.SHOTS[name])
DOC = lambda **kw: dict(kind="cine", shot=document_shot(**kw))
SEC = "SEC staff report, 2021"

EP = dict(
    slug="yt-013-gamestop-109",
    title="109% of GameStop Was Sold Short. How Is That Possible?",
    score="suspense",
    # 19 Nov: the transition day of score.pick's daily slots. The slot for today's film (solo piano in Bb) repeats
    # yesterday's Reel B style and #12's key, because yesterday's runs were picked the old way; so for this one film:
    # the one style none of the last three videos used and none of today's other slots takes, in a key also unused.
    score_style="noir_jazz",
    score_key="D",
    hook_first=True,
    fx="action",
    held_life=True,
    text_life=True,
    thumb=dict(film_a=dict(shot=F.SHOTS["hook_109"], dur=12.0, t=1.9, pos="70% 40%",
                           segs=[("On the last day of twenty twenty, more GameStop shares had been sold short than the company had in existence.", .3, 5.0),
                                 ("A hundred and nine percent of them.", 5.2, 7.2),
                                 ("How can you sell more of something than exists?", 7.4, 10.0)]),
               film_b=dict(shot=F.SHOTS["lend_twice_2"], dur=15.0, t=14.5, pos="50% 30%",
                           segs=[("And the second investor's broker can lend them out again.", .3, 2.9),
                                 ("A second short seller borrows them, and sells them to a third investor.", 3.1, 6.7),
                                 ("There are still only a hundred shares.", 6.9, 8.7),
                                 ("But two hundred have been sold short, and three investors each count a hundred as theirs.", 8.9, 13.5)]),
               big_a="<span style='color:#D93A12'>109%</span> sold short. How?", size_a=104,
               big="<span style='color:#D93A12'>109%</span> of it, sold short", size=100,
               small="GameStop, 2021"),
    chapters=[
        dict(title="More than all of it", art=("bars", dict(values=[100, 109], labels=["SHARES", "SOLD SHORT"], hi=1)), beats=[
            dict(say="On the last day of twenty twenty, more GameStop shares had been sold short than the company had in existence. A hundred and nine percent of them. How can you sell more of something than exists?",
                 show=CINE("hook_109")),
            dict(say="Within four weeks, the price went from a little under twenty dollars to four hundred and eighty three. And on its wildest day, some of the most popular trading apps stopped letting their customers buy it.",
                 shows=[dict(kind="number", value=483, start=20, count_d="sentence", pre="$", label="from a little under $20 (end of 2020) to the high of January 28, 2021 · SEC staff report"),
                        SS("server", "On the wildest day, buying switched off.", "", (), 96, flip=True, lights=True)]),
            dict(say="This is the story of January twenty twenty one, told from the official record. We'll see how one share can be sold short twice, why a message at eleven minutes past five in the morning switched off the buy button, and what the regulator found about the squeeze everyone talked about.",
                 shows=[S("document", "The official record.", "SEC staff report, 2021 · Tenev testimony, 2021", ["official"], 96, title="THE RECORD", lines=4, stamp="2021"),
                        dict(kind="list", title="In this film", items=["One share, sold short twice", "A message at 5:11 a.m.", "Was it really a squeeze?"])]),
        ]),
        dict(title="Selling what you don't own", art=("seesaw", dict(left="BORROW", right="SELL", tip=1)), beats=[
            dict(say="GameStop is an American chain that sells video games. In twenty twenty, about six point seven million of its shares changed hands on an average day.",
                 shows=[S("shopfront", "A video game chain.", "", ["video"], 96, n=3, banner="GAMES"),
                        dict(kind="number", value=6.7, dec=1, suf="m", label="shares traded on an average day, 2020 · SEC staff report")]),
            dict(say="Some investors expected it to shrink, and bet against it by selling it short. In the regulator's words, short selling involves the sale of a stock that the seller does not own.",
                 shows=[S("arrows", "A bet that it shrinks.", "", ["shrinks."], 100, up="", down="SHORT"),
                        dict(kind="term", term="Short selling", text="involves the sale of a stock that the seller does not own. SEC staff report, 2021")]),
            dict(say="Here's how it works, with our own round numbers. You borrow a share and sell it for twenty dollars. Later you buy one back and return it. If the price has fallen to ten, you keep ten dollars. If it has risen to fifty, you've lost thirty.",
                 shows=[S("bulb", "Our round numbers.", "", ["round"], 110, text="$"),
                        S("handshake", "Borrow one, sell it: $20.", "Our example", ["$20."], 96, flip=True, left="LENDER", right="YOU"),
                        SS("two_ways", "Buy one back, give it back.", "", (), 96, left=("BUY", "BACK"), right=("GIVE", "BACK")),
                        dict(kind="compare", left=("Sold for", "$20"), right=("Bought back at", "$10"), note="You keep $10 · our example"),
                        SC("bars", "Our example: sold at $20, bought back at $50: a $30 loss", values=[20, 50], labels=["SOLD", "BUY BACK"], hi=1)]),
            dict(say="There's a catch. A share you buy can only fall to zero, so your loss has a floor. A share you've sold short can keep rising, and so can your loss.",
                 shows=[S("magnifier", "There's a catch.", "", ["catch."], 110, label="?"),
                        SS("empty_pockets", "Buy: the most you lose is what you paid.", "", (), 96, flip=True, label="$0"),
                        S("rocket", "Short: no ceiling.", "", ["ceiling."], 100)]),
        ]),
        dict(title="The same share, twice", art=("handshake", dict(left="LEND", right="LEND AGAIN")), beats=[
            dict(say="Picture a company with just a hundred shares, all owned by one investor. Her broker lends all hundred to a short seller, who sells them to a second investor. Now the second investor owns a hundred shares too. The first still counts hers as her own, because she lent them, she didn't sell them.",
                 show=CINE("lend_twice")),
            dict(say="And the second investor's broker can lend them out again. A second short seller borrows them, and sells them to a third investor. There are still only a hundred shares. But two hundred have been sold short, and three investors each count a hundred as theirs.",
                 show=CINE("lend_twice_2")),
            dict(say="The staff at the SEC put it in one line. Short interest can exceed a hundred percent when the same shares are lent multiple times by successive purchasers.",
                 shows=[dict(kind="quote", text="Short interest can exceed 100% ... when the same shares are lent multiple times by successive purchasers.",
                             hl=["exceed", "100%", "lent", "multiple"], who="SEC staff report, 2021, p. 26", size=80)]),
            dict(say="Every short seller still owes a share back, and has to buy one in the market to return it. When more shares are owed than exist, and the price starts to climb, a lot of them may want to buy at the same time. That rush to buy back is what's called a short squeeze.",
                 shows=[S("ledger", "Every short seller owes shares.", "Our illustration", ["owes"], 96, names=("Short seller 1  owes 100", "Short seller 2  owes 100", "Shares that exist  100"), hi=(0, 1)),
                        SS("crowd_rush", "All buying at the same time.", "", (), 96, flip=True, target="BUY BACK"),
                        dict(kind="term", term="A short squeeze", text="short sellers rushing to buy back at once, pushing the price up as they do.")]),
        ]),
        dict(title="January", art=("calendar", dict(day="22", month="JAN", note="2021")), beats=[
            dict(say="GameStop had started to get attention on Reddit in twenty nineteen, in a forum called WallStreetBets. At the end of twenty twenty, its shares traded for a little under twenty dollars.",
                 shows=[S("phone", "Talked about on Reddit.", "From 2019 · SEC staff report", ["Reddit."], 100),
                        dict(kind="number", value=20, pre="$", label="a little under this, end of 2020 · SEC staff report")]),
            dict(say="On the twenty second of January, twenty twenty one, it rose from about forty three dollars to about seventy two in roughly three hours. That day, a hundred and ninety seven million shares changed hands, about twenty nine times the average day of twenty twenty. On the twenty seventh, it closed at three hundred and forty seven dollars and fifty one cents.",
                 show=CINE("laptop_prints")),
            dict(say="By the twenty seventh, nearly nine hundred thousand separate accounts were trading it. Trading was paused again and again to let the price settle: forty times in January, against once in the whole of twenty twenty.",
                 shows=[S("crowd_rush", "Nearly 900,000 accounts.", "By January 27 · SEC staff report", ["900,000"], 96, target="GME"),
                        SC("bars", "Trading pauses in GameStop (SEC staff report, 2021)", values=[1, 40], labels=["ALL OF 2020", "JANUARY 2021"], hi=1)]),
            dict(say="Some funds that had bet against it closed out their short positions, in the report's words, realizing significant losses. One of them, Melvin Capital, was reported to have lost fifty three percent in January, and took two point seven five billion dollars of new money from two other firms, Citadel and Point Seventy Two.",
                 shows=[S("empty_pockets", "Significant losses.", "SEC staff report, 2021", ["losses."], 100, label="SHORT"),
                        dict(kind="compare", left=("Reported loss, January 2021", "53%"), right=("New money from two firms", "$2.75bn"),
                             note="Melvin Capital · Fox Business, February 1, 2021, citing a source")]),
        ]),
        dict(title="Eleven minutes past five", art=("clock", dict(time="5:11")), beats=[
            dict(say="To see why the buying was switched off, you need one piece of plumbing. In the US in twenty twenty one, a share trade didn't finish when you pressed the button. It settled two business days later, which the industry calls T plus two.",
                 shows=[S("server", "The plumbing.", "", ["plumbing."], 110),
                        SS("hourglass72", "A trade isn't finished at once.", "", (), 96, flip=True, rate="T+2", left="TRADE", right="SETTLED"),
                        dict(kind="timeline", title="Settlement in 2021 (T+2)", items=[("T", "You trade"), ("T+1", "Waiting"), ("T+2", "It settles")], hi=2)]),
            dict(say="Until a trade settles, the broker's clearing firm has to post collateral with a clearing house, the NSCC, in case something goes wrong in between. The more trading, and the wilder the prices, the bigger that deposit.",
                 shows=[dict(kind="flow", title="While a trade settles", items=[("doc", "You trade"), ("coin", "The broker posts collateral"), ("scales", "The clearing house holds it")]),
                        S("scale", "Wilder prices, bigger deposit.", "Tenev testimony, 2021", ["bigger"], 96, flip=True, left="RISK", right="DEPOSIT", tip=1)]),
            dict(say="On the twenty seventh of January, the clearing house made intraday margin calls totalling six point nine billion dollars on thirty six of its members.",
                 shows=[dict(kind="compare", left=("Margin calls, January 27", "$6.9bn"), right=("Members called", "36"), note="NSCC, during the day · SEC staff report, 2021")]),
            dict(say="At about eleven minutes past five the next morning, Robinhood's clearing firm got an automated notice. According to the company's chief executive, Vlad Tenev, it owed about three billion dollars more than it had on deposit.",
                 show=CINE("dawn_notice")),
            dict(say="Most of it was one charge, an excess capital premium of over two point two billion dollars. Tenev said it was set off because the clearing house's risk charge had grown bigger than the firm's own net capital.",
                 shows=[SC("bars", "The demand, January 28, $ billion (Tenev testimony, 2021)", values=[1.3, 2.2], labels=["RISK CHARGE, NEARLY", "PREMIUM, OVER"], hi=1),
                        S("seesaw", "Risk charge over net capital.", "Tenev testimony, 2021", ["over"], 96, flip=True, left="RISK CHARGE", right="NET CAPITAL", tip=0)]),
            dict(say="Between half past six and half past seven that morning, Robinhood decided to stop customers opening new positions in GameStop and a few other stocks. They could sell, but they couldn't buy.",
                 show=CINE("buy_grey")),
            dict(say="Shortly after nine, the clearing house waived the premium for that day. The requirement fell to about one point four billion dollars. Robinhood met it with about seven hundred and thirty seven million dollars of new cash, on top of the six hundred and ninety six million it already had there.",
                 shows=[SC("stamp", "The premium, waived for the day (Tenev testimony, 2021)", text="WAIVED"),
                        dict(kind="number", value=1.4, dec=1, pre="$", suf="bn", label="the new requirement, about · Tenev testimony, 2021"),
                        SC("bars", "Meeting it, $ million (Tenev testimony, 2021)", values=[696, 737], labels=["ALREADY THERE", "NEW CASH"], hi=1)]),
            dict(say="GameStop hit four hundred and eighty three dollars that day, its high, and closed at a hundred and ninety three dollars and sixty cents.",
                 shows=[dict(kind="compare", left=("High, January 28", "$483.00"), right=("Close, January 28", "$193.60"), note="SEC staff report, 2021")]),
        ]),
        dict(title="Was it a squeeze?", art=("seesaw", dict(left="SQUEEZE", right="BUYERS", tip=1)), beats=[
            dict(say="The popular story is that short sellers, forced to buy back, drove the price up. The staff at the SEC looked at the trading data. They found that buying to cover probably did push the price up at some moments. But it was a small fraction of all the buying.",
                 shows=[S("rocket", "The popular story.", "", ["popular"], 100),
                        SS("magnifier", "The staff looked at the data.", "", (), 96, flip=True, label="DATA"),
                        S("arrows", "Up, at some moments.", "SEC staff report, 2021", ["moments."], 96, up="COVERING", down=""),
                        dict(kind="term", term="A small fraction", text="of overall buy volume. SEC staff report, 2021")]),
            dict(say="Their conclusion: it was the positive sentiment, not the buying to cover, that sustained the weeks-long price appreciation of GameStop stock.",
                 show=DOC(style="opinion", head="U.S. SECURITIES AND EXCHANGE COMMISSION", sub="STAFF REPORT, OCTOBER 2021",
                          quote="it was the positive sentiment, not the buying-to-cover, that sustained the weeks-long price appreciation of GameStop stock.",
                          hl=("positive sentiment", "weeks-long"), start=(0, "it was"), wrap=42,
                          source="Staff Report on Equity and Options Market Structure Conditions in Early 2021, p. 27", badge_text="Quoted from the report", seed=32)),
            dict(say="And the short interest didn't stay fixed. As the price rose from the twenty second to the twenty seventh, the short interest fell. Short sellers were leaving, and the price kept rising.",
                 shows=[S("tower", "Not fixed.", "", ["fixed."], 100, floors=6, label="SHORTS"),
                        SC("seesaw", "January 22 to 27: price up, short interest down (SEC staff report)", left="PRICE", right="SHORTS", tip=1),
                        S("figures", "Short sellers leaving.", "Our summary", ["leaving."], 96, n=4, hi=0)]),
            dict(say="In our reading, the hundred and nine percent set the stage, but most of the fuel came from people who wanted to own the stock. The fall came fast too. By the third of February, it was under a hundred dollars. On the nineteenth, it touched forty dollars and fifty nine cents.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 110, text="!"),
                        SS("rocket", "The fall came fast.", "", (), 96, flip=True, fall=True),
                        dict(kind="timeline", title="After the high (SEC staff report, 2021)", items=[("JAN 28", "$483 high"), ("FEB 3", "Under $100"), ("FEB 19", "$40.59 low")], hi=2),
                        dict(kind="number", value=40.59, dec=2, pre="$", label="the low, February 19, 2021 · SEC staff report")]),
        ]),
        dict(title="One day instead of two", art=("calendar", dict(day="28", month="MAY", note="2024")), beats=[
            dict(say="The staff's report suggested one way to cut the risk in the plumbing: shorten the settlement cycle. Our reading of why: a shorter wait means fewer days of trades for a clearing deposit to cover.",
                 shows=[dict(kind="term", term="Shorten the settlement cycle", text="one method to mitigate the systemic risk. SEC staff report, 2021"),
                        S("hourglass72", "Fewer days to cover.", "Our reading", ["Fewer"], 100, flip=True, rate="T+1", left="T+2", right="T+1")]),
            dict(say="In February twenty twenty three, the SEC adopted a rule that moved most US trades from two business days to one. It took effect on the twenty eighth of May, twenty twenty four. The chair of the SEC, Gary Gensler, said it answered one of the areas his staff had flagged after the meme stock events of twenty twenty one.",
                 shows=[dict(kind="timeline", title="From T+2 to T+1 (SEC press release, 2023)", items=[("FEB 2023", "Rule adopted"), ("MAY 28, 2024", "T+1 in force")], hi=1),
                        S("calendar", "May 28, 2024.", "SEC, 2023", ["May"], 100, flip=True, day="28", month="MAY", note="T+1"),
                        S("document", "After the meme stock events.", "SEC press release, 2023", ["meme"], 96, title="SEC 2023-29", lines=4, stamp="T+1")]),
        ]),
        dict(title="The share that counts twice", art=("handshake", dict(left="OWNS", right="OWES")), beats=[
            dict(say="Here's our reading of the whole story. A hundred and nine percent wasn't a typo. It's what happens when lent shares are sold and lent again: the same share can sit in several accounts at once, as long as someone owes it back.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 120, text="?"),
                        dict(kind="number", value=109, suf="%", label="short interest, December 31, 2020: not a typo · SEC staff report"),
                        S("ledger", "One share, several accounts.", "Our illustration", ["several"], 96, flip=True, names=("Owner 1  100", "Owner 2  100", "Owner 3  100", "Shares that exist  100"), hi=(3,))]),
            dict(say="And on the record we have, the buy button went grey over a clearing deposit: money a broker has to post while trades settle, which jumped when the trading went wild.",
                 shows=[SC("scale", "The buy button and the clearing deposit (Tenev testimony, 2021)", left="DEPOSIT", right="BUY", tip=0)]),
            dict(say="The squeeze got the headlines. The plumbing set the limits.",
                 shows=[dict(kind="statement", text="The squeeze got the headlines. The plumbing set the limits.", hl=["plumbing"], size=100)]),
            dict(say="If an interviewer asks how short interest can top a hundred percent, here's a short answer. Shares that are lent and sold can be lent again, so the same share can be borrowed more than once. This is education, not financial advice.",
                 shows=[S("document", "How can it top 100%?", "Interview prep", ["100%?"], 100, title="Q: 109%?", lines=3, stamp="2021"),
                        dict(kind="list", title="The short answer", items=["Lent, then sold", "Lent again", "Owed back more than once"]),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. Should a broker be allowed to stop customers buying a stock when its clearing deposit jumps? Tell us in the comments.",
                 shows=[S("bulb", "Our question for you.", "", ["question"], 110, text="?"),
                        SC("seesaw", "Stop the buying, or keep it open?", left="STOP", right="KEEP OPEN", tip=0),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "On the last day of 2020, the GameStop shares sold short came to 109% of all the shares the company had. That's more "
        "than all of it. Within four weeks the price went from a little under $20 to $483, and on that day some of the most "
        "popular trading apps wouldn't let their customers buy it.\n\nSo how can you sell short more of a company than exists? "
        "We'll follow one share as it's lent and sold, then lent and sold again, until a company with 100 shares has 200 sold "
        "short. Then the plumbing you don't usually see: T+2 settlement, the clearing house deposit, and the automated notice "
        "at 5:11 a.m. on January 28 that asked one broker for about $3 billion more than it had posted.\n\nThen the question "
        "everyone argued about. Was it really a short squeeze? The SEC's staff went through the trading data, and their answer "
        "isn't the one you'd expect. We finish with what changed in 2024 and our own reading of the story. Should a broker be "
        "allowed to stop the buying? Tell us what you think below."),
    sources=[
        ("SEC staff, Report on Equity and Options Market Structure Conditions in Early 2021 (October 2021)",
         "https://SEC.gov/files/staff-report-equity-options-market-struction-conditions-early-2021.pdf"),
        ("Vlad Tenev, written testimony to the House Financial Services Committee, 18 February 2021",
         "https://democrats-financialservices.house.gov/UploadedFiles/HHRG-117-BA00-Wstate-TenevV-20210218.pdf"),
        ("SEC press release 2023-29, SEC Finalizes Rules to Reduce Risks in Clearance and Settlement (T+1), 15 February 2023",
         "https://sec.gov/news/press-release/2023-29"),
        ("Fox Business, Melvin Capital, hedge fund that bet against GameStop, lost 53% in January (1 February 2021)",
         "https://foxbusiness.com/markets/melvin-capital-hedge-fund-that-bet-against-gamestop-lost-53-in-january"),
        ("SEC press release 2021-212, SEC Staff Releases Report on Equity and Options Market Structure Conditions in Early 2021",
         "https://www.sec.gov/news/press-release/2021-212"),
    ],
    source_note="We drew the filmed scenes ourselves. The trading app you'll see is our illustration, it isn't a real app, and the "
                "rooms are stylised reconstructions, not the real offices. Nobody in them is a portrait, and nobody speaks. The "
                "company with 100 shares and the $20, $10 and $50 short sale are our own examples. \"About 29 times\" is our "
                "arithmetic (197.2 million against 6.7 million). Melvin Capital's January loss was reported from an unnamed "
                "source. The readings in the last chapters are ours, so feel free to disagree with them. This channel is "
                "educational and isn't affiliated with, or endorsed by, any company, broker, fund or regulator named in it.",
    hashtags=["GameStop", "ShortSelling", "FinanceHistory"],
    tags=["GameStop", "GameStop short squeeze", "GME 2021", "short interest over 100%", "how short selling works",
          "short squeeze explained", "Robinhood January 28 2021", "NSCC clearing deposit", "T+2 settlement", "T+1 settlement",
          "SEC GameStop report", "WallStreetBets", "meme stocks", "investment banking interview", "financial history"],
)

if __name__ == "__main__":
    make(EP)
