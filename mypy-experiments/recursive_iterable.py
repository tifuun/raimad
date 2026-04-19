from typing import Protocol, Iterable, TypeVar, Iterator, runtime_checkable

@runtime_checkable
class RecursiveIterable[V](Protocol):
    def __iter__(self) -> Iterator[V | RecursiveIterable[V]]: ...

W = TypeVar("W")
def flatten(iterable: W | RecursiveIterable[W]) -> list[W]:
    """Recursively flatten a nested iterable."""
    if not isinstance(iterable, Iterable) or isinstance(iterable, str):
        # This terminates the recursion
        return [iterable]

    return [
        item
        for sub in iterable
        for item in flatten(sub)
        ]

foo: RecursiveIterable[str] = ['a', 'b', 'c']

flatten([[['a', 'bcd'], 'e', ['f'], ['g', 'h'], 'ij'], 'klm'])
flatten([1, 2, 3, 4, 5, 6, 7, 8])
flatten([[[1, 2], 3, [4], [5, 6], 7], 8])
flatten(10)
flatten('string')

