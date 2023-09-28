from typing import TypeVar, Generic, Self
import sys

# First time using generics, wish me luck!
T = TypeVar('T')
class Option(Generic[T]):
    name: str
    default: T
    description: str = ''
    shadow: bool = False

    Shadow = None

    def __init__(self, default: T, description: str = ''):
        self.default = default
        self.description = description

    def __set_name__(self, owner, name: str):
        self.name = name

    def __get__(self, obj, objtype=None) -> T | Self:
        if obj is None:
            return self

        return obj._option_values.get(self.name, self.default)

    def __set__(self, obj, value: T):
        raise NotImplementedError
        obj._option_values[self.name] = value


# Allows constructing a base Option object
# (i.e. unspecified option category)
# by calling this module directly
# (i.e. pc.Option('description') instead of pc.Option.Option('descr') )


class Geometric(Option):
    """
    Geometric parameters of the design.
    Widths, lengths, thicknesses, etc.
    """
    pass

class Functional(Option):
    """
    Functional parameters. Wavelengths, frequencies, etc.
    """
    pass

class Environmental(Option):
    """
    Physical constants / effects that influence the design.
    """
    pass

class Manufacture(Option):
    """
    Geometric options that regard the manufacturing process.
    """
    pass

class Debug(Option):
    """
    Options used for debugging by the component developer.
    """
    pass


thismodule = sys.modules[__name__]
class ModuleWithACustom__call__BecauseIDoWhatIWant(type(thismodule)):
    """
    Adds shortcut so that you can call pc.Option() instead of
    pc.Option.Option()
    """
    __call__ = Option


thismodule.__class__ = ModuleWithACustom__call__BecauseIDoWhatIWant

