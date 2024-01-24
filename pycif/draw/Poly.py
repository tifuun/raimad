"""
Poly -- a method for prepresenting geometry
that can be exported to cif
"""

from io import StringIO

from copy import deepcopy

import pycif as pc

class Poly(pc.Markable, pc.BBoxable):
    """
    Poly.
    Inheritrs from Transformable, so you can transform it.
    """
    def __init__(self):
        """
        """
        super().__init__()
        self._xyarray = None

    def __repr__(self):
        return (
            f'<Poly {type(self).__name__} '
            f'with {str(self.transform)}>'
            )

    def copy(self):
        """
        Return a copy of this poly
        """
        return deepcopy(self)

    def _repr_svg_(self):
        """IPython/Jupyter integration: show poly as svg."""

        # TODO this is very hacky!
        class WrapperCompo(pc.Compo):
            class Layers(pc.Compo.Layers):
                root = pc.Layer()

            def _make(c_self):
                c_self.add_subpoly(self)

        return pc.export_svg(WrapperCompo())


