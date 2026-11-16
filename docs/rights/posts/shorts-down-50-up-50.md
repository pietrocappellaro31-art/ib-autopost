# shorts-down-50-up-50 (YouTube Short, Format C: one surprising concept)

- Platform: YouTube Short, uploaded by hand by Pietro. Not cross-posted to Instagram.
- Concept: a $100 stock that falls 50% and then rises 50% ends at $75. The rise is 50% of a smaller number, so getting back from a 50% fall takes a 100% gain; the same $50 is 50% of $100 and 100% of $50; the gain needed grows faster than the loss (10% needs about 11%, 80% needs 400%); the S&P 500's 2007 to 2009 fall of about 57% needed about 131% and took until 28 March 2013 to recover.
- Sources checked in the run (16 Nov 2026): Exceljet, "Required recovery rate" (formula and examples); Wikipedia, "United States bear market of 2007-2009" (closes 1,565.15 on 9 Oct 2007 and 676.53 on 9 Mar 2009, -56.78%); NPR, 28 Mar 2013 (record close at 1,569 erasing the 9 Oct 2007 record). Links in the description and the episode docstring.
- Our arithmetic (episode docstring, checked with a script): 100 x 0.5 x 1.5 = 75; gain needed 1 / (1 - loss) - 1; 1,565.15 / 676.53 - 1 = 131.4%. Closing prices, index level without dividends.
- Chart: the three real closes only; the line between them drawn smooth and labelled on screen "S&P 500 CLOSES (WIKIPEDIA, NPR), PATH SIMPLIFIED". The $100 stock of the puzzle is an illustration, not a real security.
- Script: ours (build/shorts_down-50-up-50.py).
- Reconstruction: none. The trader character (our own design) points at the bar in the hook and asks the question at the close; he plays nobody.
- Voice: HEART, synthetic (Kokoro af_heart, Apache 2.0, en-us, speed 0.9). Imitates nobody.
- Masters: clean only (voice, effects, room tone). No scored master (the day's task prompt: no scored master unless Pietro asks).
- Music: none in the master. Pietro may add a sound in the YouTube app at upload from YouTube's licensed Shorts library (suggestion: Pietro's library pick, REFERENCE_ONLY, used only through the app).
- Sound effects: synthesised in build/sfx.py (pop, tick, thump, clink, paper, soft knock, ding). No whoosh.
- Visuals and fonts: ours (Source Serif 4, IBM Plex Sans, SIL OFL). Drawings in build/sketch.py: gold money bars, price tags, arrows, a loss-to-gain bar ladder, a simplified line chart. No index provider's logo or chart, no photos, no real people.
- Index named: the S&P 500, as the historical source of the figures; the description says we are not affiliated with S&P Dow Jones Indices. Educational only; no advice, prediction or return claim.
- Disclosure: description ends with the narration line; not-financial-advice line present. Recommended: altered or synthetic content = Yes, for the realistic synthetic narrator (reasoning in qa.md); Made for kids = No.
- Approval: Pietro uploads by hand after reviewing the finished file.
