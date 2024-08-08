"""
graphviz.py

Utilities for generating DOT code
"""

from typing import Sequence, Any, TypeAlias, Iterator

class DOTString(str):
    def _repr_dot_(self) -> str:
        return self

AdjList: TypeAlias = Sequence[tuple[Any, Any]]

def _adjlist2dot(adjlist: AdjList) -> Iterator[str]:
    """
    Convert adjecency list to DOT code
    (generator)
    """

    yield 'digraph D {\n'
    for from_, to in adjlist:
        yield f'\t {from_} -> {to};\n'
    yield '}\n'

def adjlist2dot(adjlist: AdjList) -> str:
    """
    Convert adjecency list to DOT code
    """
    return ''.join(_adjlist2dot(adjlist))

def _make_dot(adjlist: AdjList, names: dict[int, str]) -> Iterator[str]:
    yield 'digraph D {\n'

    for rout_num, name in names.items():
        yield f'\t {rout_num} [label="{name}"];'

    for from_, to in adjlist:
        yield f'\t {from_} -> {to};\n'

    yield '}\n'

def make_dot(adjlist: AdjList, names: dict[int, str]) -> str:
    return ''.join(_make_dot(adjlist, names))

