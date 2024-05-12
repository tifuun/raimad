"""
Tests for pycif 1.0.0 cif exporter
"""

import unittest
import re

import numpy as np

import pycif as pc

# Regex to find procedure calls in CIF file
find_procedure_calls = re.compile(r"^\s*C (\w+);", re.MULTILINE)

# Regex to find box commands in CIF file
find_box_calls = re.compile(
    r"^\s*B (\d+) (\d+) (-?\d+) (-?\d+)\s;",
    re.MULTILINE
    )

# Regex to find cif polygons with four points
find_rect_polys = re.compile(
    r"^\s*P\s(-?\d+)\s(-?\d+)\s(-?\d+)\s(-?\d+)"
    r"\s(-?\d+)\s(-?\d+)\s(-?\d+)\s(-?\d+)\s*;",
    re.MULTILINE
    )

class CIFRoutGraphChecker():
    """
    Mixin for unittest.TestCase
    that can be used to check whether the graph representing cif routine calls
    matches the structure of the cif subcomponent graph.
    """
    def assertCIFRoutStructure(self, exporter, adjlist):
        self.assertEqual(
            {
                tuple(exporter.compo2rout[proxy] for proxy in edge)
                for edge in adjlist
                },
            set(exporter.edges)
            )

class Boxes(pc.Compo):
    """
    cif-linked boxes in "star" topology:
    multiple boxes are cif links of one root box
    """
    def _make(self, add_root: bool):
        first = pc.RectWH(10, 10).proxy().map('first')
        second = first.copy().move(20, 0).map('second')
        third = first.copy().move(-20, 0).map('third')
        fourth = first.copy().move(0, 20).map('fourth')

        if add_root:
            self.subcompos.first = first

        self.subcompos.second = second
        self.subcompos.third = third
        self.subcompos.fourth = fourth

        self.first = first

class Sub1(pc.Compo):
    """
    Two rectangles, one above the other
    """
    def _make(self):
        self.subcompos.first = pc.RectWH(10, 10).proxy().map('first')
        self.subcompos.second = (
            self.subcompos.first.copy()
            .move(0, 20)
            .map('second')
            )

class Sub2(pc.Compo):
    """
    Two circles, one above the other
    """
    def _make(self):
        self.subcompos.first = pc.Circle(10).proxy().map('first')
        self.subcompos.second = (
            self.subcompos.first.copy()
            .move(0, 20)
            .map('second')
            )

class Complex(pc.Compo):
    """
    Left: two rectangles
    middle: two circles, slightly rotated
    right: two circles, rotated a little more
    """
    def _make(self, invalid_transform: bool = False):
        self.subcompos.sub1 = Sub1().proxy().map({
            'first': 'sub1_first',
            'second': 'sub1_second',
            }).move(-20, 0)

        self.subcompos.sub2 = Sub2().proxy().map({
            'first': 'sub2_first',
            'second': 'sub2_second',
            }).rotate(np.deg2rad(10))

        if invalid_transform:
            self.subcompos.sub2.scale(2)

        self.subcompos.sub22 = (
            self.subcompos.sub2.copy()
            .move(20, 0)
            .rotate(np.deg2rad(5))
            .map({
                'first': 'sub22_first',
                'second': 'sub22_second',
                })
            )



