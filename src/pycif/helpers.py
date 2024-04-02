from enum import Enum
import numpy as np
import pycif as pc

fullcircle = pc.degrees(360)
halfcircle = pc.degrees(180)
quartercircle = pc.degrees(90)
eigthcircle = pc.degrees(45)

semicircle = pc.degrees(180)
demisemicircle = pc.degrees(90)
hemidemisemicircle = pc.degrees(45)

class Orientation(Enum):
    POS = 1
    NEG = -1

def angspace(
        start: float,
        end: float,
        num_steps: int = 50,
        orientation: Orientation = Orientation.POS,
        endpoint: bool = True,
        ):
    """
    Angular space:
    construct an array of angles going from `start` to `end`
    in the positive orientation (counterclockwise)
    """
    if orientation is Orientation.NEG:
        start, end = end, start

    while start < 0:
        start += fullcircle

    while end < start:
        end += fullcircle

    return np.linspace(start, end, num_steps, endpoint=endpoint)

def angle_between(p1, p2):
    """
    Angle between two points
    """
    x, y = np.array(p2) - np.array(p1)
    return np.arctan2(y, x)

def polar(arg, mod=1):
    return np.array([
        np.cos(arg),
        np.sin(arg)
        ]) * mod

def is_compo_class(obj):
    return (
        isinstance(obj, type)
        and issubclass(obj, pc.Compo)
        and obj is not pc.Compo
        )


