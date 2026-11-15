# w2-levels-14 (IB Interview Levels #14, enterprise value vs equity value; HEART, cinematic standard)

- Platform: Instagram Reel, posted by hand by Pietro.
- Concept: EV = equity value + debt - cash (simplified bridge; preferred stock and non-controlling interests named in the docstring, none in the examples). L2 100 + 40 - 10 = 130; L3 borrow 50 and hold it as cash: +50 debt, +50 cash, EV unchanged at 130; L4 EV below equity value when cash exceeds debt (100 + 0 - 30 = 70). Bonus: 20 + 0 - 50 = -30. No earlier Reel on EV (topics.md).
- Script: ours. Every answer worked in build/reels_ev-vs-equity.py. Textbook definitions, round example numbers. No company, deal, statistic, "typical" figure or credential claimed.
- Voice: HEART, synthetic (Kokoro af_heart at 0.9, Apache 2.0). Not a real person. No Pocket TTS, so no Kyutai line. No de-noise or other processing on the narrator (audio-standard 1b).
- Visuals and fonts: ours, from the repo. Three level drawings from build/sketch.py (ev_whole, ev_bridge, ev_borrow, new today): a generic office block, a generic bank shape, stick figures, bars, a balance; no bank, company or logo. Two filmed beats from build/cine.py (cine_lib.office_today and the new cine_lib.monitor_ev): an invented office, no real person, firm or skyline, so no RECONSTRUCTION badge; the monitor shows only the worked numbers ($100, $0 debt, $30 cash, $70). Source Serif 4, IBM Plex Sans (SIL OFL; docs/rights/ledger.md). No stock, logos or AI images.
- Sound effects: synthesised in build/sfx.py and the cine.py foley; no whoosh.
- Music: none in the clean master (the deliverable; Pietro adds a track from Instagram's library in the app). Scored alternative w2-levels-14-scored.mp4: our own score.py cue (discover, resolve; GeneralUser GS v2.0.3 via TinySoundFont), class ORIGINAL_GENERATED, voice 18.5 dB over the music. No commercial or library music in any file.
- Disclosure: caption narration line; Instagram AI label recommended when posting (realistic synthetic voiceover; Meta asks for a label on realistic-sounding AI audio). The visuals are clearly drawn animation and need no label of their own.
- Claims: no statistics, no outcomes, no promise of returns or jobs. "in a lot of the examples you practise with it is" is a general remark, not a figure.
- Approval: Pietro posts by hand after reviewing the finished file.
