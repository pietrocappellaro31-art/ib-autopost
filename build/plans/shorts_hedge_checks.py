"""Checks for build/shorts_hedge-own-shares.py (24 Nov 2026): every number said or shown, from our own example."""
inv0, inv1 = 100, 60
owed = inv0 - inv1
partner0 = 100
fall = 0.70
partner1 = round(partner0 * (1 - fall), 2)
assert owed == 40 and partner1 == 30
assert partner0 >= owed                      # before the shares fall: covered
assert partner1 < owed and owed - partner1 == 10   # after: $10 short, can't pay
# close (not given on screen): the break point is where partner0 * (1 - x) = owed
x = 1 - owed / partner0
assert abs(x - 0.60) < 1e-9                  # more than a 60% fall and it can't pay the $40
for f in (.1, .2, .3, .4, .5):               # the close's steps stop at -50%: still $50 >= $40, nothing given away
    assert partner0 * (1 - f) >= owed
print("ok: owed 40, partner 100 -> 30 after -70%, short 10; break point 60% (close, not shown)")
