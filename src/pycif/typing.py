"""
typing.py
A collection of type hints
"""

from typing import TypeAlias, Sequence, Any
import numpy as np
import pycif as pc

CompoClass: TypeAlias = type[pc.Compo] | pc.Partial
Compo: TypeAlias = pc.Compo | pc.Proxy
RealCompo: TypeAlias = pc.Compo
Proxy: TypeAlias = pc.Proxy
Point: TypeAlias = \
        tuple[float, float] | \
        np.typing.NDArray[np.float64] | \
        pc.BoundPoint
Poly: TypeAlias = Sequence[Point]
PolyArray: TypeAlias = np.typing.NDArray[np.float64]
Polys: TypeAlias = Sequence[Poly]
Geoms: TypeAlias = dict[str, Polys]
Transform: TypeAlias = pc.Transform
BBox: TypeAlias = pc.BBox
Affine: TypeAlias = np.typing.NDArray[np.float64]

LMapShorthand: TypeAlias = None | str | dict[str, str]
#XYarray: TypeAlias = np.ndarray[Any, Point]
#Geoms: TypeAlias = dict[str, list[XYarray]]
LMap: TypeAlias = pc.LMap


