"""
Rectangle that behaves like a wire.
You give it two points to connect, and a thickness.
"""

import numpy as np

from PyCIF.draw.Polygon import Polygon
from PyCIF.draw.Point import Point
from PyCIF.draw.PointRef import PointRef


class RectWire(Polygon):

    def __init__(self, p1: Point, p2: Point, thickness: float):
        super().__init__()

        angle = np.degrees(np.arctan2(
            p2.y - p1.y,
            p2.x - p1.x,
            ))

        self.v1 = p1.move_polar(
            thickness / 2,
            angle + 90,
            )

        self.v2 = p1.move_polar(
            thickness / 2,
            angle - 90,
            )

        self.v3 = p2.move_polar(
            thickness / 2,
            angle - 90,
            )

        self.v4 = p2.move_polar(
            thickness / 2,
            angle + 90,
            )

    def _get_xyarray(self) -> np.ndarray:
        return np.array(
            (
                (self.v1.x, self.v1.y),
                (self.v2.x, self.v2.y),
                (self.v3.x, self.v3.y),
                (self.v4.x, self.v4.y),
                ),
            dtype=np.float64,
            )

