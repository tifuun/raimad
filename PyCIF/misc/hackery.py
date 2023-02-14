"""
hackery -- various kludges and hijinks.
"""


def new_without_init(cls: type):
    """
    Create a new object without calling __init__.
    """
    return cls.__new__(cls)


