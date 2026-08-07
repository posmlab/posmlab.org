# Instagram feed setup

The homepage pulls the lab's latest Instagram posts (@posm_lab) into a grid at the
bottom of the page. There's no live API call from the site itself — GitHub Pages is
fully static — so a scheduled GitHub Action (`.github/workflows/instagram-feed.yml`)
fetches the latest posts once a day, writes them to `_data/instagram.json`, and
commits that file. The homepage just renders whatever's in that file
(`_includes/themes/lab/instagram-feed.html`).

Until the two secrets below are set, `_data/instagram.json` stays `[]` and the feed
section simply doesn't render (no broken images, it just doesn't show up).

## One-time setup (you'll need to do this in Meta's tools — I can't create accounts
## or app registrations on your behalf)

1. **Make sure @posm_lab is an Instagram *Business* or *Creator* account**, connected
   to a Facebook Page. (Instagram Settings → Account type.) The Graph API only works
   for Business/Creator accounts, not personal ones.

2. **Create a Meta Developer app** at https://developers.facebook.com/apps — choose
   "Business" type. Add the "Instagram Graph API" product to it.

3. **Get a User access token** with the `instagram_basic` and `pages_show_list`
   permissions. The quickest way is the Graph API Explorer
   (https://developers.facebook.com/tools/explorer/): select your app, select those
   permissions, generate a token.

4. **Find your Page's connected Instagram Business Account ID:**

   ```
   GET /me/accounts
   ```
   (gives you your Page ID), then:
   ```
   GET /{page-id}?fields=instagram_business_account
   ```
   This returns the numeric Instagram Business Account ID — this is your `IG_USER_ID`.

5. **Exchange the short-lived token for a long-lived one** (lasts ~60 days):

   ```
   GET https://graph.facebook.com/v21.0/oauth/access_token
       ?grant_type=fb_exchange_token
       &client_id={app-id}
       &client_secret={app-secret}
       &fb_exchange_token={short-lived-token}
   ```
   This is your `IG_ACCESS_TOKEN`.

   (Double-check the current Graph API version number in Meta's docs — `v21.0` is
   what the workflow uses right now, but Meta increments this periodically.)

6. **Add both as repo secrets**: on GitHub, go to this repo → Settings → Secrets
   and variables → Actions → New repository secret. Add:
   - `IG_USER_ID`
   - `IG_ACCESS_TOKEN`

7. **Trigger the workflow once manually** to confirm it works: Actions tab →
   "Update Instagram feed" → Run workflow. Check that `_data/instagram.json` gets
   populated and committed.

## Ongoing maintenance

The access token expires roughly every 60 days. When it does, the workflow will
start failing (check the Actions tab). Repeat step 5 to get a fresh long-lived
token and update the `IG_ACCESS_TOKEN` secret. There's no automatic renewal wired
up — automating that would require storing an additional token with permission to
rewrite repo secrets, which adds its own security surface, so it's left as a manual
~2-minute task every couple of months.
