"""
Cinematic 2D engine (13 Nov 2026, Pietro's cinematic-upgrade directive).

The channel's earlier engine (youtube.py, levels.py, sketch.py) draws a picture beside a line of text. This
module films scenes instead: an illustrated world in depth layers, a camera that moves through it, people
with joints who walk, sit, read, reach, point and react, objects that are handled, light that changes, and
transitions motivated by things in the scene. It runs on the same deterministic machinery as motion.py
(HTML + SVG, one seek(t) per frame, Playwright screenshots piped to FFmpeg), so a frame is always the same
for the same input, and every motion.py effect (count, draw, kara, stamp, ...) still works inside a shot.
Remotion was considered and not adopted: it is the same idea (a browser renders frames) with a second
toolchain, a React rewrite of every existing scene and a company-licence question; see
docs/production/animation-engine.md.

A film is a list of shots. A shot is

    dict(dur=6.0,                                   seconds
         layers=[layer(z, svg_or_html), ...],       the world, far (z near 0) to near (z > 1)
         actors=[actor(...)],                       rigged people (rig() / actor())
         cam=[[t, cx, cy, zoom], ...],              camera keys in shot seconds (world px, depth-1 plane)
         focus=[[t, z], ...], dof=7,                depth of field: blur grows with |z - focus|
         over=[html],                               screen-space overlays (labels, titles), motion.py fx
         grade="warm" | dict(color, op), tin=("cut" | "dissolve" | "flash" | "iris", seconds),
         shake=0.6)                                 subtle handheld drift, px

World coordinates: the depth-1 plane is 1920 x 1080 at zoom 1. A layer at depth z moves z times as far as
that plane when the camera pans (parallax) and is magnified 1 + (zoom - 1) * z when it zooms. A vertical
(9:16) film uses the same world: stage() fits the world's height to the frame, so one scene serves the long
video and the Short.

People: rig(look) builds an articulated SVG figure (hip root; torso, head, two arms of two segments with a
hand, two legs of two segments with a shoe) in one of the LOOKS (18th-century coats and wigs, modern suits).
actor(id, look, pos=[[t, x, y], ...], pose=[[t, POSE or dict], ...], turn=[...]) animates it. Between
position keys the figure walks: its legs, arms and body bob follow a gait cycle whose phase comes from the
distance travelled, so the feet do not skate, and footstep times can be read back for the sound
(footsteps()). Poses blend smoothly; the face has brows, mouth shapes and blinks; breathing never stops.

    python3 build/cine_poc_newton.py        the proof of concept (Newton buys back in, June 1720)
"""

import base64
import io
import json
import math
import pathlib
import random
import subprocess

import numpy as np

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"
OUT = HERE / "out"

RED, TEAL, INK, PAPER, MUSTARD = "#D93A12", "#0F766E", "#0A0A0A", "#F7F5F2", "#F2C35B"
W0, H0 = 1920, 1080                       # the world's reference frame
LEG = 82 + 78                             # thigh + shin, rig units
HIP_H = LEG + 10                          # hip height above the ground when standing

# ----------------------------------------------------------------------------------------------- runtime

CSS = """
@font-face{font-family:'Serif';src:url('FONTS/serif700.woff2') format('woff2');font-weight:700}
@font-face{font-family:'Serif';src:url('FONTS/serif400i.woff2') format('woff2');font-weight:400;font-style:italic}
@font-face{font-family:'Serif';src:url('FONTS/serif600i.woff2') format('woff2');font-weight:600;font-style:italic}
@font-face{font-family:'Sans';src:url('FONTS/sans400.woff2') format('woff2');font-weight:400}
@font-face{font-family:'Sans';src:url('FONTS/sans500.woff2') format('woff2');font-weight:500}
@font-face{font-family:'Sans';src:url('FONTS/sans600.woff2') format('woff2');font-weight:600}
html,body{margin:0;padding:0;background:#0A0A0A}
.f{position:relative;overflow:hidden;background:#0A0A0A;font-family:'Sans',sans-serif;color:#0A0A0A}
.shot{position:absolute;inset:0;visibility:hidden;overflow:hidden}
.world{position:absolute;left:0;top:0;transform-origin:0 0}
.layer{position:absolute;left:0;top:0;transform-origin:0 0;will-change:transform,filter}
.layer>svg{position:absolute;left:0;top:0;overflow:visible}
.over{position:absolute;inset:0;pointer-events:none}
.grade{position:absolute;inset:0;pointer-events:none}
.vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 55%,rgba(20,10,0,.38) 100%)}
.grain{position:absolute;left:-200px;top:-200px;right:-200px;bottom:-200px;pointer-events:none;mix-blend-mode:overlay}
.flash{position:absolute;inset:0;pointer-events:none;background:#FFF4DC;opacity:0}
.a{will-change:transform,opacity}
.mark{position:absolute;font-family:'Serif',serif;font-weight:700;z-index:9;color:#F7F5F2;text-shadow:0 2px 10px rgba(0,0,0,.35)}
.badge{position:absolute;font-family:'Sans',sans-serif;font-weight:600;letter-spacing:.16em;text-transform:uppercase;
 color:#F7F5F2;background:rgba(10,10,10,.55);border-radius:6px;z-index:9}
.cap{position:absolute;left:0;right:0;text-align:center;z-index:9;pointer-events:none}
.cap span.line{display:inline-block;font-family:'Sans',sans-serif;font-weight:600;color:#F7F5F2;
 background:rgba(10,10,10,.62);border-radius:10px;line-height:1.3}
.cap .w{opacity:.45}
.title{position:absolute;z-index:9;color:#F7F5F2;text-shadow:0 3px 18px rgba(0,0,0,.45)}
.title .k{font-family:'Sans',sans-serif;font-weight:600;letter-spacing:.22em;text-transform:uppercase;opacity:.9}
.title .h{font-family:'Serif',serif;font-weight:700;letter-spacing:-.02em;line-height:1.02}
.num{font-family:'Serif',serif;font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.hand{font-family:'Serif',serif;font-style:italic;font-weight:400}
"""

