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
    turn_radius: float | None  # at start of connection
    bridges: bool | None
    bridge_spacing: float | None
    bridge_scramble: float | None
    bridge_width: float | None

    def __init__(
            self,
            to: ConnectionTarget,
            bridges: bool | None = None,
            bridge_spacing: float | None = None,
            bridge_scramble: float | None = None,
            bridge_width: float | None = None,
            ):
        if type(self) is Connection:
            raise Exception("Cannot create abstract Connection")

        self.to = to
        self.bridges = bridges
        self.bridge_spacing = bridge_spacing
        self.bridge_scramble = bridge_scramble
        self.bridge_width = bridge_width

class StartAt(Connection):
    """
    Start at point or markable
    """
    def __repr__(self):
        return f"Start at    {self.to}"

class JumpTo(Connection):
    """
    Indicates no connection to next point
    """
    def __repr__(self):
        return f"Jump to     {self.to}"

class StraightTo(Connection):
    """
    Direction connection between points with one straight line segment
    """
    def __repr__(self):
        return f"Straight to {self.to}"

class ElbowTo(Connection):
    """
    Elbow connection (90 degree) between two points
    """
    def __repr__(self):
        return f"Elbow to    {self.to}"

class MeanderTo(Connection):
    """
    Meander between two points
    """
    def __repr__(self):
        return f"Meander to  {self.to}"

    def __init__(*args, **kwargs):
        raise NotImplementedError


#from enum import Enum
#from dataclasses import dataclass
#
#import PyCIF as pc
#
## Might be able to include other things in the future
## (Advances?) so best to keep an alias for now
## TODO move to pc.typing?
#ConnectionTarget = pc.typing.Point
#
#@dataclass
#class Connection:
#    """
#    Abstract base for connection type
#    """
#    class Line(Enum):
#        StartAt = 0
#        JumpTo = 1
#        StraightTo = 2
#        ElbowTo = 3
#        MeanderTo = 4
#
#        def __repr__(self):
#            return [
#                'Start at    ',
#                'Jump to     ',
#                'Straight to ',
#                'Elbow to    ',
#                'Meander to  ',
#                ][self]
#
#        __str__ = __repr__
#        __format__ = __repr__
#
#    to: ConnectionTarget
#    line: Line
#    turn_radius: float  # at start of connection
#    bridges: bool
#    bridge_spacing: float
#    bridge_scramble: float
#    bridge_width: float
#
#
#def StartAt(
#        to: ConnectionTarget,
#        turn_radius: float = 10,
#        bridges: bool = True,
#        bridge_spacing: float = 10,
#        bridge_scramble: float = 4,
#        bridge_width: float = 2,
#        ):
#    return Connection(
#        to,
#        Connection.Line.StartAt,
#        turn_radius,
#        bridges,
#        bridge_spacing,
#        bridge_scramble,
#        bridge_width,
#        )
#
#def StraightTo(
#        to: ConnectionTarget,
#        turn_radius: float = 10,
#        bridges: bool = True,
#        bridge_spacing: float = 10,
#        bridge_scramble: float = 4,
#        bridge_width: float = 2,
#        ):
#    return Connection(
#        to,
#        Connection.Line.StraightTo,
#        turn_radius,
#        bridges,
#        bridge_spacing,
#        bridge_scramble,
#        bridge_width,
#        )
#
#def JumpTo(
#        to: ConnectionTarget,
#        turn_radius: float = 10,
#        bridges: bool = True,
#        bridge_spacing: float = 10,
#        bridge_scramble: float = 4,
#        bridge_width: float = 2,
#        ):
#    return Connection(
#        to,
#        Connection.Line.JumpTo,
#        turn_radius,
#        bridges,
#        bridge_spacing,
#        bridge_scramble,
#        bridge_width,
#        )
#
#def ElbowTo(
#        to: ConnectionTarget,
#        turn_radius: float = 10,
#        bridges: bool = True,
#        bridge_spacing: float = 10,
#        bridge_scramble: float = 4,
#        bridge_width: float = 2,
#        ):
#    return Connection(
#        to,
#        Connection.Line.ElbowTo,
#        turn_radius,
#        bridges,
#        bridge_spacing,
#        bridge_scramble,
#        bridge_width,
#        )
#
#def MeanderTo(
#        to: ConnectionTarget,
#        turn_radius: float = 10,
#        bridges: bool = True,
#        bridge_spacing: float = 10,
#        bridge_scramble: float = 4,
#        bridge_width: float = 2,
#        ):
#    raise NotImplementedError
#    return Connection(
#        to,
#        Connection.Line.MeanderTo,
#        turn_radius,
#        bridges,
#        bridge_spacing,
#        bridge_scramble,
#        bridge_width,
#        )
#
