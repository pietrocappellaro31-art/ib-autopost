"""
YouTube #16 (23 Nov 2026): Enron, 1999 to 2001. In October 2000 a committee of Enron's board was shown a chart:
$27 billion of the company's $60 billion in assets, almost half, was held off its books. Fourteen months later Enron
was bankrupt. Why didn't the people paid to watch it stop it? Scandals, accounting (mark to market, special purpose
entities, the 3% rule, hedging with your own shares), corporate governance, auditor independence. Made to
docs/production/long-form-standard.md, the 18 Nov decision (open on the hook, the number on screen in the first
frame; title and thumbnail on the same number) and the 22 Nov decision (at least 1% better than the previous film,
measured). Visual plan: build/plans/ep016.md. Calculations: build/plans/ep016_checks.py. Score: suspense (style and
key: score.pick's slot for the long film).

Point of view (our reading, labelled as ours): every step looked reasonable on its own (a waiver with controls, an
entity with an outside owner, almost, a hedge on paper); added up, almost half the company sat off its books, and
the people paid to check were paid in other ways too. Educational, not advice.

Every claim, sourced (only pages opened or returned by a search in this run):
  [PSI] US Senate, Permanent Subcommittee on Investigations, "The Role of the Board of Directors in Enron's
      Collapse", Senate Print 107-70, 8 July 2002: Enron "then the seventh largest publicly traded corporation in the
      United States" (when it declared bankruptcy on December 2, 2001); "with over $100 billion in gross revenues and
      more than 20,000 employees worldwide"; "Enron's gross revenues had jumped from $40 billion in 1999 to $100
      billion in 2000"; "In October 2000, the Finance Committee reviewed the chart showing that $27 billion out of
      $60 billion of Enron's assets, or almost 50 percent, were held off Enron's books"; "The Board normally met five
      times during the year"; director pay "valued by Enron at about $350,000 or more than twice the national average
      for Board compensation"; "The first LJM presentation made to the Board took place on June 28, 1999, at a special
      Board meeting held by teleconference."; "the Board ratified the code of conduct waiver and approved the LJM1
      proposal with little study or debate."; LJM2 "The Board approved it on October 12, 1999."; LJM3 "with a third
      code of conduct waiver and even less debate."; "Mr. Fastow admitted receiving LJM compensation totalling $45
      million, $23 million from LJM1 and $22 million from LJM2." (Dr. LeMaistre's notes); "in 1999, Audit Committee
      members were given a nine-page presentation on mark-to-market and fair value accounting issues"; the Raptors:
      "recorded a $710 million charge to earnings and a $1.2 billion reduction in shareholder equity" (footnote 155:
      pre-tax $711m, after-tax $544m); Andersen: "during 2000, paid Andersen about $52 million or $1 million per week
      for its work", consulting "about $27 million compared to auditing fees of about $25 million"; "The Audit
      Committee formally reviewed Andersen's independence annually"; "The facts suggest that the Enron Audit Committee
      went through the motions"; Finding (2) "The Enron Board of Directors knowingly allowed Enron to engage in high
      risk accounting practices."; Finding (6) "The independence of the Enron Board of Directors was compromised by
      financial ties"; "Enron's high-risk accounting practices, for example, were not hidden from the Board." "The
      Board knew of them and took no action to prevent Enron from using them."
  [POW] Report of Investigation by the Special Investigative Committee of the Board of Directors of Enron Corp.
      (William C. Powers, Jr., chair), 1 February 2002, filed with the SEC on Form 8-K: "Many of the most significant
      transactions apparently were designed to accomplish favorable financial statement results, not to achieve bona
      fide economic objectives or to transfer risk."; "an owner independent of the company must make a substantive
      equity investment of at least 3% of the SPE's assets, and that 3% must remain at risk throughout the
      transaction"; Chewco: "Enron and Kopper, however, were unable to locate any such outside investor, and instead
      financed Chewco's purchase of the JEDI interest almost entirely with debt, not equity."; the Raptors "were
      funded principally with Enron's own stock (or contracts for the delivery of Enron stock) that was intended to
      "hedge" against declines in the value of a large group of Enron's merchant investments."; "If the value of the
      investments fell at the same time as the value of Enron stock fell, the SPEs would be unable to meet their
      obligations and the "hedges" would fail."; "Enron never escaped the risk of loss, because it had provided the
      bulk of the capital with which the SPEs would pay Enron."; earnings "from the third quarter of 2000 through the
      third quarter of 2001 that were almost $1 billion higher than should have been reported"; "Fastow by at least
      $30 million".
  [8K] Enron Corp., Form 8-K, 8 November 2001 (and Exhibit 99.1): restatement of 1997 to 2000 and the first two
      quarters of 2001; Table 1 net income as reported 105, 703, 893, 979 and restated 9, 590, 643, 847 ($m, 1997 to
      2000); "four SPEs known as Raptor I-IV (collectively, "Raptor"), were created in 2000"; Chewco and JEDI "should
      have been consolidated beginning in November 1997"; debt increase "$628 million in 2000"; the statements and
      audit reports for 1997 to 2000 "should not be relied upon".
  [BRI] Encyclopaedia Britannica, "Enron scandal: Downfall and bankruptcy": mark to market "allowed the company to
      write unrealized future gains from some trading contracts into current income statements"; Dynegy agreed to
      acquire Enron in November 2001 and "weeks later Dynegy backed out of the deal"; "On December 2, 2001, Enron filed
      for Chapter 11 bankruptcy protection."; "taking with it the value of Enron employees' 401(k) pensions, which were
      mainly tied to the company stock."; Andersen indicted for obstruction of justice (March 2002), "found guilty of
      shredding evidence" (15 June 2002), the Supreme Court "unanimously" overturned it three years later; "Fastow
      pleaded guilty ... and was sentenced to six years in prison"; Skilling "initially sentenced to more than 24 years";
      Lay "died before he was sentenced".
  [HIS] History.com, "Enron files for bankruptcy" (2 December): shares "dropping from $90.75 in August 2000 to $0.26 by
      closing on November 30, 2001"; Lay "was found guilty on 10 counts of fraud and conspiracy" (May 2006).
  [ABA] ABA Journal, "Dec. 2, 2001: Enron files for bankruptcy": "the largest corporate bankruptcy claim until that
      point in history" (not used on screen).

Labelled as ours: the mark-to-market example ($10 a year for 10 years, $77 at 5%: build/plans/ep016_checks.py), the
hedge puzzle ($100 investment, $100 of the company's own shares, falls to $60 and 70%: ours, not the Raptors' real
figures), the 100-square grid, the filmed rooms and streets (illustrations and reconstructions: nobody is a portrait or
a likeness, nobody speaks), the readings in the last chapters.

    python build/youtube_ep016.py
"""

