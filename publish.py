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
from datetime import datetime, time as clock, timedelta, timezone
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo("America/New_York")

# The manifest holds carousels and Stories. Since 10 Nov 2026 the page runs
# 3 carousels per Eastern day (Pietro's call), plus the Reel he uploads by hand,
# so the manifest may publish at most 3 carousels per Eastern day. Backlog never
# goes out in a burst.
MAX_PER_EASTERN_DAY = 3
# Slot times used to release backlog on a day that has no scheduled entry.
DEFAULT_SLOTS_ET = (clock(8, 0), clock(12, 30), clock(17, 30))

# 16 Nov 2026 (Pietro): two Reels a day, posted automatically with no approval step. Reels have their own
# daily cap and never take a carousel's place. Their video files are not in main's history: each Reel waits on
# a temporary branch reel/<slug> (the session cannot create releases) and the branch is deleted once posted.
MAX_REELS_PER_EASTERN_DAY = 2
PROBE_HOURS = 6                      # while Meta blocks the app, try once every 6 hours, never more
REPO = os.environ.get("GITHUB_REPOSITORY", "pietrocappellaro31-art/ib-autopost")
# Errors that mean Meta is unhappy with the app or the account: stop the whole run, retry nothing.
BLOCK_MARKERS = ("API access blocked", "2207042", "temporarily blocked", "unusual activity", "\"code\":368", "\"code\":4,",
                 "\"code\":17,", "\"code\":32,", "\"code\":613")

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


def is_story(post):
    return post.get("type") == "story"


def is_reel(post):
    return post.get("type") == "reel" or bool(post.get("video"))


def is_block_error(error):
    text = str(error)
    return any(marker in text for marker in BLOCK_MARKERS)


def publish_one_story(ig_user_id, post, image_base):
    """Publish one image Story. Stories take no caption and no stickers via the API."""
    name = post["images"][0]
    image_url = name if name.startswith("http") else image_base + name
    result = call_graph(f"{ig_user_id}/media", {"media_type": "STORIES", "image_url": image_url}, method="POST")
    wait_until_ready(result["id"])
    media_id = publish_container(ig_user_id, result["id"])
    print(f"  story published as {media_id}")
    return media_id


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
    """Create a Reel container from a public video URL and return its id (the older path, kept for entries that
    carry a full video URL). Audio must already be inside the file."""
    params = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true",
        "is_ai_generated": "true",
    }
    if cover_url:
        params["cover_url"] = cover_url
    return call_graph(f"{ig_user_id}/media", params, method="POST")["id"]


def branch_url(branch, name):
    return f"https://raw.githubusercontent.com/{REPO}/refs/heads/{urllib.parse.quote(branch)}/{urllib.parse.quote(name)}"


def fetch_bytes(url):
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def reel_container_resumable(ig_user_id, post, cover_url=None):
    """16 Nov: a Reel container for a binary upload (no public video URL needed by Meta). The AI info label is set
    here, at creation, which is the only time the API accepts it (is_ai_generated, Meta changelog 22 Jun 2026)."""
    params = {"media_type": "REELS", "upload_type": "resumable", "caption": post["caption"]}
    if post.get("ai_label", True):
        params["is_ai_generated"] = "true"
    if cover_url:
        params["cover_url"] = cover_url
    elif post.get("thumb_offset_ms") is not None:
        params["thumb_offset"] = str(int(post["thumb_offset_ms"]))
    if post.get("audio_name"):
        params["audio_name"] = post["audio_name"]
    return call_graph(f"{ig_user_id}/media", params, method="POST")


def upload_binary(container_id, data):
    """Send the video bytes to Meta's upload host (rupload), the documented resumable flow."""
    request = urllib.request.Request(
        f"https://rupload.facebook.com/ig-api-upload/{GRAPH_VERSION}/{container_id}", data=data, method="POST",
        headers={"Authorization": f"OAuth {os.environ['IG_ACCESS_TOKEN']}", "offset": "0", "file_size": str(len(data))})
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            body = json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as error:
        body = error.read().decode(errors="replace").replace(os.environ["IG_ACCESS_TOKEN"], "<token>")
        raise RuntimeError(f"rupload {error.code}: {body}") from None
    if not body.get("success"):
        raise RuntimeError(f"rupload did not confirm the upload: {body}")


