"""
Daily Story: question of the day, for @investmentbankinginterviews.

One 1080x1920 JPEG per day. Each story answers yesterday's question at the
top and asks today's below, so the stories read as a chain and a viewer has a
reason to come back tomorrow. The API cannot add polls or other stickers, so
the image carries everything on its own.

Safe zones: Instagram's story UI covers roughly the top and bottom 12.5%, so
everything sits between y=250 and y=1650, with 84px side margins.

    python build/stories.py            render every story in STORIES
    python build/stories.py 2026-11-04 render one day
"""

import pathlib
import sys

from playwright.sync_api import sync_playwright

from motion import CSS, FONTS, HANDLE

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "images"

# date (Eastern) -> (question, answer). Every answer is worked through; no
# figures beyond the ones in the question.
STORIES = {
    "2026-11-04": ("A company issues $100 of debt. What changes on the balance sheet?",
                   "Cash goes up $100 on the asset side and debt goes up $100 on the liability side. "
                   "It balances, and nothing hits the income statement until interest is paid."),
    "2026-11-05": ("Can a company run negative working capital and still be healthy?",
                   "Yes. Retailers and subscription businesses often collect cash before they pay "
                   "suppliers or deliver, so payables and deferred revenue fund the business."),
    "2026-11-06": ("Why do you add back depreciation on the cash flow statement?",
                   "It's a non-cash expense. It reduced net income, but no cash left the business."),
    "2026-11-07": ("Which is usually higher: the cost of equity or the cost of debt?",
                   "The cost of equity. Shareholders are paid last and carry more risk, and interest "
                   "on debt is tax-deductible."),
    "2026-11-08": ("A company buys back shares with its cash. What happens to enterprise value?",
                   "In theory, nothing. Cash falls, and equity value falls by the same amount."),
    "2026-11-09": ("Why can't you use P/E for a company with negative earnings?",
                   "A negative P/E means nothing. Use EV/Revenue, or EV/EBITDA if EBITDA is positive."),
}

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>{css}
.sf{{position:absolute;left:84px;right:84px;top:250px;bottom:270px;display:flex;flex-direction:column}}
.ans{{background:rgba(94,200,180,.1);border:3px solid rgba(94,200,180,.45);border-radius:26px;padding:30px 34px}}
.ans .q{{font-size:32px;line-height:1.35;opacity:.65;margin-top:12px}}
.ans .a{{font-size:38px;line-height:1.35;font-weight:500;margin-top:14px}}
</style></head><body><div class="f">
<div class="sf">
 <div style="display:flex;justify-content:space-between;align-items:baseline">
  <div style="display:flex;align-items:baseline;gap:20px">
   <span style="font-family:Serif;font-weight:700;font-size:52px;letter-spacing:-.03em">IB<span class="r">.</span></span>
   <span class="lbl">Question of the day</span></div>
  <span class="lbl">{day}</span></div>
 {answer}
 <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
  <div class="num r" style="font-size:150px;line-height:.9">Q.</div>
  <h1 style="font-size:{qsize}px;margin-top:26px">{question}</h1>
 </div>
 <div style="display:flex;justify-content:space-between;align-items:center">
  <span class="lbl" style="color:#5EC8B4;opacity:1;white-space:nowrap">Answer in tomorrow&rsquo;s story</span>
  </div>
</div></div></body></html>"""

CHECK = """() => {
  const bad = [];
  document.querySelectorAll('.sf *').forEach(n => {
    if (!n.childNodes.length) return;
    const r = n.getBoundingClientRect();
    if (r.width && (r.left < 83 || r.right > 997 || r.top < 249 || r.bottom > 1651))
      bad.push(`${n.tagName} ${Math.round(r.left)},${Math.round(r.top)} to ${Math.round(r.right)},${Math.round(r.bottom)}`);
  });
  return bad;
}"""


def html_for(day):
    import datetime as dt
    d = dt.date.fromisoformat(day)
    question, _ = STORIES[day]
    prev = (d - dt.timedelta(days=1)).isoformat()
    answer = ""
    if prev in STORIES:
        pq, pa = STORIES[prev]
        answer = (f'<div class="ans" style="margin-top:56px"><span class="lbl" style="color:#5EC8B4;opacity:1">'
                  f"Yesterday&rsquo;s answer</span><div class=\"q\">{pq}</div><div class=\"a\">{pa}</div></div>")
    qsize = 84 if len(question) < 70 else 76
    css = CSS.replace("FONTS/", f"{FONTS.resolve()}/")
    return PAGE.format(css=css, day=f"{d:%a} {d.day} {d:%b}", answer=answer, question=question,
                       qsize=qsize, handle=HANDLE)


def render(days):
    OUT.mkdir(exist_ok=True)
    work = HERE / "out" / "stories"
    work.mkdir(parents=True, exist_ok=True)
    files = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 1080, "height": 1920})
        for day in days:
            src = work / f"{day}.html"
            src.write_text(html_for(day))
            pg.goto(src.resolve().as_uri())
            pg.evaluate("Promise.all([400, 500, 600].map(w => document.fonts.load(w + ' 40px Sans')).concat([document.fonts.load(\"700 40px 'Serif'\")]))")
            if pg.evaluate("[...document.fonts].filter(f => f.status === 'loaded').length") < 4:
                raise RuntimeError("brand fonts did not load")
            bad = pg.evaluate(CHECK)
            if bad:
                raise RuntimeError(f"{day}: outside the story safe zone: {bad}")
            out = OUT / f"story-{day}.jpg"
            out.write_bytes(pg.screenshot(type="jpeg", quality=92,
                                          clip={"x": 0, "y": 0, "width": 1080, "height": 1920}))
            files.append(out)
            print(f"  {out.name}")
        browser.close()
    return files


if __name__ == "__main__":
    render(sys.argv[1:] or sorted(STORIES))
