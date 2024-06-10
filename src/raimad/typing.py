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
    
import numpy as np
import raimad as rai

CompoClass: TypeAlias = type[rai.Compo] | rai.Partial
Compo: TypeAlias = rai.Compo | rai.Proxy
RealCompo: TypeAlias = rai.Compo
Proxy: TypeAlias = rai.Proxy
Point: TypeAlias = \
        tuple[float, float] | \
        np.typing.NDArray[np.float64] | \
        rai.BoundPoint
Poly: TypeAlias = Sequence[Point]
PolyArray: TypeAlias = np.typing.NDArray[np.float64]
Polys: TypeAlias = Sequence[Poly]
Geoms: TypeAlias = dict[str, Polys]
Transform: TypeAlias = rai.Transform
BBox: TypeAlias = rai.BBox
Affine: TypeAlias = np.typing.NDArray[np.float64]

LMapShorthand: TypeAlias = None | str | dict[str, str]
#XYarray: TypeAlias = np.ndarray[Any, Point]
#Geoms: TypeAlias = dict[str, list[XYarray]]
LMap: TypeAlias = rai.LMap

# Well, isn't this lovely?
Bool: TypeAlias = bool | np.bool_


