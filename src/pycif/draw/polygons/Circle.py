"""
Circle polygon
"""

import numpy as np

import PyCIF as pc

class Circle(pc.Polygon):
    class Marks(pc.Polygon.Marks):
        center = pc.Mark('Center of the circle')

    radius: float

    def __init__(
            self,
            radius: float,
            ):
        super().__init__()
        self.radius = radius
        self.marks.center = pc.Point(0, 0)

    def _get_xyarray(self):
        points = 200
        points = np.linspace(0, 2 * np.pi, points)

        return np.array([
            pc.Point(arg=angle, mag=self.radius)
            for angle in points
            ])

