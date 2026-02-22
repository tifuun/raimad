from __future__ import annotations
from typing import Protocol, runtime_checkable, Literal, TypeAlias
from collections.abc import Sequence, Mapping
from numbers import Real

# "loose" types: for annotating inputs of functions that
# can support many different types of objects, as
# long as they fulfill some criteria.

@runtime_checkable
class Vec2(Protocol):
    def __getitem__(self, i: Literal[0, 1]) -> float | Real: ...

Poly: TypeAlias = Sequence[Vec2]
Polys: TypeAlias = Sequence[Poly]
Geoms: TypeAlias = Mapping[str, Polys]

# "strict" types: for annotating outputs of functions,
# where the exact return type is always known

Vec2S: TypeAlias = tuple[float, float]
PolyS: TypeAlias = list[Vec2S]
PolysS: TypeAlias = list[PolyS]
GeomsS: TypeAlias = dict[str, PolysS]

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

