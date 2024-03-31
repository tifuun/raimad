import inspect

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

class SubcompoContainer(pc.DictList):
    def _filter(self, item):
        if isinstance(item, pc.Compo):
            return pc.Proxy(item)
        elif isinstance(item, pc.Proxy):
            return item
        else:
            raise Exception  # TODO actual exception

class Compo:
    def __init__(self, *args, **kwargs):
        self.geoms = {}
        self.subcompos = SubcompoContainer()
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

    def __init_subclass__(cls):
        _class_to_dictlist(cls, 'Marks', pc.MarkAnnot)
        _class_to_dictlist(cls, 'Layers', pc.LayerAnnot)
        _class_to_dictlist(cls, 'Options', pc.OptionAnnot)

        for param in inspect.signature(cls._make).parameters.values():
            if param.name not in cls.Options.keys():
                # TODO unannotated
                continue

            cls.Options[param.name].default = param.default

            if (
                    param.annotation is inspect._empty
                    and param.default is not inspect._empty
                    ):
                cls.Options[param.name].annot = type(param.default)
            else:

                cls.Options[param.name].annot = param.annotation

    # TODO pass lmap and transform directly?
    # TODO name?
    def subcompo(self, compo, name: str | None = None):
        proxy = pc.Proxy(compo)
        if name is None:
            self.subcompos.append(proxy)
        else:
            # TODO runtime check for subcompo reassignment?
            self.subcompos[name] = proxy
        return proxy


def _class_to_dictlist(cls, attr, wanted_type):
    if not hasattr(cls, attr):
        setattr(cls, attr, pc.DictList())
        return

    new_list = pc.DictList()
    for name, annot in getattr(cls, attr).__dict__.items():
        if not isinstance(annot, wanted_type):
            continue
        annot.name = name
        new_list[name] = annot

    setattr(cls, attr, new_list)

