from copy import deepcopy
from typing import Self

import numpy as np
import pycif as pc

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
        return pc.affine.transform_xyarray(self._affine, xyarray)

    def transform_point(self, point):
        """
        Apply transformation to point and return new transformed point
        """
        return pc.affine.transform_point(self._affine, point)

    def compose(self, transform):
        """
        Apply a transform to this transform
        """
        self._affine = transform._affine @ self._affine
        return self

    def get_translation(self):
        return pc.affine.get_translation(self._affine)

    def get_rotation(self):
        return pc.affine.get_rotation(self._affine)

    def get_shear(self):
        return pc.affine.get_shear(self._affine)

    def get_scale(self):
        return pc.affine.get_scale(self._affine)

    def does_translate(self):
        return np.linalg.norm(self.get_translation()) > 0.001  # TODO epsilon

    def does_rotate(self):
        return abs(self.get_rotation()) > 0.001  # TODO epsilon

    def does_shear(self):
        return abs(self.get_shear()) > 0.001  # TODO epsilon

    def does_scale(self):
        return 1 - np.linalg.norm(self.get_scale()) > 0.001  # TODO epsilon

    def __repr__(self):
        does_translate = self.does_translate()
        does_rotate = self.does_rotate()
        does_shear = self.does_shear()
        does_scale = self.does_scale()

        move_x, move_y = self.get_scale()
        rotation = self.get_rotation()
        shear = self.get_shear()
        scale_x, scale_y = self.get_scale()

        if True not in {does_translate, does_rotate, does_shear, does_scale}:
            # Could also test if affine == identity
            return "<Identity Transform>"

        return ''.join((
            "<Transform ",
            f"Move ({move_x:+.2f}, {move_y:+.2f}) "
                if does_translate else '',
            f"Rotate {pc.rad2deg(rotation):.2f}) "
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
        self._affine = pc.affine.move(x, y) @ self._affine
        return self

    def movex(self, x: float = 0) -> Self:
        self._affine = pc.affine.move(x, 0) @ self._affine
        return self

    def movey(self, y: float = 0) -> Self:
        self._affine = pc.affine.move(0, y) @ self._affine
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

    #    self._affine = pc.affine.around(pc.affine.scale(x, y), cx, cy) @ self._affine
    #    return self
    def scale(self, x, y=None):
        if y is None:
            y = x
        self._affine = pc.affine.scale(x, y) @ self._affine
        return self

    def rotate(
            self,
            angle: float,
            x: float | pc.Point = 0,
            y: float = 0
            ) -> Self:

        if isinstance(x, pc.Point):
            x, y = x

        self._affine = pc.affine.around(pc.affine.rotate(angle), x, y) @ self._affine

        return self

    def hflip(self, x: float = 0) -> Self:
        self._affine = pc.affine.around(pc.affine.scale(1, -1), 0, x) @ self._affine
        return self

    def vflip(self, y: float = 0) -> Self:
        self._affine = pc.affine.around(pc.affine.scale(-1, 1), y, 0) @ self._affine
        return self

    def flip(self, x: float = 0, y: float = 0) -> Self:
        self._affine = pc.affine.around(pc.affine.scale(-1, -1), x, y) @ self._affine
        return self

    def inverse(self):
        self._affine = np.linalg.inv(self._affine)
        return self

