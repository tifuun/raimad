"""lyp.py: RAIMAD support for KLayout's Layer Properties (.lyp) format."""

from dataclasses import dataclass
from typing import Mapping, TypeAlias, Iterator, Sequence
from warnings import warn
import re

import raimad as rai

@dataclass(frozen=True)
class CustomLineStyle:
    """
    Custom line style.

    The pattern is given as a single string of '*' and '.'.
    Order number is not specified; it is computed automatically during export.
    """

    pattern: str
    name: str

@dataclass(frozen=True)
class BuiltinLineStyle:
    """
    KLayout-builtin line pattern.

    Currently this is just a wrapper for an `str` like `I0`, `I1`, `I2`, etc.

    https://github.com/KLayout/klayout/
    src/laybasic/laybasic/layLineStyles.cc
    """

    def __init__(self, ref: str) -> None:
        object.__setattr__(self, 'ref', ref)  # weird syntax because frozen
        match = re.fullmatch(r'I(\d+)', self.ref)

        if not match:
            warn(
                f"{self.ref}: not a valid klayout builtin line "
                "style reference."
                ,
                UserWarning
                )
            return


        number = int(match.groups()[0])
        if number > 7:
            warn(
                f"{self.ref}: KLayout only has 7 "
                "builtin line styles (starting with `0`)."
                ,
                UserWarning
                )


    ref: str

lines = rai.DictList({
    'solid': BuiltinLineStyle('I0'),
    'dotted': BuiltinLineStyle('I1'),
    'dashed': BuiltinLineStyle('I2'),
    'dash-dotted': BuiltinLineStyle('I3'),
    'short dashed': BuiltinLineStyle('I4'),
    'short dash-dotted': BuiltinLineStyle('I5'),
    'long dashed': BuiltinLineStyle('I6'),
    'dash-double-dotted': BuiltinLineStyle('I7'),
}, copy=False)

@dataclass(frozen=True)
class BuiltinDitherPattern:
    """
    KLayout-builtin dither pattern.

    Currently this is just a wrapper for an `str` like `I0`, `I1`, `I2`, etc.
    Definitions of klayout builtin dither patterns:

    https://github.com/KLayout/klayout/
    src/laybasic/laybasic/layDitherPattern.cc
    """

    def __init__(self, ref: str) -> None:
        object.__setattr__(self, 'ref', ref)  # weird syntax because frozen
        match = re.fullmatch(r'I(\d+)', self.ref)

        if not match:
            warn(
                f"{self.ref}: not a valid klayout builtin dither "
                "pattern reference."
                ,
                UserWarning
                )
            return


        number = int(match.groups()[0])
        if number > 46:
            warn(
                f"{self.ref}: KLayout only has 47 "
                "builtin dither patterns (starting with `0`)."
                ,
                UserWarning
                )


    ref: str

# DO NOT EDIT THIS DICTLIST MANUALLY
# Use scripts/patch_klayout_dither_patterns.py

