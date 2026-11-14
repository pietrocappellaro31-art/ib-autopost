"""
Story engine for YouTube Shorts (13 Nov, docs/production/short-form-standard.md formats B to F: a story, one
surprising concept, an animated calculation, a myth, a choice). The four-level quiz keeps levels.py; this engine
tells one idea as a run of beats, each with its own colour ground, a label pill, the narration as captions lit
word by word, and a large drawing from sketch.py that acts out the sentence (the recurring trader character,
counters, stamps). Same voice handling, word check, effects ducking, two-stage -14 LUFS master and sound report
as levels.py, which it reuses.

An episode:
    EP = dict(slug="shorts-...", kicker="...", mood="playful", lufs=-14, music=False,
              beats=[dict(tag="THE MYTH", say=[(spoken, display), ...], art=lambda t0, d: picture(...),
                          bg="#...", hl=[...], size=64, sfx=[(seconds after the beat starts, "pop"|"tick"|"ding"|
                          "thump"|"step"|"paper"|"clink"|"knock", gain), ...], hold=.45), ...],
              close=dict(say=[...], bg="#...", art=lambda t0, d: ...),   # the comment ask and the brand
              floaters=lambda total: html)
    make(EP, "HEART")

14 Nov: a beat can take badge="RECONSTRUCTION" (a pill beside its label), split=True (said one sentence at a time),
art=lambda t0, d, seg: ... (seg: each sentence's absolute start and end, to act on the words), and sfx offsets tied
to the words: ("s", j, o) or ("e", j, o) seconds from sentence j's start or end, ("d", f) a fraction of the drawing
time. Cue kinds now include the foley set: "step", "paper", "clink", "knock".
"""

import html as H
import json
import pathlib

import numpy as np

import levels as L
import sfx as sfx_lib
from motion import A, build, OUT
from voice import passage, SR
from voice_clone import make_voice

RED, TEAL, INK, W = L.RED, L.TEAL, L.INK, L.W
ART_W, ART_H = 752, 640          # 13 Nov: 700 x 560 left 300 px of the frame empty under the drawing
T_SW = .34


def synth(ep, voice_name):
    v = make_voice(voice_name)
    texts = {f"b{i}": [s for s, _ in b["say"]] for i, b in enumerate(ep["beats"])}
    texts["close"] = [s for s, _ in ep["close"]["say"]]
    for ss in texts.values():
        v.phonemes(" ".join(ss))                       # fail early on an unknown word
    parts = {}
    split = {f"b{i}" for i, b in enumerate(ep["beats"]) if b.get("split")}
    for n, (k, ss) in enumerate(texts.items()):
        pace = (ep.get("speed", 1.0) + (.012 if n % 3 == 1 else -.008 if n % 3 == 2 else 0)) * getattr(v, "pace_scale", 1.0)
        if k in split:
            # 14 Nov: a beat whose word blurred in the flowing passage ("PIN" heard as "pen") is said one sentence
            # at a time, which said it cleanly when tested alone.
            parts[k] = L.joined(v, [[x] for x in ss], pace, gap=.2)
            continue
        try:
            parts[k] = passage(v, " ".join(ss), pace)
        except ValueError:
            parts[k] = L.joined(v, [[x] for x in ss], pace, gap=.2)
        if len(parts[k][1]) != len(ss):
            parts[k] = L.joined(v, [[x] for x in ss], pace, gap=.2)
        if len(parts[k][1]) != len(ss):
            raise ValueError(f"{k}: expected {len(ss)} sentences, aligned {len(parts[k][1])}")
    return v, parts


def timeline(ep, parts):
    dur = lambda k: len(parts[k][0]) / SR
    at, spans, t = {}, [], .25
    for i, b in enumerate(ep["beats"]):
        at[f"b{i}"] = t + (.0 if i == 0 else .3)
        end = at[f"b{i}"] + dur(f"b{i}") + b.get("hold", .45)
        spans.append((t, end))
        t = end
    at["close"] = t + .3
    total = at["close"] + dur("close") + 1.7
    return at, spans, total


