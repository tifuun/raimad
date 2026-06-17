import unittest

import raimad as rai
import cift as cf

import math

class TestExactOrthogonalRotations(unittest.TestCase):
    def test_exact_orthogonal_rotations_square(self):
        class Square(rai.Compo):
            def _make(self):
                self.geoms.update({
                    'root': [
                        [
                            (-1, -1),
                            (+1, -1),
                            (+1, +1),
                            (-1, +1),
                            ]
                        ]
                    })

        sqr0 = (
            Square(),
            Square().proxy(),
            )
        # TODO rotate by zero degrees causes empty bbox..?
        #sqr0_2 = Square().proxy().rotate(_0)
        # TODO print bound point from empty bbox -- error...??

        sqr1 = (
            Square().proxy().orotate(1),
            sqr0[1].proxy().orotate(1),
            )

        sqr2 = (
            Square().proxy().orotate(2),
            sqr1[1].proxy().orotate(1),
            )

        sqr3 = (
            Square().proxy().orotate(3),
            sqr2[1].proxy().orotate(1),
            sqr2[1].proxy().orotate(-5),
            )

        sqr4 = (
            Square().proxy().orotate(4),
            sqr3[1].proxy().orotate(1),
            Square().proxy().orotate(-4),
            )

        # Sanity about how floating point works
        self.assertNotEqual(1e-14, 0)
        self.assertNotEqual(1e-20, 0)
        self.assertNotEqual(0.1 * 3, 0.3)
        self.assertEqual(0.125 * 6, 0.75)

        for sqr in sqr0:
            self.assertEqual(sqr.bbox.top_left,  (-1, +1))
            self.assertEqual(sqr.bbox.top_right, (+1, +1))
            self.assertEqual(sqr.bbox.bot_left,  (-1, -1))
            self.assertEqual(sqr.bbox.bot_right, (+1, -1))

        for sqr in sqr1:
            self.assertEqual(sqr.bbox.top_left,  (-1, +1))
            self.assertEqual(sqr.bbox.top_right, (+1, +1))
            self.assertEqual(sqr.bbox.bot_left,  (-1, -1))
            self.assertEqual(sqr.bbox.bot_right, (+1, -1))

        for sqr in sqr2:
            self.assertEqual(sqr.bbox.top_left,  (-1, +1))
            self.assertEqual(sqr.bbox.top_right, (+1, +1))
            self.assertEqual(sqr.bbox.bot_left,  (-1, -1))
            self.assertEqual(sqr.bbox.bot_right, (+1, -1))

        for sqr in sqr3:
            self.assertEqual(sqr.bbox.top_left,  (-1, +1))
            self.assertEqual(sqr.bbox.top_right, (+1, +1))
            self.assertEqual(sqr.bbox.bot_left,  (-1, -1))
            self.assertEqual(sqr.bbox.bot_right, (+1, -1))

        for sqr in sqr4:
            self.assertEqual(sqr.bbox.top_left,  (-1, +1))
            self.assertEqual(sqr.bbox.top_right, (+1, +1))
            self.assertEqual(sqr.bbox.bot_left,  (-1, -1))
            self.assertEqual(sqr.bbox.bot_right, (+1, -1))

    def test_exact_orthogonal_rotations_diamondthing(self):
        class Diamondthing(rai.Compo):
            def _make(self):
                self.geoms.update({
                    'root': [
                        [
                            (-1, -1),
                            (+2, -2),
                            (+3, +3),
                            (-4, +4),
                            ]
                        ]
                    })

        sqr0 = (
            Diamondthing(),
            Diamondthing().proxy(),
            )
        # TODO rotate by zero degrees causes empty bbox..?
        #sqr0_2 = Diamondthing().proxy().rotate(_0)
        # TODO print bound point from empty bbox -- error...??

        sqr1 = (
            Diamondthing().proxy().orotate(1),
            sqr0[1].proxy().orotate(1),
            )

        sqr2 = (
            Diamondthing().proxy().orotate(2),
            sqr1[1].proxy().orotate(1),
            )

        sqr3 = (
            Diamondthing().proxy().orotate(3),
            sqr2[1].proxy().orotate(1),
            sqr2[1].proxy().orotate(-5),
            )

        sqr4 = (
            Diamondthing().proxy().orotate(4),
            sqr3[1].proxy().orotate(1),
            Diamondthing().proxy().orotate(-4),
            )


        # Sanity about how floating point works
        self.assertNotEqual(1e-14, 0)
        self.assertNotEqual(1e-20, 0)
        self.assertNotEqual(0.1 * 3, 0.3)
        self.assertEqual(0.125 * 6, 0.75)

        for sqr in sqr0:
            self.assertEqual(sqr.bbox.top_left,  (-4, +4))
            self.assertEqual(sqr.bbox.top_right, (+3, +4))
            self.assertEqual(sqr.bbox.bot_left,  (-4, -2))
            self.assertEqual(sqr.bbox.bot_right, (+3, -2))

        for sqr in sqr1:
            self.assertEqual(sqr.bbox.top_left,  (-4, +3))
            self.assertEqual(sqr.bbox.top_right, (+2, +3))
            self.assertEqual(sqr.bbox.bot_left,  (-4, -4))
            self.assertEqual(sqr.bbox.bot_right, (+2, -4))

        for sqr in sqr2:
            self.assertEqual(sqr.bbox.top_left,  (-3, +2))
            self.assertEqual(sqr.bbox.top_right, (+4, +2))
            self.assertEqual(sqr.bbox.bot_left,  (-3, -4))
            self.assertEqual(sqr.bbox.bot_right, (+4, -4))

        for sqr in sqr3:
            self.assertEqual(sqr.bbox.top_left,  (-2, +4))
            self.assertEqual(sqr.bbox.top_right, (+4, +4))
            self.assertEqual(sqr.bbox.bot_left,  (-2, -3))
            self.assertEqual(sqr.bbox.bot_right, (+4, -3))

        for sqr in sqr4:
            self.assertEqual(sqr.bbox.top_left,  (-4, +4))
            self.assertEqual(sqr.bbox.top_right, (+3, +4))
            self.assertEqual(sqr.bbox.bot_left,  (-4, -2))
            self.assertEqual(sqr.bbox.bot_right, (+3, -2))

