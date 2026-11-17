"""Calculations in YouTube #11 (Herstatt, 1974), checked against the sources. python3 build/plans/ep011_checks.py"""
from datetime import datetime, timedelta, timezone
# 3:30 p.m. German time (CET, UTC+1: West Germany had no summer time from 1950 to 1979) in New York (EDT, UTC-4:
# the US was on daylight time all year in 1974 under the Emergency Daylight Saving Time Energy Conservation Act)
close = datetime(1974, 6, 26, 15, 30, tzinfo=timezone(timedelta(hours=1)))
ny = close.astimezone(timezone(timedelta(hours=-4)))
assert (ny.hour, ny.minute) == (10, 30)                                           # "half past ten in the morning"
assert (close.utcoffset() - ny.utcoffset()) == timedelta(hours=5)                 # "five hours apart"
total, pvp, gross = 14.0, 5.2, 1.4                                                # $tn a day, April 2025 (BIS 2026)
assert 1 / 3 < pvp / total < 0.40                                                 # "just over a third" (BIS: 36% on unrounded totals)
assert abs(gross / total - 0.10) < 0.005                                          # "ten percent"
assert 15 < 32 / 2                                                                # 32% (2006) to 15% (2025) "more than halved"
assert 2026 - 1974 == 52                                                          # "half a century later", "fifty years later"
assert 2002 - 1974 == 28                                                          # "28 YRS" on the hourglass (Herstatt to CLS)
assert 100 * (1 - 0.60) == 40                                                     # index 100 -> 40 = the BIS's estimated 60% fall
assert 18 > 7                                                                     # currencies: 7 in 2002 (BIS), 18 (CLS 2024)
assert 12 - 7 == 5                                                                # the CLS window 07:00 to 12:00 CET is five hours
print("ep011 checks OK: 15:30 CET = 10:30 EDT (5 h) | 5.2/14 =", round(pvp / total, 3), "| 1.4/14 =", round(gross / total, 3),
      "| 32% -> 15% | 52 years | index 100 -> 40 | window 5 h")
