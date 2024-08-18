"""graphviz.py: utilities for generating DOT code."""

from typing import Sequence, Any, TypeAlias, Iterator

class DOTString(str):
    """
    A string containing DOT code.

    This is just a subclass of string that defines a `_repr_dot_`
    method returning self,
    which tells RAIMARK to render it as a DOT picture.
    """

    def _repr_dot_(self) -> str:
        """
        Return self.

        The presence of this method tells RAIMARK to render
        this string as a DOT picture.
        """
        return self


AdjList: TypeAlias = Sequence[tuple[Any, Any]]

def _adjlist2dot(adjlist: AdjList) -> Iterator[str]:
    """Convert adjecency list to DOT code (generator)."""
    yield 'digraph D {\n'
    for from_, to in adjlist:
        yield f'\t {from_} -> {to};\n'
    yield '}\n'

def adjlist2dot(adjlist: AdjList) -> str:
    """Convert adjecency list to DOT code."""
    return ''.join(_adjlist2dot(adjlist))

def _make_dot(adjlist: AdjList, names: dict[int, str]) -> Iterator[str]:
    yield 'digraph D {\n'

    for rout_num, name in names.items():
        yield f'\t {rout_num} [label="{name}"];'

    for from_, to in adjlist:
        yield f'\t {from_} -> {to};\n'

    yield '}\n'

def make_dot(adjlist: AdjList, names: dict[int, str]) -> str:
    """Given an adjacency list and node names, generate DOT code."""
    return ''.join(_make_dot(adjlist, names))

