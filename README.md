# ib-autopost

Unattended publishing for **@investmentbankinginterviews**.

A GitHub Actions cron wakes every 15 minutes, reads `posts.json`, and publishes
anything whose scheduled time has passed through Meta's Content Publishing API.
The laptop can be shut.

This repository must be **public** — Meta fetches each image from its URL rather
than accepting an upload, so `raw.githubusercontent.com` has to serve it. Nothing
secret lives here; the token is a repository secret and never appears in the code
or the logs.

## One-time setup

**1. Make the repository public** and upload every file in this folder.

**2. Edit `image_base` in `posts.json`** — replace `OWNER/REPO` with your GitHub
username and this repository's name. That is the only URL to edit; every image
in every future post is resolved against it.

**3. Add one repository secret** under Settings → Secrets and variables →
Actions → New repository secret:

| Name | Value |
|---|---|
| `IG_ACCESS_TOKEN` | the system user token, permissions `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement` |

The Instagram account id is discovered from the token at run time, so there is
nothing else to paste and nothing to get wrong. Add an optional `IG_USER_ID`
secret only if the token ever reaches more than one Instagram account — the run
will say so explicitly if that happens.

**4. Run the self-test.** Actions → *Publish scheduled Instagram posts* →
Run workflow → mode `selftest`. It creates a single media container and
publishes nothing; an unpublished container expires by itself in 24 hours.
A green run proves the credentials, the image hosting and the API all work.

## Adding a post

Append an entry to `posts["posts"]`:

```json
{
  "id": "2026-11-05-dcf-walkthrough",
  "series": "Technical of the Day",
  "scheduled_utc": "2026-11-05T13:00:00",
  "images": ["IB-post2-01.jpg", "IB-post2-02.jpg"],
  "caption": "...",
  "published_id": null,
  "published_at_utc": null
}
```

Times are **UTC**. US Eastern is UTC−4 through 31 October 2026 and UTC−5 from
1 November, so 9:00 a.m. Eastern is `13:00` until the end of October and
`14:00` from November onwards.

Image filenames resolve against `image_base`; put the files in `images/`.

## How a run behaves

- A post with a non-null `published_id` is never touched again. The workflow
  commits that id back after publishing, so a post cannot go out twice.
- A `concurrency` group stops two runs overlapping.
- Instagram allows 50 posts per rolling 24 hours. A carousel counts as one.
  The run checks the remaining quota before it starts and publishes only what
  fits.
- Images must be **JPEG**. PNG is rejected by the API.
- One failed post does not stop the others; the run exits non-zero so the
  failure is visible in the Actions tab.
- The token is stripped from any error body before it is printed, so it cannot
  leak into a public log.

## Posts published before this repo existed

Set `published_id` to any non-empty string and the cron will skip that entry
for good. The first carousel carries `"business-suite-2026-10-28"` because it
went out by hand through Meta Business Suite.
