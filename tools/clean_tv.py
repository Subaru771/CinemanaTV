from pathlib import Path
import sys
root=Path(sys.argv[1]); base=root/'app/src/main/java/app/cinemanatv'
def modify(rel,fn):
 p=base/rel; s=p.read_text(); new=fn(s); p.write_text(new)
def rep(s,a,b=''):
 assert a in s, a[:90]
 return s.replace(a,b)
def cut(s,a,b):
 i=s.index(a); j=s.index(b,i+len(a)); return s[:i]+s[j:]
for name in ['data/CeeAlternativeSource.kt','data/CeeAutomaticMatch.kt','data/CeeWebRoutes.kt','ui/CeeWebScreen.kt','ui/AlternativeSourceDialog.kt']:
 (base/name).unlink()
for p in (root/'app/src/test').rglob('*Cee*Test.kt'): p.unlink()
(root/'ALTERNATIVE-SOURCE.md').unlink(missing_ok=True)

def repo(s):
 s=cut(s,'    suspend fun automaticAlternative(', '    /** Resolve stream URLs ahead of the Play press.')
 for a,b in [
 ('private val episodeCache = DetailCache<List<Video>>()','private val episodeCache = DetailCache<List<Video>>(limit = 8)'),
 ('private suspend fun listOrNull(block: suspend () -> JsonElement)','private suspend fun listOrNull(maxItems: Int = 120, block: suspend () -> JsonElement)'),
 ('Payloads.videos(payload) }','Payloads.videos(payload, maxItems) }'),
 ('private suspend fun list(block: suspend () -> JsonElement): List<Video> = listOrNull(block).orEmpty()','private suspend fun list(maxItems: Int = 120, block: suspend () -> JsonElement): List<Video> = listOrNull(maxItems, block).orEmpty()'),
 ('val pages = if (single) listOf(0, 1, 2) else listOf(0)','val pages = if (single) listOf(0, 1) else listOf(0)'),
 ('withTimeoutOrNull(9_000L) { browse(k, sort, page) }','withTimeoutOrNull(7_500L) { browse(k, sort, page) }'),
 ('if (CeeAlternativeSource.owns(v.id)) return v\n        ',''),
 ('if (CeeAlternativeSource.owns(id)) return emptyList()\n        episodeCache','episodeCache'),
 ('if (CeeAlternativeSource.owns(id)) return emptyList()\n        relatedCache','relatedCache'),
 ('if (CeeAlternativeSource.owns(id)) return CeeAlternativeSource.resolve(id)\n',''),
 ('return list { api.episodes(id) }','return list(maxItems = 5_000) { api.episodes(id) }'),
 ('if (CeeAlternativeSource.owns(id)) emptyList()\n        else withContext(Dispatchers.Default) { Payloads.subtitles(api.subtitles(id)) }','withContext(Dispatchers.Default) { Payloads.subtitles(api.subtitles(id)) }')]: s=rep(s,a,b)
 return cut(s,'        if (recentVideoId != null && CeeAlternativeSource.owns(recentVideoId)) {','        val catalog = try {')
modify('data/Repository.kt',repo)
modify('data/Prefs.kt',lambda s:cut(s,'    private fun validAlternative(id: String): Boolean','    // ---- Android TV Watch Next integration'))

def vm(s):
 for a in ['    data class Web(val url: String) : Screen\n','    var catalogWebFallbackOpened = false\n','            is Screen.Web -> if (contentFilterMode == ContentFilterMode.OFF &&\n                app.cinemanatv.data.CeeWebRoutes.validStart(s.url)) stack.add(s)\n']: s=rep(s,a)
 return s
modify('ui/AppViewModel.kt',vm)

