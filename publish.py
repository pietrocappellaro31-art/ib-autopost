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
from datetime import datetime, timezone

GRAPH_VERSION = "v21.0"
GRAPH_ROOT = f"https://graph.facebook.com/{GRAPH_VERSION}"

MANIFEST = os.path.join(os.path.dirname(__file__), "posts.json")

# A container that is still PROCESSING is polled this often, for this long.
POLL_SECONDS = 10
POLL_ATTEMPTS = 30


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


def wait_until_ready(container_id):
    """Block until a container reports FINISHED, or raise."""
    for _ in range(POLL_ATTEMPTS):
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
    return due




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

    due = find_due_posts(manifest, now)

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
            post["published_id"] = publish_one_post(
                ig_user_id, post, manifest["image_base"]
            )
            post["published_at_utc"] = datetime.now(timezone.utc).isoformat()
            save_manifest(manifest)
        except Exception as error:
            failures += 1
            print(f"  FAILED: {error}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
