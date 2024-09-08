"""show.py: show() function implementation."""

import tempfile
import platform
import os
import subprocess
import shutil
from pathlib import Path

import raimad as rai

def is_linux():
    return platform.system() == "Linux"

def is_native_klayout_installed():
    return bool(shutil.which('klayout'))

def is_flatpak_installed():
    return bool(shutil.which('flatpak'))

def is_flatpak_klayout_installed():
    result = subprocess.run(
        ["flatpak", "list", "--app", "--columns=application"],
        capture_output=True,
        text=True,
        check=True
    )
    return "de.klayout.KLayout" in result.stdout

def get_custom_cifview_command():
    return (
        os.environ.get("RAIMAD_CIF_VIEWER")
        or
        os.environ.get("CIF_VIEWER")
        or
        None
        )

def is_klayout_running():
    if not is_linux():
        raise NotImplementedError(
            "raimad.show() is not available on your platform yet. "
            "Contact maybetree and request support."
            )

    result = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.count("klayout") > 0


def get_cifview_args(file):
    if not is_linux():
        raise NotImplementedError(
            "raimad.show() is not available on your platform yet. "
            "Contact maybetree and request support."
            )

    custom_command = get_custom_cifview_command()
    if custom_command:
        return (
            file if arg == '__FILE__' else arg
            for arg in
            shlex.split(custom_command)
            )

    if is_native_klayout_installed():
        return ("klayout", file)

    if is_flatpak_installed():
        if is_flatpak_klayout_installed():
            return (
                "flatpak",
                "run",
                "--file-forwarding",
                "de.klayout.KLayout",
                "@@",
                file,
                "@@"
                )

    raise Exception(
        'I could not figure out how to show you the CIF file. '
        'Please install KLayout using your system package manager '
        'or flatpak. '
        'To use a different CIF viewer (or KLayout installed at a custom path)'
        'set the following environment variable: '
        'CIF_VIEWER="your_viewer_command __FILE__"'
        )

def show(compo):
    if is_klayout_running():
        print("Klayout already running.")
        return

    file = tempfile.NamedTemporaryFile(
        'w',
        suffix='.cif',
        prefix='RAIMAD-SHOW',
        delete=False
        )

    rai.export_cif(compo, file)

    args = get_cifview_args(file.name)
    print(f"Running {args}...")

    subprocess.Popen(args)

