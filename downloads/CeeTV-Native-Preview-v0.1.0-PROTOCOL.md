# CEE Leanback protocol map

Reference APK SHA-256: `8fe238852b46bf2a69431781ff22e384d7727f987aa495914f0b4f9d8444ea7e`.
Package `com.shabakaty.cbox.cee`, version 4.5.4. The packed main DEX was decoded locally and its DEX SHA-1 integrity verified. JADX reconstructed the main classes; 25 decompilation errors elsewhere mean this is a targeted protocol investigation, not a claim of complete source recovery. Critical data-flow paths were also inspected as bytecode.

No reference bytecode, reconstructed Java files, assets or embedded keys are redistributed here.

## Read paths used by the APK

| Consumer | Relative API route | Contract |
| --- | --- | --- |
| Banner | banner/level/{level} | VideoModel array |
| Home groups | videoGroups/lang/{language}/kindGroup/{kind} | groups[] with title, groupsID, content[] |
| Group pagination | videoGroups/groupID/{id}/page/{page}/itemsPerPage/{size} | VideoModel array; additional pages start after page zero |
| Listings | video/videoKind/{type}/categoryNb/{cat}/langNb/{lang}/sortParam/{sort}/itemsPerPage/{size}/searchTextValue/{query}/pageNumber/{page} | VideoModel array |
| Search | video/V/2/videoKind/{type}/itemsPerPage/20/video_title_search/{query} | Base64 NO_WRAP, Uri.encode, then normal Retrofit Path encoding |
| Details | allVideoInfo/id/{id} | VideoModel; translations and introSkipping live here |
| Seasons | videoSeason/id/{id} | Episodes with rootSeries, season, episodeNummer |
| Related | relatedVideos/id/{id}/kind/{kind} | VideoModel array |
| Playback | transcoddedfiles/id/{id} | TranscodedFile array: resolution, videoUrl, container, name |

Evidence classes: b.i.a.a.b.h (Retrofit definitions), b.i.a.a.b.g (API client, request interceptor and search transform), Models.VideoGroupModel and Models.Groups (home schema), Models.TranscodedFile and Models.VideoFile (quality model), player.PlayerFragment and b.i.a.a.o.r.b (quality switch), Activities.SeriesActivity (seasons), Models.Translation and VideoModel getters (subtitle fields).

The player builds its choices from the returned resolution labels, switches to the corresponding videoUrl and restores its position. It does not manufacture five resolutions for every title. The source/download path uses those same returned files. Subtitles are represented by translations[] with name, extention (provider spelling), and file. Intro timing is supplied in seconds.

The API request interceptor uses Android-TV/version/device fields and adds Authorization and Non-Translated only when account state supplies them. Guest reads do not contain a universal token. The APK also contains licence/category/device-signature and account-mutation paths; these are not replicated or bypassed by this guest adapter.

## Live observations

On 2026-11-13, the exact native group/banner/listing routes and cee.buzz/home returned connection-timeout HTTP 503 responses from this environment. No valid live native catalogue/file JSON or hardware playback was obtained.

The supplied Soft31 address serves a landing page; /2.html embeds https://cee.buzz/home. API-looking paths on the Soft31 hostname return the same landing HTML with HTTP 200. That hostname is not established as an interchangeable API base.

The old Cee TV source instead hard-codes https://cinamana.cc/ and parses its website. Its successful website HLS tests do not establish the native CEE API's availability or equivalent catalogue/quality coverage.

## App Cloner configuration

The separate App Cloner DEX and encrypted cloneSettings resource were decoded locally. The configuration contains HTTP proxy=false, SOCKS proxy=false, an empty mappedHosts list and an empty SOCKS proxy list. Thus no App Cloner network relay or hostname remapping is configured in this APK. The presence of HostMapper/proxy classes alone was not evidence that they were active.

The configuration also sets keepScreenOn=true, disableNetworkingWhenScreenOff=false and exitAppOnScreenOff=false. These are configuration facts, not a physical-device verification of all ScreenOff behavior. Device-identity modifications are not copied. Raw configuration, embedded keys and device values are excluded from the delivered source.
