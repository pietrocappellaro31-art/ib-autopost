"""
Offline checks for the Reel publishing changes of 26 Nov (Pietro): one Reel a day, trending music attached through
Instagram's Audio API, Trial Reels, and the fallback that posts without an extra Meta refuses. No network: call_graph
is replaced by a recorder.

    python3 build/publish_reel_test.py
"""

import json
import os
import pathlib
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
os.environ.setdefault("IG_ACCESS_TOKEN", "test-token")
import publish as P  # noqa: E402

calls = []


def fake(refuse=()):
    def call(path, params, method="GET", root=None):
        calls.append((path, dict(params)))
        for key in refuse:
            if key in params:
                raise RuntimeError(f"Graph API 400 on {path}: invalid {key}")
        return {"id": "c1"}
    return call


def post(**kw):
    base = dict(id="reel-x", type="reel", media_branch="reel/x", video="x.mp4", cover="x.jpg", caption="c",
                ai_label=True)
    base.update(kw)
    return base


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        check.failed = True


check.failed = False
P.wait_until_ready = lambda *a, **k: None

# 1. one Reel a day
check("cap is one Reel a day", P.MAX_REELS_PER_EASTERN_DAY == 1)

# 2. music and trial are set on the container
calls.clear()
P.call_graph = fake()
p = post(audio={"audio_id": "123", "title": "Song"}, trial=True)
P.publish_one_reel("u", p, "", publish=False)
params = calls[0][1]
check("music on the container", json.loads(params["audio_configuration"]) == {"audio_id": "123", "audio_volume": 15, "video_volume": 100})
check("trial on the container", json.loads(params["trial_params"]) == {"graduation_strategy": "SS_PERFORMANCE"})
check("AI label kept", params.get("is_ai_generated") == "true")

# 3. a plain Reel carries neither
calls.clear()
P.publish_one_reel("u", post(), "", publish=False)
check("plain Reel has no extras", "audio_configuration" not in calls[0][1] and "trial_params" not in calls[0][1])

# 4. refused music: retried without it, trial kept, the drop recorded
calls.clear()
P.call_graph = fake(refuse=("audio_configuration",))
p = post(audio={"audio_id": "9"}, trial=True)
P.publish_one_reel("u", p, "", publish=False)
check("retried without music", len(calls) == 2 and "audio_configuration" not in calls[1][1] and "trial_params" in calls[1][1])
check("drop recorded", "audio_configuration" in p.get("dropped", {}))

# 5. a block error is never retried
calls.clear()
P.call_graph = lambda *a, **k: (calls.append(1), (_ for _ in ()).throw(RuntimeError("API access blocked 5258005")))[1]
try:
    P.publish_one_reel("u", post(audio={"audio_id": "9"}), "", publish=False)
    check("block error raised", False)
except RuntimeError:
    check("block error raised, not retried", len(calls) == 1)

# 6. the daily cap holds a second Reel
now = datetime(2026, 11, 27, 23, 0, tzinfo=timezone.utc)
m = {"posts": [post(id="a", scheduled_utc="2026-11-27T17:00:00"), post(id="b", scheduled_utc="2026-11-27T22:00:00")]}
due = P.apply_daily_cap(m, list(m["posts"]), now)
check("only one Reel released", [x["id"] for x in due] == ["a"])
m26 = {"posts": [post(id="c", scheduled_utc="2026-11-27T02:00:00"),
                 post(id="p1", published_id="1", published_at_utc="2026-11-26T17:30:00"),
                 post(id="p2", published_id="2", published_at_utc="2026-11-26T23:00:00")]}
due = P.apply_daily_cap(m26, [m26["posts"][0]], datetime(2026, 11, 27, 2, 5, tzinfo=timezone.utc))
check("26 Nov slot C still posts (old cap that day)", [x["id"] for x in due] == ["c"])

if check.failed:
    sys.exit(1)
print("all Reel publishing checks passed")
