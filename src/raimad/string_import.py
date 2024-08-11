"""
string_import -- given a string specifying module and object, import it.

This code is ~~stolen from~~ heavily inspired by uvicorn.
"""

from typing import Any

import importlib
import raimad as rai

class StringImportError(ImportError):
    """Error type for errors raised by `string_import()`."""

# TODO Any is not appropriate here
def string_import(import_str: str, multiple: bool = False) -> Any:
    """
    Import a compo, specified by a string.

    Parameters
    ----------
    import_str : str
        A string representing a component or an entire module.
        The string is the the format
        `module.module.module.[...].compo` to import a specific
        compo,
        or 
        `module.module.module.[...]` to import all compos
        in an entire module

    TODO finish this docstring

    """
    module_str, _, attr_str = import_str.partition(':')

    try:
        module = importlib.import_module(module_str)
    except ImportError as exc:
        if exc.name != module_str:
            raise exc from None
        raise StringImportError(
            f'Could not import module "{module_str}".'
            )

    if attr_str == '':

        names = []
        compos = []
        for name, attr in module.__dict__.items():
            if rai.is_compo_class(attr):
                names.append(name)
                compos.append(attr)

        if not compos:
            raise StringImportError(
                f"Module {module} identified by `{module_str}` "
                "does not have any raimad components inside of it."
                )

        elif multiple:
            return compos

        elif len(compos) == 1:
            return compos[0]

        else:
            raise StringImportError(
                f"Module {module} identified by `{module_str}` "
                "has multiple components inside it: "
                f"`{names}`. "
                "You need to tell me which one you want."
                )

    else:
        try:
            attr = getattr(module, attr_str)

        except AttributeError:
            raise StringImportError(
                f"Module {module} identified by `{module_str}` "
                f"does not have an object called `{attr_str}`."
                )

    if not rai.is_compo_class(attr):
        raise StringImportError(
            f"Object `{attr}` of "
            f"module {module} identified by `{module_str}` "
            "is not a raimad component."
            )

    return attr

