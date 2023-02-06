"""
Polygon -- a method for prepresenting geometry
that can be exported to cif
"""

from typing import Self

import numpy as np

from PyCIF.draw.Alignable import Alignable


class Polygon(Alignable):
    """
    Polygon.
    Inheritrs from Transformable, so you can transform it.
    """
    def __init__(self, xyarray, transform=None, bbox=None):
        super().__init__(transform=transform, bbox=bbox)

        #if isinstance(xyarray, np.ndarray):
        #    self.xyarray = xyarray.copy()
        #else:
        #    self.xyarray = np.array(xyarray)

        self.xyarray = xyarray.copy()
        self._bbox.add_xyarray(self.xyarray)

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
        new_polygon = self.__class__(self.xyarray, self.transform, self.bbox)
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
        Helper class method for creating a rectangle from a point
        (top left),
        width, and height
        """
        return cls.rect_2point(x1, y1, x1 + width, y1 + height)

    @classmethod
    def rect_center(cls, x, y, width, height):
        """
        Helper class method for creating a rectangle from a center
        (center),
        width, and height
        """
        return cls.rect_2point(
            x - width / 2,
            y - height / 2,
            x + width / 2,
            y + height / 2,
            )

    @classmethod
    def rect_float(cls, width, height):
        """
        Helper class method for creating a rectangle from
        just the width and height,
        with an undetermined position.
        The intent is to use a snap/align function straight away.
        """
        return cls.rect_wh(
            1000,
            0,
            width,
            height,
            )
