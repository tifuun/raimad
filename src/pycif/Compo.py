import pycif as pc

class MarksContainer(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._proxy = None

    def __setattr__(self, name, value):

        if name.startswith('_'):
            super().__setattr__(name, value)
            return

        if hasattr(self.__class__, name):
            raise Exception  # TODO actual exception
        else:
            self[name] = value

    def __getattr__(self, name):

        if self._proxy is None:
            return self[name]

        return self._proxy.get_mark(name)

    def _proxy_copy(self, proxy):
        new = type(self)({
            key: val for key, val in self.items()
            })
        new._proxy = proxy
        return new

class Compo:
    def __init__(self, *args, **kwargs):
        self.geoms = {}
        self.subcompos = []
        self.marks = MarksContainer()

        self._make(*args, **kwargs)

    def get_geoms(self) -> dict:
        geoms = self.geoms.copy()
        for subcompo in self.subcompos:
            # TODO override "update" method in geoms container?
            for layer_name, layer_geoms in subcompo.get_geoms().items():
                if layer_name not in geoms.keys():
                    geoms[layer_name] = []
                geoms[layer_name].extend(layer_geoms)
        return geoms

    def final(self):
        return self

    def depth(self):
        return 0

    def walk_hier(self):
        yield self
        for subcompo in self.subcompos:
            yield from subcompo.walk_hier()

    # Transform functions #
    # TODO for all transforms
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

    def rotate(self, angle):
        return pc.Proxy(
            self,
            transform=pc.Transform().rotate(angle)
            )

    # lmap function #
    def __matmul__(self, lmap):
        return pc.Proxy(
            self,
            lmap=lmap
            )

    # mark functions #
    def set_mark(self, name, point):
        self.marks[name] = pc.Mark(self, point)

    def get_mark(self, name):
        return self.marks[name]

    # bbox functions #
    @property
    def bbox(self):
        bbox = pc.BBox()
        for geoms in self.get_geoms().values():
            for geom in geoms:
                bbox.add_xyarray(geom)
        return bbox


