"""
transform.py: home to Transform class.

See the docstring of Transform for more information.
"""
from typing import overload, Sequence
from types import NoneType
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

    #-------------#
    # Rotate      #
    #-------------#

    def crotate(
            self,
            angle: float,
            x: float = 0,
            y: float = 0
            ) -> Self:
        """
        Rotate around a point given by x and y coordinate.

        Parameters
        ----------
        angle : float
            Angle to rotate by, in radians.
        x : float
            Rotate around this point (x coordinate)
            default: 0
        y : float
            Rotate around this point (y coordinate)
            default: 0

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

    def protate(
            self,
            angle: float,
            pivot: 'rai.typing.Point' = (0, 0),
            ) -> None:
        """
        Rotate around a reference point given as an (x, y) tuple.

        Parameters
        ----------
        angle : float
            Angle to rotate by, in radians.
        pivot : 'rai.typing.Point'
            The point (x, y) to rotate around. Default: origin.

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.rotate(angle), pivot[0], pivot[1]),
            self._affine
            )

        return self

    @overload
    def rotate(self, angle: float, x: float, y: float) -> None: ...
    @overload
    def rotate(self, angle: float, pivot: 'rai.typing.Point') -> None: ...

    def rotate(
            self,
            angle: float,
            a: 'float | rai.typing.Point',
            b: float | None = None
            ) -> None:
        """
        TODO overloaded docstrings??
        """
        if (
                isinstance(a, float | int) and
                isinstance(b, float | int)
                ):
            self.crotate(angle, a, b)
        elif (
                isinstance(a, Sequence) and
                isinstance(b, NoneType)
                ):
            self.protate(angle, a)
        elif (
                isinstance(a, NoneType) and
                isinstance(b, NoneType)
                ):
            self.protate(angle)
        else:
            # TODO custom type?
            raise TypeError(f"foobar {a}, {b}")

        return self


    #-------------#
    # Move        #
    #-------------#

    def cmove(
            self,
            x: float = 0,
            y: float = 0
            ) -> Self:
        """
        Translate by x and y.

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

    def pmove(
            self,
            offset: 'rai.typing.Point'
            ) -> None:
        """
        Translate by x and y, given as a tuple.

        Parameters
        ----------
        offset : 'rai.typing.Point'
            A tuple of two values (x, y).

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
                rai.affine.move(offset[0], offset[1]),
                self._affine)

        return self

    @overload
    def move(self, x: float, y: float) -> None: ...
    @overload
    def move(self, offset: 'rai.typing.Point') -> None: ...

    def move(
            self,
            a: 'float | rai.typing.Point',
            b: float | None = None
            ) -> None:
        """
        TODO overloaded docstrings??
        """
        if isinstance(a, tuple):
            self.pmove(a)
        elif b is not None:
            self.cmove(a, b)
        else:
            # TODO custom type?
            raise TypeError("foobar")

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

    #-------------#
    # Flip        #
    #-------------#

    def cflip(
            self,
            x: float = 0,
            y: float = 0
            ) -> Self:
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

    def pflip(
            self,
            pivot: 'rai.typing.Point'
            ) -> None:
        """
        Flip (mirror) along both horizontal and vertical axis (tuple).

        Parameters
        ----------
        pivot: 'rai.typing.Point'
            Tuple representing x and y coordinates of lines to mirror
            against

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(
                rai.affine.scale(-1, -1),
                pivot[0], pivot[1],
                ),
            self._affine
            )

    @overload
    def flip(self, x: float, y: float) -> None: ...
    @overload
    def flip(self, offset: 'rai.typing.Point') -> None: ...

    def flip(
            self,
            a: 'float | rai.typing.Point',
            b: float | None = None
            ) -> None:
        """
        TODO overloaded docstrings??
        """
        if (
                isinstance(a, float | int) and
                isinstance(b, float | int)
                ):
            self.cflip(a, b)
        elif (
                isinstance(a, Sequence) and
                isinstance(b, NoneType)
                ):
            self.pflip(a)
        else:
            # TODO custom type?
            raise TypeError(f"foobar {a}, {b}")

        return self


    def vflip(self, y: float = 0) -> Self:
        """
        Flip (mirror) along horizontal axis.

        Parameters
        ----------
        y : float
            Flip around this horizontal line (y coordinate)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.scale(1, -1), 0, y),
            self._affine
            )
        return self

    def hflip(self, x: float = 0) -> Self:
        """
        Flip (mirror) along vertical axis.

        Parameters
        ----------
        x : float
            Flip around this vertical line (x coordinate)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.scale(-1, 1), x, 0),
            self._affine
            )
        return self

    #-------------#
    # Scale       #
    #-------------#

    def cpscale(
            self,
            x: float,
            y: float,
            pivot: 'rai.typing.Point' = (0, 0),
            ) -> Self:
        """
        Scale width and height (two floats) around pivot point (tuple)

        Parameters
        ----------
        x : float
            Factor to scale by along the x axis
        y : float
            Factor to scale by along the y axis.
        pivot : rai.typing.Point | None
            Use this point as origin for the scale.
            Default: origin

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(
                rai.affine.scale(x, y),
                pivot[0], pivot[1]
                ),
            self._affine
            )

        return self

    def ccscale(
            self,
            x: float,
            y: float,
            px: float = 0,
            py: float = 0,
            ) -> Self:
        """
        Scale width and height (two floats) around pivot point (two floats)

        Parameters
        ----------
        x : float
            Factor to scale by along the x axis
        y : float
            Factor to scale by along the y axis.
        px : float
            X coordinate of origin of the scale (default: 0)
        py : float
            Y coordinate of origin of the scale (default: 0)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(
                rai.affine.scale(x, y),
                px, py
                ),
            self._affine
            )

        return self

    def ppscale(
            self,
            scale: 'rai.typing.Point',
            pivot: 'rai.typing.Point' = (0, 0),
            ) -> Self:
        """
        Scale width and height (tuple) around pivot point (tuple)

        Parameters
        ----------
        scale : 'rai.typing.Point'
            The x and y scale factors
        pivot : rai.typing.Point
            Use this point as origin for the scale.
            Default: origin

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(
                rai.affine.scale(
                    scale[0], scale[1]
                    ),
                pivot[0], pivot[1]
                ),
            self._affine
            )
        return self

    def pcscale(
            self,
            scale: 'rai.typing.Point',
            px: float = 0,
            py: float = 0,
            ) -> Self:
        """
        Scale width and height (tuple) around pivot point (two floats)

        Parameters
        ----------
        scale : 'rai.typing.Point'
            The x and y scale factors
           `None` means origin.
        px : float
            X coordinate of origin of the scale (default: 0)
        py : float
            Y coordinate of origin of the scale (default: 0)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
            rai.affine.around(
                rai.affine.scale(
                    scale[0], scale[1]
                    ),
                px, py
                ),
            self._affine
            )
        return self

    def apscale(
            self,
            factor: float,
            pivot: 'rai.typing.Point' = (0, 0),
            ) -> Self:
        """
        Scale both width and height by same factor around pivot (tuple)

        Parameters
        ----------
        factor : float
            Factor to scale by.
        pivot : rai.typing.Point | None
            Use this point as origin for the scale.
            Default: origin

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
                rai.affine.around(
                    rai.affine.scale(factor, factor),
                    pivot[0], pivot[1]
                    ),
                self._affine
                )
        return self

    def acscale(
            self,
            factor: float,
            px: float = 0,
            py: float = 0,
            ) -> Self:
        """
        Scale both width and height by same factor around pivot (two floats)

        Parameters
        ----------
        factor : float
            Factor to scale by.
        px : float
            X coordinate of origin of the scale (default: 0)
        py : float
            Y coordinate of origin of the scale (default: 0)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        self._affine = rai.affine.matmul(
                rai.affine.around(
                    rai.affine.scale(factor, factor),
                    px, py
                    ),
                self._affine
                )
        return self

    # TODO
    @overload
    def scale(self, x: float, y: float) -> None: ...
    @overload
    def scale(self, scale: 'rai.typing.Point') -> None: ...
    @overload
    def scale(self, factor: float) -> None: ...

    def scale(
            self, a, b, c, d
            ) -> None:
        """
        TODO overloaded docstrings??
        """
        # "Mom, can we have structural pattern matching?"
        # "We have structural pattern matching at python39"
        # Structural pattern matching at python39:

        if (
                isinstance(a, float | int) and
                isinstance(b, float | int) and
                isinstance(c, float | int) and
                isinstance(d, float | int)
                ):
            return self.ccscale(a, b, c, d)
        if (
                isinstance(a, Sequence) and
                isinstance(b, Sequence) and
                isinstance(c, NoneType) and
                isinstance(d, NoneType)
                ):
            return self.ppscale(a, b)
        if (
                isinstance(a, float | int) and
                isinstance(b, float | int) and
                isinstance(c, Sequence) and
                isinstance(d, NoneType)
                ):
            return self.cpscale(a, b, c)
        if (
                isinstance(a, Sequence) and
                isinstance(b, float | int) and
                isinstance(c, float | int) and
                isinstance(d, NoneType)
                ):
            return self.pcscale(a, b, c)
        if (
                isinstance(a, float | int) and
                isinstance(b, float | int) and
                isinstance(c, float | int) and
                isinstance(d, NoneType)
                ):
            return self.acscale(a, b, c)
        if (
                isinstance(a, Sequence) and
                isinstance(b, NoneType) and
                isinstance(c, NoneType) and
                isinstance(d, NoneType)
                ):
            return self.ppscale(a)
        if (
                isinstance(a, float | int) and
                isinstance(b, float | int) and
                isinstance(c, NoneType) and
                isinstance(d, NoneType)
                ):
            return self.cpscale(a, b)
        if (
                isinstance(a, float | int) and
                isinstance(b, NoneType) and
                isinstance(c, NoneType) and
                isinstance(d, NoneType)
                ):
            return self.acscale(a)
        if (
                isinstance(a, float | int) and
                isinstance(b, Sequence) and
                isinstance(c, NoneType) and
                isinstance(d, NoneType)
                ):
            return self.apscale(a, b)

        raise TypeError(f"foobar {a} {b} {c} {d}")

    #-------------#
    # Extract     #
    #-------------#

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
        return norm > rai.epsilon

    def does_rotate(self) -> bool:
        """
        Check whether this transform applies a rotation.

        Returns
        -------
        bool
            True if the transform rotates.
            False otherwise.
        """
        return abs(self.get_rotation()) > rai.epsilon

    def does_shear(self) -> bool:
        """
        Check whether this transform applies a shear.

        Returns
        -------
        bool
            True if the transform shears.
            False otherwise.
        """
        return abs(self.get_shear()) > rai.epsilon

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
        return abs(1 - scale_x) > rai.epsilon or abs(1 - scale_y) > rai.epsilon

    #-------------#
    # Misc        #
    #-------------#

    def reset(self) -> None:
        """Reset this transform to be an identity transform."""
        self._affine = rai.affine.identity()

    def transform_poly(
            self,
            poly: 'rai.typing.Poly'
            ) -> 'rai.typing.Poly':
        """
        Apply transformation to poly and return new transformed poly.

        Parameters
        ----------
        poly : rai.typing.Poly
            The Poly to transform

        Returns
        -------
        rai.typing.Poly
            The new, transformed, Poly
        """
        return rai.affine.transform_poly(self._affine, poly)

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
        point : 'rai.typing.Point'Like
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

