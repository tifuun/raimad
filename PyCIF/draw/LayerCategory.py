"""
OptCategory -- Option categories
"""

raise NotImplementedError

from dataclasses import dataclass


@dataclass
class LayerCategory(object):
    """
    Layer category specification.
    I don't think users should create their own
    """
    description: str

    def __hash__(self):
        return hash(self.description)

    def __eq__(self, other):
        return self is other


Unspecified = LayerCategory(
    "Unspecified layer category",
    )

Foreground = LayerCategory(
    "Foreground layer, fully opaque",
    )

Background = LayerCategory(
    "Background layer, transparent",
    )

