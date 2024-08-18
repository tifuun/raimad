"""option.py: home to the Option class and its subclasses."""
from typing import ClassVar, Any

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

import raimad as rai


class Option(rai.Annotation):
    """
    Option: an annotation for an option.

    Option objects are meant to be declared inside the `Options`
    nested class of every Compo.
    They serve as annotations for the options that the `_make`
    method takes that better explain what those options do.

    TODO explain that its better to use the subclasses
    """

    annot: str | rai.EmptyType | type
    default: Any | rai.EmptyType

    def __init__(
            self,
            desc: str,
            browser_default: Any | rai.EmptyType = rai.Empty) -> None:
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
    """
    Geometric option annotation.

    This subclass of Option is meant for options that directly
    correspond to physical dimensions in the compo:
    lengths, widths, angles.
    """

class Functional(Option):
    """
    Functional option annotation.

    This subclass of Option is meant for options that correspond
    to functional properties of a compo:
    frequencies, impedances, etc.
    The idea is that Functional options are used to derive
    the geometry of a Compo
    """

class Debug(Option):
    """
    Debug option annotation.

    This subclass of Option is meant for options that
    are useful for debugging, but not production use.
    They can control whether extra info is printed to stderr,
    whether parts of the compo are ommitted for faster compilation,
    etc.
    """

class Environmental(Option):
    """
    Environmental option annotation.

    This subclass of Option is meant for options that
    prescribe envrionmental constants like temperature
    of absolute zero,
    planck length,
    and so forth,
    that you don't feel like hardcoding.
    """


Option.Functional = Functional
Option.Geometric = Geometric
Option.Debug = Debug
Option.Environmental = Environmental

