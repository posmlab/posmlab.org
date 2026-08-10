"""Refresh the lab's long-lived Instagram access token before it expires
(~60 days) and hand the new value to the workflow via a local file.

Requires one GitHub Actions repo secret:
  IG_ACCESS_TOKEN  The current long-lived Instagram access token (must be at
                   least 24 hours old and not yet expired)

Writes the refreshed token to ig_refreshed_token.txt (gitignored/ephemeral —
the workflow reads it, feeds it to `gh secret set`, then deletes it). Never
prints the token itself; only non-secret status info goes to stdout/stderr.

See instagram-setup.md for the manual equivalent and the one-time OAuth
setup this depends on.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

OUTPUT_FILE = "ig_refreshed_token.txt"

IG_ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN")


def main():
    if not IG_ACCESS_TOKEN:
        print("IG_ACCESS_TOKEN must be set as a repo secret.", file=sys.stderr)
        sys.exit(1)

    params = urllib.parse.urlencode({
        "grant_type": "ig_refresh_token",
        "access_token": IG_ACCESS_TOKEN,
    })
    url = f"https://graph.instagram.com/refresh_access_token?{params}"

    try:
        with urllib.request.urlopen(url) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        # Most common cause: the current token already expired, so there's
        # nothing left to refresh. Fall back to the full OAuth flow in
        # instagram-setup.md (steps 4-5) for a brand-new token in that case.
        print(f"Instagram refresh request failed: {e.code} {e.read().decode('utf-8', 'ignore')}", file=sys.stderr)
        sys.exit(1)

    new_token = payload.get("access_token")
    expires_in = payload.get("expires_in")
    if not new_token:
        print(f"Refresh response missing access_token: {payload}", file=sys.stderr)
        sys.exit(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(new_token)

    days = round(expires_in / 86400) if expires_in else "unknown"
    print(f"Refreshed token wrote to {OUTPUT_FILE} (expires in ~{days} days)")


if __name__ == "__main__":
    main()
