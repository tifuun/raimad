"""
graphviz.py

Utilities for generating DOT code
"""

class DOTString(str):
    def _repr_dot_(self):
        return self

def _adjlist2dot(adjlist):
    """
    Convert adjecency list to DOT code
    (generator)
    """

    yield 'digraph D {\n'
    for from_, to in adjlist:
        yield f'\t {from_} -> {to};\n'
    yield '}\n'

def adjlist2dot(adjlist):
    """
    Convert adjecency list to DOT code
    """
    return ''.join(_adjlist2dot(adjlist))

def _make_dot(adjlist, names):
    yield 'digraph D {\n'

    for rout_num, name in names.items():
        yield f'\t {rout_num} [label="{name}"];'

    for from_, to in adjlist:
        yield f'\t {from_} -> {to};\n'

    yield '}\n'

def make_dot(adjlist, names):
    return ''.join(_make_dot(adjlist, names))

