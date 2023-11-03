"""
Allow specifying component options partially
"""

import PyCIF as pc

class Partial:
    def __init__(
            self,
            Compo: pc.Component,
            options: dict | None = None,
            ):
        self.Compo = Compo
        self.options = options or {}

    def __call__(self, options=None):
        return self.Compo(
            options=pc.Dict(self.options, options),
            )


