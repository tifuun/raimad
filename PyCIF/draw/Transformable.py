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

    def scale(
            self,
            x: float | pc.Point,  # TODO typing.point
            y: float | None = None,
            cx: float = 0,
            cy: float = 0,
            ) -> Self:

        self.transform.scale(x, y, cx, cy)
        return self

    def rotate(self, angle: float, x: float | pc.Point = 0, y: float = 0) -> Self:
        self.transform.rotate(angle, x, y)
        return self

    def hflip(self, y: float = 0) -> Self:
        self.transform.hflip(y)
        return self

    def vflip(self, x: float = 0) -> Self:
        self.transform.vflip(x)
        return self

    def flip(self, x: float = 0, y: float = 0) -> Self:
        self.transform.flip(x, y)
        return self

    def apply_transform(self, transform: pc.Transform) -> Self:
        self.transform.apply_transform(transform)
        return self


