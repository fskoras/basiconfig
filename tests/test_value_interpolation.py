import unittest
from subconfig import SubConfig


class TestJsonConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config = SubConfig(["config.json"])

    def test_name(self):
        self.assertEqual("Jane", self.config["name"])

    def test_surname(self):
        self.assertEqual("Doe", self.config["surname"])

    def test_full_name(self):
        self.assertEqual("Jane Doe", self.config["full_name"])
