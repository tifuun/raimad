"""boundbbox.py: contains BBox class."""
import raimad as rai

class BoundBBox(rai.AbstractBBox['rai.typing.BoundPoint']):
    """
    BoundBBox: a BBox bound to a Proxy.

    A BoundBBox is just like a BBox, except the points
    returned by its attributes are BoundPoints,
    thus allowing you to perform transformations around
    bbox points of a proxy, for example like this:
    `someproxy.bbox.mid_right.to(somepoint)`
    """

    _proxy: 'rai.typing.Proxy'

    def __init__(
            self,
            proxy: 'rai.typing.Proxy',
            poly: 'rai.typing.Poly | None' = None,
            ) -> None:
        super().__init__(poly)
        self._proxy = proxy

    def interpolate(
            self,
            x_ratio: float,
            y_ratio: float,
            ) -> 'rai.typing.BoundPoint':
        """
        Find a point inside (or outside) the bbox given X and Y ratios.

        So, for example, 0,0 is top left,
        1,1 is bottom right, 0.5,0.5 is center,
        and 0.5,1 is bottom middle.
        The ratios may be negative or higher than 1,
        but doing so would probably make your code difficult to understand.

        Parameters
        ----------
        x_ratio: float
            A number, such that 0 represents all the way to the left
            of the bbox, and 1 represents all the way to the right.
        y_ratio: float
            A number, such that 0 represents all the way to the bottom
            of the bbox, and 1 represents all the way to the top.

        Raises
        ------
        EmptyBBoxError
            if the bbox is empty

        Returns
        -------
        rai.typing.BoundPoint
            The interpolated point.
        """
        point = super()._interpolate(x_ratio, y_ratio)
        return rai.BoundPoint(
            point[0],
            point[1],
            self._proxy
            )

