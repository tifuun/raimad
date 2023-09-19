"""
Convenience constants and functions for dealing with angles
"""

from enum import Enum

import numpy as np

fullcircle = np.pi * 2
halfcircle = np.pi
quartercircle = np.pi / 2

# British variants
semicircle = np.pi
demisemicircle = np.pi / 2

class Orientation(Enum):
    Clockwise = -1
    Counterclockwise = 1

class TurnDirection(Enum):
    Around = -1
    Straight = 0
    Left = 1
    Right = 2

def angspace(
        start: float,
        end: float,
        num_steps:
        int = 50,
        orientation: Orientation = Orientation.Counterclockwise,
        ):
    """
    Angular space:
    construct an array of angles going from `start` to `end`
    in the positive orientation (counterclockwise)
    """
    if orientation is Orientation.Clockwise:
        start, end = end, start

    while start < 0:
        start += fullcircle

    while end < start:
        end += fullcircle

    return np.linspace(start, end, num_steps)

def classify_turn(before, point, after):
    # Thank you ChatGPT for this one,
    # it seems the day has come when AI
    # understands linear algebra better than I do
    prod = np.cross(point - before, after - point)

    if abs(prod) < 0.01:  # TODO epsilon
        return TurnDirection.Straight
    if prod > 0:
        return TurnDirection.Left
    elif prod < 0:
        return TurnDirection.Right

    # TODO turns around


