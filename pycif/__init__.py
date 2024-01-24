"""
pycif: CAD platform for hierarchical design of on-chip imaging devices.

__init__.py file of pycif
Right now, it is used for namespace flattening
(e.g. exposing deeply-nested objects, such as
pycif.helpers.angles.angspace through
through friendlier paths like
pycif.angspace.

Many convenience functions from numpy are also made available
(sin, cos, degrees, etc.)
"""

from numpy import radians as degrees
from numpy import degrees as radians
from numpy import sin
from numpy import cos
from numpy import tan
from numpy import pi

# Order of these imports is very important.
# For example, Polygon must be imported before
# and actual polygons, because
# many polygons use these shorthands in their representation.

from pycif.logging import get_logger
from pycif.helpers.overload import kwoverload
from pycif.helpers.slots import SlotsFromAnnotationsMeta

from pycif.draw.Point import Point
from pycif.draw.Transform import Transform
from pycif.draw.Transformable import Transformable
from pycif.draw.BoundPoint import BoundPoint
from pycif.draw.BBox import BBox
from pycif.draw.BBoxable import BBoxable
from pycif.draw.Mark import Mark
from pycif.draw.Markable import Markable
from pycif.draw.Polygon import Polygon
from pycif.draw.Group import Group
from pycif.draw import Option
from pycif.draw.Layer import Layer
from pycif.draw.Compo import Compo
from pycif.draw.Partial import Partial

from pycif import typing

from pycif.helpers import iter  # TODO good practice? (iter is built-in name)

from pycif.helpers.draw import to_polar
from pycif.helpers.draw import angle_between
from pycif.helpers.draw import distance_between
from pycif.helpers.draw import midpoint
from pycif.helpers.draw import colinear

from pycif.helpers.angles import fullcircle
from pycif.helpers.angles import halfcircle
from pycif.helpers.angles import quartercircle
from pycif.helpers.angles import semicircle
from pycif.helpers.angles import demisemicircle
from pycif.helpers.angles import angspace
from pycif.helpers.angles import classify_turn
from pycif.helpers.angles import Orientation
from pycif.helpers.angles import TurnDirection

from pycif.draw import TransmissionLine as tl

from pycif.draw.polygons.Arc import Arc
from pycif.draw.polygons.Circle import Circle
from pycif.draw.polygons.RectWire import RectWire
from pycif.draw.polygons.RectWH import RectWH
from pycif.draw.polygons.CustomPolygon import CustomPolygon

from pycif.draw.Snowman import Snowman

from pycif import viz as viz

from pycif.exporters.cif import export_cif
from pycif.exporters.svg import export_svg

from pycif import err

