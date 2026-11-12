"""
YouTube long-form explainer engine (8 Nov) for The Banker's Notebook / the
@investmentbankinginterviews channel: 1920x1080, paper ground, brand fonts,
voiced by the day's trial voice (voice_clone.youtube_voice(); Kokoro, Apache 2.0; GEORGE to 10 Nov), sound effects from sfx.py,
and an original music bed from music.py ducked under the voice.

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
Outputs in out/<slug>/: <slug>.mp4, thumbnail_a.jpg and thumbnail_b.jpg, <slug>.srt,
metadata.json (title, description with chapter times, tags, AI-disclosure setting),
description.txt, layout.json (drawings fitted, layout problems found while rendering)
and sound.json (voice over music, DNSMOS, loudness).

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
                f'<div style="width:{lw};flex:none">{left}</div><div style="flex:1;display:flex;justify-content:center"><div>{right}</div></div></div>')
    if k == "scene":           # the drawing alone, big, with a heading above
        art = sketch.scene(show["art"], t0 + .1, max(dur * .8, 1.2), **show.get("opts", {}))
        return ((A(H.escape(show["label"]), "fade", t0, .4, cls="lbl", style="margin-bottom:10px;text-align:center") if show.get("label") else "")
                + f'<div style="display:flex;justify-content:center;transform:scale(1.05)">{art}</div>')
    raise ValueError(k)


def synth(ep, voice_name, work=None):
    """11 Nov: every line is cached in work/synth.pkl, keyed on the voice, the speed and the words, so a
    re-render after a visual fix, a timing check before the render, or a one-line script edit only
    synthesises what changed. Visual/sentence counts are checked before any synthesis."""
    import pickle
    from voice import split_sentences
    for ch in ep["chapters"]:
        for beat in ch["beats"]:
            n = len(beat.get("shows") or [1])
            assert n == 1 or n == len(split_sentences(beat["say"])), f"{n} visuals for {len(split_sentences(beat['say']))} sentences: {beat['say'][:50]}"
    cache = work / "synth.pkl" if work else None
    store = pickle.load(open(cache, "rb")) if cache and cache.exists() else {}
    if not isinstance(store, dict):
        store = {}
    v, hits = None, 0
    def say(text, speed):
        nonlocal v, hits
        k = (voice_name, round(speed, 4), text)
        if k in store:
            hits += 1
            return store[k]
        if v is None:
            v = make_voice(voice_name)
        store[k] = passage(v, text, speed)
        return store[k]
    from voice_clone import voices, key as vkey
    vd = voices().get(vkey(voice_name), {})
    scale = vd.get("speed", 1.0) if vd.get("engine") == "kokoro" else 1.0      # = make_voice(...).pace_scale
    out = []
    try:
        for c, ch in enumerate(ep["chapters"]):
            a, segs = say(ch["title"] + ".", scale * .98)
            out.append(("title", c, None, a, segs))
            for b, beat in enumerate(ch["beats"]):
                a, segs = say(beat["say"], scale * (1.0 if b % 2 else .98))
                out.append(("beat", c, b, a, segs))
    finally:                                    # 12 Nov: keep the lines already said even if one fails (a missing word)
        if cache:
            pickle.dump(store, open(cache, "wb"))
    print(f"  voice: {hits} of {len(out)} lines reused from synth.pkl", flush=True)
    return out


def takes(ep, items, voice_name, work):
    """12 Nov: the long video gets a takes.json like the Shorts. Every line (chapter titles and beats) is
    transcribed once on its own and checked word for word; the result is cached per voice and text in
    work/takes_cache.json, so a re-render only transcribes the lines that changed."""
    from voice_check import transcribe, wer
    cache_p = work / "takes_cache.json"
    cache = json.load(open(cache_p)) if cache_p.exists() else {}
    log, clip = [], work / "_line.wav"
    for kind, c, b, a, segs in items:
        text = ep["chapters"][c]["title"] + "." if kind == "title" else ep["chapters"][c]["beats"][b]["say"]
        k = f"{voice_name}|{text}"
        if k not in cache:
            write_wav(clip, a / max(np.abs(a).max(), 1e-6) * .7)
            heard = transcribe(clip)
            cache[k] = dict(heard=heard)
        heard = cache[k]["heard"]                                   # the score is recomputed, so a better word check applies
        log.append(dict(kind=kind, chapter=c, beat=b, text=text, heard=heard, wer=round(wer(text, heard), 3)))
    clip.unlink(missing_ok=True)
    json.dump(cache, open(cache_p, "w"), indent=0)
    json.dump(log, open(work / "takes.json", "w"), indent=1)
    exact = sum(1 for x in log if x["wer"] == 0)
    print(f"  takes: {exact} of {len(log)} lines heard word for word", flush=True)
    for x in log:
        if x["wer"] > 0:
            print(f"    miss ({x['wer']:.0%}): {x['text'][:70]}\n      heard: {x['heard'][:70]}", flush=True)
    return log


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
            # 12 Nov: every chapter card holds at least 2.8 s (a short title like "Germany's bill" flashed by in 2 s on #4)
            sc.append(dict(dur=max(dur + 1.1, ep.get("card_min", 2.8)), push=.03, enter="", ghost=str(c + 1), html=html, voice=(a, .35),
                           ci=c, nc=n_ch, bg=RED))
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


FIT_JS = r"""
window.fitSvg = function (svg, zmax, zmin) {
  // Zoom the viewBox onto what was actually drawn, so a small drawing fills its box (10 Nov, after
  // "drawings that are small in their box look lost"). Keeps the 800 x 640 shape and the element size.
  if (svg.dataset.fit === 'no' || svg.dataset.fitted) return 0;
  let b; try { b = svg.getBBox(); } catch (e) { return 0; }
  if (!b.width || !b.height) return 0;
  const pad = 30, ar = 800 / 640;
  let x = b.x - pad, y = b.y - pad, w = b.width + 2 * pad, h = b.height + 2 * pad;
  if (w / h > ar) { const nh = w / ar; y -= (nh - h) / 2; h = nh; } else { const nw = h * ar; x -= (nw - w) / 2; w = nw; }
  const lim = (k) => { x -= (w * k - w) / 2; y -= (h * k - h) / 2; w *= k; h *= k; };
  if (w < 800 / zmax) lim(800 / zmax / w);
  if (w > 800 / zmin) lim(800 / zmin / w);
  svg.setAttribute('viewBox', `${x.toFixed(1)} ${y.toFixed(1)} ${w.toFixed(1)} ${h.toFixed(1)}`);
  svg.dataset.fitted = (800 / w).toFixed(2);
  return 1;
};
window.fitSketches = function (zmax = 1.5, zmin = .8) {
  // Each scene is measured at its end, when everything in it has been drawn.
  let n = 0;
  window.SCENES.forEach((s, i) => {
    seek(s.start + s.dur - .05);
    document.getElementById('s' + i).querySelectorAll('svg.sk').forEach(svg => { n += fitSvg(svg, zmax, zmin); });
  });
  seek(0);
  return n;
};
window.check16 = function (t) {
  // 16:9 layout check: no visible text or drawing off the frame or under the header, and the main
  // content clear of the caption line. 11 Nov: an element still inside its entry animation (a stamp
  // mid-slam, a slide on its way in) is skipped until data-at + data-d has passed, so a clean render reads 0.
  const bad = [];
  document.querySelectorAll('.scene').forEach((s, si) => {
    if (s.style.visibility !== 'visible') return;
    const local = (t === undefined) ? 1e9 : t - window.SCENES[si].start;
    const moving = n => { for (let q = n; q && q !== s; q = q.parentElement)
      if (q.classList && q.classList.contains('a') && local < +(q.dataset.at || 0) + +(q.dataset.d || .5) + .05) return true; return false; };
    const cap = s.querySelector('.cap');
    const capTop = cap ? cap.getBoundingClientRect().top : 2000;
    s.querySelectorAll('.safe *').forEach(n => {
      if (n.closest('.cap') || !n.childNodes.length || n.tagName === 'tspan') return;
      for (let q = n; q && q !== s; q = q.parentElement) if (getComputedStyle(q).opacity === '0') return;
      const r = n.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      if (moving(n)) return;
      const isText = n.tagName === 'text' || [...n.childNodes].some(c => c.nodeType === 3 && c.textContent.trim());
      if (!isText && n.tagName !== 'svg') return;
      if (r.left < 30 || r.right > 1890 || r.top < 105 || r.bottom > 1050 || (r.bottom > capTop - 6 && r.top < capTop))
        bad.push(`${s.id} <${n.tagName.toLowerCase()}> "${(n.textContent || '').trim().slice(0, 30)}" ${Math.round(r.left)},${Math.round(r.top)} to ${Math.round(r.right)},${Math.round(r.bottom)}`);
    });
  });
  return bad;
};
"""


def page(sc):
    starts, t = [], 0.0
    for s in sc:
        starts.append({"start": round(t, 3), "dur": s["dur"], "push": s.get("push", 0), "enter": s.get("enter", ""), "exit": s.get("exit", "")})
        t += s["dur"]
    def deco(i, s):
        """Moving background for every scene: a drifting dot grid and slow rings, so no frame is ever still."""
        r = 520 + 140 * (i % 3)
        x, y = [(1500, -180), (-260, 560), (1380, 640), (-200, -220)][i % 4]
        tw = min(90, 380 // max(s["nc"], 1))                      # 10 Nov: narrower tabs for 5+ chapters, clear of the chapter name
        tabs = "".join(f'<i class="{"on" if k == s["ci"] else "done" if k < s["ci"] else ""}" style="width:{tw}px"></i>' for k in range(s["nc"]))
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
            + f"<script>window.SCENES={json.dumps(starts)};window.TOTAL={t};{JS}{FIT_JS}</script></body></html>"), t


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
        fitted = pg.evaluate("fitSketches()")
        zooms = pg.evaluate("[...document.querySelectorAll('svg.sk')].map(s => +(s.dataset.fitted || 1))")
        print(f"  fitted {fitted} drawings to their boxes (zoom {min(zooms):.2f} to {max(zooms):.2f}, median {sorted(zooms)[len(zooms) // 2]:.2f})", flush=True)
        bad = {}
        for f in range(n):
            pg.evaluate(f"seek({f / FPS})")
            if f % 12 == 6:
                for x in pg.evaluate(f"check16({f / FPS})"):
                    bad.setdefault(x.split(" ")[0] + " " + x.split('"')[1], f"{f / FPS:.1f}s {x}")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=90))
        b.close()
    ff.stdin.close()
    ff.wait()
    json.dump(dict(layout_problems=list(bad.values()), drawings_fitted=fitted, zoom=[min(zooms), max(zooms)]), open(work / "layout.json", "w"), indent=1)
    print(f"  layout: {len(bad)} problems" + "".join(f"\n    {v}" for v in list(bad.values())[:20]), flush=True)
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
    artb = ""
    if t.get("art_b", t.get("art")):                               # 10 Nov: B carries a drawing too, so both test options have art
        name, opts = t.get("art_b", t.get("art"))
        artb = (f"<div style='position:absolute;right:20px;top:50%;transform:translateY(-46%) scale(.66);transform-origin:right center'>"
                f"{sketch.scene(name, 0, 1, seed=3, **opts)}</div>")
    b = ("<div class='t' style='background:#F7F5F2'>"
         f"<div style='position:absolute;left:0;top:0;bottom:0;width:26px;background:{RED}'></div>"
         f"<div style='position:absolute;right:-40px;bottom:-120px;font-family:\"Serif\";font-weight:700;font-size:520px;line-height:1;color:#0A0A0A;opacity:.06'>{H.escape(t.get('ghost', ''))}</div>"
         + artb +
         f"<div style='position:absolute;left:80px;top:70px;font-family:\"Serif\";font-weight:700;font-size:40px'>IB<span style='color:{RED}'>.</span></div>"
         f"<div style='position:absolute;left:80px;{'width:660px' if artb else 'right:70px'};top:150px;font-family:\"Serif\";font-weight:700;font-size:{t.get('size', 132)}px;line-height:1.0;letter-spacing:-.03em'>{t['big']}</div>"
         f"<div style='position:absolute;left:80px;bottom:70px;font-size:46px;font-weight:600;color:{RED};letter-spacing:.02em'>{H.escape(t.get('small', ''))}</div></div>")
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1280, "height": 720})
        for name, body in (("thumbnail_a.jpg", a), ("thumbnail_b.jpg", b)):
            (work / "thumb.html").write_text(f"<!doctype html><html><head><style>{css}</style></head><body>{body}</body></html>")
            pg.goto((work / "thumb.html").resolve().as_uri())
            pg.evaluate("Promise.all([document.fonts.load(\"700 40px 'Serif'\"), document.fonts.load('600 40px Sans')])")
            pg.add_script_tag(content=FIT_JS)
            pg.evaluate("document.querySelectorAll('svg.sk').forEach(s => fitSvg(s, 1.5, .8))")
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


def mix(ep, work):
    """Voice, sound effects and the video's own music bed, ducked under the
    voice, mastered to -14 LUFS (what YouTube plays at). Rerunnable on its own
    (remix) since the silent video and the stems stay in out/<slug>/."""
    import music
    tm = json.load(open(work / "timing.json"))
    seed = ep.get("music_seed", sum(map(ord, ep["slug"])))
    # 12 Nov (Pietro's music library): pick the library track that fits ep["mood"] and write our own bed
    # in its tempo, key, mode and feel. The reference's audio never enters the mix (music_library.py).
    import music_library
    ref = music_library.pick(ep.get("mood", "curious"), "long", slug=ep["slug"]) if ep.get("music_library", True) else None
    if ref:
        bed, info = music_library.bed(ref, tm["total"], seed=seed, breaks=tm["chapters"][1:])
        info["upload_note"] = music_library.instructions(ref, "long")
        print(f"  music: library pick {ref['id']} for mood {ep.get('mood', 'curious')!r} -> original bed at "
              f"{info['bpm']:.0f} BPM, {info['key']} {info['mode']}, drums {info['drums']}", flush=True)
    else:
        bed, info = music.track(tm["total"], seed=seed, breaks=tm["chapters"][1:])
    music.write(work / "music.wav", bed)
    json.dump(info, open(work / "music.json", "w"))
    final = work / f"{ep['slug']}.mp4"
    mv = ep.get("music_level", .2)
    graph = (f"[1:a]{MASTER},aresample=48000,asplit=2[v][key];[2:a]aresample=48000[fx];"
             f"[3:a]volume={mv}[m];[m][key]sidechaincompress=threshold=0.02:ratio=5:attack=30:release=350:makeup=1[md];"
             f"[v][fx][md]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(work / f"{ep['slug']}-silent.mp4"), "-i", str(work / "voice.wav"),
                    "-i", str(work / "sfx.wav"), "-i", str(work / "music.wav"),
                    "-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", "-movflags", "+faststart", str(final)], check=True)
    trim_loudness(final)
    # the ducked music on its own, to measure how far the voice sits above it
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(work / "voice.wav"), "-i", str(work / "music.wav"), "-filter_complex",
                    f"[0:a]{MASTER},aresample=48000[key];[1:a]aresample=48000,volume={mv}[m];"
                    f"[m][key]sidechaincompress=threshold=0.02:ratio=5:attack=30:release=350:makeup=1[md]",
                    "-map", "[md]", "-ac", "1", str(work / "music_ducked.wav")], check=True)
    return final


def lufs_of(path):
    lo = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    tail = lo[lo.rfind("Summary:"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail).group(1))


def trim_loudness(final, target=-14.0, ceiling=-1.5):
    """12 Nov: one-pass loudnorm left #4 at -14.6 and #5 at -15.0 LUFS (the true-peak ceiling holds it back).
    Second stage: measure, apply the missing gain, catch the peaks with a look-ahead limiter, keep the video
    stream as it is, and keep the result only if it lands closer to the target without breaking the ceiling."""
    i0, tp0 = lufs_of(final)
    if abs(i0 - target) < .4:
        return i0
    tmp = final.with_name(final.stem + "-trim.mp4")
    lim = 10 ** ((ceiling - .4) / 20)
    for extra in (0.0, .3, .6):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-af",
                        f"volume={target - i0 + extra:.2f}dB,alimiter=limit={lim:.3f}:attack=2:release=60:level=false,aresample=48000",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(tmp)], check=True)
        i1, tp1 = lufs_of(tmp)
        if i1 >= target - .3 or extra == .6:
            break
    if abs(i1 - target) < abs(i0 - target) and tp1 <= -1.0:                  # -1 dBTP is the usual streaming ceiling
        tmp.replace(final)
        print(f"  loudness: {i0} -> {i1} LUFS, {tp0} -> {tp1} dBTP (second stage)", flush=True)
        return i1
    tmp.unlink(missing_ok=True)
    print(f"  loudness: second stage not kept ({i1} LUFS, {tp1} dBTP)", flush=True)
    return i0


def sound_report(work, final):
    """10 Nov: the long video's sound measured on every render, like the Shorts: voice over the ducked
    music while speaking, DNSMOS of the voice and of the final mix, loudness and true peak."""
    import quality
    v, m = quality.load16(work / "voice.wav"), quality.load16(work / "music_ducked.wav")
    k = min(len(v), len(m))
    v, m = v[:k], m[:k]
    win = 1600
    rv = np.sqrt(np.convolve(v ** 2, np.ones(win) / win, "same"))
    on = rv > .25 * np.percentile(rv[rv > 1e-4], 90)
    vom = 20 * np.log10(np.sqrt(np.mean(v[on] ** 2)) / max(np.sqrt(np.mean(m[on] ** 2)), 1e-9))
    lo = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(final), "-af", "ebur128=peak=true", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    tail = lo[lo.rfind("Summary:"):]
    lufs = float(re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail).group(1))
    rep = dict(voice_over_music_db=round(float(vom), 1), dnsmos_voice=quality.score(work / "voice.wav"),
               dnsmos_mix=quality.score(final), lufs=lufs, true_peak_dbtp=tp)
    json.dump(rep, open(work / "sound.json", "w"), indent=1)
    print(f"  sound: voice {rep['voice_over_music_db']} dB over the music while speaking, DNSMOS voice {rep['dnsmos_voice']['ovrl']} / mix "
          f"{rep['dnsmos_mix']['ovrl']}, {lufs} LUFS, {tp} dBTP" + ("  (voice under 15 dB over the music: lower music_level)" if vom < 15 else ""), flush=True)
    return rep


def describe(ep, chapters, total, voice_name, work):
    """description.txt and metadata.json. 10 Nov (Pietro: "since my channel is verified, make sure to add
    links to the sources and references"): every source is listed with its link, from ep["sources"], a list
    of (label, url). Hashtags (ep["hashtags"], up to 3, our choice) go at the end of the description; the
    tags (ep["tags"]) are not hashtags: they go in Studio's Tags field (Details, Show more), max 500 characters."""
    stamp = lambda s: f"{int(s // 60)}:{int(s % 60):02d}"
    chap_lines = "\n".join(f"{stamp(0 if i == 0 else c)} {title}" for i, (c, title) in enumerate(chapters))
    src = ""
    if ep.get("sources"):
        src = "\n\nSources and references\n" + "\n".join(f"- {label}: {url}" for label, url in ep["sources"])
    if ep.get("source_note"):
        src += "\n" + ep["source_note"]
    tags = ep.get("hashtags", [])
    desc = (ep["description"].strip() + src + "\n\nChapters\n" + chap_lines
            + "\n\nNarration: AI-generated voice; script and analysis are our original work. "
              "Educational content, not financial advice. Not affiliated with any company mentioned."
            + ("\n\n" + " ".join("#" + h.lstrip("#") for h in tags) if tags else ""))
    tag_field = ", ".join(ep.get("tags", []))
    assert len(desc) <= 5000, f"description is {len(desc)} characters; YouTube allows 5,000"
    assert len(tag_field) <= 500, f"tags are {len(tag_field)} characters; Studio allows 500"
    meta = dict(title=ep["title"], description=desc, tags=ep.get("tags", []), tags_for_studio=tag_field, hashtags=tags,
                duration_s=round(total, 1), voice=voice_name,
                youtube_altered_or_synthetic="Yes: realistic synthetic narration voice (not a real person). Tick it in YouTube Studio.",
                made_for_kids=False, music="original, made for this video by build/music.py (no licence needed)"
                + (f"; written in the tempo, key and feel of the library pick ({mj['reference_title']}), no audio, melody or chords from it"
                   if (mj := (json.load(open(work / "music.json")) if (work / "music.json").exists() else {})).get("reference") else ""),
                music_library_pick=mj.get("upload_note"))
    json.dump(meta, open(work / "metadata.json", "w"), indent=1)
    (work / "description.txt").write_text(desc)
    return meta


def redescribe(ep):
    """Rewrite description.txt and metadata.json after a render, without rendering again."""
    work = OUT / ep["slug"]
    tm = json.load(open(work / "timing.json"))
    chapters = [(c, ch["title"]) for c, ch in zip(tm["chapters"], ep["chapters"])]
    old = json.load(open(work / "metadata.json"))
    return describe(ep, chapters, tm["total"], old.get("voice", YOUTUBE_VOICE), work)


def make(ep, voice_name=YOUTUBE_VOICE):
    work = OUT / ep["slug"]
    work.mkdir(parents=True, exist_ok=True)
    items = synth(ep, voice_name, work)
    try:
        takes(ep, items, voice_name, work)
    except Exception as e:                                          # a word check must never cost the render
        print("  takes failed:", e)
    sc, chapters, sounds, total = scenes(ep, items)
    html, total = page(sc)
    print(f"  timing: {total / 60:.2f} min, {len(sc)} scenes, {int((total + .5) * FPS)} frames to render", flush=True)
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
    json.dump(dict(total=total, chapters=[c for c, _ in chapters]), open(work / "timing.json", "w"))
    final = mix(ep, work)
    try:
        sound_report(work, final)
    except Exception as e:                                          # a report must never cost the render
        print("  sound report failed:", e)
    thumbnail(ep, work)
    srt(sc, items, work / f"{ep['slug']}.srt")
    meta = describe(ep, chapters, total, voice_name, work)
    print(f"  -> {final.name}  {total / 60:.1f} min  voice {voice_name}")
    return final, meta
