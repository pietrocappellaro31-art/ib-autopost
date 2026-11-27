# w3-depreciation-cash (Instagram Reel, the first full-frame animated Reel)

- Platform: Instagram Reel, posted automatically by publish.py on 27 Nov 2026, slot B (18:00 ET), with the AI label (is_ai_generated) and the first comment. Not a Trial Reel.
- Concept: the superday question "depreciation goes up $10, what happens to cash?": pre-tax profit -10, tax -2.50 at 25%, net income -7.50, depreciation added back +10, cash +2.50. Standard interview assumptions, stated in the caption (25% tax, tax follows the books, nothing else changes). No source needed beyond the accounting identity; no statistic, quote or real company.
- Our arithmetic (episode docstring): 10 x 25% = 2.50; -10 + 2.50 = -7.50; -7.50 + 10 = +2.50; balance sheet PP&E -10, cash +2.50, retained earnings -7.50.
- Script: ours (build/reelf_depreciation.py). Story and characters invented: an interview room at an unnamed bank, two invented people. No real person's likeness.
- Voice: HEART, synthetic (Kokoro af_heart, Apache 2.0, en-us, speed 0.9). Imitates nobody. New PHONEMES entry: "superday".
- Master: one clean master, voice and effects only (-16.0 LUFS, -1.8 dBTP, 0 clipped samples, DNSMOS SIG 3.65, recogniser word error 0 on the whole master).
- Music: none in the file. Instagram attaches "Breath Between Thoughts" (Lucent Hours) at posting through the Instagram Audio API, which returns only tracks Meta has authorised for third-party use (docs: developers.facebook.com/docs/instagram-platform/content-publishing/audio-api). The track is licensed by Instagram for use on Instagram only; it is never downloaded, stored or put in any of our files. Not for paid partnerships or ads (the track is not ads-eligible).
- Sound effects: synthesised in build/sfx.py (marker, paper, stamp, soft hits, coin clinks, office room tone). No whoosh.
- Visuals and fonts: ours, drawn in build/reel_film.py and the episode (cine.py engine). Source Serif 4, IBM Plex Sans (SIL OFL). No logos, no photos.
- Educational only; no advice or forecast.
- Disclosure: caption ends with "Narration: AI-generated voice; script is our original work."; Instagram's AI label set at publishing.
- Approval: automatic posting per Pietro's 16 Nov decision; format, cadence, music route and Trial Reels per his 26 Nov decisions (docs/decisions-log.md).
