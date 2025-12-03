"""saveto.py: helper for saving string to path, open file, or stream."""

from typing import TypeAlias
from pathlib import Path
from typing import TextIO

class InvalidDestinationError(ValueError):
    """Error raised by `_saveto` helper when `dest` is set incorrectly."""

# This can be useful to end-users but will hold off making
# this a public method for now because many possible usecases
# not handled (e.g. bytes)

Destination: TypeAlias = str | Path | TextIO | None

def _saveto(string: str, dest: Destination = None):
    if dest is None:
        pass
    elif isinstance(dest, (str, Path)):
        with open(dest, 'w') as file:
            file.write(string)
    elif hasattr(dest, 'write'):
        dest.write(string)
    else:
        raise InvalidDestinationError(
            f"Invalid destination type {type(dest)}. "
            "Must be a file path or a file-like stream."
            )

    return string

