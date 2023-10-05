class Layer:
    name: str
    description: str

    def __init__(self, description: str = ''):
        self.description = description

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.name
        return self.name

    def __set__(self, obj, value):
        assert type(obj) is self._component
        raise Exception("Cannot override layers")

