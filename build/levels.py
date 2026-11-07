"""
"Levels": the escalating quiz Reel (7 Nov). Five interview questions, each one
harder, read by the voice; the viewer keeps score and comments it at the end.

    hook    the hardest question is asked first, then "That's level five", so
            the Reel opens a loop that only the last level closes
    level   lockup (big numeral, LEVEL, italic tail), the question on a card
            lit word by word as it is read, a think bar with ticks, then the
            answer, revealed word by word, and a worked chip
    close   "What's your score out of five?", a spinning score, the brand

Paper ground, red for the stake, teal for the answer. Each level whips in and
out; the level meter at the top stays. Voice: whole passages per call
(voice.passage) so intonation flows, timings recovered from the audio's own
pauses, then the recording chain and -16 LUFS, as in findgame.

An episode is a config: see reels_levels1.py.
"""

import html as H
import json
import pathlib
import re
import subprocess

import numpy as np

from findgame import noise_tile
from motion import A, build, OUT
from voice import passage, write_wav, SR, MASTER
from voice_clone import make_voice
import sfx as sfx_lib

RED, TEAL, INK = "#D93A12", "#0F766E", "#0A0A0A"
W = 752                                    # safe-area width


# ---------------------------------------------------------------- text ----

def kara(display, start, dur, cols=None, hide=False, hl=(), cls="", style="", lit=False):
    """Karaoke text: each word lights (or, with hide, appears) at its moment.
    Word moments are spread across the sentence by character count; the
    sentence boundaries themselves come from the audio."""
    cols = cols or {}
    ws = display.split()
    lens = [0 if w == "|" else max(len(re.sub(r"\W", "", w)), 1) + 1 for w in ws]
    t, acc = [], 0
    for n in lens:
        t.append(round(dur * acc / sum(lens), 3))
        acc += n
    spans = []
    for w, tt in zip(ws, t):
        if w == "|":                                   # a line break in the display text
            spans.append("<br>")
            continue
        key = re.sub(r"[^\w$%×/]", "", w).lower()
        c = cols.get(key)
        spans.append(f'<span class="w" data-t="{tt}"' + (f' data-c="{c}"' if c else "")
                     + f' style="display:inline-block">{H.escape(H.unescape(w))}</span>')
    # Highlighter behind a phrase, swiped on as its first word is said.
    for phrase in hl:
        p = phrase.split()
        for i in range(len(ws) - len(p) + 1):
            if [re.sub(r"\W", "", x).lower() for x in ws[i:i + len(p)]] == [re.sub(r"\W", "", x).lower() for x in p]:
                mark = A("", "wipe", round(start + t[i], 3), .4,
                         style="position:absolute;left:-8px;right:-8px;bottom:.06em;height:.42em;"
                               "background:rgba(217,58,18,.2);border-radius:8px;z-index:-1")
                spans[i:i + len(p)] = [f'<span style="position:relative;display:inline-block;white-space:nowrap">{mark}'
                                       + " ".join(spans[i:i + len(p)]) + "</span>"]
                break
    if lit:                                            # fully readable from the start (the hook)
        return f'<div class="{cls}" style="{style}">' + " ".join(spans) + "</div>"
    return A(" ".join(spans), "kara", round(start, 3), dur, cls=cls, style=style, **({"hide": 1} if hide else {}))


# --------------------------------------------------------------- voice ----

def synth(ep, voice_name):
    v = make_voice(voice_name)                         # Kokoro name, or clone:/path/to/reference.wav
    texts = {"hook": [s for s, _ in ep["hook"]["say"]], "close": [s for s, _ in ep["close"]["say"]]}
    for i, lv in enumerate(ep["levels"]):
        texts[f"q{i}"] = ([lv["label"]] if lv.get("label") else []) + [s for s, _ in lv["q"] if s]   # "" = on the card, not said
        texts[f"a{i}"] = [s for s, *_ in lv["a"]]
    for k, ss in texts.items():
        v.phonemes(" ".join(ss))                       # fail before rendering on an unknown word
    sp = ep.get("speed", 1.0)
    parts = {}
    for n, (k, ss) in enumerate(texts.items()):
        pace = sp + (.015 if n % 3 == 1 else -.01 if n % 3 == 2 else 0)      # small variation in pace
        if k.startswith("a") and len(ss) > 1:
            # The verdict is said on its own, then a beat, then the reasoning,
            # the way a person answers: "Nothing." ... "Debt is up a hundred..."
            parts[k] = joined(v, [ss[:1], ss[1:]], pace, gap=.2)
        else:
            parts[k] = passage(v, " ".join(ss), pace)
        if len(parts[k][1]) != len(ss):
            raise ValueError(f"{k}: expected {len(ss)} sentences, aligned {len(parts[k][1])}")
    return v, parts


