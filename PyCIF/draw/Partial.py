"""
Allow specifying component options partially
"""

import PyCIF as pc

class Partial:
    def __init__(
            self,
            Compo: pc.Component,
            opts: pc.Dict | None = None,
            transform: pc.Transform | None = None,
            ):
        self.Compo = Compo
        self.opts = pc.Dict({
            k: v for k, v in opts.items()
            if k in Compo.Options.keys()
            }) if opts else pc.Dict()
        self.transform = transform.copy() if transform else pc.Transform()

    def __call__(self, opts=None, transform=None):
        return self.Compo(
            pc.Dict(self.opts, opts),
            self.transform.apply_transform(transform)
                if transform else self.transform,
            )


