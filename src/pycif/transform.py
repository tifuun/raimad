from copy import deepcopy
from typing import Self

import numpy as np
import pycif as pc

def _rot(angle):
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1],
        ])

def _mov(x, y):
    return np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1],
        ])

def _scale(x, y):
    return np.array([
        [x, 0, 0],
        [0, y, 0],
        [0, 0, 1],
        ])

def _around(matrix, x, y):
    to_origin = _mov(-x, -y)
    from_origin = _mov(x, y)

    return from_origin @ matrix @ to_origin

def get_translation(matrix):
    """
    Given an affine matrix, return the corresponding translation.
    Written by ChatGPT
    """
    return matrix[:2, 2]

def get_scale_shear(matrix):
    """
    Given an affine matrix, return the corresponding scale and shear.
    Written by ChatGPT
    """
    scale_x = np.linalg.norm(matrix[:, 0])
    scale_y = np.linalg.norm(matrix[:, 1])
    shear = np.dot(matrix[:, 0], matrix[:, 1]) / (scale_x * scale_y)
    return scale_x, scale_y, shear

def get_rotation(matrix):
    """
    Given an affine matrix, return the corresponding rotation
    Written by ChatGPT
    """
    return np.arctan2(matrix[1, 0], matrix[0, 0])


class Transform(object):
    """
    Transformation: container for affine matrix
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self._affine = np.identity(3)

    def transform_xyarray(self, xyarray: np.ndarray):
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
        transformed = np.dot(homogeneous, self._affine.T)
        euclidean = transformed[:, :2] / transformed[:, 2].reshape(-1, 1)

        return euclidean

    def transform_point(self, point):
        """
        Apply transformation to point and return new transformed point
        """
        homogeneous = np.append(point, 1)
        transformed = np.dot(homogeneous, self._affine.T)
        cartesian = transformed[:2] / transformed[2]

        return np.array(cartesian)

    def compose(self, transform):
        """
        Apply a transform to this transform
        """
        self._affine = transform._affine @ self._affine
        return self

    def __repr__(self):
        move_x, move_y = get_translation(self._affine)
        scale_x, scale_y, shear = get_scale_shear(self._affine)
        rotation = get_rotation(self._affine)

        does_translate = np.linalg.norm((move_x, move_y)) > 0.001  # TODO epsilon
        does_rotate = rotation > 0.01
        does_shear = shear > 0.01
        does_scale = 1 - np.linalg.norm((scale_x, scale_y)) > 0.001

        if True not in {does_translate, does_rotate, does_shear, does_scale}:
            # Could also test if affine == identity
            return "<Identity Transform>"

        return ''.join((
            "<Transform ",
            f"Move ({move_x:+.2f}, {move_y:+.2f}) "
                if does_translate else '',
            f"Rotate {pc.radians(rotation):.2f}) "
                if does_rotate else '',
            f"Shear {shear:.2f} "
                if does_shear else '',
            f"Scale ({scale_x:.2f}, {scale_y:.2f})"
                if does_scale else '',
            ">",
            ))

    def copy(self):
        return deepcopy(self)

    # TODO typing.point
    # types defined in own files
    # then mergen in pc.typing
    # or just PointType, CompoClassType, etc
    def move(self, x: 0, y: float = 0):
        if isinstance(x, pc.Point):
            x, y = x
        self._affine = _mov(x, y) @ self._affine
        return self

    def movex(self, x: float = 0) -> Self:
        self._affine = _mov(x, 0) @ self._affine
        return self

    def movey(self, y: float = 0) -> Self:
        self._affine = _mov(0, y) @ self._affine
        return self

    #def scale(
    #        self,
    #        x: float | pc.Point,  # TODO typing.point
    #        y: float | None = None,
    #        cx: float = 0,
    #        cy: float = 0,
    #        ) -> Self:

    #    if isinstance(x, pc.Point):
    #        x, y = x

    #    elif y is None:
    #        y = x

    #    self._affine = _around(_scale(x, y), cx, cy) @ self._affine
    #    return self
    def scale(self, x, y=None):
        if y is None:
            y = x
        self._affine = _scale(x, y) @ self._affine
        return self

    def rotate(
            self,
            angle: float,
            x: float | pc.Point = 0,
            y: float = 0
            ) -> Self:

        if isinstance(x, pc.Point):
            x, y = x

        self._affine = _around(_rot(angle), x, y) @ self._affine

        return self

    def hflip(self, x: float = 0) -> Self:
        self._affine = _around(_scale(1, -1), 0, x) @ self._affine
        return self

    def vflip(self, y: float = 0) -> Self:
        self._affine = _around(_scale(-1, 1), y, 0) @ self._affine
        return self

    def flip(self, x: float = 0, y: float = 0) -> Self:
        self._affine = _around(_scale(-1, -1), x, y) @ self._affine
        return self

    def inverse(self):
        self._affine = np.linalg.inv(self._affine)
        return self

