import unittest
from math import pi

import raimad as rai

from .utils import ArrayAlmostEqual


class TestAngspace(unittest.TestCase, ArrayAlmostEqual):

    def test_angspace_pos(self):
        self.assertArrayAlmostEqual(
            rai.angspace(0, 2 * pi, 4, rai.Orientation.POS, True),
            [0, pi / 2, pi, 3 / 4 * pi, 2 * pi]
            )

    def test_angspace_pos_noendpoint(self):
        self.assertArrayAlmostEqual(
            rai.angspace(0, 2 * pi, 4, rai.Orientation.POS, False),
            [0, (3 / 4 * pi) * 1 / 3, (3 / 4 * pi) * 2 / 3, (3 / 4 * pi) * 3 / 3]
            )

    def test_angspace_wrong_orientation(self):
        self.assertArrayAlmostEqual(
            rai.angspace(0, 2 * pi, 4, rai.Orientation.NEG, False),
            []
            )

    def test_angspace_start_is_end(self):
        self.assertArrayAlmostEqual(
            rai.angspace(0, 0, 4, rai.Orientation.NEG, False),
            []
            )

    def test_angspace_neg_and_pos(self):
        self.assertArrayAlmostEqual(
            rai.angspace(pi, 0, 4, rai.Orientation.NEG, True),
            [pi, 2 / 3 * pi, 1 / 3 * pi, 0]
            )

        self.assertArrayAlmostEqual(
            rai.angspace(pi, 0, 4, rai.Orientation.POS, True),
            [pi, 4 / 3 * pi, 5 / 3 * pi, 2 * pi]
            )

        self.assertArrayAlmostEqual(
            rai.angspace(0, pi, 4, rai.Orientation.NEG, True),
            [2 * pi, 5 / 3 * pi, 4 / 3 * pi, pi]
            )

        self.assertArrayAlmostEqual(
            rai.angspace(0, pi, 4, rai.Orientation.POS, True),
            [0, 1 / 3 * pi, 2 / 3 * pi, pi]
            )

    def test_angspace_neg_noendpoint(self):
        self.assertArrayAlmostEqual(
            rai.angspace(pi, 0, 4, rai.Orientation.NEG, False),
            [pi, 1 / 4 * pi * (1 / 3), 1 / 4 * pi * (2 / 3), 0]
            )

    def test_angspace_zerosteps(self):
        self.assertArrayAlmostEqual(
            rai.angspace(5, 9, 0, rai.Orientation.POS, True),
            []
            )

    def test_angspace_pos_zerocross(self):
        self.assertArrayAlmostEqual(
            rai.angspace(-pi / 4, pi / 4, 3, rai.Orientation.POS, True),
            [7 / 4 * pi, 2 * pi, 9 / 4 * pi]
            )



if __name__ == '__main__':
    unittest.main()

