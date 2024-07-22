from typing import (
        Callable,
        Generator,
        TypeVar,
        Iterator,
        )

import sys

# see https://github.com/python/mypy/issues/16903
if sys.version_info >= (3, 10):
    from typing import ParamSpec, TypeAlias
else:
    from typing_extensions import ParamSpec, TypeAlias


from enum import Enum
import functools
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
    """
    Angle between two points
    """
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    return math.atan2(y, x)

def polar(arg: float, mod: float = 1) -> tuple[float, float]:
    return (
        math.cos(arg) * mod,
        math.sin(arg) * mod
        )

def is_compo_class(obj: type) -> bool:
    return (
        isinstance(obj, type)
        and issubclass(obj, rai.Compo)
        and obj is not rai.Compo
        )

def _custom_base(value: int, glyphs: list[str]) -> Iterator[str]:
    """
    Convert an int into a base-n number
    (generator)
    """
    div, mod = divmod(value, len(glyphs))
    if div > 0:
        yield from _custom_base(div, glyphs)
    yield glyphs[mod]

def custom_base(value: int, glyphs: list[str]) -> str:
    return ''.join(_custom_base(value, glyphs))

WINGDINGS = [
    f"\033[0;{color}m{symbol} "
    for color in [31, 32, 34, 35, 36]
    for symbol in r"●■◀▶▲▼▚x╚╔╝═╩╗╦╵╷┴┬╰/\╭╮╯∞o8:"
    ]

def wingdingify(value: int) -> str:
    """
    Encode an integer with a bunch of symbols.
    """
    return ''.join((
        custom_base(value, WINGDINGS),
        '\033[0m',
        ))

def midpoint(
        p1: 'rai.typing.Point',
        p2: 'rai.typing.Point'
        ) -> 'rai.typing.Point':
    """
    Midpoint between two points
    """
    return (
        (p1[0] + p2[0]) / 2,
        (p1[1] + p2[1]) / 2,
        )

# TODO chaining boundpoint actions?

def klay(cifstring: str) -> None:
    """
    Do not use this function.
    This is a helper for me to debug the CIF export process
    until I come up with something better
    """
    import subprocess
    with open('/home/maybetree/tmp/raimad.cif', 'w') as cif:
        cif.write(cifstring)
    #subprocess.Popen(
    #    'flatpak run de.klayout.KLayout /home/maybetree/tmp/raimad.cif'
    #    .split(' '))


