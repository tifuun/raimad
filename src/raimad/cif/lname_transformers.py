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

from warnings import warn
import raimad as rai
from raimad.types import LNameTransformers

class CIFLayerNameWarning(UserWarning):
    """Warning for automatic numeric layer names."""

class UntransformableLayerName(ValueError):
    """RAIMAD layer name could not be transformed to CIF layer name."""

class InvalidLayerNameTransformerOutput(UserWarning):
    """Layer name transformer did not return a valid CIF layer name."""

class InvalidLayerNameTransformerCallable(TypeError):
    """Invalid layer name transformer callable (e.g. doesn't take one arg)."""

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

    def __init__(self, warning: str | None = None) -> None:
        self.layer_indices = {}
        self.warning = warning

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

        result = f'{layer_index:04d}'

        if self.warning is not None:
            warn(
                self.warning.format(name=name, result=result),
                CIFLayerNameWarning,
                )

        return result

def klayout(name: str) -> str | None:
    """
    Prefix layer name with `_L`.

    This will produce CIF layer names that are recognized
    by KLayout, even if not necessarily conformant with the CIF spec.
    """
    return f'L_{name}'


def get_lname_transformers(compo):
    # TODO DOCUMENT THE LAMBDA THING SOMEWHERE!!
    if hasattr(compo, '_experimental_lname_transformers'):
        if hasattr(compo._experimental_lname_transformers, '__call__'):
            return compo._experimental_lname_transformers()
        else:
            return compo._experimental_lname_transformers
    else:
        if hasattr(compo, '_experimental_extra_lname_transformers'):
            if hasattr(
                    compo._experimental_extra_lname_transformers,
                    '__call__'
                    ):
                extras = compo._experimental_extra_lname_transformers()
            else:
                extras = compo._experimental_extra_lname_transformers
        else:
            extras = []

        return (
            *extras,
            root,
            noop,
            capitalise,
            Enumerator(
                warning=(
                    "RAIMAD Layer name `{name}` converted to numeric CIF "
                    "name `{result}.` For custom CIF layer names, specify "
                    "a layer name transformer. To silence this warning "
                    "while keeping the behavior, specify the "
                    "rai.cif.lname_transformers.Enumerator() transformer "
                    "manually. "
                    )
                )
            )

    assert False


def transform_lname(lname_transformers: LNameTransformers, name: str) -> str:
    for transformer in lname_transformers:
        if hasattr(transformer, '__getitem__'):
            try:
                transformed = transformer[name]
            except KeyError:
                transformed = None

        #elif isinstance(transformer, rai.types.LNameTransformerCallable):
        elif hasattr(transformer, '__call__'):
            try:
                transformed = transformer(name)
            except TypeError as err:
                raise InvalidLayerNameTransformerCallable(
                    "Could not call lname transformer {transformer}."
                    ) from err

        if transformed is not None:
            if not rai.is_lname_valid(transformed):
                warn(
                    f"Layer name `{name}` was transformed to `{transformed}` "
                    f"by transformer `{transformer}`, which is not a valid "
                    f"CIF layer name. "
                    f"The produced file may not be compatible with "
                    f"all CIF viewers!!"
                    ,
                    InvalidLayerNameTransformerOutput
                    )
            break

    if transformed is None:
        raise UntransformableLayerName(
            f"RAIMAD Layer name `{name}` could not be transformed to "
            "a valid CIF layer name by any of the specified transformers "
            f"( {lname_transformers} ). "
            "Change the layer name or add a transformer that understands it. "
            )

    return transformed

