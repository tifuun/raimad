"""
empty.py
This file contains the EmptyType class and the Empty object
"""

from typing import ClassVar

try:
    from typing import Self

except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

class EmptyType:
    """
    Empty: an object representing an empty field.
    This can be used similar to `None`,
    except in cases where `None` has a different meaning.
    For example, compo options by default have their
    `browser_default` property set to Empty,
    indicating that there is no default value to use
    in the component browser.
    Setting it to None would mean that the default value is None.

    This is a singleton class.
    """
    instance: ClassVar[Self]

    def __new__(cls) -> 'EmptyType':
        if not hasattr(cls, 'instance'):
            cls.instance = super(EmptyType, cls).__new__(cls)
        return cls.instance

    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        return "<Empty>"

    def __repr__(self) -> str:
        return "<Empty>"


Empty: EmptyType = EmptyType()

