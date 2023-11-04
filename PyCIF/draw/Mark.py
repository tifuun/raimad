"""
Mark: labeled point with description
"""

import PyCIF as pc

log = pc.get_logger(__name__)

class Mark(metaclass=pc.SlotsFromAnnotationsMeta):
    description: str
    name: str

    def __init__(self, description: str = ''):
        self.description = description

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, cls=None):
        point = obj._mark_values[self.name]
        x, y = obj._transformable.transform.transform_point(point)
        return pc.BoundPoint(x, y, obj._transformable)

    def __set__(self, obj, value):
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

