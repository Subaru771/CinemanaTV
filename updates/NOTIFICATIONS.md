# CinemanaTV manual update notifications

**Feed:** https://raw.githubusercontent.com/Subaru771/CinemanaTV/main/updates/tv.json

**Edit the feed:** https://github.com/Subaru771/CinemanaTV/edit/main/updates/tv.json

This file controls the in-app **Update available** dialog for TV builds starting with **CinemanaTV 1.21** (Android `versionCode: 127`).

## Easiest method: publish with a GitHub form

1. Open **[Publish CinemanaTV Update Notice](https://github.com/Subaru771/CinemanaTV/actions/workflows/publish-tv-update.yml)**.
2. Select **Run workflow**, choose the **main** branch, and enter the new version, Android versionCode, tested APK HTTPS URL, and the English/Arabic message.
3. Select **enabled = true** only when the APK is available, then select **Run workflow** again to confirm.

The workflow validates the inputs and updates `updates/tv.json` for you. Leave `enabled = false` to pause notices. Owners with write access to this repository can use the form.

## Publish an update notice manually

1. Build, sign, and **test** the new TV APK. Host the APK somewhere with a persistent public **HTTPS** download URL.
2. In `updates/tv.json`, set `tv.version` to the new version label (such as `1.22`).
3. Set `tv.versionCode` to an Android version code **greater than 127** (for example 128). Every new release must use a strictly increasing Android versionCode.
4. Set `tv.downloadUrl` to the actual publicly accessible APK or download page.
5. Edit `tv.notes.en` and `tv.notes.ar` to your notification text (max. 240 characters shown).
6. Set `tv.enabled` to `true` and commit.

The prompt appears **on the next launch** for users whose installed versionCode is lower than the feed version. They can choose **Get update**, **Remind me later** (24-hour snooze), or **Skip this version**. A new `versionCode` can prompt even if an earlier release was skipped.

Set `enabled:false` at any time to pause announcements. Do **not** set it to true for the installed version 1.21 unless you genuinely have a newer APK: the app intentionally ignores equal version codes.

The app reads this public file without any administrator secret. Only people who can edit the GitHub repository can publish new notifications. No Firebase or paid push service is required. This is **an in-app popup**, not a system notification when the app is closed. GitHub's raw file CDN may take several minutes to refresh.

## Older builds

The previous 1.4.4 TV build uses the older Cloudflare update feed (`https://cinemana-updates-e8l.pages.dev/updates.json`). Changing this GitHub file **will not alert that installed build**. To announce 1.21 to older installs, you must separately update the old Cloudflare feed to point to the published, working 1.21 APK.

## Important signing note

An APK signed with a new CI debug key may not install over an older build. For reliable in-place updates, use the **same protected production signing key** for future releases. Never publish a private signing key in GitHub.
