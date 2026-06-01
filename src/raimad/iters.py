"""iters.py: iteration-related helpers."""

from typing import TypeVar, Any, TypeAlias
from collections.abc import Iterable, Callable, Sequence
from itertools import chain


T = TypeVar('T')
def overlap(n: int, seq: Sequence[T]) -> Iterable[Iterable[T]]:
    """
    Iterate n items at a time, with overlap.

    overlap(3, [1,2,3,4,5]) = [
        [1,2,3],
        [2,3,4],
        [3,4,5],
        ]
    """
    return zip(*[seq[offset:] for offset in range(n)])


def nonoverlap(n: int, seq: Sequence[T]) -> Iterable[Iterable[T]]:
    """
    Iterate n items at a time, without overlap.

    Truncates the iterable such that it is a multiple of n.

    overlap(2, [1,2,3,4,5,6]) = [
        [1,2],
        [3,4],
        [5,6],
        ]

    overlap(2, [1,2,3,4,5]) = [
        [1,2],
        [3,4],
        ]
    """
    return zip(*[seq[offset::n] for offset in range(n)])


def _make_alias(
        name: str,
        iterator: Callable[[int, Sequence[T]], Iterable[Iterable[T]]],
        n: int) -> Callable[[Sequence[T]], Iterable[Iterable[T]]]:

    def iterator_alias(seq: Sequence[T]) -> Iterable[Iterable[T]]:
        return iterator(n, seq)

    iterator_alias.__doc__ = (
        f'Iterator through a list {n} items at a time, '
        f'with{"out" if iterator is nonoverlap else ""} overlap.\n'
        f'Equivalent to {iterator.__name__}({n}, iterable)'
        )
    iterator_alias.__name__ = name

    return iterator_alias


duplets = _make_alias('duplets', overlap, 2)
triplets = _make_alias('triplets', overlap, 3)
quadlets = _make_alias('quadlets', overlap, 4)
quintlets = _make_alias('quintlets', overlap, 5)

couples = _make_alias('couples', nonoverlap, 2)
triples = _make_alias('triples', nonoverlap, 3)
quadles = _make_alias('quadles', nonoverlap, 4)
quintles = _make_alias('quintles', nonoverlap, 5)

# Python does not (really) support recursive types
# (see mypy-experiments/recursive_iterable.py).
# Solution: The Great Pyramid of Iterable
#
# Not a complete solution since it does not
# support "asymmetric" nested iterables (like an unbalanced tree made
# out of lists),
# but like whatever, caller can just type:ignore it
I: TypeAlias = Iterable  #  noqa:E741
V = TypeVar("V")
def flatten(
        iterable:
                                  V |
                                 I[V] |
                                I[I[V]] |
                               I[I[I[V]]] |
                              I[I[I[I[V]]]] |
                             I[I[I[I[I[V]]]]] |
                            I[I[I[I[I[I[V]]]]]] |
                           I[I[I[I[I[I[I[V]]]]]]] |
                          I[I[I[I[I[I[I[I[V]]]]]]]] |
                         I[I[I[I[I[I[I[I[I[V]]]]]]]]] |
                        I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]] |
                       I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]] |
                      I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]] |
                     I[I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]]] |
                    I[I[I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]]]] |
                   I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]]]]] |
                  I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]]]]]] |
                 I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]]]]]]] |
                I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]]]]]]]] |
               I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]]]]]]]]] |
              I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]]]]]]]]]] |
             I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]]]]]]]]]]] |
            I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[I[V]]]]]]]]]]]]]]]]]]]]]]
        ) -> list[V]:
    """Recursively flatten a nested iterable."""
    if not isinstance(iterable, Iterable) or isinstance(iterable, str):
        # This terminates the recursion
        return [iterable]

    return [
        item
        for sub in iterable
        for item in flatten(sub)
        ]

