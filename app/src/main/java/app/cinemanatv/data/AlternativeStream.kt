package app.cinemanatv.data

import java.net.URI

/** Only explicit, user-provided, direct HTTPS media URLs. No scraping or bypass. */
object AlternativeStream {
    fun isValid(value: String): Boolean = try {
        val uri = URI(value)
        uri.scheme.equals("https", ignoreCase = true) &&
            !uri.host.isNullOrBlank() && uri.userInfo == null &&
            uri.port in -1..65535 &&
            value.length <= 4096 &&
            !value.any { it == '\n' || it == '\r' } &&
            listOf(".mp4", ".m3u8", ".mpd", ".webm", ".mkv").any { ext ->
                uri.path.orEmpty().lowercase().endsWith(ext)
            }
    } catch (_: Exception) { false }
}
