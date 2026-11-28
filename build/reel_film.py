"""
Full-frame animated Reels (26 Nov 2026, Pietro).

Pietro, 26 Nov: Reels are underperforming; "we're going to try to animate the whole video a lot, so there will not
be an image in an image. It will just be the whole video completely animated"; "I also don't like the blurred
background"; "we need to have better storytelling"; the music comes from Instagram's trending library.

What this module changes against the 16 to 26 Nov Reels (build/story.py: a drawing on a paper card floating on a
dark, glowing ground, under a block of heading text):

  * The whole 1080 x 1920 frame is one filmed world (build/cine.py: depth layers, a moving camera, rigged people,
    props that act). No card, no panel, no frame inside the frame, no slide headings.
  * Nothing is blurred: depth of field is 0 on every shot and every layer is marked noblur (check_shots refuses a
    shot with dof). The vignette is light.
  * Numbers live in the world (a whiteboard written as the narrator says them, a sheet on the table, coins) or as
    one big kinetic number over the picture at the payoff, never on a card.
  * Story first: a person with something at stake (an interview, a deal, a bill), the wrong answer most people give,
    the turn, the payoff with one number, a loop or a question back to the viewer. The hook is SAID and SHOWN in the
    first two seconds (hook()).
  * No subtitles (Pietro, 27 Nov: "we don't need subtitles. We don't want subtitles in the videos."). captions()
    returns only the screen-text CSS unless SUBTITLES is set back to True.
  * Every Reel ends on the follow ask, SAID and SHOWN (Pietro, 27 Nov: "include an invitation to follow, and make sure
    that invitation is not just visual but also verbal"): narration() refuses a script whose last line does not ask
    for the follow, and film() refuses a last shot without follow_ask() (the handle and a + FOLLOW button that is
    tapped and turns to FOLLOWING, in the band the subtitles used to have).
  * The narrator is voice_clone.narrator(): EMMA (Kokoro bf_emma, 0.97) from 27 Nov to 4 Dec (Pietro), else HEART.
  * Sound: voice and action-timed effects only. The music is a trending licensed track that Instagram attaches at
    posting (publish.py, Audio API), so the MP4 never carries music.

Shots are timed from the narration itself (beats()): one beat per narrated line, the shot running from the line's
start to the next line's start, so picture and voice cannot drift.

    from reel_film import *          (see build/reelf_depreciation.py, the first Reel made with it)
"""

import json
import pathlib
import subprocess
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cine as C            # noqa: E402
import cine_lib as L        # noqa: E402

W, H = 1080, 1920
BIG, LX, LY = 10000, -3200, -1400
GAP = .22                     # seconds of air between narrated lines
LEAD = .35                    # the first line starts this far in (frame 0 is already moving)
INK, RED, TEAL, PAPER, MUSTARD = C.INK, C.RED, C.TEAL, C.PAPER, C.MUSTARD
GREEN = "#2F8F4E"

# Instagram covers the bottom ~380 px (caption, audio line) and a ~140 px column on the right (buttons).
SAFE = dict(top=220, bottom=380, right=150, left=60)
ACTION_BOTTOM = 1390          # keep numbers and faces above this screen y: the caption band starts there
CAP_BOTTOM = 380              # the band just above the covered one (screen y about 1400 to 1540): the follow ask
SUBTITLES = False             # 27 Nov (Pietro): no subtitles in the videos
FOLLOW_TAIL = 1.7             # seconds the last shot runs after the last line ends (the tap and FOLLOWING read)
FOLLOW_LINE = "Follow for a new interview question every day."
HANDLE = "@investmentbankinginterviews"


def lay(z, inner):
    """A depth layer that is never blurred."""
    return C.layer(z, inner, x=LX, y=LY, w=BIG, h=4000, noblur=True)


def cam_x(x, z):
    """The camera x (depth-1 plane) that puts world x on layer z in the middle of the frame."""
    return 960 + (x - 960) / z


def cam_y(y, z):
    return 540 + (y - 540) / z


def shot(dur, layers, actors=(), cam=None, over=(), grade="none", tin=("cut", 0), shake=.25, vig=.35):
    return dict(dur=dur, layers=list(layers), actors=list(actors), cam=cam, over=list(over), dof=0, focus=None,
                grade=grade, tin=tin, shake=shake, vig=vig)


