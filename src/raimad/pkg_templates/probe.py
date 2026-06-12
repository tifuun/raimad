import os
import importlib
import datetime
from typing import Callable

def try_get_string(fn: Callable[[], str], fallback: str) -> str:
    try:
        val = fn()
        if isinstance(val, str) and bool(val):
            return val
    except Exception:
        pass

    return fallback


def probe_author_name() -> str:
    return try_get_string(os.getlogin, "John Doe")

def probe_raimad_dep() -> str:
    version = importlib.metadata.version('raimad')
    if version:
        return f"raimad=={version}"
    return "raimad"

def probe_copyright_year() -> str:
    return f"{datetime.datetime.now().year}"




