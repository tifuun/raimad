import unittest

import numpy as np

import pycif as pc


class TestPolys(unittest.TestCase):

    def test_angle_between(self):
        self.assertAlmostEqual(
            pc.angle_between((0, 0), (10, 0)),
            np.deg2rad(0))

        self.assertAlmostEqual(
            pc.angle_between((0, 0), (100, 0)),
            np.deg2rad(0))

        self.assertAlmostEqual(
            pc.angle_between((10, 0), (100, 0)),
            np.deg2rad(0))

        self.assertAlmostEqual(
            pc.angle_between((10, 0), (-100, 0)),
            np.deg2rad(180))

        self.assertAlmostEqual(
            pc.angle_between((10, 10), (20, 20)),
            np.deg2rad(45))

    def test_polar(self):
        self.assertIsNone(np.testing.assert_array_almost_equal(
            pc.polar(np.deg2rad(60), 2),
            (1, np.sqrt(3))
            ))

        self.assertIsNone(np.testing.assert_array_almost_equal(
            pc.polar(np.deg2rad(-60), 2),
            (1, -np.sqrt(3))
            ))

        self.assertIsNone(np.testing.assert_array_almost_equal(
            pc.polar(np.deg2rad(180), 100),
            (-100, 0)
            ))



if __name__ == '__main__':
    unittest.main()

