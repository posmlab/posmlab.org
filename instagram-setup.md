# Instagram feed setup

The homepage pulls the lab's latest Instagram posts (@posm_lab) into a grid at the
bottom of the page. There's no live API call from the site itself — GitHub Pages is
fully static — so a scheduled GitHub Action (`.github/workflows/instagram-feed.yml`)
fetches the latest posts once a day, writes them to `_data/instagram.json`, and
commits that file. The homepage just renders whatever's in that file
(`_includes/themes/lab/instagram-feed.html`).

Until the two secrets below are set, `_data/instagram.json` stays `[]` and the feed
section simply doesn't render (no broken images, it just doesn't show up).

**Note:** this uses the newer **Instagram API with Instagram Login** flow, which
talks to `graph.instagram.com` directly — it does *not* go through a Facebook Page,
even though some of Meta's UI still uses "Page" terminology along the way. If you
try the classic Facebook Login / Page Access Token approach instead, you'll hit
`Invalid Scopes` errors, because that's a different, older flow.

## One-time setup (in Meta's tools — I can't do this part for you, it requires
## your own login/account)

1. **Confirm @posm_lab is an Instagram Business or Creator account** (Instagram
   Settings → Account type). Already confirmed — it's set to Creator.

2. **Create a Meta Developer app** at https://developers.facebook.com/apps.

3. **Add these Use cases to the app** (left sidebar → "Use cases" → Add):
   - "Manage messaging & content on Instagram" — this is the one that actually
     unlocks the permissions needed to read the account's own media.
   - "Embed Facebook, Instagram and Threads content in other websites" — not
     strictly required for this feed, but harmless to have.

4. **Generate a token in Graph API Explorer**
   (https://developers.facebook.com/tools/explorer/):
   - Select your app from the app dropdown
   - In the token-type dropdown, choose **"Get Page Access Token"**
   - Make sure `instagram_basic` (and any other Instagram permissions offered)
     are checked
   - Generate — this gives you a short-lived token

5. **Find your Instagram-scoped user ID.** In the same Explorer request box, run:
   ```
   GET /me?fields=user_id,username,account_type
   ```
   The `user_id` value in the response (not the `id` value — there are two
   different IDs in the response, only `user_id` works for the `/media` calls
   below) is your `IG_USER_ID`.

   Sanity check it worked by running:
   ```
   GET /{user_id}/media?fields=id,caption,media_type,permalink,timestamp
   ```
   substituting in the actual number. You should get back a list of your recent
   posts.

6. **Exchange the short-lived token for a long-lived one** (lasts ~60 days).
   This is a plain HTTPS request — easiest to run it from a terminal with `curl`,
   or paste the URL into a browser address bar (substituting your own values):

   ```
   https://graph.instagram.com/access_token
       ?grant_type=ig_exchange_token
       &client_secret={instagram-app-secret}
       &access_token={short-lived-token}
   ```

   `{instagram-app-secret}` is in your app's dashboard under App Settings → Basic
   → "App Secret" (click "Show"). The response's `access_token` field is your
   `IG_ACCESS_TOKEN`.

7. **Add both as repo secrets**: on GitHub, go to this repo → Settings → Secrets
   and variables → Actions → New repository secret. Add:
   - `IG_USER_ID`
   - `IG_ACCESS_TOKEN`

8. **Trigger the workflow once manually** to confirm it works: Actions tab →
   "Update Instagram feed" → Run workflow. Check that `_data/instagram.json` gets
   populated and committed.

## Ongoing maintenance

The long-lived access token expires roughly every 60 days. When it does, the
workflow will start failing (check the Actions tab). To refresh it, run:

```
https://graph.instagram.com/refresh_access_token
    ?grant_type=ig_refresh_token
    &access_token={current-long-lived-token}
```

(Token must be at least 24 hours old to refresh, and this must happen before it
expires — refreshing resets the 60-day clock.) Take the new `access_token` from
the response and update the `IG_ACCESS_TOKEN` repo secret. This is simpler than
the exchange step in step 6 — no app secret needed this time, just the existing
token. There's no automatic renewal wired up (that would mean storing a second,
more powerful token with permission to rewrite repo secrets), so this is a manual
~2-minute task every couple of months.
