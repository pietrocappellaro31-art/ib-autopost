"""Calculations behind YouTube #16 (Enron, 1999 to 2001). Every derived number on screen or in the script, checked
here. python3 build/plans/ep016_checks.py"""

# [PSI] October 2000 chart: $27bn of $60bn of assets off the books, "almost 50 percent"
off, assets = 27, 60
print("27 / 60 =", off / assets)
assert .4 < off / assets < .5                       # 'almost half' (45%)
assert assets - off == 33                           # the 'on the books' bar in chapter 9 (60 - 27)
# October 2000 to the bankruptcy on 2 December 2001 [BRI]: 'fourteen months later'
months = (2001 - 2000) * 12 + (12 - 10)
print("Oct 2000 -> Dec 2001:", months, "months")
assert months == 14
# [HIS] shares $90.75 (Aug 2000) to $0.26 (close, 30 Nov 2001)
print("fall:", round((1 - .26 / 90.75) * 100, 2), "%")
# [PSI] gross revenues $40bn (1999) to $100bn (2000): bars on one scale (8 px per $bn)
assert 40 * 8 == 320 and 100 * 8 == 800
# [PSI] the hook's bars: 13 px per $bn on the wall display (1000 px wide): 60 -> 780 px, 27 -> 351 px
assert 60 * 13 == 780 and round(27 * 13) == 351 and 40 + 780 + 14 + 150 < 1000
# our mark-to-market example: $10 a year for 10 years, today's value at 5% a year
pv = sum(10 / 1.05 ** k for k in range(1, 11))
print("PV of $10 a year for 10 years at 5%:", round(pv, 2))
assert round(pv) == 77
assert 10 * 10 == 100                               # undiscounted (not said)
# our hedge puzzle: investment $100 -> $60, the partner owes $40; its $100 of shares fall 70% -> $30
inv0, inv1 = 100, 60
owe = inv0 - inv1
shares = 100 * (1 - .70)
print("owes", owe, "has", shares)
assert owe == 40 and round(shares) == 30 and shares < owe
# [8K] Table 1: net income as reported and restated ($m), 1997 to 2000; 'every year after was lower too'
rep = {1997: 105, 1998: 703, 1999: 893, 2000: 979}
res = {1997: 9, 1998: 590, 1999: 643, 2000: 847}
for y in rep:
    assert res[y] < rep[y]
    print(y, rep[y], "->", res[y], "difference", rep[y] - res[y])
# the press release's per-year reductions (96, 113, 250, 132) match Table 1's differences
assert [rep[y] - res[y] for y in rep] == [96, 113, 250, 132]
print("total reduction 1997-2000:", sum(rep[y] - res[y] for y in rep), "$m (not said)")
# restate bars: .64 px per $m, the longest bar (979) ends at 130 + 627 = 757 px, its label clear of the plant (< 880)
assert 130 + 979 * .64 + 12 + 70 < 880
# [PSI] Andersen 2000: about $52m, $1m a week; consulting about $27m vs audit about $25m
assert 27 + 25 == 52 and abs(52 / 52 - 1) < 1e-9 and 27 > 25
# [PSI] directors: about $350,000 a year
# [PSI] Fastow: $45m = $23m (LJM1) + $22m (LJM2); [POW] 'at least $30 million'
assert 23 + 22 == 45 and 45 > 30
# [PSI] three waivers: 28 Jun 1999 (LJM1), 12 Oct 1999 (LJM2), LJM3 in 2000
# [BRI] Andersen guilty 15 June 2002; overturned three years later (2005)
assert 2002 + 3 == 2005
# [8K] debt added for 2000 from consolidating JEDI and Chewco: $628m
print("all checks pass")
