import unittest
from math import sin, cos, radians

import raimad as rai

class TestAffine(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(
            rai.affine.identity(),
            ((1, 0, 0), (0, 1, 0), (0, 0, 1))
            )

    def test_matmul_singular(self):
        mat1 = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            )

        self.assertEqual(
            rai.affine.matmul(mat1),
            mat1
            )

    def test_matmul_double(self):
        mat1 = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            )

        mat2 = (
            (4, 5, 6),
            (1, 2, 3),
            (7, 8, 9),
            )

        self.assertEqual(
            rai.affine.matmul(mat1, mat2),
            (
                (27,  33,  39),
                (63,  78,  93),
                (99, 123, 147),
                )
            )

    def test_matmul_triple(self):
        mat1 = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            )

        mat2 = (
            (4, 5, 6),
            (1, 2, 3),
            (7, 8, 9),
            )

        mat3 = (
            (4, 1, 6),
            (1, 1, 1),
            (7, 1, 9),
            )

        self.assertEqual(
            rai.affine.matmul(mat1, mat2, mat3),
            (
                (414, 99, 546),
                (981, 234, 1293),
                (1548, 369, 2040),
                )
            )

    def test_norm_empty(self):
        self.assertEqual(
            rai.affine.norm([]),
            0
            )

    def test_norm_single(self):
        self.assertEqual(
            rai.affine.norm([420]),
            420
            )

    def test_norm_double(self):
        self.assertAlmostEqual(
            rai.affine.norm([3, 4]),
            5
            )

    def test_norm_triple(self):
        self.assertAlmostEqual(
            rai.affine.norm([3, 4, 5]),
            7.0710678118654755
            )

    def test_norm_quad(self):
        self.assertAlmostEqual(
            rai.affine.norm([3, 4, 5, 6]),
            9.273618495495704
            )

    def test_get_matrix_translation(self):
        x, y = rai.affine.get_translation(
            (
                (1, 0, 6),
                (0, 1, 9),
                (0, 0, 1),
                )
            )
        self.assertAlmostEqual(x, 6)
        self.assertAlmostEqual(y, 9)

    def test_get_matrix_scale(self):
        x, y = rai.affine.get_scale(
            (
                (6, 0, 0),
                (0, 9, 0),
                (0, 0, 1),
                )
            )
        self.assertAlmostEqual(x, 6)
        self.assertAlmostEqual(y, 9)

    def test_get_matrix_shear(self):
        shear = rai.affine.get_shear(
            (
                (1, 0.5, 0),
                (0, 1, 0),
                (0, 0, 1),
                )
            )
        self.assertAlmostEqual(shear, 0.4472135954999)

    def test_get_matrix_rotation(self):
        angle = rai.affine.get_rotation(
            (
                (cos(radians(30)), -sin(radians(30)), 0),
                (sin(radians(30)), cos(radians(30)), 0),
                (0, 0, 1),
                )
            )
        self.assertAlmostEqual(angle, radians(30))
        


if __name__ == '__main__':
    unittest.main()

