import unittest

import numpy as np

import pycif as pc


class TestPolys(unittest.TestCase):

    def test_rectwh(self):
        rect = pc.RectWH(10, 20)
        self.assertIsNone(np.testing.assert_array_almost_equal(
            rect.geoms['root'][0],
            [
                [-5, -10],
                [5, -10],
                [5, 10],
                [-5, 10]
            ]))

    def test_circle(self):
        circle = pc.Circle(69)
        points = circle.geoms['root'][0]
        self.assertGreaterEqual(len(points), 10)
        for point in points:
            self.assertAlmostEqual(
                np.linalg.norm(point),
                69
                )

    def test_rectwire(self):
        rectwire = pc.RectWire((0, 0), (0, 20), 10)
        self.assertIsNone(np.testing.assert_array_almost_equal(
            rectwire.geoms['root'][0],
            [
                [-5, 0],
                [5, 0],
                [5, 20],
                [-5, 20]
            ]))

    def test_ansec(self):
        same = [
            pc.AnSec(
                r1=10,
                r2=20,
                theta1=pc.eigthcircle,
                theta2=-pc.eigthcircle,
                orientation=pc.Orientation.NEG
                ),
            pc.AnSec(
                r1=10,
                r2=20,
                theta1=-pc.eigthcircle,
                theta2=pc.eigthcircle,
                orientation=pc.Orientation.POS
                ),
            pc.AnSec(
                r1=10,
                dr=10,
                theta1=-pc.eigthcircle,
                theta2=pc.eigthcircle,
                orientation=pc.Orientation.POS
                ),
            pc.AnSec(
                r2=20,
                dr=10,
                theta1=-pc.eigthcircle,
                theta2=pc.eigthcircle,
                orientation=pc.Orientation.POS
                ),
            pc.AnSec(
                r2=20,
                dr=10,
                theta1=-pc.eigthcircle,
                dtheta=pc.quartercircle,
                orientation=pc.Orientation.POS
                ),
            pc.AnSec(
                r2=20,
                dr=10,
                theta2=pc.eigthcircle,
                dtheta=pc.quartercircle,
                orientation=pc.Orientation.POS
                ),
            pc.AnSec(
                rmid=15,
                dr=10,
                theta2=-pc.eigthcircle,
                dtheta=-pc.quartercircle,
                orientation=pc.Orientation.NEG
                ),
            pc.AnSec(
                rmid=15,
                dr=10,
                thetamid=0,
                dtheta=pc.quartercircle,
                orientation=pc.Orientation.POS
                ),
            pc.AnSec(
                rmid=15,
                dr=-10,
                thetamid=0,
                dtheta=-pc.quartercircle,
                orientation=pc.Orientation.NEG
                ),
            ]

        #class Foobar(pc.Compo):
        #    def _make(self):
        #        for i, c in enumerate(same):
        #            self.subcompos.append(
        #                c.movex(i * 40)
        #                )
        #c = Foobar()
        #with open('/tmp/foo.cif', 'w') as f: f.write(pc.export_cif(c))

        geoms = [np.sort(ansec.geoms['root'][0], axis=0) for ansec in same]

        self.assertTrue(np.allclose(geoms[0], geoms))

        # invalid
        with self.assertRaises(pc.err.AnSecError):
            pc.AnSec(
                r2=20,
                r1=10,
                dr=-10,
                theta1=-pc.eigthcircle,
                theta2=pc.eigthcircle,
                orientation=pc.Orientation.POS
                )

        with self.assertRaises(pc.err.AnSecError):
            pc.AnSec(
                r2=20,
                dr=10,
                theta2=pc.eigthcircle,
                theta1=0,
                dtheta=-pc.quartercircle,
                orientation=pc.Orientation.NEG
                )

        with self.assertRaises(pc.err.AnSecError):
            pc.AnSec(
                rmid=15,
                theta2=pc.eigthcircle,
                dtheta=pc.quartercircle,
                orientation=pc.Orientation.NEG
                ),

        with self.assertRaises(pc.err.AnSecError):
            pc.AnSec(
                rmid=15,
                dr=5,
                dtheta=pc.semicircle,
                orientation=pc.Orientation.NEG
                ),


if __name__ == '__main__':
    unittest.main()