def joined(v, groups, pace, gap):
    audio, segs, t = [], [], 0.0
    for g in groups:
        a, ss = passage(v, " ".join(g), pace)
        audio += [a, np.zeros(int(gap * SR), np.float32)]
        segs += [(s, round(t + x, 3), round(t + y, 3)) for s, x, y in ss]
        t += len(a) / SR + gap
    return np.concatenate(audio[:-1]), segs


def timeline(ep, parts):
    dur = lambda k: len(parts[k][0]) / SR
    at, lv = {"hook": .3}, []
    t = at["hook"] + dur("hook") + .35                  # the hook group whips out here
    hook_end = t
    for i, L in enumerate(ep["levels"]):
        start = t
        at[f"q{i}"] = start + .32
        q_end = at[f"q{i}"] + dur(f"q{i}")
        think0 = q_end + .12
        at[f"a{i}"] = think0 + L["think"] + .1
        end = at[f"a{i}"] + dur(f"a{i}") + L.get("hold", .6)
        lv.append(dict(start=start, think0=think0, think=L["think"], end=end))
        t = end
    at["close"] = t + .35
    total = at["close"] + dur("close") + 1.7
    return at, hook_end, lv, total


# --------------------------------------------------------------- scene ----

def lockup(n, tail, tail_col=INK):
    return (f'<div style="display:flex;align-items:center;gap:30px">'
            f'<div class="num" style="font-size:200px;line-height:.86;color:{RED};letter-spacing:-.04em">{n}</div>'
            f'<div><div class="lbl" style="font-size:30px;letter-spacing:.24em;opacity:.55">LEVEL</div>'
            f'<div class="it" style="font-size:78px;line-height:1;font-weight:600;color:{tail_col};margin-top:6px">{tail}</div></div></div>')


def card(inner, accent=None):
    border = f"border:4px solid {accent};" if accent else ""
    return (f'<div style="position:relative;z-index:0;margin-top:36px;width:{W}px;box-sizing:border-box;{border}'
            f'background:#fff;border-radius:30px;padding:34px 44px 38px;'
            f'box-shadow:0 30px 70px rgba(10,10,10,.13),0 4px 14px rgba(10,10,10,.06)">{inner}</div>')


def ghost(n):
    """A huge faint numeral behind the level, for depth; it whips with the level."""
    return (f'<div class="nochk num" style="position:absolute;right:-250px;top:120px;font-size:1050px;line-height:1;'
            f'opacity:.045;z-index:-1;letter-spacing:-.06em">{n}</div>')


def column(inner):
    return (f'<div style="position:absolute;left:0;top:100px;width:{W}px;height:1110px;display:flex;flex-direction:column;'
            f'justify-content:center">{inner}</div>')


def group(inner, at, d, **kw):
    return A(inner, "pass", round(at, 3), round(d, 3), style=f"position:absolute;left:0;top:0;width:{W}px;height:1210px", **kw)


