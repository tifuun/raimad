"""
Rectangle between top-left and bottom-right points
"""

import numpy as np

from PyCIF.draw.polygons.Rect import Rect
from PyCIF.draw.Point import Point
from PyCIF.draw.PointRef import PointRef


class Rect2P(Rect):

    def __init__(self, p1: Point, p2: Point):
        super().__init__()
        self._x1 = p1.x
        self._y1 = p1.y
        self._x2 = p2.x
        self._y2 = p2.y

    @property
    def x1(self) -> float:
        return self._x1

    @property
    def y1(self) -> float:
        return self._y1

    @property
    def x2(self) -> float:
        return self._x2

    @property
    def y2(self) -> float:
        return self._y2

