# w2-fifo-lifo (Reel, Format F: a choice, FIFO or LIFO with rising prices; HEART, story engine, black)

- Platform: Instagram Reel, posted automatically by publish.py at slot B (Pietro, 16 Nov: two Reels a day, no approval; the content-compliance gate is the gate).
- Concept: units bought at $10 then $12, one sold for $20. FIFO: cost $10, profit $10, the $12 unit stays in inventory. LIFO: cost $12, profit $8, the $10 unit stays. Rising prices: LIFO shows less profit, so less tax (25%: $2.50 vs $2.00, 50 cents on one sale). US GAAP allows LIFO; IFRS does not. Close asks falling prices ($10 then $8: LIFO shows more profit, not given); comment bonus: weighted average ($11 cost, $9 profit). Not in topics.md "Used".
- Sources opened in the run: IAS Plus, IAS 2 Inventories (LIFO removed in the 2003 revision; FIFO or weighted average permitted) https://www.iasplus.com/standard/ias02.htm ; KPMG, Inventory accounting: IFRS Standards vs US GAAP (LIFO permitted under US GAAP, prohibited under IFRS) https://advisory.kpmg.us/articles/2021/inventory-accounting.html
- Script: ours, every number worked in build/reels_fifo-lifo.py. A worked illustration with round numbers of our own; no company, statistic or credential claimed. The tax line is limited to rising prices and one sale; the LIFO conformity rule is noted in the docstring, not said.
- Voice: HEART, synthetic (Kokoro af_heart at 0.9, Apache 2.0). Not a real person. Natural chain only.
- Visuals and fonts: ours. Seven drawings new today in build/sketch.py (fl_hook, fl_both, fl_fifo, fl_lifo, fl_tax, fl_rules, fl_asks): crates with price tags on a shelf, a till, profit columns to scale (30 px a dollar) with 25% tax caps, a coin, two rule books (generic, no logos). Source Serif 4, IBM Plex Sans (SIL OFL).
- Sound effects: synthesised (build/sfx.py), each on a visible action; no whoosh.
- Music: the posted file is the scored master: our own build/score.py cue (ORIGINAL_GENERATED). Clean master kept as the fallback. No commercial or platform-library music.
- Disclosure: caption narration line; Instagram's AI label set at creation by the publisher (is_ai_generated). AI label recommended: the narrator is synthetic.
- Claims: no outcomes, returns, jobs, tax or accounting advice; the tax example is arithmetic on stated assumptions.
- Gate: see the 18 Nov IG Reels row in docs/daily/quality-log.md for the measures; PASS recorded there only if every gate passed.
