from typing import Self, Iterator, Any
from copy import copy

import pycif as pc

class LMap:
    def __init__(self, shorthand: 'pc.typing.LMapShorthand') -> None:
        self.shorthand = shorthand

    def __getitem__(self, name: str) -> str:
        if self.shorthand is None:
            return name

        if isinstance(self.shorthand, str):
            return self.shorthand

        return self.shorthand[name]
    # TODO hacky

class Proxy:
    def __init__(self,
                 compo: 'pc.typing.Compo',
                 lmap: 'pc.typing.LMap' = None,
                 transform: 'pc.typing.Transform' = None,
                 _cif_link: bool = False,
                 _autogen: bool = False,
                 ):
        self._cif_linked = False
        self._cif_link = _cif_link
        self._autogen = _autogen
        self.compo = compo
        self.lmap = LMap(lmap)
        self.transform = transform or pc.Transform()

    def steamroll(self) -> 'pc.typing.Geoms':
        return {
            self.lmap[layer]: [
                self.transform.transform_xyarray(geom)
                for geom in geoms
                ]
            for layer, geoms
            in self.compo.steamroll().items()
            }

    def get_flat_transform(self, maxdepth: int = -1) -> 'pc.typing.Transform':
        if maxdepth == 0:
            return pc.Transform()

        #return (
        #    self.compo.get_flat_transform(maxdepth - 1)
        #    .compose(self.transform)
        #    )

        return self.transform.copy().compose(
            self.compo.get_flat_transform(maxdepth - 1)
            )

    @property
    def geoms(self) -> 'pc.typing.Geoms':
        return {
            self.lmap[layer]: [
                self.transform.transform_xyarray(geom)
                for geom in geoms
                ]
            for layer, geoms
            in self.compo.geoms.items()
            }

    @property
    def subcompos(self) -> pc.DictList:
        return pc.DictList({
            name: self.copy_reassign(subcompo, _autogen=True)
            for name, subcompo in self.compo.subcompos.items()
            })
        return self.compo.subcompos

    def final(self) -> 'pc.typing.RealCompo':
        return self.compo.final()

    def depth(self) -> int:
        return self.compo.depth() + 1

    def descend(self) -> 'Iterator[pc.typing.Compo]':
        yield self
        yield from self.compo.descendre()

    def descend_p(self) -> 'Iterator[pc.typing.Proxy]':
        yield self
        yield from self.compo.descend_p()

    def proxy(self) -> 'pc.typing.Proxy':
        return pc.Proxy(self)

    def walk_hier(self) -> 'Iterator[pc.typing.Proxy]':
        for subcompo in self.compo.walk_hier():
            yield self.copy_reassign(subcompo)

    def copy(self) -> 'pc.typing.Proxy':
        if self.depth() > 1:
            # TODO think about why someone would want to do this
            raise Exception("Copying proxy of depth more than 1")

        return type(self)(
            self.compo,
            copy(self.lmap),
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
            new_subcompo: 'pc.typing.Compo',
            _autogen: bool = False,
            ) -> 'pc.typing.Proxy':

        return type(self)(
            new_subcompo,
            copy(self.lmap),
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
        #        if isinstance(self.compo, pc.Compo)
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
            f"Proxy of {self.final()} at {pc.wingdingify(id(self))} "
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
    #    #return pc.Proxy(
    #    #    self,
    #    #    lmap=lmap
    #    #    )
    def map(self, lmap):
        self.lmap = LMap(lmap)
        return self

    # mark functions #
    def get_mark(self, name: str) -> pc.BoundPoint:
        return pc.BoundPoint(
            self.transform.transform_point(
                self.compo.get_mark(name)
                ),
            self
            )

    @property
    def marks(self):
        return self.compo.marks._proxy_copy(self)

    # bbox functions #
    # TODO same as compo -- some sort of reuse?
    @property
    def bbox(self):
        bbox = pc.BBox(proxy=self)
        for geoms in self.steamroll().values():
            for geom in geoms:
                bbox.add_xyarray(geom)
        return bbox

    # snapping functions #
    def snap_left(self, other):
        self.bbox.mid_right.to(other.bbox.mid_left)
        return self

    def snap_right(self, other):
        self.bbox.mid_left.to(other.bbox.mid_right)
        return self

    def snap_above(self, other):
        self.bbox.bot_mid.to(other.bbox.top_mid)
        return self

    def snap_below(self, other):
        self.bbox.top_mid.to(other.bbox.bot_mid)
        return self

    def _repr_svg_(self):
        """
        Make svg representation of component.
        This is called by jupyter and raimark
        """
        return pc.export_svg(self)

    #def _export_cif(self, transform=None):
    #    return self.compo._export_cif(
    #        self.transform.copy().compose(transform)
    #        if transform is not None else self.transform
    #        )



