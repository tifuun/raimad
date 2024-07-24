import unittest

import numpy as np

import raimad as rai


class TestPolys(unittest.TestCase):

    def test_angle_between(self):
        self.assertAlmostEqual(
            rai.angle_between((0, 0), (10, 0)),
            np.deg2rad(0))

        self.assertAlmostEqual(
            rai.angle_between((0, 0), (100, 0)),
            np.deg2rad(0))

        self.assertAlmostEqual(
            rai.angle_between((10, 0), (100, 0)),
            np.deg2rad(0))

        self.assertAlmostEqual(
            rai.angle_between((10, 0), (-100, 0)),
            np.deg2rad(180))

        self.assertAlmostEqual(
            rai.angle_between((10, 10), (20, 20)),
            np.deg2rad(45))

    def test_polar(self):
        self.assertIsNone(np.testing.assert_array_almost_equal(
            rai.polar(np.deg2rad(60), 2),
            (1, np.sqrt(3))
            ))

        self.assertIsNone(np.testing.assert_array_almost_equal(
            rai.polar(np.deg2rad(-60), 2),
            (1, -np.sqrt(3))
            ))

        self.assertIsNone(np.testing.assert_array_almost_equal(
            rai.polar(np.deg2rad(180), 100),
            (-100, 0)
            ))

    def test_is_rotated(self):
        self.assertTrue(rai.iters.is_rotated(
            'abc',
            'bca',
            ))

        self.assertFalse(rai.iters.is_rotated(
            'abc',
            'aabc',
            ))

        self.assertFalse(rai.iters.is_rotated(
            'abc',
            'cba',
            ))

        self.assertTrue(rai.iters.is_rotated(
            'abcd',
            'bcda',
            ))

        self.assertTrue(rai.iters.is_rotated(
            [1, 2, 3, 4],
            [3, 4, 1, 2],
            ))

        self.assertTrue(rai.iters.is_rotated(
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

        self.assertFalse(rai.iters.is_rotated(
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

