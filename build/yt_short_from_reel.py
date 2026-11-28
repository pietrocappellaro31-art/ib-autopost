"""
YouTube Short from an Instagram Reel (27 Nov 2026, Pietro: "for the short youtube video make sure to use the same
reels. Simply when you produce the instagram reels, please provide the same description and tabs for youtube").

The Reel's picture, unchanged. Its file has voice and effects only (Instagram adds its licensed track at posting), so
the YouTube copy gets our original score under the voice (master.scored_alternative: ORIGINAL_GENERATED, a different
style and key each video, ducked under speech, -14 LUFS for YouTube). That follows the 17 Nov YouTube rule (one file,
with our score) and keeps every licensed Instagram track off YouTube.

Text: the Reel's caption as the description (same words), with the Instagram follow line turned into a subscribe line
and the music credit added; #Shorts first among at most three hashtags; tags from the hashtags and the hook; title =
the caption's first line (the hook), at most 100 characters (aim under 70).

    python3 build/yt_short_from_reel.py <slug>
writes build/out/<slug>/<slug>-youtube.mp4 and build/out/<slug>/youtube.txt (title, description, tags)
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


def youtube_text(caption):
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
                        MUSIC + "\nNarration: AI-generated voice; script is our original work.")
    if MUSIC not in desc:
        desc += "\n\n" + MUSIC
    desc += "\nEducational only, not financial advice."
    hashtags = ["#Shorts"] + [f"#{t}" for t in tags_ig[:2]]
    desc += "\n\n" + " ".join(hashtags)
    words = re.sub(r"[^A-Za-z0-9 ]", " ", title).lower().split()
    tags = list(dict.fromkeys(tags_ig + ["investment banking interview", "ib interview questions", "finance interview",
                                         "accounting interview questions", " ".join(words[:6])]))
    return dict(title=title, description=desc, tags=[t for t in tags if t][:15])


def main(slug):
    import master
    work = HERE / "out" / slug
    clean = work / f"{slug}.mp4"
    if not clean.exists():
        raise SystemExit(f"no Reel master at {clean}")
    cap = (HERE / "captions" / f"{slug}.txt").read_text()
    out = work / f"{slug}-youtube.mp4"
    rep = master.scored_alternative(clean, moods=MOODS, out=out, lufs=-14.0)
    text = youtube_text(cap)
    text["music"] = dict(style=rep.get("style_label") or rep.get("style"), key=rep.get("key"), bpm=rep.get("bpm"))
    text["checks"] = {k: rep.get(k) for k in ("lufs", "true_peak", "clipped_samples", "wer_scored_vs_clean") if k in rep}
    (work / "youtube.json").write_text(json.dumps(text, indent=1))
    (work / "youtube.txt").write_text(f"TITLE\n{text['title']}\n\nDESCRIPTION\n{text['description']}\n\nTAGS\n{', '.join(text['tags'])}\n")
    print(json.dumps({k: v for k, v in text.items() if k != "description"}, indent=1))
    return out, text


if __name__ == "__main__":
    main(sys.argv[1])
