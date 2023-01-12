import numpy as np


class Transform(object):
    """
    Container for an affine matrix
    with methods to apply elementary transformations
    to that matrix.

    This is my first time working with affine matrices,
    so expect some obtuse code.

    You can see that the transformation methods all return
    the object themselves.
    You can use this for shortuts like

    flipped = transformable.copy().hflip()
    """
    transform_methods = {}

    def __init__(self, affine_mat=None):
        if affine_mat is None:
            self.affine_mat = np.identity(3)
        else:
            self.affine_mat = affine_mat.copy()

    def copy(self):
        return Transform(self.affine_mat)

    def get_matrix(self):
        """
        Return affine matrix
        """
        return self.affine_mat

    def _fix_affine(self):
        self.affine_mat[2, 0] = 0
        self.affine_mat[2, 1] = 0
        self.affine_mat[2, 2] = 1

    def apply_transform(self, transform):
        """
        Apply another Transform to this Transform
        """
        self.affine_mat = np.matmul(
            transform.affine_mat,
            self.affine_mat,
            )
        return self

    def move(self, x, y):
        self.affine_mat = np.matmul(
            np.array([
                [1, 0, x],
                [0, 1, y],
                [0, 0, 1],
                ]),
            self.affine_mat,
            )
        self._fix_affine()
        return self

    def movex(self, x):
        return self.move(x, 0)

    def movey(self, y):
        return self.move(0, y)

    def scale(self, x, y=None):
        if y is None:
            y = x
        self.affine_mat = np.matmul(
            np.array([
                [x, 0, 0],
                [0, y, 0],
                [1, 0, 1],
                ]),
            self.affine_mat,
            )
        self._fix_affine()
        return self

    def rot(self, degrees):
        cosine = np.cos(np.radians(degrees))
        sine = np.sin(np.radians(degrees))
        self.affine_mat = np.matmul(
            np.array([
                [cosine, -sine, 0],
                [sine, cosine, 0],
                [1, 0, 1],
                ]),
            self.affine_mat,
            )
        self._fix_affine()
        return self

    def hflip(self):
        self.scale(1, -1)
        return self

    def vflip(self):
        self.scale(-1, 1)
        return self

    def flip(self):
        self.scale(-1, -1)
        return self