def check_shots(shots):
    """The 26 Nov rules, enforced: no depth of field, nothing marked for blur, no card or panel classes."""
    problems = []
    for i, s in enumerate(shots):
        if s.get("dof", 0):
            problems.append(f"shot {i}: dof {s['dof']} (no blur in Reels)")
        for layer in s["layers"]:
            if 'data-noblur="1"' not in layer:
                problems.append(f"shot {i}: a layer that can be blurred")
                break
        html = "".join(s["layers"]) + "".join(s.get("over", []))
        for bad in ("class=\"panel", "paper panel", "backdrop-filter", "filter:blur", "blur("):
            if bad in html:
                problems.append(f"shot {i}: {bad}")
    return problems


# ------------------------------------------------------------------------------------------------ screen text

CSS = """<style>
.cap span.line{background:none!important;font-family:'Sans',sans-serif;font-weight:600;color:#fff;
 -webkit-text-stroke:0;text-shadow:0 0 2px #000,0 0 6px rgba(0,0,0,.95),0 3px 14px rgba(0,0,0,.7);letter-spacing:.005em}
.cap .w{opacity:.55}
.hk{position:absolute;left:60px;right:150px;text-align:left;font-family:'Serif',serif;font-weight:700;color:#fff;
 line-height:1.02;letter-spacing:-.02em;text-shadow:0 0 3px #000,0 2px 10px rgba(0,0,0,.9),0 8px 30px rgba(0,0,0,.6);z-index:8}
.hk .y{color:#F2C35B}
.bn{position:absolute;left:0;right:0;text-align:center;font-family:'Serif',serif;font-weight:700;color:#fff;z-index:8;
 text-shadow:0 0 4px #000,0 4px 16px rgba(0,0,0,.9),0 10px 40px rgba(0,0,0,.6)}
</style>"""


def hook(lines, at=0.0, d=2.8, top=300, size=104):
    """The promise, on screen from frame 0: lines is a list of (text, yellow?) pieces per line, each line pops in
    on its own. It sits in the top band, clear of the captions and of the action."""
    from motion import A
    out = ""
    for i, line in enumerate(lines):
        html = "".join(f'<span class="y">{t}</span>' if yel else t for t, yel in line)
        out += A(A(html, "pop", round(at + i * .18, 3), .35), "life", 0, at + d, style=f"position:absolute;left:0;top:{i * size * 1.04:.0f}px",
                 fi=.01, fo=.3)
    return f'<div class="hk" style="top:{top}px;font-size:{size}px">{out}</div>'


def big_number(text, at, d, top=620, size=230, color="#fff", count=None):
    """One number over the picture at the payoff (no card). count=(from, to, decimals, prefix, suffix) counts up."""
    from motion import A
    if count:
        f0, f1, dec, pre, suf = count
        inner = (f'<span class="a" data-fx="count" data-at="{at:.3f}" data-d=".8" data-from="{f0}" data-to="{f1}" data-dec="{dec}" '
                 f'data-pre="{pre}" data-suf="{suf}">{pre}{f0}{suf}</span>')
    else:
        inner = text
    return A(A(inner, "pop", at, .4), "life", 0, at + d, cls="bn", style=f"top:{top}px;font-size:{size}px;color:{color}", fi=.01, fo=.3)


# ------------------------------------------------------------------------------------------------ the voice

def asks_follow(text):
    return "follow" in text.lower()


def narration(lines, work, voice_name=None):
    """Say each line once with the narrator of the day (cached per line and voice), then find its word times.
    The last line must ask for the follow (27 Nov)."""
    from voice import write_wav, SR
    from voice_clone import make_voice, narrator
    from voice_check import transcribe, wer
    import wave
    if not asks_follow(lines[-1]):
        raise SystemExit(f"REEL RULES: the last spoken line must ask for the follow (e.g. {FOLLOW_LINE!r}); it is {lines[-1]!r}")
    name = voice_name or narrator()
    cache = pathlib.Path(work) / "lines"
    cache.mkdir(parents=True, exist_ok=True)
    v, out = None, []
    for i, text in enumerate(lines):
        key, wav = cache / f"{i:02d}.json", cache / f"{i:02d}.wav"
        meta = json.load(open(key)) if key.exists() else {}
        if meta.get("text") != text or meta.get("voice") != name or not wav.exists():
            v = v or make_voice(name)
            write_wav(wav, v.say(text))
            heard, words = transcribe(str(wav), with_words=True)
            meta = dict(text=text, voice=name, heard=heard, wer=float(wer(text, heard)), words=words)
            json.dump(meta, open(key, "w"), indent=1)
        with wave.open(str(wav)) as wf:
            meta["dur"] = wf.getnframes() / SR
        meta["wav"] = str(wav)
        out.append(meta)
    return out


