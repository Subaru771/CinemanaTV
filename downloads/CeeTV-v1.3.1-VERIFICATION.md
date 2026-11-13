# Cee TV 1.3.1 / Native Preview 0.3.0 verification

Checks performed on 2026-11-14 (Asia/Baghdad). The shared app retains the 1.3.0 quality/download, phone/TV, signing and cache fixes and adds the hosted website adapter/server.

## New coverage

Android CeeApiCatalogTest covers every catalogue/file JSON contract using response fixtures produced by the server's HTTP tests; URL-prefix/query encoding, access-key headers, redirect refusal, cancellation of stalled requests, response limits, rejected-route recovery and errors without private upstream bodies. HostedProviderSettingsTest verifies an insecure replacement cannot overwrite the previously saved server/key.

The Node suite checks real HTTP routes with controlled upstream fixtures, provider/category identity, watch-page deep links, quality declarations sharing a URL, reordered/quoted source objects, escaped queries, codec/dimension/Arabic-digit labels, redirect destination checks, streamed body limits and cache sharing/retry. The original parser smoke tests remain.

The first full Android run encountered a disk-full error while Docker was building: an existing adaptive-offline test could not create its cache directory. Generated build outputs and this task's Docker image/cache were removed to recover space. This was not treated as a passing regression run; final rerun counts are recorded below.

The Docker image built with a session CA supplied via BuildKit secret. A container startup attempt ran out of workspace space; production-mode service behavior is checked directly under Node instead. No session CA/key or Docker storage is included in the deliverables. The supplied Compose configuration and public HTTPS certificate provisioning still require deployment on the user's host.

Final app suite counts, local service/live checks, packaged identities and public hashes are appended before delivery. Physical-device decoding, full-movie downloads and live native API playback are not claimed.

## Completed app and server checks

- Full deterministic website-flavor rerun: **319 tests, 310 passed, 9 optional live tests skipped**, no failures/errors. XML and logs were archived before live follow-up checks.
- Targeted native-flavor run: **43 tests passed**, no failures/errors/skips, covering native protocol/parser behavior, hosted adapter contracts, orientation, update package identity, exact offline track selection and quality refresh.
- Node server: **13 tests passed**, plus original parser smoke checks. Dependency audit reported **0 known vulnerabilities** for the locked production dependencies.
- Final live follow-up: **2 tests passed**. The real hosted website adapter loaded **4 catalogue rows** and found **3 matching viewing/download resolutions** after successful HLS playlist/segment probes. The existing direct website check independently found the same count of 3 source-declared resolutions for its sample title. This is metadata/sample validation, not full-movie decoding/downloading.
- Direct production-mode Node service checks passed health/schema, required-key rejection and a live catalogue request. These local checks use a temporary test-only key and service; neither becomes the default app endpoint.
- Native ICU 76 accepted the production source pattern, 24 other provider literals and 8 raw patterns; the old closing-brace syntax failure was reproduced separately.

Release package IDs/version codes, signatures, network policies and public artifact hashes are validated before delivery. The native preview remains unpromoted: native service availability was not established by website checks.

Final targeted hardening: **9 API regression tests passed**, including preservation of catalogue artwork/year/rating/intro metadata when details are partial and acceptance of updated IMDb/plot data. The **hosted settings regression also passed** after making validation save an immutable URL/key pair and disabling edits during validation. Existing full-suite and native counts above refer to their archived runs before these focused changes.

The server additionally matches the app's current downet media hosts, direct MP4/DASH master declarations, HTTPS port restrictions, and watch-page recovery when the theme's server endpoints fail. Unrelated ad iframes do not consume the approved route budget. These cases are included in the 13 server tests.

Final server-only live lookups returned two declared HLS routes for sample 2148687 and a direct MP4 declaration for sample 3215087. These are source-resolution checks; a complete MP4 download was not performed. The deployment template gives the non-root runtime ownership of both package metadata and source files.

## Final APK packaging

The final settings regression passed and both assembleWebsiteRelease/assembleNativeApiRelease tasks completed successfully. apksigner verified the v2 signatures and the original development certificate; aapt verified package/version/labels, regular and TV launcher entries, minimum API 26 and non-debuggable packaging. These are development-key sideload builds, not a production-key rotation.

Certificate SHA-256: `23de31aa29f0d532e882abad4b1df80e156f95c05180869aceb9353e7566b101`.

| Flavor | Package | Version/code | APK SHA-256 |
| --- | --- | --- | --- |
| website | app.cinemanatv.cee | 1.3.1 / 13 | `8387ca2075894dedcd785efbcfb56c323d6d221bf67a1be9960753c2f03f92ac` |
| nativeApi | app.cinemanatv.cee.nativepreview | 0.3.0-native-preview / 3 | `5918eca073855aad02f183388d5104f1b57e406d8ce4542319eabd952526dc79` |

Both manifest and compiled network-security XML were checked: website cleartext is disabled; native legacy-media cleartext remains enabled. Release constants select the correct provider. Native's update-feed URL stays blank; website uses the package-checked stable feed.

Source/server archives exclude build/cache output, node_modules, local.properties, real environment files and signing keys. The blank .env.example and locked dependency manifest are included. Public artifact SHA-256 values are compared with local files before advancing the stable feed. APK downloads still open through the browser/Android installer; a separate in-app APK checksum verifier is not claimed.

Native origin recheck during delivery: 503 from this environment. This is independent of successful website/hosted-server checks. No live native promotion was performed.
