from typing import Self

import PyCIF as pc

log = pc.get_logger(__name__)

class BoundPoint(pc.Point):
    _transformable: pc.Transformable

    def __init__(self, x: float, y: float, transformable: pc.Transformable):
        super().__init__(x, y)
        #self.x, self.y = transformable.transform.transform_point((x, y))
        self._transformable = transformable

    def to(self, point: pc.Point):
        #vec = point - self
        #px, py = self._transformable.transform.copy().inverse().transform_point(point)
        # TODO wtf is going on here?
        px, py = point
        x = px - self.x
        y = py - self.y
        #self._transformable.move(vec.x, vec.y)
        log.debug('Move %s: %s, %s', self._transformable, point, self)
        self._transformable.move(x, y)
        return self._transformable

    def rotate(self, angle: float):
        self._transformable.rotate(angle, self)
        return self._transformable

    def scale(
            self,
            x: float | pc.Point,  # TODO typing.point
            y: float | None = None,
            ) -> Self:

        self._transformable.scale(x, y, self.x, self.y)
        return self._transformable

    def hflip(self) -> Self:
        self._transformable.hflip(self.y)
        return self

    def vflip(self) -> Self:
        self._transformable.vflip(self.x)
        return self

    def flip(self) -> Self:
        self._transformable.flip(self.x, self.y)
        return self


