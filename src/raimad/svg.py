
def export_svg(compo: 'rai.typing.Compo') -> str:
    return ''.join(yield_svg(compo))

def yield_svg(compo):
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

