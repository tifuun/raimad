from __future__ import annotations
from typing import Protocol, runtime_checkable, Literal
from numbers import Real

@runtime_checkable
class Vec2(Protocol):
    #def __getitem__(self, i: int) -> Real: ...
    def __getitem__(self, i: Literal[0, 1]) -> Real: ...

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

