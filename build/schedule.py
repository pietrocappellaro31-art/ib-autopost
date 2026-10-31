"""
Add a finished post to the repo: copy its media in, append its manifest entry.

Usage:
    python3 schedule.py <slug> <scheduled_utc> [--reel]

The slug is the folder under out/ and the prefix of its files. Carousels take
every <slug>-NN.jpg in order; reels take <slug>.mp4 plus <slug>-cover.jpg.
Caption is read from captions/<short>.clean.txt.

Re-running with the same id replaces that entry rather than duplicating it,
so a post can be corrected and re-scheduled without hand-editing JSON.
"""

import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).parent
REPO = pathlib.Path(__file__).resolve().parent.parent


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)

    slug = sys.argv[1]
    scheduled = sys.argv[2]
    is_reel = "--reel" in sys.argv

    source = HERE / "out" / slug
    short = slug.split("-")[0] + "-" + slug.split("-")[1]      # w1-01
    caption_file = HERE / "captions" / f"{short}.clean.txt"
    if not caption_file.exists():
        sys.exit(f"no caption at {caption_file}")
    caption = caption_file.read_text().strip()

    images_dir = REPO / "images"
    images_dir.mkdir(exist_ok=True)

    entry = {
        "id": slug,
        "series": "Technical of the Day",
        "scheduled_utc": scheduled,
        "caption": caption,
        "published_id": None,
        "published_at_utc": None,
    }

    if is_reel:
        video = source / f"{slug}.mp4"
        cover = source / f"{slug}-cover.jpg"
        shutil.copy(video, images_dir / video.name)
        entry["video"] = video.name
        if cover.exists():
            shutil.copy(cover, images_dir / cover.name)
            entry["cover"] = cover.name
        carried = [video.name]
    else:
        slides = sorted(source.glob(f"{slug}-[0-9][0-9].jpg"))
        if not slides:
            sys.exit(f"no slides in {source}")
        for s in slides:
            shutil.copy(s, images_dir / s.name)
        entry["images"] = [s.name for s in slides]
        carried = entry["images"]

    manifest_path = REPO / "posts.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["posts"] = [p for p in manifest["posts"] if p.get("id") != slug]
    manifest["posts"].append(entry)
    manifest["posts"].sort(key=lambda p: p["scheduled_utc"])
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    print(f"{slug}  {scheduled}  {len(carried)} file(s)  caption {len(caption)} chars")


if __name__ == "__main__":
    main()
