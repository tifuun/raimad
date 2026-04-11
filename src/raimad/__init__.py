"""__init__.py: Namespace flattening for RAIMAD."""

import sys

from raimad import types

from raimad.empty import Empty, EmptyType
from raimad import graphviz as gv
from raimad import saveto
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
    is_lname_valid,
    vec2s,
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

from raimad.cif.lyp import export_lyp
from raimad.cif import lyp

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


epsilon = sys.float_info.epsilon

# __all__ should contain all re-exported objects
# (checked by mypy and ruff)
# do not edit this definition manually;
# use scripts/patch_dunder_all.py
# to update automatically.

__all__ = [
    "sys",
    "types",
    "Empty",
    "EmptyType",
    "graphviz",
    "saveto",
    "fullcircle",
    "halfcircle",
    "quartercircle",
    "eigthcircle",
    "semicircle",
    "demisemicircle",
    "hemidemisemicircle",
    "angle_between",
    "polar",
    "is_compo_class",
    "custom_base",
    "WINGDINGS",
    "wingdingify",
    "midpoint",
    "add",
    "eq",
    "sub",
    "distance_between",
    "is_lname_valid",
    "vec2s",
    "affine",
    "iters",
    "overlap",
    "nonoverlap",
    "duplets",
    "triplets",
    "quadlets",
    "quintlets",
    "couples",
    "triples",
    "quadles",
    "quintles",
    "flatten",
    "braid",
    "string_import",
    "FilteredDictList",
    "DictList",
    "Annotation",
    "Mark",
    "Layer",
    "Option",
    "BoundPoint",
    "Transform",
    "Compo",
    "MarksContainer",
    "SubcompoContainer",
    "ProxyableDictList",
    "Proxy",
    "LMap",
    "Partial",
    "AbstractBBox",
    "BBox",
    "BoundBBox",
    "RectLW",
    "RectWire",
    "Circle",
    "AnSec",
    "CustomPoly",
    "typing",
    "typing",
    "cif",
    "export_cif",
    "export_svg",
    "show",
    "err",
    "export_lyp",
    "lyp",
    "fortune",
    "fortunes_technology",
    "fortunes_economy",
    "fortunes_education",
    "fortunes_politics",
    "fortunes_engineering",
    "fortunes_resilience",
    "fortunes_misc",
    "fortunes_all",
    "Snowman",
    ]


