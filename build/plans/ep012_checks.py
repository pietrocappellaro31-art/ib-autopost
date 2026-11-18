"""Calculations behind YouTube #12 (LTCM, 1998). Every derived number on screen or in the script, checked here.
python3 build/plans/ep012_checks.py"""
from datetime import date

# capital (PWG 1999): 4.8 on 1 Jan 1998, 4.1 on 31 Jul, August loss 1.8, 2.3 at end of August
assert round(4.1 - 1.8, 1) == 2.3
print("August loss as share of July capital:", round(1.8 / 4.1 * 100, 1), "% (Federal Reserve History: 44%)")
assert round(1.8 / 4.1 * 100) == 44
print("Year to end of August:", round((1 - 2.3 / 4.8) * 100, 1), "% down ('more than half'; McDonough: 52%)")
assert (1 - 2.3 / 4.8) > .5 and round((1 - 2.3 / 4.8) * 100) == 52
print("4.1 vs 4.8: down", round((1 - 4.1 / 4.8) * 100, 1), "% (PWG: 'down about fifteen percent')")
# three weeks: letter 2 Sept, deal 23 Sept
assert (date(1998, 9, 23) - date(1998, 9, 2)).days == 21
# Nobel 'the year before': prize announced 14 Oct 1997, letter 1998
assert 1998 - 1997 == 1
# a tenth of a percent on $1bn a year (our arithmetic)
assert abs(1e9 * 0.001 - 1e6) < 1
# leverage: at 25 to 1, assets falling 4% wipe out capital; 1% takes a quarter
assert abs(1 / 25 - .04) < 1e-12
assert abs(25 * .01 - .25) < 1e-12
# PWG: assets > $125bn on 31 Aug, capital $4.8bn at the start of the year: 'more than 25 to 1'
print("125 / 4.8 =", round(125 / 4.8, 1))
assert 125 / 4.8 > 25
# 1994 founded Feb; returns 20, 43, 41, 17 (Federal Reserve History) are as given, not derived
# rescue: 14 firms, $3.6bn (3.625), 90% to the consortium, 10% left: 90 + 10 = 100
assert 90 + 10 == 100 and round(3.625, 1) == 3.6
# Buffett group: $250m + $3.75bn (as given)
# 17 counterparties: $3bn to $5bn (as given)
print("all checks pass")
