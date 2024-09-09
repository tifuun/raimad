"""bbox.py: contains BBox class and relevant Exceptions."""

from typing import Iterator, Generic, TypeVar
from copy import copy

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

import raimad as rai

# Disable to use computer-style Y axis (increases downwards)
# DO NOT TOUCH THIS IT WILL BREAK EVERYTHING
MATHEMATIC_Y_AXIS = True

class EmptyBBoxError(Exception):
    """
    EmptyBBoxError: attempted operation on an empty bbox.

    An empty bbox is one that does not contain any points.
    Most properties of an empty bbox (length, width, specific corners, etc.)
    do not make sense, and attempting to query them will raise this exception.
    """


T = TypeVar('T', 'rai.typing.Point', 'rai.typing.BoundPoint', )
class AbstractBBox(Generic[T]):
    """
    """

    max_x: float
    max_y: float
    min_x: float
    min_y: float

    def __init__(
            self,
            poly: 'rai.typing.Poly | None' = None,
            ):
        """
        Create a new BBox.

        Parameters
        ----------
        poly: np.ndarray | None
            A N x 2 numpy array containing points to initialize the bbox with.
            This is optional.
        proxy: rai.Proxy | None
            The proxy that this bbox should be bound to.
            This is optional.
        """
        self.max_x = float('-inf')
        self.max_y = float('-inf')
        self.min_x = float('inf')
        self.min_y = float('inf')

        if poly is not None:
            self.add_poly(poly)

    def as_list(self) -> list[float]:
        """Return as list of [min_x, min_y, max_x, max_y]."""
        return [self.min_x, self.min_y, self.max_x, self.max_y]

    def __iter__(self) -> Iterator[float]:
        """Return as iter of [min_x, min_y, max_x, max_y]."""
        return iter(self.as_list())

    def is_empty(self) -> bool:
        """
        Check if bbox is empty.

        An empoty bbox has no paints.
        BBoxes created with no `poly` argument are empty
        until you manually add points to them with
        `add_poly` or `add_point`.

        Returns
        -------
        bool
            Whether or not the bbox is empty.

        See Also
        --------
        .5        -------
        BBox.assert_nonempty()
        """
        return (
            self.max_x == float('-inf') or
            self.max_y == float('-inf') or
            self.min_x == float('inf') or
            self.min_y == float('inf')
            )

    def assert_nonempty(self, message: str | None = None) -> None:
        """
        Throw EmptyBBoxError is the bbox is empty, do nothing otherwise.

        Parameters
        ----------
        message : str
            Message to pass to EmptyBBoxError

        Raises
        ------
        EmptyBBoxError

        See Also
        --------
        BBox.is_empty()
        """
        if self.is_empty():
            if message is None:
                raise EmptyBBoxError()
            raise EmptyBBoxError()

    def copy(self) -> Self:
        """Copy bbox."""
        # TODO read up on how to properly do copies
        # in Python
        return copy(self)

    def add_poly(self, poly: 'rai.typing.Poly') -> None:
        """
        Add new points to the bounding box.

        Parameters
        ----------
        poly: np.ndarray
            A N x 2 numpy array containing points to add to the bbox.
        """
        for point in poly:
            self.add_point(point)

    def add_point(self, point: 'rai.typing.PointLike') -> None:
        """
        Add a new point to the bounding box.

        Parameters
        ----------
        point
            the point to add
        """
        # TODO simplify with ELIFs?
        if point[0] > self.max_x:
            self.max_x = point[0]
        if point[0] < self.min_x:
            self.min_x = point[0]

        if point[1] > self.max_y:
            self.max_y = point[1]
        if point[1] < self.min_y:
            self.min_y = point[1]

    @property
    def length(self) -> float:
        """
        Get length of the bbox.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        Returns
        -------
        float
            length of the bbox
        """
        self.assert_nonempty("Tried to get length of empty bbox.")
        return self.max_x - self.min_x

    @property
    def width(self) -> float:
        """
        Get width of the bbox.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        Returns
        -------
        float
            width of the bbox
        """
        self.assert_nonempty("Tried to get width of empty bbox.")
        return self.max_y - self.min_y

    @property
    def left(self) -> float:
        """
        Get the X coordinate of the left wall of the bbox.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        Returns
        -------
        float
            left X ccordinate of the bbox
        """
        self.assert_nonempty("Tried to get left of empty bbox.")
        return self.min_x

    @property
    def top(self) -> float:
        """
        Get the Y coordinate of the top wall of the bbox.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        Returns
        -------
        float
            top Y coordinate of the bbox
        """
        self.assert_nonempty("Tried to get top of empty bbox.")
        return self.max_y if MATHEMATIC_Y_AXIS else self.min_y

    @property
    def right(self) -> float:
        """
        Get the X coorinate of the right wall of the bbox.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        Returns
        -------
        float
            right X coordinate of the bbox
        """
        self.assert_nonempty("Tried to get right of empty bbox.")
        return self.max_x

    @property
    def bottom(self) -> float:
        """
        Get the Y coordinate of the bottom of the bbox.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        Returns
        -------
        float
            bottom Y of the bbox
        """
        self.assert_nonempty("Tried to get bottom of empty bbox.")
        return self.min_y if MATHEMATIC_Y_AXIS else self.max_y

    def _interpolate(
            self,
            x_ratio: float,
            y_ratio: float,
            ) -> 'rai.typing.Point':
        x = self.min_x + self.length * x_ratio
        y = self.min_y + self.width * y_ratio

        return (x, y)

    def interpolate(
            self,
            x_ratio: float,
            y_ratio: float,
            ) -> T:
        """
        Find a point inside (or outside) the bbox given X and Y ratios.

        So, for example, 0,0 is top left,
        1,1 is bottom right, 0.5,0.5 is center,
        and 0.5,1 is bottom middle.
        The ratios may be negative or higher than 1,
        but doing so would probably make your code difficult to understand.

        Parameters
        ----------
        x_ratio: float
            A number, such that 0 represents all the way to the left
            of the bbox, and 1 represents all the way to the right.
        y_ratio: float
            A number, such that 0 represents all the way to the bottom
            of the bbox, and 1 represents all the way to the top.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        """
        raise NotImplementedError()

    @property
    def mid(self) -> T:
        """
        Get the point in the MIDDLE of the bbox.

        Like this:
        .-.-.
        |   |
        . X .
        |   |
        ._._.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        """
        self.assert_nonempty("Tried to get middle point of empty bbox")
        return self.interpolate(0.5, 0.5)

    @property
    def top_mid(self) -> T:
        """
        Get the point in the TOP MIDDLE of the bbox.

        Like this:
        .-X-.
        |   |
        . . .
        |   |
        ._._.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        """
        self.assert_nonempty("Tried to get top middle point of empty bbox")
        return self.interpolate(0.5, MATHEMATIC_Y_AXIS)

    @property
    def bot_mid(self) -> T:
        """
        Get the point in the BOTTOM MIDDLE of the bbox.

        Like this:
        .-.-.
        |   |
        . . .
        |   |
        ._X_.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        """
        self.assert_nonempty("Tried to get bottom middle point of empty bbox")
        return self.interpolate(0.5, not MATHEMATIC_Y_AXIS)

    @property
    def mid_left(self) -> T:
        """
        Get the point in the MIDDLE LEFT of the bbox.

        Like this:
        .-.-.
        |   |
        X . .
        |   |
        ._._.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        """
        self.assert_nonempty("Tried to get middle left point of empty bbox")
        return self.interpolate(0, 0.5)

    @property
    def mid_right(self) -> T:
        """
        Get the point in the MIDDLE RIGHT of the bbox.

        Like this:
        .-.-.
        |   |
        . . X
        |   |
        ._._.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        """
        self.assert_nonempty("Tried to get middle right point of empty bbox")
        return self.interpolate(1, 0.5)

    @property
    def top_left(self) -> T:
        """
        Get the point in the TOP LEFT of the bbox.

        Like this:
        X-.-.
        |   |
        . . .
        |   |
        ._._.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        """
        self.assert_nonempty("Tried to get top left point of empty bbox")
        return self.interpolate(0, MATHEMATIC_Y_AXIS)

    @property
    def top_right(self) -> T:
        """
        Get the point in the TOP RIGHT of the bbox.

        Like this:
        .-.-X
        |   |
        . . .
        |   |
        ._._.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        """
        self.assert_nonempty("Tried to get top right point of empty bbox")
        return self.interpolate(1, MATHEMATIC_Y_AXIS)

    @property
    def bot_left(self) -> T:
        """
        Get the point in the BOTTOM LEFT of the bbox.

        Like this:
        .-.-.
        |   |
        . . .
        |   |
        X_._.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        """
        self.assert_nonempty("Tried to get bottom left point of empty bbox")
        return self.interpolate(0, not MATHEMATIC_Y_AXIS)

    @property
    def bot_right(self) -> T:
        """
        Get the point in the middle of the bbox.

        Like this:
        .-.-.
        |   |
        . . .
        |   |
        ._._X

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        """
        self.assert_nonempty("Tried to get bottom right point of empty bbox")
        return self.interpolate(1, not MATHEMATIC_Y_AXIS)

    def pad(
            self,
            x: float = 0,
            y: float | None = None,
            /,
            *,
            left: float = 0,
            top: float = 0,
            right: float = 0,
            bottom: float = 0,
            ) -> Self:
        """
        Create a copy of this bbox with extra padding.

        Bound bboxes will be turned into unbound ones (Or will they O_O ).

        Examples
        --------
        bbox.pad(5)  # Pad evenly on every side
        bbox.pad(5, 10)  # Pad 5 units horizontally and 10 units vertically
        bbox.pad(left=10)  # Pad 10 units on the left side only
        bbox.pad(left=10, bottom=5)  # Pad 10 on th left, 5 on the bottom
        bbox.pad(5, left=10)  # Pad 15 units on the left, 5 everywhere else.

        Parameters
        ----------
        x: float
            Base padding (is y in not specified) or horizontal padding
            (if y IS specified)
        y: float
            Vertical padding.
        left: float
            Additional left padding
        right: float
            Additional right padding
        top: float
            Additional top padding
        bottom: float
            Additional bottom padding

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        Returns
        -------
        Self
            A new bbox with the corresponding padding.
        """
        self.assert_nonempty("Tried to pad empty bbox")

        y = y or x

        new = self.copy()
        new.min_x -= left + x
        new.max_x += right + x
        new.min_y -= bottom + y
        new.max_y += top + y

        return new


class BBox(AbstractBBox['rai.typing.Point']):
    def interpolate(
            self,
            x_ratio: float,
            y_ratio: float,
            ) -> 'rai.typing.Point':
        return super()._interpolate(x_ratio, y_ratio)

