"""
Namespace flattening for RAIMAD.
If you're confused by the redundant `import X as X` syntax,
that's because mypy wants it that way.
"""

import numpy as np
Point = np.ndarray  # TODO

from pycif.empty import Empty
from pycif import graphviz as gv
from pycif.helpers import *
from pycif import affine
import pycif.iters as iters
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
from pycif.compo import Compo as Compo
from pycif.proxy import Proxy as Proxy
from pycif.proxy import LMap
from pycif.partial import Partial
from pycif.bbox import BBox

from pycif.rectwh import RectWH
from pycif.rectwire import RectWire
from pycif.circle import Circle
from pycif.ansec import AnSec
from pycif.custompoly import CustomPoly

from pycif import typing

from pycif.cif import export_cif
from pycif.cif import CIFExporter
from pycif.svg import export_svg
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