RUNTIME = r"""
const CE = {
  lin: p => p,
  inout: p => p < .5 ? 4*p*p*p : 1 - Math.pow(-2*p + 2, 3) / 2,
  sine: p => -(Math.cos(Math.PI*p) - 1) / 2,
  out: p => 1 - Math.pow(1 - p, 3),
  in: p => p*p*p,
  hold: p => 0,
};
const cl = v => Math.max(0, Math.min(1, v));
// keys: [[t, v1, v2, ..., (ease name)], ...] -> [v1, v2, ...] at time t (ease belongs to the segment it ends)
function keyed(keys, t) {
  if (!keys || !keys.length) return null;
  const strip = k => typeof k[k.length - 1] === 'string' ? k.slice(1, -1) : k.slice(1);
  if (t <= keys[0][0]) return strip(keys[0]);
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i], b = keys[i + 1];
    if (t < b[0]) {
      const en = typeof b[b.length - 1] === 'string' ? b[b.length - 1] : 'inout';
      const q = CE[en](cl((t - a[0]) / Math.max(b[0] - a[0], 1e-6)));
      const va = strip(a), vb = strip(b);
      return va.map((v, j) => v + (vb[j] - v) * q);
    }
  }
  return strip(keys[keys.length - 1]);
}
// pose keys: [[t, {field: value}, (ease)], ...]; fields missing from a key keep the base pose
function posed(keys, t, base) {
  const out = Object.assign({}, base);
  if (!keys || !keys.length) return out;
  const full = keys.map(k => Object.assign({}, base, k[1]));
  if (t <= keys[0][0]) return Object.assign(out, full[0]);
  for (let i = 0; i < keys.length - 1; i++) {
    if (t < keys[i + 1][0]) {
      const en = keys[i + 1][2] || 'inout';
      const q = CE[en](cl((t - keys[i][0]) / Math.max(keys[i + 1][0] - keys[i][0], 1e-6)));
      for (const f in out) out[f] = full[i][f] + (full[i + 1][f] - full[i][f]) * q;
      return out;
    }
  }
  return Object.assign(out, full[full.length - 1]);
}
const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
function noise1(x, seed) {                        // smooth value noise, -1..1
  const i = Math.floor(x), f = x - i, u = f*f*(3 - 2*f);
  return (hash(i + seed*17.3) * (1 - u) + hash(i + 1 + seed*17.3) * u) * 2 - 1;
}

// ---- actors -------------------------------------------------------------------------------------
const BASE = {lean: 0, head: 0, shF: 4, elF: 8, shB: -4, elB: 8, hipF: 2, knF: -3, hipB: -2, knB: -3,
              ftF: 0, ftB: 0, rootY: 0, brow: 0, mouth: 0, eyeY: 0, walkAmp: 1};
function distAt(pos, t) {                          // distance walked along x up to t
  let d = 0;
  for (let i = 0; i < pos.length - 1; i++) {
    const a = pos[i], b = pos[i + 1];
    if (t <= a[0]) break;
    const x = t >= b[0] ? b[1] : keyed([a, b], t)[0];
    d += Math.abs(x - a[1]);
  }
  return d;
}
function poseActor(A, t) {
  const R = A._r || (A._r = (() => {
    const g = document.getElementById(A.id), q = s => g.querySelector(s);
    return {g, root: q('.root'), torso: q('.torso'), head: q('.head'), tail: q('.tail'),
            shF: q('.shF'), elF: q('.elF'), shB: q('.shB'), elB: q('.elB'),
            hipF: q('.hipF'), knF: q('.knF'), hipB: q('.hipB'), knB: q('.knB'), ftF: q('.ftF'), ftB: q('.ftB'),
            eye: q('.eye'), brow: q('.brow'), mouths: [...g.querySelectorAll('.mouth')], shadow: q('.shadow'),
            breath: q('.breath'), holdF: q('.holdF'), holdB: q('.holdB')};
  })());
  const tl = t - (A.t0 || 0);
  const p = keyed(A.pos, tl) || [0, 0];
  const o = posed(A.pose, tl, BASE);
  // walking: weight from speed, phase from distance
  const dt = .06, pa = keyed(A.pos, tl - dt), pb = keyed(A.pos, tl + dt);
  const v = pa && pb ? Math.abs(pb[0] - pa[0]) / (2*dt) : 0;
  const w = cl(v / (A.vfull || 70)) * (A.walk === false ? 0 : 1);
  const ph = (distAt(A.pos, tl) / A.stride) * 2 * Math.PI + (A.ph || 0);
  const amp = (A.amp || 24) * o.walkAmp, s = Math.sin(ph), c = Math.cos(ph);
  const sw = (x) => Math.pow(Math.max(0, x), 1.4);
  const walk = {hipF: amp*s, hipB: -amp*s, knF: -(5 + 44*sw(c)), knB: -(5 + 44*sw(-c)),
                ftF: 10*sw(c) - 6*sw(-c), ftB: 10*sw(-c) - 6*sw(c),
                shF: -amp*.8*s, shB: amp*.8*s, elF: 14 + 8*sw(-s), elB: 14 + 8*sw(s), lean: 4};
  for (const f in walk) o[f] = o[f] + (walk[f] - (f === 'lean' ? 0 : o[f])) * w * (f === 'lean' ? 1 : 1);
  const bob = (-5*Math.cos(2*ph)) * w;
  // facing: turn keys pass through zero (a quick flat turn)
  const dir = A.turn ? keyed(A.turn, tl)[0] : (A.dir || 1);
  const sc = A.scale || 1;
  const sx = Math.abs(dir) < .06 ? .06 * Math.sign(dir || 1) : dir;
  // idle life: breath, head drift, blink, small weight shift
  const sd = A.seed || 1;
  const breath = Math.sin(tl * 1.9 + sd) * .5 + .5;
  const headDrift = 1.6*noise1(tl*.45, sd) + o.head;
  const sway = 1.2*noise1(tl*.3, sd + 3) * (1 - w);
  const hipY = -HIP + o.rootY + bob;
  R.root.setAttribute('transform', `translate(${p[0]},${p[1]}) scale(${sx*sc},${sc})`);
  R.torso.setAttribute('transform', `translate(0,${hipY}) rotate(${o.lean + sway})`);
  if (R.breath) R.breath.setAttribute('transform', `translate(0,-75) scale(${1 + .006*breath},${1 + .012*breath}) translate(0,75)`);
  R.head.setAttribute('transform', `translate(0,-158) rotate(${headDrift})`);
  const J = (el, x, y, a) => el && el.setAttribute('transform', `translate(${x},${y}) rotate(${-a})`);
  J(R.shF, 7, -134, o.shF); J(R.elF, 0, 66, o.elF);
  J(R.shB, -5, -134, o.shB); J(R.elB, 0, 66, o.elB);
  R.hipF.setAttribute('transform', `translate(${5 + (o.lean + sway)*.0},${hipY + 4}) rotate(${-o.hipF})`);
  R.hipB.setAttribute('transform', `translate(-5,${hipY + 4}) rotate(${-o.hipB})`);
  J(R.knF, 0, 80, o.knF); J(R.knB, 0, 80, o.knB);
  J(R.ftF, 0, 77, o.ftF); J(R.ftB, 0, 77, o.ftB);
  // a held prop can stay level and readable whatever the arm and the facing do
  if (A.uprightF && R.holdF) R.holdF.setAttribute('transform', `rotate(${o.shF + o.elF - o.lean - sway}) scale(${Math.sign(sx)},1)`);
  if (A.uprightB && R.holdB) R.holdB.setAttribute('transform', `rotate(${o.shB + o.elB - o.lean - sway}) scale(${Math.sign(sx)},1)`);
  if (R.tail) R.tail.setAttribute('transform', `rotate(${-(o.hipF + o.hipB)*.18 + 4*w*Math.sin(ph*2)})`);
  // face
  const blink = ((tl + sd*1.37) % (3.1 + (sd % 5)*.37)) < .11 ? .12 : 1;
  if (R.eye) R.eye.setAttribute('transform', `translate(0,${o.eyeY*2}) scale(1,${blink})`);
  if (R.brow) R.brow.setAttribute('transform', `translate(0,${-o.brow*3}) rotate(${-o.brow*9},16,-43)`);
  R.mouths.forEach(m => { const k = +m.dataset.m; m.style.opacity = cl(1 - Math.abs(o.mouth - k)); });
  if (R.shadow) R.shadow.setAttribute('transform', `translate(${p[0]},${p[1]}) scale(${sc*(1 - .05*w*(.5 - .5*Math.cos(2*ph)))},${sc})`);
}

// ---- shots --------------------------------------------------------------------------------------
function camAt(S, t) {
  const c = keyed(S.cam, t) || [960, 540, 1, 0];
  const sh = S.shake || 0;
  c[0] += sh * noise1(t*.6, 11) * 6; c[1] += sh * noise1(t*.5, 23) * 4;
  return c;
}
function layout(S, el, t) {
  const c = camAt(S, t), st = FILM.stage;
  const cx = c[0], cy = c[1], zm = c[2], rot = c[3] || 0;
  const foc = S.focus ? keyed(S.focus, t)[0] : 1;
  el._layers.forEach(L => {
    const z = +L.dataset.z, s = (1 + (zm - 1) * z) * st.s;
    const lx = W0/2 + (cx - W0/2) * z, ly = H0/2 + (cy - H0/2) * z;
    L.style.transform = `translate(${FILM.w/2}px,${FILM.h/2}px) rotate(${rot}deg) scale(${s}) translate(${-lx}px,${-ly}px)`;
    // 13 Nov: blur is most of the frame time on a software GPU, so it is skipped where nobody could see it:
    // layers marked noblur (soft gradients) and anything under 1 px; the radius is quantised so Chrome can reuse it
    const dz = Math.max(0, Math.abs(z - foc) - (S.band ?? .28));          // a depth band around the focus stays sharp
    const b = L.dataset.noblur ? 0 : Math.min((S.dof || 0) * dz * (z > foc ? 1.8 : 1) * st.s, 12);
    L.style.filter = b >= 1 ? `blur(${(Math.round(b * 2) / 2).toFixed(1)}px)` : 'none';
  });
}
function grain(t) {
  const f = Math.floor(t * 24);
  const r = n => ((Math.sin(f * 12.9898 + n * 78.233) * 43758.5453) % 1 + 1) % 1;
  document.querySelectorAll('.grain').forEach(g => g.style.transform = `translate(${-r(1)*200}px,${-r(2)*200}px)`);
}
function life(t, el) {                            // procedural ambient things inside a shot
  el.querySelectorAll('[data-swing]').forEach(s => {
    const [a, w, ph, px, py] = JSON.parse(s.dataset.swing);
    s.setAttribute('transform', `rotate(${a*Math.sin(t*w + ph)},${px},${py})`); });
  el.querySelectorAll('[data-drift]').forEach(s => {
    const [vx, vy, wrap] = JSON.parse(s.dataset.drift);
    let x = vx*t; if (wrap) x = ((x % wrap) + wrap) % wrap - wrap/2;
    s.setAttribute('transform', `translate(${x},${vy*t})`); });
  el.querySelectorAll('[data-flick]').forEach(s => {
    const [base, amp, sd] = JSON.parse(s.dataset.flick);
    s.style.opacity = base + amp * (noise1(t*7, sd)*.6 + noise1(t*19, sd + 5)*.4); });
  el.querySelectorAll('[data-motes]').forEach(s => {
    if (!s._m) { s._m = [...s.children].map((c, i) => [c, hash(i*3.1), hash(i*7.7), hash(i*1.3)]); }
    const [w, h, spd] = JSON.parse(s.dataset.motes);
    s._m.forEach(([c, a, b, d]) => {
      const x = (a*w + 18*Math.sin(t*(.3 + d*.4) + a*9) + t*spd*(d - .4)) % w;
      const y = ((b*h - t*spd*(.25 + d*.5)) % h + h) % h;
      c.setAttribute('cx', x.toFixed(1)); c.setAttribute('cy', y.toFixed(1));
      c.style.opacity = (.25 + .75*Math.abs(Math.sin(t*(.8 + d) + b*6))) * +s.dataset.op; }); });
  el.querySelectorAll('[data-steam]').forEach(s => {
    const k = +s.dataset.steam;
    [...s.children].forEach((c, i) => {
      const q = ((t*.35 + i/ s.children.length) % 1);
      c.setAttribute('transform', `translate(${8*Math.sin(t*1.3 + i*2 + k)},${-q*90}) scale(${1 + q*1.4})`);
      c.style.opacity = (Math.sin(q*Math.PI)*.55).toFixed(3); }); });
  el.querySelectorAll('[data-kv]').forEach(s => {            // keyed attributes: [[attr, keys], ...]
    s._kv = s._kv || JSON.parse(s.dataset.kv);
    s._kv.forEach(([attr, keys]) => {
      const v = keyed(keys, t);
      if (attr === 'translate') s.setAttribute('transform', `translate(${v[0]},${v[1]})` + (v.length > 2 ? ` rotate(${v[2]})` : '') + (v.length > 3 ? ` scale(${v[3]})` : ''));
      else if (attr === 'opacity') s.style.opacity = v[0];
      else if (attr === 'dash') { const L = s._L || (s._L = s.getTotalLength()); s.style.strokeDasharray = L; s.style.strokeDashoffset = L*(1 - v[0]); }
      else if (attr === 'count') { const d = +(s.dataset.dec || 0); s.textContent = (s.dataset.pre || '') + v[0].toFixed(d).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (s.dataset.suf || ''); }
      else if (attr === 'clip') s.style.clipPath = `inset(${v[0]}% ${v[1]}% ${v[2]}% ${v[3]}%)`;
      else s.setAttribute(attr, v[0]); }); });
}
window.seek = function (t) {
  grain(t);
  let flash = 0;
  FILM.shots.forEach((S, i) => {
    const el = document.getElementById('shot' + i);
    if (!el._layers) el._layers = [...el.querySelectorAll('.layer')];
    const tin = S.tin || ['cut', 0], d = tin[1] || 0;
    const local = t - S.start;
    const on = local >= -d && local < S.dur + ((FILM.shots[i + 1] && FILM.shots[i + 1].tin) ? FILM.shots[i + 1].tin[1] || 0 : 0);
    el.style.visibility = on ? 'visible' : 'hidden';
    if (!on) return;
    let op = 1;
    if (local < 0 && d > 0) {
      const q = CE.inout(cl((local + d) / d));
      if (tin[0] === 'dissolve') op = q;
      else if (tin[0] === 'flash') { op = q > .5 ? 1 : 0; flash = Math.max(flash, Math.sin(q*Math.PI)); }
      else if (tin[0] === 'iris') { op = 1; el.style.clipPath = `circle(${q*120}% at ${tin[2] || 50}% ${tin[3] || 50}%)`; }
      else op = q;
    } else if (tin[0] === 'iris') el.style.clipPath = 'none';
    el.style.opacity = op;
    el.style.zIndex = i;
    layout(S, el, local);
    (S.actors || []).forEach(A => poseActor(A, local));
    life(local, el);
    el.querySelectorAll('.a').forEach(a => place(a, local));
  });
  document.querySelector('.flash').style.opacity = flash;
  const cap = FILM.caps || [];
  document.querySelectorAll('.cap .a').forEach(a => place(a, t));
};
"""


