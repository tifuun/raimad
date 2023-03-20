"""
Circle polygon
"""

import numpy as np

import PyCIF as pc

class Circle(pc.Polygon):
    radius: float

    def __init__(
            self,
            radius: float,
            ):
        super().__init__()
        self.radius = radius

    def _get_xyarray(self):
        points = 200
        points = np.linspace(0, 2 * np.pi, points)

        return np.array([
            pc.point_polar(angle, self.radius)
            for angle in points
            ])

