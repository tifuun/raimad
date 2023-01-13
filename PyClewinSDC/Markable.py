"""
Markable -- interface for adding marks to components

This extends the Alignable class with the ability to add custom
marks that can be used to align the component in the same way as bbox
points can be used
"""

from PyClewinSDC.Alignable import Alignable
from PyClewinSDC.Transform import Transform
from PyClewinSDC.BBox import BBox
from PyClewinSDC.Dotdict import Dotdict
from PyClewinSDC.Point import Point
from PyClewinSDC.PointRef import PointRef


class MarkContainer(object):
    """
    """
    def __init__(self, transform):
        self._transform = transform
        self._marks = {}

    def __getattr__(self, name):
        if name not in self._marks.keys():
            raise Exception("No such mark.")

        point = self._marks[name]
        return point.copy().apply_transform(self._transform)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            return super().__setattr__(name, value)

        if not isinstance(value, Point):
            raise Exception("Can only add Points to MarkContainer")

        self._marks[name] = value



class Markable(Alignable):
    def __init__(
            self,
            transform: Transform | None = None,
            bbox: BBox | None = None,
            ):

        super().__init__(transform=transform, bbox=bbox)
        self.marks = MarkContainer(self.transform)
