from typing import Callable, Union, Mapping, TypeAlias, Sequence

import raimad as rai

def root(name: str) -> str | None:
    if name == 'root':
        return 'ROOT'
    return None

def noop(name: str) -> str | None:
    if rai.is_lname_valid(name):
        return name
    return None

def capitalise(name: str) -> str | None:
    if 0 < len(name) <= 4:
        if name.isalnum():
            return name.upper()
    return None

class Enumerator:

    layer_indices: dict[str, int]

    def __init__(self) -> None:
        self.layer_indices = {}

    def __call__(self, name: str) -> str | None:
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

        return str(layer_index)