def hud(ep, spans, close_at, total):
    """The kicker and a segmented progress bar (one segment per beat) at the top, on screen throughout."""
    n = len(spans)
    gap = 10
    sw = (W - gap * (n - 1)) / n
    bar = ""
    for i, (s0, s1) in enumerate(spans):
        x = i * (sw + gap)
        fill = A("", "growX", s0 + .1, max(s1 - s0 - .2, .3), style=f"position:absolute;inset:0;background:{RED};border-radius:7px")
        bar += (f'<div style="position:absolute;left:{x:.1f}px;top:58px;width:{sw:.1f}px;height:14px;border-radius:7px;'
                f'background:rgba(10,10,10,.09);overflow:hidden">{fill}</div>')
    return (f'<div style="position:absolute;left:0;top:0;width:{W}px;height:80px;z-index:6;font-size:26px;font-weight:600;'
            f'letter-spacing:.16em"><span style="opacity:.6">{ep["kicker"]}</span>{bar}</div>')


def pill(tag, at, color=RED):
    return A(f'<span style="display:inline-block;background:{color};color:#fff;font-size:30px;font-weight:700;letter-spacing:.16em;'
             f'padding:12px 24px;border-radius:14px">{H.escape(tag)}</span>', "pop", round(at, 3), .4,
             style="transform-origin:left center")


def _arity(f):
    import inspect
    return len(inspect.signature(f).parameters)


def sentences(parts, at, k):
    """The absolute (start, end) of each spoken sentence of part k, so a drawing can act on the words (14 Nov)."""
    return [(round(at[k] + x, 3), round(at[k] + y, 3)) for _, x, y in parts[k][1]]


def cue_time(off, i, parts, at, spans):
    """A cue's time: a number is seconds after the beat starts (as before); 14 Nov, tied to the words instead:
    ("s", j, o) is o seconds after sentence j starts, ("e", j, o) o seconds after it ends, ("d", f) a fraction f
    of the beat's drawing time."""
    k = f"b{i}"
    if not isinstance(off, tuple):
        return at[k] + off
    if off[0] == "d":
        return at[k] + .05 + off[1] * (spans[i][1] - at[k])
    seg = sentences(parts, at, k)[off[1]]
    return (seg[0] if off[0] == "s" else seg[1]) + off[2]


