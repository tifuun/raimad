"""
width-height Rectangle
"""

import numpy as np

from PyCIF.draw.polygons.Rect import Rect
from PyCIF.draw.Point import Point
from PyCIF.draw.PointRef import PointRef


class RectWH(Rect):

    def __init__(self, width: float, height: float):
        super().__init__()
        self._width = width
        self._height = height

    @property
    def x1(self) -> float:
        return 0

    @property
    def y1(self) -> float:
        return 0

    @property
    def x2(self) -> float:
        return self._width

    @property
    def y2(self) -> float:
        return self._height

