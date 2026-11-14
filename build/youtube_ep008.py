"""
YouTube #8 (14 Nov 2026): the night the gold window closed. On Sunday 15 August 1971 Richard Nixon told the country
he had directed the Treasury to "suspend temporarily" the convertibility of the dollar into gold. Fifty five years
later it is still suspended. Economic history and money, made to docs/production/long-form-standard.md (visual plan:
build/plans/ep008.md). Score: suspense. Eleven filmed beats from build/cine_1971.py (four new sets: a 1971 living
room, a gold vault, a dealing room, a lodge), badged RECONSTRUCTION or "our illustration".

Point of view: the popular story is that 1971 was the night Americans lost the right to swap their dollars for gold.
They had lost it in 1934; in 1971 only foreign governments and central banks could use the gold window. What changed
was the anchor: from a gold promise to other countries to the judgement of the Federal Reserve, and the 1970s showed
what a weak anchor costs. Our reading, labelled as ours. Educational, not advice.

Every claim, sourced:
  [FRH-71] Sandra Kollen Ghizoni, "Nixon Ends Convertibility of U.S. Dollars to Gold and Announces Wage/Price
      Controls", Federal Reserve History: 44 countries met at Bretton Woods, New Hampshire, in 1944; currencies fixed
      to the dollar and the dollar to gold at $35 an ounce; operational in 1958; the US held about three quarters of
      the world's official gold; by the 1960s more foreign-held dollars than US gold; the Exchange Stabilization Fund
      intervened from March 1961; the Fed's first swap line, with the Bank of France, in March 1962, nine central
      banks with lines totalling up to $900 million by end 1962; a London gold run pushed the price to $40 an ounce on
      20 Oct 1960; the London Gold Pool formed 1 Nov 1961 with eight central banks and collapsed in March 1968; the
      "Triffin dilemma"; Nixon and fifteen advisers at Camp David 13 to 15 Aug 1971, including Arthur Burns, John
      Connally and Paul Volcker; the address on the evening of 15 Aug; gold window closed, "in effect, the
      international monetary system turned into a fiat one"; a 90-day freeze on wages and prices, the first outside
      wartime; a 10 percent import surcharge; inflation practically halted during the freeze, then reappeared.
  [OH] Office of the Historian, US Department of State, "Nixon and the End of the Bretton Woods System, 1971-1973":
      the dollar at "the congressionally-set price of $35 per ounce"; Camp David on 13 Aug with Connally and Shultz;
      Secretary of State William Rogers and Henry Kissinger absent; the 15 Aug New Economic Policy; Smithsonian
      Agreement December 1971, Nixon called it "the most significant monetary agreement in the history of the world";
      February 1973 a further devaluation; March 1973 joint floating, the effective end of Bretton Woods.
  [APP] The American Presidency Project (UC Santa Barbara), Address to the Nation Outlining a New Economic Policy:
      "The Challenge of Peace", 15 Aug 1971, 9 p.m., Oval Office, live on radio and television. Verbatim: "I have
      directed Secretary Connally to suspend temporarily the convertibility of the dollar into gold"; "your dollar
      will be worth just as much tomorrow as it is today" (preceded by "if you are among the overwhelming majority of
      Americans who buy American-made products in America"); "a freeze on all prices and wages throughout the United
      States for a period of 90 days"; "an additional tax of 10 percent on goods imported into the United States".
  [FRH-SA] "The Smithsonian Agreement", Federal Reserve History: in December 1971 the US devalued the dollar against
      gold by approximately 8.5 percent to $38 an ounce; roughly a 10.7 percent average devaluation against the other
      key currencies; gold about $60 by mid 1972 and about $90 by early 1973 in the market; February 1973 a further
      10 percent devaluation to $42; within a month nearly all major currencies floating; collapsed within fifteen
      months of the meeting; US inflation from under 2% in early 1965 to 6% by end 1969.
  [IMF] IMF, "Money Matters" exhibit, System in Crisis (1959-1971): in 1966 foreign central banks and governments
      held over 14 billion US dollars; the US held $13.2 billion in gold, only $3.2 billion of it available to cover
      foreign dollar holdings (the rest for domestic holdings); converting even a quarter at once could not be honoured.
  [BOR] Michael D. Bordo, "The Imbalances of the Bretton Woods System 1965 to 1973: U.S. Inflation, the Elephant in
      the Room", NBER Working Paper 25409 (2018): Triffin posited that demand for dollars as reserves would eventually
      exceed the US monetary gold stock, "leading to the possibility of a run on Fort Knox"; by 1966 official dollar
      liabilities exceeded the gold stock; fears that the British would convert their dollar holdings into gold led
      to the 15 Aug 1971 announcement.
  [NYF] Charles A. Coombs, "Treasury and Federal Reserve Foreign Exchange Operations", FRBNY Monthly Review, October
      1971: "From January 1 through mid-August a total of $3.1 billion in such assets was paid out, including $864
      million of gold"; in the week after 6 Aug "$3.7 billion moved across the exchanges and into central bank hands".
  [FRH-GRA] "Gold Reserve Act of 1934", Federal Reserve History: signed 30 Jan 1934; title to monetary gold passed to
      the Treasury, currency at $35 an ounce; private possession regulated, coins banned; US citizens able to own and
      deal in gold freely since 1974, when President Ford signed an act of Congress.
  [FRH-GI] Michael Bryan, "The Great Inflation", Federal Reserve History: inflation above 14 percent in 1980; Volcker
      took office in August 1979; by the end of the 1981-82 recession inflation back under 5 percent.
Our own: the drawings and filmed reconstructions (no portraits; nobody on screen speaks), the $35 million example,
and the reading in the last two chapters. Calculations (build/plans/ep008_checks.py): $35,000,000 / $35 = 1,000,000
ounces; a quarter of $14bn is $3.5bn, more than the $3.2bn available; $35 to $38 is +8.6% on the gold price (the
dollar's gold value down 7.9%, "about 8.5 percent" in FRH's words); 1971 to 2026 is 55 years.

    python build/youtube_ep008.py
"""

