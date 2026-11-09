"""
YouTube #2: the Berlin Wall fell on 9 November 1989. Eight months later West
Germany had to answer a finance question nobody had answered before: what is
a whole country's money worth? Politics and finance. Released on the 37th
anniversary.

Point of view: the usual story calls the one-to-one rate either a gift or a
blunder. Our reading: an exchange rate is a price, and setting it moves the
bill, it does not cancel it. A high rate is paid in jobs, a low rate in people
leaving, and Germany chose to pay in transfers.

Every claim, sourced:
  [1] The World (PRX), "How a mistake at a press conference helped topple the
      Berlin Wall", 2 Oct 2020: 9 Nov 1989, press conference from 6 p.m.;
      Guenter Schabowski read the new travel rules, having received the paper
      shortly before; asked when, "as far as I know, it's effective
      immediately"; the passport process was meant to start the next morning;
      between 10 p.m. and midnight thousands rushed to the border.
  [2] Deutsche Bundesbank, "No blueprint for reunification": about 800,000
      people moved from the GDR to West Germany in the second half of 1989 and
      first half of 1990; 6 Feb 1990 Bundesbank President Karl Otto Poehl said
      on TV that monetary union was too early, the same day Chancellor Kohl
      announced negotiations; the D-Mark was introduced in the GDR on 1 July
      1990; wages and salaries converted one to one; average GDR wage about 40%
      of the West German level, about 20% at one to two, below West German
      social assistance (Richard Schroeder); Reint Gropp: "The conversion rate
      of course meant dramatic appreciation for East German products",
      traditional markets in Eastern Europe had shrunk, and a cheaper rate would
      have meant a much larger exodus of skilled workers; Treuhand strategy
      "to sell firms as quickly as possible".
  [3] Leipzig Runde Ecke museum (runde-ecke-leipzig.de), March 1990: the
      18 March 1990 election "was a referendum for the rapid introduction of
      the D-Mark", turnout above 93%.
  [4] Konrad Adenauer Foundation, Geschichte der CDU, "Die Wirtschafts-,
      Waehrungs- und Sozialunion ... tritt in Kraft": on 30 March 1990 the
      Bundesbank council proposed two to one for everything except savings up
      to 2,000 marks per inhabitant; Labour Minister Norbert Bluem argued for
      one to one; GDR parties spoke of a broken promise ("Wortbruch");
      Hans Tietmeyer warned one to one would inflate the money supply;
      compromise on 1 May; treaty signed 18 May 1990 by Theo Waigel and
      Walter Romberg.
  [5] German History in Documents and Images (GHDI), "GDR citizens protest
      against the proposed 2:1 exchange rate, 5 April 1990": about 100,000
      people in front of the Palast der Republik in East Berlin demanded 1:1.
  [6] DDR Museum Berlin, "Monetary, economic and social union" (2018):
      allowances at one to one: up to 2,000 marks for children up to 14,
      4,000 under 60, 6,000 over 60; everything above at two to one;
      Lothar de Maiziere on signing day: "No GDR citizen will be worse off
      than before. On the contrary!"
  [7] Federal Reserve Bank of San Francisco, Economic Letter 90-26 (1990):
      official rate 3 Ostmarks per D-Mark, black market 5 to 6.
  [8] GHDI, "The Economic and Currency Union takes effect, July 1, 1990"
      (Tagesschau report): a West German bank branch opened at midnight on
      Alexanderplatz with about 10,000 people celebrating; the rush began at
      9 a.m., many waited for hours; most took less than the maximum and
      began saving; "The Trabi, once an object of desire, is now being
      kicked."
  [9] Akerlof, Rose, Yellen and Hessenius, "East Germany in from the Cold",
      Brookings Papers on Economic Activity 1991(1): firms employing
      8 percent of the labour force were viable after union.
  [10] Library of Congress, Germany: A Country Study, "Unification and Its
      Aftermath": industrial production in eastern Germany fell to less than
      half the previous rate; the Treuhand took over about 8,000 enterprises
      and had privatised some 14,000 by the end of 1994 (firms were split);
      federal spending in the east well over DM350 billion in the first three
      years.
  [11] Obituary of Karl Otto Poehl (inkl, Dec 2014): in spring 1991 he told a
      European Parliament committee the result was "a disaster"; he laid
      groundwork for the European Central Bank. Bundesbank presidency
      1980 to 1991.
  [12] Federal Reserve History, Janet L. Yellen: Chair of the Federal Reserve
      Board 2014 to 2018.
No other numbers are used.

    python build/youtube_ep002.py
"""

