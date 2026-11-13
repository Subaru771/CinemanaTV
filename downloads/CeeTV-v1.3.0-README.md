# Cee TV 1.3.0 / Native Preview 0.2.0

One shared Kotlin/Compose/Media3 source tree builds two separately installed apps:

| Flavor | Application ID | Version/code | Provider |
| --- | --- | --- | --- |
| website | app.cinemanatv.cee | 1.3.0 / 12 | Existing cinamana.cc catalogue/player adapter |
| nativeApi | app.cinemanatv.cee.nativepreview | 0.2.0-native-preview / 2 | Recovered cee.buzz/api/android guest protocol |

Each updates its own previous installation when signed by the same key. The native preview has a separate cache/library and no default update feed. It never substitutes website titles after an API failure. The website build retains its own HTTPS-only network policy; native legacy media URLs retain the scheme declared by that provider. API traffic remains HTTPS with normal certificate verification.

## Changes

- Phone browsing follows the user's rotation. Playback, TV and tablet layouts request landscape; leaving playback restores the previous orientation request through a lifecycle effect.
- Narrow windows get compact headers, a scrolling bottom navigation bar, a smaller full-width hero, responsive grids and details, a full-width search field and horizontal settings categories. Large fonts increase the compact hero height; settings choices stack instead of overflowing. The existing TV rail/remote layout remains.
- Provider quality declarations remain visible alongside decoder metadata. Explicitly unsupported current-stream tracks are labelled and disabled; missing metadata alone never marks a quality unsupported. A refreshed URL/list preserves a manual resolution by value rather than by its old list index.
- Numbered adaptive downloads select the exact supported video track while retaining master-playlist audio/subtitles. An unavailable resolution returns an error instead of silently downloading a lower one. Preparation has a timeout and cancellation prevents late queueing and releases the helper on the main thread.
- Cancelled quality scans ignore late callbacks and release their Media3 helper once.
- Native file entries are deduplicated by URL AND height. Resolution parsing recognizes dimensions/p labels without confusing codec numbers for video heights. Series certification uses the provider's series rating ahead of unrelated movie fields.
- Splash and Home share a pending catalogue request owned by the ViewModel. Language changes cancel pending tab loads and reset discovery/search/focus state. Disk catalogue caches are separated by language. Native catalogue requests have an overall deadline; optional banners cannot delay ready rows.
- Update checks validate the running application's package identity. Both flavors support explicit controlled signing and missing/partial production-signing guards. Player presentation helpers are extracted into PlayerParts.kt.

## Build

JDK 17, Android SDK 35:

```sh
bash gradlew testWebsiteDebugUnitTest assembleWebsiteDebug
bash gradlew testNativeApiDebugUnitTest assembleNativeApiDebug
bash gradlew assembleWebsiteRelease assembleNativeApiRelease
```

Website APK: app/build/outputs/apk/website/release/app-website-release.apk.
Native APK: app/build/outputs/apk/nativeApi/release/app-nativeApi-release.apk.

Windows: MAKE-APK.cmd / BUILD-APK.cmd build the website flavor; BUILD-NATIVE-APK.cmd builds native. MAKE-APK.ps1 accepts -Provider website/nativeApi, -Debug and -SkipTests. CI uses explicit flavor tasks and filenames. Windows helpers were updated by inspection; Windows execution was not available here.

## Signing

Unconfigured release-type sideload builds use the existing development key. Production builds must supply all four properties (local.properties or Gradle -P) or corresponding environment variables:

| Property | Environment |
| --- | --- |
| cee.signing.storeFile | CEE_SIGNING_STORE_FILE |
| cee.signing.storePassword | CEE_SIGNING_STORE_PASSWORD |
| cee.signing.keyAlias | CEE_SIGNING_KEY_ALIAS |
| cee.signing.keyPassword | CEE_SIGNING_KEY_PASSWORD |

-Pcee.productionRelease=true rejects missing keys; partial signing configuration always fails. Privately back up the exact existing key before changing signing. A newly generated debug keystore has a different identity even with the same alias/password. Do not publish keys or passwords to the public repository/source archive. Environment variables or private properties avoid putting passwords into shell history. Verify signer fingerprint and package/version on every delivered APK. Plan rotation against the supported Android versions before adopting a different key for an existing package.

## Verification and limits

VERIFICATION.md records final counts and checks. New phone tests use 360dp and 412dp portrait windows, including 1.3x Compose font scale, real pointer navigation/search/settings/details, cancellation and pending-catalogue sharing. Existing TV remote/landscape tests remain. Preview PNGs are simulated Robolectric renders, not photographs of a physical device.

No physical TV/phone playback, decoder/HDR/audio or poor-network buffering run was available. Successful contract tests are not successful live native API captures. The recovered CEE origin previously returned HTTP 503 from this environment; its current availability is rechecked separately. Direct files provide only their actual encoded resolution. Genuine VK playback retains its official provider controls. Provider account sync/licence/device-signature logic, DLNA and App Cloner behavior are not implemented.

REVERSE-ENGINEERING-MAP.md documents the reference protocol and disabled proxy/empty host-map configuration. Historical investigation notes describe earlier versions. Claude's edited files were not supplied; this tree independently implements the fixes and responsive layout above.
