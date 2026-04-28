#!/usr/bin/env python3
"""Parse dithers from `reference/raidithers` and patch `lyp.yp`."""

from pathlib import Path
from typing import Any
from typing import Iterator
from itertools import batched
import ast
import re

BYTE_FINDER = re.compile(r'0x([0-9a-f][0-9a-f])')

BITS_IN_BYTE = 8
XBM_WIDTH = 32
XBM_HEIGHT = 32

def translate(xbm: str, name: str) -> Iterator[str]:
    """Given a since xbm dither pattern and name, yield python code."""
    yield f"    '{name}': CustomDitherPattern(name='{name}', lines=(\n"
    xbm_bytes = BYTE_FINDER.findall(xbm)
    assert len(xbm_bytes) == XBM_WIDTH * XBM_HEIGHT // BITS_IN_BYTE
    for line in batched(xbm_bytes, XBM_WIDTH // BITS_IN_BYTE):
        yield "        '"
        for byte in line:
            byte = int(byte, 16)
            for bitpos in range(BITS_IN_BYTE):
                yield '.*'[bool(byte & (1 << bitpos))]

        yield "',\n"
    yield "    )),\n"

def translate_all(ass_id:str, xbms: list[tuple[str, str]]) -> Iterator[str]:
    """Given a list of (name, xbm dither pattern), yield python code."""
    yield f'{ass_id} = rai.DictList({{\n'
    for name, xbm in xbms:
        yield from translate(xbm, name)
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

def patch(
        files_xbm: list[Path],
        file_py: Path,
        ) -> None:
    """Parse dithers from `reference/raidithers` and patch `lyp.yp`."""

    ass_id = 'raidithers'

    xbms = [(file.stem, file.read_text()) for file in files_xbm]
    with file_py.open('r') as f:
        lines = f.readlines()

    tree = ast.parse(''.join(lines))
    visitor = Visitor(ass_id=ass_id)
    visitor.visit(tree)

    replacement = translate_all(ass_id, xbms)
    assert visitor.line_range is not None
    lines[visitor.line_range[0]:visitor.line_range[1]] = replacement

    with file_py.open('w') as f:
        f.writelines(lines)


if __name__ == "__main__":
    patch(
        [
            Path("reference/raidithers/tifuun.xbm"),
            Path("reference/raidithers/tifuunalt.xbm"),
            Path("reference/raidithers/pebble.xbm"),
            Path("reference/raidithers/snow.xbm"),
            Path("reference/raidithers/carrot.xbm"),
            Path("reference/raidithers/stratal.xbm"),
            Path("reference/raidithers/raimad.xbm"),
            Path("reference/raidithers/oni.xbm"),
            ],
        Path("src/raimad/cif/lyp.py"),
        )

