"""
Alignable -- encapsulates transform and bbox
"""

from typing import Self

from PyClewinSDC.Transform import Transform
from PyClewinSDC.BBox import BBox
from PyClewinSDC.PointRef import PointRef


def wrap_transform_method(method):
    def wrapper(self, *args, **kwargs):
        method(self.transform, *args, **kwargs)
        return self
    return wrapper


def wrap_bbox_property(prop):
    def wrapper(self):
        # We need transformed BBOX here TODO caching?
        point = prop.fget(self.bbox)
        return PointRef(self, point)
    return wrapper


class Alignable(object):
    def __init__(
            self,
            transform: Transform | None = None,
            bbox: BBox | None = None,
            ):

        self.transform = transform.copy() if transform else Transform()
        self._bbox = bbox.copy() if bbox else BBox()

    @property
    def bbox(self):
        """
        Return a bbox with correct transformation
        """
        # TODO caching
        return self._bbox.copy().apply_transform(self.transform)

    # TODO possible to embed docstrings?
    apply_transform = wrap_transform_method(Transform.apply_transform)
    move = wrap_transform_method(Transform.move)
    movex = wrap_transform_method(Transform.movex)
    movey = wrap_transform_method(Transform.movey)
    scale = wrap_transform_method(Transform.scale)
    rot = wrap_transform_method(Transform.rot)
    hflip = wrap_transform_method(Transform.hflip)
    vflip = wrap_transform_method(Transform.vflip)
    flip = wrap_transform_method(Transform.flip)

    # TODO docstrings for property
    top_left = property(wrap_bbox_property(BBox.top_left))
    top_mid = property(wrap_bbox_property(BBox.top_mid))
    top_right = property(wrap_bbox_property(BBox.top_right))

    mid_left = property(wrap_bbox_property(BBox.mid_left))
    mid = property(wrap_bbox_property(BBox.mid))
    mid_right = property(wrap_bbox_property(BBox.mid_right))

    bot_left = property(wrap_bbox_property(BBox.bot_left))
    bot_mid = property(wrap_bbox_property(BBox.bot_mid))
    bot_right = property(wrap_bbox_property(BBox.bot_right))

    def snap_top(self, other: Self):
        """
        Snap on top of other alignable
        """
        self.bot_mid.align(other.top_mid)

    def snap_bot(self, other: Self):
        """
        Snap on the bottom of other alignable
        """
        self.top_mid.align(other.bot_mid)

    def snap_left(self, other: Self):
        """
        Snap to the left of other alignable
        """
        self.mid_right.align(other.mid_left)

    def snap_right(self, other: Self):
        """
        Snap to the right of other alignable
        """
        self.mid_left.align(other.mid_left)

