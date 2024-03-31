
class DictList(dict):
    """
    A dict that is also a list and is accesible with attribute syntax!
    """
    def __setattr__(self, name, value):

        if name.startswith('_'):
            super().__setattr__(name, value)
            return

        if hasattr(self.__class__, name):
            raise Exception  # TODO actual exception
        else:
            self[name] = self._filter(value)

    def __getattr__(self, name):
        return self[name]

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self.values())[key]
        return super().__getitem__(key)

    def append(self, item):
        self[len(self)] = self._filter(item)

    def extend(self, items):
        for item in items:
            self.append(item)

    # TODO update

    def __iter__(self):
        return iter(self.values())

    def _filter(self, item):
        return item

