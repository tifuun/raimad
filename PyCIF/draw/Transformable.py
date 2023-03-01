"""
Transformable -- enacpsulates transform and exposes its methods
"""

from typing import Self

from PyCIF.draw.Transform import Transform
from PyCIF.draw.PointRef import PointRef
from PyCIF.helpers import encapsulation


@encapsulation.expose_encapsulated(Transform, 'transform')
class Transformable(object):
    transform: Transform

    def __init__(self):
        self.transform = Transform()
        super().__init__()

