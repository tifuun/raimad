"""helpers.py: misc helper functions."""

from typing import Iterator
import math

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

class Infix:
    def __init__(self, func = None):
        self.func = func or self.__call__

    def __ror__(self, other):
        return type(self)(lambda x, self=self, other=other: self.func(other, x))

    def __or__(self, other):
        return self.func(other)

class Midpoint(Infix):
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

class Add(Infix):
    def __call__(
            self,
            p1: 'rai.typing.Point',
            p2: 'rai.typing.Point'
            ) -> 'rai.typing.Point':
        return (
            p1[0] + p2[0],
            p1[1] + p2[1],
            )

add = Add()

class Sub(Infix):
    def __call__(
            self,
            p1: 'rai.typing.Point',
            p2: 'rai.typing.Point'
            ) -> 'rai.typing.Point':
        return (
            p1[0] - p2[0],
            p1[1] - p2[1],
            )

sub = Sub()

class Eq(Infix):
    def __call__(
            self,
            p1: 'rai.typing.Point',
            p2: 'rai.typing.Point'
            ) -> bool:
        return rai.affine.norm((
            p1[0] - p2[0],
            p1[1] - p2[1],
            )) < rai.epsilon

eq = Eq()

