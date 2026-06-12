#from raimad.pkg_templates.default import template_default
from pathlib import Path
from typing import TypeAlias
from string import Template

Fillable: TypeAlias = str | Template
Tree: TypeAlias = 'dict[Fillable, Fillable | Tree]'

def fill(fillable: Fillable):
    if isinstance(fillable, str):
        return fillable
    elif isinstance(fillable, Template):
        return fillable.substitute(
            NAME="samplepackage",
            DESCRIPTION="A package for things and stuff",
            AUTHOR_NAME="Foo Barr",
            AUTHOR_EMAIL="no@email.com",
            RAIMAD_DEP="raimad==1.3.0",
            YEAR="2026",
            COMPO_SNAKE="my_compo",
            COMPO_CAMEL="MyCompo",
            )

def unpack(basepath: Path, template: Tree):
    # TODO check that already exists
    for name, val in template.items():
        name = fill(name)
        if isinstance(val, Fillable):
            val = fill(val)
            basepath.mkdir(exist_ok=True, parents=True)
            (basepath / name).write_text(val)
        elif isinstance(val, dict):
            unpack(basepath / name, val)
        else:
            raise TypeError()

