"""
Namespace flattening for RAIMAD.
"""

import numpy as np
Point = np.ndarray  # TODO

from raimad.empty import Empty
from raimad import graphviz as gv
from raimad.helpers import *
from raimad import affine
import raimad.iters as iters
from raimad.iters import (
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
from raimad.string_import import string_import
from raimad.docparse import split_docstring

from raimad.dictlist import DictList

from raimad.mark import Mark
from raimad.layer import Layer
from raimad.option import Option
from raimad.boundpoint import BoundPoint
from raimad.transform import Transform
from raimad.compo import Compo
from raimad.compo import MarksContainer
from raimad.compo import SubcompoContainer
from raimad.proxy import Proxy
from raimad.proxy import LMap
from raimad.partial import Partial
from raimad.bbox import BBox

from raimad.rectlw import RectLW
from raimad.rectwire import RectWire
from raimad.circle import Circle
from raimad.ansec import AnSec
from raimad.custompoly import CustomPoly

from raimad import typing

from raimad import cif
from raimad.cif.shorthand import export_cif
from raimad.svg import export_svg
from raimad import err
from raimad import debug

from raimad.checker.violations import (
    Viol,
    MarksViol,
    LenientViol,
    RAI412,
    RAI442
    )

from raimad.checker.checker import (
    check_compo,
    check_module,
    Flake8Checker
    )

from raimad.snowman import Snowman

# Mypy really wants __all__ to be present
__all__ = [
    'export_svg',
    'Transform',
    'Compo',
    'DictList',
    'Proxy',
    'BoundPoint',
    'MarksContainer',
    'SubcompoContainer',
    'BBox',
    'Partial',
    'LMap',
    ]


