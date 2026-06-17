import unittest

import raimad as rai
import cift as cf

from .utils import GeomsEqual


def micron2cif_floor(micron: float, multiplier: float = 100) -> int:
    """
    Convert microns to cif units with floor rounding.
    """
    return int(micron * multiplier)

class MyCompo(rai.Compo):
    def _make(self, foo: float = 0.6) -> None:
        self.subcompos.foo = (
            rai.RectLW(foo * 2, foo * 2).proxy()
            .bbox.mid.to(2, 4)
        )

        self.subcompos.bar = (
            rai.RectLW(foo * 4, foo * 4).proxy()
            .bbox.bot_mid.to(
                self.subcompos.foo.bbox.mid[0] / 2,
                self.subcompos.foo.bbox.mid[1] / 2
                )
            )

expected: rai.types.Geoms = {
    'ROOT': [
        [(140, 340), (260, 340), (260, 460), (140, 460)],
        [(-20, 200), (220, 200), (220, 440), (-20, 440)],
        ]
    }


class TestCIFNoReuse(GeomsEqual, unittest.TestCase):
    def test_cif_rounding_isolate(self):
        """
        Test that using floor rounding for CIF export indeed causes issues.

        Floor rounding is NOT what cif export currently uses.
        Because it causes issues.
        But this test is here to confirm that it indeed does
        cause issues,
        if you do use it.

        More info: https://github.com/tifuun/raimad/issues/11
        """

        compo = MyCompo()
        exporter = rai.cif.NoReuse(compo, _unit_conv_fn=micron2cif_floor)
        geoms_parsed = cf.parse(exporter.cif_string)
        # TODO once `geom` from cifreuse is merged also compare
        # with internal representation
        #geoms_internal_multiplied = cf.parse(exporter.cif_string)
        #self.assertGeomsNotEqual(geoms, expected)

        # TODO assertGeomsNotEqual method
        with self.assertRaises(AssertionError):
            self.assertGeomsEqual(geoms_parsed, expected)

        # These are the polygons it actually generates:
        # P 140 340 260 340 260 459 140 459 ;
        # P -19 200 220 200 220 440 -19 440 ;
        #
        # Note the off-by-one errors:
        # 459 instead of 460 and -19 instead of -20

    def test_cif_rounding_fix(self):
        """
        Test that using default rounding method for CIF export works.

        More info: https://github.com/tifuun/raimad/issues/11
        """

        compo = MyCompo()
        exporter = rai.cif.NoReuse(compo)
        geoms_parsed = cf.parse(exporter.cif_string)
        # TODO once `geom` from cifreuse is merged also compare
        # with internal representation
        #geoms_internal_multiplied = cf.parse(exporter.cif_string)
        #self.assertGeomsNotEqual(geoms, expected)

        self.assertGeomsEqual(geoms_parsed, expected)


