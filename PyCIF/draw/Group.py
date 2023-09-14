"""
Polygon group -- used for grouping polygons together for transformations
"""

import numpy as np

import PyCIF as pc

class Group(pc.Transformable, pc.BBoxable):
    def __init__(self, *polygons):
        super().__init__()
        self.polys = polygons

        #if bbox is None:
        #    for poly in polygons:
        #        self._bbox.add_xyarray(poly.get_xyarray())

    def apply(self):
        for poly in self.polys:
            poly.apply_transform(self.transform)
        self.transform.reset()

    def _get_xyarray(self):
        xyarray = []
        for poly in self.polys:
            # TODO slow
            xyarray.extend(poly.get_xyarray())
        return np.array(xyarray)

    def get_polygons(self):
        return self.polys

    #def get_polygons(self):
    #    return [
    #        polygon.copy().apply_transform(self.transform)
    #        for polygon
    #        in self.polygons
    #        ]

    #def apply(self):
    #    for poly in self.polygons:
    #        poly.apply_transform(self.transform)
    #    return self

    #def copy(self):
    #    return PolygonGroup(
    #        *[polygon.copy() for polygon in self.polygons],
    #        transform=self.transform
    #        )

    #def get_bbox(self):
    #    # TODO TODO TODO we need actual bbox system
    #    return BBox([
    #        point
    #        for poly in self.get_polygons()
    #        for point in np.reshape(poly.get_bbox(), [2, 2])
    #        ])
    #    # TODO would be much faster to first compute bbox then transform


