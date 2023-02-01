import unittest
from basiconfig import BasiConfig


class TestJsonConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.bc = BasiConfig(["interpolation.json"])

    def test_name(self):
        self.assertEqual("Filip", self.bc["name"])

    def test_surname(self):
        self.assertEqual("Skóraś", self.bc["surname"])

    def test_full_name(self):
        self.assertEqual("Filip Skóraś", self.bc["full_name"])
