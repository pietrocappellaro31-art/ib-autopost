"""
Suspense Reel: "Your DCF is a balloon". Mirrors the 4 Nov reference (a macro
shot of a balloon, a needle creeping down, "FRAMES TO IMPACT" counting down,
then the fourth wall: "You just watched a balloon for 7 seconds... still
here, waiting for it to pop", a pivot, and only then the pop).

Ours pivots to valuation: the balloon is your DCF, the needle is WACC.
Worked example, a growing perpetuity: $300M of cash flow growing at 2%.
At an 8% WACC: 300 / (8% - 2%) = $5.0B. At 9%: 300 / 7% = $4.29B, about
$4.3B. One point of WACC takes $714M off. Nothing else is claimed.

    python build/reels_pop.py
"""

from motion import A, build
from reels_motion import ch

RED, INK = "#D93A12", "#0A0A0A"
TXT = "text-shadow:0 2px 18px rgba(0,0,0,.55)"


def art(inner, z=1):
    return (f'<div class="nochk" style="position:absolute;left:-84px;top:-230px;width:1080px;height:1920px;'
            f'z-index:{z};pointer-events:none">{inner}</div>')


def place(html, x, y, z=4, extra=""):
    """Position in frame coordinates."""
    return f'<div style="position:absolute;left:{x - 84}px;top:{y - 230}px;z-index:{z};{extra}">{html}</div>'


def row(*parts, gap=18):
    return f'<div style="display:flex;justify-content:center;align-items:baseline;gap:{gap}px;flex-wrap:wrap">{"".join(parts)}</div>'


def line_block(at, d, html):
    return A(html, "life", at, d, style=f"position:absolute;left:0;right:0;top:600px;text-align:center;z-index:6;{TXT}")


def balloon():
    dent = A(A('<div style="width:120px;height:44px;border-radius:50%;'
               'background:radial-gradient(ellipse at 50% 40%,rgba(25,4,0,.92),rgba(90,18,4,.55) 55%,rgba(217,58,18,0) 72%);'
               'box-shadow:0 3px 0 rgba(255,170,130,.35)"></div>',
               "scale", 20.4, 2.0, s0=1, s1=1.7, style="transform-origin:50% 0"),
             "scale", 3.2, 3.8, s0=.05, s1=1, style="position:absolute;left:240px;top:-6px;transform-origin:50% 0")
    grid = A('<div style="position:absolute;inset:0;border-radius:50%;overflow:hidden;'
             'background:repeating-linear-gradient(0deg,rgba(255,255,255,.22) 0 2px,transparent 2px 28px),'
             'repeating-linear-gradient(90deg,rgba(255,255,255,.22) 0 2px,transparent 2px 56px)"></div>',
             "life", 15.6, 20, fi=.6, style="position:absolute;inset:0")
    body = ('<div style="position:absolute;left:240px;top:600px;width:600px;height:600px;border-radius:50%;'
            'background:radial-gradient(circle at 36% 28%,#ff9a6c 0%,#e8501f 30%,#D93A12 52%,#6e1a05 100%);'
            'box-shadow:0 0 140px rgba(217,58,18,.35),inset -30px -40px 90px rgba(40,6,0,.55)">'
            '<div style="position:absolute;left:120px;top:90px;width:150px;height:80px;border-radius:50%;'
            'background:rgba(255,235,220,.55);filter:blur(14px);transform:rotate(-30deg)"></div>'
            + grid + dent +
            f'<div style="position:absolute;left:286px;top:596px;width:28px;height:26px;background:#8a2208;'
            'clip-path:polygon(50% 0,100% 100%,0 100%)"></div></div>')
    # Macro push: scale about the top of the balloon, which is where the needle lands.
    return A(body, "scale", 2.3, 1.3, s0=1, s1=2.8,
             style="position:absolute;inset:0;transform-origin:540px 600px")


def needle():
    shaft = ('<div style="width:8px;height:820px;background:linear-gradient(90deg,#5c5c5c,#f2f2f2 45%,#8a8a8a);'
             'clip-path:polygon(0 0,100% 0,100% 94%,50% 100%,0 94%)"></div>')
    n = A(A(A(shaft, "slide", 20.4, 2.0, ease="inout", y0=0, y1=40),
            "slide", 3.4, 3.6, y0=0, y1=36),
          "slide", .2, 2.3, ease="inout", y0=0, y1=400,
          style="position:absolute;left:536px;top:-620px;z-index:3")
    return n


