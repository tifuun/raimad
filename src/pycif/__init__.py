import numpy as np
Point = np.ndarray  # TODO

from numpy import radians as degrees
radians = lambda r: r

from pycif.helpers import *

from pycif.Mark import Mark, MarkAnnot
from pycif.Layer import Layer, LayerAnnot
from pycif.Option import Option, OptionAnnot
from pycif.Transform import Transform
from pycif.Compo import Compo
from pycif.Proxy import Proxy
from pycif.BoundPoint import BoundPoint
from pycif.BBox import BBox

from pycif.RectWH import RectWH
from pycif.RectWire import RectWire
from pycif.Circle import Circle
from pycif.AnSec import AnSec

from pycif.cif import export_cif
from pycif import err
from pycif import debug

from pycif.checker.violations import (
    Viol,
    MarksViol,
    LenientViol,
    RAI412,
    RAI442
    )

from pycif.checker.checker import (
    check_compo,
    check_module,
    Flake8Checker
    )

