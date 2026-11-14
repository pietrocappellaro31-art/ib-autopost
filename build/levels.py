"""
"Levels": the escalating quiz Reel (7 Nov). Five interview questions, each one
harder, read by the voice; the viewer keeps score and comments it at the end.

    hook    the hardest question is asked first, so the Reel opens a loop that
            only the last level closes. The question alone on every Reel and Short
            (Pietro: Reels 11 Nov, every video 12 Nov: no "That's level 4. Keep
            score."); hk["say"] has one entry. A Short's hook art sits centred
            under the question, bigger now that no lines sit beside it
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

def synth(ep, voice_name, only=None):
    """voice_name: a Kokoro voice ('af_heart'), 'clone:/path/to/reference.wav'
    (Pietro's cloned voice) or 'real:/path/to/memo' (Pietro reading the
    script himself; see voice_real.py)."""
    texts = {"hook": [s for s, _ in ep["hook"]["say"]], "close": [s for s, _ in ep["close"]["say"]]}
    for i, lv in enumerate(ep["levels"]):
        texts[f"q{i}"] = ([lv["label"]] if lv.get("label") else []) + [s for s, _ in lv["q"] if s]   # "" = on the card, not said
        texts[f"a{i}"] = [s for s, *_ in lv["a"]]
    if voice_name.startswith("real:"):
        from voice_real import parts_from_recording
        order = ([("hook", texts["hook"])]
                 + [x for i in range(len(ep["levels"])) for x in ((f"q{i}", texts[f"q{i}"]), (f"a{i}", texts[f"a{i}"]))]
                 + [("close", texts["close"])])
        parts, err = parts_from_recording(order, voice_name[5:])
        print(f"  real voice: script matched with {err:.0%} word differences (mostly the recogniser mishearing)")
        return None, parts
    v = make_voice(voice_name)
    if only:                                            # re-say only these passages (see make(redo=...))
        texts = {k: ss for k, ss in texts.items() if k in only}
        if hasattr(v, "tries"):
            v.tries = 10
    for k, ss in texts.items():
        v.phonemes(" ".join(ss))                       # fail before rendering on an unknown word
    sp = ep.get("speed", 1.0)
    parts = {}
    for n, (k, ss) in enumerate(texts.items()):
        pace = sp + (.015 if n % 3 == 1 else -.01 if n % 3 == 2 else 0)      # small variation in pace
        pace *= getattr(v, "pace_scale", 1.0)                             # a Kokoro voice's own pace (voices.json)
        if k.startswith("a") and len(ss) > 1:
            # The verdict is said on its own, then a beat, then the reasoning,
            # the way a person answers: "Nothing." ... "Debt is up a hundred..."
            parts[k] = joined(v, [ss[:1], ss[1:]], pace, gap=.2)
        elif k.startswith("q") and ep["levels"][int(k[1:])].get("label") and len(ss) > 1:
            # 12 Nov: "Last one." said on its own, then the question. Said as one passage, a short
            # label ran into the next sentence and the word check cut it in the wrong place.
            parts[k] = joined(v, [ss[:1], ss[1:]], pace, gap=.25)
        else:
            try:
                parts[k] = passage(v, " ".join(ss), pace)
            except ValueError:                           # a voice that barely pauses: say the sentences one by one
                parts[k] = joined(v, [[x] for x in ss], pace, gap=.18)
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
    q_html = kara(hk["say"][0][1], at["hook"] + hs[0][1], hs[0][2] - hs[0][1], hk.get("cols"), hl=hk.get("hl", ()), lit=True, cls="olchk olfix",
                  style=f"font-family:'Serif',serif;font-weight:700;font-size:{hk.get('qsize', 86)}px;line-height:1.06;letter-spacing:-.02em;"
                        f"text-wrap:balance")      # 14 Nov: the hook balances and re-balances itself (motion.unorphan)
    lines = "".join(kara(d, at["hook"] + a, b - a, hk.get("cols"), hide=True,
                         style=f"font-family:'Serif',serif;font-style:italic;font-weight:600;font-size:{hk.get('lsize', 70)}px;line-height:1.12;"
                               f"margin-top:6px;white-space:nowrap")      # 10 Nov: never "That's level / 4."
                    for (s, d), (_, a, b) in zip(hk["say"][1:], hs[1:]))
    hook = (ghost(n_lv) + lockup(n_lv, ep["levels"][-1]["tail"], RED)
            + card(f'<div class="lbl" style="font-size:28px;letter-spacing:.2em;color:{RED};opacity:1;margin-bottom:20px">'
                   f'THE LAST QUESTION</div>{q_html}', accent=RED)
            + f'<div style="margin-top:{hk.get("sub_gap", 44)}px"><div style="font-size:44px;font-weight:500;opacity:.7;margin-bottom:20px;text-wrap:balance">{hk["sub"]}</div>'
            # 13 Nov (cinematic standard, build step 7): a filmed hook. The page keeps an ink-framed window; the
            # cine.py film is laid into it after the page is filmed (film_hook), so the cover still reads.
            + (f'<div id="filmbox" class="nochk" style="position:relative;margin:0 auto;width:{hk["film_w"]}px;height:{hk["film_h"]}px;'
               f'outline:5px solid {INK};border-radius:4px;background:#2B2F3A"></div>' if hk.get("film") else "")
            + (f'<div class="nochk" style="position:relative;margin:0 auto;width:{hk.get("art_w", 280)}px;height:{hk.get("art_h", 224)}px">'
               f'{hk["art"](at["hook"], hook_end - at["hook"])}</div>'
               if hk.get("art") and not lines and not hk.get("film") else            # 12 Nov, Pietro: no "That's level 4. Keep score." on any video;
               f'<div style="display:flex;align-items:center;justify-content:space-between;gap:20px"><div>{lines}</div>'    # 10 Nov: a picture
               f'<div class="nochk" style="position:relative;flex:none;width:{hk.get("art_w", 280)}px;height:{hk.get("art_h", 224)}px">'   # beside the
               f'{hk["art"](at["hook"], hook_end - at["hook"])}</div></div>' if hk.get("art") and not hk.get("film") else lines)                     # hook lines
            + '</div>')
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
                ans += kara(d, aa + a, b - a, L.get("acols"), hide=True, cls="ansbig olchk olfix",
                            style=f"font-family:'Serif',serif;font-weight:700;font-size:{L.get('bigsize', 122)}px;line-height:1.02;"
                                  f"letter-spacing:-.03em;color:{TEAL};text-wrap:balance")
            else:
                ans += kara(d, aa + a, b - a, L.get("acols"), hide=True, cls="ansline olchk",
                            style="font-size:47px;font-weight:500;line-height:1.26;margin-top:14px;text-wrap:balance")
        rip = A("", "ripple", aa + .02, .9, style=f"position:absolute;left:-70px;top:-90px;width:320px;height:320px;border-radius:50%;"
                                                   f"border:5px solid {TEAL};z-index:-1")
        chip = ""
        if L.get("foot") and not L.get("chip"):
            # 13 Nov: a source line shows even when the level has no chip (it was silently dropped)
            chip = A(f'<div style="font-size:28px;font-weight:500;opacity:.6">{L["foot"]}</div>', "fade",
                     aa + chip_time(asg, min(1, len(asg) - 1)), .45, cls="anschip", style="margin-top:22px")
        if L.get("chip"):
            t0 = aa + chip_time(asg, L.get("chip_at", 0))
            foot = (f'<div style="font-size:28px;font-weight:500;opacity:.6;margin-top:10px">{L["foot"]}</div>' if L.get("foot") else "")
            chip = A(f'<div style="display:inline-block;border:3px solid {TEAL};background:rgba(15,118,110,.08);border-radius:24px;'
                     f'padding:18px 30px;font-size:44px;font-weight:600;line-height:1.3" class="olchk">{L["chip"]}</div>{foot}',
                     "pop", t0, .45, cls="anschip", style="margin-top:30px;transform-origin:left center")
        art = ""
        if L.get("art"):
            # 10 Nov (Pietro: "pictures and colors and more animated"): a drawing fills the
            # empty answer zone while the question is read and the clock runs, then fades as
            # the answer lands on top of it.
            art = A(L["art"](T["start"] + .3, aa - T["start"] - .3), "life", T["start"] + .25, aa - T["start"] - .05, fi=.35, fo=.3,
                    cls="nochk", style=f"position:absolute;left:0;top:0;width:{W}px;height:{L.get('ans_min', 420)}px;z-index:-1")
            if L.get("art_after"):
                # 13 Nov: data-settle lets motion.clearAfter() move the answer's words (or the picture) apart
                art += A(L["art_after"](aa), "life", aa + .1, T["end"] - aa + .3, fi=.35, fo=.2, cls="nochk aftr",
                         settle=round(T["end"] - .35, 3),
                         style=f"position:absolute;right:0;top:0;z-index:-1")
        filmbox = ""
        if L.get("film"):
            # 14 Nov (build step 7, second filmed beat): a level can carry a filmed window under its answer, shown
            # from the moment the card swipes in, so the question is set up on film and the answer is filmed too
            filmbox = (f'<div id="filmbox{i}" class="nochk" style="position:relative;margin:{L.get("film_gap", 30)}px auto 0;'
                       f'width:{L["film_w"]}px;height:{L["film_h"]}px;outline:5px solid {INK};border-radius:4px;background:#2B2F3A"></div>')
        answer = (f'<div style="position:relative;margin-top:22px;min-height:{L.get("ans_min", 420 if L.get("art") else 0)}px">'
                  f'{art}{rip}{ans}{chip}{filmbox}</div>')
        grp = ghost(i + 1) + lockup(i + 1, L["tail"], RED if last else INK) + qcard + think + answer
        els.append(group(column(grp), T["start"] - .02, T["end"] - T["start"] + T_SW + .02))
        check_at.append(T["end"] - .2)

    # Close: the score.
    cs = seg("close")
    ca = at["close"]
    big = kara(ep["close"]["say"][0][1], ca + cs[0][1], cs[0][2] - cs[0][1],
               style="font-family:'Serif',serif;font-weight:700;font-size:108px;line-height:1.03;letter-spacing:-.03em")
    digits = "".join(f"<span>{x}</span>" for x in [str(k) for k in range(n_lv + 1)] * 2 + ["?"])
    rest = "".join(kara(d, ca + a, b - a, ep["close"].get("cols"), hide=True, cls="olchk",
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
    # Colour grounds (10 Nov): each part of the Short gets its own full-bleed colour,
    # cross-faded at the swipes, under everything else. ep["hook"]["bg"], levels[i]["bg"],
    # ep["close"]["bg"]; none set keeps the paper ground.
    spans = [(ep["hook"].get("bg"), -1, hook_end)] + [(L.get("bg"), lv[i]["start"], lv[i]["end"]) for i, L in enumerate(ep["levels"])] \
        + [(ep["close"].get("bg"), at["close"] - .35, total + 1)]
    under = ""
    for col, s0, s1 in spans:
        if not col:
            continue
        kf = json.dumps([[round(s0, 3), 0, 0, 1, 0 if s0 > 0 else 1], [round(s0 + .4, 3), 0, 0, 1, 1], [round(s1, 3), 0, 0, 1, 1],
                         [round(s1 + .45, 3), 0, 0, 1, 0]])
        under += A("", "kf", 0, 1, cls="nochk", kf=H.escape(kf),
                   style=f"position:absolute;left:-84px;top:-230px;width:1080px;height:1920px;background:{col}")
    if ep.get("floaters"):                               # slow drifting shapes behind everything, for life
        under += ep["floaters"](total)
    if ep["close"].get("art"):                           # behind the score, above the ground
        under += ep["close"]["art"](at["close"], total - at["close"])
    if under:
        els.insert(0, f'<div class="nochk" style="position:absolute;left:0;top:0;width:{W}px;height:10px;z-index:0">{under}</div>')
    html = "".join(els) + brand + layer
    return dict(dur=total, push=.025, html=html), check_at


SCORE = ('<div class="a roll num nochk" data-fx="roll" data-at="{at:.2f}" data-d="1" data-hold=".17" '
         'style="font-size:220px;line-height:1.3;color:#D93A12;background:none;padding:0;border-radius:0;height:1.3em">'
         '<span class="rl">{digits}</span></div>'
         '<span class="num" style="font-size:220px;line-height:1.3;opacity:.22;vertical-align:top">/{n}</span>')


# --------------------------------------------------------------- sound ----

def chip_time(segs, k):
    """When the worked chip pops in, from the start of its answer part (10 Nov): in the
    pause just before sentence k, so its pop lands between words, not on them (it used
    to come .25 s into the sentence, under the voice)."""
    if k == 0:
        return segs[0][1] + .25
    gap0, gap1 = segs[k - 1][2], segs[k][1]
    return max(gap0, gap1 - .14)


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
    # 10 Nov: effects land between words. Each pop may slide a little (within lo..hi
    # seconds) to where its first 120 ms hits the least voice: the numeral pop used to land
    # on the last word of the previous part (the voice was 11.7 dB over the effects while
    # speaking; 15.8 dB after, mix DNSMOS unchanged). Ticks keep their rhythm and the answer
    # ding stays on the reveal (moving it into the pause before cost 0.24 mix DNSMOS).
    # 11 Nov: the answer ding rings for about a quarter of a second (decay 12, was 5: a full
    # second under the first words of the answer). On Levels #9's stems: the answer dings were
    # about 60% of the effect energy under speech; decay 12 took the voice margin from 16.2 to
    # 18.3 dB and the mix DNSMOS from 2.98 to 3.14. Leading it into the pause, or a lower gain,
    # did worse (2.86, 3.05). ep["ding_decay"], ep["ding_lead"], ep["ding_gain"] to override.
    env = np.convolve(voice ** 2, np.ones(int(.01 * SR)) / int(.01 * SR), "same")
    put_raw = put

    def put(buf, sig, t, gain=1.0, lo=-.12, hi=.12):
        if buf is sfx and n_voice:
            w = int(.12 * SR)
            best = min((float(np.sum(env[max(0, int((t + o) * SR)):max(0, int((t + o) * SR)) + w])), abs(o), o)
                       for o in np.arange(lo, hi + 1e-6, .01))
            t += best[2]
        put_raw(buf, sig, t, gain)

    n_voice = bool(np.any(voice))
    for i in range(n_lv):                                     # the meter filling in the first second
        put(sfx, tick, .1 + i * .09, .1, lo=0, hi=0)
    for i, L in enumerate(lv):
        put(sfx, pop, L["start"] + .28, .26)                      # the level numeral lands
        for j in range(int(round(L["think"] / .5))):
            put(sfx, tick, L["think0"] + .05 + j * .5, .22 + .04 * j, lo=0, hi=0)
        put(sfx, sfx_lib.ding((ep or {}).get("ding_decay", 12)), at[f"a{i}"] + .02 - (ep or {}).get("ding_lead", 0), (ep or {}).get("ding_gain", .12), lo=0, hi=0)     # the answer
        if ep and ep["levels"][i].get("chip"):                     # the worked chip pops in
            segs = parts[f"a{i}"][1]
            put(sfx, pop, at[f"a{i}"] + chip_time(segs, ep["levels"][i].get("chip_at", 0)), .18)
    ca = at["close"]
    for j in range(12):                                         # the score spinning like a slot
        put(sfx, tick, ca + .4 + j * .17 + .16, .09, lo=0, hi=0)          # a rhythm: never moved
    put(sfx, pop, ca + .4 + 12 * .17 + .3, .26)                   # ... and landing on "?"
    end_voice = ca + parts["close"][1][-1][2]
    put(sfx, ding, end_voice + .78, .07)                          # the brand
    # Duck the effects about 6 dB while the voice is speaking (9 Nov: DNSMOS on the
    # BELLA mix was 2.87 against 3.34 for the voice alone), back up in the pauses.
    k = int(.03 * SR)
    lev = np.convolve(np.abs(voice), np.ones(k) / k, "same")
    talking = (lev > .02 * max(lev.max(), 1e-9)).astype(np.float32)
    talking = np.convolve(talking, np.ones(int(.12 * SR)) / int(.12 * SR), "same")    # soft 120 ms edges
    sfx *= 1 - (ep or {}).get("duck", .5) * np.clip(talking, 0, 1)
    g = .12 / max(np.sqrt(np.mean(voice[voice != 0] ** 2)), 1e-6)
    return voice * g, sfx * g


def takes_from_track(work, parts, at):
    """How every line was heard, cut from the final voice track and transcribed
    on its own (9 Nov): Kokoro voices have no take log of their own, so this
    writes takes.json for them, one entry per sentence, as the clone does."""
    import wave
    from voice_check import transcribe, wer
    with wave.open(str(work / "voice.wav")) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    log = []
    for k, (_, segs) in parts.items():
        for text, x, y in segs:
            i0, i1 = int((at[k] + x - .12) * sr), int((at[k] + y + .15) * sr)
            clip = work / "_line.wav"
            write_wav(clip, a[max(i0, 0):i1] / max(np.abs(a).max(), 1e-6) * .7, sr)
            heard = transcribe(clip)
            log.append(dict(part=k, text=text, wer=round(wer(text, heard), 3), heard=heard, takes=1))
    (work / "_line.wav").unlink(missing_ok=True)
    return log


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
    silent = OUT / (ep["slug"] + "-silent") / (ep["slug"] + "-silent.mp4")
    # 14 Nov: the old path referred to mp4 and cover before they existed whenever the hook was filmed; the films
    # are laid in again here (same numbers, so the same picture) to get their foley and the filmed picture
    mp4, _, fol = films(ep, silent, silent.with_suffix(".jpg"), at, hook_end, lv)
    voice, sfx = soundtrack(parts, at, lv, total + .6, ep)
    sfx = add_foley(sfx, fol, total)
    sfx = sfx * shorts_mix(ep)[1]
    mux(ep, voice_name, voice, sfx, total, mp4)
    print(f"  -> remixed {ep['slug']}.mp4")


def shorts_mix(ep):
    """Room tone, effect level and a peak limiter for the master (11 Nov). Measured on the Singles' Day
    Short's stems at -14 LUFS (HEART): room .0012 / effects 1.0 / no limiter (the 10 Nov chain) gave mix
    DNSMOS 3.03 at -15.0 LUFS (the -1.5 dBTP ceiling held loudnorm under -14); room .0006, effects 0.8 and
    a limiter at 0.4 before loudnorm gave 3.11 at -14.6. No room at all did worse (2.95 to 3.03): a faint
    room still helps. 12 Nov, the same test on a Reel's stems at -16 LUFS (Levels #10, BELLA): the old
    chain gave 3.06 (13.7 dB voice over effects); room .0006 / effects .8 / limiter .4 gave 3.13 at -16.1
    (15.6 dB); effects left at 1.0 scored 3.16 but broke the true-peak ceiling (-1.3 dBTP) and cut the
    margin to 13.7 dB; no limiter 3.09; room .0009 3.11. So every master with no music bed (Reels and
    Shorts) now uses room .0006, effects .8 and the limiter. Override with ep["room"], ep["fx_gain"],
    ep["limit"] (None: no limiter)."""
    plain = not ep.get("music")
    return (ep.get("room", .0006 if plain else .0012), ep.get("fx_gain", .8 if plain else 1.0),
            ep.get("limit", .4 if plain else None))


def mux(ep, voice_name, voice, sfx, total, mp4):
    work = OUT / ep["slug"]
    room, _, limit = shorts_mix(ep)
    write_wav(work / "voice.wav", voice)
    write_wav(work / "sfx.wav", sfx)
    final = work / f"{ep['slug']}.mp4"
    from voice_clone import master_chain
    chain = master_chain(voice_name) or (CLONE_MASTER if voice_name.startswith(("clone:", "real:")) else MASTER)
    if ep.get("denoise") and "anlmdn" not in chain:          # 13 Nov: per episode (G2 carries it in voices.json)
        chain += "," + ep["denoise"]
    lim = f"alimiter=limit={limit}:attack=2:release=50:level=false," if limit else ""
    graph = (f"[1:a]{chain}[v];anoisesrc=color=brown:amplitude={room}:sample_rate={SR}:duration={total + .6:.2f}[room];"
             f"[v][2:a][room]amix=inputs=3:normalize=0,{lim}loudnorm=I={ep.get('lufs', -16)}:TP={ep.get('tp', -1.5)}:LRA=11[a]")
    # ep["lufs"] (10 Nov): YouTube Shorts ship without music now and still master at -14 like YouTube; Reels stay -16.
    extra = []
    if ep.get("music"):
        # YouTube Shorts (8 Nov): an original music bed (music.py), ducked under the voice, -14 LUFS.
        # Instagram Reels stay without music: Pietro adds it in the app.
        import music
        bed, info = music.track(total + .5, seed=ep.get("music_seed", sum(map(ord, ep["slug"]))))
        music.write(work / "music.wav", bed)
        extra = ["-i", str(work / "music.wav")]
        graph = (f"[1:a]{chain},aresample=48000,asplit=2[v][key];[2:a]aresample=48000[fx];"
                 f"[3:a]volume={ep.get('music_level', .2)}[m];[m][key]sidechaincompress=threshold=0.02:ratio=5:attack=30:release=350[md];"
                 "[v][fx][md]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    if not ep.get("music") and ep.get("master", "two_stage" if ep.get("lufs", -16) == -14 else "loudnorm") == "two_stage":
        return two_stage(ep, mp4, work, graph, final)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-i", str(work / "voice.wav"), "-i", str(work / "sfx.wav"), *extra,
                    "-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", str(final)], check=True)
    return final


def loudness(path):
    """Integrated LUFS and true peak (dBTP) of a file, from ffmpeg's ebur128."""
    out = subprocess.run(["ffmpeg", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summ = out[out.rfind("Summary:"):]
    i, p = re.search(r"I:\s+(-?[\d.]+) LUFS", summ), re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ)
    return float(i.group(1)), float(p.group(1))


def two_stage(ep, mp4, work, graph, final, tp=-1.5):
    """12 Nov: the -14 LUFS master in two stages, because one dynamic loudnorm behind the 0.4 limiter
    landed at -14.6 to -14.8 (it holds gain back to keep the -1.5 dBTP ceiling). Stage 1 mixes voice,
    effects and room through the same chain and limiter, with no loudnorm, to a 48 kHz stem. Stage 2
    measures it, applies one plain gain to the target and a true-peak limiter at the ceiling; a second
    measure corrects any residual (the limiter takes a little loudness off the loudest words).
    Measured on the compound interest Short's stems (MICHAEL): single stage -15.2 LUFS, mix DNSMOS 3.12;
    two stage -14.1 LUFS, -1.7 dBTP, mix 3.10. Default for -14 LUFS masters with no music bed;
    ep["master"] = "loudnorm" restores the single stage."""
    target = ep.get("lufs", -14)
    pre = work / "premaster.wav"
    g1 = graph.split("loudnorm=")[0].rstrip(",") + "[a]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(work / "voice.wav"), "-i", str(work / "sfx.wav"),
                    "-filter_complex", g1.replace("[1:a]", "[0:a]").replace("[2:a]", "[1:a]"), "-map", "[a]",
                    "-ar", "48000", "-c:a", "pcm_f32le", str(pre)], check=True)
    i0, _ = loudness(pre)
    ceil = 10 ** ((tp - .3) / 20)                           # 0.3 dB under the ceiling for the AAC encode
    gain = target - i0
    for _ in range(3):
        af = (f"volume={gain:.2f}dB,aresample=192000,alimiter=limit={ceil:.4f}:attack=1:release=60:level=false,"
              "aresample=48000")                             # limiting at 4x sample rate catches inter-sample peaks
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-i", str(pre), "-map", "0:v", "-map", "1:a",
                        "-af", af, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                        "-movflags", "+faststart", str(final)], check=True)
        i1, p1 = loudness(final)
        if abs(i1 - target) <= .2 and p1 <= tp + .05:
            break
        gain += target - i1
    pre.unlink(missing_ok=True)
    return final


