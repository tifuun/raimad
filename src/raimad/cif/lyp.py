"""lyp.py: RAIMAD support for KLayout's Layer Properties (.lyp) format."""

from dataclasses import dataclass
from typing import Mapping, TypeAlias, Iterator, Sequence
from warnings import warn

import raimad as rai

@dataclass(frozen=True)
class DitherPattern:
    """
    Custom dither pattern.

    Lines of the pattern are given as a seuqnce of strings (no newline char).
    Order number is not specified; it is computed automatically during export.
    """

    lines: Sequence[str]
    name: str

@dataclass
class Properties:
    """
    Individual layer properties.

    All fields are the same as in the lyp xml file,
    with two exceptions:
    1. there is not `name` field. A `Properties` object
        is associated with a layer name using a dict.
    2. The `dither_pattern` field is not an index,
        but a `DitherPattern` object.
        Indices are computed automatically.
    """

    expanded: bool | None = None
    frame_color: str | None = None
    fill_color: str | None = None
    frame_brightness: int | None = None
    fill_brightness: int | None = None
    #dither_pattern: str | None = None
    dither_pattern: DitherPattern | None = None
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

class LypExporter:
    """Lyp exporter adhering to the exporter protocol."""

    def __init__(
            self,
            compo: 'rai.typing.CompoLike',
            ) -> None:
        
        if hasattr(compo, '_experimental_lyp'):
            self.cif_string = export_properties(compo._experimental_lyp)
        else:
            self.cif_string = ''

def export_properties(
        lyp: LayerProperties,
        dest: rai.saveto.Destination = None,
        ) -> str:
    """Save LayerProperties to path, file, or stream. Returns saved string."""
    return rai.saveto._saveto('\n'.join(_export_properties(lyp)), dest)

def _export_properties(
        lyp: LayerProperties,
        ) -> Iterator[str]:
    yield '<?xml version="1.0" encoding="utf-8"?>'
    yield '<layer-properties>'

    patterns = _extract_dither_patterns(lyp)

    for pattern, order in patterns.items():
        yield '<custom-dither-pattern>'

        yield '<pattern>'

        if pattern.lines:
            pattern_width = len(pattern.lines[0])

            if pattern_width not in {8, 16, 32}:
                # TODO test warnings
                warn(
                    "Pattern width is not 8, 16, or 32.",
                    UserWarning
                    )

            for line in pattern.lines:
                yield f'<line>{line}</line>'

                if len(line) != pattern_width:
                    warn(
                        "Irregular pattern width.",
                        UserWarning
                        )

                if set(line) > {'.', '*'}:
                    warn(
                        "Pattern line contains characters "
                        "other than `.` and `*`."
                        ,
                        UserWarning
                        )
        else:
            warn(
                "Pattern with no lines...?",
                UserWarning
                )


        yield '</pattern>'

        yield f'<order>{order}</order>'
        yield f'<name>{pattern.name}</name>'

        yield '</custom-dither-pattern>'

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
            pattern_idx = patterns[layer.dither_pattern]
            yield f'<dither-pattern>C{pattern_idx}</dither-pattern>'

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

        yield '</properties>'

    yield '<name/>'
    yield '</layer-properties>'

def _extract_dither_patterns(
        lyp: LayerProperties
        ) -> Mapping[DitherPattern, int]:
    patterns: dict[DitherPattern, int] = {}
    idx = 0
    for layer in lyp.values():
        if layer.dither_pattern is not None:
            patterns[layer.dither_pattern] = idx
        idx += 1
    return patterns



