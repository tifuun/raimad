import numpy as np
Point = np.ndarray  # TODO

from numpy import radians as degrees
radians = lambda r: r

from pycif.helpers import *

from pycif.Mark import Mark
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

