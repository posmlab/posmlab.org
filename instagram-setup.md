# Instagram feed setup

The homepage pulls the lab's latest Instagram posts (@posm_lab) into a grid at the
bottom of the page. There's no live API call from the site itself — GitHub Pages is
fully static — so a scheduled GitHub Action (`.github/workflows/instagram-feed.yml`)
fetches the latest posts once a day, writes them to `_data/instagram.json`, and
commits that file. The homepage just renders whatever's in that file
(`_includes/themes/lab/instagram-feed.html`).

If `_data/instagram.json` is `[]` (e.g. secrets missing or a token issue), the feed
section simply doesn't render — no broken images, it just doesn't show up.

This uses the **Instagram API with Instagram Login** flow (`graph.instagram.com`),
not the classic Facebook Page-based Graph API.

## How it works

Three repo secrets (Settings → Secrets and variables → Actions) power this:

- **`IG_USER_ID`** — the Instagram-scoped user ID for @posm_lab. Doesn't change;
  no maintenance needed.
- **`IG_ACCESS_TOKEN`** — a long-lived Instagram access token, valid ~60 days at a
  time. Used daily by `instagram-feed.yml` to fetch posts.
- **`SECRETS_PAT`** — a fine-grained GitHub personal access token, scoped to only
  this repo and only "Secrets: Read and write." Used by
  `.github/workflows/refresh-instagram-token.yml`, which runs on the 1st and 16th
  of every month, calls Instagram's refresh endpoint, and writes the renewed
  token back into `IG_ACCESS_TOKEN` — so `IG_ACCESS_TOKEN` never actually expires
  under normal operation, and no one needs to touch it by hand.

`SECRETS_PAT` itself has an expiration date (set when it was created, since GitHub
requires one on fine-grained PATs). GitHub will email the token's owner before it
expires. When that happens, generate a replacement:

1. GitHub → your profile photo → Settings → Developer settings → Personal access
   tokens → Fine-grained tokens → Generate new token.
2. **Resource owner**: the `posmlab` organization. **Repository access**: only
   this repo. **Permissions**: Repository permissions → **Secrets** →
   **Read and write** (this must be read-and-write, not read-only — a read-only
   token will authenticate fine but fail with a 403 the moment the workflow
   tries to write the refreshed token). Leave everything else at "No access."