class TestCIF100(unittest.TestCase, CIFRoutGraphChecker):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.boxes_sub = Boxes(add_root=True)
        self.boxes_nosub = Boxes(add_root=False)

    def test_cif_native_rectwh(self):
        """
        Check native cif export of rectwh
        """
        compo = pc.RectWH(10, 20)
        cifstring = pc.export_cif(
            compo,
            cif_native=True
            )
        box_calls = find_box_calls.findall(cifstring)
        self.assertEqual(
            box_calls,
            [
                (
                    str(int(pc.CIFExporter.multiplier * 10)),
                    str(int(pc.CIFExporter.multiplier * 20)),
                    '0',
                    '0')
                ]
            )
        # This assumes that RectWH is centered at origin,
        # which it should be.

        # TODO also check rotation

    def test_cif_link_sub(self):
        """
        """

        compo = self.boxes_sub

        exporter = pc.CIFExporter(
            compo,
            cif_native=False,
            transform_fatal=True,
            )
        cifstring = exporter.cif_string

        # There should only be one polygon,
        # and the rest are copies
        polygons = find_rect_polys.findall(cifstring)
        self.assertEqual(len(polygons), 1)

        # Test that the structure of the component
        # corresponds with the structure of the cif routine calls
        self.assertCIFRoutStructure(
            exporter,
            {
                (compo, compo.subcompos.first),
                (compo, compo.subcompos.second),
                (compo, compo.subcompos.third),
                (compo, compo.subcompos.fourth),
                (compo.subcompos.first, compo.subcompos.first.compo),
                (compo.subcompos.second, compo.subcompos.first.compo),
                (compo.subcompos.third, compo.subcompos.first.compo),
                (compo.subcompos.fourth, compo.subcompos.first.compo),
                }
            )

        # TODO here check geometry

    def test_cif_link_nosub(self):
        """
        """

        compo = self.boxes_nosub

        exporter = pc.CIFExporter(
            compo,
            cif_native=False,
            transform_fatal=True,
            )
        cifstring = exporter.cif_string

        # There should only be one polygon,
        # and the rest are copies
        polygons = find_rect_polys.findall(cifstring)
        self.assertEqual(len(polygons), 1)

        # Test that the structure of the component
        # corresponds with the structure of the cif routine calls
        self.assertCIFRoutStructure(
            exporter,
            {
                # This one should be missing compared to boxes_star_sub:
                # (compo, compo.subcompos.first),
                (compo, compo.subcompos.second),
                (compo, compo.subcompos.third),
                (compo, compo.subcompos.fourth),
                (compo.subcompos.second, compo.first.compo),
                (compo.subcompos.third, compo.first.compo),
                (compo.subcompos.fourth, compo.first.compo),
                }
            )

        self.assertTrue(
            compo.first.compo not in compo.subcompos.values()
            )

        # TODO here check geometry

    def test_cif_link_complex(self):
        """
        like test_cif_link,
        but a little more complex
        """
        mycompo = Complex()

        cifstring = pc.export_cif(
            mycompo,
            cif_native=False,
            transform_fatal=True,
            flatten_proxies=False,
            )

        polygons = find_rect_polys.findall(cifstring)
        self.assertEqual(len(polygons), 2)

        # TODO here check geometry

    def test_cif_invalid_transform_fail(self):
        """
        """

        mycompo = Complex(invalid_transform=True)

        with self.assertRaises(pc.err.CannotCompileTransformError):
            pc.export_cif(
                mycompo,
                cif_native=False,
                transform_fatal=True
                )

    def test_cif_invalid_transform_fallback(self):
        """
        """

        class MyCompo(pc.Compo):
            def _make(self):
                self.subcompos.append(
                    pc.RectWH(10, 20)
                    .proxy()
                    .scale(2)
                    .bbox.bot_left.to((0, 0))
                    )

        mycompo = MyCompo()

        exporter = pc.CIFExporter(
            mycompo,
            flatten_proxies=True,
            cif_native=False,
            native_inline=False,
            transform_fatal=False,
            multiplier=1,
            )
        cifstring = exporter.cif_string

        self.assertEqual(
            len(exporter.invalid_transforms),
            1
            )

        polys = find_rect_polys.findall(cifstring)

        self.assertEqual(len(polys), 1)

        self.assertEqual(
            polys[0],
            (
                '0', '0',
                '20', '0',
                '20', '40',
                '0', '40',
                )
            )

    def test_cif_invalid_transform_fallback_export_proxy(self):
        """
        """
        mycompo = (
            pc.RectWH(10, 20)
            .proxy()
            .scale(2)
            .bbox.bot_left.to((0, 0))
            )

        exporter = pc.CIFExporter(
            mycompo,
            flatten_proxies=True,
            cif_native=False,
            native_inline=False,
            transform_fatal=False,
            multiplier=1,
            )
        cifstring = exporter.cif_string

        self.assertEqual(
            len(exporter.invalid_transforms),
            1
            )

        polys = find_rect_polys.findall(cifstring)

        self.assertEqual(len(polys), 1)

        self.assertEqual(
            polys[0],
            (
                '0', '0',
                '20', '0',
                '20', '40',
                '0', '40',
                )
            )


# TODO
# test non-subcompo link
# test fallback on un-cifable transform
# link is just self.compo?
# TODO DISALLOW ADDING DIRECT COMPOS!

if __name__ == '__main__':
    unittest.main()

