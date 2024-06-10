"""
docparse.py: utilities for parsing docstrings
"""

from typing import NamedTuple
import inspect

class SplitDocstring(NamedTuple):
    heading: str
    description: str


def split_docstring(docstring: str | None) -> SplitDocstring:
    """
    Split docstring by first line and other lines
    """
    if not docstring:
        return SplitDocstring('', '')

    split = inspect.cleandoc(docstring).split('\n', 1)

    if len(split) == 0:
        return SplitDocstring('', '')

    elif len(split) == 1:
        return SplitDocstring(split[0], '')

    else:
        return SplitDocstring(split[0], split[1])

