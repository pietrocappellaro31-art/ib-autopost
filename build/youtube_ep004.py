"""
YouTube #4 (11 Nov 2026, Armistice Day): who actually paid for the First World War. The headline
version is that Britain "finally paid off" its war debt in 2015 and Germany paid the last of its
reparations in 2010. Our reading: almost none of that debt was ever paid off in the way a household
pays off a loan. It was hidden, rolled over, cut, cancelled, defaulted on or inflated away, and the
people who paid most were the patriotic savers who lent the money. History of finance, with one
technical idea for interviews (a perpetual bond's price is its coupon divided by the yield).

Point of view: governments almost never repay war debt; they refinance it and let inflation shrink
it. A fixed sum lent for a long time is a bet against inflation. Educational, not advice.

Every claim, sourced:
  [1] World History Encyclopedia, "The 1918 Armistice with Germany": fighting stopped at 11am on
      11 November 1918.
  [2] GOV.UK, "Chancellor to repay the nation's First World War debt", 3 Dec 2014: Treasury to redeem
      the outstanding GBP 1.9 billion (1,938.6m nominal) of 3.5% War Loan on 9 March 2015; 3.5% War
      Loan created in 1932 in a conversion led by Chancellor Neville Chamberlain, exchanged for 5% War
      Loan 1929-47, issued in 1917 to fund the war; DMO estimate of about GBP 5.5 billion of interest
      paid on the two since 1917; more than 120,000 holders, 97,000 holding less than GBP 1,000 and
      almost 38,000 less than GBP 100; 4% Consols (GBP 218.4m) also redeemed, the first planned
      repayment of an undated gilt of this kind for 67 years; Osborne: "We can, at last, pay off the
      debts Britain incurred to fight the First World War."
  [3] Bank Underground (Bank of England staff blog), Anson, Cohen, Owens and Todman, "Your country
      needs funds", 8 Aug 2017: the 1914 War Loan had a GBP 350m target; only GBP 91.1m was bought;
      the shortfall was secretly plugged by the Bank; advances to the Chief Cashier Gordon Nairn and
      his deputy Ernest Harvey, who bought in their own names; booked as "Other Securities"; FT,
      23 Nov 1914: over-subscribed by GBP 250,000,000, "And still the applications are pouring in";
      Keynes, 1915 memo: "masterly manipulation"; a return of 4.1% against 2.5% on other government
      debt; 97,635 investors; the 1917 War Loan raised GBP 2bn offering 5.4%.
  [4] Queen Mary University of London news, 8 Aug 2017: raised less than a third of the target;
      Nairn later swore a statement that all GBP 350m had been sold to the public; Norma Cohen: "The
      fund raising effort was such a failure that the establishment felt compelled to cover it up."
  [5] Western Front Association, "The First World War paid off?": the Third War Loan, offered
      mid-January to mid-February 1917; about GBP 960m of new money from just over two million
      subscribers; the 2015 repayment "simply merged debt which had no maturity date into other
      government borrowing".
  [6] MoneyWeek, "Why Britain is repaying its war debt" (2014): 1917 slogan "if you cannot fight,
      invest all you can in 5% bonds. Unlike the soldier, the investor runs no risk."; the 1932 cut
      from 5% to 3.5%; in 1927 Chancellor Churchill rolled maturing war bonds into a 4% undated
      Consolidated loan; the same refinancing took in an 1853 Gladstone bond that consolidated, among
      other things, the capital stock of the South Sea Company; in real terms GBP 100 lent in 1927 is
      bought back for the equivalent of GBP 1.82; War Loan at GBP 91.70, a yield of 3.8%.
  [7] History.com, "Germany Finally Pays Off World War I Debt": 132 billion gold marks at Versailles;
      Dawes Plan 1924; Young Plan cut it to 121 billion; Hitler cancelled payments in 1933; London
      1953 cancelled half and stretched the rest; part of the back interest due only once Germany
      reunified; last payment 3 October 2010.
  [8] RNZ, "Germany finally pays off its World War I debt", 3 Oct 2010: a final payment of around
      US$96 million.
  [9] Wikipedia, "The Economic Consequences of the Peace": Keynes, Treasury delegate at Paris,
      resigned 26 May 1919; urged reparations be limited to GBP 2,000 million; "Carthaginian peace";
      about 100,000 copies in six months.
  [10] Economic History Society, David James Gill, "The UK's unpaid war debts to the United States,
      1917-1980": Britain stopped paying in 1934, after the Johnson Act; unpaid debts exceeding
      $4 billion; it later stood in the way of a return to the New York bond market in the late 1970s.
Our own arithmetic, labelled on screen: 3.5 / 3.8% = about GBP 92, beside the GBP 91.70 quoted.
The poster, newspaper, ledger and certificate are our own drawings, not copies of real ones.

    python build/youtube_ep004.py
"""

