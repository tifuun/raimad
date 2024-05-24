import unittest
from .utils import GeomsEqual

import raimad as rai


class TestGeomsEqualMixin(GeomsEqual, unittest.TestCase):
    """
    Test whether the `GeomsEqual` TestCase mixin
    works properly.
    Yes, even our unit tests have unit tests!
    """

    def test_geoms_equal_mixin_trivial(self):
        self.assertGeomsEqual(
            {
                'root': [
                    [
                        (0, 0),
                        (0, 1),
                        (1, 0),
                        ],
                    ],
                },
            {
                'root': [
                    [
                        (0, 0),
                        (0, 1),
                        (1, 0),
                        ],
                    ],
                },
            )

    def test_geoms_equal_mixin_poly_order(self):
        self.assertGeomsEqual(
            {
                'root': [
                    [
                        (0, 0),
                        (0, 1),
                        (1, 0),
                        ],
                    [
                        (0, 0),
                        (0, 2),
                        (2, 0),
                        ],
                    ],
                },
            {
                'root': [
                    [
                        (0, 0),
                        (0, 2),
                        (2, 0),
                        ],
                    [
                        (0, 0),
                        (0, 1),
                        (1, 0),
                        ],
                    ],
                },
            )

    def test_geoms_equal_point_order(self):
        self.assertGeomsEqual(
            {
                'root': [
                    [
                        (1, 0),
                        (0, 0),
                        (0, 1),
                        ],
                    ],
                },
            {
                'root': [
                    [
                        (0, 0),
                        (0, 1),
                        (1, 0),
                        ],
                    ],
                },
            )

    def test_geoms_equal_poly_order(self):
        self.assertGeomsEqual(
            {
                'root': [
                    [
                        (1, 0),
                        (0, 0),
                        (0, 1),
                        ],
                    [
                        (2, 0),
                        (0, 0),
                        (0, 2),
                        ],
                    [
                        (3, 0),
                        (0, 0),
                        (0, 3),
                        ],
                    ],
                },
            {
                'root': [
                    [
                        (1, 0),
                        (0, 0),
                        (0, 1),
                        ],
                    [
                        (3, 0),
                        (0, 0),
                        (0, 3),
                        ],
                    [
                        (2, 0),
                        (0, 0),
                        (0, 2),
                        ],
                    ],
                },
            )

    def test_geoms_equal_mixin_layer_order(self):
        self.assertGeomsEqual(
            {
                'root': [
                    [
                        (0, 0),
                        (0, 1),
                        (1, 0),
                        ],
                    ],
                'aux': [
                    [
                        (0, 0),
                        (0, 2),
                        (2, 0),
                        ],
                    ],
                'sec': [
                    [
                        (0, 0),
                        (0, 3),
                        (3, 0),
                        ],
                    ],
                },
            {
                'aux': [
                    [
                        (0, 0),
                        (0, 2),
                        (2, 0),
                        ],
                    ],
                'root': [
                    [
                        (0, 0),
                        (0, 1),
                        (1, 0),
                        ],
                    ],
                'sec': [
                    [
                        (0, 0),
                        (0, 3),
                        (3, 0),
                        ],
                    ],
                },
            )

    def test_geoms_equal_mixin_complex(self):
        self.assertGeomsEqual(
            {
                'root': [
                    [
                        (0, 0),
                        (0, 1),
                        (1, 0),
                        ],
                    [
                        (0, 0),
                        (3, 0),
                        (3, 3),
                        (0, 3),
                        ],
                    [
                        (0, 0),
                        (4, 0),
                        (4, 4),
                        (0, 4),
                        ],
                    ],
                'aux': [
                    [
                        (2, 0),
                        (0, 0),
                        (0, 2),
                        ],
                    ],
                },
            {
                'aux': [
                    [
                        (0, 0),
                        (0, 2),
                        (2, 0),
                        ],
                    ],
                'root': [
                    [
                        (3, 3),
                        (0, 3),
                        (0, 0),
                        (3, 0),
                        ],
                    [
                        (0, 1),
                        (1, 0),
                        (0, 0),
                        ],
                    [
                        (0, 0),
                        (4, 0),
                        (4, 4),
                        (0, 4),
                        ],
                    ],
                },
            )

    def test_geoms_unequal_mixin_point_order(self):
        with self.assertRaises(AssertionError):
            self.assertGeomsEqual(
                {
                    'root': [
                        [
                            (0, 0),
                            (0, 1),
                            (1, 0),
                            ],
                        ],
                    },
                {
                    'root': [
                        [
                            (0, 0),
                            (1, 0),
                            (0, 1),
                            ],
                        ],
                    },
                )


if __name__ == '__main__':
    unittest.main()

