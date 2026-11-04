# Schedule and slot reasoning

Three posts a day. Carousels publish themselves; Reels are uploaded by hand so
a trending track can be added.

## Slots, Eastern

| Slot | Format | Why |
|---|---|---|
| 08:00 | Carousel | Before the day starts, and it breaks up the subject matter |
| 12:30 | Carousel | A save is a deliberate act and people are at a desk |
| 21:30 | Reel | Completion rate decides how far a Reel travels, and late evening is when nobody has anything queued after the scroll |

Nine hours separate the midday and evening posts so they never compete for the
same session. The most shareable piece of a week takes a Sunday evening slot,
because that is when people plan and forward things. Friday evening is the
weakest slot for this audience, so a Friday Reel moves to midday.

**These are hypotheses, not findings.** They are reasoned from how each format
is ranked, not measured on this account. Re-time from the account's own
insights after two or three weeks.

## Content logic

The first post promised two technical questions a day and named five questions
it would return to. The carousels deliver exactly those, in order, so the grid
reads as one body of work rather than scattered tips.

The mix across a week runs roughly nine technical, three recruiting, and two
built to pull comments, because people in this niche cannot resist correcting
each other.

Reels take the punchy, list-shaped and recruiting topics, which travel.
Carousels take the deep technical ones that need a diagram and earn a save.

## Reel slots after the 2 November re-space

The carousels moved when Meta blocked API access, so the Reel slots moved with
them. All at 21:30 Eastern, keeping three posts a day:

| Date | Reel |
|---|---|
| Tue 3 Nov | EV vs equity value |
| Wed 4 Nov | Eight words that give you away |
| Thu 5 Nov | Why investment banking |
| Fri 6 Nov | Five answers that get you dinged |
| Sat 7 Nov | Accretive or dilutive in five seconds |
| Sun 8 Nov | Summer 2028 is already open |
| Mon 9 Nov | Any questions for me |

The recruiting calendar keeps the Sunday evening slot: it is the most
shareable piece and Sunday night is when people plan and forward things. The
file names in the handover bundle carry the **old** dates, so go by this table.

## Week 1, for reference

Carousels: 3 statements, DCF, WACC, how a profitable company runs out of cash,
the LBO, four kinds of free cash flow, which method prints the highest value,
tell me about yourself, building a comp set, why an acquirer pays a premium,
goodwill, net working capital, which multiple pairs with which number, the
15-minute networking call.

Reels: EV vs equity value, Summer 2028 is already open, why investment
banking, five answers that get you dinged, accretive or dilutive in five
seconds, eight words that give you away, any questions for me.

## Adding a post

Append to `posts["posts"]` in `posts.json`:

```json
{
  "id": "2026-11-10-example",
  "series": "Technical of the Day",
  "scheduled_utc": "2026-11-10T13:00:00",
  "images": ["example-01.jpg", "example-02.jpg"],
  "caption": "...",
  "first_comment": "A specific question the page posts under it",
  "published_id": null,
  "published_at_utc": null
}
```

Times are **UTC**. US Eastern is UTC-5 from 1 November, so 08:00 Eastern is
13:00 UTC and 12:30 Eastern is 17:30 UTC. A Reel entry carries `video` and
`cover` instead of `images`.

`build/schedule.py <slug> <scheduled_utc> [--reel]` does all of this: it copies
the media in, reads the matching caption, and keeps the manifest sorted.
