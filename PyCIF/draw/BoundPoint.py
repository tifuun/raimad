"""BoundPoint.py: contains BoundPoint class."""

import PyCIF as pc

log = pc.get_logger(__name__)

class BoundPoint(pc.Point):
    """
    BoundPoint: Storage for XY coordinate pair and temporaty origin.

    A BoundPoint is just a Point that references a Transformable.
    BoundPoints allow for temporarily treating a specific point
    as the origin for a transformation.

    In other words, BoundPoints
    are what is returned by bound bboxes or markable objects,
    and allow for syntax like:

    mypolygon.bbox.mid.rotate(pc.quartercircle)
    # Rotate 45 degrees around middle

    or
    mycomponent.marks.readout_connection.to((10, 20))
    # Position mycomponent such that the readout connection
    # point is exactly at (10, 20)

    In many ways, BoundPoints allow you to make your code less ambiguous.
    Consider, for example:

    mycomponent.rotate(pc.semicircle)
    # This rotates mycomponent by 45 degrees around the origin
    # of its internal coordinate system.
    # But where is that origin?
    # Anyone reading your code will have to go dig up the source code
    # of mycomponent to figure out

    versus

    mycomponent.bbox.mid.rotate(pc.semicircle)
    # Immediately clear where the component will end up

    That is not to say you must use the BoundPoint interface for
    absolutely all transformations.
    For example, the below point is prefectly concise:

    mycomponent.rotate(45)
    mycomponent.bbox.mid.to((10, 10))
    # It's still ambiguous around which point the first rotation is happening,
    # but it doesn't matter, since the component gets moved
    # to a new position immediately after.

    See Also
    --------
    pc.Markable
    pc.BBoxable
    """

    _transformable: pc.Transformable

    def __init__(self, x: float, y: float, transformable: pc.Transformable):
        """Create a new BoundPoint."""
        super().__init__(x, y)
        self._transformable = transformable

    def to(self, point: pc.Point):
        """Grab the Transformable by this point and move it to another point."""
        px, py = point
        x = px - self.x
        y = py - self.y
        log.debug('Move %s: %s, %s', self._transformable, point, self)
        self._transformable.move(x, y)
        return self._transformable

    def rotate(self, angle: float):
        """Rotate the Transformable around this point."""
        self._transformable.rotate(angle, self)
        return self._transformable

    def scale(
            self,
            x: float | pc.Point,  # TODO typing.point
            y: float | None = None,
            ) -> pc.Transformable:
        """Scale this Transformable, with this point as the origin."""
        self._transformable.scale(x, y, self.x, self.y)
        return self._transformable

    def hflip(self) -> pc.Transformable:
        """Flip the Transformable horizontaly, with this point as the origin."""
        self._transformable.hflip(self.y)
        return self._transformable

    def vflip(self) -> pc.Transformable:
        """Flip the Transformable vertically, with this point as the origin."""
        self._transformable.vflip(self.x)
        return self._transformable

    def flip(self) -> pc.Transformable:
        """Flip the Transformable, with this point as the origin."""
        self._transformable.flip(self.x, self.y)
        return self._transformable


