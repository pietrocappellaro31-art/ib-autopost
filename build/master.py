"""
Dual masters (13 Nov 2026, cinematic upgrade): one picture, two soundtracks.

  CLEAN   narration + sound effects + ambience. No music. For when Pietro adds a track from a platform's own
          library (YouTube "Add sound", Audio Library, Instagram in-app music), and the safe default for any
          platform whose music rights we have not checked.
  SCORED  the same, plus our original score (score.py), ducked under the voice. Only for music whose rights
          are cleared for that platform (music-library classes ORIGINAL_GENERATED or LICENSED_FOR_...).

The picture is rendered once; each master copies the same video stream and gets its own audio, so the two
can never drift apart in timing or imagery.

    from master import Stems, dual
    st = Stems(total)                         # 48 kHz stereo buses
    st.voice_at(wav_24k, at_seconds)          # narration lines where they belong
    st.add("foley", array); st.add("amb", array, gain); st.add("music", array)
    report = dual(st, silent_mp4, out_dir, slug, lufs=-14, tp=-1.5, script="...")

Everything is measured on the files written, not assumed from settings: integrated loudness, true peak and
loudness range (ffmpeg ebur128), clipped samples, the longest stretch of silence, how far the voice sits
above the music while speaking, DNSMOS on each master, and a word-error check of the scored master itself
(can a recogniser still hear every word through the music?). Results go to <out>/<slug>-masters.json.
"""

import json
import pathlib
import re
import subprocess
import tempfile

import numpy as np

SR = 48000


def _resample(x, sr_in):
    if sr_in == SR:
        return x
    from scipy.signal import resample_poly
    from math import gcd
    g = gcd(SR, sr_in)
    return resample_poly(x, SR // g, sr_in // g).astype(np.float32)


def read_wav(path):
    import wave
    with wave.open(str(path)) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        a = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768
    a = a.reshape(-1, ch)
    return a, sr


def write_wav(path, x):
    import wave
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = x[:, None]
    with wave.open(str(path), "wb") as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


class Stems:
    def __init__(self, total, tail=.6):
        self.total = total
        self.n = int((total + tail) * SR)
        self.bus = {k: np.zeros((self.n, 2), np.float32) for k in ("voice", "foley", "amb", "music")}

    def voice_at(self, wav, at, gain=1.0):
        a, sr = read_wav(wav)
        mono = _resample(a.mean(1), sr) * gain
        i = int(at * SR)
        m = max(0, min(len(mono), self.n - i))
        self.bus["voice"][i:i + m] += mono[:m, None]

    def add(self, bus, x, gain=1.0, at=0.0):
        if x.ndim == 1:
            x = np.repeat(x[:, None], 2, 1)
        i = int(at * SR)
        m = max(0, min(len(x), self.n - i))
        self.bus[bus][i:i + m] += x[:m] * gain


def voice_chain(x, chain):
    """Run the voice bus through an ffmpeg filter chain (the narrator's EQ, de-esser, compressor)."""
    with tempfile.TemporaryDirectory() as d:
        a, b = pathlib.Path(d) / "a.wav", pathlib.Path(d) / "b.wav"
        write_wav(a, x)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(a), "-af", chain, "-ar", str(SR), "-ac", "2", str(b)], check=True)
        y, _ = read_wav(b)
    out = np.zeros_like(x)
    out[:min(len(y), len(x))] = y[:len(x)]
    return out


def envelope(x, win=.02, attack=.06, release=.35):
    """0..1 speech activity from the voice bus, with attack and release smoothing."""
    mono = np.abs(x).mean(1) if x.ndim == 2 else np.abs(x)
    hop = int(win * SR)
    rms = np.array([np.sqrt(np.mean(mono[i:i + hop] ** 2)) for i in range(0, len(mono), hop)])
    act = (rms > max(1e-4, np.percentile(rms[rms > 0], 60) * .15 if np.any(rms > 0) else 1)).astype(float) if len(rms) else rms
    sm = np.zeros_like(act)
    a_c, r_c = np.exp(-win / attack), np.exp(-win / release)
    for i in range(len(act)):
        prev = sm[i - 1] if i else 0
        c = a_c if act[i] > prev else r_c
        sm[i] = c * prev + (1 - c) * act[i]
    return np.repeat(sm, hop)[:len(mono)]


