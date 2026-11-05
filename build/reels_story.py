"""
Story Reel: "The IB. Daily". Modelled on the 4 Nov reference (an ad where a
man is so absorbed in a newspaper about a building that he walks through the
whole city reading it, arrives there, and the paper flies off to loop back to
the first shot).

Ours: a candidate reads one page on the morning of his superday. He walks
through the city without looking up (a taxi, a building site, a fountain), a
clock counting down to 9:00, gets the exact question the page asked, answers
it in five steps, gets the offer, throws the paper out of the window, and it
lands in the next student's hands. The page was ours.

Faceless by construction: the newspaper covers his face in every shot.
Every technical line is standard: unlevered free cash flow at WACC, terminal
value, enterprise value, the bridge to equity value.

    python build/reels_story.py
"""

from motion import A, build
from reels_motion import ch, SHADOW, TEAL_D

INK, RED, PAPER = "#0A0A0A", "#D93A12", "#F7F5F2"
SUIT, SUIT2, SKIN = "#1f2838", "#2b3446", "#e7c4a0"


def g(fx, inner, at=0, d=1, style="", **data):
    attrs = "".join(f' data-{k}="{v}"' for k, v in data.items())
    st = f' style="{style}"' if style else ""
    return f'<g class="a" data-fx="{fx}" data-at="{at}" data-d="{d}"{attrs}{st}>{inner}</g>'


PIVOT = "transform-box:fill-box;transform-origin:50% 3%"


def person(walk=True, scale=1.5, coat=None):
    """A candidate in a suit, reading a newspaper that hides his face."""
    def leg(x, fill, ph):
        body = (f'<rect x="{x}" y="250" width="26" height="144" rx="12" fill="{fill}"/>'
                f'<ellipse cx="{x + 20}" cy="396" rx="23" ry="9" fill="{INK}"/>')
        return g("swing", body, amp=22, w=9, ph=ph, style=PIVOT) if walk else body
    paper = (f'<rect x="136" y="40" width="88" height="116" rx="4" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
             f'<rect x="144" y="50" width="72" height="11" rx="2" fill="{INK}"/>'
             f'<rect x="144" y="66" width="30" height="6" fill="{RED}"/>'
             f'<rect x="144" y="78" width="72" height="9" rx="2" fill="#333"/>'
             f'<rect x="144" y="91" width="56" height="9" rx="2" fill="#333"/>'
             + "".join(f'<rect x="144" y="{108 + k * 9}" width="{72 if k % 3 else 50}" height="4" fill="#bbb"/>'
                       for k in range(5))
             + f'<line x1="180" y1="40" x2="180" y2="156" stroke="#ddd" stroke-width="2"/>')
    body = (
        f'<ellipse cx="112" cy="404" rx="64" ry="9" fill="rgba(10,10,10,.13)"/>'
        + leg(96, SUIT2, 3.14) + leg(104, SUIT, 0)
        + f'<rect x="74" y="126" width="80" height="140" rx="26" fill="{coat or SUIT}"/>'
        + f'<path d="M104 128 L117 160 L130 128Z" fill="{PAPER}"/>'
        + f'<path d="M114 138 h6 l3 36 l-6 7 l-6 -7Z" fill="{RED}"/>'
        + f'<circle cx="108" cy="94" r="31" fill="{INK}"/>'
        + f'<rect x="118" y="138" width="64" height="22" rx="11" fill="{SUIT2}" transform="rotate(-30 118 149)"/>'
        + paper
        + f'<rect x="116" y="150" width="68" height="22" rx="11" fill="{SUIT}" transform="rotate(-24 116 161)"/>'
        + f'<circle cx="178" cy="124" r="10" fill="{SKIN}"/>')
    bob = g("float", body, amp=3, w=18, ph=0) if walk else body
    return (f'<svg width="{220 * scale:.0f}" height="{420 * scale:.0f}" viewBox="0 0 220 420" '
            f'style="overflow:visible;display:block">{bob}</svg>')


