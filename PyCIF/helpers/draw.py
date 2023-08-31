# geometry-related convenience functions

import PyCIF as pc

import numpy as np

def point_polar(angle: float, magnitude: float = 1):
    """
    Return a vector given angle and magnitude.
    """
    return np.array([
        np.cos(angle),
        np.sin(angle),
        ]) * magnitude

def to_polar(p1: pc.typing.Point, p2: pc.typing.Point | None = None):
    if p2 is not None:
        return to_polar(p2 - p1)

    return (
        np.arctan2(p1[1], p1[0]),
        np.linalg.norm(p1)
        )

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

def midpoint(p1, p2):
    """
    Midpoint between two points
    """
    return (p1 + p2) / 2

def bounding_box_cartesian(points):
    """
    Return [x1, y1, x2, y2] bounding box
    for a collection of points
    (Cartesian coordinates, Y increases upwards)
    """
    x1 = np.inf
    y1 = np.inf
    x2 = -np.inf
    y2 = -np.inf

    for x, y in points:
        if x < x1:
            x1 = x
        elif x > x2:
            x2 = x
        if y < y1:
            y1 = y
        elif y > y2:
            y2 = y

    return [x1, y1, x2, y2]

def bounding_box_size(bbox):
    return [bbox[2] - bbox[0], bbox[3] - bbox[1]]


