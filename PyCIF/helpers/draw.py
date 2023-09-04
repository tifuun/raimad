# geometry-related convenience functions

import PyCIF as pc

import numpy as np

def to_polar(p1: pc.typing.Point, p2: pc.typing.Point | None = None):
    if p2 is not None:
        return to_polar(p2 - p1)

    return (
        np.arctan2(p1[1], p1[0]),
        np.linalg.norm(p1)
        )

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

    return [bbox[2] - bbox[0], bbox[3] - bbox[1]]

def colinear(*points):
    for prev, point, next_ in pc.iter.triples(points):
        if (
                pc.angle_between(prev, point)
                !=
                pc.angle_between(point, next_)
                ):
            return False
    # TODO not optimal
    # TODO what if points in wrong order?
    # Definition of colinear?
    return True




def non_colinear(*points):
    pass


