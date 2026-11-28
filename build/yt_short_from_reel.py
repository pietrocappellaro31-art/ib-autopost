"""
YouTube Short from an Instagram Reel (27 Nov 2026, Pietro: "for the short youtube video make sure to use the same
reels. Simply when you produce the instagram reels, please provide the same description and tabs for youtube").

The Reel's picture, unchanged. Its file has voice and effects only (Instagram adds its licensed track at posting), so
the YouTube copy gets a track from Pietro's music library under the voice (Pietro, 27 Nov: "Use our library"; the IB
Music Library artifact, Pixabay tracks of class LICENSED_FOR_ALL_REQUIRED_PLATFORMS): picked by the Reel's mood, never
the same track as the last 3 days' Shorts, cut from its calm_start, faded, ducked under speech, -14 LUFS
(master.library_alternative), credited "Music: <title> by <artist> (Pixabay)" in the description. The audio must be
in build/music_library/audio/ (load it from the artifact with the ib-music-access skill: read_file on files.json, then
the track's paths, join .pNN parts in order, check sha256). --score uses our original score instead.

Text: the Reel's caption as the description (same words), with the Instagram follow line turned into a subscribe line
and the music credit added; #Shorts first among at most three hashtags; tags from the hashtags and the hook; title =
the caption's first line (the hook), at most 100 characters (aim under 70).

    python3 build/yt_short_from_reel.py <slug> [--mood curious]
writes build/out/<slug>/<slug>-youtube.mp4 and build/out/<slug>/youtube.txt (title, description, tags)
    python3 build/yt_short_from_reel.py <slug> --film --mood story
a long film: <slug>-clean.mp4 with library music as <slug>-music.mp4, credits added to description.txt
"""

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))

MOODS = ("explain", "resolve")
SUBSCRIBE = "Subscribe for a new IB interview question, worked out, every day."
MUSIC = "Music: original score made for this video."
AUDIO = HERE / "music_library" / "audio"


def _secs(x):
    if isinstance(x, (int, float)):
        return float(x)
    m, sec = str(x or "0:00").split(":")
    return int(m) * 60 + float(sec)


def credit_line(t):
    import re as _re
    q = _re.search(r'"(Music: [^"]+)"', t.get("note", ""))
    return q.group(1) if q else f"Music: {t['title']} by {t['artist']} (Pixabay)"


def choose_track(slug, mood="curious", track_id=None, avoid_days=3):
    """The mixable library track nearest the mood, not used by a Short in the last avoid_days days."""
    import datetime
    import music_library as ML
    lib = ML.load()
    ok = [t for t in lib["tracks"] if ML.mixable(t, "youtube")]
    if track_id:
        t = next(t for t in ok if t["id"] == track_id)
    else:
        e, v = ML.MOODS[mood]
        today = datetime.date.today()
        recent = {u["id"] for u in lib.get("used", []) if u.get("kind") == "short" and u.get("slug") != slug
                  and (today - datetime.date.fromisoformat(u["date"])).days < avoid_days}
        t = min(ok, key=lambda t: (t["energy"] - e) ** 2 + (t["valence"] - v) ** 2 + (.5 if t["id"] in recent else 0))
    lib["used"] = [u for u in lib.get("used", []) if u.get("slug") != slug] + [
        dict(date=str(datetime.date.today()), slug=slug, kind="short", id=t["id"], mood=mood)]
    ML.save(lib)
    return t


def youtube_text(caption, music_line=MUSIC):
    lines = caption.strip().splitlines()
    title = lines[0].strip()
    if len(title) > 100:
        title = title[:97].rsplit(" ", 1)[0] + "..."
    tags_ig = re.findall(r"#(\w+)", caption)
    body = [l for l in lines if not re.fullmatch(r"\s*(#\w+\s*)+", l)]
    out = []
    for l in body:
        if l.lower().startswith("follow @"):
            out.append(SUBSCRIBE)
        else:
            out.append(l)
    desc = "\n".join(out).rstrip()
    desc = desc.replace("Narration: AI-generated voice; script is our original work.",
                        music_line + "\nNarration: AI-generated voice; script is our original work.")
    if music_line not in desc:
        desc += "\n\n" + music_line
    desc += "\nEducational only, not financial advice."
    hashtags = ["#Shorts"] + [f"#{t}" for t in tags_ig[:2]]
    desc += "\n\n" + " ".join(hashtags)
    words = re.sub(r"[^A-Za-z0-9 ]", " ", title).lower().split()
    tags = list(dict.fromkeys(tags_ig + ["investment banking interview", "ib interview questions", "finance interview",
                                         "accounting interview questions", " ".join(words[:6])]))
    return dict(title=title, description=desc, tags=[t for t in tags if t][:15])


