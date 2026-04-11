#!/usr/bin/env python3

import ast
from typing import Any

class Visitor(ast.NodeVisitor):

    names: list[str]
    line_range: None | tuple[int, int]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.line_range = None
        self.names = []
        super().__init__(*args, **kwargs)

    def visit(self, node: ast.AST) -> None:
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

def replace_all_assignments(filename: str) -> None:
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
    replace_all_assignments("src/raimad/err.py")
    replace_all_assignments("src/raimad/__init__.py")
    replace_all_assignments("src/raimad/cif/__init__.py")

