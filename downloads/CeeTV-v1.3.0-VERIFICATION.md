# Cee TV 1.3.0 / native preview 0.2.0 verification

The shared source is validated with a full website-flavor deterministic suite and targeted native-flavor checks. New coverage includes 360/412dp portrait interaction (412dp at 1.3x font scale), navigation across library tabs, editable search, settings persistence, details playback actions, startup/Home sharing, cancellation when changing language and disabled unsupported-quality pointer behavior. Existing TV/landscape interaction tests remain.

Focused data tests cover exact offline video-track overrides, unavailable/unsupported resolutions, audio-only periods, manual choices surviving new URLs/order, per-language disk caches, native URL/height pairs, codec-safe resolution parsing, series certification, slow optional banners, native lookup deadlines and update package identity. Local server fixtures are synthetic protocol records, not successful production native API captures.

Phone PNGs are Robolectric/Compose renders. No physical device, full-movie native playback, HDR/audio route or real-network buffering run was completed. Optional legacy live website tests are reported separately. Provider connectivity is rechecked independently before publication.

## Completed checks

- Full deterministic website suite: **309 tests, 301 passed, 8 optional live tests skipped**, no failures/errors. XML and logs were archived before the focused follow-up run.
- Targeted native-flavor suite: **61 tests passed**, no skips/failures/errors. This covers native protocol/parser behavior and shared portrait/TV interaction, player quality menus, exact offline selection, quality refresh, orientation, locale caches and update identity.
- Native ICU 76 accepted the production source regex, 23 other literal provider patterns and 8 raw provider patterns. The former unescaped-closing-brace regression was reproduced as an ICU syntax error.
- Connectivity recheck on 2026-11-13: cee.buzz/api/android/videoGroups/lang/en/kindGroup/1 returned **HTTP 503**. The Soft31 entry page returned HTML HTTP 200; that does not establish a working catalogue or media API.

- Final follow-up after quality-scan cancellation cleanup: **37 checks passed**, including a live website title (cee_2148687). Its 3 published HLS resolutions matched between viewing and download inventory. This reads stream metadata; it is not a full-film decode/download test. The other optional live cases were not rerun.
- Signing guards rejected both missing explicit production credentials (-Pcee.productionRelease=true) and a partially supplied configuration. No replacement signing key was generated.

Packaged APK identities/certificates/network policy and public artifact hashes are checked separately before announcing downloads.

## Packaged APKs

Both optimized release-type APKs built successfully with assembleWebsiteRelease assembleNativeApiRelease. apksigner verified APK Signature Scheme v2; neither APK is debuggable. aapt verified both regular and TV launcher entries, minimum Android 8/API 26, version/application label and separate package identities. Their development certificate is unchanged from the earlier delivered builds; these are sideload builds, not a new production-key rollout.

Certificate SHA-256: `23de31aa29f0d532e882abad4b1df80e156f95c05180869aceb9353e7566b101`.

| Flavor | Package | Version/code | APK SHA-256 |
| --- | --- | --- | --- |
| website | app.cinemanatv.cee | 1.3.0 / 12 | `a46296c1d7f0b50eebcac35befc7a15f76a4a707f642b75f1fe6e011885e244f` |
| nativeApi | app.cinemanatv.cee.nativepreview | 0.2.0-native-preview / 2 | `706c17a23acafce41fb722daf5e7a24731e56aeec87b0b981a125aa3ab178d39` |

Both the packaged manifest and compiled network-security XML were inspected: website cleartext is disabled; native legacy media cleartext is enabled. Generated release constants select the correct adapter. Native preview has a blank update-feed URL; website retains the stable feed. Update parsing/checking validates the package identity.

The source ZIP excludes build/cache output, local.properties, keystores and environment files. Its SHA-256 is published separately to avoid a self-referential checksum. Public APK/source downloads are compared against local SHA-256 values before changing the stable update feed. The app itself opens APK downloads in the browser; it does not implement a separate in-app APK hash verifier.
