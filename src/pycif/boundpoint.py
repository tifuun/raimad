from typing import Any, Self
import numpy as np

import pycif as pc

# see
# https://numpy.org/doc/stable/user/basics.subclassing.html
class BoundPoint(np.ndarray[Any, np.dtype[np.float64]]):

    _proxy: 'pc.typing.Proxy | None'

    def __new__(
            cls,
            input_array: 'pc.typing.Point',
            proxy: 'pc.typing.Proxy'
            ) -> Self:
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj._proxy = proxy
        # Finally, we must return the newly created object:
        return obj

    @property
    def proxy(self) -> 'pc.typing.Proxy':
        if self._proxy is None:
            # TODO exception type
            raise Exception('Unbound BoundPoint')

        return self._proxy

    def __array_finalize__(self, obj: np.typing.NDArray[np.float64] | None) -> None:
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self._proxy = getattr(obj, 'proxy', None)

    def to(self, point: 'pc.typing.Point') -> 'pc.typing.Proxy':
        self.proxy.transform.move(
            point[0] - self[0],
            point[1] - self[1],
            )
        return self.proxy

    def rotate(self, angle: float) -> 'pc.typing.Proxy':
        self.proxy.transform.rotate(
            angle,
            self[0],
            self[1]
            )
        return self.proxy

    def move(self, x: float, y: float) -> 'pc.typing.Proxy':
        """
        `move`ing a boundpoint is functionally identical to `move`ing
        the proxy itself, so there is no reason to call this explicitly.
        However, this function is still defined, so that you can use
        `move` in a chain of actions on a boundpoint
        """
        self.proxy.transform.move(x, y)
        return self.proxy

    # TODO the rest of the functions

