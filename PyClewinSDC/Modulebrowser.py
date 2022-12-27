"""
Module browser
makes it easy to look through existing modules
"""
from typing import Type, List

from pathlib import Path

from PyClewinSDC.Component import Component
from PyClewinSDC.exporters.SVGExporter import SVGExporter

compo_template = """\
<div class="component" id="__NAME__">
    <div class="component-left">
        <img width="99px" src="components/__NAME__/preview.svg" class="preview" id="__NAME__-preview" / >
    </div>
    <div class="component-right">
        <div class="component-title">
            <h1>__FANCY_NAME__</h1>
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
    </div>
</div>
"""

html_template = """\
<!DOCTYPE html>
<html>
    <head>
        <style>
            .component {
                width: 50%;
                border: 10px solid black;
                background-color: #8888ff;
                padding: 20px;
                float: left;
            }
            .component-left {
                width: 19%;
                float: left;
            }
            .component-right {
                width: 59%;
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

    opts_list = '\n'.join([
        f'<li>{name} = {default_value}</li>'
        for name, default_value in Compo.default_opts.items()
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
        ).replace('__OPTS__', opts_list)

    return html_compo


def generate_entries(Compos: List[Type[Component]], path: Path):
    html_compos = []
    for Compo in Compos:
        html_compo = generate_entry(Compo, path)
        html_compos.append(html_compo)

    html = html_template.replace('__BODY__', html_compo)
    (path / 'index.html').write_text(html)


