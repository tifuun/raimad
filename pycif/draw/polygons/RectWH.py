"""
width-height Rectangle
"""

import numpy as np

import pycif as pc


class RectWH(pc.Polygon):

    def __init__(self, width: float, height: float):
        super().__init__()
        self.width = width
        self.height = height

    def _get_xyarray(self) -> np.ndarray:
        return np.array(
            (
                (0, 0),
                (self.width, 0),
                (self.width, self.height),
                (0, self.height),
                ),
            dtype=np.float64,
            )


