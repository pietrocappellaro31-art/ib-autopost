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


# ---------------------------------------------------------------------------
# r03, the "Why banking?" swap test. Built for watch time: the hook challenges
# the viewer's own answer, a generic answer types itself out, its key word
# spins like a slot machine and the answer survives every swap (FAILS), then
# the 3-part fix, then a specific answer that breaks when swapped (PASSES),
# then one follow ask tied to what the page actually posts.

PAPER_C = "#F7F5F2"


def typed(tokens, at, d, size=44):
    """A paragraph that types itself word by word; a token may be raw HTML."""
    words = "".join(f'<span class="w">{w}</span> ' for w in tokens)
    return A(f'<div style="font-size:{size}px;line-height:1.3;font-weight:500">{words}</div>', "words", at, d)


def roll(options, at, hold):
    opts = "".join(f"<span>{o}</span>" for o in options)
    return (f'<span class="a roll" data-fx="roll" data-at="{at}" data-hold="{hold}" '
            f'style="background:rgba(15,118,110,.2);color:#0F766E;font-weight:600">'
            f'<span class="rl">{opts}</span></span>')


def stamp(text, colour, at, rot=-8):
    return A(f'<div style="border:8px solid {colour};color:{colour};border-radius:16px;padding:6px 26px;'
             f'font-family:Serif;font-weight:700;font-size:92px;letter-spacing:.04em;background:rgba(247,245,242,.86)">'
             f'{text}</div>', "stamp", at, .4, rot=rot,
             style="position:absolute;right:30px;bottom:-62px")


def paper(inner, style=""):
    return (f'<div style="position:relative;background:{PAPER_C};color:#0A0A0A;border-radius:26px;'
            f'padding:38px 42px;margin-top:22px;{style}">{inner}</div>')


def chips_row(items, colour, ink, at0, step):
    return ('<div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:30px">'
            + "".join(A(c, "pop", at0 + k * step, .35,
                        style=f"background:{colour};color:{ink};font-size:38px;font-weight:600;"
                              "padding:14px 26px;border-radius:999px;white-space:nowrap")
                      for k, c in enumerate(items)) + '</div>')


def part(n, title, sub, examples):
    dots = "".join(
        (A("", "pop", .15, .4, style=f"width:60px;height:10px;border-radius:5px;background:{TEAL}") if k == n
         else f'<span style="width:60px;height:10px;border-radius:5px;background:'
              f'{TEAL if k < n else "rgba(255,255,255,.2)"}"></span>')
        for k in range(1, 4))
    return dict(dur=3.7, enter="right", exit="left", html=(
        '<div style="height:900px">'
        f'<div style="display:flex;gap:12px;margin-bottom:70px">{dots}</div>'
        + f'<div style="display:flex;align-items:center;gap:26px">'
          f'<div style="width:96px;height:96px;border-radius:50%;background:{TEAL};color:#0A0A0A;'
          f'display:flex;align-items:center;justify-content:center;font-family:Serif;font-weight:700;'
          f'font-size:60px">{n}</div><div class="lbl">Part {n}</div></div>'
        + f'<h1 style="font-size:100px;margin-top:40px">{title}<span class="r">.</span></h1>'
        + A(f'<div class="sub" style="font-size:46px">{sub}</div>', "rise", .35, .45)
        + A('<div class="lbl" style="margin-top:64px">For example</div>', "fade", .9, .3)
        + chips_row(examples, "rgba(255,255,255,.1)", "#fff", 1.05, .22)
        + '</div>'))


