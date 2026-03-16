"""
transform.py: home to Transform class.

See the docstring of Transform for more information.
"""
from typing import overload
from types import NoneType
from math import degrees

from copy import deepcopy

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

import raimad as rai
from raimad.types import Vec2, Vec2S, PolyS, Num, NumS

class EditingArgumentError(TypeError):
    """
    Invalid arguments are passed to "automatic" editing functions like *.move.
    """
    def __init__(self) -> None:
        super().__init__(f"Invalid arguments passed to editing method.")


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
            angle: Num,
            x: Num = 0,
            y: Num = 0
            ) -> Self:
        """
        Rotate around a point given by x and y coordinate.

        Parameters
        ----------
        angle : Num
            Angle to rotate by, in radians.
        x : Num
            Rotate around this point (x coordinate)
            default: 0
        y : Num
            Rotate around this point (y coordinate)
            default: 0

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        angle = float(angle)
        x = float(x)
        y = float(y)

        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.rotate(angle), x, y),
            self._affine
            )

        return self

    def protate(
            self,
            angle: Num,
            pivot: Vec2S = (0, 0),
            ) -> Self:
        """
        Rotate around a reference point given as an (x, y) tuple.

        Parameters
        ----------
        angle : Num
            Angle to rotate by, in radians.
        pivot : Vec2S
            The point (x, y) to rotate around. Default: origin.

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        angle = float(angle)
        pivot = rai.vec2s(pivot)

        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.rotate(angle), pivot[0], pivot[1]),
            self._affine
            )

        return self

    @overload
    def rotate(self, angle: Num, /) -> Self: ...
    # Trailing `/` is needed for mypy for some reason
    @overload
    def rotate(self, angle: Num, /, a: Num, b: Num) -> Self: ...
    @overload
    def rotate(self, angle: Num, /, a: Vec2) -> Self: ...

    def rotate(
            self,
            angle: Num,
            /,
            a: Num | Vec2 | None = None,
            b: Num | None = None,
            ) -> Self:
        """
        Rotate around a pivot point (overload).

        This is an overloaded method that can take the position of the pivot
        point either as two separate x and y arguments, or as a single tuple
        of two values.

        Parameters
        ----------
        angle : Num
            Angle to rotate by, in radians.
        a : Num | Vec2S
            Either the X coordinate, the entire pivot point,
            or None
        b : Num | None
            Either the Y coordinate or None

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        # `Isinstance` check is against Num
        # to support weird things like mypy numbers
        # which we then convert to regular float

        angle_float = float(angle)

        if (
                isinstance(a, Num) and
                isinstance(b, Num)
                ):
            self.crotate(angle_float, float(a), float(b))
        elif (
                isinstance(a, Vec2) and
                isinstance(b, NoneType)
                ):
            self.protate(angle_float, rai.vec2s(a))
        elif (
                isinstance(a, NoneType) and
                isinstance(b, NoneType)
                ):
            self.protate(angle_float)
        else:
            raise EditingArgumentError()

        return self


    #-------------#
    # Move        #
    #-------------#

    def cmove(
            self,
            x: Num = 0,
            y: Num = 0
            ) -> Self:
        """
        Translate by x and y.

        Parameters
        ----------
        x : Num
            Move this many units along x axis.
        y : Num
            Move this many units along y axis.

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        x = float(x)
        y = float(y)

        self._affine = rai.affine.matmul(rai.affine.move(x, y), self._affine)

        return self

    def pmove(
            self,
            offset: Vec2,
            ) -> Self:
        """
        Translate by x and y, given as a tuple.

        Parameters
        ----------
        offset : Vec2S
            A tuple of two values (x, y).

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        offset = rai.vec2s(offset)

        self._affine = rai.affine.matmul(
                rai.affine.move(offset[0], offset[1]),
                self._affine)

        return self

    @overload
    def move(self, /, a: Num, b: Num) -> Self: ...
    @overload
    def move(self, /, a: Vec2S) -> Self: ...

    def move(
            self,
            /,
            a: Num | Vec2,
            b: Num | None = None,
            ) -> Self:
        """
        Translate vertically and horizontally (overload).

        This is an overloaded method that can take the X and Y offsets either
        as two separate x and y arguments, or as a single tuple of two values.

        Parameters
        ----------
        a : Num | Vec2S
            X offset or tuple of offsets
        b : Num | None
            Y offset or None

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        # `Isinstance` check is against Num
        # to support weird things like mypy numbers
        # which we then downcast to regular float
        if (
                isinstance(a, Num) and
                isinstance(b, Num)
                ):
            self.cmove(float(a), float(b))
        elif (
                isinstance(a, Vec2) and
                isinstance(b, NoneType)
                ):
            self.pmove(a)
        else:
            raise EditingArgumentError()

        return self

    def movex(self, x: Num = 0) -> Self:
        """
        Move along x axis.

        Parameters
        ----------
        x : Num
            Move this many units along x axis.

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        x = float(x)
        self._affine = rai.affine.matmul(rai.affine.move(x, 0), self._affine)
        return self

    def movey(self, y: Num = 0) -> Self:
        """
        Move along y axis.

        Parameters
        ----------
        y : Num
            Move this many units along y axis.

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        y = float(y)
        self._affine = rai.affine.matmul(rai.affine.move(0, y), self._affine)
        return self

    #-------------#
    # Flip        #
    #-------------#

    def cflip(
            self,
            x: Num = 0,
            y: Num = 0
            ) -> Self:
        """
        Flip (mirror) along both horizontal and vertical axis.

        Parameters
        ----------
        x : Num
            Flip around this point (x coordinate)
        y : Num
            Flip around this point (y coordinate)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        x = float(x)
        y = float(y)

        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.scale(-1, -1), x, y),
            self._affine
            )
        return self

    def pflip(
            self,
            pivot: Vec2
            ) -> Self:
        """
        Flip (mirror) along both horizontal and vertical axis (tuple).

        Parameters
        ----------
        pivot: Vec2S
            Tuple representing x and y coordinates of lines to mirror
            against

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        pivot = rai.vec2s(pivot)

        self._affine = rai.affine.matmul(
            rai.affine.around(
                rai.affine.scale(-1, -1),
                pivot[0], pivot[1],
                ),
            self._affine
            )
        return self

    @overload
    def flip(self, /, a: Num, b: Num) -> Self: ...
    @overload
    def flip(self, /, a: Vec2) -> Self: ...

    def flip(
            self,
            /,
            a: Num | Vec2,
            b: Num | None = None,
            ) -> Self:
        """
        Flip (mirror) along both horizontal and vertical axis.

        This is an overloaded method that can take the X and Y intercepts of
        the two mirroring lines either as two separate x and y arguments, or as
        a single tuple of two values.

        Parameters
        ----------
        a : Num | Vec2S
            Either the x-intercept or a tuple of the two intercepts.
        b : Num | None
            Either the y-intercept or None

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        # `Isinstance` check is against Num
        # to support weird things like mypy numbers
        # which we then downcast to regular float
        if (
                isinstance(a, Num) and
                isinstance(b, Num)
                ):
            self.cflip(float(a), float(b))
        elif (
                isinstance(a, Vec2) and
                isinstance(b, NoneType)
                ):
            self.pflip(a)
        else:
            raise EditingArgumentError()

        return self


    def vflip(self, y: Num = 0) -> Self:
        """
        Flip (mirror) along horizontal axis.

        Parameters
        ----------
        y : Num
            Flip around this horizontal line (y coordinate)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        y = float(y)

        self._affine = rai.affine.matmul(
            rai.affine.around(rai.affine.scale(1, -1), 0, y),
            self._affine
            )
        return self

    def hflip(self, x: Num = 0) -> Self:
        """
        Flip (mirror) along vertical axis.

        Parameters
        ----------
        x : Num
            Flip around this vertical line (x coordinate)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        x = float(x)

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
            x: Num,
            y: Num,
            pivot: Vec2 = (0, 0),
            ) -> Self:
        """
        Scale width and height (two Nums) around pivot point (tuple)

        Parameters
        ----------
        x : Num
            Factor to scale by along the x axis
        y : Num
            Factor to scale by along the y axis.
        pivot : Vec2S
            Use this point as origin for the scale.
            Default: origin

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        x = float(x)
        y = float(y)
        pivot = rai.vec2s(pivot)

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
            x: Num,
            y: Num,
            px: Num = 0,
            py: Num = 0,
            ) -> Self:
        """
        Scale width and height (two Nums) around pivot point (two Nums)

        Parameters
        ----------
        x : Num
            Factor to scale by along the x axis
        y : Num
            Factor to scale by along the y axis.
        px : Num
            X coordinate of origin of the scale (default: 0)
        py : Num
            Y coordinate of origin of the scale (default: 0)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        x = float(x)
        y = float(y)
        px = float(px)
        py = float(py)

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
            scale: Vec2,
            pivot: Vec2 = (0, 0),
            ) -> Self:
        """
        Scale width and height (tuple) around pivot point (tuple)

        Parameters
        ----------
        scale : Vec2S
            The x and y scale factors
        pivot : Vec2S
            Use this point as origin for the scale.
            Default: origin

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        scale = rai.vec2s(scale)
        pivot = rai.vec2s(pivot)

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
            scale: Vec2,
            px: Num = 0,
            py: Num = 0,
            ) -> Self:
        """
        Scale width and height (tuple) around pivot point (two Nums)

        Parameters
        ----------
        scale : Vec2S
            The x and y scale factors
        px : Num
            X coordinate of origin of the scale (default: 0)
        py : Num
            Y coordinate of origin of the scale (default: 0)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        scale = rai.vec2s(scale)
        px = float(px)
        py = float(py)

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
            factor: Num,
            pivot: Vec2 = (0, 0),
            ) -> Self:
        """
        Scale both width and height by same factor around pivot (tuple)

        Parameters
        ----------
        factor : Num
            Factor to scale by.
        pivot : Vec2S
            Use this point as origin for the scale.
            Default: origin

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        factor = float(factor)
        pivot = rai.vec2s(pivot)

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
            factor: Num,
            px: Num = 0,
            py: Num = 0,
            ) -> Self:
        """
        Scale both width and height by same factor around pivot (two Nums)

        Parameters
        ----------
        factor : Num
            Factor to scale by.
        px : Num
            X coordinate of origin of the scale (default: 0)
        py : Num
            Y coordinate of origin of the scale (default: 0)

        Returns
        -------
        Self
            This transform is returned to allow chaining methods.
        """
        factor = float(factor)
        px = float(px)
        py = float(py)

        self._affine = rai.affine.matmul(
                rai.affine.around(
                    rai.affine.scale(factor, factor),
                    px, py
                    ),
                self._affine
                )
        return self

    @overload
    def scale(self, /, a: Num ,                             ) -> Self: ...
    @overload
    def scale(self, /, a: Num ,          b: Vec2S,          ) -> Self: ...
    @overload
    def scale(self, /, a: Num ,          b: Num , c: Num  ) -> Self: ...
    @overload
    def scale(self, /, a: Num , b: Num                     ) -> Self: ...
    @overload
    def scale(self, /, a: Vec2S,                             ) -> Self: ...
    @overload
    def scale(self, /, a: Num , b: Num, c: Vec2S,          ) -> Self: ...
    @overload
    def scale(self, /, a: Vec2S,          b: Vec2S,          ) -> Self: ...
    @overload
    def scale(self, /, a: Num , b: Num, c: Num , d: Num, ) -> Self: ...
    @overload
    def scale(self, /, a: Vec2S,          b: Num , c: Num  ) -> Self: ...

    def scale(
            self,
            /,
            a: Num | Vec2S,
            b: Num | Vec2S | None = None,
            c: Num | Vec2S | None = None,
            d: Num | None = None,
            ) -> Self:
        """
        Scale width and height around a pivot point (overload).

        This is an overloaded function. It can take:
        - single scale factor
            - `self.scale(5)`
        - single scale factor and pivot point (tuple)
            - `self.scale(5, (1, 1))`
        - single scale factor and pivot point (separate values)
            - `self.scale(5, 1, 1)`
        - x, y scale factors (separate values)
            - `self.scale(5, 4)`
        - x, y scale factors (tuple)
            - `self.scale((5, 4))`
        - x, y scale factors (separate values) and pivot (tuple)
            - `self.scale(5, 4, (1, 1))`
        - x, y scale factors (tuple) and pivot (tuple)
            - `self.scale((5, 4), (1, 1))`
        - x, y scale factors (separate values) and pivot (separate values)
            - `self.scale(5, 4, 1, 1)`
        - x, y scale factors (tuple) and pivot (separate values)
            - `self.scale((5, 4), 1, 1)`

        Returns
        -------
        Self
            This transform is returned to allow method chaining.
        """
        # "Mom, can we have structural pattern matching?"
        # "We have structural pattern matching at python39"
        # Structural pattern matching at python39:

        if (
                isinstance(a, Num) and
                isinstance(b, Num) and
                isinstance(c, Num) and
                isinstance(d, Num)
                ):
            return self.ccscale(float(a), float(b), float(c), float(d))
        if (
                isinstance(a, Vec2) and
                isinstance(b, Vec2) and
                isinstance(c, NoneType) and
                isinstance(d, NoneType)
                ):
            return self.ppscale(a, b)
        if (
                isinstance(a, Num) and
                isinstance(b, Num) and
                isinstance(c, Vec2) and
                isinstance(d, NoneType)
                ):
            return self.cpscale(float(a), float(b), c)
        if (
                isinstance(a, Vec2) and
                isinstance(b, Num) and
                isinstance(c, Num) and
                isinstance(d, NoneType)
                ):
            return self.pcscale(a, float(b), float(c))
        if (
                isinstance(a, Num) and
                isinstance(b, Num) and
                isinstance(c, Num) and
                isinstance(d, NoneType)
                ):
            return self.acscale(float(a), float(b), float(c))
        if (
                isinstance(a, Vec2) and
                isinstance(b, NoneType) and
                isinstance(c, NoneType) and
                isinstance(d, NoneType)
                ):
            return self.ppscale(a)
        if (
                isinstance(a, Num) and
                isinstance(b, Num) and
                isinstance(c, NoneType) and
                isinstance(d, NoneType)
                ):
            return self.cpscale(float(a), float(b))
        if (
                isinstance(a, Num) and
                isinstance(b, NoneType) and
                isinstance(c, NoneType) and
                isinstance(d, NoneType)
                ):
            return self.acscale(float(a))
        if (
                isinstance(a, Num) and
                isinstance(b, Vec2) and
                isinstance(c, NoneType) and
                isinstance(d, NoneType)
                ):
            return self.apscale(float(a), b)

        raise EditingArgumentError()

    #-------------#
    # Extract     #
    #-------------#

    def get_translation(self) -> Vec2S:
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

    def get_rotation(self) -> NumS:
        """
        Return how much this transform rotates the coordinate plane.

        Returns
        -------
        float
            The angle by which this transform rotates the
            coordinate plane (radians, in the positive orientation)
        """
        return rai.affine.get_rotation(self._affine)

    def get_shear(self) -> NumS:
        """
        Return a how much this transform shears the coordinate plane.

        Returns
        -------
        float
            A number representing the shear.
        """
        return rai.affine.get_shear(self._affine)

    def get_scale(self) -> Vec2S:
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
            poly: PolyS
            ) -> PolyS:
        """
        Apply transformation to poly and return new transformed poly.

        Parameters
        ----------
        poly : PolyS
            The Poly to transform

        Returns
        -------
        PolyS
            The new, transformed, Poly
        """
        return rai.affine.transform_poly(self._affine, poly)

    def transform_point(
            self,
            point: Vec2S
            ) -> Vec2S:
        """
        Apply this transform to a point, and return the transformed point.

        A Point (tuple of two floats) is always returned,
        even if a BoundPoint is passed in.

        Parameters
        ----------
        point : Vec2S
            The point to transform.

        Returns
        -------
        Vec2S
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

