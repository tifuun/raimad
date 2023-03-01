"""
Polygon group -- used for grouping polygons together for transformations
"""

from PyCIF.draw.Transformable import Transformable


class PolygonGroup(Transformable):
    def __init__(self, *args, transform=None, bbox=None):
        super().__init__(transform=transform, bbox=bbox)
        self.polygons = args

        if bbox is None:
            for poly in args:
                self._bbox.add_xyarray(poly.get_xyarray())

    def get_polygons(self):
        return [
            polygon.copy().apply_transform(self.transform)
            for polygon
            in self.polygons
            ]

    def apply(self):
        for poly in self.polygons:
            poly.apply_transform(self.transform)
        return self

    def copy(self):
        return PolygonGroup(
            *[polygon.copy() for polygon in self.polygons],
            transform=self.transform
            )


