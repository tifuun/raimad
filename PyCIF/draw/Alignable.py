"""
Alignable -- encapsulates transform and bbox
"""

from typing import Self

from PyCIF.draw.Transform import Transform
from PyCIF.draw.PointRef import PointRef
from PyCIF.misc import encapsulation


#def wrap_transform_method(method):
#    def wrapper(self, *args, **kwargs):
#        method(self.transform, *args, **kwargs)
#        return self
#    return wrapper
#
#
#def wrap_bbox_property(prop):
#    def wrapper(self):
#        # We need transformed BBOX here TODO caching?
#        point = prop.fget(self.bbox)
#        return PointRef(self, point)
#    return wrapper


@encapsulation.expose_encapsulated(Transform, 'transform')
class Alignable(object):
    transform: Transform

    def __init__(self):
        self.transform = Transform()
        super().__init__()

    #def snap_top(self, other: Self):
    #    """
    #    Snap on top of other alignable
    #    """
    #    self.bbox.bot_mid.align(other.top_mid)

    #def snap_bot(self, other: Self):
    #    """
    #    Snap on the bottom of other alignable
    #    """
    #    self.bbox.top_mid.align(other.bot_mid)

    #def snap_left(self, other: Self):
    #    """
    #    Snap to the left of other alignable
    #    """
    #    self.bbox.mid_right.align(other.mid_left)

    #def snap_right(self, other: Self):
    #    """
    #    Snap to the right of other alignable
    #    """
    #    self.bbox.mid_left.align(other.mid_left)


