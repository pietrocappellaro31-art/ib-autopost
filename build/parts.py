"""Shared diagram pieces, so six carousels look like one account."""

from brand import INK, MUTE, RED, TEAL, WHITE


def cover(title, chips, kicker, chip_bg=WHITE, chip_fg=INK):
    """Cover slide: headline, chip row, one line of stake.

    Chips are white on red and ink grounds; pass chip_bg=INK, chip_fg=WHITE on
    a paper ground, where white chips would vanish.
    """
    row = "".join(
        f'<div style="transform:rotate({-4 + i * 3.5}deg);background:{chip_bg};color:{chip_fg};'
        f'padding:14px 24px;font-size:27px;font-weight:600;border-radius:11px;'
        f'box-shadow:0 9px 0 rgba(0,0,0,.18)">{c}</div>' for i, c in enumerate(chips))
    return ('<div style="display:flex;flex-direction:column;gap:40px">'
            f'<h1 style="font-size:112px">{title}</h1>'
            f'<div style="display:flex;flex-wrap:wrap;gap:15px;max-width:830px">{row}</div>'
            '<div class="body" style="font-size:36px;font-weight:500;opacity:.95;max-width:860px">'
            f'{kicker}</div></div>')


def stake(headline, body):
    """Ink slide that says why the question matters."""
    return ('<div style="display:flex;flex-direction:column;gap:34px">'
            f'<h1 style="font-size:88px">{headline}<span style="color:{RED}">.</span></h1>'
            f'<div class="body" style="font-size:40px;font-weight:500">{body}</div></div>')


def ladder(rows, total_label=None, total_value=None, total_colour=TEAL):
    """A stack of label/value lines with an optional ruled total."""
    out = ""
    for label, value, colour in rows:
        out += ('<div style="display:flex;justify-content:space-between;align-items:baseline;'
                'padding:12px 0;border-bottom:1px solid rgba(10,10,10,.12)">'
                f'<span style="font-size:30px;font-weight:400">{label}</span>'
                f'<span style="font-family:\'Serif\',serif;font-weight:700;font-size:38px;'
                f'color:{colour}">{value}</span></div>')
    if total_label:
        out += ('<div style="display:flex;justify-content:space-between;align-items:baseline;'
                f'padding:15px 0 2px;border-top:3px solid {INK};margin-top:6px">'
                f'<span style="font-size:32px;font-weight:600">{total_label}</span>'
                f'<span style="font-family:\'Serif\',serif;font-weight:700;font-size:48px;'
                f'color:{total_colour}">{total_value}</span></div>')
    return f'<div class="card">{out}</div>'


def steps(items):
    """A numbered horizontal chain, for anything that happens in order."""
    cells = ""
    for i, t in enumerate(items, 1):
        cells += (f'<div style="flex:1;border:3px solid {INK};border-radius:14px;padding:16px 8px;'
                  f'text-align:center;background:{WHITE}">'
                  f'<div style="font-family:\'Serif\',serif;font-weight:700;font-size:34px;'
                  f'color:{RED}">{i}</div>'
                  f'<div style="font-size:23px;font-weight:600;line-height:1.2;margin-top:4px">'
                  f'{t}</div></div>')
    return f'<div class="card"><div style="display:flex;gap:10px;align-items:stretch">{cells}</div></div>'


def bars(series, caption=None):
    """Labelled bar chart. series is (label, relative_height, colour).

    Heights are normalised rather than used raw: the label sits under the bar
    inside the same column, so a raw height close to the container height
    pushes the column past it and the tallest bar breaks out of the card.
    """
    tallest = max(h for _, h, _ in series) or 1
    body = "".join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px;flex:1;'
        f'justify-content:flex-end;height:100%">'
        f'<div style="width:100%;max-width:120px;height:{round(h / tallest * 162)}px;'
        f'background:{c};border-radius:5px 5px 0 0"></div>'
        f'<span style="font-size:23px;font-weight:600;opacity:.75;text-align:center;'
        f'line-height:1.15;min-height:54px">{l}</span></div>' for l, h, c in series)
    cap = (f'<div style="margin-top:12px;font-size:25px;font-weight:600;color:{TEAL};'
           f'text-align:center">{caption}</div>' if caption else "")
    return ('<div class="card"><div style="display:flex;align-items:flex-end;gap:16px;'
            f'height:230px">{body}</div>{cap}</div>')


def formula(parts):
    """One equation, large, with coloured terms. parts is (text, colour)."""
    body = "".join(
        f'<span style="color:{c}">{t}</span>' for t, c in parts)
    return ('<div class="card" style="text-align:center">'
            f'<div style="font-family:\'Serif\',serif;font-weight:700;font-size:46px;'
            f'line-height:1.35">{body}</div></div>')


def recap(title, items, accent="#5EC8B4"):
    """Ink recap slide: numbered list of the takeaways."""
    rows = ""
    for n, (head, tail) in enumerate(items, 1):
        rows += ('<div style="display:flex;gap:22px;align-items:flex-start;padding:14px 0;'
                 'border-top:1px solid rgba(255,255,255,.22)">'
                 f'<span style="font-family:\'Serif\',serif;font-weight:700;font-size:38px;'
                 f'color:{RED};width:34px;flex:none">{n}</span>'
                 f'<div style="flex:1"><div style="font-size:31px;line-height:1.25;'
                 f'font-weight:500">{head}</div>'
                 f'<div style="font-size:21px;font-weight:600;letter-spacing:.11em;'
                 f'text-transform:uppercase;color:{accent};margin-top:4px">{tail}</div></div></div>')
    rows += '<div style="border-top:1px solid rgba(255,255,255,.22)"></div>'
    return ('<div style="display:flex;flex-direction:column;gap:20px">'
            f'<h1 style="font-size:82px">{title}<span style="color:{RED}">.</span></h1>'
            f'<div>{rows}</div></div>')


def cta(headline, lines, tomorrow):
    """Red closing slide: the thing to remember, then what comes next."""
    body = "".join(
        f'<div style="display:flex;gap:18px;align-items:baseline">'
        f'<span style="font-family:\'Serif\',serif;font-weight:700;font-size:34px;'
        f'color:{RED};width:34px;flex:none">{i}</span>'
        f'<span style="font-size:29px;line-height:1.3">{t}</span></div>'
        for i, t in enumerate(lines, 1))
    return ('<div style="display:flex;flex-direction:column;gap:32px">'
            f'<h1 style="font-size:98px">{headline}</h1>'
            f'<div style="background:{WHITE};color:{INK};border-radius:16px;padding:32px 36px;'
            f'display:flex;flex-direction:column;gap:14px">{body}</div>'
            '<div class="body" style="font-size:34px;font-weight:500;opacity:.95">'
            f'{tomorrow}</div></div>')