def _script_words(text, heard_words, start, dur):
    ws = text.split()
    if heard_words and len(heard_words) == len(ws):
        return [(w, start + a, start + b) for w, (_, a, b) in zip(ws, heard_words)]
    a0, a1 = (heard_words[0][1], heard_words[-1][2]) if heard_words else (.05, dur - .05)
    lens = np.cumsum([0] + [len(w) + 1 for w in ws])
    return [(w, start + a0 + (a1 - a0) * lens[i] / lens[-1], start + a0 + (a1 - a0) * lens[i + 1] / lens[-1]) for i, w in enumerate(ws)]


def beats(voice, holds=None):
    """Line start times, shot lengths and per-line word times. holds: {line index: extra seconds after it}."""
    holds = holds or {}
    t, starts = LEAD, []
    for i, m in enumerate(voice):
        starts.append(round(t, 3))
        t += m["dur"] + GAP + holds.get(i, 0)
    ends = starts[1:] + [round(t - GAP + FOLLOW_TAIL, 3)]
    shot_starts = [0.0] + starts[1:]
    durs = [round(e - s, 3) for s, e in zip(shot_starts, ends)]
    words = [_script_words(m["text"], m["words"], s, m["dur"]) for m, s in zip(voice, starts)]
    return dict(starts=starts, shot_starts=shot_starts, durs=durs, words=words, total=round(sum(durs), 3))


def at_word(b, line, token, shot=None, end=False, nth=1):
    """When a word is said (its nth occurrence in the line): film seconds, or shot seconds if shot is given."""
    k = 0
    for w, a, z in b["words"][line]:
        if w.strip(".,?!:;").lower() == token.strip(".,?!:;").lower():
            k += 1
            if k < nth:
                continue
            t = z if end else a
            return round(t - (b["shot_starts"][shot] if shot is not None else 0), 3)
    raise KeyError(f"{token!r} not in line {line}")


def captions(voice, b):
    """Sentence by sentence, word by word, big, outlined, no box. Off since 27 Nov (SUBTITLES): only the CSS."""
    if not SUBTITLES:
        return CSS
    out = []
    for m, wd in zip(voice, b["words"]):
        cur = []
        for x in wd:
            cur.append(x)
            if x[0].endswith((".", "?", "!", ":")) and len(cur) > 2:
                out.append((" ".join(y[0] for y in cur), cur[0][1], cur[-1][2] + .12, cur))
                cur = []
        if cur:
            if out and len(cur) <= 2 and out[-1][3][-1][1] >= wd[0][1]:
                prev = out.pop()
                cur = prev[3] + cur
            out.append((" ".join(y[0] for y in cur), cur[0][1], cur[-1][2] + .12, cur))
    for i in range(len(out) - 1):
        if out[i][2] > out[i + 1][1] - .08:
            out[i] = (out[i][0], out[i][1], out[i + 1][1] - .08, out[i][3])
    return CSS + C.captions(out, W, H, size=58, bottom=CAP_BOTTOM, maxw=840)


# ------------------------------------------------------------------------------------------------ the sets

