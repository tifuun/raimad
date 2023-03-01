"""
Arc polygon
"""

from typing import ClassVar
from enum import Enum

import numpy as np

from PyCIF.draw.Polygon import Polygon
from PyCIF.draw.Point import Point
from PyCIF.draw.PointRef import PointRef
from PyCIF.draw.angles import angspace, Bearing


class Arc(Polygon):
    radius_inner: ClassVar[float]
    radius_outter: ClassVar[float]
    angle: ClassVar[float]

    def __init__(
            self,
            radius_inner: float,
            radius_outter: float,
            bearing_start: float,
            bearing_end: float,
            center: Point | None = None,
            backwards: bool = False,
            ):
        super().__init__()

        self.radius_inner = radius_inner
        self.radius_outter = radius_outter
        self.bearing_start = bearing_start
        self.bearing_end = bearing_end
        self._center = center.copy() if center is not None else Point(0, 0)
        self.backwards = backwards

        self.midradius = (self.radius_inner + self.radius_outter) / 2

        self._add_mark(
            'center',
            self._center,
            'Center of the arc',
            )

        self._add_mark(
            'start_mid',
            self._center + self.bearing_start.as_point() * self.midradius,
            'Midway between the two radii, at the start of the arc'
            )

        self._add_mark(
            'end_mid',
            self._center + self.bearing_end.as_point() * self.midradius,
            'Midway between the two radii, at the end of the arc'
            )

    def _get_xyarray(self):

        if self.bearing_start == self.bearing_end:
            return np.array([])

        points = angspace(
            self.bearing_start,
            self.bearing_end,
            backwards=self.backwards,
            )

        return np.array([
            (
                *(bearing.as_point() * radius + self._center),
            )  # FIXME weird syntax
            for radius in (self.radius_inner, self.radius_outter)
            for bearing in (points, reversed(points))[
                radius is self.radius_inner
                ]
            ])

