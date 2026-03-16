from dataclasses import dataclass
from typing import Mapping, TypeAlias, Iterator

import raimad as rai

@dataclass
class Properties:
    expanded: bool | None = None
    frame_color: str | None = None
    fill_color: str | None = None
    frame_brightness: int | None = None
    fill_brightness: int | None = None
    dither_pattern: str | None = None
    line_style: str | None = None
    valid: bool | None = None
    visible: bool | None = None
    transparent: bool | None = None
    width: int | None = None
    marked: bool | None = None
    xfill: bool | None = None
    animation: int | None = None
    name: str | None = None
    #klay_source: str

LayerProperties: TypeAlias = Mapping[str, Properties]

def export_lyp(
        lyp: LayerProperties,
        dest: rai.saveto.Destination = None,
        ) -> str:
    return rai.saveto._saveto('\n'.join(_export_lyp(lyp)), dest)

def _export_lyp(
        lyp: LayerProperties,
        ) -> Iterator[str]:
    yield '<?xml version="1.0" encoding="utf-8"?>'
    yield '<layer-properties>'

    for source, layer in lyp.items():

        if isinstance(layer, dict):
            layer = Properties(**layer)

        yield '<properties>'

        yield f'<source>{source}</source>'

        if layer.expanded is not None:
            yield f'<expanded>{layer.expanded}</expanded>'

        if layer.frame_color is not None:
            yield f'<frame-color>{layer.frame_color}</frame-color>'

        if layer.fill_color is not None:
            yield f'<fill-color>{layer.fill_color}</fill-color>'

        if layer.frame_brightness is not None:
            yield (
                    '<frame-brightness>'
                    f'{layer.frame_brightness}'
                    '</frame-brightness>'
                    )

        if layer.fill_brightness is not None:
            yield f'<fill-brightness>{layer.fill_brightness}</fill-brightness>'

        if layer.dither_pattern is not None:
            yield f'<dither-pattern>{layer.dither_pattern}</dither-pattern>'

        if layer.line_style is not None:
            yield f'<line-style>{layer.line_style}</line-style>'

        if layer.valid is not None:
            yield f'<valid>{layer.valid}</valid>'

        if layer.visible is not None:
            yield f'<visible>{layer.visible}</visible>'

        if layer.transparent is not None:
            yield f'<transparent>{layer.transparent}</transparent>'

        if layer.width is not None:
            yield f'<width>{layer.width}</width>'

        if layer.marked is not None:
            yield f'<marked>{layer.marked}</marked>'

        if layer.xfill is not None:
            yield f'<xfill>{layer.xfill}</xfill>'

        if layer.animation is not None:
            yield f'<animation>{layer.animation}</animation>'

        if layer.name is not None:
            yield f'<name>{layer.name}</name>'

        yield f'</properties>'

    yield '<name/>'
    yield '</layer-properties>'




