from unittest import TestCase
from utils.misc import SatisfySemVer, to_semver


class TestSatisfySemver(TestCase):
    def test_basic(self):
        self.assertEqual(SatisfySemVer("Hello World!".encode()).data, "Hello World!".encode())
        self.assertEqual(SatisfySemVer("Hello World!".encode()).data, "Hello World!".encode())

    def test_r_a(self):
        self.assertEqual(
            SatisfySemVer.from_semver(SatisfySemVer("Hello World!".encode()).semver()).semver(),
            (2429212711, 3728781022, 1919706145, 'd')
        )
