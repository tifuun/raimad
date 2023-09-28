from dataclasses import dataclass, field
from typing import Any

class Layer:
    name: str
    description: str

    def __init__(self, description: str = ''):
        self.description = description

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return self.name

    def __set__(self, obj, value):
        assert type(obj) is self._component
        raise Exception("Cannot override layers")


#@dataclass
#class Layer(object):
#    """
#    Specification of a layer:
#    index, name, fancy name, color1, color2
#    """
#    fancy_name: str = ''
#    #color1: str = ''
#    #color2: str = ''
#    category: LayerCategory.LayerCategory = field(
#        default_factory=lambda: LayerCategory.Unspecified,
#        )
#
#    # Index should be kept last
#    index: int = -1
#
#    @classmethod
#    def Foreground(cls, fancy_name: str = ''):
#        return cls(fancy_name, LayerCategory.Foreground)
#
#    @classmethod
#    def Background(cls, fancy_name: str = ''):
#        return cls(fancy_name, LayerCategory.Background)
#
## TODO layers are a mess
## Foreground/background is dumb,
## index is unused??

