"""
Polygon -- a method for prepresenting geometry
that can be exported to cif
"""

from copy import deepcopy

import PyCIF as pc

class Polygon(pc.Markable, pc.BBoxable):
    """
    Polygon.
    Inheritrs from Transformable, so you can transform it.
    """
    def __init__(self):
        """
        """
        super().__init__()
        self._xyarray = None

    def __repr__(self):
        return (
            f'<Polygon {type(self).__name__} '
            f'with {str(self.transform)}>'
            )

    def copy(self):
        """
        Return a copy of this polygon
        """
        return deepcopy(self)

