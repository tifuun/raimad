from typing import Any, Type, Tuple

import numpy as np

from PyCIF.draw.Component import Component
from PyCIF.draw.Partial import Partial
from PyCIF.draw.Point import Point as pc_Point

Point = np.ndarray | pc_Point | Tuple[float, float]
ComponentClass = Type[Component] | Partial

