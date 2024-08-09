import raimad as rai

class BoundBBox(rai.AbstractBBox['rai.typing.BoundPoint']):
    _proxy: 'rai.typing.Proxy'

    def __init__(
            self,
            proxy: 'rai.typing.Proxy',
            xyarray: 'rai.typing.Poly | None' = None,
            ) -> None:
        """
        Create a new BBox.

        Parameters
        ----------
        xyarray: np.ndarray | None
            A N x 2 numpy array containing points to initialize the bbox with.
            This is optional.
        proxy: rai.Proxy | None
            The proxy that this bbox should be bound to.
            This is optional.
        """
        super().__init__(xyarray)
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
        rai.Point | pc.BoundPoint
            A regular rai.Point for unbound bboxes,
            and a rai.BoundPoint for bound bboxes.
        """
        point = super()._interpolate(x_ratio, y_ratio)
        return rai.BoundPoint(
            point[0],
            point[1],
            self._proxy
            )

    mid_left: 'rai.typing.BoundPoint'

