"""affine.py: operations on affine matrices and other math helpers."""

from math import sin, cos, sqrt, atan2
from typing import Sequence

import raimad as rai

def identity() -> 'rai.typing.Affine':
    """Make 3x3 identity matrix."""
    return (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
        )

def matmul(*arrays: 'rai.typing.Affine') -> 'rai.typing.Affine':
    """
    Multiply 3x3 matrices.

    Parameters
    ----------
    *arrays: rai.typing.Affine
        The matrices to multiply.
        If only one matrix is passed, that matrix is returned unchanged.
        Otherwise, the product of all the passed matrices is returned.

    Returns
    -------
    rai.typing.Affine
        The product of the matrices.
    """
    if len(arrays) == 1:
        return arrays[0]

    if len(arrays) == 2:
        a, b = arrays
        # This is faster than both numpy and comprehensions,
        # see benchamrks/matmul.py
        # Also, not using numpy has the benefit of not needing a PhD
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
    Calculate the norm of a vector (aka equclidean distance).

    Parameters
    ----------
    vec: Sequence[float]
        The vector to compute the norm of.
        It can have any dimension.
        Zero-dimensional vectors are treated as having a norm of zero.

    Returns
    -------
    float
        The norm of the vector.
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
    """Generate an affine matrix corresponding to a rotation."""
    return (
        (cos(angle), -sin(angle), 0),
        (sin(angle), cos(angle), 0),
        (0, 0, 1),
        )

def move(x: float, y: float) -> 'rai.typing.Affine':
    """Generate an affine matrix corresponding to a translation."""
    return (
        (1, 0, x),
        (0, 1, y),
        (0, 0, 1),
        )

def scale(x: float, y: float) -> 'rai.typing.Affine':
    """Generate an affine matrix corresponding to a scale."""
    return (
        (x, 0, 0),
        (0, y, 0),
        (0, 0, 1),
        )

def around(
        matrix: 'rai.typing.Affine',
        x: float,
        y: float
        ) -> 'rai.typing.Affine':
    """
    Change the origin of an affine matrix.

    This matrix takes an affine matrix and a new origin point.
    It returns a new affine matrix that corresponds to a product of:
    - A translation matrix that puts the new origin into the origin
    - The passed matrix
    - A translation that restores the original origin

    This can be used to perform transformations such as scale or rotation
    around a specific point.
    """
    to_origin = move(-x, -y)
    from_origin = move(x, y)

    return matmul(from_origin, matrix, to_origin)

def get_translation(matrix: 'rai.typing.Affine') -> tuple[float, float]:
    """Given an affine matrix, return the corresponding translation."""
    return matrix[0][2], matrix[1][2]

def get_scale(matrix: 'rai.typing.Affine') -> tuple[float, float]:
    """Given an affine matrix, return the corresponding scale."""
    scale_x = norm((matrix[0][0], matrix[1][0], matrix[2][0]))
    scale_y = norm((matrix[0][1], matrix[1][1], matrix[2][1]))
    return float(scale_x), float(scale_y)

def get_shear(matrix: 'rai.typing.Affine') -> float:
    """Given an affine matrix, return the corresponding shear."""
    scale_x, scale_y = get_scale(matrix)
    return (
        matrix[0][0] * matrix[0][1]
        + matrix[1][0] * matrix[1][1]
        + matrix[2][0] * matrix[2][1]
        ) / (scale_x * scale_y)

def get_rotation(matrix: 'rai.typing.Affine') -> float:
    """Given an affine matrix, return the corresponding rotation."""
    return float(atan2(matrix[1][0], matrix[0][0]))

def transform_poly(
        matrix: 'rai.typing.Affine',
        poly: 'rai.typing.Poly'
        ) -> 'rai.typing.Poly':
    """Apply transformation to poly and return new transformed poly."""
    return [
        transform_point(matrix, point)
        for point in poly
        ]
    # TODO remove "poly name"

def transform_point(
        matrix: 'rai.typing.Affine',
        point: 'rai.typing.PointLike'
        ) -> 'rai.typing.Point':
    """Apply transformation to point and return transformed point."""
    # code written by perplexity.ai
    x, y = point
    a, b, c = matrix[0]
    d, e, f = matrix[1]

    # Apply the transformation
    new_x = a * x + b * y + c
    new_y = d * x + e * y + f

    return (new_x, new_y)

