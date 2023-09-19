from typing import Self

import PyCIF as pc

log = pc.get_logger(__name__)

class BoundPoint(pc.Point):
    _transformable: pc.Transformable

    def __init__(self, x: float, y: float, transformable: pc.Transformable):
        super().__init__(x, y)
        #self.x, self.y = transformable.transform.transform_point(point)
        self._transformable = transformable

    def canonical(self):
        return pc.Point(*self)

    def __add__(self, other):
        """
        Allow adding CoordPairs together
        """
        new = self.copy()
        x = self.x + other[0]
        y = self.y + other[1]
        x, y = self._transformable.transform.copy().inverse().transform_point((x, y))
        new._x = x
        new._y = y
        #new._x -= other[0]
        #new._y -= other[1]
        return new

    def __sub__(self, other):
        """
        Allow subtractin CoordPairs
        """
        new = self.copy()
        x = self.x - other[0]
        y = self.y - other[1]
        x, y = self._transformable.transform.copy().inverse().transform_point((x, y))
        new._x = x
        new._y = y
        #new._x -= other[0]
        #new._y -= other[1]
        return new

    def __rsub__(self, other):
        """
        Allow subtractin CoordPairs
        """
        new = self.copy()
        x = other[0] - self.x
        y = other[1] - self.y
        x, y = self._transformable.transform.copy().inverse().transform_point((x, y))
        new._x = x
        new._y = y
        #new._x = other[0] - self._x
        #new._y = other[1] - self._y
        return new

    def to(self, point: pc.Point):
        #vec = point - self
        #px, py = self._transformable.transform.copy().inverse().transform_point(point)
        # TODO wtf is going on here?
        px, py = point
        x = px - self._x
        y = py - self._y
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

class BoundRelativePoint(BoundPoint):
    @property
    def x(self):
        x, y = self._transformable.transform.transform_point(
            (self._x, self._y)
            )
        return x

    @property
    def y(self):
        x, y = self._transformable.transform.transform_point(
            (self._x, self._y)
            )
        return y



#class BoundPoint(pc.Point):
#    _transformable: pc.Transformable
#
#    def __init__(self, point: pc.Point, transformable: pc.Transformable):
#        self.x, self.y = transformable.transform.transform_point(point)
#        self._transformable = transformable
#
#    def to(self, point: pc.Point):
#        self._transformable.move(*(point - self))
#
#    def rotate(self, angle: float):
#        self._transformable.rotate(angle, self)
#
#    #TODO chaining won't work, b/c x and y don't get re-calculated.
#    # Would it be better to have x and y as properties?
#    # Or similar to bbox, so like actual Marks container is private,
#    # and public version is a property that returns 'transformed'
#    # container?
#
#    #def move(self, x: float | pc.Point = 0, y: float = 0) -> Self:
#    #    self._transformable.move(x, y)
#    #    return self
#
#    #def movex(self, x: float = 0) -> Self:
#    #    self._transformable.movex(x)
#    #    return self
#
#    #def movey(self, y: float = 0) -> Self:
#    #    self._transformable.movey(y)
#    #    return self
#
#    #def scale(self, x: float | pc.Point, y: float | None = None) -> Self:
#    #    self._transformable.scale(x, y)
#    #    return self
#
#    #def rotate(self, angle: float, x: float | pc.Point = 0, y: float = 0) -> Self:
#    #    self._transformable.rotate(angle, x, y)
#    #    return self
#
#    #def hflip(self) -> Self:
#    #    self._transformable.hflip()
#    #    return self
#
#    #def vflip(self) -> Self:
#    #    self._transformable.vflip()
#    #    return self
#
#    #def flip(self) -> Self:
#    #    self._transformable.flip()
#    #    return self
