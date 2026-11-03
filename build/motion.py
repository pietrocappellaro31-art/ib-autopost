"""
Animated Reel renderer for @investmentbankinginterviews.

Same brand frame as reel.py (ink ground, Source Serif 4 and IBM Plex Sans,
IB mark, handle, progress bar, safe area), but every element can move. A
scene is plain HTML; elements marked with class "a" carry their animation in
data attributes, and one JavaScript function, seek(t), places every element
for time t. Playwright calls seek() once per frame and screenshots, so the
render is deterministic: the same input always gives the same video.

    data-fx   rise | fade | pop | wipe | growX | growY | growYdown | move | count | strike
    data-at   start, seconds from the scene's start (negative = already in at t=0)
    data-d    duration in seconds
    data-from / data-to / data-dec / data-pre / data-suf   for count
    data-x / data-y                                         for move (start offset, px)
    data-show=1                                             count is visible before it starts

Rules carried over from the brand system:
- Safe area: nothing above y=230 or below y=1440, right 244px clear.
- Frame 0 is the cover, so the first scene's text is fully in at t=0.
- No audio stream: Pietro adds a trending track in the app.
"""

import json
import pathlib
import subprocess

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"
OUT = HERE / "out"
FPS = 30

INK, RED, TEAL, PAPER, WHITE = "#0A0A0A", "#D93A12", "#5EC8B4", "#F7F5F2", "#FFFFFF"
HANDLE = "@investmentbankinginterviews"

CSS = """
@font-face{font-family:'Serif';src:url('FONTS/serif700.woff2') format('woff2');font-weight:700}
@font-face{font-family:'Sans';src:url('FONTS/sans400.woff2') format('woff2');font-weight:400}
@font-face{font-family:'Sans';src:url('FONTS/sans500.woff2') format('woff2');font-weight:500}
@font-face{font-family:'Sans';src:url('FONTS/sans600.woff2') format('woff2');font-weight:600}
html,body{margin:0;padding:0;background:#0A0A0A}
.f{width:1080px;height:1920px;position:relative;overflow:hidden;background:#0A0A0A;color:#fff;
 font-family:'Sans',sans-serif}
.glow{position:absolute;width:1400px;height:1400px;border-radius:50%;
 background:radial-gradient(closest-side,rgba(94,200,180,.11),rgba(94,200,180,0));pointer-events:none}
.ghost{position:absolute;right:-30px;top:360px;font-family:'Serif',serif;font-weight:700;
 font-size:620px;line-height:1;letter-spacing:-.06em;color:#fff;opacity:0}
.mark{position:absolute;left:84px;top:132px;font-family:'Serif',serif;font-weight:700;
 font-size:52px;letter-spacing:-.03em;z-index:5}
.tag{position:absolute;left:84px;bottom:300px;font-size:34px;font-weight:600;opacity:.75;z-index:5}
.bar{position:absolute;left:84px;right:244px;bottom:240px;height:8px;border-radius:4px;
 background:rgba(255,255,255,.18);z-index:5}
.bar i{display:block;height:8px;border-radius:4px;background:#D93A12;width:0}
.scene{position:absolute;inset:0;visibility:hidden}
.safe{position:absolute;left:84px;right:244px;top:230px;bottom:480px;
 display:flex;flex-direction:column;justify-content:center}
h1{margin:0;font-family:'Serif',serif;font-weight:700;line-height:1.03;letter-spacing:-.03em;
 font-size:104px}
.sub{font-size:44px;line-height:1.3;font-weight:500;margin-top:30px}
.t{color:#5EC8B4} .r{color:#D93A12}
.a{will-change:transform,opacity}
.card{background:rgba(255,255,255,.07);border:3px solid rgba(255,255,255,.22);
 border-radius:22px;padding:24px 32px;margin-top:44px}
.row{display:flex;justify-content:space-between;align-items:baseline;padding:18px 0;
 border-bottom:1px solid rgba(255,255,255,.14);font-size:42px;font-weight:500}
.row:last-child{border-bottom:0}
.row b{font-family:'Serif',serif;font-weight:700;font-size:52px}
.num{font-family:'Serif',serif;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.lbl{font-size:30px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;opacity:.7}
"""

