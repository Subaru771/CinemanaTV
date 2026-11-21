# Cinemana Updates — existing Cloudflare Pages project

**Production site:** https://cinemana-updates-e8l.pages.dev/  
**Production JSON:** https://cinemana-updates-e8l.pages.dev/updates.json

This is the **existing** Cloudflare Pages project, NOT cinemana-guide. The site controls update notices for Cinemana TV **and** Cinemana iOS.

## Architecture

- `cloudflare-updates/index.html` — interactive editor on the Pages root.
- `updates/cloudflare.json` — the editable TV + iOS manifest. The site writes it through GitHub's API using a short-lived fine-grained token kept in browser memory.
- `.github/workflows/deploy-existing-cloudflare-updates.yml` — redeploys to the existing Cloudflare Pages project using Wrangler.
- `/updates.json` — retains the original schema, with both `tv` and `ios` objects.
- `updates/tv.json` — synchronized **after** Cloudflare deploy succeeds, for CinemanaTV 1.21's newer GitHub-based updater.

On the FIRST deployment, if GitHub's combined manifest is absent, the workflow imports the existing live `/updates.json` to preserve both platforms' settings. If that fetch fails, deployment stops instead of replacing live values.

## One-time account authorization

In https://github.com/Subaru771/CinemanaTV/settings/secrets/actions create these repository secrets:

| Secret | Value |
| --- | --- |
| `CLOUDFLARE_ACCOUNT_ID` | Your Cloudflare account ID shown in the dashboard |
| `CLOUDFLARE_API_TOKEN` | A Cloudflare API token scoped to your account with **Cloudflare Pages: Edit** |

Do NOT paste tokens into chat, commit them, or use a global Cloudflare API key.

Then open https://github.com/Subaru771/CinemanaTV/actions/workflows/deploy-existing-cloudflare-updates.yml and choose **Run workflow** on `main`.

The workflow verifies the existing project named `cinemana-updates-e8l` before deployment and will NOT create a new Pages project. It publishes a complete static website. **If your current production deployment has other required assets beyond the manifest, merge them into `cloudflare-updates/` first.** Do not deploy a partial site snapshot that could delete required assets.

## Publish updates later

1. Open https://cinemana-updates-e8l.pages.dev/.
2. Edit TV and iOS separately: switch, version/code or build, URL, English and Arabic notes.
3. Connect using a short-lived GitHub fine-grained PAT restricted to `Subaru771/CinemanaTV` with **Contents: Read and write**. The dashboard does not store tokens.
4. Click **Publish changes**. A workflow deploys the notice to Cloudflare and syncs TV 1.21.
5. Disable the switch and republish to pause updates.

TV v1.21 uses versionCode **127**. A new notice for that installed build needs versionCode **128+**. Only announce an APK/IPA that has actually been built and tested. Updates appear when apps check the feed, not as background system push notifications.