def scene(ep, parts, at, spans, total):
    els = [hud(ep, spans, at["close"], total)]
    seg = lambda k: parts[k][1]
    check_at = []
    for i, b in enumerate(ep["beats"]):
        k, ba = f"b{i}", at[f"b{i}"]
        s0, s1 = spans[i]
        cap = "".join(L.kara(d, ba + x, y - x, b.get("cols"), hl=b.get("hl", ()), lit=(i == 0), cls="olchk",
                             style=f"font-family:'Serif',serif;font-weight:700;font-size:{b.get('size', 62)}px;line-height:1.1;"
                                   f"letter-spacing:-.015em;margin-top:{0 if j == 0 else 10}px;text-wrap:balance")
                      for j, ((s, d), (_, x, y)) in enumerate(zip(b["say"], seg(k))))
        art = ""
        if b.get("art"):
            args = (ba + .05, s1 - ba) + ((sentences(parts, at, k),) if _arity(b["art"]) > 2 else ())
            art = (f'<div class="nochk" style="position:relative;margin:28px auto 0;width:{b.get("art_w", ART_W)}px;'
                   f'height:{b.get("art_h", ART_H)}px">{b["art"](*args)}</div>')
        extra = b["over"](ba, s1 - ba) if b.get("over") else ""
        badge = (A(f'<span style="display:inline-block;border:3px solid {INK};color:{INK};font-size:24px;font-weight:700;'
                   f'letter-spacing:.14em;padding:9px 16px;border-radius:12px;margin-left:14px;vertical-align:middle;'
                   f'background:rgba(255,255,255,.55)">{H.escape(b["badge"])}</span>', "fade", round(max(s0, 0) + .25, 3), .4,
                   style="display:inline-block") if b.get("badge") else "")      # 14 Nov: RECONSTRUCTION, as the gate asks
        inner = (f'<div>{pill(b["tag"], max(s0, 0) + .15, b.get("tag_color", RED))}{badge}</div>'
                 f'<div style="margin-top:22px">{cap}</div>{art}{extra}')
        col = (f'<div style="position:absolute;left:0;top:120px;width:{W}px;height:1090px;display:flex;flex-direction:column;'
               f'justify-content:flex-start">{inner}</div>')
        els.append(L.group(col, -1 if i == 0 else s0 - .02, (s1 - (-1 if i == 0 else s0 - .02)) + T_SW + .02,
                           **({"fi": 0} if i == 0 else {})))
        check_at.append(s1 - .2)
    # The close: the comment ask, the brand.
    c = ep["close"]
    cs, ca = seg("close"), at["close"]
    big = L.kara(c["say"][0][1], ca + cs[0][1], cs[0][2] - cs[0][1], cls="olchk",
                 style="font-family:'Serif',serif;font-weight:700;font-size:96px;line-height:1.04;letter-spacing:-.03em;text-wrap:balance")
    rest = "".join(L.kara(d, ca + x, y - x, c.get("cols"), hide=True, cls="olchk",
                          style="font-size:50px;font-weight:600;line-height:1.24;margin-top:18px;text-wrap:balance")
                   for (s, d), (_, x, y) in zip(c["say"][1:], cs[1:]))
    end_voice = ca + cs[-1][2]
    pic = (f'<div class="nochk" style="position:relative;margin:24px auto 0;width:{c.get("art_w", 520)}px;height:{c.get("art_h", 416)}px">'
           f'{c["pic"](ca, end_voice - ca + 1)}</div>') if c.get("pic") else ""
    els.append(L.group(L.column(f'<div style="margin-top:{-120 if pic else -260}px">{big}{rest}{pic}</div>'), ca - .35,
                       end_voice - ca + 1.0, fo=.45, out="fade"))
    check_at.append(end_voice - .1)
    brand = A(f'<div style="text-align:center"><div class="num" style="font-size:170px;line-height:1">IB<span style="color:{RED}">.</span></div>'
              '<div style="font-size:26px;font-weight:600;letter-spacing:.24em;opacity:.7;margin-top:16px">INVESTMENT BANKING INTERVIEWS</div></div>',
              "rise", end_voice + .75, .55, style=f"position:absolute;left:0;top:470px;width:{W}px;z-index:8")
    # Colour grounds, floaters and the close art under everything (as levels.py).
    grounds = [(b.get("bg"), -1 if i == 0 else spans[i][0], spans[i][1]) for i, b in enumerate(ep["beats"])]
    grounds.append((c.get("bg"), ca - .35, total + 1))
    under = ""
    for col_, g0, g1 in grounds:
        if not col_:
            continue
        kf = json.dumps([[round(g0, 3), 0, 0, 1, 0 if g0 > 0 else 1], [round(g0 + .4, 3), 0, 0, 1, 1], [round(g1, 3), 0, 0, 1, 1],
                         [round(g1 + .45, 3), 0, 0, 1, 0]])
        under += A("", "kf", 0, 1, cls="nochk", kf=H.escape(kf),
                   style=f"position:absolute;left:-84px;top:-230px;width:1080px;height:1920px;background:{col_}")
    if ep.get("floaters"):
        under += ep["floaters"](total)
    if c.get("art"):
        under += c["art"](ca, total - ca)
    els.insert(0, f'<div class="nochk" style="position:absolute;left:0;top:0;width:{W}px;height:10px;z-index:0">{under}</div>')
    grain = A("", "grain", 0, 1, op=.05, fps=12,
              style=f"position:absolute;left:0;top:0;width:1300px;height:2150px;background:url({L.noise_tile()});mix-blend-mode:multiply")
    layer = (f'<div class="nochk" style="position:absolute;left:-84px;top:-230px;width:1080px;height:1920px;z-index:9;'
             f'pointer-events:none;overflow:hidden">{grain}</div>')
    return dict(dur=total, push=.02, html="".join(els) + brand + layer), check_at