JS = r"""
const E = {
  out3: p => 1 - Math.pow(1 - p, 3),
  inout: p => p < .5 ? 4*p*p*p : 1 - Math.pow(-2*p + 2, 3) / 2,
  back: p => { const c = 1.70158, c3 = c + 1; return 1 + c3*Math.pow(p-1,3) + c*Math.pow(p-1,2); },
};
const clamp = v => Math.max(0, Math.min(1, v));
function fmt(v, el) {
  const dec = +(el.dataset.dec || 0);
  return (el.dataset.pre || '') + v.toFixed(dec) + (el.dataset.suf || '');
}
function place(el, local) {
  const at = +(el.dataset.at || 0), d = +(el.dataset.d || .5);
  const raw = clamp((local - at) / d);
  const fx = el.dataset.fx;
  const p = E.out3(raw);
  let o = 1, tf = '';
  if (fx === 'rise') { o = p; tf = `translateY(${(1-p)*46}px)`; }
  else if (fx === 'fade') { o = p; }
  else if (fx === 'pop') { const q = E.back(raw); o = clamp(raw*3); tf = `scale(${.55 + .45*q})`; }
  else if (fx === 'wipe') { el.style.clipPath = `inset(-20px ${(1-E.inout(raw))*100}% -20px -20px)`; }
  else if (fx === 'growX') { tf = `scaleX(${E.inout(raw)})`; el.style.transformOrigin = 'left center'; }
  else if (fx === 'growY') { tf = `scaleY(${E.inout(raw)})`; el.style.transformOrigin = 'center bottom'; }
  else if (fx === 'growYdown') { tf = `scaleY(${E.inout(raw)})`; el.style.transformOrigin = 'center top'; }
  else if (fx === 'move') { const q = E.inout(raw); tf = `translate(${(1-q)*(+el.dataset.x||0)}px,${(1-q)*(+el.dataset.y||0)}px)`; }
  else if (fx === 'count') { o = el.dataset.show ? 1 : clamp(raw*4); const q = E.inout(raw);
      el.textContent = fmt(+el.dataset.from + (+el.dataset.to - +el.dataset.from)*q, el); }
  else if (fx === 'strike') { tf = `scaleX(${E.inout(raw)})`; el.style.transformOrigin = 'left center'; }
  el.style.opacity = o; if (tf) el.style.transform = tf;
}
window.seek = function (t) {
  const scenes = window.SCENES, total = window.TOTAL;
  document.querySelector('.bar i').style.width = (100 * Math.min(t/total, 1)) + '%';
  const g = document.querySelector('.glow');
  g.style.left = (-260 + 140*Math.sin(t*.35)) + 'px';
  g.style.top = (380 + 160*Math.cos(t*.27)) + 'px';
  scenes.forEach((s, i) => {
    const el = document.getElementById('s' + i), local = t - s.start;
    const last = i === scenes.length - 1;
    const on = local >= 0 && (local < s.dur || (last && local <= s.dur + 1));
    el.style.visibility = on ? 'visible' : 'hidden';
    if (!on) return;
    const exit = last ? 0 : clamp((local - (s.dur - .32)) / .32);
    const e = E.inout(exit);
    el.querySelector('.safe').style.opacity = 1 - e;
    el.querySelector('.safe').style.transform = `translateY(${-38*e}px)`;
    const gh = el.querySelector('.ghost');
    if (gh) gh.style.opacity = .055 * clamp(local / .6) * (1 - e);
    el.querySelectorAll('.a').forEach(a => place(a, local));
  });
};
window.check = function () {
  // Every visible text-bearing element must sit inside the safe area.
  const bad = [];
  document.querySelectorAll('.scene').forEach(s => {
    if (s.style.visibility !== 'visible') return;
    s.querySelectorAll('.safe *').forEach(n => {
      if (!n.childNodes.length || getComputedStyle(n).opacity === '0') return;
      const r = n.getBoundingClientRect();
      if (r.width === 0) return;
      if (r.left < 83 || r.right > 837 || r.top < 229 || r.bottom > 1441)
        bad.push(`${s.id} <${n.tagName.toLowerCase()} class="${n.className}"> ${Math.round(r.left)},${Math.round(r.top)} to ${Math.round(r.right)},${Math.round(r.bottom)}`);
    });
  });
  return bad;
};
"""


