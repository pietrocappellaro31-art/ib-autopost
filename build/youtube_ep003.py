"""
YouTube #3: the dot-com crash, told the other way round. The usual story is
that everyone in 2000 was a fool. Our reading: most of the people who lost
money were right about the internet and wrong about the price, and the
difference between those two is the most useful lesson in finance for any
boom, including the AI one people are arguing about this month. Technical
explainer (price to sales, payback) inside a history story.

Point of view: a great company and a great investment are different
questions; the price you pay decides which one you own. Calling a top early
looks the same as being wrong. Three questions for any boom: is it real, who
keeps the money, what price is already paid. Educational, not advice: no
verdict on AI.

Every claim, sourced:
  [1] SWBC, "Market Commentary: Week of November 9, 2026": a sharp reversal
      that Thursday, with heavy selling in AI-linked leaders on worries about
      AI spending, growth and slower data-centre expansion.
  [2] Fortune, "Nasdaq surpasses Internet bubble peak to set new record",
      23 Apr 2015: Nasdaq Composite closed at 5,048.62 on 10 March 2000; fell
      78.4% to 1,114.11, reached 31 months after the peak; closed at a record
      5,056.06 on 23 April 2015, about 15 years later.
  [3] Jeff Bezos, 2000 letter to Amazon.com shareholders (Seattle Times
      archive, 14 Apr 2001): opens "Ouch. It's been a brutal year for many in
      the capital markets and certainly for Amazon.com shareholders."; "our
      shares are down more than 80% from when I wrote you last year"; "We
      served 20 million customers in 2000, up from 14 million in 1999";
      quotes Benjamin Graham: "In the short term, the stock market is a voting
      machine; in the long term, it's a weighing machine."
  [4] Sherwood News, "After a quarter century, Cisco surpasses its dot-com
      bubble closing high", Dec 2025 (and Bloomberg, "Cisco Shares Finally
      Top Dot-Com Record After More Than 25 Years", 10 Dec 2025): closing high
      $80.06 in March 2000; briefly the world's most valuable company, above
      $550 billion in late March 2000; shares up about 4,000% from the end of
      1994 to the March 2000 peak; fell nearly 90% before bottoming in late
      2002; first close above the old high in December 2025; market value still
      roughly $250 billion below the 2000 peak because buybacks cut the share
      count.
  [5] Scott McNealy, chief executive of Sun Microsystems, in Businessweek,
      "A Talk with Scott McNealy", 31 March 2002 (bloomberg.com archive; the
      passage as quoted by Kailash Concepts): "At 10 times revenues, to give
      you a 10-year payback, I have to pay you 100% of revenues for 10 straight
      years", then the assumptions that requires (no cost of goods, no
      expenses with about 39,000 employees, no taxes, no R&D for ten years),
      ending "What were you thinking?"
  [6] CNNMoney, "10 big dot.com flops" (2010): Pets.com went public in
      February 2000, opened at $11; lost $147 million in the first nine months
      of 2000; the stock fell below $1 and stayed there; folded in November
      2000, about nine months after going public; about 300 employees laid off.
  [7] Cato Institute, "Reflections on Greenspan's Irrational Exuberance Speech
      after 25 Years" (2021): Alan Greenspan, 5 December 1996, American
      Enterprise Institute: "How do we know when irrational exuberance has
      unduly escalated asset values".
The 10% margin, 100 times profit and 100-year figures are labelled on screen
as our own illustration of McNealy's arithmetic, not data. "Nobody rings a
bell at the top" is an old market saying, not a quote. No other numbers.

    python build/youtube_ep003.py
"""

from youtube import make

# S(drawing, line, label, highlighted words, size, flip, **drawing options); SC(drawing, heading, **drawing options)
S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)

