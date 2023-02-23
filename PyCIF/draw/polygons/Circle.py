"""
Circle polygon
"""

import numpy as np

from PyCIF.draw.Polygon import Polygon
from PyCIF.draw.Point import Point
from PyCIF.draw.PointRef import PointRef


class Circle(Polygon):
    radius: float

    def __init__(
            self,
            radius: float,
            ):
        super().__init__()
        self.radius = radius

    @property
    def _xyarray(self):
        points = 200
        points = np.linspace(0, 2 * np.pi, points)

        return np.array([
            (
                np.cos(angle) * self.radius,
                np.sin(angle) * self.radius,
            )
            for angle in points
            ])

    @property
    def center(self):
        """
        Center of the arc
        """
        return PointRef(self, Point(0, 0))

