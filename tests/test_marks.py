import unittest

import PyCIF as pc

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

        with open('./test.cif', 'w') as f:
            pc.export_cif(f, compo)

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
        self.assertEqual(poly1.bbox.mid, pc.Point(0, 0))
        self.assertEqual(poly2.bbox.mid, pc.Point(0, 1))

        poly2.snap_left(poly1)
        self.assertEqual(poly1.bbox.mid, pc.Point(0, 0))
        self.assertEqual(poly2.bbox.mid, pc.Point(-1, 0))

        poly2.snap_right(poly1)
        self.assertEqual(poly1.bbox.mid, pc.Point(0, 0))
        self.assertEqual(poly2.bbox.mid, pc.Point(1, 0))

        poly2.snap_below(poly1)
        self.assertEqual(poly1.bbox.mid, pc.Point(0, 0))
        self.assertEqual(poly2.bbox.mid, pc.Point(0, -1))

        poly3.snap_below(poly2)
        self.assertEqual(poly1.bbox.mid, pc.Point(0, 0))
        self.assertEqual(poly2.bbox.mid, pc.Point(0, -1))
        self.assertEqual(poly3.bbox.mid, pc.Point(0, -2))
