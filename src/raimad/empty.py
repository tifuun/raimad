"""empty.py: Home to EmptyType and Empty."""

from typing import ClassVar

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

    This is a singleton class, meaning only one Empty exists
    in the entire world.
    If you try to instantiate a new Empty,
    you will just get the same one.
    """

    instance: ClassVar['EmptyType']

    def __new__(cls) -> 'EmptyType':
        """Return the one Empty or create it if missing."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(EmptyType, cls).__new__(cls)
        return cls.instance

    def __bool__(self) -> bool:
        """Get boolean representation of Empty (always False)."""
        return False

    def __str__(self) -> str:
        """Get string representation of Empty."""
        return "<Empty>"

    def __repr__(self) -> str:
        """Get string representation of Empty."""
        return "<Empty>"


Empty: EmptyType = EmptyType()

