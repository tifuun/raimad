import unittest

import raimad as rai
import cift as cf

from .utils import GeomsEqual


class Bridge(rai.Compo):
    def _make(self, do_maps: bool):
        foo = rai.RectLW(30, 10).proxy()
        bar = rai.RectLW(40, 5).proxy()
        bar.bbox.mid.to(foo.bbox.mid)

        if do_maps:
            foo.map('FOO')
            bar.map('BAR')

        self.subcompos.foo = foo
        self.subcompos.bar = bar

class TLine(rai.Compo):
    def _make(self, do_maps: bool):
        foo = rai.RectLW(4000, 10).proxy()
        bar = rai.RectLW(4000, 8).proxy()
        baz = rai.RectLW(4000, 8).proxy()
        ayy = rai.RectLW(4000, 26).proxy()
        bar.snap_above(foo).movey(5)
        baz.snap_below(foo).movey(-5)
        ayy.bbox.mid.to(foo.bbox.mid)

        if do_maps:
            foo.map('CND')
            bar.map('CND')
            baz.map('CND')
            ayy.map('MAS')

        self.subcompos.foo = foo
        self.subcompos.bar = bar
        self.subcompos.baz = baz
        self.subcompos.ayy = ayy

class TLineCompo(rai.Compo):
    def _make(self, do_maps: bool, num_bridges: int = 50):
        line = TLine(do_maps=do_maps).proxy()
        bridge = Bridge(do_maps=do_maps).proxy().rotate(rai.quartercircle)

        for x in range(0, num_bridges):
            bridgep = bridge.proxy()
            bridgep.bbox.mid.to(
                line.bbox.interpolate((x + 0.5) / num_bridges, 0.5)
                )
            self.subcompos[f"bridge_{x}"] = bridgep

        self.subcompos.line = line


class TestCIFReuse(GeomsEqual, unittest.TestCase):

    def test_cif_reuse_rect(self):
        """
        """
        compo = rai.RectLW(10, 20)

        exporter = rai.cif.Reuse(
            compo,
            multiplier=1,
            )

        layers = cf.parse(
            exporter.cif_string,
            grammar=cf.grammar.lenient_layers
            )

        self.assertGeomsEqual(
            layers,
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

    def test_cif_reuse_proxy(self):
        """
        """
        compo = (
            rai.RectLW(10, 20)
            .proxy()
            .map('mylayer')
            .bbox.bot_left.to((0, 0))
            )

        exporter = rai.cif.Reuse(
            compo,
            multiplier=1,
            )

        layers = cf.parse(
            exporter.cif_string,
            grammar=cf.grammar.lenient_layers
            )

        self.assertGeomsEqual(
            layers,
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

    def test_cif_reuse_ciffable_proxy(self):
        """
        Test that reuse parser detects that a proxy can be
        converted to a cif symbol call and actually does that
        instead of steamrolling it
        """
        compo = (
            rai.RectLW(10, 20)
            .proxy()
            .bbox.bot_left.to((0, 0))
            )

        exporter = rai.cif.Reuse(
            compo,
            multiplier=1,
            )

        layers = cf.parse(
            exporter.cif_string,
            grammar=cf.grammar.lenient_layers
            )

        self.assertEqual(exporter.stat.steamrolls, 0)

        self.assertGeomsEqual(
            layers,
            {
                'Lroot': [
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

        exporter = rai.cif.Reuse(
            compo,
            multiplier=1,
            )

        layers = cf.parse(
            exporter.cif_string,
            grammar=cf.grammar.lenient_layers
            )

        self.assertGeomsEqual(
            layers,
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
            exporter = rai.cif.Reuse(
                compo,
                multiplier=1,
                )

            layers = cf.parse(
                exporter.cif_string,
                grammar=cf.grammar.lenient_layers
                )
            return layers

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

    def test_cif_reuse_bridges(self):
        """
        test case: a transmission line with some bridges.
        Bridges should be reused.
        """

        compo = TLineCompo(do_maps=False)

        exporter = rai.cif.Reuse(
            compo,
            multiplier=1,
            )

        from pathlib import Path
        Path('test.cif').write_text(exporter.cif_string)
        Path('test.gv').write_text(exporter.stat.call_graph_dot())

        #layers = cf.parse(
        #    exporter.cif_string,
        #    grammar=cf.grammar.lenient_layers
        #    )

        self.assertEqual(exporter.stat.steamrolls, 0)


    def test_cif_reuse_maps_bridges(self):
        """
        test case: a transmission line with some bridges.
        Bridges should be reused.
        """

        compo = TLineCompo(do_maps=True)

        exporter = rai.cif.Reuse(
            compo,
            multiplier=1,
            )

        #layers = cf.parse(
        #    exporter.cif_string,
        #    grammar=cf.grammar.lenient_layers
        #    )

        self.assertEqual(exporter.stat.steamrolls, 0)

                
    def test_cif_reuse_proxyorder(self):
        class One(rai.Compo):
            def _make(self):
                self.subcompos.foo = (
                    rai.RectLW(20, 10).proxy().bbox.mid.to((0,0))
                    )
                
        class Two(rai.Compo):
            def _make(self):
                self.subcompos.foo = One().proxy().rotate(rai.eigthcircle)
                
        class Three(rai.Compo):
            def _make(self):
                self.subcompos.foo = Two().proxy().rotate(rai.eigthcircle)
                
        class Four(rai.Compo):
            def _make(self):
                self.subcompos.foo = Three().proxy().rotate(rai.eigthcircle)
                
        class Five(rai.Compo):
            def _make(self):
                self.subcompos.foo = Four().proxy().rotate(rai.eigthcircle)
                
        class Six(rai.Compo):
            def _make(self):
                self.subcompos.foo = Five().proxy().rotate(rai.eigthcircle)
                
        class Seven(rai.Compo):
            def _make(self):
                self.subcompos.foo = Six().proxy().rotate(rai.eigthcircle)

        #for f in [One, Two, Three, Four, Five, Six, Seven]:
        #    c = f()
        #    rai.export_cif(c, f"{f.__name__}.cif", rai.cif.Reuse, multiplier=1)
                
        compo = Seven()
        exporter = rai.cif.Reuse(compo, multiplier=1)
        layers = cf.parse(
            exporter.cif_string,
            grammar=cf.grammar.lenient_layers
            )

        self.assertGeomsEqual(
            layers,
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

if __name__ == '__main__':
    unittest.main()

