"""
__init__.py file of PyCIF
Right now, it is used for namespace flattening
(e.g. exposing deeply-nested objects, such as
PyCIF.helpers.angles.angspace through
through friendlier paths like
PyCIF.angspace.

Many convenience functions from numpy are also made available
(sin, cos, degrees, etc.)
"""

from numpy import radians as degrees
from numpy import sin
from numpy import cos
from numpy import tan
from numpy import pi

# Order of these imports is very important.
# For example, Polygon must be imported before
# and actual polygons, because
# many polygons use these shorthands in their representation.

from addict import Dict


from PyCIF.draw.Transform import Transform
from PyCIF.draw.Markable import Markable
from PyCIF.draw.BBox import BBox
from PyCIF.draw.Polygon import Polygon
from PyCIF.draw.PolygonGroup import PolygonGroup
#from PyCIF.draw.Component import Component
from PyCIF.draw.Option import Option
from PyCIF.draw.Layer import Layer
from PyCIF.draw.Component import Component
from PyCIF.draw.Partial import Partial

from PyCIF import typing

from PyCIF.helpers.draw import to_polar
from PyCIF.helpers.draw import point_polar
from PyCIF.helpers.draw import point
from PyCIF.helpers.draw import angle_between
from PyCIF.helpers.draw import distance_between
from PyCIF.helpers.draw import midpoint
from PyCIF.helpers.draw import bounding_box_cartesian
from PyCIF.helpers.draw import bounding_box_size

from PyCIF.helpers.angles import fullcircle
from PyCIF.helpers.angles import semicircle
from PyCIF.helpers.angles import quartercircle
from PyCIF.helpers.angles import angspace
from PyCIF.helpers.angles import Orientation

from PyCIF.helpers import iter  # TODO good practice? (iter is built-in name)
from PyCIF.helpers.overload import kwoverload

from PyCIF.draw.polygons.Arc import Arc
from PyCIF.draw.polygons.Circle import Circle
from PyCIF.draw.polygons.RectWire import RectWire
from PyCIF.draw.polygons.RectWH import RectWH
from PyCIF.draw.polygons.CustomPolygon import CustomPolygon

from PyCIF import viz as viz

from PyCIF.draw.TransmissionLine import path
#from PyCIF.draw.PolygonGroup import PolygonGroup