from youtube import make

# S(drawing, line, label, highlighted words, size, flip, **drawing options); SC(drawing, heading, **drawing options)
S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)

EP = dict(
    slug="yt-004-who-paid-for-ww1",
    title="Britain Paid Off World War One in 2015. So Who Really Paid?",
    thumb=dict(art=("shrink", dict(label="£100", last="£1.82")),
               big_a="Lent £100.<br>Repaid, worth<br><span style='color:#0A0A0A'>£1.82.</span>", size_a=90,
               art_b=("perpetual", dict()),
               big="The war debt that was <span style='color:#D93A12'>never</span> paid off.",
               small="Who really paid for World War One", ghost="1918", size=100),
    chapters=[
        dict(title="The war that ended twice", art=("clock", dict(time="11:00")), beats=[
            dict(say="At eleven in the morning on the eleventh of November, nineteen eighteen, the guns stopped. That is why today is Armistice Day.",
                 shows=[S("clock", "11am, 11 November 1918.", "The Armistice", ["11am,"], 110, time="11:00"),
                        S("calendar", "Armistice Day.", "Today", ["Armistice"], 120, flip=True, day="11", month="NOV", note="1918")]),
            dict(say="But the bills kept running. Germany made its last payment on the war in October twenty ten.",
                 shows=[S("document", "The bills kept running.", "After 1918", ["bills"], 110, title="Invoice: the war", lines=5),
                        S("calendar", "Germany's last payment.", "3 October 2010", ["last"], 110, flip=True, day="3", month="OCT", note="2010")]),
            dict(say="And in March twenty fifteen, Britain's Treasury repaid one point nine billion pounds of a bond called the War Loan. The Chancellor said Britain could, at last, pay off the debts it took on to fight the First World War.",
                 shows=[S("perpetual", "£1.9 billion of War Loan.", "March 2015", ["£1.9"], 100, coupon="3½%"),
                        dict(kind="quote", text="We can, at last, pay off the debts Britain incurred to fight the First World War.",
                             hl=["at", "last,"], who="George Osborne, Chancellor of the Exchequer, 3 December 2014", size=80)]),
            dict(say="It's a great headline. We think it's mostly wrong.",
                 shows=[S("newspaper", "A great headline.", "2015", ["great"], 110, headline="WAR DEBT PAID", sub="A CENTURY LATER", date="2015"),
                        dict(kind="verdict", text="The war debt was paid off.", stamp="MOSTLY NOT", size=110)]),
            dict(say="Almost none of that money was paid back the way you would pay back a loan. It was hidden, rolled over, cut, cancelled, defaulted on, and quietly shrunk by inflation.",
                 shows=[S("coins", "Not paid back like a loan.", "The real story", ["Not"], 110, stacks=[8, 5, 2]),
                        dict(kind="icons", title="What happened to the debt", items=[("lock", "Hidden"), ("clock", "Rolled over"), ("cross", "Cancelled"), ("down", "Inflated away")], hi=3)]),
            dict(say="In this video we follow the money from the first war loan to the last payment, and answer one question. Who really paid for the First World War?",
                 shows=[dict(kind="timeline", title="Following the money", items=[("1914", "First loan"), ("1917", "Big loan"), ("1932", "Cut"), ("2015", "Repaid?")], hi=3),
                        S("magnifier", "Who really paid?", "The question", ["really"], 130, label="WHO?")]),
        ]),
        dict(title="The loan that failed", art=("newspaper", dict(headline="OVER-SUBSCRIBED", sub="AND STILL THEY POUR IN", date="1914")), beats=[
            dict(say="Wars are paid for in three ways: taxes, printing money, and borrowing. Britain borrowed, and in November nineteen fourteen it launched its first War Loan.",
                 shows=[dict(kind="icons", title="Three ways to pay for a war", items=[("doc", "Taxes"), ("coin", "Printing"), ("hand", "Borrowing")], hi=2),
                        S("poster", "The first War Loan.", "November 1914", ["first"], 110, top="YOUR COUNTRY NEEDS", big="FUNDS", bottom="WAR LOAN 1914")]),
            dict(say="The target was three hundred and fifty million pounds. It offered a return of about four point one percent, when other government debt paid two and a half.",
                 shows=[dict(kind="number", value=350, pre="£", suf="m", label="the target of the first War Loan, 1914 (Bank of England research)"),
                        dict(kind="compare", left=("Other government debt", "2.5%"), right=("War Loan 1914", "4.1%"), note="A generous return, for the time")]),
            dict(say="On the twenty third of November, the Financial Times reported that the loan had been over-subscribed by two hundred and fifty million pounds. And still, it said, the applications are pouring in.",
                 shows=[S("newspaper", "Over-subscribed by £250 million.", "23 November 1914", ["£250"], 96, headline="OVER-SUBSCRIBED", sub="BY £250,000,000", date="1914"),
                        dict(kind="quote", text="And still the applications are pouring in.", hl=["pouring", "in."], who="Financial Times, 23 November 1914", size=96)]),
            dict(say="It wasn't true. In twenty seventeen, researchers went through the Bank of England's own ledgers.",
                 shows=[dict(kind="verdict", text="Over-subscribed.", stamp="FALSE", size=150),
                        S("ledger", "The Bank's own ledgers.", "Opened in 2017", ["ledgers."], 100, flip=True,
                          names=("A. Smith  £300", "J. Brown  £1,000", "Clerk  ...", "Clerk  ..."), hi=())]),
            dict(say="Only ninety one point one million pounds had been bought. That is less than a third of the target.",
                 shows=[dict(kind="number", value=91.1, dec=1, pre="£", suf="m", label="actually bought, against a £350m target"),
                        S("bars", "Less than a third.", "Target vs sold", ["third."], 120, values=[350, 91], labels=["Target", "Sold"], hi=1)]),
            dict(say="So the Bank of England plugged the gap in secret. It lent money to its chief cashier, Gordon Nairn, and his deputy, Ernest Harvey, and they bought the bonds in their own names.",
                 shows=[S("bank", "The gap, plugged in secret.", "The Bank of England", ["secret."], 110, label="BANK"),
                        S("ledger", "Bought in their own names.", "Nairn and Harvey", ["own", "names."], 96, flip=True,
                          names=("A. Smith  £300", "J. Brown  £1,000", "G. Nairn  ?", "E. Harvey  ?"), hi=(2, 3))]),
            dict(say="On the Bank's balance sheet, they were filed under other securities, not government debt. Nairn later swore a statement that the whole three hundred and fifty million had been sold to the public.",
                 shows=[S("document", "Filed as other securities.", "The balance sheet", ["other"], 100, title="Other securities", lines=5, stamp="?"),
                        S("speech", "All £350m sold to the public.", "The sworn statement", ["£350m"], 100, flip=True, text="All sold to the public")]),
            dict(say="John Maynard Keynes, in a Treasury memo in nineteen fifteen, called it a masterly manipulation. The researchers called the loan a spectacular failure that was covered up.",
                 shows=[dict(kind="quote", text="a masterly manipulation", hl=["masterly"], who="John Maynard Keynes, Treasury memo, 1915 (Bank Underground)", size=130),
                        S("stamp", "A spectacular failure, covered up.", "The verdict, 2017", ["covered", "up."], 100, flip=True, text="COVERED UP")]),
            dict(say="Here is the first thing the story gets wrong. The war was not first funded by eager savers. The central bank quietly bought the debt itself, which is close to printing the money.",
                 shows=[S("bulb", "What the story gets wrong.", "Lesson one", ["wrong."], 120, text="1"),
                        S("figures", "Not eager savers.", "1914", ["Not"], 110, flip=True, n=5, hi=None),
                        dict(kind="flow", items=[("bank", "Central bank"), ("doc", "Buys the bonds"), ("coin", "Like new money")])]),
        ]),
        dict(title="If you cannot fight, invest", art=("poster", dict()), beats=[
            dict(say="By nineteen seventeen, Britain needed far more. So it went to the public with everything it had.",
                 shows=[S("chart", "Britain needed far more.", "1917", ["far", "more."], 110, values=[1, 1.4, 2.2, 3.4, 5, 7.4], label="Needs"),
                        S("poster", "Everything it had.", "The campaign", ["Everything"], 110, flip=True)]),
            dict(say="The slogan was blunt. If you cannot fight, invest all you can in five percent bonds. Unlike the soldier, the investor runs no risk.",
                 shows=[S("speech", "The slogan was blunt.", "1917", ["blunt."], 120, text="If you cannot fight..."),
                        S("poster", "Invest all you can in 5% bonds.", "", ["5%"], 100, flip=True, top="IF YOU CANNOT FIGHT", big="INVEST", bottom="5% WAR BONDS"),
                        dict(kind="quote", text="Unlike the soldier, the investor runs no risk.", hl=["no", "risk."], who="War Loan slogan, 1917 (as quoted by MoneyWeek)", size=92)]),
            dict(say="This time it worked. Just over two million people signed up between January and February, with about nine hundred and sixty million pounds of new money.",
                 shows=[S("queue", "Just over 2 million people.", "January to February 1917", ["2", "million"], 100, n=8, label="SUBSCRIBERS"),
                        dict(kind="number", value=960, pre="£", suf="m", label="of new money, about, in the 1917 War Loan (Western Front Association)")]),
            dict(say="Compare that with nineteen fourteen. The Bank's ledgers count ninety seven thousand, six hundred and thirty five investors in the first loan.",
                 shows=[S("ledger", "Compare 1914.", "The first loan", ["1914."], 110, names=("A. Smith  £300", "J. Brown  £1,000", "...", "..."), hi=()),
                        dict(kind="number", value=97635, label="investors in the 1914 War Loan (Bank Underground)")]),
            dict(say="With old bonds swapped in, the War Loan of nineteen seventeen came to around two billion pounds.",
                 show=S("coins", "Around £2 billion in all.", "With old bonds swapped in", ["£2", "billion"], 110, stacks=[3, 6, 10], labels=["1914", "1915", "1917"])),
            dict(say="Hold on to that slogan, because it is the part the rest of this story undoes. The investor runs no risk.",
                 shows=[S("bulb", "Hold on to that slogan.", "", ["slogan."], 110, text="!"),
                        dict(kind="verdict", text="The investor runs no risk.", stamp="WATCH", size=110)]),
            dict(say="After the war, the five percent was a heavy bill. Interest alone on these loans would run for nearly a century.",
                 shows=[S("interest_stack", "A heavy bill.", "5% a year", ["heavy"], 110, base="£2bn", rate="5%"),
                        dict(kind="number", value=5.5, dec=1, pre="£", suf=" bn", label="interest paid on the 1917 War Loan and its successor, 1917 to 2015 (UK Debt Management Office estimate)")]),
        ]),
        dict(title="A bond with no end", art=("perpetual", dict()), beats=[
            dict(say="In nineteen thirty two, the government asked holders to swap their five percent bonds for new ones paying three and a half. Holders were asked to take the cut voluntarily.",
                 shows=[S("rateboard", "5% swapped for 3.5%.", "1932", ["3.5%."], 110, rate="3½%", sub="WAS 5%"),
                        S("figures", "A cut, taken voluntarily.", "The holders", ["voluntarily."], 110, flip=True, n=6, hi=2)]),
            dict(say="The new bond had a strange feature. It had no date by which it had to be repaid. The government could pay the interest forever.",
                 shows=[S("perpetual", "No date to repay.", "3.5% War Loan", ["No", "date"], 110),
                        dict(kind="term", term="Perpetual", text="A bond with no maturity: it pays its coupon every year, and the issuer repays only if it chooses to."),
                        dict(kind="icon", icon="clock", label="Forever", text="Interest, every year, forever.", hl=["forever."], size=100)]),
            dict(say="Britain had done this before. In nineteen twenty seven, Winston Churchill, then Chancellor, rolled maturing war bonds into a four percent bond with no end date, called Consols.",
                 shows=[S("book", "Britain had done this before.", "", ["before."], 110, title="Undated debt"),
                        S("perpetual", "4% Consols, 1927.", "Churchill, Chancellor", ["4%"], 110, flip=True, title="CONSOLS", coupon="4%")]),
            dict(say="The same refinancing swept up an older bond from eighteen fifty three. That bond had itself absorbed the capital stock of the South Sea Company, the bubble that burst in seventeen twenty.",
                 shows=[dict(kind="timeline", title="One debt, rolled into the next", items=[("1720", "South Sea"), ("1853", "Gladstone"), ("1927", "Consols"), ("2015", "Repaid")], hi=3),
                        S("ship", "Back to the South Sea Company.", "1720", ["South", "Sea"], 100)]),
            dict(say="By one estimate, the Consols paid about one point two six billion pounds of interest between nineteen twenty seven and twenty fifteen. The government never had to give the money back, so it just kept paying.",
                 shows=[dict(kind="number", value=1.26, dec=2, pre="£", suf=" bn", label="interest paid on the 4% Consols since 1927 (MoneyWeek)"),
                        S("payback", "It just kept paying.", "Interest, year after year", ["kept"], 100, flip=True, years=10, paid=10, label="")]),
            dict(say="Here is the idea every analyst should know. A bond with no end is valued like this: the yearly payment, divided by the return investors want.",
                 shows=[S("bulb", "The idea every analyst should know.", "Interview prep", ["analyst"], 96, text="÷"),
                        dict(kind="term", term="P = C ÷ y", text="A perpetuity: the yearly coupon divided by the yield investors want.")]),
            dict(say="In twenty fourteen, the War Loan paid three pounds fifty a year and traded at about ninety one pounds seventy, a yield of three point eight percent. Three fifty divided by three point eight percent is about ninety two pounds. The formula holds.",
                 shows=[dict(kind="compare", left=("Coupon", "£3.50"), right=("Yield", "3.8%"), note="2014 (MoneyWeek)"),
                        dict(kind="number", value=92, pre="£", label="3.50 ÷ 3.8%: our own arithmetic, beside a quoted price of £91.70"),
                        S("scale", "The formula holds.", "", ["holds."], 110, flip=True, left="£92", right="£91.70", tip=0)]),
            dict(say="And it tells you why the bonds were repaid when they were. With interest rates very low, the Treasury could borrow more cheaply than three and a half percent, so swapping the old debt for new debt saved money.",
                 shows=[S("chart", "Interest rates very low.", "2014", ["low."], 110, values=[8, 7, 6.5, 5, 4, 2.5, 1.5], color="#0F766E", label="Rates", arrow=False),
                        dict(kind="flow", items=[("doc", "Old 3.5% bond"), ("hand", "Borrow cheaper"), ("check", "Repay the old")])]),
        ]),
        dict(title="Germany's bill", art=("coins", dict(stacks=[10, 7, 4, 1])), beats=[
            dict(say="Now the other side. At Versailles in nineteen nineteen, Germany's bill was set at one hundred and thirty two billion gold marks.",
                 shows=[S("document", "The Treaty of Versailles.", "1919", ["Versailles."], 110, title="Treaty, 1919", lines=6, stamp="SIGNED"),
                        dict(kind="number", value=132, suf=" bn", label="gold marks: the reparations bill set for Germany (History.com)")]),
            dict(say="One British Treasury official thought the bill would ruin Europe. John Maynard Keynes resigned in May nineteen nineteen and wrote a book calling it a Carthaginian peace.",
                 shows=[S("suitcase", "He resigned in May 1919.", "Keynes, at Paris", ["resigned"], 110, n=1),
                        S("book", "A Carthaginian peace.", "The Economic Consequences of the Peace, 1919", ["Carthaginian"], 96, flip=True, title="Consequences")]),
            dict(say="He argued the bill should be capped at two billion pounds. The book sold about a hundred thousand copies in six months.",
                 shows=[dict(kind="number", value=2000, pre="£", suf="m", label="the cap Keynes argued for"),
                        S("figures", "About 100,000 copies in 6 months.", "Readers", ["100,000"], 100, flip=True, n=7, hi=None)]),
            dict(say="Then the bill kept shrinking. The Dawes Plan of nineteen twenty four eased it, and the Young Plan cut it to one hundred and twenty one billion.",
                 show=dict(kind="timeline", title="Germany's bill", items=[("1919", "132 bn"), ("1924", "Dawes"), ("Young", "121 bn"), ("1933", "Stopped")], hi=2)),
            dict(say="In nineteen thirty three, Hitler stopped paying altogether.",
                 show=S("stamp", "Payments stopped.", "1933", ["stopped."], 130, text="STOPPED")),
            dict(say="In nineteen fifty three, a deal in London cancelled half of what was left and stretched out the rest. Part of the interest would only fall due if Germany was ever reunited.",
                 shows=[S("handshake", "Half cancelled in London.", "1953", ["Half"], 110, left="Lenders", right="Germany"),
                        S("wall", "Due only if Germany reunited.", "A clause for later", ["reunited."], 100, flip=True, gap=False, label="1953")]),
            dict(say="It did, in nineteen ninety. And on the third of October twenty ten, the twentieth anniversary, Germany made its final payment, of around ninety six million dollars.",
                 shows=[S("wall", "Reunited in 1990.", "", ["1990."], 120, gap=True, label="1990"),
                        dict(kind="number", value=96, pre="$", suf="m", label="around: Germany's final payment, 3 October 2010 (RNZ)")]),
            dict(say="Ninety two years after the war ended. But notice what really happened: most of the bill was never paid at all. It was cut, suspended and cancelled.",
                 shows=[S("calendar", "92 years later.", "1918 to 2010", ["92"], 120, day="92", month="YEARS", note="1918 to 2010"),
                        S("cake", "Most of the bill, never paid.", "Our reading", ["never"], 100, flip=True, slices=8, hi=0),
                        dict(kind="icons", title="What happened to the bill", items=[("down", "Cut"), ("clock", "Suspended"), ("cross", "Cancelled")], hi=2)]),
        ]),
        dict(title="The debt nobody mentions", art=("handshake", dict(left="UK", right="US")), beats=[
            dict(say="Britain didn't only borrow from its own people. It also borrowed heavily from the United States.",
                 shows=[S("ship", "Britain borrowed too.", "1917", ["borrowed"], 110),
                        S("handshake", "From the United States.", "", ["United", "States."], 100, flip=True, left="UK", right="US")]),
            dict(say="In the nineteen thirties the dominoes fell. Germany stopped paying, France defaulted on America, and in nineteen thirty four, Britain stopped paying too.",
                 shows=[S("dominoes", "The dominoes fell.", "The 1930s", ["fell."], 100, labels=["Germany", "France", "UK", ""], fall=3),
                        S("calendar", "Britain stopped paying.", "1934", ["stopped"], 120, flip=True, day="1934", month="UK", note="stopped paying")]),
            dict(say="The unpaid debt was more than four billion dollars. According to the historian David James Gill, it still stood in the way of Britain returning to the New York bond market in the late nineteen seventies.",
                 shows=[dict(kind="number", value=4, pre="$", suf=" bn+", label="Britain's unpaid war debt to the United States (Economic History Society)"),
                        S("ticker", "Still in the way in the late 1970s.", "New York", ["1970s."], 96, flip=True, price="UK", change="Blocked")]),
            dict(say="Ministers had kept paying for a while after France stopped. Their main fear, Gill writes, was that countries owing Britain money would use a British default as an excuse to stop paying Britain.",
                 shows=[S("calendar", "Paying on, after France stopped.", "18 months", ["France"], 100, day="18", month="MONTHS", note="after France"),
                        S("dominoes", "The fear: Britain's debtors stop too.", "The cabinet's worry", ["fear:"], 96, flip=True, labels=["UK", "Debtor", "Debtor", "Debtor"], fall=1)]),
            dict(say="So when the headline says Britain paid off its First World War debt, it means the debt Britain owed to its own people. The debt it owed to America was simply never paid.",
                 shows=[S("newspaper", "Paid off, says the headline.", "2015", ["headline."], 110, headline="WAR DEBT PAID", sub="A CENTURY LATER", date="2015", stamp="HALF TRUE"),
                        dict(kind="split", left=("people", "Owed to savers", "Repaid, 2015"), right=("globe", "Owed to the US", "Never paid"), mid="vs")]),
        ]),
        dict(title="So who paid?", art=("shrink", dict()), beats=[
            dict(say="Back to twenty fifteen: was the War Loan really paid off? The Western Front Association called it bookkeeping.",
                 shows=[S("perpetual", "Was it really paid off?", "2015", ["really"], 110),
                        S("book", "It called it bookkeeping.", "Western Front Association", ["bookkeeping."], 100, flip=True, title="Bookkeeping")]),
            dict(say="The Treasury repaid the old bond by borrowing again, more cheaply. The debt did not disappear; it moved into other government borrowing.",
                 shows=[dict(kind="flow", items=[("doc", "Old War Loan"), ("hand", "New borrowing"), ("clock", "Still owed")]),
                        S("dominoes", "The debt moved, it did not vanish.", "", ["moved,"], 100, flip=True, labels=["1917", "1932", "2015", "?"], fall=0)]),
            dict(say="And look at who held it at the end. More than a hundred and twenty thousand holders. About ninety seven thousand of them held less than a thousand pounds.",
                 shows=[S("perpetual", "Who held it at the end?", "3.5% War Loan, 2014", ["end?"], 110),
                        S("figures", "More than 120,000 holders.", "December 2014", ["120,000"], 110, n=7, hi=3),
                        S("bars", "97,000 held under £1,000.", "Small savers", ["97,000"], 100, flip=True, values=[120, 97, 38], labels=["All", "<£1,000", "<£100"], hi=1)]),
            dict(say="Now the real cost. For the four percent Consols of nineteen twenty seven, one estimate is that a hundred pounds lent then was bought back for the equivalent of one pound eighty two in today's money.",
                 shows=[S("shrink", "£100 in 1927.", "Consols", ["£100"], 110),
                        dict(kind="number", value=1.82, dec=2, pre="£", label="what £100 lent in 1927 was worth in real terms when repaid (MoneyWeek estimate)")]),
            dict(say="The pounds came back. What they could buy had almost all gone. That is who paid for the war: the savers, through inflation, slowly, over almost ninety years.",
                 shows=[S("pricetag", "The pounds came back.", "", ["came", "back."], 110, value="£100", tag="BACK"),
                        S("shrink", "What they could buy had gone.", "", ["gone."], 110, flip=True),
                        dict(kind="icon", icon="people", label="Who really paid", text="The savers, through inflation.", hl=["savers,"], size=100)]),
            dict(say="Remember the slogan: the investor runs no risk. The money came back, but it was worth a sliver of what was lent.",
                 shows=[dict(kind="verdict", text="The investor runs no risk.", stamp="MYTH", size=110),
                        S("cake", "Worth a sliver of what was lent.", "", ["sliver"], 110, flip=True, slices=12, hi=0)]),
            dict(say="So here is what we take from it. Governments almost never pay off big debts in the way you pay off a mortgage. They roll them over, and time and inflation do the rest.",
                 shows=[S("bulb", "What we take from it.", "Our reading", ["take"], 120, text="2"),
                        S("house", "Not like paying off a mortgage.", "", ["mortgage."], 100, flip=True, price="PAID"),
                        S("clock", "Time and inflation do the rest.", "", ["inflation"], 110, time="11:00")]),
            dict(say="Which means a fixed sum lent for a very long time is a bet that prices stay calm. That is worth knowing before you buy any long bond. This is history, not financial advice.",
                 shows=[S("scale", "A bet that prices stay calm.", "A long, fixed loan", ["calm."], 110, left="Coupon", right="Inflation", tip=1),
                        S("magnifier", "Worth knowing before any long bond.", "", ["long"], 100, flip=True, label="LONG?"),
                        dict(kind="icon", icon="book", label="History, not advice", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="And if an interviewer asks what happens to a perpetual bond when yields rise, you know the answer. The price falls, because you divide the same coupon by a bigger number.",
                 shows=[S("document", "The interview question.", "Interview prep", ["interview"], 110, title="Perpetual bond", lines=4, stamp="C ÷ y"),
                        S("seesaw", "Yields up, price down.", "Same coupon, bigger divisor", ["down."], 110, flip=True, left="Yield", right="Price", tip=-1)]),
            dict(say="A hundred and eight years after the guns stopped, here is our question for you. If you had been asked in nineteen seventeen, would you have bought the bond? Tell us in the comments.",
                 shows=[S("clock", "108 years after the Armistice.", "11 November 2026", ["108"], 110, time="11:00"),
                        S("poster", "Would you have bought the bond?", "Your turn", ["bought"], 100, flip=True),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "In March 2015 Britain repaid £1.9bn of its First World War debt, and the headlines said the war had finally been paid off. "
        "We think that's mostly wrong. The first War Loan in 1914 raised £91.1m against a £350m target, and the Bank of England quietly plugged "
        "the gap through its own cashiers. The big 1917 loan sold \"no risk\" to 2 million savers. Their 5% was cut to 3.5% in 1932, on a bond with no repayment date. "
        "Germany's 132 billion gold mark bill was cut, stopped and cancelled before a last payment in 2010, and Britain's own debt to the United States was never paid at all. "
        "We follow the money, show how a perpetual bond is priced (a favourite interview question), and end on who really paid: the savers, through inflation. "
        "Would you have bought the bond in 1917?"),
    sources=[
        ("World History Encyclopedia, The 1918 Armistice with Germany", "https://www.worldhistory.org/article/2833/the-1918-armistice-with-germany/"),
        ("GOV.UK, Chancellor to repay the nation's First World War debt (3 December 2014)", "https://gov.uk/government/news/chancellor-to-repay-the-nations-first-world-war-debt"),
        ("Bank Underground (Bank of England staff blog), Your country needs funds (8 August 2017)", "https://bankunderground.co.uk/2017/08/08/your-country-needs-funds-the-extraordinary-story-of-britains-early-efforts-to-finance-the-first-world-war/"),
        ("Queen Mary University of London, Bank of England ledgers reveal failure of World War One loan scheme (8 August 2017)", "https://www.qmul.ac.uk/news/latest-news/2017/hss/bank-of-england-ledgers-reveal-failure-of-world-war-one-loan-scheme.html"),
        ("Western Front Association, The First World War paid off?", "https://www.westernfrontassociation.com/world-war-i-articles/the-first-world-war-paid-off/"),
        ("MoneyWeek, Why Britain is repaying its war debt", "https://moneyweek.com/355224/repaying-our-war-debt"),
        ("History.com, Germany Finally Pays Off World War I Debt", "https://www.history.com/articles/germany-world-war-i-debt-treaty-versailles"),
        ("RNZ, Germany finally pays off its World War I debt (3 October 2010)", "https://www.rnz.co.nz/news/world/58438/germany-finally-pays-off-its-world-war-i-debt"),
        ("The Economic Consequences of the Peace (Keynes, 1919), overview", "https://en.wikipedia.org/wiki/The_Economic_Consequences_of_the_Peace"),
        ("Economic History Society, David James Gill, The UK's unpaid war debts to the United States, 1917-1980", "https://ehs.org.uk/the-uks-unpaid-war-debts-to-the-united-states-1917-1980/"),
    ],
    source_note="The £92 perpetuity price (3.50 divided by 3.8%) is our own arithmetic. The poster, newspaper, ledger and bond certificate are our own drawings, not copies of real ones.",
    hashtags=["ArmisticeDay", "FinanceHistory", "WarDebt"],
    tags=["First World War debt", "WW1 war loan", "Armistice Day", "war bonds", "Bank of England 1914", "perpetual bond",
          "consols", "German reparations", "Treaty of Versailles", "Keynes", "inflation", "government debt", "history of finance",
          "finance explained", "bond pricing"],
)

if __name__ == "__main__":
    make(EP)
