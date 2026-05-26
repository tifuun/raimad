import unittest

import raimad as rai
import cift as cf

import math


if 0:
    _pi = rai.symbolic.PieceOfPi()
    _quartercircle = _pi * 1 / 2
    _semicircle = _pi
    _fullcircle = _pi * 2
    _0 = 0
    _2 = 2
    _3 = 3
else:
    _pi = math.pi
    _quartercircle = rai.quartercircle
    _semicircle = rai.semicircle
    _fullcircle = rai.fullcircle
    _0 = 0
    _2 = 2
    _3 = 3

class TestExactCardinalRotations(unittest.TestCase):
    def test_exact_cardinal_rotations_square(self):
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

        sqr0_0 = Square()
        sqr0_1 = Square().proxy()
        # TODO rotate by zero degrees causes empty bbox..?
        #sqr0_2 = Square().proxy().rotate(_0)
        # TODO print bound point from empty bbox -- error...??

        sqr1_0 = Square().proxy().rotate(_quartercircle)
        sqr1_1 = sqr0_1.proxy().rotate(_quartercircle)
        sqr1_2 = Square().proxy().rotate(_pi / _2)

        sqr2_0 = Square().proxy().rotate(_semicircle)
        sqr2_1 = sqr1_1.proxy().rotate(_quartercircle)
        sqr2_2 = Square().proxy().rotate(_pi)

        sqr3_0 = Square().proxy().rotate(_3 * _quartercircle)
        sqr3_1 = sqr2_1.proxy().rotate(_quartercircle)
        sqr3_2 = Square().proxy().rotate(_pi * _3 / _2)

        sqr4_0 = Square().proxy().rotate(_fullcircle)
        sqr4_1 = sqr3_1.proxy().rotate(_quartercircle)
        sqr4_2 = Square().proxy().rotate(_pi * _2)

        # Sanity about how floating point works
        self.assertNotEqual(1e-14, 0)
        self.assertNotEqual(1e-20, 0)
        self.assertNotEqual(0.1 * 3, 0.3)
        self.assertEqual(0.125 * 6, 0.75)

        for sqr0 in (sqr0_0, sqr0_1): #, sqr0_2):
            self.assertEqual(sqr0.bbox.top_left,  (-1, +1))
            self.assertEqual(sqr0.bbox.top_right, (+1, +1))
            self.assertEqual(sqr0.bbox.bot_left,  (-1, -1))
            self.assertEqual(sqr0.bbox.bot_right, (+1, -1))

        for sqr1 in (sqr1_0, sqr1_1, sqr1_2):
            self.assertEqual(sqr1.bbox.top_left,  (-1, +1))
            self.assertEqual(sqr1.bbox.top_right, (+1, +1))
            self.assertEqual(sqr1.bbox.bot_left,  (-1, -1))
            self.assertEqual(sqr1.bbox.bot_right, (+1, -1))

        for sqr2 in (sqr2_0, sqr2_1, sqr2_2):
            self.assertEqual(sqr2.bbox.top_left,  (-1, +1))
            self.assertEqual(sqr2.bbox.top_right, (+1, +1))
            self.assertEqual(sqr2.bbox.bot_left,  (-1, -1))
            self.assertEqual(sqr2.bbox.bot_right, (+1, -1))

        for sqr3 in (sqr3_0, sqr3_1, sqr3_2):
            self.assertEqual(sqr3.bbox.top_left,  (-1, +1))
            self.assertEqual(sqr3.bbox.top_right, (+1, +1))
            self.assertEqual(sqr3.bbox.bot_left,  (-1, -1))
            self.assertEqual(sqr3.bbox.bot_right, (+1, -1))

    def test_exact_cardinal_rotations_diamondthing(self):
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

        sqr0_0 = Diamondthing()
        sqr0_1 = Diamondthing().proxy()
        #sqr0_2 = Diamondthing().proxy().rotate(_0)

        sqr1_0 = Diamondthing().proxy().rotate(_quartercircle)
        sqr1_1 = sqr0_1.proxy().rotate(_quartercircle)
        sqr1_2 = Diamondthing().proxy().rotate(_pi / _2)

        sqr2_0 = Diamondthing().proxy().rotate(_semicircle)
        sqr2_1 = sqr1_1.proxy().rotate(_quartercircle)
        sqr2_2 = Diamondthing().proxy().rotate(_pi)

        sqr3_0 = Diamondthing().proxy().rotate(_3 * _quartercircle)
        sqr3_1 = sqr2_1.proxy().rotate(_quartercircle)
        sqr3_2 = Diamondthing().proxy().rotate(_pi * _3 / _2)

        sqr4_0 = Diamondthing().proxy().rotate(_fullcircle)
        sqr4_1 = sqr3_1.proxy().rotate(_quartercircle)
        sqr4_2 = Diamondthing().proxy().rotate(_pi * _2)

        # Sanity about how floating point works
        self.assertNotEqual(1e-14, 0)
        self.assertNotEqual(1e-20, 0)
        self.assertNotEqual(0.1 * 3, 0.3)
        self.assertEqual(0.125 * 6, 0.75)

        for sqr0 in (sqr0_0, sqr0_1): #, sqr0_2):
            self.assertEqual(sqr0.bbox.top_left,  (-4, +4))
            self.assertEqual(sqr0.bbox.top_right, (+3, +4))
            self.assertEqual(sqr0.bbox.bot_left,  (-4, -2))
            self.assertEqual(sqr0.bbox.bot_right, (+3, -2))

        for sqr1 in (sqr1_0, sqr1_1, sqr1_2):
            self.assertEqual(sqr1.bbox.top_left,  (-4, +3))
            self.assertEqual(sqr1.bbox.top_right, (+2, +3))
            self.assertEqual(sqr1.bbox.bot_left,  (-4, -4))
            self.assertEqual(sqr1.bbox.bot_right, (+2, -4))

        for sqr2 in (sqr2_0, sqr2_1, sqr2_2):
            self.assertEqual(sqr2.bbox.top_left,  (-3, +2))
            self.assertEqual(sqr2.bbox.top_right, (+4, +2))
            self.assertEqual(sqr2.bbox.bot_left,  (-3, -4))
            self.assertEqual(sqr2.bbox.bot_right, (+4, -4))

        for sqr3 in (sqr3_0, sqr3_1, sqr3_2):
            self.assertEqual(sqr3.bbox.top_left,  (-2, +4))
            self.assertEqual(sqr3.bbox.top_right, (+4, +4))
            self.assertEqual(sqr3.bbox.bot_left,  (-2, -3))
            self.assertEqual(sqr3.bbox.bot_right, (+4, -3))


