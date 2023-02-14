"""
Vector -- immutable storage for x, y coordinate pair.
You can think of it as either a coordinate point,
or as an arrow pointing from origin to a specific point.
"""

from typing import Tuple, Self

import numpy as np

class Vector(object):
    def __init__(self, x: float | None = None, y: float | None = None):
        if x is None or y is None:
            raise Exception('Use Vector.xy or Vector.polar')
        self.x = x
        self.y = y
    
    @classmethod
    def xy(cls, x, y):
        """
        Create new vector from x, y coordinate pair
        """
        return cls(x, y)
    
    @classmethod
    def polar(cls, argument, magnitude):
        """
        Create new vector from argument, magnitude pair
        """
        x = np.cos(argument) * magnitude
        y = np.sin(argument) * magnitude
        return cls(x, y)

    def __iter__(self) -> Tuple[float, float]:
        """
        Iterator method allows unpacking
        a Vector into [x, y]
        """
        return iter((self.x, self.y))

    def __add__(self, other: Self) -> Self:
        """
        Allow adding Vectors together
        """
        return type(self)(
            self.x + other.x,
            self.y + other.y,
            )

    def __sub__(self, other: Self) -> Self:
        """
        Allow subtracting Vectors
        """
        return type(self)(
            self.x - other.x,
            self.y - other.y,
            )