import cine_1971 as F
from youtube import make

S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)
CINE = lambda name: dict(kind="cine", shot=F.SHOTS[name])

GOLD_PATH = dict(points=(("1971", 35), ("DEC 71", 38), ("MID 72", 60), ("EARLY 73", 90)), unit="$", note="GOLD, $ AN OUNCE (MARKET APPROX.)", counter=False)

EP = dict(
    slug="yt-008-gold-window",
    title="In 1971 the Dollar Stopped Being Gold. Most Americans Couldn't Swap It Anyway.",
    score="suspense",
    thumb=dict(film_a=dict(shot=F.SHOTS["vault_window"], dur=9.0, t=7.6, pos="40% 70%",
                           segs=[("The key was the gold window.", .3, 2.6), ("A central bank could hand over dollars and ask for gold.", 2.8, 8.6)]),
               film_b=dict(shot=F.SHOTS["speech"], dur=12.0, t=11.6, pos="38% 50%",
                           segs=[("He spoke.", .3, 2.0), ("First, the gold window.", 2.2, 4.4), ("Second, a freeze.", 4.6, 7.0), ("Third, a tax.", 7.2, 9.8)]),
               big_a="The night the dollar stopped being <span style='color:#F2C35B'>gold</span>", size_a=84,
               big="Closed <span style='color:#0A0A0A'>“temporarily”</span>. In 1971.", size=80,
               small="The gold window, 1971", looks=["ink-gold-left", "red-art-right"]),
    chapters=[
        dict(title="Nine o'clock, Sunday night", art=("clock", dict(time="9:00")), beats=[
            dict(say="On a Sunday evening in August nineteen seventy one, at nine o'clock, Americans watching television saw their President, Richard Nixon. He said he had directed his Treasury Secretary to suspend, temporarily, the convertibility of the dollar into gold.",
                 show=CINE("tv_hook")),
            dict(say="Temporarily. That was fifty five years ago, and the window he closed has never reopened.",
                 shows=[S("calendar", "Temporarily.", "Since 1971", ["Temporarily."], 130, day="15", month="AUG", note="1971"),
                        dict(kind="number", value=55, suf=" years", label="since the gold window closed, and it is still shut")]),
            dict(say="So why didn't the dollar simply collapse? And what did that one sentence actually change? The answer starts with a surprise. Most Americans could not swap their dollars for gold that night anyway.",
                 shows=[S("magnifier", "Why didn't it collapse?", "", ["collapse?"], 110, label="$"),
                        S("speech", "What did one sentence change?", "", ["change?"], 100, flip=True, text="Temporarily..."),
                        S("bulb", "A surprise.", "", ["surprise."], 120, text="!"),
                        S("stamp", "Most Americans could not swap anyway.", "", ["could", "not"], 96, flip=True, text="NOT YOU")]),
        ]),
        dict(title="The promise of Bretton Woods", art=("globe", dict()), beats=[
            dict(say="Go back to nineteen forty four. Delegates from forty four countries met in Bretton Woods, New Hampshire, to design the money system for the world after the war.",
                 shows=[S("globe", "Forty four countries.", "Bretton Woods, 1944", ["Forty", "four"], 110),
                        S("handshake", "A money system for after the war.", "", ["after"], 100, flip=True, left="44 nations", right="One system")]),
            dict(say="The design was a chain. Other currencies were fixed to the dollar. And the dollar was fixed to gold, at thirty five dollars an ounce.",
                 shows=[dict(kind="flow", items=[("coin", "Other currencies"), ("bank", "The US dollar"), ("coin", "Gold at $35 an ounce")]),
                        S("notes", "Other currencies, fixed to the dollar.", "", ["fixed"], 96, flip=True, left="X", right="$", lab_l="Other currency", lab_r="Dollar"),
                        S("pricetag", "Thirty five dollars an ounce.", "Set by Congress", ["thirty", "five"], 110, value="$35", tag="1 OZ")]),
            dict(say="It seemed safe, because the United States held about three quarters of the world's official gold.",
                 shows=[S("cake", "About three quarters of the world's gold.", "Official reserves", ["three", "quarters"], 100, slices=4, hi=0)]),
            dict(say="The system only became fully operational in nineteen fifty eight. Within a few years, it was in trouble.",
                 shows=[dict(kind="timeline", title="A short life", items=[("1944", "Designed"), ("1958", "Fully working"), ("1960s", "Strain"), ("1971", "Window shut")], hi=1)]),
        ]),
        dict(title="How the gold window worked", art=("scale", dict(left="$35", right="1 oz", tip=0)), beats=[
            dict(say="The key was what officials called the gold window. A foreign central bank holding dollars could hand them to the United States Treasury and ask for gold, at the fixed price.",
                 show=CINE("vault_window")),
            dict(say="Take an example of our own. A central bank brings thirty five million dollars to the window. At thirty five dollars an ounce, it leaves with one million ounces of gold.",
                 show=CINE("vault_count")),
            dict(say="That promise is what made the other pegs believable. If the dollar was as good as gold, a currency fixed to the dollar was anchored too.",
                 shows=[S("tower", "As good as gold.", "", ["gold."], 110, floors=6, label="$"),
                        S("seesaw", "Every peg leaned on one promise.", "", ["promise."], 100, flip=True, left="Other pegs", right="$35 gold", tip=1)]),
            dict(say="But notice who stood at that window. Central banks and governments. Not you.",
                 shows=[S("figures", "Central banks and governments.", "", ["governments."], 110, n=4, hi=0),
                        dict(kind="split", left=("bank", "At the window", "Foreign central banks"), right=("person", "Not at it", "Ordinary people"), mid="vs"),
                        S("stamp", "Not you.", "", ["Not", "you."], 130, text="NOT YOU")]),
        ]),
        dict(title="More dollars than gold", art=("bars", dict(values=[14, 13.2], labels=["DOLLARS ABROAD", "US GOLD"], hi=0)), beats=[
            dict(say="The trouble was arithmetic. The world economy was growing, and other countries wanted more dollars to hold as reserves.",
                 shows=[S("chart", "The world wanted more dollars.", "Our sketch, no data", ["more"], 100, values=(2, 3, 4, 5, 6, 7, 8), color="#0F766E", arrow=True),
                        S("ship", "Trade grew.", "", ["grew."], 110, flip=True)]),
            dict(say="The economist Robert Triffin pointed out the catch. If the demand for dollars kept growing, the dollars held abroad would one day exceed America's gold, and a run on Fort Knox would become possible.",
                 shows=[S("bulb", "Robert Triffin's catch.", "", ["catch."], 110, text="!"),
                        dict(kind="quote", text="...leading to the possibility of a run on Fort Knox.", hl=["run", "Fort", "Knox."],
                             who="Michael Bordo, summarising Triffin (NBER, 2018)", size=80)]),
            dict(say="It became known as the Triffin dilemma. Supply the world with dollars, and you weaken the gold promise. Stop supplying them, and the world runs short of reserves.",
                 shows=[dict(kind="term", term="The Triffin dilemma", text="The reserve currency must supply the world with dollars, and every extra dollar abroad weakens its gold promise."),
                        S("scale", "Supply dollars, and weaken the promise.", "", ["weaken"], 100, flip=True, left="Dollars", right="Gold", tip=0),
                        S("empty_pockets", "Or the world runs short.", "", ["short."], 100, label="RESERVES")]),
            dict(say="By nineteen sixty six, the IMF says, foreign central banks and governments held over fourteen billion dollars. America held thirteen point two billion dollars of gold, and only three point two billion of it was available to cover those foreign dollars. The rest was needed to back dollars at home. So if foreign holders had tried to convert even a quarter of their dollars at once, the United States could not have paid.",
                 show=CINE("vault_gap")),
        ]),
        dict(title="Cracks in the price", art=("price_path", dict(points=(("OFFICIAL", 35), ("OCT 1960", 40)), unit="$", note="GOLD IN LONDON", counter=False)), beats=[
            dict(say="Markets noticed early. On October the twentieth, nineteen sixty, a rush to buy gold in London pushed its price to forty dollars an ounce, against the official thirty five.",
                 show=CINE("london_1960")),
            dict(say="Officials pushed back. The Treasury began intervening in currency markets in nineteen sixty one. And the Federal Reserve set up its first swap line, with the Bank of France, in March nineteen sixty two.",
                 shows=[S("seesaw", "Officials pushed back.", "", ["back."], 110, left="Market", right="Officials", tip=1),
                        S("notes", "The Treasury stepped into currency markets.", "From March 1961", ["Treasury"], 96, flip=True, left="$", right="FX", lab_l="Dollars", lab_r="Other currencies"),
                        S("handshake", "The Fed's first swap line.", "Nine central banks, up to $900m, by end 1962", ["swap"], 100, left="The Fed", right="Bank of France")]),
            dict(say="Eight central banks formed the London Gold Pool, selling gold together to hold the market price down. It began in nineteen sixty one and collapsed in March nineteen sixty eight.",
                 shows=[S("coins", "Eight central banks, selling together.", "The London Gold Pool", ["Eight"], 100, stacks=[2, 3, 4, 5, 4, 3, 2, 1]),
                        S("stamp", "Collapsed, March 1968.", "", ["Collapsed,"], 110, flip=True, text="COLLAPSED")]),
            dict(say="Then inflation made it worse. American inflation rose from under two percent in early nineteen sixty five to six percent by the end of nineteen sixty nine.",
                 shows=[S("bars", "Under 2% to 6%.", "US inflation, 1965 to 1969", ["6%."], 100, values=[2, 6], labels=["EARLY 1965: <2%", "END 1969: 6%"], hi=1)]),
            dict(say="In plain terms, a dollar was buying less of almost everything else, while its official price in gold had not moved at all.",
                 shows=[S("scale", "Less of everything, except gold on paper.", "Gold still $35 an ounce", ["except"], 96, left="Everything", right="Gold $35", tip=0)]),
        ]),
        dict(title="The run on the dollar", art=("outflow", dict(label="DOLLARS OUT")), beats=[
            dict(say="By the summer of nineteen seventy one, money was leaving the dollar. From January to mid August, the New York Fed reported, the United States paid out three point one billion dollars of reserve assets, including eight hundred and sixty four million dollars of gold.",
                 shows=[S("outflow", "Money was leaving the dollar.", "1971", ["leaving"], 100, label="RESERVES OUT"),
                        dict(kind="compare", left=("Reserve assets paid out, Jan to mid Aug 1971", "$3.1bn"), right=("of which gold", "$864m"), note="Federal Reserve Bank of New York, Monthly Review, Oct 1971")]),
            dict(say="Then it became a flood. In the week after August the sixth, three point seven billion dollars moved across the exchanges and into the hands of central banks.",
                 show=CINE("flood_1971")),
            dict(say="Those central banks could, in principle, bring their dollars to the gold window. The economist Michael Bordo writes that fears Britain would convert its dollars into gold led to the decision that followed.",
                 shows=[S("queue", "Dollars heading for the window.", "", ["window."], 100, n=6, label="GOLD"),
                        S("speech", "Fears about Britain.", "Bordo, NBER 2018", ["Britain."], 100, flip=True, text="Gold, please?")]),
        ]),
        dict(title="A weekend at Camp David", art=("bankers_table", dict()), beats=[
            dict(say="On Friday, August the thirteenth, Nixon took about fifteen advisers to Camp David, the presidential retreat. Among them were the Federal Reserve chairman Arthur Burns, the Treasury Secretary John Connally, and a Treasury official named Paul Volcker.",
                 show=CINE("camp_arrive")),
            dict(say="The Secretary of State was not there, and neither was Henry Kissinger. This was treated as an economic decision, even though it would reshape the world's money.",
                 shows=[S("figures", "Who was not in the room.", "", ["not"], 110, n=2, hi=1, glass=True),
                        S("globe", "An economic decision, a world problem.", "", ["world"], 100, flip=True)]),
            dict(say="In three days they put together a package with three main parts: one about gold, one about prices and wages, and one about imports.",
                 show=CINE("camp_plan")),
        ]),
        dict(title="The speech", art=("calendar", dict(day="15", month="AUG", note="1971")), beats=[
            dict(say="On the evening of Sunday, August the fifteenth, Nixon spoke from the Oval Office, live on radio and television. First, the gold window. Foreign central banks could no longer swap their dollars for gold. Second, a freeze on all prices and wages across the United States, for ninety days. Third, an extra tax of ten percent on imports.",
                 show=CINE("speech")),
            dict(say="The Federal Reserve's history calls the freeze the first wage and price control outside wartime.",
                 shows=[S("pricetag", "The first peacetime freeze.", "Federal Reserve History", ["peacetime"], 100, value="FROZEN", tag="90 DAYS")]),
            dict(say="And he made a promise to viewers. In his words: if you are among the overwhelming majority of Americans who buy American made products in America, your dollar will be worth just as much tomorrow as it is today.",
                 shows=[S("podium", "A promise to viewers.", "", ["promise"], 110, words="Tomorrow"),
                        dict(kind="quote", text="...your dollar will be worth just as much tomorrow as it is today.", hl=["just", "as", "much"],
                             who="Richard Nixon, 15 August 1971 (American Presidency Project)", size=84)]),
            dict(say="Notice the condition inside that sentence. American made products, in America. Imports now carried an extra ten percent tax, so they were about to cost more.",
                 shows=[S("magnifier", "Notice the condition.", "", ["condition."], 110, label="IF..."),
                        S("factory", "American made, in America.", "", ["American"], 100, flip=True, label="MADE IN USA"),
                        S("pricetag", "Imports: plus ten percent tax.", "", ["Imports:"], 100, flip=True, value="+10%", tag="IMPORT")]),
        ]),
        dict(title="Temporarily", art=("price_path", dict(GOLD_PATH)), beats=[
            dict(say="What followed was not a return to normal. In December nineteen seventy one, the Smithsonian agreement tried to rebuild fixed rates around a cheaper dollar. The official gold price went from thirty five to thirty eight dollars an ounce.",
                 shows=[S("rateboard", "Not a return to normal.", "", ["normal."], 110, rate="$35?", sub="GOLD, AN OUNCE"),
                        S("document", "The Smithsonian agreement.", "December 1971", ["Smithsonian"], 100, title="New parities", lines=4, stamp="$38"),
                        S("pricetag", "From $35 to $38 an ounce.", "Official price", ["$38"], 110, flip=True, value="$38", tag="1 OZ")]),
            dict(say="Nixon called it the most significant monetary agreement in the history of the world.",
                 shows=[dict(kind="quote", text="the most significant monetary agreement in the history of the world", hl=["most", "significant"],
                             who="Richard Nixon on the Smithsonian Agreement (Office of the Historian)", size=84)]),
            dict(say="The market disagreed. Gold traded at about sixty dollars an ounce by the middle of nineteen seventy two, and about ninety by early nineteen seventy three.",
                 show=CINE("market_1972")),
            dict(say="In February nineteen seventy three the dollar was devalued again, by another ten percent, to about forty two dollars an ounce. Within a month, nearly all the major currencies were floating against the dollar. The system built to last had come apart about fifteen months after the Smithsonian meeting.",
                 shows=[S("price_path", "Devalued again: about $42.", "February 1973", ["$42."], 96, **GOLD_PATH),
                        S("ship", "Currencies floating.", "March 1973", ["floating."], 110, flip=True),
                        S("dominoes", "Fifteen months later, it fell apart.", "", ["apart."], 100, labels=("1944", "1958", "1971", "1973"), fall=3)]),
        ]),
        dict(title="The part most people get wrong", art=("scroll", dict(title="GOLD RESERVE ACT", seal="1934")), beats=[
            dict(say="Now the surprise from the start. Many people picture August nineteen seventy one as the night Americans lost the right to swap a dollar bill for gold.",
                 shows=[dict(kind="verdict", text="1971: the night Americans lost their gold.", stamp="MYTH", size=96)]),
            dict(say="They had lost it decades earlier. Under the Gold Reserve Act, signed in January nineteen thirty four, monetary gold passed to the Treasury, and private holdings were tightly restricted.",
                 shows=[S("scroll", "Gold Reserve Act, 1934.", "Signed January 30, 1934", ["1934."], 100, title="GOLD RESERVE ACT", seal="1934"),
                        S("bank", "Monetary gold passed to the Treasury.", "", ["Treasury."], 100, flip=True, label="US TREASURY")]),
            dict(say="Americans could not freely own and trade gold again until a law signed by President Ford in nineteen seventy four.",
                 shows=[dict(kind="timeline", title="Who could swap dollars for gold?", items=[("1934", "Not Americans"), ("1944", "Foreign officials"), ("1971", "Nobody"), ("1974", "Americans may own gold")], hi=2)]),
            dict(say="So in nineteen seventy one, the gold window was a privilege of foreign governments. Closing it did not change the cash in an American's wallet that night. It changed what anchored the dollar.",
                 show=CINE("wallet")),
            dict(say="Before, the anchor was a gold promise to other countries. After, it was the judgement of the Federal Reserve. And the first years went badly. Inflation rose above fourteen percent in nineteen eighty.",
                 shows=[S("coins", "Before: a gold promise abroad.", "Before 1971", ["Before:"], 100, stacks=[2, 4, 6]),
                        S("bank", "After: the Federal Reserve's judgement.", "After 1971", ["After:"], 96, flip=True, label="FEDERAL RESERVE"),
                        S("stamp", "The first years went badly.", "", ["badly."], 110, text="1970s"),
                        S("bars", "Above 14% in 1980.", "US inflation", ["14%"], 100, values=[6, 14], labels=["END 1969: 6%", "1980: >14%"], hi=1)]),
            dict(say="It took Paul Volcker, the same man who had been at Camp David, now the Federal Reserve chairman, and a deep recession in the early nineteen eighties, to bring inflation back under five percent.",
                 shows=[S("bars", "Back under 5%.", "Paul Volcker, Fed chairman from 1979", ["under"], 100, values=[14, 5], labels=["1980: >14%", "1982: <5%"], hi=1)]),
        ]),
        dict(title="What backs a dollar now", art=("seesaw", dict(left="Gold", right="Trust", tip=1)), beats=[
            dict(say="Here is our reading. The dollar did not collapse in nineteen seventy one because gold was never what made it useful day to day. Americans paid wages, rents, taxes and debts in dollars, and they kept doing so.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 130, text="1"),
                        S("bank", "Gold was never what made it useful.", "Our reading", ["useful."], 96, flip=True, label="$"),
                        dict(kind="icons", title="What kept dollars useful", items=[("coin", "Wages"), ("house", "Rent"), ("bank", "Taxes"), ("book", "Debts")], hi=2)]),
            dict(say="What gold had added was a brake. It limited how many dollars could be promised against it, at least on paper. Without it, the brake has to come from the central bank, and the nineteen seventies showed what happens when it slips.",
                 shows=[S("bricks", "Gold was a brake.", "Our reading", ["brake."], 100, label="GOLD"),
                        S("ladder_wallet", "A limit on promises, on paper.", "", ["limit"], 100, flip=True, tag="$35"),
                        S("tower", "When the brake slips.", "The 1970s", ["slips."], 100, flip=True, crack=True, label="$")]),
            dict(say="So a dollar today rests on an institution's credibility, not on gold in a vault. Credibility can be lost, as the nineteen seventies showed. But a central bank can also lend in a panic without first checking how much gold it has.",
                 shows=[S("scale", "Credibility, not metal.", "", ["Credibility,"], 100, left="Metal", right="Credibility", tip=1),
                        S("chart", "Credibility can be lost.", "Our sketch, no data", ["lost,"], 100, flip=True, values=(2, 3, 5, 7, 9, 8, 5), color="#D93A12", arrow=False),
                        S("bank", "It can lend in a panic.", "", ["panic."], 100, flip=True, label="CENTRAL BANK")]),
            dict(say="If an interviewer asks what fiat money is, nineteen seventy one is a good answer. A fixed price for gold, more dollars abroad than gold to pay them, a run, a closed window, and an anchor that moved to the central bank. This is education, not financial advice.",
                 shows=[S("document", "What is fiat money?", "Interview prep", ["fiat"], 100, title="Q: what is fiat money?", lines=4, stamp="1971"),
                        dict(kind="list", title="The 1971 answer", items=["Gold fixed at $35", "More dollars than gold", "A run in August", "The window closed", "The anchor: the central bank"]),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. Would you trust a currency more if you could swap it for gold, even if, like most Americans in nineteen seventy one, you never actually could? Tell us in the comments.",
                 shows=[S("magnifier", "Our question for you.", "", ["question"], 120, label="YOU?"),
                        S("pricetag", "Would gold make you trust it more?", "Your turn", ["trust"], 92, flip=True, value="$1", tag="GOLD?"),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "Sunday 15 August 1971, 9 p.m.: Richard Nixon tells the country he's directed the Treasury to \"suspend temporarily\" the convertibility "
        "of the dollar into gold. Fifty five years on, the gold window's still shut. So why didn't the dollar collapse?\n\n"
        "We go back to Bretton Woods in 1944, where the dollar was fixed at $35 an ounce and everyone else's currency was fixed to the dollar. "
        "You'll see the Triffin dilemma, the IMF's 1966 numbers (over $14 billion held abroad against $13.2 billion of gold, and only $3.2 billion "
        "of that available), gold hitting $40 in London in 1960, the run of August 1971 ($3.7 billion into central banks in a single week), the "
        "weekend at Camp David, the speech, and how the Smithsonian agreement fell apart.\n\n"
        "Then the bit most people get wrong. Ordinary Americans hadn't been able to swap dollars for gold since 1934. What 1971 changed was the "
        "anchor, and that's the part we think matters. Would you trust a currency more if you could swap it for gold? Tell us below."),
    sources=[
        ("Federal Reserve History, Nixon Ends Convertibility of U.S. Dollars to Gold and Announces Wage/Price Controls", "https://www.federalreservehistory.org/essays/gold_convertibility_ends"),
        ("Office of the Historian, US Department of State, Nixon and the End of the Bretton Woods System, 1971-1973", "https://history.state.gov/milestones/1969-1976/nixon-shock"),
        ("The American Presidency Project, Address to the Nation Outlining a New Economic Policy: The Challenge of Peace (15 Aug 1971)", "https://www.presidency.ucsb.edu/documents/address-the-nation-outlining-new-economic-policy-the-challenge-peace"),
        ("Federal Reserve History, The Smithsonian Agreement", "https://www.federalreservehistory.org/essays/smithsonian-agreement"),
        ("IMF, Money Matters exhibit, System in Crisis (1959-1971)", "https://www.imf.org/external/np/exr/center/mm/eng/sc_sub_3.htm"),
        ("Michael D. Bordo, The Imbalances of the Bretton Woods System 1965 to 1973, NBER Working Paper 25409", "https://www.nber.org/papers/w25409.pdf"),
        ("Charles A. Coombs, Treasury and Federal Reserve Foreign Exchange Operations, FRBNY Monthly Review, October 1971 (FRASER)", "https://fraser.stlouisfed.org/files/docs/publications/frbnyreview/rev_frbny_197110.pdf"),
        ("Federal Reserve History, Gold Reserve Act of 1934", "https://www.federalreservehistory.org/essays/gold-reserve-act"),
        ("Federal Reserve History, The Great Inflation (Michael Bryan)", "https://www.federalreservehistory.org/essays/great-inflation"),
    ],
    source_note="We drew the filmed scenes ourselves. They're stylised reconstructions, not portraits, and nobody in them speaks. The $35 "
                "million example is ours, the 1972 and 1973 market gold prices are approximate, and the reading in the last two chapters is "
                "ours, so you're welcome to disagree with it.",
    hashtags=["Nixon1971", "FinanceHistory", "GoldStandard"],
    tags=["Nixon shock", "gold window 1971", "end of the gold standard", "Bretton Woods", "why the dollar is not backed by gold", "fiat money",
          "Triffin dilemma", "Smithsonian Agreement", "Camp David 1971", "Paul Volcker", "Gold Reserve Act 1934", "economic history",
          "financial history", "investment banking interview"],
)

if __name__ == "__main__":
    make(EP)
