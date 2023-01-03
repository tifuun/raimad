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


def generate_interface_db(component_list: List[Type[Component]]):
    """
    Generate a dict mapping components to a set of their interfaces
    """
    return {
        Compo: {
            Interface
            for Interface in component_list
            if Interface.is_interface(Compo)
            }
        for Compo in component_list
        #if not Compo.is_interface()
        }


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


def generate_entry(Compo: Type[Component], path: Path, interface_db):
    module = inspect.getmodule(Compo)
    name = Compo.__name__
    fancy_name = Compo.__doc__.split('\n')[1]
    description = '\n'.join(Compo.__doc__.split('\n')[2:])
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

        num_options=len([1 for spec in Compo.optspecs.values() if not spec.shadow]),
        num_layers=len(Compo.layerspecs),
        num_interfaces=len(interface_db[Compo]),

        options_plural='s' * (len([1 for spec in Compo.optspecs.values() if not spec.shadow]) != 1),
        layers_plural='s' * (len(Compo.layerspecs) != 1),
        interfaces_plural='s' * (len(interface_db[Compo]) != 1),

        options='\n'.join([
            format_resource(
                'option.html',
                name=name,
                value=optspec.default,
                description=optspec.desc,
                shadow='shadow' * optspec.shadow,
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

        interfaces='\n'.join([
            format_resource(
                'interface.html',
                name=interface.__name__,
                )
            for interface in interface_db[Compo]
            ]),

        modulename=module.__name__,
        )

    return html_compo


def generate_entries(Compos: List[Type[Component]], path: Path):
    html_compos = []
    interface_db = generate_interface_db(Compos)
    for Compo in Compos:
        html_compo = generate_entry(Compo, path, interface_db)
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


