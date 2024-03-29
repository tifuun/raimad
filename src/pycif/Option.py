from typing import Any
from dataclasses import dataclass

@dataclass
class OptionAnnot:
    name: str
    desc: str
    category: type  # TODO smarter type annotation for this
    default: Any
    annot: Any  # TODO is there a type annotation for type annotations?

class Option:
    def __init__(self):
        raise NotImplementedError

    def __class_getitem__(cls, key):
        return OptionAnnot(
            desc=key,
            name='this should be set in Compo.__init_subclass_',
            category=cls,
            default='this should be set in Compo.__init_subclass_',
            annot='this should be set in Compo.__init_subclass_',
            )

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

