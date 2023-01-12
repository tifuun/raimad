"""
PointRef -- reference to a point and a transformable
"""

from typing import Self

from PyClewinSDC.Point import Point
#from PyClewinSDC.Alignable import Alignable
# TODO correct type annotation requires circular import


class PointRef(object):
    def __init__(self, alignable, point: Point):
        self.alignable = alignable
        self.point = point

    def align(self, to: Point | Self):
        """
        Align the referenced transformable such that the referenced point is
        matched with the target point (or PointRef)
        """
        # TODO overloading thing so asterisk is not needed
        self.alignable.move(*(to - self.point))
        return self.alignable

    # TODO type annotations

    def __iter__(self):
        return self.point.__iter__

    def __add__(self, other):
        return self.point.__add__(other)

    def __sub__(self, other):
        return self.point.__sub__(other)
