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

    def test_cif_2024_09_09(self):
        """Test that a bug that we found on 2024-09-09 doesn't occur."""
        class First(rai.Compo):
            def _make(self):
                self.subcompos.a = (rai.RectLW(10, 10).proxy())

        class Second(rai.Compo):
            def _make(self):
                self.subcompos.a = (
                    First()
                    .proxy()
                    .bbox.mid.to((0, 0))
                    )
                self.subcompos.b = (
                    self.subcompos.a
                    .proxy()
                    .snap_right(self.subcompos.a)
                    )

        class Third(rai.Compo):
            def _make(self):
                self.subcompos.a = (Second().proxy())

        exporter = rai.cif.NoReuse(
            Third(),
            multiplier=1,
            )

        parser = cift.Parser()
        parser.parse(exporter.cif_string)

        self.assertGeomsEqual(
            parser.layers,
            {
                'Lroot': [
                    [
                        (-5, -5),
                        (5, -5),
                        (5, 5),
                        (-5, 5),
                        ],
                    [
                        (-5 + 5, -5),
                        (5 + 5, -5),
                        (5 + 5, 5),
                        (-5 + 5, 5),
                        ],
                    ]
                }
            )


if __name__ == '__main__':
    unittest.main()

