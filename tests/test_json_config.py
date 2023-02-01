import unittest
from basiconfig import BasiConfig


class TestJsonConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.input = {
            "test_name": "json_config",
            "details.year": 1991,
            "details.month": "October",
            "details.day": 4,
            "messages.0.id": 0,
            "messages.0.title": None,
            "messages.0.message": "not title in this message",
            "messages.1.id": 1,
            "messages.1.title": "second message",
            "messages.1.message": "hello with title"
        }
        self.bc = BasiConfig(["config.json"])

    def test_json_config_values(self):
        for k, v in self.input.items():
            self.assertEqual(v, self.bc[k])
