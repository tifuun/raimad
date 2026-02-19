"""boundpoint.py: home to BoundPoint class."""

from typing import Literal, Iterator, overload, Sequence
from types import NoneType

import raimad as rai

class BoundPoint():
    """
    A point bound to a Proxy.

    There is often a desire to perform a certain transformation
    of some proxy in reference to a given point at that proxy.
    We might want to rotate a proxy around the top left corner
    of its bbox,
    or move a proxy such that one of its marks is at a given point.

    These things can be done with the following syntax in raimad:
    - `someproxy.bbox.top_left.rotate(someangle)`
    - `someproxy.marks.important_mark.to((x, y))`

    In the examples above, `top_left` and `important_mark` are both
    BoundPoints.
    They behave just like regular points (a tuple of x and y),
    but they also define transformation methods like
    `rotate`, `to`, `vflip`, and so forth
    that perform the corresponding transformation
    to the bound proxy, with the BoundPoint treated as the new origin
    for the transformation.
    """

    def __init__(self, x: float, y: float, proxy: 'rai.typing.Proxy'):
        """
        Initialize new boundpoint.

        Note that in normal RAIMAD usage,
        you should not have to create boundpoints
        manually.

        Parameters
        ----------
        x
            The x coordinate of the point
        y
            The y coordinate of the point
        proxy
            The proxy this to bind to
        """
        self._x = x
        self._y = y
        self._proxy = proxy

    def __getitem__(self, index: Literal[0, 1]) -> float:
        """
        Get the X or Y coordinate of this BoundPoint.

        Parameters
        ----------
        index: int
            0 or 1 for the x and y coordinate respectively

        Returns
        -------
        float
            The coordinate value

        Raises
        ------
        IndexError
            IndexError is raised if `index` is anything other than 0 or 1.

        Example
        -------
        somepoint[0]  # X coordinate
        somepoint[1]  # Y coordinate
        """
        if index == 0:
            return self._x

        elif index == 1:
            return self._y

        # The esxception type HAS TO BE IndexError
        # if we want Python to allow unpacking BoundPoints
        # using the asterisk syntax
        raise IndexError(
            "BoundPoint has only x and y coordinates, "
            "so the index must be either 0 or 1"
            )

    def __iter__(self) -> Iterator[float]:
        """
        Return an iterator of the x and y coordinates of this BoundPoint.

        Returns
        -------
        Iterator[float]
            Iterator containing x and y coordinate.

        """
        return iter((self._x, self._y))

    def __eq__(self, other: object) -> bool:
        """
        Check for equality of BoundPoint.

        Comparing BoundPoints using the == operator
        (i.e. this method) may be a bad idea for the same reason
        that comparing floats in this way is a bad idea.

        Parameters
        ----------
        other: object
            The object to check equality against.
            This may be another BoundPoint, a regular Point,
            or any other object.
            If `other` does not implement a `__getitem__` method,
            then the result is automatically zero.
            If `other` does implement `__getitem__`,
            then the result is True iff
            the x coordinate of this boundpoint == other[0] and
            the y coordinate of this boundpoint == other[1].

        Returns
        -------
        bool
            True if this boundpoint is equal to `other`,
            False otherwise.

        """
        if not hasattr(other, "__getitem__"):
            return False

        return bool(
            (self._x == other[0])
            and
            (self._y == other[1])
            )

    def __repr__(self) -> str:
        """
        Return string representation of this BoundPoint.

        Returns
        -------
        str
            TODO sample string
        """
        return str(self)

    def __str__(self) -> str:
        """
        Return string representation of this BoundPoint.

        Returns
        -------
        str
            TODO sample string
        """
        #FIXME brackets?
        return ''.join((
            f'<({self._x}, {self._y}) bound to <\n',
            self._proxy._str(1),
            '>'
            ))

    #-------------#
    # Rotate      #
    #-------------#

    def rotate(self, angle: float) -> 'rai.typing.Proxy':
        """
        Rotate the bound Proxy around this BoundPoint.

        Parameters
        ----------
        angle: float
            The rotation angle, specified in radians in the positive
            direction.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.crotate(
            angle,
            self._x,
            self._y
            )
        return self._proxy


    #-------------#
    # Move        #
    #-------------#

    def cmove(
            self,
            x: float = 0,
            y: float = 0
            ) -> 'rai.typing.Proxy':
        """
        Translate by x and y.

        Parameters
        ----------
        x : float
            Move this many units along x axis.
        y : float
            Move this many units along y axis.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.cmove(x, y)
        return self._proxy

    def pmove(
            self,
            offset: 'rai.typing.Point'
            ) -> None:
        """
        Translate by x and y, given as a tuple.

        Parameters
        ----------
        offset : 'rai.typing.Point'
            A tuple of two values (x, y).

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.pmove(offset)
        return self._proxy

    @overload
    def move(self, x: float, y: float) -> None: ...
    @overload
    def move(self, offset: 'rai.typing.Point') -> None: ...

    def move(
            self,
            a: 'float | rai.typing.Point',
            b: float | None = None
            ) -> None:
        """
        TODO overloaded docstrings??
        """
        self._proxy.transform.move(a, b)
        return self._proxy

    def movex(self, x: float = 0) -> 'rai.typing.Proxy':
        """
        Move along x axis.

        Parameters
        ----------
        x : float
            Move this many units along x axis.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.movex(x)
        return self._proxy

    def movey(self, y: float = 0) -> 'rai.typing.Proxy':
        """
        Move along y axis.

        Parameters
        ----------
        y : float
            Move this many units along y axis.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.movey(y)
        return self._proxy

    #-------------#
    # Flip        #
    #-------------#

    def flip(
            self,
            ) -> None:
        #TODO add tests
        """
        Flip the bound proxy around this boundpoint.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.flip(self._x, self._y)
        return self._proxy

    def hflip(self) -> 'rai.typing.Proxy':
        """
        Flip proxy along horizontal axis passing thru this boundpoint.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        #TODO add tests
        self._proxy.transform.hflip(self._x)
        return self._proxy

    def vflip(self) -> 'rai.typing.Proxy':
        """
        Flip the bound proxy along vertical axis passing thru this boundpoint.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        #TODO add tests
        self._proxy.transform.vflip(self._y)
        return self._proxy

    #-------------#
    # Scale       #
    #-------------#

    def cscale(
            self,
            x: float,
            y: float,
            ) -> 'rai.typing.Proxy':
        """
        Scale width and height (two floats) with this boundpoint as pivot

        Parameters
        ----------
        x : float
            Factor to scale by along the x axis
        y : float
            Factor to scale by along the y axis.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.ccscale(x, y, self._x, self._y)
        return self._proxy

    def pscale(
            self,
            scale: 'rai.typing.Point',
            ) -> 'rai.typing.Proxy':
        """
        Scale width and height (tuple) with this boundpoint as pivot

        Parameters
        ----------
        scale : 'rai.typing.Point'
            The x and y scale factors

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.ccscale(scale[0], scale[1], self._x, self._y)
        return self._proxy

    def ascale(
            self,
            factor: float,
            ) -> 'rai.typing.Proxy':
        """
        Scale width and height by same factor with this boundpoint as pivot

        Parameters
        ----------
        factor : float
            Factor to scale by.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.acscale(factor, self._x, self._y)
        return self._proxy

    # TODO
    @overload
    def scale(self, x: float, y: float) -> None: ...
    @overload
    def scale(self, scale: 'rai.typing.Point') -> None: ...
    @overload
    def scale(self, factor: float) -> None: ...

    def scale(
            self, /, a=None, b=None
            ) -> None:
        """
        TODO overloaded docstrings??
        """
        if (
                isinstance(a, float | int) and
                isinstance(b, float | int)
                ):
            self._proxy.transform.ccscale(a, b, self._x, self._y)
        elif (
                isinstance(a, Sequence) and
                isinstance(b, NoneType)
                ):
            self._proxy.transform.pcscale(a, self._x, self._y)
        elif (
                isinstance(a, float | int) and
                isinstance(b, NoneType)
                ):
            self._proxy.transform.acscale(a, self._x, self._y)
        else:
            #TODO
            raise TypeError('foobar')

        return self._proxy

    #-------------#
    # To          #
    #-------------#

    def pto(self, point: 'rai.typing.PointLike') -> 'rai.typing.Proxy':
        """
        Move the Proxy such that this BoundPoint ends up at `point` (tuple).

        Parameters
        ----------
        point: rai.typing.PointLike
            Target point.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.move(
            point[0] - self._x,
            point[1] - self._y,
            )
        return self._proxy

    def cto(self, x: float, y: float) -> 'rai.typing.Proxy':
        """
        Move the Proxy so that this BoundPoint ends up at `point` (two floats).

        Parameters
        ----------
        x : float
            Move this many units along x axis.
        y : float
            Move this many units along y axis.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        self._proxy.transform.move(
            x - self._x,
            y - self._y,
            )
        return self._proxy

    # TODO overload
    def to(self, a=None, b=None) -> 'rai.typing.Proxy':
        """
        Move the Proxy so that this BoundPoint ends up at `point` (two floats).

        Parameters
        ----------
        x : float
            Move this many units along x axis.
        y : float
            Move this many units along y axis.

        Returns
        -------
        rai.typing.Proxy
            The bound proxy (not this BoundPoint!) is returned
            to allow chaining methods.
        """
        if (
                isinstance(a, float | int) and
                isinstance(b, float | int)
                ):
            self.cto(a, b)
        elif (
                isinstance(a, Sequence) and
                isinstance(b, NoneType)
                ):
            self.pto(a)
        else:
            # TODO
            raise TypeError('foobar')

        return self._proxy

