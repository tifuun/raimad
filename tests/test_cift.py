"""
Tests for raimad 1.0.0 cif exporter.
As opposed to `test_cif_100`,
these tests use CIFT to verify the generated CIF files.
"""

from pprint import pprint
from sys import stderr
import unittest

import cift as cf
import numpy as np

import raimad as rai

from .utils import PrettyEqual

class CIFTRoutGraphChecker():
    """
    """
    def assertCIFTRoutStructure(self, exporter, parser, expected_edges):
        compos_expected = set(rai.flatten(expected_edges)) - {-1}
        compos_actual = set(exporter.compo2rout.keys())
        if compos_expected > compos_actual:
            raise AssertionError(
                f"Could not find these compos: "
                f"{compos_expected - compos_actual}"
                )

        expected_as_routs = {
            tuple(
                (
                    -1 if proxy == -1 else
                    exporter.compo2rout[proxy]
                    )
                for proxy in edge)
            for edge in expected_edges
            }

        try:
            self.assertEqual(
                expected_as_routs,
                set(parser.edges)
                )

        except AssertionError as err:
            print("ACTUAL STRUCTURE: ", file=stderr)
            pprint(parser.edges, stream=stderr)
            print("DESIRED STRUCTURE: ", file=stderr)
            pprint(expected_as_routs, stream=stderr)
            raise err


class TestCIFT(unittest.TestCase, PrettyEqual, CIFTRoutGraphChecker):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_cif_layer_simple(self):
        """
        """
        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.rec = (
                    rai.RectWH(10, 20).proxy()
                    .map('mylayer')
                    .bbox.bot_left.to((0, 0))
                    )

        compo = MyCompo()
        exporter = rai.CIFExporter(
            compo,
            multiplier=1,
            rot_multiplier=1,
            cif_native=False,
            flatten_proxies=False,
            native_inline=False,
            transform_fatal=False
            )
        cif_string = exporter.cif_string
        parser = cf.Parser()
        parser.parse(cif_string)
        self.assertPrettyEqual(
            parser.layers,
            {
                'Lmylayer': [
                    (
                        (0, 0),
                        (10, 0),
                        (10, 20),
                        (0, 20),
                        )
                    ]
                }
            )

    def test_cif_layer_notsosimple(self):
        """
        """
        class Inner(rai.Compo):
            def _make(self):
                self.subcompos.rec1 = (
                    rai.RectWH(10, 10).proxy()
                    .map('first')
                    )

                self.subcompos.rec2 = (
                    rai.RectWH(10, 10).proxy()
                    .map('second')
                    .snap_below(self.subcompos.rec1)
                    )

        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.rec = (
                    rai.RectWH(10, 20).proxy()
                    .map('mylayer')
                    .bbox.bot_left.to((0, 0))
                    )

                self.subcompos.inner = (
                    Inner().proxy()
                    .map({
                        'first': 'inner_first',
                        'second': 'inner_second',
                        })
                    .bbox.top_right.to((0, 0))
                    )

        compo = MyCompo()
        exporter = rai.CIFExporter(
            compo,
            multiplier=1,
            rot_multiplier=1,
            cif_native=False,
            flatten_proxies=False,
            native_inline=False,
            transform_fatal=False
            )
        cif_string = exporter.cif_string
        parser = cf.Parser()
        parser.parse(cif_string)
        self.assertPrettyEqual(
            parser.layers,
            {
                'Lmylayer': [
                    (
                        (0, 0),
                        (10, 0),
                        (10, 20),
                        (0, 20),
                        )
                    ],
                'Linner_first': [
                    (
                        (-10, -10),
                        (0, -10),
                        (0, 0),
                        (-10, 0),
                        )
                    ],
                'Linner_second': [
                    (
                        (-10, -20),
                        (0, -20),
                        (0, -10),
                        (-10, -10),
                        )
                    ],
                }
            )

    def test_cif_inline_simple(self):
        """
        """
        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.rec1 = (
                    rai.RectWH(10, 20).proxy()
                    .map('right')
                    .bbox.bot_left.to((0, 0))
                    )

                self.subcompos.rec2 = (
                    rai.RectWH(10, 20).proxy()
                    .map('left')
                    .bbox.bot_right.to((0, 0))
                    )

        compo = MyCompo()
        exporter = rai.CIFExporter(
            compo,
            multiplier=1,
            rot_multiplier=1,
            cif_native=True,
            flatten_proxies=False,
            native_inline=True,
            transform_fatal=False
            )
        cif_string = exporter.cif_string
        parser = cf.Parser()
        parser.parse(cif_string)

        self.assertEqual(len(exporter.steamrolled), 0)

        self.assertPrettyEqual(
            parser.layers,
            {
                'Lright': [
                    (
                        (0, 0),
                        (10, 0),
                        (10, 20),
                        (0, 20),
                        )
                    ],
                'Lleft': [
                    (
                        (-10, 0),
                        (0, 0),
                        (0, 20),
                        (-10, 20),
                        )
                    ]
                }
            )

        self.assertCIFTRoutStructure(
            exporter,
            parser,
            [
                (-1, compo),
                ]
            )

    def test_cif_inline_city(self):
        """
        """
        class TwoTowers(rai.Compo):
            def _make(self):
                self.subcompos.short = (
                    rai.RectWH(10, 40).proxy()
                    .map('short')
                    .bbox.bot_left.to((0, 0))
                    )

                self.subcompos.tall = (
                    rai.RectWH(10, 60).proxy()
                    .map('tall')
                    .snap_right(self.subcompos.short)
                    )

        class CityBlock(rai.Compo):
            def _make(self):
                self.subcompos.one = TwoTowers().proxy()
                self.subcompos.two = self.subcompos.one.copy().move(30, 0)
                self.subcompos.three = self.subcompos.two.copy().move(30, 0)
                self.subcompos.four = self.subcompos.three.copy().move(30, 0)

        class City(rai.Compo):
            def _make(self):
                self.subcompos.one = (
                    CityBlock()
                    .proxy()
                    .map({
                        'short': 'short_mapped',
                        'tall': 'tall_mapped',
                        })
                    )
                self.subcompos.two = self.subcompos.one.copy().move(0, 100)
                self.subcompos.three = self.subcompos.two.copy().move(0, 100)
                self.subcompos.four = self.subcompos.three.copy().move(0, 100)

        compo = City()
        exporter = rai.CIFExporter(
            compo,
            multiplier=1,
            rot_multiplier=1,
            cif_native=True,
            flatten_proxies=False,
            native_inline=True,
            transform_fatal=False
            )
        cif_string = exporter.cif_string
        parser = cf.Parser()
        parser.parse(cif_string)

        self.assertEqual(len(exporter.steamrolled), 0)

        geom_short = np.array((
            (0, 0),
            (10, 0),
            (10, 40),
            (0, 40),
            ))

        geom_tall = np.array((
            (0, 0),
            (10, 0),
            (10, 40),
            (0, 40),
            )) + (10, 0)

        expected_layer_short = []
        expected_layer_tall = []

        for block in range(0, 4):
            for tower in range(0, 4):
                expected_layer_short.append(
                    geom_short + (30 * tower, 100 * block)
                    )
                expected_layer_tall.append(
                    geom_tall + (30 * tower, 100 * block)
                    )

        self.assertPrettyEqual(
            parser.layers,
            {
                'Lshort': expected_layer_short,
                'Ltall': expected_layer_tall,
                }
            )

        self.assertCIFTRoutStructure(
            exporter,
            parser,
            [
                (-1, compo),
                ]
            )


if __name__ == '__main__':
    unittest.main()

