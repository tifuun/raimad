"""
PointRef -- reference to a point and a transformable
"""

from PyClewinSDC.Point import Point
#from PyClewinSDC.Alignable import Alignable
# TODO correct type annotation requires circular import


class PointRef(Point):
    def __init__(self, alignable, point: Point):
        self.x = point.x
        self.y = point.y
        self.alignable = alignable

    def align(self, to: Point):
        """
        Align the referenced transformable such that the referenced point is
        matched with the target point (or PointRef)
        """
        # TODO overloading thing so asterisk is not needed
        self.alignable.move(*(to - self))
        return self.alignable