3. Copy the new token value and update the `SECRETS_PAT` repo secret with it.
4. Trigger the workflow once manually (Actions tab → "Refresh Instagram access
   token" → Run workflow) to confirm it still succeeds.

## If the feed stops updating

Check the Actions tab for failures in either workflow.

- **`instagram-feed.yml` failing, `refresh-instagram-token.yml` succeeding**:
  likely unrelated to the token (e.g. Instagram API changes) — check the run's
  logs.
- **`refresh-instagram-token.yml` failing**: usually `SECRETS_PAT` — expired,
  wrong permission, or org access policy changed (org Settings → Third-party
  Access → Personal access tokens has both a policy toggle and a per-token
  approval queue; check both). Fix per the steps above, then re-run.
- **Both failing, or `IG_ACCESS_TOKEN` has actually expired** (the refresh
  workflow can't refresh a token that's already dead — it can only extend one
  that's still valid): fall back to a manual refresh, or if that also fails,
  get a completely new token from scratch. Both are covered below.

### Manual refresh

Only works if you already have the *current* long-lived token's value saved
somewhere outside GitHub — repo secrets are write-only and can't be viewed once
saved, by anyone, so there's no way to pull it back out of `IG_ACCESS_TOKEN` to
feed into this:

```powershell
$refreshParams = @{
  grant_type   = "ig_refresh_token"
  access_token = "YOUR_CURRENT_LONG_LIVED_TOKEN"
}
$refreshed = Invoke-RestMethod -Uri "https://graph.instagram.com/refresh_access_token" -Body $refreshParams -Method Get
$refreshed.access_token | Set-Clipboard
```

(Token must be at least 24 hours old and not yet expired; refreshing resets the
60-day clock.) Paste the refreshed token from your clipboard into the
`IG_ACCESS_TOKEN` repo secret.

### Getting a brand-new token from scratch

Needed if the token has fully expired and you don't have a saved copy to refresh,
or if the whole chain needs rebuilding (e.g. the Meta app gets deleted). Requires
your own login to whoever manages @posm_lab's Meta account.

1. **Confirm @posm_lab is an Instagram Business or Creator account** (Instagram
   Settings → Account type). Already done — it's set to Creator.

2. **Create a Meta Developer app** at https://developers.facebook.com/apps, and
   add the **"Manage messaging & content on Instagram"** use case (left sidebar →
   "Use cases" → Add). This unlocks a separate **Instagram App ID** and
   **Instagram App Secret**, distinct from the app's general Facebook App
   ID/Secret under App Settings → Basic — you need the *Instagram* ones for
   everything below.

3. **Register an OAuth redirect URI.** In the Instagram Login / Business Login use
   case's settings, add an HTTPS redirect URI. It doesn't need to be a real,
   reachable server — we only need to read a `code` parameter off the resulting
   URL in the browser's address bar. `https://posmlab.org/` works fine for this.

4. **Get an authorization code.** Build this URL (your Instagram App ID, and the
   exact redirect URI registered in step 3) and open it in a browser:

   ```
   https://www.instagram.com/oauth/authorize?client_id=YOUR_INSTAGRAM_APP_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&scope=instagram_business_basic
   ```

   Log in as whoever manages @posm_lab and click Authorize. You'll land on a page
   that may not load (expected — it's not a real server), but the address bar will
   show something like `https://posmlab.org/?code=AQD...#_`. Copy everything
   between `code=` and the trailing `#_`. This code is single-use and expires
   within a minute or two, so move to the next step right away.

5. **Exchange the code for a short-lived token, then immediately for a long-lived
   one**, in a single PowerShell block so the token is never displayed truncated
   or pasted around by hand:

   ```powershell
   $params = @{
     client_id     = "YOUR_INSTAGRAM_APP_ID"
     client_secret = "YOUR_INSTAGRAM_APP_SECRET"
     grant_type    = "authorization_code"
     redirect_uri  = "YOUR_REDIRECT_URI"
     code          = "THE_CODE_YOU_COPIED"
   }
   $shortLived = Invoke-RestMethod -Uri "https://api.instagram.com/oauth/access_token" -Method Post -Body $params

   $longLivedParams = @{
     grant_type    = "ig_exchange_token"
     client_secret = "YOUR_INSTAGRAM_APP_SECRET"
     access_token  = $shortLived.access_token
   }
   $longLived = Invoke-RestMethod -Uri "https://graph.instagram.com/access_token" -Body $longLivedParams -Method Get

   Write-Output "Expires in $($longLived.expires_in) seconds (~$([math]::Round($longLived.expires_in / 86400)) days)"
   $longLived.access_token | Set-Clipboard
   ```

   The `expires_in` value (~60 days, in seconds) confirms success. The full token
   is now on your clipboard — this is your new `IG_ACCESS_TOKEN`.

6. **Find your Instagram-scoped user ID**, if you don't already have it:
   ```
   GET /me?fields=user_id,username,account_type
   ```
   (run via Graph API Explorer, using any valid token for the app — this call
   works fine there even though token generation doesn't). Use the `user_id`
   value, not `id`. This is your `IG_USER_ID`.

7. **Update the repo secrets**: Settings → Secrets and variables → Actions.
   Paste the new `IG_ACCESS_TOKEN` (and `IG_USER_ID`, if it changed) directly
   from the clipboard — don't retype it.

8. **Trigger `instagram-feed.yml` once manually** to confirm it works: Actions
   tab → "Update Instagram feed" → Run workflow. Check that
   `_data/instagram.json` gets populated and committed.
