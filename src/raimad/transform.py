"""
transform.py: home to Transform class.

See the docstring of Transform for more information.
"""
from math import degrees

from copy import deepcopy

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

import raimad as rai

class Transform:
    """Transformation: container for affine matrix."""

    _affine: 'rai.typing.Affine'

    def __init__(self) -> None:
        """Initialize a new Transform as an identity transform."""
        self.reset()

    def reset(self) -> None:
        """Reset this transform to be an identity transform."""
        self._affine = rai.affine.identity()

    def transform_xyarray(
            self,
            poly: 'rai.typing.Poly'
            ) -> 'rai.typing.Poly':  # TODO rename xyarray to polygon
        """
        Apply transformation to xyarray and return new transformed xyarray.

        Parameters
        ----------
        poly : rai.typing.Poly
            The Poly to transform

        Returns
        -------
        rai.typing.Poly
            The new, transformed, Poly
        """
        return rai.affine.transform_xyarray(self._affine, poly)

    def transform_point(
            self,
            point: 'rai.typing.PointLike'
            ) -> 'rai.typing.Point':
        """
        Apply this transform to a point, and return the transformed point.

        A Point (tuple of two floats) is always returned,
        even if a BoundPoint is passed in.

        Parameters
        ----------
        point : rai.typing.PointLike
            The point to transform.

        Returns
        -------
        rai.typing.Point
            The transformed point.
        """
        return rai.affine.transform_point(self._affine, point)

    def compose(self, transform: Self) -> Self:
        """
        Apply a different transform to this transform.

        Parameters
        ----------
        transform : Self
            The other transform to apply to this one

        Returns
        -------
        Self
            This transform is returned to allow method chaining.
        """
        if transform is not None:
            self._affine = rai.affine.matmul(transform._affine, self._affine)
        return self

    def get_translation(self) -> tuple[float, float]:
        """
        Return how much this transform translates the coordinate plane.

        Returns
        -------
        tuple[float, float]
            The first item is how much the plane is moved
            along the x axis.
            The second item is how much the plane is moved
            along the y axis.
        """
        return rai.affine.get_translation(self._affine)

    def get_rotation(self) -> float:
        """
        Return how much this transform rotates the coordinate plane.

        Returns
        -------
        float
            The angle by which this transform rotates the
            coordinate plane (radians, in the positive orientation)
        """
        return rai.affine.get_rotation(self._affine)

    def get_shear(self) -> float:
        """
        Return a how much this transform shears the coordinate plane.

        Returns
        -------
        float
            A number representing the shear.
        """
        return rai.affine.get_shear(self._affine)

    def get_scale(self) -> tuple[float, float]:
        """
        Return how much this transform scales the x and y axis.

        Returns
        -------
        tuple[float, float]
            The first float is the scaling factor along the x axis.
            The second float is the scaling factor along
            the y axis.
        """
        return rai.affine.get_scale(self._affine)

    def does_translate(self) -> bool:
        """
        Check whether this transform applies a translation.

        Returns
        -------
        bool
            True if the transform translates.
            False otherwise.
        """
        norm = rai.affine.norm(self.get_translation())
        return norm > 0.001  # TODO epsilon

    def does_rotate(self) -> bool:
        """
        Check whether this transform applies a rotation.

        Returns
        -------
        bool
            True if the transform rotates.
            False otherwise.
        """
        return abs(self.get_rotation()) > 0.001  # TODO epsilon

    def does_shear(self) -> bool:
        """
        Check whether this transform applies a shear.

        Returns
        -------
        bool
            True if the transform shears.
            False otherwise.
        """
        return abs(self.get_shear()) > 0.001  # TODO epsilon

    def does_scale(self) -> bool:
        """
        Check whether this transform applies a scale.

        Returns
        -------
        bool
            True if the transform scales.
            False otherwise.
        """
        scale_x, scale_y = self.get_scale()
        # TODO epsilon
        return abs(1 - scale_x) > 0.001 or abs(1 - scale_y) > 0.001

    def __repr__(self) -> str:
        """
        Return string representation of transform.

        Returns
        -------
        str
            A representation of this transform.
        """
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
            f"Rotate {degrees(rotation):.2f}) "
                if does_rotate else '',
            f"Shear {shear:.2f} "
                if does_shear else '',
            f"Scale ({scale_x:.2f}, {scale_y:.2f})"
                if does_scale else '',
            ">",
            ))

    def copy(self) -> Self:
        """
        Duplicate transform.

        Returns
        -------
        Self
            The copied transform.
        """
        return deepcopy(self)

    # TODO typing.point
    # types defined in own files
    # then mergen in rai.typing
    # or just PointType, CompoClassType, etc
    def move(self, x: float, y: float) -> Self:
        """
        Move transform.

        Parameters
        ----------
        x : float
            Move this many units along x axis.
        y : float
            Move this many units along y axis.

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(rai.affine.move(x, y), self._affine)
        return self

    def movex(self, x: float = 0) -> Self:
        """
        Move along x axis.

        Parameters
        ----------
        x : float
            Move this many units along x axis.

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(rai.affine.move(x, 0), self._affine)
        return self

    def movey(self, y: float = 0) -> Self:
        """
        Move along y axis.

        Parameters
        ----------
        y : float
            Move this many units along y axis.

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(rai.affine.move(0, y), self._affine)
        return self

    def scale(self, x: float, y: float | None = None) -> Self:
        """
        Scale a transform.

        Parameters
        ----------
        x : float
            Factor to scale by along the x axis
        y : float
            Factor to scale by along the y axis.
            If unspecified or None,
            use the x scale factor.

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
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
        """
        Rotate around a point.

        Parameters
        ----------
        angle : float
            Angle to rotate by, in radians.
        x : float
            Rotate around this point (x coordinate)
            default: origin
        y : float
            Rotate around this point (y coordinate)
            default: origin

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.rotate(angle), x, y),
            self._affine
            )

        return self

    def hflip(self, x: float = 0) -> Self:
        """
        Flip (mirror) along horizontal axis.

        Parameters
        ----------
        x : float
            Flip around this horizontal line (y coordinate)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.scale(1, -1), 0, x),
            self._affine
            )
        return self

    def vflip(self, y: float = 0) -> Self:
        """
        Flip (mirror) along vertical axis.

        Parameters
        ----------
        y : float
            Flip around this vertical line (y coordinate)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.scale(-1, 1), y, 0),
            self._affine
            )
        return self

    def flip(self, x: float = 0, y: float = 0) -> Self:
        """
        Flip (mirror) along both horizontal and vertical axis.

        Parameters
        ----------
        x : float
            Flip around this point (x coordinate)
        y : float
            Flip around this point (y coordinate)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.scale(-1, -1), x, y),
            self._affine
            )
        return self

