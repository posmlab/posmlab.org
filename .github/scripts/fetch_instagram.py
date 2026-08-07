"""Fetch recent posts for the lab's Instagram account via the Instagram Graph API
and write them to _data/instagram.json for the homepage feed.

Requires two GitHub Actions repo secrets:
  IG_USER_ID       Instagram Business/Creator account ID (a numeric string)
  IG_ACCESS_TOKEN  A long-lived Page access token with instagram_basic scope

See instagram-setup.md for how to obtain these.
"""

import json
import os
import sys
import urllib.parse
import urllib.request

GRAPH_VERSION = "v21.0"
LIMIT = 6

IG_USER_ID = os.environ.get("IG_USER_ID")
IG_ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN")


def main():
    if not IG_USER_ID or not IG_ACCESS_TOKEN:
        print("IG_USER_ID and IG_ACCESS_TOKEN must be set as repo secrets.", file=sys.stderr)
        sys.exit(1)

    fields = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp"
    params = urllib.parse.urlencode({
        "fields": fields,
        "access_token": IG_ACCESS_TOKEN,
        "limit": LIMIT,
    })
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{IG_USER_ID}/media?{params}"

    try:
        with urllib.request.urlopen(url) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"Instagram Graph API request failed: {e.code} {e.read().decode('utf-8', 'ignore')}", file=sys.stderr)
        sys.exit(1)

    if "error" in payload:
        print(f"Instagram Graph API error: {payload['error']}", file=sys.stderr)
        sys.exit(1)

    posts = []
    for item in payload.get("data", [])[:LIMIT]:
        image = item.get("thumbnail_url") or item.get("media_url")
        if not image:
            continue
        posts.append({
            "id": item.get("id"),
            "caption": (item.get("caption") or "")[:200],
            "image": image,
            "permalink": item.get("permalink"),
            "timestamp": item.get("timestamp"),
        })

    os.makedirs("_data", exist_ok=True)
    with open("_data/instagram.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)
        f.write("\n")

    print(f"Wrote {len(posts)} posts to _data/instagram.json")


if __name__ == "__main__":
    main()
