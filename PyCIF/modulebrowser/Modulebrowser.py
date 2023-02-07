"""
Module browser.

makes it easy to look through existing modules
"""
from typing import Type, List
from importlib.resources import read_text
from importlib.resources import files as package_files
from importlib.resources import as_file as traversable_as_file
import inspect
from pathlib import Path
from dataclasses import dataclass, field
import sys
import shutil

import jinja2

from PyCIF.draw.Component import Component
from PyCIF.exporters.svg import export as svgexport
from PyCIF.modulebrowser.themes import FirstLight


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

