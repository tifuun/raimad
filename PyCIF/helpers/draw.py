# geometry-related convenience functions

import numpy as np

def point_polar(angle: float, magnitude: float = 1):
    """
    Return a vector given angle and magnitude.
    """
    return np.array([
        np.cos(angle),
        np.sin(angle),
        ]) * magnitude

def point(x: float, y: float):
    return np.array([x, y], dtype=np.float32)

def angle_between(p1, p2):
    """
    Angle between two points
    """
    x, y = p2 - p1
    return np.arctan2(y, x)

def distance_between(p1, p2):
    """
    distance between two points
    """
    return np.linalg.norm(p2 - p1)