def delete_branch(branch):
    """Remove the temporary reel/<slug> branch once the Reel is live (best effort; needs contents: write)."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token or not branch.startswith("reel/"):
        return
    request = urllib.request.Request(f"https://api.github.com/repos/{REPO}/git/refs/heads/{urllib.parse.quote(branch)}",
                                     method="DELETE", headers={"Authorization": f"Bearer {token}",
                                                               "Accept": "application/vnd.github+json"})
    try:
        urllib.request.urlopen(request, timeout=30)
        print(f"  deleted branch {branch}")
    except Exception as error:
        print(f"  branch {branch} not deleted: {error}", file=sys.stderr)


def publish_one_reel(ig_user_id, post, image_base, publish=True):
    """Upload, transcode and publish a single Reel. Entries made by build/reel_queue.py carry media_branch, video
    (a file name on that branch) and cover; an entry whose video is a full URL uses the older URL path."""
    branch = post.get("media_branch")
    if branch:
        data = fetch_bytes(branch_url(branch, post["video"]))
        cover = branch_url(branch, post["cover"]) if post.get("cover") else None
        print(f"  reel {post['video']} from {branch}: {len(data) / 1e6:.1f} MB")
        container_id = reel_container_resumable(ig_user_id, post, cover)["id"]
        upload_binary(container_id, data)
    else:
        video_url = post["video"] if post["video"].startswith("http") else image_base + post["video"]
        cover = post.get("cover")
        if cover and not cover.startswith("http"):
            cover = image_base + cover
        print(f"  reel {video_url.rsplit('/', 1)[-1]}")
        container_id = create_reel_container(ig_user_id, video_url, post["caption"], cover)
    print(f"  reel container: {container_id}")
    # Transcoding a 60-second reel can take several minutes.
    wait_until_ready(container_id, attempts=REEL_POLL_ATTEMPTS)
    if not publish:
        return container_id
    media_id = publish_container(ig_user_id, container_id)
    print(f"  published as {media_id}")
    if branch:
        delete_branch(branch)
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
        if post.get("attempts", 0) >= 3:            # 16 Nov: a post that failed 3 times waits for a person
            print(f"Skipping {post['id']}: failed {post['attempts']} times ({post.get('last_error', '')[:120]})")
            continue
        scheduled = datetime.fromisoformat(post["scheduled_utc"]).replace(tzinfo=timezone.utc)
        if is_reel(post) and post.get("slot") and (now - scheduled).total_seconds() > 6 * 3600:
            # 16 Nov: a Reel that missed its slot by more than 6 hours (a block, an outage) moves to the next time its
            # slot comes round, instead of going out at an odd hour.
            hh, mm = map(int, manifest.get("reel_slots_et", {}).get(post["slot"], "12:30").split(":"))
            nxt = datetime.combine(now.astimezone(EASTERN).date(), clock(hh, mm), EASTERN)
            if nxt.astimezone(timezone.utc) <= now:
                nxt += timedelta(days=1)
            post["scheduled_utc"] = nxt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
            print(f"Reel {post['id']} missed its slot; moved to {post['scheduled_utc']} UTC")
            continue
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

    # Stories are outside the cap: they never take a carousel's place, and
    # their times are not carousel slots.
    stories = [post for post in due if is_story(post)]
    reels = [post for post in due if is_reel(post) and not is_story(post)]
    due = [post for post in due if not is_story(post) and not is_reel(post)]
    feed = [post for post in manifest["posts"] if not is_story(post) and not is_reel(post)]

    # Reels (16 Nov): their own cap, at most MAX_REELS_PER_EASTERN_DAY a day, oldest first; they post at or
    # after their own scheduled slot and never use a carousel slot.
    reels_today = sum(
        1 for post in manifest["posts"]
        if is_reel(post) and post.get("published_id") and post.get("published_at_utc")
        and _utc(post["published_at_utc"]).astimezone(EASTERN).date() == today
    )
    reel_allowance = max(MAX_REELS_PER_EASTERN_DAY - reels_today, 0)
    if len(reels) > reel_allowance:
        print(f"Reel cap: {reels_today} Reel(s) published today (ET). Holding: "
              + ", ".join(post["id"] for post in reels[reel_allowance:]))
    reels = reels[:reel_allowance]

    published_today = sum(
        1 for post in feed
        if post.get("published_id") and post.get("published_at_utc")
        and _utc(post["published_at_utc"]).astimezone(EASTERN).date() == today
    )

    slots = {
        _utc(post["scheduled_utc"]) for post in feed
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
    return due[:allowance] + reels + stories




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


# --------------------------------------------------------------------------------------------- performance
# 16 Nov 2026 (Pietro: "use your own intelligence to analyze the top performing reels ... decide at what time to
# post"). Every day the publisher records how each Reel and carousel did and when followers are online, into
# docs/daily/performance.json (committed by the workflow) and a readable docs/daily/performance.md. The daily
# Reel runs read them to choose formats, hooks and slots. Metrics a token cannot read are recorded as missing.

PERF_JSON = os.path.join(os.path.dirname(__file__), "docs", "daily", "performance.json")
PERF_MD = os.path.join(os.path.dirname(__file__), "docs", "daily", "performance.md")
REEL_METRICS = ("reach", "views", "saved", "shares", "total_interactions", "likes", "comments",
                "ig_reels_avg_watch_time", "ig_reels_video_view_total_time", "follows")
FEED_METRICS = ("reach", "views", "saved", "shares", "total_interactions", "likes", "comments", "follows")


def media_metrics(media_id, names):
    """Ask for all metrics at once; if Meta rejects one, ask one by one so the others are still recorded."""
    try:
        res = call_graph(f"{media_id}/insights", {"metric": ",".join(names)})
        return {m["name"]: (m.get("values") or [{}])[0].get("value", m.get("total_value", {}).get("value")) for m in res.get("data", [])}, []
    except Exception:
        got, missing = {}, []
        for name in names:
            try:
                res = call_graph(f"{media_id}/insights", {"metric": name})
                for m in res.get("data", []):
                    got[m["name"]] = (m.get("values") or [{}])[0].get("value", m.get("total_value", {}).get("value"))
            except Exception as error:
                missing.append(f"{name}: {str(error)[:300]}")
        return got, missing


def collect_insights(ig_user_id, limit=40):
    res = call_graph(f"{ig_user_id}/media", {"fields": "id,caption,media_product_type,media_type,timestamp,permalink,"
                                                         "like_count,comments_count", "limit": str(limit)})
    rows, problems, first_error = [], set(), []
    supported = {}                       # kind -> metrics Meta accepted on the first post of that kind (call budget:
    for m in res.get("data", []):        # one call a post after that, well inside 200 calls an hour)
        reel = m.get("media_product_type") == "REELS"
        kind = "reel" if reel else "feed"
        if kind in supported:
            got, missing = media_metrics(m["id"], supported[kind]) if supported[kind] else ({}, [])
        else:
            got, missing = media_metrics(m["id"], REEL_METRICS if reel else FEED_METRICS)
            bad = {x.split(":")[0] for x in missing}
            supported[kind] = [x for x in (REEL_METRICS if reel else FEED_METRICS) if x not in bad]
        problems.update(f"{kind} {x.split(':')[0]}" for x in missing)
        if missing and not first_error:
            first_error.append(missing[0][:300])
        when = _utc(m["timestamp"].replace("+0000", "+00:00"))
        rows.append(dict(id=m["id"], kind="reel" if reel else m.get("media_type", "").lower(), permalink=m.get("permalink"),
                         posted_et=when.astimezone(EASTERN).strftime("%Y-%m-%d %a %H:%M"),
                         hours_live=round((datetime.now(timezone.utc) - when).total_seconds() / 3600, 1),
                         caption=(m.get("caption") or "").split("\n")[0][:90],
                         **{"likes": m.get("like_count"), "comments": m.get("comments_count"), **got}))
    online = None
    try:
        res = call_graph(f"{ig_user_id}/insights", {"metric": "online_followers", "period": "lifetime"})
        vals = (res.get("data") or [{}])[0].get("values") or []
        online = vals[-1].get("value") if vals else None        # {hour (account time zone, Pacific): followers online}
    except Exception as error:
        problems.add("online_followers")
        first_error.append("online_followers: " + str(error)[:300])
    granted, comments_read = None, None
    try:                                         # which permissions the token carries, and a read-only comments check
        granted = sorted(x["permission"] for x in call_graph("me/permissions", {}).get("data", []) if x.get("status") == "granted")
    except Exception as error:
        granted = f"not readable: {str(error)[:120]}"
    if rows:
        try:
            call_graph(f"{rows[0]['id']}/comments", {"limit": "1"})
            comments_read = True
        except Exception as error:
            comments_read = f"no: {str(error)[:160]}"
    return dict(updated_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"), media=rows,
                token_permissions=granted, comments_access=comments_read,
                online_followers_by_hour_pacific=online, unavailable=sorted(problems), first_errors=first_error)


def write_performance(perf):
    with open(PERF_JSON, "w") as handle:
        json.dump(perf, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    reels = sorted([r for r in perf["media"] if r["kind"] == "reel" and r["hours_live"] >= 24],
                   key=lambda r: -(r.get("reach") or 0))
    lines = ["# Performance (written by publish.py; do not edit by hand)", "",
             f"Updated {perf['updated_utc']} UTC. Reels live at least 24 hours, best reach first. "
             "Watch time in milliseconds as Meta reports it.", "",
             "| Posted (ET) | Reach | Views | Shares | Saves | Likes | Comments | Follows | Avg watch | Opening line |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in reels:
        lines.append(f"| {r['posted_et']} | {r.get('reach', '')} | {r.get('views', '')} | {r.get('shares', '')} | {r.get('saved', '')} | "
                     f"{r.get('likes', '')} | {r.get('comments', '')} | {r.get('follows', '')} | {r.get('ig_reels_avg_watch_time', '')} | "
                     f"{r['caption'].replace('|', '/')} |")
    if perf.get("online_followers_by_hour_pacific"):
        lines += ["", "Followers online by hour (Pacific time, as Meta reports it): "
                  + ", ".join(f"{h}h {v}" for h, v in sorted(perf["online_followers_by_hour_pacific"].items(), key=lambda kv: int(kv[0])))]
    if perf.get("unavailable"):
        lines += ["", "Not readable with the current token: " + ", ".join(perf["unavailable"])]
        lines += [f"- {e}" for e in perf.get("first_errors", [])]
    with open(PERF_MD, "w") as handle:
        handle.write("\n".join(lines) + "\n")


def insights_if_stale(ig_user_id, max_age_hours=20):
    try:
        with open(PERF_JSON) as handle:
            age = (datetime.now(timezone.utc) - _utc(json.load(handle)["updated_utc"])).total_seconds() / 3600
    except Exception:
        age = 1e9
    if age < max_age_hours:
        return
    perf = collect_insights(ig_user_id)
    write_performance(perf)
    print(f"  performance recorded: {len(perf['media'])} posts; unavailable: {perf['unavailable'] or 'none'}")


def reel_selftest(ig_user_id, branch, name):
    """16 Nov: prove the Reel path end to end WITHOUT publishing: fetch the file from its branch, create a REELS
    container with the AI label, upload the bytes, wait for FINISHED. Then read insights and the Audio API once.
    The container expires unpublished after 24 hours."""
    post = dict(caption="Self-test, not published.", media_branch=branch, video=name)
    container = publish_one_reel(ig_user_id, post, "", publish=False)
    status = call_graph(container, {"fields": "status_code,status"})
    print(f"  container {container}: {status.get('status_code')} (nothing published)")
    try:
        res = call_graph(container, {"fields": "is_ai_generated"})
        print(f"  container reports is_ai_generated={res.get('is_ai_generated')}")
    except Exception as error:
        print(f"  is_ai_generated not readable on a container: {str(error)[:120]}")
    perf = collect_insights(ig_user_id, limit=10)
    print(f"  insights: {len(perf['media'])} posts read; unavailable: {perf['unavailable'] or 'none'}")
    print(f"  online followers by hour: {'yes' if perf['online_followers_by_hour_pacific'] else 'no'}")
    try:
        res = call_graph("ig_audio", {"audio_type": "music", "user_id": ig_user_id})
        print(f"  Audio API: {len(res.get('audio', res.get('data', [])))} tracks returned")
    except Exception as error:
        print(f"  Audio API not available to this token: {str(error)[:160]}")
    print("PASS - the Reel upload path works. Nothing was posted.")
    return 0


def main():
    now = datetime.now(timezone.utc)
    manifest = load_manifest()

    if "OWNER/REPO" in manifest["image_base"]:
        print("image_base still contains the OWNER/REPO placeholder.", file=sys.stderr)
        return 1

    if "--selftest" in sys.argv:
        return selftest(resolve_ig_user_id(), manifest)
    if "--reel-selftest" in sys.argv:
        i = sys.argv.index("--reel-selftest")
        return reel_selftest(resolve_ig_user_id(), sys.argv[i + 1], sys.argv[i + 2])
    if "--insights" in sys.argv:
        perf = collect_insights(resolve_ig_user_id())
        write_performance(perf)
        print(f"performance recorded: {len(perf['media'])} posts; unavailable: {perf['unavailable'] or 'none'}")
        print(f"token permissions: {perf.get('token_permissions')}; comments access: {perf.get('comments_access')}")
        return 0

    due = apply_daily_cap(manifest, find_due_posts(manifest, now), now)

    # 16 Nov: a circuit breaker. Meta blocked the app on 2 Nov and again on 16 Nov ("API access blocked", subcode
    # 5258005). While a block is recorded, runs make no API call at all except one probe every PROBE_HOURS, so a
    # blocked app is not hit every few minutes by cron and dispatches; the probe clears the flag when access is back.
    block = manifest.get("api_block")
    if due and block:
        last = _utc(block.get("last_probe_utc") or block["since_utc"])
        if (now - last).total_seconds() < PROBE_HOURS * 3600:
            print(f"API BLOCKED since {block['since_utc']} ({block.get('error', '')[:120]}). "
                  f"{len(due)} post(s) waiting; next probe after {PROBE_HOURS} h. Pietro must restore access in Meta's "
                  "developer dashboard.", file=sys.stderr)
            return 1

    if not due:
        # The cron runs every 15 minutes, so most runs end here. Nothing has
        # touched the network yet, which keeps the quiet runs genuinely free.
        print("Nothing due.")
        return 0

    try:
        ig_user_id = resolve_ig_user_id()
        quota = remaining_quota(ig_user_id)
    except Exception as error:
        if is_block_error(error):
            manifest["api_block"] = dict(since_utc=(block or {}).get("since_utc") or now.isoformat(timespec="seconds"),
                                         last_probe_utc=now.isoformat(timespec="seconds"), error=str(error)[:300])
            save_manifest(manifest)
            print(f"API BLOCKED: {error}. Recorded; no more calls for {PROBE_HOURS} h.", file=sys.stderr)
            return 1
        raise
    if block:
        manifest.pop("api_block", None)
        save_manifest(manifest)
        print(f"API access is back (blocked since {block['since_utc']}).")
    print(f"{len(due)} post(s) due, {quota} remaining in the 24h window")
    if quota < len(due):
        print("Quota too low for everything due; publishing what fits.")
        due = due[:max(quota, 0)]

    failures = 0
    for post in due:
        print(f"Publishing {post['id']} (scheduled {post['scheduled_utc']})")
        try:
            publisher = (publish_one_story if is_story(post)
                         else publish_one_reel if post.get("video") else publish_one_post)
            post["published_id"] = publisher(
                ig_user_id, post, manifest["image_base"]
            )
            post["published_at_utc"] = datetime.now(timezone.utc).isoformat()
            save_manifest(manifest)
            if not is_story(post):
                post_first_comment(post["published_id"], post)
            save_manifest(manifest)
        except Exception as error:
            failures += 1
            post["last_error"] = str(error)[:300]
            post["attempts"] = post.get("attempts", 0) + 1
            save_manifest(manifest)
            print(f"  FAILED: {error}", file=sys.stderr)
            if is_block_error(error):
                if "access blocked" in str(error).lower():
                    manifest["api_block"] = dict(since_utc=now.isoformat(timespec="seconds"),
                                                 last_probe_utc=now.isoformat(timespec="seconds"), error=str(error)[:300])
                    save_manifest(manifest)
                # 16 Nov: never push on when Meta signals a block or a rate limit; everything waits for a person.
                print("STOPPING: the error looks like a block or a rate limit. Nothing else is published this run.",
                      file=sys.stderr)
                break

    try:
        insights_if_stale(ig_user_id)
    except Exception as error:                     # measuring must never fail a publishing run
        print(f"  insights not refreshed: {error}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
