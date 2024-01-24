"""
Custom poly built from a set of points
"""

import numpy as np

import pycif as pc


class CustomPoly(pc.Poly):

    def __init__(self, points):
        super().__init__()
        self.points = np.array(points, dtype=np.float64)

    def _get_xyarray(self) -> np.ndarray:
        return self.points


