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

from numpy import degrees
from numpy import sin
from numpy import cos
from numpy import tan
from numpy import pi

# Order of these imports is very important.
# For example, Polygon must be imported before
# and actual polygons, because
# many polygons use these shorthands in their representation.


from PyCIF.draw.Polygon import Polygon
#from PyCIF.draw.Component import Component
from PyCIF.draw.Component import ComponentMeta

from PyCIF.helpers.draw import point_polar
from PyCIF.helpers.draw import point
from PyCIF.helpers.draw import angle_between
from PyCIF.helpers.draw import distance_between

from PyCIF.helpers.angles import fullcircle
from PyCIF.helpers.angles import semicircle
from PyCIF.helpers.angles import quartercircle
from PyCIF.helpers.angles import angspace
from PyCIF.helpers.angles import Orientation

from PyCIF.draw.polygons.Arc import Arc
from PyCIF.draw.polygons.Circle import Circle
from PyCIF.draw.polygons.RectWire import RectWire
from PyCIF.draw.polygons.RectWH import RectWH


