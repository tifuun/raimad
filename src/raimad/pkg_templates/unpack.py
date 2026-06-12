"""unpack.py: utilities for unpacking pkg template dict into file hierarchy."""

from pathlib import Path
from string import Template
from raimad.pkg_templates.types import UserInput, Context, Fillable, Tree
from raimad.pkg_templates.prompt import prompt
from raimad.pkg_templates import probe
from raimad.pkg_templates.default import template_default

def hydrate(user_input: UserInput) -> Context:
    """Convert UserInput to Context, filling in additional fields using."""
    return Context(
        pkg_name=user_input.pkg_name,
        pkg_desc=user_input.pkg_desc,
        author_name=user_input.author_name,
        author_email=user_input.author_email,

        raimad_dep=probe.probe_raimad_dep(),
        copyright_year=probe.probe_copyright_year(),

        compo_camel=user_input.compo_camel,
        compo_snake=user_input.compo_snake,
        )

def fill(fillable: Fillable, context: Context) -> str:
    """
    Format template with context, if it is a template.

    Parameters
    ----------
    fillable: Fillable
        String or template. String will be returned verbatim.
        Template will be formatted with `context.

    context: Context
        Template context.

    Returns
    -------
    str
        If a string was passed as input, it will be returned unchanged.
        Otherwise, the result of formatting `fillable` with `context`
        will be returned.
    """
    if isinstance(fillable, str):
        return fillable
    elif isinstance(fillable, Template):
        return fillable.substitute(**context.__dict__)

def unpack(basepath: Path, template: Tree, context: Context) -> None:
    """
    Format package template with context and unpack into file hierarchy.

    Parameters
    ----------
    basepath: Path
        Path to root of package.
        Parents do not have to exist necessarily.

    template: Tree
        dict describing file hierarchy

    context: Context
        Context dataclass used to fill in the template strings in `template`.
    """
    for name, val in template.items():
        name = fill(name, context)
        if isinstance(val, Fillable):
            val = fill(val, context)
            basepath.mkdir(exist_ok=True, parents=True)
            (basepath / name).write_text(val)
        elif isinstance(val, dict):
            unpack(basepath / name, val, context)
        else:
            raise TypeError()

def doit() -> None:
    """Prompt user for package details and create package file hierarchy."""
    user_input = prompt()
    context = hydrate(user_input)
    unpack(Path(user_input.path), template_default, context)

