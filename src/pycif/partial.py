from typing import Any
from copy import copy
import pycif as pc

class Partial:
    compo_cls: 'pc.typing.CompoClass'

    def __init__(self, compo_cls: 'pc.typing.CompoClass', **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.compo_cls = compo_cls

    def __call__(self, **kwargs: Any) -> 'pc.typing.RealCompo':
        kwargs2 = copy(self.kwargs)
        kwargs2.update(kwargs)
        return self.compo_cls(**kwargs2)

