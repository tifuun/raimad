"""
lname_transformers.py: Layer name transformer system for RAIMAD.

RAIMAD layer names and CIF layer names follow different requirements.
While RAIMAD layer names can be (almost) any valid Python identifier,
CIF layer names have a much stricter requirement:
        - must be 1, 2, 3, or 4 characters long
        - must consist of only digits and UPPERCASE letters
        - the layer name `ZZZZ` is reserved and should not be used directly
            in CIF files.
TODO cite spec.

The layer transformer framework allows for a flexible way to
specify how RAIMAD layer names get mapped to CIF layer names
during CIF export.
A single layer transformer is a mapping or callable
(e.g. dict, function, class with a __call__ method),
that takes in the RAIMAD layer name and resutrs a CIF layer name.

The layer transformer may return None or raise KeyError
in order to indicate that it doesn't know what to do with a layer name.
In that case, the CIF exporter will move on to the next
layer transformer and try again.
"""

import raimad as rai

class UntransformableLayerName(ValueError):
    """RAIMAD layer name could not be transformed to CIF layer name"""

class InvalidLayerNameTransformerOutput(ValueError):
    """Layer name transformer did not return a valid CIF layer name"""

def root(name: str) -> str | None:
    """
    Layer name transformer: replace `root` with `ROOT`.

    `root` is the default layer used in all builtin RAIMAD components.
    This transformer maps it to a CIF-compatible name.
    """
    if name == 'root':
        return 'ROOT'
    return None

def noop(name: str) -> str | None:
    """
    No-op layer name transformer.

    If the RAIMAD layer name is already CIF-compatible, just use it.
    """
    if rai.is_lname_valid(name):
        return name
    return None

def capitalise(name: str) -> str | None:
    """
    Capitalizing layer name transformer.

    If the RAIMAD layer name becomes a valid CIF layer name
    by capitalizing all letters in it, use it.
    """
    if 0 < len(name) <= 4:
        if name.isalnum():
            return name.upper()
    return None

class Enumerator:
    """
    Lname transformer that simply counts layers.

    This lname transformer will produce layer names starting from `0001`
    and counting upwards.
    """

    layer_indices: dict[str, int]

    def __init__(self) -> None:
        self.layer_indices = {}

    def __call__(self, name: str) -> str | None:
        """Convert RAIMAD layer name to CIF layer name via enumeration."""
        try:
            layer_index = self.layer_indices[name]

        except KeyError:
            if len(self.layer_indices) >= 9999:
                # TODO test this
                raise RuntimeError(  # TODO custom exception class??
                    "Cannot generate numeric CIF layer name "
                    "because there are more than 9999 layers. "
                    "WHAT are you event doing!?!?!? "
                    )
            layer_index = len(self.layer_indices) + 1
            self.layer_indices[name] = layer_index

        # TODO how does this play with layer order?? Annotations??

        return f'{layer_index:04d}'

