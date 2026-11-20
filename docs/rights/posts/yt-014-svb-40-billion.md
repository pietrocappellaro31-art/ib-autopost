# yt-014-svb-40-billion (YouTube long-form #14, 20 Nov 2026)

- Platform: YouTube long-form (16:9), uploaded by hand by Pietro. Nothing posted or scheduled by Claude.
- Concept: Silicon Valley Bank, March 2023. Over $40 billion of deposits left in one day (9 March), with over
  $100 billion more expected the next; most of what the bank owned was bonds. The film explains, with our own round
  numbers, why a bond that never misses a payment loses value when rates rise (a $100, 10-year, 1.5% bond is worth
  about $79.72 once new bonds pay 4%), then SVB's growth ($71bn to over $211bn of assets, 2019 to 2021), its
  deposits ($173bn, $151.5bn estimated above the insurance limit), the held-to-maturity label ($91.3bn on the books,
  $76.2bn at market, against $16.0bn of equity), the 8 March announcement ($21bn sold, $1.8bn after-tax loss, $2.25bn
  sought), the run, the closure on 10 March, the 12 March joint statement and the Fed's own conclusions. Our point of
  view: safe from default is not safe from rates; the loss only matters if you have to sell, and a bank whose deposits
  can leave in a day may have to. Original analysis; no advice.
- Script: ours. Every fact sourced in `build/youtube_ep014.py` (docstring: the Federal Reserve's review of April 2023,
  executive summary and key takeaways; Michael Barr's Senate testimony of 28 March 2023; SVB Financial Group's 2022
  Form 10-K; the joint statement of 12 March 2023; FDIC press release 2023-16; American Banker, 9 March 2023) and
  linked in the description. Labelled as ours: the $100 bond and its $79.72 price, "more than half of everything it
  owned was bonds" (our sum on the 10-K), the readings in chapters 6, 8 and 9. Calculations in
  `build/plans/ep014_checks.py`.
- Quotes: short verbatim passages from Barr's testimony (one filmed document, one quote card, one term card), the
  Fed review's conclusion (paraphrased on a term card and attributed) and the joint statement (one term card). The
  filmed document is our own drawn page: only the passage is legible; no real letterhead, seal or logo (names in
  plain type).
- Real people and institutions named as facts: Michael Barr (as the author of the testimony); Silicon Valley Bank and
  SVB Financial Group, the Federal Reserve, the Treasury, the FDIC, the California Department of Financial Protection
  and Innovation, Washington Mutual and Wachovia (as the Fed review's comparisons). Named only, never shown or voiced.
  The description carries the educational-and-unaffiliated line.
- Logos and buildings: the branch front is our own generic drawing whose fascia says only BANK (no bank's name, logo,
  colours or building), badged "Reconstruction · not the real branch"; the notice on its door is badged "our
  illustration" and carries only what the record says (closed on 10 March 2023 by the California regulator, the FDIC
  appointed receiver). The phone in the hook is a generic news screen ("our illustration · not the real bank"); the
  office, its wall screen and the laptop are our illustrations, showing only the 10-K's and the Fed review's figures.
- Reconstructions: the branch door on 10 March; the office, the kitchen and the street ("Our illustration"). Every
  figure is a generic articulated figure (`cine.LOOKS` office_2023, office_2023b, office_2023c, new today, and the
  2021 looks); nobody is a portrait or a likeness; nobody speaks.
- Voice: HEART, synthetic (Kokoro af_heart, en-us, speed 0.9, Apache 2.0), the channel narrator. Not a real person,
  no cloning. The narrator does not claim to be a person.
- Music: one file (Pietro, 17 Nov): an original "suspense" score for this video by `build/score.py` (our own notes per
  chapter) in the style chosen by `score.pick` (named in `build/out/yt-014-svb-40-billion/music.json` and the
  delivery), on the GeneralUser GS SoundFont instruments (free for commercial music; class ORIGINAL_GENERATED); no
  third-party melody, recording or arrangement; ducked under the voice, level solved for 24 dB of voice over the music
  (`youtube.vom_level`). The clean mix exists only as the score gate's reference and is not delivered.
- Sound effects and ambience: synthesised in `build/sfx.py` (footsteps, paper, split-flap, clank, ticks, taps, buzz,
  mallet hits, city ambience, room tone). Action-timed in the drawn beats.
- Visuals: drawn by us in `build/sketch.py` and `build/youtube.py`, filmed in `build/cine.py` with `build/cine_2023.py`
  (new: bank_office_today, branch_front_today, bond_paper, wall_bars, rows_screen), `build/cine_2021.py` (street,
  kitchen, phone) and `cine_lib.document_shot`. Thumbnails use frames from our own filmed scenes, labelled
  RECONSTRUCTION. Fonts: Source Serif 4, IBM Plex Sans (SIL OFL).
- Disclosure: description ends with the music line, the AI-narration line and the not-financial-advice line. Studio:
  Altered or synthetic content / AI use = Yes recommended (reason in `docs/production/quality-gates.md` section 6);
  Made for kids = No.
- Claims: education, not investment advice; said in the narration and the description. No bank, product or return is
  recommended; the closing question asks for opinions on accounting rules.
- Approval: Pietro reviews the file before uploading.
