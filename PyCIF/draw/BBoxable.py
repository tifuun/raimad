"""BBoxable.py: contains BBoxable class."""

from typing import Self

import numpy as np

import PyCIF as pc

class BBoxable(pc.Transformable):
    """
    BBoxable: Objects with coordinate points and a bounding box.

    BBoxable serves as a base class for Polygons, Groups, and Components.
    It provides functionality for easily retrieving a (bounded) bbox,
    as well as snapping objects to each other.

    See also
    --------
    BBoxable.py
    """

    def _get_xyarray(self) -> np.ndarray:
        """
        Get array of x,y coordinate pairs in internal coordinates.

        Polygons should override this method with one that actually
        generates their representation as an xyarray in internal coordinates.

        Returns
        -------
        np.ndarray
            Untransformed (i.e. internal coordinate system)
            N x 2 array of points
        """
        raise NotImplementedError()

    def get_xyarray(self) -> np.ndarray:
        """
        Get array of x,y coordinate pairs in external coordinates.

        Polygons should NOT override this method.
        Polygons should instead override the provate method
        `_get_xyarray()`.
        This method simply calls `_get_xyarray()` and applies
        the transformation.


        Returns
        -------
        np.ndarray
            Transformed (i.e. external coordinate system)
            N x 2 array of points
        """
        return self.transform.transform_xyarray(
            self._get_xyarray()
            )

    # FIXME huge mess
    # TODO can the above FIXME be removed?

    @property
    def _bbox(self) -> pc.BBox:
        """
        Get unbounded bbox in internal coordinates.

        Returns
        -------
        pc.BBox
            Unbounded bbox in internal coordinates
        """
        return pc.BBox(self._get_xyarray())

    @property
    def bbox(self) -> pc.BBox:
        """
        Get bounded bbox in external coordinates.

        Returns
        -------
        pc.BBox
            Bounded bbox in external coordinates
        """
        return pc.BBox(self.get_xyarray(), self)

    def snap_below(self, other: Self) -> Self:
        """
        Snap self to the bottom of another BBoxable.

        Equivalent to aligning self.bbox.top_mid
        to other.bbox.bot_mid
        Like this:

        .----------.----------.
        |                     |
        .        other        .
        |                     |
        .-----.----X----.-----.
              |         |
              .   self  .
              |         |
              .----.----.

        Returns
        -------
        Self
            returns self, can be used for chaining transformations.
        """
        self.bbox.top_mid.to(other.bbox.bot_mid)
        return self

    def snap_above(self, other: Self) -> Self:
        """
        Snap self to the top of another BBoxable.

        Equivalent to aligning self.bbox.bot_mid
        to other.bbox.top_mid
        Like this:

              .----.----.
              |         |
              .   self  .
              |         |
        .-----.----X----.-----.
        |                     |
        .        other        .
        |                     |
        .----------.----------.

        Returns
        -------
        Self
            returns self, can be used for chaining transformations.
        """
        self.bbox.bot_mid.to(other.bbox.top_mid)
        return self

    def snap_right(self, other: Self) -> Self:
        """
        Snap self to the right of another BBoxable.

        Equivalent to aligning self.bbox.mid_left
        to other.bbox.mid_right
        Like this:

        .---.---.
        |       |
        |       .----.----.
        |       |         |
        . other X   self  |
        |       |         |
        |       .----.----.
        |       |
        .-------.

        Returns
        -------
        Self
            returns self, can be used for chaining transformations.
        """
        self.bbox.mid_left.to(other.bbox.mid_right)
        return self

    def snap_left(self, other: Self) -> Self:
        """
        Snap self to the left of another BBoxable.

        Equivalent to aligning self.bbox.mid_right
        to other.bbox.mid_left
        Like this:

                  .-------.
                  |       |
        .----.----.       |
        |         |       |
        .   self  X other .
        |         |       |
        .----.----.       |
                  |       |
                  .-------.

        Returns
        -------
        Self
            returns self, can be used for chaining transformations.
        """
        self.bbox.mid_right.to(other.bbox.mid_left)
        return self