def A(html, fx="rise", at=0.0, d=0.5, cls="", style="", **data):
    """An animated element."""
    attrs = "".join(f' data-{k}="{v}"' for k, v in data.items())
    st = f' style="{style}"' if style else ""
    return f'<div class="a {cls}" data-fx="{fx}" data-at="{at}" data-d="{d}"{attrs}{st}>{html}</div>'


def page(scenes):
    starts, t = [], 0.0
    for s in scenes:
        starts.append({"start": round(t, 3), "dur": s["dur"]})
        t += s["dur"]
    body = "".join(
        f'<div class="scene" id="s{i}">'
        + (f'<div class="ghost">{s["ghost"]}</div>' if s.get("ghost") else "")
        + f'<div class="safe">{s["html"]}</div></div>'
        for i, s in enumerate(scenes))
    html = ("<!doctype html><html><head><meta charset='utf-8'><style>"
            + CSS.replace("FONTS/", f"{FONTS.resolve()}/") + "</style></head><body>"
            + '<div class="f"><div class="glow"></div>'
            + f'<div class="mark">IB<span class="r">.</span></div>{body}'
            + f'<div class="tag">{HANDLE}</div><div class="bar"><i></i></div></div>'
            + f"<script>window.SCENES={json.dumps(starts)};window.TOTAL={t};{JS}</script>"
            + "</body></html>")
    return html, t, starts


def build(slug, scenes):
    work = OUT / slug
    work.mkdir(parents=True, exist_ok=True)
    html, total, starts = page(scenes)
    src = work / "motion.html"
    src.write_text(html)
    mp4 = work / f"{slug}.mp4"
    cover = work / f"{slug}-cover.jpg"
    n = int(round((total + 0.6) * FPS))      # hold the final frame briefly

    ff = subprocess.Popen([
        "ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(FPS),
        "-c:v", "mjpeg", "-i", "-", "-an",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(mp4)], stdin=subprocess.PIPE)

    problems = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        pg.goto(src.resolve().as_uri())
        pg.evaluate("document.fonts.ready")
        loaded = pg.evaluate("[...document.fonts].filter(f => f.status === 'loaded').length")
        if loaded < 4:
            raise RuntimeError(f"only {loaded} of 4 brand fonts loaded")
        # Layout check at the settled point of every scene.
        for i, s in enumerate(starts):
            pg.evaluate(f"seek({s['start'] + s['dur'] - .4})")
            problems += pg.evaluate("check()")
        for f in range(n):
            pg.evaluate(f"seek({f / FPS})")
            shot = pg.screenshot(type="jpeg", quality=93, clip={"x": 0, "y": 0, "width": 1080, "height": 1920})
            ff.stdin.write(shot)
            if f == 0:
                cover.write_bytes(shot)
        browser.close()
    ff.stdin.close()
    ff.wait()
    if problems:
        print("SAFE-AREA PROBLEMS:\n  " + "\n  ".join(problems))
    probe = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=width,height",
         "-of", "json", str(mp4)], capture_output=True, text=True, check=True).stdout)
    print(f"  -> {mp4.name}  {float(probe['format']['duration']):.1f}s  "
          f"{int(probe['format']['size']) // 1024}KB  {n} frames  silent")
    return mp4, cover, problems
