import raimad as rai

class ProxyableDictListMixin():
    _proxy: 'None | rai.typing.Proxy'

    def _post_init(self) -> None:
        self._proxy = None

    def _get_proxy_view(self, proxy: 'rai.t.Proxy') -> Self:
        new = type(self)(self._dict, copy=False)
        new._proxy = proxy
        return new

class BaseMarksContainer(
        rai.DictList(['rai.t.Point', 'rai.t.PointLike', 'rai.t.PointLike'])
        ):
    def _filter_set(self, val: 'rai.t.PointLike') -> 'rai.t.Point':
        """
        set filter for markscontainer:
        make sure that no matter what creature gets passed in
        (regular tuple or boundpoint or whatever),
        what gets stored is a simple regular tuple.
        """
        return (val[0], val[1])


class MarksContainer(
        BaseMarksContainer(['rai.t.Point', 'rai.t.PointLike', 'rai.t.Point'])
        ):
    pass

class ProxyMarksContainer(
        ProxyableDictListMixin,
        rai.DictList(['rai.t.Point', 'rai.t.PointLike', 'rai.t.BoundPoint'])
        ):
    def _filter_get(self, val: 'rai.typing.Point') -> 'rai.typing.BoundPoint':

        # TODO poke around with these annotation
        # and see if mypy detects them

        return rai.BoundPoint(
            *self._proxy.transform_point(val),
            self._proxy
            )

class SubcompoContainer(
        ProxyableDictListMixin,
        rai.DictList(['rai.t.Proxy', 'rai.t.Proxy', 'rai.t.Proxy'])
        ):
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
    
    def _filter_get(self, val: T) -> T:
        if self._proxy is not None:
            return self._proxy.copy_reassign(val, _autogen=True)
        return val

