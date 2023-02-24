"""
Turn and Bearing: two ways of expressing angles
"""

from typing import Self, Any
from enum import Enum

import numpy as np

from PyCIF.draw.Point import Point


class Angle():
    """
    Angle container.
    """
    def __init__(self, degrees: float | Self):
        """
        Create new Angle, given a measure in degrees.
        It is preferred to use the Degrees, Radians, and CircleFraction
        classmethods
        rather than using the __init__ method directly.
        """
        if isinstance(degrees, type(self)) or isinstance(self, type(degrees)):
            degrees = degrees.degrees

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

    @staticmethod
    def _verify_angle(obj: Any):
        """
        Raise an exception if someone is trying
        to use a binary operator between an Angle and a
        standard float or int.
        """
        if isinstance(obj, float | int):
            raise Exception(
                f"Object of type {type(obj)} is ambiguous. "
                "Please construct an Angle using Angle.Deg, "
                "Angle.Rad, or Angle.Frac instead."
                )

    def __str__(self):
        return f'{self.degrees}\xb0'

    __repr__ = __str__

    def __abs__(self):
        return self.__class__(degrees=abs(self._degrees))

    def __neg__(self):
        return self.__class__(degrees=-self._degrees)

    def __add__(self, other: Self):
        self._verify_angle(other)
        return self.__class__(degrees=self.degrees + other.degrees)

    def __sub__(self, other: Self):
        self._verify_angle(other)
        return self.__class__(degrees=self.degrees - other.degrees)

    def __mul__(self, multiplier: float):
        return self.__class__(degrees=self.degrees * multiplier)

    def __truediv__(self, dividend: float):
        return self.__class__(degrees=self.degrees / dividend)

    def __gt__(self, other: Self):
        self._verify_angle(other)
        return self.degrees > other.degrees

    def __lt__(self, other: Self):
        self._verify_angle(other)
        return self.degrees < other.degrees

    def __ge__(self, other: Self):
        self._verify_angle(other)
        return self.degrees >= other.degrees

    def __le__(self, other: Self):
        self._verify_angle(other)
        return self.degrees <= other.degrees


Delta = Angle.Degrees(0.1)
Fullcircle = Angle.CircleFraction(1)
Semicircle = Angle.CircleFraction(1 / 2)
Quartercircle = Angle.CircleFraction(1 / 4)


def sin(angle: Angle):
    return np.sin(angle.radians)

def cos(angle: Angle):
    return np.sin(angle.radians)

def tan(angle: Angle):
    return np.sin(angle.radians)


def bounded_angle(minimum: Angle, maximum: Angle):
    """
    Decorator to create subclasses of Angle
    that only permit a fixed range of values.
    `minimum` is inclusive, `maximum` is exlusive.
    """
    assert maximum > minimum
    assert (maximum - minimum) <= Fullcircle
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


@bounded_angle(Angle.Degrees(0), Angle.Degrees(360))
class Bearing(Angle):
    @classmethod
    def Arctan2(cls, y: float, x: float):
        """
        Like np.arctan2, but using bearing.
        """
        mathematical = np.degrees(np.arctan2(y, x))
        bearing = (360 - mathematical + 90) % 360
        return cls(degrees=bearing)

    @classmethod
    def Between_points(cls, source: Point, destination: Point):
        """
        Calculate bearing of a line between two Points.
        """
        x, y = (destination - source)
        return cls.Arctan2(y, x)

    def as_point(self) -> Point:
        mathangle = np.radians(-self._degrees + 90)
        return Point(np.cos(mathangle), np.sin(mathangle))

    def __neg__(self):
        return self.__class__(self + Semicircle)


@bounded_angle(Angle.Degrees(-180), Angle.Degrees(180))
class Turn(Angle):
    @classmethod
    def Right(cls, angle: Angle):
        return cls(degrees=angle.degrees)

    @classmethod
    def Left(cls, angle: Angle):
        return cls(degrees=-angle.degrees)

    @classmethod
    def Straight(cls):
        return cls(degrees=0)

    @classmethod
    def Backwards(cls):
        return cls(degrees=-180)

    def __str__(self):
        if self.direction in {self.Straight, self.Backwards}:
            return self.direction.__name__
        return f'{abs(self._degrees)}\xb0 {self.direction.__name__}'

    @property
    def direction(self):
        if self._degrees == 0:
            return self.Straight

        if self._degrees == -180:
            return self.Backwards

        if self._degrees <= 0:
            return self.Left

        if self._degrees >= 0:
            return self.Right

    def Between_bearings(incoming: Bearing, outgoing: Bearing):
        #outgoing = outgoing - Semicircle
        #outgoing = outgoing

        if abs(incoming - outgoing) < Delta:
            return Turn.Straight()

        if incoming > outgoing:
            return Turn.Left(incoming - outgoing)

        if outgoing > incoming:
            return Turn.Right(outgoing - incoming)


def angspace(
        start: Angle,
        end: Angle,
        num_steps: int = 50,
        backwards: bool = False,
        ):

    # `start` and `end` may be passed as bounded angles
    # (for example, Bearings)
    # so we cast them to Angles to allow the full range of motion
    start = Angle(start)
    end = Angle(end)

    print('aaa', start, end, end=' ')

    if backwards:
        while end > start:
            end -= Fullcircle

    print('aaa', start, end, end='\n\n')

    return [
            #-Bearing.Rad(rad) + Quartercircle
        Bearing.Rad(rad)
        for rad
        in np.linspace(start.radians, end.radians, num_steps)
        ]

