import inspect

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

from copy import deepcopy

import raimad as rai

class MarksContainer(rai.DictList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._proxy = None

    def __getattr__(self, name):

        if self._proxy is None:
            return self[name]

        return self._proxy.get_mark(name)

    def _proxy_copy(self, proxy: 'rai.typing.Proxy') -> Self:
        new = type(self)({
            key: val for key, val in self.items()
            })
        new._proxy = proxy
        return new

class SubcompoContainer(rai.DictList):
    def _filter(self, item):
        if isinstance(item, rai.Compo):
            return rai.Proxy(item, _autogen=True)
        elif isinstance(item, rai.Proxy):
            return item
        else:
            raise Exception  # TODO actual exception
        # TODO generally need to standardize runtime checks.

class Compo:
    marks: MarksContainer
    subcompos: SubcompoContainer

    def __init__(self, *args, **kwargs):
        self.geoms = {}
        self.subcompos = SubcompoContainer()
        self.marks = MarksContainer()

        self._make(*args, **kwargs)

    @classmethod
    def partial(cls, **kwargs):
        return rai.Partial(cls, **kwargs)

    def steamroll(self) -> dict:
        """
        Steamroll the entire compo hierarchy into one Geoms dict
        TODO more informative
        """
        geoms = self.geoms.copy()
        for subcompo in self.subcompos.values():
            # TODO override "update" method in geoms container?
            for layer_name, layer_geoms in subcompo.steamroll().items():
                if layer_name not in geoms.keys():
                    geoms[layer_name] = []
                geoms[layer_name].extend(layer_geoms)
        return geoms

    def final(self):
        return self

    def depth(self):
        return 0

    def descend(self):
        yield self

    def descend_p(self):
        return
        yield

    def proxy(self):
        return rai.Proxy(self)

    def copy(*args, **kwargs):
        """
        Don't copy components, copy proxies
        """
        return NotImplemented

    def walk_hier(self):
        yield self
        for subcompo in self.subcompos.values():
            yield from subcompo.walk_hier()

    # Transform functions #
    # TODO for all transforms
    #def scale(self, factor):
    #    return rai.Proxy(
    #        self,
    #        transform=rai.Transform().scale(factor)
    #        )

    #def movex(self, factor):
    #    return rai.Proxy(
    #        self,
    #        transform=rai.Transform().movex(factor)
    #        )

    #def movey(self, factor):
    #    return rai.Proxy(
    #        self,
    #        transform=rai.Transform().movey(factor)
    #        )

    #def rotate(self, angle):
    #    return rai.Proxy(
    #        self,
    #        transform=rai.Transform().rotate(angle)
    #        )

    # lmap function #
    #def __matmul__(self, what):
    #    if isinstance(what, dict | str):  # TODO lmap shorthand type
    #        return rai.Proxy(
    #            self,
    #            lmap=what
    #            )
    #    elif isinstance(what, rai.Transform):
    #        return rai.Proxy(
    #            self,
    #            transform=what
    #            )
    #    else:
    #        raise Exception()  # TODO

    # mark functions #
    def set_mark(self, name, point):
        # TODO this is a boundpoint but not actually a boundpoint?
        self.marks[name] = rai.BoundPoint(point, None)

    def get_mark(self, name):
        return self.marks[name]

    # bbox functions #
    @property
    def bbox(self):
        bbox = rai.BBox()
        for geoms in self.steamroll().values():
            for geom in geoms:
                bbox.add_xyarray(geom)
        return bbox

    def __init_subclass__(cls):
        _class_to_dictlist(cls, 'Marks', rai.Mark)
        _class_to_dictlist(cls, 'Layers', rai.Layer)
        _class_to_dictlist(cls, 'Options', rai.Option)

        for param in inspect.signature(cls._make).parameters.values():
            if param.name not in cls.Options.keys():
                # TODO unannotated
                continue

            cls.Options[param.name].annot = rai.Empty
            cls.Options[param.name].default = rai.Empty

            if param.default is not inspect._empty:
                cls.Options[param.name].default = param.default

            if param.annotation is inspect._empty:
                if param.default is not inspect._empty:
                    cls.Options[param.name].annot = type(param.default)
            else:
                cls.Options[param.name].annot = param.annotation

    # Condemned method, I don't like it
    #def subcompo(self, compo, name: str | None = None):
    #    proxy = rai.Proxy(compo)
    #    if name is None:
    #        self.subcompos.append(proxy)
    #    else:
    #        # TODO runtime check for subcompo reassignment?
    #        self.subcompos[name] = proxy
    #    return proxy

    def auto_subcompos(self, locs=None):
        """
        Automatically add all proxies defined in whatever function you
        call this from as subcompos using some arcane stack inspection
        hackery.
        """
        # Get all local variables in the above frame
        locs = locs or inspect.stack()[1].frame.f_locals

        for name, obj in locs.items():
            if (
                    isinstance(obj, rai.Proxy)
                    and name != 'self'
                    and not name.startswith('_')
                    ):
                # TODO forbid adding compo directly as subcompo,
                # only proxy, instead of doing it automatically.
                self.subcompos[name] = obj

    def __str__(self):
        return (
            "<"
            f"{type(self).__name__} at {rai.wingdingify(id(self))} "
            ">"
            )

    def __repr__(self):
        return self.__str__()

    def _repr_svg_(self):
        """
        Make svg representation of component.
        This is called by jupyter and raimark
        """
        return rai.export_svg(self)

def _class_to_dictlist(cls, attr, wanted_type):
    if not hasattr(cls, attr):
        setattr(cls, attr, rai.DictList())
        return

    new_list = rai.DictList()
    for name, annot in getattr(cls, attr).__dict__.items():
        if not isinstance(annot, wanted_type):
            continue
        annot.name = name
        new_list[name] = annot

    setattr(cls, attr, new_list)

