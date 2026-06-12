#from raimad.pkg_templates.default import template_default
from pathlib import Path
from string import Template
from raimad.pkg_templates.types import UserInput, Context, Fillable, Tree
from raimad.pkg_templates.prompt import prompt
from raimad.pkg_templates import probe
from raimad.pkg_templates.default import template_default

def hydrate(user_input: UserInput) -> Context:
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
    if isinstance(fillable, str):
        return fillable
    elif isinstance(fillable, Template):
        return fillable.substitute(**context.__dict__)

def unpack(basepath: Path, template: Tree, context: Context) -> None:
    # TODO check that already exists
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
    user_input = prompt()
    context = hydrate(user_input)
    unpack(Path(user_input.path), template_default, context)

