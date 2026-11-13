"""
YouTube #6 (13 Nov 2026): Isaac Newton and the South Sea Bubble of 1720. The story everyone shares is that
the greatest scientist of his age was fooled by a bubble and said he could calculate the motions of the
heavens but not the madness of people. The records tell a stranger story: he was not fooled at first. He sold
his whole stake in April 1720 for a large profit, then in June moved almost all his safe money back in near the
top, and lost more than he had made. History of finance, with an interview tie at the end.

Point of view: Newton's mistake was not missing the bubble; it was seeing it, getting out, and going back in
because everyone else was still making money. Being right once is not a plan, and the decision that costs most
is often the second one. The quote that makes him the fool was written down second-hand decades later. Educational,
not advice.

Every claim, sourced:
  [1] Andrew Odlyzko, "Newton's financial misadventures in the South Sea Bubble", Notes and Records: The Royal
      Society Journal of the History of Science, 73(1), March 2019, pp. 25-59; revised version "Isaac Newton and
      the perils of the financial South Sea" (5 March 2020, author's site): early 1720 just under half his assets
      in South Sea stock, the rest in government bonds; most of the stake bought at 100 or below; instructions to
      sell on 19 and 23 April 1720, the whole or almost the whole stake liquidated that week; an early profit of
      about £20,000; re-entry mostly in mid-June, later purchases close to the peak; net worth somewhat over
      £30,000 before the Bubble and about £20,000 by mid-1721; had he kept his gain he would have had over £50,000;
      his estate at death in 1727 roughly the same as before the Bubble (not ruined); Warden of the Mint 1696,
      Master 1699 to his death; by 1720 income over £3,000 a year.
  [2] Andrew Odlyzko, "Isaac Newton and the perils of the financial South Sea", Physics Today 73(7), 1 July 2020:
      company set up in 1711 to deal with a backlog of unpaid government bills, creditors offered South Sea stock;
      Newton "decided to liquidate his entire stake ... on Tuesday and Saturday, 19 and 23 April"; "In June of that
      year, Newton liquidated almost all of his newly acquired stake in government bonds and used the proceeds to
      buy South Sea stock"; net worth "just over £30 000" before and "about £20 000" by mid-1721, "he had lost all
      his early profits and a good bit more besides"; the letter of 14 September 1724: "I lost very much by the
      South Sea company which makes my pockets empty, & my mind averse from dealing in these matters"; "He was
      brilliant, but he was not a universal genius"; "he was standing in a swamp"; by October the stock was worth
      less than a quarter of its peak.
  [3] Wikipedia, "South Sea Company" (opened 13 Nov 2026): about £128 in January 1720, £175 February, £330 March,
      £550 at the end of May, £890 in early June after the Bubble Act, £1,000 first reached in early August, £150 by
      the end of September, about £100 before the year ended (our chart adds about £350 at the end of April from [4]); the Bubble Act of June 1720 (charters needed for
      joint-stock companies), not repealed until 1825; the 1721 inquiry found fraud; directors stripped of on
      average 82% of their wealth (the money went to the victims); politicians "sold" shares with an option to sell
      back; Parliament recalled in December 1720; many banks and goldsmiths failed when they could not collect loans
      secured on stock; John Aislabie found guilty of corruption and imprisoned (Chancellor of the Exchequer, per [4]).
  [4] The National Archives blog, "The South Sea Bubble of 1720" (Dr Alice Marples, The Newton Project, 2020):
      share price about £350 at the end of April 1720; Jonathan Swift among the losers; the Royal Society lost about £600; Thomas Guy sold his shares at £600 each
      and used the proceeds to establish Guy's Hospital in Southwark in 1721.
  [5] Wikipedia, "Thomas Guy": "before the South Sea Bubble burst, Guy sold 54,040 stock for £234,428, making a
      profit of about £175,000".
  [6] Wist (Wordsmithed Quotations), Isaac Newton, "I can calculate the movement of the stars, but not the madness
      of the people" (Attributed): earliest record Joseph Spence's notes (1756), via Lord Radnor, printed in
      Singer's 1820 edition of Spence's Anecdotes; that version places the remark before the bubble burst.
Our own illustration, labelled on screen: the chart is drawn from the approximate prices in [3]; the crowd, the
apple, the pockets, the hospital, the parchment and the letter are our own drawings, not portraits.

    python build/youtube_ep006.py
"""

