"""
Publish scheduled Instagram carousels through Meta's Content Publishing API.

Run by GitHub Actions on a cron. Reads posts.json, finds anything whose
scheduled time has passed and that has not been published, publishes it,
and writes the post id back into the manifest.

Needs one environment variable, supplied as a repository secret:
    IG_ACCESS_TOKEN   a system user token with instagram_content_publish

The Instagram account id is discovered from that token. Set IG_USER_ID only
to override the discovery, for instance when the token reaches more than one
Instagram account.

Nothing here ever prints the token.
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, time as clock, timezone
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo("America/New_York")

# The manifest holds carousels only. The page's cap is 3 posts per Eastern day,
# and the third is a Reel Pietro uploads by hand, so the manifest may publish
# at most 2 per Eastern day. Backlog never goes out in a burst.
MAX_PER_EASTERN_DAY = 2
# Slot times used to release backlog on a day that has no scheduled entry.
DEFAULT_SLOTS_ET = (clock(8, 0), clock(12, 30))

GRAPH_VERSION = "v21.0"
GRAPH_ROOT = f"https://graph.facebook.com/{GRAPH_VERSION}"

MANIFEST = os.path.join(os.path.dirname(__file__), "posts.json")

# A container that is still PROCESSING is polled this often, for this long.
POLL_SECONDS = 10
POLL_ATTEMPTS = 30
REEL_POLL_ATTEMPTS = 60   # video transcoding is slow; 10 minutes at 10s


def call_graph(path, params, method="GET"):
    """Send one request to the Graph API and return the decoded JSON."""
    params = dict(params)
    params["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    url = f"{GRAPH_ROOT}/{path}"
    data = urllib.parse.urlencode(params).encode()

    if method == "GET":
        request = urllib.request.Request(f"{url}?{data.decode()}")
    else:
        request = urllib.request.Request(url, data=data, method="POST")

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        body = error.read().decode(errors="replace")
        # Strip the token in case Meta echoes the request back in the error.
        body = body.replace(os.environ["IG_ACCESS_TOKEN"], "<token>")
        raise RuntimeError(f"Graph API {error.code} on {path}: {body}") from None


def create_item_container(ig_user_id, image_url):
    """Create one carousel child container and return its id."""
    result = call_graph(
        f"{ig_user_id}/media",
        {"image_url": image_url, "is_carousel_item": "true"},
        method="POST",
    )
    return result["id"]


def create_carousel_container(ig_user_id, child_ids, caption):
    """Create the parent carousel container and return its id."""
    result = call_graph(
        f"{ig_user_id}/media",
        {
            "media_type": "CAROUSEL",
            "children": ",".join(child_ids),
            "caption": caption,
        },
        method="POST",
    )
    return result["id"]


def wait_until_ready(container_id, attempts=POLL_ATTEMPTS):
    """Block until a container reports FINISHED, or raise."""
    for _ in range(attempts):
        status = call_graph(container_id, {"fields": "status_code,status"})
        code = status.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Container {container_id} ended as {code}: {status}")
        time.sleep(POLL_SECONDS)
    raise RuntimeError(f"Container {container_id} never finished processing")


def publish_container(ig_user_id, container_id):
    """Publish a finished carousel container and return the new media id."""
    result = call_graph(
        f"{ig_user_id}/media_publish",
        {"creation_id": container_id},
        method="POST",
    )
    return result["id"]


def remaining_quota(ig_user_id):
    """Return how many more posts the account may publish in this window."""
    result = call_graph(f"{ig_user_id}/content_publishing_limit", {"fields": "quota_usage,config"})
    entry = result.get("data", [{}])[0]
    used = entry.get("quota_usage", 0)
    cap = entry.get("config", {}).get("quota_total", 50)
    return cap - used


def publish_one_post(ig_user_id, post, image_base):
    """Run the three-stage carousel flow for a single manifest entry."""
    print(f"  {len(post['images'])} slides")

    child_ids = []
    for name in post["images"]:
        image_url = name if name.startswith("http") else image_base + name
        child_ids.append(create_item_container(ig_user_id, image_url))
    print(f"  item containers created: {len(child_ids)}")

    carousel_id = create_carousel_container(ig_user_id, child_ids, post["caption"])
    print(f"  carousel container: {carousel_id}")

    wait_until_ready(carousel_id)
    media_id = publish_container(ig_user_id, carousel_id)
    print(f"  published as {media_id}")
    return media_id


def post_first_comment(media_id, post):
    """Post the page's own engagement question under a just-published post.

    Never fails the run: the post is already live, so a comment error is
    logged and recorded in the manifest, not raised. Needs the
    instagram_manage_comments permission on the token.
    """
    question = (post.get("first_comment") or "").strip()
    if not question or post.get("first_comment_id"):
        return
    try:
        result = call_graph(f"{media_id}/comments", {"message": question}, method="POST")
        post["first_comment_id"] = result.get("id")
        print(f"  first comment posted: {post['first_comment_id']}")
    except Exception as error:
        post["first_comment_error"] = str(error)[:300]
        print(f"  first comment NOT posted: {error}", file=sys.stderr)



def create_reel_container(ig_user_id, video_url, caption, cover_url=None):
    """Create a Reel container and return its id.

    Instagram transcodes the video before the container is publishable, which
    takes substantially longer than an image, so callers poll for longer.
    Audio must already be inside the file: the API cannot attach a trending
    track, and a silent reel is throttled, so every reel here ships with a
    voiceover baked in.
    """
    params = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true",
    }
    if cover_url:
        params["cover_url"] = cover_url
    return call_graph(f"{ig_user_id}/media", params, method="POST")["id"]


def publish_one_reel(ig_user_id, post, image_base):
    """Upload, transcode and publish a single Reel."""
    video_url = post["video"]
    if not video_url.startswith("http"):
        video_url = image_base + video_url
    cover = post.get("cover")
    if cover and not cover.startswith("http"):
        cover = image_base + cover

    print(f"  reel {video_url.rsplit('/', 1)[-1]}")
    container_id = create_reel_container(ig_user_id, video_url, post["caption"], cover)
    print(f"  reel container: {container_id}")

    # Transcoding a 60-second reel can take several minutes.
    wait_until_ready(container_id, attempts=REEL_POLL_ATTEMPTS)
    media_id = publish_container(ig_user_id, container_id)
    print(f"  published as {media_id}")
    return media_id


def load_manifest():
    with open(MANIFEST) as handle:
        return json.load(handle)


def save_manifest(manifest):
    with open(MANIFEST, "w") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def find_due_posts(manifest, now):
    """Return manifest entries that are scheduled in the past and unpublished."""
    due = []
    for post in manifest["posts"]:
        if post.get("published_id"):
            continue
        scheduled = datetime.fromisoformat(post["scheduled_utc"]).replace(tzinfo=timezone.utc)
        if scheduled <= now:
            due.append(post)
    due.sort(key=lambda post: post["scheduled_utc"])
    return due


def _utc(stamp):
    parsed = datetime.fromisoformat(stamp)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def apply_daily_cap(manifest, due, now):
    """Trim the due list so no Eastern day gets more than its share.

    Two limits, both counted in America/New_York:
      - at most MAX_PER_EASTERN_DAY manifest posts publish per Eastern day;
      - no more posts than slots that have already passed today, so backlog
        is released one per slot (at slot times) rather than at midnight.
    Today's slots are the scheduled times of today's manifest entries plus
    DEFAULT_SLOTS_ET. Held posts stay queued
    and go out oldest first on later runs.
    """
    today = now.astimezone(EASTERN).date()

    published_today = sum(
        1 for post in manifest["posts"]
        if post.get("published_id") and post.get("published_at_utc")
        and _utc(post["published_at_utc"]).astimezone(EASTERN).date() == today
    )

    slots = {
        _utc(post["scheduled_utc"]) for post in manifest["posts"]
        if _utc(post["scheduled_utc"]).astimezone(EASTERN).date() == today
    }
    slots |= {datetime.combine(today, t, EASTERN) for t in DEFAULT_SLOTS_ET}
    slots_passed = sum(1 for slot in slots if slot <= now)

    allowance = min(MAX_PER_EASTERN_DAY, slots_passed) - published_today
    allowance = max(allowance, 0)
    if len(due) > allowance:
        held = [post["id"] for post in due[allowance:]]
        print(
            f"Daily cap: {published_today} published today (ET), "
            f"{slots_passed} slot(s) passed, cap {MAX_PER_EASTERN_DAY}. "
            f"Holding {len(held)}: {', '.join(held)}"
        )
    return due[:allowance]




def resolve_ig_user_id():
    """Find the Instagram account id from the token, so nobody has to paste it.

    The token's Pages are listed, and the professional Instagram account
    connected to one of them is the account we publish to. Set IG_USER_ID
    explicitly to override this.
    """
    explicit = os.environ.get("IG_USER_ID", "").strip()
    if explicit:
        return explicit

    result = call_graph("me/accounts", {"fields": "name,instagram_business_account{id,username}"})
    found = []
    for page in result.get("data", []):
        account = page.get("instagram_business_account")
        if account:
            found.append((page.get("name"), account["id"], account.get("username")))

    if not found:
        raise RuntimeError(
            "No Instagram professional account is reachable from this token. "
            "Check that the Page is assigned to the system user and that the "
            "Instagram account is connected to that Page."
        )
    if len(found) > 1:
        listing = ", ".join(f"{u} ({i})" for _, i, u in found)
        raise RuntimeError(f"Several Instagram accounts reachable: {listing}. Set IG_USER_ID.")

    page_name, ig_id, username = found[0]
    print(f"Resolved @{username} ({ig_id}) via Page '{page_name}'")
    return ig_id


def selftest(ig_user_id, manifest):
    """Prove the credentials and the pipeline work, without publishing anything.

    Creates a single carousel item container from the first image in the
    manifest. An unpublished container simply expires after 24 hours, so this
    leaves nothing behind on the account. This is the test that settles whether
    a Development-mode app can publish without App Review.
    """
    post = manifest["posts"][0]
    image_url = manifest["image_base"] + post["images"][0]
    print(f"Self-test against {image_url}")

    print(f"  remaining quota in this 24h window: {remaining_quota(ig_user_id)}")
    container_id = create_item_container(ig_user_id, image_url)
    print(f"  container created: {container_id}")
    wait_until_ready(container_id)
    print("  container reached FINISHED")
    print("PASS - credentials, image hosting and the publishing API all work.")
    print("Nothing was posted. The container expires on its own in 24 hours.")
    return 0


def main():
    now = datetime.now(timezone.utc)
    manifest = load_manifest()

    if "OWNER/REPO" in manifest["image_base"]:
        print("image_base still contains the OWNER/REPO placeholder.", file=sys.stderr)
        return 1

    if "--selftest" in sys.argv:
        return selftest(resolve_ig_user_id(), manifest)

    due = apply_daily_cap(manifest, find_due_posts(manifest, now), now)

    if not due:
        # The cron runs every 15 minutes, so most runs end here. Nothing has
        # touched the network yet, which keeps the quiet runs genuinely free.
        print("Nothing due.")
        return 0

    ig_user_id = resolve_ig_user_id()
    quota = remaining_quota(ig_user_id)
    print(f"{len(due)} post(s) due, {quota} remaining in the 24h window")
    if quota < len(due):
        print("Quota too low for everything due; publishing what fits.")
        due = due[:max(quota, 0)]

    failures = 0
    for post in due:
        print(f"Publishing {post['id']} (scheduled {post['scheduled_utc']})")
        try:
            publisher = publish_one_reel if post.get("video") else publish_one_post
            post["published_id"] = publisher(
                ig_user_id, post, manifest["image_base"]
            )
            post["published_at_utc"] = datetime.now(timezone.utc).isoformat()
            save_manifest(manifest)
            post_first_comment(post["published_id"], post)
            save_manifest(manifest)
        except Exception as error:
            failures += 1
            print(f"  FAILED: {error}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
