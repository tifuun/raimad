"""
State -- an interface for what Akira calls "toy train" design.
"""

from PyClewinSDC.Dotdict import Dotdict
from PyClewinSDC.Polygon import Polygon


class State(object):
    """
    Transformation State container
    """
    def __init__(self):
        self.affine_mat = None

    def polygon(self, xyarray):
        return Polygon(self.affine_mat * xyarray)

