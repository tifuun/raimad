from typing import TypeVar, Protocol, Self

#K = TypeVar('K', covariant=True)
#class Concattable(Protocol[K]):
#    def __add__(self, other: Self) -> Self: ...

I = TypeVar('I', contravariant=True)
S = TypeVar('S', list[I], tuple[I, ...])
def duplicate(seq: S, bound: I | None = None) -> S:
    return seq + seq

# No issue
mylist = [1,2,3]
assert duplicate(mylist) == [1,2,3,1,2,3]

# Issue
assert duplicate([1,2,3]) == [1,2,3,1,2,3]

