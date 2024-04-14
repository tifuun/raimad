from copy import copy

import pycif as pc

class LMap:
    def __init__(self, shorthand):
        self.shorthand = shorthand

    def __getitem__(self, name):
        if self.shorthand is None:
            return name

        if isinstance(self.shorthand, str):
            return self.shorthand

        return self.shorthand[name]
    # TODO hacky

class Proxy:
    def __init__(self, compo, lmap=None, transform=None):
        self.compo = compo
        self.lmap = LMap(lmap)
        self.transform = transform or pc.Transform()

    def get_geoms(self):
        return {
            self.lmap[layer]: [
                self.transform.transform_xyarray(geom)
                for geom in geoms
                ]
            for layer, geoms
            in self.compo.get_geoms().items()
            }

    @property
    def geoms(self):
        return {
            self.lmap[layer]: [
                self.transform.transform_xyarray(geom)
                for geom in geoms
                ]
            for layer, geoms
            in self.compo.geoms.items()
            }

    @property
    def subcompos(self):
        return pc.DictList({
            name: self.copy(subcompo)
            for name, subcompo in self.compo.subcompos.items()
            })
        return self.compo.subcompos

    def final(self):
        return self.compo.final()

    def depth(self):
        return self.compo.depth() + 1

    def walk_hier(self):
        for subcompo in self.compo.walk_hier():
            yield self.copy(subcompo)

    def copy(self, new_subcompo=None):
        return type(self)(
            new_subcompo or self.compo,
            copy(self.lmap),
            self.transform.copy(),
            )

    def deepcopy(self):
        return type(self)(
            (
                self.compo
                if isinstance(self.compo, pc.Compo)
                else self.compo.copy()
                ),
            copy(self.lmap),
            self.transform.copy(),
            )

    def __str__(self):
        return f"<Proxy of {self.compo} at {id(self)}>"

    # Transform functions #
    # TODO for all transforms
    # TODO same implementation as in Compo
    # TODO stack another transform or modify self?
    def scale(self, factor):
        self.transform.scale(factor)
        return self

    def movex(self, factor):
        self.transform.movex(factor)
        return self

    def movey(self, factor):
        self.transform.movey(factor)
        return self

    def move(self, x: 0, y: float = 0):
        self.transform.move(x, y)
        return self

    def hflip(self, x: float = 0):
        self.transform.hflip(x)
        return self

    def vflip(self, y: float = 0):
        self.transform.vflip(y)
        return self

    def flip(self, x: float = 0, y: float = 0):
        self.transform.flip(x, y)
        return self

    def rotate(self, angle: float, x: float = 0, y: float = 0):
        self.transform.rotate(angle, x, y)
        return self

    # lmap function #
    def __matmul__(self, lmap):
        return pc.Proxy(
            self,
            lmap=lmap
            )

    # mark functions #
    def get_mark(self, name):
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
        for geoms in self.get_geoms().values():
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



