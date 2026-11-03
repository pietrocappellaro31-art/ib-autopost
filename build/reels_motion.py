"""
Animated Reels. Same copy rules as the carousels: every number is worked
through, no em dashes, nothing invented.

r01, EV vs equity value. The worked example matches the caption exactly:
$50 a share x 100M diluted shares = $5.0B equity value; + $1.0B debt,
- $0.2B cash = $5.8B enterprise value. Adding the cash instead gives $6.2B,
which is $400M off.
"""

import sys

from motion import A, build

TEAL, RED = "#5EC8B4", "#D93A12"


def num(text, size, colour="#fff", extra=""):
    return f'<span class="num" style="font-size:{size}px;color:{colour};{extra}">{text}</span>'


def count(frm, to, at, d, size, colour, dec=1, pre="$", suf="B", style="", **more):
    return A(f"{pre}{frm:.{dec}f}{suf}", "count", at, d, cls="num",
             style=f"font-size:{size}px;color:{colour};{style}",
             **{"from": frm, "to": to, "dec": dec, "pre": pre, "suf": suf}, **more)


def r01():
    s = []

    # 1. Hook. Fully composed at t=0 because frame 0 is the cover.
    s.append(dict(dur=4.0, ghost="?", html=(
        '<h1>Enterprise value<br>vs <span class="t" style="position:relative;display:inline-block">'
        'equity value'
        + A("", "growX", 0.3, 0.8, style="position:absolute;left:0;right:0;bottom:-6px;height:9px;"
            f"background:{TEAL};border-radius:5px")
        + '</span><span class="r">.</span></h1>'
        '<div class="sub">Get it backwards and the interview ends early.</div>')))

    # 2. Equity value: price x shares, the grid fills, the total counts up.
    squares = "".join(
        A("", "pop", 0.9 + i * 0.011, 0.28,
          style=f"width:30px;height:30px;border-radius:6px;background:{TEAL}")
        for i in range(100))
    s.append(dict(dur=5.2, ghost="1", html=(
        A('<h1>Equity value<span class="r">.</span></h1>', "rise", 0, .5)
        + A('<div class="sub">What the shareholders own.</div>', "rise", .25, .5)
        + '<div style="display:flex;gap:44px;margin-top:60px;align-items:flex-end">'
          '<div><div style="display:grid;grid-template-columns:repeat(10,30px);gap:6px">'
        + squares + '</div>'
        + A('<div class="lbl" style="margin-top:18px">1 square = 1M shares</div>', "fade", 2.0, .4)
        + '</div><div style="flex:1;display:flex;flex-direction:column;gap:22px">'
        + A('<div class="lbl">Share price</div>' + num("$50", 76), "rise", 0.9, .5)
        + A('<div class="lbl">&times; Diluted shares</div>' + num("100M", 76), "rise", 1.4, .5)
        + A("", "growX", 2.1, .5, style="height:3px;background:rgba(255,255,255,.45)")
        + A('<div class="lbl" style="color:#5EC8B4;opacity:1">= Equity value</div>', "fade", 2.3, .4)
        + count(0, 5.0, 2.4, 1.1, 100, TEAL)
        + '</div></div>')))

    # 3. Enterprise value: one business, two claims on it.
    s.append(dict(dur=4.4, ghost="2", html=(
        A('<h1><span class="t">Enterprise value</span><span class="r">.</span></h1>', "rise", 0, .5)
        + A('<div class="sub">What it costs to buy the whole business, whoever financed it.</div>',
            "rise", .25, .5)
        + '<div style="position:relative;height:380px;margin-top:54px">'
        + A("", "rise", 0.9, .6, style="position:absolute;inset:0;border:3px solid rgba(255,255,255,.55);"
            "border-radius:22px")
        + A("", "fade", 1.5, .5, style="position:absolute;left:3px;right:3px;top:3px;height:282px;"
            "border-radius:19px 19px 0 0;background:rgba(94,200,180,.2)")
        + A("", "growX", 1.5, .5, style="position:absolute;left:3px;right:3px;top:285px;height:3px;"
            "background:rgba(255,255,255,.55)")
        + A('<div class="lbl" style="opacity:1;color:#5EC8B4">Shareholders</div>'
            '<div style="font-size:38px;font-weight:500;margin-top:8px">Equity</div>',
            "rise", 1.8, .5, style="position:absolute;left:36px;top:36px")
        + A('<div style="font-size:36px;font-weight:600">Lenders <span style="opacity:.6;font-weight:500">'
            'Debt</span></div>', "rise", 2.2, .5, style="position:absolute;left:36px;top:308px")
        + '</div>')))

    # 4. The bridge, row by row. Cash is the one that subtracts.
    def row(label, value, colour, at, hl=False):
        box = (A("", "pop", 2.2, .45, style=f"position:absolute;inset:-4px -18px;border:4px solid {RED};"
                 "border-radius:16px") if hl else "")
        return A(f'<div class="row" style="position:relative"><span>{label}</span>'
                 f'<b style="color:{colour}">{value}</b>{box}</div>', "rise", at, .45)
    s.append(dict(dur=4.4, ghost="3", html=(
        A('<h1>The bridge<span class="r">.</span></h1>', "rise", 0, .5)
        + '<div class="card">'
        + row("Equity value", "start", "#fff", .5)
        + row("Debt", "+", "#fff", .85)
        + row("Preferred, NCI", "+", "#fff", 1.2)
        + row("Cash", "&minus;", RED, 1.55, hl=True)
        + '</div>')))

    # 5. Waterfall with the numbers. 100px per $1B.
    base = 112

    def bar(x, bottom, h, colour, at, d, down=False, outline=False):
        fill = (f"border:3px solid {colour};background:rgba(255,255,255,.08)" if outline
                else f"background:{colour}")
        return A("", "growYdown" if down else "growY", at, d,
                 style=f"position:absolute;left:{x}px;width:152px;bottom:{bottom}px;height:{h}px;"
                       f"border-radius:8px;{fill}")

    def link(x, y, at):
        return A("", "growX", at, .35, style=f"position:absolute;left:{x}px;width:48px;bottom:{y}px;"
                 "border-top:3px dashed rgba(255,255,255,.5)")

    def label(x, bottom, inner, at, fx="fade"):
        return A(inner, fx, at, .4, style=f"position:absolute;left:{x}px;width:152px;bottom:{bottom}px;"
                 "text-align:center")

    def cat(x, text, colour="#fff"):
        return (f'<div style="position:absolute;left:{x}px;width:152px;bottom:0;height:{base - 20}px;'
                f'text-align:center;font-size:30px;font-weight:600;line-height:1.2;color:{colour}">{text}</div>')

    s.append(dict(dur=5.8, ghost="4", html=(
        A('<h1 style="font-size:92px">Run the numbers<span class="r">.</span></h1>', "rise", 0, .5)
        + '<div style="position:relative;height:800px;margin-top:30px">'
        + f'<div style="position:absolute;left:0;right:0;bottom:{base - 6}px;height:3px;'
          'background:rgba(255,255,255,.3)"></div>'
        + bar(0, base, 500, "#fff", .6, .7)
        + A(count(0, 5.0, .6, .7, 46, "#fff"), "move", .6, .7, style=f"position:absolute;left:0;width:152px;bottom:{base + 514}px;text-align:center", y=500)
        + link(152, base + 500, 1.4)
        + bar(200, base + 500, 100, "#fff", 1.6, .5, outline=True)
        + label(200, base + 614, num("+$1.0B", 46), 1.7)
        + link(352, base + 600, 2.2)
        + bar(400, base + 580, 20, RED, 2.4, .4, down=True)
        + label(400, base + 614, num("&minus;$0.2B", 46, RED), 2.4, "pop")
        + link(552, base + 580, 3.0)
        + bar(600, base, 580, TEAL, 3.2, .8)
        + A(count(0, 5.8, 3.2, .8, 46, TEAL), "move", 3.2, .8, style=f"position:absolute;left:600px;width:152px;bottom:{base + 594}px;text-align:center", y=580)
        + cat(0, "Equity<br>value") + cat(200, "+ Debt") + cat(400, "&minus; Cash", RED)
        + cat(600, "Enterprise<br>value", TEAL)
        + '</div>')))

    # 6. Why subtract?
    s.append(dict(dur=3.8, ghost="5", html=(
        A('<h1>Why <span class="t">subtract</span><br>cash<span class="r">?</span></h1>', "rise", 0, .5)
        + '<div style="display:flex;gap:56px;margin-top:70px;align-items:center">'
        + A('<span style="position:relative;display:inline-block">' + num("+ Cash", 110, "rgba(255,255,255,.8)")
            + A("", "strike", 1.4, .45, style=f"position:absolute;left:-8px;right:-8px;top:52%;height:10px;"
                f"background:{RED};border-radius:5px") + '</span>', "rise", .7, .5)
        + A(num("&minus; Cash", 110, TEAL), "pop", 2.1, .5)
        + '</div>')))

    # 7. Because the cash comes with the company and pays down the debt.
    s.append(dict(dur=4.6, ghost="6", html=(
        A('<h1 style="font-size:88px">It comes with the company<span class="r">.</span></h1>', "rise", 0, .5)
        + A('<div class="sub">You use it to repay the debt you borrowed to buy it.</div>', "rise", .25, .5)
        + '<div class="a" data-fx="rise" data-at=".5" data-d=".5" style="position:relative;height:300px;margin-top:56px">'
        + '<div style="position:absolute;left:0;top:0;width:340px;height:300px;border-radius:22px;box-sizing:border-box;'
          'border:3px solid rgba(255,255,255,.4)"><div class="lbl" style="margin:28px 30px">The company</div></div>'
        + '<div style="position:absolute;left:412px;top:0;width:340px;height:300px;border-radius:22px;box-sizing:border-box;'
          'border:3px solid rgba(255,255,255,.4)"><div class="lbl" style="margin:28px 30px">The debt</div>'
        + '<div style="position:absolute;left:30px;top:84px">'
        + count(1.0, 0.8, 2.4, .8, 84, "#fff", show=1) + '</div></div>'
        + A(f'<div style="background:{TEAL};color:#0A0A0A;border-radius:14px;padding:16px 22px;'
            'font-size:34px;font-weight:600;white-space:nowrap">$0.2B cash</div>',
            "move", 1.2, 1.1, style="position:absolute;left:442px;top:200px", x=-412, y=-60)
        + '</div>')))

    # 8. The answer, and what adding it costs you.
    s.append(dict(dur=4.6, ghost="7", html=(
        A('<h1 style="font-size:96px">You <span class="t">subtract</span> the cash'
          '<span class="r">.</span></h1>', "rise", 0, .5)
        + '<div style="display:flex;gap:56px;margin-top:64px;align-items:center">'
        + A('<span style="position:relative;display:inline-block">' + num("$6.2B", 110, "rgba(255,255,255,.55)")
            + A("", "strike", 1.3, .45, style=f"position:absolute;left:-8px;right:-8px;top:52%;height:10px;"
                f"background:{RED};border-radius:5px") + '</span>', "rise", .6, .5)
        + A(num("$5.8B", 110, TEAL), "pop", 1.8, .5)
        + '</div>'
        + A("<div class=\"sub\">Add it instead and you're $400M off.</div>", "rise", 2.4, .5)
        )))
    return s


