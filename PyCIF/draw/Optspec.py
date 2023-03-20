from typing import Any
from dataclasses import dataclass, field

from PyCIF.draw import OptCategory
from PyCIF.helpers.Dotdict import Dotdict


Shadow = None

@dataclass
class Optspec(object):
    """
    Specification of an option:
    includes default value, description, shadow status
    """
    default: Any
    desc: str = ''
    category: OptCategory.OptCategory = field(
        default_factory=lambda: OptCategory.Unspecified,
        )
    # Shadow must be kept last!
    shadow: bool = False

    def get_shadow(self):
        """
        Get shadow version of this optspec
        """
        return Optspec(self.default, self.desc, True)

def make_opts(parent_class, **kwargs):
    """
    Helper function to generate options and option descriptions
    for a component class.
    You must pass in the parent class
    TODO add example
    """
    optspecs = Dotdict(parent_class.optspecs)
    for name, spec in kwargs.items():
        if spec is Shadow:
            optspecs[name] = parent_class.optspecs[name].get_shadow()
        else:
            if isinstance(spec, dict):
                optspecs[name] = Optspec(**spec)
            else:
                optspecs[name] = Optspec(*spec)

    return optspecs