def r03():
    s = []
    # 1. Hook, readable at frame 0; the red pen circles "fails" after.
    s.append(dict(dur=2.9, exit="left", html=(
        '<h1 style="font-size:100px">Your <span class="t">&ldquo;Why banking?&rdquo;</span> answer '
        '<span style="position:relative;display:inline-block" class="r">fails'
        '<svg class="a pen" data-fx="draw" data-at=".35" data-d=".55" data-c="#D93A12" width="0" height="0" '
        'style="position:absolute;left:0;top:0"></svg></span> this test<span class="r">.</span></h1>'
        '<div class="sub">Try it on yours. It takes 10 seconds.</div>')))

    # 2. The safe answer types out, then its key word spins through other jobs.
    generic = (["I", "want", "to", "work", "in", roll(["investment banking", "consulting", "tech", "law"], 4.9, 1.0)]
               + "because I want a steep learning curve, real responsibility early and smart people around me.".split())
    s.append(dict(dur=10.6, enter="right", exit="left", html=(
        '<div style="height:1000px">'
        + A('<div class="lbl">The safe answer</div>', "fade", -1, .3)
        + paper(typed(generic, .25, 3.0)
                + stamp("FAILS", RED, 7.6, rot=-7), style="min-height:400px;box-sizing:border-box;padding-bottom:60px")
        + A('<div class="sub" style="font-size:46px;margin-top:92px">Sounds fine. Now swap one word.</div>', "rise", 3.7, .45)
        + chips_row(["Consulting &#10003;", "Tech &#10003;", "Law &#10003;"], TEAL, "#0A0A0A", 5.35, 1.0)
        + A('<div class="sub" style="font-size:46px;margin-top:40px">If it works for any job, '
            '<span class="r">it isn&rsquo;t an answer.</span></div>', "rise", 8.3, .45)
        + '</div>')))

    # 3. Bridge to the fix.
    s.append(dict(dur=1.9, enter="right", exit="left", html=(
        '<div style="display:flex;align-items:baseline;gap:30px">'
        + A(f'<span class="num" style="font-size:380px;line-height:.9;color:{TEAL}">3</span>', "pop", .05, .5)
        + '<h1 style="font-size:110px">parts<span class="r">.</span></h1></div>'
        + '<div class="sub" style="font-size:48px">Every answer that passes has them.</div>')))

    # 4-6. The parts.
    s.append(part(1, "Where it started", "One specific moment. Not &ldquo;an interest in markets.&rdquo;",
                  ["A deal you followed", "A company you watched get bought"]))
    s.append(part(2, "What you did about it", "The proof that part 1 really happened.",
                  ["A model you built", "A stock pitch", "A club you ran"]))
    s.append(part(3, "Why this seat", "Why banking, and not the next closest thing.",
                  ["Not equity research", "Not consulting"]))

    # 7. A specific answer, the same swap, and this time it breaks.
    strong = ("Watching Broadcom buy VMware, I wanted to know why a chip company would pay that much "
              "for software. So I built the model.").split() + [
        roll(["Banking", "Consulting"], 2.6, 1.0), "is",
        '<span style="position:relative;display:inline-block">'
        + A("", "wipe", 3.25, .4, style="position:absolute;left:-4px;right:-4px;top:4px;bottom:2px;"
            "background:rgba(217,58,18,.22);border-radius:8px")
        + "where&nbsp;I&rsquo;d&nbsp;be&nbsp;on&nbsp;the&nbsp;deal,</span>"] + "not reading about it after.".split()
    s.append(dict(dur=7.4, enter="right", exit="left", html=(
        '<div style="height:1000px">'
        + A('<div class="lbl" style="color:#5EC8B4;opacity:1">A specific answer</div>', "fade", -1, .3)
        + paper(typed(strong, .15, 1.9, size=42) + stamp("PASSES", "#0F766E", 4.3, rot=-6),
                style="min-height:440px;box-sizing:border-box;padding-bottom:60px")
        + A('<div class="sub" style="font-size:46px;margin-top:92px">Swap the word and it breaks.</div>', "rise", 2.2, .45)
        + chips_row(["Consulting &#10007; doesn&rsquo;t fit"], RED, "#fff", 3.6, .2)
        + A('<div class="sub" style="font-size:46px;margin-top:36px">That&rsquo;s the test. '
            '<span class="t">Specific survives.</span></div>', "rise", 5.0, .45)
        + '</div>')))

    # 8. Close and the one ask.
    s.append(dict(dur=4.8, enter="right", html=(
        '<h1 style="font-size:92px">Run the swap on yours tonight<span class="r">.</span></h1>'
        + A('<div style="display:flex;align-items:center;gap:26px;margin-top:80px;background:rgba(255,255,255,.07);'
            'border:3px solid rgba(255,255,255,.2);border-radius:28px;padding:30px">'
            f'<div style="width:110px;height:110px;border-radius:50%;background:{RED};display:flex;align-items:center;'
            'justify-content:center;font-family:Serif;font-weight:700;font-size:48px;color:#fff;flex:none">IB'
            '<span style="color:#0A0A0A">.</span></div>'
            '<div style="min-width:0"><div style="font-size:34px;font-weight:600">investmentbankinginterviews</div>'
            '<div style="font-size:32px;opacity:.7;margin-top:6px">2 interview questions a day</div></div></div>',
            "rise", .5, .5)
        + '<div style="position:relative;margin-top:30px">'
        + A(A(f'<div style="position:relative;overflow:hidden;border-radius:18px;background:{TEAL};color:#0A0A0A;'
              'font-size:44px;font-weight:600;text-align:center;padding:26px">'
              + A("Follow", "fade", -1, .1, style="position:relative")
              + A("", "ripple", 2.0, .7, style="position:absolute;left:50%;top:50%;width:300px;height:300px;"
                  "margin:-150px 0 0 -150px;border-radius:50%;background:#fff")
              + '</div>', "press", 2.0, .35)
            + A('<div style="position:absolute;inset:0;border-radius:18px;background:#16201E;'
                'border:3px solid rgba(94,200,180,.6);color:#fff;font-size:44px;font-weight:600;'
                'display:flex;align-items:center;justify-content:center">Following &#10003;</div>',
                "fade", 2.3, .1, style="position:absolute;inset:0"),
            "rise", .9, .5)
        + '</div>')))
    return s


