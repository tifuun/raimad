"""
Point -- storage for x, y coordinate pair
"""
from typing import Self

import numpy as np

import PyCIF as pc

class Point(object):
    def __init__(self, x: float = 0, y: float = 0, arg: float | None = None, mag: float | None = None):
        """
        Create a point from (x, y)
        with short syntax: pc.Point(10, 20)
        """
        if arg is not None:
            self.x = np.cos(arg) * mag
            self.y = np.sin(arg) * mag
        else:
            self.x = x
            self.y = y

    # TODO better overloading framework. Should support:
    # pc.Point()  # create an origin
    # pc.Point(10, 10)  # x, y
    # pc.Point(x=10, y=10)  # x, y
    # pc.Point(arg=pc.degrees(45), mag=10)  # polar
    # pc.Point(arg=pc.degrees(45))  # polar, mag is 1

    def __repr__(self):
        return f"Point({self.x:.3f}, {self.y:.3f})"

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

    def __pos__(self):
        return self

    def __neg__(self):
        # TODO neg creates a copy, but pos doesnt. What do?
        # Should makes points immovable?
        return self * -1

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

    #@classmethod
    #def Polar(cls, arg: float, mag: float = 1):
    #    return cls(
    #        np.cos(angle) * magnitude,
    #        np.sin(angle) * magnitude
    #        )

    @property
    def arg(self):
        return np.arctan2(self.y, self.x)

    @property
    def mag(self):
        return np.linalg.norm(self)

    def distance_to(self, other: Self):
        """
        Also see pc.Point.distance_from and pc.distance_between
        """
        return np.linalg.norm(other - self)

    def distance_from(self, other: Self):
        """
        Also see pc.Point.distance_to and pc.distance_between
        """
        return np.linalg.norm(self - other)

    #def apply_transform(self, transform: pc.Transform):
    #    # TODO forms of this are copy-pasted in multiple places.
    #    self.x, self.y, _ = transform.get_matrix().dot(
    #            np.array([self.x, self.y, 1]))
    #    return self

    #def copy(self):
    #    # TODO use python standard copy?
    #    new_point = Point(self.x, self.y)
    #    return new_point

