"""
YouTube long-form explainer engine (8 Nov) for The Banker's Notebook / the
@investmentbankinginterviews channel: 1920x1080, paper ground, brand fonts,
voiced by GEORGE (Kokoro bm_george, Apache 2.0), sound effects from sfx.py,
no music in the master.

An episode is a config (see youtube_ep001.py):

    EP = dict(
        slug="yt-001-...", title="...", thumb=dict(big="...", small="..."),
        chapters=[dict(title="...", beats=[
            dict(say="One or two sentences.", show=dict(kind="statement", text="...", hl=["key words"])),
            dict(say="...", show=dict(kind="number", value=1250, pre="$", label="...")),
            dict(say="...", show=dict(kind="list", items=["...", "..."])),
            dict(say="...", show=dict(kind="compare", left=("Label", "value"), right=("Label", "value"))),
            dict(say="...", show=dict(kind="term", term="...", text="...")),
        ])],
        description="...", tags=[...],
    )

Each beat is spoken in one pass (Kokoro, phoneme-exact), its visual builds
while it is spoken, and captions run under it. Chapters open on a title card.
Outputs in out/<slug>/: <slug>.mp4, thumbnail.jpg, metadata.json (title,
description with chapter times, tags, AI-disclosure setting), quality.json.

    python build/youtube_ep001.py
"""

import html as H
import json
import pathlib
import re
import subprocess

import numpy as np
from playwright.sync_api import sync_playwright

import sfx as S
from motion import A, JS, FONTS, OUT
from voice import passage, write_wav, SR, MASTER
from voice_clone import make_voice, YOUTUBE_VOICE
import sketch

W, Hh, FPS = 1920, 1080, 24
RED, TEAL, INK = "#D93A12", "#0F766E", "#0A0A0A"

CSS = """
@font-face{font-family:'Serif';src:url('FONTS/serif700.woff2') format('woff2');font-weight:700}
@font-face{font-family:'Serif';src:url('FONTS/serif400i.woff2') format('woff2');font-weight:400;font-style:italic}
@font-face{font-family:'Serif';src:url('FONTS/serif600i.woff2') format('woff2');font-weight:600;font-style:italic}
@font-face{font-family:'Sans';src:url('FONTS/sans400.woff2') format('woff2');font-weight:400}
@font-face{font-family:'Sans';src:url('FONTS/sans500.woff2') format('woff2');font-weight:500}
@font-face{font-family:'Sans';src:url('FONTS/sans600.woff2') format('woff2');font-weight:600}
html,body{margin:0;padding:0;background:#F7F5F2}
.f{width:1920px;height:1080px;position:relative;overflow:hidden;background:#F7F5F2;color:#0A0A0A;font-family:'Sans',sans-serif}
.glow{position:absolute;width:1600px;height:1600px;border-radius:50%;background:radial-gradient(closest-side,rgba(217,58,18,.06),rgba(217,58,18,0))}
.mark{position:absolute;left:96px;top:64px;font-family:'Serif',serif;font-weight:700;font-size:44px;z-index:5}
.chap{position:absolute;right:96px;top:74px;font-size:24px;font-weight:600;letter-spacing:.18em;opacity:.55;z-index:5}
.bar{position:absolute;left:96px;right:96px;bottom:48px;height:6px;border-radius:3px;background:rgba(10,10,10,.1);z-index:5}
.bar i{display:block;height:6px;border-radius:3px;background:#D93A12;width:0}
.scene{position:absolute;inset:0;visibility:hidden}
.safe{position:absolute;left:160px;right:160px;top:150px;bottom:230px;display:flex;flex-direction:column;justify-content:center}
.ghost{position:absolute;right:-60px;top:80px;font-family:'Serif',serif;font-weight:700;font-size:900px;line-height:1;color:#0A0A0A;opacity:0}
.a{will-change:transform,opacity}
.num{font-family:'Serif',serif;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.it{font-family:'Serif',serif;font-style:italic;font-weight:600}
.lbl{font-size:26px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;opacity:.55}
.cap{position:absolute;left:0;right:0;bottom:-150px;text-align:center;font-size:40px;font-weight:600;line-height:1.3;z-index:6}
.roll,.rl{display:none}
.dots{position:absolute;inset:-60px;background-image:radial-gradient(rgba(10,10,10,.085) 2.4px,transparent 2.6px);background-size:46px 46px}
.ring{position:absolute;border-radius:50%;border:3px solid rgba(217,58,18,.16)}
.ring2{position:absolute;border-radius:50%;border:2px dashed rgba(10,10,10,.12)}
.tabs{position:absolute;left:50%;top:76px;transform:translateX(-50%);display:flex;gap:14px;z-index:5}
.tabs i{display:block;width:90px;height:8px;border-radius:4px;background:rgba(10,10,10,.12)}
.tabs i.on{background:#D93A12}.tabs i.done{background:rgba(10,10,10,.45)}
"""


