from typing import Literal, Iterator

import raimad as rai

class BoundPoint():
    def __init__(self, x: float, y: float, proxy: 'rai.typing.Proxy'):
        self._x = x
        self._y = y
        self._proxy = proxy

    def __getitem__(self, index: Literal[0, 1]) -> float:
        if index == 0:
            return self._x

        elif index == 1:
            return self._y

        # This error is here not only for users,
        # but to make sure the unpacking operator works
        # on boundpoints.
        raise IndexError(
            "BoundPoint has only x and y coordinates, "
            "so the index must be either 0 or 1"
            )

    def __iter__(self) -> Iterator[float]:
        return iter((self._x, self._y))

    def __eq__(self, other: object) -> bool:
        if not hasattr(other, "__getitem__"):
            return False

        return bool(
            (self._x == other[0])
            and
            (self._y == other[1])
            )

    def __repr__(self) -> str:
        return f'<({self._x}, {self._y}) bound to {self._proxy}>'

    def to(self, point: 'rai.typing.PointLike') -> 'rai.typing.Proxy':
        self._proxy.transform.move(
            point[0] - self._x,
            point[1] - self._y,
            )
        return self._proxy

    def rotate(self, angle: float) -> 'rai.typing.Proxy':
        self._proxy.transform.rotate(
            angle,
            self._x,
            self._y
            )
        return self._proxy

    def move(self, x: float, y: float) -> 'rai.typing.Proxy':
        """
        `move`ing a boundpoint is functionally identical to `move`ing
        the proxy itself, so there is no reason to call this explicitly.
        However, this function is still defined, so that you can use
        `move` in a chain of actions on a boundpoint
        """
        self._proxy.transform.move(x, y)
        return self._proxy

    def flip(self) -> 'rai.typing.Proxy':
        """
        TODO add tests
        """
        self._proxy.transform.flip(self._x, self._y)
        return self._proxy

    def hflip(self) -> 'rai.typing.Proxy':
        """
        TODO add tests
        """
        self._proxy.transform.flip(self._x)
        return self._proxy

    def vflip(self) -> 'rai.typing.Proxy':
        """
        TODO add tests
        """
        self._proxy.transform.flip(self._y)
        return self._proxy

    # TODO the rest of the functions

