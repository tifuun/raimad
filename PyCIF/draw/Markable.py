"""
Markable -- interface for adding named points to components
"""

from typing import Self

from PyCIF.draw.Transformable import Transformable
from PyCIF.draw.Transform import Transform

#@encapsulation.expose_encapsulated(Transform, 'transformable')
#class Mark():
#    """
#    """
#    def __init__(self, transformable):
#        self.transformable = transformable
#
#    def __get__(self, obj: MarkContainer, objtype=None):
#        obj._markable.get_mark(self.name)
#
#    def align(self, target_point):
#        obj._markable.get_mark(self.name)
#
#
#
#
#class MarkContainer(object):
#    """
#    """
#    def __init__(self, markable, transform):
#        self._markable = markable
#        self._transform = transform
#        self._marks = {}
#
#    def __getattr__(self, name):
#        if name not in self._marks.keys():
#            raise Exception("No such mark.")
#
#        point = self._marks[name]
#        return PointRef(self._markable, point.copy().apply_transform(self._transform))
#
#    def __setattr__(self, name, value):
#        if name.startswith('_'):
#            return super().__setattr__(name, value)
#
#        if not isinstance(value, Point):
#            raise Exception("Can only add Points to MarkContainer")
#
#        self._marks[name] = value
#
#    def items(self):
#        return self._marks.items()
#
#    def keys(self):
#        return self._marks.keys()
#
#    def values(self):
#        return self._marks.values()


class Markable(Transformable):
    _marks: dict
    _mark_docstrings: dict

    def __init__(self):
        super().__init__()
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

