"""
Poly group -- used for grouping polys together for transformations
"""

import numpy as np

import pycif as pc

class Group(pc.BBoxable):
    def __init__(self, *polys):
        super().__init__()
        self.polys = polys

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

    def get_polys(self):
        return self.polys

