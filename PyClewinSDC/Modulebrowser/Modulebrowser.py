"""
Module browser
makes it easy to look through existing modules
"""
from typing import Type, List
from importlib.resources import read_text
import inspect
from string import Template

from pathlib import Path

from PyClewinSDC.Component import Component
from PyClewinSDC.exporters.SVGExporter import SVGExporter
from PyClewinSDC.Modulebrowser.themes import FirstLight


def format_string(string, **kwargs):
    """
    Shorthand for formatting a string
    """
    return Template(string).safe_substitute(kwargs)


def format_resource(resource, theme=FirstLight, **kwargs):
    """
    Shorthand for reading a file from a theme and formatting it.
    """
    return Template(read_text(theme, resource)).safe_substitute(kwargs)


def generate_entry(Compo: Type[Component], path: Path):
    name = Compo.__name__
    fancy_name = Compo.__doc__.split('\n')[1]
    description = '\n'.join(Compo.__doc__.split('\n')[2:])
    howtoget = Compo.modulebrowser_howtoget or \
        f"from {inspect.getmodule(Compo).__name__} import {Compo.__name__}"
    #layers = '\n'.join([
    #    f"<li>{layerspec.fancy_name or name}</li>"
    #    for name, layerspec in Compo.layerspecs.items()
    #    ])

    #opts_list = '\n'.join([
    #    f'<li><strike><b>{name}</b> = {spec.default}: <i>{spec.desc}</i></strike></li>'
    #    if spec.shadow else
    #    f'<li><b>{name}</b> = {spec.default}: <i>{spec.desc}</i></li>'
    #    for name, spec in Compo.optspecs.items()
    #    ])

    compo_path = path / 'components' / name
    compo_path.mkdir(parents=True, exist_ok=True)

    compo = Compo()
    compo.make()

    with (compo_path / 'preview.svg').open('w') as svgfile:
        SVGExporter(svgfile, compo)

    html_compo = format_resource(
        'component.html',
        name=name,
        fancy_name=fancy_name,
        description=description,

        num_options=len(Compo.optspecs),
        num_layers=len(Compo.layerspecs),
        num_interfaces=1,

        options_plural='s' * (len(Compo.optspecs) != 1),
        layers_plural='s' * (len(Compo.layerspecs) != 1),
        interfaces_plural='s' * 0,

        options='\n'.join([
            format_resource(
                'option.html',
                name=name,
                value=optspec.default,
                description=optspec.desc,
                )
            for name, optspec in Compo.optspecs.items()
            ]),

        layers='\n'.join([
            format_resource(
                'layer.html',
                name=layerspec.fancy_name or name,
                )
            for name, layerspec in Compo.layerspecs.items()
            ]),

        modulename=inspect.getmodule(Compo).__name__,
        )

    return html_compo


def generate_entries(Compos: List[Type[Component]], path: Path):
    html_compos = []
    for Compo in Compos:
        if Compo.interface_name != Component.interface_name:
            continue
        html_compo = generate_entry(Compo, path)
        html_compos.append(html_compo)

    html = format_resource(
        'index.html',
        components='\n'.join(html_compos),
        )

    return html


def generate_package_entries(package, path: Path):
    html = generate_entries(package.pc_export_components, path)
    html = format_string(
        html,
        author=package.__author__,
        package=package.__name__,
        )
    (path / 'index.html').write_text(html)
    (path / 'style.css').write_text(read_text(FirstLight, 'style.css'))
    (path / 'expand.svg').write_text(read_text(FirstLight, 'expand.svg'))
    (path / 'background-light.svg').write_text(read_text(FirstLight, 'background-light.svg'))
    (path / 'background-dark.svg').write_text(read_text(FirstLight, 'background-dark.svg'))


