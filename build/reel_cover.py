"""
Grid-safe Reel covers (16 Nov 2026, Pietro: "when the reels get posted, the cover of the reel is not perfectly readable
or centred, or both, on the home page ... part of the thing written there is cut").

Why: Instagram's profile grid shows a Reel as a 3:4 crop from the middle of its 9:16 cover, so the top and bottom
240 px of a 1080 x 1920 cover are cut. Until 16 Nov the cover was a frame of the video, laid out for the Reel player
(text kept left of the right-hand action rail, header near the top), so on the grid the header was cut and the text
sat off to the left.

What this makes: a 1080 x 1920 cover designed for the grid tile, in the carousel covers' style so the grid reads as
one page: the IB mark and the series on top, the question large and centred in Source Serif, the level chips, the
handle and a Watch cue at the bottom, all inside the middle 1080 x 1440 band (y 240 to 1680) with an 80 px margin.
The ground follows the Reel's theme (ink for black Reels, paper otherwise). The render measures every text box and
refuses a cover with anything outside the band, and writes a 3:4 preview of exactly what the grid will show.

    python3 build/reel_cover.py <slug> [--title "Question?"] [--kicker "IB INTERVIEW LEVELS #16"] [--theme black]
        -> build/out/<slug>/cover_grid.jpg and cover_grid_preview.jpg (the 3:4 tile)

build/reel_queue.py calls make() for every Reel it queues, so the automatic posts always carry this cover.
"""
import argparse
import html as H
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "out"
FONTS = ROOT / "build" / "fonts"
INK, RED, TEAL, PAPER, TEAL_ON_INK = "#0A0A0A", "#D93A12", "#0F766E", "#F7F5F2", "#5EC8B4"
BAND = (240, 1680)           # what the 3:4 grid tile shows of a 1080 x 1920 cover
MARGIN = 80


def episode_for(slug):
    """Find the EP whose slug matches (the black variant shares its parent's file)."""
    base = re.sub(r"-black$", "", slug)
    for f in sorted((ROOT / "build").glob("*.py")):
        text = f.read_text(errors="ignore")
        if f'slug="{base}"' in text or f"slug='{base}'" in text:
            spec = importlib.util.spec_from_file_location("ep_" + f.stem.replace("-", "_"), f)
            m = importlib.util.module_from_spec(spec)
            sys.path.insert(0, str(ROOT / "build"))
            try:
                spec.loader.exec_module(m)
            except SystemExit:
                pass
            return getattr(m, "EP", None)
    return None


def page(title, kicker, chips, theme, hl, lead=""):
    ground, fg, sub = (INK, "#FFFFFF", "rgba(255,255,255,.72)") if theme == "black" else (PAPER, INK, "rgba(10,10,10,.68)")
    t = H.escape(title)
    for w in hl or []:                                   # the key words in red, as on the Reel
        t = t.replace(H.escape(w), f'<span style="color:{RED}">{H.escape(w)}</span>', 1)
    chip_html = "".join(f'<span class="chip">{H.escape(c)}</span>' for c in chips)
    n = len(title)
    size = 132 if n <= 40 else 116 if n <= 56 else 100 if n <= 74 else 88
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Serif';src:url('{(FONTS / "serif700.woff2").as_uri()}') format('woff2');font-weight:700}}
@font-face{{font-family:'Sans';src:url('{(FONTS / "sans400.woff2").as_uri()}') format('woff2');font-weight:400}}
@font-face{{font-family:'Sans';src:url('{(FONTS / "sans500.woff2").as_uri()}') format('woff2');font-weight:500}}
@font-face{{font-family:'Sans';src:url('{(FONTS / "sans600.woff2").as_uri()}') format('woff2');font-weight:600}}
html,body{{margin:0;width:1080px;height:1920px;background:{ground};overflow:hidden}}
.band{{position:absolute;left:{MARGIN}px;right:{MARGIN}px;top:{BAND[0] + 60}px;bottom:{1920 - BAND[1] + 60}px;
  display:flex;flex-direction:column;justify-content:space-between;font-family:'Sans',sans-serif;color:{fg}}}
