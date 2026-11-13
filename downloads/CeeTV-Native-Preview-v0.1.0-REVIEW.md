# Second opinion and implementation choices

The review's main concerns are reasonable, but two factual assumptions need correction. The inspected Cee TV source hard-codes cinamana.cc, not the Soft31 landing hostname. The recovered Leanback client targets cee.buzz/api/android/, not the unmodified Shabakaty API. Merely finding Retrofit, Leanback, download libraries and remote config does not prove which backend is used or that runtime behavior is correct. The decoded App Cloner configuration has proxies disabled and no host mappings; there is no configured network relay to duplicate.

## Smooth TV behavior

Keep the catalogue/stream contract stable, then profile the actual slow path. Separate the player engine/session, source/quality state and control composables. Extracting helper functions alone does not fix network latency, recomposition, focus loss or decoder stalls. Keep heavy work off the main thread, bound/cancel lookups, prefetch after settled focus, show cached catalogue data and load optional subtitles/markers independently. Use stable item IDs and restore focus by ID when returning from details. Validate D-pad repeats, quality switching at the current position, slow Wi-Fi, episode auto-next and app background/resume on real TVs; use frame/decoder measurements rather than line count as the performance criterion.

## API and scraper boundary

Use the recovered native API as one provider adapter and the verified website scraper as another. Each implements the same catalogue/details/episodes/files interface with explicit provider identity. Do not pass a website post ID into a native lookup or auto-select a similarly named film from another catalogue. An HTML 200, unknown JSON envelope, refusal, empty result and network timeout are different states.

The native preview implements native reads with cancellable bounded HTTP, typed normalization, guest-only headers, direct resolution/URL mapping, fresh stream lookups and separate native IDs/cache. Website fallback remains a separate product/provider choice rather than a hidden response to API failure. A cleaner scraper should isolate selectors/parsers, version captured sanitized fixtures, follow the actual entry/player path, preserve required sessions/headers where verified, retain HLS audio/subtitle structure and distinguish catalogue success from media delivery. Never cache expiring playback tokens to persistent preferences or invent quality URLs.

## Signing and phone layout

Preserve and privately back up the exact stable signing key before changing build configuration. Check signer fingerprint, application ID and version code before distribution. Use a controlled release key/CI secret store for production, with failure on missing production signing configuration. A repository name differing from the app name is cosmetic; a stable HTTPS feed and correct package/signing identity matter. Publishing a new signing key under the existing application ID requires a verified rotation/migration plan.

Portrait is a screen-by-screen responsive design task. Keep one navigation/playback state model; adapt navigation and layouts using available window size, and handle landscape player orientation through lifecycle effects that restore the previous request on exit. Cover Home, Movies/Series collections, Search/keyboard, Settings, Downloads and Details. Test 360/412dp portrait, phone landscape, large font scale, rotation with open details/download chooser, and D-pad TV behavior. Do not infer compact-layout coverage from tests at 720dp and above.

Claude's edited source was not attached, so its split composables, signing implementation and orientation changes have not been compiled or reviewed here. This preview starts from the locally verified Cee TV 1.2.2 source and isolates the native provider change. A production/native-backend promotion still needs a successful real API capture and device playback.
