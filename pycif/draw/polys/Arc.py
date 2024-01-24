"""
Arc poly
"""

import numpy as np

import pycif as pc

class Arc(pc.Poly):
    radius_inner: float
    radius_outter: float
    angle_start: float
    angle_end: float
    orientation: pc.Orientation
    radial_center: float

    class Marks(pc.Poly.Marks):
        center = pc.Mark('Center of the arc')
        start_mid = pc.Mark(
            'Midway between the two radii, at the start of the arc'
            )
        end_mid = pc.Mark(
            'Midway between the two radii, at the end of the arc'
            )

    @pc.kwoverload
    def __init__(
            self,
            angle_start: float,
            angle_end: float,
            orientation: pc.Orientation = pc.Orientation.Counterclockwise,
            *,
            radius_inner: float,
            radius_outter: float,
            ):
        super().__init__()

        self.radius_inner = radius_inner
        self.radius_outter = radius_outter
        self.angle_start = angle_start
        self.angle_end = angle_end
        self.orientation = orientation
        self.radial_center = (self.radius_inner + self.radius_outter) / 2

        self._set_marks()

    @__init__.register
    def _(
            self,
            angle_start: float,
            angle_end: float,
            orientation: pc.Orientation = pc.Orientation.Counterclockwise,
            *,
            radius_inner: float,
            radial_width: float,
            ):
        super().__init__()

        self.radius_inner = radius_inner
        self.radius_outter = radius_inner + radial_width
        self.angle_start = angle_start
        self.angle_end = angle_end
        self.orientation = orientation
        self.radial_center = (self.radius_inner + self.radius_outter) / 2

        self._set_marks()

    @__init__.register
    def _(
            self,
            angle_start: float,
            angle_end: float,
            orientation: pc.Orientation = pc.Orientation.Counterclockwise,
            *,
            radius_outter: float,
            radial_width: float,
            ):
        super().__init__()

        self.radius_inner = radius_outter - radial_width
        self.radius_outter = radius_outter
        self.angle_start = angle_start
        self.angle_end = angle_end
        self.orientation = orientation
        self.radial_center = (self.radius_inner + self.radius_outter) / 2

        self._set_marks()

    @__init__.register
    def _(
            self,
            angle_start: float,
            angle_end: float,
            orientation: pc.Orientation = pc.Orientation.Counterclockwise,
            *,
            radial_center: float,
            radial_width: float,
            ):
        super().__init__()

        self.radius_inner = radial_center - radial_width / 2
        self.radius_outter = radial_center + radial_width / 2
        self.angle_start = angle_start
        self.angle_end = angle_end
        self.orientation = orientation
        self.radial_center = radial_center

        self._set_marks()

    def _set_marks(self):
        self.marks.center = pc.Point(0, 0)

        self.marks.start_mid = pc.Point(
            arg=self.angle_start,
            mag=self.radial_center
            )

        self.marks.end_mid = pc.Point(
            arg=self.angle_end,
            mag=self.radial_center
            )

    def _get_xyarray(self):

        if self.angle_start == self.angle_end:
            return np.array([])

        angspace = pc.angspace(
            self.angle_start,
            self.angle_end,
            orientation=self.orientation,
            )

        return np.array([
            pc.Point(arg=angle, mag=radius)
            for radius, angles in [
                [self.radius_inner, angspace],
                [self.radius_outter, reversed(angspace)],
                ]
            for angle in angles
            ])

