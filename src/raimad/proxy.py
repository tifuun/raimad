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

class Proxy:
    compo: 'rai.typing.Compo'

    def __init__(self,
                 compo: 'rai.typing.Compo',
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

        #return (
        #    self.compo.get_flat_transform(maxdepth - 1)
        #    .compose(self.transform)
        #    )

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
        # TODO FrozenSubcompoContainer?
        return rai.SubcompoContainer({
            name: self.copy_reassign(subcompo, _autogen=True)
            for name, subcompo in self.compo.subcompos.items()
            })
        return self.compo.subcompos

    def final(self) -> 'rai.typing.RealCompo':
        return self.compo.final()

    def depth(self) -> int:
        return self.compo.depth() + 1

    def descend(self) -> 'Iterator[rai.typing.Compo]':
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

    #def cifcopy(self):
    #    if self.depth() > 1:
    #        # TODO think about why someone would want to do this
    #        raise Exception("Copying proxy of depth more than 1")

    #    self._cif_linked = True

    #    return type(self)(
    #        self.compo,
    #        copy(self.lmap),
    #        self.transform.copy(),
    #        _cif_link=True
    #        )

    def copy_reassign(
            self,
            new_subcompo: 'rai.typing.Compo',
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
        #return type(self)(
        #    (
        #        self.compo
        #        if isinstance(self.compo, rai.Compo)
        #        else self.compo.copy()
        #        ),
        #    copy(self.lmap),
        #    self.transform.copy(),
        #    )

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

    ## lmap function #
    #def __matmul__(self, lmap):
    #    # TODO warn on override lmap?
    #    self.lmap = LMap(lmap)
    #    return self
    #    #return rai.Proxy(
    #    #    self,
    #    #    lmap=lmap
    #    #    )
    def map(self, lmap_shorthand: 'rai.typing.LMapShorthand') -> Self:
        self.lmap = LMap(lmap_shorthand)
        return self

    # mark functions #
    def get_mark(self, name: str) -> rai.BoundPoint:
        return rai.BoundPoint(
            self.transform.transform_point(
                self.compo.get_mark(name)
                ),
            self
            )

    @property
    def marks(self) -> rai.MarksContainer:
        return self.compo.marks._proxy_copy(self)

    # bbox functions #
    # TODO same as compo -- some sort of reuse?
    @property
    def bbox(self) -> 'rai.typing.BBox':
        bbox = rai.BBox(proxy=self)
        for geoms in self.steamroll().values():
            for geom in geoms:
                bbox.add_xyarray(geom)
        return bbox

    # snapping functions #
    def snap_left(self, other: Self) -> Self:
        self.bbox.mid_right.to(other.bbox.mid_left)
        return self

    def snap_right(self, other: Self) -> Self:
        self.bbox.mid_left.to(other.bbox.mid_right)
        return self

    def snap_above(self, other: Self) -> Self:
        self.bbox.bot_mid.to(other.bbox.top_mid)
        return self

    def snap_below(self, other: Self) -> Self:
        self.bbox.top_mid.to(other.bbox.bot_mid)
        return self

    def _repr_svg_(self) -> str:
        """
        Make svg representation of component.
        This is called by jupyter and raimark
        """
        return rai.export_svg(self)

