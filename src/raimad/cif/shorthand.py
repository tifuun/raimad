"""
shorthand.py

The job of this file is to define an `export_cif`
function that uses whatever cif exporter is stable in this version of raimad
"""

from pathlib import Path
from typing import TextIO, Protocol, Any

import raimad as rai

class InvalidDestinationError(ValueError):
    pass

class ExporterProto(Protocol):
    def __init__(
            self,
            compo: 'rai.typing.CompoLike',
            *args: Any,
            **kwargs: Any
            ) -> None:
        ...

    cif_string: str

def export_cif(
        compo: 'rai.typing.CompoLike',
        dest: str | Path | TextIO | None = None,
        exporter: type[ExporterProto] | None = None,
        *args: Any,
        **kwargs: Any,
        ) -> str:
    exporter_instance = (exporter or rai.cif.NoReuse)(compo, *args, **kwargs)
    cif_string = exporter_instance.cif_string

    if dest is None:
        pass
    elif isinstance(dest, (str, Path)):
        with open(dest, 'w') as file:
            file.write(cif_string)
    elif hasattr(dest, 'write'):
        dest.write(cif_string)
    else:
        raise InvalidDestinationError(
            f"Invalid destination type {type(dest)}. "
            "Must be a file path or a file-like stream."
            )

    return cif_string

