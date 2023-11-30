"""
Scalable Vector Graphics Exporter.
"""

from io import IOBase, StringIO
import typing
from pathlib import Path

import numpy as np

import pycif as pc

COLORS = [  # Matplotlib tab10 colorscheme ;D
    '1f77b4',
    'ff7f0e',
    '2ca02c',
    'd62728',
    '9467bd',
    '8c564b',
    'e377c2',
    '7f7f7f',
    'bcbd22',
    '17becf',
    ]

def _export_svg(stream, component: pc.Component):
    """
    Export SVG file to stream.
    """
    bbox = component.bbox.pad(10)

    stream.write(
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{bbox.width}" '
        f'height="{bbox.height}" '
        #f'viewBox="{bbox.left} {bbox.bottom} {bbox.width} {bbox.height}"'
        '>\n'
        '\n'
        f'<g transform="translate({-bbox.left},{bbox.top})">\n'
        # TODO handle neg left correctly?
        '<g transform="scale(1,-1)">\n'
        )

    for index, color in enumerate(COLORS):
        stream.write(
            '<pattern '
            f'id="hatch_{index}" '
            'patternUnits="userSpaceOnUse" width="4" height="4">'
            '<path d="M-1,1 l2,-2'
            '   M0,4 l4,-4'
            '   M3,5 l2,-2" '
            f'   style="stroke:#{color}; stroke-width:1" />'
            '</pattern>\n'
            )

    for subpoly in component.get_subpolygons():
        poly = subpoly.polygon

        color_index = sum(map(ord, subpoly.layer)) % len(COLORS)

        stream.write(
            '<polygon '
            f'fill="url(#hatch_{color_index})" '
            f'stroke="#{COLORS[color_index]}" '
            'stroke-width="1" '
            'points="'
            )

        try:
            for point in poly.get_xyarray():
                stream.write(f'{point[0]},{point[1]} ')

        except Exception as e:
            raise Exception(
                f'Failed to export polygon {subpoly}. ',
                ) from e

        stream.write('" />\n')

    stream.write('</g></g></svg>\n')


def export_svg(
        component: pc.Component,
        dest: None | str | Path | IOBase = None):
    """
    Export SVG file as string or to stream or to filename
    """
    if dest is None:
        stream = StringIO()
        _export_svg(stream, component)
        return stream.getvalue()

    elif isinstance(dest, str | Path):
        with open(dest, 'w') as file:
            _export_svg(file, component)

    elif isinstance(dest, IOBase):
        _export_svg(dest, component)

    else:
        raise Exception(f"Cannot export to {dest}")