# Line icons, drawn on screen stroke by stroke (one path each, 100x100 box).
# Ours: drawn for this channel, nothing to license.
ICONS = {
    "tulip": "M50 92 V52 M50 64 C40 57 31 60 27 71 M50 72 C60 65 69 67 73 76 M35 24 C33 40 39 52 50 52 C61 52 67 40 65 24 L57 33 L50 20 L43 33 Z",
    "house": "M16 50 L50 20 L84 50 M25 43 V84 H75 V43 M43 84 V62 H57 V84",
    "coin": "M50 16 A34 34 0 1 1 49.9 16 Z M50 30 V70 M61 38 C57 32 41 32 40 41 C39 50 61 49 61 59 C60 68 43 69 39 62",
    "doc": "M28 14 H62 L76 28 V86 H28 Z M62 14 V28 H76 M37 42 H67 M37 54 H67 M37 66 H57",
    "gavel": "M28 40 L48 20 L66 38 L46 58 Z M57 48 L84 75 M16 88 H58",
    "scales": "M50 18 V82 M30 82 H70 M20 32 H80 M20 32 L10 58 H30 Z M80 32 L70 58 H90 Z",
    "people": "M36 30 A11 11 0 1 1 35.9 30 Z M16 84 C16 60 56 60 56 84 M68 30 A9 9 0 1 1 67.9 30 Z M60 58 C68 52 88 56 88 78",
    "person": "M50 22 A14 14 0 1 1 49.9 22 Z M24 88 C24 58 76 58 76 88",
    "search": "M42 16 A26 26 0 1 1 41.9 16 Z M61 61 L86 86",
    "book": "M50 26 C40 18 24 18 14 22 V80 C24 76 40 76 50 84 C60 76 76 76 86 80 V22 C76 18 60 18 50 26 Z M50 26 V84",
    "down": "M12 86 H88 M16 26 L36 44 L52 36 L82 74 M82 74 L66 73 M82 74 L82 58",
    "up": "M12 86 H88 M16 74 L38 54 L52 62 L82 24 M82 24 L66 25 M82 24 L82 40",
    "bank": "M12 38 L50 16 L88 38 Z M22 44 V74 M40 44 V74 M60 44 V74 M78 44 V74 M12 82 H88",
    "ship": "M12 62 H88 L76 82 H24 Z M50 62 V14 M50 18 L74 52 H50",
    "virus": "M50 30 A20 20 0 1 1 49.9 30 Z M50 30 V16 M50 70 V84 M30 50 H16 M70 50 H84 M36 36 L26 26 M64 64 L74 74 M64 36 L74 26 M36 64 L26 74",
    "cross": "M24 24 L76 76 M76 24 L24 76",
    "check": "M18 52 L40 74 L82 28",
    "question": "M34 34 C34 14 68 14 68 34 C68 48 50 50 50 64 M50 80 V84",
    "calendar": "M16 24 H84 V86 H16 Z M16 40 H84 M34 14 V30 M66 14 V30 M30 54 H40 M46 54 H56 M62 54 H72 M30 68 H40 M46 68 H56",
    "hand": "M20 60 L40 40 L58 44 L82 30 M20 60 L36 76 L52 72 M58 44 L44 58 M52 72 L72 58 M82 30 L88 44",
    "clock": "M50 14 A36 36 0 1 1 49.9 14 Z M50 28 V50 L66 60",
    "pen": "M20 80 L26 62 L66 22 L78 34 L38 74 Z M60 28 L72 40 M20 80 L32 76",
    "globe": "M50 14 A36 36 0 1 1 49.9 14 Z M14 50 H86 M50 14 C34 30 34 70 50 86 M50 14 C66 30 66 70 50 86",
    "lock": "M26 46 H74 V86 H26 Z M36 46 V32 C36 14 64 14 64 32 V46 M50 62 V72",
    "fire": "M50 88 C28 88 22 68 30 52 C34 60 40 62 42 58 C38 42 46 26 58 14 C58 34 76 42 76 62 C76 78 66 88 50 88 Z",
}


