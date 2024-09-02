import unittest

import raimad as rai

from .utils import GeomsEqual, ArrayAlmostEqual

class TestPolys(GeomsEqual, ArrayAlmostEqual, unittest.TestCase):

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
                theta1=rai.eigthcircle,
                theta2=-rai.eigthcircle,
                num_points=300,
                ),
            rai.AnSec.from_auto(
                r1=10,
                r2=20,
                theta1=rai.eigthcircle,
                theta2=-rai.eigthcircle,
                ),
            rai.AnSec.from_auto(
                r1=10,
                r2=20,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                ),
            rai.AnSec.from_auto(
                r1=10,
                dr=10,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                ),
            rai.AnSec.from_auto(
                r2=20,
                dr=10,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                ),
            rai.AnSec.from_auto(
                r2=20,
                dr=10,
                theta1=-rai.eigthcircle,
                dtheta=rai.quartercircle,
                ),
            rai.AnSec.from_auto(
                r2=20,
                dr=10,
                theta2=rai.eigthcircle,
                dtheta=rai.quartercircle,
                ),
            rai.AnSec.from_auto(
                rmid=15,
                dr=10,
                theta2=-rai.eigthcircle,
                dtheta=-rai.quartercircle,
                ),
            rai.AnSec.from_auto(
                rmid=15,
                dr=10,
                thetamid=0,
                dtheta=rai.quartercircle,
                ),
            rai.AnSec.from_auto(
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
            rai.AnSec.from_auto(
                r2=20,
                r1=10,
                dr=-10,
                theta1=-rai.eigthcircle,
                theta2=rai.eigthcircle,
                )

        with self.assertRaises(rai.err.AnSecError):
            # too many parameters for theta
            rai.AnSec.from_auto(
                r2=20,
                dr=10,
                theta2=rai.eigthcircle,
                theta1=0,
                dtheta=-rai.quartercircle,
                )

        with self.assertRaises(rai.err.AnSecError):
            # No radius specified
            rai.AnSec.from_auto(
                rmid=15,
                theta2=rai.eigthcircle,
                dtheta=rai.quartercircle,
                ),

        with self.assertRaises(rai.err.AnSecError):
            # No start angle specified
            rai.AnSec.from_auto(
                rmid=15,
                dr=5,
                dtheta=rai.semicircle,
                ),


if __name__ == '__main__':
    unittest.main()

