import unittest

import raimad as rai

from .utils import GeomsEqual, ArrayAlmostEqual

class TestFlips(GeomsEqual, ArrayAlmostEqual, unittest.TestCase):
    def test_hflip(self):
        shape = rai.CustomPoly([
            (0, 10),
            (10, 0),
            (-10, 0),
            ])
        hflip = shape.proxy().hflip()

        self.assertGeomsEqual(
            shape.geoms,
            {
                'root': [
                    [
                        (0, 10),
                        (10, 0),
                        (-10, 0),
                        ],
                    ]
                }
            )

        self.assertGeomsEqual(
            hflip.geoms,
            {
                'root': [
                    [
                        (0, 10),
                        (-10, 0),
                        (10, 0),
                        ],
                    ]
                }
            )

    def test_vflip(self):
        shape = rai.CustomPoly([
            (0, 10),
            (10, 0),
            (-10, 0),
            ])
        vflip = shape.proxy().vflip()

        self.assertGeomsEqual(
            shape.geoms,
            {
                'root': [
                    [
                        (0, 10),
                        (10, 0),
                        (-10, 0),
                        ],
                    ]
                }
            )

        self.assertGeomsEqual(
            vflip.geoms,
            {
                'root': [
                    [
                        (0, -10),
                        (10, 0),
                        (-10, 0),
                        ],
                    ]
                }
            )

