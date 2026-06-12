import os
import importlib
import datetime

def try_get_string(fn, fallback):
    try:
        val = fn()
        if isinstance(val, str) and bool(val):
            return val
    except Exception:
        pass

    return fallback


def probe_author_name():
    return try_get_string(os.getlogin, "John Doe")

def probe_raimad_dep():
    version = importlib.metadata.version('raimad')
    if version:
        return f"raimad=={version}"
    return "raimad"

def probe_copyright_year():
    return f"{datetime.datetime.now().year}"




