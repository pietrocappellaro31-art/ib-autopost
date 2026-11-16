"""Calculations in YouTube #10 (the salad oil swindle), checked against Time's figures. python3 build/plans/ep010_checks.py"""
receipts, found = 1_800e6, 100e6                 # pounds, Time 4 June 1965
assert abs(found / receipts - 0.0556) < 1e-3 and round(receipts / found) == 18      # about 1 pound in 18
lbs, worth = 1.2e9, 120e6                        # contracted by mid 1963, Time 1965
assert abs(worth / lbs - 0.10) < 1e-9                                               # about 10 cents a pound
assert abs(lbs * 0.01 - 12e6) < 1                                                   # 1 cent a pound = $12m (Time's own figure)
assert abs(0.05 * worth - 6e6) < 1 and abs(lbs * 0.005 - 6e6) < 1                   # 5% deposit = half a cent a pound = $6m
assert 1963 + 7 == 1970                                                             # SIPA
assert abs((62 - 35) / 62 - 0.435) < 1e-3                                           # AmEx shares, Time
assert 3 * 1 == 3                                                                   # loans on 3x the tank space (Time), bars 1 and 3
print("ep010 checks OK: 1 in", round(receipts / found), "| 10c a lb | 1c = $12m | half a cent = $6m = 5% deposit | 1970 | -43.5%")
