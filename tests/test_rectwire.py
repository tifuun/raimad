import unittest

import raimad as rai

from .utils import GeomsEqual, ArrayAlmostEqual

class TestPolys(GeomsEqual, ArrayAlmostEqual, unittest.TestCase):

    def test_rectwire_p2p(self):
        rectwire = rai.RectWire.from_points((0, 0), (0, 20), 10)
        self.assertGeomsEqual(
            rectwire.geoms,
            {
                'root': [
                    [
                        [-5, 0],
                        [5, 0],
                        [5, 20],
                        [-5, 20]
                        ],
                    ]
                }
            )

    def test_rectwire_shortsyntax(self):
        rectwire = rai.RectWire((0, 0), (0, 20), 10)
        self.assertGeomsEqual(
            rectwire.geoms,
            {
                'root': [
                    [
                        [-5, 0],
                        [5, 0],
                        [5, 20],
                        [-5, 20]
                        ],
                    ]
                }
            )

    def test_rectwire_polar(self):
        rectwire = rai.RectWire.from_polar(
            (0, 0),
            angle=rai.quartercircle,
            length=20,
            width=10,
            )
        self.assertGeomsEqual(
            rectwire.geoms,
            {
                'root': [
                    [
                        [-5, 0],
                        [5, 0],
                        [5, 20],
                        [-5, 20]
                        ],
                    ]
                }
            )


if __name__ == '__main__':
    unittest.main()

