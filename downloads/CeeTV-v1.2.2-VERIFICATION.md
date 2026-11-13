# Cee TV 1.2.2 verification

The regression suite includes the actual native player quality menu: a source with numbered adaptive options must show its real resolutions and tapping 720p must pass the matching source to the engine. A failing decoder fixture keeps the test independent of remote media access; it does not verify hardware decoding.

Inventory tests cover a later source adding resolutions after a working first source, an unavailable source, partial results while another source is blocked, cancellation, deduplication and preservation of the master for audio/subtitles. Menu regression tests cover one current video track alongside a complete provider inventory, partial declarations, numbered HLS choices and their originating servers. Current direct-MP4/HLS/DASH parser tests cover the observed CDN declaration and rejection of lookalike domains, credentials and unapproved paths.

Live browser evidence and native APK findings are detailed in REFERENCE-APK-FINDINGS.md. Native API connectivity failed with HTTP 503 here. HLS metadata was retrieved for the existing regression sample. No physical phone/TV or full-movie decoding was tested. Provider outages, single-encode files and official VK controls remain limitations.

Final automated counts and signed APK validation are appended before publication.

Final validation: 249 deterministic tests passed; eight optional live tests skipped (257 total, zero failures/errors). The actual player-menu tap test passed, including selecting a numbered adaptive source. Separate live quality inventory check matched three published resolutions between the merged viewing inventory and downloads. Native ICU checks passed. Package app.cinemanatv.cee, version code 11/name 1.2.2 and the same certificate as previous Cee TV builds were verified before publication.