def icon(name, size=320, color=INK, at=0.0, d=1.1, width=5):
    return A(f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" style="overflow:visible;display:block">'
             f'<path d="{ICONS[name]}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/></svg>',
             "draw", round(at, 3), d)


def badge(name, size=360, color=INK, ring=RED, at=0.0):
    """An icon inside a soft disc that pops in, then draws."""
    return A(f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:#fff;box-shadow:0 30px 80px rgba(10,10,10,.10);'
             f'display:flex;align-items:center;justify-content:center;border:6px solid {ring}">'
             + icon(name, int(size * .58), color, at + .25) + "</div>", "pop", round(at, 3), .5)


def words_kara(text, start, dur, hl=(), size=72, serif=True, hide=False, color=INK):
    ws = text.split()
    lens = [max(len(re.sub(r"\W", "", w)), 1) + 1 for w in ws]
    acc, spans = 0, []
    hlw = {re.sub(r"\W", "", x).lower() for p in hl for x in p.split()}
    for w, n in zip(ws, lens):
        t = round(dur * acc / sum(lens), 3)
        acc += n
        c = RED if re.sub(r"\W", "", w).lower() in hlw else ""
        spans.append(f'<span class="w" data-t="{t}"' + (f' data-c="{c}"' if c else "") + f' style="display:inline-block">{H.escape(H.unescape(w))}</span>')
    fam = "font-family:'Serif',serif;font-weight:700;letter-spacing:-.02em" if serif else "font-weight:600"
    return A(" ".join(spans), "kara", round(start, 3), dur, style=f"{fam};font-size:{size}px;line-height:1.12;color:{color}",
             **({"hide": 1} if hide else {}))


