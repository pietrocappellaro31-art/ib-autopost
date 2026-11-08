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
"""


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
            html = (f'<div class="lbl" style="margin-bottom:26px">Part {c + 1} of {n_ch}</div>'
                    + words_kara(H.escape(ch["title"]), .25, dur, size=120, hide=True))
            sc.append(dict(dur=dur + 1.1, push=.03, enter="", ghost=str(c + 1), html=html, voice=(a, .35)))
            sounds.append(("ding", t + .3, .1))
        else:
            beat = ch["beats"][b]
            show = beat.get("show", dict(kind="statement", text=beat["say"]))
            vis = visual(show, .25, dur)
            cap = "" if show.get("kind", "statement") == "statement" else (
                f'<div class="cap nochk">{words_kara(H.escape(beat["say"]), .25, dur, size=40, serif=False)}</div>')
            sc.append(dict(dur=dur + .75, push=.02, enter="", html=vis + cap,
                           chap=ch["title"], voice=(a, .25)))
            sounds.append(("pop", t + .3, .14))
        t += sc[-1]["dur"]
    return sc, chapters, sounds, t


def page(sc):
    starts, t = [], 0.0
    for s in sc:
        starts.append({"start": round(t, 3), "dur": s["dur"], "push": s.get("push", 0), "enter": s.get("enter", ""), "exit": s.get("exit", "")})
        t += s["dur"]
    body = "".join(f'<div class="scene" id="s{i}">' + (f'<div class="ghost">{s["ghost"]}</div>' if s.get("ghost") else "")
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
    t = ep["thumb"]
    html = ("<!doctype html><html><head><style>" + CSS.replace("FONTS/", f"{FONTS.resolve()}/")
            + "body{margin:0}.t{width:1280px;height:720px;background:#F7F5F2;position:relative;overflow:hidden;font-family:'Sans'}"
            "</style></head><body><div class='t'>"
            f"<div style='position:absolute;left:0;top:0;bottom:0;width:26px;background:{RED}'></div>"
            f"<div style='position:absolute;right:-40px;bottom:-120px;font-family:\"Serif\";font-weight:700;font-size:520px;line-height:1;color:#0A0A0A;opacity:.06'>{H.escape(t.get('ghost', ''))}</div>"
            f"<div style='position:absolute;left:80px;top:70px;font-family:\"Serif\";font-weight:700;font-size:40px'>IB<span style='color:{RED}'>.</span></div>"
            f"<div style='position:absolute;left:80px;right:70px;top:150px;font-family:\"Serif\";font-weight:700;font-size:{t.get('size', 132)}px;line-height:1.0;letter-spacing:-.03em'>{t['big']}</div>"
            f"<div style='position:absolute;left:80px;bottom:70px;font-size:46px;font-weight:600;color:{RED};letter-spacing:.02em'>{H.escape(t.get('small', ''))}</div>"
            "</div></body></html>")
    (work / "thumb.html").write_text(html)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto((work / "thumb.html").resolve().as_uri())
        pg.evaluate("document.fonts.load(\"700 40px 'Serif'\")")
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(work / "thumbnail.jpg"), type="jpeg", quality=92)
        b.close()


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
