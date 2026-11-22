"""
Queue a finished Reel for automatic posting (16 Nov 2026, Pietro: "We will post two each day. You won't need my
approval. ... You will decide at what time to post each day").

    python3 build/reel_queue.py <slug> --slot A|B|C [--date YYYY-MM-DD] [--master scored|clean] [--dry-run]
                                [--caption build/captions/<slug>.txt] [--comment "the comment question"]

What it does, in order, and it stops at the first failed check:
  1. Picks the master: the scored one (build/out/<slug>/<slug>-scored.mp4) when it exists and its report passed
     (words within 5% of the clean file, loudness within 1 LU of -16, true peak at or under -1.0 dBTP); otherwise the clean one.
     Instagram music cannot be added by a person any more, so the scored file is the default.
  2. Checks the file Instagram will get: H.264 and AAC, 1080 x 1920, 3 to 90 seconds, under 100 MB, audio present.
  3. Checks the caption: present, at most 2,200 characters, at most 5 hashtags, the AI-narration line, no em dash.
  4. Makes the cover with build/reel_cover.py (designed for the 3:4 profile-grid tile: everything inside y 240 to
     1680, centred; a video frame is never the cover) unless --cover is given.
  5. Pushes the video and the cover to a temporary branch reel/<slug> (one commit, no history; main never holds an
     MP4). The publisher deletes the branch once the Reel is live.
  6. Adds the entry to posts.json at the slot's time (America/New_York) and commits it to main.

The slots live in posts.json "reel_slots_et" so a run can move them from the performance data
(docs/daily/performance.md) and record why in docs/decisions-log.md. The publisher posts at or after the slot, sets
Instagram's AI label (is_ai_generated) and posts the comment question as the page's first comment.
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "out"
MANIFEST = ROOT / "posts.json"
ET = ZoneInfo("America/New_York")
DEFAULT_SLOTS = {"A": "12:30", "B": "18:00", "C": "21:00"}      # C: 22 Nov, three Reels a day
AI_LINE = "Narration: AI-generated voice; script is our original work."


def run(*cmd, cwd=ROOT, check=True):
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)


def probe(mp4):
    r = run("ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height:format=duration,size",
            "-of", "json", str(mp4))
    j = json.loads(r.stdout)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), {})
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), {})
    return dict(vcodec=v.get("codec_name"), w=v.get("width"), h=v.get("height"), acodec=a.get("codec_name"),
                dur=float(j["format"]["duration"]), mb=int(j["format"]["size"]) / 1e6)


def pick_master(slug, want):
    work = OUT / slug
    clean = work / f"{slug}.mp4"
    scored = work / f"{slug}-scored.mp4"
    if want in (None, "scored") and scored.exists():
        rep = json.loads((work / f"{slug}-scored.json").read_text()) if (work / f"{slug}-scored.json").exists() else {}
        # 16 Nov: within 5% of the clean file's transcript, the long-video gate's figure. On Levels #15 the 2.6% left
        # was all formatting ("$7.50." against "750.", "four" against "4", commas), not a changed word.
        w = rep.get("wer_scored_vs_clean")
        ok = (isinstance(w, (int, float)) and w <= .05 and abs(rep.get("lufs", 0) + 16) <= 1.0
              and rep.get("true_peak", 0) <= -1.0 and rep.get("clipped_samples", 1) == 0)
        if ok:
            return scored, "scored"
        if want == "scored":
            sys.exit(f"scored master failed its checks: {rep}")
        print(f"scored master not used (checks: {rep and {k: rep.get(k) for k in ('wer_scored_vs_clean', 'lufs', 'true_peak')}})")
    if not clean.exists():
        sys.exit(f"no master in {work}")
    return clean, "clean"


def check_video(mp4):
    p = probe(mp4)
    problems = []
    if p["vcodec"] != "h264" or p["acodec"] != "aac":
        problems.append(f"codecs {p['vcodec']}/{p['acodec']} (need h264/aac)")
    if (p["w"], p["h"]) != (1080, 1920):
        problems.append(f"size {p['w']}x{p['h']} (need 1080x1920)")
    if not 3 <= p["dur"] <= 90:
        problems.append(f"length {p['dur']:.1f} s (3 to 90)")
    if p["mb"] >= 100:
        problems.append(f"{p['mb']:.0f} MB (under 100)")
    return p, problems


def check_caption(text):
    problems = []
    if not text.strip():
        problems.append("empty caption")
    if len(text) > 2200:
        problems.append(f"{len(text)} characters (at most 2,200)")
    tags = re.findall(r"(?<!\w)#\w+", text)
    if len(tags) > 5:
        problems.append(f"{len(tags)} hashtags (at most 5)")
    if AI_LINE not in text:
        problems.append("missing the AI-narration line")
    if "—" in text:
        problems.append("em dash")
    return problems


def push_media_branch(slug, files, dry):
    branch = f"reel/{slug}"
    if dry:
        return branch
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="reelq-"))
    try:
        run("git", "init", "-q", str(tmp))
        for src, name in files:
            shutil.copy(src, tmp / name)
        run("git", "add", "-A", cwd=tmp)
        run("git", "-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "commit", "-q", "-m",
            f"Media for Reel {slug} (temporary; deleted after posting)", cwd=tmp)
        url = run("git", "remote", "get-url", "origin").stdout.strip()
        r = run("git", "push", "-q", url, f"HEAD:refs/heads/{branch}", cwd=tmp, check=False)
        if r.returncode:
            sys.exit(f"push of {branch} failed: {r.stderr.strip()[:400]}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return branch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--slot", choices=["A", "B", "C"], required=True)
    ap.add_argument("--date", help="Eastern date, default today")
    ap.add_argument("--master", choices=["scored", "clean"])
    ap.add_argument("--caption")
    ap.add_argument("--comment", default="")
    ap.add_argument("--cover", help="a ready 1080 x 1920 cover; default: build/reel_cover.py makes a grid-safe one")
    ap.add_argument("--title", help="cover title, default the Reel's hook question")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text())
    slots = manifest.get("reel_slots_et", DEFAULT_SLOTS)
    day = date.fromisoformat(a.date) if a.date else datetime.now(ET).date()
    hh, mm = map(int, slots[a.slot].split(":"))
    when_utc = datetime.combine(day, time(hh, mm), ET).astimezone(ZoneInfo("UTC"))

    master, kind = pick_master(a.slug, a.master)
    p, problems = check_video(master)
    cap_path = pathlib.Path(a.caption) if a.caption else ROOT / "build" / "captions" / f"{a.slug}.txt"
    caption = cap_path.read_text().strip() if cap_path.exists() else ""
    problems += check_caption(caption)
    # 16 Nov (Pietro: the cover on the profile grid was cut and off centre): every queued Reel gets a cover designed
    # for the 3:4 grid tile (build/reel_cover.py), unless --cover names another file; a video frame is never used.
    if a.cover:
        cover = pathlib.Path(a.cover)
    else:
        import reel_cover
        cover = reel_cover.make(a.slug, title=a.title)
    print(f"cover: {cover} (grid tile preview: {cover.with_name('cover_grid_preview.jpg')})")
    if problems:
        sys.exit("NOT QUEUED: " + "; ".join(problems))
    pid = f"reel-{a.slug}"
    if any(x["id"] == pid for x in manifest["posts"]):
        sys.exit(f"{pid} is already in posts.json")

    files = [(master, f"{a.slug}.mp4")] + ([(cover, f"{a.slug}.jpg")] if cover else [])
    branch = push_media_branch(a.slug, files, a.dry_run)
    entry = dict(id=pid, type="reel", scheduled_utc=when_utc.strftime("%Y-%m-%dT%H:%M:%S"), slot=a.slot,
                 media_branch=branch, video=f"{a.slug}.mp4", cover=f"{a.slug}.jpg" if cover else None,
                 master=kind, caption=caption, first_comment=a.comment.strip(), ai_label=True, published_id=None)
    if not cover:
        entry.pop("cover")
        entry["thumb_offset_ms"] = 1500
    print(json.dumps({k: v for k, v in entry.items() if k != "caption"}, indent=1))
    print(f"video: {p['w']}x{p['h']} {p['vcodec']}/{p['acodec']}, {p['dur']:.1f} s, {p['mb']:.1f} MB, master {kind}")
    if a.dry_run:
        print("dry run: nothing pushed or written")
        return
    manifest["posts"].append(entry)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"queued {pid} for {slots[a.slot]} ET on {day} ({entry['scheduled_utc']} UTC). Commit posts.json and push.")


if __name__ == "__main__":
    main()
