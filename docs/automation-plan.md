# How publishing works

Pietro approves ideas. Everything else runs on GitHub's machines, so posts go
out with the laptop shut.

## Architecture

| Piece | Where |
|---|---|
| Publisher | `publish.py`, three-stage carousel flow plus a Reels path |
| Scheduler | `.github/workflows/publish.yml` |
| Schedule | `posts.json`, one entry per post, times in UTC |
| Slides | `images/*.jpg`, served to Meta over raw.githubusercontent.com |
| Credential | repo secret `IG_ACCESS_TOKEN`, a never-expiring system user token |

Meta app **IB Autopost**, id `2675690806197543`.
Business portfolio **Investment Banking Interview**, id `1110036318302825`.
System user **IB Autopost Bot**, id `61595860719464`, Employee role, holding the
Page (Content, Insights), the app (Full access) and the Instagram account
(Content, Insights).
Instagram account id `17841416394786069`, discovered from the token at run time
rather than stored.

## The app review question: answered

All four permissions, `instagram_basic`, `instagram_content_publish`,
`pages_show_list` and `pages_read_engagement`, sit at **Ready for testing** in
the app's Instagram use case. That is Meta's term for usable in development
mode without App Review, so this costs nothing and Buffer is not needed.

The permissions had to be added to the use case by hand. An app created from
the Instagram use case ships with none attached, which is why the token screen
first reported "No permissions available".

## Verified facts, from passing runs rather than docs

- Publishing quota is **100 posts per rolling 24 hours**, not the 50 some docs
  state. A carousel counts as one.
- **JPEG only.** PNG is rejected.
- Media must sit at a public URL; Meta fetches it and will not accept bytes.
  This is the only reason the repository is public. No credential lives in it.
- Unpublished containers expire in 24 hours, which is what makes
  `--selftest` safe to re-run at any time.
- **GitHub does not guarantee cron timing** and drops runs from high-frequency
  schedules on quiet repositories. A `*/15` schedule fired once in seven hours.
  Runs are now concentrated into the UTC windows that contain post times, with
  an hourly sweep, which GitHub honours far more reliably.

## Safety properties

- A post with a non-null `published_id` is never touched again. The workflow
  commits the id back after publishing, so a post cannot go out twice.
- A `concurrency` group prevents two runs overlapping.
- The token is stripped from any error body before printing, so a public
  Actions log cannot leak it.
- An idle run makes no network call at all.
- Setting `published_id` to any non-empty string skips a post for good, which
  is how posts published by hand elsewhere are recorded.

## Known limitations

- **Trending audio cannot be attached to a Reel through the API.** Reels
  published this way carry only the audio inside the file. This is why Reels
  are uploaded by hand.
- **There is no draft or scheduled state.** `media_publish` publishes
  immediately, so nothing can be placed in Instagram's Planned tab.
- Alt text is not settable through this path.
- The API has no schedule parameter. The cron holds each post and publishes at
  its time, within about ten minutes.

## Running it

```
# prove credentials and hosting without publishing anything
Actions, Run workflow, mode selftest

# publish anything due
Actions, Run workflow, mode publish
```

## Rejected alternatives

- **vidIQ.** Reels analysis, not carousel publishing. Its own docs say
  "Stories and static image posts are not included yet." Worth revisiting only
  for its outlier and views-per-hour badges.
- **Buffer**, about $5 per channel per month. Only needed if App Review had
  blocked the direct route. It did not.
- **Ayrshare** supports carousels but starts at $149 a month. Rejected on cost.
