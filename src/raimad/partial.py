from typing import Any
from copy import copy
import raimad as rai

class Partial:
    compo_cls: 'rai.typing.CompoClass'

    def __init__(self, compo_cls: 'rai.typing.CompoClass', **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.compo_cls = compo_cls

    def __call__(self, **kwargs: Any) -> 'rai.typing.RealCompo':
        kwargs2 = copy(self.kwargs)
        kwargs2.update(kwargs)
        return self.compo_cls(**kwargs2)

