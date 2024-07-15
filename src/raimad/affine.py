"""
Operations on affine matrices
"""

from math import sin, cos, sqrt
from functools import reduce
from typing import Sequence

import numpy as np
import numpy.typing as _

import raimad as rai

def identity():
    return (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
        )

def matmul(*arrays: 'rai.typing.Affine') -> 'rai.typing.Affine':
    if len(arrays) == 1:
        return arrays[0]

    if len(arrays) == 2:
        a, b = arrays
        # This is faster than both numpy and comprehensions,
        # see benchamrks/matmul.py
        # Also has the benefit of not needing a PhD
        # in type gymnastics to get mypy to stop complaining
        return (
            (
                a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0],
                a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1],
                a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2]
                ),
            
            (
                a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0],
                a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1],
                a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2]
                ),
                
            (
                a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0],
                a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1],
                a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2]
                )
            )

    return matmul(matmul(arrays[0], arrays[1]), *arrays[2:])

def norm(vec: Sequence[float]) -> float:
    """
    Calculate the norm of a vector (aka equclidean distance)
    """

    # Hardcoding the special cases for vectors of length 0, 1, 2 and 3
    # seems to save a bit of time,
    # see benchmarks/norm.py
    if len(vec) == 0:
        return 0

    if len(vec) == 1:
        return vec[0]

    if len(vec) == 2:
        # `sqrt` is the tiniest bit faster than `** (1/2)`,
        # at least on my machine
        return sqrt(vec[0] ** 2 + vec[1] ** 2)

    if len(vec) == 3:
        return sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)

    # This is around three times faster than
    # numpy.linalg.norm for small vectors
    return sqrt(sum((coord ** 2 for coord in vec)))


def rotate(angle: float) -> 'rai.typing.Affine':
    return (
        (cos(angle), -sin(angle), 0),
        (sin(angle), cos(angle), 0),
        (0, 0, 1),
        )

def move(x: float, y: float) -> 'rai.typing.Affine':
    return (
        (1, 0, x),
        (0, 1, y),
        (0, 0, 1),
        )

def scale(x: float, y: float) -> 'rai.typing.Affine':
    return (
        (x, 0, 0),
        (0, y, 0),
        (0, 0, 1),
        )

def around(matrix: 'rai.typing.Affine', x: float, y: float) -> 'rai.typing.Affine':
    to_origin = move(-x, -y)
    from_origin = move(x, y)

    print('a')
    print(matmul(from_origin, matrix, to_origin))
    return matmul(from_origin, matrix, to_origin)

def get_translation(matrix: 'rai.typing.Affine') -> tuple[float, float]:
    """
    Given an affine matrix, return the corresponding translation.
    """
    return matrix[0][2], matrix[1][2]

def get_scale(matrix: 'rai.typing.Affine') -> tuple[float, float]:
    """
    Given an affine matrix, return the corresponding scale.
    """
    scale_x = norm((matrix[0][0], matrix[1][0], matrix[2][0]))
    scale_y = norm((matrix[0][1], matrix[1][1], matrix[2][1]))
    return float(scale_x), float(scale_y)

def get_shear(matrix: 'rai.typing.Affine') -> float:
    """
    Given an affine matrix, return the corresponding shear.
    """
    scale_x, scale_y = get_scale(matrix)
    return (
        matrix[0][0] * matrix[0][1]
        + matrix[1][0] * matrix[1][1]
        + matrix[2][0] * matrix[2][1]
        ) / (scale_x * scale_y)

def get_rotation(matrix: 'rai.typing.Affine') -> float:
    """
    Given an affine matrix, return the corresponding rotation
    """
    return float(np.arctan2(matrix[1][0], matrix[0][0]))

def transform_xyarray(
        matrix: 'rai.typing.Affine',
        xyarray: 'rai.typing.Poly'
        ) -> 'rai.typing.Poly':
    """
    Apply transformation to xyarray and return new transformed xyarray
    """
    return tuple(
        transform_point(matrix, point)
        for point in xyarray
        )

def transform_point(
        matrix: 'rai.typing.Affine',
        point: 'rai.typing.Point'
        ) -> 'rai.typing.Point':
    """
    Apply transformation to point and return transformed point
    Written by perplexity.ai
    """
    x, y = point
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    
    # Apply the transformation
    new_x = a * x + b * y + c
    new_y = d * x + e * y + f
    
    return (new_x, new_y)

