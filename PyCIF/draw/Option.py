from typing import Any
from dataclasses import dataclass, field

from PyCIF.draw import OptCategory
from PyCIF.helpers.Dotdict import Dotdict


Shadow = None

@dataclass
class Option(object):
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
        return type(self)(self.default, self.desc, True)

