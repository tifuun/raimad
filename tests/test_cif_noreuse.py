import unittest

import raimad as rai
import cift as cf

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

        layers = cf.parse(
            exporter.cif_string,
            )

        self.assertGeomsEqual(
            layers,
            {
                'ROOT': [
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
            .map('LAYR')
            .bbox.bot_left.to((0, 0))
            )

        exporter = rai.cif.NoReuse(
            compo,
            multiplier=1,
            )

        layers = cf.parse(
            exporter.cif_string,
            )

        self.assertGeomsEqual(
            layers,
            {
                'LAYR': [
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

        exporter = rai.cif.NoReuse(compo, multiplier=1)

        layers = cf.parse(exporter.cif_string)

        self.assertGeomsEqual(
            layers,
            {
                'ROOT': [
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
                    rai.RectLW(10, 10).proxy().map('FOO'),
                    rai.RectLW(20, 20).proxy().map('BAR'),
                ))

        compo = MyCompo()

        p0 = compo.proxy()
        p1 = compo.proxy().map({'FOO': None, 'BAR': 'BAR'})
        p2 = compo.proxy().map({'FOO': 'FOO', 'BAR': None})
        p3 = compo.proxy().map({'FOO': None, 'BAR': None})
        p4 = compo.proxy().map({'FOO': None, 'BAR': 'AYY'})
        p5 = compo.proxy().map({'FOO': 'AYY', 'BAR': None})
        p6 = compo.proxy().map({'FOO': 'AYY', 'BAR': 'LMAO'})

        def layers(compo: 'rai.typing.CompoLike') -> :
            exporter = rai.cif.NoReuse(
                compo,
                multiplier=1,
                )

            layers = cf.parse(
                exporter.cif_string,
                )
            return layers

        self.assertEqual(layers(p0).keys(), {'FOO', 'BAR'})
        self.assertEqual(layers(p1).keys(), {'BAR'})
        self.assertEqual(layers(p2).keys(), {'FOO'})
        self.assertEqual(layers(p3).keys(), set())
        self.assertEqual(layers(p4).keys(), {'AYY'})
        self.assertEqual(layers(p5).keys(), {'AYY'})
        self.assertEqual(layers(p6).keys(), {'AYY', 'LMAO'})

        self.assertGeomsEqualButAllowDifferentNames(layers(p0), layers(p6))
        self.assertGeomsEqualButAllowDifferentNames(layers(p1), layers(p4))
        self.assertGeomsEqualButAllowDifferentNames(layers(p2), layers(p5))
        self.assertEqual(len(layers(p3)), 0)

if __name__ == '__main__':
    unittest.main()