def main(slug, mood="curious", track_id=None, score=False):
    import master
    work = HERE / "out" / slug
    clean = work / f"{slug}.mp4"
    if not clean.exists():
        raise SystemExit(f"no Reel master at {clean}")
    cap = (HERE / "captions" / f"{slug}.txt").read_text()
    out = work / f"{slug}-youtube.mp4"
    if score:
        rep = master.scored_alternative(clean, moods=MOODS, out=out, lufs=-14.0)
        line, music = MUSIC, dict(kind="original score", style=rep.get("style_label") or rep.get("style"), key=rep.get("key"))
        wer_key = "wer_scored_vs_clean"
    else:
        t = choose_track(slug, mood, track_id)
        mp3 = AUDIO / t["file"]
        if not mp3.exists():
            raise SystemExit(f"LOAD THE TRACK FIRST: {t['file']} ({t['title']} by {t['artist']}) is not in {AUDIO}. "
                             "Use the ib-music-access skill: read_file on the IB Music Library artifact "
                             "(slug 331a2c60-239a-4b00-acd3-dffde353a56a) files.json, then the track's paths; join .pNN parts "
                             f"in order; check sha256 {t.get('sha256', '')[:12]}...; then run this again.")
        line = credit_line(t)
        rep = master.library_alternative(clean, mp3, start_s=_secs(t.get("calm_start")), out=out, lufs=-14.0, credit=line)
        music = dict(kind="library", id=t["id"], title=t["title"], artist=t["artist"], mood=mood, start=t.get("calm_start"))
        wer_key = "wer_music_vs_clean"
    text = youtube_text(cap, line)
    text["music"] = music
    text["checks"] = {k: rep.get(k) for k in ("lufs", "true_peak", "clipped_samples", wer_key, "voice_over_music_db") if k in rep}
    (work / "youtube.json").write_text(json.dumps(text, indent=1))
    (work / "youtube.txt").write_text(f"TITLE\n{text['title']}\n\nDESCRIPTION\n{text['description']}\n\nTAGS\n{', '.join(text['tags'])}\n")
    print(json.dumps({k: v for k, v in text.items() if k != "description"}, indent=1))
    return out, text


def film(slug, mood="story"):
    """A long film's delivered file with library music (Pietro, 27 Nov): build/out/<slug>/<slug>-clean.mp4 gets the
    best track for the mood from its calm_start, and a second track of the same mood with a crossfade if the first runs
    out; writes <slug>-music.mp4 and adds the credit lines to description.txt above the narration line."""
    import datetime
    import master
    import music_library as ML
    work = HERE / "out" / slug
    clean = work / f"{slug}-clean.mp4"
    total = float(subprocess_out(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(clean)]))
    first = choose_track(slug, mood)
    chosen, cover = [first], first["duration_s"] - _secs(first.get("calm_start"))
    lib = ML.load()
    e, v = ML.MOODS[mood]
    for t in sorted((t for t in lib["tracks"] if ML.mixable(t, "youtube") and t["id"] != first["id"]),
                    key=lambda t: (t["energy"] - e) ** 2 + (t["valence"] - v) ** 2):
        if cover >= total:
            break
        chosen.append(t)
        cover += t["duration_s"] - _secs(t.get("calm_start")) - 2.5
    missing = [t["file"] for t in chosen if not (AUDIO / t["file"]).exists()]
    if missing:
        raise SystemExit(f"LOAD THESE TRACKS FIRST from the IB Music Library artifact (ib-music-access skill): {missing}")
    lines = [credit_line(t) for t in chosen]
    out = work / f"{slug}-music.mp4"
    rep = master.library_alternative(clean, [(AUDIO / t["file"], _secs(t.get("calm_start"))) for t in chosen], out=out,
                                     lufs=-14.0, tp=-1.0, credit="; ".join(lines))
    desc = work / "description.txt"
    if desc.exists():
        d = desc.read_text()
        d = "\n".join(l for l in d.splitlines() if not l.startswith("Music: original score"))
        anchor = "Narration: AI-generated voice"
        d = d.replace(anchor, "\n".join(lines) + "\n" + anchor, 1) if anchor in d else d + "\n" + "\n".join(lines)
        desc.write_text(d)
    print(json.dumps(dict(file=str(out), tracks=[t["id"] for t in chosen], credits=lines,
                          checks={k: rep.get(k) for k in ("lufs", "true_peak", "clipped_samples", "wer_music_vs_clean", "voice_over_music_db")}), indent=1))
    return out, lines


def subprocess_out(cmd):
    import subprocess
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--mood", default="curious", help="calm reflective melancholy curious warm hopeful playful upbeat tense dark dramatic story")
    ap.add_argument("--track", help="a library track id, to override the pick")
    ap.add_argument("--score", action="store_true", help="our original score instead of a library track")
    ap.add_argument("--film", action="store_true", help="a long film: <slug>-clean.mp4 gets library music, <slug>-music.mp4")
    a = ap.parse_args()
    if a.film:
        film(a.slug, a.mood if a.mood != "curious" else "story")
    else:
        main(a.slug, a.mood, a.track, a.score)