def visual(show, t0, dur):
    k = show.get("kind", "statement")
    if k == "statement":
        return words_kara(show["text"], t0, dur * .9, show.get("hl", ()), size=show.get("size", 112))
    if k == "number":
        v = show["value"]
        dec = show.get("dec", 0)
        num = A("0", "count", t0 + .2, min(1.6, dur * .6), cls="num", style=f"font-size:220px;line-height:1;color:{RED}",
                **{"from": show.get("start", 0), "to": v, "dec": dec, "pre": show.get("pre", ""), "suf": show.get("suf", "")})
        lab = A(H.escape(show.get("label", "")), "rise", t0 + .5, .5, style="font-size:48px;font-weight:500;margin-top:24px;opacity:.85")
        return num + lab
    if k == "list":
        n = len(show["items"])
        out = ""
        for i, it in enumerate(show["items"]):
            out += A(f'<span style="color:{RED};font-family:&quot;Serif&quot;;font-weight:700;margin-right:28px">{i + 1:02d}</span>{H.escape(it)}',
                     "rise", t0 + .2 + i * dur * .8 / n, .45,
                     style="font-family:'Serif',serif;font-weight:700;font-size:78px;line-height:1.15;margin:16px 0")
        return (A(H.escape(show.get("title", "")), "fade", t0, .4, cls="lbl", style="margin-bottom:18px") if show.get("title") else "") + out
    if k == "compare":
        (l1, v1), (l2, v2) = show["left"], show["right"]
        col = lambda lab, val, c, d: A(f'<div class="lbl">{H.escape(lab)}</div><div class="num" style="font-size:150px;line-height:1.05;color:{c}">{H.escape(val)}</div>',
                                       "pop", t0 + d, .5, style="flex:1;background:#fff;border-radius:28px;padding:48px 56px;box-shadow:0 24px 60px rgba(10,10,10,.1)")
        return (f'<div style="display:flex;gap:56px">{col(l1, v1, INK, .2)}{col(l2, v2, TEAL, dur * .45)}</div>'
                + (A(H.escape(show.get("note", "")), "rise", t0 + dur * .6, .5, style="font-size:52px;font-weight:500;margin-top:40px;opacity:.85")
                   if show.get("note") else ""))
    if k == "term":
        return (A(H.escape(show["term"]), "pop", t0 + .1, .5, cls="num", style=f"font-size:200px;line-height:1;color:{RED}")
                + A(H.escape(show["text"]), "rise", t0 + .7, .6, style="font-size:58px;font-weight:500;line-height:1.3;margin-top:30px;max-width:1450px"))
    if k == "icon":            # big drawn icon beside a line of text
        side = badge(show["icon"], show.get("isize", 470), at=t0, ring=show.get("ring", RED))
        txt = words_kara(show["text"], t0 + .3, dur * .85, show.get("hl", ()), size=int(show.get("size", 96) * 1.18))
        return (f'<div style="display:flex;align-items:center;gap:90px">{side}<div style="flex:1">'
                + (A(H.escape(show["label"]), "fade", t0, .4, cls="lbl", style="margin-bottom:22px") if show.get("label") else "")
                + txt + "</div></div>")
    if k == "icons":           # a row of drawn icons, each with its label, one after another
        n = len(show["items"])
        cells = ""
        for i, (ic, lab) in enumerate(show["items"]):
            at = t0 + .15 + i * dur * .75 / n
            cells += (f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:34px">'
                      + badge(ic, 330, at=at, ring=RED if i == show.get("hi", -1) else "rgba(10,10,10,.12)")
                      + A(H.escape(lab), "rise", at + .3, .45, style="font-family:'Serif',serif;font-weight:700;font-size:66px;text-align:center;line-height:1.1")
                      + "</div>")
        return ((A(H.escape(show["title"]), "fade", t0, .4, cls="lbl", style="margin-bottom:46px;text-align:center") if show.get("title") else "")
                + f'<div style="display:flex;gap:40px;justify-content:center">{cells}</div>')
    if k == "timeline":        # a line that draws, dates that pop on it
        n = len(show["items"])
        line = A("", "growX", t0, min(1.2, dur * .4), style=f"position:absolute;left:0;right:0;top:146px;height:10px;border-radius:4px;background:{INK}")
        pts = ""
        for i, (when, lab) in enumerate(show["items"]):
            x = 4 + 92 * i / max(n - 1, 1)
            at = t0 + .3 + i * dur * .7 / n
            hot = i == show.get("hi", n - 1)
            pts += (f'<div style="position:absolute;left:{x}%;top:0;transform:translateX(-50%);width:420px;text-align:center">'
                    + A(H.escape(when), "rise", at, .4, cls="num", style=f"font-size:84px;color:{RED if hot else INK};height:120px")
                    + A("", "pop", at + .1, .4, style=f"width:44px;height:44px;border-radius:50%;margin:0 auto;background:{RED if hot else '#fff'};border:8px solid {RED if hot else INK};box-sizing:border-box")
                    + A(H.escape(lab), "rise", at + .25, .45, style="font-size:50px;font-weight:600;margin-top:34px;line-height:1.2")
                    + "</div>")
        return ((A(H.escape(show["title"]), "fade", t0, .4, cls="lbl", style="margin-bottom:40px") if show.get("title") else "")
                + f'<div style="position:relative;height:420px;margin:0 140px">{line}{pts}</div>')
    if k == "flow":            # boxes joined by arrows: cause and effect
        n = len(show["items"])
        out = ""
        for i, (ic, lab) in enumerate(show["items"]):
            at = t0 + .1 + i * dur * .75 / n
            hot = i == n - 1
            out += A(f'<div style="display:flex;flex-direction:column;align-items:center;gap:22px">{icon(ic, 210, RED if hot else INK, at + .2, .8, 6)}'
                     f'<div style="font-family:Sans;font-size:52px;font-weight:600;text-align:center;line-height:1.15">{H.escape(lab)}</div></div>',
                     "pop", at, .45, style=f"width:410px;background:#fff;border-radius:34px;padding:52px 24px;box-shadow:0 24px 60px rgba(10,10,10,.09);border:4px solid {RED if hot else 'transparent'}")
            if i < n - 1:
                out += A('<svg width="110" height="60" viewBox="0 0 110 60"><path d="M6 30 H96 M76 12 L98 30 L76 48" fill="none" stroke="#D93A12" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
                         "draw", at + .35, .5)
        return ((A(H.escape(show["title"]), "fade", t0, .4, cls="lbl", style="margin-bottom:44px;text-align:center") if show.get("title") else "")
                + f'<div style="display:flex;align-items:center;justify-content:center;gap:26px">{out}</div>')
    if k == "verdict":         # a claim, then a stamp: MYTH, TRUE, LEGEND
        st = show.get("stamp", "MYTH")
        col = TEAL if st in ("TRUE", "FACT") else RED
        return (f'<div style="position:relative;display:inline-block">'
                + (icon(show["icon"], 300, INK, t0, 1.0) if show.get("icon") else "")
                + words_kara(show["text"], t0 + .2, dur * .5, (), size=show.get("size", 104))
                + A(st, "stamp", t0 + dur * .55, .35, rot=-9,
                    style=f"position:absolute;right:-30px;bottom:-190px;white-space:nowrap;font-family:'Serif',serif;font-weight:700;font-size:120px;color:{col};"
                          f"border:12px solid {col};border-radius:20px;padding:6px 40px;letter-spacing:.06em;background:rgba(247,245,242,.85)")
                + "</div>")
    if k == "quote":           # a sourced quote, attributed
        return (A("“", "pop", t0, .4, cls="num", style=f"font-size:340px;line-height:.6;color:{RED};height:150px")
                + words_kara(show["text"], t0 + .25, dur * .7, show.get("hl", ()), size=show.get("size", 92))
                + A(f'<span style="display:inline-block;width:70px;height:6px;background:{RED};vertical-align:middle;margin-right:24px"></span>'
                    + H.escape(show["who"]), "rise", t0 + dur * .55, .5, style="font-size:46px;font-weight:600;margin-top:44px"))
    if k == "split":           # two sides, each with an icon: before and after, legend and archive
        (i1, l1, s1), (i2, l2, s2) = show["left"], show["right"]
        side = lambda ic, lab, sub, c, at, ring: A(
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:30px;text-align:center">{badge(ic, 360, c, ring, at + .1)}'
            f'<div class="lbl">{H.escape(lab)}</div><div style="font-family:\'Serif\',serif;font-weight:700;font-size:88px;line-height:1.1;color:{c}">{H.escape(sub)}</div></div>',
            "rise", at, .5, style="flex:1")
        mid = A(H.escape(show.get("mid", "vs")), "pop", t0 + dur * .4, .4, cls="num", style=f"font-size:90px;color:{RED};align-self:center")
        return f'<div style="display:flex;gap:40px;align-items:flex-start">{side(i1, l1, s1, INK, t0, "rgba(10,10,10,.12)")}{mid}{side(i2, l2, s2, TEAL, t0 + dur * .45, TEAL)}</div>'
    if k == "sketch":          # a hand-drawn scene that draws itself on, beside the line it illustrates
        art = sketch.scene(show["art"], t0 + .1, max(dur * .8, 1.2), seed=hash(show.get("text", "")) % 97, **show.get("opts", {}))
        txt = (A(H.escape(show["label"]), "fade", t0, .4, cls="lbl", style="margin-bottom:22px") if show.get("label") else "")
        txt += words_kara(show.get("text", ""), t0 + .25, dur * .8, show.get("hl", ()), size=show.get("size", 92)) if show.get("text") else ""
        left, right = (art, txt) if show.get("flip") else (txt, art)
        lw = "820px" if not show.get("flip") else "800px"
        return (f'<div style="display:flex;align-items:center;gap:60px;margin:0 -60px">'
                f'<div style="width:{lw};flex:none">{left}</div><div style="flex:1;display:flex;justify-content:center">{right}</div></div>')
    if k == "scene":           # the drawing alone, big, with a heading above
        art = sketch.scene(show["art"], t0 + .1, max(dur * .8, 1.2), **show.get("opts", {}))
        return ((A(H.escape(show["label"]), "fade", t0, .4, cls="lbl", style="margin-bottom:10px;text-align:center") if show.get("label") else "")
                + f'<div style="display:flex;justify-content:center;transform:scale(1.05)">{art}</div>')
    raise ValueError(k)


