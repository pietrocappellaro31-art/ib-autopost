"""
Post 1 of the week: "Walk me through the 3 statements."

The canonical opener. Post 1 of the account promised each of its five
questions would get its own post; this is the first of those.

Technicals, checked:
  Depreciation +10, tax rate 25%.
  IS   EBIT -10, pre-tax -10, tax -2.5, net income -7.5
  CFS  net income -7.5, add back depreciation +10, cash from ops +2.5
  BS   cash +2.5, PP&E -10 -> assets -7.5; retained earnings -7.5. Balances.
Deferred tax is ignored, as it is in the expected interview answer.
"""

from brand import ARROW, BOOKMARK, Deck, INK, MUTE, PAPER, RED, TEAL, WHITE, check

d = Deck("w1-01-statements", "Technical of the Day", 9)

# ---------------------------------------------------------------- 1 cover
stack = "".join(
    f'<div style="transform:rotate({-4 + i * 4}deg);background:{WHITE};color:{INK};'
    f'padding:15px 26px;font-size:28px;font-weight:600;border-radius:11px;'
    f'box-shadow:0 9px 0 rgba(0,0,0,.18)">{t}</div>'
    for i, t in enumerate(["Income statement", "Cash flow", "Balance sheet"]))

d.slide(RED, WHITE, accent=WHITE, inner=(
    '<div style="display:flex;flex-direction:column;gap:40px">'
    '<h1 style="font-size:118px">Walk me through<br>the <span style="position:relative;'
    'display:inline-block">3 statements'
    '<svg width="400" height="34" viewBox="0 0 520 42" fill="none" style="position:absolute;'
    f'left:0;bottom:-10px"><path d="M6 28c110-22 300-26 508-8" stroke="{WHITE}" stroke-width="9" '
    'stroke-linecap="round" opacity=".85"/></svg></span>.</h1>'
    f'<div style="display:flex;flex-wrap:wrap;gap:16px;max-width:820px">{stack}</div>'
    '<div class="body" style="font-size:36px;font-weight:500;opacity:.95;max-width:860px">'
    'Asked in every single interview. Almost nobody answers it well.</div></div>'))

# ---------------------------------------------------------------- 2 stake
d.slide(INK, WHITE, inner=(
    '<div style="display:flex;flex-direction:column;gap:36px">'
    f'<h1 style="font-size:88px">Anyone can name the three<span style="color:{RED}">.</span></h1>'
    '<div style="display:flex;gap:18px;align-items:center">'
    + "".join(f'<div style="flex:1;border:3px solid rgba(255,255,255,.3);border-radius:14px;'
              f'padding:26px 10px;text-align:center;font-size:29px;font-weight:600;'
              f'opacity:.45">{t}</div>' for t in ["Income", "Cash flow", "Balance sheet"])
    + '</div>'
    f'<div class="body" style="font-size:40px;font-weight:500">The offer goes to whoever can show '
    f'<span style="color:{RED}">how they connect</span>.</div></div>'))


# ---------------------------------------------------------------- 3 what each answers
def box(title, question):
    return (f'<div style="flex:1;border:3px solid {INK};border-radius:14px;padding:20px 14px;'
            f'text-align:center;background:{WHITE}">'
            f'<div style="font-size:25px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;'
            f'color:{TEAL}">{title}</div>'
            f'<div style="font-size:27px;font-weight:500;line-height:1.25;margin-top:10px">{question}</div>'
            f'</div>')


d.qa("What each statement actually answers.", "actually",
     '<div class="card"><div style="display:flex;gap:14px;align-items:stretch">'
     + box("Income", "Did it make a&nbsp;profit?")
     + box("Cash flow", "Did cash go up or&nbsp;down?")
     + box("Balance sheet", "What does it own and&nbsp;owe?")
     + '</div></div>',
     "Three different questions about the same business, at a point in time or over a period.",
     "Describing what each one contains instead of what each one is for.", 72)


# ---------------------------------------------------------------- 4 the links
def arrow(label):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px;flex:none">'
            f'<svg width="80" height="24" viewBox="0 0 80 24" fill="none" stroke="{RED}" '
            f'stroke-width="3.5"><path d="M0 12h68M60 5l9 7-9 7"/></svg>'
            f'<span style="font-size:21px;font-weight:600;color:{RED};white-space:nowrap">{label}</span>'
            f'</div>')


def flowbox(t):
    return (f'<div style="flex:1;border:3px solid {INK};border-radius:14px;padding:18px 10px;'
            f'text-align:center;font-size:27px;font-weight:600;line-height:1.2;background:{WHITE}">{t}</div>')


d.qa("The two links that make it one model.", "two links",
     '<div class="card"><div style="display:flex;align-items:center;gap:8px">'
     + flowbox("INCOME<br>STATEMENT") + arrow("net income")
     + flowbox("CASH FLOW<br>STATEMENT") + arrow("ending cash")
     + flowbox("BALANCE<br>SHEET") + '</div>'
     f'<div style="margin-top:16px;font-size:25px;font-weight:600;color:{TEAL};text-align:center">'
     f'net income also lands in retained earnings &rarr; equity</div></div>',
     "Net income starts the cash flow statement and feeds retained earnings. Ending cash lands on the balance sheet.",
     "Reciting the three separately. The links are the answer.", 68)