def worker(hat, turn_at, ph=0, sc=1.4):
    head = g("swing", f'<circle cx="60" cy="62" r="24" fill="{INK}"/>'
                      f'<path d="M30 60 a30 26 0 0 1 60 0 h8 v8 h-76 v-8z" fill="{hat}"/>',
             at=turn_at, amp=10, w=6, ph=ph, style="transform-box:fill-box;transform-origin:50% 90%")
    return (f'<svg width="{120 * sc:.0f}" height="{260 * sc:.0f}" viewBox="0 0 120 260" style="overflow:visible;display:block">'
            f'<ellipse cx="60" cy="252" rx="44" ry="7" fill="rgba(10,10,10,.12)"/>'
            f'<rect x="38" y="160" width="20" height="90" rx="9" fill="{SUIT2}"/>'
            f'<rect x="62" y="160" width="20" height="90" rx="9" fill="{SUIT2}"/>'
            f'<rect x="26" y="84" width="68" height="94" rx="22" fill="{RED}"/>'
            f'<rect x="26" y="118" width="68" height="9" fill="{PAPER}"/>'
            f'<rect x="26" y="140" width="68" height="9" fill="{PAPER}"/>'
            f'{head}</svg>')


def car():
    wheel = lambda x: g("spin", f'<circle cx="{x}" cy="118" r="26" fill="{INK}"/><circle cx="{x}" cy="118" r="10" fill="#888"/>'
                                f'<rect x="{x - 2}" y="96" width="4" height="44" fill="#888"/>',
                        deg=900, style="transform-box:fill-box;transform-origin:50% 50%")
    lines = "".join(f'<rect x="{-170 + k * 24}" y="{50 + k * 18}" width="{120 - k * 20}" height="6" rx="3" '
                    f'fill="rgba(10,10,10,.18)"/>' for k in range(4))
    return (f'<svg width="380" height="160" viewBox="0 0 380 160" style="overflow:visible;display:block">{lines}'
            f'<path d="M20 112 q0 -40 40 -44 l50 -4 l50 -44 h120 l40 44 l30 6 q20 4 20 30 v12 h-350z" fill="{RED}"/>'
            f'<path d="M176 28 h100 l32 36 h-162z" fill="{PAPER}" opacity=".9"/>'
            f'<rect x="222" y="28" width="7" height="36" fill="{RED}"/>'
            f'<rect x="100" y="72" width="60" height="18" rx="3" fill="#f1d36b"/>'
            f'<text x="130" y="86" text-anchor="middle" font-family="Sans" font-weight="600" font-size="13" fill="{INK}">TAXI</text>'
            + wheel(90) + wheel(300) + '</svg>')


def skyline(y=760, op=.09):
    xs = [(0, 300), (70, 420), (150, 260), (210, 520), (300, 360), (380, 610), (470, 300), (540, 470),
          (640, 380), (720, 540), (820, 330), (900, 450), (980, 300)]
    bld = "".join(f'<rect x="{x}" y="{y - h}" width="{80 + (i % 3) * 14}" height="{h}" fill="rgba(10,10,10,{op})"/>'
                  for i, (x, h) in enumerate(xs))
    return (f'<circle cx="790" cy="{y - 420}" r="120" fill="rgba(217,58,18,.16)"/>{bld}'
            f'<rect x="0" y="{y}" width="1080" height="12" fill="rgba(10,10,10,.16)"/>')


def stage(inner):
    """Full-bleed illustration layer, in frame coordinates, skipped by the text check."""
    return (f'<div class="nochk" style="position:absolute;left:-84px;top:-230px;width:1080px;height:1920px">'
            f'<svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;inset:0">{inner}</svg>'
            f'</div>')


def at_px(html, x, y, z=1):
    return f'<div style="position:absolute;left:{x - 84}px;top:{y - 230}px;z-index:{z}">{html}</div>'


GROUND = 1330


def top_for(scale):
    """Top edge that puts a person's feet on the ground line."""
    return GROUND - 404 * scale


def walker(x0, x1, y, at, d, scale=1.5):
    return A(person(scale=scale), "slide", at, d, cls="nochk", x0=x0, x1=x1,
             style=f"position:absolute;left:{-84}px;top:{top_for(scale) - 230:.0f}px;z-index:3")


