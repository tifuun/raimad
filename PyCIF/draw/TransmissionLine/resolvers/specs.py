from dataclasses import dataclass

import PyCIF as pc

@dataclass
class BendSpec:
    angle_start: float
    angle_end: float
    orientation: pc.Orientation
    point_enter: pc.Point
    point_exit: pc.Point
    point_center: pc.Point
    # TODO radius

