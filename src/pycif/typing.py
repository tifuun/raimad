"""
typing.py
A collection of type hints
"""

from typing import TypeAlias, Sequence
import numpy as np
import pycif as pc

CompoClass: TypeAlias = type[pc.Compo] | pc.Partial
Compo: TypeAlias = pc.Compo | pc.Proxy
RealCompo: TypeAlias = pc.Compo
Proxy: TypeAlias = pc.Proxy
Point: TypeAlias = tuple[float, float] | np.ndarray[float] | pc.BoundPoint
Poly: TypeAlias = Sequence[Point]
Polys: TypeAlias = Sequence[Poly]
Geoms: TypeAlias = dict[str, Polys]
Transform: TypeAlias = pc.Transform

LMapShorthand: TypeAlias = None | str | dict[str, str]
XYarray: TypeAlias = np.ndarray[Point]
Geoms: TypeAlias = dict[str, list[XYarray]]
LMap: TypeAlias = pc.LMap


