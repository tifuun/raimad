import unittest

import numpy as np

import raimad as rai

from .utils import GeomsEqual, ArrayAlmostEqual

class TestPolys(GeomsEqual, ArrayAlmostEqual, unittest.TestCase):

    def test_rectlw(self):
        rect = rai.RectLW(10, 20)
        self.assertGeomsEqual(
            rect.geoms,
            {
                'root': [
                    [
                        [-5, -10],
                        [5, -10],
                        [5, 10],
                        [-5, 10]
                        ],
                    ]
                }
            )

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
        self.assertGeomsEqual(
            rectwire.geoms,
            {
                'root': [
                    [
                        [-5, 0],
                        [5, 0],
                        [5, 20],
                        [-5, 20]
                        ],
                    ]
                }
            )

    def test_rectwire_shortsyntax(self):
        rectwire = rai.RectWire((0, 0), (0, 20), 10)
        self.assertGeomsEqual(
            rectwire.geoms,
            {
                'root': [
                    [
                        [-5, 0],
                        [5, 0],
                        [5, 20],
                        [-5, 20]
                        ],
                    ]
                }
            )

    def test_rectwire_polar(self):
        rectwire = rai.RectWire(
            (0, 0),
            angle=rai.quartercircle,
            length=20,
            width=10,
            )
        self.assertGeomsEqual(
            rectwire.geoms,
            {
                'root': [
                    [
                        [-5, 0],
                        [5, 0],
                        [5, 20],
                        [-5, 20]
                        ],
                    ]
                }
            )

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
                ),
            rai.AnSec(
                r1=10,
                r2=20,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                ),
            rai.AnSec(
                r1=10,
                dr=10,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                ),
            rai.AnSec(
                r2=20,
                dr=10,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                ),
            rai.AnSec(
                r2=20,
                dr=10,
                theta1=-rai.eigthcircle,
                dtheta=rai.quartercircle,
                ),
            rai.AnSec(
                r2=20,
                dr=10,
                theta2=rai.eigthcircle,
                dtheta=rai.quartercircle,
                ),
            rai.AnSec(
                rmid=15,
                dr=10,
                theta2=-rai.eigthcircle,
                dtheta=-rai.quartercircle,
                ),
            rai.AnSec(
                rmid=15,
                dr=10,
                thetamid=0,
                dtheta=rai.quartercircle,
                ),
            rai.AnSec(
                rmid=15,
                dr=-10,
                thetamid=0,
                dtheta=-rai.quartercircle,
                ),
            ]

        for i, x in enumerate(same):
            open(f'/tmp/{i}.svg', 'w').write(rai.export_svg(x))

        i = 1
        for compo in same[1:]:
            print(i)
            i += 1
            self.assertArrayAlmostEqual(
                same[0].bbox.as_list(),
                compo.bbox.as_list(),
                epsilon=1
                )
            #self.assertGeomsEqual(
            #    same[0].geoms,
            #    compo.geoms
            #    )

        #geoms = [np.sort(ansec.geoms['root'][0], axis=0) for ansec in same]

        #for x in geoms:
        #    print(x)

        #self.assertTrue(np.allclose(geoms[0], geoms))

        # invalid
        with self.assertRaises(rai.err.AnSecError):
            # too many parameters for radius
            rai.AnSec(
                r2=20,
                r1=10,
                dr=-10,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                )

        with self.assertRaises(rai.err.AnSecError):
            # too many parameters for theta
            rai.AnSec(
                r2=20,
                dr=10,
                theta2=rai.eigthcircle,
                theta1=0,
                dtheta=-rai.quartercircle,
                )

        with self.assertRaises(rai.err.AnSecError):
            # No radius specified
            rai.AnSec(
                rmid=15,
                theta2=rai.eigthcircle,
                dtheta=rai.quartercircle,
                ),

        with self.assertRaises(rai.err.AnSecError):
            # No start angle specified
            rai.AnSec(
                rmid=15,
                dr=5,
                dtheta=rai.semicircle,
                ),

    def test_custompoly(self):
        """
        Test CustomPoly
        """
        poly = rai.CustomPoly([
            [10, 10],
            [20, 10],
            [20, 30],
            ])
        self.assertGeomsEqual(
            poly.geoms,
            {
                'root': [
                    [
                        [10, 10],
                        [20, 10],
                        [20, 30],
                        ],
                    ]
                }
            )

    def test_custompoly_marks(self):
        """
        Test CustomPoly with dynamic marks
        """
        poly = rai.CustomPoly([
            ['start', [10, 10]],
            [20, 10],
            ['end', [20, 30]],
            ])
        self.assertGeomsEqual(
            poly.geoms,
            {
                'root': [
                    [
                        [10, 10],
                        [20, 10],
                        [20, 30],
                        ],
                    ]
                }
            )
        self.assertEqual(
            poly.marks.start,
            [10, 10]
            )
        self.assertEqual(
            poly.marks.end,
            [20, 30]
            )


if __name__ == '__main__':
    unittest.main()