def soundtrack(ep, parts, at, spans, total):
    """Voice plus effects tied to what happens on screen: a pop as each label lands, then each beat's own cues
    (b["sfx"]: a tick rhythm under a counter, a thump under a stamp, a ding on a reveal). No whoosh. Effects slide
    up to 0.12 s into the nearest gap between words and are ducked about 6 dB under speech, as in levels.py."""
    n = int(total * SR) + SR
    voice, fx = np.zeros(n, np.float32), np.zeros(n, np.float32)

    def raw(buf, sig, t, gain=1.0):
        i = int(max(t, 0) * SR)
        buf[i:i + len(sig)] += sig[: max(0, n - i)] * gain

    for k, (a, _) in parts.items():
        raw(voice, a, at[k])
    env = np.convolve(voice ** 2, np.ones(int(.01 * SR)) / int(.01 * SR), "same")

    def put(sig, t, gain, slide=True):
        if slide:
            w = int(.12 * SR)
            t += min((float(np.sum(env[max(0, int((t + o) * SR)):max(0, int((t + o) * SR)) + w])), abs(o), o)
                     for o in np.arange(-.12, .121, .01))[2]
        raw(fx, sig, t, gain)

    S = dict(tick=sfx_lib.tick(), pop=sfx_lib.pop(), thump=sfx_lib.thump(), ding=sfx_lib.ding(12))
    from scipy.signal import resample_poly
    foley = dict(step=lambda k: sfx_lib.footstep(k, "floor"), paper=lambda k: sfx_lib.paper(k, .4),
                 clink=lambda k: sfx_lib.clink(k), knock=lambda k: sfx_lib.soft_hit(k, 180))
    n_fx = [0]

    def cue(kind):
        """14 Nov: the 48 kHz foley of the filmed scenes (footsteps, paper, a coin clink, a soft knock) joins the
        story cues, resampled to the engine's 24 kHz, a new take (seed) every time so steps never repeat."""
        if kind in S:
            return S[kind]
        n_fx[0] += 1
        return resample_poly(foley[kind](n_fx[0]), 1, 2).astype(np.float32)

    for i, b in enumerate(ep["beats"]):
        put(S["pop"], max(spans[i][0], 0) + .17, .24)
        for off, kind, gain in b.get("sfx", ()):
            put(cue(kind), cue_time(off, i, parts, at, spans), gain, slide=kind not in ("tick", "step"))
    ca = at["close"]
    end_voice = ca + parts["close"][1][-1][2]
    put(S["pop"], ca - .1, .2)
    raw(fx, S["ding"], end_voice + .78, .07)
    k = int(.03 * SR)
    lev = np.convolve(np.abs(voice), np.ones(k) / k, "same")
    talking = (lev > .02 * max(lev.max(), 1e-9)).astype(np.float32)
    talking = np.convolve(talking, np.ones(int(.12 * SR)) / int(.12 * SR), "same")
    fx *= 1 - ep.get("duck", .5) * np.clip(talking, 0, 1)
    g = .12 / max(np.sqrt(np.mean(voice[voice != 0] ** 2)), 1e-6)
    return voice * g, fx * g