REELS["w1-r03-why-banking"] = r03


# ---------------------------------------------------------------------------
# Kinetic style, from the 3 Nov reference Reel (see docs/reel-style.md):
# paper ground, lockups of small sans + huge serif accent + italic tail,
# letters revealed out of a blur, whip transitions, slow push-in, marker
# highlights, soft shadowed cards. A new beat every 2 to 3 seconds.

INK_C, TEAL_D = "#0A0A0A", "#0F766E"
SHADOW = "0 34px 70px rgba(10,10,10,.13), 0 8px 18px rgba(10,10,10,.07)"


def ch(text, at, size, cls="", colour="", st=.032, cd=.38, extra=""):
    """Text that reveals letter by letter out of a blur. Words never break.

    Takes plain text (real quotes and apostrophes, no HTML entities). Long
    lines reveal faster, so every line finishes within about a second.
    """
    import html as _h
    text = _h.unescape(text)
    st = min(st, .95 / max(len(text), 1))
    words = []
    for w in text.split(" "):
        words.append('<span class="wd">' + "".join(f'<span class="c">{_h.escape(c)}</span>' for c in w) + "</span>")
    style = f"font-size:{size}px;{('color:' + colour + ';') if colour else ''}{extra}"
    return A(" ".join(words), "chars", at, 1, cls=cls, style=style, st=st, cd=cd)


def swoosh(at, colour=TEAL_D, width=520):
    return (f'<svg class="a" data-fx="draw" data-at="{at}" data-d=".5" width="{width}" height="40" '
            f'viewBox="0 0 {width} 40" style="display:block;margin-top:-6px;overflow:visible">'
            f'<path d="M6 26 C {width*.25:.0f} 8, {width*.55:.0f} 34, {width - 8} 12" fill="none" stroke="{colour}" '
            'stroke-width="9" stroke-linecap="round"/></svg>')


def marked(text, at, colour="rgba(217,58,18,.24)"):
    return ('<span style="position:relative;display:inline;white-space:nowrap">'
            + f'<span class="a" data-fx="wipe" data-at="{at}" data-d=".45" style="position:absolute;left:-6px;right:-6px;'
            f'top:12%;bottom:4%;background:{colour};border-radius:8px;z-index:0"></span>'
            + f'<span style="position:relative;z-index:1">{text}</span></span>')


def wrong(n, before, phrase, after):
    return dict(dur=2.4, enter="whip", exit="whip", push=.035, html=(
        '<div style="display:flex;align-items:baseline;gap:18px;margin-bottom:34px">'
        + ch(f"0{n}", -.28, 64, cls="num", colour="#D93A12", st=.06)
        + ch("/ 05", -.2, 40, cls="num", extra="opacity:.35")
        + A('<span class="lbl" style="margin-left:18px">You say</span>', "fade", -.15, .3) + '</div>'
        + A(f'<div style="position:relative;background:#fff;border-radius:30px;padding:46px 44px 54px;margin:0 14px;'
            f'box-shadow:{SHADOW};transform:rotate(-1.6deg)">'
            f'<div style="font-size:58px;line-height:1.25;font-weight:500">&ldquo;{before}{marked(phrase, .6)}{after}&rdquo;</div>'
            + A('<div style="width:104px;height:104px;border-radius:50%;background:#D93A12;color:#fff;display:flex;'
                'align-items:center;justify-content:center;font-size:62px;font-weight:600">&#10007;</div>',
                "stamp", 1.0, .35, rot=-6, style="position:absolute;right:18px;top:-46px")
            + '</div>', "rise", -.3, .45)))


