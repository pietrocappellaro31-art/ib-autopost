"""
Music library (12 Nov, Pietro: "attach all these audios to a library ... used for the creation of both
YouTube shorts and YouTube video. The video should pick from the library the most appropriate music.").

The tracks Pietro sends are commercial recordings. They never go into a master and the audio is never
committed: Content ID would claim the video (docs/decisions-log.md, 12 Nov). The library uses them
two lawful ways:

  1. Each video picks the best-fitting track for its mood. A Short gets that song as the first sound to
     add with "Add sound" in the YouTube app (YouTube licenses it for Shorts), with the start time
     of its calmest stretch. A long video gets the same pick in its upload notes, to add through
     YouTube's own tools if YouTube offers it there.
  2. A long video's own bed (music.py) is written in the picked track's tempo, key, mode and feel
     (drums or none, bright or dark). That way it sounds like it belongs with the song, and it stays
     wholly original: no melody, chords or audio are taken from the reference.

A track Pietro holds a real licence for can be marked "licence" (with the proof in docs/rights/ledger.md);
only those may ever be mixed into a master (mixable()).

    python3 build/music_library.py add <file.mp3> [...]     analyse and add (audio kept in the session only)
    python3 build/music_library.py set <id> title=.. artist=.. search=..   fix names after intake
    python3 build/music_library.py reanalyse                after a change to analyse()
    python3 build/music_library.py list                     the library, with each track's profile
    python3 build/music_library.py pick <mood> [--short]    the best track for a mood (e.g. calm, curious)

From an episode:  pick(mood, kind="short"|"long", slug=...) -> track dict;  bed(track, total_s, seed, breaks)
"""

import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
LIB = HERE / "music_library" / "library.json"
AUDIO = HERE / "music_library" / "audio"                  # gitignored: commercial audio is never committed
SR = 22050

# Krumhansl-Kessler key profiles.
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# What each video mood wants: energy and brightness (valence), 0 to 1.
MOODS = {
    "calm": (.2, .55), "reflective": (.25, .35), "melancholy": (.25, .2), "curious": (.45, .55),
    "warm": (.4, .7), "hopeful": (.45, .75), "playful": (.6, .8), "upbeat": (.75, .8),
    "tense": (.65, .25), "dark": (.55, .1), "dramatic": (.6, .3), "story": (.35, .45),
}


# ------------------------------------------------------------------ analysis

