from typing import Callable, Union, Mapping, TypeAlias, Sequence

import raimad as rai

LNameTransformer: TypeAlias = Union[
        Callable[[str], str | None],
        Mapping[str, str | None]
        ]
LNameTransformers: TypeAlias = Sequence[LNameTransformer]

def root(name: str):
    if name == 'root':
        return 'ROOT'

def noop(name: str):
    if rai.is_lname_valid(name):
        return name

def annot(name: str):
    if rai.is_lname_valid(name):
        return name

def capitalise(name: str):
    if 0 < len(name) <= 4:
        if name.is_alnum():
            return name.upper()
    return None

class Enumerator:
    def __init__(self):
        self.layer_indices = {}

    def __call__(self, name: str):
        try:
            layer_index = self.layer_indices[layer]

        except KeyError:
            if len(self.layer_indices) >= 9999:
                # TODO test this
                raise RuntimeError(  # TODO custom exception class??
                    "Cannot generate numeric CIF layer name "
                    "because there are more than 9999 layers. "
                    "WHAT are you event doing!?!?!? "
                    )
            layer_index = len(self.layer_indices) + 1
            self.layer_indices[layer] = layer_index

        # TODO how does this play with layer order?? Annotations??

        return str(layer_index)

