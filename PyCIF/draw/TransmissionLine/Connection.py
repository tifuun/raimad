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
    do_bridges: bool | None
    bridge_spacing: float | None
    bridge_scramble: float | None
    bridge_length: float | None

    pretty_name: ClassVar[str] = 'Connect to'

    def __init__(
            self,
            to: ConnectionTarget,
            radius: float | None = None,
            do_bridges: bool | None = None,
            bridge_spacing: float | None = None,
            bridge_scramble: float | None = None,
            bridge_length: float | None = None,
            clone_from: Self | None = None,
            ):
        if type(self) is Connection:
            raise Exception("Cannot create abstract Connection")

        if clone_from is not None:
            to = to or clone_from.to
            radius = radius or clone_from.radius
            do_bridges = do_bridges or clone_from.do_bridges
            bridge_spacing = bridge_spacing or clone_from.bridge_spacing
            bridge_scramble = bridge_scramble or clone_from.bridge_scramble
            bridge_length = bridge_length or clone_from.bridge_length

        if isinstance(to, pc.Point):
            self.to = to
        else:
            self.to = pc.Point(*to)  # TODO

        self.radius = radius
        self.do_bridges = do_bridges
        self.bridge_spacing = bridge_spacing
        self.bridge_scramble = bridge_scramble
        self.bridge_length = bridge_length

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


