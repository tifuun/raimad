from typing import (
    ItemsView,
    KeysView,
    ValuesView,
    Iterable,
    Iterator,
    TypeVar,
    Generic,
    Any,
    Never,
    )

# This class could also be implemented by deriving from `dict`
# instead of encapsulating it
# (actually, that's how it worked originally),
# but that has no real benefit, at the cost of not being 100%
# sure which methods are implemented and where.

# TODO tests for this class!

T_STORED = TypeVar('T_STORED')
T_ADDED = TypeVar('T_ADDED')
T_RETURNED = TypeVar('T_RETURNED')
class FilteredDictList(Generic[T_STORED, T_ADDED, T_RETURNED]):
    """
    A dict that is also a list and is accesible with attribute syntax!
    """
    _dict: dict[str | int, T_STORED]

    def __init__(
            self,
            dict_: dict[int | str, T_STORED] | None = None,
            *,
            copy: bool | None = None
            ) -> None:

        if dict_ is None:
            self._dict = dict()

        elif isinstance(dict_, dict):
            if copy is True:
                self._dict = dict(dict_)

            elif copy is False:
                self._dict = dict_

            elif copy is None:
                raise TypeError("Must specify `copy` (bool) if passing `dict_`")

            else:
                raise TypeError('`copy` must be a bool')

        else:
            raise TypeError('`dict_` must be a dict')

        self._post_init()

    def __setitem__(self, key: int | str, val: T_ADDED) -> None:
        if isinstance(key, int):
            self._dict[tuple(self._dict.keys())[key]] = self._filter_set(val)

        elif isinstance(key, str):
            if key.startswith('_'):
                raise KeyError(
                    "Keys cannot start with underscore; "
                    "underscores are reserved for custom attributes. "
                    )

            if hasattr(self.__class__, key):
                raise KeyError(
                    f"Key cannot be the same as an existing class attribute. "
                    )

            self._dict.__setitem__(key, self._filter_set(val))

        else:
            raise TypeError("key must be int or str")

        self._sanitycheck()

    def __getitem__(self, key: int | str) -> T_RETURNED:
        if isinstance(key, int):
            val = list(self._dict.values())[key]
        elif isinstance(key, str):
            val = self._dict.__getitem__(key)
        else:
            raise KeyError("Key must be int or str")

        return self._filter_get(val)

    def __setattr__(self, name: str, val: T_ADDED) -> None:

        if name.startswith('_'):
            super().__setattr__(name, val)

        elif hasattr(self.__class__, name):
            self._sanitycheck()
            raise AttributeError(
                f"Cannot override class attribute {name}"
                )

        else:
            self._dict[name] = self._filter_set(val)

        self._sanitycheck()

    def __getattr__(self, name: str) -> T_RETURNED | Any:
        if name.startswith('_'):
            return super().__getattribute__(name)

        return self._filter_get(self._dict[name])

    def append(self, val: T_ADDED) -> None:
        self._sanitycheck()
        self._dict[len(self)] = self._filter_set(val)

    def extend(self, items: Iterable[T_ADDED]) -> None:
        for item in items:
            self.append(item)

    def _sanitycheck(self) -> None:
        assert all((isinstance(key, (int, str)) for key in self._dict.keys()))

        int_keys = [key for key in self._dict.keys() if isinstance(key, int)]
        if int_keys:
            assert max(int_keys) <= len(self)

    # TODO update method

    def __iter__(self) -> Never:
        raise NotImplementedError(
            "Iterating over dictlist is ambiguous. "
            "Please use `.keys()`, `.values()`, or `.items()`."
            )

    def items(self) -> Iterator[tuple[str | int, T_RETURNED]]:
        return (
            (key, self._filter_get(val))
            for key, val in self._dict.items()
            )

    def values(self) -> Iterator[T_RETURNED]:
        return (
            self._filter_get(val)
            for val in self._dict.values()
            )

    def keys(self) -> KeysView[str | int]:
        return self._dict.keys()

    def __len__(self) -> int:
        return self._dict.__len__()

    def _post_init(self) -> None:
        """
        Child classes may override this method to add more code
        after running __init__ without having to remember
        __init__'s signature.
        """

    def _filter_set(self, val: T_ADDED) -> T_STORED:
        raise NotImplementedError

    def _filter_get(self, val: T_STORED) -> T_RETURNED:
        raise NotImplementedError


T = TypeVar('T')
class DictList(FilteredDictList[T, T, T]):
    def _filter_set(self, val: T) -> T:
        return val

    def _filter_get(self, val: T) -> T:
        return val

