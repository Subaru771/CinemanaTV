# Reference APK investigation — Cee TV 1.2.2

Reference: user-uploaded CEE Leanback_ScreenOff.apk, SHA-256 `8fe238852b46bf2a69431781ff22e384d7727f987aa495914f0b4f9d8444ea7e`.
Package `com.shabakaty.cbox.cee`, version 4.5.4. This is the same APK supplied earlier, confirmed byte for byte. A previous shallow string scan inspected its loader rather than its packed application code; that scan did not establish the application's playback mechanism.

The main packed DEX was decoded locally and its DEX SHA-1 integrity verified. No reference application code, binary or packed assets are included in this source distribution.

## What the native APK does

The main code names `https://cee.buzz/api/android/` as its API base and `transcoddedfiles/id/{videoid}` as a playback lookup. Its TranscodedFile model contains resolution, videoUrl, name, container and transcoddedFileName. getResolution and getVideoUrl return the corresponding fields. Its native quality dialog iterates transcodedFiles and uses each entry's resolution as a choice; selecting one switches the player URL while retaining the playback position. The download/detail code also uses the supplied resolutions and URLs. There are named quality values for 240p, 360p, 480p, 720p and 1080p; this is not evidence that every title supplies every quality.

Cee TV currently uses the cinamana.cc website catalogue and player declarations. That is a different provider integration. CEE native API IDs cannot be presumed interchangeable with website post IDs.

## Live checks and limits

Direct HTTP and an ordinary Chromium session both reached the native API with HTTP 503 connection-timeout responses in this environment. The actual native API payload, current catalogue mapping and media delivery were therefore not verified. This update does not replace the catalogue with that unavailable API or claim to reproduce the APK's working backend.

Chromium reached the website, inspected current server responses and found both its existing scdns HLS route and a direct MP4 masterUrl on s203d1.downet.net. HLS metadata for the existing regression sample was readable on direct and official relay routes and advertised heights 800, 532 and 266. The downet MP4 endpoint returned a connection error here; recognizing its official declaration is not proof of playback on a physical device.

## Concrete corrections in 1.2.2

- Complete provider quality discovery continues after the decoder reports one current video track; the menu merges both sources of metadata.
- Numbered HLS/DASH options display as resolutions instead of generic server entries, and selection retains the originating asset/master.
- All supplied adaptive sources (up to three) are scanned concurrently, and ready choices are published immediately; discovery no longer returns after the first successful source.
- HLS masters remain the playback/download asset to preserve separately declared audio and subtitles.
- The current downet.net direct MP4 declaration becomes a real Original file choice. It is never assigned invented resolutions.

Automated regression evidence and physical-device limitations are recorded in VERIFICATION.md.
