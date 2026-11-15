"""
YouTube #9 (15 Nov 2026): Charles Ponzi and the reply coupon. In 1920 Ponzi promised fifty percent profit in forty
five days, and the price gap he pointed to (an international reply coupon bought cheaply in Spain, swapped for a
five-cent US stamp) was real. Why could it never work? Financial history and scandals, made to
docs/production/long-form-standard.md (visual plan: build/plans/ep009.md). Score: suspense. Fourteen filmed beats:
seven from build/cine_1920.py (three new sets: a Boston street of 1920, a 1920 office with a counter, two post
offices with the sea between them) and seven filmed documents (cine_lib.document_shot, the 14 Nov next
improvement: a quote is read off a document on a desk instead of a text card).

Point of view: the coupon was not a lie; its size was. A real, checkable mechanism made an impossible promise sound
checkable, and almost nobody checked the size. Our reading, labelled as ours. Educational, not advice.

Every claim, sourced:
  [SCOTUS] Cunningham v. Brown, 265 U.S. 1 (1924), opinion of Chief Justice Taft (Cornell LII; syllabus on Justia):
      "In December, 1919, with a capital of $150, he began the business of borrowing money on his promissory notes";
      he "spread the false tale" (our narration: "a false tale") of buying international postal coupons abroad and selling them elsewhere "at 100 per
      cent. profit"; "By a written promise in 90 days to pay them $150 for every $100 loaned, he induced thousands to
      lend him"; he paid "his 90-day notes in full at the end of 45 days"; "Within eight months he took in
      $9,582,000, for which he issued his notes for $14,374,000"; agents' commission 10 per cent; "He was always
      insolvent, and became daily more so, the more his business succeeded"; "He made no investments of any kind";
      "By July 1st, Ponzi was taking in about $1,000,000 a week"; ceased selling notes on July 26th because of an
      investigation by public authority; the report caused a run on the Boston office; on August 2d a Boston
      newspaper declared him hopelessly insolvent; the run "was finally ended by an overdraft on August 9th";
      withdrawals 19 July to 10 August $6,692,000; the lenders repaid were "creditors equally with the others", the
      repayments preferences recoverable by the trustees; "it is a case the circumstances of which call strongly for
      the principle that equality is equity".
  [SMITH] Mary Darby, "In Ponzi We Trust", Smithsonian Magazine: the idea came "while opening his mail one day in
      August 1919" (a coupon from a Spanish correspondent); a reply coupon bought in a Spanish post office for 30
      centavos could be exchanged for a US stamp worth 5 cents, at a rate fixed by international treaty; because the
      peseta had fallen, about a 10 percent profit in theory; postal officials said "it was impossible for anyone to
      do what Ponzi claimed to be doing"; agents' 10 percent commissions; the Boston Post front page of 24 July 1920
      ("DOUBLES THE MONEY WITHIN THREE MONTHS"); the line from City Hall Annex to School Street on Monday 26 July;
      thousands rushed to redeem and "On one day, the Post reported, Ponzi paid out more than $1 million"; the Post's
      2 August report by his former publicity agent William McMasters, "hopelessly insolvent"; auditor Edwin Pride
      found him $3 million in the red, later $7 million; some 40,000 people; note holders received less than 30
      cents on the dollar; a final audit "turned up $61 worth of the coupons" (citing Donald Dunn); Ponzi to the New
      York Times: "I landed in this country with $2.50 in cash and $1 million in hopes".
  [MASS] Mass Moments (Mass Humanities), "Ponzi Scheme Begins to Unravel", July 24, 1920: a May 1920 flyer of the
      Securities Exchange Company, 27 School Street, advertised "fifty percent profit" payable "forty-five days from
      date of investment"; opened December 1919; the Post's series won its first Pulitzer Prize; deported to Italy;
      moved to Brazil in 1939 and died about a decade later in a charity ward.
  [NPM] Smithsonian National Postal Museum, "Ponzi Scheme" (Behind the Badge): the UPU created International Reply
      Coupons in 1906; post-war devaluation made exchange rates unstable; postal inspectors concluded worldwide IRC
      sales "were not nearly high enough"; Monday 26 July he met the authorities; Monday 9 August the bank
      commissioner told the Hanover Trust Company to stop honoring his checks; charged with using the mails in a
      scheme to defraud, pled guilty in November 1920, sentenced to five years; 1925 another seven to nine years;
      deported to Italy on 7 October 1934.
  [PULITZER] The Pulitzer Prizes, Boston Post, 1921 Public Service: "For its exposure of the operations of Charles
      Ponzi by a series of articles which finally led to his arrest."
  [UPU] Universal Postal Union press release, 2025: IRCs introduced 1 October 1907; on 17 September 2025 the 28th
      Congress (Dubai) decided to discontinue them as of 31 December 2026, after "almost 120 years".
  [SEC] Investor.gov (US SEC), "Ponzi Scheme": "A Ponzi scheme is an investment fraud that pays existing investors
      with funds collected from new investors"; named after Charles Ponzi; red flags including "High returns with
      little or no risk", "Overly consistent returns", "Secretive, complex strategies", "Difficulty receiving
      payments".
  [DOJ] US Department of Justice, 30 Dec 2024: the Madoff Victim Fund has paid over $4.3 billion to 40,930 victims in
      127 countries (93.71% of their fraud losses); Madoff ran the scheme "for decades", pleaded guilty to 11 federal
      felonies on 12 March 2009 and was sentenced to 150 years on 29 June 2009.
Kept apart: the flyer's words and the headline are quoted as the sources quote them; the reconstruction scenes are
illustrations; the $100 rolled over for eight rounds and the coupon count are our own calculations; the closing
reading is ours. Ponzi's later claims about himself are not used as facts.
Calculations (checked with a script, build/plans/ep009_checks.py): 14,374,000 - 9,582,000 = 4,792,000;
4,792,000 / 0.05 = 95,840,000 coupons; 9,582,000 x 1.5 = 14,373,000 (the notes are 1.5 times the money);
100 x 1.5^8 = 2,562.89 after 8 rounds of 45 days = 360 days; 1 Oct 1907 to 31 Dec 2026 is 119 years.

    python build/youtube_ep009.py
"""

