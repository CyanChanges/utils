from unittest import TestCase
from utils.misc import SatisfySemVer, to_semver, semver_stringify


class TestSatisfySemver(TestCase):
    def test_basic(self):
        self.assertEqual(SatisfySemVer("Hello World!".encode()).data, "Hello World!".encode())
        self.assertEqual(SatisfySemVer("Hello World!".encode()).data, "Hello World!".encode())

    def test_r_a(self):
        self.assertEqual(
            SatisfySemVer.from_semver(SatisfySemVer("Hello World!".encode()).semver()).semver(),
            (2429212711, 3728781022, 1919706145, 'd')
        )

    def test_to_semver(self):
        self.assertEqual(to_semver('0.0.0'), (0, 0, 0))
        self.assertEqual(to_semver('1.2.3'), (1, 2, 3))
        self.assertEqual(to_semver('2.3.3-a'), (2, 3, 3, 'a'))
        self.assertEqual(to_semver('2.3.3-b'), (2, 3, 3, 'b'))

    def test_stringify_semver(self):
        self.assertEquals(semver_stringify((0, 0, 0)), '0.0.0')
        self.assertEquals(semver_stringify((1, 2, 3)), '1.2.3')
        self.assertEquals(semver_stringify((1, 2, 3, 'a')), '1.2.3-a')
        self.assertEquals(semver_stringify((2, 3, 3, 'b')), '2.3.3-b')
