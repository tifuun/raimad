import unittest

import numpy as np

import raimad as rai

from .utils import ArrayAlmostEqual

class TwoCircles(rai.Compo):
    """
    TwoCircles
    Two circles of radius 5 side-by-side on the x axis
    """
    def _make(self):
        self.subcompos.append(
            rai.Circle(5).proxy().movex(-5)
            )
        self.subcompos.append(
            rai.Circle(5).proxy().movex(5)
            )

class RotatedCircles(rai.Compo):
    """
    RotatedCircles
    Two circles of radius 5 side-by-side on the y axis
    """
    def _make(self):
        self.subcompos.append(
            TwoCircles().proxy().rotate(np.deg2rad(90))
            )

class TestBBox(ArrayAlmostEqual, unittest.TestCase, decimal=2):

    def test_bbox_basic(self):
        circle = rai.Circle(5)

        self.assertArrayAlmostEqual(
            circle.bbox,
            np.array([-5, -5, 5, 5])
            )
        self.assertAlmostEqual(circle.bbox.length, 10)
        self.assertAlmostEqual(circle.bbox.width, 10)
        self.assertAlmostEqual(circle.bbox.top, 5)
        self.assertAlmostEqual(circle.bbox.bottom, -5)
        self.assertAlmostEqual(circle.bbox.left, -5)
        self.assertAlmostEqual(circle.bbox.right, 5)
        self.assertArrayAlmostEqual(
            circle.bbox.top_left,
            (-5, 5)
            )
        self.assertArrayAlmostEqual(
            circle.bbox.top_mid,
            (0, 5)
            )
        self.assertArrayAlmostEqual(
            circle.bbox.top_right,
            (5, 5)
            )
        self.assertArrayAlmostEqual(
            circle.bbox.mid_left,
            (-5, 0)
            )
        self.assertArrayAlmostEqual(
            circle.bbox.mid,
            (0, 0)
            )
        self.assertArrayAlmostEqual(
            circle.bbox.mid_right,
            (5, 0)
            )
        self.assertArrayAlmostEqual(
            circle.bbox.bot_left,
            (-5, -5)
            )
        self.assertArrayAlmostEqual(
            circle.bbox.bot_mid,
            (0, -5)
            )
        self.assertArrayAlmostEqual(
            circle.bbox.bot_right,
            (5, -5)
            )

    def test_bbox_subcompo(self):
        circles = TwoCircles()

        self.assertArrayAlmostEqual(
            circles.bbox,
            np.array([-10, -5, 10, 5])
            )
        self.assertAlmostEqual(circles.bbox.length, 20)
        self.assertAlmostEqual(circles.bbox.width, 10)
        self.assertAlmostEqual(circles.bbox.top, 5)
        self.assertAlmostEqual(circles.bbox.bottom, -5)
        self.assertAlmostEqual(circles.bbox.left, -10)
        self.assertAlmostEqual(circles.bbox.right, 10)
        self.assertArrayAlmostEqual(
            circles.bbox.top_left,
            (-10, 5)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.top_mid,
            (0, 5)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.top_right,
            (10, 5)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.mid_left,
            (-10, 0)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.mid,
            (0, 0)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.mid_right,
            (10, 0)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.bot_left,
            (-10, -5)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.bot_mid,
            (0, -5)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.bot_right,
            (10, -5)
            )

    def test_bbox_transform(self):
        circles = RotatedCircles()

        self.assertArrayAlmostEqual(
            circles.bbox,
            np.array([-5, -10, 5, 10])
            )
        self.assertAlmostEqual(circles.bbox.length, 10)
        self.assertAlmostEqual(circles.bbox.width, 20)
        self.assertAlmostEqual(circles.bbox.top, 10)
        self.assertAlmostEqual(circles.bbox.bottom, -10)
        self.assertAlmostEqual(circles.bbox.left, -5)
        self.assertAlmostEqual(circles.bbox.right, 5)
        self.assertArrayAlmostEqual(
            circles.bbox.top_left,
            (-5, 10)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.top_mid,
            (0, 10)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.top_right,
            (5, 10)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.mid_left,
            (-5, 0)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.mid,
            (0, 0)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.mid_right,
            (5, 0)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.bot_left,
            (-5, -10)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.bot_mid,
            (0, -10)
            )
        self.assertArrayAlmostEqual(
            circles.bbox.bot_right,
            (5, -10)
            )

    def test_bbox_pad(self):
        circles = RotatedCircles()
        bbox = circles.bbox

        self.assertArrayAlmostEqual(
            bbox,
            np.array([-5, -10, 5, 10])
            )

        self.assertArrayAlmostEqual(
            bbox.pad(.1),
            np.array([-5.1, -10.1, 5.1, 10.1])
            )

        self.assertArrayAlmostEqual(
            bbox.pad(.2, .3),
            np.array([-5.2, -10.3, 5.2, 10.3])
            )

        with self.assertRaises(TypeError):
            bbox.pad(.2, .3, .4)

        with self.assertRaises(TypeError):
            bbox.pad(.2, .3, .4, .5)

        self.assertArrayAlmostEqual(
            bbox.pad(left=0.3),
            np.array([-5.3, -10, 5, 10])
            )

        self.assertArrayAlmostEqual(
            bbox.pad(bottom=0.4),
            np.array([-5, -10.4, 5, 10])
            )

        self.assertArrayAlmostEqual(
            bbox.pad(right=0.2, bottom=0.4),
            np.array([-5, -10.4, 5.2, 10])
            )

        self.assertArrayAlmostEqual(
            bbox.pad(right=0.3, bottom=0.4, left=0.1),
            np.array([-5.1, -10.4, 5.3, 10])
            )

        self.assertArrayAlmostEqual(
            bbox.pad(.2, top=0.3, bottom=0.4, left=0.1),
            np.array([-5 - .2 - .1, -10 - .2 - .4, 5 + .2, 10 + .2 + .3])
            )

        self.assertArrayAlmostEqual(
            bbox.pad(.2, .1, top=0.3, bottom=0.4, left=0.1),
            np.array([-5 - .2 - .1, -10 - .1 - .4, 5 + .2, 10 + .1 + .3])
            )

    def test_bbox_manual(self):
        bbox = rai.BBox()

        self.assertTrue(bbox.is_empty())

        with self.assertRaises(rai.err.EmptyBBoxError):
            bbox.assert_nonempty()

        with self.assertRaises(rai.err.EmptyBBoxError):
            bbox.top

        with self.assertRaises(rai.err.EmptyBBoxError):
            bbox.top_mid

        with self.assertRaises(rai.err.EmptyBBoxError):
            bbox.pad(1, 1)

        bbox.add_point((1, 1))

        self.assertArrayAlmostEqual(
            bbox,
            np.array([1, 1, 1, 1])
            )

        self.assertFalse(bbox.is_empty())

        # all of these should NOT raise EmptyBBoxError
        bbox.assert_nonempty()
        bbox.top
        bbox.top_mid
        bbox.pad(1, 1)

        bbox.add_point((-2, -3))

        self.assertArrayAlmostEqual(
            bbox,
            np.array([-2, -3, 1, 1])
            )

    def test_bbox_snapping(self):
        c1 = rai.Proxy(rai.Circle(10))
        c2 = rai.Proxy(rai.Circle(5))
        c3 = rai.Proxy(rai.Circle(2))

        c1.bbox.mid.to((0, 0))
        c2.snap_left(c1)
        c3.bbox.top_mid.to(c1.bbox.mid_right)

        self.assertArrayAlmostEqual(c1.bbox.mid, (0, 0))
        self.assertArrayAlmostEqual(c2.bbox.mid, (-10 - 5, 0))
        self.assertArrayAlmostEqual(c3.bbox.mid, (10, -2))


if __name__ == '__main__':
    unittest.main()