import cine_1920 as F
from cine_lib import document_shot
from youtube import make

S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)
CINE = lambda name: dict(kind="cine", shot=F.SHOTS[name])
DOC = lambda **kw: dict(kind="cine", shot=document_shot(**kw))

OPINION = dict(style="opinion", head="SUPREME COURT OF THE UNITED STATES", sub="CUNNINGHAM v. BROWN, 265 U.S. 1 (1924)",
               source="Opinion of the Court, Chief Justice Taft", badge_text="Quoted from the opinion")

EP = dict(
    slug="yt-009-ponzi-coupon",
    title="Ponzi's Scheme Started With a Real Trade. Here's Why It Could Never Work.",
    score="suspense",
    thumb=dict(film_a=dict(shot=F.SHOTS["street_queue"], dur=9.0, t=6.5, pos="45% 60%",
                           segs=[("In the summer of 1920, crowds filled School Street.", .3, 4.0), ("The line stretched all the way to his door.", 4.2, 8.6)]),
               film_b=dict(shot=F.SHOTS["coupon_trade"], dur=13.0, t=12.2, pos="70% 50%",
                           segs=[("Here's the trade.", .3, 1.2), ("In Spain, a coupon cost thirty centavos.", 1.4, 3.8),
                                 ("Taken to America, it could be swapped for a U.S. stamp worth five cents.", 4.0, 8.0),
                                 ("And because the peseta had fallen, thirty centavos cost less than five cents in dollars.", 8.2, 12.6)]),
               big_a="50% in 45 days. The trade was <span style='color:#0A0A0A'>real</span>.", size_a=84,
               big="A 5¢ stamp. <span style='color:#D93A12'>96 million</span> of them.", size=80,
               small="Ponzi, 1920"),
    chapters=[
        dict(title="A line on School Street", art=("queue", dict(n=6, label="$")), beats=[
            dict(say="In the summer of nineteen twenty, crowds filled School Street in Boston, outside the office of a man named Charles Ponzi. On Monday, July the twenty sixth, the line stretched all the way from City Hall Annex to his door.",
                 show=CINE("street_queue")),
            dict(say="His company's flyer promised fifty percent profit, payable forty five days from the date of investment. And here's the strange part. The price gap he said he was trading was real.",
                 show=DOC(style="flyer", head="THE SECURITIES EXCHANGE COMPANY", sub="27 SCHOOL STREET, BOSTON · MAY 1920",
                          quote="“fifty percent profit” ... “forty-five days from date of investment”", hl=("fifty percent profit", "forty-five days"),
                          start=(0, "fifty"), end=0, source="Wording as quoted by Mass Moments (Mass Humanities)", wrap=34,
                          badge_text="Reconstruction · wording as quoted", seed=2)),
            dict(say="So why could it never work? Not just because he lied, though he did. Because of a five cent stamp, and a piece of arithmetic anyone could have done.",
                 shows=[SC("magnifier", "Why could it never work?", label="50%?"),
                        S("speech", "Not just the lies.", "", ["lies."], 110, flip=True, text="Trust me"),
                        SC("pricetag", "A five cent stamp, and some arithmetic", value="5¢", tag="STAMP")]),
        ]),
        dict(title="A coupon from Spain", art=("letter", dict(date="1919", sign="", hi_line=1)), beats=[
            dict(say="Ponzi was an Italian immigrant who later said he had landed in America with two dollars and fifty cents. In August nineteen nineteen, opening his mail, he found an international reply coupon, sent by a correspondent in Spain.",
                 show=CINE("mail_coupon")),
            dict(say="Reply coupons were a postal invention. The Universal Postal Union agreed on them in nineteen oh six, so that a letter writer could pay for the answer from abroad.",
                 shows=[S("globe", "A postal invention.", "Universal Postal Union", ["postal"], 110),
                        dict(kind="flow", items=[("coin", "Buy a coupon at home"), ("pen", "Send it with a letter"), ("coin", "The reply is paid for")])]),
            dict(say="You bought a coupon at your post office and sent it with your letter. The person who got it swapped it at their own post office for a stamp, at a rate fixed by international treaty.",
                 shows=[S("parcel", "Buy it, post it.", "", ["post"], 110, label="REPLY", n=2),
                        S("handshake", "Swapped for a stamp abroad.", "At a rate fixed by treaty", ["stamp"], 100, flip=True, left="Coupon", right="Stamp")]),
            dict(say="After the First World War, exchange rates across Europe were unstable, and the peseta had fallen against the dollar. The coupon's treaty rate didn't follow the market.",
                 shows=[SC("chart", "The peseta fell against the dollar (our sketch, no data)", values=(8, 7, 7, 6, 5, 5, 4), color="#D93A12", arrow=False),
                        S("seesaw", "The coupon's rate stayed put.", "", ["stayed"], 100, flip=True, left="Market", right="Treaty", tip=0)]),
        ]),
        dict(title="The real trade", art=("pricetag", dict(value="5¢", tag="STAMP")), beats=[
            dict(say="Here's the trade. In Spain, a coupon cost thirty centavos. Taken to America, it could be swapped for a U.S. stamp worth five cents. And because the peseta had fallen, thirty centavos cost less than five cents in dollars.",
                 show=CINE("coupon_trade")),
            dict(say="Smithsonian Magazine puts the profit, in theory, at about ten percent, not fifty. And notice what you're left holding at the end. Stamps, not dollars.",
                 shows=[dict(kind="compare", left=("The coupon trade, in theory", "about 10%"), right=("Ponzi's promise, in 45 days", "50%"), note="Smithsonian Magazine; the flyer, via Mass Moments"),
                        SC("magnifier", "What are you left holding?", label="?"),
                        S("pricetag", "Stamps, not dollars.", "", ["Stamps,"], 110, value="5¢", tag="NOT $")]),
            dict(say="To turn stamps back into cash, you'd have to find buyers for them. And at the time, postal officials said it was impossible to do what Ponzi claimed he was doing.",
                 shows=[S("shopfront", "Then find buyers for the stamps.", "", ["buyers"], 100, label="STAMPS"),
                        S("stamp", "Impossible, said the postal officials.", "Smithsonian Magazine", ["Impossible,"], 100, flip=True, text="IMPOSSIBLE")]),
            dict(say="The Supreme Court later called his story a false tale. He claimed to be buying the coupons abroad and selling them in other countries at a hundred percent profit.",
                 shows=[S("scroll", "A false tale, said the Court.", "Cunningham v. Brown, 1924", ["false"], 100, title="FALSE TALE", seal="1924"),
                        S("pricetag", "A hundred percent profit, he claimed.", "", ["hundred"], 96, flip=True, value="100%", tag="CLAIMED")]),
        ]),
        dict(title="Fifty percent in forty five days", art=("calendar", dict(day="45", month="DAYS", note="+50%")), beats=[
            dict(say="The Supreme Court later described how it started. In its words: in December, nineteen nineteen, with a capital of one hundred and fifty dollars, he began the business of borrowing money on his promissory notes.",
                 show=DOC(**OPINION, quote="In December, 1919, with a capital of $150, he began the business of borrowing money on his promissory notes.",
                          hl=("$150", "promissory notes"), start=(1, "december"), seed=3)),
            dict(say="Each note promised a hundred and fifty dollars in ninety days for every hundred dollars lent. In practice, he paid them in full after forty five days.",
                 shows=[S("document", "$150 back for every $100.", "Ninety-day notes", ["$150"], 100, title="NOTE", lines=3, stamp="$150"),
                        S("calendar", "Paid in forty five days.", "Supreme Court opinion", ["forty", "five"], 100, flip=True, day="45", month="DAYS", note="1920")]),
            dict(say="Agents sold the notes for a ten percent commission, and the first lenders were paid, so word spread. By the summer, the money was pouring in. By July the first, nineteen twenty, Ponzi was taking in about a million dollars a week.",
                 show=CINE("office_cash")),
            dict(say="In about eight months he took in nine point six million dollars, and wrote notes promising fourteen point four million back. Tens of thousands of people had lent to him.",
                 shows=[dict(kind="compare", left=("Taken in, about 8 months", "$9,582,000"), right=("Promised back in notes", "$14,374,000"), note="Supreme Court, Cunningham v. Brown (1924)"),
                        S("figures", "Tens of thousands of lenders.", "Smithsonian: some 40,000", ["thousands"], 100, flip=True, n=6, hi=0)]),
        ]),
        dict(title="Where the money went", art=("coins", dict(stacks=[2, 4, 6])), beats=[
            dict(say="So what was he doing with it? The Court found that he made no investments of any kind. Money from new lenders paid the earlier ones.",
                 show=CINE("jars")),
            dict(say="That works for as long as more money comes in than goes out. And every forty five days, what he owes grows by half.",
                 shows=[S("seesaw", "More in than out.", "", ["in"], 110, left="In", right="Out", tip=0),
                        S("interest_stack", "Every 45 days, half as much again.", "", ["half"], 96, flip=True, base="$100", rate="50%")]),
            dict(say="Take an example of our own. Lend him a hundred dollars and keep rolling it over. After eight rounds of forty five days, about a year, he owes you about two thousand five hundred and sixty three dollars.",
                 shows=[S("bulb", "Our example.", "", ["example."], 120, text="$100"),
                        S("interest_stack", "Keep rolling it over.", "", ["rolling"], 100, flip=True, base="$100", rate="+50%"),
                        SC("bars", "Our example: $100 at +50% every 45 days, about $2,563 after 360 days",
                           values=[100, 225, 506, 1139, 2563], labels=["START", "90 DAYS", "180 DAYS", "270 DAYS", "360: $2,563"], hi=4)]),
            dict(say="The Court put it in a single line. He was always insolvent, and became daily more so, the more his business succeeded.",
                 show=DOC(**OPINION, quote="He was always insolvent, and became daily more so, the more his business succeeded.",
                          hl=("always insolvent", "more his business succeeded"), start=(1, None), seed=4)),
        ]),
        dict(title="Ninety six million coupons", art=("pricetag", dict(value="96m", tag="COUPONS")), beats=[
            dict(say="Now test the real trade against the promise. To pay what his notes promised, Ponzi needed about four point eight million dollars more than he had taken in.",
                 shows=[S("scale", "Test the trade against the promise.", "", ["promise."], 100, left="Trade", right="Promise", tip=1),
                        dict(kind="compare", left=("Promised back", "$14,374,000"), right=("Taken in", "$9,582,000"), note="Gap $4,792,000: Supreme Court figures, our subtraction")]),
            dict(say="Suppose every coupon cost him nothing at all. Each one still turns into a five cent stamp at most, so he'd need at least ninety six million coupons, and then he'd have to sell ninety six million stamps for cash.",
                 show=CINE("coupon_pile")),
            dict(say="Postal inspectors came at it from the other side. Worldwide sales of reply coupons weren't nearly high enough to produce what he claimed.",
                 shows=[S("magnifier", "Postal inspectors checked.", "", ["inspectors"], 110, label="IRC"),
                        S("globe", "Not nearly enough coupons sold.", "Smithsonian National Postal Museum", ["enough"], 100, flip=True)]),
            dict(say="And when it was all over, a final audit of his company turned up sixty one dollars' worth of coupons.",
                 shows=[S("receipt", "$61 worth of coupons.", "Final audit, via Smithsonian Magazine", ["$61"], 110, total="$61", circle=0)]),
        ]),
        dict(title="The run on School Street", art=("crowd_rush", dict(n=7, target="SCHOOL ST.")), beats=[
            dict(say="The end came quickly. On Saturday, July the twenty fourth, the Boston Post ran a front page story on him under this headline. Doubles the money within three months.",
                 show=DOC(style="newspaper", head="THE BOSTON POST", sub="BOSTON · SATURDAY, JULY 24, 1920", quote="DOUBLES THE MONEY WITHIN THREE MONTHS",
                          hl=("DOUBLES THE MONEY",), start=(2, None), wrap=22, size=78, before=1, after=5,
                          source="Front page headline, as quoted by Smithsonian Magazine", badge_text="Reconstruction · headline as reported", seed=5)),
            dict(say="Two days later, with officials investigating, he stopped taking new money. Thousands rushed to his office to get theirs back, and he paid. The Post reported that on one day he paid out more than a million dollars.",
                 show=CINE("run")),
            dict(say="Paying calmed people, for a while. From July the nineteenth to August the tenth, withdrawals came to six point seven million dollars.",
                 shows=[S("outflow", "Paying calmed people, for a while.", "", ["calmed"], 100, label="PAID OUT"),
                        S("calendar", "$6,692,000 withdrawn.", "19 July to 10 August 1920, Supreme Court", ["$6,692,000"], 100, flip=True, day="10", month="AUG", note="1920")]),
            dict(say="On August the second, the Post printed a report by his former publicity agent, calling him hopelessly insolvent. On August the ninth, the state's bank commissioner told his bank to stop honouring his checks. The run was over.",
                 shows=[S("newspaper", "Hopelessly insolvent.", "Boston Post, 2 August 1920", ["insolvent."], 100, headline="HOPELESSLY INSOLVENT", sub="", date="2 AUG 1920", masthead="THE BOSTON POST"),
                        S("bank_closed", "His bank stopped paying his checks.", "9 August 1920", ["stopped"], 96, flip=True),
                        SC("stamp", "The run was over", text="OVER")]),
        ]),
        dict(title="After the fall", art=("scroll", dict(title="CUNNINGHAM v. BROWN", seal="1924")), beats=[
            dict(say="A government auditor found him millions of dollars in the red. Ponzi was charged with using the mails to defraud. In November nineteen twenty he pleaded guilty, and was sentenced to five years in prison.",
                 shows=[S("empty_pockets", "Millions in the red.", "Government audit, 1920", ["red."], 100, label="ASSETS"),
                        S("parcel", "Charged: using the mails to defraud.", "", ["mails"], 96, flip=True, label="MAIL", n=3),
                        S("calendar", "Guilty plea, November 1920.", "Five years in prison", ["Guilty"], 100, day="5", month="YEARS", note="1920")]),
            dict(say="The newspaper that brought him down won a Pulitzer Prize. The citation reads: for its exposure of the operations of Charles Ponzi by a series of articles which finally led to his arrest.",
                 show=DOC(style="notice", head="THE PULITZER PRIZES", sub="1921 · PUBLIC SERVICE · BOSTON POST",
                          quote="For its exposure of the operations of Charles Ponzi by a series of articles which finally led to his arrest.",
                          hl=("exposure", "led to his arrest"), start=(1, "for its"), source="Prize citation, pulitzer.org",
                          badge_text="Quoted from the citation", seed=8)),
            dict(say="Note holders got back less than thirty cents on the dollar. Later he was convicted on state charges too, and in nineteen thirty four he was deported to Italy. He died poor, in a charity ward in Brazil.",
                 shows=[S("pricetag", "Under 30 cents on the dollar.", "Smithsonian Magazine", ["30"], 100, value="<30¢", tag="PER $1"),
                        SC("ship", "Deported to Italy, 1934"),
                        S("hospital", "Died poor, in Brazil.", "In a charity ward", ["poor,"], 100)]),
            dict(say="One question was left for the courts. Lenders paid in the final weeks had been paid with other lenders' money. Should they keep it? In nineteen twenty four, the Supreme Court said no. In its words, it is a case the circumstances of which call strongly for the principle that equality is equity.",
                 show=DOC(**OPINION, quote="It is a case the circumstances of which call strongly for the principle that equality is equity.",
                          hl=("equality is equity",), start=(4, "it is"), wrap=40, seed=6)),
        ]),
        dict(title="A hundred years later", art=("rocket", dict()), beats=[
            dict(say="Today the SEC defines the fraud that carries his name in one sentence. In its words, a Ponzi scheme is an investment fraud that pays existing investors with funds collected from new investors.",
                 show=DOC(style="notice", head="INVESTOR.GOV · U.S. SECURITIES AND EXCHANGE COMMISSION", sub="TYPES OF FRAUD · PONZI SCHEME",
                          quote="A Ponzi scheme is an investment fraud that pays existing investors with funds collected from new investors.",
                          hl=("pays existing investors", "from new investors"), start=(1, "a ponzi"), source="Investor.gov, accessed 15 November 2026",
                          badge_text="Quoted from Investor.gov", seed=7)),
            dict(say="Its warning signs read like a description of nineteen twenty. High returns with little or no risk. Overly consistent returns. Secretive, complex strategies. And trouble getting your money out.",
                 shows=[S("calendar", "Like 1920.", "SEC red flags", ["1920."], 120, day="24", month="JUL", note="1920"),
                        SC("rocket", "High returns with little or no risk"),
                        SC("chart", "Overly consistent returns (our sketch, no data)", values=(2, 3, 4, 5, 6, 7, 8), color="#0F766E", arrow=True),
                        S("document", "Secretive, complex strategies.", "", ["Secretive,"], 96, flip=True, title="STRATEGY", lines=4, stamp="SECRET"),
                        SC("bank_closed", "Trouble getting your money out")]),
            dict(say="Bernard Madoff ran one for decades. He pleaded guilty in March two thousand nine, and was sentenced to a hundred and fifty years in prison.",
                 shows=[S("ledger", "Madoff ran one for decades.", "US Justice Department", ["decades."], 100, names=("Founded 1960", "For decades", "Guilty, 2009", "150 years"), hi=(1,)),
                        S("calendar", "Guilty, March 2009. 150 years.", "Justice Department", ["150"], 100, flip=True, day="12", month="MAR", note="2009")]),
            dict(say="By the end of twenty twenty four, the Justice Department's victim fund had paid out more than four point three billion dollars, to more than forty thousand victims in a hundred and twenty seven countries.",
                 shows=[dict(kind="compare", left=("Paid to victims by December 2024", "$4.3bn+"), right=("Victims, in 127 countries", "40,930"),
                             note="US Department of Justice, 30 December 2024")]),
        ]),
        dict(title="The coupon test", art=("magnifier", dict(label="50%?")), beats=[
            dict(say="Here's our reading. The coupon mattered because it was real. A true story about a small, odd price gap made an enormous promise sound checkable. And almost nobody checked the size.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 130, text="1"),
                        S("pricetag", "The coupon was real.", "Our reading", ["real."], 100, flip=True, value="5¢", tag="REAL"),
                        S("magnifier", "A small gap, a huge promise.", "Our reading", ["huge"], 96, label="10% vs 50%"),
                        SC("tower", "Nobody checked the size", floors=7, crack=True, label="$")]),
            dict(say="And the reply coupon itself? The Universal Postal Union has decided to retire it. After almost a hundred and twenty years, it's discontinued at the end of twenty twenty six, a few weeks from now.",
                 shows=[SC("letter", "And the coupon itself?", date="1907", sign="", hi_line=1),
                        S("globe", "Retired by the Postal Union.", "Decided 17 September 2025", ["Retired"], 100, flip=True),
                        S("calendar", "Gone after 31 December 2026.", "After almost 120 years", ["2026."], 100, day="31", month="DEC", note="2026")]),
            dict(say="If an interviewer asks how you'd test a return that looks too good, use Ponzi's coupon. Find the real mechanism, then ask how big it can get. This is education, not financial advice.",
                 shows=[S("document", "Testing a too good return.", "Interview prep", ["test"], 100, title="Q: 50% in 45 days?", lines=3, stamp="TEST"),
                        dict(kind="list", title="The coupon test", items=["Find the real mechanism", "Ask how big it can get", "Compare it with the promise"]),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. What's the best return you've ever been promised that came with a story that sounded real? Tell us in the comments.",
                 shows=[SC("magnifier", "Our question for you", label="YOU?"),
                        S("pricetag", "The best return you were ever promised?", "Your turn", ["promised?"], 92, flip=True, value="50%", tag="REAL?"),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "Boston, summer 1920. A line of people stretches from City Hall Annex to an office on School Street, where Charles Ponzi is promising "
        "50% profit in 45 days. The odd part is that the trade he pointed to was real: a postal reply coupon bought for 30 centavos in Spain "
        "could be swapped for a 5 cent stamp in the US.\n\n"
        "So why could it never work? We follow the coupon from Spain to Boston, read what the Supreme Court found in Cunningham v. Brown "
        "($9,582,000 taken in, $14,374,000 promised back, no investments of any kind), and do the arithmetic he hoped nobody would do: even with "
        "free coupons he'd have needed at least 96 million of them. Then the Boston Post headline, the run, and the 1924 ruling that people paid in the "
        "final weeks had to share with everyone else.\n\n"
        "We finish with the SEC's definition, Madoff, and a simple test for any return that sounds too good. What's the best return you've ever "
        "been promised that came with a story that sounded real? Tell us below."),
    sources=[
        ("Cunningham v. Brown, 265 U.S. 1 (1924), opinion of the Court (Cornell LII)", "https://www.law.cornell.edu/supremecourt/text/265/1"),
        ("Cunningham v. Brown, 265 U.S. 1 (1924), syllabus (Justia)", "https://supreme.justia.com/cases/federal/us/265/1/"),
        ("Mary Darby, In Ponzi We Trust, Smithsonian Magazine", "https://www.smithsonianmag.com/history/in-ponzi-we-trust-64016168/"),
        ("Mass Moments, Mass Humanities: Ponzi Scheme Begins to Unravel (July 24, 1920)", "https://www.massmoments.org/moment-details/ponzi-scheme-begins-to-unravel.html"),
        ("Smithsonian National Postal Museum, Behind the Badge: Ponzi Scheme", "https://postalmuseum.si.edu/exhibition/behind-the-badge-case-histories-scams-and-schemes/ponzi-scheme"),
        ("The Pulitzer Prizes, Boston Post, 1921 Public Service", "https://www.pulitzer.org/winners/boston-post"),
        ("Universal Postal Union, End of a chapter, start of a legacy: the international reply coupon enters the history books (2025)", "https://www.upu.int/en/press-release/2025/end-of-a-chapter-start-of-a-legacy-the-international-reply-coupon-enters-the-history-books"),
        ("Investor.gov, US Securities and Exchange Commission, Ponzi Scheme", "https://www.investor.gov/protect-your-investments/fraud/types-fraud/ponzi-scheme"),
        ("US Department of Justice, Justice Department's 10th distribution brings total provided over $4.3B (30 Dec 2024)", "https://www.justice.gov/archives/opa/pr/justice-departments-10th-distribution-brings-total-provided-over-43b-nearly-full-recovery"),
    ],
    source_note="We drew the filmed scenes ourselves. They're stylised reconstructions, not portraits, and nobody in them speaks. The coupon "
                "and the stamp are our own designs, not the real ones. The $100 example and the 96 million coupons are our own calculations "
                "from the Supreme Court's figures, and the reading in the last chapter is ours, so you're welcome to disagree with it.",
    hashtags=["Ponzi", "FinanceHistory", "Fraud"],
    tags=["Charles Ponzi", "Ponzi scheme", "original Ponzi scheme", "international reply coupon", "how a Ponzi scheme works", "Boston 1920",
          "Cunningham v. Brown", "Bernie Madoff", "investment fraud red flags", "too good to be true returns", "financial history", "scandals",
          "investment banking interview"],
)

if __name__ == "__main__":
    make(EP)
