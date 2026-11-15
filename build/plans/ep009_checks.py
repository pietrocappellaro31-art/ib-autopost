"""Calculation checks for YouTube #9 (every derived number in the script and on screen)."""
import datetime
taken, promised = 9_582_000, 14_374_000                    # Cunningham v. Brown (1924)
gap = promised - taken
assert gap == 4_792_000                                    # "about four point eight million"
coupons = gap / 0.05                                       # even a free coupon becomes at most a 5-cent stamp
assert coupons == 95_840_000                               # "at least ninety six million"
print(f"notes / money = {promised / taken:.4f} (50% on top: {taken * 1.5:,.0f})")
assert abs(promised / taken - 1.5) < .001
owed = [100 * 1.5 ** k for k in range(9)]                  # our example: $100 rolled over every 45 days
assert round(owed[8]) == 2563 and 8 * 45 == 360            # "about two thousand five hundred and sixty three", "about a year"
assert [round(owed[k]) for k in (0, 2, 4, 6, 8)] == [100, 225, 506, 1139, 2563]   # the bars, one honest scale
assert round(9.582, 1) == 9.6 and round(14.374, 1) == 14.4 and round(6.692, 1) == 6.7
for d, name in [((1920, 7, 24), "Saturday"), ((1920, 7, 26), "Monday"), ((1920, 8, 2), "Monday"), ((1920, 8, 9), "Monday")]:
    assert datetime.date(*d).strftime("%A") == name, d
assert 2026 - 1907 == 119                                  # UPU: "almost 120 years"
assert 40_930 > 40_000                                     # DOJ: "more than forty thousand victims"
print("all checks pass")
