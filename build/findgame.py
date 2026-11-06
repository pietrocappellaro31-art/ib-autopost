"""
"Find the error": the reusable voiced game format (first built as
reels_find.py, 6 Nov). An episode is a small config; this module does the rest.

    hook      a passage read before the countdown ("One number ... is wrong")
    go        the word that starts the 10-second countdown
    countdown "Check every line", then Three, Two, One, Time
    reveal    passages; every sentence can focus rows of the table and fire an
              event: pen (circle the wrong cell), strike, fix (show the right
              value), or chip (show a rule card above the table)
    close     big centred sentences, the last one held to the end

Voice: whole passages per call (voice.passage) for natural intonation, at a
slightly unhurried pace, then a recording chain (voice.MASTER), a faint room
tone and loudness at -16 LUFS. Captions are burned in word by word.
"""

import base64
import io
import json
import pathlib
import subprocess

import numpy as np
from PIL import Image

from motion import A, build, OUT
from voice import Voice, passage, write_wav, SR, MASTER

RED, TEAL = "#D93A12", "#5EC8B4"
COUNT = 10.0
FOCUS = {"n": "rgba(255,255,255,.09)", "t": "rgba(94,200,180,.18)", "r": "rgba(217,58,18,.2)"}


def words_in(voice, sentence, dur):
    toks = sentence.split()
    lens = [max(len(voice.phonemes(t.strip(".,!?"))), 1) for t in toks]
    acc, out = 0, []
    for w, n in zip(toks, lens):
        out.append((w, round(dur * acc / sum(lens), 3)))
        acc += n
    return out


def synth(ep, voice_name):
    v = Voice(voice_name)
    # Fail before rendering anything if a word has no pronunciation.
    for block in [ep["hook"], ep["go"], ep["look"], "Three. Two. One.", "Time.", *[" ".join(x[0] for x in p) for p in ep["reveal"]],
                  " ".join(ep["close"])]:
        v.phonemes(block)
    sp = ep.get("speed", .95)
    parts = {}
    parts["hook"] = passage(v, ep["hook"], sp)
    for key, text in (("go", ep["go"]), ("look", ep["look"]), ("n3", "Three."), ("n2", "Two."), ("n1", "One."), ("time", "Time.")):
        parts[key] = passage(v, text, 1.0)
    for i, p in enumerate(ep["reveal"]):
        parts[f"r{i}"] = passage(v, " ".join(x[0] for x in p), sp - .01 * (i % 2))   # small variation in pace
    parts["close"] = passage(v, " ".join(ep["close"]), sp)
    return v, parts


def timeline(parts):
    dur = lambda k: len(parts[k][0]) / SR
    at, t = {}, .25
    at["hook"] = t
    t += dur("hook") + .4
    at["go"] = t
    count0 = t + .1
    at["look"] = count0 + 3.2
    for k, n in (("n3", 7), ("n2", 8), ("n1", 9)):
        at[k] = count0 + n
    at["time"] = count0 + COUNT
    t = at["time"] + dur("time") + .55
    i = 0
    while f"r{i}" in parts:
        at[f"r{i}"] = t
        t += dur(f"r{i}") + .45
        i += 1
    at["close"] = t + .2
    total = at["close"] + dur("close") + 1.6
    return at, count0, total


def noise_tile():
    rng = np.random.default_rng(7)
    a = (rng.random((170, 170)) * 255).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(a, "L").resize((512, 512), Image.BILINEAR).save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def caption(words, start, dur, cols, big=False, hold=None, first=False, until=None):
    spans = []
    for w, t in words:
        c = cols.get(w.strip(".,!?").lower())
        spans.append(f'<span class="w" data-t="{t}"' + (f' data-c="{c}"' if c else "") + f'>{w}</span>')
    inner = " ".join(spans)
    if big:
        return A(A(f'<div class="num" style="font-size:92px;line-height:1.1">{inner}</div>', "kara", start, dur),
                 "life", start - .1, hold or dur + .45, fo=.01 if hold else .25,
                 style="position:absolute;left:0;right:0;top:470px;text-align:center;z-index:8")
    begin = -1 if first else start - .05
    end = start + dur + .3
    if until is not None:
        end = min(end, until - .02)                  # gone before the next caption arrives
    return A(A(f'<div style="font-size:50px;font-weight:600;line-height:1.25">{inner}</div>', "kara", start, dur),
             "life", begin, end - begin, fi=.12, fo=.12,
             style="position:absolute;left:0;right:0;top:1060px;text-align:center;z-index:8;"
                   "text-shadow:0 2px 14px rgba(0,0,0,.8)")


