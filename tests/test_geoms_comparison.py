import unittest

import raimad as rai

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
            rai.rotated(box_cw_top_right, 1),
            )

        self.assertEqual(
            box_ccw_top_left,
            rai.rotated(box_ccw_top_right, -1),
            )

        self.assertEqual(
            rai.rotated(box_cw_top_left, -1),
            box_cw_top_right,
            )

        self.assertEqual(
            rai.rotated(box_ccw_top_left, 1),
            box_ccw_top_right,
            )

        self.assertEqual(
            rai.rotated(box_ccw_top_right, 4),
            box_ccw_top_right,
            )

        self.assertTrue(
            rai.is_rotated(
                rai.reversed(box_cw_top_right),
                box_ccw_top_right,
            )
        )

        self.assertTrue(
            rai.is_rotated(
                rai.reversed(box_cw_top_left),
                box_ccw_top_left,
            )
        )

        for sqr in all_boxs:
            self.assertFalse(rai.is_rotated(sqr, cross_box))

    def test_poly_comparison(self):

        # Test that none of the box variants are equal to each other
        # under strict comparison
        for first, second in rai.duplets((*all_boxs, cross_box)):
            self.assertFalse(rai.geom.poly_equal(
                first, second, check_rotation=True, check_orientation=True))

        # Check that a box is equal to itself under all
        # types of comparison
        for sqr in (*all_boxs, cross_box):
            self.assertTrue(rai.geom.poly_equal(
                sqr, sqr, check_rotation=True, check_orientation=True))
            self.assertTrue(rai.geom.poly_equal(
                sqr, sqr, check_rotation=False, check_orientation=True))
            self.assertTrue(rai.geom.poly_equal(
                sqr, sqr, check_rotation=False, check_orientation=False))
            self.assertTrue(rai.geom.poly_equal(
                sqr, sqr, check_rotation=True, check_orientation=False))

        # Check that strict orientation checking detects
        # boxes with different orientation
        self.assertFalse(rai.geom.poly_equal(
            box_cw_top_left, box_ccw_top_left,
            check_rotation=False, check_orientation=True))

        self.assertFalse(rai.geom.poly_equal(
            box_cw_top_right, box_ccw_top_right,
            check_rotation=False, check_orientation=True))

        # Check that strict rotation checking detects
        # boxes with different rotation
        self.assertFalse(rai.geom.poly_equal(
            box_cw_top_left, box_cw_top_right,
            check_rotation=True, check_orientation=False))

        self.assertFalse(rai.geom.poly_equal(
            box_ccw_top_left, box_ccw_top_right,
            check_rotation=True, check_orientation=False))

        # check that disabling strict orientation checking
        # actually makes it not care about orientation
        self.assertTrue(rai.geom.poly_equal(
            box_cw_top_left, box_ccw_top_left,
            check_rotation=True, check_orientation=False))

        self.assertTrue(rai.geom.poly_equal(
            box_cw_top_right, box_ccw_top_right,
            check_rotation=True, check_orientation=False))

        # check that disabling strict rotation checking
        # actually makes it not care about rotation
        self.assertTrue(rai.geom.poly_equal(
            box_cw_top_left, box_cw_top_right,
            check_rotation=False, check_orientation=True))

        self.assertTrue(rai.geom.poly_equal(
            box_ccw_top_left, box_ccw_top_right,
            check_rotation=False, check_orientation=True))
        
        # check that under loose comparison (any rotation, any orientation)
        # boxes with different rotation and orientation are the same
        self.assertTrue(rai.geom.poly_equal(
            box_ccw_top_left, box_cw_top_right,
            check_rotation=False, check_orientation=False))


        # Check that none of the box variants are equal to the cross-box
        # under loose comparison
        for sqr in all_boxs:
            self.assertFalse(rai.geom.poly_equal(
                sqr, cross_box,
                check_rotation=False, check_orientation=False))

    def test_polys_comparison_common(self):
        for bitfield in range(0b000, 0b111 + 1):
            check_poly_order = bool(bitfield & (1 << 0))
            check_rotation = bool(bitfield & (1 << 1))
            check_orientation = bool(bitfield & (1 << 2))

            # Identical lists should be equal under all comparison options
            self.assertTrue(rai.geom.polys_equal(
                [shape0, shape1, shape2],
                [shape0, shape1, shape2],
                check_poly_order=check_poly_order,
                check_rotation=check_rotation,
                check_orientation=check_orientation,
                ))

            # empty polys's should be equal under all comparison options
            self.assertTrue(rai.geom.polys_equal(
                [],
                [],
                check_poly_order=check_poly_order,
                check_rotation=check_rotation,
                check_orientation=check_orientation,
                ))

            # single poly
            self.assertTrue(rai.geom.polys_equal(
                [shape0],
                [shape0],
                check_poly_order=check_poly_order,
                check_rotation=check_rotation,
                check_orientation=check_orientation,
                ))

            # Repeated single poly
            self.assertTrue(rai.geom.polys_equal(
                [shape0, shape0, shape0, shape0, shape0],
                [shape0, shape0, shape0, shape0, shape0],
                check_poly_order=check_poly_order,
                check_rotation=check_rotation,
                check_orientation=check_orientation,
                ))

            # Repeated single poly with one extra
            self.assertTrue(rai.geom.polys_equal(
                [shape0, shape0, shape0, shape0, shape1],
                [shape0, shape0, shape0, shape0, shape1],
                check_poly_order=check_poly_order,
                check_rotation=check_rotation,
                check_orientation=check_orientation,
                ))


            # different number of shapes: no matter what, should  never equal
            self.assertFalse(rai.geom.polys_equal(
                [shape1, shape0],
                [shape1, shape0, shape1],
                check_poly_order=check_poly_order,
                check_rotation=check_rotation,
                check_orientation=check_orientation,
                ))

            # Again, different number of shapes, but one is empty.
            # should never equal
            self.assertFalse(rai.geom.polys_equal(
                [],
                [shape2],
                check_poly_order=check_poly_order,
                check_rotation=check_rotation,
                check_orientation=check_orientation,
                ))

            # completely different shapes, but some are same: again, should
            # never equal
            self.assertFalse(rai.geom.polys_equal(
                [shape1, shape0, shape2],
                [shape1, shape0, shape1],
                check_poly_order=check_poly_order,
                check_rotation=check_rotation,
                check_orientation=check_orientation,
                ))


    def test_polys_comparison_strict_order(self):
        # same shapes, different order are not equal with strict
        # order checking...
        self.assertFalse(rai.geom.polys_equal(
            [shape1, shape1, shape0],
            [shape1, shape0, shape1],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        # ...and are equal without strict order checking
        self.assertTrue(rai.geom.polys_equal(
            [shape1, shape1, shape0],
            [shape1, shape0, shape1],
            check_poly_order=False,
            check_rotation=True,
            check_orientation=True,
            ))


    def test_polys_comparison_propagate(self):
        # check_rotation and check_orientation
        # of polys_equal
        # should just propagate
        # to poly_equal

        # first, rotation: equal with strick checking disabled...
        self.assertTrue(rai.geom.polys_equal(
            [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
            [box_ccw_top_left, box_cw_top_right, box_cw_top_left],
            check_poly_order=True,
            check_rotation=False,
            check_orientation=True,
            ))

        # ...and not equal with strict checking enabled.
        self.assertFalse(rai.geom.polys_equal(
            [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
            [box_ccw_top_left, box_cw_top_right, box_cw_top_left],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        # Same thing but now for orientation.
        # Strict checking disabled means should be equal...
        self.assertTrue(rai.geom.polys_equal(
            [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
            [box_cw_top_right, box_ccw_top_left, box_ccw_top_right],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=False,
            ))

        # ...and not equal with strict checking enabled.
        self.assertFalse(rai.geom.polys_equal(
            [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
            [box_cw_top_right, box_ccw_top_left, box_ccw_top_right],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        # Magnum opus of looseness: different order,
        # different orientations, different rotations,
        # but should still be equal under loosest checking
        self.assertTrue(rai.geom.polys_equal(

            [box_ccw_top_right, shape0, shape0,
                box_cw_top_left, box_cw_top_right],

            [shape0, box_cw_top_left, box_ccw_top_left,
                box_cw_top_left, shape0],

            check_poly_order=False,
            check_rotation=False,
            check_orientation=False,
            ))

        # We could test for more permutations here
        # but since it's literally just passing options
        # through to a different function that's already tested,
        # I don't think it's necessary.

    def test_geom_collapse(self):
        coll_rot = rai.geom.coll_rot
        coll_or = rai.geom.coll_or

        # test collapse rotation
        self.assertEqual(
            coll_rot(box_cw_top_left),
            coll_rot(box_cw_top_right),
            )

        self.assertEqual(
            coll_rot(box_ccw_top_left),
            coll_rot(box_ccw_top_right),
            )

        # test collapse both
        # TODO currying..?
        for first, second in rai.duplets(all_boxs):
            self.assertEqual(
                rai.geom.coll_rot_or(first),
                rai.geom.coll_rot_or(second),
                )

        # test collapse orientation TODO
        #self.assertEqual(
        #    coll_rot(box_cw_top_left),
        #    coll_or(box_ccw_top_left),
        #    )

        #self.assertEqual(
        #    coll_rot(box_cw_top_left),
        #    coll_or(box_ccw_top_left),
        #    )

        # test that order of operations doesnt matter
        #for box in all_boxs:
        #    self.assertEqual(
        #        coll_rot(coll_or(box)),
        #        coll_or(coll_rot(box)),
        #        )



if __name__ == '__main__':
    unittest.main()

