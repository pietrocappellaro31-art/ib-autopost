# Scene library

13 Nov 2026. The reusable finance scene families, what each is for, and what builds it today. "cine" = `build/cine.py`
plus `build/cine_lib.py`; "sketch" = `build/sketch.py` drawings in the existing engine; "levels" = `build/levels.py`.
"To build" marks the next components worth adding (one per daily improvement is a good pace).

| | Family | Use it for | Built with today | To build |
|---|---|---|---|---|
| A | Historical reconstruction | a real moment in finance history, badged RECONSTRUCTION | cine: `street_1720`, `study_1720`, crowds, 1700s looks, newspaper, letter, quill, certificate | a trading pit, a 1900s bank hall, a 1980s trading floor, a 2008 office at night |
| B | Financial mechanism | money moving through a system | cine: coins between jars, numbers lifting off a document; sketch: `flow`, `t_account`, `multiplier`, `outflow` | pipes and tanks for cash flow; an LBO structure where debt and equity fill a purchase price |
| C | Data reveal | a chart that tells the story as it is said | cine: `price_line` (draws on, flags, riding counter, sourced x positions, dashed unknowns); sketch: `chart`, `bars`, `price_path` | stacked bars that rearrange; a log-scale toggle explained on screen |
| D | Decision point | a real trade-off, one choice at a time | cine: a figure reading, reacting, writing the order; sketch: `scale`, `seesaw` | a split-screen with two futures diverging |
| E | Comparison | two outcomes side by side | sketch: `compare`, `split`, `cent_or_million`, `coin_stacks` | two filmed lives side by side (same set, two grades) |
| F | Calculation | a number built step by step with units | levels quiz answers; sketch: `interest_stack`, `markup_tag`, `doubling_bars`; motion `count` | a calculator tape that prints each step; a DCF timeline discounting year by year |
| G | Visual metaphor | an abstract idea made physical | sketch: `bubble`, `tower`, `dominoes`, `hourglass72`, `wall` | a balance that tips with leverage; ice melting for inflation |
| H | Character action | a person doing the thing the narration says | cine rig: walk, sit, read, write, point, reach, hold up, cheer, shrug, concern, talk | stand up and sit down helpers; hand poses; phone in hand; a 3/4 view |
| I | Document explanation | a letter, filing, contract or statement whose key line matters | cine: `letter` with ink reveal and a hand that follows the nib; `newspaper` price list | a 10-K page with a highlighter sweep; a term sheet with clauses lifting off |
| J | Chapter transition | a restrained change of chapter with topic art | existing red chapter cards with a drawing; cine: push into an object and match, dissolve, cut on action | a page turn; a door; light change from day to night |
| K | Quiz interaction | timers, choices, reveals, level meter | levels (the four-level format); a filmed hook (`levels.film_hook`, hook `film=`; first used on Levels #12: an analyst at his desk, his screen builds the DCF) | the film blurred with the card at the swipe; a filmed answer beat |
| L | Cinematic conclusion | the takeaway made visible | cine: the price path with the decision marked and the future dashed | a slow pull-back from the key object to the whole scene |

1960s and 1970s, ready in `cine_1971.py` (14 Nov): sets `living_room_1971` (a console TV; `tv_screen(items=, quote=)` puts
numbered items or a quote card on its screen), `vault_1971` (cages of gold bars, a counter, a vault door), `dealing_room`
(a split-flap board whose rows count on cue, `desk_phone` handsets that jiggle when they ring), `lodge_1971` (an easel
whose items write themselves on cue); props `gold_bar`, `bar_stack`, `dollar_bundle`, `dollar_bill` (generic), `typewriter`;
looks `suit_1971` to `suit_1971d`, `home_1971`, `lady_1971`; foley `ring`, `clank`, `flap`, `office_ambience`. Data in
the world: `vault_gap` draws two quantities at one honest scale as physical columns.

Modern objects ready in cine_lib: `phone`, `card`, `terminal`, `ledger_book`, `cup`; set `office_today` (an analyst's desk at dusk) and `monitor_dcf` (a DCF on screen, bars then the terminal-value block). Modern looks: `modern_navy`,
`modern_grey`.

Rules: each scene has a teaching purpose stated in the visual plan; reconstructions are badged; data comes from the
docstring's sources; no bank logos; red is the accent, not the crowd.
