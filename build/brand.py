"""
Shared slide primitives for @investmentbankinginterviews.

Every carousel in the week is built from these, so the account reads as one
designed thing rather than fourteen separate posts. The rules here come from
the brand system and from mistakes already made and fixed:

- Chromium's --window-size yields a viewport about 80px shorter than asked,
  so slides are rendered at 1080x1500 and cropped to 1080x1350. Without this
  every slide silently loses its bottom padding, which is invisible on a pale
  ground and ruins the post.
- Header and footer must be position:absolute. An inline position:relative on
  the footer overrides the class and drops it into the flow, where it collides
  with the body text.
- The handle is @investmentbankinginterviews. It shipped once as a working
  name and was caught only by inspecting the live account.
"""

import pathlib
import subprocess

from PIL import Image

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"
OUT = HERE / "out"

INK = "#0A0A0A"
RED = "#D93A12"        # the mistake, the warning, the accent
TEAL = "#0F766E"       # the correct answer; chosen over green because red/green
PAPER = "#F7F5F2"      # is the one pair colourblind readers cannot separate
WHITE = "#FFFFFF"
MUTE = "#C9C4BC"

HANDLE = "@investmentbankinginterviews"

CSS = """<!doctype html><html lang="en"><head><meta charset="utf-8"><style>
@font-face{font-family:'Serif';src:url('FONTS/serif700.woff2') format('woff2');font-weight:700}
@font-face{font-family:'Sans';src:url('FONTS/sans400.woff2') format('woff2');font-weight:400}
@font-face{font-family:'Sans';src:url('FONTS/sans500.woff2') format('woff2');font-weight:500}
@font-face{font-family:'Sans';src:url('FONTS/sans600.woff2') format('woff2');font-weight:600}
html,body{margin:0;padding:0}
.slide{width:1080px;height:1350px;box-sizing:border-box;padding:76px 80px;font-family:'Sans',sans-serif;
 display:flex;flex-direction:column;justify-content:center;overflow:hidden;position:relative}
h1{margin:0;font-family:'Serif',serif;font-weight:700;line-height:1.04;letter-spacing:-.03em}
.hdr{position:absolute;left:80px;right:80px;top:72px;display:flex;justify-content:space-between;
 align-items:center;z-index:3;font-size:26px;font-weight:600;letter-spacing:.13em;text-transform:uppercase}
.ftr{position:absolute;left:80px;right:80px;bottom:72px;display:flex;justify-content:space-between;
 align-items:center;font-size:26px;font-weight:600;z-index:3}
.logo{font-family:'Serif',serif;font-weight:700;font-size:40px;letter-spacing:-.03em;line-height:1}
.pill{display:inline-block;border-radius:999px;padding:9px 24px;font-size:24px;font-weight:600;
 letter-spacing:.1em;text-transform:uppercase;color:#FFF}
.body{font-size:33px;line-height:1.34;font-weight:400}
.ghost{position:absolute;right:-30px;bottom:150px;font-family:'Serif',serif;font-weight:700;
 font-size:400px;line-height:1;letter-spacing:-.05em;opacity:.05}
.card{background:#FFF;border:3px solid #0A0A0A;border-radius:18px;padding:26px 24px}
</style></head><body>"""

ARROW = ('<svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
BOOKMARK = ('<svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M6 3h12v18l-6-4-6 4z"/></svg>')


class Deck:
    """One carousel. Collects slides, then renders and crops them."""

    def __init__(self, slug, series, total):
        self.slug = slug
        self.series = series
        self.total = total
        self.slides = []

    # --- slide construction -------------------------------------------------

    def slide(self, bg, fg, inner, cue="Swipe", icon=ARROW, accent=RED, ghost=None):
        n = len(self.slides) + 1
        ghost_html = f'<div class="ghost" style="color:{fg}">{ghost}</div>' if ghost else ""
        self.slides.append(
            CSS.replace("FONTS/", f"{FONTS}/")
            + f'<div class="slide" style="background:{bg};color:{fg}">{ghost_html}'
            f'<div class="hdr"><span style="display:flex;align-items:center;gap:18px">'
            f'<span class="logo">IB<span style="color:{accent}">.</span></span>'
            f'<span style="opacity:.6">{self.series}</span></span>'
            f'<span style="color:{accent}">{n:02d} / {self.total:02d}</span></div>'
            f'<div style="position:relative;z-index:2;padding:40px 0;max-height:1040px">{inner}</div>'
            f'<div class="ftr"><span>{HANDLE}</span>'
            f'<span style="display:flex;align-items:center;gap:14px;color:{accent}">{cue} {icon}</span>'
            f'</div></div></body></html>'
        )
        return self

    def qa(self, question, keyword, diagram, answer, mistake, size=80):
        """A question slide: headline, diagram of the mechanism, answer, mistake."""
        n = len(self.slides) + 1
        h = question.replace(keyword, f'<span style="color:{TEAL}">{keyword}</span>', 1) if keyword else question
        h = h[:-1] + f'<span style="color:{RED}">{h[-1]}</span>'
        return self.slide(PAPER, INK, ghost=f"{n:02d}", inner=(
            '<div style="display:flex;flex-direction:column;gap:22px">'
            f'<h1 style="font-size:{size}px">{h}</h1>{diagram}'
            f'<div><span class="pill" style="background:{TEAL}">The answer</span>'
            f'<div class="body" style="margin-top:12px">{answer}</div></div>'
            f'<div><span class="pill" style="background:{RED}">Common mistake</span>'
            f'<div class="body" style="margin-top:12px;font-size:31px">{mistake}</div></div></div>'))

    # --- rendering ----------------------------------------------------------

    def render(self):
        """Render every slide to a cropped JPEG and verify the bottom edge."""
        OUT.mkdir(exist_ok=True)
        work = OUT / self.slug
        work.mkdir(exist_ok=True)
        paths = []

        for i, doc in enumerate(self.slides, 1):
            html = work / f"s{i:02d}.html"
            html.write_text(doc)
            png = work / f"{self.slug}-{i:02d}.png"
            subprocess.run([
                "/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu",
                "--hide-scrollbars", "--allow-file-access-from-files",
                "--force-device-scale-factor=1", "--window-size=1080,1500",
                f"--screenshot={png}", f"file://{html}",
            ], check=True, capture_output=True)

            # Crop away the phantom rows Chromium leaves, then ship JPEG:
            # the Content Publishing API rejects PNG.
            jpg = work / f"{self.slug}-{i:02d}.jpg"
            image = Image.open(png).convert("RGB").crop((0, 0, 1080, 1350))
            image.save(jpg, quality=92, optimize=True)
            png.unlink()
            html.unlink()
            paths.append(jpg)

        return paths


def check(paths, expected_total):
    """Fail loudly on the failure modes that are invisible to the eye."""
    problems = []
    if len(paths) != expected_total:
        problems.append(f"{len(paths)} slides rendered, expected {expected_total}")

    for p in paths:
        image = Image.open(p)
        if image.size != (1080, 1350):
            problems.append(f"{p.name}: {image.size}, expected (1080, 1350)")

        rgb = image.convert("RGB")
        # A clipped slide shows body text running into the bottom edge. Sample
        # the row just above the edge across its width: on a correct slide that
        # row is flat background, because the footer sits 72px higher.
        row = [rgb.getpixel((x, 1344)) for x in range(60, 1020, 20)]
        if len(set(row)) > 3:
            problems.append(f"{p.name}: bottom edge is not flat, content is clipped")

        if p.stat().st_size > 8_000_000:
            problems.append(f"{p.name}: {p.stat().st_size // 1024}KB, over the API limit")

    return problems
