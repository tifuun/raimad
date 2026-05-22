import unittest
from math import radians

import raimad as rai

from .utils import ArrayApproxEqual

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
            TwoCircles().proxy().rotate(radians(90))
            )

class TestBBox(ArrayApproxEqual, unittest.TestCase, epsilon=0.01):

    def test_bbox_basic(self):
        circle = rai.Circle(5)

        self.assertArrayApproxEqual(
            list(circle.bbox),
            [-5, -5, 5, 5]
            )
        self.assertApproxEqual(circle.bbox.length, 10)
        self.assertApproxEqual(circle.bbox.width, 10)
        self.assertApproxEqual(circle.bbox.top, 5)
        self.assertApproxEqual(circle.bbox.bottom, -5)
        self.assertApproxEqual(circle.bbox.left, -5)
        self.assertApproxEqual(circle.bbox.right, 5)
        self.assertArrayApproxEqual(
            list(circle.bbox.top_left),
            (-5, 5)
            )
        self.assertArrayApproxEqual(
            list(circle.bbox.top_mid),
            (0, 5)
            )
        self.assertArrayApproxEqual(
            list(circle.bbox.top_right),
            (5, 5)
            )
        self.assertArrayApproxEqual(
            list(circle.bbox.mid_left),
            (-5, 0)
            )
        self.assertArrayApproxEqual(
            list(circle.bbox.mid),
            (0, 0)
            )
        self.assertArrayApproxEqual(
            list(circle.bbox.mid_right),
            (5, 0)
            )
        self.assertArrayApproxEqual(
            list(circle.bbox.bot_left),
            (-5, -5)
            )
        self.assertArrayApproxEqual(
            list(circle.bbox.bot_mid),
            (0, -5)
            )
        self.assertArrayApproxEqual(
            list(circle.bbox.bot_right),
            (5, -5)
            )

    def test_bbox_subcompo(self):
        circles = TwoCircles()

        self.assertArrayApproxEqual(
            list(circles.bbox),
            [-10, -5, 10, 5]
            )
        self.assertApproxEqual(circles.bbox.length, 20)
        self.assertApproxEqual(circles.bbox.width, 10)
        self.assertApproxEqual(circles.bbox.top, 5)
        self.assertApproxEqual(circles.bbox.bottom, -5)
        self.assertApproxEqual(circles.bbox.left, -10)
        self.assertApproxEqual(circles.bbox.right, 10)
        self.assertArrayApproxEqual(
            list(circles.bbox.top_left),
            (-10, 5)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.top_mid),
            (0, 5)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.top_right),
            (10, 5)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.mid_left),
            (-10, 0)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.mid),
            (0, 0)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.mid_right),
            (10, 0)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.bot_left),
            (-10, -5)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.bot_mid),
            (0, -5)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.bot_right),
            (10, -5)
            )

    def test_bbox_transform(self):
        circles = RotatedCircles()

        self.assertArrayApproxEqual(
            list(circles.bbox),
            [-5, -10, 5, 10]
            )
        self.assertApproxEqual(circles.bbox.length, 10)
        self.assertApproxEqual(circles.bbox.width, 20)
        self.assertApproxEqual(circles.bbox.top, 10)
        self.assertApproxEqual(circles.bbox.bottom, -10)
        self.assertApproxEqual(circles.bbox.left, -5)
        self.assertApproxEqual(circles.bbox.right, 5)
        self.assertArrayApproxEqual(
            list(circles.bbox.top_left),
            (-5, 10)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.top_mid),
            (0, 10)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.top_right),
            (5, 10)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.mid_left),
            (-5, 0)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.mid),
            (0, 0)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.mid_right),
            (5, 0)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.bot_left),
            (-5, -10)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.bot_mid),
            (0, -10)
            )
        self.assertArrayApproxEqual(
            list(circles.bbox.bot_right),
            (5, -10)
            )

    def test_bbox_pad(self):
        circles = RotatedCircles()
        bbox = circles.bbox

        self.assertArrayApproxEqual(
            list(bbox),
            [-5, -10, 5, 10]
            )

        self.assertArrayApproxEqual(
            list(bbox.pad(.1)),
            [-5.1, -10.1, 5.1, 10.1]
            )

        self.assertArrayApproxEqual(
            list(bbox.pad(.2, .3)),
            [-5.2, -10.3, 5.2, 10.3]
            )

        with self.assertRaises(TypeError):
            bbox.pad(.2, .3, .4)  # type: ignore
            # Mypy catches it too

        with self.assertRaises(TypeError):
            bbox.pad(.2, .3, .4, .5)  # type: ignore
            # Mypy catches it too

        self.assertArrayApproxEqual(
            list(bbox.pad(left=0.3)),
            [-5.3, -10, 5, 10]
            )

        self.assertArrayApproxEqual(
            list(bbox.pad(bottom=0.4)),
            [-5, -10.4, 5, 10]
            )

        self.assertArrayApproxEqual(
            list(bbox.pad(right=0.2, bottom=0.4)),
            [-5, -10.4, 5.2, 10]
            )

        self.assertArrayApproxEqual(
            list(bbox.pad(right=0.3, bottom=0.4, left=0.1)),
            [-5.1, -10.4, 5.3, 10]
            )

        self.assertArrayApproxEqual(
            list(bbox.pad(.2, top=0.3, bottom=0.4, left=0.1)),
            [-5 - .2 - .1, -10 - .2 - .4, 5 + .2, 10 + .2 + .3]
            )

        self.assertArrayApproxEqual(
            list(bbox.pad(.2, .1, top=0.3, bottom=0.4, left=0.1)),
            [-5 - .2 - .1, -10 - .1 - .4, 5 + .2, 10 + .1 + .3]
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

        self.assertArrayApproxEqual(
            list(bbox),
            [1, 1, 1, 1]
            )

        self.assertFalse(bbox.is_empty())

        # all of these should NOT raise EmptyBBoxError
        bbox.assert_nonempty()
        bbox.top
        bbox.top_mid
        bbox.pad(1, 1)

        bbox.add_point((-2, -3))

        self.assertArrayApproxEqual(
            list(bbox),
            [-2, -3, 1, 1]
            )

    def test_bbox_snapping(self):
        c1 = rai.Proxy(rai.Circle(10))
        c2 = rai.Proxy(rai.Circle(5))
        c3 = rai.Proxy(rai.Circle(2))

        c1.bbox.mid.to((0, 0))
        c2.snap_left(c1)
        c3.bbox.top_mid.to(c1.bbox.mid_right)

        self.assertArrayApproxEqual(rai.vec2s(c1.bbox.mid), (0, 0))
        self.assertArrayApproxEqual(rai.vec2s(c2.bbox.mid), (-10 - 5, 0))
        self.assertArrayApproxEqual(rai.vec2s(c3.bbox.mid), (10, -2))

    def test_bbox_bound(self):
        c1 = rai.Circle(10)
        unbound = c1.bbox

        with self.assertRaises(AttributeError):
            unbound.mid.to((0, 0))  # type: ignore
            # MyPy catches this too

        # TODO there's no easy way here to write an error message like
        # "hey, you tried to do a transform through an unbound bbox,
        # you need to do it through a bound bbox"
        # All you get is a cryptic "tuple has no attribute 'to'"
        # Maybe we need a raidoc page with common errors?

    def test_bbox_copy_transform(self):
        c1 = rai.Circle(10).proxy()

        c1.bbox.pad(5).mid_left.to((0, 0))

        self.assertArrayApproxEqual(
            rai.vec2s(c1.bbox.mid),
            (15, 0)
            )


if __name__ == '__main__':
    unittest.main()