import cine_2001 as F
from cine_lib import document_shot
from youtube import make

S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                         hl=list(hl), size=size, flip=flip)
SC = lambda art, lab="", **opts: dict(kind="scene", art=art, opts=opts, label=lab)
SS = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: SC(art, txt, **opts)
CINE = lambda name: dict(kind="cine", shot=F.SHOTS[name])
DOC = lambda **kw: dict(kind="cine", shot=document_shot(**kw))
PSI = "US Senate report, 2002"
POW = "The Powers report, 2002"

EP = dict(
    slug="yt-016-enron-27-billion",
    title="$27 Billion of Enron Was Off the Books. Its Board Saw the Chart.",
    score="suspense",
    hook_first=True,
    fx="action",
    held_life=True,
    text_life=True,
    thumb=dict(film_a=dict(shot=F.SHOTS["hook_27bn"], dur=13.0, t=3.0, pos="55% 45%",
                           segs=[("In October two thousand, a committee of Enron's board was shown a chart.", .3, 3.6),
                                 ("Of the company's sixty billion dollars in assets, twenty seven billion, almost half, was held off its books.", 3.8, 9.0),
                                 ("So why didn't the board stop it?", 9.4, 11.6)]),
               film_b=dict(shot=F.SHOTS["raptor_2"], dur=12.0, t=9.0, pos="55% 45%",
                           segs=[("Now Enron's shares fall too, by seventy percent.", .3, 3.0),
                                 ("The partner's shares are worth thirty dollars, and it owes forty, so it can't pay.", 3.2, 7.4),
                                 ("And the thirty it does have is Enron's own stock.", 7.6, 10.4)]),
               big_a="<span style='color:#D93A12'>$27BN</span> off the books", size_a=104,
               big="<span style='color:#D93A12'>$27BN</span>. The board knew.", size=100,
               small="Enron, 2000"),
    chapters=[
        dict(title="Almost half", art=("ledger", dict(names=("ASSETS  $60BN", "OFF THE BOOKS  $27BN", "ALMOST 50%", "?"), hi=(1, 2))), beats=[
            dict(say="In October two thousand, a committee of Enron's board was shown a chart. Of the company's sixty billion dollars in assets, twenty seven billion, almost half, was held off its books. So why didn't the board stop it?",
                 show=CINE("hook_27bn")),
            dict(say="Fourteen months later, Enron was bankrupt. Its shares went from ninety dollars and seventy five cents in August two thousand to twenty six cents at the close on the thirtieth of November, two thousand and one.",
                 show=CINE("share_path")),
            dict(say="This film follows the money from the boardroom out. A way of counting profit early, funds run by the company's own finance chief, and a hedge that was really a promise from Enron to itself.",
                 shows=[S("magnifier", "From the boardroom out.", "", ["boardroom"], 104, label="$"),
                        dict(kind="list", title="In this film", items=["Profit counted early", "The finance chief's funds", "A hedge with itself"])]),
        ]),
        dict(title="A giant in Houston", art=("tower", dict(floors=8, label="2000")), beats=[
            dict(say="Enron's gross revenues had jumped from forty billion dollars in nineteen ninety nine to a hundred billion in two thousand. When it failed, the Senate counted it as the seventh largest publicly traded company in America.",
                 show=CINE("revenue_jump")),
            dict(say="It had more than twenty thousand employees around the world. Its board of directors normally met five times a year.",
                 shows=[SC("figures", "More than 20,000 employees (US Senate report)", n=6, hi=0),
                        SC("calendar", "The board: normally five meetings a year", day="5", month="A YEAR", note="BOARD")]),
            dict(say="And the directors were well paid for it. Enron valued each one's pay at about three hundred and fifty thousand dollars a year, more than twice the national average.",
                 shows=[SS("coins", "Directors, well paid"),
                        dict(kind="number", value=350000, pre="$", label="a year per director, as Enron valued it · more than twice the national average · US Senate report")]),
        ]),
        dict(title="Profit up front", art=("hourglass72", dict()), beats=[
            dict(say="Part of Enron's growth was in how it counted. It used what's called mark to market accounting. In Britannica's words, that let it write unrealised future gains from some trading contracts into its current income.",
                 show=CINE("mtm_term")),
            dict(say="Here's our own example. A deal is expected to bring in ten dollars a year for ten years. Count it as it comes, and this year's profit is ten dollars. Use mark to market instead, and you can book today's estimate of all ten years at once. At five percent a year, that's about seventy seven dollars, in year one, before a single extra dollar has come in.",
                 show=CINE("mtm")),
            dict(say="If the estimate is right, nothing is lost but time. If it's wrong, the profit has already been reported, and the cash never comes. The board knew about this. In nineteen ninety nine, its audit committee was given a nine page presentation on mark to market accounting.",
                 shows=[SC("seesaw", "Our reading: the estimate carries the weight", left="ESTIMATE RIGHT", right="ESTIMATE WRONG", tip=1),
                        dict(kind="statement", text="If it's wrong, the profit is already reported.", hl=["reported."], size=80),
                        S("bulb", "The board knew.", PSI, ["knew."], 104, text="!"),
                        S("document", "Nine pages, 1999.", PSI, ["Nine"], 100, flip=True, title="MARK TO MARKET", lines=5, stamp="1999")]),
        ]),
        dict(title="The waiver", art=("stamp", dict(text="WAIVED")), beats=[
            dict(say="On the twenty eighth of June, nineteen ninety nine, the board held a special meeting by teleconference. It heard a proposal for a private equity fund called LJM, to be run by Enron's chief financial officer, Andrew Fastow, that would do deals with Enron.",
                 show=CINE("waiver_1")),
            dict(say="A finance chief on both sides of a deal is a conflict of interest, so it needed a waiver of the company's code of conduct. In the Senate's words, the board ratified the waiver and approved the fund with little study or debate.",
                 show=CINE("waiver_2")),
            dict(say="On the twelfth of October, it approved a second fund, LJM two. Then a third, with a third waiver and even less debate.",
                 shows=[dict(kind="timeline", title="Three waivers (US Senate report)", items=[("28 JUN 1999", "LJM1"), ("12 OCT 1999", "LJM2"), ("2000", "LJM3")], hi=2),
                        SC("stamp", "The third waiver: even less debate", text="LJM3")]),
            dict(say="How much did he make? Enron's own investigators said at least thirty million dollars. Notes the Senate quotes put his own figure at forty five million, from the first two funds.",
                 shows=[SC("coins", "How much did he make?"),
                        dict(kind="compare", left=("Enron's investigators", "$30M+"), right=("His own figure, in notes", "$45M"), note="The Powers report, 2002 · US Senate report, 2002"),
                        S("document", "From two funds.", PSI, ["two"], 96, flip=True, title="LJM1 + LJM2", lines=3, stamp="$45M")]),
        ]),
        dict(title="Off the books", art=("scale", dict(left="ON", right="OFF", tip=1)), beats=[
            dict(say="Many of these deals used special purpose entities, separate companies that could keep assets and debts off Enron's balance sheet. There was a rule for that.",
                 shows=[dict(kind="term", term="Special purpose entity", text="a separate company that can keep assets and debts off the sponsor's balance sheet."),
                        SC("scale", "On or off the books: there was a rule", left="ON", right="OFF", tip=1)]),
            dict(say="As the Powers report puts it, an owner independent of the company had to put in equity of at least three percent of the entity's assets, and that three percent had to stay at risk.",
                 show=CINE("three_pct")),
            dict(say="One entity, Chewco, didn't have it. The report explains why, naming an Enron employee, Michael Kopper. Enron and Kopper, however, were unable to locate any such outside investor, and instead financed Chewco's purchase of the JEDI interest almost entirely with debt, not equity.",
                 show=DOC(style="opinion", head="THE POWERS REPORT", sub="SPECIAL INVESTIGATIVE COMMITTEE OF ENRON'S BOARD, FEBRUARY 1, 2002",
                          quote="Enron and Kopper, however, were unable to locate any such outside investor, and instead financed Chewco's purchase of the JEDI interest almost entirely with debt, not equity.",
                          hl=("any such outside investor", "almost entirely with debt"), start=(2, "Enron"), wrap=42,
                          source="Report of the Special Investigative Committee, filed on Form 8-K", badge_text="Quoted from the Powers report", seed=61)),
            dict(say="In November two thousand and one, Enron said Chewco, and the JEDI fund it invested in, should have been on its books since nineteen ninety seven.",
                 shows=[S("document", "On Enron's books since 1997.", "Enron, Form 8-K, November 8, 2001", ["1997."], 96, title="CHEWCO · JEDI", lines=4, stamp="1997")]),
        ]),
        dict(title="A hedge with itself", art=("seesaw", dict(left="ENRON", right="ENRON", tip=0)), beats=[
            dict(say="In two thousand, Enron set up four more entities, called the Raptors. They were meant to hedge, to protect against falls in the value of a large group of Enron's investments. But they were funded mainly with Enron's own stock.",
                 shows=[SC("tower", "Four Raptors, set up in 2000 (Enron, Form 8-K)", floors=4, label="R1-R4"),
                        dict(kind="flow", title="A hedge, as designed", items=[("doc", "Investments fall"), ("scales", "The Raptors pay"), ("coin", "Enron's results protected")]),
                        SC("coins", "Funded mainly with Enron's own stock (the Powers report)")]),
            dict(say="Here's the puzzle, with our own numbers. Enron owns an investment worth a hundred dollars. A partner promises to cover any fall, and all its money is a hundred dollars of Enron shares. The investment falls to sixty. The partner pays the forty, and the loss is covered.",
                 show=CINE("raptor_1")),
            dict(say="Now Enron's shares fall too, by seventy percent. The partner's shares are worth thirty dollars, and it owes forty, so it can't pay. And the thirty it does have is Enron's own stock.",
                 show=CINE("raptor_2")),
            dict(say="The Powers report saw the drawback. Enron never escaped the risk, it says, because it had provided most of the money the entities would pay it with.",
                 shows=[S("magnifier", "The drawback.", POW, ["drawback."], 104, label="!"),
                        SC("seesaw", "Both sides: Enron", left="ENRON'S RISK", right="ENRON'S MONEY", tip=0)]),
            dict(say="Here's how the report put it. If the value of the investments fell at the same time as the value of Enron stock fell, the SPEs would be unable to meet their obligations and the hedges would fail.",
                 show=DOC(style="opinion", head="THE POWERS REPORT", sub="SPECIAL INVESTIGATIVE COMMITTEE OF ENRON'S BOARD, FEBRUARY 1, 2002",
                          quote="If the value of the investments fell at the same time as the value of Enron stock fell, the SPEs would be unable to meet their obligations and the \"hedges\" would fail.",
                          hl=("value of Enron stock", "unable to meet"), start=(1, None), wrap=42,
                          source="Report of the Special Investigative Committee, filed on Form 8-K", badge_text="Quoted from the Powers report", seed=62)),
            dict(say="It found these deals let Enron report earnings almost a billion dollars higher than it should have, from late two thousand to late two thousand and one.",
                 shows=[dict(kind="number", value=1, pre="almost $", suf=" billion", label="of earnings reported that shouldn't have been, Q3 2000 to Q3 2001 · The Powers report")]),
        ]),
        dict(title="Unwinding", art=("calendar", dict(day="8", month="NOV", note="2001")), beats=[
            dict(say="In October two thousand and one, Enron recorded a charge of seven hundred and ten million dollars to its earnings, and cut its shareholders' equity by one point two billion. The Senate report ties both to the Raptors.",
                 show=CINE("charge_oct")),
            dict(say="On the eighth of November, it said it would restate its accounts for nineteen ninety seven to two thousand. Net income for nineteen ninety seven fell from a hundred and five million dollars to nine million, and every year after was lower too.",
                 show=CINE("restate")),
            dict(say="It said those statements, and the audit reports on them, should not be relied upon. And it added debt that had been off the books, about six hundred and twenty eight million dollars for two thousand alone.",
                 shows=[SC("stamp", "1997 to 2000: should not be relied upon (Form 8-K)", text="NOT RELIED"),
                        dict(kind="number", value=628, pre="$", suf="M", label="of debt added for 2000 alone · Enron, Form 8-K, November 8, 2001")]),
            dict(say="That month, a rival, Dynegy, agreed to buy Enron. Weeks later, it backed out. On the second of December, two thousand and one, Enron filed for Chapter eleven bankruptcy.",
                 show=CINE("collapse")),
            dict(say="It took with it the value of employees' retirement plans, which were mainly tied to the company's stock.",
                 shows=[SC("empty_pockets", "Retirement plans, mainly in Enron stock (Britannica)", label="401(k)")]),
        ]),
        dict(title="The watchers", art=("magnifier", dict(label="WHO?")), beats=[
            dict(say="Enron's auditor was Arthur Andersen. The Senate found that Enron, during two thousand, paid Andersen about fifty two million dollars, or one million dollars per week, for its work.",
                 show=DOC(style="opinion", head="UNITED STATES SENATE", sub="PERMANENT SUBCOMMITTEE ON INVESTIGATIONS, JULY 8, 2002",
                          quote="during 2000, paid Andersen about $52 million or $1 million per week for its work.",
                          hl=("about $52", "$1 million per week"), start=(1, "during"), wrap=36,
                          source="The Role of the Board of Directors in Enron's Collapse, Senate Print 107-70", badge_text="Quoted from the Senate report", seed=63)),
            dict(say="About twenty seven million of it was for consulting, against about twenty five million for the audit. The audit committee reviewed Andersen's independence every year. The Senate found that it went through the motions.",
                 shows=[dict(kind="compare", left=("Consulting", "$27M"), right=("The audit", "$25M"), note="Andersen's fees from Enron, 2000 · US Senate report"),
                        SC("calendar", "Andersen's independence: reviewed every year", day="1", month="A YEAR", note="REVIEW"),
                        S("stamp", "Through the motions.", PSI, ["motions."], 100, flip=True, text="CHECKED?")]),
            dict(say="In June two thousand and two, Andersen was found guilty of obstruction of justice, for shredding evidence. Three years later, the Supreme Court overturned the conviction.",
                 shows=[S("document", "Found guilty, 2002.", "Encyclopaedia Britannica", ["guilty,"], 100, title="ANDERSEN", lines=4, stamp="2002"),
                        dict(kind="timeline", title="Arthur Andersen (Britannica)", items=[("JUN 2002", "Found guilty"), ("2005", "Overturned")], hi=1)]),
            dict(say="And the Senate's second finding was about the board itself. The Enron Board of Directors knowingly allowed Enron to engage in high risk accounting practices.",
                 show=DOC(style="opinion", head="UNITED STATES SENATE", sub="PERMANENT SUBCOMMITTEE ON INVESTIGATIONS, FINDING 2",
                          quote="The Enron Board of Directors knowingly allowed Enron to engage in high risk accounting practices.",
                          hl=("knowingly allowed", "high risk"), start=(1, None), wrap=34,
                          source="The Role of the Board of Directors in Enron's Collapse, Senate Print 107-70", badge_text="Quoted from the Senate report", seed=64)),
        ]),
        dict(title="Why nobody stopped it", art=("figures", dict(n=5, hi=0)), beats=[
            dict(say="So why didn't the board stop it? The Senate's answer was that the accounting wasn't hidden from them. The board knew of it, and took no action to prevent it.",
                 shows=[S("magnifier", "Why didn't they stop it?", "", ["stop"], 100, label="?"),
                        S("document", "Not hidden.", PSI, ["hidden."], 100, flip=True, title="THE BOARD", lines=4, stamp="KNEW"),
                        dict(kind="statement", text="The board knew, and took no action.", hl=["no"], size=84)]),
            dict(say="Our reading is that every step looked reasonable on its own. A waiver, with controls. An entity, with an outside owner, almost. A hedge, on paper. Added up, almost half the company sat off its books.",
                 shows=[S("bulb", "Our reading.", "", ["reading."], 110, text="?"),
                        S("stamp", "A waiver.", "", ["waiver."], 100, text="WAIVED"),
                        S("scale", "An outside owner, almost.", "", ["almost."], 96, flip=True, left="3%", right="DEBT", tip=1),
                        S("handshake", "A hedge, on paper.", "", ["paper."], 96, left="ENRON", right="ENRON"),
                        SC("bars", "Added up: assets on and off the books, October 2000 ($bn, US Senate report)", values=[33, 27], labels=["ON THE BOOKS: $33BN", "OFF: $27BN"], hi=1)]),
            dict(say="And the people paid to check were paid in other ways too. The auditor earned more from consulting than from the audit. The Senate found the board's independence was compromised by financial ties.",
                 shows=[S("figures", "Paid to check.", "", ["check"], 100, n=4, hi=1),
                        SC("scale", "Andersen's fees, 2000: consulting against the audit", left="CONSULTING $27M", right="AUDIT $25M", tip=0),
                        dict(kind="statement", text="Independence compromised by financial ties.", hl=["compromised"], size=80)]),
            dict(say="Fastow pleaded guilty, and was sentenced to six years in prison. Jeffrey Skilling, a former chief executive, was sentenced to more than twenty four years. Kenneth Lay, the chairman, was found guilty in two thousand and six, and died before he was sentenced.",
                 shows=[S("stamp", "Six years.", "Encyclopaedia Britannica", ["Six"], 104, text="FASTOW"),
                        S("stamp", "More than 24 years.", "Encyclopaedia Britannica", ["24"], 100, flip=True, text="SKILLING"),
                        dict(kind="timeline", title="The verdicts (Britannica; History.com)", items=[("FASTOW", "Six years"), ("SKILLING", "24+ years"), ("LAY, 2006", "Died before sentencing")], hi=2)]),
        ]),
        dict(title="Who carries the risk", art=("scale", dict(left="RISK", right="WHO?", tip=1)), beats=[
            dict(say="If an interviewer asks what off balance sheet means, here's a short answer. It's an asset or a debt a company is exposed to that isn't on its balance sheet. The question to ask is who carries the risk if it goes wrong. At Enron, the answer was Enron. This is education, not financial advice.",
                 shows=[S("document", "Off balance sheet?", "Interview prep", ["Off"], 100, title="Q: OFF BS?", lines=3, stamp="2001"),
                        dict(kind="term", term="Off balance sheet", text="exposed to it, but not on the balance sheet."),
                        S("scale", "Who carries the risk?", "", ["risk"], 100, flip=True, left="RISK", right="WHO?", tip=1),
                        SS("seesaw", "At Enron: Enron.", left="ENRON", right="ENRON", tip=0),
                        dict(kind="icon", icon="book", label="Education", text="Not financial advice.", hl=["advice."], size=110)]),
            dict(say="Our question for you. If a company hedges with a partner that's paid in the company's own shares, is that a hedge at all? Tell us in the comments.",
                 shows=[S("bulb", "Our question for you.", "", ["question"], 110, text="?"),
                        SC("handshake", "A partner paid in your own shares", left="COMPANY", right="ITS SHARES"),
                        dict(kind="icon", icon="pen", label="Your turn", text="Tell us in the comments.", hl=["comments."], size=100)]),
        ]),
    ],
    description=(
        "In October 2000, a committee of Enron's board was shown a chart: $27 billion of the company's $60 billion in "
        "assets, almost half, was held off its books. Fourteen months later, Enron was bankrupt. So why didn't the board "
        "stop it?\n\n"
        "We'll follow the money from the boardroom out: how mark to market accounting let Enron count years of profit up "
        "front, how the board waived its own code of conduct so the finance chief could run funds that did deals with "
        "Enron, the 3% rule that was meant to keep those entities honest, and the Raptors, a hedge paid for with Enron's "
        "own shares. There's a puzzle on the way: if your insurer's only money is your own stock, what happens when your "
        "stock falls too? Then the restatement, the bankruptcy, the auditor, and what the Senate found about the board. "
        "Our question for you: if a company hedges with a partner that's paid in its own shares, is that a hedge at all? "
        "Tell us below."),
    sources=[
        ("US Senate, Permanent Subcommittee on Investigations, The Role of the Board of Directors in Enron's Collapse (Senate Print 107-70, 8 July 2002)",
         "https://www.govinfo.gov/content/pkg/CPRT-107SPRT80393/html/CPRT-107SPRT80393.htm"),
        ("Report of Investigation by the Special Investigative Committee of the Board of Directors of Enron Corp. (the Powers report, 1 February 2002), filed with the SEC on Form 8-K",
         "https://www.sec.gov/Archives/edgar/data/0001024401/000090951802000089/big.txt"),
        ("Enron Corp., Form 8-K, 8 November 2001 (the restatement)",
         "https://www.sec.gov/Archives/edgar/data/0001024401/000095012901503835/h91831e8-k.txt"),
        ("Enron Corp., press release of 8 November 2001 (Exhibit 99.1)",
         "https://www.sec.gov/Archives/edgar/data/0001024401/000095012901503835/h91831ex99-1.txt"),
        ("Encyclopaedia Britannica, Enron scandal: Downfall and bankruptcy",
         "https://www.britannica.com/event/Enron-scandal/Downfall-and-bankruptcy"),
        ("History.com, Enron files for bankruptcy",
         "https://www.history.com/this-day-in-history/december-2/enron-files-for-bankruptcy"),
    ],
    source_note="We drew the filmed scenes ourselves. The boardroom, the offices, the kitchen and the streets, and the screens, "
                "papers and billboards in them, are our illustrations and stylised reconstructions. They aren't the real rooms, "
                "documents or people, nobody in them is a portrait or a likeness, and nobody speaks. The share price shows only "
                "its two sourced prints, with nothing drawn in between. The $10 a year example and the hedge puzzle use our own "
                "numbers, not Enron's. The readings in the last chapters are ours, so feel free to disagree with them. This "
                "channel is educational and isn't affiliated with, or endorsed by, any company, firm or government body named in it.",
    hashtags=["Enron", "Accounting", "FinanceHistory"],
    tags=["Enron", "Enron scandal", "Enron collapse 2001", "off balance sheet", "mark to market accounting", "special purpose entity",
          "Raptors Enron", "LJM Andrew Fastow", "Arthur Andersen", "Powers report", "corporate governance", "board of directors",
          "investment banking interview", "financial history"],
)

if __name__ == "__main__":
    make(EP)