def synth(ep, voice_name):
    v = make_voice(voice_name)
    scale = getattr(v, "pace_scale", 1.0)
    out = []
    for c, ch in enumerate(ep["chapters"]):
        a, segs = passage(v, ch["title"] + ".", scale * .98)
        out.append(("title", c, None, a, segs))
        for b, beat in enumerate(ch["beats"]):
            a, segs = passage(v, beat["say"], scale * (1.0 if b % 2 else .98))
            out.append(("beat", c, b, a, segs))
    return out


def scenes(ep, items):
    sc, t, chapters, sounds = [], 0.0, [], []
    n_ch = len(ep["chapters"])
    for kind, c, b, a, segs in items:
        dur = len(a) / SR
        ch = ep["chapters"][c]
        if kind == "title":
            chapters.append((t, ch["title"]))
            html = (f'<div class="lbl" style="margin-bottom:26px;color:#fff;opacity:.85">Part {c + 1} of {n_ch}</div>'
                    + words_kara(H.escape(ch["title"]), .25, dur, size=140, hide=True, color="#fff"))
            if ch.get("art"):
                name, opts = ch["art"]
                html = (f'<div style="display:flex;align-items:center;gap:40px"><div style="flex:1">{html}</div>'
                        f'<div style="flex:none;transform:scale(.82);background:#F7F5F2;border-radius:48px;padding:30px 20px;box-shadow:0 40px 90px rgba(0,0,0,.25)">'
                        f'{sketch.scene(name, .3, max(dur, 1.4), **opts)}</div></div>')
            sc.append(dict(dur=dur + 1.1, push=.03, enter="", ghost=str(c + 1), html=html, voice=(a, .35), ci=c, nc=n_ch, bg=RED))
            sounds.append(("ding", t + .3, .1))
        else:
            beat = ch["beats"][b]
            shows = beat.get("shows") or [beat.get("show", dict(kind="statement", text=beat["say"]))]
            if len(shows) == 1:
                vis = visual(shows[0], .25, dur)
            else:                                   # one visual per sentence, each replacing the last
                assert len(shows) == len(segs), f"{len(shows)} visuals for {len(segs)} sentences: {beat['say'][:40]}"
                vis = ""
                for j, (shw, (_, s0, s1)) in enumerate(zip(shows, segs)):
                    a0 = (s0 + .25) if j else 0.0
                    end = (segs[j + 1][1] + .25) if j + 1 < len(segs) else dur + 2
                    vis += A(f'<div style="width:100%">{visual(shw, .25 + s0 if j else .25, max(s1 - s0, .8))}</div>', "life", round(a0, 3),
                             round(end - a0, 3), fi=.3 if j else .01, fo=.3,
                             style="position:absolute;inset:0;display:flex;align-items:center")
                    if j:
                        sounds.append(("pop", t + .25 + s0, .12))
            cap = (f'<div class="cap nochk">{words_kara(H.escape(beat["say"]), .25, dur, size=40, serif=False)}</div>'
                   if any(x.get("kind", "statement") not in ("statement", "quote", "verdict") for x in shows) else "")
            sc.append(dict(dur=dur + .75, push=.02, enter="", html=vis + cap,
                           chap=ch["title"], voice=(a, .25), ci=c, nc=n_ch))
            sounds.append(("pop", t + .3, .14))
        t += sc[-1]["dur"]
    return sc, chapters, sounds, t


