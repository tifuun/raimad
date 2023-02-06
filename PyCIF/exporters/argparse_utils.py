"""
argparse-related shorthands.
"""

import argparse
from PyCIF.misc.import_from_string import import_from_string


def arg_output_file(parser):
    """
    Add an output filename argument.
    """
    parser.add_argument(
        '--output-file',
        '-o',
        type=argparse.FileType('w', encoding='utf-8'),
        help='Output file. Use `-` for stdout.',
        default='-',
        )


def arg_component(parser):
    """
    Add an argument for specifying the compoent
    in uvicorn import_fom_string notation.
    """
    parser.add_argument(
        'component',
        type=import_from_string,
        help='Component to export. {Path to module}:{Object name}',
        )


