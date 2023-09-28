"""
Markable -- interface for adding named points to components
"""

from copy import copy

from typing import Self, Annotated, Tuple, Mapping

import PyCIF as pc

class Mark(metaclass=pc.SlotsFromAnnotationsMeta):
    # TODO static access
    #_boundpoint: pc.BoundPoint | None
    description: str
    name: str

    def __init__(self, description: str = ''):
        self.description = description
        #self._boundpoint = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, cls=None):
        #return self._boundpoint
        point = obj._mark_values[self.name]
        x, y = obj._transformable.transform.transform_point(point)
        return pc.BoundPoint(x, y, obj._transformable)
    
    def __set__(self, obj, value):
        #self._boundpoint = pc.BoundPoint(*value, obj._transformable)
        if self.name in obj._mark_values.keys():
            log.warning(
                f"Mark {self} of Markable {obj}\n"
                f"got changed from {obj._mark_values[self]}\n"
                f"to {self}"
                )
        obj._mark_values[self.name] = value

# TODO
# This will eventually be very useful:
# https://stackoverflow.com/questions/3278077/difference-between-getattr-and-getattribute
# TODO wait I think I pasted the wrong link when I wrote the previous TODO

class Markable(pc.Transformable):

    class Marks():

        _transformable: pc.Transformable
        _mark_values: Mapping[str, pc.Point]

        origin = Mark('Origin of the coordinate system of this Markable')

        def __init__(self, transformable):
            self._transformable = transformable
            self._mark_values = {}

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