EP = dict(
    slug="yt-003-right-about-the-internet",
    title="The Dot-Com Crowd Was Right About the Internet. So Why Did They Lose?",
    thumb=dict(art=("ticker", dict(price="$80.06", change="-90%")),
               big_a="Right about<br>the internet.<br><span style='color:#0A0A0A'>Still lost.</span>", size_a=96,
               art_b=("bubble", dict(label="2000")),
               big="Right about the future. <span style='color:#D93A12'>Wrong</span> about the price.",
               small="The dot-com lesson for AI", ghost="", size=104),
    chapters=[
        dict(title="Is this 2000 again?", art=("bubble", dict(label="2000")), beats=[
            dict(say="This month, AI-linked stocks had a sharp sell-off, and one question came back everywhere. Is this two thousand again?",
                 shows=[S("ticker", "A sharp sell-off.", "November 2026", ["sell-off."], 110, price="AI", change="Sell-off"),
                        S("calendar", "Is this 2000 again?", "The question", ["2000"], 110, flip=True, day="10", month="MAR", note="2000")]),
            dict(say="On the tenth of March, two thousand, the Nasdaq closed at five thousand and forty eight. Thirty one months later, it was at one thousand one hundred and fourteen.",
                 shows=[dict(kind="number", value=5048.62, dec=2, label="Nasdaq Composite close, 10 March 2000 (Fortune)"),
                        S("chart", "31 months later: 1,114.", "October 2002", ["1,114."], 100, values=[3, 5, 8, 7, 5, 3, 2, 1], label="-78%")]),
            dict(say="That is a fall of seventy eight percent. It took fifteen years, until April twenty fifteen, to close above the old record.",
                 shows=[S("bubble", "A 78% fall.", "Peak to bottom", ["78%"], 130, pop=True, label="-78%"),
                        dict(kind="timeline", title="The Nasdaq", items=[("2000", "Peak"), ("2002", "Bottom"), ("2015", "Back")], hi=2)]),
            dict(say="The usual story is that everyone back then was a fool. We think that story is wrong, and the real one is far more useful.",
                 shows=[dict(kind="verdict", text="Everyone was a fool.", stamp="MYTH", size=120),
                        S("bulb", "The real story is more useful.", "Our reading", ["useful."], 100)]),
            dict(say="Most of the people who lost money were right. They were right about the internet. They were wrong about the price.",
                 shows=[S("figures", "Most of them were right.", "The investors of 2000", ["right."], 110, n=5, hi=2, glass=True),
                        S("globe", "Right about the internet.", "", ["internet."], 110, flip=True),
                        S("pricetag", "Wrong about the price.", "", ["Wrong"], 120, value="$", tag="?")]),
            dict(say="In this video we'll show you how both can be true at once, with three real companies and one piece of arithmetic every banker should know.",
                 show=dict(kind="icons", title="Coming up", items=[("bank", "3 companies"), ("pen", "1 sum"), ("question", "3 questions")], hi=1)),
        ]),
        dict(title="Right about the internet", art=("parcel", dict(n=3)), beats=[
            dict(say="Start with the bet itself. In the late nineteen nineties, investors said the internet would change how people shop, talk and work.",
                 shows=[S("magnifier", "Start with the bet.", "The late 1990s", ["bet."], 120, label="THE BET"),
                        dict(kind="icons", title="The internet would change how we", items=[("house", "Shop"), ("people", "Talk"), ("pen", "Work")])]),
            dict(say="That turned out to be true. If anything, they underestimated it.",
                 shows=[dict(kind="verdict", text="The internet changes everything.", stamp="TRUE", size=104),
                        S("globe", "If anything, they underestimated it.", "", ["underestimated"], 96)]),
            dict(say="Now look at one company that was right about all of it. In April two thousand and one, its founder wrote to shareholders, and the letter opened with one word.",
                 shows=[S("parcel", "Right about all of it.", "An online shop", ["all"], 110, n=3),
                        S("document", "It opened with one word.", "April 2001", ["one", "word."], 100, flip=True, title="To our shareholders", lines=5)]),
            dict(say="Ouch. The shares were down more than eighty percent from a year earlier.",
                 shows=[dict(kind="quote", text="Ouch.", hl=["Ouch."], who="Jeff Bezos, letter to Amazon.com shareholders on the year 2000", size=200),
                        S("ticker", "Down more than 80% in a year.", "The share price", ["80%"], 96, price="AMZN", change="-80%+")]),
            dict(say="Yet in the same letter, he pointed out that the company had served twenty million customers that year, up from fourteen million the year before.",
                 show=S("bars", "Customers: 14 million to 20 million.", "Same letter", ["20", "million."], 96, values=[14, 20], labels=["1999", "2000"], hi=1)),
            dict(say="And he wrote that, by almost any measure, the company was in a stronger position than at any time in its past. The price said one thing. The business said another.",
                 shows=[S("tower", "Stronger than at any time in its past.", "Same letter", ["Stronger"], 96, floors=9, label="The business"),
                        S("ticker", "The price said one thing.", "", ["price"], 110, flip=True, price="AMZN", change="Down"),
                        S("chart", "The business said another.", "", ["another."], 110, values=[2, 3, 3.6, 4.5, 5.4, 6.6], color="#0F766E", label="Customers")]),
            dict(say="The business was growing while the stock was collapsing. He quoted the investor Benjamin Graham: in the short term, the market is a voting machine; in the long term, it is a weighing machine.",
                 shows=[S("seesaw", "Business up. Stock down.", "2000", ["down."], 110, left="Business", right="Stock", tip=-1),
                        SC("ballot", "Benjamin Graham, quoted in the letter: voting machine, weighing machine")]),
            dict(say="A voting machine counts how excited people are. A weighing machine measures what the business is actually worth. In two thousand, the two had drifted very far apart.",
                 shows=[dict(kind="icon", icon="people", label="Voting", text="How excited people are.", hl=["excited"], size=96),
                        S("scale", "What it's actually worth.", "Weighing", ["worth."], 110, flip=True, left="Hype", right="Worth", tip=-1),
                        S("arrows", "Very far apart in 2000.", "", ["apart"], 110, up="Price", down="Value")]),
        ]),
        dict(title="The best company, the worst stock", art=("server", dict()), beats=[
            dict(say="If you wanted to own the internet in two thousand, you could buy the company that sold the equipment it ran on. That was Cisco.",
                 shows=[S("server", "The kit the internet ran on.", "Own the internet?", ["kit"], 100),
                        dict(kind="term", term="Cisco", text="Network equipment: the routers and switches that move internet traffic.")]),
            dict(say="From the end of nineteen ninety four to March two thousand, its shares rose about four thousand percent. For a short time that March, it was the most valuable company in the world.",
                 shows=[S("rocket", "About +4,000%.", "End of 1994 to March 2000", ["+4,000%."], 130),
                        dict(kind="number", value=550, pre="$", suf=" bn+", label="market value, late March 2000: briefly the world's largest (Sherwood News)")]),
            dict(say="And the bet on its business was right. The internet really did need all that equipment.",
                 shows=[dict(kind="verdict", text="The internet needed the kit.", stamp="TRUE", size=110),
                        dict(kind="flow", items=[("globe", "Internet grows"), ("lock", "Needs networks"), ("coin", "Cisco sells")])]),
            dict(say="The stock still fell nearly ninety percent by late two thousand and two. Its closing high had been eighty dollars and six cents.",
                 shows=[S("ticker", "Nearly -90% by late 2002.", "And yet", ["-90%"], 100, price="CSCO", change="-90%"),
                        dict(kind="number", value=80.06, dec=2, pre="$", label="Cisco's closing high, March 2000")]),
            dict(say="It did not close above that price again until December twenty twenty five. That is more than twenty five years.",
                 shows=[S("calendar", "Back above $80.06.", "Finally", ["$80.06."], 110, flip=True, day="10", month="DEC", note="2025"),
                        dict(kind="timeline", title="Cisco's share price", items=[("2000", "$80.06"), ("2002", "-90%"), ("2025", "Back above")], hi=2)]),
            dict(say="Even then, the company as a whole was worth about two hundred and fifty billion dollars less than at its peak. Buybacks had cut the number of shares, so the price came back before the value did.",
                 shows=[S("coins", "About $250 bn less in value.", "December 2025 vs March 2000", ["less"], 100, stacks=[9, 5], labels=["2000", "2025"]),
                        S("cake", "Fewer shares, so a higher price each.", "Buybacks", ["Fewer"], 96, flip=True, slices=8, hi=2)]),
            dict(say="A buyback is when a company uses its cash to buy its own shares and cancel them. The same company, cut into fewer slices, makes each slice worth more.",
                 shows=[S("coins", "A company buys its own shares.", "What a buyback is", ["own"], 100, flip=True, stacks=[3, 6, 4]),
                        SC("cake", "Fewer slices, so each one is bigger", slices=5, hi=0)]),
            dict(say="So here is the first lesson. A great company and a great investment are not the same thing. The difference is the price you pay.",
                 shows=[S("bulb", "Lesson one.", "", ["one."], 140, text="1"),
                        dict(kind="verdict", text="Great company, great investment.", stamp="NOT ALWAYS", size=104),
                        S("pricetag", "The difference is the price.", "", ["price."], 110, value="$", tag="?")]),
        ]),
        dict(title="What were you thinking?", art=("payback", dict(years=10, paid=10)), beats=[
            dict(say="The clearest explanation came from a man who ran one of the hottest companies of the boom. Scott McNealy was the chief executive of Sun Microsystems, which sold servers, the computers behind websites.",
                 shows=[S("podium", "One of the hottest companies of the boom.", "The clearest explanation", ["hottest"], 92, words=""),
                        S("server", "Scott McNealy, Sun Microsystems.", "Chief executive", ["Sun"], 96, flip=True)]),
            dict(say="In two thousand and two, looking back at his own company's share price, he told Businessweek this.",
                 show=S("document", "Looking back, in 2002.", "Businessweek interview", ["2002."], 110, title="Interview, 2002", lines=4)),
            dict(say="At ten times revenues, to give you a ten year payback, I have to pay you a hundred percent of revenues for ten straight years.",
                 show=dict(kind="quote", text="At 10 times revenues, to give you a 10-year payback, I have to pay you 100% of revenues for 10 straight years.",
                           hl=["10-year", "payback,"], who="Scott McNealy, Sun Microsystems, Businessweek, 2002", size=76)),
            dict(say="Then he listed what that would take. No cost of making anything. No salaries, though Sun had about thirty nine thousand employees. No taxes. And no research for ten years.",
                 shows=[S("payback", "What it would take.", "His list", ["take."], 110, years=10, paid=10, label="Every dollar of revenue, to you"),
                        S("factory", "No cost of making anything.", "1", ["No"], 100, flip=True, closed=True),
                        S("figures", "No salaries for 39,000 people.", "2", ["No"], 96, n=6, hi=0),
                        S("document", "No taxes.", "3", ["No"], 130, flip=True, title="Tax bill", lines=3, stamp="$0"),
                        S("bulb", "No research for 10 years.", "4", ["No"], 100, text="R&D")]),
            dict(say="His question to the investors who had paid that price was short. What were you thinking?",
                 show=S("speech", "What were you thinking?", "McNealy, 2002", ["thinking?"], 110, text="What were you thinking?")),
            dict(say="Here is the arithmetic, because it is the most useful thing in this video. A price of ten times revenue means that even if a company handed you every dollar it took in, you would wait ten years to get your money back.",
                 shows=[S("bulb", "The arithmetic.", "Price to sales", ["arithmetic."], 130, text="10x"),
                        SC("payback", "10 times revenue: every dollar of sales, paid to you, for 10 years", years=10, paid=10, label="")]),
            dict(say="But revenue is not profit. Take an illustration where a company keeps ten cents of profit from every dollar of sales. Then ten times revenue is a hundred times profit.",
                 shows=[dict(kind="verdict", text="Revenue is profit.", stamp="NO", size=130),
                        S("cake", "Keep 10 cents in each dollar.", "An illustration", ["10", "cents"], 100, flip=True, slices=10, hi=1),
                        dict(kind="number", value=100, suf="x", label="price to profit, at 10 times sales and a 10% margin (our illustration)")]),
            dict(say="At that price, if profits never grew, the wait would be a hundred years. So the price is not a number about today. It is a bet that profits will grow very fast, for a very long time.",
                 shows=[S("calendar", "A 100-year wait.", "If profits stay flat", ["100-year"], 120, flip=True, day="100", month="YEARS", note="illustration"),
                        dict(kind="verdict", text="A number about today.", stamp="NO", size=120),
                        S("chart", "A bet on fast growth, for years.", "What the price assumes", ["growth,"], 100, values=[1, 1.5, 2.3, 3.4, 4.8, 6.5, 8.5], color="#0F766E", label="Profits")]),
            dict(say="If you are preparing for a banking interview, this is the idea behind every multiple. A price to earnings ratio, before any growth, is simply how many years of today's profit you are paying for.",
                 shows=[S("document", "The idea behind every multiple.", "Interview prep", ["multiple."], 96, title="Valuation", lines=5, stamp="P/E"),
                        S("payback", "P/E: years of today's profit you pay for.", "Before growth", ["years"], 92, flip=True, years=10, paid=10, label="P/E of 10")]),
        ]),
        dict(title="Nine months on the market", art=("petbowl", dict(closed=True)), beats=[
            dict(say="Some companies never got the chance to grow into their price. Pets dot com sold pet supplies online, and went public in February two thousand.",
                 shows=[S("bubble", "Some never got the chance.", "", ["chance."], 110, label="2000"),
                        S("petbowl", "Pet supplies, online.", "Pets.com, IPO February 2000", ["online."], 110, flip=True, closed=False)]),
            dict(say="Its shares opened at eleven dollars. In the first nine months of that year, it lost a hundred and forty seven million dollars.",
                 shows=[S("ticker", "Opened at $11.", "February 2000", ["$11."], 130, price="$11", change="IPO", up=True),
                        dict(kind="number", value=147, pre="$", suf="m", label="lost in the first nine months of 2000 (CNNMoney)")]),
            dict(say="The shares fell below a dollar and stayed there. In November two thousand, about nine months after going public, the company shut down, and about three hundred people lost their jobs.",
                 shows=[S("ticker", "Below $1, and it stayed there.", "Autumn 2000", ["$1,"], 96, price="<$1", change="Below $1"),
                        S("petbowl", "Shut down after 9 months.", "November 2000", ["9", "months."], 110, flip=True, closed=True)]),
            dict(say="Here is the part that is easy to miss. A young company that loses money needs new cash from investors to keep going. When prices fall, the door to that cash closes, so a falling share price can end the business itself.",
                 shows=[S("bulb", "The part that is easy to miss.", "", ["miss."], 100, text="!"),
                        dict(kind="flow", items=[("down", "Losses"), ("hand", "Needs new cash"), ("lock", "Investors leave")]),
                        S("bubble", "A falling price can end the business.", "", ["end"], 96, flip=True, pop=True, label="END")]),
            dict(say="Selling pet food online was not a silly idea. Plenty of people buy it that way now. The idea was early, the costs were high, and the money ran out first.",
                 shows=[dict(kind="verdict", text="A silly idea.", stamp="MYTH", size=140),
                        S("parcel", "Plenty of people buy it that way now.", "Today", ["now."], 92, n=2),
                        S("bubble", "The money ran out first.", "", ["first."], 110, pop=True, label="CASH")]),
            dict(say="That's the second lesson. Being in the right industry is not the same as having a business that can survive long enough to win.",
                 shows=[S("bulb", "Lesson two.", "", ["two."], 140, text="2"),
                        S("tower", "The right industry is not enough.", "Survive long enough to win", ["enough."], 96, flip=True, crack=True, floors=8)]),
        ]),
        dict(title="The problem with calling it", art=("bell", dict()), beats=[
            dict(say="If the prices were so clearly too high, why didn't someone say so? Someone did, and early.",
                 shows=[dict(kind="icon", icon="question", label="Hindsight", text="Why didn't anyone say so?", hl=["say", "so?"], size=96),
                        S("podium", "Someone did. Early.", "Washington, 1996", ["Early."], 130, words="")]),
            dict(say="In December nineteen ninety six, the chairman of the Federal Reserve, Alan Greenspan, asked in a speech how we know when irrational exuberance has unduly escalated asset values.",
                 show=dict(kind="quote", text="How do we know when irrational exuberance has unduly escalated asset values",
                           hl=["irrational", "exuberance"], who="Alan Greenspan, Federal Reserve chairman, 5 December 1996", size=88)),
            dict(say="It became a famous phrase. And the Nasdaq kept climbing for more than three years after it, until March two thousand.",
                 shows=[S("speech", "A famous phrase.", "December 1996", ["famous"], 120, text="Irrational exuberance"),
                        S("chart", "Then it kept climbing for 3 years.", "1997 to 2000", ["climbing"], 96, values=[2, 2.6, 2.4, 3.5, 4.4, 4.1, 6, 8.4], label="Nasdaq")]),
            dict(say="That is the trap. Being early looks exactly like being wrong, sometimes for years.",
                 shows=[S("bell", "That is the trap.", "Nobody rings a bell at the top", ["trap."], 120),
                        S("seesaw", "Early looks like wrong.", "For years", ["wrong."], 120, flip=True, left="Early", right="Wrong", tip=0)]),
            dict(say="So a warning is not useless. It tells you the price is high. It does not tell you when it will fall.",
                 shows=[S("clock", "A warning is not useless.", "", ["not"], 110, time="11:55"),
                        S("pricetag", "It tells you the price is high.", "", ["high."], 100, flip=True, value="$$$", tag="!"),
                        S("calendar", "Not when it will fall.", "", ["when"], 120, day="?", month="WHEN", note="nobody knows")]),
            dict(say="And when the fall did come, it took the Nasdaq fifteen years to get back. Calling the top is hard. Living through the bottom is harder.",
                 shows=[dict(kind="timeline", title="The Nasdaq, 1996 to 2015", items=[("1996", "Warning"), ("2000", "Peak"), ("2002", "Bottom"), ("2015", "Back")], hi=3),
                        S("magnifier", "Calling the top is hard.", "", ["hard."], 110, label="TOP?"),
                        S("dominoes", "Living through the bottom is harder.", "", ["harder."], 96, flip=True, labels=["Peak", "Fall", "Wait", "Back"], fall=2)]),
        ]),
        dict(title="Three questions for any boom", art=("magnifier", dict(label="?")), beats=[
            dict(say="So what do you do with this, now that AI is the story everyone is arguing about? We can't tell you whether today is two thousand. Nobody can, from a chart.",
                 shows=[S("speech", "The story everyone argues about.", "2026", ["argues"], 100, text="Is AI a bubble?"),
                        dict(kind="icon", icon="question", label="Honestly", text="Is today 2000? We can't tell you.", hl=["can't"], size=92),
                        S("chart", "Nobody can, from a chart.", "", ["chart."], 110, flip=True, values=[2, 4, 3, 6, 5, 8, 7], color="#0A0A0A", label="?", arrow=False)]),
            dict(say="But the dot-com crash gives you three questions that work on any boom.",
                 show=dict(kind="icons", title="Three questions for any boom", items=[("check", "Is it real?"), ("coin", "Who keeps the money?"), ("search", "What's the price?")], hi=2)),
            dict(say="Question one: is the thing real? In two thousand, it was. The internet was real, and that is exactly why the story was so convincing.",
                 shows=[S("magnifier", "Question 1: is it real?", "", ["real?"], 110, label="REAL?"),
                        S("globe", "In 2000, it was.", "", ["was."], 130, flip=True),
                        S("speech", "That's why the story convinced people.", "", ["convinced"], 96, text="This changes everything")]),
            dict(say="Question two: who keeps the money? Our reading is that much of the value went to customers, and to the few companies that survived, not to everyone who bought in.",
                 shows=[S("coins", "Question 2: who keeps the money?", "", ["money?"], 100, stacks=[2, 4, 8]),
                        S("figures", "Customers, and the few who survived.", "Our reading", ["survived."], 96, flip=True, n=5, hi=1)]),
            dict(say="Question three: what price is already paid? Ask how many years of revenue, and of profit, the price is asking you to wait.",
                 shows=[S("pricetag", "Question 3: what price is paid?", "", ["price"], 100, value="10x", tag="?"),
                        SC("payback", "How many years would you wait?", years=10, paid=6, label="")]),
            dict(say="Put the three together and you get the dot-com crash in one line. The technology was real, the money went to a few, and the price had already paid for a future that took years, even decades, to arrive.",
                 shows=[dict(kind="icons", title="The crash in one line", items=[("check", "Real"), ("coin", "A few kept it"), ("clock", "Price paid early")], hi=2),
                        S("dominoes", "The future took years to arrive.", "Cisco: 25 years. Nasdaq: 15.", ["decades"], 96, labels=["Real", "Few", "Price", "Wait"], fall=4)]),
            dict(say="Those questions don't tell you what to buy, and this video isn't financial advice. They tell you what the story leaves out.",
                 shows=[dict(kind="icon", icon="book", label="History, not advice", text="Not financial advice.", hl=["advice."], size=110),
                        S("book", "What the story leaves out.", "", ["leaves", "out."], 100, flip=True, title="The story")]),
            dict(say="The people of two thousand saw the future clearly. What they missed was the price. If you had been there, which of these companies would you have bought? Tell us in the comments.",
                 shows=[S("figures", "They saw the future.", "2000", ["future."], 120, n=4, glass=True),
                        S("pricetag", "They missed the price.", "", ["price."], 120, flip=True, value="$", tag="?"),
                        dict(kind="icons", title="Which would you have bought?", items=[("globe", "Cisco"), ("book", "Amazon"), ("house", "Pets.com")]),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "On 10 March 2000 the Nasdaq closed at 5,048.62. Thirty-one months later it had lost 78%, and it didn't get back for 15 years. "
        "You've probably heard that everyone in 2000 was a fool. We don't buy it. Most of the people who lost money were right about the internet; "
        "they were wrong about the price. We follow Amazon, whose shares fell more than 80% while it went from 14 million customers to 20 million. "
        "Then Cisco, which took more than 25 years to get back to its 2000 share price. And Pets.com, which lasted about nine months. "
        "We'll work through Scott McNealy's famous price-to-sales sum (it's the logic behind every multiple you'll meet in a banking interview), "
        "and we'll finish with three questions you can ask about any boom, AI included. What would you have bought?\n\n"
        "Sources: SWBC, Market Commentary, week of 9 November 2026; Fortune, \"Nasdaq surpasses Internet bubble peak to set new record\" (23 April 2015); "
        "Jeff Bezos, 2000 letter to Amazon.com shareholders (Seattle Times archive, 2001); Sherwood News, \"After a quarter century, Cisco surpasses "
        "dot-com bubble closing high\" (December 2025) and Bloomberg (10 December 2025); Scott McNealy, \"A Talk with Scott McNealy\", Businessweek (31 March 2002); "
        "CNNMoney, \"10 big dot.com flops\" (2010); Cato Institute, \"Reflections on Greenspan's Irrational Exuberance Speech after 25 Years\" (2021). "
        "The 10% margin and 100-year payback are our own illustration of the arithmetic, not data."),
    tags=["dot-com bubble", "dot com crash", "AI bubble", "Nasdaq 2000", "stock market crash", "Cisco", "Amazon 2000",
          "Pets.com", "price to sales", "valuation", "history of finance", "investing lessons", "irrational exuberance", "finance explained"],
)

if __name__ == "__main__":
    make(EP)
