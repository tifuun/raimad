"""dictlist.py: home to FilteredDictList and DictList classes."""

from typing import (
    KeysView,
    Iterable,
    Iterator,
    TypeVar,
    Generic,
    Any,
    NoReturn,
    )

T_STORED = TypeVar('T_STORED')
T_ADDED = TypeVar('T_ADDED')
T_RETURNED = TypeVar('T_RETURNED')
class FilteredDictList(Generic[T_STORED, T_ADDED, T_RETURNED]):
    """
    Base class for making containers that act like both list and dict.

    FilteredDictList stores data in an internal dict,
    but that data can also be accessed by index,
    and by attribute notation.
    FilteredDictList is an abstract class with two virtual
    methods: _filter_set and _filter_get.
    _filter_set takes any new item added to the list
    (via assignment to attribute, assignment to key, or .append)
    of generic type T_ADDED and transforms it to
    generic type T_STORED,
    which is what is actually stored in the encapsulated dict.
    _filter_get takes an item of type T_STORED
    and transforms it into T_RETURNED just before it
    is returned from the list
    (via getting an attribute, key, by index, or by iteration)

    TODO raises, examples, link to dictlist
    TODO explain how it is used in markscontainer, etc.
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
                raise TypeError(
                    "Must specify `copy` (bool) if passing `dict_`"
                    )

            else:
                raise TypeError('`copy` must be a bool')

        else:
            raise TypeError('`dict_` must be a dict')

        self._post_init()

    def __setitem__(self, key: int | str, val: T_ADDED) -> None:
        """Add or replace item in dictlist by key."""
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
                    "Key cannot be the same as "
                    "an existing class attribute. "
                    )

            self._dict.__setitem__(key, self._filter_set(val))

        else:
            raise TypeError("key must be int or str")

        self._sanitycheck()

    def __getitem__(self, key: int | str) -> T_RETURNED:
        """Get item from dictlist by key."""
        if isinstance(key, int):
            val = list(self._dict.values())[key]
        elif isinstance(key, str):
            val = self._dict.__getitem__(key)
        else:
            raise KeyError("Key must be int or str")

        return self._filter_get(val)

    def __setattr__(self, name: str, val: T_ADDED) -> None:
        """Add item to dictlist by key with attr notation."""
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
        """Get item from dictlist by key with attr notation."""
        if name.startswith('_'):
            return super().__getattribute__(name)

        return self._filter_get(self._dict[name])

    def append(self, val: T_ADDED) -> None:
        """Add item to dictlist."""
        self._sanitycheck()
        self._dict[len(self)] = self._filter_set(val)

    def extend(self, items: Iterable[T_ADDED]) -> None:
        """Add multiple items to dictlist."""
        for item in items:
            self.append(item)

    def _sanitycheck(self) -> None:
        assert all((isinstance(key, (int, str)) for key in self._dict.keys()))

        int_keys = [key for key in self._dict.keys() if isinstance(key, int)]
        if int_keys:
            assert max(int_keys) <= len(self)

    # TODO update method

    def __iter__(self) -> NoReturn:
        """
        Deliberately not implemented.

        Iterating through a dictlist is ambiguous.
        Use `.keys()`, `.values()`, or `.items()`.
        """
        raise NotImplementedError(
            "Iterating over dictlist is ambiguous. "
            "Please use `.keys()`, `.values()`, or `.items()`."
            )

    def items(self) -> Iterator[tuple[str | int, T_RETURNED]]:
        """Get iterator of key-value pairs in DictList."""
        return (
            (key, self._filter_get(val))
            for key, val in self._dict.items()
            )

    def values(self) -> Iterator[T_RETURNED]:
        """Get values in DictList."""
        return (
            self._filter_get(val)
            for val in self._dict.values()
            )

    def keys(self) -> KeysView[str | int]:
        """Get keys of DictList."""
        return self._dict.keys()

    def __len__(self) -> int:
        """Get number of items stored in DictList."""
        return self._dict.__len__()

    def _post_init(self) -> None:
        """
        Function that gets automatically run after __init__.

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
    """
    A container that acts like a dict, a list, and an object all in one.

    This is a simplified version of FilteredDictList
    where T_STORED, T_ADDED, and T_RETURNED are all the same.
    It is not an abstract class, you can instantiate it
    directly.

    TODO examples.
    """

    def _filter_set(self, val: T) -> T:
        return val

    def _filter_get(self, val: T) -> T:
        return val

