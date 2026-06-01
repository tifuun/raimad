import unittest
from math import radians, sqrt

import raimad as rai
from raimad import add, eq, sub, midpoint

from .utils import ArrayApproxEqual


class TestPolys(ArrayApproxEqual, unittest.TestCase):

    def test_angle_between(self):
        self.assertApproxEqual(
            rai.angle_between((0, 0), (10, 0)),
            radians(0))

        self.assertApproxEqual(
            rai.angle_between((0, 0), (100, 0)),
            radians(0))

        self.assertApproxEqual(
            rai.angle_between((10, 0), (100, 0)),
            radians(0))

        self.assertApproxEqual(
            rai.angle_between((10, 0), (-100, 0)),
            radians(180))

        self.assertApproxEqual(
            rai.angle_between((10, 10), (20, 20)),
            radians(45))

    def test_polar(self):
        self.assertArrayApproxEqual(
            rai.polar(radians(60), 2),
            (1, sqrt(3))
            )

        self.assertArrayApproxEqual(
            rai.polar(radians(-60), 2),
            (1, -sqrt(3))
            )

        self.assertArrayApproxEqual(
            rai.polar(radians(180), 100),
            (-100, 0)
            )

    def test_is_cycled(self):
        self.assertTrue(rai.iters.is_cycled(
            'abc',
            'bca',
            ))

        self.assertFalse(rai.iters.is_cycled(
            [1, 2],
            [1, 1],
            ))

        self.assertFalse(rai.iters.is_cycled(
            [1, 1],
            [1, 2],
            ))

        self.assertFalse(rai.iters.is_cycled(
            'abc',
            'aabc',
            ))

        self.assertFalse(rai.iters.is_cycled(
            'abc',
            'ab',
            ))

        self.assertFalse(rai.iters.is_cycled(
            'abc',
            'cba',
            ))

        self.assertTrue(rai.iters.is_cycled(
            'abcd',
            'bcda',
            ))

        self.assertTrue(rai.iters.is_cycled(
            [1, 2, 3, 4],
            [3, 4, 1, 2],
            ))

        self.assertTrue(rai.iters.is_cycled(
            [
                (1, 2),
                (3, 4),
                (5, 6),
                (7, 8),
                ],
            [
                (5, 6),
                (7, 8),
                (1, 2),
                (3, 4),
                ],
            ))

        self.assertFalse(rai.iters.is_cycled(
            [
                (1, 2),
                (3, 4),
                (5, 6),
                (7, 8),
                ],
            [
                (1, 2),
                (3, 4),
                (7, 8),
                (5, 6),
                ],
            ))

    def test_reversed(self):
        self.assertEqual(rai.reversed(''), '')
        self.assertEqual(rai.reversed('a'), 'a')
        self.assertEqual(rai.reversed('abcd'), 'dcba')
        self.assertEqual(rai.reversed([]), [])
        self.assertEqual(rai.reversed(['a']), ['a'])
        self.assertEqual(
            rai.reversed(['a', 'b', 'c', 'd']),
            ['d', 'c', 'b', 'a'],
            )
 
    def test_reversed_pin(self):
        self.assertEqual(rai.reversed_pin('a'), 'a')
        self.assertEqual(rai.reversed_pin('abcd'), 'adcb')
        self.assertEqual(rai.reversed_pin('abcd',  0), 'adcb')
        self.assertEqual(rai.reversed_pin('abcd',  1), 'cbad')
        self.assertEqual(rai.reversed_pin('abcd',  2), 'adcb')
        self.assertEqual(rai.reversed_pin('abcd',  3), 'cbad')
        self.assertEqual(rai.reversed_pin('abcd', -4), 'adcb')
        self.assertEqual(rai.reversed_pin('abcd', -1), 'cbad')
        self.assertEqual(rai.reversed_pin('abcd', -2), 'adcb')
        self.assertEqual(rai.reversed_pin('abcd', -1), 'cbad')

        with self.assertRaises(IndexError):
            rai.reversed_pin('')
            rai.reversed_pin([])
        with self.assertRaises(IndexError):
            rai.reversed_pin('abcd', 4)
        with self.assertRaises(IndexError):
            rai.reversed_pin('abcd', 5)
        with self.assertRaises(IndexError):
            rai.reversed_pin('abcd', -5)

        self.assertEqual(rai.reversed_pin(['a']), ['a'])
        self.assertEqual(
            rai.reversed_pin(['a', 'b', 'c', 'd']),
            ['a', 'd', 'c', 'b'],
            )

    def test_cycled(self):
        self.assertEqual(rai.cycled('', -8), '')
        self.assertEqual(rai.cycled('a', -8), 'a')
        self.assertEqual(rai.cycled([], -8), [])
        self.assertEqual(rai.cycled(['a'], -8), ['a'])

        self.assertEqual(rai.cycled('abcd', -8), 'abcd')
        self.assertEqual(rai.cycled('abcd', -7), 'dabc')
        self.assertEqual(rai.cycled('abcd', -6), 'cdab')
        self.assertEqual(rai.cycled('abcd', -5), 'bcda')
        self.assertEqual(rai.cycled('abcd', -4), 'abcd')
        self.assertEqual(rai.cycled('abcd', -3), 'dabc')
        self.assertEqual(rai.cycled('abcd', -2), 'cdab')
        self.assertEqual(rai.cycled('abcd', -1), 'bcda')
        self.assertEqual(rai.cycled('abcd',  0), 'abcd')
        self.assertEqual(rai.cycled('abcd',  1), 'dabc')
        self.assertEqual(rai.cycled('abcd',  2), 'cdab')
        self.assertEqual(rai.cycled('abcd',  3), 'bcda')
        self.assertEqual(rai.cycled('abcd',  4), 'abcd')
        self.assertEqual(rai.cycled('abcd',  5), 'dabc')
        self.assertEqual(rai.cycled('abcd',  6), 'cdab')
        self.assertEqual(rai.cycled('abcd',  7), 'bcda')
        self.assertEqual(rai.cycled('abcd',  8), 'abcd')

        self.assertEqual(rai.cycled(list('abcd'), -8), list('abcd'))
        self.assertEqual(rai.cycled(list('abcd'), -7), list('dabc'))
        self.assertEqual(rai.cycled(list('abcd'), -6), list('cdab'))
        self.assertEqual(rai.cycled(list('abcd'), -5), list('bcda'))
        self.assertEqual(rai.cycled(list('abcd'), -4), list('abcd'))
        self.assertEqual(rai.cycled(list('abcd'), -3), list('dabc'))
        self.assertEqual(rai.cycled(list('abcd'), -2), list('cdab'))
        self.assertEqual(rai.cycled(list('abcd'), -1), list('bcda'))
        self.assertEqual(rai.cycled(list('abcd'),  0), list('abcd'))
        self.assertEqual(rai.cycled(list('abcd'),  1), list('dabc'))
        self.assertEqual(rai.cycled(list('abcd'),  2), list('cdab'))
        self.assertEqual(rai.cycled(list('abcd'),  3), list('bcda'))
        self.assertEqual(rai.cycled(list('abcd'),  4), list('abcd'))
        self.assertEqual(rai.cycled(list('abcd'),  5), list('dabc'))
        self.assertEqual(rai.cycled(list('abcd'),  6), list('cdab'))
        self.assertEqual(rai.cycled(list('abcd'),  7), list('bcda'))
        self.assertEqual(rai.cycled(list('abcd'),  8), list('abcd'))

    def test_flatten(self):
        self.assertEqual(
            rai.flatten([[[1, 2], 3, [4], [5, 6], 7], 8]),
            [1, 2, 3, 4, 5, 6, 7, 8]
            )

        self.assertEqual(
            rai.flatten([1, 2, 3, 4, 5, 6, 7, 8]),
            [1, 2, 3, 4, 5, 6, 7, 8]
            )

        self.assertEqual(
            rai.flatten([[['a', 'bcd'], 'e', ['f'], ['g', 'h'], 'ij'], 'klm']),
            ['a', 'bcd', 'e', 'f', 'g', 'h', 'ij', 'klm']
            )

        self.assertEqual(
            rai.flatten('string'),
            ['string'],
            )

        self.assertEqual(
            rai.flatten(10),
            [10],
            )

    def test_add_eq(self):
        self.assertTrue(
            rai.eq(
                rai.add(
                    (10, 12),
                    (13, 14),
                    ),
                (23, 26)
                )
            )

    def test_add_eq_infix(self):
        self.assertTrue(
            (23, 26) |eq| ( (10, 12) |add| (13, 14) )
            )

    def test_sub_eq(self):
        self.assertTrue(
            rai.eq(
                rai.sub(
                    (10, 12),
                    (13, 14),
                    ),
                (-3, -2)
                )
            )

    def test_sub_infix(self):
        self.assertTrue(
            (-3, -2) |eq| ( (10, 12) |sub| (13, 14) )
            )

    def test_midpoint(self):
        self.assertTrue(
            rai.eq(
                rai.midpoint((10, 20), (20, 40)),
                (15, 30)
                )
            )

    def test_midpoint_infix(self):
        self.assertTrue(
            rai.eq(
                (10, 20) |midpoint| (20, 40),
                (15, 30)
                )
            )

    def distance_between(self):
        self.assertEqual(
            rai.distance_between((10, 9), (7, 5)),
            5
            )


    #def test_force_evaluate(self):
    #    # We define it here as a factory, because
    #    # the various checks, etc.
    #    # alter the state of a generator
    #    def generator_of_maps():
    #        return (
    #            map(lambda x: x ** 2, range(x))
    #            for x in range(5)
    #            )

    #    self.assertTrue(isinstance(generator_of_maps(), types.GeneratorType))
    #    self.assertTrue(isinstance(
    #        next(generator_of_maps()),
    #        map
    #        ))

    #    evaluated_as_lists = rai.force_evaluate(generator_of_maps(), list)
    #    evaluated_as_tuples = rai.force_evaluate(generator_of_maps(), tuple)

    #    self.assertEqual(
    #        evaluated_as_lists,
    #        [
    #            [0, ],
    #            [0, 1, ],
    #            [0, 1, 2, ],
    #            [0, 1, 4, 9,],
    #            [0, 1, 4, 9, 16, ],
    #            ]
    #        )

    #    self.assertEqual(
    #        evaluated_as_tuples,
    #        (
    #            (0, ),
    #            (0, 1, ),
    #            (0, 1, 2, ),
    #            (0, 1, 4, 9,),
    #            (0, 1, 4, 9, 16, ),
    #            )
    #        )


if __name__ == '__main__':
    unittest.main()

