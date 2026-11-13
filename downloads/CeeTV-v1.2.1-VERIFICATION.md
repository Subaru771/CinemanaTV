# Cee TV 1.2.1 verification

Focused pointer tests passed for one-tap activation, distinct long press, swiping without opening a card, opening/closing native player menus, timeline release seeking, series resume/start actions and phone landscape navigation/settings. They inject pointer events, not accessibility-click substitutes. Existing remote interaction tests remain in the suite.

Data regressions cover quoted/reordered/extended provider source objects, escaped query characters, commented legacy sources, source reuse after consumed prefetch, Arabic episode/season parsing, chronological batches/queues and most-recent episode resume. The source-level live quality test passed with three declared HLS resolutions matching between viewing and download choices. It does not establish full-movie decoding or every title/provider.

The combined UI run exposed test-process timing leaks between renderer/screen configurations. Test classes use isolated JVMs and phone/TV configurations are separated, retaining all assertions. Final regression counts and signed package checks are recorded below before publication.

No physical phone or TV testing was available. Existing provider outages/access refusals, single-resolution files and official VK player controls remain limitations. Successful metadata caches are in-memory and short lived; signed URLs are not added to persistent settings.

Final validation: 232 deterministic tests passed; eight optional live tests skipped (240 total, zero failures/errors). All eight remote and eight pointer UI tests passed, including phone landscape, drag seek, resume ordering and quality controls. Separate live viewing/download quality inventory check passed with three published resolutions. Native ICU checks passed. Package app.cinemanatv.cee, code 10/version 1.2.1, with the same certificate as prior Cee TV builds verified before publication.
