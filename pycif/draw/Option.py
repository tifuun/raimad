from typing import TypeVar, Generic, Self, Any
import sys

class InvalidOptionNameError(KeyError):
    pass

class UnknownOptionSuppliedError(KeyError):
    pass

class Option(str):

    _forbidden_names = set(dir(dict))

    default: Any
    descr: str = ''
    #shadow: bool = False

    #Shadow = None

    def __new__(cls, default: Any, descr: str = '', pretty_name: str = '', _name: str = ''):
        new = super().__new__(cls, _name)
        new.default = default
        new.descr = descr
        new.pretty_name = pretty_name
        return new

    #def __init__(self, default: T, description: str = ''):
    #    self.default = default
    #    self.description = description

    #def __set_name__(self, owner, name: str):
    #    self.name = name

    def __set_name__(self, owner, name):
        # This is some advanced descriptor abuse
        if name in self._forbidden_names:
            raise InvalidOptionNameError(
                f'Invalid option name `{name}`. '
                'Consider choosing a different option name.'
                )

        setattr(owner, name, Option(
            _name=name,
            default=self.default,
            descr=self.descr,
            pretty_name=self.pretty_name
            ))

    #def __get__(self, obj, objtype=None) -> T | Self:
    #    if obj is None:
    #        return self

    #    return obj._option_values.get(self.name, self.default)

    def __get__(self, owner, objtype=None):
        if owner is None:
            return self
        return owner[self]

    #def __set__(self, obj, value: T):
    #    raise NotImplementedError
    #    obj._option_values[self.name] = value


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
    Options used for debugging by the compo developer.
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

