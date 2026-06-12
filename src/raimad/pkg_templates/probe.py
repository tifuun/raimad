"""Probe current environment and guess some info for package template."""

import os
import importlib
import datetime
from typing import Callable

def try_get_string(fn: Callable[[], str], fallback: str) -> str:
    """Try to execute buggy function and return fallback it it fails."""
    try:
        val = fn()
        if isinstance(val, str) and bool(val):
            return val
    except Exception:
        pass

    return fallback


def probe_author_name() -> str:
    """Guess author name from system username."""
    return try_get_string(os.getlogin, "John Doe")

def probe_raimad_dep() -> str:
    """Get pyproject.toml requirement string for this version of RAIMAD."""
    version = importlib.metadata.version('raimad')
    if version:
        return f"raimad=={version}"
    return "raimad"

def probe_copyright_year() -> str:
    """Get copyright year (i.e. year from current system time)."""
    return f"{datetime.datetime.now().year}"




