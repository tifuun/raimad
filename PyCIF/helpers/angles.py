"""
Convenience constants and functions for dealing with angles
"""

from enum import Enum

import numpy as np

fullcircle = np.pi * 2
semicircle = np.pi
quartercircle = np.pi / 2

class Orientation(Enum):
    Clockwise = -1
    Counterclockwise = 1

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


