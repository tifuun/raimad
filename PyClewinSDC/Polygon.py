"""
Polygon -- a method for prepresenting geometry
that can be exported to cif
"""

from typing import Self

import numpy as np

from PyClewinSDC.Transformable import Transformable
from PyClewinSDC.BBox import BBox


class Polygon(Transformable):
    """
    Polygon.
    Inheritrs from Transformable, so you can transform it.
    """
    def __init__(self, xyarray, transform=None, bbox=None):
        super().__init__(transform)

        #if isinstance(xyarray, np.ndarray):
        #    self.xyarray = xyarray.copy()
        #else:
        #    self.xyarray = np.array(xyarray)

        self.xyarray = xyarray.copy()

        # Outsiders can access this bbox directly
        # TODO read up on how private / public is done in Python
        self._bbox = bbox.copy() if bbox else BBox(self.xyarray)

    def get_xyarray(self):
        """
        Return transformed xyarray
        """
        return np.array([
            (self.transform.get_matrix().dot(np.append(point, 1)))[:2]
            for point in self.xyarray
            ])

    @property
    def bbox(self):
        # TODO caching
        return self._bbox.copy().apply_transform(self.transform)

    def copy(self):
        """
        Return a copy of this polygon
        """
        new_polygon = self.__class__(self.xyarray, self.transform, self.bbox)
        return new_polygon

    def snap_top(self, to: Self):
        """
        Snap on to the top of another polygon.
        """
        # TODO Function overloading in Python?
        # to pass CoordPair or separate x,y to self.move?
        self.move(*(to.bbox.top_mid - self.bbox.bot_mid))
        return self

    def snap_bottom(self, to: Self):
        """
        Snap on to the bottom of another polygon.
        """
        # TODO Function overloading in Python?
        # to pass CoordPair or separate x,y to self.move?
        self.move(*(to.bbox.bot_mid - self.bbox.top_mid))
        return self

    def align_mid(self, to: Self):
        """
        Align centers with another polygon.
        """
        # TODO class for this, like transformable
        self.move(*(to.bbox.mid - self.bbox.mid))
        return self

    def align(self, own_point, target_point):
        """
        Align two arbitrary points
        """
        self.move(*(target_point - own_point))
        return self

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
