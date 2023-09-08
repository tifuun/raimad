"""
iter.py -- iteration-related helpers
"""

from collections.abc import Iterable


def overlap(n, iterable):
    """
    Iterate n items at a time, with overlap:

    overlap(3, [1,2,3,4,5]) = [
        [1,2,3],
        [2,3,4],
        [3,4,5],
        ]
    """
    return zip(*[iterable[offset:] for offset in range(n)])


def nonoverlap(n, iterable):
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
    return zip(*[iterable[offset::n] for offset in range(n)])


def _make_alias(name, iterator, n):
    def iterator_alias(iterable):
        return iterator(n, iterable)

    iterator_alias.__doc__ = \
        f'Iterator through a list {n} items at a time, ' \
        f'with{"out" if iterator is nonoverlap else ""} overlap.\n' \
        f'Equivalent to {iterator.__name__}({n}, iterable)'
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

def flatten(iterable):
    """
    Recursively flatten a nested iterable
    """

    if not isinstance(iterable, Iterable):
        # This terminates the recursion
        return [iterable]

    return [
        item
        for sub in iterable
        for item in flatten(sub)
        ]


