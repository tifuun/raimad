"""
Polygon -- a method for prepresenting geometry
that can be exported to cif
"""

from typing import Self
#from abc import ABC, abstractmethod
from copy import deepcopy

import numpy as np

import PyCIF as pc

class Polygon(pc.Markable, pc.BBoxable):
    """
    Polygon.
    Inheritrs from Transformable, so you can transform it.
    """
    #@abstractmethod
    def __init__(self):
        """
        """
        super().__init__()
        self._xyarray = None
        #self._bbox = None

    def __str__(self):
        return (
            f'Polygon {type(self).__name__} '
            f'with {str(self.transform)}'
            )

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


