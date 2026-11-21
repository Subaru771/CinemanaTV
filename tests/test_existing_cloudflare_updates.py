import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
script_path = ROOT / "tools" / "build_existing_cloudflare_updates.py"
spec = importlib.util.spec_from_file_location("cloudflare_updates", script_path)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)

def sample():
    return {
        "schema": 1,
        "tv": {
            "enabled": False,
            "version": "1.21",
            "versionCode": 127,
            "downloadUrl": "https://github.com/Subaru771/CinemanaTV",
            "notes": {"en": "TV update", "ar": "تحديث التلفزيون"}
        },
        "ios": {
            "enabled": False,
            "version": "2.1.2",
            "build": 30,
            "downloadUrl": "https://github.com/Subaru771/Cinemana-IOS",
            "notes": {"en": "iOS update", "ar": "تحديث آيفون"}
        }
    }

class CloudflareManifestTests(unittest.TestCase):
    def test_preserves_two_channels(self):
        value = sample()
        self.assertEqual(tool.validate(value), value)
        self.assertIn("ios", value)
    def test_enabled_requires_https(self):
        value = sample()
        value["tv"]["enabled"] = True
        value["tv"]["downloadUrl"] = "http://example.org/update.apk"
        with self.assertRaises(ValueError):
            tool.validate(value)
    def test_enabled_rejects_credentials(self):
        value = sample()
        value["ios"]["enabled"] = True
        value["ios"]["downloadUrl"] = "https://user:password@example.org/ipa"
        with self.assertRaises(ValueError):
            tool.validate(value)
    def test_invalid_schema_fails(self):
        value = sample()
        value["schema"] = 2
        with self.assertRaises(ValueError):
            tool.validate(value)
    def test_rejects_missing_ios(self):
        value = sample()
        del value["ios"]
        with self.assertRaises(ValueError):
            tool.validate(value)
    def test_paused_channels_stay_paused(self):
        value = sample()
        checked = tool.validate(value)
        self.assertFalse(checked["tv"]["enabled"])
        self.assertFalse(checked["ios"]["enabled"])
    def test_ios_build_comparison_keeps_integer(self):
        value = sample()
        value["ios"]["enabled"] = True
        value["ios"]["version"] = "2.1.3"
        value["ios"]["build"] = 31
        self.assertEqual(tool.validate(value)["ios"]["build"], 31)
    def test_rejects_float_code(self):
        value = sample()
        value["tv"]["versionCode"] = 127.1
        with self.assertRaises(ValueError):
            tool.validate(value)

if __name__ == "__main__":
    unittest.main()
