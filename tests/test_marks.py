import unittest

import PyCIF as pc

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



