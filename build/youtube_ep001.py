"""
YouTube #1: tulip mania, the most famous bubble in finance, and why most of
the story is not true. History of finance.

Every claim, sourced (Smithsonian Magazine, "There Never Was a Real Tulip
Fever", Sept 2017, on Anne Goldgar's archive research):
  - the craze is dated to the 1630s; trading peaked in late 1636 and the
    market collapsed by February 1637;
  - the popular version comes from Charles Mackay's book Extraordinary
    Popular Delusions and the Madness of Crowds (1841);
  - the sailor who ate a bulb, and a bulb worth more than a mansion, are
    legends;
  - Goldgar (King's College London) found few people involved, minor
    economic effects, and "I couldn't find anybody that went bankrupt";
  - the real damage: buyers refused to pay agreed prices and courts would
    not enforce the contracts, so trust broke, not the economy;
  - the prized striped "broken" tulips were later linked to a virus;
  - many of the wild stories came from moralising pamphlets of the time;
  - economist Peter Garber argued the speculation "was not obvious madness".
No prices, no counts: none are given, so none are said.

    python build/youtube_ep001.py
"""

from youtube import make

EP = dict(
    slug="yt-001-tulip-mania",
    title="Tulip Mania: The Famous Bubble That Mostly Never Happened",
    thumb=dict(art=("tulip", dict(n=1, broken=False)), big_a="The bubble that <span style='color:#0A0A0A'>never</span> burst", big="The bubble that <span style='color:#D93A12'>never</span> burst", small="Tulip mania, 1637", ghost="1637"),
    chapters=[
        dict(title="The story everyone tells", art=("tulip", dict(n=1)), beats=[
            dict(say="In the sixteen thirties, the Dutch went mad for tulips.",
                 show=dict(kind="sketch", art="tulip", opts=dict(n=3), label="The Dutch Republic, 1630s", text="The Dutch went mad for tulips.", hl=["tulips."], size=100)),
            dict(say="Or so the story goes. Chimney sweeps and rich merchants, all trading bulbs. A single flower worth more than a house. Then, in February sixteen thirty seven, it all collapsed.",
                 shows=[dict(kind="verdict", text="The legend.", stamp="LEGEND", size=150),
                        dict(kind="sketch", art="figures", opts=dict(n=5, hi=4), label="Who was trading", text="Chimney sweeps and rich merchants.", hl=["merchants."], size=88),
                        dict(kind="sketch", art="house", opts=dict(price="= 1 bulb"), label="The famous price", text="A single flower worth more than a house.", hl=["house."], size=88),
                        dict(kind="sketch", art="chart", opts=dict(values=[1, 2, 3, 5, 8, 9, 3, 1], label="1637"), label="The crash", text="February 1637. It all collapsed.", hl=["collapsed."], size=92)]),
            dict(say="It's the first bubble every finance student learns about. And most of it isn't true.",
                 shows=[dict(kind="sketch", art="book", opts=dict(title="Bubbles, chapter 1"), label="Lesson one", text="The first bubble every finance student learns.", hl=["first", "bubble"], size=84),
                        dict(kind="verdict", text="Most of it isn't true.", stamp="MYTH", size=120)]),
        ]),
        dict(title="Where the story came from", art=("book", dict(title="1841")), beats=[
            dict(say="The version you know was made popular by a Scottish journalist, Charles Mackay, in eighteen forty one.",
                 show=dict(kind="timeline", title="Two centuries later", items=[("1637", "The crash"), ("1841", "Mackay's book")], hi=1)),
            dict(say="He leaned on pamphlets written at the time. Moral warnings about greed, not market reports.",
                 shows=[dict(kind="sketch", art="document", opts=dict(title="Pamphlet, 1637", lines=6), label="His sources", text="Pamphlets written at the time.", hl=["pamphlets"], size=96),
                        dict(kind="split", left=("pen", "Written as", "A sermon"), right=("down", "Read as", "Market data"), mid="\u2260")]),
            dict(say="That's where the best stories come from. The sailor who ate a priceless bulb, thinking it was an onion. Legend.",
                 shows=[dict(kind="sketch", art="magnifier", opts=dict(label="?"), label="Look closer", text="Where the best stories come from.", size=90),
                        dict(kind="sketch", art="ship", label="The famous one", text="The sailor who ate a priceless bulb.", hl=["ate"], size=92),
                        dict(kind="sketch", art="document", opts=dict(title="The sailor story", lines=4, stamp="LEGEND"), text="Legend.", hl=["Legend."], size=150)]),
        ]),
        dict(title="What the archives say", art=("magnifier", dict(label="1637")), beats=[
            dict(say="The historian Anne Goldgar went back to the Dutch archives. She found far fewer people involved than the legend says.",
                 shows=[dict(kind="sketch", art="figures", opts=dict(n=3, glass=True), label="Anne Goldgar, historian", text="Back to the Dutch archives.", hl=["archives."], size=100),
                        dict(kind="split", left=("people", "The legend", "Everyone"), right=("person", "The archives", "Far fewer"))]),
            dict(say="And the ruin? In her words: I couldn't find anybody that went bankrupt.",
                 shows=[dict(kind="sketch", art="dominoes", opts=dict(labels=["Bulbs", "Traders", "Banks", "Economy"], fall=0), label="The ruin", text="And the ruin?", size=130),
                        dict(kind="quote", text="I couldn't find anybody that went bankrupt.", hl=["bankrupt."], who="Anne Goldgar")]),
            dict(say="What actually broke was trust. Buyers refused to pay the prices they had agreed, and the courts would not enforce the contracts.",
                 shows=[dict(kind="sketch", art="document", opts=dict(title="Contract", lines=5, stamp="UNPAID"), label="What broke", text="Trust.", hl=["Trust."], size=200),
                        dict(kind="flow", items=[("doc", "Price agreed"), ("cross", "Buyer won't pay"), ("gavel", "Courts stay out")])]),
        ]),
        dict(title="The lesson for today", art=("bulb", dict(text="Trust")), beats=[
            dict(say="The economist Peter Garber went further. He argued the bulb trade was not obvious madness at all.",
                 shows=[dict(kind="sketch", art="book", opts=dict(title="Famous First Bubbles"), label="An economist's view", text="Peter Garber went further.", size=100),
                        dict(kind="verdict", text="Obvious madness?", stamp="NO", size=140)]),
            dict(say="So the real lesson is not that crowds go crazy. It's that a market runs on contracts people trust. When nobody has to pay, prices stop meaning anything.",
                 shows=[dict(kind="verdict", text="Crowds go crazy.", stamp="NOT IT", size=140),
                        dict(kind="flow", items=[("doc", "Contracts"), ("hand", "Trust"), ("scales", "A market")]),
                        dict(kind="sketch", art="scale", opts=dict(left="Price", right="Payment", tip=1), label="Without it", text="Prices stop meaning anything.", hl=["anything."], size=96)]),
            dict(say="Next time someone calls something tulip mania, ask them. Who went bankrupt? Follow for more stories finance gets wrong.",
                 shows=[dict(kind="sketch", art="speech", opts=dict(text="It's just like tulip mania!"), label="Next time you hear it", text="Tulip mania?", hl=["mania?"], size=150),
                        dict(kind="icon", icon="question", label="Ask one question", text="Who went bankrupt?", hl=["bankrupt?"], size=130),
                        dict(kind="icon", icon="bank", label="More soon", text="Stories finance gets wrong.", hl=["wrong."], size=100)]),
        ]),
    ],
    description=(
        "Tulip mania is the first bubble every finance student hears about: everyone trading bulbs, one flower worth a house, "
        "then a crash in February 1637. Historians who went back to the Dutch archives found a very different story.\n\n"
        "Sources: Anne Goldgar, Tulipmania: Money, Honor, and Knowledge in the Dutch Golden Age; "
        "Smithsonian Magazine, \"There Never Was a Real Tulip Fever\"; Peter Garber, Famous First Bubbles; "
        "Charles Mackay, Extraordinary Popular Delusions and the Madness of Crowds (1841)."),
    tags=["tulip mania", "history of finance", "financial bubbles", "Dutch Golden Age", "economics", "investing history",
          "Charles Mackay", "Anne Goldgar", "finance explained"],
)

if __name__ == "__main__":
    make(EP)
