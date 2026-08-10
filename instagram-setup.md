# Instagram feed setup

The homepage pulls the lab's latest Instagram posts (@posm_lab) into a grid at the
bottom of the page. There's no live API call from the site itself — GitHub Pages is
fully static — so a scheduled GitHub Action (`.github/workflows/instagram-feed.yml`)
fetches the latest posts once a day, writes them to `_data/instagram.json`, and
commits that file. The homepage just renders whatever's in that file
(`_includes/themes/lab/instagram-feed.html`).

Until the two secrets below are set, `_data/instagram.json` stays `[]` and the feed
section simply doesn't render (no broken images, it just doesn't show up).

This uses the **Instagram API with Instagram Login** flow (`graph.instagram.com`),
not the classic Facebook Page-based Graph API. Note: **Graph API Explorer's "Get
Page Access Token" does not produce a token compatible with this flow**, even
though it can be used to read media directly — the actual short-lived token has to
come from Instagram's own OAuth authorization page. This tripped us up during
initial setup, so the steps below are the verified-working path, not the first
thing we tried.

## One-time setup (in Meta's tools — requires your own login/account)

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
   is now on your clipboard — this is your `IG_ACCESS_TOKEN`.

6. **Find your Instagram-scoped user ID**, if you don't already have it:
   ```
   GET /me?fields=user_id,username,account_type
   ```
   (run via Graph API Explorer, using any valid token for the app — this call
   works fine there even though token generation doesn't). Use the `user_id`
   value, not `id`. This is your `IG_USER_ID`.

7. **Add both as repo secrets**: this repo on GitHub → Settings → Secrets and
   variables → Actions → New repository secret. Add `IG_USER_ID` and
   `IG_ACCESS_TOKEN` (paste the clipboard contents from step 5 directly, don't
   retype it).

8. **Trigger the workflow once manually** to confirm it works: Actions tab →
   "Update Instagram feed" → Run workflow. Check that `_data/instagram.json` gets
   populated and committed.

## Ongoing maintenance

The long-lived access token expires roughly every 60 days. A scheduled workflow
(`.github/workflows/refresh-instagram-token.yml`) refreshes it automatically on
the 1st and 16th of each month, well within that window. **This requires a
one-time setup step** (below) — until that's done, or if the refresh workflow
itself starts failing, fall back to the manual refresh described further down.

### One-time setup for automatic refresh

The refresh workflow needs to *write* a repo secret (`IG_ACCESS_TOKEN`), which
the default `GITHUB_TOKEN` every workflow gets is deliberately not allowed to
do — that's a GitHub security boundary. So it needs a separate, standing
credential with that specific permission:

1. Create a **fine-grained personal access token**: GitHub → your profile photo
   → Settings → Developer settings → Personal access tokens → Fine-grained
   tokens → Generate new token.
2. **Resource owner**: the `posmlab` organization. **Repository access**: "Only
   select repositories" → this repo only. **Permissions**: Repository
   permissions → "Secrets" → Read and write (leave everything else at "No
   access"). Set an expiration (e.g. 1 year) — you'll need to repeat this setup
   when it expires.
3. Generate the token and copy it immediately (GitHub shows it once).
4. Add it as a repo secret named `SECRETS_PAT` (Settings → Secrets and
   variables → Actions → New repository secret) — same place `IG_ACCESS_TOKEN`
   lives, but this one is more powerful: it can only touch this repo's
   secrets, but it can touch *all* of them, not just the Instagram one. Don't
   reuse or widen its scope.
5. Trigger the workflow once manually (Actions tab → "Refresh Instagram access
   token" → Run workflow) to confirm it succeeds end to end.

### Manual refresh (fallback)

If the current token has already expired, or the automatic workflow is
failing and you need the feed working again immediately, refresh it by hand.
Unlike getting the *first* token, refreshing an existing long-lived one is
simple and doesn't require repeating the OAuth dance — just:

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
`IG_ACCESS_TOKEN` repo secret — but note you need to already have the current
token's value saved somewhere outside GitHub to run this (repo secrets are
write-only and can't be viewed once saved, by anyone). If you don't have it
saved anywhere, skip straight to redoing steps 4–5 above for a fresh token.
