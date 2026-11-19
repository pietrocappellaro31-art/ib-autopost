"""Calculations behind YouTube #13 (GameStop, January 2021). Every derived number on screen or in the script, checked
here. python3 build/plans/ep013_checks.py"""
from datetime import date

# 22 Jan volume against the 2020 average day (SEC staff report pp. 18, 20): 'about twenty nine times'
r = 197.2 / 6.7
print("197.2m / 6.7m =", round(r, 2))
assert 28.5 < r < 29.5
# 'a little under $20' to the $483.00 intraday high: more than 24 times (not said on screen; context only)
assert 483 / 20 > 24
# 22 Jan: 'from $43 to $72 in about three hours'; the report rounds it to 71% from unrounded prices; 43 -> 72 is 67%
print("72 / 43 - 1 =", round((72 / 43 - 1) * 100, 1), "% (the film gives the two prices, not a percentage)")
# Tenev: on deposit $696m, VaR 'nearly $1.3bn', ECP 'over $2.2bn', deficit 'approximately $3bn'
print("VaR + ECP =", round(1.3 + 2.2, 1), "bn; less 0.696 on deposit =", round(1.3 + 2.2 - .696, 2), "bn ('about $3bn', given as such)")
assert abs((1.3 + 2.2 - .696) - 3) < .25
# after the waiver: requirement about $1.4bn = $696m already there + $737m new
print("696 + 737 =", 696 + 737)
assert round((696 + 737) / 1000, 1) == 1.4
# the 'premium is most of it': 2.2 of about 3.5
assert 2.2 / (1.3 + 2.2) > .5
# our short-sale example: sold at $20; bought back at $10 keeps $10; at $50 loses $30
assert 20 - 10 == 10 and 50 - 20 == 30
# the lending chain: 100 shares, lent and sold twice
exist, short, owned = 100, 0, 100
short += 100; owned += 100          # lent to short seller 1, sold to owner 2
short += 100; owned += 100          # lent again to short seller 2, sold to owner 3
assert (exist, short, owned) == (100, 200, 300)
# 109.26% rounds to 109
assert round(109.26) == 109
# 28 Jan: high 483.00, close 193.60 (as given); 'over 86%' fall from the high to the first week of February's close
# (not used on screen). Feb 3 under $100; Feb 19 low $40.59 (as given)
# 'Within four weeks': 31 Dec 2020 to 28 Jan 2021
print("31 Dec to 28 Jan:", (date(2021, 1, 28) - date(2020, 12, 31)).days, "days")
assert (date(2021, 1, 28) - date(2020, 12, 31)).days == 28
# T+1: adopted 15 Feb 2023, compliance 28 May 2024 (as given); 40 LULD pauses in Jan 2021 vs 1 in 2020 (as given)
# Melvin: -53% in January, $2.75bn from Citadel and Point72 (as reported)
print("all checks pass")
