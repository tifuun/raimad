"""
Operations on affine matrices
"""

import numpy as np
import numpy.typing as _

import raimad as rai

def rotate(angle: float) -> 'rai.typing.Affine':
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1],
        ])

def move(x: float, y: float) -> 'rai.typing.Affine':
    return np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1],
        ])

def scale(x: float, y: float) -> 'rai.typing.Affine':
    return np.array([
        [x, 0, 0],
        [0, y, 0],
        [0, 0, 1],
        ])

def around(matrix: 'rai.typing.Affine', x: float, y: float) -> 'pc.typing.Affine':
    to_origin = move(-x, -y)
    from_origin = move(x, y)

    return from_origin @ matrix @ to_origin

def get_translation(matrix: 'rai.typing.Affine') -> np.typing.NDArray[np.float64]:
    """
    Given an affine matrix, return the corresponding translation.
    Written by ChatGPT
    """
    return matrix[:2, 2]

def get_scale(matrix: 'rai.typing.Affine') -> tuple[np.float64, np.float64]:
    """
    Given an affine matrix, return the corresponding scale.
    Written by ChatGPT
    """
    scale_x = np.linalg.norm(matrix[:, 0])
    scale_y = np.linalg.norm(matrix[:, 1])
    return scale_x, scale_y

def get_shear(matrix: 'rai.typing.Affine') -> float:
    """
    Given an affine matrix, return the corresponding shear.
    Written by ChatGPT
    """
    scale_x, scale_y = get_scale(matrix)
    shear = float(np.dot(matrix[:, 0], matrix[:, 1]) / (scale_x * scale_y))
    return shear

def get_rotation(matrix: 'rai.typing.Affine') -> float:
    """
    Given an affine matrix, return the corresponding rotation
    Written by ChatGPT
    """
    return float(np.arctan2(matrix[1, 0], matrix[0, 0]))

def transform_xyarray(
        matrix: 'rai.typing.Affine',
        xyarray: 'rai.typing.Poly | pc.typing.PolyArray'
        ) -> 'rai.typing.Poly | pc.typing.PolyArray':
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
    euclidean: np.typing.NDArray[np.float64] = \
        transformed[:, :2] / transformed[:, 2].reshape(-1, 1)

    return euclidean

def transform_point(
        matrix: 'rai.typing.Affine',
        point: 'rai.typing.Point'
        ) -> 'rai.typing.Point':
    """
    Apply transformation to point and return new transformed point
    """
    homogeneous = np.append(point, 1)
    transformed = np.dot(homogeneous, matrix.T)
    cartesian = transformed[:2] / transformed[2]

    return np.array(cartesian)


