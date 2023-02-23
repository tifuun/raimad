"""
Turn and Bearing: two ways of expressing angles
"""

from typing import Self
from enum import Enum

import numpy as np


class Angle():
    """
    Angle container.
    """
    def __init__(self, degrees: float):
        """
        Create new Angle, given a measure in degrees.
        It is preferred to use the Degrees, Radians, and CircleFraction
        classmethods
        rather than using the __init__ method directly.
        """
        self._setvalue(degrees)

    def _setvalue(self, degrees: float):
        """
        Set internal degrees value.
        This method may be overwritten by, for example,
        BoundedAngle classes to apply the bounding rules.
        """
        self._degrees = degrees

    @classmethod
    def Degrees(cls, degrees: float) -> Self:
        """
        Construct a new angle, given the measure in degrees.
        """
        return cls(degrees=degrees)

    @classmethod
    def Radians(cls, radians: float) -> Self:
        """
        Construct a new angle, given the measure in radians.
        """
        return cls(degrees=np.degrees(radians))

    @classmethod
    def CircleFraction(cls, fraction: float) -> Self:
        """
        Construct a new angle, given a fraction of a circle.
        """
        return cls(degrees=360 * fraction)

    # Aliases
    Deg = Degrees
    Rad = Radians
    Frac = CircleFraction

    @classmethod
    def Degrees(cls, degrees: float) -> Self:
        """
        Construct a new angle, given the measure in degrees.
        """
        return cls(degrees=degrees)

    @property
    def degrees(self):
        """
        Get value in degrees.
        """
        return self._degrees

    @property
    def radians(self):
        """
        Get value in radians.
        """
        return self._degrees / 180 * np.pi

    def __str__(self):
        return f'{self.degrees}\xb0'

    def __add__(self, other: Self):
        return Angle(degrees=self.degrees + other.degrees)

    def __sub__(self, other: Self):
        return Angle(degrees=self.degrees - other.degrees)

    def __gt__(self, other: Self):
        return self.degrees > other.degrees

    def __lt__(self, other: Self):
        return self.degrees < other.degrees

    def __ge__(self, other: Self):
        return self.degrees >= other.degrees

    def __le__(self, other: Self):
        return self.degrees <= other.degrees


Circle = Angle.CircleFraction(1)
Semicircle = Angle.CircleFraction(1 / 2)
Quartercircle = Angle.CircleFraction(1 / 4)


def bounded_angle(minimum: Angle, maximum: Angle):
    """
    Decorator to create subclasses of Angle
    that only permit a fixed range of values.
    `minimum` is inclusive, `maximum` is exlusive.
    """
    assert maximum > minimum
    assert (maximum - minimum) <= Circle
    _range = maximum - minimum

    def _setvalue(self, degrees: float):
        #if not (minimum.degrees <= degrees < maximum.degrees):
        #    raise Exception(f'Not in range {minimum}, {maximum}')
        degrees = ((degrees - minimum.degrees) % _range.degrees + minimum.degrees)
        Angle._setvalue(self, degrees)

    def make_bounded_angle(cls):
        setattr(cls, '_setvalue', _setvalue)
        return cls

    return make_bounded_angle


@bounded_angle(Angle.Degrees(-180), Angle.Degrees(180))
class Turn(Angle):
    class Direction(Enum):
        Left = 1
        Right = 2
        Straight = 3
        Backwards = 4

    Left = Direction.Left
    Right = Direction.Right
    Straight = Direction.Straight
    Backwards = Direction.Backwards

    def __str__(self):
        if self.direction in {self.Straight, self.Backwards}:
            return self.direction.name
        return f'{abs(self._degrees)}\xb0 {self.direction.name}'

    @property
    def direction(self) -> Direction:
        if self._degrees == 0:
            return self.Straight

        if self._degrees == -180:
            return self.Backwards

        if self._degrees <= 0:
            return self.Left

        if self._degrees >= 0:
            return self.Right


@bounded_angle(Angle.Degrees(0), Angle.Degrees(360))
class Bearing(Angle):
    pass



