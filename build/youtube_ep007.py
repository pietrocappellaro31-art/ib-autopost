"""
YouTube #7 (13 Nov 2026): the Panic of 1907. America had no central bank, so when a run on New York's trust
companies froze the money market, a 70-year-old private banker, J. P. Morgan, organised the rescue himself,
ending with the trust company presidents locked inside his library until they signed. Banking crisis, first film
made to docs/production/long-form-standard.md (visual plan: build/plans/ep007.md). Score: suspense.

Point of view: the common story makes Morgan the lone hero. The record shows a rescue by many hands (the Treasury,
the New York Clearing House, Rockefeller, other banks), run by one man who decided who would be saved, and whose
firm also gained from it. That is the real lesson of 1907: a lender of last resort is too important to depend on
the judgement and interests of one private person, which is the case the country then made for the Federal
Reserve. Educational, not advice.

Every claim, sourced (FRH, BOS and MOR are used in the plan):
  [FRH] Jon R. Moen and Ellis W. Tallman, "The Panic of 1907", Federal Reserve History (as of 4 Dec 2015): "the first
      worldwide financial crisis of the twentieth century"; turned a recession into a contraction second in severity
      only to the Great Depression; 16 Oct 1907 failed attempt by F. Augustus Heinze and Charles W. Morse to corner
      United Copper stock (traded on the curb); runs on associated banks; 20 Oct the New York Clearing House declared
      the Heinze-related member banks solvent after examination, forced out their management and offered loans;
      18 Oct news that Knickerbocker Trust's president Charles T. Barney was an associate of Morse sparked a run;
      21 Oct the Clearing House refused aid (resources for members; most New York trusts were not members) and the
      National Bank of Commerce stopped clearing for it; 22 Oct after depositors withdrew nearly $8 million the
      trust suspended; trusts were state chartered and competed with banks for deposits; cash reserves about 5% of
      deposits for trusts against 25% for national banks; trust deposits payable in cash on demand; Trust Company of
      America saw the most intense runs; call loan rate from 9.5% to 70% on 22 Oct and 100% two days later, at times
      no lenders at that rate; the NYSE stayed open largely because of Morgan, who had cash delivered to the
      exchange's loan post; Benjamin Strong examined Knickerbocker's books and could not reach a firm judgement in
      the time available; 26 Oct the Clearing House formed a committee to issue clearing house loan certificates and
      members restricted convertibility of deposits into cash, which created a cash premium and drew gold imports
      that helped the recovery; industrial output fell 17% in 1908, real GNP 12%; trusts lost over 36% of deposits
      between 22 Aug and 19 Dec 1907 while New York national bank deposits rose; the era preceded the Fed, the FDIC
      and the SEC.
  [BOS] Federal Reserve Bank of Boston, "The Panic of 1907" (pamphlet): Morgan about 70, no official position;
      United Copper rose past $62 a share on 14 Oct and closed at $15 two days later; the Knickerbocker run took
      about three hours and the trust closed shortly after noon on 22 Oct; Morgan's people audited the books and he
      chose not to bail it out; Trust Company of America aided; Treasury Secretary George Cortelyou announced shortly
      after 1 a.m. on 24 Oct that $25 million of government funds would be deposited in New York banks; Rockefeller
      pledged $10 million; on 24 Oct a $25 million pool organised by J. P. Morgan & Co. went to the Stock Exchange as
      call money, raised in about 15 minutes; an all-night session in the library produced a $25 million pool to
      rescue weaker trusts; the rescue of the broker Moore & Schley also let Morgan's bank arrange U.S. Steel's
      purchase of a competing company; 30 Oct a Morgan syndicate placed $30 million of New York City bonds; Aldrich's
      1910 central bank bill failed but parts went into the Federal Reserve Act, signed by Woodrow Wilson on 23 Dec
      1913; Morgan died on 31 Mar 1913; Aldrich: "We may not always have Pierpont Morgan with us to meet a banking
      crisis."
  [MOR] The Morgan Library & Museum, online guide, stop 23, "Panic of 1907": on Sunday 3 November, after two weeks of
      crisis, Morgan "summoned the trust company presidents to his library and quietly locked the front doors"; just
      after 4 a.m. each participant signed a pledge for the bailout; the panic led to the founding of the Federal
      Reserve System in 1913.
Our own: the drawings (stylised, no portraits), the illustrative scales, and the reading in the last chapter.
Calculations (checked in a script): $62 to $15 is a fall of about 76%; 25% against 5% is five times the cash per
dollar of deposits.

    python build/youtube_ep007.py
"""

