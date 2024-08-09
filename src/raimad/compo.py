import inspect
from typing import Any, NoReturn, Iterator, TypeVar

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

import raimad as rai

class InvalidSubcompoError(TypeError):
    """
    Error for when you try to add
    something weird as a subcompo instead of a proxy
    """

class ProxyCompoConfusionError(TypeError):
    """
    Error for when you try to do something to a compo
    that should be done to a proxy instead
    """

class CompoInsteadOfProxyAsSubcompoError(
        InvalidSubcompoError,
        ProxyCompoConfusionError
        ):
    """
    Special case of InvalidSubcompoError for when you try to add
    a Compo instead of a Proxy as a subcompo
    """

class TransformCompoError(ProxyCompoConfusionError):
    """
    Error for when you try to use transformation function on a compo
    instead of its proxy
    """

class CopyCompoError(ProxyCompoConfusionError):
    """
    Error for when you try to copy a compo
    instead of its proxy
    """


T = TypeVar('T')
class ProxyableDictList(rai.DictList[T]):
    _proxy: 'None | rai.typing.Proxy'

    def _post_init(self) -> None:
        self._proxy = None

    def _get_proxy_view(self, proxy: 'rai.t.Proxy') -> Self:
        new = type(self)(self._dict, copy=False)
        new._proxy = proxy
        return new


class MarksContainer(
        rai.FilteredDictList[
            'rai.typing.Point',
            'rai.typing.PointLike',
            'rai.typing.Point',
            ]):
    def _filter_set(self, val: 'rai.typing.PointLike') -> 'rai.typing.Point':
        """
        set filter for markscontainer:
        make sure that no matter what creature gets passed in
        (regular tuple or boundpoint or whatever),
        what gets stored is a simple regular tuple.
        """
        return (val[0], val[1])

    def _filter_get(self, val: 'rai.typing.Point') -> 'rai.typing.Point':
        return val

class SubcompoContainer(ProxyableDictList['rai.typing.Proxy']):
    def _filter_set(self, item: 'rai.typing.Proxy') -> 'rai.typing.Proxy':
        if isinstance(item, rai.Compo):
            raise CompoInsteadOfProxyAsSubcompoError(
                f"Tried to add object `{item}` of type `{type(item)}` "
                f"as a subcompo of `{self}`. "
                "All subcompos must be of type `raimad.Proxy`."
                "You can call the `.proxy()` method of a `raimad.Compo` "
                "in order to get a proxy that points to it."
                )

        if not isinstance(item, rai.Proxy):
            raise InvalidSubcompoError(
                f"Tried to add object `{item}` of type `{type(item)}` "
                f"as a subcompo of `{self}`. "
                "All subcompos must be of type `raimad.Proxy`."
                )

        return item

    def _filter_get(self, val: 'rai.typing.Proxy') -> 'rai.typing.Proxy':
        if self._proxy is not None:
            return self._proxy.copy_reassign(val, _autogen=True)
        return val

class Compo:
    geoms: 'rai.typing.Geoms'
    marks: MarksContainer
    subcompos: SubcompoContainer

    Marks: rai.DictList[rai.Mark]
    Layers: rai.DictList[rai.Layer]
    Options: rai.DictList[rai.Option]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.geoms = {}
        self.subcompos = SubcompoContainer()
        self.marks = MarksContainer()

        self._make(*args, **kwargs)

    def _make(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()

    @classmethod
    def partial(cls, **kwargs: Any) -> 'rai.typing.Partial':
        return rai.Partial(cls, **kwargs)

    def steamroll(self) -> 'rai.typing.Geoms':
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

    def final(self) -> Self:
        return self

    def depth(self) -> int:
        return 0

    def descend(self) -> Iterator[Self]:
        yield self

    def descend_p(self) -> 'Iterator[rai.typing.Proxy]':
        return
        yield

    def proxy(self) -> 'rai.typing.Proxy':
        return rai.Proxy(self)

    @property
    def copy(self) -> NoReturn:
        raise CopyCompoError(
            f"`{self}` is a Compo, not a Proxy! "
            "Don't copy compos; instead, "
            "create a Proxy using the `.proxy()` method "
            "and copy that instead."
            )

    def walk_hier(self) -> Iterator['rai.typing.CompoLike']:
        yield self
        for subcompo in self.subcompos.values():
            yield from subcompo.walk_hier()

    def transform_point(
            self,
            point: 'rai.typing.PointLike'
            ) -> 'rai.typing.PointLike':
        return point

    @property
    def scale(self) -> NoReturn:
        raise TransformCompoError(
            f"Tried to scale `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def move(self) -> NoReturn:
        raise TransformCompoError(
            f"Tried to move `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def movex(self) -> NoReturn:
        raise TransformCompoError(
            f"Tried to move `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def movey(self) -> NoReturn:
        raise TransformCompoError(
            f"Tried to move `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def rotate(self) -> NoReturn:
        raise TransformCompoError(
            f"Tried to rotate `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def flip(self) -> NoReturn:
        raise TransformCompoError(
            f"Tried to flip `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def hflip(self) -> NoReturn:
        raise TransformCompoError(
            f"Tried to hflip `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def vflip(self) -> NoReturn:
        raise TransformCompoError(
            f"Tried to vflip `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    # bbox functions #
    @property
    def bbox(self) -> 'rai.BBox':
        bbox = rai.BBox()
        for geoms in self.steamroll().values():
            for geom in geoms:
                bbox.add_xyarray(geom)
        return bbox

    def __init_subclass__(cls) -> None:
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

    def auto_subcompos(self, locs: dict[Any, Any] | None = None) -> None:
        """
        """
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

    def __str__(self) -> str:
        return (
            "<"
            f"{type(self).__name__} at {rai.wingdingify(id(self))} "
            ">"
            )

    def __repr__(self) -> str:
        return self.__str__()

    def _repr_svg_(self) -> str:
        """
        Make svg representation of component.
        This is called by jupyter and raimark
        """
        return rai.export_svg(self)


K = TypeVar('K', bound=rai.Annotation)
def _class_to_dictlist(
        cls: type,
        attr: str,
        wanted_type: type[K]
        ) -> None:

    if not hasattr(cls, attr):
        setattr(cls, attr, rai.DictList())
        return

    new_list: rai.DictList[K] = rai.DictList()
    for name, annot in getattr(cls, attr).__dict__.items():
        if not isinstance(annot, wanted_type):
            continue
        annot.name = name
        new_list[name] = annot

    setattr(cls, attr, new_list)

