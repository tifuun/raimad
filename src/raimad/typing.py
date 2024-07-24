"""
typing.py
A collection of type hints
"""

from typing import Sequence, Any
try:
    from typing import TypeAlias
except ImportError:
    #py3.9 and lower
    from typing_extensions import TypeAlias
    
import raimad as rai

CompoType: TypeAlias = type[rai.Compo]
Partial: TypeAlias = rai.Partial
CompoTypeLike: TypeAlias = type[rai.Compo] | rai.Partial

Compo: TypeAlias = rai.Compo | rai.Proxy
Proxy: TypeAlias = rai.Proxy
CompoLike: TypeAlias = rai.Compo | rai.Proxy

Point: TypeAlias = tuple[float, float]
BoundPoint: TypeAlias = rai.BoundPoint
PointLike: TypeAlias = Point | rai.BoundPoint

Poly: TypeAlias = list[Point]
Polys: TypeAlias = list[Poly]
Geoms: TypeAlias = dict[str, Polys]
Transform: TypeAlias = rai.Transform
BBox: TypeAlias = rai.BBox
BoundBBox: TypeAlias = rai.BoundBBox
Affine: TypeAlias = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
    ]

LMapShorthand: TypeAlias = None | str | dict[str, str]
#XYarray: TypeAlias = np.ndarray[Any, Point]
#Geoms: TypeAlias = dict[str, list[XYarray]]
LMap: TypeAlias = rai.LMap