REELS = {"w1-r01-ev-equity": r01}


# ---------------------------------------------------------------------------
# r06, 8 words that give you away. Each vague word is circled in red pen,
# then blank cards flip to show the precise versions, so the viewer gets a
# beat to guess first. The counter and the sideways swipe make it read as a
# run of eight, which is what keeps people to the end.

WORDS = [
    ("Profit", ["Net income", "EBIT", "EBITDA"], "Three different lines. Name one."),
    ("Valuation", ["Enterprise value", "Equity value"], "The bridge between them is the question."),
    ("Cash flow", ["Operating", "Levered FCF", "Unlevered FCF"], "Levered: cost of equity. Unlevered: WACC."),
    ("Debt", ["Gross", "Net"], "Net subtracts the cash."),
    ("Multiple", ["EV / EBITDA", "P / E"], "Of what, and LTM or forward?"),
    ("Margin", ["Gross", "EBITDA", "Net"], "Same revenue, three different percentages."),
    ("Shares", ["Basic", "Diluted"], "Equity value uses diluted."),
    ("Return", ["IRR", "MOIC"], "IRR counts time. MOIC doesn't."),
]


def counter(i):
    dots = ""
    for k in range(8):
        if k < i:
            dots += f'<span style="width:16px;height:16px;border-radius:50%;background:{TEAL}"></span>'
        elif k == i:
            dots += A("", "pop", .1, .4, style=f"width:24px;height:24px;border-radius:50%;background:{TEAL}")
        else:
            dots += '<span style="width:16px;height:16px;border-radius:50%;border:3px solid rgba(255,255,255,.3);box-sizing:border-box"></span>'
    return ('<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:76px">'
            + num(f'{i + 1:02d}<span style="opacity:.35"> / 08</span>', 58)
            + f'<div style="display:flex;align-items:center;gap:12px">{dots}</div></div>')


