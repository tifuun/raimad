"""
Polygon group -- used for grouping polygons together for transformations
"""

import numpy as np

import PyCIF as pc

class Group(pc.Transformable, pc.BBoxable):
    def __init__(self, *polygons):
        super().__init__()
        self.polys = polygons

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

