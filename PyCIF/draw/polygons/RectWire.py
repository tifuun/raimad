"""
Rectangle that behaves like a wire.
You give it two points to connect, and a thickness.
"""

import numpy as np

import PyCIF as pc

class RectWire(pc.Polygon):

    def __init__(self, p1, p2, thickness: float):
        super().__init__()

        angle = pc.angle_between(p1, p2)

        self.v1 = p1 + pc.Point_polar(
            angle + 90,
            thickness / 2,
            )

        self.v2 = p1 + pc.Point_polar(
            angle - 90,
            thickness / 2,
            )

        self.v3 = p2 + pc.Point_polar(
            angle - 90,
            thickness / 2,
            )

        self.v4 = p2 + pc.Point_polar(
            angle + 90,
            thickness / 2,
            )

    def _get_xyarray(self) -> np.ndarray:
        return np.array([
            self.v1,
            self.v2,
            self.v3,
            self.v4,
            ])

