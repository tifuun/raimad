"""
Module browser
makes it easy to look through existing modules
"""
from typing import Type, List
import inspect

from pathlib import Path

from PyClewinSDC.Component import Component
from PyClewinSDC.exporters.SVGExporter import SVGExporter

compo_template = """\
<div class="component" id="__NAME__">
    <div class="component-left">
        Preview:
        <br />
        <img width="99px" src="components/__NAME__/preview.svg" class="preview" id="__NAME__-preview" / >
    </div>
    <div class="component-right">
        <div class="component-title">
            <h1>__FANCY_NAME__</h1>
            Author: __AUTHOR__
            Package: __PACKAGE__
            Name in code: __NAME__
        </div>
        <div class="component-blurb">
            __BLURB__
        </div>
        <div class="component-opts">
            Options:
            <ul>
            __OPTS__
            </ul>
        </div>
        <div class="component-layers">
            Layers:
            <ul>
            </ul>
        </div>
        <div class="component-howtoget">
            How to get: __HOWTOGET__
        </div>
    </div>
</div>
"""

html_template = """\
<!DOCTYPE html>
<html>
    <head>
        <style>
            .component {
                margin-left: 10%;
                margin-bottom: 10px;
                margin-top: 10px;
                border: 4px solid black;
                width: 80%;
                background-color: #8888ff;
                padding: 20px;
                float: left;
            }
            .component-left {
                width: 20%;
                float: left;
            }
            .component-right {
                width: 80%;
                float: left;
            }
            .component-title {
                width: 99%;
                background-color: #88ff88;
            }
            .component-blurb {
                width: 99%;
                background-color: #ffffff;
            }
            .component-opts {
                width: 99%;
                background-color: #aaaaaa;
            }
        </style>
    </head>
    <body>
        __BODY__
    </body>
</html>
"""


def generate_entry(Compo: Type[Component], path: Path):
    name = Compo.__name__
    fancy_name = Compo.__doc__.split('\n')[1]
    blurb = '\n'.join(Compo.__doc__.split('\n')[2:])
    howtoget = Compo.modulebrowser_howtoget or \
        f"from {inspect.getmodule(Compo).__name__} import {Compo.__name__}"

    opts_list = '\n'.join([
        f'<li><strike><b>{name}</b> = {spec.default}: <i>{spec.desc}</i></strike></li>'
        if spec.shadow else
        f'<li><b>{name}</b> = {spec.default}: <i>{spec.desc}</i></li>'
        for name, spec in Compo.optspecs.items()
        ])

    compo_path = path / 'components' / name
    compo_path.mkdir(parents=True, exist_ok=True)

    compo = Compo()
    compo.make()

    with (compo_path / 'preview.svg').open('w') as svgfile:
        SVGExporter(svgfile, compo)

    html_compo = (compo_template
        ).replace('__NAME__', name
        ).replace('__FANCY_NAME__', fancy_name
        ).replace('__BLURB__', blurb
        ).replace('__OPTS__', opts_list
        ).replace('__LAYERS__', ''
        ).replace('__HOWTOGET__', howtoget
        )

    return html_compo


def generate_entries(Compos: List[Type[Component]], path: Path):
    html_compos = []
    for Compo in Compos:
        html_compo = generate_entry(Compo, path)
        html_compos.append(html_compo)

    html = html_template.replace('__BODY__', '\n'.join(html_compos))
    return html


def generate_package_entries(package, path: Path):
    html = generate_entries(package.pc_export_components, path)
    html = (html
        ).replace('__AUTHOR__', package.__author__
        ).replace('__PACKAGE__', package.__name__
        )
    (path / 'index.html').write_text(html)


