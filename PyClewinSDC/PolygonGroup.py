"""
Polygon group -- used for grouping polygons together for transformations
"""

from PyClewinSDC.Transformable import Transformable
from PyClewinSDC.BBox import BBox


class PolygonGroup(Transformable):
    def __init__(self, *args, transform=None, bbox=None):
        super().__init__(transform)
        self.polygons = args

        if bbox:
            self._bbox = bbox.copy()
        else:
            self._bbox = BBox()
            for poly in args:
                self._bbox.add_xyarray(poly.get_xyarray())

    def get_polygons(self):
        return [
            polygon.copy().apply_transform(self.transform)
            for polygon
            in self.polygons
            ]

    @property
    def bbox(self):
        # TODO caching
        return self._bbox.copy().apply_transform(self.transform)

    def copy(self):
        return PolygonGroup(
            *[polygon.copy() for polygon in self.polygons],
            transform=self.transform
            )