def scene(ep, parts, at, hook_end, lv, total):
    n_lv = len(ep["levels"])
    seg = lambda k: parts[k][1]
    els = []
    T_SW = .34                                      # the swipe between levels

    # Level meter and HUD, on screen throughout.
    gap = 12
    sw = (W - gap * (n_lv - 1)) / n_lv
    meter = ""
    for i in range(n_lv):
        x = i * (sw + gap)
        fills = A("", "growX", .05 + i * .09, .28, style=f"position:absolute;inset:0;background:{RED};border-radius:7px")
        fills = A(fills, "life", -1, hook_end + 1 + .1, fi=.01, fo=.3, style="position:absolute;inset:0")
        cur = A(A("", "growX", lv[i]["start"] + .15, .4, style=f"position:absolute;inset:0;background:{RED};border-radius:7px"),
                "life", lv[i]["start"], lv[i]["end"] - lv[i]["start"] + .3, fi=.01, fo=.3, style="position:absolute;inset:0")
        done = A("", "fade", lv[i]["end"], .3, style=f"position:absolute;inset:0;background:{INK};border-radius:7px")
        meter += (f'<div style="position:absolute;left:{x:.1f}px;top:58px;width:{sw:.1f}px;height:14px;border-radius:7px;'
                  f'background:rgba(10,10,10,.09);overflow:hidden">{fills}{cur}{done}</div>')
    hud_r = A(f"LEVEL {n_lv}/{n_lv}", "life", -1, hook_end + 1 + .1, fi=.01, fo=.2, style="position:absolute;right:0;top:0")
    for i in range(n_lv):
        hud_r += A(f"LEVEL {i + 1}/{n_lv}", "life", lv[i]["start"] + .1, lv[i]["end"] - lv[i]["start"], fi=.2, fo=.15,
                   style="position:absolute;right:0;top:0")
    hud_r += A("YOUR SCORE", "life", at["close"] - .2, total, fi=.2, style="position:absolute;right:0;top:0")
    els.append(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:80px;z-index:6;font-size:26px;font-weight:600;'
               f'letter-spacing:.16em"><span style="opacity:.6">{ep["kicker"]}</span>{hud_r}{meter}</div>')

    # Hook: the last level asked first. The question is fully readable from
    # frame 0; the highlighter swipes on as it is said.
    hk = ep["hook"]
    hs = seg("hook")
    q_html = kara(hk["say"][0][1], at["hook"] + hs[0][1], hs[0][2] - hs[0][1], hk.get("cols"), hl=hk.get("hl", ()), lit=True,
                  style=f"font-family:'Serif',serif;font-weight:700;font-size:{hk.get('qsize', 86)}px;line-height:1.06;letter-spacing:-.02em")
    lines = "".join(kara(d, at["hook"] + a, b - a, hk.get("cols"), hide=True,
                         style="font-family:'Serif',serif;font-style:italic;font-weight:600;font-size:70px;line-height:1.12;margin-top:6px")
                    for (s, d), (_, a, b) in zip(hk["say"][1:], hs[1:]))
    hook = (ghost(n_lv) + lockup(n_lv, ep["levels"][-1]["tail"], RED)
            + card(f'<div class="lbl" style="font-size:28px;letter-spacing:.2em;color:{RED};opacity:1;margin-bottom:20px">'
                   f'THE LAST QUESTION</div>{q_html}', accent=RED)
            + f'<div style="margin-top:44px"><div style="font-size:44px;font-weight:500;opacity:.7;margin-bottom:20px;text-wrap:balance">{hk["sub"]}</div>'
              f'{lines}</div>')
    els.append(group(column(hook), -1, hook_end + 1 + T_SW, fi=0, fo=T_SW))

    # The levels.
    check_at = [hook_end - .5]
    for i, L in enumerate(ep["levels"]):
        T = lv[i]
        last = i == n_lv - 1
        qs = seg(f"q{i}")[1:] if L.get("label") else seg(f"q{i}")      # a spoken "Level N." is not on the card
        qa = at[f"q{i}"]
        spoken = iter(qs)
        q_html = ""
        for s_, d in L["q"]:
            if not s_:                                    # already asked (the hook): shown, not read again
                q_html += kara(d, qa, .01, L.get("cols"), lit=True, style="display:inline;opacity:.55") + " "
                continue
            _, a, b = next(spoken)
            q_html += kara(d, qa + a, b - a, L.get("cols"), hl=L.get("hl", ()), style="display:inline") + " "
        qcard = card(f'<div style="font-family:\'Serif\',serif;font-weight:700;font-size:{L.get("qsize", 62)}px;line-height:1.12;'
                     f'letter-spacing:-.015em">{q_html}</div>', accent=RED if last else None)
        think = A(f'<div style="display:flex;align-items:center;gap:24px"><span class="lbl" style="font-size:30px;letter-spacing:.22em;'
                  f'opacity:.65">THINK</span><div style="position:relative;flex:1;height:16px;border-radius:8px;background:rgba(10,10,10,.08)">'
                  + A("", "shrinkX", T["think0"], T["think"], style=f"position:absolute;inset:0;border-radius:8px;background:{RED}")
                  + '</div></div>', "life", T["think0"] - .15, T["think"] + .45, fi=.15, fo=.3, style="margin-top:28px;height:40px")
        # The answer: first sentence big in teal, the rest as lines, then the chip.
        aa = at[f"a{i}"]
        asg = seg(f"a{i}")
        ans = ""
        for j, ((s, d, *style), (_, a, b)) in enumerate(zip(L["a"], asg)):
            kind = style[0] if style else ("big" if j == 0 else "line")
            if kind == "big":
                ans += kara(d, aa + a, b - a, L.get("acols"), hide=True,
                            style=f"font-family:'Serif',serif;font-weight:700;font-size:{L.get('bigsize', 122)}px;line-height:1.02;"
                                  f"letter-spacing:-.03em;color:{TEAL}")
            else:
                ans += kara(d, aa + a, b - a, L.get("acols"), hide=True,
                            style="font-size:47px;font-weight:500;line-height:1.26;margin-top:14px;text-wrap:balance")
        rip = A("", "ripple", aa + .02, .9, style=f"position:absolute;left:-70px;top:-90px;width:320px;height:320px;border-radius:50%;"
                                                   f"border:5px solid {TEAL};z-index:-1")
        chip = ""
        if L.get("chip"):
            t0 = aa + asg[L.get("chip_at", 0)][1] + .25
            foot = (f'<div style="font-size:28px;font-weight:500;opacity:.6;margin-top:10px">{L["foot"]}</div>' if L.get("foot") else "")
            chip = A(f'<div style="display:inline-block;border:3px solid {TEAL};background:rgba(15,118,110,.08);border-radius:24px;'
                     f'padding:18px 30px;font-size:44px;font-weight:600;line-height:1.3">{L["chip"]}</div>{foot}',
                     "pop", t0, .45, style="margin-top:30px;transform-origin:left center")
        answer = f'<div style="position:relative;margin-top:22px;min-height:{L.get("ans_min", 0)}px">{rip}{ans}{chip}</div>'
        grp = ghost(i + 1) + lockup(i + 1, L["tail"], RED if last else INK) + qcard + think + answer
        els.append(group(column(grp), T["start"] - .02, T["end"] - T["start"] + T_SW + .02))
        check_at.append(T["end"] - .2)

    # Close: the score.
    cs = seg("close")
    ca = at["close"]
    big = kara(ep["close"]["say"][0][1], ca + cs[0][1], cs[0][2] - cs[0][1],
               style="font-family:'Serif',serif;font-weight:700;font-size:108px;line-height:1.03;letter-spacing:-.03em")
    digits = "".join(f"<span>{x}</span>" for x in [str(k) for k in range(n_lv + 1)] * 2 + ["?"])
    rest = "".join(kara(d, ca + a, b - a, ep["close"].get("cols"), hide=True,
                        style="font-size:50px;font-weight:600;line-height:1.24;margin-top:14px;text-wrap:balance")
                   for (s, d), (_, a, b) in zip(ep["close"]["say"][1:], cs[1:]))
    end_voice = ca + cs[-1][2]
    close = f'{big}<div style="margin-top:24px;margin-bottom:10px">{SCORE.format(digits=digits, at=ca + .4, n=n_lv)}</div>{rest}'
    els.append(group(column(close), ca - .35, end_voice - ca + 1.0, fo=.45, out="fade"))
    check_at.append(end_voice - .1)
    brand = A(f'<div style="text-align:center"><div class="num" style="font-size:170px;line-height:1">IB<span style="color:{RED}">.</span></div>'
              '<div style="font-size:26px;font-weight:600;letter-spacing:.24em;opacity:.7;margin-top:16px">INVESTMENT BANKING INTERVIEWS</div></div>',
              "rise", end_voice + .75, .55, style=f"position:absolute;left:0;top:470px;width:{W}px;z-index:8")

    grain = A("", "grain", 0, 1, op=.05, fps=12,
              style=f"position:absolute;left:0;top:0;width:1300px;height:2150px;background:url({noise_tile()});mix-blend-mode:multiply")
    layer = (f'<div class="nochk" style="position:absolute;left:-84px;top:-230px;width:1080px;height:1920px;z-index:9;'
             f'pointer-events:none;overflow:hidden">{grain}</div>')
    html = "".join(els) + brand + layer
    return dict(dur=total, push=.025, html=html), check_at


