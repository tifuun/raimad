"""jupyter.py -- helper methods for jupyter notebook integration."""

from typing import Any

try:
    import IPython
    # FIXME any way to get ipython to play nice with mypy?
    # or just have to use these type: ignore crutches?
    # FIXME this is not covered by unit tests!
    if 'IPKernelApp' in IPython.get_ipython().config:  # type: ignore
        IS_NOTEBOOK = True
    else:
        IS_NOTEBOOK = False
except ImportError:
    IS_NOTEBOOK = False
except AttributeError:
    IS_NOTEBOOK = False

def jupyter_display(thing: Any) -> None:
    """
    Alias for IPython.display.display().

    Parameters
    ----------
    thing
        the object to display.
    """
    IPython.display.display(thing)  # type: ignore

__all__ = ["IS_NOTEBOOK", "jupyter_display"]

