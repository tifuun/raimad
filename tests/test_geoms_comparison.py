import unittest

import raimad as rai

all_squares = (
    # clockwise square starting top left
    square_cw_top_left := [(-1, +1), (+1, +1), (+1, -1), (-1, -1)],
    # clockwise square starting top right
    square_cw_top_right := [(+1, +1), (+1, -1), (-1, -1), (-1, +1)],
    # counter clockwise square starting top left
    square_ccw_top_left := [(-1, +1), (-1, -1), (+1, -1), (+1, +1)],
    # counter clockwise square starting top right
    square_ccw_top_right := [(+1, +1), (-1, +1), (-1, -1), (+1, -1)],
    # weird cross-square thing (not a square)
    cross_square := [(+1, +1), (-1, -1), (+1, -1), (-1, +1)],
    )

class TestGeomsComparison(unittest.TestCase):
    def test_sanity(self):
        for one, two in rai.duplets(all_squares):
            self.assertNotEqual(one, two)
            self.assertEqual(set(one), set(two))

        self.assertEqual(
            square_cw_top_left,
            rai.rotated(1, square_cw_top_right),
            )

        self.assertEqual(
            square_ccw_top_left,
            rai.rotated(-1, square_ccw_top_right),
            )

        self.assertEqual(
            rai.rotated(-1, square_cw_top_left),
            square_cw_top_right,
            )

        self.assertEqual(
            rai.rotated(1, square_ccw_top_left),
            square_ccw_top_right,
            )

        self.assertEqual(
            rai.rotated(4, square_ccw_top_right),
            square_ccw_top_right,
            )

        self.assertTrue(
            rai.is_rotated(
                rai.reversed(square_cw_top_right),
                square_ccw_top_right,
            )
        )

        self.assertTrue(
            rai.is_rotated(
                rai.reversed(square_cw_top_left),
                square_ccw_top_left,
            )
        )

        for sqr in (
                square_cw_top_left,
                square_cw_top_right,
                square_ccw_top_left,
                square_ccw_top_right,
                ):

            self.assertFalse(rai.is_rotated(sqr, cross_square))


if __name__ == '__main__':
    unittest.main()