def braid(*iterables: Iterable[T]) -> Iterable[T]:
    """
    Honestly no clue what this does.

    TODO document and test.
    """
    return list(chain(*zip(*iterables)))

def is_distinct(iterable: Iterable[Any]) -> bool:
    """Return true if no two items in `iterable` are the same."""
    raise NotImplementedError()
    return len(iterable) == len(set(iterable))

def is_cycled(
        first: Sequence[T],
        second: Sequence[T],
        comparison: Callable[[Sequence[T], Sequence[T]], bool] =
                lambda a, b: a == b) -> bool:
    """
    Given two iterables, figure out whether they are "cycled" versions of each other.

    Type of the iterables is not taken into account.

    'abcd', 'bcda' -> True
    [1, 2, 3, 4], (3, 4, 1, 2) -> True
    'abcd', 'bacd' -> False
    'abcd', 'abcde' -> False

    :first: the first iterable
    :second: the other iterable
    :returns: Whether or not one can be obtained by cycling the other
    """
    if len(first) != len(second):
        return False

    length = len(first)
    first_as_tuple = tuple(first)
    # Cast `first` as tuple, since `second` will
    # also be cast to tuple

    for x in range(0, length):
        cycled = (*second[x:], *second[:x])
        assert len(cycled) == length
        if comparison(first_as_tuple, cycled):
            return True
    return False

def cycled(seq: Sequence[T], count: int) -> list[T]:
    """
    Return `seq` cycled by `count` steps.

    By "cycling" a sequence we mean shifting its items forward
    (higher index numbers), and wrapping the last item back
    to the start such that the length stays the same.

    Parameters
    ----------
    seq : Sequence[T]
        The sequence to cycle
    count: int
        Number of steps to cycle the sequence forward

    Returns
    -------
    list[T]
        The sequence, cycled. No matter the type of the input sequence,
        a list is always returned.

    Examples
    --------
    >>> raimad.cycled(('a', 'b', 'c', 'd'), 2)
    ('c', 'd', 'a', 'b')

    >>> raimad.cycled(('a', 'b', 'c', 'd'), -1)
    ('b', 'c', 'd', 'a')
    """
    if len(seq) == 0:
        return list(seq[:])

    count = count % len(seq)

    if count < 0:
        count = len(seq) + count

    if count == 0:
        return list(seq[:])

    assert count > 0

    return [*seq[-count:], *seq[:-count]]

#T = TypeVar("T")
def reversed(seq: Sequence[T]) -> list[T]:
    """Return `seq` backwards (in reverse order), as a list."""
    return list(seq[::-1])

#T = TypeVar("T")
def reversed_pin(seq: Sequence[T], idx: int = 0) -> list[T]:
    """
    Return `seq` reversed and cycled so that a particular item does not move.

    Will return `seq`, as a list, in reverse order, and cycled
    by `idx` * 2 - 1 positions.
    This will make it so the item at index `idx` in the original
    is in the same index in the returned list.
    Useful for cycling the points of a Poly or PolyS while keeping
    one point in place.

    Parameters
    ----------
    seq : Sequence[T]
        Any Sequence (list, tuple, etc).
    idx : int, optional
        Index to pin in place. 0 by default.

    Returns
    -------
    list[T]
        A list is returned no matter the type of the original sequence.

    Raises
    ------
    IndexError
        If `idx` is out of bounds of `seq` ( idx >= len(seq) OR
        idx < -len(seq) )

    Examples
    --------
    >>> raimad.reversed_pin(('a', 'b', 'c', 'd'))
    ('a', 'd', 'c', 'b')

    >>> raimad.reversed_pin(('a', 'b', 'c', 'd'), 1)
    ('c', 'b', 'a', 'd')

    """
    if idx >= len(seq):
        raise IndexError("Pin index out of range of sequence.")
    if idx < -len(seq):
        raise IndexError("Pin back-index out of range of sequence.")

    return reversed(cycled(seq, idx * 2 - 1))

