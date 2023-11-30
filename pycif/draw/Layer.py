class InvalidLayerNameError(KeyError):
    pass

class Layer(str):
    _forbidden_names = set(dir(dict))

    __slots__ = ('descr', 'pretty_name')

    descr: str
    pretty_name: str

    def __new__(cls, descr: str = '', pretty_name: str = '', _value: str = ''):
        new = super().__new__(cls, _value)
        new.descr = descr
        new.pretty_name = pretty_name
        return new

    def __set_name__(self, owner, name):
        if name in self._forbidden_names:
            raise InvalidLayerNameError(
                f'Invalid layer name `{name}`. '
                'Consider choosing a different layer name.'
                )

        # This is some advanced descriptor abuse
        setattr(owner, name, Layer(
            _value=name,
            descr=self.descr,
            pretty_name=self.pretty_name
            ))

    def __set__(self, instance, value):
        raise TypeError(f'{type(self)} is immutable')