def page(sc):
    starts, t = [], 0.0
    for s in sc:
        starts.append({"start": round(t, 3), "dur": s["dur"], "push": s.get("push", 0), "enter": s.get("enter", ""), "exit": s.get("exit", "")})
        t += s["dur"]
    def deco(i, s):
        """Moving background for every scene: a drifting dot grid and slow rings, so no frame is ever still."""
        r = 520 + 140 * (i % 3)
        x, y = [(1500, -180), (-260, 560), (1380, 640), (-200, -220)][i % 4]
        tabs = "".join(f'<i class="{"on" if k == s["ci"] else "done" if k < s["ci"] else ""}"></i>' for k in range(s["nc"]))
        return (A("", "float", 0, 1, cls="dots", amp=14, w=.35, ph=i)
                + A("", "spin", 0, 1, cls="ring", deg=4 if i % 2 else -4, style=f"left:{x}px;top:{y}px;width:{r}px;height:{r}px")
                + A("", "spin", 0, 1, cls="ring2", deg=-7 if i % 2 else 7, style=f"left:{x + 90}px;top:{y + 90}px;width:{r - 180}px;height:{r - 180}px")
                + f'<div class="tabs">{tabs}</div>')

    body = "".join(f'<div class="scene" id="s{i}">'
                   + (f'<div style="position:absolute;inset:0;background:{s["bg"]}"></div>' if s.get("bg") else "") + deco(i, s) + (f'<div class="ghost">{s["ghost"]}</div>' if s.get("ghost") else "")
                   + (f'<div class="chap">{H.escape(s["chap"]).upper()}</div>' if s.get("chap") else "")
                   + f'<div class="safe">{s["html"]}</div></div>' for i, s in enumerate(sc))
    return ("<!doctype html><html><head><meta charset='utf-8'><style>" + CSS.replace("FONTS/", f"{FONTS.resolve()}/") + "</style></head><body>"
            + '<div class="f"><div class="glow"></div><div class="mark">IB<span style="color:#D93A12">.</span></div>'
            + body + '<div class="bar"><i></i></div></div>'
            + f"<script>window.SCENES={json.dumps(starts)};window.TOTAL={t};{JS}</script></body></html>"), t


