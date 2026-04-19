import unittest

import raimad as rai

from .utils import GeomsEqual, ArrayApproxEqual

class TestFlips(GeomsEqual, ArrayApproxEqual, unittest.TestCase):
    """
    Test that vflip and hflip do what you expect.

    This is to isolate issue #2 in which Louis points out that
    in old versions, hflip and vflip seem to be swapped.
    It used to be that vflip flips along vertical axis,
    and hflip flips along horizontal axis.
    The opposite is more intuitive, which is 
    the new bahvior and what this testcase tests for.
    """
    def test_hflip(self):
        shape = rai.CustomPoly([
            (0, 10),
            (10, 0),
            (-10, 0),
            ])
        hflip = shape.proxy().hflip()

        # Also test that transform's method
        hflip_t = shape.proxy()
        hflip_t.transform.hflip()

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

        for shape2 in (hflip, hflip_t):
            self.assertGeomsEqual(
                shape2.geoms,
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

        # Also test that transform's method
        vflip_t = shape.proxy()
        vflip_t.transform.vflip()

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

        for shape2 in (vflip, vflip_t):
            self.assertGeomsEqual(
                shape2.geoms,
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

