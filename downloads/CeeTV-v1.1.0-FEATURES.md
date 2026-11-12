# Cinemana TV feature audit for Cee TV 1.1.0

The native player, preferences and local library were carried forward from the user's Cinemana TV source. This build does not reintroduce the original Shabakaty API/authentication into a CEE-backed app.

| Area | State |
|---|---|
| TV D-pad navigation and Back handling | Retained; settings category navigation and collection restoration refined |
| English / Arabic interface | Retained; new category/action labels localized |
| Home, Series, Movies | Real category rows and paged category grids added; hero scrolls with content |
| Catalogue identities | Original numeric CEE page IDs and stable series IDs retained; display cleanup does not change IDs |
| Search | Type, genre, year, rating, sorting and marker filters retained; optional detail loading retrieves source-declared genres/ratings for up to 24 results |
| Details / series | Source synopsis, genre/rating extraction, season selection and episode pages; source-advertised extra episode pages can be loaded natively |
| My List, history, Continue Watching | Device-local functionality retained |
| Native playback | Quality, Auto/Preferred limits, audio selection, speed, aspect, seek, resume, error recovery and external-player action retained |
| Subtitles | Native track/language/style/size/position/delay and supported synchronization controls retained; tracks must exist in the media/provider |
| Episode playback | Native loaded-queue auto-next, preloading and three-episode prompt retained; Load more episodes extends the list before choosing a queue |
| Scene/intro/credits skipping | Controls retained; requires trustworthy markers for the exact source cut and runtime. No fabricated IDs or timestamps |
| Downloads | Numbered MP4 and Auto HLS/DASH fixes retained; progress, retry/cancel/delete, storage selection and completed offline playback retained. Adaptive media uses device storage |
| Storage and diagnostics | Cache/preload controls, storage checks, separate catalogue/media checks and last-error report retained |
| Android TV launcher | Watch Next preference and integration retained |
| Update notices | Separate Cee TV HTTPS feed restored; startup check, 24-hour reminder, version skip and manual About check |
| Telegram | Existing @CinemanaHub invitation restored with persistent opt-out and Settings access |
| Branding | Original native vector C / play / E logo, matching launcher/banner and branded startup page |
| Genuine VK embeds | Official embedded player retained. Native offline/markers/resume/automatic-next do not apply to VK's own player |

Public provider data determines title availability, ratings, subtitles and marker coverage. The public CEE route does not expose an account/cloud-library API; no account synchronization is claimed. APK updates open the system handler/browser; APK installation remains a user action.
