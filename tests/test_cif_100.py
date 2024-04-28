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

# Regext to find cif polygons with four points
find_rect_polys = re.compile(
    r"^\s*P\s(-?\d+)\s(-?\d+)\s(-?\d+)\s(-?\d+)"
    r"\s(-?\d+)\s(-?\d+)\s(-?\d+)\s(-?\d+)\s*;",
    re.MULTILINE
    )

def adjlist_to_cif(exporter, adjlist):
    """
    Helper for checking CIF routine call structure.
    Convert an adjecency list in the format {
        (proxy, proxy),
        (proxy, proxy),
        ...
    }
    to the format {
        (cif_rout_number, cif_rout_number),
        (cif_rout_number, cif_rout_number),
        ...
    }
    given the exporter object.
    """

class CIFRoutGraphChecker():
    """
    Mixin for unittest.TestCase
    that can be used to check whether the graph representing cif routine calls
    matches the structure of the cif subcomponent graph.
    """
    def assertCIFRoutStructure(self, exporter, adjlist):
        self.assertEqual(
            {
                tuple(exporter.rout_map[proxy] for proxy in edge)
                for edge in adjlist
                },
            exporter.rout_list
            )

class BoxesStar(pc.Compo):
    """
    cif-linked boxes in "star" topology:
    multiple boxes are cif links of one root box
    """
    def _make(self, add_root: bool):
        first = pc.RectWH(10, 10) @ 'first'
        second = first.cifcopy().move(20, 0) @ 'second'
        third = first.cifcopy().move(-20, 0) @ 'third'
        fourth = first.cifcopy().move(0, 20) @ 'fourth'

        if add_root:
            self.subcompos.first = first

        self.subcompos.second = second
        self.subcompos.third = third
        self.subcompos.fourth = fourth

class BoxesChain(pc.Compo):
    """
    cif-linked boxes in "chain" topology:
    there is a root box, a link to that box, a link to that box, ...
    """
    def _make(self):
        first = pc.RectWH(10, 10) @ 'root'
        second = first.cifcopy().move(20, 0)
        third = second.cifcopy().move(20, 0)
        fourth = third.cifcopy().move(20, 0)

        self.subcompos.first = first
        self.subcompos.second = second
        self.subcompos.third = third
        self.subcompos.fourth = fourth