def _noise_tile(n=256, seed=7):
    rng = np.random.default_rng(seed)
    a = (rng.normal(128, 38, (n, n))).clip(0, 255).astype(np.uint8)
    from PIL import Image
    buf = io.BytesIO()
    Image.fromarray(a, "L").save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


# ----------------------------------------------------------------------------------------------- the rig

# A look is the wardrobe and colouring of a figure. Hair "wig" is a long periwig (1700s gentlemen), "short"
# modern, "cap" a working man's cap, "bonnet" a woman's cap. Coat "long" flares to the knee (1700s), "suit"
# stops at the hip, "dress" is a long skirt over the legs.
LOOKS = {
    "gent_red":   dict(coat=RED, coat2="#A92C0D", vest=MUSTARD, legs="#3A2A22", stock="#EFE8DC", shoe=INK, skin="#E9BC98", hair="#EDE7DD", hat="tricorn", style="long", cuff="#F7F5F2"),
    "gent_teal":  dict(coat=TEAL, coat2="#0B5A54", vest="#F7F5F2", legs="#2B2B2B", stock="#EFE8DC", shoe=INK, skin="#C99372", hair="#D9D2C6", hat="", style="long", cuff="#F7F5F2"),
    "gent_ink":   dict(coat="#2A2522", coat2="#191513", vest="#B5553A", legs="#2A2522", stock="#EFE8DC", shoe=INK, skin="#E3B08C", hair="#F1EDE6", hat="tricorn", style="long", cuff="#EFE8DC"),
    "gent_mus":   dict(coat="#C99A3B", coat2="#A27A28", vest="#7A3B22", legs="#3B2F27", stock="#EFE8DC", shoe=INK, skin="#8D5A3B", hair="#2A1E18", hat="tricorn", style="long", cuff="#F7F5F2"),
    "gent_brown": dict(coat="#7A4A30", coat2="#5E3622", vest=MUSTARD, legs="#3A2A22", stock="#EFE8DC", shoe=INK, skin="#F0C7A4", hair="#BDB4A6", hat="", style="long", cuff="#EFE8DC"),
    "newton":     dict(coat="#3E3A4A", coat2="#2B2834", vest="#7A2E1C", legs="#2B2834", stock="#EFE8DC", shoe=INK, skin="#EBC3A3", hair="#F4F1EC", hat="", style="long", cuff="#F7F5F2"),
    "trader_cap": dict(coat="#5B6B5A", coat2="#47554A", vest="#C9A27A", legs="#4A3B30", stock="#D8CFC0", shoe="#2A1E18", skin="#D59E7B", hair="#3A2A20", hat="cap", style="long", cuff="#D8CFC0"),
    "lady_blue":  dict(coat="#3F6E8C", coat2="#2E5670", vest="#F7F5F2", legs="#3F6E8C", stock="#3F6E8C", shoe="#2A1E18", skin="#F1CBAA", hair="#5A3A28", hat="bonnet", style="dress", cuff="#F7F5F2"),
    "lady_red":   dict(coat="#A8402A", coat2="#86301E", vest="#F7F5F2", legs="#A8402A", stock="#A8402A", shoe="#2A1E18", skin="#B97A55", hair="#1E1410", hat="bonnet", style="dress", cuff="#F7F5F2"),
    "modern_navy": dict(coat="#1F2A44", coat2="#151D31", vest="#F7F5F2", legs="#1F2A44", stock="#1F2A44", shoe=INK, skin="#E5B391", hair="#2A1E18", hat="", style="suit", cuff="#F7F5F2", tie=RED),
    # 13 Nov, YouTube #7 (New York, 1907): frock coats and top hats, lounge suits and bowlers, long skirts. Generic
    # period clothing; nobody's likeness. era="1907" drops the 1700s periwig and shoe buckles.
    "banker_1907": dict(coat="#23252B", coat2="#16181C", vest="#3A3D44", legs="#3A3A3A", stock="#3A3A3A", shoe=INK, skin="#E8BB98", hair="#9A948C", hat="top", style="long", cuff="#F7F5F2", era="1907"),
    "banker_1907b": dict(coat="#3A2E28", coat2="#2A211C", vest="#7A3B22", legs="#2E2E30", stock="#2E2E30", shoe=INK, skin="#D9A684", hair="#3A2A20", hat="top", style="long", cuff="#F7F5F2", era="1907"),
    "banker_1907c": dict(coat="#2F3B46", coat2="#222C35", vest="#C99A3B", legs="#2B2B2B", stock="#2B2B2B", shoe=INK, skin="#B8805C", hair="#1E1410", hat="top", style="long", cuff="#F7F5F2", era="1907"),
    "clerk_1907": dict(coat="#4A4D52", coat2="#36383C", vest="#F7F5F2", legs="#4A4D52", stock="#4A4D52", shoe=INK, skin="#E5B391", hair="#5A3A28", hat="bowler", style="suit", cuff="#F7F5F2", tie=INK, era="1907"),
    "clerk_1907b": dict(coat="#5B4636", coat2="#46362A", vest="#F7F5F2", legs="#5B4636", stock="#5B4636", shoe=INK, skin="#8D5A3B", hair="#14100D", hat="bowler", style="suit", cuff="#F7F5F2", tie=RED, era="1907"),
    "clerk_1907c": dict(coat="#2E4A5A", coat2="#223845", vest="#F7F5F2", legs="#2E4A5A", stock="#2E4A5A", shoe=INK, skin="#F0C7A4", hair="#BDB4A6", hat="bowler", style="suit", cuff="#F7F5F2", tie=MUSTARD, era="1907"),
    "worker_1907": dict(coat="#5B6B5A", coat2="#47554A", vest="#C9A27A", legs="#4A3B30", stock="#4A3B30", shoe="#2A1E18", skin="#D59E7B", hair="#3A2A20", hat="cap", style="suit", cuff="#D8CFC0", tie="#7A3B22", era="1907"),
    "lady_1907": dict(coat="#5A3F5E", coat2="#452F49", vest="#F7F5F2", legs="#5A3F5E", stock="#5A3F5E", shoe="#2A1E18", skin="#F1CBAA", hair="#5A3A28", hat="wide", style="dress", cuff="#F7F5F2", era="1907"),
    "lady_1907b": dict(coat="#2E5670", coat2="#22435A", vest="#F7F5F2", legs="#2E5670", stock="#2E5670", shoe="#2A1E18", skin="#B97A55", hair="#1E1410", hat="wide", style="dress", cuff="#F7F5F2", era="1907"),
    "modern_grey": dict(coat="#4A4D52", coat2="#36383C", vest="#F7F5F2", legs="#4A4D52", stock="#4A4D52", shoe=INK, skin="#8A5638", hair="#14100D", hat="", style="suit", cuff="#F7F5F2", tie=TEAL),
    # 14 Nov, YouTube #8 (1960 to 1973): generic period suits in browns, tans and grey-blues with wide ties, a 1970s
    # dress, a cardigan for home. Nobody's likeness; used by build/cine_1971.py.
    "suit_1971": dict(coat="#6B4A32", coat2="#553A27", vest="#F1E6CF", legs="#6B4A32", stock="#6B4A32", shoe=INK, skin="#E5B391", hair="#5A3A28", hat="", style="suit", cuff="#F1E6CF", tie=MUSTARD, era="1971"),
    "suit_1971b": dict(coat="#3E4F66", coat2="#2F3D50", vest="#EEF0F2", legs="#3E4F66", stock="#3E4F66", shoe=INK, skin="#D9A684", hair="#2A1E18", hat="", style="suit", cuff="#EEF0F2", tie=RED, era="1971"),
    "suit_1971c": dict(coat="#A68A5E", coat2="#8C7349", vest="#F7F1E4", legs="#7A6446", stock="#7A6446", shoe="#2A1E18", skin="#F0C7A4", hair="#BDB4A6", hat="", style="suit", cuff="#F7F1E4", tie=TEAL, era="1971"),
    "suit_1971d": dict(coat="#2E2E33", coat2="#1F1F23", vest="#F2F2F2", legs="#2E2E33", stock="#2E2E33", shoe=INK, skin="#8D5A3B", hair="#14100D", hat="", style="suit", cuff="#F2F2F2", tie="#7A3B22", era="1971"),
    "home_1971": dict(coat="#C9733A", coat2="#A85E2E", vest="#F1E6CF", legs="#5B4A3A", stock="#5B4A3A", shoe="#2A1E18", skin="#E9BC98", hair="#7A4A2A", hat="", style="suit", cuff="#F1E6CF", tie="#C9733A", era="1971"),
    "lady_1971": dict(coat="#3F7A5A", coat2="#2F6048", vest="#F7F5F2", legs="#3F7A5A", stock="#3F7A5A", shoe="#2A1E18", skin="#F1CBAA", hair="#8A5A2A", hat="", style="dress", cuff="#F7F5F2", era="1971"),
}

