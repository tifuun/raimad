"""compo.py: home of Compo class and supporting constructs."""
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
    Error for when you try to add something weird as a subcompo.

    Subcompos must be proxies, nothing else.
    """

class ProxyCompoConfusionError(TypeError):
    """(abstract) error for performing operations on compo instead of proxy."""

class CompoInsteadOfProxyAsSubcompoError(
        InvalidSubcompoError,
        ProxyCompoConfusionError
        ):
    """
    Error for when you try to add a Compo instead of a Proxy as a subcompo.

    TODO example
    """

class TransformCompoError(ProxyCompoConfusionError):
    """
    Error for when you try to use transformation function on a compo.

    Compos are supposed to be immutable, you should transform
    a proxy pointing to the compo instead.
    """

class CopyCompoError(ProxyCompoConfusionError):
    """
    Error for when you try to copy a compo instead of its proxy.

    Compos are supposed to be fungible, you should probably
    be copying a proxy pointing to the compo instead.
    """


T = TypeVar('T')
class ProxyableDictList(rai.DictList[T]):
    """TODO document this."""

    _proxy: 'None | rai.typing.Proxy'

    def _post_init(self) -> None:
        self._proxy = None

    def _get_proxy_view(self, proxy: 'rai.t.Proxy') -> Self:
        """TODO document this."""
        assert False
        new = type(self)(self._dict, copy=False)

        #assert not isinstance(proxy.compo, rai.Proxy), str(proxy)


        assert isinstance(proxy, rai.Proxy)
        #assert proxy.depth() == 1
        proxy = proxy.final_p()
        #assert self._proxy is None
        #if isinstance(self._proxy, rai.Proxy):
        #    print(self._proxy.__insane_str__())
        new._proxy = (
            #proxy.deep_copy(_autogen=True) if self._proxy is None else
            proxy if self._proxy is None else
            proxy.shallow_copy_reassign(self._proxy, _autogenned=True)
            )
        # TODO just store lmap and transform
        return new


class MarksContainer(
        rai.FilteredDictList[
            'rai.typing.Point',
            'rai.typing.PointLike',
            'rai.typing.Point',
            ]):
    """
    Specialized container that implements Compo.marks.

    TODO explain.
    """

    def _filter_set(self, val: 'rai.typing.PointLike') -> 'rai.typing.Point':
        """
        Set filter for markscontainer.

        Make sure that no matter what creature gets passed in
        (regular tuple or boundpoint or whatever),
        what gets stored is a simple regular tuple.
        """
        return (val[0], val[1])

    def _filter_get(self, val: 'rai.typing.Point') -> 'rai.typing.Point':
        return val

class SubcompoContainer(ProxyableDictList['rai.typing.Proxy']):
    """
    Specialized container that implements Compo.subcompos.

    TODO explain.
    """

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
            return self._proxy.deep_copy_reassign(val, _autogenned=True)
        return val

class Compo:
    """
    Compos: the building blocks of RAIMAD.

    TODO explain
    """

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
        """
        Return a Partial of this component class.

        Parameters
        ----------
        kwargs: Any
            Options to store in the Partial

        Returns
        -------
        rai.typing.Partial
            The new Partial
        """
        return rai.Partial(cls, **kwargs)

    def steamroll(self) -> 'rai.typing.Geoms':
        """
        Steamroll the entire compo hierarchy into one Geoms dict.

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
        """
        Return self.

        This method exists for uniformity with Proxy.final
        """
        return self

    def depth(self) -> int:
        """
        Return the number zero.

        This method exists for uniformity with Proxy.depth
        """
        return 0

    def descend(self) -> Iterator[Self]:
        """
        Yield self.

        This method exists for uniformity with Proxy.descend
        """
        yield self

    def descend_p(self) -> 'Iterator[rai.typing.Proxy]':
        """
        Yield nothing.

        This method exists for uniformity with Proxy.descend_p
        """
        return
        yield

    def proxy(self) -> 'rai.typing.Proxy':
        """Return new Proxy pointing to this Compo."""
        return rai.Proxy(self)

    #@property
    #def copy(self) -> NoReturn:
    #    """Deliberately unimplemented -- see Proxy.copy()."""
    #    raise CopyCompoError(
    #        f"`{self}` is a Compo, not a Proxy! "
    #        "Don't copy compos; instead, "
    #        "create a Proxy using the `.proxy()` method "
    #        "and copy that instead."
    #        )

    def walk_hier(self) -> Iterator['rai.typing.CompoLike']:
        """
        Traverse the subcomponent hierarchy of this compo.

        This method will recursively walk through the entire
        subcompo hierarchy of this compo, including self.
        """
        yield self
        for subcompo in self.subcompos.values():
            yield from subcompo.walk_hier()

    def transform_point(
            self,
            point: 'rai.typing.PointLike'
            ) -> 'rai.typing.PointLike':
        """
        Do nothing to `point` and return as-is.

        This method exists for uniformity with Proxy.transform_point.
        """
        return point

    @property
    def scale(self) -> NoReturn:
        """Deliberately unimplemented -- see Proxy.scale."""
        raise TransformCompoError(
            f"Tried to scale `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def move(self) -> NoReturn:
        """Deliberately unimplemented -- see Proxy.move."""
        raise TransformCompoError(
            f"Tried to move `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def movex(self) -> NoReturn:
        """Deliberately unimplemented -- see Proxy.movex."""
        raise TransformCompoError(
            f"Tried to move `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def movey(self) -> NoReturn:
        """Deliberately unimplemented -- see Proxy.movey."""
        raise TransformCompoError(
            f"Tried to move `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def rotate(self) -> NoReturn:
        """Deliberately unimplemented -- see Proxy.rotate."""
        raise TransformCompoError(
            f"Tried to rotate `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def flip(self) -> NoReturn:
        """Deliberately unimplemented -- see Proxy.flip."""
        raise TransformCompoError(
            f"Tried to flip `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def hflip(self) -> NoReturn:
        """Deliberately unimplemented -- see Proxy.hflip."""
        raise TransformCompoError(
            f"Tried to hflip `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )

    @property
    def vflip(self) -> NoReturn:
        """Deliberately unimplemented -- see Proxy.vflip."""
        raise TransformCompoError(
            f"Tried to vflip `{self}`, which is a Compo. "
            "Compos are not transformable; call the `.proxy()` method "
            "to get a Proxy pointing to this compo and transform that instead."
            )
        # TODO tests to make sure the transform functions are all the same
        # in transform, proxy, and compo

    # bbox functions #
    @property
    def bbox(self) -> 'rai.BBox':
        """Get bbox of this compo."""
        bbox = rai.BBox()
        for geoms in self.steamroll().values():
            for geom in geoms:
                bbox.add_poly(geom)
        return bbox

    def __init_subclass__(cls) -> None:
        """Bookkeeping for creating new Compo classes."""
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
        Dirty hack for use in `_make` to quickly add all proxies as subcompos.

        Simply call `self.auto_subcompos(locals())` at the
        end of your `_make()` function, and all of the
        proxies in the scope of `_make()` will be added as
        subcompos.
        If you do no provide `locals()`, this function
        will instead use arcane `inspect` magic
        to traverse the stack and extract them automatically.

        ...or, better yet, do not use this function and
        add subcompos explicitly.
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

    def _str(self, depth: int = 0) -> str:
        """Get string representation of compo."""
        return (
            f"{'<' * (depth == 0)}"
            f"{'\t' * depth}{type(self).__name__} at {rai.wingdingify(id(self))} "
            f"{'>' * (depth == 0)}"
            )

    def __str__(self) -> str:
        return self._str()

    def __repr__(self) -> str:
        """Get string representation of compo."""
        return self.__str__()

    def _repr_svg_(self) -> str:
        """
        Make svg representation of component.

        This is called by jupyter and raimark.
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