def film_window(ep, mp4, box, t0, t_rest, t_out, fn, tag, T_SW=.34, fade_out=True):
    """13 Nov (cinematic-standard.md section 8, step 7: a filmed segment inside the Levels engine); generalised
    14 Nov to any window (the hook's #filmbox, a level's #filmbox<i>). The window is measured on the filmed page
    every 30 ms through the card's whip in (t0 to t_rest) and whip out (t_out to t_out + T_SW), and at points in
    between (the page's slow push moves it a pixel or two), the film is laid into it piecewise-linearly, and fades
    with the card. fn(dur, w, h) returns (shots, foley events in film seconds).
    14 Nov: the film gets the card's motion blur. The page's pass blurs the card by 26 px per 1000 px of swipe
    (motion.py 'pass': bl = b * 26 as x = -b * 1000), so the film's Gaussian sigma follows the measured offset
    from where the window rests, stepped every 30 ms (gblur with timeline enable). Before, the film stayed sharp
    inside a blurred card. Returns (mp4, foley events in Reel seconds, the window record)."""
    import cine
    from playwright.sync_api import sync_playwright
    src = OUT / (ep["slug"] + "-silent") / "motion.html"
    times = sorted(set([round(t0 + .03 * k, 3) for k in range(int((t_rest - t0) / .03) + 1)]
                       + [round(t_rest + (t_out - t_rest) * k / 4, 3) for k in range(5)]
                       + [round(t_out + .03 * k, 3) for k in range(1, int(T_SW / .03) + 2)]))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(src.resolve().as_uri())
        pg.evaluate("document.fonts.ready")
        rects = []
        for t in times:
            pg.evaluate(f"seek({t})")
            rects.append(pg.evaluate(f"(() => {{ const r = document.getElementById('{box}').getBoundingClientRect();"
                                     " return [r.left, r.top, r.width, r.height]; })()"))
        b.close()
    rest = [r for t, r in zip(times, rects) if t_rest - 1e-3 <= t <= t_out + 1e-3]
    fw, fh = rest[0][2], rest[0][3]
    fw, fh = int(round(fw / 2) * 2), int(round(fh / 2) * 2)
    dur = round(t_out + T_SW + .1 - t0, 2)
    shots, fx = fn(dur, fw, fh)
    html, total = cine.film_html(shots, fw, fh, caps="", mark=False)
    work = OUT / ep["slug"]
    work.mkdir(parents=True, exist_ok=True)
    film, secs = cine.render(html, total, work, tag, fw, fh, fps=30)
    out = pathlib.Path(str(mp4).replace(".mp4", f"-{tag}.mp4"))
    def pw(i):                                    # piecewise-linear position through the sampled moments
        e = f"{rects[-1][i]:.2f}"
        for (ta, ra), (tb, rb) in reversed(list(zip(zip(times, rects), zip(times[1:], rects[1:])))):
            e = f"if(lt(t,{tb:.3f}),{ra[i]:.2f}+({rb[i] - ra[i]:.3f})*(t-{ta:.3f})/{max(tb - ta, 1e-3):.3f},{e})"
        return e
    xe, ye = pw(0), pw(1)
    x_in, x_out = rest[0][0], rest[-1][0]
    steps = []
    for (ta, ra), (tb, rb) in zip(zip(times, rects), zip(times[1:], rects[1:])):
        xm = (ra[0] + rb[0]) / 2
        ref = x_in if tb <= t_rest + 1e-3 else x_out if ta >= t_out - 1e-3 else None
        if ref is None:
            continue
        sig = 26 * abs(xm - ref) / 1000
        if sig > .3:
            steps.append((round(ta, 3), round(tb, 3), round(sig, 2)))
    blur = "".join(f"gblur=sigma={g}:enable='between(t,{a_},{b_})'," for a_, b_, g in steps)
    end = t_out + T_SW
    graph = (f"[1:v]setpts=PTS+{t0:.3f}/TB,{blur}format=yuva420p"
             + (f",fade=t=out:st={end - .12:.3f}:d=0.12:alpha=1" if fade_out else "") + "[f];"
             f"[0:v][f]overlay=x='{xe}':y='{ye}':eof_action=pass:enable='between(t,{t0:.3f},{end + .1:.3f})'[v]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-i", str(film), "-filter_complex", graph, "-map", "[v]",
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", str(out)], check=True)
    rec = dict(box=box, t0=round(t0, 3), rest=rest[0], rest_end=rest[-1], bottom=round(max(r[1] + r[3] for r in rest), 1),
               film=[fw, fh], dur=dur, render_seconds=round(secs, 1), foley=len(fx), blur_steps=steps)
    print(f"  filmed {box}: {fw} x {fh} px, {dur:.2f} s from {t0:.2f} s, bottom {rec['bottom']} px, {len(fx)} foley events, "
          f"{len(steps)} motion-blur steps (max sigma {max([g for *_, g in steps] or [0])})", flush=True)
    return out, [(e[0], e[1] + t0, *e[2:]) for e in fx], rec


def films(ep, mp4, cover, at, hook_end, lv, T_SW=.34):
    """Every filmed window of the episode (the hook's, then any level's), with their foley as (events, gain)
    and film.json. The cover is taken again from the result. Returns (mp4, cover, [(events, gain), ...])."""
    hk, recs, fol = ep["hook"], [], []
    if hk.get("film"):
        mp4, fx, rec = film_window(ep, mp4, "filmbox", 0.0, 0.0, hook_end, lambda d, w, h: hk["film"](d, w, h, hook_end - at["hook"]),
                                   "hook-film", T_SW)
        recs.append(rec); fol.append((fx, hk.get("foley_gain", .5)))
    for i, L in enumerate(ep["levels"]):
        if not L.get("film"):
            continue
        t0, end = lv[i]["start"] - .02, lv[i]["end"]
        marks = dict(q=at[f"q{i}"] - t0, a=at[f"a{i}"] - t0, think=lv[i]["think0"] - t0, end=end - t0)
        mp4, fx, rec = film_window(ep, mp4, f"filmbox{i}", t0, t0 + T_SW + .03, end, lambda d, w, h, m=marks, L=L: L["film"](d, w, h, m),
                                   f"l{i}-film", T_SW)
        recs.append(rec); fol.append((fx, L.get("foley_gain", .5)))
    if recs:
        cov = pathlib.Path(str(cover).replace(".jpg", "-film.jpg"))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(hook_end - .2, 0):.3f}", "-i", str(mp4), "-frames:v", "1",
                        "-q:v", "2", str(cov)], check=True)
        cover = cov
        json.dump(recs, open(OUT / ep["slug"] / "film.json", "w"), indent=1)
    return mp4, cover, fol


