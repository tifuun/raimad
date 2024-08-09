from copy import deepcopy

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

import numpy as np
import raimad as rai

class Transform:
    """
    Transformation: container for affine matrix
    """

    _affine: 'rai.typing.Affine'

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._affine = rai.affine.identity()

    def transform_xyarray(
            self,
            poly: 'rai.typing.Poly'
            ) -> 'rai.typing.Poly':
        """
        Apply transformation to xyarray and return new transformed xyarray
        """
        return rai.affine.transform_xyarray(self._affine, poly)

    def transform_point(
            self,
            point: 'rai.typing.PointLike'
            ) -> 'rai.typing.Point':
        """
        Apply transformation to point and return new transformed point
        """
        return rai.affine.transform_point(self._affine, point)

    def compose(self, transform: Self) -> Self:
        """
        Apply a transform to this transform
        """
        if transform is not None:
            self._affine = rai.affine.matmul(transform._affine, self._affine)
        return self

    def get_translation(self) -> tuple[float, float]:
        return rai.affine.get_translation(self._affine)

    def get_rotation(self) -> float:
        return rai.affine.get_rotation(self._affine)

    def get_shear(self) -> float:
        return rai.affine.get_shear(self._affine)

    def get_scale(self) -> tuple[float, float]:
        return rai.affine.get_scale(self._affine)

    def does_translate(self) -> bool:
        norm = rai.affine.norm(self.get_translation())
        return norm > 0.001  # TODO epsilon

    def does_rotate(self) -> bool:
        return abs(self.get_rotation()) > 0.001  # TODO epsilon

    def does_shear(self) -> bool:
        return abs(self.get_shear()) > 0.001  # TODO epsilon

    def does_scale(self) -> bool:
        scale_x, scale_y = self.get_scale()
        # TODO epsilon
        return abs(1 - scale_x) > 0.001 or abs(1 - scale_y) > 0.001

    def __repr__(self) -> str:
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
            f"Rotate {np.rad2deg(rotation):.2f}) "
                if does_rotate else '',
            f"Shear {shear:.2f} "
                if does_shear else '',
            f"Scale ({scale_x:.2f}, {scale_y:.2f})"
                if does_scale else '',
            ">",
            ))

    def copy(self) -> Self:
        return deepcopy(self)

    # TODO typing.point
    # types defined in own files
    # then mergen in rai.typing
    # or just PointType, CompoClassType, etc
    def move(self, x: float, y: float) -> Self:
        self._affine = rai.affine.matmul(rai.affine.move(x, y), self._affine)
        return self

    def movex(self, x: float = 0) -> Self:
        self._affine = rai.affine.matmul(rai.affine.move(x, 0), self._affine)
        return self

    def movey(self, y: float = 0) -> Self:
        self._affine = rai.affine.matmul(rai.affine.move(0, y), self._affine)
        return self

    def scale(self, x: float, y: float | None = None) -> Self:
        if y is None:
            y = x
        self._affine = rai.affine.matmul(rai.affine.scale(x, y), self._affine)
        return self

    def rotate(
            self,
            angle: float,
            x: float = 0,
            y: float = 0
            ) -> Self:

        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.rotate(angle), x, y),
            self._affine
            )

        return self

    def hflip(self, x: float = 0) -> Self:
        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.scale(1, -1), 0, x),
            self._affine
            )
        return self

    def vflip(self, y: float = 0) -> Self:
        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.scale(-1, 1), y, 0),
            self._affine
            )
        return self

    def flip(self, x: float = 0, y: float = 0) -> Self:
        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.scale(-1, -1), x, y),
            self._affine
            )
        return self

