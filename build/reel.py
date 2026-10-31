"""
Reel builder for @investmentbankinginterviews.

A reel is a list of beats. Each beat has a line that gets spoken and a frame
that gets shown while it is spoken, so the cut timing is driven by the audio
rather than guessed. Output is a 1080x1920 H.264/AAC MP4 ready for the
Content Publishing API.

Why there is a voiceover at all: the API cannot attach a trending track to a
reel, and a silent reel is throttled. Baking speech into the file is the only
way to ship a reel through this pipeline that Instagram will actually push.

Safe area, from the brand system: nothing above y=230 or below y=1440, and
the right 230px stay clear of the UI overlay.
"""

import json
import pathlib
import re
import subprocess

from PIL import Image

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"
OUT = HERE / "out"

INK = "#0A0A0A"
RED = "#D93A12"
TEAL = "#5EC8B4"       # lifted for contrast on ink, the darker 0F766E dies here
PAPER = "#F7F5F2"
WHITE = "#FFFFFF"

HANDLE = "@investmentbankinginterviews"

CSS = """<!doctype html><html lang="en"><head><meta charset="utf-8"><style>
@font-face{font-family:'Serif';src:url('FONTS/serif700.woff2') format('woff2');font-weight:700}
@font-face{font-family:'Sans';src:url('FONTS/sans400.woff2') format('woff2');font-weight:400}
@font-face{font-family:'Sans';src:url('FONTS/sans500.woff2') format('woff2');font-weight:500}
@font-face{font-family:'Sans';src:url('FONTS/sans600.woff2') format('woff2');font-weight:600}
html,body{margin:0;padding:0}
.f{width:1080px;height:1920px;box-sizing:border-box;background:BG;color:FG;position:relative;
 font-family:'Sans',sans-serif;overflow:hidden}
.safe{position:absolute;left:84px;right:244px;top:230px;bottom:480px;
 display:flex;flex-direction:column;justify-content:center}
h1{margin:0;font-family:'Serif',serif;font-weight:700;line-height:1.03;letter-spacing:-.03em;
 font-size:104px}
.sub{font-size:44px;line-height:1.3;font-weight:500;margin-top:34px}
.mark{position:absolute;left:84px;top:132px;font-family:'Serif',serif;font-weight:700;
 font-size:52px;letter-spacing:-.03em}
.tag{position:absolute;left:84px;bottom:300px;font-size:34px;font-weight:600;opacity:.75}
.bar{position:absolute;left:84px;right:244px;bottom:240px;height:8px;border-radius:4px;
 background:rgba(255,255,255,.18)}
.bar i{display:block;height:8px;border-radius:4px;background:ACC}
.card{background:rgba(255,255,255,.07);border:3px solid rgba(255,255,255,.22);
 border-radius:22px;padding:34px 32px;margin-top:40px}
.row{display:flex;justify-content:space-between;align-items:baseline;padding:16px 0;
 border-bottom:1px solid rgba(255,255,255,.14);font-size:42px;font-weight:500}
.row b{font-family:'Serif',serif;font-weight:700;font-size:50px}
</style></head><body>"""


def frame(inner, progress, bg=INK, fg=WHITE, accent=RED):
    """One full-bleed 1080x1920 frame."""
    css = (CSS.replace("FONTS/", f"{FONTS}/").replace("BG", bg)
              .replace("FG", fg).replace("ACC", accent))
    return (css
            + f'<div class="f">'
            f'<div class="mark">IB<span style="color:{accent}">.</span></div>'
            f'<div class="safe">{inner}</div>'
            f'<div class="tag">{HANDLE}</div>'
            f'<div class="bar"><i style="width:{progress:.0f}%"></i></div>'
            f'</div></body></html>')


def shoot(html, png):
    """Render a frame, cropping away the rows Chromium silently withholds."""
    subprocess.run([
        "/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu",
        "--hide-scrollbars", "--allow-file-access-from-files",
        "--force-device-scale-factor=1", "--window-size=1080,2100",
        f"--screenshot={png}", f"file://{html}",
    ], check=True, capture_output=True)
    image = Image.open(png).convert("RGB")
    if image.size[1] < 1920:
        raise RuntimeError(f"{png.name}: only {image.size[1]}px tall, cannot crop to 1920")
    image.crop((0, 0, 1080, 1920)).save(png)


def reading_seconds(text, min_beat=2.6, max_beat=4.8):
    """How long a frame needs to stay up to be read comfortably.

    Silent reels are read, not heard, so beat length comes from word count
    rather than from speech. The cap matters more than the formula: a frame
    held longer than about five seconds reads as a stall, and the whole reel
    wants to land near thirty seconds so a trending clip fits over it.
    """
    words = len(re.findall(r"[\w'%-]+", text))
    return max(min_beat, min(max_beat, words / 3.2 + 0.9))


def build(slug, beats):
    """Render every beat and mux them into one silent 1080x1920 MP4.

    No audio stream at all. The reel is uploaded by hand and a trending track
    is added in the Instagram app, which is the one thing the publishing API
    cannot do and the one thing that matters most for reach on this format.
    """
    work = OUT / slug
    work.mkdir(parents=True, exist_ok=True)

    durations, pngs = [], []
    for i, (read_text, inner) in enumerate(beats, 1):
        progress = 100 * i / len(beats)
        html = work / f"b{i:02d}.html"
        html.write_text(frame(inner, progress))
        png = work / f"b{i:02d}.png"
        shoot(html, png)
        html.unlink()

        seconds = reading_seconds(read_text)
        durations.append(seconds)
        pngs.append(png)
        print(f"  beat {i}: {seconds:4.1f}s  {read_text[:58]}")

    vlist = work / "video.txt"
    vlist.write_text("".join(
        f"file '{p.name}'\nduration {d:.3f}\n" for p, d in zip(pngs, durations))
        + f"file '{pngs[-1].name}'\n")

    mp4 = work / f"{slug}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-f", "concat", "-safe", "0", "-i", str(vlist),
        "-an",                                   # no audio stream
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-vf", "scale=1080:1920,format=yuv420p",
        "-movflags", "+faststart", str(mp4),
    ], check=True, cwd=work)

    cover = work / f"{slug}-cover.jpg"
    Image.open(pngs[0]).convert("RGB").save(cover, quality=92)

    vlist.unlink()

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size:stream=codec_name,width,height",
         "-of", "json", str(mp4)], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    print(f"  -> {mp4.name}  {float(info["format"]["duration"]):.1f}s  "
          f"{int(info["format"]["size"]) // 1024}KB  silent")
    return mp4, cover
