"""
Rectangle polygon
"""

from typing import ClassVar

import numpy as np

from PyCIF.draw.Polygon import Polygon

class Rect(Polygon):
    width: ClassVar[int]
    height: ClassVar[int]

    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height

    @property
    def _xyarray(self):
        return np.array((
            (0, 0),
            (self.width, 0),
            (self.width, self.height),
            (0, self.height),
            ))

