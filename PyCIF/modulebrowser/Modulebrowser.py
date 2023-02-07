"""
Module browser.

makes it easy to look through existing modules
"""
from typing import Type, List
from importlib.resources import read_text
from importlib.resources import files as package_files
from importlib.resources import as_file as traversable_as_file
import inspect
from string import Template
from pathlib import Path
from dataclasses import dataclass, field
import sys
import shutil

import jinja2

from PyCIF.draw.Component import Component
from PyCIF.exporters.svg import export as svgexport
from PyCIF.modulebrowser.themes import FirstLight


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
        svgexport(svgfile, compo)

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


def generate_multi_package_entries(packages, path: Path):

    html_compos = []

    for package in packages:
        Compos = package.pc_export_components
        interface_db = generate_interface_db(Compos)
        for Compo in Compos:
            html_compo = generate_entry(Compo, path, interface_db)
            html_compos.append(html_compo)

    html = format_resource(
        'index.html',
        components='\n'.join(html_compos),
        )

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


@dataclass
class ComponentEntry(object):
    """
    Entry for a component in the modulebrowser database.
    """

    interfaces: List[Component] = field(
        default_factory=lambda: [],
        )


@dataclass
class CTXOption(object):
    """
    jinja2 context for a componenent option.
    """

    name: str
    default_value: str
    description: str
    shadow: bool


@dataclass
class CTXLayer(object):
    """
    jinja2 context for a componenent layer.
    """

    name: str


@dataclass
class CTXInterface(object):
    """
    jinja2 context for a component interface.
    """

    name: str


@dataclass
class CTXComponent(object):
    """
    jinja2 context for a component.
    """

    name: str
    fancy_name: str
    module_name: str
    author: str
    description: str
    options: List[CTXOption]
    layers: List[CTXLayer]
    interfaces: List[CTXInterface]


class Modulebrowser(object):
    def __init__(self):
        self.components = {}

    def register_component(self, new_compo):
        """
        Add new component to database
        """
        new_entry = ComponentEntry()
        for existing_compo, existing_entry in self.components.items():

            if existing_compo.is_interface(new_compo):
                new_entry.interfaces.append(existing_compo)

            elif new_compo.is_interface(existing_compo):
                existing_entry.interfaces.append(new_compo)

        self.components[new_compo] = new_entry

    def register_package(self, package):
        """
        Add new package into database
        """
        for compo in package.PC_EXPORT_COMPONENTS:
            self.register_component(compo)

    def _generate_component_context(self, compo):
        """
        Generate jinja2 context for one component
        """
        entry = self.components[compo]
        module = inspect.getmodule(compo)

        return CTXComponent(
            name=compo.__name__,
            fancy_name=compo.__doc__.split('\n')[1],
            module_name=module.__name__,
            author=sys.modules[module.__package__].__author__,
            description='\n'.join(compo.__doc__.split('\n')[2:]),
            options=[
                CTXOption(
                    name=name,
                    default_value=optspec.default,
                    description=optspec.desc,
                    shadow=optspec.shadow,
                    )
                for name, optspec in compo.optspecs.items()
                ],
            layers=[
                CTXLayer(
                    name=layerspec.fancy_name or name,
                    )
                for name, layerspec in compo.layerspecs.items()
                ],
            interfaces=[
                CTXInterface(
                    name=interface.__name__,
                    )
                for interface in entry.interfaces
                ],
            )

    def _generate_context(self):
        """
        Generate jinja2 context from database
        """
        return {
            'components': [
                self._generate_component_context(compo)
                for compo in self.components.keys()
                ],
            }

    def _copy_basedir(self, path: Path):
        """
        Move static files (basedir) from theme into target path
        """
        # FIXME this won't work if the package is installed as a zip,
        # it think.
        theme = FirstLight
        shutil.rmtree(path, ignore_errors=True)
        shutil.copytree(
            package_files(theme) / 'basedir',
            path,
            )

    def _generate_preview_image(self, path: Path, compo):
        """
        Generate preview images for component
        """
        instance = compo()
        instance.make()

        compo_path = path / 'components' / compo.__name__
        compo_path.mkdir()
        svg_path = compo_path / 'preview.svg'

        with svg_path.open('w') as svgfile:
            svgexport(svgfile, instance)

    def _generate_preview_images(self, path: Path):
        """
        Generate preview images for all components in database
        """
        (path / 'components').mkdir()
        for compo in self.components.keys():
            self._generate_preview_image(path, compo)

    def generate_html(self, path: Path):
        self._copy_basedir(path)
        self._generate_preview_images(path)

        context = self._generate_context()
        theme = FirstLight
        env = jinja2.Environment(autoescape=True)
        template = env.from_string(read_text(theme, 'index.html'))
        (path / 'index.html').write_text(template.render(context))


def test_theme(path: Path):
    compos = [
        {
            'name': 'test1',
            'fancy_name': 'Test Component 1',
            'modulename': 'testmodule',
            'author': 'Asuka Langley Soryu',
            'description': 'Test test test McTestyFace',
            'options': [
                {
                    'name': 'snorkub',
                    'default_value': '100',
                    'description': 'Snorkface combobulation index',
                    'shadow': True,
                },
                {
                    'name': 'proj_scatter',
                    'default_value': '0.0054',
                    'description': 'Projection scattering coefficient',
                },
                {
                    'name': 'height',
                    'default_value': '25',
                    'description': 'Height of main resonator beam',
                },
                ],
            'layers': [
                {'name': 'layer1'},
                {'name': 'layer2'},
                {'name': 'layer3'},
                ],
            'interfaces': [
                {'name': 'test2'},
                ],
        },
        {
            'name': 'test2',
            'fancy_name': 'Test Component 2',
            'modulename': 'testmodule',
            'author': 'Ikari Shinji',
            'description': 'Test test test McTestyFace',
            'options': [
                {
                    'name': 'snorkub',
                    'default_value': '100',
                    'description': 'Snorkface combobulation index',
                },
                {
                    'name': 'proj_scatter',
                    'default_value': '0.0054',
                    'description': 'Projection scattering coefficient',
                    'shadow': True,
                },
                {
                    'name': 'height',
                    'default_value': '25',
                    'description': 'Height of main resonator beam',
                    'shadow': True,
                },
                ],
            'layers': [
                {'name': 'layer1'},
                {'name': 'layer2'},
                {'name': 'layer3'},
                ],
            'interfaces': [
                {'name': 'test2'},
                ],
        },
        {
            'name': 'test3',
            'fancy_name': 'Super Amazing Test Component',
            'modulename': 'some_other_testmodule',
            'author': 'Ayanami Rei',
            'description': 'Lorem Ipsum Dolor Sit Amet',
            'options': [
                {
                    'name': 'snorkub',
                    'default_value': '100',
                    'description': 'Snorkface combobulation index',
                    'shadow': False,
                },
                ],
            'layers': [
                {'name': 'layer1'},
                {'name': 'layer2'},
                {'name': 'layer3'},
                ],
            'interfaces': [
                {'name': 'test2'},
                ],
        },
        ]

    context = {
        'components': compos,
        }

    theme = FirstLight
    env = jinja2.Environment(autoescape=True)
    template = env.from_string(read_text(theme, 'index.html'))
    (path / 'index.html').write_text(template.render(context))

