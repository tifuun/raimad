"""Fundamental types for RAIMAD.

This module provides two flavours of types: strict, and loose.
The strict types are what RAIMAD functions return: concrete numeric types
like float/int, concrete containers like lists, tuples, and dicts, etc.
The loose types are what (most) RAIMAD function take in as arguments:
protocols, generic types, etc.
These support a wide range of classes, such as numpy numeric types
and arrays.

We make this decision to allow users of RAIMAD to pass in weird things
(e.g. numpy arrays) directly into RAIMAD functions,
without losing any confidence in what RAIMAD will hand back to them.
"""

from __future__ import annotations
from typing import (
        Callable,
        Literal,
        Protocol,
        SupportsFloat,
        Tuple,
        TypeAlias,
        Union,
        runtime_checkable,
        )
from collections.abc import Sequence, Mapping
from pathlib import Path
from typing import TextIO

# `float | int` is equivalent to just `float`
# for static mypy checking,
# but isinstance checks against just `float`
# will reject `int`, so we include both.
Num: TypeAlias = float | int | SupportsFloat

@runtime_checkable
class Vec2(Protocol):
    """Protocol for a vector of 2 numbers, x and y."""

    def __getitem__(self, i: Literal[0, 1]) -> Num:
        """Get either X (index 0) or Y (index 1) coordinate."""
        ...

Poly: TypeAlias = Sequence[Vec2]
Polys: TypeAlias = Sequence[Poly]
Geoms: TypeAlias = Mapping[str, Polys]
Mat3: TypeAlias = Tuple[
        Tuple[Num, Num, Num],
        Tuple[Num, Num, Num],
        Tuple[Num, Num, Num]
        ]

types_loose: set[TypeAlias] = {
        Num,
        Vec2,
        Poly,
        Polys,
        Geoms,
        Mat3,
    }

# "strict" types: for annotating outputs of functions,
# where the exact return type is always known

NumS: TypeAlias = float | int
Vec2S: TypeAlias = tuple[NumS, NumS]
PolyS: TypeAlias = list[Vec2S]
PolysS: TypeAlias = list[PolyS]
GeomsS: TypeAlias = dict[str, PolysS]
Mat3S: TypeAlias = Tuple[
        Tuple[NumS, NumS, NumS],
        Tuple[NumS, NumS, NumS],
        Tuple[NumS, NumS, NumS]
        ]

types_strict: set[TypeAlias] = {
        NumS,
        Vec2S,
        PolyS,
        PolysS,
        GeomsS,
        Mat3S,
    }


LNameTransformerCallable: TypeAlias = Callable[[str], str | None]
LNameTransformer: TypeAlias = Union[
        LNameTransformerCallable,
        Mapping[str, str | None]
        ]
LNameTransformers: TypeAlias = Sequence[LNameTransformer]
LNameTransformersLambda: TypeAlias = Callable[[], LNameTransformers]

SavetoDest: TypeAlias = str | Path | TextIO | None