def clock(time, note, at=-.2):
    return ('<div style="position:absolute;left:0;top:0;z-index:5;display:flex;align-items:baseline;gap:18px">'
            + ch(time, at, 64, cls="num", colour=RED, st=.05)
            + ch(note, at + .15, 34, extra="font-weight:600;letter-spacing:.04em;text-transform:uppercase;opacity:.6")
            + '</div>')


def bubble(text_html, at, width=None, tail="left", style=""):
    tail_css = ("left:60px" if tail == "left" else "right:60px")
    w = f"width:{width}px;" if width else ""
    return A(f'<div style="position:relative;background:#fff;border-radius:28px;padding:30px 36px;{w}'
             f'box-shadow:{SHADOW}">{text_html}'
             f'<div style="position:absolute;bottom:-16px;{tail_css};width:34px;height:34px;background:#fff;'
             f'transform:rotate(45deg);border-radius:4px"></div></div>', "pop", at, .4, style=style)


def newspaper_close(overlay=""):
    """The front page, filling the frame. Used to open and to close, so the Reel loops."""
    lines = "".join(f'<div style="height:10px;border-radius:5px;background:#d8d4cd;margin-top:16px;width:{w}%"></div>'
                    for w in (100, 92, 97, 60))
    paper = (
        f'<div style="position:relative;background:#fff;border-radius:10px;padding:40px 40px 46px;margin:0 18px;box-shadow:{SHADOW};'
        'transform:rotate(-2deg)">'
        f'<div style="border-bottom:4px solid {INK};padding-bottom:14px">'
        f'<div style="font-family:Serif;font-weight:700;font-size:74px;letter-spacing:-.03em;line-height:1">The IB<span style="color:{RED}">.</span> Daily</div>'
        '<div style="font-size:22px;font-weight:600;letter-spacing:.1em;opacity:.55;margin-top:10px">2 INTERVIEW QUESTIONS A DAY</div></div>'
        f'<div style="display:inline-block;margin-top:26px;background:{RED};color:#fff;font-size:26px;font-weight:600;'
        'letter-spacing:.1em;padding:8px 16px;border-radius:4px">TODAY&rsquo;S QUESTION</div>'
        '<div style="font-family:Serif;font-weight:700;font-size:112px;line-height:.98;letter-spacing:-.035em;margin-top:22px">'
        f'Walk me through a DCF<span style="color:{RED}">.</span></div>'
        f'<div style="display:flex;gap:30px;margin-top:30px"><div style="flex:1">{lines}</div><div style="flex:1">{lines}</div></div>'
        '</div>')
    return f'<div style="position:relative;margin-top:300px">{paper}</div>' + overlay


