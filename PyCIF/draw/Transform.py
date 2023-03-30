import inspect
from dataclasses import dataclass
from typing import Self, ClassVar, Tuple

import numpy as np

from PyCIF.helpers import encapsulation
from PyCIF.helpers.hackery import new_without_init


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


@encapsulation.expose_class
class Transform(object):
    """
    Transformation: container for affine matrix
    """

    def __init__(self):
        self._affine = np.identity(3)

    def transform_xyarray(self, xyarray: np.ndarray):
        """
        Apply transformation to xyarray and return new transformed xyarray
        """
        if len(xyarray) == 0:
            return xyarray

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

        return cartesian

    @encapsulation.exposable
    def apply_transform(self, transform: Self):
        """
        Apply a transform to this transform
        """
        self._affine = transform._affine @ self._affine
        return self

    def __str__(self):
        return self._affine.__str__()

    #def copy(self) -> Self:
    #    new_transform = new_without_init(self.__class__)
    #    new_transform.translate_x = self.translate_x
    #    new_transform.translate_y = self.translate_y
    #    new_transform.angle = self.angle
    #    return new_transform

    #__copy__ = copy

    #def __str__(self):
    #    return '[\n%s]\b]' % ''.join([f'\t{action}\n' for action in self.history])

    #@encapsulation.exposable
    #def apply_transform(self, other: Self) -> Self:
    #    """
    #    Apply another Transform to this Transform.
    #    """
    #    #self.history.extend(other.history)
    #    return self

    @encapsulation.exposable
    def move(self, x: float = 0, y: float = 0) -> Self:
        self._affine = _mov(x, y) @ self._affine
        return self
        #arr = np.array((x, y), np.float64)
        #arr = self.transform_xyarray(arr)
        #x = float(arr[0])
        #y = float(arr[1])
        #self.history.append((_move, x, y))
        #return self

    #@encapsulation.exposable
    #def movex(self, x: float) -> Self:
    #    self.history.append((_move, x, 0))
    #    return self

    #@encapsulation.exposable
    #def movey(self, y: float) -> Self:
    #    self.history.append((_move, 0, y))
    #    return self

    #@encapsulation.exposable
    #def scale(self, x: float, y: float | None = None) -> Self:
    #    self.history.append((_scale, x, x if y is None else y))
    #    return self

    @encapsulation.exposable
    def rotate(self, angle: float, x: float = 0, y: float = 0) -> Self:
        to_origin = _mov(-x, -y)
        rot = _rot(angle)
        from_origin = _mov(x, y)

        rotaround = from_origin @ rot @ to_origin
        self._affine = rotaround @ self._affine

        return self

    #@encapsulation.exposable
    #def hflip(self) -> Self:
    #    self.history.append((_scale, 1, -1))
    #    return self

    #@encapsulation.exposable
    #def vflip(self) -> Self:
    #    self.history.append((_scale, -1, 1))
    #    return self

    #@encapsulation.exposable
    #def flip(self) -> Self:
    #    self.history.append((_scale, -1, -1))
    #    return self

