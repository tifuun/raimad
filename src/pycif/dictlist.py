

# This class could also be implemented by deriving from `dict`
# instead of encapsulating it
# (actually, that's how it worked originally),
# but that has no real benefit, at the cost of not being 100%
# sure which methods are implemented and where.

# TODO tests for this class!

class DictList():
    """
    A dict that is also a list and is accesible with attribute syntax!
    """
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)

    def __setattr__(self, name, value):

        if name.startswith('_'):
            super().__setattr__(name, value)
            return

        if hasattr(self.__class__, name):
            raise Exception  # TODO actual exception
        else:
            self._dict[name] = self._filter(value)

    def __getattr__(self, name):
        return self._dict[name]

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self._dict.values())[key]
        return self._dict.__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            list(self._dict.values())[key] = value
        self._dict.__setitem__(key, value)

    def append(self, item):
        self._dict[len(self._dict)] = self._filter(item)

    def extend(self, items):
        for item in items:
            self.append(item)

    # TODO update method

    def __iter__(self):
        return iter(self._dict.values())

    def items(self):
        return self._dict.items()

    def values(self):
        return self._dict.values()

    def keys(self):
        return self._dict.keys()

    def __len__(self):
        return self._dict.__len__()

    def _filter(self, item):
        """
        This method is run on every item that gets added to the dictlist.
        This method is intended to be overridden by deriving classes.
        For example, SubcompoContainer uses this to wrap every
        raw compo that gets added in a proxy.
        """
        return item