dithers = rai.DictList({
    'solid': BuiltinDitherPattern('I0'),
    'hollow': BuiltinDitherPattern('I1'),
    'dotted': BuiltinDitherPattern('I2'),
    'coarsely dotted': BuiltinDitherPattern('I3'),
    'left-hatched': BuiltinDitherPattern('I4'),
    'lightly left-hatched': BuiltinDitherPattern('I5'),
    'strongly left-hatched dense': BuiltinDitherPattern('I6'),
    'strongly left-hatched sparse': BuiltinDitherPattern('I7'),
    'right-hatched': BuiltinDitherPattern('I8'),
    'lightly right-hatched': BuiltinDitherPattern('I9'),
    'strongly right-hatched dense': BuiltinDitherPattern('I10'),
    'strongly right-hatched sparse': BuiltinDitherPattern('I11'),
    'cross-hatched': BuiltinDitherPattern('I12'),
    'lightly cross-hatched': BuiltinDitherPattern('I13'),
    'checkerboard 2px': BuiltinDitherPattern('I14'),
    'strongly cross-hatched sparse': BuiltinDitherPattern('I15'),
    'heavy checkerboard': BuiltinDitherPattern('I16'),
    'hollow bubbles': BuiltinDitherPattern('I17'),
    'solid bubbles': BuiltinDitherPattern('I18'),
    'pyramids': BuiltinDitherPattern('I19'),
    'turned pyramids': BuiltinDitherPattern('I20'),
    'plus': BuiltinDitherPattern('I21'),
    'minus': BuiltinDitherPattern('I22'),
    '22.5 degree down': BuiltinDitherPattern('I23'),
    '22.5 degree up': BuiltinDitherPattern('I24'),
    '67.5 degree down': BuiltinDitherPattern('I25'),
    '67.5 degree up': BuiltinDitherPattern('I26'),
    '22.5 degree cross hatched': BuiltinDitherPattern('I27'),
    'zig zag': BuiltinDitherPattern('I28'),
    'sine': BuiltinDitherPattern('I29'),
    'heavy unordered': BuiltinDitherPattern('I30'),
    'light unordered': BuiltinDitherPattern('I31'),
    'vertical dense': BuiltinDitherPattern('I32'),
    'vertical': BuiltinDitherPattern('I33'),
    'vertical thick': BuiltinDitherPattern('I34'),
    'vertical sparse': BuiltinDitherPattern('I35'),
    'vertical sparse, thick': BuiltinDitherPattern('I36'),
    'horizontal dense': BuiltinDitherPattern('I37'),
    'horizontal': BuiltinDitherPattern('I38'),
    'horizontal thick': BuiltinDitherPattern('I39'),
    'horizontal sparse': BuiltinDitherPattern('I40'),
    'horizontal sparse, thick': BuiltinDitherPattern('I41'),
    'grid dense': BuiltinDitherPattern('I42'),
    'grid': BuiltinDitherPattern('I43'),
    'grid thick': BuiltinDitherPattern('I44'),
    'grid sparse': BuiltinDitherPattern('I45'),
    'grid sparse, thick': BuiltinDitherPattern('I46'),
}, copy=False)


@dataclass(frozen=True)
class CustomDitherPattern:
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
    dither_pattern: CustomDitherPattern | BuiltinDitherPattern | None = None
    line_style: CustomLineStyle | BuiltinLineStyle | None = None
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
    styles = _extract_line_styles(lyp)

    yield from _export_dither_patterns(patterns)
    yield from _export_line_styles(styles)

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
            if isinstance(layer.dither_pattern, CustomDitherPattern):
                pattern_idx = patterns[layer.dither_pattern]
                yield f'<dither-pattern>C{pattern_idx}</dither-pattern>'
            elif isinstance(layer.dither_pattern, BuiltinDitherPattern):
                yield (
                    '<dither-pattern>'
                    f'{layer.dither_pattern.ref}'
                    '</dither-pattern>'
                    )
            else:
                assert False

        if layer.line_style is not None:
            if isinstance(layer.line_style, CustomLineStyle):
                style_idx = styles[layer.line_style]
                yield f'<line-style>C{style_idx}</line-style>'
            elif isinstance(layer.line_style, BuiltinLineStyle):
                yield (
                    '<line-style>'
                    f'{layer.line_style.ref}'
                    '</line-style>'
                    )
            else:
                assert False

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
        ) -> Mapping[CustomDitherPattern, int]:
    patterns: dict[CustomDitherPattern, int] = {}
    idx = 0
    for layer in lyp.values():
        if not isinstance(layer.dither_pattern, CustomDitherPattern):
            continue

        patterns[layer.dither_pattern] = idx
        idx += 1

    return patterns

def _export_dither_patterns(
        patterns: Mapping[CustomDitherPattern, int]
        ):
    for pattern, order in patterns.items():

        if not isinstance(pattern, CustomDitherPattern):
            continue

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

def _extract_line_styles(
        lyp: LayerProperties
        ) -> Mapping[CustomLineStyle, int]:
    styles: dict[CustomLineStyle, int] = {}
    idx = 0
    for layer in lyp.values():
        if not isinstance(layer.line_style, CustomLineStyle):
            continue

        styles[layer.line_style] = idx
        idx += 1

    return styles

def _export_line_styles(
        styles: Mapping[CustomLineStyle, int]
        ):
    for style, order in styles.items():

        if not isinstance(style, CustomLineStyle):
            continue

        yield '<custom-line-style>'

        yield f'<pattern>{style.pattern}</pattern>'

        if len(style.pattern) > 32:
            # TODO test warnings
            warn(
                "Line style longer than 32",
                UserWarning
                )

        if set(style.pattern) > {'.', '*'}:
            warn(
                "Line style contains characters other than `.` and `*`.",
                UserWarning
                )

        yield f'<order>{order}</order>'
        yield f'<name>{style.name}</name>'

        yield '</custom-line-style>'