def add_foley(sfx, fol, total):
    """The filmed windows' foley, timed by the same numbers as their pictures, onto the effects track."""
    if not fol:
        return sfx
    from scipy.signal import resample_poly
    import sfx as sfx_lib
    for fx, gain in fol:
        if not fx:
            continue
        f = resample_poly(sfx_lib.foley_track(fx, total + .6).mean(1), 1, 2).astype(np.float32)
        k = min(len(sfx), len(f))
        sfx[:k] += f[:k] * gain
    return sfx


def make(ep, voice_name="af_heart", keep_voice=False, redo=()):
    """keep_voice: reuse the last render's voice takes (a layout fix).
    redo: with keep_voice, say these passages again ("hook", "q0", "a0", ...,
    "close"), with up to 10 takes each, and keep the rest."""
    say = ep["hook"]["say"]
    if len(say) > 1 and any(re.search(r"keep score|that's level", s_, re.I) for s_, _ in say[1:]):
        # 12 Nov, Pietro: "'That's level 4, keep score' is useless and should be removed from all videos."
        # Enforced here so an episode copied from an older file cannot bring it back.
        ep["hook"] = dict(ep["hook"], say=[x for x in say if not re.search(r"keep score|that's level", x[0], re.I)])
        print("  hook: dropped \"That's level 4. Keep score.\" (Pietro, 12 Nov: removed from all videos)")
    if keep_voice:
        parts = reuse(OUT / ep["slug"])
        v = None
        if redo:
            v, again = synth(ep, voice_name, only=set(redo))
            parts.update(again)
            old_takes = OUT / ep["slug"] / "takes.json"
            if old_takes.exists() and getattr(v, "log", None):      # keep the record of the passages not redone
                kept = " ".join(x for k, (_, segs) in parts.items() if k not in redo for x, _, _ in segs)
                keep = [r for r in json.load(open(old_takes)) if r["text"] in kept]     # lines still in the Reel
                v.log[:0] = keep
    else:
        v, parts = synth(ep, voice_name)
    at, hook_end, lv, total = timeline(ep, parts)
    sc, check_at = scene(ep, parts, at, hook_end, lv, total)
    mp4, cover, problems = build(ep["slug"] + "-silent", [sc], theme="paper", cover_at=hook_end - .2, crf=21,
                                 check_at=check_at, fit=ep.get("fit", True))
    mp4, cover, fol = films(ep, mp4, cover, at, hook_end, lv)
    voice, sfx = soundtrack(parts, at, lv, total + .6, ep)
    sfx = add_foley(sfx, fol, total)
    sfx = sfx * shorts_mix(ep)[1]                            # 11 Nov: effects a touch lower on YouTube Shorts
    work = OUT / ep["slug"]
    work.mkdir(parents=True, exist_ok=True)
    final = mux(ep, voice_name, voice, sfx, total, mp4)
    (work / "cover.jpg").write_bytes(pathlib.Path(cover).read_bytes())
    json.dump({"at": at, "hook_end": hook_end, "levels": lv, "total": total, "voice": voice_name,
               "segments": {k: p[1] for k, p in parts.items()}}, open(work / "timeline.json", "w"), indent=1)
    from voice_clone import voices, log_voice, key
    named = key(voice_name)
    if voices().get(named, {}).get("rotation"):
        log_voice(ep["slug"], named)                         # keeps the L2 / L3 alternation across sessions
    if getattr(v, "log", None):                              # a cloned voice: how each line was heard
        json.dump(v.log, open(work / "takes.json", "w"), indent=1)
    elif not keep_voice or redo:                             # a Kokoro voice: check every line from the track itself
        log = takes_from_track(work, parts, at)
        json.dump(log, open(work / "takes.json", "w"), indent=1)
        bad = [x for x in log if x["wer"] > 0]
        print(f"  lines heard word for word: {len(log) - len(bad)}/{len(log)}" + "".join(f"\n    CHECK {x['part']}: {x['text']!r} heard {x['heard']!r}" for x in bad))
    if not ep.get("music") and ep["slug"].startswith("shorts-"):
        # 12 Nov (Pietro's music library): the library track that fits the Short's mood, to add with
        # "Add sound" in the YouTube app at upload. Never mixed into the file (music_library.py).
        import music_library
        ref = music_library.pick(ep.get("mood", "playful"), "short", slug=ep["slug"])
        if ref:
            pick = dict(id=ref["id"], search=ref.get("search"), start=ref["calm_start"], tags=ref["tags"], others=ref["others"],
                        line=music_library.instructions(ref, "short"))
            json.dump(pick, open(work / "music_pick.json", "w"), indent=1)
            print(f"  music: {pick['line']}")
    report = sound_report(work, final, voice, sfx)
    json.dump(report, open(work / "sound.json", "w"), indent=1)
    print(f"  sound: DNSMOS voice {report['voice']['ovrl']} / mix {report['mix']['ovrl']} (bak {report['mix']['bak']}), "
          f"voice over effects {report['voice_over_fx_db']} dB while speaking, {report['lufs']} LUFS, {report['tp']} dBTP"
          + ("" if report["mix"]["ovrl"] >= 3.1 else "  CHECK mix below 3.1"))
    print(f"  -> {final.name}  {total:.1f}s  voice {voice_name}" + ("  CHECK over 60 s" if total > 60 else ""))
    return final, problems


