import PyCIF as pc

class BoundPoint(pc.Point):
    _transformable: pc.Transformable

    def __init__(self, point: pc.Point, transformable: pc.Transformable):
        super().__init__(*point)
        #self.x, self.y = transformable.transform.transform_point(point)
        self._transformable = transformable

    def to(self, point: pc.Point):
        self._transformable.move(*(point - self))

    def rotate(self, angle: float):
        self._transformable.rotate(angle, self)

class BoundRelativePoint(BoundPoint):
    _transformable: pc.Transformable

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

    def to(self, point: pc.Point):
        self._transformable.move(*(point - self))

    def rotate(self, angle: float):
        self._transformable.rotate(angle, self)


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