def chip(text, at):
    real = A(text, "flipin", at + .18, .32,
             style=f"background:{TEAL};color:#0A0A0A;font-size:46px;font-weight:600;padding:18px 32px;"
                   "border-radius:999px;white-space:nowrap")
    blank = A(A('<span style="font-family:Serif;font-size:46px;color:rgba(255,255,255,.55)">?</span>',
                "flipout", at, .2, style="position:absolute;inset:0;display:flex;align-items:center;"
                "justify-content:center;border:3px dashed rgba(255,255,255,.4);border-radius:999px"),
              "fade", .85, .25, style="position:absolute;inset:0")
    return f'<div style="position:relative">{real}{blank}</div>'


def word_scene(i, word, precise, why):
    chips = "".join(chip(c, 1.2 + j * .16) for j, c in enumerate(precise))
    return dict(dur=4.0, enter="right", exit="left", html=(
        '<div style="height:980px">' + counter(i)
        + A('<div class="lbl">You say</div>', "fade", -1, .3)
        + '<div>' + A(
            '<div style="display:inline-block;position:relative;background:rgba(255,255,255,.07);'
            'border:3px solid rgba(255,255,255,.22);border-radius:30px;padding:28px 38px;margin-top:20px">'
            '<span style="position:relative;display:inline-block;font-family:Serif;font-weight:700;'
            f'font-size:114px;letter-spacing:-.03em;line-height:1.05">&ldquo;{word}&rdquo;'
            '<svg class="a pen" data-fx="draw" data-at=".45" data-d=".5" width="0" height="0" style="position:absolute;left:0;top:0"></svg></span></div>',
            "pop", -1, .45, style="display:inline-block;transform-origin:left center") + '</div>'
        + A('<div class="lbl" style="color:#5EC8B4;opacity:1;margin-top:88px">Say which</div>', "fade", .8, .3)
        + f'<div style="display:flex;flex-wrap:wrap;gap:18px;margin-top:26px">{chips}</div>'
        + A(f'<div class="sub" style="font-size:48px;margin-top:60px">{why}</div>', "rise", 1.85, .45) + '</div>'))


