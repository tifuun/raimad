"""__init__.py: Namespace flattening for RAIMAD."""

import sys

epsilon = sys.float_info.epsilon

from raimad.empty import Empty, EmptyType
from raimad import graphviz as gv
from raimad.helpers import (
    fullcircle,
    halfcircle,
    quartercircle,
    eigthcircle,
    semicircle,
    demisemicircle,
    hemidemisemicircle,
    angle_between,
    polar,
    is_compo_class,
    custom_base,
    WINGDINGS,
    wingdingify,
    midpoint,
    add,
    eq,
    sub,
    distance_between,
    )
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
from raimad.compo import ProxyableDictList
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
from raimad import typing as t

from raimad import cif
from raimad.cif.shorthand import export_cif
from raimad.svg import export_svg
from raimad.show import show
from raimad import err

from raimad.fortune import fortune
from raimad.fortune import fortunes_technology
from raimad.fortune import fortunes_economy
from raimad.fortune import fortunes_education
from raimad.fortune import fortunes_politics
from raimad.fortune import fortunes_engineering
from raimad.fortune import fortunes_resilience
from raimad.fortune import fortunes_misc
from raimad.fortune import fortunes_all

from raimad.snowman import Snowman

# The function of __all__ is to specify which things get imported
# when someone does `from raimad import *`,
# but it also lets tools like ruff and mypy know that we're
# importing these things for the purpose of namespace flattening,
# so they don't complain that these are "unused" imports
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
    'Snowman',
    'err',
    'cif',
    'split_docstring',  # TODO is needed?
    'braid',
    'flatten',
    'quintles',
    'quadles',
    'triples',
    'couples',
    'quintlets',
    'quadlets',
    'triplets',
    'duplets',
    'overlap',
    'nonoverlap',
    'iters',
    'affine',
    'fullcircle',
    'halfcircle',
    'quartercircle',
    'eigthcircle',
    'semicircle',
    'demisemicircle',
    'hemidemisemicircle',
    'angle_between',
    'polar',
    'is_compo_class',
    'custom_base',
    'WINGDINGS',
    'wingdingify',
    'midpoint',
    'gv',
    'add',
    'eq',
    'epsilon',
    'show',
    'distance_between',
    'fortune',
    'fortunes_technology',
    'fortunes_economy',
    'fortunes_education',
    'fortunes_politics',
    'fortunes_engineering',
    'fortunes_resilience',
    'fortunes_misc',
    'fortunes_all',
    ]