def mix(st, music_gain=1.0, duck_db=11.0, amb_duck_db=4.0, chain=None, music_under_db=8.0, amb_under_db=24.0,
        foley_level_db=-17.0, voice_level_db=-12.0):
    """Returns (clean, scored, info): float32 stereo pre-loudness mixes.
    13 Nov: dense beds are set by RMS against the speech, not by peak (a peak-normalised score sat only 12.6 dB under
    the voice on the first proof). The music's RMS is music_under_db below the speech RMS before ducking, so about
    music_under_db + duck_db below it while speaking; the ambience amb_under_db below. Effects are transients and are
    set by peak."""
    def norm_peak(x, db):
        p = np.abs(x).max()
        return x * (10 ** (db / 20) / p) if p > 0 else x
    def rms(x):
        return float(np.sqrt(np.mean(x ** 2))) if x.size else 0.0
    v = st.bus["voice"]
    if chain:
        v = voice_chain(v, chain)
    v = norm_peak(v, voice_level_db)
    env = envelope(v)
    sp = env > .7
    v_rms = rms(v[sp]) if sp.any() else rms(v)
    def under(x, db):
        r = rms(x[np.abs(x).mean(1) > 1e-6]) if np.any(np.abs(x) > 1e-6) else 0
        return x * (v_rms * 10 ** (-db / 20) / r) if r > 0 else x
    duck = 10 ** (-duck_db * env / 20)
    aduck = 10 ** (-amb_duck_db * env / 20)
    music = under(st.bus["music"], music_under_db) * duck[:, None] * music_gain
    amb = under(st.bus["amb"], amb_under_db) * aduck[:, None]
    foley = norm_peak(st.bus["foley"], foley_level_db)
    clean = v + amb + foley
    scored = clean + music
    vom = None
    if sp.any() and np.abs(music).max() > 0:
        vom = round(float(20 * np.log10(v_rms / max(rms(music[sp]), 1e-9))), 1)
    amb_db = round(float(20 * np.log10(v_rms / max(rms(amb[sp]), 1e-9))), 1) if sp.any() and np.abs(amb).max() > 0 else None
    return clean, scored, dict(voice_over_music_db=vom, voice_over_ambience_db=amb_db, duck_db=duck_db)


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    get = lambda pat: float(re.search(pat, tail).group(1))
    return dict(lufs=get(r"I:\s+(-?[\d.]+) LUFS"), lra=get(r"LRA:\s+(-?[\d.]+) LU"), true_peak=get(r"Peak:\s+(-?[\d.]+) dBFS"))


