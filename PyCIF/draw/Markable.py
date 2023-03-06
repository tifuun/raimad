"""
Markable -- interface for adding named points to components
"""

from typing import Self

from PyCIF.draw.Transformable import Transformable
from PyCIF.draw.Transform import Transform
from PyCIF.draw.Point import Point
from PyCIF.draw.PointRef import PointRef


class Markable(Transformable):
    _marks: dict
    _mark_docstrings: dict

    def __init__(self):
        super().__init__()
        self._marks = {}
        self._mark_docstrings = {}

    def _add_mark(self, name: str, point: Point, docstring: str | None = None):
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

        self._marks[name] = PointRef(self, point)
        self._mark_docstrings[name] = docstring

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

    def _align_points(self, source_point: Point, target_point: Point):
        """
        Move self such that `source_point`
        (specified in own internal coordinates)
        is at the same position as `target_points`
        (specified in external coordinates)
        """
        source_point_ext = self.transform.transform_point(source_point)
        self.move(
            target_point.x - source_point_ext.x,
            target_point.y - source_point_ext.y,
            )

    def align_mark_to_point(self, source_mark_name: str, target_point: Point):
        """
        Move self such that the mark `source_mark_name`
        is at the same position as `target_point`
        (specified in external coordinates)
        """
        self._align_points(
            self._get_mark(source_mark_name),
            target_point,
            )

    def align_marks(self,
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

    def rotate_around_point(self,
            point: Point,
            angle,
            ):
        """
        Rotate around a point (in internal coords)
        """
        point_ext = self.transform.transform_point(point)
        self.rotate(angle, point_ext.x, point_ext.y)

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