.top{{display:flex;justify-content:space-between;align-items:center;font-size:30px;font-weight:600;letter-spacing:.14em}}
.mark{{font-family:'Serif',serif;font-weight:700;font-size:46px;letter-spacing:0;margin-right:22px}}
.mid{{display:flex;flex-direction:column;align-items:center;text-align:center;gap:44px}}
.q{{font-family:'Serif',serif;font-weight:700;font-size:{size}px;line-height:1.06;letter-spacing:-.02em;text-wrap:balance}}
.chips{{display:flex;gap:18px;flex-wrap:wrap;justify-content:center}}
.chip{{background:#FFFFFF;color:{INK};border-radius:14px;padding:12px 26px;font-size:34px;font-weight:600;
  box-shadow:0 6px 0 rgba(0,0,0,.25)}}
.lead{{font-size:40px;color:{sub};font-weight:500}}
.bottom{{display:flex;justify-content:space-between;align-items:center;font-size:32px;font-weight:600}}
.watch{{color:{RED}}}
</style></head><body><div class="band">
<div class="top"><span><span class="mark">IB<span style="color:{RED}">.</span></span><span class="k">{H.escape(kicker)}</span></span></div>
<div class="mid"><div class="q">{t}</div><div class="chips">{chip_html}</div>
{f'<div class="lead">{H.escape(lead)}</div>' if lead else ''}</div>
<div class="bottom"><span>@investmentbankinginterviews</span><span class="watch">Watch &#9654;</span></div>
</div></body></html>"""


def render(html_text, out_jpg):
    from playwright.sync_api import sync_playwright
    src = out_jpg.with_suffix(".html")
    src.write_text(html_text)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(src.resolve().as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        boxes = pg.evaluate("""[...document.querySelectorAll('.band *')].filter(e => e.childElementCount === 0 || e.classList.contains('q'))
            .map(e => { const r = e.getBoundingClientRect(); return {t: e.className || e.tagName, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom}; })""")
        pg.screenshot(path=str(out_jpg.with_suffix(".png")), full_page=False)
        b.close()
    from PIL import Image
    im = Image.open(out_jpg.with_suffix(".png")).convert("RGB")
    im.save(out_jpg, quality=92)
    im.crop((0, BAND[0], 1080, BAND[1])).resize((540, 720)).save(out_jpg.with_name("cover_grid_preview.jpg"), quality=90)
    out_jpg.with_suffix(".png").unlink()
    bad = [bx for bx in boxes if bx["y0"] < BAND[0] + 20 or bx["y1"] > BAND[1] - 20 or bx["x0"] < 40 or bx["x1"] > 1040]
    return boxes, bad


def make(slug, title=None, kicker=None, theme=None, chips=None):
    ep = episode_for(slug) or {}
    hook = ep.get("hook", {})
    if title is None and hook.get("say"):
        title = " ".join(screen for _, screen in hook["say"])
    if not title:
        raise SystemExit(f"no title for {slug}: pass --title")
    kicker = kicker or ep.get("kicker", "IB INTERVIEW")
    theme = theme or ("black" if slug.endswith("-black") else ep.get("theme", "paper"))
    hl = [w.rstrip("?.!") for w in hook.get("hl", [])]
    quiz = bool(ep.get("levels"))                       # the chips and the line belong to the Levels quiz only
    if chips is None:
        chips = [f"Level {i + 1}" for i in range(len(ep["levels"]))] if quiz else []
    lead = (hook.get("sub") or "") if quiz else ""
    out = OUT / slug
    out.mkdir(parents=True, exist_ok=True)
    jpg = out / "cover_grid.jpg"
    boxes, bad = render(page(title, kicker, chips, theme, hl, lead), jpg)
    if bad:
        raise SystemExit(f"cover text outside the grid band: {json.dumps(bad)[:400]}")
    return jpg


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--title")
    ap.add_argument("--kicker")
    ap.add_argument("--theme")
    a = ap.parse_args()
    print(make(a.slug, a.title, a.kicker, a.theme))