def two_stage(src_wav, dst_wav, lufs, tp):
    """Measure, then normalise with the measured values (linear when possible), then a true-peak limiter."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src_wav), "-af", f"loudnorm=I={lufs}:TP={tp}:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    f = (f"loudnorm=I={lufs}:TP={tp}:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
         f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,alimiter=limit={10 ** ((tp - .3) / 20):.4f}:level=false")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src_wav), "-af", f + ",aresample=48000", "-ar", str(SR), str(dst_wav)], check=True)
    m = loudness(dst_wav)
    if abs(m["lufs"] - lufs) > .4:                                    # second pass: a plain gain trim, then the limiter again
        g = lufs - m["lufs"]
        tmp = pathlib.Path(str(dst_wav) + ".tmp.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(dst_wav), "-af", f"volume={g}dB,alimiter=limit={10 ** ((tp - .3) / 20):.4f}:level=false",
                        "-ar", str(SR), str(tmp)], check=True)
        tmp.replace(dst_wav)
    return loudness(dst_wav)


def silences(x, floor_db=-50, min_s=1.2):
    mono = np.abs(x).mean(1)
    hop = int(.05 * SR)
    rms = np.array([np.sqrt(np.mean(mono[i:i + hop] ** 2)) for i in range(0, len(mono) - hop, hop)])
    db = 20 * np.log10(rms + 1e-12)
    runs, i = [], 0
    while i < len(db):
        if db[i] < floor_db:
            j = i
            while j < len(db) and db[j] < floor_db:
                j += 1
            if (j - i) * .05 >= min_s:
                runs.append((round(i * .05, 2), round(j * .05, 2)))
            i = j
        else:
            i += 1
    return runs


def mux(silent_mp4, wav, out):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent_mp4), "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", str(out)], check=True)


def dual(st, silent_mp4, out_dir, slug, lufs=-14.0, tp=-1.5, script=None, chain=None, scored=True, excerpt=None, **mixargs):
    """script: the whole narration, for a word check of the entire master (short films). excerpt: (t0, t1, text),
    one narrated stretch checked in each master (long films, where transcribing everything is slow)."""
    out_dir = pathlib.Path(out_dir)
    clean, sc, info = mix(st, chain=chain, **mixargs)
    stems_dir = out_dir / "stems"
    stems_dir.mkdir(parents=True, exist_ok=True)
    for k, v in st.bus.items():
        write_wav(stems_dir / f"{k}.wav", v / max(np.abs(v).max(), 1e-9) * .9 if np.abs(v).max() > 0 else v)
    report = dict(slug=slug, target_lufs=lufs, target_tp=tp, **info, masters={})
    for name, x in (("clean", clean),) + ((("scored", sc),) if scored else ()):
        raw, fin = out_dir / f"{slug}-{name}-raw.wav", out_dir / f"{slug}-{name}.wav"
        write_wav(raw, x)
        meas = two_stage(raw, fin, lufs, tp)
        y, _ = read_wav(fin)
        mp4 = out_dir / f"{slug}-{name}.mp4"
        mux(silent_mp4, fin, mp4)
        m = dict(file=mp4.name, **meas, clipped_samples=int((np.abs(y) >= .999).sum()), silences=silences(y))
        try:
            import quality
            m["dnsmos"] = quality.score(str(fin))
        except Exception as e:                                         # the model is optional; say so
            m["dnsmos"] = f"not measured ({type(e).__name__})"
        if script:
            from voice_check import transcribe, wer
            mono16 = out_dir / f"{slug}-{name}-mono.wav"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(fin), "-ac", "1", "-ar", "24000", str(mono16)], check=True)
            heard = transcribe(str(mono16))
            m["wer_of_master"] = round(float(wer(script, heard)), 3)
            m["heard"] = heard
        if excerpt:
            from voice_check import transcribe, wer
            a, b, text = excerpt
            cut = out_dir / f"{slug}-{name}-excerpt.wav"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(a - .1, 0):.2f}", "-t", f"{b - a + .3:.2f}", "-i", str(fin), "-ac", "1",
                            "-ar", "24000", str(cut)], check=True)
            heard = transcribe(str(cut))
            m["wer_excerpt"] = round(float(wer(text, heard)), 3)
            m["excerpt"] = dict(t0=round(a, 2), t1=round(b, 2), heard=heard)
            cut.unlink()
        report["masters"][name] = m
        raw.unlink()
    json.dump(report, open(out_dir / f"{slug}-masters.json", "w"), indent=1)
    return report


def scored_alternative(clean_mp4, moods=("explain", "resolve"), out=None, lufs=-14.0, tp=-1.5, key="F", bpm=80, seed=7,
                       music_under_db=8.0, duck_db=11.0):
    """13 Nov (cinematic upgrade): a scored alternative for a finished CLEAN master (a Levels Short or a Reel),
    without re-rendering the picture or touching its engine. The clean soundtrack (voice + effects) is kept as it
    is; an original score.py cue in the given moods (split evenly across the film) is set by RMS under it, ducked
    while anyone speaks, and the sum is mastered to the clean master's platform target. The word check compares
    what a recogniser hears in the scored file against the clean one. Writes <stem>-scored.mp4 (or out) and
    <stem>-scored.json. Rights: the score is ORIGINAL_GENERATED (music-library), so it may go in any platform's file.

        python3 build/master.py scored build/out/<slug>/<slug>.mp4 [-16 for a Reel] [mood mood ...]
    """
    import score as SC
    clean_mp4 = pathlib.Path(clean_mp4)
    out = pathlib.Path(out) if out else clean_mp4.with_name(clean_mp4.stem + "-scored.mp4")
    tmp = pathlib.Path(tempfile.mkdtemp())
    wav = tmp / "clean.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(clean_mp4), "-vn", "-ac", "2", "-ar", str(SR), str(wav)], check=True)
    cl, _ = read_wav(wav)
    total = len(cl) / SR
    n = len(moods)
    secs = [(total * i / n, total * (i + 1) / n, m) for i, m in enumerate(moods)]
    stems, sco = SC.compose(secs, key=key, bpm=bpm, seed=seed)
    music = SC.master_music(stems)
    m = np.zeros_like(cl)
    k = min(len(m), len(music))
    m[:k] = music[:k]
    env = envelope(cl)                                          # the clean track's own speech-and-effects envelope
    sp = env > .7
    rms = lambda x: float(np.sqrt(np.mean(x ** 2))) if x.size else 0.0
    ref = rms(cl[sp]) if sp.any() else rms(cl)
    mr = rms(m[np.abs(m).mean(1) > 1e-6]) or 1e-9
    m = m * (ref * 10 ** (-music_under_db / 20) / mr) * (10 ** (-duck_db * env / 20))[:, None]
    raw, fin = tmp / "raw.wav", tmp / "fin.wav"
    write_wav(raw, cl + m)
    meas = two_stage(raw, fin, lufs, tp)
    mux(clean_mp4, fin, out)
    y, _ = read_wav(fin)
    rep = dict(file=out.name, from_clean=clean_mp4.name, engine="score.py + GeneralUser GS v2.0.3 (TinySoundFont)",
               rights="ORIGINAL_GENERATED", sections=[(round(a, 2), round(b, 2), mo) for a, b, mo in secs], notes=len(sco.events),
               key=key, bpm=bpm, seed=seed, **meas, clipped_samples=int((np.abs(y) >= .999).sum()),
               voice_over_music_db=round(float(20 * np.log10(ref / max(rms(m[sp]), 1e-9))), 1) if sp.any() else None)
    try:
        from voice_check import transcribe, wer
        heard = {}
        for name, src in (("clean", wav), ("scored", fin)):
            mono = tmp / f"{name}-mono.wav"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-ac", "1", "-ar", "24000", str(mono)], check=True)
            heard[name] = transcribe(str(mono))
        rep["wer_scored_vs_clean"] = round(float(wer(heard["clean"], heard["scored"])), 3)
        rep["heard_scored"] = heard["scored"]
    except Exception as e:                                       # the recogniser is optional; say so
        rep["wer_scored_vs_clean"] = f"not measured ({type(e).__name__})"
    try:
        import quality
        rep["dnsmos"] = quality.score(str(fin))
    except Exception as e:
        rep["dnsmos"] = f"not measured ({type(e).__name__})"
    json.dump(rep, open(out.with_suffix(".json"), "w"), indent=1)
    return rep


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "scored":
        args = sys.argv[3:]
        lu = float(args.pop(0)) if args and args[0].lstrip("-").replace(".", "").isdigit() else -14.0
        r = scored_alternative(sys.argv[2], moods=tuple(args) or ("explain", "resolve"), lufs=lu)
        print(json.dumps({k: v for k, v in r.items() if k != "heard_scored"}, indent=1))
    else:
        print(scored_alternative.__doc__)