def activity(s):
 s=rep(s,'current is Screen.Play || current is Screen.Web','current is Screen.Play')
 s=rep(s,'vm.stack.last() is Screen.Play || vm.stack.last() is Screen.Web','vm.stack.last() is Screen.Play')
 s=cut(s,'            onAlternativePlay = { alternative ->','        ) }')
 return rep(s,'        is Screen.Web -> androidx.compose.runtime.key(screen.url) {\n            app.cinemanatv.ui.CeeWebScreen(screen.url, onExit = { vm.pop() }, onRegisterBack = onPlayerBackChanged)\n        }\n')
modify('MainActivity.kt',activity)

def home(s):
 s=cut(s,'    LaunchedEffect(error, data) {','    val d = data')
 return rep(s,'                AppButton(if (LocalInterfaceLanguage.current == "ar") "تصفح المصدر البديل" else "Browse alternative source") {\n                    vm.push(Screen.Web(app.cinemanatv.data.CeeWebRoutes.HOME))\n                }\n')
modify('ui/Home.kt',home)
modify('ui/Detail.kt',lambda s:rep(s,'                    if (vm != null) AppButton(if (LocalInterfaceLanguage.current == "ar") "فتح مشغل CEE" else "Open CEE player") {\n                        vm.push(Screen.Web(app.cinemanatv.data.CeeWebRoutes.title(info)))\n                    }\n'))
modify('ui/Settings.kt',lambda s:rep(s,'                        SettingsCard(label("CEE alternative source", "مصدر CEE البديل"),\n                            label("The CEE website player opens automatically when the original source fails. You can also open its catalog here.",\n                                "يفتح مشغل موقع CEE تلقائياً عند تعذر تشغيل المصدر الأصلي. يمكنك أيضاً فتح فهرسه من هنا.")) {\n                            AppButton(label("Browse alternative source", "تصفح المصدر البديل")) {\n                                vm.push(Screen.Web(app.cinemanatv.data.CeeWebRoutes.HOME))\n                            }\n                        }\n'))

def player(s):
 for a in ['    onAlternativePlay: (Video) -> Unit = {},\n    onWebFallback: ((String) -> Unit)? = null,\n','    var showAlternative by remember { mutableStateOf(false) }\n',
           '    var alternativeAttempted by remember(video.id) { mutableStateOf(false) }\n    var checkingAlternative by remember(video.id) { mutableStateOf(false) }\n    var alternativeNote by remember(video.id) { mutableStateOf("") }\n',
           '    val alternativeNotice = if (LocalInterfaceLanguage.current == "ar") "تم التبديل إلى المصدر البديل" else "Switched to alternative source"\n',
           '        if (app.cinemanatv.data.CeeAlternativeSource.owns(video.id)) {\n            detailInfo = video\n            detailLookupComplete = true\n            return@LaunchedEffect\n        }\n',
           '        if (app.cinemanatv.data.CeeAlternativeSource.owns(video.id)) {\n            matureSkipMessage = "Mature skip unavailable · alternative source has no verified markers"\n            return@LaunchedEffect\n        }\n',
           '            if (!alternativeAttempted && !app.cinemanatv.data.CeeAlternativeSource.owns(video.id) &&\n                prefs.contentFilterMode == app.cinemanatv.data.ContentFilterMode.OFF) {\n                player.pause()\n                buffering = false\n                fetchError = "Original stream is not starting. Applying alternative source."\n                controlsVisible = true\n                continue\n            }\n',
           '                checkingAlternative -> rootRequester.requestFocus()\n',
           '                if (alternativeNote.isNotBlank()) Text(alternativeNote, color = Muted, fontSize = 13.sp)\n',
           '                if (checkingAlternative) CinemaSpinner()\n                if (!checkingAlternative) {\n',
           '                }\n                PlayerTile(if (LocalInterfaceLanguage.current == "ar") "البحث في المصدر البديل" else "Find alternative source", "↗",\n                    onClick = { showAlternative = true })\n']:
  s=rep(s,a)
 s=cut(s,'        LaunchedEffect(Unit) {\n            if (onWebFallback != null','        var showError by remember')
 s=cut(s,'    if (showAlternative) AlternativeSourceDialog(', '    var sources by remember')
 s=cut(s,'    // All terminal lookup, decoder, network and repeated-stall errors converge on fetchError.', '    // Temporary decoder/network failures get bounded re-prepare attempts before')
 for a,b in [
  ('            } else if (app.cinemanatv.data.CeeAlternativeSource.owns(video.id)) {\n                Services.repo.loadSources(video.id)\n            } else withTimeoutOrNull(12_000L) { Services.repo.loadSources(video.id) }','            } else withTimeoutOrNull(12_000L) { Services.repo.loadSources(video.id) }'),
  ('              fetchError = if (app.cinemanatv.data.CeeAlternativeSource.owns(video.id))\n                  error.message ?: "Alternative source unavailable."\n              else NetworkResilience.diagnose(context, error).message','              fetchError = NetworkResilience.diagnose(context, error).message'),
  ('LaunchedEffect(controlsVisible, sheet, fetchError, finished, video.id, checkingAlternative)','LaunchedEffect(controlsVisible, sheet, fetchError, finished, video.id)'),
  ('Text(t(if (checkingAlternative) "Checking alternative source…" else "Playback unavailable"),','Text(t("Playback unavailable"),')]: s=rep(s,a,b)
 return s
