"""helpers.py: misc helper functions."""

from typing import Iterator, TypeVar, Generic
import math

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

import raimad as rai

fullcircle = math.radians(360)
halfcircle = math.radians(180)
quartercircle = math.radians(90)
eigthcircle = math.radians(45)

semicircle = math.radians(180)
demisemicircle = math.radians(90)
hemidemisemicircle = math.radians(45)

def angle_between(p1: 'rai.typing.Point', p2: 'rai.typing.Point') -> float:
    """
    Calculate angle between two points.

    Parameters
    ----------
    p1
        The first point
    p2
        The second point

    Returns
    -------
    float
        The angle, in [numpy convention](coords-transforms.md)

    """
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    return math.atan2(y, x)

def polar(arg: float, mod: float = 1) -> 'rai.typing.Point':
    """
    Construct an XY point from an argument and modulus.

    Parameters
    ----------
    arg
        The argument (angle) in
        [numpy convention](coords-transforms.md)
    mod
        The modulus/magnitue/length

    Returns
    -------
    rai.typing.Point
        The constructed point
    """
    return (
        math.cos(arg) * mod,
        math.sin(arg) * mod
        )

def is_compo_class(obj: type) -> bool:
    """
    Check whether an object is a CompoType.

    Parameters
    ----------
    obj
        The object to check

    Returns
    -------
    bool
        True if `obj` is a class that inherits from `raimad.Compo`.
        False if class IS `raimad.Compo` and in all other cases.
    """
    return (
        isinstance(obj, type)
        and issubclass(obj, rai.Compo)
        and obj is not rai.Compo
        )

def _custom_base(value: int, glyphs: list[str]) -> Iterator[str]:
    """
    Encode an integer into base-N using a custom set of glyphs (generator).

    Parameters
    ----------
    value: int
        The integer to encode
    glyphs: list[str]
        A list of N strings representing the glyphs
        in your custom base.
        TODO low to high or high to low? I forgot.

    Yields
    ------
    str
        Your encoded integer is yielded, glyph by glyph
    """
    div, mod = divmod(value, len(glyphs))
    if div > 0:
        yield from _custom_base(div, glyphs)
    yield glyphs[mod]

def custom_base(value: int, glyphs: list[str]) -> str:
    """
    Encode an integer into base-N using a custom set of glyphs.

    Parameters
    ----------
    value: int
        The integer to encode
    glyphs: list[str]
        A list of N strings representing the glyphs
        in your custom base.
        TODO low to high or high to low? I forgot.

    Returns
    -------
    str
        A string with your encoded integer.
    """
    return ''.join(_custom_base(value, glyphs))


WINGDINGS = [
    f"\033[0;{color}m{symbol} "
    for color in [31, 32, 34, 35, 36]
    for symbol in r"●■◀▶▲▼▚x╚╔╝═╩╗╦╵╷┴┬╰/\╭╮╯∞o8:"
    ]

def wingdingify(value: int) -> str:
    r"""
    Encode an integer into a string of colorful symbols.

    The symbols are given color using ANSI escape sequences
    i.e. they will only be visible in the terminal.

    Parameters
    ----------
    value
        The integer to encode

    Returns
    -------
    str
        The encoded string.

    Example
    -------
    raimad.wingdingify(id(None))
        '\x1b[0;31m╝ \x1b[0;31m/ \x1b[0;31m┴ \x1b[0;31m▲ \
        \x1b[0;34m╯ \x1b[0;34m╝ \x1b[0;31m╮ \x1b[0m'
    """
    return ''.join((
        custom_base(value, WINGDINGS),
        '\033[0m',
        ))

T = TypeVar('T')
R = TypeVar('R')
class _Infix(Generic[T, R]):
    left: T | None

    def __init__(self) -> None:
        self.left = None

    def __ror__(self, left: T) -> Self:
        self.left = left
        return self

    def __or__(self, right: T) -> R:
        assert \
            self.left is not None, \
            "Incorrect usage of infix operator"

        return self(self.left, right)

    def __call__(self, left: T, right: T) -> R:
        raise NotImplementedError() ## TODO undo

class Midpoint(_Infix['rai.typing.PointLike', 'rai.typing.PointLike']):
    """
    Infix operator for calculating midpoint of points.

    See docstring of __call__ for more info.
    """

    def __call__(
            self,
            p1: 'rai.typing.PointLike',
            p2: 'rai.typing.PointLike'
            ) -> 'rai.typing.PointLike':
        """
        Get midpoint between two points.

        Parameters
        ----------
        p1
            The first point
        p2
            The second point

        Returns
        -------
        rai.typing.Point
            The midpoint
        """
        return (
            (p1[0] + p2[0]) / 2,
            (p1[1] + p2[1]) / 2,
            )

midpoint = Midpoint()
# TODO more than 1 input

class Add(_Infix['rai.typing.PointLike', 'rai.typing.PointLike']):
    """
    Infix operator for adding points.

    See docstring of __call__ for more info.
    """

    def __call__(
            self,
            p1: 'rai.typing.PointLike',
            p2: 'rai.typing.PointLike'
            ) -> 'rai.typing.PointLike':
        """
        Add together two points.

        Parameters
        ----------
        p1
            One point
        p2
            Another point

        Returns
        -------
        rai.typing.PointLike
            The sum of p1 and p2
        """
        return (
            p1[0] + p2[0],
            p1[1] + p2[1],
            )

add = Add()

class Sub(_Infix['rai.typing.PointLike', 'rai.typing.PointLike']):
    """
    Infix operator for subtracting points.

    See docstring of __call__ for more info.
    """

    def __call__(
            self,
            p1: 'rai.typing.PointLike',
            p2: 'rai.typing.PointLike'
            ) -> 'rai.typing.PointLike':
        """
        Subtract one point from another.

        Parameters
        ----------
        p1
            The point to be subtracted from
        p2
            The point to subtract

        Returns
        -------
        rai.typing.PointLike
            The resulting point.
        """
        return (
            p1[0] - p2[0],
            p1[1] - p2[1],
            )

sub = Sub()

class Eq(_Infix['rai.typing.PointLike', bool]):
    """
    Infix operator for testing point equality.

    See docstring of __call__ for more info.
    """

    def __call__(
            self,
            p1: 'rai.typing.PointLike',
            p2: 'rai.typing.PointLike'
            ) -> bool:
        """
        Check whether two points are the same.

        Parameters
        ----------
        p1
            The first point
        p2
            The second point

        Returns
        -------
        bool
            True if the euclidean distance between `p1` and `p2`
            is less than `rai.epsilon`.
            False otherwise.
        """
        return rai.affine.norm((
            p1[0] - p2[0],
            p1[1] - p2[1],
            )) < rai.epsilon

eq = Eq()

def distance_between(
        p1: 'rai.typing.Point',
        p2: 'rai.typing.Point'
        ) -> float:
    """
    Get euclidean distance between two points.

    Parameters
    ----------
    p1
        The first point
    p2
        The second point

    Returns
    -------
    float
        Euclidean distance between two points
    """

    return rai.affine.norm((
        p1[0] - p2[0],
        p1[1] - p2[1],
        ))

