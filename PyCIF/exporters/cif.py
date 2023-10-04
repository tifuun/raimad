"""
Caltech Intermediate Form Exporter.
"""

import numpy as np

import PyCIF as pc
from PyCIF.exporters import argparse_utils

CLI_NAME = 'cif'


def export(stream, component: pc.Component):
    """
    Export CIF file to stream.
    """
    stream.write('(CIF written by CleWin 3.1);\n')
    stream.write('(1 unit = 0.001 micron);\n')
    stream.write('(SRON);\n')
    stream.write('(Sorbonnelaan 2);\n')
    stream.write('(3584 CA  Utrecht);\n')
    stream.write('(Nederland);\n')

    subpolys = sorted(
        component.get_subpolygons(),
        key=lambda subpoly: subpoly.layer
        )

    prev_layer = None
    for subpoly in subpolys:
        if subpoly.layer != prev_layer:
            stream.write(f'L L{subpoly.layer};\n')

        xyarray = subpoly.polygon.get_xyarray()

        if len(xyarray) == 0:
            continue

        stream.write('P ')

        try:
            for point in np.nditer(xyarray):
                point2 = point * 100  # TODO wtf??
                stream.write(f'{point2:9.0f} ')
            stream.write(';\n')

        except Exception as e:
            raise Exception(
                f'Failed to export polygon {subpoly}. ',
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
    export(args.output_file, component)

