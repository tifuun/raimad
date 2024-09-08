"""show.py: show() function implementation."""

import tempfile
import platform
import os
import subprocess
import shutil
import shlex
from pathlib import Path

import sys

import raimad as rai

def is_native_klayout_installed() -> bool:
    """Check whether KLayout is installed and available from the terminal."""
    return bool(shutil.which('klayout'))

def is_klayout_installed_win() -> bool:
    appdata = os.getenv('APPDATA')
    return Path(rf"{appdata}\KLayout\klayout_app.exe").exists()

def is_flatpak_installed() -> bool:
    """Check whether Flatpak is installed."""
    return bool(shutil.which('flatpak'))

def is_flatpak_klayout_installed() -> bool:
    """Checked whether KLayout is installed via flatpak."""
    result = subprocess.run(
        ["flatpak", "list", "--app", "--columns=application"],
        capture_output=True,
        text=True,
        check=True
    )
    return "de.klayout.KLayout" in result.stdout

def get_custom_cifview_command() -> str | None:
    """Check if an env variable set that specifies a custom CIF viewer."""
    return (
        os.environ.get("RAIMAD_CIF_VIEWER")
        or
        os.environ.get("CIF_VIEWER")
        or
        None
        )

def is_klayout_running() -> bool:
    """Check whether klayout is already running."""

    if platform.system() == "Linux":
        return subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True,
            check=True
            ).stdout.count("klayout") > 0

    elif platform.system() == "Windows":
        return subprocess.run(
            ["tasklist"],
            capture_output=True,
            text=True,
            check=True
            ).stdout.count("kalyout_app.exe") > 0

    raise NotImplementedError(
        "raimad.show() is not available on your platform yet. "
        "Contact maybetree and request support."
        )


def get_cifview_args(file: str) -> tuple[str, ...]:
    """Get a command to open `file` in a CIF viewer."""

    custom_command = get_custom_cifview_command()
    if custom_command:
        return tuple(
            file if arg == '__FILE__' else arg
            for arg in
            shlex.split(custom_command)
            )

    if platform.system() == "Linux":
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
            'To use a different CIF viewer '
            '(or KLayout installed at a custom path) '
            'set the following environment variable: '
            'CIF_VIEWER="your_viewer_program __FILE__". '
            )

    elif platform.system() == "Windows":
        if is_klayout_installed_win():
            appdata = os.getenv('APPDATA')
            return (
                rf"{appdata}\KLayout\klayout_app.exe",
                file,
                )

        raise Exception(
            'I could not figure out how to show you the CIF file. '
            'Please install KLayout. '
            'Is KLayout already installed at a non-standard path, '
            'or would you like to use a different CIF viewer? '
            'Then set the following environment variable: '
            'CIF_VIEWER="your_viewer_program __FILE__". '
            )


    raise NotImplementedError(
        "raimad.show() is not available on your platform yet. "
        "Contact maybetree and request support."
        )


def show(compo: 'rai.typing.CompoLike', ignore_running: bool = False) -> None:
    """Export `compo` and open it in a CIF viewer."""

    file = Path(tempfile.gettempdir()) / "RAIMAD-SHOW.cif"
    rai.export_cif(compo, file)
    print(f"Saved to {file}")

    if not ignore_running and is_klayout_running():
        print("Klayout already running.")
        return

    args = get_cifview_args(str(file))
    print(f"Running {args}...")

    subprocess.Popen(args)

