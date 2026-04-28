#!/usr/bin/env python3
"""
Read Klayout source and update RAIMAD line/dither style definitions.

This script reads klayout's layDitherPatterns.cc and layLineStyles.cc code,
extracts all builtin dither pattern and line style names,
and updates RAIMAD's source code to mirror them.
"""

from typing import Any
from typing import Iterator
import ast
import re


# One day you are young, hopeful, and full of energy,
# and the next you are parsing C++ code with regex
DITHER_FINDER = re.compile(
    r'\s*//\s*(\d+):\s*(.*)$\s*"(.*)"\s*,\s*$',
    re.MULTILINE
    )

def translate(cc_code: str, ass_id: str, dataclass_name: str) -> Iterator[str]:
    """Translate klayout C++ dither pattern defs to Python code."""
    yield f'{ass_id} = rai.DictList({{\n'
    found = re.findall(DITHER_FINDER, cc_code)
    prev_num = -1
    for num, _comment_name, name in found:
        num = int(num)
        assert num == prev_num + 1
        prev_num = num

        #yield num, name
        print(num, name)
        yield f"    '{name}': {dataclass_name}('I{num}'),\n"
    yield '}, copy=False)\n'

class Visitor(ast.NodeVisitor):
    """Visit nodes in Python source and find assignment."""

    line_range: None | tuple[int, int]

    def __init__(self, ass_id: str, *args: Any, **kwargs: Any) -> None:
        self.line_range = None
        self.ass_id = ass_id
        super().__init__(*args, **kwargs)

    def visit(self, node: ast.AST) -> None:
        """Visit nodes in Python source and find assignment."""
        match node:
            case ast.Assign(
                    targets=[
                        ast.Name(id=self.ass_id),
                        ],
                    #value=ast.List(),
                    ):

                # ...end line can be None according to mypy???
                # Panic if this is the case.
                assert node.end_lineno is not None

                self.line_range = (node.lineno - 1, node.end_lineno)

                # no need to parse further
                return

        super().generic_visit(node)

def patch_dithers_def(
        file_cc: str,
        file_py: str,
        ass_id: str,
        dataclass_name: str,
        ) -> None:
    """Patch `builtin=` assignment with defs generated from klayout C++."""
    with open(file_py, 'r') as f:
        lines = f.readlines()

    with open(file_cc, 'r') as f:
        cc_source = f.read()
    
    tree = ast.parse(''.join(lines))
    visitor = Visitor(ass_id=ass_id)
    visitor.visit(tree)

    replacement = translate(cc_source, ass_id, dataclass_name)
    assert visitor.line_range is not None
    lines[visitor.line_range[0]:visitor.line_range[1]] = replacement

    with open(file_py, 'w') as f:
        f.writelines(lines)


if __name__ == "__main__":
    patch_dithers_def(
        'reference/vendor/klayout/layDitherPattern.cc',
        'src/raimad/cif/lyp.py',
        'dithers',
        'BuiltinDitherPattern',
        )
    print('a')
    patch_dithers_def(
        'reference/vendor/klayout/layLineStyles.cc',
        'src/raimad/cif/lyp.py',
        'lines',
        'BuiltinLineStyle',
        )