SCORE = ('<div class="a roll num nochk" data-fx="roll" data-at="{at:.2f}" data-d="1" data-hold=".17" '
         'style="font-size:220px;line-height:1.3;color:#D93A12;background:none;padding:0;border-radius:0;height:1.3em">'
         '<span class="rl">{digits}</span></div>'
         '<span class="num" style="font-size:220px;line-height:1.3;opacity:.22;vertical-align:top">/{n}</span>')


# --------------------------------------------------------------- sound ----

def soundtrack(parts, at, lv, total, ep=None):
    """Voice plus effects. No whoosh on the swipes (Pietro, 6 Nov: the one
    sound he found annoying); everything else that moves can make a sound."""
    n = int(total * SR) + SR
    voice, sfx = np.zeros(n, np.float32), np.zeros(n, np.float32)

    def put(buf, sig, t, gain=1.0):
        i = int(max(t, 0) * SR)
        buf[i:i + len(sig)] += sig[: max(0, n - i)] * gain

    for k, (a, _) in parts.items():
        put(voice, a, at[k])
    tick, ding, pop = sfx_lib.tick(), sfx_lib.ding(), sfx_lib.pop()            # the house sounds (sfx.py)
    n_lv = len(lv)
    for i in range(n_lv):                                     # the meter filling in the first second
        put(sfx, tick, .1 + i * .09, .1)
    for i, L in enumerate(lv):
        put(sfx, pop, L["start"] + .28, .26)                      # the level numeral lands
        for j in range(int(round(L["think"] / .5))):
            put(sfx, tick, L["think0"] + .05 + j * .5, .22 + .04 * j)
        put(sfx, ding, at[f"a{i}"] + .02, .12)                      # the answer
        if ep and ep["levels"][i].get("chip"):                     # the worked chip pops in
            segs = parts[f"a{i}"][1]
            put(sfx, pop, at[f"a{i}"] + segs[ep["levels"][i].get("chip_at", 0)][1] + .27, .18)
    ca = at["close"]
    for j in range(12):                                         # the score spinning like a slot
        put(sfx, tick, ca + .4 + j * .17 + .16, .09)
    put(sfx, pop, ca + .4 + 12 * .17 + .3, .26)                   # ... and landing on "?"
    end_voice = ca + parts["close"][1][-1][2]
    put(sfx, ding, end_voice + .78, .07)                          # the brand
    g = .12 / max(np.sqrt(np.mean(voice[voice != 0] ** 2)), 1e-6)
    return voice * g, sfx * g


