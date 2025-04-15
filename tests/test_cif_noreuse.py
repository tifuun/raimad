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

        compo = Third()

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
                        (-5, -5),
                        (5, -5),
                        (5, 5),
                        (-5, 5),
                        ],
                    [
                        (5, -5),
                        (15, -5),
                        (15, 5),
                        (5, 5),
                        ],
                    ]
                }
            )

    def test_layers_discard(self):
        """
        Test that LMAPping a layer to None actually discards it.
        (bug 2025-04-14)
        """

        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.extend((
                    rai.RectLW(10, 10).proxy().map('foo'),
                    rai.RectLW(20, 20).proxy().map('bar'),
                ))

        compo = MyCompo()

        p0 = compo.proxy()
        p1 = compo.proxy().map({'foo': None, 'bar': 'bar'})
        p2 = compo.proxy().map({'foo': 'foo', 'bar': None})
        p3 = compo.proxy().map({'foo': None, 'bar': None})
        p4 = compo.proxy().map({'foo': None, 'bar': 'ayy'})
        p5 = compo.proxy().map({'foo': 'ayy', 'bar': None})
        p6 = compo.proxy().map({'foo': 'ayy', 'bar': 'lmao'})

        def layers(compo):
            exporter = rai.cif.NoReuse(
                compo,
                multiplier=1,
                )

            parser = cift.Parser()
            parser.parse(exporter.cif_string)
            return parser.layers

        self.assertEqual(layers(p0).keys(), {'Lfoo', 'Lbar'})
        self.assertEqual(layers(p1).keys(), {'Lbar'})
        self.assertEqual(layers(p2).keys(), {'Lfoo'})
        self.assertEqual(layers(p3).keys(), set())
        self.assertEqual(layers(p4).keys(), {'Layy'})
        self.assertEqual(layers(p5).keys(), {'Layy'})
        self.assertEqual(layers(p6).keys(), {'Layy', 'Llmao'})

        self.assertGeomsEqualButAllowDifferentNames(layers(p0), layers(p6))
        self.assertGeomsEqualButAllowDifferentNames(layers(p1), layers(p4))
        self.assertGeomsEqualButAllowDifferentNames(layers(p2), layers(p5))
        self.assertEqual(len(layers(p3)), 0)

if __name__ == '__main__':
    unittest.main()

