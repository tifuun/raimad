import unittest
import itertools

from typing import Iterable

import raimad as rai
from raimad.types import PolyS

all_boxs = (
    # clockwise box starting top left
    box_cw_top_left := [(-1, +1), (+1, +1), (+1, -1), (-1, -1)],
    # clockwise box starting top right
    box_cw_top_right := [(+1, +1), (+1, -1), (-1, -1), (-1, +1)],
    # counter clockwise box starting top left
    box_ccw_top_left := [(-1, +1), (-1, -1), (+1, -1), (+1, +1)],
    # counter clockwise box starting top right
    box_ccw_top_right := [(+1, +1), (-1, +1), (-1, -1), (+1, -1)],
    # weird cross-box thing (not a box)
    )

cross_box = [(+1, +1), (-1, -1), (+1, -1), (-1, +1)]
shape0 = [(1, 1), (10, 10), (10, 1)]
shape1 = [(1, 1), (10, 10), (20, 10), (10, 1)]
shape2 = [(2, 1), (20, 10), (10, 10), (-10, 1)]


class TestGeomsComparison(unittest.TestCase):
    def test_sanity(self):
        for one, two in rai.duplets((*all_boxs, cross_box)):
            self.assertNotEqual(one, two)
            self.assertEqual(set(one), set(two))

        self.assertEqual(
            box_cw_top_left,
            rai.cycled(box_cw_top_right, 1),
            )

        self.assertEqual(
            box_ccw_top_left,
            rai.cycled(box_ccw_top_right, -1),
            )

        self.assertEqual(
            rai.cycled(box_cw_top_left, -1),
            box_cw_top_right,
            )

        self.assertEqual(
            rai.cycled(box_ccw_top_left, 1),
            box_ccw_top_right,
            )

        self.assertEqual(
            rai.cycled(box_ccw_top_right, 4),
            box_ccw_top_right,
            )

        self.assertTrue(
            rai.is_cycled(
                rai.reversed(box_cw_top_right),
                box_ccw_top_right,
            )
        )

        self.assertTrue(
            rai.is_cycled(
                rai.reversed(box_cw_top_left),
                box_ccw_top_left,
            )
        )

        for sqr in all_boxs:
            self.assertFalse(rai.is_cycled(sqr, cross_box))

    def test_poly_comparison(self):

        # Test that none of the box variants are equal to each other
        # under strict comparison
        for first, second in rai.duplets((*all_boxs, cross_box)):
            self.assertFalse(rai.geom.poly_equal(
                (first, second), None))

        # Check that a box is equal to itself under all
        # types of comparison
        for sqr in (*all_boxs, cross_box):
            self.assertTrue(rai.geom.poly_equal(
                (sqr, sqr), rai.geom.canon_rot_or))
            self.assertTrue(rai.geom.poly_equal(
                (sqr, sqr), rai.geom.canon_or))
            self.assertTrue(rai.geom.poly_equal(
                (sqr, sqr), None))
            self.assertTrue(rai.geom.poly_equal(
                (sqr, sqr), rai.geom.canon_or))

        # Check that strict orientation checking detects
        # boxes with different orientation
        self.assertFalse(rai.geom.poly_equal(
            (box_cw_top_left, box_ccw_top_left),
            rai.geom.canon_rot))

        self.assertFalse(rai.geom.poly_equal(
            (box_cw_top_right, box_ccw_top_right),
            rai.geom.canon_rot))

        # Check that strict rotation checking detects
        # boxes with different rotation
        self.assertFalse(rai.geom.poly_equal(
            (box_cw_top_left, box_cw_top_right),
            rai.geom.canon_or))

        self.assertFalse(rai.geom.poly_equal(
            (box_ccw_top_left, box_ccw_top_right),
            rai.geom.canon_or))

        # check that disabling strict orientation checking
        # actually makes it not care about orientation
        self.assertTrue(rai.geom.poly_equal(
            (box_cw_top_left, box_ccw_top_left),
            rai.geom.canon_or))

        self.assertTrue(rai.geom.poly_equal(
            (box_cw_top_right, box_ccw_top_right),
            rai.geom.canon_or))

        # check that disabling strict rotation checking
        # actually makes it not care about rotation
        self.assertTrue(rai.geom.poly_equal(
            (box_cw_top_left, box_cw_top_right),
            rai.geom.canon_rot))

        self.assertTrue(rai.geom.poly_equal(
            (box_ccw_top_left, box_ccw_top_right),
            rai.geom.canon_rot))
        
        # check that under loose comparison (any rotation, any orientation)
        # boxes with different rotation and orientation are the same
        self.assertTrue(rai.geom.poly_equal(
            (box_ccw_top_left, box_cw_top_right),
            rai.geom.canon_rot_or))


        # Check that none of the box variants are equal to the cross-box
        # under loose comparison
        for sqr in all_boxs:
            self.assertFalse(rai.geom.poly_equal(
                (sqr, cross_box),
                rai.geom.canon_rot_or))

    def test_polys_comparison_common(self):
        for canon_polys, canon_poly in itertools.product(
                (None, rai.geom.canon_order),
                (
                    None,
                    rai.geom.canon_or,
                    rai.geom.canon_rot,
                    rai.geom.canon_rot_or
                    ),
                ):

            # Identical lists should be equal under all comparison options
            self.assertTrue(rai.geom.polys_equal(
                (
                    [shape0, shape1, shape2],
                    [shape0, shape1, shape2],
                ),
                canon_polys, canon_poly,
                ))

            # empty polys's should be equal under all comparison options
            self.assertTrue(rai.geom.polys_equal(
                (
                    [],
                    [],
                ),
                canon_polys, canon_poly,
                ))

            # single poly
            self.assertTrue(rai.geom.polys_equal(
                (
                    [shape0],
                    [shape0],
                ),
                canon_polys, canon_poly,
                ))

            # Repeated single poly
            self.assertTrue(rai.geom.polys_equal(
                (
                    [shape0, shape0, shape0, shape0, shape0],
                    [shape0, shape0, shape0, shape0, shape0],
                ),
                canon_polys, canon_poly,
                ))

            # Repeated single poly with one extra
            self.assertTrue(rai.geom.polys_equal(
                (
                    [shape0, shape0, shape0, shape0, shape1],
                    [shape0, shape0, shape0, shape0, shape1],
                ),
                canon_polys, canon_poly,
                ))


            # different number of shapes: no matter what, should  never equal
            self.assertFalse(rai.geom.polys_equal(
                (
                    [shape1, shape0],
                    [shape1, shape0, shape1],
                ),
                canon_polys, canon_poly,
                ))

            # Again, different number of shapes, but one is empty.
            # should never equal
            self.assertFalse(rai.geom.polys_equal(
                (
                    [],
                    [shape2],
                ),
                canon_polys, canon_poly,
                ))

            # completely different shapes, but some are same: again, should
            # never equal
            self.assertFalse(rai.geom.polys_equal(
                (
                    [shape1, shape0, shape2],
                    [shape1, shape0, shape1],
                ),
                canon_polys, canon_poly,
                ))


    def test_polys_comparison_strict_order(self):
        # same shapes, different order are not equal with strict
        # order checking...
        self.assertFalse(rai.geom.polys_equal(
            (
                [shape1, shape1, shape0],
                [shape1, shape0, shape1],
            ),
            None, None,
            ))

        # ...and are equal without strict order checking
        self.assertTrue(rai.geom.polys_equal(
            (
                [shape1, shape1, shape0],
                [shape1, shape0, shape1],
            ),
            rai.geom.canon_order,
            None,
            ))


    def test_polys_comparison_propagate(self):
        # check_rotation and check_orientation
        # of polys_equal
        # should just propagate
        # to poly_equal

        # first, rotation: equal with strick checking disabled...
        self.assertTrue(rai.geom.polys_equal(
            (
                [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
                [box_ccw_top_left, box_cw_top_right, box_cw_top_left],
            ),
            None,
            rai.geom.canon_rot
            ))

        # ...and not equal with strict checking enabled.
        self.assertFalse(rai.geom.polys_equal(
            (
                [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
                [box_ccw_top_left, box_cw_top_right, box_cw_top_left],
            ),
            None, None
            ))

        # Same thing but now for orientation.
        # Strict checking disabled means should be equal...
        self.assertTrue(rai.geom.polys_equal(
            (
                [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
                [box_cw_top_right, box_ccw_top_left, box_ccw_top_right],
            ),
            None, rai.geom.canon_or
            ))

        # ...and not equal with strict checking enabled.
        self.assertFalse(rai.geom.polys_equal(
            (
                [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
                [box_cw_top_right, box_ccw_top_left, box_ccw_top_right],
            ),
            None, None,
            ))

        # Magnum opus of looseness: different order,
        # different orientations, different rotations,
        # but should still be equal under loosest checking
        self.assertTrue(rai.geom.polys_equal(

            (
                [box_ccw_top_right, shape0, shape0,
                    box_cw_top_left, box_cw_top_right],

                [shape0, box_cw_top_left, box_ccw_top_left,
                    box_cw_top_left, shape0],
            ),

            rai.geom.canon_order, rai.geom.canon_rot_or
            ))

        # We could test for more permutations here
        # but since it's literally just passing options
        # through to a different function that's already tested,
        # I don't think it's necessary.

    def test_geom_canon(self):
        canon_rot = rai.geom.canon_rot
        canon_or = rai.geom.canon_or

        # test canon rotation
        self.assertEqual(
            canon_rot(box_cw_top_left),
            canon_rot(box_cw_top_right),
            )

        self.assertEqual(
            canon_rot(box_ccw_top_left),
            canon_rot(box_ccw_top_right),
            )

        # test canon both
        # TODO currying..?
        for first, second in rai.duplets(all_boxs):
            self.assertEqual(
                rai.geom.canon_rot_or(first),
                rai.geom.canon_rot_or(second),
                )

        self.assertEqual(
            canon_or(box_cw_top_left),
            canon_or(box_ccw_top_left),
            )

        self.assertEqual(
            canon_or(box_cw_top_left),
            canon_or(box_ccw_top_left),
            )


if __name__ == '__main__':
    unittest.main()

