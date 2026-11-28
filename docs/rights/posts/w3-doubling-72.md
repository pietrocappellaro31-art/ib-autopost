# w3-doubling-72 (Instagram Reel, full-frame animated, home desk set)

- Platform: Instagram Reel, made 28 Nov 2026 for slot A (12:30 ET) but NOT queued: build/reel_queue.py still allows one Reel per Eastern day and the change to two a day was not made in this run. Waits for Pietro (queue it with the same caption, comment and track, or post by hand with the AI label). Not a Trial Reel.
- Concept: $10,000 at 8% a year doubles in about 9 years, not 12.5: simple interest ($800 a year, 10,000 / 800 = 12.5) is the wrong answer; with the interest reinvested year 1 adds $800, year 2 $864; 10,000 x 1.08^9 = $19,990.05; the rule of 72 (a standard approximation): 72 / 8 = 9 (exact ln 2 / ln 1.08 = 9.006). Close (asked, not answered): 6% a year (72 / 6 = 12; 1.06^12 = 2.012). Comment bonus: 12% (72 / 12 = 6; 1.12^6 = 1.974). An invented example, stated as such in the caption; no market data, statistic, quote or real company.
- Our arithmetic: episode docstring and _check() in build/reelf_doubling.py (asserted at build time).
- Script: ours (build/reelf_doubling.py). Story and character invented: an analyst at a home desk, her first bonus; the street outside is invented.
- Voice: EMMA, synthetic (Kokoro bf_emma, Apache 2.0, speed 0.97), the 27 Nov to 4 Dec narrator (Pietro, 27 Nov). Imitates nobody. No new PHONEMES entries.
- Master: one clean master, voice, room tone and effects only (-16.0 LUFS, -1.8 dBTP, 0 clipped samples, DNSMOS SIG 3.65, recogniser word error 0 on every line and on the whole master).
- Music: none in the file. Instagram attaches "Lofi Memoir" (Adam Griffith) at posting through the Instagram Audio API, which returns only tracks Meta has authorised for third-party use. Licensed by Instagram for use on Instagram only; never downloaded, stored or put in any of our files. Not for paid partnerships or ads. (Content-compliance 4b: PASS.)
- Sound effects: synthesised in build/sfx.py (hits, marker, paper, stamp, coin clinks, tap, room tone).
- Visuals and fonts: ours, drawn in build/reel_film.py (home_desk and hero_desk, new 28 Nov) and the episode (cine.py engine). Source Serif 4, IBM Plex Sans (SIL OFL). No logos, no photos, no real person's likeness.
- Educational only; no advice, forecast or promised return.
- Disclosure: caption ends with "Narration: AI-generated voice; script is our original work."; Instagram's AI label set at publishing (realistic synthetic voiceover).
- Approval: automatic posting per Pietro's 16 Nov decision; format, cadence, music route and Trial Reels per his 26 and 27 Nov decisions (docs/decisions-log.md).

Release checklist: original value PASS (the rule of 72 not a Reel topic before; the 12 Nov YouTube Short mentioned it in another format); facts PASS; rights PASS; no music in the master PASS; voice EMMA (recorded window) PASS; reconstructions N/A; AI label recommended ON (realistic synthetic narrator) PASS; sponsorship N/A; title, cover, caption, hashtags accurate PASS; Pietro's approval: standing (16 Nov).
