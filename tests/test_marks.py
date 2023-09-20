import unittest

import numpy as np
import itertools

import PyCIF as pc

log = pc.get_logger(__name__)

class ThreeMarkCompo(pc.Component):
    Layers = pc.Dict(
        l1=pc.Layer()
        )

    class Marks(pc.Component.Marks):
        center = pc.Mark('Test mark at the origin')
        right = pc.Mark('Test mark to the right')
        down = pc.Mark('Test mark below the origin')

    def _make(self, opts):
        self.marks.center = pc.Point(0, 0)
        self.marks.right = pc.Point(1, 0)
        self.marks.down = pc.Point(0, -1)

class TestMarks(unittest.TestCase):
    def test_marks(self):
        
        class MyCompo(pc.Component):
            Layers = pc.Dict(
                l1=pc.Layer(),
                l2=pc.Layer(),
                l3=pc.Layer()
                )

            def _make(self, opts):
                arc1 = pc.Arc(
                    angle_start=pc.degrees(45),
                    angle_end=pc.degrees(90),
                    radius_inner=10,
                    radius_outter=20
                    )

                # TODO rotate around mark

                arc2 = arc1.copy().rotate(70).scale(0.3)
                arc3 = arc1.copy().rotate(-70).scale(0.3)

                #arc2.align_mark_to_point('center', arc1.marks.end_mid)
                #arc3.align_mark_to_point('center', arc1.marks.start_mid)
                arc2.marks.center.to(arc1.marks.end_mid)
                arc3.marks.center.to(arc1.marks.start_mid)

                self.add_subpolygon(arc1, 'l1')
                self.add_subpolygon(arc2, 'l2')
                self.add_subpolygon(arc3, 'l3')

        compo = MyCompo()

        #with open('./test.cif', 'w') as f:
        #    pc.export_cif(f, compo)

    def test_poly_bbox_transform(self):
        poly = pc.RectWH(1, 1)

        poly.bbox.mid.to((0, 0))
        self.assertEqual(poly.bbox.mid, (0, 0))

        poly.bbox.mid.to((0, 0))
        self.assertEqual(poly.bbox.mid, (0, 0))

        poly.bbox.mid.to((5, 6))
        self.assertEqual(poly.bbox.mid, (5, 6))

        poly.bbox.mid.to((0, 0))
        self.assertEqual(poly.bbox.mid, (0, 0))

    def test_mark_compo_transform(self):

        compo = ThreeMarkCompo()

        self.assertEqual(compo.marks.center, pc.Point(0, 0))
        self.assertEqual(compo.marks.right, pc.Point(1, 0))
        self.assertEqual(compo.marks.down, pc.Point(0, -1))

        compo.move(5, 5)
        self.assertEqual(compo.marks.center, pc.Point(5, 5))
        self.assertEqual(compo.marks.right, pc.Point(6, 5))
        self.assertEqual(compo.marks.down, pc.Point(5, 4))

        compo.marks.center.rotate(pc.degrees(90))
        self.assertEqual(compo.marks.center, pc.Point(5, 5))
        self.assertEqual(compo.marks.right, pc.Point(5, 6))
        self.assertEqual(compo.marks.down, pc.Point(6, 5))

        compo.marks.right.scale(2)
        self.assertEqual(compo.marks.center, pc.Point(5, 4))
        self.assertEqual(compo.marks.right, pc.Point(5, 6))
        self.assertEqual(compo.marks.down, pc.Point(7, 4))

        compo.marks.right.scale(0.5)
        self.assertEqual(compo.marks.center, pc.Point(5, 5))
        self.assertEqual(compo.marks.right, pc.Point(5, 6))
        self.assertEqual(compo.marks.down, pc.Point(6, 5))

        compo.marks.center.rotate(pc.degrees(-90))
        self.assertEqual(compo.marks.center, pc.Point(5, 5))
        self.assertEqual(compo.marks.right, pc.Point(6, 5))
        self.assertEqual(compo.marks.down, pc.Point(5, 4))

        compo.move(-5, -5)
        self.assertEqual(compo.marks.center, pc.Point(0, 0))
        self.assertEqual(compo.marks.right, pc.Point(1, 0))
        self.assertEqual(compo.marks.down, pc.Point(0, -1))

    def test_compo_transform_chaining(self):

        compo = ThreeMarkCompo()

        self.assertEqual(compo.marks.origin, pc.Point(0, 0))

        self.assertEqual(compo.marks.center, pc.Point(0, 0))
        self.assertEqual(compo.marks.right, pc.Point(1, 0))
        self.assertEqual(compo.marks.down, pc.Point(0, -1))

        compo.move(5, 5).move(-5, -5)

        self.assertEqual(compo.marks.center, pc.Point(0, 0))
        self.assertEqual(compo.marks.right, pc.Point(1, 0))
        self.assertEqual(compo.marks.down, pc.Point(0, -1))

        compo.scale(10).scale(0.2)

        self.assertEqual(compo.marks.center, pc.Point(0, 0))
        self.assertEqual(compo.marks.right, pc.Point(2, 0))
        self.assertEqual(compo.marks.down, pc.Point(0, -2))

        (
            compo
            .scale(0.5)
            .rotate(pc.degrees(45))
            .scale(2 ** (1 / 2))
            .move(5, 0)
            .move(0, 5)
            )

        self.assertEqual(compo.marks.center, pc.Point(5, 5))
        self.assertEqual(compo.marks.right, pc.Point(6, 6))
        self.assertEqual(compo.marks.down, pc.Point(6, 4))

    def test_poly_snap(self):

        poly1 = pc.RectWH(1, 1).bbox.mid.to(pc.Point(0, 0))
        poly2 = poly1.copy()
        poly3 = poly1.copy()

        poly2.snap_above(poly1)
        self.assertEqual(poly1.bbox.mid, (0, 0))
        self.assertEqual(poly2.bbox.mid, (0, 1))

        poly2.snap_left(poly1)
        self.assertEqual(poly1.bbox.mid, (0, 0))
        self.assertEqual(poly2.bbox.mid, (-1, 0))

        poly2.snap_right(poly1)
        self.assertEqual(poly1.bbox.mid, (0, 0))
        self.assertEqual(poly2.bbox.mid, (1, 0))

        poly2.snap_below(poly1)
        self.assertEqual(poly1.bbox.mid, (0, 0))
        self.assertEqual(poly2.bbox.mid, (0, -1))

        poly3.snap_below(poly2)
        self.assertEqual(poly1.bbox.mid, (0, 0))
        self.assertEqual(poly2.bbox.mid, (0, -1))
        self.assertEqual(poly3.bbox.mid, (0, -2))

    def test_bbox_pad(self):

        poly1 = pc.RectWH(2, 2)
        poly1.bbox.mid.to((0, 0))
        bbox = poly1.bbox

        self.assertEqual(bbox.left,   -1)
        self.assertEqual(bbox.right,   1)
        self.assertEqual(bbox.top,     1)
        self.assertEqual(bbox.bottom, -1)

        # No args: simple copy
        bbox2 = bbox.pad()
        self.assertEqual(bbox2.left,   -1)
        self.assertEqual(bbox2.right,   1)
        self.assertEqual(bbox2.top,     1)
        self.assertEqual(bbox2.bottom, -1)

        # One arg: same pad everywhere
        bbox2 = bbox.pad(1)
        self.assertEqual(bbox2.left,   -2)
        self.assertEqual(bbox2.right,   2)
        self.assertEqual(bbox2.top,     2)
        self.assertEqual(bbox2.bottom, -2)

        # two args: pad horizontally and vertically
        bbox2 = bbox.pad(5, 10)
        self.assertEqual(bbox2.left,   -6)
        self.assertEqual(bbox2.right,   6)
        self.assertEqual(bbox2.top,     11)
        self.assertEqual(bbox2.bottom, -11)

        # explicit pad for all sides
        bbox2 = bbox.pad(
            left=5,
            top=7,
            right=0,
            bottom=4
            )
        self.assertEqual(bbox2.left,   -6)
        self.assertEqual(bbox2.right,   1)
        self.assertEqual(bbox2.top,     8)
        self.assertEqual(bbox2.bottom, -5)

        # Base padding + specific on sides
        bbox2 = bbox.pad(
            2,
            left=5,
            top=7,
            right=0,
            bottom=4
            )
        self.assertEqual(bbox2.left,   -8)
        self.assertEqual(bbox2.right,   3)
        self.assertEqual(bbox2.top,     10)
        self.assertEqual(bbox2.bottom, -7)

    def test_compo_flip(self):
        
        compo = ThreeMarkCompo()
        self.assertEqual(compo.marks.down, (0, -1))

        compo.marks.center.hflip()
        self.assertEqual(compo.marks.down, (0, 1))

        compo.marks.center.hflip()
        self.assertEqual(compo.marks.down, (0, -1))

        (compo.marks.center + (0, 1)).hflip()
        self.assertEqual(compo.marks.down, (0, 3))  # TODO correct?

    def test_subpolygon_transform(self):

        class MyCompo(pc.Component):
            Layers = pc.Dict(
                root=pc.Layer(),
                )

            def _make(self, opts):
                rect = pc.RectWH(10, 10)
                rect.bbox.mid.to((0, 0))
                self.add_subpolygon(rect)

        compo = MyCompo()
        layers = compo.get_polygons()
        self.assertEqual(len(layers), 1)
        layer = layers['root']
        self.assertEqual(len(layer), 1)
        poly = layer[0]
        self.assertEqual(poly.bbox.mid, (0, 0))

        compo = MyCompo().bbox.mid.to((5, 5))
        layers = compo.get_polygons()
        self.assertEqual(len(layers), 1)
        layer = layers['root']
        self.assertEqual(len(layer), 1)
        poly = layer[0]
        self.assertEqual(poly.bbox.mid, (5, 5))

    def test_subcomponent_transform_simple(self):

        class Inner(pc.Component):
            Layers = pc.Dict(
                root=pc.Layer()
                )

            def _make(self, opts):
                rect = pc.RectWH(1, 1)
                rect.bbox.mid.to((0, 0))
                rect.move(5, 5)
                self.add_subpolygon(rect)

        class Outter(pc.Component):
            Layers = pc.Dict(
                root=pc.Layer()
                )

            def _make(self, opts):
                inner = Inner()
                self.add_subcomponent(inner)

        compo = Outter()
        self.assertEquals(compo.bbox.mid, (5, 5))
        poly = compo.get_polygons()['root'][0]
        self.assertEqual(poly.bbox.mid, (5, 5))

        compo.bbox.mid.to((5, 5))
        self.assertEquals(compo.bbox.mid, (5, 5))
        poly = compo.get_polygons()['root'][0]
        self.assertEqual(poly.bbox.mid, (5, 5))

        compo.move(5, 0)
        self.assertEquals(compo.bbox.mid, (10, 5))
        poly = compo.get_polygons()['root'][0]
        self.assertEqual(poly.bbox.mid, (10, 5))

    def test_subcomponent_transform(self):

        class NestedCompoA(pc.Component):
            """
            A component consisting of one layer containing a 1x16 rectangle
            with marks at (0, 0) and (0, 16)
            """
            Layers = pc.Dict(
                l1=pc.Layer()
                )

            class Marks(pc.Component.Marks):
                start = pc.Mark('Start of the rectangle')
                end = pc.Mark('End of the rectangle')

            def _make(self, opts):
                self.marks.start = pc.Point(0, 0)
                self.marks.end = pc.Point(0, 16)
                self.add_subpolygon(pc.RectWire(self.marks.start, self.marks.end, 2))

        class NestedCompoB(pc.Component):
            """
            A component that includes NestedCompoA
            """
            Layers = pc.Dict(
                l1=pc.Layer(),
                l2=pc.Layer()
                )

            class Marks(pc.Component.Marks):
                start = pc.Mark('Start of the rectangle')
                end = pc.Mark('End of the rectangle')
                child_start = pc.Mark('Start of the child rectangle')
                child_end = pc.Mark('End of the child rectangle')

            def _make(self, opts):
                self.marks.start = pc.Point(0, 0)
                self.marks.end = pc.Point(0, 16)
                self.add_subpolygon(pc.RectWire(self.marks.start, self.marks.end, 2), 'l1')

                child = NestedCompoA()
                child.marks.start.to(self.marks.end)
                child.marks.start.rotate(-pc.degrees(90))
                child.marks.start.scale(1 / 2)
                self.add_subcomponent(
                    child,
                    pc.Dict(
                        l1='l2'
                        )
                    )

                self.marks.child_start = child.marks.start
                self.marks.child_end = child.marks.end

        class NestedCompoC(pc.Component):
            """
            A component that includes NestedCompoB
            """
            Layers = pc.Dict(
                l1=pc.Layer(),
                l2=pc.Layer(),
                l3=pc.Layer()
                )

            class Marks(pc.Component.Marks):
                start = pc.Mark('Start of the rectangle')
                end = pc.Mark('End of the rectangle')
                child_start = pc.Mark('Start of the child rectangle')
                child_end = pc.Mark('End of the child rectangle')
                grandchild_start = pc.Mark('Start of the granchild rectangle')
                grandchild_end = pc.Mark('End of the grandchild rectangle')

            def _make(self, opts):
                self.marks.start = pc.Point(0, 0)
                self.marks.end = pc.Point(0, 16)
                self.add_subpolygon(pc.RectWire(self.marks.start, self.marks.end, 2), 'l1')
                child = NestedCompoB()
                child.marks.start.to(self.marks.end)
                child.marks.start.rotate(-pc.degrees(90))
                child.marks.start.scale(1 / 2)
                self.add_subcomponent(
                    child,
                    pc.Dict(
                        l1='l2',
                        l2='l3',
                        )
                    )
                self.marks.child_start = child.marks.start
                self.marks.child_end = child.marks.end
                self.marks.grandchild_start = child.marks.child_start
                self.marks.grandchild_end = child.marks.child_end


        class MyCompo(pc.Component):
            Layers = pc.Dict(
                l1=pc.Layer(),
                l2=pc.Layer(),
                l3=pc.Layer(),
                )

            def _make(self, opts):
                compo_a = NestedCompoA()
                compo_b = NestedCompoB()
                compo_c = NestedCompoC()

                compo_a.marks.start.to((0, 0))
                compo_b.marks.start.to((16, 0))
                compo_c.marks.start.to((32, 0))

                self.add_subcomponent(compo_a)
                self.add_subcomponent(compo_b)
                self.add_subcomponent(compo_c)

                #self.add_subpolygon(pc.Circle(3).bbox.mid.to((0, 0)), 'l1')
                #self.add_subpolygon(pc.Circle(3).bbox.mid.to((16, 0)), 'l1')
                #self.add_subpolygon(pc.Circle(3).bbox.mid.to((32, 0)), 'l1')

        compo = MyCompo()

        # If you're trying to figure out what's going on with
        # this test, taking a look at the component that's
        # being generated might help:
        with open('../test.cif', 'w') as f:
            pc.export_cif(f, compo)

        expected_polys_l1 = [
            p1 := np.array([
                [-1, 0],
                [-1, 16],
                [1, 16],
                [1, 0],
                ]),
            p1 + [16, 0],
            p1 + [32, 0],
            ]

        expected_polys_l2 = [
            p1 := np.array([
                [16, 15.5],
                [16, 16.5],
                [24, 16.5],
                [24, 15.5],
                ]),
            p1 + [16, 0],
            ]

        expected_polys_l3 = [
            np.array([
                [39.75, 12],
                [39.75, 16],
                [40.25, 16],
                [40.25, 12],
                ]),
            ]
        expected_polys = [expected_polys_l1, expected_polys_l2, expected_polys_l3]

        layers = compo.get_polygons()
        l1 = layers['l1']
        l2 = layers['l2']
        l3 = layers['l3']

        self.assertEqual(len(l1), 3)
        self.assertEqual(len(l2), 2)
        self.assertEqual(len(l3), 1)

        for actual_layer, expected_layer in zip((l1, l2, l3), expected_polys):
            for actual_poly in actual_layer:
                for i, expected_poly in enumerate(expected_layer):

                    deviation = abs((actual_poly.get_xyarray() - expected_poly).sum())
                    log.debug(deviation)
                    if deviation < 0.001:
                        expected_layer.pop(i)
                        break

                else:
                    self.assertTrue(False)

    def test_tl_simple(self):

        length = 100
        bridge_spacing = 10
        bridge_width = 2
        start = pc.Point(10, 10)
        stop = start + (length, 0)

        path0 = [
            pc.tl.StartAt(start),
            pc.tl.StraightTo(stop),
            ]

        # No elbows, should be equal
        path1 = pc.tl.resolve_elbows(path0)
        self.assertEqual(path0, path1)
        
        # No duplicate straights, should be equal
        path2 = pc.tl.reduce_straights(path1)
        self.assertEqual(path1, path2)
        
        # No bends
        path3, bendspecs = pc.tl.construct_bends(path2, radius=10)
        self.assertEqual(path2, path3)
        self.assertFalse(bendspecs)

        # Set bridge spacing to once every 10 px,
        # should be 100 / 10 = 10
        path4, bridgespecs = pc.tl.construct_bridges(
            path3,
            spacing=bridge_spacing,
            scramble=0,
            bridge_width=bridge_width
            )
        #log.debug(pc.tl.format_path(path4))
        #self.assertEqual(path3, path4)
        self.assertEqual(len(bridgespecs), length / bridge_spacing)

        # TODO this just tests that all bridges are
        # somewhere on the line segment between the two points.
        # Is this what we want?
        for bridge in bridgespecs:
            self.assertTrue(bridge.start.x in range(start.x, stop.x))

    #def test_nested_compo_transform_2(self):

    #    class MyCompo(pc.Component):
    #        Layers = pc.Dict(
    #            l1=pc.Layer(),
    #            l2=pc.Layer(),
    #            l3=pc.Layer(),
    #            )

    #        def _make(self, opts):
    #            compo_a = NestedCompoA()
    #            compo_b = NestedCompoB()
    #            compo_c = NestedCompoC()

    #            compo_b.snap_right(compo_a)
    #            compo_b.movex(5)

    #            compo_c.snap_right(compo_b)
    #            compo_c.movex(5)

    #            self.add_subcomponent(compo_a)
    #            self.add_subcomponent(compo_b)
    #            self.add_subcomponent(compo_c)

    #    compo = MyCompo()