def render(slug, html, total, work):
    src = work / "video.html"
    src.write_text(html)
    mp4 = work / f"{slug}-silent.mp4"
    n = int(round((total + .5) * FPS))
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4)],
                          stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": Hh})
        pg.goto(src.resolve().as_uri())
        pg.evaluate("Promise.all([400,500,600].map(w => document.fonts.load(w + ' 40px Sans')).concat([document.fonts.load(\"700 40px 'Serif'\"),"
                    " document.fonts.load(\"italic 600 40px 'Serif'\")]))")
        for f in range(n):
            pg.evaluate(f"seek({f / FPS})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=90))
        b.close()
    ff.stdin.close()
    ff.wait()
    return mp4


def thumbnail(ep, work):
    """Two options, like the earlier videos (upload both to YouTube's Test & compare):
    A on brand red with the drawing, B on paper with the big type."""
    t = ep["thumb"]
    css = CSS.replace("FONTS/", f"{FONTS.resolve()}/") + "body{margin:0}.t{width:1280px;height:720px;position:relative;overflow:hidden;font-family:'Sans'}"
    art = ""
    if t.get("art"):
        name, opts = t["art"]
        art = (f"<div style='position:absolute;right:30px;top:50%;transform:translateY(-50%) scale(.68);transform-origin:right center;background:#F7F5F2;border-radius:44px;"
               f"padding:24px 10px;box-shadow:0 30px 80px rgba(0,0,0,.3)'>{sketch.scene(name, 0, 1, **opts)}</div>")
    a = (f"<div class='t' style='background:{RED}'>{art}"
         f"<div style='position:absolute;left:70px;top:56px;display:flex;align-items:center;gap:14px'><div style='width:60px;height:60px;background:#fff;"
         f"display:flex;align-items:center;justify-content:center;font-family:\"Serif\";font-weight:700;font-size:32px;color:{RED}'>IB<span style='color:{INK}'>.</span></div></div>"
         f"<div style='position:absolute;left:70px;width:{560 if art else 1100}px;top:170px;font-family:\"Serif\";font-weight:700;font-size:{t.get('size_a', 104)}px;"
         f"line-height:1.0;letter-spacing:-.02em;color:#fff'>{t.get('big_a', t['big'])}</div>"
         f"<div style='position:absolute;left:70px;bottom:60px;background:{INK};color:#fff;font-size:38px;font-weight:600;padding:12px 22px'>{H.escape(t.get('small', ''))}</div></div>")
    b = ("<div class='t' style='background:#F7F5F2'>"
         f"<div style='position:absolute;left:0;top:0;bottom:0;width:26px;background:{RED}'></div>"
         f"<div style='position:absolute;right:-40px;bottom:-120px;font-family:\"Serif\";font-weight:700;font-size:520px;line-height:1;color:#0A0A0A;opacity:.06'>{H.escape(t.get('ghost', ''))}</div>"
         f"<div style='position:absolute;left:80px;top:70px;font-family:\"Serif\";font-weight:700;font-size:40px'>IB<span style='color:{RED}'>.</span></div>"
         f"<div style='position:absolute;left:80px;right:70px;top:150px;font-family:\"Serif\";font-weight:700;font-size:{t.get('size', 132)}px;line-height:1.0;letter-spacing:-.03em'>{t['big']}</div>"
         f"<div style='position:absolute;left:80px;bottom:70px;font-size:46px;font-weight:600;color:{RED};letter-spacing:.02em'>{H.escape(t.get('small', ''))}</div></div>")
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1280, "height": 720})
        for name, body in (("thumbnail_a.jpg", a), ("thumbnail_b.jpg", b)):
            (work / "thumb.html").write_text(f"<!doctype html><html><head><style>{css}</style></head><body>{body}</body></html>")
            pg.goto((work / "thumb.html").resolve().as_uri())
            pg.evaluate("Promise.all([document.fonts.load(\"700 40px 'Serif'\"), document.fonts.load('600 40px Sans')])")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(work / name), type="jpeg", quality=92)
        br.close()
    (work / "thumbnail.jpg").write_bytes((work / "thumbnail_a.jpg").read_bytes())


