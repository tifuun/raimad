import inspect
from dataclasses import dataclass
from typing import Self, ClassVar, Tuple

import numpy as np

from PyCIF.helpers import encapsulation
from PyCIF.helpers.hackery import new_without_init

FULL_CIRCLE = 360


def _rot(xyarray, angle, x, y, /):
    radians = np.radians(angle)
    rotmatrix = np.array((
        (np.cos(radians), -np.sin(radians)),
        (np.sin(radians), np.cos(radians)),
        ))

    xyarray -= (x, y)
    xyarray = xyarray @ rotmatrix
    # TODO replace with @= when it becomes implemented.
    xyarray += (x, y)
    return xyarray


@encapsulation.expose_class
class Transform(object):
    """
    Transformation: stores new origin, rotation, x and y scale.
    """

    def __init__(self):
        self.translate_x = 0
        self.translate_y = 0
        self.rotate_x = 0
        self.rotate_y = 0
        self.angle = 0

    def transform_xyarray(self, xyarray: np.ndarray):
        if len(xyarray) == 0:
            return xyarray

        xyarray = _rot(xyarray, self.angle, self.rotate_x, self.rotate_y)
        xyarray += (self.translate_x, self.translate_y)

        return xyarray

    def copy(self) -> Self:
        new_transform = new_without_init(self.__class__)
        new_transform.translate_x = self.translate_x
        new_transform.translate_y = self.translate_y
        new_transform.angle = self.angle
        return new_transform

    __copy__ = copy

    #def __str__(self):
    #    return '[\n%s]\b]' % ''.join([f'\t{action}\n' for action in self.history])

    @encapsulation.exposable
    def apply_transform(self, other: Self) -> Self:
        """
        Apply another Transform to this Transform.
        """
        #self.history.extend(other.history)
        return self

    @encapsulation.exposable
    def move(self, x: float, y: float) -> Self:
        self.translate_x += x
        self.translate_y += y
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

    #@encapsulation.exposable
    #def rot(self, angle: float, x: float = 0, y: float = 0) -> Self:
    #    arr = np.array((x, y), np.float64)
    #    arr = self.transform_xyarray(arr)
    #    x = float(arr[0])
    #    y = float(arr[1])
    #    self.history.append((_rot, angle, x, y))
    #    return self

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

