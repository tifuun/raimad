"""
Markable -- interface for adding named points to components
"""

from copy import copy

from typing import Self, Annotated, Tuple

import PyCIF as pc

class Mark(metaclass=pc.SlotsFromAnnotationsMeta):
    # TODO static access
    _point: pc.Point | None
    #_boundpoint: pc.Point | None
    description: str

    def __init__(self, description: str):
        self.description = description
        self._point = None
        #self._boundpoint = None

    def __get__(self, obj, cls=None):
        #return self._boundpoint
        return pc.BoundRelativePoint(*self._point, obj._transformable)
    
    def __set__(self, obj, value):
        #self._boundpoint = pc.BoundPoint(value, obj._transformable)
        self._point = value

# TODO
# This will eventually be very useful:
# https://stackoverflow.com/questions/3278077/difference-between-getattr-and-getattribute

class Markable(pc.Transformable):

    class Marks():

        _transformable: pc.Transformable

        origin = Mark('Origin of the coordinate system of this Markable')

        def __init__(self, transformable):
            self._transformable = transformable

        #def _copy(self, new_transformable: pc.Transformable):
        #    new = type(self)(new_transformable)
        #    for attr in self.__slots__:
        #        if attr.startwith('_'): continue
        #    return new

    marks: Marks

    def __init__(self):
        super().__init__()

        if not issubclass(self.Marks, Markable.Marks):
            raise Exception(
                """`Marks` class must inherit from Markable.Marks"""
                )

        self.marks = self.Marks(self)

        self.marks.origin = pc.Point(0, 0)

        self._marks = {}
        self._mark_docstrings = {}