def scene(ep, v, parts, at, count0, total):
    rows, cols_head = ep["rows"], ep["cols"]
    wr, wc, wrong_txt, right_txt = ep["wrong"]
    card_top, head, rh = 590, 100, 92
    row_y = [card_top + head + rh * i + rh / 2 for i in range(len(rows))]
    end_card = at["close"] - .2
    caps, bars, chips = [], "", ""
    ev = {}

    def add_caps(key, colmap, big=False, first_key=False, hold_last=False):
        """One caption per sentence; long sentences are split into chunks of at
        most 7 words, each on screen while its own words are spoken."""
        audio, segs = parts[key]
        for j, (s, a, b) in enumerate(segs):
            cm = colmap[j] if isinstance(colmap, list) else colmap
            ws = words_in(v, s, b - a)
            n = 1 if big else -(-len(ws) // 7)
            size = -(-len(ws) // n)
            chunks = [ws[k:k + size] for k in range(0, len(ws), size)]
            for c, chunk in enumerate(chunks):
                c0 = chunk[0][1]
                c1 = chunks[c + 1][0][1] if c + 1 < len(chunks) else b - a
                last = hold_last and j == len(segs) - 1 and c == len(chunks) - 1
                caps.append(dict(words=[(w, round(t - c0, 3)) for w, t in chunk], start=at[key] + a + c0, dur=c1 - c0,
                                 cols=cm, big=big, hold=(total + 2) if last else None, first=(first_key and j == 0 and c == 0)))

    add_caps("hook", ep.get("hook_cols", {}), first_key=True)
    add_caps("go", {"go.": RED, "go": RED})
    add_caps("look", {})
    add_caps("time", {"time": RED})

    spot_keys = []
    for i, p in enumerate(ep["reveal"]):
        key = f"r{i}"
        segs = parts[key][1]
        add_caps(key, [x[2] if len(x) > 2 else {} for x in p])
        for j, ((text, focus, *rest), (s, a, b)) in enumerate(zip(p, segs)):
            t0, t1 = at[key] + a, at[key] + b
            event = rest[1] if len(rest) > 1 else None
            if focus:
                rws, tone = focus
                top, n = min(rws), max(rws) - min(rws) + 1
                bars += A("", "life", t0, (t1 - t0) + .35, fi=.2, fo=.25,
                          style=f"position:absolute;left:-20px;right:-20px;top:{head + rh * top}px;height:{rh * n}px;"
                                f"background:{FOCUS[tone]};border-radius:14px")
                spot_keys.append([t0, 90, (row_y[top] + row_y[top + n - 1]) / 2 - 450, .9, 1])
            if event:
                kind = event if isinstance(event, str) else event[0]
                ev.setdefault(kind, t0)
    # Rule chips, stacked above the table in the order they are said.
    chip_list = []
    for i, p in enumerate(ep["reveal"]):
        for j, ((text, focus, *rest), (s, a, b)) in enumerate(zip(p, parts[f"r{i}"][1])):
            event = rest[1] if len(rest) > 1 else None
            if isinstance(event, tuple) and event[0] == "chip":
                chip_list.append((at[f"r{i}"] + a, event[1]))
    chips = "".join(
        A(f'<div style="display:inline-block;background:rgba(94,200,180,.14);border:2px solid {TEAL};'
          f'border-radius:999px;padding:14px 28px;font-size:40px;font-weight:600">{label}</div>',
          "life", t0, end_card - t0 + .3, fi=.3, fo=.3,
          style=f"position:absolute;left:0;right:0;top:{60 + 100 * n}px;text-align:center;z-index:7")
        for n, (t0, label) in enumerate(chip_list))

    add_caps("close", {}, big=True, hold_last=True)

    def cell(i, c, val):
        if (i, c) != (wr, wc):
            return val
        wrong = (f'<span style="position:relative;display:inline-block">{wrong_txt}'
                 + f'<svg class="a pen" data-fx="draw" data-at="{ev["pen"] + .3:.2f}" data-d=".55" width="0" height="0" '
                 'style="position:absolute;left:0;top:0"></svg>'
                 + A("", "strike", ev["strike"] + .1, .3, style=f"position:absolute;left:-8px;right:-8px;top:50%;height:7px;"
                     f"background:{RED};border-radius:4px") + '</span>')
        return (A(wrong, "life", -1, ev["fix"] + 1.0, fo=.25, style="display:inline-block")
                + A(f'<span style="color:{TEAL};text-shadow:0 0 24px rgba(94,200,180,.45);white-space:nowrap">{right_txt}</span>',
                    "pop", ev["fix"] + .35, .45, style="position:absolute;right:0;top:0"))

    def row(i, label, *vals):
        cells = "".join(
            f'<span class="num" style="font-size:58px;text-align:right;{"opacity:.75" if c == 0 and len(vals) > 1 else ""}">'
            f'<span style="position:relative;display:inline-block">{cell(i, c, val)}</span></span>'
            for c, val in enumerate(vals))
        return (f'<div style="position:relative;display:grid;grid-template-columns:1fr {" ".join(["170px"] * len(vals))};'
                f'align-items:center;height:{rh}px;border-bottom:1px solid rgba(255,255,255,.08)">'
                f'<span style="font-size:42px;font-weight:500;opacity:.9">{label}</span>{cells}</div>')

    header = "".join(f'<span style="font-size:24px;font-weight:600;letter-spacing:.14em;text-align:right;'
                     f'{"color:" + TEAL if c == len(cols_head) - 1 else "opacity:.6"}">{h}</span>'
                     for c, h in enumerate(cols_head))
    card = (f'<div style="position:relative;background:linear-gradient(180deg,#171a1c,#101213);border:2px solid rgba(255,255,255,.12);'
            f'border-radius:28px;padding:0 34px 18px;box-shadow:0 40px 90px rgba(0,0,0,.6)"><div style="position:relative">{bars}'
            f'<div style="display:grid;grid-template-columns:1fr {" ".join(["170px"] * len(cols_head))};align-items:end;height:{head}px;'
            f'border-bottom:2px solid rgba(255,255,255,.18);padding-bottom:14px;box-sizing:border-box">'
            f'<span style="font-size:24px;font-weight:600;letter-spacing:.14em;opacity:.6">{ep["title"]}</span>{header}</div>'
            + "".join(row(i, *r) for i, r in enumerate(rows)) + '</div></div>')
    card = A(card, "life", -1, end_card + 1, fo=.4, style=f"position:absolute;left:0;right:0;top:{card_top - 230}px;z-index:4")

    ring = (f'<svg width="190" height="190" viewBox="0 0 190 190" style="display:block"><circle cx="95" cy="95" r="84" '
            f'fill="rgba(0,0,0,.35)" stroke="rgba(255,255,255,.14)" stroke-width="9"/></svg>'
            f'<svg class="a" data-fx="draw" data-lin="1" data-at="{count0}" data-d="{COUNT}" width="190" height="190" viewBox="0 0 190 190" '
            f'style="position:absolute;left:0;top:0;transform:rotate(-90deg)"><path d="M95 11 a84 84 0 1 1 -0.01 0" fill="none" '
            f'stroke="{RED}" stroke-width="9" stroke-linecap="round" transform="rotate(90 95 95)"/></svg>')
    number = A(A("10", "count", count0, COUNT, cls="num", style="font-size:96px;line-height:1",
                 **{"from": COUNT, "to": 0, "lin": 1, "pad": 1, "ceil": 1, "pre": "", "suf": "", "show": 1}),
               "beat", count0, 1, n=int(COUNT), style="display:inline-block")
    hook_end = at["hook"] + parts["hook"][1][-1][1] - .1
    countdown = A(f'<div style="position:relative;width:190px;height:190px;margin:0 auto">{ring}'
                  f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">{number}</div></div>',
                  "life", hook_end, count0 + COUNT + 1.0 - hook_end, fi=.35, fo=.4,
                  style="position:absolute;left:0;right:0;top:120px;z-index:6")

    hud = A('<div style="display:flex;justify-content:space-between;font-size:26px;font-weight:600;letter-spacing:.12em">'
            f'<span><span style="color:{RED}">&#9679;</span> FIND THE ERROR &middot; #{ep["number"]}</span><span>ERRORS FOUND '
            + A("0", "count", ev["fix"] + .35, .2, style="display:inline",
                **{"from": 0, "to": 1, "lin": 1, "pad": 1, "pre": "", "suf": "", "show": 1})
            + '/1</span></div>', "life", -1, end_card + 1, fo=.4, style="position:absolute;left:0;right:0;top:0;z-index:7")

    keys = [[0, 90, row_y[1] - 450, 1, 0], [count0 - .2, 90, row_y[0] - 450, 1, .9]]
    order = [3, 1, 5, 0, 4, 2, 5, 3]
    for j, r in enumerate(order):
        keys.append([count0 + .4 + j * 1.2, 90 + (-140 if j % 2 else 140), row_y[r % len(rows)] - 450, 1.05, .9])
    keys += sorted(spot_keys)
    keys.append([end_card, 90, row_y[wr] - 450, .9, 0])
    spotlight = A("", "kf", 0, 1, kf=json.dumps([[round(x, 3) for x in k] for k in keys]),
                  style="position:absolute;left:0;top:0;width:900px;height:900px;border-radius:50%;"
                        "background:radial-gradient(circle,rgba(255,236,214,.15),rgba(255,236,214,0) 62%);mix-blend-mode:screen")
    grain = A("", "grain", 0, 1, op=.06, fps=12,
              style=f"position:absolute;left:0;top:0;width:1300px;height:2150px;background:url({noise_tile()});mix-blend-mode:overlay")
    vignette = ('<div style="position:absolute;inset:0;background:radial-gradient(ellipse 75% 60% at 50% 45%,'
                'rgba(0,0,0,0),rgba(0,0,0,.65))"></div>')
    layer = lambda inner, z: (f'<div class="nochk" style="position:absolute;left:-84px;top:-230px;width:1080px;height:1920px;'
                              f'z-index:{z};pointer-events:none;overflow:hidden">{inner}</div>')
    brand = A(f'<div style="text-align:center"><div class="num" style="font-size:150px;line-height:1">IB<span style="color:{RED}">.</span></div>'
              '<div style="font-size:26px;font-weight:600;letter-spacing:.24em;opacity:.75;margin-top:14px">INVESTMENT BANKING INTERVIEWS</div></div>',
              "rise", at["close"] + parts["close"][1][-1][1] + .2, .5,
              style="position:absolute;left:0;right:0;top:780px;z-index:8")
    caps.sort(key=lambda c: c["start"])
    small = [c for c in caps if not c["big"]]
    rendered = []
    for c in caps:
        nxt = None
        if not c["big"]:
            later = [x["start"] for x in small if x["start"] > c["start"]]
            nxt = min(later) if later else None
        rendered.append(caption(c["words"], c["start"], c["dur"], c["cols"], big=c["big"], hold=c["hold"],
                                first=c["first"], until=nxt))
    html = layer(spotlight, 2) + hud + countdown + chips + card + "".join(rendered) + brand + layer(vignette + grain, 9)
    return dict(dur=total, push=.03, html=html), ev


def soundtrack(parts, at, count0, total, ev):
    n = int(total * SR) + SR
    voice, sfx = np.zeros(n, np.float32), np.zeros(n, np.float32)

    def put(buf, sig, t, gain=1.0):
        i = int(t * SR)
        buf[i:i + len(sig)] += sig[: max(0, n - i)] * gain

    for k, (a, _) in parts.items():
        put(voice, a, at[k])
    tt = np.arange(int(.05 * SR)) / SR
    tick = (np.sin(2 * np.pi * 1900 * tt) * np.exp(-tt * 70)).astype(np.float32)
    for k in range(int(COUNT)):
        put(sfx, tick, count0 + k, .22 if k < 7 else .34)
    tt = np.arange(int(.5 * SR)) / SR
    put(sfx, (np.sin(2 * np.pi * 62 * tt) * np.exp(-tt * 7)).astype(np.float32), count0 + COUNT, .55)
    tt = np.arange(SR) / SR
    ding = ((np.sin(2 * np.pi * 1318.5 * tt) + .5 * np.sin(2 * np.pi * 1975.5 * tt)) * np.exp(-tt * 4.5)).astype(np.float32)
    put(sfx, ding, ev["fix"] + .35, .16)
    g = .12 / max(np.sqrt(np.mean(voice[voice != 0] ** 2)), 1e-6)
    return voice * g, sfx * g


def make(ep, voice_name="af_heart"):
    v, parts = synth(ep, voice_name)
    at, count0, total = timeline(parts)
    sc, ev = scene(ep, v, parts, at, count0, total)
    mp4, cover, problems = build(ep["slug"] + "-silent", [sc], theme="ink", cover_at=at["go"] - .08, crf=20)
    voice, sfx = soundtrack(parts, at, count0, total + .6, ev)
    work = OUT / ep["slug"]
    work.mkdir(parents=True, exist_ok=True)
    write_wav(work / "voice.wav", voice)
    write_wav(work / "sfx.wav", sfx)
    final = work / f"{ep['slug']}.mp4"
    graph = (f"[1:a]{MASTER}[v];anoisesrc=color=brown:amplitude=0.0012:sample_rate={SR}:duration={total + .6:.2f}[room];"
             "[v][2:a][room]amix=inputs=3:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-i", str(work / "voice.wav"), "-i", str(work / "sfx.wav"),
                    "-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", str(final)], check=True)
    (work / "cover.jpg").write_bytes(pathlib.Path(cover).read_bytes())
    json.dump({"at": at, "count0": count0, "total": total, "voice": voice_name, "events": ev,
               "segments": {k: p[1] for k, p in parts.items()}}, open(work / "timeline.json", "w"), indent=1)
    print(f"  -> {final.name}  {total:.1f}s  voice {voice_name}")
    return final, problems
