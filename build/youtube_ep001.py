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
    thumb=dict(big="The bubble that <span style='color:#D93A12'>never</span> burst", small="Tulip mania, 1637", ghost="1637"),
    chapters=[
        dict(title="The story everyone tells", beats=[
            dict(say="In the sixteen thirties, the Dutch went mad for tulips.",
                 show=dict(kind="statement", text="The Dutch went mad for tulips.", hl=["tulips."])),
            dict(say="Or so the story goes. Chimney sweeps and rich merchants, all trading bulbs. A single flower worth more than a house. Then, in February sixteen thirty seven, it all collapsed.",
                 show=dict(kind="list", title="The legend", items=["Everyone trading bulbs", "One bulb worth a house", "Collapse in February 1637"])),
            dict(say="It's the first bubble every finance student learns about. And most of it isn't true.",
                 show=dict(kind="statement", text="Most of it isn't true.", hl=["isn't", "true."])),
        ]),
        dict(title="Where the story came from", beats=[
            dict(say="The version you know was made popular by a Scottish journalist, Charles Mackay, in eighteen forty one.",
                 show=dict(kind="term", term="1841", text="Charles Mackay, Extraordinary Popular Delusions and the Madness of Crowds")),
            dict(say="He leaned on pamphlets written at the time. Moral warnings about greed, not market reports.",
                 show=dict(kind="compare", left=("Written as", "Sermon"), right=("Read as", "Data"), note="The sources were moral pamphlets.")),
            dict(say="That's where the best stories come from. The sailor who ate a priceless bulb, thinking it was an onion. Legend.",
                 show=dict(kind="statement", text="The sailor who ate the bulb? Legend.", hl=["Legend."])),
        ]),
        dict(title="What the archives say", beats=[
            dict(say="The historian Anne Goldgar went back to the Dutch archives. She found far fewer people involved than the legend says.",
                 show=dict(kind="statement", text="Far fewer people than the legend says.", hl=["fewer"])),
            dict(say="And the ruin? In her words: I couldn't find anybody that went bankrupt.",
                 show=dict(kind="statement", text="“I couldn't find anybody that went bankrupt.”", hl=["bankrupt.”"], size=76)),
            dict(say="What actually broke was trust. Buyers refused to pay the prices they had agreed, and the courts would not enforce the contracts.",
                 show=dict(kind="list", title="What broke", items=["Buyers walked away", "Courts stayed out", "Trust, not the economy"])),
        ]),
        dict(title="The lesson for today", beats=[
            dict(say="The economist Peter Garber went further. He argued the bulb trade was not obvious madness at all.",
                 show=dict(kind="term", term="Not madness", text="Peter Garber, on the bulb trade")),
            dict(say="So the real lesson is not that crowds go crazy. It's that a market runs on contracts people trust. When nobody has to pay, prices stop meaning anything.",
                 show=dict(kind="statement", text="A market runs on contracts people trust.", hl=["trust."])),
            dict(say="Next time someone calls something tulip mania, ask them. Who went bankrupt? Follow for more stories finance gets wrong.",
                 show=dict(kind="statement", text="Who went bankrupt?", hl=["bankrupt?"])),
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
