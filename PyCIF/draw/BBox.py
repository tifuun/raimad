"""
BBox -- bounding box
"""

import numpy as np

import PyCIF as pc

# Disable to use computer-style Y axis (increases downwards)
MATHEMATIC_Y_AXIS = True


class BBox(object):
    def __init__(self, xyarray=None, bind_to: pc.Transformable | None = None):
        self.max_x = float('-inf')
        self.max_y = float('-inf')
        self.min_x = float('inf')
        self.min_y = float('inf')
        self.bind_to = bind_to

        if bind_to is not None:
            xyarray = bind_to.transform.transform_xyarray(xyarray)

        if xyarray is not None:
            self.add_xyarray(xyarray)
            assert self.is_valid()

    def as_list(self):
        return [self.min_x, self.min_y, self.max_x, self.max_y]

    def __array__(self):
        return np.array(self.as_list())

    def __iter__(self):
        return iter(self.as_list())

    def is_valid(self):
        return (
            self.max_x != float('-inf') and
            self.max_y != float('-inf') and
            self.min_x != float('inf') and
            self.min_y != float('inf')
            )

    #def copy(self):
    #    # TODO read up on how to properly do copies
    #    # in Python
    #    new_bbox = BBox()
    #    new_bbox.max_x = self.max_x
    #    new_bbox.max_y = self.max_y
    #    new_bbox.min_x = self.min_x
    #    new_bbox.min_y = self.min_y
    #    return new_bbox

    def add_xyarray(self, xyarray):
        """
        Process a new xyarray and update the
        bounding box accordingly.
        """
        for point in xyarray:
            self.add_point(point)

    def add_point(self, point):
        # TODO simplify with ELIFs?
        if point[0] > self.max_x:
            self.max_x = point[0]
        if point[0] < self.min_x:
            self.min_x = point[0]

        if point[1] > self.max_y:
            self.max_y = point[1]
        if point[1] < self.min_y:
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
        return self.max_y if MATHEMATIC_Y_AXIS else self.min_y

    @property
    def right(self):
        assert self.is_valid()
        return self.max_x

    @property
    def bottom(self):
        assert self.is_valid()
        return self.min_y if MATHEMATIC_Y_AXIS else self.max_y

    def interpolate(self, x_ratio, y_ratio):
        """
        Find a point inside the bounding box
        given ratios between min_x -- max_x,
        and min_y -- max_y.
        So, for example, 0,0 is top left,
        1,1 is bottom right, 0.5,0.5 is center,
        and 0.5,1 is bottom middle.
        """
        x = self.min_x + self.width * x_ratio
        y = self.min_y + self.height * y_ratio
        point = pc.Point(x, y)

        if self.bind_to is None:
            return point
        else:
            return pc.BoundPoint(point, self.bind_to)

    @property
    def mid(self):
        assert self.is_valid()
        return self.interpolate(0.5, 0.5)

    @property
    def top_mid(self):
        assert self.is_valid()
        return self.interpolate(0.5, MATHEMATIC_Y_AXIS)

    @property
    def bot_mid(self):
        assert self.is_valid()
        return self.interpolate(0.5, not MATHEMATIC_Y_AXIS)

    @property
    def mid_left(self):
        assert self.is_valid()
        return self.interpolate(0, 0.5)

    @property
    def mid_right(self):
        assert self.is_valid()
        return self.interpolate(1, 0.5)

    @property
    def top_left(self):
        assert self.is_valid()
        return self.interpolate(0, MATHEMATIC_Y_AXIS)

    @property
    def top_right(self):
        assert self.is_valid()
        return self.interpolate(1, MATHEMATIC_Y_AXIS)

    @property
    def bot_left(self):
        assert self.is_valid()
        return self.interpolate(0, not MATHEMATIC_Y_AXIS)

    @property
    def bot_right(self):
        assert self.is_valid()
        return self.interpolate(1, not MATHEMATIC_Y_AXIS)