def r_story():
    s = []

    # 0. Hook: the front page, and the POV line. Frame 0 is the bare front page
    #    so the last scene (the same page) loops into it.
    hook = ('<div style="position:absolute;left:0;right:0;top:0;z-index:4">'
            + ch("POV:", .15, 100, cls="num", colour=RED, st=.06)
            + ch("you read one page the morning of your superday", .45, 58, extra="font-weight:500;line-height:1.2;margin-top:6px")
            + '</div>')
    s.append(dict(dur=2.8, exit="whip", push=.04, html=newspaper_close(hook)))

    # 1. The city. He walks across without looking up.
    s.append(dict(dur=2.6, enter="whip", exit="whip", push=.03, html=(
        stage(skyline(1330))
        + walker(-300, 600, 980, -.3, 3.0)
        + clock("8:14", "Superday at 9:00"))))

    # 2. The taxi.
    honk = A(f'<div style="font-family:Serif;font-weight:700;font-size:120px;color:{RED};transform:rotate(-8deg)">BEEP<span style="color:{INK}">!</span></div>',
             "stamp", 1.0, .3, rot=-8, style="position:absolute;left:330px;top:300px;z-index:6")
    s.append(dict(dur=2.6, enter="whip", exit="whip", push=.03, html=(
        stage(skyline(1330, .06) + '<rect x="0" y="1310" width="1080" height="110" fill="rgba(10,10,10,.07)"/>'
              + "".join(f'<rect x="{x}" y="1360" width="80" height="10" rx="5" fill="#fff"/>' for x in range(20, 1080, 160)))
        + A(car(), "slide", .15, 1.5, cls="nochk", x0=1200, x1=-760, style=f"position:absolute;left:{300 - 84}px;top:{1330 - 142 - 230}px;z-index:4")
        + walker(-160, 480, 960, -.3, 3.0)
        + honk + clock("8:23", "Still reading"))))

    # 3. The building site: workers turn and stare, he walks straight through.
    tape = (f'<rect x="-40" y="1223" width="1160" height="34" fill="{RED}" transform="rotate(-4 540 1240)"/>'
            + "".join(f'<rect x="{x}" y="1219" width="34" height="42" fill="#fff" transform="rotate(-4 540 1240) skewX(-30)"/>'
                      for x in range(0, 1100, 90)))
    cones = "".join(f'<path d="M{x} 1350 l34 -100 l34 100z" fill="{RED}"/><rect x="{x + 14}" y="1290" width="40" height="12" fill="#fff"/>'
                    for x in (140, 820))
    wy = 1330 - 252 * 1.4
    wk = ('<div class="nochk">' + at_px(worker(RED, .6), 590, wy, 2) + at_px(worker(TEAL_D, .8, 1.5), 700, wy + 12, 2)
          + at_px(worker("#f1d36b", .7, 3), 805, wy - 6, 2) + '</div>')
    q = A(f'<div style="font-family:Serif;font-weight:700;font-size:110px;color:{RED}">?!</div>', "pop", 1.2, .35,
          style="position:absolute;left:620px;top:560px;z-index:6")
    s.append(dict(dur=2.8, enter="whip", exit="whip", push=.03, html=(
        stage(skyline(1330, .05) + cones) + wk
        + walker(-260, 520, 980, -.3, 3.3)
        + stage(tape) + q + clock("8:31", "Building site"))))

    # 4. The fountain: in, splash, out, still reading.
    drops = "".join(
        A(f'<div style="width:{18 + k % 3 * 8}px;height:{18 + k % 3 * 8}px;border-radius:50%;background:{TEAL_D};opacity:.7"></div>',
          "slide", 1.15 + k * .03, .7, ease="out", x0=0, x1=(-1) ** k * (60 + k * 22), y0=0, y1=-(160 + (k * 37) % 140),
          cls="nochk", style=f"position:absolute;left:{470 - 84 + k * 8}px;top:{1330 - 220 - 230}px;z-index:6")
        for k in range(10))
    basin = (f'<ellipse cx="540" cy="1310" rx="360" ry="70" fill="rgba(15,118,110,.18)" stroke="{TEAL_D}" stroke-width="8"/>'
             f'<path d="M540 1300 C 520 1080, 470 1040, 420 1130" fill="none" stroke="{TEAL_D}" stroke-width="10" stroke-linecap="round" opacity=".6"/>'
             f'<path d="M540 1300 C 560 1080, 610 1040, 660 1130" fill="none" stroke="{TEAL_D}" stroke-width="10" stroke-linecap="round" opacity=".6"/>')
    dip = A(A(person(), "slide", .9, .5, ease="inout", y0=0, y1=90),
            "slide", -.3, 3.3, cls="nochk", x0=-200, x1=620, style=f"position:absolute;left:-84px;top:{top_for(1.5) - 230:.0f}px;z-index:3")
    front = (f'<path d="M180 1310 a360 70 0 0 0 720 0" fill="rgba(15,118,110,.22)" stroke="{TEAL_D}" stroke-width="8"/>')
    splash = A(f'<div style="font-family:Serif;font-weight:700;font-size:110px;color:{TEAL_D};transform:rotate(6deg)">SPLASH<span style="color:{RED}">.</span></div>',
               "stamp", 1.2, .3, rot=6, style="position:absolute;left:140px;top:300px;z-index:6")
    s.append(dict(dur=2.8, enter="whip", exit="whip", push=.03, html=(
        stage(skyline(1330, .05) + basin) + dip + stage(front) + drops + splash
        + clock("8:47", "The fountain"))))

    # 5. The tower and the lift to floor 42.
    win = "".join(f'<rect x="{360 + c * 70}" y="{1330 - 960 + r * 80}" width="44" height="54" rx="4" fill="rgba(10,10,10,.12)"/>'
                  for r in range(11) for c in range(5))
    tower = (f'<rect x="330" y="330" width="380" height="1000" rx="10" fill="rgba(10,10,10,.07)"/>{win}'
             f'<rect x="470" y="1190" width="100" height="140" rx="6" fill="{INK}"/>')
    panel = A('<div style="background:#0A0A0A;color:#fff;border-radius:24px;padding:26px 34px;box-shadow:' + SHADOW + '">'
              '<div style="font-size:26px;font-weight:600;letter-spacing:.1em;opacity:.6">FLOOR</div>'
              + A("1", "count", .4, 1.6, cls="num", style="font-size:150px;line-height:1;color:#5EC8B4",
                  **{"from": 1, "to": 42, "dec": 0, "pre": "", "suf": "", "show": 1})
              + '</div>', "rise", -.2, .4, style="position:absolute;right:0;top:420px;z-index:6")
    s.append(dict(dur=2.8, enter="whip", exit="whip", push=.035, html=(
        stage(tower) + walker(-200, 330, 980, -.3, 1.6, scale=1.2) + panel
        + clock("8:58", "Floor 42"))))

    # 6. The question he just read, and the five-step answer.
    steps = ["Project free cash flow", "Discount it at WACC", "Add a terminal value",
             "Sum to enterprise value", "Bridge to equity value"]
    rows = "".join(A(f'<div style="display:flex;align-items:center;gap:20px;font-size:42px;font-weight:500;padding:9px 0">'
                     f'<span class="num" style="width:58px;height:58px;border-radius:50%;background:{TEAL_D};color:#fff;'
                     f'display:inline-flex;align-items:center;justify-content:center;font-size:34px;flex:none">{k + 1}</span>{t}</div>',
                     "rise", 1.25 + k * .38, .35) for k, t in enumerate(steps))
    room = (f'<rect x="120" y="780" width="840" height="34" rx="8" fill="rgba(10,10,10,.75)"/>'
            f'<circle cx="760" cy="660" r="52" fill="{INK}"/><rect x="680" y="710" width="160" height="80" rx="40" fill="{SUIT}"/>'
            f'<circle cx="300" cy="685" r="48" fill="{INK}"/><rect x="226" y="730" width="150" height="70" rx="36" fill="{SUIT2}"/>')
    s.append(dict(dur=4.6, enter="whip", exit="whip", push=.025, html=(
        stage(room)
        + bubble(ch("Walk me through a DCF.", .2, 58, cls="num", st=.03), .05, tail="right",
                 style="position:absolute;right:0;top:130px;z-index:5")
        + bubble(f'<div>{rows}</div>', .95, width=640, tail="left",
                 style="position:absolute;left:0;top:640px;z-index:5")
        + clock("9:00", "The question"))))

    # 7. The offer.
    letter = A('<div style="background:#fff;border-radius:14px;padding:44px 46px;width:520px;box-shadow:' + SHADOW + ';'
               'transform:rotate(-3deg)"><div style="font-family:Serif;font-weight:700;font-size:44px">Summer Analyst</div>'
               + "".join(f'<div style="height:10px;border-radius:5px;background:#e2ded7;margin-top:18px;width:{w}%"></div>'
                         for w in (100, 86, 94, 52))
               + A(f'<div style="border:8px solid {RED};color:{RED};border-radius:14px;padding:6px 22px;font-family:Serif;'
                   f'font-weight:700;font-size:96px;letter-spacing:.04em;background:rgba(255,255,255,.85)">OFFER</div>',
                   "stamp", 1.1, .35, rot=-9, style="position:absolute;right:-30px;bottom:-40px")
               + '</div>', "rise", .5, .45, style="position:absolute;left:80px;top:560px;z-index:4")
    s.append(dict(dur=2.8, enter="whip", exit="whip", push=.03, html=(
        bubble(ch("When can you start?", .1, 58, cls="num", st=.03), -.1, tail="right",
               style="position:absolute;right:0;top:130px;z-index:5")
        + letter + clock("9:41", "Offer"))))

    # 8. Out of the window it goes.
    window = (f'<rect x="150" y="380" width="780" height="980" rx="16" fill="rgba(94,200,180,.12)" stroke="{INK}" stroke-width="14"/>'
              f'<rect x="533" y="380" width="14" height="980" fill="{INK}"/>' + skyline(1360, .07))
    flying = A('<svg width="200" height="150" viewBox="0 0 200 150" style="display:block">'
               f'<rect x="4" y="4" width="192" height="142" rx="6" fill="#fff" stroke="{INK}" stroke-width="4"/>'
               f'<rect x="20" y="20" width="160" height="18" fill="{INK}"/><rect x="20" y="50" width="70" height="10" fill="{RED}"/>'
               f'<rect x="20" y="70" width="160" height="12" fill="#444"/><rect x="20" y="92" width="120" height="12" fill="#444"/></svg>',
               "slide", .2, 2.2, cls="nochk", x0=40, x1=720, y0=860, y1=-60, r=540, style="position:absolute;left:0;top:0;z-index:5")
    s.append(dict(dur=2.6, enter="whip", exit="whip", push=.03, html=(stage(window) + flying)))

    # 9. It lands in the next student's hands, back by the river.
    catch = A(person(walk=False, coat=TEAL_D), "fade", .9, .2, cls="nochk",
              style=f"position:absolute;left:{300 - 84}px;top:{top_for(1.5) - 230:.0f}px;z-index:3")
    waiting = A('<svg width="220" height="420" viewBox="0 0 220 420" style="display:block">'
                f'<ellipse cx="112" cy="404" rx="64" ry="9" fill="rgba(10,10,10,.13)"/>'
                f'<rect x="96" y="250" width="26" height="144" rx="12" fill="{SUIT2}"/><rect x="104" y="250" width="26" height="144" rx="12" fill="{SUIT}"/>'
                f'<rect x="74" y="126" width="80" height="140" rx="26" fill="{TEAL_D}"/><circle cx="108" cy="94" r="31" fill="{INK}"/></svg>',
                "fade", -1, .2, cls="nochk", style=f"position:absolute;left:{300 - 84}px;top:{top_for(1.5) - 230:.0f}px;z-index:2;transform:scale(1.5);transform-origin:0 0")
    falling = A('<svg width="120" height="90" viewBox="0 0 200 150" style="display:block">'
                f'<rect x="4" y="4" width="192" height="142" rx="6" fill="#fff" stroke="{INK}" stroke-width="6"/>'
                f'<rect x="20" y="20" width="160" height="18" fill="{INK}"/></svg>',
                "slide", -.2, 1.1, ease="out", cls="nochk", x0=200, x1=120, y0=-200, y1=top_for(1.5) + 40 * 1.5 - 230, r=-400,
                style="position:absolute;left:300px;top:0;z-index:5")
    s.append(dict(dur=2.6, enter="whip", exit="zoom", push=.05, html=(
        stage(skyline(1330) + '<rect x="0" y="1312" width="1080" height="8" fill="rgba(15,118,110,.3)"/>')
        + waiting + falling + catch
        + A(ch("Next.", .9, 120, cls="num", colour=RED), "fade", .9, .1,
            style="position:absolute;left:0;top:140px;z-index:6"))))

    # 10. The same front page, now with the reveal and the one ask. Loops to scene 0.
    cta = ('<div style="position:absolute;left:0;right:0;top:0;z-index:4">'
           + ch("This was the page.", .2, 60, extra="font-weight:500")
           + ch("Follow.", .7, 150, cls="num", colour=RED, st=.06, extra="line-height:1;margin-top:4px")
           + '</div>')
    s.append(dict(dur=3.4, enter="zoomin", push=.03, html=newspaper_close(cta)))
    return s


if __name__ == "__main__":
    print("w1-story-ib-daily")
    build("w1-story-ib-daily", r_story(), theme="paper", cover_at=2.2)
