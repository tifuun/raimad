"""
Polygon -- a method for prepresenting geometry
that can be exported to cif
"""

import numpy as np

from PyClewinSDC.Transformable import Transformable


class Polygon(Transformable):
    """
    Polygon.
    Inheritrs from Transformable, so you can transform it.
    """
    def __init__(self, xyarray, transform=None):
        super().__init__(transform)
        self.xyarray = xyarray.copy()

    def get_xyarray(self):
        """
        Return transformed xyarray
        """
        return np.array([
            (self.transform.get_matrix().dot(np.append(point, 1)))[:2]
            for point in self.xyarray
            ])

    def copy(self):
        """
        Return a copy of this polygon
        """
        new_polygon = self.__class__(self.xyarray, self.transform)
        return new_polygon

    @classmethod
    def rect_2point(cls, x1, y1, x2, y2):
        """
        Helper class method for creating a rectangle from two points
        """
        return cls(np.array([
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
            ]))

    @classmethod
    def rect_wh(cls, x1, y1, width, height):
        """
        Helper class method for creating a rectangle from a point,
        width, and height
        """
        return cls.rect_2point(x1, y1, x1 + width, y1 + height)
