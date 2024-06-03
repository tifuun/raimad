import unittest

import raimad as rai
import cift

from .utils import GeomsEqual

class TestCIFNoReuse(GeomsEqual, unittest.TestCase):

    def test_cif_noreuse_rect(self):
        """
        """
        compo = rai.RectLW(10, 20)

        exporter = rai.cif.NoReuse(
            compo,
            multiplier=1,
            )

        parser = cift.Parser()
        parser.parse(exporter.cif_string)

        self.assertGeomsEqual(
            parser.layers,
            {
                'Lroot': [
                    [
                        (-5, -10),
                        (5, -10),
                        (5, 10),
                        (-5, 10),
                        ],
                    ]
                }
            )

    def test_cif_noreuse_proxy(self):
        """
        """
        compo = (
            rai.RectLW(10, 20)
            .proxy()
            .map('mylayer')
            .bbox.bot_left.to((0, 0))
            )

        exporter = rai.cif.NoReuse(
            compo,
            multiplier=1,
            )

        parser = cift.Parser()
        parser.parse(exporter.cif_string)

        self.assertGeomsEqual(
            parser.layers,
            {
                'Lmylayer': [
                    [
                        (0, 0),
                        (10, 0),
                        (10, 20),
                        (0, 20),
                        ],
                    ]
                }
            )


if __name__ == '__main__':
    unittest.main()

