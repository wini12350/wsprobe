import unittest
from wsprobe.classifier import classify_message

class ClassifierTests(unittest.TestCase):
    def test_normal_json(self):
        self.assertEqual(classify_message('{"status":"ok"}'), "normal_reply")
    def test_error_json(self):
        self.assertEqual(classify_message('{"status":"error"}'), "error_reply")
    def test_non_json_text(self):
        self.assertEqual(classify_message("hello"), "normal_reply")
    def test_silence(self):
        self.assertEqual(classify_message(None), "silence")

if __name__ == "__main__":
    unittest.main()
