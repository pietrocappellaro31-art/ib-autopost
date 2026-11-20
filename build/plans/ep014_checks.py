"""Calculations behind YouTube #14 (Silicon Valley Bank, March 2023). Every derived number on screen or in the
script, checked here. python3 build/plans/ep014_checks.py"""

# our example bond: $100, 10 years, 1.5% a year (annual coupons), priced so a buyer earns 4% a year
price = lambda c, y, n: sum(c / (1 + y) ** t for t in range(1, n + 1)) + 100 / (1 + y) ** n
p = price(1.5, .04, 10)
print("price at 4%:", round(p, 2))
assert round(p, 2) == 79.72                      # 'about seventy nine dollars and seventy cents'
assert abs(price(1.5, .015, 10) - 100) < 1e-9     # at 1.5% it is worth its $100
assert 0.18 < 1 - p / 100 < 0.22                  # 'about a fifth of it is gone' (20.3%)
assert price(1.5, .04, 6) > p                     # 'the longer the bond, the further it falls' (6 years: $86.89)
# 10-K, 31 Dec 2022, $ million
htm_cost, htm_fv, htm_loss = 91327, 76169, 15160
assert abs((htm_cost - htm_fv) - htm_loss) <= 2   # 15,158 net (15,160 loss less 2 gain)
assert round(htm_cost / 1000, 1) == 91.3 and round(htm_fv / 1000, 1) == 76.2 and round(htm_loss / 1000, 1) == 15.2
equity = 16004
assert round(equity / 1000, 1) == 16.0
print("HTM loss / equity:", round(htm_loss / equity, 3))
afs_fv, assets = 26069, 211793
bonds = (91321 + afs_fv) / 1000                   # HTM net carrying value + AFS fair value
print("bonds:", round(bonds, 1), "of", round(assets / 1000, 1), "=", round(bonds / (assets / 1000), 3))
assert bonds / (assets / 1000) > .5               # 'more than half of everything it owned was bonds' (55%)
dep22, dep21 = 173109, 189203
assert round(dep22 / 1000) == 173 and round(dep21 / 1000, 1) == 189.2
assert 151.5 < dep22 / 1000                       # uninsured US estimate below total deposits
# Fed review: $71bn to over $211bn, 2019 to 2021: 'tripled'
print("211 / 71 =", round(211 / 71, 2))
assert 2.9 < 211 / 71 < 3.1
# March 9: over $40bn; expected over $100bn more; 'roughly 85 percent' (as given; (40 + 100) / 173.1 = 81%, both 'over')
print("(40 + 100) / 173.1 =", round(140 / 173.1, 3), "(the review's 85% uses the actual figures; we quote it as given)")
# Comparison bars: Wachovia about $10bn over 8 days, WaMu $19bn over 16 days, SVB over $40bn in one day (as given)
# 8 March: $21bn sold, $1.8bn after-tax loss, $2.25bn sought (as given)
print("all checks pass")
# added before the render: the other way (new bonds at 1%), and duration (our bond, rates 1.5% -> 2.5%)
assert round(price(1.5, .01, 10), 2) == 104.74
q = price(1.5, .025, 10)
assert round(q, 2) == 91.25 and 8.5 < 100 - q < 9.0                   # 'falls about nine percent'
c, y = 1.5, .015
mac = (sum(t * c / (1 + y) ** t for t in range(1, 11)) + 10 * 100 / (1 + y) ** 10) / price(c, y, 10)
print("duration:", round(mac, 2), "Macaulay,", round(mac / (1 + y), 2), "modified")
assert 9.0 < mac / (1 + y) < 9.4                                      # 'a little over nine' (9.2)
# AFS: fair value $26,069m, unrealized loss $2,533m (10-K)
assert round(26069 / 1000) == 26 and round(2533 / 1000, 1) == 2.5
print("added checks pass")
