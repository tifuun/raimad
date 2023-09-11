"""
Transformable -- enacpsulates transform and exposes its methods
"""

from typing import Self

import PyCIF as pc


#@encapsulation.expose_encapsulated(Transform, 'transform')
class Transformable(object):
    transform: pc.Transform

    def __init__(self):
        self.transform = pc.Transform()
        super().__init__()

    def move(self, x: float | pc.Point = 0, y: float = 0) -> Self:
        self.transform.move(x, y)
        return self

    def movex(self, x: float = 0) -> Self:
        self.transform.movex(x)
        return self

    def movey(self, y: float = 0) -> Self:
        self.transform.movey(y)
        return self

    def scale(self, x: float | pc.Point, y: float | None = None) -> Self:
        self.transform.scale(x, y)
        return self

    def rotate(self, angle: float, x: float | pc.Point = 0, y: float = 0) -> Self:
        self.transform.rotate(angle, x, y)
        return self

    def hflip(self) -> Self:
        self.transform.hflip()
        return self

    def vflip(self) -> Self:
        self.transform.vflip()
        return self

    def flip(self) -> Self:
        self.transform.flip()
        return self

    def apply_transform(self, transform: Self):
        self.transform.apply_transform(transform)
        return self