def _decode(path, seconds=600):
    """Mono float audio at 22.05 kHz, the first `seconds` (an hour-long loop needs no more)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-t", str(seconds), "-i", str(path), "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def _stft_mag(x, n=2048, hop=512):
    w = np.hanning(n).astype(np.float32)
    frames = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * w
    return np.abs(np.fft.rfft(frames, axis=1)), hop / SR


def analyse(path):
    """Tempo, key and mode, loudness, brightness, pulse, and the calmest and fullest 15 s stretches."""
    x = _decode(path)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                               capture_output=True, text=True).stdout.strip() or len(x) / SR)
    mag, dt = _stft_mag(x)
    freqs = np.fft.rfftfreq(2048, 1 / SR)
    lm = np.log1p(100 * mag)
    flux = np.maximum(np.diff(lm, axis=0), 0).sum(1)
    flux = np.concatenate([[0], flux])
    onset = flux - np.convolve(flux, np.ones(16) / 16, "same")
    onset = np.maximum(onset, 0)

    # Tempo: autocorrelation of the onset envelope, 60 to 180 BPM, gently weighted towards 100.
    o = onset - onset.mean()
    ac = np.correlate(o, o, "full")[len(o) - 1:]
    ac /= ac[0] + 1e-9
    bpms = np.arange(60, 181)
    lags = 60 / bpms / dt
    vals = np.interp(lags, np.arange(len(ac)), ac)
    weight = np.exp(-.5 * (np.log2(bpms / 100) / .9) ** 2)
    k = int(np.argmax(vals * weight))
    bpm, pulse = int(bpms[k]), float(max(vals[k], 0))

    # Key: pitch-class energy from 55 Hz to 2 kHz against the major and minor profiles.
    band = (freqs > 55) & (freqs < 2000)
    pc = (np.round(12 * np.log2(freqs[band] / 440)) + 9) % 12
    chroma = np.array([mag[:, band][:, pc == i].sum() for i in range(12)])
    chroma /= chroma.sum() + 1e-9
    best = max(((np.corrcoef(chroma, np.roll(prof, i))[0, 1], i, mode)
                for i in range(12) for prof, mode in ((MAJ, "major"), (MIN, "minor"))))
    key_conf, key, mode = round(float(best[0]), 2), NOTES[best[1]], best[2]

    # Loudness, brightness, dynamics over 0.5 s blocks.
    blk = int(.5 / dt)
    rms = np.sqrt(np.mean(x[: len(x) // 11025 * 11025].reshape(-1, 11025) ** 2, 1) + 1e-12)
    db = 20 * np.log10(rms)
    cen = (mag * freqs).sum(1) / (mag.sum(1) + 1e-9)
    brightness = float(np.median(cen))

    # The calmest and the fullest 15 s, past the first 3 s and before the last 10 (not silence).
    win = 30                                                     # 30 blocks of 0.5 s
    on_blk = np.add.reduceat(onset, np.arange(0, len(onset), blk))[: len(db)]
    scores = []
    for i in range(6, max(7, len(db) - win - 50)):           # a 15 s clip that does not run into the ending
        seg_db, seg_on = db[i:i + win], on_blk[i:i + win]
        if seg_db.mean() < db.max() - 30:
            continue
        scores.append((float(seg_on.mean() / (on_blk.mean() + 1e-9) + (seg_db.mean() - np.median(db)) / 12), i * .5))
    calm = min(scores)[1] if scores else 0.0
    full = max(scores)[1] if scores else 0.0

    # Percussion: share of energy in the percussive part of a median-filter split (60 s from the middle).
    from scipy.ndimage import median_filter
    mid = len(mag) // 2
    seg = mag[max(0, mid - int(30 / dt)): mid + int(30 / dt), : 400]
    harm, perc_ = median_filter(seg, size=(17, 1)), median_filter(seg, size=(1, 17))
    perc = float((perc_ ** 2).sum() / ((perc_ ** 2).sum() + (harm ** 2).sum() + 1e-9))
    energy = float(np.clip(.3 * np.clip((bpm - 60) / 80, 0, 1) + .35 * np.clip((perc - .15) / .35, 0, 1)
                           + .2 * np.clip((np.median(db) + 26) / 16, 0, 1) + .15 * np.clip((brightness - 500) / 2000, 0, 1), 0, 1))
    pulse = round(perc, 2)                                       # "pulse" from here on means percussion share
    valence = float(np.clip((.6 if mode == "major" else .25) + .35 * np.clip((brightness - 1200) / 2200, -1, 1), 0, 1))
    return dict(duration_s=round(dur, 1), bpm=bpm, pulse=round(pulse, 2), key=key, mode=mode, key_confidence=key_conf,
                loudness_db=round(float(np.median(db)), 1), dynamics_db=round(float(np.percentile(db, 95) - np.percentile(db, 10)), 1),
                brightness_hz=round(brightness), energy=round(energy, 2), valence=round(valence, 2),
                calm_start=fmt(calm), full_start=fmt(full), tags=tags(energy, valence, bpm, pulse, mode))


def tags(energy, valence, bpm, pulse, mode):
    t = []
    t.append("slow" if bpm < 85 else "mid tempo" if bpm < 115 else "fast")
    t.append("drums" if pulse > .35 else "light rhythm" if pulse > .22 else "no drums")
    t.append("minor" if mode == "minor" else "major")
    t += [m for m, (e, v) in sorted(MOODS.items(), key=lambda kv: (kv[1][0] - energy) ** 2 + (kv[1][1] - valence) ** 2)[:3]]
    return t


def fmt(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


# ------------------------------------------------------------------ library

def load():
    return json.load(open(LIB)) if LIB.exists() else {"tracks": [], "used": []}


def save(lib):
    LIB.parent.mkdir(parents=True, exist_ok=True)
    json.dump(lib, open(LIB, "w"), indent=1, ensure_ascii=False)


def names_from_file(path):
    """Title and artist from the tags, else from the file name ("Artist - Title ...")."""
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format_tags=title,artist", "-of", "json", str(path)],
                         capture_output=True, text=True).stdout
    tg = json.loads(out or "{}").get("format", {}).get("tags", {})
    stem = re.sub(r"^[0-9a-f]{8}-", "", pathlib.Path(path).stem).replace("_", " ")
    junk = r"original kbps|official (music )?video|official visualizer|official audio|visualizer|lyrics?|\d+ hour loop|best part|tiktok"
    stem = re.sub(rf"\s*[-(•]*\s*({junk})\s*\)?", "", stem, flags=re.I).strip(" -•")
    title, artist = tg.get("title"), tg.get("artist")
    if not title:
        artist, _, title = stem.partition(" - ") if " - " in stem else ("", "", stem)
    return title.strip(), (artist or "").strip()


def add(paths, note=""):
    lib = load()
    known = {t["sha256"] for t in lib["tracks"]}
    AUDIO.mkdir(parents=True, exist_ok=True)
    for p in map(pathlib.Path, paths):
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h in known:
            print(f"  already in the library: {p.name}")
            continue
        title, artist = names_from_file(p)
        tid = re.sub(r"[^a-z0-9]+", "-", f"{artist} {title}".lower()).strip("-")[:48]
        dest = AUDIO / f"{tid}{p.suffix.lower()}"
        dest.write_bytes(p.read_bytes())
        a = analyse(dest)
        lib["tracks"].append(dict(id=tid, title=title, artist=artist, file=dest.name, sha256=h,
                                  added=str(datetime.date.today()), rights="reference", note=note, **a))
        known.add(h)
        print(f"  + {tid}: {a['bpm']} BPM, {a['key']} {a['mode']}, energy {a['energy']}, valence {a['valence']}, "
              f"calm from {a['calm_start']}  [{', '.join(a['tags'])}]")
    save(lib)
    return lib


def reanalyse():
    """Re-run the analysis on every track in place (after a change to analyse()), keeping ids, rights and use."""
    lib = load()
    for t in lib["tracks"]:
        t.update(analyse(AUDIO / t["file"]))
    save(lib)
    return lib


def pick(mood, kind="long", slug=None, avoid_days=3, record=True):
    """The track closest to the mood (a name from MOODS, or (energy, valence)). A track used in the last
    `avoid_days` days for the same kind is passed over while another fits nearly as well."""
    lib = load()
    if not lib["tracks"]:
        return None
    e, v = MOODS[mood] if isinstance(mood, str) else mood
    today = datetime.date.today()
    recent = {u["id"] for u in lib["used"] if u["kind"] == kind and (today - datetime.date.fromisoformat(u["date"])).days < avoid_days}

    def score(t):
        s = (t["energy"] - e) ** 2 + (t["valence"] - v) ** 2
        if kind == "short" and t["duration_s"] < 30:
            s += 1
        return s + (.05 if t["id"] in recent else 0)
    best = min(lib["tracks"], key=score)
    if record and slug:
        lib["used"] = [u for u in lib["used"] if u.get("slug") != slug] + [dict(date=str(today), slug=slug, kind=kind, id=best["id"], mood=mood if isinstance(mood, str) else list(mood))]
        save(lib)
    return dict(best, others=[t["id"] for t in sorted(lib["tracks"], key=score)[1:3]])


def set_fields(tid, **fields):
    """Correct a track's names after intake (an uploader's name in the artist tag, a "Visualizer" in the
    title) and set `search`, the words to type in YouTube's "Add sound"."""
    lib = load()
    t = next(t for t in lib["tracks"] if t["id"] == tid)
    t.update(fields)
    save(lib)
    return t


