"""helpers.py: misc helper functions."""

from typing import Iterator, TypeVar, Callable, Generic
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
    """Angle between two points."""
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    return math.atan2(y, x)

def polar(arg: float, mod: float = 1) -> 'rai.typing.Point':
    """Construct an XY point from an argument and modulus."""
    return (
        math.cos(arg) * mod,
        math.sin(arg) * mod
        )

def is_compo_class(obj: type) -> bool:
    """
    Check whether an object is a CompoType.

    Note that this returns False on the `rai.Compo`
    abstract base class.
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
    """Encode an integer with a bunch of symbols."""
    return ''.join((
        custom_base(value, WINGDINGS),
        '\033[0m',
        ))

T = TypeVar('T')
R = TypeVar('R')
class Infix(Generic[T, R]):
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

class Midpoint(Infix['rai.typing.PointLike', 'rai.typing.PointLike']):
    def __call__(
            self,
            p1: 'rai.typing.PointLike',
            p2: 'rai.typing.PointLike'
            ) -> 'rai.typing.PointLike':
        """Midpoint between two points."""
        return (
            (p1[0] + p2[0]) / 2,
            (p1[1] + p2[1]) / 2,
            )

midpoint = Midpoint()
# TODO more than 1 input

class Add(Infix['rai.typing.PointLike', 'rai.typing.PointLike']):
    def __call__(
            self,
            p1: 'rai.typing.PointLike',
            p2: 'rai.typing.PointLike'
            ) -> 'rai.typing.PointLike':
        return (
            p1[0] + p2[0],
            p1[1] + p2[1],
            )

add = Add()

class Sub(Infix['rai.typing.PointLike', 'rai.typing.PointLike']):
    def __call__(
            self,
            p1: 'rai.typing.PointLike',
            p2: 'rai.typing.PointLike'
            ) -> 'rai.typing.PointLike':
        return (
            p1[0] - p2[0],
            p1[1] - p2[1],
            )

sub = Sub()

class Eq(Infix['rai.typing.PointLike', bool]):
    def __call__(
            self,
            p1: 'rai.typing.PointLike',
            p2: 'rai.typing.PointLike'
            ) -> bool:
        return rai.affine.norm((
            p1[0] - p2[0],
            p1[1] - p2[1],
            )) < rai.epsilon

eq = Eq()

def distance_between(
        p1: 'rai.typing.Point',
        p2: 'rai.typing.Point'
        ) -> float:

    return rai.affine.norm((
        p1[0] - p2[0],
        p1[1] - p2[1],
        ))

