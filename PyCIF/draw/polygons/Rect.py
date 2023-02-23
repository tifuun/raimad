"""
Abstract rectangle
"""

from abc import ABC, abstractmethod

import numpy as np

from PyCIF.draw.Polygon import Polygon
from PyCIF.draw.Point import Point
from PyCIF.draw.PointRef import PointRef


# FIXME I'm pretty sure ABC here is not required,
# since Polygon is already an ABC?
class Rect(Polygon):
    """
    Abstract rectangle.
    Deriving rectangles must implement __init__,
    as well as x1, y1, x2, y2 proprties.
    Points on the rectangle and _xyarray property are derived
    from those.
    """

    @property
    @abstractmethod
    def x1(self) -> float:
        """
        Return top left x coordinate
        """

    @property
    @abstractmethod
    def y1(self) -> float:
        """
        Return top left y coordinate
        """

    @property
    @abstractmethod
    def x2(self) -> float:
        """
        Return bottom right x coordinate
        """

    @property
    @abstractmethod
    def y2(self) -> float:
        """
        Return bottom right y coordinate
        """

    @property
    def _xyarray(self) -> np.ndarray:
        return np.array(
            (
                (self.x1, self.y1),
                (self.x2, self.y1),
                (self.x2, self.y2),
                (self.x1, self.y2),
                ),
            dtype=np.float64,
            )

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def mid_right(self):
        """
        .-.-.
        |   |
        .   X
        |   |
        .-.-.
        """
        return PointRef(self, Point(
            self.x1 + self.width,
            self.y1 + self.height / 2,
            ))

    @property
    def mid_left(self):
        """
        .-.-.
        |   |
        X   .
        |   |
        .-.-.
        """
        return PointRef(self, Point(
            self.x1,
            self.y1 + self.height / 2,
            ))

