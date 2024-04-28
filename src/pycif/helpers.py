from enum import Enum
import functools

import numpy as np

import pycif as pc

fullcircle = pc.degrees(360)
halfcircle = pc.degrees(180)
quartercircle = pc.degrees(90)
eigthcircle = pc.degrees(45)

semicircle = pc.degrees(180)
demisemicircle = pc.degrees(90)
hemidemisemicircle = pc.degrees(45)

class Orientation(Enum):
    POS = 1
    NEG = -1

def angspace(
        start: float,
        end: float,
        num_steps: int = 50,
        orientation: Orientation = Orientation.POS,
        endpoint: bool = True,
        ):
    """
    Angular space:
    construct an array of angles going from `start` to `end`
    in the positive orientation (counterclockwise)
    """
    if orientation is Orientation.NEG:
        start, end = end, start

    while start < 0:
        start += fullcircle

    while end < start:
        end += fullcircle

    return np.linspace(start, end, num_steps, endpoint=endpoint)

def angle_between(p1, p2):
    """
    Angle between two points
    """
    x, y = np.array(p2) - np.array(p1)
    return np.arctan2(y, x)

def polar(arg, mod=1):
    return np.array([
        np.cos(arg),
        np.sin(arg)
        ]) * mod

def is_compo_class(obj):
    return (
        isinstance(obj, type)
        and issubclass(obj, pc.Compo)
        and obj is not pc.Compo
        )

def _custom_base(value: int, glyphs: list[str]):
    """
    Convert an int into a base-n number
    (generator)
    """
    div, mod = divmod(value, len(glyphs))
    if div > 0:
        yield from _custom_base(div, glyphs)
    yield glyphs[mod]

def custom_base(value: int, glyphs: list[str]):
    return ''.join(_custom_base(value, glyphs))


WINGDINGS = [
    f"\033[0;{color}m{symbol} "
    for color in [31, 32, 34, 35, 36]
    for symbol in r"●■◀▶▲▼▚x╚╔╝═╩╗╦╵╷┴┬╰/\╭╮╯∞o8:"
    ]

def wingdingify(value: int):
    """
    Encode an integer with a bunch of symbols.
    """
    return ''.join((
        custom_base(value, WINGDINGS),
        '\033[0m',
        ))

def join_generator(string):
    def join_generator_inner(generator):
        @functools.wraps(generator)
        def wrapper(*args, **kwargs):
            return string.join(generator(*args, **kwargs))
        return wrapper
    return join_generator_inner