modify('ui/Player.kt',player)
def episode_parser(s):
 s=rep(s,'"episodes", "season", "files"', '"episodes", "season", "seasons", "episodeList", "videoSeason", "videoSeasons", "files"')
 s=rep(s,'if (depth > 5 || results.size >= maxItems) return','if (depth > (if (maxItems > 120) 10 else 5) || results.size >= maxItems) return')
 return s
modify('data/Payloads.kt',episode_parser)

p=root/'app/build.gradle.kts'; p.write_text(p.read_text().replace('versionCode = 125','versionCode = 126').replace('versionName = "1.4.3"','versionName = "1.4.4"'))

p=root/'app/src/test/java/app/cinemanatv/data/PayloadsTest.kt'
s=p.read_text()
test='''    @Test fun returnsEveryEpisodeFromNestedSeasons() {
        val episodes = com.google.gson.JsonArray()
        (1..320).forEach { index ->
            val ep = com.google.gson.JsonObject()
            ep.addProperty("nb", index.toString())
            ep.addProperty("en_title", "Episode " + index)
            ep.addProperty("season", ((index - 1) / 80 + 1).toString())
            ep.addProperty("episodeNummer", ((index - 1) % 80 + 1).toString())
            episodes.add(ep)
        }
        val payload = JsonParser.parseString("""{"result":{"data":{"seasons":[{"episodes":[]}]}}}""").asJsonObject
        payload.getAsJsonObject("result").getAsJsonObject("data").getAsJsonArray("seasons")[0]
            .asJsonObject.add("episodes", episodes)
        val found = Payloads.videos(payload, maxItems = 5_000)
        assertEquals(320, found.size)
        assertEquals(4, found.last().seasonNumber)
    }

'''
s=rep(s,'    @Test fun parsesReferenceModelFieldNames() {',test+'    @Test fun parsesReferenceModelFieldNames() {')
p.write_text(s)


# Remove the obsolete CEE-pairing test, retaining crash-report redaction tests.
p=root/'app/src/test/java/app/cinemanatv/util/CrashReportsTest.kt'
q=p.read_text()
q=cut(q,'    @Test fun confirmedPairingPersistsOnlyAlternativeIdentity()', '    @Test fun savedReportRedactsStreamTokensAndHeaders()')
p.write_text(q)

terms=['CeeAlternativeSource','CeeWebRoutes','CeeWebScreen','AlternativeSourceDialog','Screen.Web','onAlternativePlay','onWebFallback','checkingAlternative','alternativeAttempted']
assert not [(p,t) for p in base.rglob('*.kt') for t in terms if t in p.read_text()]
print('Cleaned TV source; episode limit 5000')
