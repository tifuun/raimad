from typing import Any
from dataclasses import dataclass, field

from PyCIF.draw import OptCategory

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

    Shadow = None

    def get_shadow(self):
        """
        Get shadow version of this optspec
        """
        return type(self)(self.default, self.desc, True)

    @classmethod
    def Geometric(cls, default: Any, desc: str = ''):
        return cls(default, desc, OptCategory.Geometric)

    @classmethod
    def Functional(cls, default: Any, desc: str = ''):
        return cls(default, desc, OptCategory.Functional)

    @classmethod
    def Environmental(cls, default: Any, desc: str = ''):
        return cls(default, desc, OptCategory.Environmental)

    @classmethod
    def Manufacture(cls, default: Any, desc: str = ''):
        return cls(default, desc, OptCategory.Manufacture)

    @classmethod
    def DevDebug(cls, default: Any, desc: str = ''):
        return cls(default, desc, OptCategory.DevDebug)


