#!/usr/bin/env python3

import re
from pathlib import Path

# One day you are young, hopeful, and full of energy,
# and the next you are parsing C++ code with regex
DITHER_FINDER = re.compile(
    r'\s*//\s*(\d+):\s*(.*)$\s*"(.*)"\s*,\s*$',
    re.MULTILINE
    )

def translate(string):
    yield 'builtin = rai.DictList({\n'
    found = re.findall(DITHER_FINDER, string)
    prev_num = -1
    for num, _comment_name, name in found:
        num = int(num)
        assert num == prev_num + 1
        prev_num = num

        #yield num, name
        print(num, name)
        yield f"    '{name}': BuiltinDitherPattern('I{num}'),\n"
    yield '}, copy=False)\n'

import ast
from typing import Any

class Visitor(ast.NodeVisitor):

    line_range: None | tuple[int, int]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.line_range = None
        super().__init__(*args, **kwargs)

    def visit(self, node: ast.AST) -> None:
        match node:
            case ast.Assign(
                    targets=[
                        ast.Name(id='builtin'),
                        ],
                    #value=ast.List(),
                    ):

                # ...end line can be None according to mypy???
                # Panic if this is the case.
                assert node.end_lineno is not None

                self.line_range = (node.lineno - 1, node.end_lineno)

                # assume the __all__ asignment is last meaningful line in file.
                return

        super().generic_visit(node)

def patch_dithers_def(file_cc: str, file_py: str) -> None:
    """Patch `__all__` in single file."""
    with open(file_py, 'r') as f:
        lines = f.readlines()

    with open(file_cc, 'r') as f:
        cc_source = f.read()
    
    tree = ast.parse(''.join(lines))
    visitor = Visitor()
    visitor.visit(tree)

    replacement = translate(cc_source)
    lines[visitor.line_range[0]:visitor.line_range[1]] = replacement

    with open(file_py, 'w') as f:
        f.writelines(lines)


if __name__ == "__main__":
    patch_dithers_def(
        'vendor/klayout/layDitherPattern.cc',
        'src/raimad/cif/lyp.py'
        )
    #extract(Path('vendor/klayout/layDitherPattern.cc').read_text())

