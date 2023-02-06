"""
Point -- storage for x, y coordinate pair
"""

import numpy as np

from PyCIF.Transform import Transform

class Point(object):
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __iter__(self):
        """
        Iterator method allows unpacking
        a CoordPair into [x, y]
        """
        return iter((self.x, self.y))

    def __add__(self, other):
        """
        Allow adding CoordPairs together
        """
        return Point(
            self.x + other.x,
            self.y + other.y,
            )

    def __sub__(self, other):
        """
        Allow subtractin CoordPairs
        """
        return Point(
            self.x - other.x,
            self.y - other.y,
            )

    def move(self, x, y):
        self.x += x
        self.y += y
        return self

    def apply_transform(self, transform: Transform):
        # TODO forms of this are copy-pasted in multiple places.
        self.x, self.y, _ = transform.get_matrix().dot(
                np.array([self.x, self.y, 1]))
        return self

    def copy(self):
        # TODO use python standard copy?
        new_point = Point(self.x, self.y)
        return new_point

