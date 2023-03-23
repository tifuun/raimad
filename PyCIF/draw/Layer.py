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


