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


class Markable(Alignable):
    def __init__(
            self,
            transform: Transform | None = None,
            bbox: BBox | None = None,
            ):

        super().__init__(transform=transform, bbox=bbox)
        self.marks = Dotdict()

    def add_mark(self, name: str, point: Point):
        """
        Add point
        """
        ref = PointRef(self, point)
        self.marks[name] = ref

    def get_mark(self, name):
        """
        Retrieve point and apply transform
        """
        return self.marks[name].copy().apply_transform(self.transform)

