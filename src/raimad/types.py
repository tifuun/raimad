from __future__ import annotations
from typing import Protocol, runtime_checkable, Literal, TypeAlias, Tuple, Union, Callable
from collections.abc import Sequence, Mapping
from numbers import Real
from typing import SupportsFloat

# "loose" types: for annotating inputs of functions that
# can support many different types of objects, as
# long as they fulfill some criteria.

# `float | int` is equivalent to just `float`
# for static mypy checking,
# but isinstance checks against just `float`
# will reject `int`, so we include both.
# `Real` will also match numpy numeric types.
Num: TypeAlias = float | int | SupportsFloat

@runtime_checkable
class Vec2(Protocol):
    def __getitem__(self, i: Literal[0, 1]) -> Num: ...

Poly: TypeAlias = Sequence[Vec2]
Polys: TypeAlias = Sequence[Poly]
Geoms: TypeAlias = Mapping[str, Polys]
Mat3: TypeAlias = Tuple[Tuple[Num, Num, Num], Tuple[Num, Num, Num], Tuple[Num, Num, Num]]

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
Mat3S: TypeAlias = Tuple[Tuple[NumS, NumS, NumS], Tuple[NumS, NumS, NumS], Tuple[NumS, NumS, NumS]]

types_strict: set[TypeAlias] = {
        NumS,
        Vec2S,
        PolyS,
        PolysS,
        GeomsS,
        Mat3S,
    }

#@runtime_checkable
#class Vec2Attr(Protocol):
#    x: Real
#    y: Real
#
#Vec2 = Vec2Idx | Vec2Attr
#@runtime_checkable
#class Vec2(Vec2Idx, Vec2Attr, Protocol):
#    """Either indexable at 0/1 or has .x/.y attributes."""
#    # No extra methods; this is a structural union-ish protocol
#    ...



LNameTransformer: TypeAlias = Union[
        Callable[[str], str | None],
        Mapping[str, str | None]
        ]
LNameTransformers: TypeAlias = Sequence[LNameTransformer]

