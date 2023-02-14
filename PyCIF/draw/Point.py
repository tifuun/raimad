"""
Point -- storage for x, y coordinate pair
"""

from typing import Self

import numpy as np

from PyCIF.draw.Transform import Transform

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

    def move_polar(self, distance, radians):
        self.x += np.cos(radians) * distance
        self.y += np.sin(radians) * distance
        return self

    def apply_transform(self, transform: Transform):
        # TODO forms of this are copy-pasted in multiple places.
        self.x, self.y, _ = transform.get_matrix().dot(
            np.array([self.x, self.y, 1]))
        return self

    def copy(self):
        # TODO use python standard copy?
        return Point(self.x, self.y)

    def distance_to(self, other: Self) -> float:
        """
        Get the distance between two points.
        returns the absolute distance between this point and `other` point.
        """
        return np.linalg.norm(
            (self.x, self.y),
            (other.x, other.y),
            )

    def radians_to(self, other: Self) -> float:
        """
        Get angle between two points.
        Return the angle, in radians, formed between the vertical and the
        line connecting this point and `other` point.
        The angle is measured from the right.
        """
        a = np.arctan2(
            (other.x - self.x),
            (other.y - self.y),
            )
        while a < 0:
            a += 2 * np.pi
        print(a / np.pi)
        return a

