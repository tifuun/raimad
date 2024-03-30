from dataclasses import dataclass

@dataclass
class LayerAnnot:
    name: str
    desc: str

class Layer:
    def __init__(self):
        raise NotImplementedError

    def __class_getitem__(cls, key):
        return LayerAnnot(
            desc=key,
            name='this should be set in compo.__init_subclass_'
            )

