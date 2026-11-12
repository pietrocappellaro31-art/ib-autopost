"""
YouTube #5 (12 Nov 2026): where money actually comes from. The common picture is that a bank takes in
savers' deposits and lends them out, perhaps "multiplying" them a few times. Central banks themselves
say that is wrong: when a bank makes a loan it creates a new deposit at the same moment, so most money
is created by ordinary banks lending. Technical explainer (how money works), with one interview
question at the end ("do banks lend out deposits?").

Point of view: a bank deposit is not a pile of cash in a vault; it is the bank's promise to pay, and
most of those promises were typed into being by a loan. That one fact explains why bank runs can
happen, why deposit insurance exists, and why the 2025 US stablecoin law chose the opposite design (a
token fully backed and not lent on). Educational, not advice.

Every claim, sourced:
  [1] Bank of England, Quarterly Bulletin 2014 Q1, "Money creation in the modern economy" (Michael
      McLeay, Amar Radia and Ryland Thomas, Monetary Analysis Directorate): "the majority of money in the
      modern economy is created by commercial banks making loans"; banks "do not act simply as
      intermediaries, lending out deposits that savers place with them"; "Whenever a bank makes a loan, it
      simultaneously creates a matching deposit"; bank deposits are 97% of broad money in circulation
      (December 2013), currency the rest, mostly IOUs from the central bank; section "Two misconceptions
      about money creation": the intermediary view and the "money multiplier"; "the repayment of bank
      loans destroys money"; limits: market forces (banks must lend profitably in a competitive market),
      regulation, and "The ultimate constraint on money creation is monetary policy"; QE buys assets mainly
      from non-bank financial companies and "initially increases the amount of bank deposits those
      companies hold"; the reserves QE creates are not "free money" for banks.
  [2] Deutsche Bundesbank, "How money is created", 25 April 2017: "banks can create book money just by
      making an accounting entry"; this "refutes a popular misconception that banks act simply as
      intermediaries at the time of lending"; "excess central bank reserves are not a necessary
      precondition for a bank to grant credit (and thus create money)"; banks need central bank reserves to
      settle payments when deposits move to other banks, and only the central bank creates those;
      "Commercial banks' ways of creating money are not infinite".
  [3] Federal Reserve Board, "Reserve Requirements": "As announced on March 15, 2020, the Board reduced
      reserve requirement ratios to zero percent effective March 26, 2020. This action eliminated reserve
      requirements for all depository institutions."
  [4] Bank of England Quarterly Bulletin 1969 Q2, "The Bank of England note: a short history": before the
      Bank of England was set up in 1694, banking in England "had been virtually restricted to the
      goldsmiths in London"; they were "increasingly using these funds for making loans"; "their promissory
      notes payable on demand, which were issued to depositors" came "to be used as a convenient means of
      making payments"; "It is from these goldsmiths' notes that the Bank of England note ultimately derives."
  [5] Federal Reserve Board, "Review of the Federal Reserve's Supervision and Regulation of Silicon Valley
      Bank", April 2023, executive summary: "On March 9, SVB lost over $40 billion in deposits, and SVBFG
      management expected to lose over $100 billion more on March 10"; together roughly 85 percent of the
      deposit base; the deposits were largely uninsured; SVB failed on March 10, 2023; for comparison,
      Wachovia about $10 billion over 8 days in 2008, Washington Mutual $19 billion over 16 days.
  [6] FDIC, "Deposits at a glance": "The standard insurance amount is $250,000 per depositor, per insured
      bank, for each account ownership category."
  [7] Fenwick, "Congress Enacts Comprehensive Stablecoin Legislation" (23 July 2025): the GENIUS Act was
      signed into law on 18 July 2025; reserves backing stablecoins on at least a 1:1 basis; it explicitly
      prohibits paying interest to holders; it restricts rehypothecation of reserves.
  [8] Federal Reserve Bank of St. Louis, "Regulated Payment Stablecoins Become Reality in the U.S."
      (December 2025): reserves are US currency, insured deposits, Treasuries with no more than 93 days to
      maturity and similar; issuers' activities are generally limited to issuing, redeeming, managing
      reserves and custody.
Our own illustration, labelled on screen: the £10,000 loan and the 100 / 90 / 81 textbook cascade are
examples, not data. The strongbox, notes, screen and token are our own drawings.

    python build/youtube_ep005.py
"""

