"""
Polygon group -- used for grouping polygons together for transformations
"""

from PyClewinSDC.Transformable import Transformable


class PolygonGroup(Transformable):
    def __init__(self, *args, transform=None):
        super().__init__(transform)
        self.polygons = args

    def get_polygons(self):
        return [
            polygon.copy().apply_transform(self.transform)
            for polygon
            in self.polygons
            ]

    def copy(self):
        return PolygonGroup(
            *[polygon.copy() for polygon in self.polygons],
            transform=self.transform
            )

