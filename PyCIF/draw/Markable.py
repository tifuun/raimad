"""
Markable -- interface for adding named points to components
"""

from copy import copy

from typing import Self, Annotated, Tuple

import PyCIF as pc


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

#def Mark(comment: str):
#    return Annotated[pc.Point, comment]

class BoundPoint(pc.Point):
    _transformable: pc.Transformable

    def __init__(self, point: pc.Point, transformable: pc.Transformable):
        self.x, self.y = transformable.transform.transform_point(point)
        self._transformable = transformable

    def to(self, point: pc.Point):
        self._transformable.move(*(point - self))

    def rotate(self, angle: float):
        self._transformable.rotate(angle, self)

    #TODO chaining won't work, b/c x and y don't get re-calculated.
    # Would it be better to have x and y as properties?
    #
    # but have X and Y as properties?

    #def move(self, x: float | pc.Point = 0, y: float = 0) -> Self:
    #    self._transformable.move(x, y)
    #    return self

    #def movex(self, x: float = 0) -> Self:
    #    self._transformable.movex(x)
    #    return self

    #def movey(self, y: float = 0) -> Self:
    #    self._transformable.movey(y)
    #    return self

    #def scale(self, x: float | pc.Point, y: float | None = None) -> Self:
    #    self._transformable.scale(x, y)
    #    return self

    #def rotate(self, angle: float, x: float | pc.Point = 0, y: float = 0) -> Self:
    #    self._transformable.rotate(angle, x, y)
    #    return self

    #def hflip(self) -> Self:
    #    self._transformable.hflip()
    #    return self

    #def vflip(self) -> Self:
    #    self._transformable.vflip()
    #    return self

    #def flip(self) -> Self:
    #    self._transformable.flip()
    #    return self



class Mark(metaclass=pc.SlotsFromAnnotationsMeta):
    # TODO static access
    _point: pc.Point | None
    description: str

    def __init__(self, description: str):
        self.description = description
        self._point = None

    def __get__(self, obj, cls=None):
        #return self._boundpoint
        return BoundPoint(self._point, obj._transformable)
    
    def __set__(self, obj, value):
        #self._boundpoint = BoundPoint(value, obj._transformable)
        self._point = value


#class Mark(pc.Point):
#    _transformable: pc.Transformable
#
#    def __init__(self, x: float, y: float, transformable: pc.Transformable):
#        super().__init__(x, y)
#        self._transformable = transformable
#        #self.wtf = 'wtf'
#
#    #def __get__(self, instance, cls):
#    #    if not instance:
#    #        raise Exception("wtf")
#
#    #    return instance._transformable.transform.transform_point(self)
#    #
#    #def __set__(self, instance, point):
#    #    if not instance:
#    #        raise Exception("wtf")
#
#    #    self.x = point.x
#    #    self.y = point.y
#
#    def __class_getitem__(cls, comment: str):
#        return Annotated[pc.Point, comment]
#
#    def move(self, x: float = 0, y: float = 0) -> Self:
#        self._transformable.move(x, y)
#        return self
#
#    def to(self, point: pc.Point) -> Self:
#        self._transformable.move(*(point - self))
#        return self

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

    marks: Marks

    #class Marks(metaclass=pc.SlotsFromAnnotationsMeta):

    #    _transform: pc.Transform
    #    origin: Mark['Origin of the coordinate system of this Markable']

    #    def __iter__(self):
    #        return iter(set(self.__slots__) - {'_transform'})

    #    def __contains__(self, val):
    #        # TODO separate container to avoid doing all this?
    #        return val in (set(self.__slots__) - {'_transform'})

    #    def __init__(self, transform):
    #        #self._transform = transform
    #        for name in self:
    #            # TODO uninitialised mark!
    #            setattr(self, name, Mark(0, 0, transform))

    #    #def __getattribute__(self, name):
    #    #    # TODO better with setattribute and descriptor?
    #    #    # or with separate add_mark function?
    #    #    if name.startswith('_') or name not in self:
    #    #        return super().__getattribute__(name)

    #    #    else:
    #    #        return self._transform.transform_point(
    #    #            super().__getattribute__(name)
    #    #            )

    #    # TODO warn user if accidentally make class
    #    # variable instead of annotation!

    #marks: Marks

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