def mixable(track):
    """Only a track with a recorded licence may go into a master."""
    return track.get("rights") == "licence"


def bed(track, total_s, seed=1, breaks=(), level=.9):
    """An original bed (music.py) in the reference's tempo, key, mode and feel. The tempo is folded into
    the bed's comfortable range (70 to 110 BPM) by halving or doubling."""
    import music
    bpm = track["bpm"]
    while bpm > 110:
        bpm /= 2
    while bpm < 70:
        bpm *= 2
    x, info = music.track(total_s, seed=seed, breaks=breaks, level=level, bpm=round(bpm), key=track["key"],
                          mode=track["mode"], drums=track["pulse"] > .22, bell=track["brightness_hz"] > 1500)
    info.update(reference=track["id"], reference_title=f"{track['title']} - {track['artist']}".strip(" -"))
    return x, info


def instructions(track, kind="short", volume="15 to 25"):
    """The lines for the delivery: what to search, where to start, how loud."""
    name = track.get("search") or f"{track['title']} - {track['artist']}".strip(" -")
    if kind == "short":
        return (f"From your music library: {name} ({', '.join(track['tags'][:3])}). In \"Add sound\" search \"{name}\"; "
                f"start the clip at {track['calm_start']} (its calmest stretch), volume {volume}.")
    return (f"From your music library: {name}. Our bed is already written in its tempo and key "
            f"({track['bpm']} BPM, {track['key']} {track['mode']}). Use the song itself only through YouTube's "
            f"own tools, and only if YouTube offers it for this video.")


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["list"]
    if cmd == "add":
        add(rest)
    elif cmd == "set":                                   # set <id> title=... artist=... search=... rights=...
        print(set_fields(rest[0], **dict(kv.split("=", 1) for kv in rest[1:])))
    elif cmd == "reanalyse":
        reanalyse()
    elif cmd == "pick":
        t = pick(rest[0], "short" if "--short" in rest else "long", record=False)
        print(json.dumps({k: t[k] for k in ("id", "title", "artist", "bpm", "key", "mode", "energy", "valence", "calm_start", "tags", "others")}, indent=1))
    else:
        for t in load()["tracks"]:
            print(f"{t['id']:<44} {t['bpm']:>4} BPM  {t['key']:>2} {t['mode']:<5}  energy {t['energy']:.2f}  valence {t['valence']:.2f}  "
                  f"calm {t['calm_start']:>5}  {t['rights']:<9} {', '.join(t['tags'])}")