# A real voice (the clone of Pietro) already has a room and no synthetic
# fizz: only the rumble cut and gentle compression.
CLONE_MASTER = "highpass=f=75,acompressor=threshold=-20dB:ratio=2.5:attack=12:release=140:makeup=1.5"


def reuse(work):
    """The voice parts of an earlier render (timeline.json and voice.wav in
    out/<slug>), so a layout fix does not need the voice generated again:
    a cloned voice takes minutes and gives different takes each time."""
    import wave
    t = json.load(open(work / "timeline.json"))
    with wave.open(str(work / "voice.wav")) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return {k: (a[int(t["at"][k] * SR): int(t["at"][k] * SR) + int(segs[-1][2] * SR)], [tuple(x) for x in segs])
            for k, segs in t["segments"].items()}


def remix(ep, voice_name):
    """Rebuild only the sound of an earlier render (same picture, same voice
    takes) after a change to the effects."""
    work = OUT / ep["slug"]
    parts = reuse(work)
    at, hook_end, lv, total = timeline(ep, parts)
    voice, sfx = soundtrack(parts, at, lv, total + .6, ep)
    mux(ep, voice_name, voice, sfx, total, OUT / (ep["slug"] + "-silent") / (ep["slug"] + "-silent.mp4"))
    print(f"  -> remixed {ep['slug']}.mp4")


def mux(ep, voice_name, voice, sfx, total, mp4):
    work = OUT / ep["slug"]
    write_wav(work / "voice.wav", voice)
    write_wav(work / "sfx.wav", sfx)
    final = work / f"{ep['slug']}.mp4"
    chain = CLONE_MASTER if voice_name.startswith("clone:") else MASTER
    graph = (f"[1:a]{chain}[v];anoisesrc=color=brown:amplitude=0.0012:sample_rate={SR}:duration={total + .6:.2f}[room];"
             "[v][2:a][room]amix=inputs=3:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-i", str(work / "voice.wav"), "-i", str(work / "sfx.wav"),
                    "-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", str(final)], check=True)
    return final


def make(ep, voice_name="af_heart", keep_voice=False):
    if keep_voice:
        parts = reuse(OUT / ep["slug"])
        v = None
    else:
        v, parts = synth(ep, voice_name)
    at, hook_end, lv, total = timeline(ep, parts)
    sc, check_at = scene(ep, parts, at, hook_end, lv, total)
    mp4, cover, problems = build(ep["slug"] + "-silent", [sc], theme="paper", cover_at=hook_end - .2, crf=21,
                                 check_at=check_at)
    voice, sfx = soundtrack(parts, at, lv, total + .6, ep)
    work = OUT / ep["slug"]
    work.mkdir(parents=True, exist_ok=True)
    final = mux(ep, voice_name, voice, sfx, total, mp4)
    (work / "cover.jpg").write_bytes(pathlib.Path(cover).read_bytes())
    json.dump({"at": at, "hook_end": hook_end, "levels": lv, "total": total, "voice": voice_name,
               "segments": {k: p[1] for k, p in parts.items()}}, open(work / "timeline.json", "w"), indent=1)
    if getattr(v, "log", None):                              # a cloned voice: how each line was heard
        json.dump(v.log, open(work / "takes.json", "w"), indent=1)
    print(f"  -> {final.name}  {total:.1f}s  voice {voice_name}")
    return final, problems
