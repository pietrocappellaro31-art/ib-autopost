"""Calculations behind YouTube #15 (Barings, February 1995). Every derived number on screen or in the script, checked
here. python3 build/plans/ep015_checks.py"""

# sourced: RBA (Nov 1995): losses £827m by 27 Feb 1995; recorded group capital "in the order of £350 million" (end 1994)
loss, capital = 827, 350
print("827 / 350 =", round(loss / capital, 2))
assert loss / capital > 2                          # 'more than twice its capital'
print("827 - 350 =", loss - capital)
assert loss - capital > 100                        # 'hundreds of millions still to pay' (about 477, not shown as a figure)
# Hansard 18 Jul 1995: more than £20m end 1993, more than £200m end 1994; £827m by 27 Feb 1995 (RBA)
assert 20 < 200 < 827
# founded 1762 (NLB): 233 years old in 1995
assert 1995 - 1762 == 233
# Hansard 18 Jul 1995: lending more than £300m to clients against collateral of only about £31m
print("300 / 31 =", round(300 / 31, 1))
assert 300 / 31 > 9                                # (not said on screen; bars are drawn on one scale: 660 px vs 68 px)
assert abs(300 * 2.2 - 660) < 1e-9 and abs(31 * 2.2 - 68.2) < 1e-9
# NLB: Nikkei 17,785 on 23 Jan 1995, below his line of 19,000
assert 17785 < 19000
print("fall from the line:", 19000 - 17785, "points (not said: the index level before the quake is not sourced)")
# our example: selling insurance, £1 a day for 99 calm days, then a £150 payout on day 100
fees, payout = 99 * 1, 150
total = fees - payout
print("our example total:", total)
assert total == -51
assert 99 / 100 == .99                             # 'right ninety nine days out of a hundred'
# the balance board: one scale, 0.30 px per £m
sc = .30
assert round(loss * sc) == 248 and round(capital * sc) == 105
print("board: loss", loss * sc, "px, capital", capital * sc, "px, below zero after", round((loss - capital) * sc, 1), "px")
# sentence: Leeson, 6.5 years (NLB, 1 Dec 1995)
print("all checks pass")
