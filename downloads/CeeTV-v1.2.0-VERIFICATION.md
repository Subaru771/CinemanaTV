# Cee TV 1.2.0 verification

Focused networking tests passed for actual OkHttp call cancellation before headers and during a stalled body, ordinary completion and consumer errors. Source-search tests cover checked-server priority, retaining inconclusive declared candidates and cancellation propagation. HLS tests cover long playlists, relative URLs, alternate renditions including equal heights, redirected bases and trying a second master for download choices.

A targeted live CEE test passed: source lookup, HLS master, child playlist and MPEG-TS segment bytes were readable. This is a sampled delivery-path check, not sustained playback or verification of the complete catalogue. The optional full set of provider tests is not claimed to pass.

TV interaction tests cover the rail, search return destination, download retry, Details actions, the loading Quality button, quality access after an injected engine preparation failure, and Home scroll/focus after returning from details. The engine-failure UI test injects a preparation exception; it does not claim a physical decoder failure was reproduced. Report tests verify that signed media paths/queries and private headers are removed.

Visual previews use real source catalogue artwork rendered at 1280x720, including Arabic Home and Details. Android 12+ blur is a platform effect and is not represented by the SDK 28 render. No physical Android TV or sustained full-movie playback test was performed.

Final regression counts, package/signature checks and public artifact verification are recorded before distribution.

Final validation: 218 deterministic tests passed; seven optional live tests skipped (225 total, zero failures/errors). All eight remote UI tests passed, including the loading/error Quality controls, rail/search navigation and return-to-card focus/scroll. Separate targeted live HLS master/variant/segment check passed. Native ICU checks passed. Package app.cinemanatv.cee, code 9/version 1.2.0, with the same certificate as prior Cee TV builds verified before publication.
