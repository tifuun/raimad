from typing import ClassVar

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

import raimad as rai

class Option:
    def __init__(self, desc: str, browser_default=rai.Empty):
        self.desc = desc
        self.category = type(self)
        self.name = 'this should be set in compo.__init_subclass_'
        self.default = 'this should be set in compo.__init_subclass_'
        self.browser_default = browser_default
        self.annot = 'this should be set in compo.__init_subclass_'

    # These are shorthands which will be assigned at
    # the end of this file.
    # The annotations are here to make mypy shut up
    Functional: ClassVar[type[Self]]
    Geometric: ClassVar[type[Self]]
    Debug: ClassVar[type[Self]]
    Environmental: ClassVar[type[Self]]

class Geometric(Option):
    pass

class Functional(Option):
    pass

class Debug(Option):
    pass

class Environmental(Option):
    pass


Option.Functional = Functional
Option.Geometric = Geometric
Option.Debug = Debug
Option.Environmental = Environmental

