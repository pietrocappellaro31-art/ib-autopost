"""
Narrator check (13 Nov, cinematic upgrade): say a fixed set of finance lines in a voice, then measure
what can be measured without a human ear.

    python3 build/narrator_check.py                 # HEART (Kokoro af_heart at 0.9, the narrator)
    python3 build/narrator_check.py HEART GEORGE

For every line: word errors from the Parakeet recogniser (voice_check.wer), words per second, peak level
(clipping) and the longest silence inside the line. For the whole set: DNSMOS (quality.score).
Results print as a table and land in build/out/narrator-check/<VOICE>.json; the WAVs stay there for a
listening review. These numbers are supporting evidence only: a WER of 0 does not prove natural delivery,
and nobody should report a listening verdict unless someone actually listened.

The lines double as the pronunciation regression set: bank terms, acronyms, historical names, currency
and numbers said as words. A new word that the voice cannot say raises in voice.Voice.phonemes; add it to
voice.PHONEMES (see docs/production/audio-standard.md, "Pronunciation").
"""

import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from voice import SR, write_wav            # noqa: E402
from voice_clone import make_voice         # noqa: E402

LINES = [
    "In seventeen twenty, Isaac Newton bought back into the South Sea Company.",
    "A leveraged buyout, or LBO, uses debt to fund most of the purchase price.",
    "Bankers value the business with a DCF, then check it against EBITDA multiples.",
    "The internal rate of return, the IRR, fell from twenty percent to twelve.",
    "Its weighted average cost of capital, the WACC, was about eight percent.",
    "The share price rose from about three hundred and fifty pounds to eight hundred and ninety.",
    "Thomas Guy sold at six hundred pounds a share and founded a hospital in Southwark.",
    "John Aislabie, the Chancellor of the Exchequer, was later sent to prison.",
    "Revenue minus the cost of goods sold gives you gross profit.",
    "Amortization, accrued interest and a covenant breach all show up on the balance sheet.",
    "The yield on a ten year Treasury moved forty basis points in a week.",
    "Exchange Alley was full of people who had never owned a share before.",
]


def silence_gaps(a, hop=0.01, floor=0.006):
    n = int(hop * SR)
    rms = np.array([np.sqrt(np.mean(a[i:i + n] ** 2)) for i in range(0, max(len(a) - n, 1), n)])
    quiet, best, run = rms < floor, 0, 0
    for q in quiet[5:-5]:                     # ignore the 50 ms trims at both ends
        run = run + 1 if q else 0
        best = max(best, run)
    return round(best * hop, 2)


def check(name, lines=LINES):
    from voice_check import transcribe, wer
    import quality
    out = pathlib.Path(__file__).parent / "out" / "narrator-check" / name
    out.mkdir(parents=True, exist_ok=True)
    v = make_voice(name)
    rows, allaudio = [], []
    for i, text in enumerate(lines):
        a = v.say(text)
        p = out / f"{i:02d}.wav"
        write_wav(p, a)
        heard = transcribe(str(p))
        e = wer(text, heard)
        dur = len(a) / SR
        rows.append(dict(line=text, heard=heard, wer=round(float(e), 3), seconds=round(dur, 2),
                         wps=round(len(text.split()) / dur, 2), peak_db=round(20 * np.log10(np.abs(a).max() + 1e-9), 1),
                         longest_gap_s=silence_gaps(a)))
        allaudio += [a, np.zeros(int(.4 * SR), np.float32)]
    full = out / "all.wav"
    write_wav(full, np.concatenate(allaudio))
    q = quality.score(str(full))
    summary = dict(voice=name, lines=len(rows), exact=int(sum(r["wer"] == 0 for r in rows)),
                   mean_wer=round(float(np.mean([r["wer"] for r in rows])), 3),
                   mean_wps=round(float(np.mean([r["wps"] for r in rows])), 2),
                   max_peak_db=max(r["peak_db"] for r in rows), clipped=bool(any(r["peak_db"] >= -0.1 for r in rows)),
                   dnsmos=q, rows=rows)
    json.dump(summary, open(out.parent / f"{name}.json", "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    return summary


if __name__ == "__main__":
    for name in sys.argv[1:] or ["HEART"]:
        s = check(name)
        print(f"\n{name}: {s['exact']}/{s['lines']} exact, mean WER {s['mean_wer']}, {s['mean_wps']} words/s, "
              f"peak {s['max_peak_db']} dBFS, DNSMOS {s['dnsmos']}")
        for r in s["rows"]:
            flag = "" if r["wer"] == 0 else f"   heard: {r['heard']}"
            print(f"  {r['wer']:.2f} {r['wps']:.2f}w/s gap {r['longest_gap_s']}s  {r['line']}{flag}")
