"""
Namespace flattening for RAIMAD.
"""

import numpy as np
Point = np.ndarray  # TODO

from raimad.empty import Empty, EmptyType
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

from raimad.dictlist import FilteredDictList, DictList

from raimad.annotation import Annotation
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
from raimad.bbox import AbstractBBox, BBox
from raimad.boundbbox import BoundBBox

from raimad.rectlw import RectLW
from raimad.rectwire import RectWire
from raimad.circle import Circle
from raimad.ansec import AnSec
from raimad.custompoly import CustomPoly

from raimad import typing
t = typing

from raimad import cif
from raimad.cif.shorthand import export_cif
from raimad.svg import export_svg
from raimad import err

from raimad.snowman import Snowman

# Mypy really wants __all__ to be present
__all__ = [
    'export_svg',
    'Transform',
    'Compo',
    'FilteredDictList',
    'DictList',
    'Proxy',
    'BoundPoint',
    'MarksContainer',
    'SubcompoContainer',
    'AbstractBBox',
    'BBox',
    'BoundBBox',
    'Partial',
    'LMap',
    'export_cif',
    'string_import',
    'Annotation',
    'Mark',
    'Layer',
    'Option',
    'Empty',
    'EmptyType',
    't',
    'typing',
    'AnSec',
    'Circle',
    'RectLW',
    'RectWire',
    'CustomPoly',
    ]


