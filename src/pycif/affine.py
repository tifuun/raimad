"""
Operations on affine matrices
"""

import numpy as np

def rotate(angle):
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1],
        ])

def move(x, y):
    return np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1],
        ])

def scale(x, y):
    return np.array([
        [x, 0, 0],
        [0, y, 0],
        [0, 0, 1],
        ])

def around(matrix, x, y):
    to_origin = move(-x, -y)
    from_origin = move(x, y)

    return from_origin @ matrix @ to_origin

def get_translation(matrix):
    """
    Given an affine matrix, return the corresponding translation.
    Written by ChatGPT
    """
    return matrix[:2, 2]

def get_scale(matrix):
    """
    Given an affine matrix, return the corresponding scale.
    Written by ChatGPT
    """
    scale_x = np.linalg.norm(matrix[:, 0])
    scale_y = np.linalg.norm(matrix[:, 1])
    return scale_x, scale_y

def get_shear(matrix):
    """
    Given an affine matrix, return the corresponding shear.
    Written by ChatGPT
    """
    scale_x, scale_y = get_scale(matrix)
    shear = np.dot(matrix[:, 0], matrix[:, 1]) / (scale_x * scale_y)
    return shear

def get_rotation(matrix):
    """
    Given an affine matrix, return the corresponding rotation
    Written by ChatGPT
    """
    return np.arctan2(matrix[1, 0], matrix[0, 0])

def transform_xyarray(matrix, xyarray: np.ndarray):
    """
    Apply transformation to xyarray and return new transformed xyarray
    """
    if len(xyarray) == 0:
        return xyarray

    if not isinstance(xyarray, np.ndarray):
        # TODO instead of dynamic hacks like this,
        # grind through with a static checker
        xyarray = np.array(xyarray)

    homogeneous = np.hstack((
        xyarray,
        np.ones((xyarray.shape[0], 1)),
        ))
    transformed = np.dot(homogeneous, matrix.T)
    euclidean = transformed[:, :2] / transformed[:, 2].reshape(-1, 1)

    return euclidean

def transform_point(matrix, point):
    """
    Apply transformation to point and return new transformed point
    """
    homogeneous = np.append(point, 1)
    transformed = np.dot(homogeneous, matrix.T)
    cartesian = transformed[:2] / transformed[2]

    return np.array(cartesian)


