"""
Point -- storage for x, y coordinate pair
"""
from typing import Self

import numpy as np

import PyCIF as pc

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
            self.x + other[0],
            self.y + other[1],
            )

    def __sub__(self, other):
        """
        Allow subtractin CoordPairs
        """
        return Point(
            self.x - other[0],
            self.y - other[1],
            )

    def __truediv__(self, other: Self | int | float):
        if isinstance(other, type(self)):
            return Point(
                self.x / other[0],
                self.y / other[1]
                )

        elif isinstance(other, float | int):
            return Point(
                self.x / other,
                self.y / other
                )

        raise Exception("idk wtf to do with this")


    def __getitem__(self, index):
        if index == 0:
            return self.x

        if index == 1:
            return self.y

        raise Exception("Points consist of only two coordinates")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value

        elif index == 1:
            self.y == value

        else:
            raise Exception("Points consist of only two coordinates")

    def move(self, x, y):
        self.x += x
        self.y += y
        return self

    def __array__(self):
        return np.array((self.x, self.y))

    #def apply_transform(self, transform: pc.Transform):
    #    # TODO forms of this are copy-pasted in multiple places.
    #    self.x, self.y, _ = transform.get_matrix().dot(
    #            np.array([self.x, self.y, 1]))
    #    return self

    #def copy(self):
    #    # TODO use python standard copy?
    #    new_point = Point(self.x, self.y)
    #    return new_point

