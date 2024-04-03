import numpy as np
Point = np.ndarray  # TODO

from numpy import radians as degrees
radians = lambda r: r

class EmptyType:
    def __bool__(self):
        return False

    def __str__(self):
        return "<Empty>"

    def __repr__(self):
        return "<Empty>"

Empty = EmptyType()

from pycif.helpers import *
from pycif.iters import (
    overlap,
    nonoverlap,

    duplets,
    triplets,
    quadlets,
    quintlets,

    couples,
    triples,
    quadles,
    quintles,

    flatten,
    braid
    )
from pycif.string_import import string_import
from pycif.docparse import split_docstring

from pycif.dictlist import DictList

from pycif.mark import Mark
from pycif.layer import Layer
from pycif.option import Option
from pycif.boundpoint import BoundPoint
from pycif.transform import Transform
from pycif.compo import Compo
from pycif.proxy import Proxy
from pycif.bbox import BBox

from pycif.rectwh import RectWH
from pycif.rectwire import RectWire
from pycif.circle import Circle
from pycif.ansec import AnSec
from pycif.custompoly import CustomPoly

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

from pycif.snowman import Snowman

