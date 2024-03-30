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
        return [
            self.proxy_copy(subcompo)
            for subcompo in self.compo.subcompos
            ]
        return self.compo.subcompos

    def final(self):
        return self.compo.final()

    def depth(self):
        return self.compo.depth() + 1

    def walk_hier(self):
        for subcompo in self.compo.walk_hier():
            yield self.proxy_copy(subcompo)

    def proxy_copy(self, new_subcompo=None):
        return type(self)(
            new_subcompo or self.subcompo,
            copy(self.lmap),
            self.transform.copy(),
            )

    def __str__(self):
        return f"<Proxy of {self.compo} at {id(self)}>"

    # Transform functions #
    # TODO for all transforms
    # TODO same implementation as in Compo
    def scale(self, factor):
        return pc.Proxy(
            self,
            transform=pc.Transform().scale(factor)
            )

    def movex(self, factor):
        return pc.Proxy(
            self,
            transform=pc.Transform().movex(factor)
            )

    def movey(self, factor):
        return pc.Proxy(
            self,
            transform=pc.Transform().movey(factor)
            )

    # lmap function #
    def __matmul__(self, lmap):
        return pc.Proxy(
            self,
            lmap=lmap
            )

    # mark functions #
    def get_mark(self, name):
        return self.transform.transform_point(
            self.compo.get_mark(name)
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
    # TODO the rest of the snapping functions



