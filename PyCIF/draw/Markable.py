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
        return pc.BoundRelativePoint(self._point, obj._transformable)
    
    def __set__(self, obj, value):
        #self._boundpoint = pc.BoundPoint(value, obj._transformable)
        self._point = value

# TODO
# This will eventually be very useful:
# https://stackoverflow.com/questions/3278077/difference-between-getattr-and-getattribute

class Markable(pc.Transformable):
    _marks: dict
    _mark_docstrings: dict

    class Marks():

        _transformable: pc.Transformable

        origin = Mark('Origin of the coordinate system of this Markable')

        def __init__(self, transformable):
            self._transformable = transformable

        def copy(self, new_transformable: pc.Transformable):
            new = type(self)(new_transformable)
            for attr in self.__slots__:
                if attr.startwith('_'): continue


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

    def _add_mark(self, name: str, point, docstring: str | None = None):
        """
        Add a new mark, checking that the name is valid and not already taken.
        IN INTERNAL COORDINATES
        """
        if not name.isidentifier():
            raise Exception(
                f'Mark name `{name}` is not a valid Python identifier'
                )

        if name in self._marks.keys():
            raise Exception(
                f'A mark named `{name}` already exists at point '
                f'{self._marks[name]}'
                )

        #self._marks[name] = PointRef(self, point)
        self._marks[name] = point
        self._mark_docstrings[name] = docstring

        return point

    def _get_mark(self, name):
        """
        Return mark IN INTERNAL COORDINATES
        """
        if name not in self._marks.keys():
            raise Exception(
                f'Object {self} has no mark named `{name}`. '
                f'Did you mean one of these? '
                f'{", ".join(self._marks.keys())}'
                )

        return self._marks[name]

    def get_mark(self, name):
        """
        Return mark IN EXTERNAL COORDINATES
        """
        point = self._get_mark(name)
        return self.transform.transform_point(point)

    def _align_points(self, source_point, target_point):
        """
        Move self such that `source_point`
        (specified in own internal coordinates)
        is at the same position as `target_points`
        (specified in external coordinates)
        """
        source_point_ext = self.transform.transform_point(source_point)
        self.move(*(target_point - source_point_ext))

    def align_mark_to_point(self, source_mark_name: str, target_point):
        """
        Move self such that the mark `source_mark_name`
        is at the same position as `target_point`
        (specified in external coordinates)
        """
        self._align_points(
            self._get_mark(source_mark_name),
            target_point,
            )

        return self

    def align_marks(
            self,
            source_mark_name: str,
            target_markable: Self,
            target_mark_name: str,
            ):
        """
        Move self such that the mark `source_mark_name`
        is at the same position as the mark `target_mark_name`
        of the markable object `target_mark`.
        """
        self.align_mark_to_point(
            source_mark_name,
            target_markable.get_mark(target_mark_name)
            )

        return self

    def rotate_around_point(self,
            point,
            angle,
            ):
        """
        Rotate around a point (in internal coords)
        """
        point_ext = self.transform.transform_point(point)
        self.rotate(angle, *point_ext)

        return self

    def rotate_around_mark(self,
            mark_name: str,
            angle,
            ):
        """
        Rotate around a mark
        """
        self.rotate_around_point(
            self._get_mark(mark_name),
            angle,
            )

        return self

    def snap_below(self, to: Self):
        self.align_marks(
            'top_mid',
            to,
            'bottom_mid',
            )

        return self

    def snap_above(self, to: Self):
        self.align_marks(
            'bottom_mid',
            to,
            'top_mid',
            )
        # TODO helpful error messages if marks are missing
        # Or maybe protocols somehow??

        return self

    def align_to(self, to: Self, mark_name='mid'):
        self.align_marks(
            mark_name,
            to,
            mark_name,
            )

