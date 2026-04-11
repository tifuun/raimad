#!/usr/bin/env python3
"""
patch_dunder_all.py: rewrite `__all__` assignments to include all re-exports.

There are multiple modules in RAIMAD that import other RAIMAD objects
not to use them,
but to make them available to users in a nicer syntax.
For example,
`src/raimad/__init__.py`
contains the line
`from raimad.compo import Compo`
so that users can write
`raimad.Compo`
instead of
`raimad.compo.Compo`.

These re-exports must also be included in the `__all__` list
in each of those files,
otherwise MyPy and Ruff will complain.

This script uses `ast` to scan all imports in these files
and re-write the `__all__` assignments to include all of the imports.
"""

import ast
from typing import Any

class Visitor(ast.NodeVisitor):
    """Visit every node and record object names if it is an import."""

    names: list[str]
    line_range: None | tuple[int, int]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.line_range = None
        self.names = []
        super().__init__(*args, **kwargs)

    def visit(self, node: ast.AST) -> None:
        """Visit a single node and record object names if it is an import."""
        match node:
            case ast.ImportFrom() | ast.Import():
                self.names.extend(
                    # rpartition strips the `foo.bar.`
                    # out of `import foo.bar.baz` lines
                    (alias.asname or alias.name).rpartition(".")[-1]
                    for alias in node.names
                    )

            case ast.Assign(
                    targets=[
                        ast.Name(id='__all__'),
                        ],
                    value=ast.List(),
                    ):

                # ...end line can be None according to mypy???
                # Panic if this is the case.
                assert node.end_lineno is not None

                self.line_range = (node.lineno - 1, node.end_lineno)

                # assume the __all__ asignment is last meaningful line in file.
                return

        super().generic_visit(node)

def patch_dunder_all(filename: str) -> None:
    """Patch `__all__` in single file."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    tree = ast.parse(''.join(lines))
    visitor = Visitor()
    visitor.visit(tree)
    
    if visitor.line_range is None:
        print("No '__all__ = ...' assignments found")
        return

    replacement_lines = (
        '__all__ = [\n',
        *(
            f'    "{name}",\n'
            for name in visitor.names
            ),
        '    ]\n'
        )

    lines[visitor.line_range[0]:visitor.line_range[1]] = replacement_lines

    with open(filename, 'w') as f:
        f.writelines(lines)
    

if __name__ == "__main__":
    patch_dunder_all("src/raimad/err.py")
    patch_dunder_all("src/raimad/__init__.py")
    patch_dunder_all("src/raimad/cif/__init__.py")

