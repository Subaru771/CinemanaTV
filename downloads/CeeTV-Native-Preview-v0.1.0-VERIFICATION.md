# Native preview verification

New contract tests use synthetic JSON built from the recovered field/route definitions. They exercise real local HTTP requests, provider IDs/groups/page sizes, literal file-lookup spelling, search encoding, guest headers, no-store playback lookups, partial search recovery, season ordering and parent identity, direct resolution/URL pairs, subtitle types, native intro timestamps, rejection of HTML 200/unknown JSON and visible service failure. They are not captured successful native production responses.

New native UI tests exercise provider series-card identity/twelve-item collection pagination and a visible API failure with a reachable Downloads action. Existing pointer, remote, playback-engine, download-choice and parsing tests remain in the suite. Physical TV/phone and live native playback were not tested.

Known live limitation: cee.buzz and exact API routes returned HTTP 503 connection timeouts here. Soft31 landing/API-looking paths returned HTML 200. See REVERSE-ENGINEERING-MAP.md.

The preview has a separate application ID and no default update feed. Its default release-type APK is development-key signed for testing. Optional production signing requires all four properties; the production flag must reject missing keys. No keys, local properties, reference APK assets or build directories are included in the source archive.

Final test counts and APK/package/signing checks are appended before publication.

Final validation: 269 tests passed; eight optional legacy website live tests skipped (277 total, zero failures/errors). This includes 20 new native contract/parser/UI tests. Native production JSON and playback remain unverified. Both missing-production-key and partial-signing configuration guards were exercised and correctly rejected. Native ICU checks passed. The APK signature, Cee TV Native label, separate application ID/version and empty default update feed were verified. The distributed preview uses the development certificate, not production signing.
