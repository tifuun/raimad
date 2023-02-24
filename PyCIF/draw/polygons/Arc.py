"""
Arc polygon
"""

from typing import ClassVar

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
            angle_start: float,
            angle_end: float,
            center: Point,
            backwards: bool = False,
            ):
        super().__init__()

        self.radius_inner = radius_inner
        self.radius_outter = radius_outter
        self.angle_start = angle_start #% 360
        self.angle_end = angle_end #% 360
        self._center = center.copy()
        self.backwards = backwards

    @property
    def _xyarray(self):

        if self.angle_start == self.angle_end:
            return np.array([])

        #if self._shortest:
        #    angle_start = np.radians(self.angle_start)# % 360)
        #    angle_end = np.radians(self.angle_end)# % 360)

        #    angle_start, angle_end = \
        #        min(angle_start, angle_end), max(angle_start, angle_end)

        #    print(angle_start, angle_end)
        #    if angle_end - angle_start > (np.pi):
        #        angle_start, angle_end = \
        #            angle_end - (np.pi * 2), angle_start
        #    print(angle_start, angle_end)
        #    print()

        #else:
        #    angle_start = np.radians(self.angle_start),
        #    angle_end = np.radians(self.angle_end),

        # BEARING!!
        #if self.backwards:
        #    while self.angle_start < self.angle_end:
        #        self.angle_start += 360

        #else:
        #    while self.angle_end < self.angle_start:
        #        self.angle_end += 360

        #angle_start = np.radians(- self.angle_start + 90)
        #angle_end = np.radians(- self.angle_end + 90)

        #angle_start = np.radians(self.angle_start)
        #angle_end = np.radians(self.angle_end)

        #print(self.angle_start, self.angle_end)
        #print('--', self.angle_start % 360, self.angle_end % 360)

        #points = np.linspace(
        #    angle_start,
        #    angle_end,
        #    )
        points = angspace(
            self.angle_start,
            self.angle_end,
            backwards=self.backwards,
            )

        #points = [Bearing.Deg(d) for d in np.linspace(0, 300)]
        return np.array([
            (
                #self._center.x + np.cos(angle) * radius,
                #self._center.y + np.sin(angle) * radius,
                *(angle.as_point() * radius + self._center),
            )
            for radius in (self.radius_inner, self.radius_outter)
            for angle in (points, reversed(points))[
                radius is self.radius_inner
                ]
            ])

    @property
    def midradius(self):
        return (self.radius_inner + self.radius_outter) / 2

    @property
    def center(self):
        """
        Center of the arc
        """
        return PointRef(self, self._center)

    @property
    def start_mid(self):
        """
        Midway between the two radii,
        at the start of the arc
        """
        return PointRef(self, self.angle_start.as_point() * self.midradius + self._center)
        #return self.polar(self.angle_start, self.midradius) + self._center

    @property
    def end_mid(self):
        """
        Midway between the two radii,
        at the start of the arc
        """
        return PointRef(self, self.angle_end.as_point() * self.midradius + self._center)
        #return self.polar(self.angle_end, self.midradius) + self._center

