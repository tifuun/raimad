"""
Markable -- interface for adding marks to components

This extends the Alignable class with the ability to add custom
marks that can be used to align the component in the same way as bbox
points can be used
"""

from PyClewinSDC.Alignable import Alignable
from PyClewinSDC.Transform import Transform
from PyClewinSDC.BBox import BBox


class Markable(Alignable):
    def __init__(
            self,
            transform: Transform | None = None,
            bbox: BBox | None = None,
            ):

        super().__init__(self, transform=transform, bbox=bbox)

    def add_mark(self, name, point: Point):
        pass

