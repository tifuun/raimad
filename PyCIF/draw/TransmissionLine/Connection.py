from typing import Any, ClassVar, List, Iterable

import PyCIF as pc

ConnectionTarget = pc.typing.Point | pc.Markable


class Connection:
    """
    Abstract base for connection type
    """
    to: ConnectionTarget

    def __init__(self, to):
        if type(self) is Connection:
            raise Exception("Cannot create abstract Connection")
        self.to = to

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