def sound_report(work, final, voice, sfx):
    """The sound measures of every render (9 Nov), printed next to the takes line
    so they are never left to a manual pass: DNSMOS on the voice stem and on the
    final mix, how far the voice sits over the effects while it speaks, and the
    loudness of the file."""
    import re
    rep = {}
    try:
        import quality
        rep["voice"], rep["mix"] = quality.score(work / "voice.wav"), quality.score(final)
    except Exception as e:                                 # no DNSMOS model in this session
        rep["voice"] = rep["mix"] = dict(sig=None, bak=None, ovrl=None, error=str(e)[:80])
    talking = np.abs(voice) > .02 * max(np.abs(voice).max(), 1e-9)
    k = int(.25 * SR)
    talking = np.convolve(talking.astype(np.float32), np.ones(k) / k, "same") > 0
    m = min(len(voice), len(sfx))
    v_rms = np.sqrt(np.mean(voice[:m][talking[:m]] ** 2) + 1e-12)
    f = sfx[:m][talking[:m]]
    f_rms = np.sqrt(np.mean(f[f != 0] ** 2) + 1e-12) if np.any(f != 0) else 1e-12
    rep["voice_over_fx_db"] = round(float(20 * np.log10(v_rms / f_rms)), 1)
    out = subprocess.run(["ffmpeg", "-i", str(final), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summ = out[out.rfind("Summary:"):]
    i, p = re.search(r"I:\s+(-?[\d.]+) LUFS", summ), re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ)
    rep["lufs"], rep["tp"] = (float(i.group(1)) if i else None), (float(p.group(1)) if p else None)
    return rep
