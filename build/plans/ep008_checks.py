"""Calculation checks for YouTube #8 (every derived number in the script and on screen)."""
assert 35_000_000 / 35 == 1_000_000                      # our example: ounces for $35m at $35
q = 14 / 4
assert q == 3.5 and q > 3.2                               # a quarter of $14bn+ exceeds the $3.2bn available (IMF 1966)
up = 38 / 35 - 1; down = 1 - 35 / 38
print(f"$35 -> $38: gold price +{up:.1%}, dollar's gold value -{down:.1%} (FRH: 'approximately 8.5 percent')")
assert abs(up - .0857) < .001
print(f"$38 -> $42.22: +{42.22/38-1:.1%}; dollar's gold value -{1-38/42.22:.1%} (FRH: 'an additional 10 percent')")
assert 2026 - 1971 == 55                                  # years since the window closed
assert 1974 - 1934 == 40
import datetime
assert datetime.date(1971, 8, 13).strftime("%A") == "Friday" and datetime.date(1971, 8, 15).strftime("%A") == "Sunday"
# vault_gap chart scale: $1bn = 40 px on one axis for all three bars
S = 40; print("heights px:", 14 * S, 13.2 * S, 3.2 * S, "quarter", 14 * S / 4)
print("all checks pass")