# ---------------------------------------------------------------- 5 the follow-up
d.slide(INK, WHITE, inner=(
    '<div style="display:flex;flex-direction:column;gap:32px">'
    '<div style="font-size:26px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;'
    f'color:{RED}">Then comes the real one</div>'
    f'<h1 style="font-size:92px">&ldquo;Depreciation goes up by <span style="color:#5EC8B4">10</span>. '
    f'Walk me through it<span style="color:{RED}">.</span>&rdquo;</h1>'
    '<div class="body" style="font-size:34px;font-weight:400;opacity:.85">'
    'Assume a 25% tax rate. Say that out loud before you start. Stating your '
    'assumption is part of the answer.</div></div>'))


# ---------------------------------------------------------------- 6-8 the walk
def ladder(rows, total_label, total_value, total_colour):
    out = ""
    for label, value, colour, strong in rows:
        weight = 600 if strong else 400
        out += (f'<div style="display:flex;justify-content:space-between;align-items:baseline;'
                f'padding:13px 0;border-bottom:1px solid rgba(10,10,10,.12)">'
                f'<span style="font-size:31px;font-weight:{weight}">{label}</span>'
                f'<span style="font-family:\'Serif\',serif;font-weight:700;font-size:40px;'
                f'color:{colour}">{value}</span></div>')
    out += (f'<div style="display:flex;justify-content:space-between;align-items:baseline;'
            f'padding:16px 0 2px;border-top:3px solid {INK};margin-top:6px">'
            f'<span style="font-size:33px;font-weight:600">{total_label}</span>'
            f'<span style="font-family:\'Serif\',serif;font-weight:700;font-size:50px;'
            f'color:{total_colour}">{total_value}</span></div>')
    return f'<div class="card">{out}</div>'


d.qa("Step one: the income statement.", "income statement",
     ladder([("Operating income (EBIT)", "&minus;10", RED, False),
             ("Pre-tax income", "&minus;10", RED, False),
             ("Taxes at 25%", "&minus;2.5", TEAL, False)],
            "Net income", "&minus;7.5", RED),
     "Depreciation is an expense, so EBIT falls by the full 10. The tax saving of 2.5 is real, so net income falls by 7.5.",
     "Taking net income down by the full 10 and forgetting the tax shield.", 72)

d.qa("Step two: the cash flow statement.", "cash flow statement",
     ladder([("Net income", "&minus;7.5", RED, False),
             ("Add back depreciation", "+10", TEAL, False)],
            "Cash from operations", "+2.5", TEAL),
     "Depreciation never left the building. Add it back and cash is up 2.5, which is the tax you did not pay.",
     "Forgetting the add-back, which is the entire point of the question.", 68)

d.qa("Step three: and it balances.", "balances",
     '<div class="card"><div style="display:flex;gap:18px;align-items:stretch">'
     f'<div style="flex:1">'
     f'<div style="font-size:24px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;'
     f'color:{TEAL};margin-bottom:10px">Assets</div>'
     f'<div style="font-size:30px;line-height:1.5">Cash <b style="color:{TEAL}">+2.5</b><br>'
     f'PP&amp;E <b style="color:{RED}">&minus;10</b></div>'
     f'<div style="border-top:3px solid {INK};margin-top:10px;padding-top:8px;font-size:32px;'
     f'font-weight:600">&minus;7.5</div></div>'
     f'<div style="display:flex;align-items:center;font-family:\'Serif\',serif;font-size:60px;'
     f'color:{INK}">=</div>'
     f'<div style="flex:1">'
     f'<div style="font-size:24px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;'
     f'color:{TEAL};margin-bottom:10px">Liabilities + equity</div>'
     f'<div style="font-size:30px;line-height:1.5">Liabilities <b>0</b><br>'
     f'Retained earnings <b style="color:{RED}">&minus;7.5</b></div>'
     f'<div style="border-top:3px solid {INK};margin-top:10px;padding-top:8px;font-size:32px;'
     f'font-weight:600">&minus;7.5</div></div></div></div>',
     "PP&amp;E falls by 10 and cash rises by 2.5, so assets fall 7.5. Retained earnings fall by the same 7.5.",
     "Finishing without saying it balances. Say it. That is what they are listening for.", 68)

# ---------------------------------------------------------------- 9 CTA
d.slide(RED, WHITE, accent=WHITE, cue="Save", icon=BOOKMARK, inner=(
    '<div style="display:flex;flex-direction:column;gap:34px">'
    '<h1 style="font-size:100px">Say the links out loud.</h1>'
    f'<div style="background:{WHITE};color:{INK};border-radius:16px;padding:34px 38px;'
    'display:flex;flex-direction:column;gap:14px">'
    + "".join(f'<div style="display:flex;gap:18px;align-items:baseline">'
              f'<span style="font-family:\'Serif\',serif;font-weight:700;font-size:34px;'
              f'color:{RED};width:34px;flex:none">{i}</span>'
              f'<span style="font-size:30px;line-height:1.3">{t}</span></div>'
              for i, t in enumerate(
                  ["Net income down 7.5 after the tax shield.",
                   "Add back 10, cash up 2.5.",
                   "Assets down 7.5, equity down 7.5."], 1))
    + '</div>'
    '<div class="body" style="font-size:34px;font-weight:500;opacity:.95">'
    'Tomorrow: enterprise value vs equity value.</div></div>'))

paths = d.render()
problems = check(paths, 9)
for p in paths:
    print(f"  {p.name}  {p.stat().st_size // 1024}KB")
print("PROBLEMS:", problems or "none")
