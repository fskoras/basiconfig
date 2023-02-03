import unittest
from subconfig import SubConfig


class TestJsonConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config = SubConfig(["config.json"])

    def test_doted_access_id(self):
        self.assertEqual(1, self.config["messages.1.id"])  # direct access preserve type
        self.assertEqual("1", self.config["opened_id"])  # value substitution works only with strings

    def test_doted_access_title(self):
        self.assertEqual("second message", self.config["messages.1.title"])
        self.assertEqual("second message", self.config["opened_title"])

    def test_doted_access_message(self):
        self.assertEqual("hello with title", self.config["messages.1.message"])
        self.assertEqual("hello with title", self.config["opened_message"])
