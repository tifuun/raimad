import raimad as rai

class Annotation:
    """
    Abstract base class for Options, Layers, and Marks annotations.
    Declares that all of those things have a `name` attribute,
    so mypy does not complain about `compo.py/_class_to_dictlist()`
    """
    name: str | rai.EmptyType

