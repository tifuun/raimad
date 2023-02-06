"""
PointRef -- reference to a point and a transformable
"""

from PyCIF.draw.Point import Point
#from PyCIF.draw.Alignable import Alignable
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

    def alignx(self, to: Point):
        """
        """
        # TODO overloading thing so asterisk is not needed
        self.alignable.movex((to - self).x)
        return self.alignable

    def aligny(self, to: Point):
        """
        """
        # TODO overloading thing so asterisk is not needed
        self.alignable.movey((to - self).y)
        return self.alignable