from youtube import make

EP = dict(
    slug="yt-002-price-of-a-country",
    title="The Wall Fell. Then Germany Had to Price a Whole Country",
    music_seed=1989,
    thumb=dict(art=("notes", dict(left="1", right="1", n_left=1)),
               big_a="1 mark =<br><span style='color:#0A0A0A'>1 mark?</span>", size_a=120,
               big="What is a <span style='color:#D93A12'>country</span> worth?",
               small="Berlin, 1990", ghost="1:1", size=120),
    chapters=[
        dict(title="The night the Wall opened", art=("wall", dict(gap=True)), beats=[
            dict(say="On the ninth of November, nineteen eighty nine, at a press conference in East Berlin, an official read out new travel rules he had only just been handed.",
                 show=dict(kind="sketch", art="podium", label="East Berlin, 9 Nov 1989, 6 p.m.", text="New travel rules, read out live.", hl=["live."], size=96)),
            dict(say="A reporter asked when they took effect. Guenter Schabowski answered: as far as I know, immediately.",
                 shows=[dict(kind="icon", icon="question", label="The question", text="When does this start?", hl=["start?"], size=110),
                        dict(kind="quote", text="As far as I know, it's effective immediately.", hl=["immediately."], who="Guenter Schabowski, 9 Nov 1989")]),
            dict(say="It was meant to start the next morning, with passports. Instead, between ten and midnight, thousands of people walked to the border, and the Wall opened.",
                 shows=[dict(kind="sketch", art="calendar", opts=dict(day="10", month="NOV", note="The real plan"), label="What the paper meant", text="The next morning. With passports.", hl=["morning."], size=96),
                        dict(kind="scene", art="wall", opts=dict(gap=True, label="10 p.m. to midnight"), label="What happened instead")]),
            dict(say="Nobody had planned it this way. The guards had no special instructions, so at first they turned people away, and then, as the crowds grew, they began letting them through.",
                 shows=[dict(kind="verdict", text="A plan?", stamp="NONE", size=150),
                        dict(kind="sketch", art="queue", opts=dict(n=8, label="BORDER"), label="That night", text="Then the crowds grew.", hl=["grew."], size=110)]),
            dict(say="That's the part of the story everyone knows. This video is about the part that came next, and it's a finance story.",
                 shows=[dict(kind="sketch", art="book", opts=dict(title="The famous part"), label="The story you know", text="The night the Wall opened.", hl=["opened."], size=96),
                        dict(kind="sketch", art="notes", opts=dict(left="?", right="?"), label="The story you don't", text="A finance story.", hl=["finance"], size=120)]),
            dict(say="Because once the Wall was gone, someone had to answer a question no textbook covers. What is a whole country's money worth?",
                 shows=[dict(kind="verdict", text="No textbook covers this.", stamp="NEW", size=110),
                        dict(kind="sketch", art="magnifier", opts=dict(label="1 : ?"), label="The question", text="What is a country's money worth?", hl=["worth?"], size=96)]),
        ]),
        dict(title="Two currencies, one country", art=("notes", dict(left="M", right="DM")), beats=[
            dict(say="East Germany paid in Ostmarks. West Germany paid in Deutschmarks, guarded by the Bundesbank.",
                 shows=[dict(kind="sketch", art="notes", opts=dict(left="M", right="", lab_r=""), label="East", text="The Ostmark.", hl=["Ostmark."], size=130),
                        dict(kind="split", left=("coin", "East", "Ostmark"), right=("bank", "West", "D-Mark"), mid="vs")]),
            dict(say="An exchange rate sounds technical, but it is just a price. It tells you how much of one money you hand over to get the other.",
                 shows=[dict(kind="verdict", text="Technical?", stamp="JUST A PRICE", size=150),
                        dict(kind="sketch", art="notes", opts=dict(left="?", right="1"), label="What a rate says", text="How much of one money buys the other.", hl=["buys"], size=92)]),
            dict(say="For a family in East Berlin, it would decide what their savings were worth. For a factory, it would decide what everything it made would cost.",
                 shows=[dict(kind="sketch", art="house", opts=dict(price="Savings?"), label="For a family", text="What their savings are worth.", hl=["savings"], size=100),
                        dict(kind="sketch", art="factory", label="For a factory", text="What everything it makes costs.", hl=["costs."], size=100, flip=True)]),
            dict(say="On paper, the official rate was three Ostmarks for one Deutschmark. On the black market, people paid five or six.",
                 shows=[dict(kind="sketch", art="rateboard", opts=dict(rate="3 : 1", sub="OFFICIAL RATE"), label="On paper", text="Three Ostmarks for one D-Mark.", hl=["Three"], size=96, flip=True),
                        dict(kind="compare", left=("Official rate", "3 : 1"), right=("Black market", "5-6 : 1"), note="Ostmarks per D-Mark, San Francisco Fed, 1990")]),
            dict(say="And people were leaving. The Bundesbank counts about eight hundred thousand who moved west in the year around the Wall's fall.",
                 shows=[dict(kind="scene", art="suitcase", opts=dict(n=3), label="Meanwhile"),
                        dict(kind="number", value=800000, label="moved from East to West, mid 1989 to mid 1990 (Bundesbank)")]),
            dict(say="So the D-Mark became a political demand. A museum in Leipzig describes the March election of nineteen ninety as a referendum on bringing it in fast.",
                 shows=[dict(kind="sketch", art="speech", opts=dict(text="We want the D-Mark!"), label="Spring 1990", text="A political demand.", hl=["political"], size=120),
                        dict(kind="sketch", art="document", opts=dict(title="18 March 1990", lines=5, stamp="D-MARK"), label="The election", text="A referendum on the D-Mark.", hl=["D-Mark."], size=96)]),
            dict(say="The head of the Bundesbank, Karl Otto Poehl, said on television that a monetary union was too early. The same day, Chancellor Kohl announced talks to start one.",
                 shows=[dict(kind="verdict", text="Monetary union? Too early.", stamp="BUNDESBANK", size=100),
                        dict(kind="timeline", title="6 February 1990", items=[("Bundesbank", "Too early"), ("Chancellor", "Talks announced")], hi=1)]),
        ]),
        dict(title="The fight over one number", art=("rateboard", dict(rate="? : 1")), beats=[
            dict(say="Everything came down to a single number: how many Ostmarks for one Deutschmark.",
                 show=dict(kind="sketch", art="rateboard", opts=dict(rate="? : 1"), label="Spring 1990", text="One number decides everything.", hl=["number"], size=100)),
            dict(say="At the end of March, the Bundesbank proposed two to one for almost everything. Only the first two thousand marks of each person's savings would convert one to one.",
                 shows=[dict(kind="sketch", art="notes", opts=dict(left="2", right="1", n_left=2), label="The Bundesbank's plan, 30 March", text="Two to one.", hl=["Two"], size=150),
                        dict(kind="sketch", art="coins", opts=dict(stacks=[3], labels=["First 2,000 marks: 1 : 1"]), label="The exception", text="Small savings, one to one.", hl=["savings,"], size=96)]),
            dict(say="Why so tough? The Bundesbank's job was to protect the D-Mark from inflation. Convert a whole country's money too generously, and you create a mountain of new D-Marks overnight.",
                 shows=[dict(kind="icon", icon="question", label="The central bank's view", text="Why so tough?", hl=["tough?"], size=130),
                        dict(kind="sketch", art="tower", opts=dict(label="D-Mark"), label="Its one job", text="Protect the D-Mark.", hl=["Protect"], size=110),
                        dict(kind="sketch", art="coins", opts=dict(stacks=[4, 7, 10]), label="Too generous a rate", text="New D-Marks, overnight.", hl=["overnight."], size=110)]),
            dict(say="East Germans heard a broken promise. In early April, about a hundred thousand people gathered in East Berlin to demand one to one.",
                 shows=[dict(kind="verdict", text="A broken promise.", stamp="WORTBRUCH", size=120),
                        dict(kind="sketch", art="figures", opts=dict(n=7, hi=3), label="East Berlin, 5 April 1990", text="About 100,000 people.", hl=["100,000"], size=100)]),
            dict(say="In Bonn, the labour minister argued for one to one. Others, like Hans Tietmeyer, warned it would pump money into the economy and put the D-Mark's stability at risk.",
                 shows=[dict(kind="sketch", art="seesaw", opts=dict(left="1 : 1", right="2 : 1", tip=-1), label="Bonn, divided", text="Labour: one to one.", hl=["one", "to", "one."], size=100),
                        dict(kind="flow", items=[("doc", "1 : 1"), ("coin", "More money"), ("fire", "D-Mark at risk?")])]),
            dict(say="The compromise came on the first of May. Wages and salaries at one to one. Savings at one to one up to an allowance set by age. Everything above it, two to one.",
                 shows=[dict(kind="sketch", art="calendar", opts=dict(day="1", month="MAY", note="The deal"), label="1990", text="The compromise.", hl=["compromise."], size=130),
                        dict(kind="sketch", art="rateboard", opts=dict(rate="1 : 1", sub="WAGES AND SALARIES"), label="Pay", text="Wages: one to one.", hl=["Wages:"], size=110),
                        dict(kind="sketch", art="coins", opts=dict(stacks=[2, 4, 6], labels=["Up to 14", "Under 60", "Over 60"]), label="Savings allowances at 1 : 1", text="2,000, 4,000 or 6,000 marks.", hl=["6,000"], size=88),
                        dict(kind="sketch", art="notes", opts=dict(left="2", right="1", n_left=2), label="Above the allowance", text="Two to one.", hl=["Two"], size=150)]),
            dict(say="The treaty was signed on the eighteenth of May. East Germany's prime minister, Lothar de Maiziere, promised that nobody would be worse off than before.",
                 shows=[dict(kind="sketch", art="handshake", opts=dict(left="Bonn", right="East Berlin"), label="18 May 1990", text="The treaty is signed.", hl=["signed."], size=110),
                        dict(kind="quote", text="No GDR citizen will be worse off than before. On the contrary!", hl=["worse", "off"], who="Lothar de Maiziere, 18 May 1990", size=84)]),
        ]),
        dict(title="Sunday, the first of July", art=("fireworks", dict()), beats=[
            dict(say="The D-Mark arrived at midnight on Sunday, the first of July, nineteen ninety. At the same moment, the border controls between the two Germanys ended.",
                 shows=[dict(kind="sketch", art="calendar", opts=dict(day="1", month="JUL", note="Midnight"), label="1990", text="The D-Mark arrives.", hl=["D-Mark"], size=120),
                        dict(kind="sketch", art="wall", opts=dict(gap=True), label="Also at midnight", text="Border controls end.", hl=["end."], size=110)]),
            dict(say="A West German bank opened a branch on Alexanderplatz at midnight, and the evening news counted about ten thousand people there. There were fireworks and car horns.",
                 shows=[dict(kind="sketch", art="queue", opts=dict(n=7), label="Alexanderplatz, 00:00", text="About 10,000 people.", hl=["10,000"], size=110),
                        dict(kind="scene", art="fireworks", label="East Berlin, that night")]),
            dict(say="In the morning, people queued for hours for the new money. Then most of them did something surprising. They saved it.",
                 shows=[dict(kind="sketch", art="clock", opts=dict(time="9:00"), label="Sunday morning", text="Queues for hours.", hl=["hours."], size=120),
                        dict(kind="icon", icon="question", label="Then", text="Something surprising.", size=110),
                        dict(kind="sketch", art="coins", opts=dict(stacks=[2, 4, 7]), label="What most people did", text="They saved it.", hl=["saved"], size=140)]),
            dict(say="Some took out the full amount they were allowed that day. Most took less, and far less cash crossed the counters than the banks expected.",
                 shows=[dict(kind="sketch", art="queue", opts=dict(n=5), label="At the counter", text="Some took the maximum.", hl=["maximum."], size=110),
                        dict(kind="sketch", art="bank", opts=dict(label="Bank"), label="At the counters", text="Far less cash than expected.", hl=["less"], size=100)]),
            dict(say="The reporter put the caution down to forty years of socialism. And he noticed a sign of what was coming. The Trabi, once an object of desire, is now being kicked.",
                 shows=[dict(kind="icon", icon="clock", label="Why the caution", text="Forty years of socialism.", hl=["socialism."], size=110),
                        dict(kind="icon", icon="search", label="A sign", text="Of what was coming.", hl=["coming."], size=110),
                        dict(kind="sketch", art="car", opts=dict(kicked=True), label="Tagesschau, 1 July 1990", text="The Trabi is being kicked.", hl=["kicked."], size=100)]),
        ]),
        dict(title="The hangover", art=("factory", dict(closed=True)), beats=[
            dict(say="Here's what the kicked car meant. Overnight, everything East German factories made was priced in D-Marks, at one to one.",
                 shows=[dict(kind="sketch", art="car", label="The kicked car", text="What it meant.", hl=["meant."], size=130),
                        dict(kind="sketch", art="factory", label="Overnight", text="Priced in D-Marks.", hl=["D-Marks."], size=120)]),
            dict(say="The economist Reint Gropp put it plainly. The conversion rate meant dramatic appreciation for East German products.",
                 shows=[dict(kind="sketch", art="figures", opts=dict(n=1, glass=True), label="An economist's view", text="Reint Gropp, economist.", size=100),
                        dict(kind="quote", text="The conversion rate of course meant dramatic appreciation for East German products.", hl=["dramatic", "appreciation"], who="Reint Gropp, to the Bundesbank", size=78)]),
            dict(say="Here's the arithmetic. Before the union, a West German on the black market got five or six Ostmarks for one D-Mark. After it, one mark of East German price cost one full D-Mark. To that buyer, the same price tag was suddenly five or six times dearer.",
                 shows=[dict(kind="icon", icon="pen", label="Do the maths", text="The arithmetic.", hl=["arithmetic."], size=130),
                        dict(kind="sketch", art="notes", opts=dict(left="5-6", right="1", n_left=2), label="Before: black market", text="5 or 6 Ostmarks for 1 D-Mark.", hl=["5", "6"], size=92),
                        dict(kind="sketch", art="notes", opts=dict(left="1", right="1"), label="After: 1 July 1990", text="1 mark of price, 1 D-Mark.", hl=["1", "D-Mark."], size=92),
                        dict(kind="compare", left=("Price tag, before", "1/6-1/5"), right=("Same tag, after", "1"), note="Five or six times dearer to a Western buyer")]),
            dict(say="Their goods suddenly cost far more, at home and abroad. And the old export markets in Eastern Europe were shrinking.",
                 shows=[dict(kind="sketch", art="arrows", opts=dict(up="Price", down="Sales"), label="What appreciation does", text="Goods cost far more.", hl=["more."], size=120),
                        dict(kind="sketch", art="globe", label="Abroad", text="Old markets, shrinking.", hl=["shrinking."], size=110)]),
            dict(say="In nineteen ninety one, four economists, including a future chair of the Federal Reserve, Janet Yellen, estimated which firms could still cover their costs. Firms employing just eight percent of the workforce.",
                 shows=[dict(kind="sketch", art="figures", opts=dict(n=4, glass=True, labels=["Akerlof", "Rose", "Yellen", "Hessenius"]), label="Brookings, 1991", text="Who could survive?", hl=["survive?"], size=110),
                        dict(kind="scene", art="cake", opts=dict(slices=12, hi=1), label="Firms employing 8% of workers: viable")]),
            dict(say="Industrial production in the East fell to less than half. The Treuhand, the agency that took over state firms, set out to sell them as fast as possible.",
                 shows=[dict(kind="sketch", art="chart", opts=dict(values=[9, 9, 8, 6, 4, 3.5, 3.6], label="< half"), label="Industrial output, East", text="Less than half.", hl=["half."], size=130),
                        dict(kind="sketch", art="factory", opts=dict(closed=True, label="For sale"), label="The Treuhand", text="Sell, as fast as possible.", hl=["fast"], size=100)]),
            dict(say="It took over about eight thousand enterprises. By the end of nineteen ninety four it had privatised some fourteen thousand, because big combines were broken into smaller pieces to find buyers.",
                 shows=[dict(kind="number", value=8000, pre="~", label="enterprises taken over by the Treuhand (Library of Congress)"),
                        dict(kind="sketch", art="bricks", opts=dict(n=28, red=0, label="~14,000 privatised by end 1994"), label="Broken up to be sold", text="Smaller pieces, more sales.", hl=["pieces,"], size=96)]),
            dict(say="By the spring of nineteen ninety one, Karl Otto Poehl told European lawmakers the result was a disaster. He left the Bundesbank that same year.",
                 shows=[dict(kind="quote", text="A disaster.", hl=["disaster."], who="Karl Otto Poehl, spring 1991", size=150),
                        dict(kind="sketch", art="bank", opts=dict(label="Bundesbank"), label="1991", text="He left the Bundesbank.", hl=["left"], size=100)]),
        ]),
        dict(title="So was one to one a mistake?", art=("scale", dict(left="1:1", right="2:1", tip=0)), beats=[
            dict(say="The easy answer is yes. Set the rate lower, and the factories would have been cheaper and more of them would have survived.",
                 shows=[dict(kind="verdict", text="A mistake?", stamp="EASY ANSWER", size=140),
                        dict(kind="sketch", art="factory", label="The argument", text="A lower rate saves factories.", hl=["saves"], size=100)]),
            dict(say="But look at the other side of the price. The average East German wage was about forty percent of the West German level.",
                 shows=[dict(kind="sketch", art="scale", opts=dict(left="Firms", right="Workers", tip=0), label="Every price has two sides", text="The other side.", hl=["other"], size=130),
                        dict(kind="sketch", art="bars", opts=dict(values=[100, 40], labels=["West", "East"], hi=1), label="Average wage, West = 100 (Bundesbank)", text="About 40% of the West.", hl=["40%"], size=100)]),
            dict(say="At two to one, it would have been about twenty percent. That is below what West Germany paid people on social assistance.",
                 shows=[dict(kind="sketch", art="bars", opts=dict(values=[100, 40, 20], labels=["West", "1 : 1", "2 : 1"], hi=2), label="East German wage, West = 100", text="At 2 : 1, about 20%.", hl=["20%."], size=100),
                        dict(kind="verdict", text="Below social assistance.", stamp="TOO LOW", size=110)]),
            dict(say="And people were already leaving. Gropp's view is that a cheaper rate would have meant a much bigger exodus of skilled workers.",
                 shows=[dict(kind="scene", art="suitcase", opts=dict(n=3), label="Already leaving"),
                        dict(kind="sketch", art="wall", opts=dict(gap=True), label="No wall to stop it", text="A bigger exodus.", hl=["exodus."], size=120)]),
            dict(say="And there was the politics. Voters had just backed the D-Mark, and a hundred thousand people had marched against two to one. A harsher rate would have looked like the broken promise they feared.",
                 shows=[dict(kind="sketch", art="document", opts=dict(title="March 1990", lines=4, stamp="D-MARK"), label="The vote", text="Voters backed the D-Mark.", hl=["D-Mark."], size=110),
                        dict(kind="sketch", art="figures", opts=dict(n=7, hi=0), label="5 April 1990", text="They marched against 2 : 1.", hl=["against"], size=100),
                        dict(kind="verdict", text="A harsher rate.", stamp="WORTBRUCH", size=130)]),
            dict(say="Our verdict? One to one was neither a blunder nor a gift. It was a choice about who carries the cost, made in a hurry, months after a border opened by accident.",
                 shows=[dict(kind="icon", icon="scales", label="Our verdict", text="Blunder or gift?", hl=["gift?"], size=130),
                        dict(kind="verdict", text="Neither.", stamp="A CHOICE", size=170),
                        dict(kind="timeline", title="Eight months", items=[("Nov 1989", "Border opens"), ("Jul 1990", "Rate is set")], hi=1)]),
            dict(say="So the real choice was never cheap or expensive. It was who pays the bill.",
                 shows=[dict(kind="verdict", text="Cheap or expensive?", stamp="WRONG QUESTION", size=110),
                        dict(kind="sketch", art="document", opts=dict(title="The bill", lines=5, stamp="WHO PAYS?"), label="The right question", text="Who pays?", hl=["pays?"], size=160)]),
        ]),
        dict(title="Where the bill went", art=("document", dict(title="The bill", lines=4, stamp="PAID")), beats=[
            dict(say="Set the rate high, and you pay in jobs. Set it low, and you pay in people leaving.",
                 shows=[dict(kind="sketch", art="factory", opts=dict(closed=True), label="Rate high", text="You pay in jobs.", hl=["jobs."], size=120),
                        dict(kind="scene", art="suitcase", opts=dict(n=4), label="Rate low: you pay in people leaving")]),
            dict(say="Germany chose a high rate and then paid a third way, with money. In the first three years, federal spending in the East came to well over three hundred and fifty billion D-Marks.",
                 shows=[dict(kind="flow", items=[("bank", "West"), ("coin", "Transfers"), ("house", "East")]),
                        dict(kind="number", value=350, pre="DM ", suf=" bn+", label="federal spending in the East, first three years (Library of Congress)")]),
            dict(say="Alongside the treaty, Bonn set up a German Unity Fund of one hundred and fifteen billion D-Marks for the years to nineteen ninety four. Most of it was borrowed.",
                 shows=[dict(kind="sketch", art="document", opts=dict(title="German Unity Fund", lines=4, stamp="DM 115 bn"), label="May 1990", text="A fund for 1990 to 1994.", hl=["fund"], size=100),
                        dict(kind="sketch", art="seesaw", opts=dict(left="Borrowed", right="Saved", tip=1), label="DM 85 bn borrowed, DM 20 bn from savings", text="Mostly borrowed.", hl=["borrowed."], size=120)]),
            dict(say="If you work in mergers, this should sound familiar. In a share for share deal, the exchange ratio decides who gets what. Set it too generously, and the other side's owners pay for it.",
                 shows=[dict(kind="sketch", art="handshake", opts=dict(left="Buyer", right="Target"), label="Investment banking", text="It should sound familiar.", hl=["familiar."], size=110),
                        dict(kind="sketch", art="rateboard", opts=dict(rate="X : 1", sub="EXCHANGE RATIO"), label="Share for share", text="The ratio decides who gets what.", hl=["ratio"], size=96, flip=True),
                        dict(kind="sketch", art="scale", opts=dict(left="Buyer", right="Target", tip=-1), label="Too generous", text="The other owners pay.", hl=["pay."], size=110)]),
            dict(say="That's the lesson we take from it. An exchange rate is a price, and setting a price does not make the cost disappear. It only decides where the cost lands.",
                 shows=[dict(kind="sketch", art="bulb", opts=dict(text="A price"), label="The lesson", text="An exchange rate is a price.", hl=["price."], size=110),
                        dict(kind="verdict", text="The cost disappears.", stamp="MYTH", size=120),
                        dict(kind="sketch", art="dominoes", opts=dict(labels=["Rate", "Prices", "Jobs", "Taxes"], fall=4), label="It only moves", text="It decides where the cost lands.", hl=["lands."], size=96)]),
            dict(say="Poehl went on to help lay the groundwork for Europe's central bank. The same question came back with the euro: what happens when very different economies share one currency?",
                 shows=[dict(kind="sketch", art="bank", opts=dict(label="ECB"), label="What came next", text="Groundwork for Europe's central bank.", hl=["central", "bank."], size=92),
                        dict(kind="sketch", art="globe", label="The same question", text="Different economies, one currency?", hl=["one", "currency?"], size=100)]),
            dict(say="So here's a question for the comments. If you had set the rate in nineteen ninety, would you have picked one to one? This is history, not financial advice.",
                 shows=[dict(kind="sketch", art="rateboard", opts=dict(rate="? : 1", sub="YOUR CALL"), label="Your turn", text="One to one, or not?", hl=["not?"], size=120, flip=True),
                        dict(kind="icon", icon="pen", label="Tell us", text="Would you pick one to one?", hl=["one", "to", "one?"], size=100),
                        dict(kind="icon", icon="book", label="History, not advice", text="Not financial advice.", hl=["advice."], size=110)]),
        ]),
    ],
    description=(
        "On 9 November 1989 the Berlin Wall opened after a press conference went wrong. Eight months later West Germany had to "
        "answer a finance question no textbook covers: what is a whole country's money worth? The Bundesbank wanted 2 Ostmarks "
        "for 1 D-Mark, about 100,000 people protested in East Berlin, and the deal on 1 July 1990 converted wages at 1 to 1. "
        "We'll show you what that price did to East German industry, why 2 to 1 wasn't the easy fix it sounds like, and where the bill went. "
        "If you've ever priced a share-for-share merger, you'll recognise the problem. We think it's the best lesson in exchange rates there is.\n\n"
        "Sources: The World (PRX), \"How a mistake at a press conference helped topple the Berlin Wall\" (2020); "
        "Deutsche Bundesbank, \"No blueprint for reunification\"; Runde Ecke museum, Leipzig, March 1990; "
        "Konrad Adenauer Foundation, Geschichte der CDU, on the monetary, economic and social union; "
        "German History in Documents and Images: the 5 April 1990 protest and the 1 July 1990 Tagesschau report; "
        "DDR Museum Berlin, \"Monetary, economic and social union\"; Federal Reserve Bank of San Francisco, Economic Letter 90-26 (1990); "
        "Akerlof, Rose, Yellen and Hessenius, \"East Germany in from the Cold\", Brookings Papers on Economic Activity (1991); "
        "Library of Congress, Germany: A Country Study, \"Unification and Its Aftermath\"; obituary of Karl Otto Poehl (2014); Federal Reserve History, Janet L. Yellen."),
    tags=["Berlin Wall", "German reunification", "Deutsche Mark", "Ostmark", "exchange rate", "Bundesbank", "history of finance",
          "economics explained", "monetary union", "East Germany", "Treuhand", "finance history"],
)

if __name__ == "__main__":
    make(EP)
