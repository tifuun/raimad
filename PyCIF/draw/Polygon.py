"""
Polygon -- a method for prepresenting geometry
that can be exported to cif
"""

from typing import Self
from abc import ABC, abstractmethod
from copy import deepcopy

import numpy as np

from PyCIF.draw.Alignable import Alignable
from PyCIF.draw.Point import Point
from PyCIF.draw.PointRef import PointRef


class Polygon(ABC, Alignable):
    """
    Polygon.
    Inheritrs from Transformable, so you can transform it.
    """
    @abstractmethod
    def __init__(self):
        """
        """
        super().__init__()

    @property
    @abstractmethod
    def _xyarray(self):
        """
        Get array of x,y coordinate pairs in internal coordinates
        (i.e. without applying transformation)
        """

    @property
    def xyarray(self):
        """
        Get array of x,y coordinate pairs in external coordinates
        (i.e. with transformation)
        """
        xyarray = self._xyarray.copy()
        xyarray = self.transform.transform_xyarray(xyarray)
        return xyarray

    def copy(self):
        """
        Return a copy of this polygon
        """
        return deepcopy(self)

    @property
    def origin(self):
        """
        Polygon origin mark.
        This mark is available to all Polygons.
        """
        return PointRef(self, Point(0, 0))

    # TODO TODO clear indication own coordinates or external coordinates??
    # this one is own
    def polar(self, angle, radius):
        radians = np.radians(angle)
        x = np.sin(radians) * radius
        y = np.cos(radians) * radius
        return PointRef(self, Point(x, y))