from youtube import make

# S(drawing, line, label, highlighted words, size, flip, **drawing options); SC(drawing, heading, **drawing options)
S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)

EP = dict(
    slug="yt-005-where-money-comes-from",
    title="Your Bank Doesn't Lend Out Your Savings. It Creates New Money.",
    thumb=dict(art=("keystroke", dict(amount=10000)),
               big_a="A loan.<br>A keystroke.<br><span style='color:#0A0A0A'>New money.</span>", size_a=96,
               art_b=("t_account", dict()),
               big="Your bank <span style='color:#D93A12'>doesn't</span> lend your savings.",
               small="Where money really comes from", ghost="97%", size=100),
    chapters=[
        dict(title="The money in your account", art=("bank", dict(label="BANK")), beats=[
            dict(say="Picture the money in your bank account. Most people imagine a pile of it, sitting somewhere in a vault with your name on it.",
                 shows=[S("phone", "The money in your account.", "Picture it", ["your"], 110),
                        S("bank", "A pile of it, in a vault?", "What most people imagine", ["vault?"], 110, flip=True, label="VAULT")]),
            dict(say="And they imagine that when someone borrows, the bank lends them a slice of your pile. That is the story most of us were taught.",
                 shows=[S("cake", "A slice of your pile, lent out.", "The usual story", ["slice"], 100, slices=8, hi=1),
                        S("book", "The story we were taught.", "School, textbooks", ["taught."], 110, flip=True, title="Economics 101")]),
            dict(say="In twenty fourteen, the Bank of England published a paper saying that story is wrong.",
                 show=S("document", "The story is wrong, says a central bank.", "Bank of England, 2014", ["wrong,"], 96,
                        title="Money creation", lines=5, stamp="2014")),
            dict(say="Its words were plain. Banks do not act simply as intermediaries, lending out deposits that savers place with them.",
                 shows=[S("bulb", "Its words were plain.", "Quarterly Bulletin, 2014 Q1", ["plain."], 120, text="!"),
                        dict(kind="quote", text="Banks do not act simply as intermediaries, lending out deposits that savers place with them.",
                             hl=["do", "not"], who="Bank of England, Money creation in the modern economy, 2014", size=80)]),
            dict(say="Instead, most of the money in the economy is created by ordinary banks, at the moment they make a loan.",
                 shows=[S("keystroke", "Created when a bank lends.", "Our reading of the paper", ["lends."], 100, amount=10000)]),
            dict(say="In this video we show how that works, where the idea came from three centuries ago, what stops banks printing money without limit, and why it matters for your savings today.",
                 shows=[dict(kind="timeline", title="Where we are going", items=[("Loan", "How it works"), ("1600s", "Goldsmiths"), ("Limits", "What stops it"), ("Today", "Your savings")], hi=3)]),
        ]),
        dict(title="What the textbook says", art=("multiplier", dict()), beats=[
            dict(say="The textbook version has two steps. First, savers put money in, and the bank lends it out.",
                 shows=[S("book", "Two steps.", "The textbook", ["Two"], 130, title="Textbook"),
                        dict(kind="flow", items=[("people", "Savers deposit"), ("bank", "Bank holds it"), ("hand", "Bank lends it")])]),
            dict(say="Second, that loan gets spent and deposited at another bank, which lends most of it again, and again, until a small deposit has multiplied into a lot of money.",
                 shows=[S("multiplier", "Lent, re-deposited, lent again.", "The money multiplier", ["again."], 92, stamp_text="")]),
            dict(say="Put in a hundred, the bank keeps ten and lends ninety, the next bank lends eighty one, and so on. Our numbers here are only an example of how the textbook tells it.",
                 shows=[S("bars", "100, then 90, then 81.", "Our example", ["90,"], 110, values=[100, 90, 81, 73, 66], labels=["100", "90", "81", "73", "66"], hi=0),
                        dict(kind="term", term="Money multiplier", text="The textbook idea that banks lend out a fixed share of each deposit, so a deposit multiplies through the system.")]),
            dict(say="The Bank of England called both steps misconceptions. Its paper has a section titled Two misconceptions about money creation.",
                 shows=[S("multiplier", "Both steps: misconceptions.", "Bank of England, 2014", ["misconceptions."], 92, stamp_text="MYTH"),
                        S("document", "Two misconceptions about money creation.", "The section title", ["misconceptions"], 92, flip=True,
                          title="Two misconceptions", lines=5, stamp="MYTH")]),
            dict(say="Germany's central bank, the Bundesbank, said the same in twenty seventeen. It called the intermediary story a popular misconception.",
                 shows=[S("bank", "The Bundesbank, 2017.", "Germany's central bank", ["2017."], 110, label="BUNDESBANK"),
                        dict(kind="verdict", text="Banks lend out savers' deposits.", stamp="MYTH", size=104)]),
        ]),
        dict(title="The loan is a keystroke", art=("keystroke", dict(amount=10000)), beats=[
            dict(say="So here is what really happens. Say you borrow ten thousand pounds from your bank.",
                 shows=[S("magnifier", "What really happens.", "Step by step", ["really"], 120, label="HOW?"),
                        dict(kind="number", value=10000, pre="£", label="a loan, our example")]),
            dict(say="The bank does not go to its vault, or take ten thousand pounds out of someone else's account. It types ten thousand pounds into yours.",
                 shows=[S("bank", "Nobody's account goes down.", "Not from a vault", ["Nobody's"], 110, label="VAULT"),
                        S("keystroke", "It types it into yours.", "Your account", ["types"], 110, flip=True, amount=10000)]),
            dict(say="The Bundesbank put it in one line. Banks can create book money just by making an accounting entry.",
                 shows=[S("ledger", "One line.", "Bundesbank, 2017", ["One"], 130, names=("Loan  +10,000", "Deposit  +10,000", "", ""), hi=(0, 1)),
                        dict(kind="quote", text="Banks can create book money just by making an accounting entry.", hl=["accounting", "entry."],
                             who="Deutsche Bundesbank, How money is created, 25 April 2017", size=88)]),
            dict(say="Look at the bank's books. On one side, a new asset: your loan, which you will pay back. On the other side, a new liability: your deposit, which the bank owes you.",
                 shows=[S("t_account", "Look at the bank's books.", "A balance sheet", ["books."], 110, amount="+£10k"),
                        S("t_account", "An asset: your loan.", "What you owe the bank", ["asset:"], 100, flip=True, amount="+£10k"),
                        S("t_account", "A liability: your deposit.", "What the bank owes you", ["liability:"], 100, amount="+£10k")]),
            dict(say="Both appear at the same moment. In the Bank of England's words, whenever a bank makes a loan, it simultaneously creates a matching deposit.",
                 shows=[SC("t_account", "Created together", amount="+£10k"),
                        dict(kind="quote", text="Whenever a bank makes a loan, it simultaneously creates a matching deposit.",
                             hl=["simultaneously"], who="Bank of England, 2014", size=88)]),
            dict(say="That deposit is new money. You can spend it, and the shop you pay will happily take it.",
                 shows=[S("coins", "That deposit is new money.", "", ["new", "money."], 110, stacks=[2, 5, 9]),
                        S("card_tap", "You can spend it.", "", ["spend"], 110, flip=True, amount="£10,000")]),
            dict(say="And it runs the other way too. When you pay the loan back, the deposit and the loan both shrink, and that money disappears. Repaying a loan destroys money.",
                 shows=[S("t_account", "It runs the other way too.", "Repayment", ["other"], 110, amount="£10k", destroy=True),
                        SC("t_account", "Repaid: both sides go", amount="£10k", destroy=True),
                        dict(kind="verdict", text="Repaying a loan destroys money.", stamp="TRUE", size=104)]),
        ]),
        dict(title="The goldsmiths' trick", art=("goldsmith", dict()), beats=[
            dict(say="None of this is new. Before the Bank of England was set up in sixteen ninety four, banking in England was almost entirely done by the goldsmiths of London.",
                 shows=[S("bulb", "None of this is new.", "", ["new."], 120, text="?"),
                        S("goldsmith", "The goldsmiths of London.", "Before 1694", ["goldsmiths"], 100, flip=True, bars=3, notes=3)]),
            dict(say="People left money and valuables with them for safekeeping, and the goldsmiths issued notes to their depositors, promises to pay on demand.",
                 shows=[S("goldsmith", "Promises to pay on demand.", "Notes for depositors", ["Promises"], 100, bars=3, notes=3)]),
            dict(say="Those notes started to change hands as payment. And the goldsmiths increasingly used the money left with them to make loans.",
                 shows=[S("notes", "Notes changed hands as payment.", "", ["payment."], 100, left="£", right="£", lab_l="Buyer", lab_r="Seller", n_left=1),
                        S("goldsmith", "Lending the money left with them.", "Our drawing of the idea", ["Lending"], 96, flip=True, bars=3, notes=6)]),
            dict(say="That is the whole idea in its first form. More promises to pay than there is gold to pay them with.",
                 shows=[S("goldsmith", "The whole idea, in its first form.", "", ["first"], 100, bars=3, notes=6),
                        dict(kind="compare", left=("Gold in the box", "3"), right=("Promises to pay", "6"), note="Our illustration, not a historical count")]),
            dict(say="And the Bank of England's own history says its banknote ultimately derives from the notes of those goldsmiths.",
                 shows=[dict(kind="timeline", title="From goldsmiths to banknotes", items=[("1600s", "Goldsmiths' notes"), ("1694", "Bank of England"), ("Today", "Bank deposits")], hi=2)]),
        ]),
        dict(title="So what stops them?", art=("scale", dict(left="Lend", right="Limits", tip=1)), beats=[
            dict(say="If a bank can type money into being, why doesn't it type a trillion? Because it can't do it for free.",
                 shows=[S("keystroke", "Why not type a trillion?", "The obvious question", ["trillion?"], 100, amount=1000000000000, pre="£"),
                        S("stamp", "It can't do it for free.", "", ["free."], 110, flip=True, text="NOT FREE")]),
            dict(say="First, the loan has to make money. A bank that lends to people who can't pay it back loses, and competing banks are trying to win the same borrowers.",
                 shows=[S("figures", "The loan has to make money.", "Limit one", ["make"], 110, n=5, hi=2),
                        S("seesaw", "Competing for the same borrowers.", "", ["Competing"], 100, flip=True, left="Bank A", right="Bank B", tip=0)]),
            dict(say="Second, the money moves. When you spend your ten thousand at a shop that banks somewhere else, your bank has to pay the other bank in central bank money, called reserves, and only the central bank can create those.",
                 shows=[S("flow", "The money moves.", "Limit two", ["moves."], 120, steps=("Your bank", "Reserves", "Their bank")),
                        dict(kind="term", term="Reserves", text="Money that banks hold at the central bank and use to pay each other. Only the central bank creates it.")]),
            dict(say="The Bundesbank makes the same point. Commercial banks' ways of creating money, it says, are not infinite.",
                 shows=[S("bank", "The same point, from Frankfurt.", "Bundesbank, 2017", ["same"], 110, label="BUNDESBANK"),
                        dict(kind="quote", text="Commercial banks' ways of creating money are not infinite.", hl=["not", "infinite."],
                             who="Deutsche Bundesbank, How money is created, 2017", size=96)]),
            dict(say="Third, regulators set rules on how much capital a bank must hold against its loans.",
                 shows=[S("document", "Rules on capital.", "Limit three", ["capital."], 110, title="Capital rules", lines=5, stamp="RULES")]),
            dict(say="And fourth, the one the Bank of England calls the ultimate constraint: monetary policy. The central bank sets the interest rate, and the price of borrowing decides how much people want to borrow.",
                 shows=[S("rateboard", "The ultimate constraint.", "Limit four", ["ultimate"], 100, rate="RATE", sub="MONETARY POLICY"),
                        S("seesaw", "Rates up, borrowing down.", "", ["borrowing"], 100, flip=True, left="Rate", right="Loans", tip=1)]),
            dict(say="Notice what is not on that list. In America, the Federal Reserve cut the share of deposits banks had to keep in reserve to zero, from March twenty sixth, twenty twenty.",
                 shows=[S("magnifier", "What is not on the list.", "", ["not"], 110, label="MISSING?"),
                        dict(kind="number", value=0, suf="%", label="reserve requirement for all US depository institutions since 26 March 2020 (Federal Reserve)")]),
        ]),
        dict(title="What about printing money?", art=("document", dict(title="Bonds", lines=4, stamp="BOUGHT")), beats=[
            dict(say="So where does the central bank come in, when people say it is printing money? The Bank of England's paper answers that too.",
                 shows=[S("speech", "Printing money?", "What people say", ["Printing"], 120, text="Printing money?"),
                        S("document", "The paper answers that too.", "Bank of England, 2014", ["too."], 100, flip=True, title="Quantitative easing", lines=5)]),
            dict(say="In quantitative easing, the central bank buys assets such as government bonds, mostly from firms that are not banks, like pension funds. The paper's own example is a purchase of one billion pounds of government bonds from a pension fund.",
                 shows=[dict(kind="flow", items=[("bank", "Central bank"), ("doc", "Buys bonds"), ("people", "Pension fund")]),
                        dict(kind="number", value=1, pre="£", suf=" bn", label="of government bonds from a pension fund: the paper's own example")]),
            dict(say="The pension fund sells the bonds and gets a bank deposit in return. So quantitative easing adds to deposits directly, and those deposits are money.",
                 shows=[S("t_account", "Bonds out, a deposit in.", "The pension fund's bank", ["deposit"], 100, left="RESERVES", right="DEPOSIT", amount="+£1bn",
                          title="THE PENSION FUND'S BANK"),
                        dict(kind="verdict", text="QE adds to deposits directly.", stamp="TRUE", size=104)]),
            dict(say="What it does not do, the paper says, is hand banks free money to lend. The extra reserves are not an important part of how it works.",
                 shows=[dict(kind="verdict", text="QE gives banks free money to lend.", stamp="MYTH", size=100),
                        S("stamp", "Not free money for banks.", "", ["free"], 110, flip=True, text="NOT FREE")]),
        ]),
        dict(title="When everyone asks at once", art=("outflow", dict()), beats=[
            dict(say="Here is the catch. Your deposit is not money the bank is holding for you. It is a promise the bank has made to you.",
                 shows=[S("bulb", "Here is the catch.", "", ["catch."], 130, text="!"),
                        S("bank", "Not money it is holding for you.", "Your deposit", ["holding"], 100, flip=True, label="BANK"),
                        S("speech", "A promise, not a pile.", "", ["promise,"], 110, text="We owe you")]),
            dict(say="Most of the time that doesn't matter, because people don't all want their money on the same day. When they do, it is called a run.",
                 shows=[S("calendar", "Not all on the same day.", "Most of the time", ["same"], 110, day="?", month="ANY DAY", note=""),
                        S("queue", "When they do: a run.", "", ["run."], 120, flip=True, n=8, label="BANK")]),
            dict(say="In March twenty twenty three it happened to Silicon Valley Bank. On March the ninth, it lost more than forty billion dollars of deposits in one day.",
                 shows=[S("calendar", "March 2023.", "Silicon Valley Bank", ["2023."], 120, day="9", month="MAR", note="2023"),
                        S("outflow", "More than $40 billion in a day.", "9 March 2023", ["$40"], 96, flip=True, label="$40bn+ OUT")]),
            dict(say="Its managers expected more than a hundred billion more to leave the next day. The Federal Reserve's review put the two together at roughly eighty five percent of the bank's deposits.",
                 shows=[dict(kind="number", value=100, pre="$", suf="bn+", label="expected to leave on 10 March (Federal Reserve review)"),
                        S("cake", "About 85% of its deposits.", "9 and 10 March together", ["85%"], 100, flip=True, slices=7, hi=0)]),
            dict(say="For comparison, the same review says Washington Mutual lost nineteen billion over sixteen days in two thousand and eight. Silicon Valley Bank failed on March the tenth.",
                 shows=[dict(kind="compare", left=("Washington Mutual, 2008", "$19bn / 16 days"), right=("SVB, 9 March 2023", "$40bn+ / 1 day"), note="Federal Reserve review, April 2023"),
                        S("stamp", "Failed on 10 March 2023.", "", ["Failed"], 110, flip=True, text="CLOSED")]),
            dict(say="Most of those deposits were above the insured limit. In America that limit is two hundred and fifty thousand dollars per depositor, per insured bank, for each kind of account. It exists because a deposit is a promise.",
                 shows=[S("tower", "Most were uninsured.", "Silicon Valley Bank", ["uninsured."], 110, crack=True, label="SVB"),
                        dict(kind="number", value=250000, pre="$", label="FDIC standard insurance, per depositor, per insured bank, per ownership category"),
                        S("document", "Insurance, because it's a promise.", "Why it exists", ["promise."], 100, flip=True, title="Deposit insurance", lines=4, stamp="INSURED")]),
        ]),
        dict(title="Money that can't be lent", art=("token", dict()), beats=[
            dict(say="Now the newest twist. In July twenty twenty five, America passed a law for stablecoins, digital tokens meant to be worth exactly one dollar.",
                 shows=[S("calendar", "A law for stablecoins.", "GENIUS Act", ["stablecoins."], 110, day="18", month="JUL", note="2025"),
                        S("token", "A token worth one dollar.", "", ["one", "dollar."], 100, flip=True)]),
            dict(say="The law chose the opposite of a bank. Every token has to be backed at least one for one by reserves like cash, insured deposits or very short Treasury bills.",
                 shows=[S("token", "Backed at least one for one.", "Reserves", ["one", "for", "one."], 100),
                        dict(kind="icons", title="What can back a token", items=[("coin", "Cash"), ("bank", "Insured deposits"), ("doc", "Treasury bills")], hi=2)]),
            dict(say="Issuers can't pay holders interest, and the law restricts them from lending the reserves on.",
                 shows=[S("token", "No interest, no lending the reserves.", "The rules", ["lending"], 96, flip=True, lock="NO LENDING")]),
            dict(say="So a stablecoin under this law cannot do what your bank does every day. It cannot create a new dollar by making a loan.",
                 shows=[S("bank", "It can't do what your bank does.", "", ["can't"], 100, label="BANK"),
                        dict(kind="split", left=("bank", "Your bank", "Lends, creates money"), right=("lock", "A stablecoin", "Backed, not lent"), mid="vs")]),
            dict(say="That is the trade, as we read it. A token built to be safe because nothing is lent on, and a bank deposit that can pay interest because something is.",
                 shows=[S("bulb", "That is the trade.", "Our reading", ["trade."], 120, text="="),
                        S("scale", "Safety against interest.", "", ["interest."], 110, flip=True, left="Safety", right="Interest", tip=0)]),
        ]),
        dict(title="What to take from it", art=("t_account", dict()), beats=[
            dict(say="So here is our reading. Money is mostly made of promises, and most of those promises are written when someone borrows.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 130, text="1"),
                        S("ledger", "Promises, written when someone borrows.", "", ["borrows."], 96, flip=True,
                          names=("Loan  +10,000", "Deposit  +10,000", "Loan  +2,000", "Deposit  +2,000"), hi=(1, 3))]),
            dict(say="In the United Kingdom, when the Bank of England wrote that paper, bank deposits made up ninety seven percent of broad money in circulation. Notes and coins were the rest.",
                 shows=[dict(kind="number", value=97, suf="%", label="of UK broad money held as bank deposits, December 2013 (Bank of England)"),
                        S("cake", "Notes and coins: the rest.", "", ["rest."], 110, flip=True, slices=12, hi=0)]),
            dict(say="Which means the real question about your savings is not where the bank keeps them. It is how good the bank's promise is, and who stands behind it.",
                 shows=[S("magnifier", "Not where the bank keeps it.", "", ["where"], 110, label="VAULT?"),
                        S("handshake", "How good is the promise?", "", ["promise?"], 100, flip=True, left="You", right="Bank")]),
            dict(say="And here is an interview question you can now answer. Do banks lend out their deposits? The short answer is no: loans create deposits.",
                 shows=[S("document", "An interview question.", "Interview prep", ["interview"], 110, title="Q: do banks lend deposits?", lines=4, stamp="?"),
                        dict(kind="quote", text="Do banks lend out their deposits?", hl=["deposits?"], who="A classic interview question", size=110),
                        dict(kind="verdict", text="Loans create deposits.", stamp="TRUE", size=120)]),
            dict(say="If they push further, add the limits: profit, the need for reserves to settle payments, capital rules, and interest rates. That is the full answer. This is education, not financial advice.",
                 shows=[dict(kind="icons", title="The limits", items=[("coin", "Profit"), ("bank", "Reserves"), ("doc", "Capital"), ("up", "Rates")], hi=3),
                        S("bulb", "That is the full answer.", "", ["full"], 110, text="2"),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. Knowing this, would you keep more than the insured amount in one bank? Tell us in the comments.",
                 shows=[S("magnifier", "Our question for you.", "", ["question"], 120, label="YOU?"),
                        S("tower", "More than the insured amount in one bank?", "Your turn", ["insured"], 92, flip=True, crack=False, label="BANK"),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "You were probably taught that your bank takes in savers' deposits and lends them out. We were too. In 2014 the Bank of England said that's a misconception, "
        "and in 2017 the Bundesbank agreed: when a bank makes a loan, it creates a matching deposit at the same moment, by an accounting entry. "
        "We walk through a £10,000 loan on the bank's books, show you why repaying it destroys money, and trace the idea back to the goldsmiths of 1600s London. "
        "Then the limits: profit, reserves to settle payments, capital rules and interest rates (the Fed set reserve requirements to 0% in March 2020). "
        "Why it matters to you: your deposit is a promise, which is how Silicon Valley Bank lost more than $40 billion in one day in 2023. It's also why the 2025 US stablecoin law "
        "wants tokens backed 1:1 and not lent on. We end with the answer you'd give in an interview: loans create deposits. "
        "Would you keep more than the insured amount in one bank?"),
    sources=[
        ("Bank of England Quarterly Bulletin 2014 Q1, Money creation in the modern economy (McLeay, Radia, Thomas)",
         "https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy"),
        ("Deutsche Bundesbank, How money is created (25 April 2017)", "https://bundesbank.de/en/tasks/topics/how-money-is-created-667392"),
        ("Federal Reserve Board, Reserve Requirements", "https://www.federalreserve.gov/monetarypolicy/reservereq.htm"),
        ("Bank of England Quarterly Bulletin 1969 Q2, The Bank of England note: a short history",
         "https://www.bankofengland.co.uk/quarterly-bulletin/1969/q2/the-bank-of-england-note---a-short-history"),
        ("Federal Reserve Board, Review of the supervision and regulation of Silicon Valley Bank, executive summary (April 2023)",
         "https://www.federalreserve.gov/publications/2023-April-SVB-Executive-Summary.htm"),
        ("FDIC, Deposits at a glance", "https://fdic.gov/resources/deposit-insurance/brochures/deposits-at-a-glance"),
        ("Fenwick on the GENIUS Act, the US stablecoin law (July 2025)",
         "https://www.fenwick.com/insights/publications/congress-enacts-comprehensive-stablecoin-legislation-key-provisions-and-implications-of-the-genius-act"),
        ("Federal Reserve Bank of St. Louis, Regulated Payment Stablecoins Become Reality in the U.S. (December 2025)",
         "https://www.stlouisfed.org/on-the-economy/2025/dec/regulated-payment-stablecoins-become-reality-us"),
    ],
    source_note="The £10,000 loan, the 100 / 90 / 81 textbook cascade and the 3 bars against 6 notes are our own examples, they aren't data. "
                "We drew the strongbox, notes, screen and token ourselves.",
    hashtags=["MoneyCreation", "Banking", "FinanceExplained"],
    tags=["how banks create money", "money creation", "where does money come from", "fractional reserve banking", "money multiplier",
          "Bank of England", "Bundesbank", "loans create deposits", "bank run", "Silicon Valley Bank", "deposit insurance",
          "stablecoins", "GENIUS Act", "finance explained", "investment banking interview"],
)

if __name__ == "__main__":
    make(EP)