def make(ep, voice_name="HEART"):
    v, parts = synth(ep, voice_name)
    at, spans, total = timeline(ep, parts)
    print(f"  timing: {total:.1f} s, {len(ep['beats'])} beats" + ("  CHECK over 60 s" if total > 60 else ""), flush=True)
    sc, check_at = scene(ep, parts, at, spans, total)
    mp4, cover, problems = build(ep["slug"] + "-silent", [sc], theme="paper", cover_at=ep.get("cover_at", 1.6), crf=21,
                                 check_at=check_at, fit=ep.get("fit", True))
    voice, fx = soundtrack(ep, parts, at, spans, total + .6)
    fx = fx * L.shorts_mix(ep)[1]
    work = OUT / ep["slug"]
    work.mkdir(parents=True, exist_ok=True)
    final = L.mux(ep, voice_name, voice, fx, total, mp4)
    (work / "cover.jpg").write_bytes(pathlib.Path(cover).read_bytes())
    json.dump({"at": at, "spans": spans, "total": total, "voice": voice_name,
               "segments": {k: p[1] for k, p in parts.items()}}, open(work / "timeline.json", "w"), indent=1)
    log = L.takes_from_track(work, parts, at)
    json.dump(log, open(work / "takes.json", "w"), indent=1)
    bad = [x for x in log if x["wer"] > 0]
    print(f"  lines heard word for word: {len(log) - len(bad)}/{len(log)}"
          + "".join(f"\n    CHECK {x['part']}: {x['text']!r} heard {x['heard']!r}" for x in bad))
    if not ep.get("music"):
        import music_library
        ref = music_library.pick(ep.get("mood", "playful"), "short", slug=ep["slug"])
        if ref:
            pick = dict(id=ref["id"], search=ref.get("search"), start=ref["calm_start"], tags=ref["tags"], others=ref["others"],
                        line=music_library.instructions(ref, "short"))
            json.dump(pick, open(work / "music_pick.json", "w"), indent=1)
            print(f"  music: {pick['line']}")
    print(f"  captions: {srt(ep, work).name}")
    report = L.sound_report(work, final, voice, fx)
    json.dump(report, open(work / "sound.json", "w"), indent=1)
    print(f"  sound: DNSMOS voice {report['voice']['ovrl']} / mix {report['mix']['ovrl']} (bak {report['mix']['bak']}), "
          f"voice over effects {report['voice_over_fx_db']} dB while speaking, {report['lufs']} LUFS, {report['tp']} dBTP")
    print(f"  -> {final.name}  {total:.1f}s  voice {voice_name}")
    return final, problems


def remix(ep, voice_name="HEART"):
    """Rebuild only the sound of the last render (same picture, same voice takes) after an effects change."""
    work = OUT / ep["slug"]
    parts = L.reuse(work)
    at, spans, total = timeline(ep, parts)
    voice, fx = soundtrack(ep, parts, at, spans, total + .6)
    fx = fx * L.shorts_mix(ep)[1]
    final = L.mux(ep, voice_name, voice, fx, total, OUT / (ep["slug"] + "-silent") / (ep["slug"] + "-silent.mp4"))
    report = L.sound_report(work, final, voice, fx)
    json.dump(report, open(work / "sound.json", "w"), indent=1)
    print(f"  remixed: DNSMOS voice {report['voice']['ovrl']} / mix {report['mix']['ovrl']}, voice over effects "
          f"{report['voice_over_fx_db']} dB while speaking, {report['lufs']} LUFS, {report['tp']} dBTP")
    return report


def srt(ep, work=None):
    """Captions file from the render's own sentence timings (timeline.json) and the on-screen wording."""
    work = work or OUT / ep["slug"]
    t = json.load(open(work / "timeline.json"))
    disp = {f"b{i}": [d for _, d in b["say"]] for i, b in enumerate(ep["beats"])}
    disp["close"] = [d for _, d in ep["close"]["say"]]
    fmt = lambda s: f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(round(s % 1 * 1000)) % 1000:03d}"
    rows, n = [], 0
    for k, segs in t["segments"].items():
        for (text, x, y), d in zip(segs, disp[k]):
            n += 1
            rows.append(f"{n}\n{fmt(t['at'][k] + x)} --> {fmt(t['at'][k] + y + .15)}\n{H.unescape(d).replace(' | ', ' ')}\n")
    path = work / f"{ep['slug']}.srt"
    path.write_text("\n".join(rows))
    return path
