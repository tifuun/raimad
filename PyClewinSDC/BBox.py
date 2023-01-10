"""
BBox -- bounding box
"""

import numpy as np

from dataclasses import dataclass

from PyClewinSDC.Transform import Transform


@dataclass
class CoordPair(object):
    x: float = 0
    y: float = 0

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
        return CoordPair(
            self.x + other.x,
            self.y + other.y,
            )

    def __sub__(self, other):
        """
        Allow subtractin CoordPairs
        """
        return CoordPair(
            self.x - other.x,
            self.y - other.y,
            )


class BBox(object):
    def __init__(self, xyarray=None):
        self.max_x = float('-inf')
        self.max_y = float('-inf')
        self.min_x = float('inf')
        self.min_y = float('inf')

        if xyarray is not None:
            self.add_xyarray(xyarray)
            assert self.is_valid()

    def is_valid(self):
        return (
            self.max_x != float('-inf') and
            self.max_y != float('-inf') and
            self.min_x != float('inf') and
            self.min_y != float('inf')
            )

    def apply_transform(self, transform: Transform):
        assert self.is_valid()
        (self.min_x, self.min_y), (self.max_x, self.max_y) = [
        #AAAA = [
            (transform.get_matrix().dot(np.append(point, 1)))[:2]
            for point
            in ((self.min_x, self.min_y), (self.max_x, self.max_y))
            ]
        return self

    def copy(self):
        # TODO read up on how to properly do copies
        # in Python
        new_bbox = BBox()
        new_bbox.max_x = self.max_x
        new_bbox.max_y = self.max_y
        new_bbox.min_x = self.min_x
        new_bbox.min_y = self.min_y
        return new_bbox

    def add_xyarray(self, xyarray):
        """
        Process a new xyarray and update the
        bounding box accordingly.
        """
        for point in xyarray:
            if point[0] > self.max_x:
                self.max_x = point[0]
            elif point[0] < self.min_x:
                self.min_x = point[0]

            if point[1] > self.max_y:
                self.max_y = point[1]
            elif point[1] < self.min_y:
                self.min_y = point[1]

    @property
    def width(self):
        assert self.is_valid()
        return self.max_x - self.min_x

    @property
    def height(self):
        assert self.is_valid()
        return self.max_y - self.min_y

    @property
    def left(self):
        assert self.is_valid()
        return self.min_x

    @property
    def top(self):
        assert self.is_valid()
        return self.min_y

    @property
    def right(self):
        assert self.is_valid()
        return self.max_x

    @property
    def bottom(self):
        assert self.is_valid()
        return self.max_y

    def interpolate(self, x_ratio, y_ratio):
        """
        Find a point inside the bounding box
        given ratios between min_x -- max_x,
        and min_y -- max_y.
        So, for example, 0,0 is top left,
        1,1 is bottom right, 0.5,0.5 is center,
        and 0.5,1 is bottom middle.
        """
        return CoordPair(
            self.min_x + self.width * x_ratio,
            self.min_y + self.height * y_ratio,
            )

    @property
    def center(self):
        assert self.is_valid()
        return self.interpolate(0.5, 0.5)

    @property
    def top_mid(self):
        assert self.is_valid()
        return self.interpolate(0.5, 0)

    @property
    def bot_mid(self):
        assert self.is_valid()
        return self.interpolate(0.5, 1)

    @property
    def left_mid(self):
        assert self.is_valid()
        return self.interpolate(0, 0.5)

    @property
    def right_mid(self):
        assert self.is_valid()
        return self.interpolate(1, 0.5)

    @property
    def top_left(self):
        assert self.is_valid()
        return self.interpolate(0, 0)

    @property
    def top_right(self):
        assert self.is_valid()
        return self.interpolate(1, 0)

    @property
    def bot_left(self):
        assert self.is_valid()
        return self.interpolate(0, 1)

    @property
    def bot_right(self):
        assert self.is_valid()
        return self.interpolate(1, 1)

