"""
Polygon -- a method for prepresenting geometry
that can be exported to cif
"""

import numpy as np


class Polygon(object):
    """
    Polygon
    It's meant to be immutable btw
    """
    def __init__(self, xyarray=None):
        self.xyarray = [] if xyarray is None else xyarray

    def get_transformed(self, affine_mat):
        """
        Copy polygon and apply affine matrix to the copy
        """
        for point in self.xyarray:
            pass
            #print((affine_mat * np.append(point, 0))[:3])

        new_polygon = Polygon(
            np.array([
                (affine_mat.dot(np.append(point, 1)))[:2]
                for point in self.xyarray
                ])
            )
        return new_polygon


    @classmethod
    def rect_2point(cls, x1, y1, x2, y2):
        return cls(np.array([
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
            ]))


    @classmethod
    def rect_wh(cls, x1, y1, width, height):
        return cls.rect_2point(x1, y1, x1 + width, y1 + width)
