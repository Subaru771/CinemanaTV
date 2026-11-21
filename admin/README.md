# CinemanaTV — Update Control Dashboard

The dashboard is in [admin/index.html](index.html). It reads and updates the live `updates/tv.json` notice used by CinemanaTV 1.21 and newer.

## One-time website hosting

GitHub Pages is **not enabled** for this repository. The dashboard's deployment workflow is already configured, but GitHub rejected automatic enablement ("Resource not accessible by integration").

1. As repository owner, open **https://github.com/Subaru771/CinemanaTV/settings/pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Open **https://github.com/Subaru771/CinemanaTV/actions/workflows/deploy-tv-dashboard.yml** and choose **Run workflow** on `main`.
4. Once the run succeeds, the dashboard should be available at **https://subaru771.github.io/CinemanaTV/**.

Until GitHub Pages is active, you can open `admin/index.html` as a local HTML file (or download the `CinemanaTV-Interactive-Dashboard` artifact from the deployment run).

## How to publish an update

- The dashboard loads the live notification feed automatically.
- Use **Next version**, enter the correct version code and HTTPS URL, and fill in the English and Arabic messages.
- Create a **fine-grained GitHub Personal Access Token** scoped to `Subaru771/CinemanaTV`, **Contents → Read and write**, with the shortest practical expiration.
- Paste the token in **GitHub connection → Connect**. Tokens remain in page memory only; they are never saved in local storage, cookies, the URL, or the repository.
- Click **Publish changes**. GitHub permissions control who can edit `updates/tv.json`.
- To pause notices, switch them **off** and publish again; this works even if no new APK exists.

The website itself is public, but cannot publish without a token authorized to write to the repository.

## Version safety

- Installed CinemanaTV v1.21 has Android `versionCode = 127`. To notify these users, choose a higher version code, such as `128` for v1.22.
- The app checks update notices at launch. **This is not push notification delivery when the TV app is closed.**
- Verify that the APK/release page is publicly downloadable before switching notices on.
- Earlier v1.4.4 installations use the previous Cloudflare feed and are **not** managed by this dashboard.
- Downloaded APKs must be signed with a compatible signing key to update in place.

For more details on the JSON schema, see [updates/NOTIFICATIONS.md](../updates/NOTIFICATIONS.md).
