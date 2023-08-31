from typing import Any, Type

import numpy as np

from PyCIF.draw.Component import Component
from PyCIF.draw.Partial import Partial

Point = np.ndarray
ComponentClass = Type[Component] | Partial

