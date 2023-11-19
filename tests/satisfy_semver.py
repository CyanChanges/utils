from unittest import TestCase
from utils.misc import SatisfySemver, to_semver, semver_stringify


class TestSatisfySemver(TestCase):
    def test_basic(self):
        self.assertEqual(
            SatisfySemver("There is very very very long text!!!".encode()).data,
            "There is very very very long text!!!".encode()
        )
        self.assertEqual(SatisfySemver("Some text here!".encode()).data, "Some text here!".encode())

    def test_basic2(self):
        semver = SatisfySemver("vivo 50".encode()).semver()
        self.assertEqual(SatisfySemver.from_semver(semver).data, "vivo 50".encode())

    def test_r_a(self):
        self.assertEqual(
            (1214606483, 1864390511, 491444773152, 'd0'),
            SatisfySemver.from_semver(SatisfySemver("Hello World!".encode()).semver()).semver()
        )

    def test_to_semver(self):
        self.assertEqual(to_semver('0.0.0'), (0, 0, 0))
        self.assertEqual(to_semver('1.2.3'), (1, 2, 3))
        self.assertEqual(to_semver('2.3.3-a'), (2, 3, 3, 'a'))
        self.assertEqual(to_semver('2.3.3-b'), (2, 3, 3, 'b'))

    def test_stringify_semver(self):
        self.assertEqual(semver_stringify((0, 0, 0)), '0.0.0')
        self.assertEqual(semver_stringify((1, 2, 3)), '1.2.3')
        self.assertEqual(semver_stringify((1, 2, 3, 'a')), '1.2.3-a')
        self.assertEqual(semver_stringify((2, 3, 3, 'b')), '2.3.3-b')
