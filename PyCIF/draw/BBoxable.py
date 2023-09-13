from typing import Self
import numpy as np
import PyCIF as pc

class BBoxable():
    #_bbox: pc.BBox
    _xyarray: np.ndarray

    #@abstractmethod
    def _get_xyarray(self):
        """
        Get array of x,y coordinate pairs in internal coordinates
        (i.e. without applying transformation).

        Polygons should override this method with one that actually
        generates their representation as an xyarray in internal coordinates.
        """
        raise NotImplementedError()

    def get_xyarray(self):
        """
        Get array of x,y coordinate pairs in external coordinates
        (i.e. with transformation).

        Polygons should not override this method.
        Polygons should instead override the provate method
        `_get_xyarray()`.
        This method simply calls `_get_xyarray()` and applies
        the transformation.
        """
        # TODO caching breaks everything when bbox is used
        if self._xyarray is None or 1:
            self._xyarray = self.transform.transform_xyarray(
                self._get_xyarray()
                )
        return self._xyarray

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self._bbox = pc.BBox()

    # FIXME huge mess

    @property
    def _bbox(self):
        return pc.BBox(self._get_xyarray())
        #return self._bbox.copy().apply_transform(self.transform)

    @property
    def bbox(self):
        return pc.BBox(self._get_xyarray(), self)

    #def snap_below(self, to: Self):
    #    self.align_marks(
    #        'top_mid',
    #        to,
    #        'bottom_mid',
    #        )

    #    return self

    #def snap_above(self, to: Self):
    #    self.align_marks(
    #        'bottom_mid',
    #        to,
    #        'top_mid',
    #        )
    #    # TODO helpful error messages if marks are missing
    #    # Or maybe protocols somehow??

    #    return self

    #def align_to(self, to: Self, mark_name='mid'):
    #    self.align_marks(
    #        mark_name,
    #        to,
    #        mark_name,
    #        )


#"""
#Alignable -- encapsulates transform and bbox
#"""
#
#from typing import Self
#
#from PyCIF.Transform import Transform
#from PyCIF.BBox import BBox
#from PyCIF.PointRef import PointRef
#
#
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
#
#
#class Alignable(object):
#    def __init__(
#            self,
#            transform: Transform | None = None,
#            bbox: BBox | None = None,
#            ):
#
#        self.transform = transform.copy() if transform else Transform()
#        self._bbox = bbox.copy() if bbox else BBox()
#
#    @property
#    def bbox(self):
#        """
#        Return a bbox with correct transformation
#        """
#        # TODO caching
#        return self._bbox.copy().apply_transform(self.transform)
#
#    # TODO possible to embed docstrings?
#    apply_transform = wrap_transform_method(Transform.apply_transform)
#    move = wrap_transform_method(Transform.move)
#    movex = wrap_transform_method(Transform.movex)
#    movey = wrap_transform_method(Transform.movey)
#    scale = wrap_transform_method(Transform.scale)
#    rot = wrap_transform_method(Transform.rot)
#    hflip = wrap_transform_method(Transform.hflip)
#    vflip = wrap_transform_method(Transform.vflip)
#    flip = wrap_transform_method(Transform.flip)
#
#    # TODO docstrings for property
#    top_left = property(wrap_bbox_property(BBox.top_left))
#    top_mid = property(wrap_bbox_property(BBox.top_mid))
#    top_right = property(wrap_bbox_property(BBox.top_right))
#
#    mid_left = property(wrap_bbox_property(BBox.mid_left))
#    mid = property(wrap_bbox_property(BBox.mid))
#    mid_right = property(wrap_bbox_property(BBox.mid_right))
#
#    bot_left = property(wrap_bbox_property(BBox.bot_left))
#    bot_mid = property(wrap_bbox_property(BBox.bot_mid))
#    bot_right = property(wrap_bbox_property(BBox.bot_right))
#
#    def snap_top(self, other: Self):
#        """
#        Snap on top of other alignable
#        """
#        self.bot_mid.align(other.top_mid)
#
#    def snap_bot(self, other: Self):
#        """
#        Snap on the bottom of other alignable
#        """
#        self.top_mid.align(other.bot_mid)
#
#    def snap_left(self, other: Self):
#        """
#        Snap to the left of other alignable
#        """
#        self.mid_right.align(other.mid_left)
#
#    def snap_right(self, other: Self):
#        """
#        Snap to the right of other alignable
#        """
#        self.mid_left.align(other.mid_left)
#
#