def r06():
    s = []
    spots = [(16, 70), (300, 30), (490, 160), (120, 250), (30, 880), (420, 900), (170, 1050), (470, 1080)]
    floats = "".join(
        A(f'<span style="font-family:Serif;font-weight:700;font-size:46px;opacity:.28">&ldquo;{w}&rdquo;</span>',
          "float", 0, 1, style=f"position:absolute;left:{x}px;top:{y}px;white-space:nowrap",
          amp=9 + k % 3 * 3, w=.9 + k % 4 * .15, ph=k * 1.3)
        for k, ((w, _, _), (x, y)) in enumerate(zip(WORDS, spots)))
    s.append(dict(dur=3.6, exit="left", html=(
        '<div style="position:relative;height:1210px">' + floats
        + '<div style="position:absolute;left:0;right:0;top:400px">'
          '<h1 style="font-size:100px">8 words that give you <span class="r">away</span>.</h1>'
          '<div class="sub">The vague version says you haven&rsquo;t done the reading.</div>'
        + A('<div class="lbl" style="color:#5EC8B4;opacity:1;margin-top:40px">Guess each one before it flips</div>',
            "rise", 1.3, .45)
        + '</div></div>')))
    for i, (w, p, why) in enumerate(WORDS):
        s.append(word_scene(i, w, p, why))
    grid = "".join(
        A(f'<span style="position:relative;display:inline-block;font-family:Serif;font-weight:700;font-size:58px;'
          f'color:rgba(255,255,255,.8)">&ldquo;{w}&rdquo;'
          + A("", "strike", .45 + k * .08, .28, style=f"position:absolute;left:-6px;right:-6px;top:54%;height:8px;"
              f"background:{RED};border-radius:4px") + '</span>', "pop", -1, .35)
        for k, (w, _, _) in enumerate(WORDS))
    s.append(dict(dur=4.8, enter="right", html=(
        f'<div style="display:grid;grid-template-columns:1fr 1fr;row-gap:26px;column-gap:24px">{grid}</div>'
        + A('<h1 style="font-size:96px;margin-top:70px">Say which one<span class="r">.</span><br>'
            '<span class="t">Every time.</span></h1>', "rise", 1.4, .5)
        + A('<div class="lbl" style="margin-top:36px">Save this</div>', "fade", 2.2, .4))))
    return s


REELS["w1-r06-words"] = r06

if __name__ == "__main__":
    for slug in sys.argv[1:] or list(REELS):
        print(slug)
        build(slug + "-motion", REELS[slug]())
