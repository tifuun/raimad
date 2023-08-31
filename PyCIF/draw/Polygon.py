"""
Polygon -- a method for prepresenting geometry
that can be exported to cif
"""

from typing import Self
from abc import ABC, abstractmethod
from copy import deepcopy

import numpy as np

import PyCIF as pc

class Polygon(ABC, pc.Markable):
    """
    Polygon.
    Inheritrs from Transformable, so you can transform it.
    """
    @abstractmethod
    def __init__(self):
        """
        """
        super().__init__()
        self._xyarray = None
        self._bbox = None

        self._add_mark('origin', np.array([0, 0]))

    def __str__(self):
        return (
            f'Polygon {type(self).__name__} '
            f'with {str(self.transform)}'
            )

    @abstractmethod
    def _get_xyarray(self):
        """
        Get array of x,y coordinate pairs in internal coordinates
        (i.e. without applying transformation).

        Polygons should override this method with one that actually
        generates their representation as an xyarray in internal coordinates.
        """

    def get_xyarray(self):
        """
        Get array of x,y coordinate pairs in external coordinates
        (i.e. with transformation).

        Polygons should not override this method.
        Polygons should instead override the provate method
        `_get_xyarray()`.
        This method simply calls `_get_xyarray()` and applies
        the transformation.
        """
        # TODO caching breaks everything when bbox is used
        if self._xyarray is None or 1:
            self._xyarray = self.transform.transform_xyarray(
                self._get_xyarray()
                )
        return self._xyarray

    def get_bbox(self):
        """
        TODO TODO we need a proper system for bboxes
        """
        if self._bbox is None or 1:
            self._bbox = pc.BBox(self.get_xyarray())
        return self._bbox

    def copy(self):
        """
        Return a copy of this polygon
        """
        return deepcopy(self)

    # TODO TODO clear indication own coordinates or external coordinates??
    # this one is own
    #def polar(self, bearing, radius):
    #    radians = np.radians(angle)
    #    x = np.sin(radians) * radius
    #    y = np.cos(radians) * radius
    #    return PointRef(self, Point(x, y))


