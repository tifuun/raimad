import unittest

import numpy as np

import raimad as rai


class TestPolys(unittest.TestCase):

    def test_rectlw(self):
        rect = rai.RectLW(10, 20)
        self.assertIsNone(np.testing.assert_array_almost_equal(
            rect.geoms['root'][0],
            [
                [-5, -10],
                [5, -10],
                [5, 10],
                [-5, 10]
            ]))

    def test_circle(self):
        circle = rai.Circle(69)
        points = circle.geoms['root'][0]
        self.assertGreaterEqual(len(points), 10)
        for point in points:
            self.assertAlmostEqual(
                np.linalg.norm(point),
                69
                )

    def test_rectwire(self):
        rectwire = rai.RectWire((0, 0), (0, 20), width=10)
        self.assertIsNone(np.testing.assert_array_almost_equal(
            rectwire.geoms['root'][0],
            [
                [-5, 0],
                [5, 0],
                [5, 20],
                [-5, 20]
            ]))

    def test_rectwire_shortsyntax(self):
        rectwire = rai.RectWire((0, 0), (0, 20), 10)
        self.assertIsNone(np.testing.assert_array_almost_equal(
            rectwire.geoms['root'][0],
            [
                [-5, 0],
                [5, 0],
                [5, 20],
                [-5, 20]
            ]))

    def test_rectwire_polar(self):
        rectwire = rai.RectWire(
            (0, 0),
            angle=rai.quartercircle,
            length=20,
            width=10,
            )
        self.assertIsNone(np.testing.assert_array_almost_equal(
            rectwire.geoms['root'][0],
            [
                [-5, 0],
                [5, 0],
                [5, 20],
                [-5, 20]
            ]))

    def test_rectwire_both(self):
        """
        Test that an error is raised if
        both endpoint and length/width specified
        """
        with self.assertRaises(rai.err.RectWireError):
            rai.RectWire(
                (0, 0),
                (0, 20),
                angle=rai.quartercircle,
                length=20,
                width=10,
                )

        with self.assertRaises(rai.err.RectWireError):
            rai.RectWire(
                (0, 0),
                (0, 20),
                angle=rai.quartercircle,
                width=10,
                )

        with self.assertRaises(rai.err.RectWireError):
            rai.RectWire(
                (0, 0),
                (0, 20),
                length=20,
                width=10,
                )

    def test_rectwire_notenough(self):
        """
        Test that an error is raised if
        only angle or only length is given
        """
        with self.assertRaises(rai.err.RectWireError):
            rai.RectWire(
                (0, 0),
                (0, 20),
                angle=rai.quartercircle,
                width=10,
                )

        with self.assertRaises(rai.err.RectWireError):
            rai.RectWire(
                (0, 0),
                (0, 20),
                length=20,
                width=10,
                )

    def test_ansec(self):
        same = [
            rai.AnSec(
                r1=10,
                r2=20,
                theta1=rai.eigthcircle,
                theta2=-rai.eigthcircle,
                orientation=rai.Orientation.NEG
                ),
            rai.AnSec(
                r1=10,
                r2=20,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                orientation=rai.Orientation.POS
                ),
            rai.AnSec(
                r1=10,
                dr=10,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                orientation=rai.Orientation.POS
                ),
            rai.AnSec(
                r2=20,
                dr=10,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                orientation=rai.Orientation.POS
                ),
            rai.AnSec(
                r2=20,
                dr=10,
                theta1=-rai.eigthcircle,
                dtheta=rai.quartercircle,
                orientation=rai.Orientation.POS
                ),
            rai.AnSec(
                r2=20,
                dr=10,
                theta2=rai.eigthcircle,
                dtheta=rai.quartercircle,
                orientation=rai.Orientation.POS
                ),
            rai.AnSec(
                rmid=15,
                dr=10,
                theta2=-rai.eigthcircle,
                dtheta=-rai.quartercircle,
                orientation=rai.Orientation.NEG
                ),
            rai.AnSec(
                rmid=15,
                dr=10,
                thetamid=0,
                dtheta=rai.quartercircle,
                orientation=rai.Orientation.POS
                ),
            rai.AnSec(
                rmid=15,
                dr=-10,
                thetamid=0,
                dtheta=-rai.quartercircle,
                orientation=rai.Orientation.NEG
                ),
            ]

        geoms = [np.sort(ansec.geoms['root'][0], axis=0) for ansec in same]

        self.assertTrue(np.allclose(geoms[0], geoms))

        # invalid
        with self.assertRaises(rai.err.AnSecError):
            rai.AnSec(
                r2=20,
                r1=10,
                dr=-10,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                orientation=rai.Orientation.POS
                )

        with self.assertRaises(rai.err.AnSecError):
            rai.AnSec(
                r2=20,
                dr=10,
                theta2=rai.eigthcircle,
                theta1=0,
                dtheta=-rai.quartercircle,
                orientation=rai.Orientation.NEG
                )

        with self.assertRaises(rai.err.AnSecError):
            rai.AnSec(
                rmid=15,
                theta2=rai.eigthcircle,
                dtheta=rai.quartercircle,
                orientation=rai.Orientation.NEG
                ),

        with self.assertRaises(rai.err.AnSecError):
            rai.AnSec(
                rmid=15,
                dr=5,
                dtheta=rai.semicircle,
                orientation=rai.Orientation.NEG
                ),


if __name__ == '__main__':
    unittest.main()

