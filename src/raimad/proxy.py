"""proxy.py: home to Proxy class and supporting classes."""

from typing import Iterator, Any

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

from copy import copy

import raimad as rai

class LMap:
    def __init__(self, shorthand: 'rai.typing.LMapShorthand') -> None:
        self.shorthand = shorthand

    def __getitem__(self, name: str) -> str:
        if self.shorthand is None:
            return name

        if isinstance(self.shorthand, str):
            return self.shorthand

        if isinstance(self.shorthand, dict):
            return self.shorthand[name]

        assert False
    # TODO hacky

    def copy(self) -> Self:
        return type(self)(self.shorthand)

    def compose(self, other: Self) -> Self:
        if other.shorthand is None:
            # None lmap, pass everything through
            pass

        elif isinstance(other.shorthand, str):
            # single-string lmap, flatten everything to one layer
            self.shorthand = other.shorthand

        elif isinstance(other.shorthand, dict):
            # TODO better way to do this?
            if isinstance(self.shorthand, dict):
                for self_k, self_val in tuple(self.shorthand.items()):
                    try:
                        self.shorthand[self_k] = other[self_val]
                    except KeyError:
                        pass

            elif self.shorthand is None:
                self.shorthand = copy(other.shorthand)

            elif isinstance(self.shorthand, str):
                self.shorthand = other[self.shorthand]

        else:
            assert False

        return self

class ProxiedMarksContainer(
        rai.FilteredDictList[
            'rai.typing.Point',
            'rai.typing.PointLike',
            'rai.typing.BoundPoint',
            ]):

    def __init__(
            self,
            proxy: 'rai.typing.Proxy',
            dict_: dict[int | str, 'rai.typing.Point'] | None = None,
            *,
            copy: bool | None = None
            ):
        super().__init__(dict_, copy=copy)
        self._proxy = proxy

    def _filter_set(self, val: 'rai.typing.PointLike') -> 'rai.typing.Point':
        """
        set filter for markscontainer:
        make sure that no matter what creature gets passed in
        (regular tuple or boundpoint or whatever),
        what gets stored is a simple regular tuple.
        """
        return (val[0], val[1])

    def _filter_get(self, val: 'rai.typing.Point') -> 'rai.typing.BoundPoint':

        assert not isinstance(val, rai.BoundPoint)
        assert isinstance(val, tuple)
        assert type(val) is tuple
        assert len(val) == 2

        point = self._proxy.transform_point(val)
        boundpoint = rai.BoundPoint(
            point[0],
            point[1],
            self._proxy
            )
        return boundpoint


