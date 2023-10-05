"""Point.py: contains Point class."""

from typing import Self
from copy import copy

import numpy as np

import PyCIF as pc

class Point(object, metaclass=pc.SlotsFromAnnotationsMeta):
    """Point: Storage for XY coordinate pairs."""

    x: float
    y: float

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            arg: float | None = None,
            mag: float | None = None
            ):
        """
        Create a point from (x, y) or (argument, magnitude).

        So, ethier Point(x, y)
        or Point(arg=theta, mag=r)
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

    def __repr__(self) -> str:
        """Get representation of point in cartesian coordinate system."""
        return f"Point({self.x:.3f}, {self.y:.3f})"

    def __iter__(self) -> iter:
        """
        Get [x, y] as iter object.

        This is mainly useful for unpacking a point or converting it
        to lists / arrays.
        """
        return iter((self.x, self.y))

    def __add__(self, other) -> Self:
        """Allow adding Points together."""
        new = self.copy()
        new.x += other[0]
        new.y += other[1]
        return new

    def __sub__(self, other) -> Self:
        """Allow subtracting Points."""
        new = self.copy()
        new.x -= other[0]
        new.y -= other[1]
        return new

    def __rsub__(self, other) -> Self:
        """Allow subtracting Points."""
        new = self.copy()
        new.x = other[0] - self.x
        new.y = other[1] - self.y
        return new

    def __pos__(self) -> Self:
        """Allow prefixing points with `+`. Does nothing."""
        return self

    def __neg__(self) -> Self:
        """
        Allow prefixing points with `-`.

        Creates a copy of self with inverted X and Y.
        """
        # TODO neg creates a copy, but pos doesnt. What do?
        # Should makes points immovable?
        return self * -1

    def __truediv__(self, other: Self | int | float) -> Self:
        """Allow diving point by scalar or another point."""
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

    def __getitem__(self, index) -> float:
        """Allow getting X and Y through indexing."""
        if index == 0:
            return self.x

        if index == 1:
            return self.y

        raise Exception("Points consist of only two coordinates")

    def __array__(self, dtype=None) -> np.ndarray:
        """Cast self to array."""
        return np.array((self.x, self.y), dtype=dtype)

    def __eq__(self, other) -> bool:
        """Check if two Point objects have the same coordinates."""
        return self.distance_to(other) < 0.001  # TODO delta

    @property
    def arg(self):
        """Get argument."""
        return np.arctan2(self.y, self.x)

    @property
    def mag(self):
        """Get magnitude (modulo)."""
        return np.linalg.norm(self)

    # TODO typing this accepts not only Self but also arrays, etc.
    def distance_to(self, other: Self) -> float:
        """
        Calculate distance to other point using Pythagoras' theorem.

        Parameters
        ----------
        other: Self
            Point to calculate distance to.

        See Also
        --------
        Point.distance_from
        pc.distance_between
        """
        return np.linalg.norm(other - self)

    def distance_from(self, other: Self) -> float:
        """
        Calculate distance from other point using Pythagoras' theorem.

        Parameters
        ----------
        other: Self
            Point to calculate distance from.

        See Also
        --------
        Point.distance_to
        pc.distance_between
        """
        return np.linalg.norm(self - other)

    def copy(self):
        # TODO???
        return copy(self)

    def canonical(self):
        # TODO???
        return self.copy()