def _r(x, y, w, h, fill, rx=0, sw=3.2, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" {extra}/>'


def interview_room(seed=4):
    """A bank's interview room at dusk, laid out for a vertical frame: a wall with a tall window on an invented
    skyline (lights flicker on), a small table, two chairs facing each other 400 px apart so a two-shot fits 9:16.
    The episode adds its own whiteboard (layer z .55, above the heads). Returns (layers by name: (z, svg), anchors):
    candidate x 760 and interviewer x 1160 (actor layer z .8, ground 1060), table top y 925 (z .86)."""
    import random
    rng = random.Random(seed)
    wall = C.defs() + ('<defs><linearGradient id="duskR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2B3250"/>'
                       '<stop offset=".7" stop-color="#C9825A"/></linearGradient></defs>')
    wall += '<rect x="-2600" y="-1600" width="7200" height="4200" fill="#CFC6B8"/>'
    wall += '<rect x="-2600" y="-1600" width="7200" height="300" fill="#BDB3A5"/>'
    wx, wy, ww, wh = -260, 120, 820, 860
    sky = f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="url(#duskR)"/>'
    x = wx - 10
    while x < wx + ww:
        bw, bh = rng.uniform(70, 160), rng.uniform(260, 700)
        sky += f'<rect x="{x:.0f}" y="{wy + wh - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{rng.choice(["#283048", "#323A55", "#3B4360"])}"/>'
        for r in range(int(bh // 36)):
            for c in range(int(bw // 28)):
                if rng.random() < .3:
                    op = rng.uniform(.5, .95)
                    sky += (f'<rect x="{x + 8 + c * 28:.0f}" y="{wy + wh - bh + 14 + r * 36:.0f}" width="12" height="16" fill="{MUSTARD}" '
                            f'opacity="{op:.2f}" data-flick=\'[{op:.2f},0.06,{rng.randint(0, 9)}]\'/>')
        x += bw + rng.uniform(4, 16)
    wall += (sky + f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#3F444F" stroke-width="24"/>'
             + f'<path d="M{wx + ww / 2},{wy} L{wx + ww / 2},{wy + wh}" stroke="#3F444F" stroke-width="14"/>'
             + f'<path d="M{wx},{wy + wh * .45} L{wx + ww},{wy + wh * .45}" stroke="#3F444F" stroke-width="10"/>')
    # a framed print and a wall clock, right of the board
    wall += _r(1420, 330, 200, 260, "#E8E1D4", sw=4) + _r(1436, 346, 168, 228, TEAL, sw=2) + \
        f'<path d="M1446,540 L1500,460 L1540,500 L1596,400" fill="none" stroke="{MUSTARD}" stroke-width="10" stroke-linecap="round"/>'
    wall += f'<circle cx="1520" cy="200" r="54" fill="#F7F5F2" stroke="{INK}" stroke-width="5"/><path d="M1520,200 L1520,162 M1520,200 L1548,212" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    floor = ('<rect x="-2600" y="1060" width="7200" height="1600" fill="#7E766C"/>'
             + "".join(f'<path d="M{-2600 + k * 220},1060 L{-2600 + k * 220 - 300},2660" stroke="#6E675E" stroke-width="3"/>' for k in range(34)))
    # 26 Nov, measured on a still: a seated figure (scale 1, ground 1060) has its head at y 760 to 790 and its hips
    # at about 990, so seats are at 985 and the table top at 925 (below the chest)
    chairs = (_r(640, 985, 170, 22, "#2B2F3A", rx=8) + _r(626, 790, 30, 215, "#2B2F3A", rx=12)
              + _r(1110, 985, 170, 22, "#2B2F3A", rx=8) + _r(1264, 790, 30, 215, "#2B2F3A", rx=12)
              + _r(717, 1007, 16, 50, "#5A5F6A", sw=2.4) + _r(1187, 1007, 16, 50, "#5A5F6A", sw=2.4)
              + f'<path d="M660,1058 L790,1058 M1130,1058 L1260,1058" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    table = (_r(845, 925, 230, 24, "#E8E1D4", rx=6, sw=4) + _r(868, 949, 20, 112, "#5A5F6A", sw=3) + _r(1032, 949, 20, 112, "#5A5F6A", sw=3)
             + f'<g transform="translate(1035,925) scale(.8)">{L.cup()}</g>')
    near = ""
    layers = dict(wall=(.35, wall), floor=(.6, floor), chairs=(.72, chairs), table=(.86, table))
    return layers, dict(cand_x=760, int_x=1160, ground=1060, table_y=925, near=near)


TICKERS = ["ALDR +1.2%", "BKRN -0.8%", "CVLT +0.4%", "DMSN -2.1%", "ERGO +3.0%", "FNWK -0.5%", "GLTR +0.9%",
           "HSPN -1.4%", "IVRY +0.2%", "JNPR -0.3%"]      # invented tickers for set dressing, no real company


def trading_floor(seed=7, hero_x=800, t_scroll=40.0):
    """A bank's trading floor at night (28 Nov), laid out for a vertical frame like interview_room. Back wall (z .3):
    a dark wall with a long LED ticker band (invented tickers scrolling left) and three wall screens with drifting
    lines. Middle (z .5): a row of trading desks with banks of glowing monitors that flicker. Floor (z .6). Hero desk
    (z .86): a desk in front of the trader with one big monitor whose screen the episode draws on (anchors["screen"]:
    x, y, w, h on the z .86 layer). The trader sits at hero_x on the actor layer (z .8, ground 1060), facing right
    (dir=1) toward the monitor; a chair is drawn for her (z .72). Returns (layers by name: (z, svg), anchors)."""
    import random
    rng = random.Random(seed)
    wall = C.defs() + ('<defs><linearGradient id="tfWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#26304A"/>'
                       '<stop offset="1" stop-color="#3C4862"/></linearGradient>'
                       '<radialGradient id="tfGlow"><stop offset="0" stop-color="#7FD6C2" stop-opacity=".55"/>'
                       '<stop offset="1" stop-color="#7FD6C2" stop-opacity="0"/></radialGradient></defs>')
    wall += '<rect x="-2600" y="-1600" width="7200" height="4200" fill="url(#tfWall)"/>'
    # the LED ticker band: two copies of the tape so the scroll never shows a gap
    tape = "".join(f'<tspan fill="{"#7BE08F" if "+" in t else "#FF7A6B"}">{t}</tspan><tspan fill="#5A6478">  ●  </tspan>'
                   for t in TICKERS * 3)
    band_y = 130
    wall += f'<rect x="-2600" y="{band_y - 60}" width="7200" height="96" fill="#0E1118" stroke="#3A4256" stroke-width="4"/>'
    wall += (f'<g {C.kv(translate=[[0, 0, 0], [t_scroll, -2400, 0, "lin"]])}>'
             + "".join(f'<text x="{x0}" y="{band_y + 6}" font-family="\'Sans\',sans-serif" font-weight="700" font-size="46" letter-spacing="2">{tape}</text>'
                       for x0 in (-2600,)) + '</g>')
    # three wall screens with lines that drift
    for k, sx in enumerate((-300, 560, 1420)):
        sw_, sh_ = 700, 380
        wall += _r(sx, 250, sw_, sh_, "#121722", rx=10, sw=5)
        pts, v = [], rng.uniform(.4, .6)
        for i in range(15):
            v = min(.9, max(.1, v + rng.uniform(-.12, .12)))
            pts.append(f"{sx + 30 + i * (sw_ - 60) / 14:.0f},{250 + 40 + (1 - v) * (sh_ - 80):.0f}")
        col = ["#7BE08F", "#F2C35B", "#7FB8E8"][k]
        wall += (f'<g {C.kv(translate=[[0, 0, 0], [t_scroll, 0, rng.choice([-30, 30]), "lin"]])}>'
                 f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="7" stroke-linejoin="round" opacity=".85"/></g>')
        for r in range(1, 4):
            wall += f'<path d="M{sx + 20},{250 + r * sh_ / 4:.0f} L{sx + sw_ - 20},{250 + r * sh_ / 4:.0f}" stroke="#2A3244" stroke-width="2"/>'
    # pillars between the screens
    for px in (-420, 440, 1300, 2160):
        wall += f'<rect x="{px}" y="220" width="60" height="900" fill="#252D3D"/>'
    # the row of desks behind her, each with a bank of monitors (z .5)
    row = ""
    for dx in range(-1400, 3400, 330):
        row += _r(dx, 820, 300, 26, "#3A4152", rx=4, sw=3)
        for m in range(3):
            mx = dx + 14 + m * 94
            op = rng.uniform(.55, .9)
            row += (_r(mx, 700, 86, 64, "#10141C", rx=5, sw=2.4)
                    + f'<rect x="{mx + 6}" y="706" width="74" height="52" rx="3" fill="{rng.choice(["#1F4D47", "#24395A", "#3A2F4F"])}" opacity="{op:.2f}" '
                      f'data-flick=\'[{op:.2f},0.08,{rng.randint(0, 9)}]\'/>'
                    + f'<path d="M{mx + 10},{740 - rng.randint(0, 18)} L{mx + 30},{730 - rng.randint(0, 18)} L{mx + 52},{738 - rng.randint(0, 18)} L{mx + 76},{724 - rng.randint(0, 18)}" '
                      f'fill="none" stroke="{rng.choice(["#7BE08F", "#F2C35B", "#FF7A6B"])}" stroke-width="3"/>'
                    + _r(mx + 38, 764, 10, 56, "#2A2F3A", sw=1.6))
        row += f'<rect x="{dx}" y="846" width="300" height="200" fill="#2A303D" stroke="{INK}" stroke-width="3"/>'
    floor = ('<rect x="-2600" y="1040" width="7200" height="1600" fill="#4A5062"/>'
             + "".join(f'<path d="M{-2600 + k * 240},1040 L{-2600 + k * 240 - 340},2660" stroke="#343947" stroke-width="3"/>' for k in range(32)))
    hx = hero_x
    chair = (_r(hx - 120, 985, 170, 22, "#1E222B", rx=8) + _r(hx - 134, 790, 30, 215, "#1E222B", rx=12)
             + _r(hx - 43, 1007, 16, 50, "#5A5F6A", sw=2.4)
             + f'<path d="M{hx - 100},1058 L{hx + 30},1058" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    # the hero desk and its big monitor (screen 380 x 340, its lower edge just above the desk)
    sx, sy, sw_, sh_ = hx + 100, 540, 380, 340
    desk = (f'<ellipse cx="{sx + sw_ / 2}" cy="{sy + sh_ / 2}" rx="{sw_ * .9:.0f}" ry="{sh_ * .9:.0f}" fill="url(#tfGlow)" opacity=".5"/>'
            + _r(hx + 70, 925, 560, 26, "#4A5163", rx=6, sw=4) + _r(hx + 100, 951, 22, 110, "#2A2F3A", sw=3)
            + _r(hx + 580, 951, 22, 110, "#2A2F3A", sw=3)
            + _r(sx + sw_ / 2 - 16, sy + sh_, 32, 925 - sy - sh_, "#2A2F3A", sw=2.6) + _r(sx + sw_ / 2 - 80, 912, 160, 14, "#2A2F3A", rx=5, sw=2.6)
            + _r(sx - 16, sy - 16, sw_ + 32, sh_ + 32, "#10141C", rx=14, sw=4)
            + f'<rect x="{sx}" y="{sy}" width="{sw_}" height="{sh_}" fill="#F4EFE6"/>'
            + _r(hx + 110, 905, 200, 18, "#2A2F3A", rx=5, sw=2.4)          # keyboard
            + f'<g transform="translate({hx + 590},925) scale(.8)">{L.cup()}</g>')
    layers = dict(wall=(.3, wall), row=(.5, row), floor=(.6, floor), chair=(.72, chair), desk=(.86, desk))
    return layers, dict(hero_x=hx, ground=1060, screen=(sx, sy, sw_, sh_), desk_y=925)


def marker_text(tid, x, y, text, size, color, t0, t1, anchor="start", weight=700, family="Sans"):
    """Text written onto a board or a sheet as if by a marker: inked left to right between t0 and t1 (shot s)."""
    n = len(text)
    return (f'<text id="{tid}" x="{x}" y="{y}" font-family="\'{family}\',sans-serif" font-weight="{weight}" font-size="{size}" '
            f'text-anchor="{anchor}" fill="{color}" data-type=\'[[0,0],[{t0:.3f},0],[{t1:.3f},{n}]]\'>{text}</text>')


# ------------------------------------------------------------------------------------------------ film and checks

def follow_ask(at, d, top=1388):
    """The follow ask on screen (27 Nov), from shot second `at` (when "follow" is said) to the shot's end d: a round
    IB avatar, the handle and a + FOLLOW button that a tap ring presses 0.9 s later and that turns to FOLLOWING.
    It sits in the band above Instagram's own caption (screen y 1402 to about 1530), left of the button column, over
    the world with no box behind it."""
    from motion import A
    t_tap = round(at + .9, 3)
    btn = ("position:absolute;left:0;top:0;display:inline-block;font-family:'Sans',sans-serif;font-size:44px;font-weight:700;"
           "letter-spacing:.05em;color:#fff;padding:12px 40px;border-radius:16px;white-space:nowrap")
    button = ('<div style="position:relative;height:76px;margin-top:10px">'
              + A(f'<span style="{btn};background:{RED}">+ FOLLOW</span>', "life", 0, t_tap + .05, fi=.01, fo=.05)
              + A(f'<span style="{btn};background:#2A2E35;border:3px solid #fff">FOLLOWING</span>', "life", t_tap, 99, fi=.05, fo=.01,
                  style="position:absolute;left:0;top:0")
              + A('<span style="display:block;width:110px;height:110px;border-radius:50%;border:8px solid #fff"></span>', "ripple",
                  round(t_tap - .2, 3), .6, style="position:absolute;left:62px;top:-22px")
              + '</div>')
    avatar = (f'<div style="width:132px;height:132px;border-radius:50%;background:{INK};border:6px solid #fff;flex:none;'
              f'display:flex;align-items:center;justify-content:center;font-family:\'Serif\',serif;font-weight:700;font-size:60px;color:#fff">'
              f'IB<span style="color:{RED}">.</span></div>')
    handle = (f'<div style="font-family:\'Sans\',sans-serif;font-weight:700;font-size:42px;color:#fff;white-space:nowrap;'
              f'text-shadow:0 0 3px #000,0 2px 10px rgba(0,0,0,.95),0 6px 24px rgba(0,0,0,.7)">{HANDLE}</div>')
    row = f'<div style="display:flex;align-items:center;gap:22px">{avatar}<div>{handle}{button}</div></div>'
    return A(A(row, "pop", round(at, 3), .4), "life", 0, d, cls="fol",
             style=f"position:absolute;left:60px;top:{top}px;z-index:9", fi=.01, fo=.01)


def film(shots, caps, badge=""):
    if 'class="a fol' not in "".join(shots[-1].get("over", [])):
        raise SystemExit("REEL RULES: the last shot has no follow_ask() on screen (27 Nov: said and shown)")
    probs = check_shots(shots)
    if probs:
        raise SystemExit("REEL RULES: " + "; ".join(probs))
    return C.film_html(shots, W, H, caps=caps, mark=True, badge=badge)


def full_frame_check(pngs):
    """26 Nov: the whole frame is the picture. The 16 to 26 Nov format put a card on a dark, even ground, so its
    side strips (80 px each side, the middle of the frame) were dark and nearly uniform. A still fails if those
    strips are mostly dark (the ground) or more than 25% of the frame is near-black. Calibrated on both formats:
    every still of the 26 Nov 'points vs percent' Reel fails, every still of the first full-frame Reel passes
    (a whiteboard filling the frame is the world, not a card)."""
    from PIL import Image
    out = []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB")).astype(int)
        h, w = a.shape[:2]
        dark = float((a.max(axis=2) < 28).mean())
        strips = np.concatenate([a[int(h * .25):int(h * .75), :int(w * .074)], a[int(h * .25):int(h * .75), -int(w * .074):]], axis=1)
        side_dark = float((strips.max(axis=2) < 45).mean())
        out.append(dict(still=pathlib.Path(p).name, dark=round(dark, 3), side_dark=round(side_dark, 3), ok=dark < .25 and side_dark < .5))
    return out


def sound(work, slug, voice, b, events, room=True, lufs=-16.0):
    """Voice, a quiet room tone and the action-timed effects; one clean master at the Reel target. No music:
    Instagram adds the trending track at posting."""
    import sfx
    from master import Stems, dual
    from voice import MASTER
    st = Stems(b["total"])
    for m, s in zip(voice, b["starts"]):
        st.voice_at(m["wav"], s)
    if room:
        r = sfx.office_ambience(b["total"] + .6, seed=5, busy=.35, phones=0)
        st.add("amb", r * .55)
    st.add("foley", sfx.foley_track(events, b["total"]))
    script = " ".join(m["text"] for m in voice)
    return dual(st, work / f"{slug}-silent.mp4", work, slug, lufs=lufs, tp=-1.5, script=script, chain=MASTER,
                scored=False, foley_level_db=-20.0)