def srt(sc, items, path):
    """English captions, one per sentence, from the voice's own timings."""
    stamp = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x * 1000 % 1000):03d}"
    out, t, k = [], 0.0, 1
    for s, (_, _, _, a, segs) in zip(sc, items):
        off = t + s["voice"][1]
        for sent, x, y in segs:
            out.append(f"{k}\n{stamp(off + x)} --> {stamp(off + y)}\n{sent}\n")
            k += 1
        t += s["dur"]
    path.write_text("\n".join(out))


def make(ep, voice_name=YOUTUBE_VOICE):
    work = OUT / ep["slug"]
    work.mkdir(parents=True, exist_ok=True)
    items = synth(ep, voice_name)
    sc, chapters, sounds, total = scenes(ep, items)
    html, total = page(sc)
    n = int((total + 1) * SR)
    voice = np.zeros(n, np.float32)
    t = 0.0
    for s in sc:
        a, off = s["voice"]
        i = int((t + off) * SR)
        voice[i:i + len(a)] += a[: n - i]
        t += s["dur"]
    fx = S.track(sounds, total)
    g = .12 / max(np.sqrt(np.mean(voice[voice != 0] ** 2)), 1e-6)
    write_wav(work / "voice.wav", voice * g)
    write_wav(work / "sfx.wav", fx[:n] * g)
    silent = render(ep["slug"], html, total, work)
    final = work / f"{ep['slug']}.mp4"
    graph = (f"[1:a]{MASTER}[v];[v][2:a]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")   # YouTube plays at -14 LUFS
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(work / "voice.wav"), "-i", str(work / "sfx.wav"),
                    "-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", "-movflags", "+faststart", str(final)], check=True)
    thumbnail(ep, work)
    srt(sc, items, work / f"{ep['slug']}.srt")
    stamp = lambda s: f"{int(s // 60)}:{int(s % 60):02d}"
    chap_lines = "\n".join(f"{stamp(0 if i == 0 else c)} {title}" for i, (c, title) in enumerate(chapters))
    desc = ep["description"].strip() + "\n\nChapters\n" + chap_lines + (
        "\n\nNarration: AI-generated voice; script and analysis are our original work. "
        "Educational content, not financial advice. Not affiliated with any bank mentioned.")
    meta = dict(title=ep["title"], description=desc, tags=ep.get("tags", []), duration_s=round(total, 1), voice=voice_name,
                youtube_altered_or_synthetic="Yes: realistic synthetic narration voice (not a real person). Tick it in YouTube Studio.",
                made_for_kids=False, music_in_master=False)
    json.dump(meta, open(work / "metadata.json", "w"), indent=1)
    (work / "description.txt").write_text(desc)
    print(f"  -> {final.name}  {total / 60:.1f} min  voice {voice_name}")
    return final, meta