from youtube import make

# S(drawing, line, label, highlighted words, size, flip, **drawing options); SC(drawing, heading, **drawing options)
S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)

SOLD, BOUGHT = (2, "SOLD", "#0F766E"), (4, "BOUGHT", "#D93A12")

EP = dict(
    slug="yt-006-newton-bought-back-in",
    title="Isaac Newton Beat the Bubble. Then He Bought Back In.",
    thumb=dict(art=("price_path", dict(marks=[SOLD, BOUGHT], note="SOUTH SEA STOCK, 1720", counter=False)),
               big_a="Newton <span style='color:#D93A12'>sold</span> early. Then he bought back.", size_a=92,
               art_b=("crowd_rush", dict(n=6, target="SOUTH SEA")),
               big="The genius who <span style='color:#D93A12'>went back in</span>", size=100,
               small="Newton and the South Sea Bubble", ghost="1720"),
    chapters=[
        dict(title="The story everyone shares", art=("apple_fall", dict()), beats=[
            dict(say="Isaac Newton worked out the laws of motion and gravity. And in seventeen twenty, he lost a fortune in a stock bubble.",
                 shows=[S("apple_fall", "He worked out gravity.", "Isaac Newton", ["gravity."], 110),
                        S("bubble", "Then lost a fortune in a bubble.", "1720", ["bubble."], 100, flip=True, label="1720")]),
            dict(say="That is the story people love to share, usually with a line he is supposed to have said about it.",
                 shows=[S("speech", "The line everyone shares.", "Online, every crash", ["shares."], 110, text="Madness?")]),
            dict(say="I can calculate the motions of the heavenly bodies, but not the madness of people.",
                 show=dict(kind="quote", text="I can calculate the motions of the heavenly bodies, but not the madness of people.",
                           hl=["madness"], who="Attributed to Isaac Newton", size=86)),
            dict(say="The moral seems obvious. Even a genius gets fooled by a bubble.",
                 shows=[S("bulb", "The moral seems obvious.", "", ["obvious."], 120, text="?"),
                        dict(kind="verdict", text="Even a genius gets fooled by a bubble.", stamp="MYTH?", size=100)]),
            dict(say="But the records of what he actually bought and sold tell a different story. He was not fooled. He saw it, he got out early with a big profit, and then he went back in.",
                 shows=[S("ledger", "What he actually bought and sold.", "The records", ["actually"], 96,
                          names=("19 April  SELL", "23 April  SELL", "June  BUY", "June  BUY"), hi=(2, 3)),
                        S("stamp", "He was not fooled.", "", ["not"], 120, flip=True, text="NOT FOOLED"),
                        S("price_path", "Out early, then back in.", "Our chart of 1720", ["back"], 92, marks=[SOLD, BOUGHT])]),
            dict(say="In this video we follow his money month by month, meet the man who sold and never came back, and look at where that famous quote really comes from.",
                 shows=[dict(kind="timeline", title="Where we are going", items=[("1711", "The company"), ("April", "Newton sells"),
                                                                                  ("June", "Newton buys"), ("1756", "The quote")], hi=2)]),
        ]),
        dict(title="A company made of debt", art=("document", dict(title="South Sea stock", lines=4, stamp="1711")), beats=[
            dict(say="The South Sea Company was set up in seventeen eleven to deal with a pile of government debt.",
                 shows=[S("document", "Set up in 1711.", "The South Sea Company", ["1711."], 110, title="Government bills", lines=5, stamp="UNPAID")]),
            dict(say="People the government owed money to were offered shares in the company instead. The company collected interest from the government, and paid its shareholders.",
                 shows=[dict(kind="flow", items=[("doc", "Government debt"), ("bank", "South Sea shares"), ("coin", "Interest to holders")]),
                        S("coins", "Interest from the government.", "", ["Interest"], 110, flip=True, stacks=[2, 4, 6])]),
            dict(say="In seventeen twenty it went much further, taking on a huge part of Britain's national debt in exchange for its shares.",
                 shows=[S("scale", "Debt in, shares out.", "1720", ["shares"], 110, left="Debt", right="Shares", tip=0)]),
            dict(say="And the higher the share price went, the better the deal looked for the company. So the price became the whole game.",
                 shows=[S("arrows", "A higher price, a better deal.", "For the company", ["higher"], 110, up="PRICE", down=""),
                        S("price_path", "The price became the game.", "Approximate prices", ["game."], 96, flip=True, upto=2)]),
            dict(say="That is the part to remember. The company had a reason to want its price high that had nothing to do with trade.",
                 shows=[S("bulb", "The part to remember.", "", ["remember."], 120, text="!"),
                        S("ship", "Nothing to do with trade.", "Our reading", ["trade."], 100, flip=True)]),
            dict(say="At the start of seventeen twenty a share sold for about a hundred and twenty eight pounds. By March it was about three hundred and thirty.",
                 shows=[dict(kind="number", value=128, pre="£", label="a South Sea share, January 1720 (approximate)"),
                        S("price_path", "About £330 by March.", "Up two and a half times", ["£330"], 100, flip=True, upto=2)]),
        ]),
        dict(title="Newton takes his profit", art=("price_path", dict(upto=3, marks=[SOLD])), beats=[
            dict(say="Newton was not a beginner with money. He had run the Royal Mint since sixteen ninety six, first as Warden and then as Master.",
                 shows=[S("coins", "Not a beginner with money.", "Royal Mint", ["beginner"], 110, stacks=[3, 6, 9]),
                        dict(kind="timeline", title="Isaac Newton at the Mint", items=[("1696", "Warden"), ("1699", "Master"), ("1727", "Until his death")], hi=1)]),
            dict(say="At the start of the year, just under half of what he owned was in South Sea stock. The rest was lent to the government, in bonds.",
                 shows=[S("cake", "Just under half in South Sea stock.", "Early 1720", ["half"], 100, slices=10, hi=1),
                        S("document", "The rest in government bonds.", "", ["bonds."], 100, flip=True, title="Government bonds", lines=4, stamp="SAFE")]),
            dict(say="Then, on the nineteenth and the twenty third of April, he gave orders to sell. Within a week he had sold his whole stake, or nearly all of it.",
                 shows=[S("calendar", "19 and 23 April.", "Orders to sell", ["sell."], 120, day="19", month="APR", note="1720"),
                        S("price_path", "He sold his whole stake.", "Within a week", ["whole"], 96, flip=True, upto=3, marks=[SOLD])]),
            dict(say="He had held the stock for years, and most of his shares had cost him a hundred pounds or less. Now they were worth more than three times that.",
                 shows=[S("coins", "Most cost him £100 or less.", "Bought before 1720", ["£100"], 100, stacks=[2, 3, 4]),
                        S("arrows", "Now worth over three times that.", "April 1720", ["three"], 100, flip=True, up="x3", down="")]),
            dict(say="His profit, by the best reconstruction of his accounts, was about twenty thousand pounds.",
                 shows=[dict(kind="number", value=20000, pre="£", label="Newton's early profit, about (Odlyzko, Royal Society journal, 2019)"),
                        ]),
            dict(say="Before the bubble he was worth a little over thirty thousand. So in a few months he had made about two thirds of his fortune again.",
                 shows=[S("bars", "Worth a little over £30,000.", "Before the bubble", ["£30,000."], 100, values=[30, 20], labels=["WORTH", "PROFIT"], hi=1),
                        S("bulb", "Two thirds of his fortune, again.", "", ["Two", "thirds"], 110, flip=True, text="2/3")]),
            dict(say="If the story ended here, Newton would be the hero of it. The man who took his profit while the crowd was still buying.",
                 shows=[S("stamp", "The hero of the story.", "If it ended here", ["hero"], 110, text="SOLD"),
                        S("figures", "While the crowd kept buying.", "", ["crowd"], 100, flip=True, n=6, hi=0)]),
        ]),
        dict(title="The summer everyone was in", art=("crowd_rush", dict()), beats=[
            dict(say="But the price kept going. In June, Parliament passed what became known as the Bubble Act, which made it much harder to launch a rival company without a charter.",
                 shows=[S("price_path", "The price kept going.", "May and June", ["kept"], 100, upto=5),
                        S("scroll", "The Bubble Act, June 1720.", "No rivals without a charter", ["Bubble", "Act,"], 96, flip=True, title="AN ACT", seal="1720")]),
            dict(say="Right after it, the shares jumped to about eight hundred and ninety pounds. In early August they reached a thousand.",
                 shows=[dict(kind="number", value=890, pre="£", label="a share in early June 1720 (approximate)"),
                        S("price_path", "£1,000 in early August.", "The peak", ["£1,000"], 100, flip=True, upto=6)]),
            dict(say="Everyone seemed to be in. Lords and ladies, people with their life savings, the writer Jonathan Swift, even the Royal Society, Newton's own scientific society.",
                 shows=[S("crowd_rush", "Everyone seemed to be in.", "Summer 1720", ["Everyone"], 110, n=7),
                        dict(kind="icons", title="Who was in", items=[("people", "Lords and ladies"), ("pen", "Jonathan Swift"), ("book", "The Royal Society")], hi=2)]),
            dict(say="This is what a bubble feels like from the inside. Every week the price goes up, and the people who bought look clever. The people who stayed out look foolish.",
                 shows=[S("bubble", "What a bubble feels like inside.", "", ["inside."], 110, label="£1,000"),
                        S("seesaw", "Buyers look clever.", "", ["clever,"], 100, flip=True, left="Buyers", right="Sellers", tip=0),
                        S("figures", "Sellers look foolish.", "", ["foolish."], 100, n=4, hi=0)]),
            dict(say="Imagine watching that from the outside. You sold in April. Your friends, your colleagues, your own scientific society are all richer every week.",
                 shows=[S("magnifier", "Imagine watching from outside.", "", ["outside."], 110, label="APRIL"),
                        S("figures", "You sold in April.", "", ["April."], 110, flip=True, n=5, hi=0, glass=True),
                        S("arrows", "Everyone else, richer every week.", "", ["richer"], 100, up="THEM", down="YOU")]),
        ]),
        dict(title="Newton buys back in", art=("price_path", dict(upto=5, marks=[SOLD, BOUGHT])), beats=[
            dict(say="In June, Newton went back in. And this time he went in big.",
                 shows=[S("crowd_rush", "In June, he went back in.", "", ["back"], 110, n=6),
                        S("stamp", "This time, big.", "", ["big."], 120, flip=True, text="ALL IN")]),
            dict(say="He sold almost all of the government bonds he held, the safe part of his money. And he used it to buy South Sea stock.",
                 shows=[dict(kind="flow", items=[("doc", "Government bonds"), ("hand", "Sold"), ("ship", "South Sea stock")]),
                        S("scale", "The safe part, moved into the risky part.", "", ["safe"], 96, flip=True, left="Bonds", right="South Sea", tip=1)]),
            dict(say="Most of it went in from the middle of June, and he kept buying at high prices, close to the peak.",
                 shows=[S("price_path", "Close to the peak.", "Mid June onwards", ["peak."], 110, upto=6, marks=[SOLD, BOUGHT])]),
            dict(say="So think about what that means. The man who had seen the bubble clearly in the spring was now paying more than twice the spring price.",
                 shows=[S("seesaw", "Seen clearly in April.", "", ["clearly"], 110, left="April", right="June", tip=1),
                        dict(kind="compare", left=("End of March, about", "£330"), right=("Early June, about", "£890"), note="Approximate share prices, 1720")]),
            dict(say="Why would he do that? We cannot know what he was thinking. But we do know what he was watching: a price that kept climbing for months after he sold.",
                 shows=[S("magnifier", "Why would he do that?", "", ["Why"], 120, label="WHY?"),
                        S("bulb", "We cannot know his thinking.", "", ["cannot"], 110, flip=True, text="?"),
                        S("price_path", "What he was watching.", "April to June", ["watching."], 100, upto=5, marks=[SOLD])]),
            dict(say="Nothing about the company had become safer. What had changed was the crowd.",
                 shows=[S("tower", "Nothing had become safer.", "", ["safer."], 110, crack=True, label="SOUTH SEA"),
                        S("figures", "What changed was the crowd.", "", ["crowd."], 110, flip=True, n=8, hi=7)]),
        ]),
        dict(title="Then it burst", art=("bubble", dict(pop=True, label="POP")), beats=[
            dict(say="In September, the price collapsed. By the end of that month, a share that had sold for a thousand pounds was worth about a hundred and fifty.",
                 shows=[S("bubble", "In September it collapsed.", "", ["collapsed."], 110, pop=True, label="POP"),
                        S("price_path", "£1,000 to about £150.", "End of September", ["£150."], 100, flip=True, marks=[SOLD, BOUGHT])]),
            dict(say="By the end of the year it was down to about a hundred.",
                 shows=[dict(kind="number", value=100, start=1000, pre="£", label="a share at the end of 1720 (approximate)"),
                        ]),
            dict(say="By the middle of seventeen twenty one, Newton was worth about twenty thousand pounds. He had lost all of his early profit, and a good part more.",
                 shows=[S("bars", "Worth about £20,000.", "Mid 1721", ["£20,000."], 100, values=[30, 20], labels=["BEFORE", "1721"], hi=1),
                        S("empty_pockets", "All the profit, and more.", "", ["more."], 100, flip=True)]),
            dict(say="Had he simply kept his April profit and stayed out, he would have had more than fifty thousand pounds. That is the real size of the mistake.",
                 shows=[dict(kind="compare", left=("Went back in", "£20k"), right=("Stayed out", "£50k+"), note="Odlyzko's reconstruction of Newton's accounts"),
                        S("coins", "More than fifty thousand.", "If he had stayed out", ["fifty"], 100, flip=True, stacks=[3, 6, 10])]),
            dict(say="He was not ruined. His income was large, and when he died in seventeen twenty seven his estate was about what it had been before the bubble.",
                 shows=[S("stamp", "Not ruined.", "", ["ruined."], 120, text="NOT RUINED"),
                        S("calendar", "His estate in 1727.", "About where it started", ["1727."], 110, flip=True, day="", month="1727", note="ESTATE")]),
            dict(say="But he felt it. In a letter in seventeen twenty four he wrote: I lost very much by the South Sea company, which makes my pockets empty, and my mind averse from dealing in these matters.",
                 shows=[S("letter", "He felt it.", "A letter, 1724", ["felt"], 120, date="1724"),
                        dict(kind="quote", text="I lost very much by the South Sea company which makes my pockets empty, & my mind averse from dealing in these matters.",
                             hl=["pockets", "empty,"], who="Isaac Newton, letter of 14 September 1724", size=74)]),
        ]),
        dict(title="The reckoning", art=("scroll", dict(title="THE REPORT", seal="1721")), beats=[
            dict(say="Newton was far from alone. When the bubble burst, banks and goldsmiths who had lent against South Sea shares could not collect, and many of them failed.",
                 shows=[S("figures", "Newton was far from alone.", "Autumn 1720", ["alone."], 110, n=7, hi=3),
                        S("tower", "Lenders against the shares failed.", "", ["failed."], 100, flip=True, crack=True, label="LENDERS")]),
            dict(say="Parliament was recalled in December. An inquiry the next year found fraud, and corruption that reached the cabinet.",
                 shows=[S("calendar", "Parliament recalled.", "December 1720", ["recalled."], 120, day="", month="DEC", note="1720"),
                        S("scroll", "Fraud, up to the cabinet.", "The 1721 report", ["Fraud,"], 100, flip=True, title="THE REPORT", seal="1721")]),
            dict(say="Politicians had been handed shares on easy terms, so they gained when the price rose. One minister, the Chancellor John Aislabie, ended up in prison.",
                 shows=[S("handshake", "Shares on easy terms.", "For politicians", ["easy"], 110, left="Company", right="Ministers"),
                        S("stamp", "The Chancellor, in prison.", "John Aislabie", ["prison."], 110, flip=True, text="GUILTY")]),
            dict(say="The company's directors were stripped of most of their wealth, on average about eighty two percent of it, to pay back the people who lost.",
                 shows=[dict(kind="number", value=82, suf="%", label="of their wealth, on average, taken from the company's directors"),
                        ]),
            dict(say="And the Bubble Act, passed while the price was rising, stayed on the books until eighteen twenty five. A rule written in a mania lasted more than a century.",
                 shows=[S("scroll", "On the books until 1825.", "The Bubble Act", ["1825."], 110, title="AN ACT", seal="1720"),
                        dict(kind="timeline", title="The Bubble Act", items=[("1720", "Passed"), ("1825", "Repealed")], hi=1)]),
        ]),
        dict(title="The man who stayed out", art=("hospital", dict(label="SOUTHWARK, 1721")), beats=[
            dict(say="Now compare a London bookseller called Thomas Guy.",
                 shows=[S("book", "A London bookseller.", "Thomas Guy", ["bookseller."], 120, title="Bookseller")]),
            dict(say="He also held South Sea stock, and he also sold before the crash. He got about six hundred pounds a share.",
                 shows=[S("price_path", "He sold too.", "Before the crash", ["too."], 110, upto=4, marks=[(3, "GUY", "#0F766E")]),
                        dict(kind="number", value=600, pre="£", label="a share, Thomas Guy's selling price (The National Archives)")]),
            dict(say="One account puts his sales at more than two hundred and thirty four thousand pounds. His profit, about a hundred and seventy five thousand.",
                 shows=[S("coins", "More than £234,000 of sales.", "One account", ["£234,000"], 100, stacks=[4, 8, 12]),
                        dict(kind="number", value=175000, pre="£", label="profit, about (as one account puts it)")]),
            dict(say="The difference is that Guy never went back. In seventeen twenty one he used the money to found a hospital in Southwark, which still carries his name.",
                 shows=[S("stamp", "Guy never went back.", "", ["never"], 120, text="STAYED OUT"),
                        S("hospital", "A hospital in Southwark.", "Founded 1721", ["hospital"], 100, flip=True, label="SOUTHWARK, 1721")]),
            dict(say="Same bubble, same early exit. One of them was disciplined enough to stay out.",
                 shows=[dict(kind="split", left=("person", "Newton", "Went back in"), right=("check", "Guy", "Stayed out"), mid="vs")]),
        ]),
        dict(title="About that famous quote", art=("speech", dict(text="Madness?")), beats=[
            dict(say="So where does the line about the madness of people come from?",
                 shows=[S("magnifier", "Where does the line come from?", "", ["line"], 110, label="SOURCE?")]),
            dict(say="The earliest version we could find is in the notes of a writer called Joseph Spence, from seventeen fifty six. That is almost thirty years after Newton died.",
                 shows=[S("book", "Joseph Spence's notes.", "1756", ["notes."], 110, title="Notes, 1756"),
                        dict(kind="timeline", title="The quote's trail", items=[("1720", "The bubble"), ("1727", "Newton dies"), ("1756", "Written down"), ("1820", "Printed")], hi=2)]),
            dict(say="And it is second hand. A lord tells Spence that Newton, asked about the rising price, said he could not calculate the madness of the people.",
                 shows=[S("speech", "Second hand.", "A lord, to Spence", ["Second"], 120, text="He told me..."),
                        S("figures", "Asked about the rising price.", "", ["rising"], 100, flip=True, n=3, hi=1)]),
            dict(say="In that telling, it is said before the crash, as a reason not to guess the top. It is not a lament after it.",
                 shows=[dict(kind="verdict", text="Newton said it after losing his fortune.", stamp="UNPROVEN", size=96),
                        S("price_path", "Before the crash, not after.", "In the earliest version", ["Before"], 96, flip=True, upto=5)]),
            dict(say="The words we can be sure are his are plainer, from that letter: my pockets empty. We think they teach more than the famous line.",
                 shows=[S("letter", "The words that are surely his.", "1724", ["surely"], 110, date="1724", hi_line=2),
                        S("empty_pockets", "My pockets empty.", "", ["empty."], 110, flip=True, label="1724")]),
        ]),
        dict(title="What to take from it", art=("seesaw", dict(left="Sell", right="Buy back", tip=1)), beats=[
            dict(say="Here is our reading. Newton's mistake was not failing to see the bubble. It was seeing it, acting on it, and then letting the crowd talk him out of it.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 130, text="1"),
                        S("price_path", "Not failing to see the bubble.", "", ["see"], 96, flip=True, marks=[SOLD]),
                        S("crowd_rush", "Letting the crowd talk him out of it.", "", ["crowd"], 96, n=7)]),
            dict(say="The researcher who rebuilt his accounts, Andrew Odlyzko, put it well. Newton was brilliant, but he was not a universal genius.",
                 shows=[S("document", "The researcher who rebuilt his accounts.", "Physics Today, 2020", ["rebuilt"], 96, title="Newton's accounts", lines=5),
                        dict(kind="quote", text="He was brilliant, but he was not a universal genius.", hl=["universal"],
                             who="Andrew Odlyzko, Physics Today, July 2020", size=96)]),
            dict(say="The hardest moment in a bubble is not the first decision. It is the second one, after you have sold and watched everyone else keep winning.",
                 shows=[S("seesaw", "Not the first decision.", "", ["first"], 110, left="Sell", right="Buy back", tip=1),
                        S("figures", "The second one.", "", ["second"], 110, flip=True, n=5, hi=4, glass=True)]),
            dict(say="There is a question worth asking before you buy back into anything you have sold. Has the thing itself changed, or only its price?",
                 shows=[S("document", "Before you buy back in.", "A question to ask", ["back"], 100, title="Before buying back", lines=4, stamp="?"),
                        dict(kind="split", left=("search", "The thing itself", "Changed?"), right=("up", "Only the price", "Changed?"), mid="or")]),
            dict(say="And if an interviewer ever asks you about a famous bubble, this is a better answer than the quote. Tell them how Newton read the bubble right, and still lost by going back in. This is education, not financial advice.",
                 shows=[S("document", "A better answer than the quote.", "Interview prep", ["better"], 100, title="Q: a famous bubble?", lines=4, stamp="?"),
                        S("price_path", "Right call, then back in.", "", ["back"], 96, flip=True, marks=[SOLD, BOUGHT]),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. If you had sold in April and watched your friends double their money, would you have stayed out? Tell us in the comments.",
                 shows=[S("magnifier", "Our question for you.", "", ["question"], 120, label="YOU?"),
                        S("crowd_rush", "Would you have stayed out?", "Your turn", ["stayed"], 96, flip=True, n=6),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "Everyone shares the story that Isaac Newton, the greatest scientist of his age, got fooled by the South Sea Bubble of 1720. "
        "His own trades say something odder. He sold his whole stake on 19 and 23 April 1720 for a profit of about £20,000. "
        "Then he watched the price keep climbing towards £1,000, and in June he moved almost all his government bonds back into South Sea stock, close to the top. "
        "By mid 1721 he'd lost all of that profit and more. "
        "We'll follow his money month by month, compare him with the bookseller Thomas Guy, who sold too and didn't go back (his profit founded Guy's Hospital), "
        "and look at where the famous \"madness of people\" line really comes from. It's a second-hand note from 1756. "
        "Our take: in a bubble, the decision that costs you is usually the second one, and we think that's a better interview answer than the quote. "
        "If you'd sold in April and watched your friends double their money, would you have stayed out? We're curious."),
    sources=[
        ("Andrew Odlyzko, Isaac Newton and the perils of the financial South Sea, Physics Today, July 2020",
         "https://physicstoday.aip.org/features/isaac-newton-and-the-perils-of-the-financial-south-sea"),
        ("Andrew Odlyzko, revised paper on Newton's South Sea trades (from Notes and Records of the Royal Society, 2019)",
         "https://www-users.cse.umn.edu/~odlyzko/doc/mania13c.pdf"),
        ("Andrew Odlyzko, papers on technology and financial manias", "https://www-users.cse.umn.edu/~odlyzko/doc/bubbles.html"),
        ("The National Archives blog, The South Sea Bubble of 1720 (Alice Marples, The Newton Project)",
         "https://blog.nationalarchives.gov.uk/the-south-sea-bubble-of-1720"),
        ("Wikipedia, South Sea Company (share prices through 1720, the Bubble Act)", "https://en.wikipedia.org/wiki/South_Sea_Company"),
        ("Wikipedia, Thomas Guy", "https://en.wikipedia.org/wiki/Thomas_Guy"),
        ("Wist, the 'madness of the people' quote and its earliest source", "https://wist.info/newton-isaac/45097/"),
    ],
    source_note="The share prices on our chart are approximate monthly levels from the sources above, drawn by us. "
                "The crowd, apple, pockets, hospital, parchment and letter are our own drawings, not portraits of anyone.",
    hashtags=["IsaacNewton", "SouthSeaBubble", "FinanceHistory"],
    tags=["Isaac Newton", "South Sea Bubble", "Newton stock market", "Newton South Sea", "madness of people quote",
          "financial history", "stock market bubble", "1720 bubble", "Thomas Guy", "Guy's Hospital", "FOMO investing",
          "history of finance", "market bubbles explained", "investment banking interview"],
)

if __name__ == "__main__":
    make(EP)
