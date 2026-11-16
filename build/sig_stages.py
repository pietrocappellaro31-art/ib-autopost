"""
Where the no-music master costs the voice (16 Nov 2026). The SIG-drop gate (audio-standard.md 1b, 0.15 or less from
the voice stem to the clean mix) kept landing at 0.13 to 0.16 on Shorts with the effects muted, so the drop is not the
effects. This rebuilds a story-engine render's master one stage at a time from its raw takes (out/<slug>/parts, kept
by story.keep_parts) and scores each stage with DNSMOS (quality.score), voice only and with effects and room:

    raw        the voice stem as float, no int16 rounding           (the reference)
    stem16     voice.wav as the render writes it (int16)
    chain      + the narrator chain (voice.MASTER: highpass, 7.2 kHz dip)
    gain       + the plain gain to -14 LUFS (premaster, no limiter)
    limit      + the 4x true-peak limiter of levels.two_stage
    aac        + the AAC 192k encode (what YouTube receives)
    ... and the same with the room tone and the effects mixed in (mix_*)

    python3 build/sig_stages.py build/shorts_<slug>.py

Writes out/<slug>/sig_stages.json. A score tells which stage to look at; it is not a listening verdict.
"""

import importlib.util
import json
import pathlib
import subprocess
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import levels as L              # noqa: E402
import quality                  # noqa: E402
import story                    # noqa: E402
from motion import OUT          # noqa: E402
from voice import SR, write_wav, MASTER   # noqa: E402


def ff(args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def f32(path, a, sr=SR):
    from scipy.io import wavfile
    wavfile.write(str(path), sr, np.asarray(a, np.float32))


def stages(ep, work, voice, fx, total, tag, d, ceiling=-1.5, target=-14, limiter=True, room=None):
    room = ep.get("room", .0006) if room is None else room
    out = {}
    src = d / f"{tag}_in.wav"
    if tag == "voice":
        f32(src, voice)
        graph = f"[0:a]{MASTER},aresample=48000[a]"
        inputs = ["-i", str(src)]
    else:
        f32(d / "v.wav", voice)
        f32(d / "fx.wav", fx)
        graph = (f"[0:a]{MASTER}[v];anoisesrc=color=brown:amplitude={room}:seed={ep.get('room_seed', 1)}:sample_rate={SR}:"
                 f"duration={total + .6:.2f}[room];[v][1:a][room]amix=inputs=3:normalize=0,aresample=48000[a]")
        inputs = ["-i", str(d / "v.wav"), "-i", str(d / "fx.wav")]
    chain = d / f"{tag}_chain.wav"
    ff([*inputs, "-filter_complex", graph, "-map", "[a]", "-c:a", "pcm_f32le", str(chain)])
    out["chain"] = chain
    i0, _ = L.loudness(chain)
    g = target - i0
    gain = d / f"{tag}_gain.wav"
    ff(["-i", str(chain), "-af", f"volume={g:.2f}dB", "-c:a", "pcm_f32le", str(gain)])
    out["gain"] = gain
    ceil = 10 ** ((ceiling - .3) / 20)
    lim = d / f"{tag}_limit.wav"
    ff(["-i", str(chain), "-af", f"volume={g:.2f}dB,aresample=192000,alimiter=limit={ceil:.4f}:attack=1:release=60:level=false,"
        "aresample=48000", "-c:a", "pcm_f32le", str(lim)])
    out["limit"] = lim
    aac = d / f"{tag}_aac.m4a"
    ff(["-i", str(lim), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(aac)])
    out["aac"] = aac
    return out


def main(path):
    spec = importlib.util.spec_from_file_location("ep", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    ep = m.EP
    work = OUT / ep["slug"]
    parts = story.load_parts(work)
    if not parts:
        sys.exit("no raw parts: render with the 16 Nov story.py first")
    at, spans, total = story.timeline(ep, parts)
    voice, fx = story.soundtrack(ep, parts, at, spans, total + .6)
    fx = fx * L.shorts_mix(ep)[1]
    peak = max(float(np.abs(voice).max()), float(np.abs(fx).max()), 1e-9)
    if peak > .89:
        voice, fx = voice * (.89 / peak), fx * (.89 / peak)
    d = work / "_stages"
    d.mkdir(exist_ok=True)
    rows = {}
    f32(d / "raw.wav", voice)
    rows["raw"] = d / "raw.wav"
    write_wav(d / "stem16.wav", voice)
    rows["stem16"] = d / "stem16.wav"
    for k, v in stages(ep, work, voice, fx, total, "voice", d).items():
        rows[k] = v
    for k, v in stages(ep, work, voice, fx, total, "mix", d).items():
        rows["mix_" + k] = v
    rows["final"] = work / f"{ep['slug']}.mp4"
    res = {}
    for k, p in rows.items():
        s = quality.score(p)
        res[k] = {x: round(float(s[x]), 3) for x in ("sig", "bak", "ovrl")}
        print(f"  {k:12s} SIG {res[k]['sig']:.3f}  BAK {res[k]['bak']:.3f}  OVRL {res[k]['ovrl']:.3f}", flush=True)
    for k in ("raw", "aac", "mix_aac"):                    # the same three at a common loudness (quality.score_at)
        s = quality.score_at(rows[k])
        res[k + "@-23"] = {x: round(float(s[x]), 3) for x in ("sig", "bak", "ovrl")}
        print(f"  {k + '@-23':12s} SIG {s['sig']:.3f}  BAK {s['bak']:.3f}  OVRL {s['ovrl']:.3f}", flush=True)
    json.dump(res, open(work / "sig_stages.json", "w"), indent=1)
    return res


if __name__ == "__main__":
    main(sys.argv[1])
