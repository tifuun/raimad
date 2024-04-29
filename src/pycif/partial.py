from copy import copy

class Partial:
    def __init__(self, compo_cls, **kwargs):
        self.kwargs = kwargs
        self.compo_cls = compo_cls

    def __call__(self, **kwargs):
        kwargs2 = copy(self.kwargs)
        kwargs2.update(kwargs)
        return self.compo_cls(**kwargs2)

