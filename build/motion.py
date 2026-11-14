"""
Animated Reel renderer for @investmentbankinginterviews.

Same brand frame as reel.py (ink ground, Source Serif 4 and IBM Plex Sans,
IB mark, handle, progress bar, safe area), but every element can move. A
scene is plain HTML; elements marked with class "a" carry their animation in
data attributes, and one JavaScript function, seek(t), places every element
for time t. Playwright calls seek() once per frame and screenshots, so the
render is deterministic: the same input always gives the same video.

    data-fx   rise | fade | pop | wipe | growX | growY | growYdown | move | count | strike | coinflip (10 Nov: a coin spinning on its axis, data-turns)
              flipin | flipout | draw | float | words | roll | stamp | ripple | press
    words: children with class "w" appear one by one across data-d (typewriter by word)
    roll: slot-machine word swap; children of .rl are the options, data-hold between swaps
    float: data-amp (px), data-w (rad/s), data-ph (phase); always visible, drifts with t
    draw: on an svg with class "pen"; a hand-drawn loop is fitted to its parent at load
    scene keys: enter="right" slides the scene in, exit="left" slides it out
    data-at   start, seconds from the scene's start (negative = already in at t=0)
    data-d    duration in seconds
    data-from / data-to / data-dec / data-pre / data-suf   for count
    data-x / data-y                                         for move (start offset, px)
    data-show=1                                             count is visible before it starts
    chars: children .c reveal one by one out of a blur (data-st stagger, data-cd per char)
    spin: rotates continuously at data-deg degrees per second
    swing: pendulum rotation (data-amp degrees, data-w rad/s, data-ph), for walking limbs; data-gate=1 swings only
           from data-at for data-d seconds, easing in and out over 0.22 s (14 Nov: a walk that starts and stops)
    count: data-lin=1 counts linearly, data-pad=N zero-pads to N digits
    kara: karaoke captions; children .w light up at data-t seconds after data-at (data-c colour);
          data-hide=1 keeps words invisible until spoken (answers)
    pass: whip in from the right and out to the left with blur over data-fi / data-fo (0 = none; data-out=fade)
    shrinkX: a bar that empties left to right over data-d (think timers)
    kf: keyframes data-kf=[[t,x,y,scale,opacity,rot],...] in scene seconds, eased between keys
    grain: film grain; a noise tile jittered every 1/24 s (data-op opacity)
    life: visible from data-at for data-d seconds, fading in and out (data-fi, data-fo)
    scale: data-s0 to data-s1, eased; set transform-origin in style
    slide: straight travel from data-x0,y0 to data-x1,y1 (linear unless data-ease), optional data-r spin
    Illustration layers inside an element with class "nochk" are skipped by the safe-area check.
    scene keys: enter right|whip|zoomin, exit left|whip|zoom, push (slow camera push-in, e.g. .05)
    page(theme='paper') gives the light ground used since the 3 Nov reference Reel

Rules carried over from the brand system:
- Safe area: nothing above y=230 or below y=1440, right 244px clear.
- Frame 0 is the cover, so the first scene's text is fully in at t=0.
- No audio stream here; sound is added after (sfx.py for effects, voice.py for voice),
  and Pietro adds a trending track in the app.
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
@font-face{font-family:'Serif';src:url('FONTS/serif400i.woff2') format('woff2');font-weight:400;font-style:italic}
@font-face{font-family:'Serif';src:url('FONTS/serif600i.woff2') format('woff2');font-weight:600;font-style:italic}
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
.roll{display:inline-block;vertical-align:top;overflow:hidden;height:1.3em;border-radius:10px;background:rgba(94,200,180,.28);padding:0 .18em;box-sizing:content-box}
.rl{display:flex;flex-direction:column}.rl>span{display:block;height:1.3em;line-height:1.3em;white-space:nowrap}
.c{display:inline-block;white-space:pre}.wd{display:inline-block;white-space:nowrap}
.it{font-family:'Serif',serif;font-style:italic;font-weight:400;letter-spacing:-.01em}
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
  // 12 Nov: thousands separators from 10,000 up (years and small counts stay as they are)
  let t = v.toFixed(dec);
  if (!el.dataset.nosep && Math.abs(v) >= (el.dataset.sep ? 1000 : 10000))   // data-sep=1: from 1,000 (13 Nov)
  { const [i, f] = t.split('.'); t = i.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (f ? '.' + f : ''); }
  return (el.dataset.pre || '') + t + (el.dataset.suf || '');
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
  else if (fx === 'count') { o = el.dataset.show ? 1 : clamp(raw*4); const q = el.dataset.lin ? raw : E.inout(raw);
      const v = +el.dataset.from + (+el.dataset.to - +el.dataset.from)*q;
      el.textContent = el.dataset.pad ? (el.dataset.pre || '') + String(el.dataset.ceil ? Math.ceil(v - 1e-6) : Math.round(v)).padStart(+el.dataset.pad, '0') + (el.dataset.suf || '')
                                      : fmt(v, el); }
  else if (fx === 'beat') { const k = local - at;
      const n = +(el.dataset.n || 1), ph = k - Math.floor(k);
      const on = k >= 0 && k < n; tf = `scale(${1 + (on ? .14 * Math.exp(-ph * 7) : 0)})`; }
  else if (fx === 'kara') { const pre = el.dataset.hide ? 0 : .32; el.querySelectorAll('.w').forEach(w => {
      const k = clamp((local - at - +(w.dataset.t || 0)) / (el.dataset.hide ? .14 : .001));
      w.style.opacity = pre + (1 - pre) * k; w.style.color = k > 0 ? (w.dataset.c || '') : '';
      if (el.dataset.hide) w.style.transform = `translateY(${(1 - E.out3(k)) * 14}px)`; }); }
  else if (fx === 'pass') { const fi = +(el.dataset.fi ?? .34), fo = +(el.dataset.fo ?? .34);
      // whip in from the right and out to the left, with motion blur; data-out="fade" fades instead
      const a = fi > 0 ? E.inout(clamp((local - at) / fi)) : 1, b = fo > 0 ? E.inout(clamp((local - (at + d - fo)) / fo)) : 0;
      o = local < at || local > at + d ? 0 : 1;
      const fade = el.dataset.out === 'fade';
      if (fade) o *= 1 - b;
      const x = (1 - a) * 1000 - (fade ? 0 : b * 1000), bl = (1 - a) * 26 + (fade ? 0 : b * 26);
      tf = `translate(${x}px,0)`; el.style.filter = bl > .3 ? `blur(${bl}px)` : 'none'; }
  else if (fx === 'shrinkX') { tf = `scaleX(${1 - raw})`; el.style.transformOrigin = 'left center'; }
  else if (fx === 'kf') { const k = el._kf || (el._kf = JSON.parse(el.dataset.kf)); let i = 0;
      while (i < k.length - 2 && local >= k[i + 1][0]) i++;
      const a = k[i], b = k[Math.min(i + 1, k.length - 1)];
      const q = b[0] > a[0] ? E.inout(clamp((local - a[0]) / (b[0] - a[0]))) : 1;
      const L = (j, dflt) => (a[j] ?? dflt) + ((b[j] ?? dflt) - (a[j] ?? dflt)) * q;
      tf = `translate(${L(1, 0)}px,${L(2, 0)}px) scale(${L(3, 1)}) rotate(${L(5, 0)}deg)`; o = L(4, 1); }
  else if (fx === 'grain') { const f = Math.floor(local * (+(el.dataset.fps || 24))), r = (n) => ((Math.sin(f * 12.9898 + n * 78.233) * 43758.5453) % 1 + 1) % 1;
      tf = `translate(${-r(1) * 200}px,${-r(2) * 200}px)`; o = +(el.dataset.op || .07); }
  else if (fx === 'life') { const fi = +(el.dataset.fi || .3), fo = +(el.dataset.fo || .3);
      const a = clamp((local - at) / fi), b = clamp((at + d - local) / fo); o = Math.min(a, b);
      tf = `translateY(${(1 - E.out3(a)) * 26}px)`; }
  else if (fx === 'scale') { const q = E.inout(raw), s0 = +(el.dataset.s0 || 1), s1 = +(el.dataset.s1 || 1);
      tf = `scale(${s0 + (s1 - s0) * q})`; }
  else if (fx === 'strike') { tf = `scaleX(${E.inout(raw)})`; el.style.transformOrigin = 'left center'; }
  else if (fx === 'flipin') { const q = E.out3(raw); o = raw > 0 ? 1 : 0; tf = `perspective(700px) rotateX(${(1-q)*-90}deg)`; }
  else if (fx === 'flipout') { const q = E.inout(raw); o = raw < 1 ? 1 : 0; tf = `perspective(700px) rotateX(${q*90}deg)`; }
  else if (fx === 'words') { const ws = el.querySelectorAll('.w'), n = ws.length;
      const shown = local < at ? 0 : Math.ceil(raw * n - 1e-6);
      ws.forEach((w, i) => { w.style.opacity = i < shown ? 1 : 0; }); }
  else if (fx === 'roll') { const kids = el._kids; if (kids) { const hold = +(el.dataset.hold||.9), tr = .32;
      let pos = 0; for (let i = 0; i < kids.length - 1; i++) pos += E.inout(clamp((local - at - i*hold) / tr));
      const i0 = Math.floor(pos), f = pos - i0, i1 = Math.min(i0 + 1, kids.length - 1);
      el.querySelector('.rl').style.transform = `translateY(${-pos * el._h}px)`;
      el.style.width = (el._w[i0] + (el._w[i1] - el._w[i0]) * f) + 'px'; } }
  else if (fx === 'stamp') { const q = E.out3(raw); o = clamp(raw*2.5);
      tf = `rotate(${(+(el.dataset.rot||-8)) - (1-q)*7}deg) scale(${1 + (1-q)*1.3})`; }
  else if (fx === 'ripple') { o = raw > 0 && raw < 1 ? (1-raw)*.55 : 0; tf = `scale(${.2 + 2.8*E.out3(raw)})`; }
  else if (fx === 'press') { tf = `scale(${1 - .08*Math.sin(Math.PI*raw)})`; }
  else if (fx === 'chars') { const cs = el.querySelectorAll('.c'), st = +(el.dataset.st||.035), cd = +(el.dataset.cd||.38);
      cs.forEach((c, i) => { const q = E.out3(clamp((local - at - i*st) / cd));
        c.style.opacity = q; c.style.filter = q < 1 ? `blur(${(1-q)*12}px)` : 'none';
        c.style.transform = `translateY(${(1-q)*22}px)`; }); }
  else if (fx === 'swing') { const a = +(el.dataset.amp||16), w = +(el.dataset.w||7), ph = +(el.dataset.ph||0);
      const g = el.dataset.gate ? clamp((local - at) / .22) * clamp((at + d - local) / .22) : 1;
      tf = `rotate(${Math.sin(local*w + ph)*a*g}deg)`; }
  else if (fx === 'slide') { const q = el.dataset.ease === 'inout' ? E.inout(raw) : el.dataset.ease === 'out' ? E.out3(raw) : raw;
      const x0 = +(el.dataset.x0||0), x1 = +(el.dataset.x1||0), y0 = +(el.dataset.y0||0), y1 = +(el.dataset.y1||0);
      tf = `translate(${x0 + (x1-x0)*q}px,${y0 + (y1-y0)*q}px)` + (el.dataset.r ? ` rotate(${q * +el.dataset.r}deg)` : ''); }
  else if (fx === 'coinflip') { const k = Math.max(0, local - at), turns = +(el.dataset.turns || 3);
      const sx = Math.cos(turns * 2 * Math.PI * E.out3(clamp(k / d))); o = local >= at ? 1 : 0;
      tf = `scaleX(${Math.abs(sx) < .05 ? .05 : sx})`; }
  else if (fx === 'spin') { tf = `rotate(${local * +(el.dataset.deg||40)}deg)`; }
  else if (fx === 'float') { const a = +(el.dataset.amp||10), w = +(el.dataset.w||1), ph = +(el.dataset.ph||0);
      tf = `translate(${Math.cos(local*w*.7+ph)*a*.6}px,${Math.sin(local*w+ph)*a}px)`; }
  else if (fx === 'draw') { const path = el.querySelector('path'); if (path) { const L = path.getTotalLength();
      path.style.strokeDasharray = L; path.style.strokeDashoffset = L*(1-(el.dataset.lin ? raw : E.inout(raw))); } o = raw > 0 ? 1 : 0; }
  el.style.opacity = o; if (tf) el.style.transform = tf;
}
window.initPens = function () {
  // Fit a hand-drawn loop around each .pen's parent: an ellipse that overshoots
  // its start, wobbles slightly and tilts, like a red pen circling a word.
  document.querySelectorAll('svg.pen').forEach((svg, k) => {
    const host = svg.parentElement.getBoundingClientRect();
    const padX = 34, padY = 26, W = host.width + 2*padX, H = host.height + 2*padY;
    svg.setAttribute('width', W); svg.setAttribute('height', H);
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    svg.style.cssText += `;position:absolute;left:${-padX}px;top:${-padY}px;overflow:visible;pointer-events:none`;
    const cx = W/2, cy = H/2, rx = W/2 - 8, ry = H/2 - 6, tilt = -0.05, pts = [];
    for (let i = 0; i <= 90; i++) {
      const a = Math.PI*1.08 + (i/90)*Math.PI*2.18;
      const wob = 1 + .035*Math.sin(3*a + k) + .025*(i/90);
      const x = Math.cos(a)*rx*wob, y = Math.sin(a)*ry*wob;
      pts.push([cx + x*Math.cos(tilt) - y*Math.sin(tilt), cy + x*Math.sin(tilt) + y*Math.cos(tilt)]);
    }
    const d = 'M' + pts.map(p => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' L');
    svg.innerHTML = `<path d="${d}" fill="none" stroke="${svg.dataset.c || '#D93A12'}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>`;
  });
};
window.initRolls = function () {
  document.querySelectorAll('.roll').forEach(el => {
    el._kids = [...el.querySelectorAll('.rl>span')];
    el._w = el._kids.map(k => { const r = document.createRange(); r.selectNodeContents(k); return r.getBoundingClientRect().width; });
    el._h = el._kids[0].getBoundingClientRect().height;
    el.style.width = el._w[0] + 'px';
  });
};
window.seek = function (t) {
  const scenes = window.SCENES, total = window.TOTAL;
  document.querySelector('.bar i').style.width = (100 * Math.min(t/total, 1)) + '%';
  const g = document.querySelector('.glow');
  g.style.left = (-260 + 140*Math.sin(t*.35)) + 'px';
  g.style.top = (380 + 160*Math.cos(t*.27)) + 'px';
  scenes.forEach((s, i) => {
    const el = document.getElementById('s' + i), local = t - s.start;
    const last = i === scenes.length - 1;
    const lead = ['right', 'whip', 'zoomin'].includes(s.enter) ? .3 : 0;   // arrive while the last scene leaves
    const on = local >= -lead && (local < s.dur || (last && local <= s.dur + 1));
    el.style.visibility = on ? 'visible' : 'hidden';
    if (!on) return;
    const exit = (last || s.exit === 'cut') ? 0 : clamp((local - (s.dur - .32)) / .32);   // 'cut' = hard cut
    const ent = lead ? E.inout(clamp((local + lead) / .32)) : 1;
    const e = E.inout(exit);
    const sf = el.querySelector('.safe');
    // A swipe moves the full width, in step with the neighbouring scene, and does not fade.
    const swipeOut = s.exit === 'left' || s.exit === 'whip', swipeIn = s.enter === 'right' || s.enter === 'whip';
    // The push-in is a camera move; the safe-area check measures the layout without it.
    let op = 1, sc = 1 + (window.NOPUSH ? 0 : (s.push || 0)) * clamp(local / s.dur), blur = 0;
    if (!swipeOut && s.exit !== 'zoom') op *= 1 - e;
    if (s.exit === 'zoom') { op *= 1 - e; sc *= 1 + 2.2*e; }
    if (s.enter === 'zoomin') { op *= ent; sc *= .35 + .65*ent; }
    if (s.enter === 'whip') blur += (1 - ent) * 26;
    if (s.exit === 'whip') blur += e * 26;
    sf.style.opacity = op;
    sf.style.filter = blur > .3 ? `blur(${blur}px)` : 'none';
    const dx = (swipeIn ? (1-ent)*1000 : 0) + (swipeOut ? -1000*e : 0);
    const dy = (swipeOut || s.exit === 'zoom') ? 0 : -38*e;
    sf.style.transform = `translate(${dx}px,${dy}px) scale(${sc})`;
    const gh = el.querySelector('.ghost');
    if (gh) gh.style.opacity = .055 * clamp(local / .6) * (1 - e);
    el.querySelectorAll('.a').forEach(a => place(a, local));
  });
};
window.fitSvg = function (svg, zmax, zmin) {
  // 12 Nov (ported from youtube.py): zoom the viewBox onto what is actually drawn, so a drawing fills its
  // box. Keeps the element's own shape (a 700 x 532 box gets a 700 x 532 view, not a letterboxed 800 x 640).
  if (svg.dataset.fit === 'no' || svg.dataset.fitted) return null;
  let b; try { b = svg.getBBox(); } catch (e) { return null; }
  if (!b.width || !b.height) return null;
  const vb = svg.viewBox.baseVal, ar = (+svg.getAttribute('width') || vb.width) / (+svg.getAttribute('height') || vb.height);
  const W = +svg.getAttribute('width') || vb.width, Hh = +svg.getAttribute('height') || vb.height;
  const fill0 = Math.min(b.width * Math.min(W / vb.width, Hh / vb.height) / W, 1.5);   // share of the box width drawn on, before
  const pad = 26;
  let x = b.x - pad, y = b.y - pad, w = b.width + 2 * pad, h = b.height + 2 * pad;
  if (w / h > ar) { const nh = w / ar; y -= (nh - h) / 2; h = nh; } else { const nw = h * ar; x -= (nw - w) / 2; w = nw; }
  const lim = (k) => { x -= (w * k - w) / 2; y -= (h * k - h) / 2; w *= k; h *= k; };
  if (w < vb.width / zmax) lim(vb.width / zmax / w);
  if (w > vb.width / zmin) lim(vb.width / zmin / w);
  svg.setAttribute('viewBox', `${x.toFixed(1)} ${y.toFixed(1)} ${w.toFixed(1)} ${h.toFixed(1)}`);
  svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  svg.dataset.fitted = (800 / w).toFixed(2);
  return {zoom: +(800 / w).toFixed(2), before: +fill0.toFixed(2), after: +Math.min(b.width / w, 1).toFixed(2)};
};
window.fitSketches = function (zmax = 1.5, zmin = .8) {
  // Each drawing is measured at the end of its own life (the nearest 'life' parent), when all of it is drawn.
  const out = [];
  window.SCENES.forEach((s, i) => {
    document.getElementById('s' + i).querySelectorAll('svg.sk').forEach(svg => {
      let end = s.dur - .05;
      for (let q = svg.parentElement; q; q = q.parentElement)
        if (q.classList && q.classList.contains('a') && q.dataset.fx === 'life') { end = Math.min(end, +q.dataset.at + +q.dataset.d - .12); break; }
      seek(s.start + end);
      const r = fitSvg(svg, zmax, zmin);
      if (r) out.push(r);
    });
  });
  seek(0);
  return out;
};
window.textRects = function (el) {
  // The rectangles of the words themselves (a block is full width; its words may not be).
  const out = [];
  el.querySelectorAll('.w').forEach(w => { const r = w.getBoundingClientRect(); if (r.width) out.push(r); });
  if (!out.length) { const rg = document.createRange(); rg.selectNodeContents(el); out.push(...rg.getClientRects()); }
  return out;
};
window.clearAfter = function () {
  // 13 Nov: a picture beside an answer (.aftr, levels.py art_after) must not sit on the answer's words.
  // At the level's settled moment (data-settle), each overlapping text block in the same answer is first
  // narrowed to end left of the picture (text-wrap:balance re-wraps it), then shrunk in 6% steps (to 70%);
  // if it still overlaps, the picture drops below the answer. Every move is reported, and anything
  // left overlapping is flagged by the render.
  const hit = (a, b, m = 14) => a.left < b.right + m && a.right + m > b.left && a.top < b.bottom + m && a.bottom + m > b.top;
  const out = [];
  document.querySelectorAll('.aftr').forEach((af, k) => {
    seek(+af.dataset.settle);
    const zone = af.parentElement;
    const blocks = [...zone.querySelectorAll('.ansbig, .ansline, .anschip')];
    const pic = () => { const r = (af.firstElementChild || af).getBoundingClientRect(); return r; };
    const over = () => blocks.filter(b => textRects(b).some(r => hit(r, pic())));
    const rep = {aftr: k, moves: []};
    for (let step = 0; step < 10 && over().length; step++) {
      const zr = zone.getBoundingClientRect(), room = pic().left - zr.left - 24;
      over().forEach(b => {
        const fs = parseFloat(getComputedStyle(b).fontSize);
        b.dataset.fs0 = b.dataset.fs0 || fs;
        const kind = b.className.match(/ans(big|line|chip)/)[0];
        // A big answer shrinks first (to 80%), since narrowing it can leave one word alone on a line;
        // lines and chips narrow first. Then either shrinks on, to 70%.
        if (kind === 'ansbig' && fs > .8 * b.dataset.fs0) { b.style.fontSize = (fs * .94).toFixed(1) + 'px'; }
        else if (!b.style.maxWidth) { b.style.maxWidth = room + 'px'; rep.moves.push(`${kind} narrowed to ${Math.round(room)} px`); }
        else if (fs > .7 * b.dataset.fs0) { b.style.fontSize = (fs * .94).toFixed(1) + 'px'; }
      });
    }
    let left = over();
    if (left.length) {                                         // still on top: the picture goes under the answer
      blocks.forEach(b => { b.style.maxWidth = ''; if (b.dataset.fs0) b.style.fontSize = b.dataset.fs0 + 'px'; });
      const bottom = Math.max(...blocks.map(b => b.getBoundingClientRect().bottom)) - zone.getBoundingClientRect().top;
      af.style.top = (bottom + 18) + 'px';
      rep.moves = [`picture dropped below the answer (top ${Math.round(bottom + 18)} px)`];
      left = over();
      if (pic().bottom > 1441) rep.moves.push('CHECK picture runs under the 1440 line');
    }
    blocks.forEach(b => { if (b.dataset.fs0 && parseFloat(b.style.fontSize) < b.dataset.fs0) rep.moves.push(`${b.className.match(/ans(big|line|chip)/)[0]} at ${b.style.fontSize} (was ${b.dataset.fs0}px)`); });
    rep.overlap = left.length;
    if (rep.moves.length || rep.overlap) out.push(rep);
  });
  seek(0);
  return out;
};
window.wordify = function () {
  // 14 Nov: blocks with plain text (chips) get word spans so the line check can see their words.
  // Unstyled inline spans do not change the layout.
  document.querySelectorAll('.olchk').forEach(b => {
    if (b.querySelector('.w')) return;
    const walk = document.createTreeWalker(b, NodeFilter.SHOW_TEXT);
    const nodes = []; while (walk.nextNode()) if (walk.currentNode.textContent.trim()) nodes.push(walk.currentNode);
    nodes.forEach(t => {
      const f = document.createDocumentFragment();
      t.textContent.split(/(\s+)/).forEach(x => {
        if (!x) return;
        if (/^\s+$/.test(x)) { f.appendChild(document.createTextNode(x)); return; }
        const sp = document.createElement('span'); sp.className = 'w ow'; sp.textContent = x; f.appendChild(sp);
      });
      t.parentNode.replaceChild(f, t);
    });
  });
};
window.lineWords = function (b) {
  // Words per rendered line, top to bottom (an explicit <br> line is the author's choice and is skipped).
  const tops = [];
  b.querySelectorAll('.w').forEach(w => { const r = w.getBoundingClientRect(); if (r.width) tops.push(Math.round(r.top / 8)); });
  const lines = [...new Set(tops)].sort((a, c) => a - c);
  return {n: tops.length, counts: lines.map(l => tops.filter(t => t === l).length), brs: b.querySelectorAll('br').length};
};
window.lone = function (b) {
  // 14 Nov: a single word alone on ANY line, not only the last ("Can shareholders' / equity / be negative?").
  const L = lineWords(b);
  if (L.n < 3 || L.counts.length < 2 || L.brs) return false;
  return L.counts.some(c => c === 1);
};
window.unorphan = function () {
  // 14 Nov: the hook question and the big answers (.olfix) re-balance themselves. A block with a word
  // alone on a line shrinks in 3% steps (to 85%) until every line has two words or more; the move is reported.
  const out = [];
  document.querySelectorAll('.scene').forEach(s => {
    if (s.style.visibility !== 'visible') return;
    s.querySelectorAll('.olfix').forEach(b => {
      if (b.dataset.unorph) return;
      if (!lone(b)) return;
      const fs0 = parseFloat(getComputedStyle(b).fontSize);
      let fs = fs0;
      while (lone(b) && fs > .85 * fs0) { fs *= .97; b.style.fontSize = fs.toFixed(1) + 'px'; }
      b.dataset.unorph = 1;
      out.push(`"${b.textContent.trim().slice(0, 50)}" ${Math.round(fs0)} to ${Math.round(fs)} px` + (lone(b) ? ' CHECK still a word alone' : ''));
    });
  });
  return out;
};
window.orphans = function () {
  // 13 Nov: any text block (.olchk) that wraps with a single word alone on its last line.
  // 14 Nov: on any line, and chips are checked too (wordify).
  const bad = [];
  document.querySelectorAll('.scene').forEach(s => {
    if (s.style.visibility !== 'visible') return;
    s.querySelectorAll('.olchk').forEach(b => {
      for (let q = b; q && q !== s; q = q.parentElement)            // hidden itself or inside something hidden
        if (getComputedStyle(q).opacity === '0') return;
      if (lone(b)) bad.push(`one word alone on a line (${lineWords(b).counts.join('/')} words per line): "${b.textContent.trim().slice(0, 60)}"`);
    });
  });
  return bad;
};
window.artText = function () {
  // 14 Nov: a drawing's ink over the words. The safe-area check skips drawings (.nochk), so a drawing that grew
  // or was refitted onto a caption went unnoticed (the PIN boxes over "But his wife said" on the first cut).
  // Every visible shape of every drawing (svg.sk) is tested against every visible text block (.olchk).
  const bad = [], vis = (n, stop) => { for (let q = n; q && q !== stop; q = q.parentElement)
    if (getComputedStyle(q).opacity === '0' || getComputedStyle(q).visibility === 'hidden') return false; return true; };
  document.querySelectorAll('.scene').forEach(s => {
    if (s.style.visibility !== 'visible') return;
    const caps = [...s.querySelectorAll('.olchk')].filter(c => vis(c, s)).map(c => [c, c.getBoundingClientRect()]);
    s.querySelectorAll('svg.sk').forEach(svg => {
      if (!vis(svg, s)) return;
      svg.querySelectorAll('rect,circle,ellipse,path,text,polygon,line').forEach(el => {
        if (!vis(el, svg.parentElement)) return;
        const r = el.getBoundingClientRect();
        if (r.width < 2 && r.height < 2) return;
        caps.forEach(([c, q]) => {
          const ox = Math.min(r.right, q.right) - Math.max(r.left, q.left), oy = Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top);
          if (ox > 6 && oy > 6) bad.push(`drawing <${el.tagName}> ${Math.round(r.left)},${Math.round(r.top)} over "${c.textContent.trim().slice(0, 40)}"`);
        });
      });
    });
  });
  return [...new Set(bad)].slice(0, 6);
};
window.check = function () {
  // Every visible text-bearing element must sit inside the safe area.
  const bad = [];
  document.querySelectorAll('.scene').forEach(s => {
    if (s.style.visibility !== 'visible') return;
    s.querySelectorAll('.safe *').forEach(n => {
      if (!n.childNodes.length || getComputedStyle(n).opacity === '0' || n.closest('.nochk')) return;
      for (let q = n.parentElement; q && q !== s; q = q.parentElement)      // inside something hidden
        if (getComputedStyle(q).opacity === '0') return;
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


PAPER_CSS = '.f{background:#F7F5F2;color:#0A0A0A}.t{color:#0F766E}.bar{background:rgba(10,10,10,.12)}.tag{opacity:.6}.glow{background:radial-gradient(closest-side,rgba(217,58,18,.07),rgba(217,58,18,0))}.lbl{opacity:.6}.ghost{color:#0A0A0A}'


def page(scenes, theme="ink"):
    starts, t = [], 0.0
    for s in scenes:
        starts.append({"start": round(t, 3), "dur": s["dur"], "push": s.get("push", 0),
                       "enter": s.get("enter", ""), "exit": s.get("exit", "")})
        t += s["dur"]
    body = "".join(
        f'<div class="scene" id="s{i}">'
        + (f'<div class="ghost">{s["ghost"]}</div>' if s.get("ghost") else "")
        + f'<div class="safe">{s["html"]}</div></div>'
        for i, s in enumerate(scenes))
    html = ("<!doctype html><html><head><meta charset='utf-8'><style>"
            + CSS.replace("FONTS/", f"{FONTS.resolve()}/") + (PAPER_CSS if theme == "paper" else "")
            + "</style></head><body>"
            + '<div class="f"><div class="glow"></div>'
            + f'<div class="mark">IB<span class="r">.</span></div>{body}'
            + f'<div class="tag">{HANDLE}</div><div class="bar"><i></i></div></div>'
            + f"<script>window.SCENES={json.dumps(starts)};window.TOTAL={t};{JS}</script>"
            + "</body></html>")
    return html, t, starts


def build(slug, scenes, theme="ink", cover_at=0.0, crf=18, check_at=(), fit=False):
    """Render to MP4. cover_at picks the cover frame, so a Reel can open on motion
    and still have a fully composed cover."""
    work = OUT / slug
    work.mkdir(parents=True, exist_ok=True)
    html, total, starts = page(scenes, theme)
    src = work / "motion.html"
    src.write_text(html)
    mp4 = work / f"{slug}.mp4"
    cover = work / f"{slug}-cover.jpg"
    n = int(round((total + 0.6) * FPS))      # hold the final frame briefly

    ff = subprocess.Popen([
        "ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(FPS),
        "-c:v", "mjpeg", "-i", "-", "-an",
        "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(mp4)], stdin=subprocess.PIPE)

    problems = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        pg.goto(src.resolve().as_uri())
        pg.evaluate("Promise.all([400, 500, 600].map(w => document.fonts.load(w + ' 40px Sans'))"
                    ".concat([document.fonts.load(\"700 40px 'Serif'\"), document.fonts.load(\"italic 400 40px 'Serif'\"),"
                    " document.fonts.load(\"italic 600 40px 'Serif'\")]))")
        pg.evaluate("initPens()")
        pg.evaluate("initRolls()")
        loaded = pg.evaluate("[...document.fonts].filter(f => f.status === 'loaded').length")
        if loaded < 6:
            raise RuntimeError(f"only {loaded} of 6 brand fonts loaded")
        if fit:                                  # 12 Nov: every drawing zoomed onto what is drawn
            fits = pg.evaluate("fitSketches()")
            if fits:
                (work / "fit.json").write_text(json.dumps(fits, indent=1))
                small = [k for k, r in enumerate(fits) if r["after"] < .85]
                print(f"  fitted {len(fits)} drawings: drawn width {min(r['before'] for r in fits):.2f}-{max(r['before'] for r in fits):.2f}"
                      f" of the box before, {min(r['after'] for r in fits):.2f}-{max(r['after'] for r in fits):.2f} after"
                      + (f"  CHECK under 85%: drawings {small}" if small else ""), flush=True)
        pg.evaluate("wordify()")
        # 14 Nov: the hook and the big answers re-balance before anything is checked or filmed.
        unorph = []
        for t in [s_["start"] + s_["dur"] - .4 for s_ in starts] + list(check_at):
            unorph += pg.evaluate(f"window.NOPUSH = true; seek({t}); unorphan()")
        for x in unorph:
            print("  re-balanced " + x)
        if unorph:
            (work / "unorphan.json").write_text(json.dumps(unorph, indent=1))
        # 13 Nov: pictures beside answers are moved clear of the words before anything is checked or filmed.
        cleared = pg.evaluate("window.NOPUSH = true; clearAfter()")
        if cleared:
            (work / "clear.json").write_text(json.dumps(cleared, indent=1))
            for r in cleared:
                print(f"  answer picture {r['aftr']}: " + "; ".join(r["moves"]) + (f"  CHECK still overlaps {r['overlap']} block(s)" if r["overlap"] else ""))
                if r["overlap"]:
                    problems.append(f"answer picture {r['aftr']} overlaps the answer text")
        # Layout check at the settled point of every scene.
        wraps = []
        for i, s in enumerate(starts):
            pg.evaluate(f"window.NOPUSH = true; seek({s['start'] + s['dur'] - .4})")
            problems += pg.evaluate("check()")
            problems += pg.evaluate("artText()")
            wraps += pg.evaluate("orphans()")
        for t in check_at:                       # extra settled moments inside long scenes
            pg.evaluate(f"window.NOPUSH = true; seek({t})")
            problems += [f"t={t:.1f} " + x for x in pg.evaluate("check()")]
            problems += [f"t={t:.1f} " + x for x in pg.evaluate("artText()")]
            wraps += [f"t={t:.1f} " + x for x in pg.evaluate("orphans()")]
        for x in dict.fromkeys(wraps):           # 13 Nov: a word alone on a line is flagged, not left to the eye
            print("  WRAP " + x)
        pg.evaluate("window.NOPUSH = false")
        for f in range(n):
            pg.evaluate(f"seek({f / FPS})")
            shot = pg.screenshot(type="jpeg", quality=93, clip={"x": 0, "y": 0, "width": 1080, "height": 1920})
            ff.stdin.write(shot)
            if f == int(round(cover_at * FPS)):
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
