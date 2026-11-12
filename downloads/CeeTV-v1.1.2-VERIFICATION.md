# Cee TV 1.1.2 verification

Initial live probe: `hlsVariantAndSegmentAreReadable` passed on the CEE test title. The broad catalogue/details/source probe timed out inside `CeeAlternativeSource.document` while reading a catalogue page; it was not a video-playback failure. The previous build's direct-CDN/API failures are not represented as passing checks here.

New deterministic regression tests cover HLS rendition parsing and relative URLs, rejecting a readable master with a denied child or segment, retaining master/audio groups for downloads, resolution-free masters, partial catalogue failures and fully unavailable catalogues. UI checks exercise retrying a failed download lookup, choosing a real category and playing/saving from details with a TV remote action.

First regression run: 196 passed, seven optional live tests skipped (203 total). The final run and final signed APK are checked before publishing. Visual renders are inspected at 1280x720, including Arabic Home and Details.

No physical TV testing or sustained full-movie decoding was available. A small readable segment does not establish that every variant/key/segment is available. Genuine VK uses the official embedded player's quality controls.

The new live verification initially rejected a long media playlist at its size limit. A direct diagnostic confirmed all three declared renditions (266/532/800 video pixels high) returned readable playlists and MPEG-TS segment bytes. The reader was corrected to consume a bounded prefix rather than rejecting long full-movie playlists, with a regression test retaining over one megabyte unread. This intermediate failure is preserved in the investigation; final live results are recorded below.

After correcting prefix reading, the final targeted live test passed: source resolution, HLS master, variant playlist and MPEG-TS segment bytes were readable. The separate direct HTTP diagnostic reached playlist and segment data for all three source-declared renditions. Remote UI tests also exposed delayed initial focus taking focus back from category/Quality actions; those cases are guarded and covered by tests. Original MP4 downloads without a declared height now remain selectable without claiming a resolution.

Final validation: 202 deterministic tests passed; seven optional live tests skipped (209 total, zero failures/errors). All four remote UI tests passed, including opening Quality while loading. Separate targeted live HLS master/variant/segment check passed. Native ICU checks passed. Package app.cinemanatv.cee, code 8/version 1.1.2, with the same certificate as prior Cee TV builds verified before publication.
