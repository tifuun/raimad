"""svg.py: tools for rendering compos as svg pictures."""

from typing import Iterator

import raimad as rai

def export_svg(compo: 'rai.typing.CompoLike') -> str:
    """
    Make an SVG representation of a component.

    Parameters
    ----------
    compo : rai.typing.CompoLike
        Component (or Proxy pointing to a component)
        to export to svg.

    Returns
    -------
    str
        A string containing the SVG image.
    """
    return ''.join(yield_svg(compo))

def yield_svg(compo: 'rai.typing.CompoLike') -> Iterator[str]:
    """
    Make an SVG representation of a component.

    Unlike `export_svg`, this function yields parts of the SVG
    file, instead of returning the entire string all at once.

    Parameters
    ----------
    compo : rai.typing.CompoLike
        Component (or Proxy pointing to a component)
        to export to svg.

    Returns
    -------
    Iterator[str]
        strings containing fragments of the SVG file
    """
    bbox = compo.bbox.pad(10)

    yield (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{bbox.length}" '
        f'height="{bbox.width}" '
        '>\n'
        '\n'
        f'<g transform="translate({-bbox.left},{bbox.top})">\n'
        # TODO handle neg left correctly?
        '<g transform="scale(1,-1)">\n'
        )

    for layer_name, layer_geoms in compo.steamroll().items():
        for geom in layer_geoms:
            yield (
                '<polygon '
                'fill="#00000000" '
                'stroke="#000000" '
                'stroke-width="1" '
                'points="'
                )

            for point in geom:
                yield f'{point[0]},{point[1]} '

            yield '" />\n'

    yield '</g></g></svg>\n'

