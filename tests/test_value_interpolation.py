import unittest
from basiconfig import BasiConfig


class TestJsonConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.bc = BasiConfig(["config.json"])

    def test_name(self):
        self.assertEqual("Jane", self.bc["name"])

    def test_surname(self):
        self.assertEqual("Doe", self.bc["surname"])

    def test_full_name(self):
        self.assertEqual("Jane Doe", self.bc["full_name"])
