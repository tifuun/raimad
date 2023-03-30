# unused

from dataclasses import dataclass, field

from PyCIF.draw import LayerCategory

@dataclass
class Layer(object):
    """
    Specification of a layer:
    index, name, fancy name, color1, color2
    """
    fancy_name: str = ''
    #color1: str = ''
    #color2: str = ''
    category: LayerCategory.LayerCategory = field(
        default_factory=lambda: LayerCategory.Unspecified,
        )

    # Index should be kept last
    index: int = -1

    @classmethod
    def Foreground(cls, fancy_name: str = ''):
        return cls(fancy_name, LayerCategory.Foreground)

    @classmethod
    def Background(cls, fancy_name: str = ''):
        return cls(fancy_name, LayerCategory.Background)

# TODO layers are a mess
# Foreground/background is dumb,
# index is unused??