def bracket(x, y, rot):
    return place('<div style="width:70px;height:70px;border-left:4px solid rgba(255,255,255,.55);'
                 f'border-top:4px solid rgba(255,255,255,.55);transform:rotate({rot}deg)"></div>', x, y, 5)


def r_pop():
    s = []
    hud = A('<div style="position:absolute;left:0;right:0;top:0;display:flex;justify-content:space-between;'
            'font-size:26px;font-weight:600;letter-spacing:.12em">'
            '<span><span style="color:#ff4b2b">&#9679;</span> '
            + A("REC 00:00:00", "count", 0, 7, cls="", style="display:inline", **{"from": 0, "to": 7, "lin": 1, "pad": 2,
                                                                              "pre": "REC 00:00:", "suf": "", "show": 1})
            + '</span><span style="opacity:.7">100MM MACRO</span></div>'
            + '<div style="position:absolute;left:0;right:0;top:880px;text-align:center">'
              '<div style="font-size:24px;font-weight:600;letter-spacing:.2em;opacity:.7">FRAMES TO IMPACT</div>'
            + A("200", "count", 0, 7, cls="num", style=f"font-size:110px;line-height:1.05;{TXT}",
                **{"from": 200, "to": 1, "lin": 1, "pad": 3, "pre": "", "suf": "", "show": 1})
            + '</div>', "life", -1, 8.2, fo=.35, style="position:absolute;inset:0;z-index:6")
    brackets = A(bracket(110, 300, 0) + bracket(900, 300, 90) + bracket(110, 1370, -90) + bracket(900, 1370, 180),
                 "life", -1, 8.2, fo=.35, cls="nochk", style="position:absolute;inset:0")
    watching = A('<div style="display:inline-flex;align-items:center;gap:10px;background:rgba(0,0,0,.45);'
                 'border:2px solid rgba(255,255,255,.2);border-radius:999px;padding:10px 22px;font-size:28px;font-weight:600">'
                 '<span style="color:#ff4b2b">&#9679;</span> watching '
                 + A("7.3s", "count", 7.3, 17.3, style="display:inline;min-width:90px",
                     **{"from": 7.3, "to": 24.6, "lin": 1, "dec": 1, "pre": "", "suf": "s", "show": 1})
                 + '</div>', "life", 7.3, 30, fo=.01, style="position:absolute;left:0;right:0;top:0;text-align:center;z-index:7")

    small = dict(extra="font-weight:500")
    l1 = line_block(7.5, 3.9, ch("You just watched a balloon", 7.55, 48, **small)
                    + row(ch("for", 8.3, 84, cls="num"), ch("7", 8.45, 84, cls="num", colour=INK, extra="text-shadow:none"),
                          ch("seconds.", 8.55, 84, cls="num")))
    l2 = line_block(11.6, 3.8, ch("And you’re still here,", 11.65, 48, **small)
                    + row(ch("waiting for it to", 12.3, 76, cls="num"), ch("pop.", 12.8, 76, cls="num", colour=INK, extra="text-shadow:none")))
    l3 = line_block(15.6, 4.5, ch("Now imagine it’s", 15.65, 48, **small)
                    + row(ch("your", 16.2, 96, cls="num"), ch("DCF.", 16.35, 96, cls="num", colour=INK, extra="text-shadow:none")))
    l4 = line_block(20.2, 2.5, ch("And the needle is", 20.25, 48, **small)
                    + row(ch("your", 20.6, 96, cls="num"), ch("WACC.", 20.75, 96, cls="num", colour=INK, extra="text-shadow:none")))
    l5 = line_block(22.8, 1.85, ch("1 point of WACC.", 22.85, 48, **small)
                    + ch("$714M gone.", 23.1, 104, cls="num", colour=INK, extra="text-shadow:none"), )

    chip = ("background:rgba(10,10,10,.6);border:2px solid rgba(255,255,255,.22);border-radius:22px;"
            "padding:18px 26px;min-width:300px;text-align:left")
    ev = (f'<div style="{chip}"><div style="font-size:22px;font-weight:600;letter-spacing:.14em;opacity:.7">ENTERPRISE VALUE</div>'
          + A("$5.0B", "count", 20.6, 2.0, cls="num", style="font-size:72px;line-height:1.1",
              **{"from": 5.0, "to": 4.3, "dec": 1, "pre": "$", "suf": "B", "show": 1}) + '</div>')
    wacc = (f'<div style="{chip};min-width:200px"><div style="font-size:22px;font-weight:600;letter-spacing:.14em;opacity:.7">WACC</div>'
            + A("8%", "count", 20.6, 1.4, cls="num", style=f"font-size:72px;line-height:1.1;color:#ff8a66",
                **{"from": 8, "to": 9, "dec": 0, "pre": "", "suf": "%", "show": 1}) + '</div>')
    chips = A(f'<div style="display:flex;justify-content:center;gap:20px">{ev}{wacc}</div>'
              '<div style="text-align:center;font-size:28px;margin-top:22px;opacity:.85">'
              '$300M cash flow &divide; (WACC &minus; 2% growth)</div>',
              "life", 16.6, 30, fo=.01, style=f"position:absolute;left:0;right:0;top:900px;z-index:6;{TXT}")

    s.append(dict(dur=24.6, exit="cut", html=(
        art(balloon() + needle()) + brackets + hud + watching + l1 + l2 + l3 + l4 + l5 + chips)))

    # The pop: shards from where the needle went in, and a flash.
    import math
    shards = ""
    for k in range(34):
        a = k * 2.4 + (k % 5) * .3
        r = 420 + (k * 53) % 380
        col = ["#D93A12", "#e8501f", "#ff9a6c", "#8a2208"][k % 4]
        w, h = 30 + (k * 7) % 40, 12 + (k * 5) % 18
        shards += A(f'<div style="width:{w}px;height:{h}px;border-radius:{h}px {h // 3}px;background:{col}"></div>',
                    "slide", 0, .9 + (k % 4) * .12, ease="out", x0=0, y0=0,
                    x1=round(math.cos(a) * r), y1=round(math.sin(a) * r * 1.2), r=(k % 2 * 2 - 1) * (300 + k * 20),
                    style="position:absolute;left:540px;top:640px")
    flash = A("", "ripple", 0, .22, style="position:absolute;left:240px;top:340px;width:600px;height:600px;"
              "border-radius:50%;background:radial-gradient(circle,#fff,rgba(255,180,150,.6) 45%,rgba(217,58,18,0) 70%)")
    s.append(dict(dur=1.5, exit="cut", html=art(flash + shards) + A(
        f'<div class="num" style="font-size:150px;color:{RED};transform:rotate(-6deg)">POP<span style="color:#fff">.</span></div>',
        "stamp", .25, .3, rot=-6, style="position:absolute;left:0;right:0;top:420px;text-align:center;z-index:6")))

    # The brand, and the one ask.
    star = ('<svg viewBox="0 0 100 100" width="170" height="170" style="filter:drop-shadow(0 0 30px rgba(217,58,18,.7))">'
            '<path d="M50 0 C54 38 62 46 100 50 C62 54 54 62 50 100 C46 62 38 54 0 50 C38 46 46 38 50 0Z" fill="#D93A12"/></svg>')
    s.append(dict(dur=3.8, push=.03, html=(
        '<div style="text-align:center">'
        + A(star, "spin", 0, 1, deg=25, style="display:inline-block")
        + A(f'<div class="num" style="font-size:250px;line-height:1;margin-top:10px;text-shadow:0 0 60px rgba(217,58,18,.35)">IB<span style="color:{RED}">.</span></div>',
            "pop", .05, .45)
        + ch("INVESTMENT BANKING INTERVIEWS", .3, 30, extra="font-weight:600;letter-spacing:.22em;opacity:.8;margin-top:18px")
        + A(f'<div style="display:inline-block;margin-top:56px;border:3px solid {RED};border-radius:999px;padding:18px 34px;'
            'font-size:36px;font-weight:600">Follow for 2 interview questions a day</div>', "rise", .8, .45)
        + '</div>')))
    return s


if __name__ == "__main__":
    print("w1-pop-dcf")
    build("w1-pop-dcf", r_pop(), theme="ink", cover_at=0.7)
