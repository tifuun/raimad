"""
Caltech Intermediate Form Exporter.
"""

import numpy as np

from PyCIF.draw.Component import Component
from PyCIF.exporters import argparse_utils

CLI_NAME = 'cif'


def export(stream, component: Component):
    """
    Export CIF file to stream.
    """
    stream.write('(CIF written by CleWin 3.1);\n')
    stream.write('(1 unit = 0.001 micron);\n')
    stream.write('(SRON);\n')
    stream.write('(Sorbonnelaan 2);\n')
    stream.write('(3584 CA  Utrecht);\n')
    stream.write('(Nederland);\n')

    for layer_name, polys in component.get_polygons().items():
        layer_index = component.layerspecs[layer_name].index
        stream.write(f'L L{layer_index};\n')
        for poly in polys:
            if len(poly.xyarray) == 0:
                continue

            stream.write('P ')

            try:
                for point in np.nditer(poly.xyarray):
                    point2 = point * 100  # TODO wtf??
                    stream.write(f'{point2:9.0f} ')
                stream.write(';\n')

            except Exception as e:
                raise Exception(
                    f'Failed to export polygon {poly}. ',
                    ) from e

    stream.write('E\n')


def create_parser_options(parser):
    """
    Add options to argparse parser to invoke this exporter
    """
    argparse_utils.arg_output_file(parser)
    argparse_utils.arg_component(parser)


def run_cli(args):
    component = args.component()
    component.make()
    export(args.output_file, component)