class Proxy:
    compo: 'rai.typing.CompoLike'

    def __init__(self,
                 compo: 'rai.typing.CompoLike',
                 lmap: 'rai.typing.LMapShorthand' = None,
                 transform: 'rai.typing.Transform | None' = None,
                 _cif_link: bool = False,
                 _autogen: bool = False,
                 ):
        self._cif_linked = False
        self._cif_link = _cif_link
        self._autogen = _autogen
        self.compo = compo
        self.lmap = LMap(lmap)
        self.transform = transform or rai.Transform()

    def steamroll(self) -> 'rai.typing.Geoms':
        return {
            self.lmap[layer]: [
                self.transform.transform_xyarray(geom)
                for geom in geoms
                ]
            for layer, geoms
            in self.compo.steamroll().items()
            }

    def get_flat_transform(self, maxdepth: int = -1) -> 'rai.typing.Transform':
        if maxdepth == 0 or isinstance(self.compo, rai.Compo):
            return self.transform.copy()

        # return (
        #     self.compo.get_flat_transform(maxdepth - 1)
        #     .compose(self.transform)
        #     )

        # TODO huh? copy?
        return self.transform.copy().compose(
            self.compo.get_flat_transform(maxdepth - 1)
            )

    def get_flat_lmap(self, maxdepth: int = -1) -> LMap:
        if maxdepth == 0 or isinstance(self.compo, rai.Compo):
            return self.lmap.copy()

        return self.lmap.copy().compose(
            self.compo.get_flat_lmap(maxdepth - 1)
            )

    @property
    def geoms(self) -> 'rai.typing.Geoms':
        return {
            self.lmap[layer]: [
                self.transform.transform_xyarray(geom)
                for geom in geoms
                ]
            for layer, geoms
            in self.compo.geoms.items()
            }

    @property
    def subcompos(self) -> rai.SubcompoContainer:
        return self.compo.subcompos._get_proxy_view(self)

    def final(self) -> 'rai.typing.Compo':
        return self.compo.final()

    def depth(self) -> int:
        return self.compo.depth() + 1

    def descend(self) -> 'Iterator[rai.typing.CompoLike]':
        yield self
        yield from self.compo.descend()

    def descend_p(self) -> 'Iterator[rai.typing.Proxy]':
        yield self
        yield from self.compo.descend_p()

    def proxy(self) -> 'rai.typing.Proxy':
        return rai.Proxy(self)

    def walk_hier(self) -> 'Iterator[rai.typing.Proxy]':
        for subcompo in self.compo.walk_hier():
            yield self.copy_reassign(subcompo)

    def copy(self) -> 'rai.typing.Proxy':
        if self.depth() > 1:
            # TODO think about why someone would want to do this
            raise Exception("Copying proxy of depth more than 1")

        return type(self)(
            self.compo,
            self.lmap.shorthand,
            self.transform.copy(),
            )

    def copy_reassign(
            self,
            new_subcompo: 'rai.typing.CompoLike',
            _autogen: bool = False,
            ) -> 'rai.typing.Proxy':

        return type(self)(
            new_subcompo,
            self.lmap.shorthand,
            self.transform.copy(),
            _autogen=_autogen,
            )

    def deepcopy(self) -> Any:
        """
        No clue what this is supposed to do
        """
        return NotImplemented

    def transform_point(
            self,
            point: 'rai.typing.PointLike'
            ) -> 'rai.typing.PointLike':

        return self.transform.transform_point(
            self.compo.transform_point(point)
            )

    def __str__(self) -> str:
        stack = ''.join([
            'ma'[proxy._autogen]
            for proxy in self.descend_p()
            ])
        return (
            "<"
            f"Proxy of {self.final()} at {rai.wingdingify(id(self))} "
            f"stack `{stack}x`"
            ">"
            )

    def __repr__(self) -> str:
        return self.__str__()

    # Transform functions #
    # TODO for all transforms
    # TODO same implementation as in Compo
    # TODO stack another transform or modify self?
    def scale(self, factor: float) -> Self:
        self.transform.scale(factor)
        return self

    def movex(self, factor: float) -> Self:
        self.transform.movex(factor)
        return self

    def movey(self, factor: float) -> Self:
        self.transform.movey(factor)
        return self

    def move(self, x: float, y: float) -> Self:
        self.transform.move(x, y)
        return self

    def hflip(self, x: float = 0) -> Self:
        self.transform.hflip(x)
        return self

    def vflip(self, y: float = 0) -> Self:
        self.transform.vflip(y)
        return self

    def flip(self, x: float = 0, y: float = 0) -> Self:
        self.transform.flip(x, y)
        return self

    def rotate(self, angle: float, x: float = 0, y: float = 0) -> Self:
        self.transform.rotate(angle, x, y)
        return self

    def map(self, lmap_shorthand: 'rai.typing.LMapShorthand') -> Self:
        self.lmap = LMap(lmap_shorthand)
        return self

    @property
    def marks(self) -> ProxiedMarksContainer:
        return ProxiedMarksContainer(
            self,
            self.compo.marks._dict,
            copy=False
            )

    # bbox functions #
    # TODO same as compo -- some sort of reuse?
    @property
    def bbox(self) -> 'rai.BoundBBox':
        bbox = rai.BoundBBox(proxy=self)
        for geoms in self.steamroll().values():
            for geom in geoms:
                bbox.add_xyarray(geom)
        return bbox

    # snapping functions #
    def snap_left(self, other: Self) -> Self:
        """
        Move this proxy so its bbox is to the left of the target proxy.

         ________
        |        |
        |        |________
        |        |        |
        |  self  | target |
        |        |________|
        |        |
        |________|

        Parameters
        ----------
        The target proxy

        Returns
        -------
        Self
            This proxy is returned to allow method chaining.
        """
        self.bbox.mid_right.to(other.bbox.mid_left)
        return self

    def snap_right(self, other: Self) -> Self:
        """
        Move this proxy so its bbox is to the right of the target proxy.

                  ________
                 |        |
         ________|        |
        |        |        |
        | target |  self  |
        |________|        |
                 |        |
                 |________|

        Parameters
        ----------
        The target proxy

        Returns
        -------
        Self
            This proxy is returned to allow method chaining.
        """
        self.bbox.mid_left.to(other.bbox.mid_right)
        return self

    def snap_above(self, other: Self) -> Self:
        """
        Move this proxy so its bbox is directly above the target proxy.

         ________________ 
        |                |
        |      self      |
        |________________|
            |        |
            | target |
            |________|

        Parameters
        ----------
        The target proxy

        Returns
        -------
        Self
            This proxy is returned to allow method chaining.
        """
        self.bbox.bot_mid.to(other.bbox.top_mid)
        return self

    # TODO other should be CompoLike not Proxy, Right??
    def snap_below(self, other: Self) -> Self:
        """
        Move this proxy so its bbox is directly below the target proxy.

             ________ 
            |        |
            | target |
         ___|________|___ 
        |                |
        |      self      |
        |________________|

        Parameters
        ----------
        The target proxy

        Returns
        -------
        Self
            This proxy is returned to allow method chaining.
        """
        self.bbox.top_mid.to(other.bbox.bot_mid)
        return self

    def _repr_svg_(self) -> str:
        """
        Make svg representation of component.

        This is not an official magic method specified by Python,
        but rather a convention used by Jupyter Notebook
        and related tools.
        We also use it in RAIMARK.
        """
        return rai.export_svg(self)

