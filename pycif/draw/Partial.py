"""
Allow specifying compo options partially
"""

import pycif as pc

class Partial:
    def __init__(
            self,
            Compo: pc.Compo,
            options: dict | None = None,
            ):
        self.Compo = Compo
        self.options = options or {}

    def __call__(self, options=None):
        new_options = dict()
        new_options.update(self.options)
        new_options.update(options)
        return self.Compo(
            options=new_options,
            )


