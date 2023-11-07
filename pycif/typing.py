from typing import Any, Type, Tuple

import numpy as np

from pycif.draw.Component import Component
from pycif.draw.Partial import Partial
from pycif.draw.Point import Point as pc_Point

Point = np.ndarray | pc_Point | Tuple[float, float]
ComponentClass = Type[Component] | Partial