from youtube import make

S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)

COPPER = dict(points=(("OCT 14", 62), ("OCT 16", 15)), unit="$", note="UNITED COPPER, A SHARE")

EP = dict(
    slug="yt-007-panic-of-1907",
    title="In 1907, America Had No Central Bank. So a Banker Locked the Doors.",
    score="suspense",
    thumb=dict(art=("library_lock", dict(still=True)),
               big_a="The night a banker <span style='color:#D93A12'>locked</span> Wall Street in", size_a=88,
               art_b=("rate_gauge", dict(still=True)),
               big="No central bank. <span style='color:#D93A12'>100%</span> interest.", size=96,
               small="The Panic of 1907", ghost="1907",
               looks=["split-red-paper", "paper-frame-ghost"]),
    chapters=[
        dict(title="A library at four in the morning", art=("library_lock", dict()), beats=[
            dict(say="It is just after four in the morning, on a Sunday in November nineteen oh seven. In a private library in New York, the front doors have been quietly locked.",
                 shows=[SC("library_lock", "New York, November 1907"),
                        S("clock", "The front doors are locked.", "Just after 4 a.m.", ["locked."], 110, flip=True, time="4:00")]),
            dict(say="Inside are the presidents of the city's trust companies. The man who locked them in is a seventy year old banker, John Pierpont Morgan.",
                 shows=[S("bankers_table", "The trust company presidents.", "Inside", ["presidents."], 96, pledge=False),
                        S("figures", "A banker, about seventy.", "J. P. Morgan", ["seventy."], 110, flip=True, n=1, hi=0)]),
            dict(say="He held no public office. But for three weeks, he had been doing the job a central bank would do.",
                 shows=[S("stamp", "No public office.", "", ["No"], 120, text="PRIVATE"),
                        dict(kind="split", left=("bank", "A central bank", "Lends in a panic"), right=("person", "One banker", "Did it instead"), mid="vs")]),
            dict(say="Because America, in nineteen oh seven, did not have one.",
                 shows=[S("bank", "America did not have one.", "1907", ["not"], 120, label="NO CENTRAL BANK")]),
            dict(say="This is the story of how a copper stock, a run on a trust company and an interest rate of one hundred percent led to that locked room. And why the country decided it never wanted to depend on one man again.",
                 shows=[dict(kind="timeline", title="Where we are going", items=[("Oct 14", "A copper stock"), ("Oct 22", "A run"), ("Nov 3", "The library"), ("1913", "The Fed")], hi=2),
                        S("seesaw", "Never again one man.", "", ["one", "man."], 100, flip=True, left="One man", right="A system", tip=1)]),
        ]),
        dict(title="A country with no lender of last resort", art=("bank", dict(label="1907")), beats=[
            dict(say="Start with what was missing. In nineteen oh seven there was no Federal Reserve, no deposit insurance, and no Securities and Exchange Commission.",
                 shows=[S("magnifier", "Start with what was missing.", "", ["missing."], 110, label="?"),
                        dict(kind="icons", title="Not yet invented in 1907", items=[("bank", "Federal Reserve"), ("lock", "Deposit insurance"), ("scales", "Securities regulator")], hi=0)]),
            dict(say="So when depositors panicked, nobody official could step in. There was no institution whose job was to lend to sound banks until the fear passed.",
                 shows=[S("queue", "Depositors panicked.", "", ["panicked."], 110, n=7, label="BANK"),
                        S("speech", "Nobody's job to lend.", "", ["Nobody's"], 100, flip=True, text="Who lends now?")]),
            dict(say="Economists call that a lender of last resort. The Federal Reserve's own history calls nineteen oh seven the first worldwide financial crisis of the twentieth century.",
                 shows=[dict(kind="term", term="Lender of last resort", text="An institution that lends to sound banks in a panic, so a run on cash does not sink them."),
                        S("globe", "The first worldwide crisis of the century.", "Federal Reserve History", ["worldwide"], 96, flip=True)]),
        ]),
        dict(title="A bank with thinner walls", art=("trust_vs_bank", dict()), beats=[
            dict(say="The weak point was a newer kind of institution, the trust company. Trusts were chartered by states, and they competed with banks for the same deposits.",
                 shows=[S("bank", "A newer kind of institution.", "The trust company", ["newer"], 110, label="TRUST CO."),
                        S("seesaw", "Competing for the same deposits.", "State chartered", ["same"], 100, flip=True, left="Banks", right="Trusts", tip=1)]),
            dict(say="But they kept far less cash. A national bank held cash reserves of about twenty five percent of its deposits. A trust company held about five.",
                 shows=[S("bulb", "They kept far less cash.", "", ["less"], 120, text="!"),
                        S("trust_vs_bank", "About 25% against about 5%.", "Cash reserves, share of deposits", ["5%."], 92, flip=True),
                        dict(kind="compare", left=("National bank, cash per $100 of deposits", "$25"), right=("Trust company", "$5"), note="Federal Reserve History: about 25% and about 5%")]),
            dict(say="So for every dollar of deposits, a national bank kept five times as much cash on hand.",
                 shows=[S("bars", "Five times the cash.", "Per dollar of deposits", ["Five"], 110, values=[25, 5], labels=["BANK 25%", "TRUST 5%"], hi=1)]),
            dict(say="And trust deposits could still be taken out in cash on demand. That meant a run could empty one fast. It meant a trust was every bit as exposed to a run as a bank, with a much thinner cushion.",
                 shows=[S("flow", "Cash on demand.", "", ["demand."], 120, steps=("Depositor", "Teller", "Cash")),
                        S("outflow", "A run could empty one fast.", "", ["fast."], 100, flip=True, label="CASH OUT"),
                        S("tower", "Every bit as exposed to a run.", "", ["run,"], 100, crack=True, label="TRUST"),
                        ]),
            dict(say="Take an example of our own. A trust with a hundred dollars of deposits keeps five in cash. If six of its hundred depositors want their dollar back on the same morning, it has already run out of cash, and has to sell something, fast.",
                 shows=[S("coins", "$100 of deposits, $5 in cash.", "Our example", ["$5"], 100, stacks=[1, 2, 2]),
                        S("queue", "Six depositors, one morning.", "Our example", ["Six"], 100, flip=True, n=6, label="TRUST"),
                        dict(kind="compare", left=("Cash on hand", "$5"), right=("Asked for", "$6"), note="Our illustration, not 1907 data")]),
            dict(say="Most of the big New York trusts were also outside the club that banks used to help each other, the New York Clearing House.",
                 shows=[S("handshake", "Outside the banks' club.", "The New York Clearing House", ["Outside"], 100, left="Banks", right="Clearing House")]),
        ]),
        dict(title="A copper stock breaks", art=("price_path", dict(COPPER)), beats=[
            dict(say="The spark came from a gamble. Two speculators, Augustus Heinze and Charles Morse, tried to corner the shares of a company called United Copper.",
                 shows=[S("document", "The spark was a gamble.", "October 1907", ["gamble."], 110, title="United Copper", lines=4, stamp="CORNER"),
                        S("figures", "Two speculators.", "Heinze and Morse", ["speculators."], 110, flip=True, n=2, hi=0)]),
            dict(say="To corner a stock is to buy up so much of it that anyone who has sold short has to buy from you, at your price.",
                 shows=[dict(kind="term", term="A corner", text="Buying so much of a stock that short sellers must buy it back from you, at your price.")]),
            dict(say="On October the fourteenth the shares rose past sixty two dollars. Two days later they closed at fifteen. The corner had failed.",
                 shows=[S("calendar", "October 14.", "Past $62", ["14."], 120, day="14", month="OCT", note="1907"),
                        S("price_path", "$62 to $15 in two days.", "United Copper", ["$15"], 100, flip=True, **COPPER),
                        S("stamp", "The corner failed.", "", ["failed."], 120, text="FAILED")]),
            dict(say="That is a fall of about three quarters in two days. And everyone knew the men behind it also controlled banks.",
                 shows=[dict(kind="number", value=76, suf="%", label="the fall from $62 to $15 (our arithmetic)"),
                        S("bank", "The same men controlled banks.", "", ["banks."], 110, flip=True, label="THEIR BANKS")]),
            dict(say="Depositors ran. The Clearing House examined those banks, declared them solvent, pushed Heinze and Morse out of their management, and offered loans. That fire was put out.",
                 shows=[S("queue", "Depositors ran.", "", ["ran."], 120, n=6, label="BANK"),
                        S("document", "Examined and declared solvent.", "The Clearing House", ["solvent,"], 96, flip=True, title="Examination", lines=4, stamp="SOLVENT"),
                        S("stamp", "That fire was put out.", "", ["out."], 120, text="CONTAINED")]),
        ]),
        dict(title="The run on the Knickerbocker", art=("queue", dict(n=8, label="KNICKERBOCKER")), beats=[
            dict(say="Then the fear jumped. News broke that the president of the Knickerbocker Trust was an associate of Morse.",
                 shows=[S("arrows", "The fear jumped.", "October 18", ["jumped."], 120, up="FEAR", down=""),
                        S("bank", "The Knickerbocker Trust.", "Linked to Morse", ["Knickerbocker"], 100, flip=True, label="KNICKERBOCKER")]),
            dict(say="On October the eighteenth, depositors started to pull their money out.",
                 shows=[S("queue", "Depositors pull their money.", "October 18", ["pull"], 110, n=8, label="KNICKERBOCKER")]),
            dict(say="The Knickerbocker asked the Clearing House for help. On the twenty first it was refused. The Clearing House kept its resources for its members, and the trust was not a member.",
                 shows=[S("speech", "It asked for help.", "", ["help."], 120, text="Help?"),
                        S("stamp", "Refused, October 21.", "", ["Refused,"], 110, flip=True, text="REFUSED"),
                        S("handshake", "Not a member.", "", ["member."], 110, left="Members", right="Trust")]),
            dict(say="Morgan's people looked at its books. A young banker named Benjamin Strong could not say in the time he had whether it was solvent, and Morgan decided not to save it.",
                 shows=[S("ledger", "They looked at its books.", "", ["books."], 100, names=("Loans  ?", "Deposits  ?", "Capital  ?", "Cash  ?"), hi=(2, 3)),
                        S("magnifier", "No firm answer in time.", "Benjamin Strong", ["time"], 100, flip=True, label="SOLVENT?")]),
            dict(say="On October the twenty second, in a few hours, depositors took out nearly eight million dollars. Shortly after noon, the Knickerbocker shut its doors. It was finished.",
                 shows=[S("outflow", "Nearly $8 million in a few hours.", "October 22", ["$8"], 100, label="$8M OUT"),
                        S("clock", "Shortly after noon.", "", ["noon,"], 110, flip=True, time="12:10"),
                        S("stamp", "The doors shut.", "", ["shut"], 120, text="CLOSED")]),
        ]),
        dict(title="Money at a hundred percent", art=("rate_gauge", dict()), beats=[
            dict(say="Now every trust looked suspect, and everyone wanted cash at once. The worst runs hit the Trust Company of America.",
                 shows=[S("figures", "Every trust looked suspect.", "", ["suspect,"], 110, n=7, hi=6, glass=True),
                        S("queue", "The Trust Company of America.", "The worst runs", ["America."], 100, flip=True, n=8, label="TRUST CO.")]),
            dict(say="Look at what happened to the price of money. Brokers borrowed overnight, on what was called call money.",
                 shows=[dict(kind="term", term="Call money", text="Loans to brokers that the lender can call back at any time, priced as a yearly rate.")]),
            dict(say="On October the twenty second its rate jumped from nine and a half percent to seventy. Two days later it hit one hundred percent, and at times nobody would lend at all.",
                 shows=[S("rate_gauge", "9.5%, then 70%, then 100%.", "Call money, a yearly rate", ["100%."], 92, flip=True),
                        S("stamp", "At times, nobody would lend.", "", ["nobody"], 110, text="NO LENDERS")]),
            dict(say="Without loans, brokers would have had to dump shares, and the stock exchange itself might have had to close.",
                 shows=[S("dominoes", "Brokers dump shares.", "", ["dump"], 110, labels=("LOANS", "BROKERS", "SHARES", "EXCHANGE"), fall=1)]),
        ]),
        dict(title="Three weeks of rescue", art=("coins", dict(stacks=[3, 6, 10])), beats=[
            dict(say="The rescue came from several directions. Shortly after one in the morning on October the twenty fourth, the Treasury Secretary, George Cortelyou, announced twenty five million dollars of government money would be deposited in New York banks.",
                 shows=[S("clock", "One in the morning.", "October 24", ["morning."], 110, time="1:00"),
                        dict(kind="flow", items=[("bank", "US Treasury"), ("coin", "$25 million"), ("bank", "New York banks")])]),
            dict(say="The same day, Morgan's firm organised a pool of twenty five million dollars and sent it to the stock exchange as call money. By one account it took him about fifteen minutes to raise it.",
                 shows=[S("coins", "A $25 million pool.", "For the stock exchange", ["$25"], 100, stacks=[4, 8, 12]),
                        S("clock", "About fifteen minutes.", "By one account", ["fifteen"], 110, flip=True, time="0:15")]),
            dict(say="John Rockefeller pledged ten million dollars of his own.",
                 shows=[dict(kind="number", value=10, pre="$", suf=" million", label="pledged by John D. Rockefeller (Boston Fed account)")]),
            dict(say="On October the twenty sixth, the Clearing House began issuing loan certificates, paper that banks could use to settle with each other instead of cash. Banks also limited how much cash depositors could take out.",
                 shows=[S("scrip", "Paper instead of cash.", "Clearing house loan certificates", ["instead"], 96, amount="$"),
                        S("stamp", "Cash withdrawals limited.", "", ["limited."], 110, flip=True, text="LIMITED")]),
            dict(say="Cash became so scarce that it traded at a premium. That premium drew gold into America from abroad, which helped end the squeeze.",
                 shows=[S("ship", "Gold drawn in from abroad.", "", ["Gold"], 110),
                        S("scale", "Cash at a premium.", "", ["premium."], 100, flip=True, left="Cash", right="Deposits", tip=0)]),
            dict(say="On October the thirtieth, the mayor of New York asked for help too, and a group led by Morgan agreed to place thirty million dollars of the city's bonds.",
                 shows=[S("document", "New York City asks for help.", "October 30", ["help"], 100, title="City bonds", lines=4, stamp="$30M")]),
        ]),
        dict(title="The locked doors", art=("bankers_table", dict()), beats=[
            dict(say="Two weeks in, the trusts were still under pressure. So on Sunday, November the third, Morgan summoned the trust company presidents to his library.",
                 shows=[S("calendar", "Sunday, November 3.", "1907", ["Sunday,"], 110, day="3", month="NOV", note="1907"),
                        S("library_lock", "Summoned to his library.", "", ["library."], 96, flip=True)]),
            dict(say="By the library's own account, he quietly locked the front doors.",
                 shows=[S("library_lock", "He quietly locked the doors.", "The Morgan Library & Museum", ["locked"], 96)]),
            dict(say="The deal on the table was simple: the stronger trusts would put up money to save the weaker ones. The Boston Fed's account puts that pool at twenty five million dollars.",
                 shows=[S("seesaw", "The strong save the weak.", "", ["weak"], 100, left="Strong", right="Weak", tip=0),
                        dict(kind="number", value=25, pre="$", suf=" million", label="the pool for the weaker trusts (Boston Fed account)")]),
            dict(say="Just after four in the morning, each of them signed a pledge for their share.",
                 shows=[S("bankers_table", "Each signed a pledge.", "Just after 4 a.m.", ["signed"], 96)]),
            dict(say="There was a second deal inside the rescue. Rescuing a troubled broker also let Morgan's bank arrange for United States Steel to buy a competitor.",
                 shows=[S("handshake", "A second deal.", "", ["second"], 110, left="US Steel", right="Rival"),
                        S("scale", "A rescue, and a deal.", "", ["deal."], 100, flip=True, left="Rescue", right="Deal", tip=1)]),
            dict(say="He saved the system. He also chose who was saved, and his own firm did business on the way.",
                 shows=[dict(kind="split", left=("check", "Saved", "The system"), right=("search", "Chose", "Who was saved"), mid="+")]),
        ]),
        dict(title="The bill", art=("bars", dict(values=[100, 83], labels=["1907", "1908"], hi=1)), beats=[
            dict(say="The panic ended, but the damage did not. Industrial output fell seventeen percent in nineteen oh eight, and real economic output twelve percent.",
                 shows=[S("bars", "Output fell 17% in 1908.", "Industrial output", ["17%"], 100, values=[100, 83], labels=["1907", "1908"], hi=1),
                        dict(kind="number", value=12, suf="%", label="fall in real GNP (Federal Reserve History)")]),
            dict(say="The Federal Reserve's history calls it a contraction second in severity only to the Great Depression.",
                 shows=[S("document", "Second only to the Great Depression.", "Federal Reserve History", ["Great"], 96, title="1907 to 1908", lines=4, stamp="SEVERE")]),
            dict(say="And the trusts never got their money back. Between August and December nineteen oh seven they lost more than a third of their deposits, while deposits at national banks rose.",
                 shows=[S("cake", "More than a third of their deposits.", "Trusts, Aug to Dec 1907", ["third"], 100, slices=3, hi=0),
                        S("arrows", "Bank deposits rose.", "", ["rose."], 110, flip=True, up="BANKS", down="TRUSTS")]),
        ]),
        dict(title="Never one man again", art=("bank", dict(label="FEDERAL RESERVE")), beats=[
            dict(say="Senator Nelson Aldrich put the lesson in a sentence. We may not always have Pierpont Morgan with us to meet a banking crisis.",
                 shows=[S("speech", "The lesson in one sentence.", "Senator Nelson Aldrich", ["sentence."], 110, text="Not always..."),
                        dict(kind="quote", text="We may not always have Pierpont Morgan with us to meet a banking crisis.", hl=["not", "always"],
                             who="Senator Nelson Aldrich", size=88)]),
            dict(say="His own central bank bill failed in nineteen ten. But parts of it went into the Federal Reserve Act, which President Woodrow Wilson signed on December the twenty third, nineteen thirteen.",
                 shows=[S("scroll", "His bill failed in 1910.", "", ["failed"], 110, title="A BILL", seal="1910"),
                        dict(kind="timeline", title="From the panic to the Fed", items=[("1907", "The panic"), ("1910", "Aldrich bill fails"), ("Mar 1913", "Morgan dies"), ("Dec 1913", "Fed Act signed")], hi=3)]),
            dict(say="Morgan did not see it. He had died that March.",
                 shows=[S("calendar", "He died that March.", "1913", ["March."], 110, day="31", month="MAR", note="1913")]),
        ]),
        dict(title="What to take from it", art=("seesaw", dict(left="One man", right="A system", tip=1)), beats=[
            dict(say="Here is our reading. The popular version makes Morgan the lone hero who saved Wall Street. The record shows a rescue with many hands: the Treasury, the Clearing House, Rockefeller, and the banks that paid in.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 130, text="1"),
                        dict(kind="verdict", text="One man saved Wall Street.", stamp="MYTH", size=104),
                        dict(kind="icons", title="Many hands", items=[("bank", "Treasury"), ("scales", "Clearing House"), ("coin", "Rockefeller"), ("people", "The banks")], hi=0)]),
            dict(say="What Morgan supplied was speed and authority, at a time when no public body had either. And that is exactly the problem.",
                 shows=[S("clock", "Speed and authority.", "", ["Speed"], 110, time="4:00"),
                        S("stamp", "Exactly the problem.", "", ["problem."], 110, flip=True, text="ONE MAN")]),
            dict(say="A lender of last resort decides who survives a panic. In nineteen oh seven that decision sat with one private banker, with his own business on the table. The Federal Reserve was built so it would sit with a public institution instead.",
                 shows=[S("seesaw", "Who survives a panic?", "", ["survives"], 100, left="Saved", right="Let go", tip=0),
                        S("figures", "One private banker.", "1907", ["private"], 110, flip=True, n=1, hi=0),
                        S("bank", "A public institution instead.", "1913", ["public"], 100, label="FEDERAL RESERVE")]),
            dict(say="If an interviewer asks why central banks exist, nineteen oh seven is a good answer. Trusts with thin cash reserves, a run nobody official could stop, money at a hundred percent, and a rescue that depended on one man. This is education, not financial advice.",
                 shows=[S("document", "Why do central banks exist?", "Interview prep", ["exist?"], 100, title="Q: why a central bank?", lines=4, stamp="1907"),
                        dict(kind="list", title="The 1907 answer", items=["Thin cash reserves", "A run nobody could stop", "Money at 100%", "One man's rescue"]),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. Should one private bank ever have that much power in a crisis, if it is the only one able to act? Tell us in the comments.",
                 shows=[S("magnifier", "Our question for you.", "", ["question"], 120, label="YOU?"),
                        S("library_lock", "That much power, in one room?", "Your turn", ["power,"], 92, flip=True),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "Just after 4 a.m. on Sunday 3 November 1907, the presidents of New York's trust companies were sitting in J. P. Morgan's library with the "
        "front doors locked, signing pledges to rescue each other. Why was a 70-year-old private banker doing a central bank's job? Because America didn't have one. "
        "We follow the Panic of 1907 from a failed corner of United Copper ($62 to $15 in two days) to the run on the Knickerbocker Trust, where depositors took "
        "nearly $8 million in a few hours. Trust companies held about 5% of deposits in cash, against about 25% at national banks, and call money hit 100%. "
        "Then the rescue: the Treasury's $25 million, Morgan's pools, Rockefeller's pledge, clearing house certificates, and the night in the library. "
        "Our take: it wasn't one hero, and the real lesson is why the country didn't want to depend on one man again. That's how we got the Federal Reserve in 1913. "
        "Should one private bank ever hold that much power in a crisis?"),
    sources=[
        ("Federal Reserve History, The Panic of 1907 (Jon R. Moen and Ellis W. Tallman)", "https://www.federalreservehistory.org/essays/panic-of-1907"),
        ("Federal Reserve Bank of Boston, The Panic of 1907 (pamphlet)", "https://www.bostonfed.org/about/pubs/panicof1.pdf"),
        ("The Morgan Library & Museum, online guide, Panic of 1907", "https://www.themorgan.org/exhibitions/online/guide/stop-23-panic-1907"),
    ],
    source_note="The drawings are our own stylised reconstructions, not portraits; the 76% fall and the five-times comparison are our arithmetic "
                "from the figures above; the reading in the last chapter is ours.",
    hashtags=["Panicof1907", "FinanceHistory", "FederalReserve"],
    tags=["Panic of 1907", "JP Morgan 1907", "J. P. Morgan library", "Knickerbocker Trust", "bank run", "trust companies",
          "why the Federal Reserve was created", "lender of last resort", "financial history", "banking crisis",
          "call money", "Nelson Aldrich", "Federal Reserve Act 1913", "investment banking interview"],
)

if __name__ == "__main__":
    make(EP)
