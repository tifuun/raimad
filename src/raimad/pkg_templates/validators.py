"""validators.py: validator functions for pkg template user input."""

from typing import TypeAlias, Callable
from pathlib import Path
import re

PKG_NAME_CHARS = set('abcdefghijklmnopqrstuvwxyz0123456789_')

Response: TypeAlias = tuple[bool, str]
Validator: TypeAlias = Callable[[str], Response]

def pkg_name(name: str) -> Response:
    """Validate RAIMAD package name."""
    if not name.startswith('rai_'):
        return False, "package name must start with `rai_`."

    if not name.isidentifier():
        return False, "package name must be a valid Python identifier."

    if not set(name).issubset(PKG_NAME_CHARS):
        return (
            False,
            "package name must only contain these characters: "
            f"{PKG_NAME_CHARS}"
        )

    return True, ""

def pkg_desc(desc: str) -> Response:
    """Validate RAIMAD package description."""
    if '\n' in desc:
        # AFAIK this will never happen because `input` is
        # by-definition one line
        return False, "description must be single-line"
    return True, ""

def author_email(email: str) -> Response:
    """Validate author email."""
    if not re.match(r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$", email):
        return False, "email must be valid"
    return True, ""

def compo_pascal(pascal: str) -> Response:
    """Validate component name (PascalCase)."""
    if not re.match(r"^(?:[A-Z][a-z]*[0-9]*)+$", pascal):
        return False, "Must be in PascalCase"

    if not pascal.isidentifier():
        return False, "Compo name must be a valid Python identifier."

    return True, ""

def compo_snake(snake: str) -> Response:
    """Validate component name (snake_case)."""
    if not re.match(r"^(?:[a-z0-9]+_)*[a-z0-9]+$", snake):
        print('aaaaa', snake)
        return False, "Must be in snake_case"

    if not snake.isidentifier():
        return False, "Compo name must be a valid Python identifier."

    return True, ""

def path(pathstr: str) -> Response:
    """Validate RAIMAD package path."""
    path = Path(pathstr)

    if path.exists():
        return False, f"The path `{path}` already exists."

    #earliest_parent = path
    #while not earliest_parent.exists():
    #    earlier_parent = earliest_parent.parent

    #if not os.access(earliest_parent, os.W_OK):
    #    return (
    #        False,
    #        f"The first existing parent directory (`{earliest_parent}`) "
    #        "is not writeable."
    #        )

    return True, ""

