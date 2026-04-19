"""Type hints for RAIMAD.

These are used internally,
and you can also use them to annotate your RAIMAD packages.
"""


try:
    from typing import TypeAlias
except ImportError:
    # py3.9 and lower
    from typing_extensions import TypeAlias

import raimad as rai

CompoType: TypeAlias = type[rai.Compo]
Partial: TypeAlias = rai.Partial
CompoTypeLike: TypeAlias = type[rai.Compo] | rai.Partial

BoundPoint: TypeAlias = rai.BoundPoint

Compo: TypeAlias = rai.Compo
Proxy: TypeAlias = rai.Proxy
CompoLike: TypeAlias = rai.Compo | rai.Proxy

Transform: TypeAlias = rai.Transform
BBox: TypeAlias = rai.BBox
BoundBBox: TypeAlias = rai.BoundBBox
Affine: TypeAlias = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
    ]

LMapShorthand: TypeAlias = None | str | dict[str, str | None]
LMap: TypeAlias = rai.LMap

