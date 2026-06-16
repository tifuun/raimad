"""Utilities for prompting user for input for package template system."""

import re

from raimad.pkg_templates.types import UserInput, Context
from raimad.pkg_templates import validators
from raimad.pkg_templates.validators import Validator
from raimad.pkg_templates import probe

def pascal2snake(pascal: str) -> str:
    """Translate PascalCase name to snake_case."""
    result = re.sub(
        r"([A-Z]*)([A-Z]|$)",
        lambda m: ''.join(f"_{f.lower()}" for f in m.groups() if f),
        pascal,
        ).strip('_')
    assert result.lower() == result
    return result

def pester(name: str, default: str, validator: Validator) -> str:
    """
    Keep on asking user for input until `validator` is satisfied.

    Parameters
    ----------
    name : str
        Name of the field (displayed in the `input` prompt)
    default : str
        Default value. Displayed in the `input` prompt line,
        and falls back to this value if user gives
        empty input (i.e. just presses enter key)
    validator: Validator
        Function that checks user input string
        and returns `bool`, `str` tuple
        indicating whether it's okay or not,
        and why.

    Returns
    -------
    str
        Either the user input that satisfied the validator
        or `default`.
    """
    last_input = None
    while True:
        user_input = input(f"{name} [{default}]: ") or default
        is_ok, reason = validator(user_input)

        if last_input is not None and user_input.strip() in {'`!`', '!'}:
            print(
                f'Using invalid value `{last_input}` anyway, '
                'expect breakage!'
                )
            user_input = last_input
            break

        if is_ok:
            if reason:
                print(reason)
            break

        print(f'Invalid input: {reason} Enter `!` to override.')
        print()
        last_input = user_input

    print()
    return user_input

def prompt() -> UserInput:
    """
    Ask user all questions needed to build package boilerplate.

    Returns
    -------
    UserInput
        UserInput dataclass with all answers.
    """
    # TODO nicer output on keyboardinterrupt
    print()
    print("Welcome to the RAIMAD package creator wizard!")
    print("You will be prompted to enter the following details: ")
    print()
    print("- Package name and description")
    print("- Author (that's you!) name and email address")
    print("- A single component name")
    print()
    print("For each entry, you can press Enter ")
    print("to accept the [default value].")
    print("Press Ctrl-C at any time to quit.")
    print()
    pkg_name = pester(
        "Package name",
        "rai_mypkg",
        validators.pkg_name,
        )
    print("Enter path to the package directory to be created.")
    print()
    path = pester(
        "Path",
        f"./{pkg_name}",
        validators.path,
        )
    pkg_desc = pester(
        "Package description",
        "My RAIMAD Package",
        validators.pkg_desc,
        )
    author_name = pester(
        "Author name",
        probe.probe_author_name(),
        lambda _: (True, ""),
        )
    author_email = pester(
        "Author email address",
        "noemail@example.com",
        validators.author_email
        )
    print("I will create one sample component in your package.")
    print("Enter the component name in PascalCase.")
    print("This is how your component will appear to users of your package.")
    print()
    compo_pascal = pester(
        "Component name (PascalCase)",
        "MyCompo",
        validators.compo_pascal,
        )
    print("Enter the name of your component in snake_case.")
    print("This is used for the filename containing the component code.")
    print()
    compo_snake = pester(
        "Component name (snake_case)",
        pascal2snake(compo_pascal),
        validators.compo_snake
        )

    return UserInput(
        pkg_name=pkg_name,
        pkg_desc=pkg_desc,
        author_name=author_name,
        author_email=author_email,
        compo_pascal=compo_pascal,
        compo_snake=compo_snake,
        path=path,
        )

def postunpack(ctx: Context) -> None:
    """Print some text after unpacking template."""

    print()
    print(f"Successfully created new RAIMAD package at `{ctx.path}`.")
    print("Files of interest:")
    print(f" - `{ctx.path}/pyproject.toml` -- package metadata")
    print(f" - `{ctx.path}/src/{ctx.compo_snake}.py` -- component source code")
    print(
        f" - `{ctx.path}/src/{ctx.pkg_name}/{ctx.compo_snake}.py`"
        " -- component source code"
    )
    print(
        f" - `{ctx.path}/src/{ctx.pkg_name}/__init__.py`"
        "-- namespace flattening"
    )
    print()
    print("The package has been initialised with the ")
    print("GNU General Public License Version 3 Only.")
    print("You may choose a different license by editing ")
    print("`pyproject.toml`, `README.md`, and `LICENSE.md`.")
    print()
    print("Good luck!")
    print()

