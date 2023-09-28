from typing import Self, ClassVar

import PyCIF as pc

# Might be able to include other things in the future
# (Advances?) so best to keep an alias for now
# TODO move to pc.typing?
ConnectionTarget = pc.typing.Point


class Connection:
    """
    Abstract base for connection type
    """
    to: ConnectionTarget
    radius: float | None  # at start of connection
    bridges: bool | None
    bridge_spacing: float | None
    bridge_scramble: float | None
    bridge_width: float | None

    pretty_name: ClassVar[str] = 'Connect to'

    def __init__(
            self,
            to: ConnectionTarget,
            radius: float | None = None,
            bridges: bool | None = None,
            bridge_spacing: float | None = None,
            bridge_scramble: float | None = None,
            bridge_width: float | None = None,
            clone_from: Self | None = None,
            ):
        if type(self) is Connection:
            raise Exception("Cannot create abstract Connection")

        if clone_from is not None:
            to = to or clone_from.to
            radius = radius or clone_from.radius
            bridges = bridges or clone_from.bridges
            bridge_spacing = bridge_spacing or clone_from.bridge_spacing
            bridge_scramble = bridge_scramble or clone_from.bridge_scramble
            bridge_width = bridge_width or clone_from.bridge_width

        self.to = to
        self.radius = radius
        self.bridges = bridges
        self.bridge_spacing = bridge_spacing
        self.bridge_scramble = bridge_scramble
        self.bridge_width = bridge_width

    def __repr__(self):
        return f'{self.pretty_name} {self.to}: r={self.radius}'

class StartAt(Connection):
    """
    Start at point or markable
    """
    pretty_name: ClassVar[str] = 'Start at'


class JumpTo(Connection):
    """
    Indicates no connection to next point
    """
    pretty_name: ClassVar[str] = 'Jump to'

class StraightTo(Connection):
    """
    Direction connection between points with one straight line segment
    """
    pretty_name: ClassVar[str] = 'Straight to'

class ElbowTo(Connection):
    """
    Elbow connection (90 degree) between two points
    """
    pretty_name: ClassVar[str] = 'Elbow to'

class MeanderTo(Connection):
    """
    Meander between two points
    """
    pretty_name: ClassVar[str] = 'Meander to'

    def __init__(*args, **kwargs):
        raise NotImplementedError


