"""Types for package template system."""

from dataclasses import dataclass
from typing import TypeAlias
from string import Template

Fillable: TypeAlias = str | Template
Tree: TypeAlias = 'dict[Fillable, Fillable | Tree]'

@dataclass
class UserInput:
    """Info received from user."""

    pkg_name:     str
    pkg_desc:     str
    author_name:  str
    author_email: str
    compo_pascal:  str
    compo_snake:  str
    path:         str


@dataclass
class Context:
    """Full context needed to fill in template."""

    pkg_name:       str
    pkg_desc:       str
    author_name:    str
    author_email:   str
    raimad_dep:     str
    copyright_year: str
    compo_pascal:    str
    compo_snake:    str
    path:           str