class TestCIF100(unittest.TestCase, CIFRoutGraphChecker):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.boxes_chain_sub = BoxesChain()
        self.boxes_star_sub = BoxesStar(add_root=True)
        self.boxes_star_nosub = BoxesStar(add_root=False)

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
                #TODO hardcoded multiplier
                (str(1000 * 10), str(1000 * 20), '0', '0')
                ]
            )
        # This assumes that RectWH is centered at origin,
        # which it should be.

        # TODO also check rotation

    def test_cif_link_star_sub(self):
        """
        test copy-with-cif-link feature with "star" topology:
        multiple copies link to one "root" compo.
        The root compo is also a subcompo of the toplevel.
        """

        compo = self.boxes_star_sub

        exporter = pc.CIFExporter(
            compo,
            cif_native=False,
            cif_link=True,
            cif_link_fatal=True,
            )
        cifstring = exporter.export_cif()
        open('/tmp/test.cif', 'w').write(cifstring)

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

    def test_cif_link_star_nosub(self):
        """
        test copy-with-cif-link feature with "star" topology:
        multiple copies link to one "root" compo.
        The root compo is NOT a subcompo of the toplevel.
        """

        compo = self.boxes_star_nosub

        exporter = pc.CIFExporter(
            compo,
            cif_native=False,
            cif_link=True,
            cif_link_fatal=True,
            )
        cifstring = exporter.export_cif()
        open('/tmp/test.cif', 'w').write(cifstring)

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
                (compo.subcompos.second, compo.subcompos.first),
                (compo.subcompos.third, compo.subcompos.first),
                (compo.subcompos.fourth, compo.subcompos.first),
                }
            )

        # TODO here check geometry

    def test_cif_link_chain_sub(self):

        compo = self.boxes_chain_sub

        exporter = pc.CIFExporter(
            compo,
            cif_native=False,
            cif_link=True,
            cif_link_fatal=True,
            )
        cifstring = exporter.export_cif()
        open('/tmp/test.cif', 'w').write(cifstring)

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
                (compo.subcompos.second, compo.subcompos.first),
                (compo.subcompos.third, compo.subcompos.second),
                (compo.subcompos.fourth, compo.subcompos.third),
                }
            )

        # TODO here check geometry

    def test_cif_link_chain_nosub(self):

        compo = self.boxes_chain_nosub

        exporter = pc.CIFExporter(
            compo,
            cif_native=False,
            cif_link=True,
            cif_link_fatal=True,
            )
        cifstring = exporter.export_cif()
        open('/tmp/test.cif', 'w').write(cifstring)

        # There should only be one polygon,
        # and the rest are copies
        polygons = find_rect_polys.findall(cifstring)
        self.assertEqual(len(polygons), 1)

        # Test that the structure of the component
        # corresponds with the structure of the cif routine calls
        self.assertCIFRoutStructure(
            exporter,
            {
                # This one should be missing compared to boxes_chain_sub:
                # (compo, compo.subcompos.first),
                (compo, compo.subcompos.second),
                (compo, compo.subcompos.third),
                (compo, compo.subcompos.fourth),
                (compo.subcompos.second, compo.subcompos.first),
                (compo.subcompos.third, compo.subcompos.second),
                (compo.subcompos.fourth, compo.subcompos.third),
                }
            )

        # TODO here check geometry

    def test_cif_link_complex(self):
        """
        like test_cif_link,
        but a little more complex
        """

        class Sub1(pc.Compo):
            def _make(self):
                self.subcompos.first = pc.RectWH(10, 10) @ 'first'
                self.subcompos.second = (
                    self.subcompos.first.cifcopy()
                    .move(0, 20)
                    @ 'second'
                    )

        class Sub2(pc.Compo):
            def _make(self):
                self.subcompos.first = pc.Circle(10) @ 'first'
                self.subcompos.second = (
                    self.subcompos.first.cifcopy()
                    .move(0, 20)
                    @ 'second'
                    )

        class MyCompo(pc.Compo):
            def _make(self):
                self.subcompos.sub1 = (Sub1() @ {
                    'first': 'sub1_first',
                    'second': 'sub1_second',
                    }).move(-20, 0)

                self.subcompos.sub2 = (Sub2() @ {
                    'first': 'sub2_first',
                    'second': 'sub2_second',
                    }).move(20, 0)

                self.subcompos.sub22 = (
                    self.subcompos.sub2.cifcopy()
                    .move(20, 0)
                    @ {
                        'first': 'sub22_first',
                        'second': 'sub22_second',
                        }
                    )

        mycompo = MyCompo()

        cifstring = pc.export_cif(
            mycompo,
            cif_native=False,
            cif_link=True
            )

        polygons = find_rect_polys.findall(cifstring)
        self.assertEqual(len(polygons), 2)

        # TODO here check geometry

    def test_cif_link_complex_fail(self):
        """
        Test that cif exporter detects when
        it's impossible to keep a component linked
        """

        class Sub1(pc.Compo):
            def _make(self):
                self.subcompos.first = pc.RectWH(10, 10) @ 'first'
                self.subcompos.second = (
                    self.subcompos.first.cifcopy()
                    .move(0, 20)
                    @ 'second'
                    )

        class Sub2(pc.Compo):
            def _make(self):
                self.subcompos.first = pc.Circle(10) @ 'first'
                self.subcompos.second = (
                    self.subcompos.first.cifcopy()
                    .move(0, 20)
                    @ 'second'
                    )

        class MyCompo(pc.Compo):
            def _make(self):
                self.subcompos.sub1 = (Sub1() @ {
                    'first': 'sub1_first',
                    'second': 'sub1_second',
                    }).hflip()

                self.subcompos.sub2 = (Sub2() @ {
                    'first': 'sub2_first',
                    'second': 'sub2_second',
                    }).move(20, 0)

                self.subcompos.sub22 = (
                    self.subcompos.sub2.cifcopy()
                    .move(20, 0)
                    @ {
                        'first': 'sub22_first',
                        'second': 'sub22_second',
                        }
                    )

        mycompo = MyCompo()

        with self.assertRaises(pc.err.CannotCIFLinkError):
            pc.export_cif(
                mycompo,
                cif_native=False,
                cif_link=True,
                cif_link_fatal=True
                )

# TODO
# test non-subcompo link
# test fallback on un-cifable transform
# link is just self.compo?
# TODO DISALLOW ADDING DIRECT COMPOS!

if __name__ == '__main__':
    unittest.main()