def fix(top, big, tail, big_size, count=None):
    big_el = (count(big_size) if count else ch(big, .12, big_size, cls="num", colour=TEAL_D, st=.045))
    return dict(dur=2.7, enter="whip", exit="whip", push=.04, html=(
        A('<div class="lbl" style="color:#0F766E;opacity:1;margin-bottom:30px">Say instead</div>', "fade", -.3, .3)
        + ch(top, -.22, 60, extra="font-weight:500")
        + f'<div style="line-height:1;margin:8px 0 4px">{big_el}</div>'
        + swoosh(.7)
        + ch(tail, .8, 54, cls="it", extra="line-height:1.25;margin-top:22px")))


def r04():
    s = []
    rings = "".join(
        A("", "ripple", k * .4, 1.8, style="position:absolute;left:50%;top:50%;width:620px;height:620px;"
          "margin:-310px 0 0 -310px;border-radius:50%;border:5px solid rgba(217,58,18,.5);z-index:0")
        for k in range(2))
    s.append(dict(dur=2.9, exit="zoom", push=.04, html=(
        f'<div style="position:relative">{rings}<div style="position:relative;z-index:1">'
        + ch("5 answers that get you", .05, 60, extra="font-weight:500")
        + f'<div style="line-height:.95;margin:6px 0 10px">{ch("dinged.", .45, 200, cls="num", colour="#D93A12", st=.06)}</div>'
        + ch("and the line that fixes each one", 1.05, 58, cls="it")
        + '</div></div>')))
    s.append(dict(wrong(1, "A DCF, because it&rsquo;s the ", "most accurate", "."), enter="zoomin"))
    s.append(fix("It\u2019s the most", "assumption-heavy", "method you have. Say that.", 80))
    s.append(wrong(2, "Add cash to get ", "enterprise value", "."))
    s.append(fix("You", "subtract", "the cash. It comes with the company.", 170))
    s.append(wrong(3, "Depreciation up 10, so ", "net income down 10", "."))
    s.append(fix("Net income falls", "", "at a 25% tax rate. The tax shield is real.", 0,
                 count=lambda size: A("10.0", "count", .25, 1.0, cls="num",
                                      style=f"font-size:240px;color:{TEAL_D}",
                                      **{"from": 10, "to": 7.5, "dec": 1, "pre": "", "suf": "", "show": 1})))
    s.append(wrong(4, "Goodwill is the ", "premium paid", "."))
    s.append(fix("Purchase price", "minus", "the fair value of the net identifiable assets.", 180))
    s.append(wrong(5, "No, I think you ", "covered everything", "."))
    s.append(fix("Always bring", "one question", "about something they actually worked on.", 116))
    star = ('<svg viewBox="0 0 100 100" width="90" height="90"><path d="M50 0 C54 38 62 46 100 50 C62 54 54 62 50 100 '
            'C46 62 38 54 0 50 C38 46 46 38 50 0Z" fill="#D93A12"/></svg>')
    s.append(dict(dur=3.6, enter="zoomin", push=.03, html=(
        A(star, "spin", 0, 1, deg=50, style="position:absolute;right:24px;top:12px")
        + ch("Every fix costs you", -.25, 60, extra="font-weight:500")
        + f'<div style="line-height:1;margin:8px 0 10px">{ch("one sentence.", .45, 132, cls="num", st=.04)}</div>'
        + swoosh(1.2, "#D93A12", 600)
        + ch("Save this for the night before.", 1.4, 56, cls="it", extra="margin-top:24px"))))
    return s


REELS["w1-r04-dinged"] = r04

if __name__ == "__main__":
    for slug in sys.argv[1:] or list(REELS):
        print(slug)
        opts = {"w1-r04-dinged": dict(theme="paper", cover_at=2.4)}.get(slug, {})
        build(slug + "-motion", REELS[slug](), **opts)
