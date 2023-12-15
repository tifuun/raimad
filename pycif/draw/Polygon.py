"""
Polygon -- a method for prepresenting geometry
that can be exported to cif
"""

from io import StringIO

from copy import deepcopy

import pycif as pc

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

    def _repr_svg_(self):
        """IPython/Jupyter integration: show polygon as svg."""

        # TODO this is very hacky!
        class WrapperComponent(pc.Component):
            class Layers(pc.Component.Layers):
                root = pc.Layer()

            def _make(c_self):
                c_self.add_subpolygon(self)

        return pc.export_svg(WrapperComponent())


