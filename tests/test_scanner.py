import unittest

from wsprobe.scanner import validate_local_url


class TargetScopeTests(unittest.TestCase):
    def test_accepts_loopback_targets(self):
        for url in (
            "ws://localhost:8765",
            "ws://127.0.0.1:8765",
            "wss://[::1]:8765",
        ):
            with self.subTest(url=url):
                validate_local_url(url)

    def test_rejects_non_loopback_target(self):
        with self.assertRaisesRegex(ValueError, "only scans localhost/loopback"):
            validate_local_url("ws://example.com:8765")

    def test_rejects_invalid_scheme(self):
        with self.assertRaisesRegex(ValueError, "must start with ws:// or wss://"):
            validate_local_url("http://127.0.0.1:8765")


if __name__ == "__main__":
    unittest.main()
