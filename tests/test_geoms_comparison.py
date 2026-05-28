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
    cross_box := [(+1, +1), (-1, -1), (+1, -1), (-1, +1)],
    )

shape0 = [(1, 1), (10, 10), (10, 1)]
shape1 = [(1, 1), (10, 10), (20, 10), (10, 1)]
shape2 = [(2, 1), (20, 10), (10, 10), (-10, 1)]

class TestGeomsComparison(unittest.TestCase):
    def test_sanity(self):
        for one, two in rai.duplets(all_boxs):
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

        for sqr in (
                box_cw_top_left,
                box_cw_top_right,
                box_ccw_top_left,
                box_ccw_top_right,
                ):

            self.assertFalse(rai.is_rotated(sqr, cross_box))

    def test_poly_comparison(self):
        for first, second in rai.duplets(all_boxs):
            self.assertFalse(rai.geom.poly_equal(
                first, second, check_rotation=True, check_orientation=True))

        for sqr in all_boxs:
            self.assertTrue(rai.geom.poly_equal(
                sqr, sqr, check_rotation=True, check_orientation=True))
            self.assertTrue(rai.geom.poly_equal(
                sqr, sqr, check_rotation=False, check_orientation=True))
            self.assertTrue(rai.geom.poly_equal(
                sqr, sqr, check_rotation=False, check_orientation=False))
            self.assertTrue(rai.geom.poly_equal(
                sqr, sqr, check_rotation=True, check_orientation=False))

        self.assertFalse(rai.geom.poly_equal(
            box_cw_top_left, box_ccw_top_left,
            check_rotation=False, check_orientation=True))

        self.assertFalse(rai.geom.poly_equal(
            box_cw_top_right, box_ccw_top_right,
            check_rotation=False, check_orientation=True))

        self.assertFalse(rai.geom.poly_equal(
            box_cw_top_left, box_cw_top_right,
            check_rotation=True, check_orientation=False))

        self.assertFalse(rai.geom.poly_equal(
            box_ccw_top_left, box_ccw_top_right,
            check_rotation=True, check_orientation=False))

        ###

        self.assertTrue(rai.geom.poly_equal(
            box_cw_top_left, box_ccw_top_left,
            check_rotation=True, check_orientation=False))

        self.assertTrue(rai.geom.poly_equal(
            box_cw_top_right, box_ccw_top_right,
            check_rotation=True, check_orientation=False))

        self.assertTrue(rai.geom.poly_equal(
            box_cw_top_left, box_cw_top_right,
            check_rotation=False, check_orientation=True))

        self.assertTrue(rai.geom.poly_equal(
            box_ccw_top_left, box_ccw_top_right,
            check_rotation=False, check_orientation=True))
        
        ###

        self.assertTrue(rai.geom.poly_equal(
            box_ccw_top_left, box_cw_top_right,
            check_rotation=False, check_orientation=False))


        for sqr in (
                box_cw_top_left,
                box_cw_top_right,
                box_ccw_top_left,
                box_ccw_top_right,
                ):

            self.assertFalse(rai.geom.poly_equal(
                sqr, cross_box,
                check_rotation=False, check_orientation=False))

    def test_polys_comparison(self):
        self.assertTrue(rai.geom.polys_equal(
            [shape0, shape1, shape2],
            [shape0, shape1, shape2],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        self.assertTrue(rai.geom.polys_equal(
            [],
            [],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        self.assertTrue(rai.geom.polys_equal(
            [shape0],
            [shape0],
            [box_ccw_top_right],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        self.assertTrue(rai.geom.polys_equal(
            [shape0, shape0, shape0, shape0, shape0],
            [shape0, shape0, shape0, shape0, shape0],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        self.assertTrue(rai.geom.polys_equal(
            [shape0, shape0, shape0, shape0, shape1],
            [shape0, shape0, shape0, shape0, shape1],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        ####

        self.assertFalse(rai.geom.polys_equal(
            [shape1, shape0],
            [shape1, shape0, shape1],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        self.assertFalse(rai.geom.polys_equal(
            [shape1, shape0, shape2],
            [shape1, shape0, shape1],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        self.assertFalse(rai.geom.polys_equal(
            [shape1, shape1, shape0],
            [shape1, shape0, shape1],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        self.assertFalse(rai.geom.polys_equal(
            [],
            [shape2],
            check_poly_order=True,
            check_rotation=True,
            check_orientation=True,
            ))

        ###

        self.assertTrue(rai.geom.polys_equal(
            [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
            [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
            check_poly_order=False,
            check_rotation=True,
            check_orientation=True,
            ))

        self.assertTrue(rai.geom.polys_equal(
            [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
            [box_ccw_top_right, box_cw_top_right, box_cw_top_left],
            check_poly_order=False,
            check_rotation=True,
            check_orientation=True,
            ))

        ###


        self.assertFalse(rai.geom.polys_equal(
            [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
            [box_ccw_top_right, box_cw_top_right],
            check_poly_order=False,
            check_rotation=True,
            check_orientation=True,
            ))

        ###

        self.assertFalse(rai.geom.polys_equal(
            [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
            [box_ccw_top_right, box_cw_top_left, box_cw_top_right],
            check_poly_order=False,
            check_rotation=True,
            check_orientation=True,
            ))




if __name__ == '__main__':
    unittest.main()

