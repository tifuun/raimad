import unittest

import raimad as rai

from .utils import GeomsEqual, ArrayAlmostEqual

class TestPolys(GeomsEqual, ArrayAlmostEqual, unittest.TestCase):

    def test_rectlw(self):
        rect = rai.RectLW(10, 20)
        self.assertGeomsEqual(
            rect.geoms,
            {
                'root': [
                    [
                        [-5, -10],
                        [5, -10],
                        [5, 10],
                        [-5, 10]
                        ],
                    ]
                }
            )

    def test_circle(self):
        circle = rai.Circle(69)
        points = circle.geoms['root'][0]
        self.assertGreaterEqual(len(points), 10)
        for point in points:
            self.assertAlmostEqual(
                rai.affine.norm(point),
                69
                )

    def test_custompoly(self):
        """
        Test CustomPoly
        """
        poly = rai.CustomPoly([
            [10, 10],
            [20, 10],
            [20, 30],
            ])
        self.assertGeomsEqual(
            poly.geoms,
            {
                'root': [
                    [
                        [10, 10],
                        [20, 10],
                        [20, 30],
                        ],
                    ]
                }
            )

    def test_custompoly_marks(self):
        """
        Test CustomPoly with dynamic marks
        """
        poly = rai.CustomPoly([
            ['start', [10, 10]],
            [20, 10],
            ['end', [20, 30]],
            ])
        self.assertGeomsEqual(
            poly.geoms,
            {
                'root': [
                    [
                        [10, 10],
                        [20, 10],
                        [20, 30],
                        ],
                    ]
                }
            )
        self.assertEqual(
            poly.marks.start,
            (10, 10)
            )
        self.assertEqual(
            poly.marks.end,
            (20, 30)
            )


if __name__ == '__main__':
    unittest.main()

