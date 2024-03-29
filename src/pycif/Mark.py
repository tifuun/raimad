from dataclasses import dataclass

import numpy as np

@dataclass
class MarkAnnot:
    name: str
    desc: str

class Mark:
    def __init__(self, compo, point):
        self.point = np.array(point)
        self.compo = compo

    def __array__(self):
        return self.point

    def __class_getitem__(cls, key):
        return MarkAnnot(
            desc=key,
            name='this should be set in compo.__init_subclass_'
            )

