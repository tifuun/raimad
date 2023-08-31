"""
Custom polygon built from a set of points
"""

from typing import Self

import numpy as np

import PyCIF as pc


class CustomPolygon(pc.Polygon):

    def __init__(self, points):
        super().__init__()
        self.points = np.array(points, dtype=np.float64)

    def _get_xyarray(self) -> np.ndarray:
        return self.points


