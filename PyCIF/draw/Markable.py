"""
Markable -- interface for adding named points to components
"""

from typing import Mapping

import PyCIF as pc

class Markable(pc.Transformable):

    class Marks():

        _transformable: pc.Transformable
        _mark_values: Mapping[str, pc.Point]

        origin = pc.Mark('Origin of the coordinate system of this Markable')

        def __init__(self, transformable):
            self._transformable = transformable
            self._mark_values = {}

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

