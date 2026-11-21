#!/usr/bin/env python3
"""Build the existing cinemana-updates-e8l Pages project, preserving the live feed on bootstrap."""
from __future__ import annotations

import json
import pathlib
import sys
import urllib.error
import urllib.request

BASE = pathlib.Path(__file__).resolve().parents[1]
SOURCE = BASE / "updates" / "cloudflare.json"
LIVE = "https://cinemana-updates-e8l.pages.dev/updates.json"
OUTPUT = BASE / "cloudflare-updates" / "updates.json"
MODERN_TV = BASE / "updates" / "tv.json"


def validate(raw: object) -> dict:
    if not isinstance(raw, dict) or raw.get("schema") != 1:
        raise ValueError("Expected update schema 1.")
    for channel, numeric in (("tv", "versionCode"), ("ios", "build")):
        value = raw.get(channel)
        if not isinstance(value, dict):
            raise ValueError(f"Missing {channel} update data.")
        if type(value.get("enabled")) is not bool:
            raise ValueError(f"{channel}.enabled must be true or false.")
        v = value.get("version", "")
        n = value.get(numeric)
        if not isinstance(v, str) or len(v) > 32:
            raise ValueError(f"Invalid {channel}.version.")
        if type(n) is not int or n < 0 or n > 2147483647:
            raise ValueError(f"Invalid {channel}.{numeric}.")
        notes = value.get("notes")
        if not isinstance(notes, dict):
            raise ValueError(f"Missing {channel}.notes.")
        if any(not isinstance(notes.get(lang), str) or len(notes[lang]) > 240 for lang in ("en", "ar")):
            raise ValueError(f"Invalid {channel} language notes.")
        link = value.get("downloadUrl", "")
        if not isinstance(link, str) or len(link) > 2048:
            raise ValueError(f"Invalid {channel} download URL.")
        if value["enabled"]:
            from urllib.parse import urlparse
            parsed = urlparse(link)
            if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
                raise ValueError(f"{channel} requires an HTTPS download URL when enabled.")
            if not v or n == 0:
                raise ValueError(f"{channel} must have a version and positive build code when enabled.")
    return raw


def source() -> dict:
    if SOURCE.exists():
        print("Using GitHub-controlled updates/cloudflare.json")
        return validate(json.loads(SOURCE.read_text(encoding="utf-8")))
    print("First deployment: retrieving current PRODUCTION /updates.json rather than guessing/replacing its values.")
    request = urllib.request.Request(LIVE, headers={"User-Agent": "Cinemana-update-deployment/1.0", "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.load(response)
    except (OSError, urllib.error.URLError, ValueError) as err:
        raise RuntimeError("Could not fetch existing Cloudflare manifest. Deployment stopped; production left unchanged.") from err
    return validate(result)


def prepare():
    manifest = source()
    OUTPUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Staged safe /updates.json with both TV and iOS channels.")
    for platform in ("tv", "ios"):
        d = manifest[platform]
        print(platform, d.get("version"), "ENABLED" if d["enabled"] else "disabled")


def sync():
    manifest = validate(json.loads(OUTPUT.read_text(encoding="utf-8")))
    tv = manifest["tv"]
    if tv["versionCode"] < 127:
        print("Keeping v1.21+ GitHub update feed unchanged: production Cloudflare TV code is older.")
        return
    MODERN_TV.parent.mkdir(exist_ok=True)
    MODERN_TV.write_text(json.dumps({"schema": 1, "tv": tv}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Mirrored TV notifications for v1.21+ builds into updates/tv.json.")


if __name__ == "__main__":
    operation = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    if operation == "prepare":
        prepare()
    elif operation == "sync":
        sync()
    else:
        raise SystemExit("Use prepare or sync.")
