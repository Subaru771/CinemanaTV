# Cee TV hosted website API 1.1.0

This optional Node.js service centralizes the cinamana.cc website parser and a shared two-minute, 32 MiB catalogue cache. It is independent of the native cee.buzz API. It returns provider media URLs; it does not relay video bytes or remove network restrictions on the media hosts.

## Deploy with HTTPS

Use a VPS/server with Docker Compose, a real DNS name pointing to it, and inbound ports 80/443 available. From this directory:

1. Copy `.env.example` to `.env`.
2. Set `CEE_SERVER_DOMAIN` to the actual hostname, without a scheme/path.
3. Generate a key with `openssl rand -hex 32` and privately put it in `CEE_API_KEY`. Do not commit `.env` or paste the key into public issues.
4. Run `docker compose up -d --build`.
5. Caddy obtains and renews the HTTPS certificate. Check `docker compose logs api https` if DNS/certificate validation fails.
6. In Cee TV 1.3.1, open Settings > Diagnostics > Catalogue provider. Enter `https://your-hostname/` and its key, then choose **Test and use server**. Applying a valid provider restarts browsing; history/list/downloads remain. **Use direct website** restores on-device access. Native Preview ignores these website-server settings.

The production server refuses to start without a key of at least 24 characters. Only the HTTPS proxy publishes ports; the API container runs as the node user with a read-only filesystem. Do not expose port 8787 directly to the internet. If using a different proxy, set `TRUST_PROXY_HOPS` to the known number of trusted forwarding hops (0 by default, 1 for the supplied Caddy topology). Never trust arbitrary forwarded client addresses.

The shared key provides a basic access gate, not account-based user authentication: an app user can extract a key stored on their own device. Public deployments needing per-user quotas should use individual credentials and a corresponding authorization service. Do not put administrator credentials or upstream account tokens in this field.

No hosting account, domain, or live public endpoint is bundled. This service must be deployed before hosted mode can be used; the APK defaults to its existing direct website provider.

## Run without Docker

Node 22 or newer:

```sh
npm ci --ignore-scripts
npm test
NODE_ENV=production CEE_API_KEY='your-generated-key' npm start
```

Put the process behind an HTTPS reverse proxy and configure the app with that public HTTPS URL. For loopback-only development you can omit NODE_ENV/key. The Android production app still requires HTTPS. Keep TLS certificate verification enabled. A proxy-specific CA needed during CI/build must be mounted as a temporary secret, not copied into the image or source archive.

## Contract

Every endpoint uses `x-api-key` when configured. `/api/health` returns `{ok:true,schema:1,provider:"cee-website"}`. Successful JSON and errors carry `Cache-Control: no-store`; catalogue HTML is cached internally. Playback/player pages are freshly fetched and expiring media URLs are not persisted.

- GET `/api/home?kind=1|2`: `featured`, `rows`, optional row `section` metadata.
- GET `/api/search?q=...`: `results`; accepts an actual provider watch-page URL as well as text.
- GET `/api/detail/:id?title=...&kind=...`: Video fields.
- GET `/api/browse?category=...&page=...&kind=...`: WordPress category-page results.
- GET `/api/episodes/:id?title=...`: chronological `episodes`, pagination `cursors`.
- GET `/api/episodes/:id/more?seasonId=...&page=...&currentPostId=...&season=...&title=...`: one episode chunk.
- GET `/api/related/:id`: related page cards.
- GET `/api/subtitles/:id`: published watch-page `<track>` entries, when available. Empty means no supported declaration was found; it does not invent subtitles. Embedded HLS audio/subtitle groups remain in the master playlist for Media3.
- POST `/api/sources/:id`: body `{rejected:["previously-failed-URL"]}`, response `{qualities:[{height,url,name,mimeType}],vkPlayerUrl}`. GET remains supported for an empty rejection list. Request bodies are capped at 128 KiB and compression is rejected.

Website IDs stay `cee_<postId>`; series IDs keep the existing title/year hash. Native `cee_api_*` identities are not translated or guessed. Android normalizes episode parent IDs against the series actually opened.

## Recovery and limits

Source resolution tries the site's three known server slots and multiple approved embed candidates; one iframe failure does not stop recovery. Numbered entries sharing a master URL remain distinct by URL AND height. Quoted/reordered fields, escaped query characters, dimensions, codec labels and Arabic digits are covered by tests. The Android adapter additionally checks HLS playlists/segments from the device and uses the existing shared viewing/download inventory logic.

HTTP responses are capped at 2,000,000 bytes while reading. Redirect destinations are checked individually against the configured/approved HTTPS page hosts and public DNS addresses. Concurrent catalogue lookups share one pending request; failures are not cached. Rate limits, a finite active-request limit, an overall request deadline and cancellation constrain upstream work. No arbitrary URL-fetching endpoint is exposed. Public network egress should additionally block internal/private addresses at deployment level; application DNS checks alone cannot provide complete DNS-rebinding isolation.

If HTML changes, update this parser and redeploy the server. Provider outages, changed hosts, missing subtitle declarations, DRM/account requirements, and media-server reachability still need separate handling. This is a maintained scraper, not an official provider API or an all-network playback guarantee.

## Tests

`npm test` runs HTTP route/serialization tests, parser regressions, response limits, redirect checks and cache behavior, plus the original parser smoke tests. In the full app source, the HTTP tests write the exact server response fixtures read by Android `CeeApiCatalogTest`; the standalone server package writes them under its own test folder instead.

The optional Android `CeeHostedLiveTest` requires CEE_LIVE_TEST=1, CEE_HOSTED_TEST_URL and CEE_HOSTED_TEST_KEY, supplied privately as environment variables. It checks actual catalogue, HLS playlist/segment reachability and matching viewing/download heights. It does not test physical-device decoding or download a full movie.