SW = 3.2   # ink stroke


def _p(d, fill, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'


def _leg(L, back):
    dark = 0.82 if back else 1.0
    legs, stock, shoe = _shade(L["legs"], dark), _shade(L["stock"], dark), _shade(L["shoe"], dark)
    side = "B" if back else "F"
    if L["style"] == "dress":                           # legs mostly hidden by the skirt; shoes peek out
        thigh = ""
        shin = _p("M-8,0 L-7,74 L7,74 L8,0 Z", stock)
    else:
        thigh = _p("M-15,-4 C-17,30 -14,60 -11,84 L11,84 C14,60 17,30 15,-4 Z", legs)
        shin = _p("M-11,-2 C-11,30 -9,56 -8,76 L8,76 C9,56 11,30 11,-2 Z", stock)
    shoe_d = "M-10,-5 L14,-4 C26,-3 31,3 29,9 L-10,9 Q-13,2 -10,-5 Z"
    buckle = '' if L["style"] in ("suit",) or L.get("era") in ("1907", "1971") else f'<rect x="4" y="-4" width="7" height="5" rx="1" fill="{MUSTARD}" stroke="{INK}" stroke-width="1.5"/>'
    return (f'<g class="hip{side}">{thigh}<g class="kn{side}">{shin}'
            f'<g class="ft{side}">{_p(shoe_d, shoe)}{buckle}</g></g></g>')


def _arm(L, back, hold=""):
    dark = 0.82 if back else 1.0
    coat, cuff, skin = _shade(L["coat"], dark), _shade(L["cuff"], dark), _shade(L["skin"], dark)
    side = "B" if back else "F"
    upper = _p("M-12,-6 C-14,24 -12,48 -10,70 L10,70 C12,48 14,24 12,-6 Z", coat)
    fore = _p("M-10,-4 C-10,24 -9,44 -8,56 L8,56 C9,44 10,24 10,-4 Z", coat)
    cuff_d = _p("M-12,46 L12,46 L11,62 L-11,62 Z", cuff if L["style"] != "suit" else coat)
    shirt = _p("M-7,60 L7,60 L6,66 L-6,66 Z", "#F7F5F2") if L["style"] == "suit" else ""
    hand = (f'<g transform="translate(0,70)"><ellipse cx="0" cy="0" rx="9" ry="10" fill="{skin}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M5,-4 Q12,-2 10,5" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<g class="hold{side}">{hold}</g></g>')
    return f'<g class="sh{side}">{upper}<g class="el{side}">{fore}{cuff_d}{shirt}{hand}</g></g>'


def _head(L):
    skin, hair = L["skin"], L["hair"]
    back_hair = ""
    top_hair = ""
    if L["hat"] in ("", "tricorn") and L["style"] == "long" and L.get("era") != "1907":   # periwig: curls fall behind to the shoulders
        back_hair = _p("M-18,-58 C-40,-50 -42,-16 -36,8 C-30,22 -18,24 -10,18 C-6,6 -6,-20 -2,-40 Z", hair)
        back_hair += "".join(f'<circle cx="{-30 + 7*i}" cy="{4 + (i % 2)*5}" r="7" fill="{hair}" stroke="{INK}" stroke-width="2.2"/>' for i in range(3))
        top_hair = _p("M-22,-48 C-20,-66 6,-72 22,-60 C30,-54 30,-46 26,-44 C14,-52 -2,-50 -14,-40 Z", hair)
    elif L["hat"] == "wide":                                          # 1907: hair up, under a wide hat
        back_hair = _p("M-20,-50 C-34,-44 -34,-20 -22,-14 C-14,-20 -12,-34 -6,-46 Z", hair)
        top_hair = _p("M-22,-44 C-22,-62 10,-68 24,-54 C14,-52 0,-50 -16,-36 Z", hair)
    elif L["hat"] == "bonnet":
        back_hair = _p("M-20,-50 C-34,-40 -32,-12 -20,-6 C-14,-14 -12,-30 -6,-44 Z", hair)
        top_hair = (_p("M-30,-46 C-28,-72 16,-78 30,-54 C24,-50 -6,-52 -24,-38 Z", "#F7F5F2")
                    + f'<path d="M-26,-44 C-10,-58 14,-60 28,-52" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="3 5"/>')
    elif L["style"] == "suit":
        top_hair = _p("M-24,-40 C-24,-64 10,-70 26,-52 C22,-48 10,-50 -2,-46 C-8,-44 -14,-36 -18,-30 Z", hair)
    else:
        top_hair = _p("M-22,-44 C-22,-62 10,-68 24,-54 C14,-52 0,-50 -16,-36 Z", hair)
    hat = ""
    if L["hat"] == "tricorn":
        hat = (_p("M-40,-58 C-26,-64 18,-68 40,-58 C30,-50 22,-52 14,-50 C2,-48 -12,-50 -40,-58 Z", INK)
               + _p("M-24,-62 C-20,-86 20,-86 26,-62 Z", "#1E1A18")
               + f'<path d="M-30,-58 C-6,-66 18,-64 34,-58" fill="none" stroke="{MUSTARD}" stroke-width="2.2"/>')
    elif L["hat"] == "top":                                           # 1907: a silk top hat
        hat = (_p("M-34,-60 C-20,-66 18,-68 36,-60 C28,-54 -24,-54 -34,-60 Z", INK)
               + _p("M-22,-62 L-20,-118 C-6,-122 10,-122 22,-118 L22,-62 Z", "#141416")
               + f'<path d="M-21,-72 L22,-72" stroke="#55555C" stroke-width="5"/>')
    elif L["hat"] == "bowler":                                        # 1907: a bowler (derby)
        hat = (_p("M-34,-58 C-22,-64 20,-66 38,-58 C30,-52 -24,-52 -34,-58 Z", "#1E1A18")
               + _p("M-22,-60 C-24,-96 22,-98 24,-60 Z", "#2A2522")
               + f'<path d="M-22,-64 C-4,-68 12,-68 24,-64" fill="none" stroke="#55505A" stroke-width="3"/>')
    elif L["hat"] == "wide":
        hat = (_p("M-46,-56 C-24,-66 24,-68 48,-56 C34,-48 -32,-48 -46,-56 Z", L["coat"])
               + _p("M-24,-58 C-22,-82 22,-84 26,-58 Z", L["coat2"])
               + f'<circle cx="18" cy="-70" r="7" fill="{RED}" stroke="{INK}" stroke-width="2"/>')
    elif L["hat"] == "cap":
        hat = _p("M-24,-50 C-22,-74 18,-76 26,-54 L38,-50 C30,-46 20,-48 -24,-46 Z", "#4A3B30")
    neck = _p("M-7,4 L-6,-12 L8,-12 L8,4 Z", skin)
    head = _p("M-22,-34 C-24,-58 4,-66 20,-56 C30,-50 30,-40 31,-30 L37,-24 L31,-20 C31,-12 28,-4 20,-2 C8,2 -10,-2 -18,-14 C-22,-20 -22,-28 -22,-34 Z", skin)
    ear = f'<ellipse cx="-4" cy="-28" rx="5" ry="7" fill="{skin}" stroke="{INK}" stroke-width="2.4"/>'
    eye = f'<g class="eye"><ellipse cx="18" cy="-33" rx="2.6" ry="3.4" fill="{INK}"/></g>'
    brow = f'<g class="brow"><path d="M11,-42 L22,-43" stroke="{INK}" stroke-width="3" stroke-linecap="round"/></g>'
    cheek = f'<circle cx="16" cy="-20" r="5" fill="{RED}" opacity=".12"/>'
    mouths = (f'<path class="mouth" data-m="-1" d="M15,-11 Q21,-14 26,-11" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
              f'<path class="mouth" data-m="0" d="M16,-12 L25,-12" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
              f'<path class="mouth" data-m="1" d="M15,-13 Q21,-8 26,-13" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
              f'<ellipse class="mouth" data-m="2" cx="21" cy="-11" rx="3.6" ry="4.6" fill="{INK}"/>')
    return (f'<g class="head">{back_hair}{neck}{head}{ear}{cheek}{eye}{brow}{mouths}{top_hair}{hat}</g>')


def _torso(L, holdF="", holdB=""):
    coat, coat2, vest = L["coat"], L["coat2"], L["vest"]
    if L["style"] == "long":
        body = _p("M-28,-150 C-38,-110 -36,-60 -30,-18 C-26,0 26,0 30,-18 C36,-60 36,-110 28,-150 Q0,-160 -28,-150 Z", coat)
        tail = f'<g class="tail">{_p("M-31,-26 C-40,10 -44,40 -46,62 Q0,74 44,62 C40,40 36,10 31,-26 Z", coat2)}' \
               f'<path d="M4,-10 L6,64" stroke="{INK}" stroke-width="2.4"/></g>'
        front = (_p("M14,-148 C24,-110 26,-60 24,-20 L32,-20 C34,-60 32,-110 26,-148 Z", vest)
                 + "".join(f'<circle cx="27" cy="{-130 + 16*i}" r="2.6" fill="{MUSTARD}" stroke="{INK}" stroke-width="1.4"/>' for i in range(6))
                 + _p("M10,-154 C22,-150 30,-140 26,-128 C18,-132 12,-138 8,-146 Z", "#F7F5F2"))
        cuffbits = ""
    elif L["style"] == "dress":
        body = _p("M-24,-150 C-30,-120 -26,-80 -22,-46 C-10,-40 12,-40 24,-46 C28,-80 30,-120 24,-150 Q0,-158 -24,-150 Z", coat)
        tail = f'<g class="tail">{_p("M-24,-50 C-46,0 -54,80 -58,168 Q0,182 58,168 C54,80 46,0 24,-50 Z", coat2)}' \
               f'{_p("M-30,-20 C-20,40 -18,100 -16,166", "none")}</g>'
        front = _p("M-20,-152 C-6,-140 10,-140 22,-152 C14,-130 -10,-130 -20,-152 Z", "#F7F5F2")
        cuffbits = ""
    else:                                                     # suit
        body = _p("M-28,-150 C-36,-110 -34,-60 -30,-8 C-20,6 22,6 30,-8 C34,-60 34,-110 28,-150 Q0,-160 -28,-150 Z", coat)
        tail = '<g class="tail"></g>'
        front = (_p("M8,-152 L22,-152 L18,-100 L12,-104 Z", "#F7F5F2")
                 + _p("M15,-146 L19,-146 L20,-112 L16,-106 L13,-112 Z", L.get("tie", RED))
                 + f'<path d="M24,-148 L12,-104 L26,-60" fill="none" stroke="{INK}" stroke-width="2.4"/>')
        cuffbits = ""
    return (f'<g class="torso">{_arm(L, True, holdB)}{tail}<g class="breath">{body}{front}{cuffbits}</g>'
            f'{_head(L)}{_arm(L, False, holdF)}</g>')


def _shade(hexc, k):
    if k == 1.0 or not hexc.startswith("#"):
        return hexc
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % tuple(int(max(0, min(255, c * k))) for c in (r, g, b))


def rig(aid, look, holdF="", holdB=""):
    """The SVG for one rigged figure, ids scoped by aid. Draw order: shadow, back leg, front leg, torso
    (back arm, coat tail, body, head, front arm)."""
    L = LOOKS[look] if isinstance(look, str) else look
    shadow = f'<ellipse class="shadow" cx="0" cy="0" rx="46" ry="9" fill="#0A0A0A" opacity=".16"/>'
    legs = _leg(L, True) + _leg(L, False)
    return (f'<g id="{aid}">{shadow}<g class="root">'
            f'<g class="legs">{legs}</g>{_torso(L, holdF, holdB)}</g></g>')


# Poses ("forward" is positive: an arm raised in front, a leg stepping ahead; knees bend negative).
POSES = {
    "stand":   dict(),
    "relaxed": dict(shF=2, elF=12, shB=-2, elB=12),
    "read":    dict(shF=58, elF=62, shB=52, elB=70, head=10, eyeY=1, lean=3),
    "seated":  dict(hipF=84, knF=-86, hipB=80, knB=-82, rootY=80, ftF=4, ftB=4),
    "sit_read": dict(hipF=84, knF=-86, hipB=80, knB=-82, rootY=80, shF=58, elF=64, shB=52, elB=72, head=10, eyeY=1, lean=6),
    "sit_write": dict(hipF=84, knF=-86, hipB=80, knB=-82, rootY=80, shF=40, elF=58, shB=26, elB=60, head=18, eyeY=1.4, lean=16),
    "point":   dict(shF=88, elF=6, head=-4),
    "reach":   dict(shF=64, elF=18, lean=8),
    "hold_up": dict(shF=120, elF=30, head=-8),
    "shrug":   dict(shF=24, elF=70, shB=-20, elB=70, brow=1),
    "cheer":   dict(shF=150, elF=20, shB=140, elB=24, mouth=1, brow=.6),
    "concern": dict(shF=30, elF=110, head=6, brow=-1, mouth=-1),
    "talk_a":  dict(shF=36, elF=60, mouth=2, brow=.4),
    "talk_b":  dict(shF=20, elF=40, mouth=0, brow=0),
}


def pose(name=None, **over):
    d = dict(POSES.get(name or "stand", {}))
    d.update(over)
    return d


def actor(aid, look, pos, pose_keys=None, turn=None, scale=1.0, seed=1, stride=None, t0=0.0, amp=24, dir=1,
          walk=True, holdF="", holdB="", upright=False):
    """One rigged person in a shot. pos: [[t, x, y(ground)], ...]; pose_keys: [[t, dict], ...];
    turn: [[t, dir], ...] (dir 1 faces right, -1 left; give two keys about .3 s apart to turn)."""
    stride = stride or 2 * 2 * LEG * math.sin(math.radians(amp)) * 1.0
    spec = dict(id=aid, pos=pos, pose=[[k[0], k[1]] + ([k[2]] if len(k) > 2 else []) for k in (pose_keys or [])],
                turn=turn, scale=scale, seed=seed, stride=stride, t0=t0, amp=amp, dir=dir, walk=walk,
                uprightF=bool(upright and holdF), uprightB=bool(upright and holdB))
    return dict(spec=spec, svg=rig(aid, look, holdF, holdB))


def footsteps(a, dur, shot_start=0.0):
    """Times (film seconds) when the actor's feet land, read from the same gait the runtime animates:
    a foot lands each time the gait phase passes a quarter turn while the figure is moving."""
    s = a["spec"]
    pos = s["pos"]
    if len(pos) < 2 or not s.get("walk", True):
        return []
    ts = np.arange(0, dur, 1 / 120)
    xs = np.array([_keyed_py(pos, t)[0] for t in ts])
    dist = np.concatenate([[0], np.cumsum(np.abs(np.diff(xs)))])
    ph = dist / s["stride"] * 2 * math.pi
    q = np.floor((ph - math.pi / 2) / math.pi)
    hits = []
    v = np.abs(np.gradient(xs, ts))
    for i in range(1, len(ts)):
        if q[i] > q[i - 1] and v[i] > 15:
            hits.append(round(shot_start + s["t0"] + ts[i], 3))
    return hits


def _ease(name, p):
    p = min(max(p, 0.0), 1.0)
    if name == "lin":
        return p
    if name == "out":
        return 1 - (1 - p) ** 3
    if name == "in":
        return p ** 3
    if name == "sine":
        return -(math.cos(math.pi * p) - 1) / 2
    if name == "hold":
        return 0.0
    return 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2


def _keyed_py(keys, t):
    strip = lambda k: k[1:-1] if isinstance(k[-1], str) else k[1:]
    if t <= keys[0][0]:
        return strip(keys[0])
    for a, b in zip(keys, keys[1:]):
        if t < b[0]:
            en = b[-1] if isinstance(b[-1], str) else "inout"
            q = _ease(en, (t - a[0]) / max(b[0] - a[0], 1e-6))
            return [va + (vb - va) * q for va, vb in zip(strip(a), strip(b))]
    return strip(keys[-1])


# ----------------------------------------------------------------------------------------------- building blocks

def layer(z, inner, w=4000, h=1600, x=0, y=0, cls="", noblur=False):
    """A depth layer. inner is SVG markup drawn in world coordinates (it may start left of 0).
    noblur: never blur it (a sky gradient looks the same blurred and costs most of a frame)."""
    nb = ' data-noblur="1"' if noblur else ""
    return (f'<div class="layer {cls}" data-z="{z}"{nb}><svg width="{w}" height="{h}" viewBox="{x} {y} {w} {h}" '
            f'style="left:{x}px;top:{y}px">{inner}</svg></div>')


def kv(**tracks):
    """data-kv attribute: animated SVG attributes, e.g. kv(translate=[[0,0,0],[2,100,0]], opacity=[[0,0],[1,1]])."""
    return "data-kv='" + json.dumps([[k, v] for k, v in tracks.items()]) + "'"


def motes(x, y, w, h, n=40, op=.7, spd=10, color="#FFF4DC", seed=3):
    rng = random.Random(seed)
    dots = "".join(f'<circle r="{rng.uniform(1.2, 3.2):.1f}" fill="{color}"/>' for _ in range(n))
    return f'<g transform="translate({x},{y})" data-motes=\'[{w},{h},{spd}]\' data-op="{op}">{dots}</g>'


def shaft(x, y, w, h, angle=-24, op=.35, color="255,240,200"):
    return (f'<g transform="translate({x},{y}) rotate({angle})"><rect x="0" y="0" width="{w}" height="{h}" '
            f'fill="url(#shaft)" opacity="{op}" data-flick=\'[{op},0.04,{x % 7}]\'/></g>')


def defs():
    return ('<defs><linearGradient id="shaft" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#FFF6DE" stop-opacity=".95"/><stop offset="1" stop-color="#FFF6DE" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="glowWarm"><stop offset="0" stop-color="#FFE3A3" stop-opacity=".9"/><stop offset="1" stop-color="#FFE3A3" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="candle"><stop offset="0" stop-color="#FFD27A" stop-opacity=".85"/><stop offset=".5" stop-color="#FFB347" stop-opacity=".25"/><stop offset="1" stop-color="#FFB347" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="skyWarm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9C7A6"/><stop offset=".55" stop-color="#F1DDB4"/><stop offset="1" stop-color="#F8EBCF"/></linearGradient>'
            '<pattern id="cobble" width="46" height="26" patternUnits="userSpaceOnUse"><rect width="46" height="26" fill="#A08B73"/>'
            '<path d="M2,13 Q12,2 22,13 Q12,24 2,13 Z M25,13 Q34,3 44,13 Q34,24 25,13 Z" fill="#B59F86" stroke="#7C6A57" stroke-width="1.6"/></pattern>'
            '<pattern id="boards" width="160" height="40" patternUnits="userSpaceOnUse"><rect width="160" height="40" fill="#7A5236"/>'
            '<path d="M0,39 L160,39 M80,0 L80,39" stroke="#5E3D27" stroke-width="2"/></pattern>'
            '<pattern id="paperlines" width="10" height="18" patternUnits="userSpaceOnUse"><path d="M0,17 L10,17" stroke="#CFC6B6" stroke-width="1"/></pattern>'
            '</defs>')


def stage(w, h):
    """Fit the 1920 x 1080 world to the frame: height-fit for vertical films, width-fit for wide."""
    return dict(s=h / H0 if w / h < W0 / H0 else w / W0)


# ----------------------------------------------------------------------------------------------- the film

def film_html(shots, w=1920, h=1080, caps="", mark=True, badge="", fps=30):
    t, specs, body = 0.0, [], []
    for i, S in enumerate(shots):
        specs.append(dict(start=round(t, 4), dur=S["dur"], cam=S.get("cam"), focus=S.get("focus"), dof=S.get("dof", 0),
                          tin=list(S.get("tin", ("cut", 0))), shake=S.get("shake", 0), band=S.get("band", .28),
                          actors=[a["spec"] for a in S.get("actors", [])]))
        grade = S.get("grade", "warm")
        gcol, gop = {"warm": ("#FFB25E", .10), "cool": ("#6FA3B8", .10), "dusk": ("#D9733F", .16),
                     "none": ("#000", 0)}.get(grade, (None, None)) if isinstance(grade, str) else (grade["color"], grade["op"])
        body.append(f'<div class="shot" id="shot{i}"><div class="world">{"".join(S["layers"])}</div>'
                    f'<div class="grade" style="background:{gcol};opacity:{gop};mix-blend-mode:soft-light"></div>'
                    f'<div class="vig" style="opacity:{S.get("vig", 1)}"></div>'
                    f'<div class="over">{"".join(S.get("over", []))}</div></div>')
        t += S["dur"]
    st = stage(w, h)
    s = min(w, h) / 1080
    chrome = ""
    if mark:
        chrome += f'<div class="mark" style="left:{int(70*s)}px;top:{int(50*s) if w > h else int(150*s)}px;font-size:{int(42*s)}px">IB<span style="color:#D93A12">.</span></div>'
    if badge:
        chrome += (f'<div class="badge" style="right:{int(70*s)}px;top:{int(58*s) if w > h else int(158*s)}px;font-size:{int(17*s)}px;'
                   f'padding:{int(7*s)}px {int(12*s)}px">{badge}</div>')
    css = CSS.replace("FONTS/", f"{FONTS.resolve()}/")
    from motion import JS as MJS
    film = dict(shots=specs, w=w, h=h, stage=st, total=t)
    noise = _noise_tile()
    html = ("<!doctype html><html><head><meta charset='utf-8'><style>" + css
            + f".grain{{background-image:url({noise});opacity:.07}}</style></head><body>"
            + f'<div class="f" style="width:{w}px;height:{h}px">{"".join(body)}<div class="grain"></div><div class="flash"></div>'
            + chrome + caps + "</div>"
            + "<script>window.SCENES=[];window.TOTAL=1;" + MJS.split("window.seek = function")[0]
            + f"\nconst W0={W0},H0={H0},HIP={HIP_H};window.FILM={json.dumps(film)};\n" + RUNTIME + "</script></body></html>")
    return html, t


def captions(lines, w=1920, h=1080, size=None, bottom=None, maxw=None):
    """Burned captions, word by word. lines: [(text, start, end, [(word, t0, t1), ...] or None)], film seconds."""
    s = min(w, h) / 1080
    size = size or int((40 if w > h else 50) * s)
    bottom = bottom if bottom is not None else (int(64 * s) if w > h else int(520 * s))
    maxw = maxw or (int(1500 * s) if w > h else int(900 * s))
    out = []
    for text, a, b, words in lines:
        if not words:
            ws = text.split()
            per = (b - a) / max(len(ws), 1)
            words = [(x, a + k * per, a + (k + 1) * per) for k, x in enumerate(ws)]
        spans = "".join(f'<span class="w" data-t="{max(0.0, wa - a):.3f}">{x}</span> ' for x, wa, _ in words)
        out.append(f'<div class="cap" style="bottom:{bottom}px"><div class="a" data-fx="life" data-at="{a - .1:.3f}" data-d="{b - a + .2:.3f}" '
                   f'data-fi=".15" data-fo=".15"><span class="line" style="font-size:{size}px;max-width:{maxw}px;padding:{int(10*s)}px {int(22*s)}px">'
                   f'<span class="a" data-fx="kara" data-at="{a:.3f}" data-d="{b - a:.3f}">{spans}</span></span></div></div>')
    return "".join(out)


def _render_range(args):
    src, w, h, fps, f0, f1, out, quality, crf = args
    from playwright.sync_api import sync_playwright
    import time
    t0 = time.time()
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p", "-g", str(fps * 2), str(out)],
                          stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--disable-gpu-vsync"])
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(pathlib.Path(src).resolve().as_uri())
        pg.evaluate("Promise.all([400,500,600].map(w => document.fonts.load(w + ' 40px Sans')).concat([document.fonts.load(\"700 40px 'Serif'\"),"
                    " document.fonts.load(\"italic 400 40px 'Serif'\")]))")
        for f in range(f0, f1):
            pg.evaluate(f"seek({f / fps})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=quality))
            if (f - f0) % 90 == 0:
                print(f"  [{f0}-{f1}] frame {f} ({time.time() - t0:.0f} s)", flush=True)
        b.close()
    ff.stdin.close()
    ff.wait()
    return out


def render(html, total, work, name, w=1920, h=1080, fps=30, frames=None, quality=90, crf=18, workers=2):
    """Film every frame. Returns (silent MP4 path, seconds). The frames are split into contiguous ranges, each
    rendered by its own headless browser (one per CPU core), and the parts are joined without re-encoding.
    frames=(first, last) renders a slice for previews."""
    import time
    from concurrent.futures import ProcessPoolExecutor
    work = pathlib.Path(work)
    work.mkdir(parents=True, exist_ok=True)
    src = work / f"{name}.html"
    src.write_text(html)
    mp4 = work / f"{name}-silent.mp4"
    n = int(round(total * fps))
    f0, f1 = frames or (0, n)
    k = max(1, min(workers, (f1 - f0) // 30))
    # 13 Nov: a queue of short chunks, not one half per worker: shots differ a lot in cost (a crowded street
    # with depth of field against a chart on parchment), so halves left one core idle for minutes
    size = max(48, (f1 - f0) // (k * 5)) if k > 1 else (f1 - f0)
    cuts = list(range(f0, f1, size)) + [f1]
    parts = [work / f"{name}-part{i:03d}.mp4" for i in range(len(cuts) - 1)]
    t0 = time.time()
    jobs = [(str(src), w, h, fps, cuts[i], cuts[i + 1], str(parts[i]), quality, crf) for i in range(len(parts))]
    if k == 1:
        _render_range(jobs[0])
    else:
        with ProcessPoolExecutor(k) as ex:
            list(ex.map(_render_range, jobs))
    lst = work / f"{name}-parts.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(mp4)], check=True)
    for p in parts:
        p.unlink()
    lst.unlink()
    secs = time.time() - t0
    print(f"  rendered {f1 - f0} frames in {secs:.0f} s ({secs / max(f1 - f0, 1):.2f} s a frame, {k} workers)", flush=True)
    return mp4, secs


def stills(html, times, work, name, w=1920, h=1080):
    """PNG frames at given film seconds (contact sheets, thumbnails, checks)."""
    from playwright.sync_api import sync_playwright
    work = pathlib.Path(work)
    src = work / f"{name}.html"
    src.write_text(html)
    paths = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(src.resolve().as_uri())
        pg.evaluate("document.fonts.ready")
        for t in times:
            pg.evaluate(f"seek({t})")
            out = work / f"{name}-{t:06.2f}.png"
            pg.screenshot(path=str(out))
            paths.append(out)
        b.close()
    return paths
