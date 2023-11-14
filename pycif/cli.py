"""
cli.py: Command-line interface to pycif.

cli.py -- defines cli(),
a function for handling command line invocation
for things like exporting designs,
generating modulebrowser,
etc.
"""

import argparse
from pathlib import Path
from sys import stdout

import pycif
from pycif.helpers.import_from_string import import_from_string

ACTION_EXPORT = 'export'
FORMATS = (  # These MUST be lowercase!
    FORMAT_CIF := 'cif',
    FORMAT_SVG := 'svg',
    FORMAT_BROWSER := 'pycif-browser',
    )

def cli(custom_args = None):

    parser = _setup_parser()
    args = parser.parse_args(*[custom_args])
    _process_args(args)

    compo = args.component()

    if args.action == ACTION_EXPORT:
        if args.format == FORMAT_CIF:
            pycif.export_cif(compo, args.output_file)

        elif args.format == FORMAT_SVG:
            pycif.export_svg(compo, args.output_file)

        elif args.format == FORMAT_BROWSER:
            NotImplemented

        else:
            # This should never happen, since
            # argparse validates this.
            parser.error('Unknown format')

    else:
        # This should never happen, since
        # argparse validates this.
        parser.error('Unknown action')

def _setup_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

    subparsers = parser.add_subparsers(
        title='Action',
        dest='action',
        description='Which action to perform',
        )

    _add_export_action(subparsers)

    return parser

def _add_export_action(subparsers):
    parser = subparsers.add_parser(
        ACTION_EXPORT,
        help=(
            "Export a component to disk"
            )
        )

    parser.add_argument(
        'component',
        type=import_from_string,
        help=(
            'Component to export in the format '
            '`{dot-separated path to module}:{Object name}`. '
            'For example, `pycif:Snowman`.'
            )
        )

    parser.add_argument(
        '--output-file',
        '-o',
        type=str,
        nargs='?',
        help=(
            'Output file. Use `-` for stdout. '
            '`{name}` will get formatted with component name. '
            'Extension is used to guess format.'
            ),
        default='{name}.cif',
        )

    parser.add_argument(
        '--format',
        '-f',
        type=str,
        choices=FORMATS,
        nargs='?',
        help=(
            'Output format. '
            'If not given, guess from extension of output file. '
            'If output file is `-` (stdout), cif format is assumed. '
            ),
        )

def _process_args(args):
    if args.output_file == '-':
        args.output_file = stdout
        if not args.format:
            args.format = FORMAT_CIF

    else:
        args.output_file = args.output_file.replace(
            '{name}',
            args.component.__name__
            )

    if not args.format:
        lower = args.output_file.lower()
        for fmt in FORMATS:
            if lower.endswith(f'.{fmt}'):
                args.format = fmt
                break
        else:
            raise Exception(
                "Could not determine format from filename."
                )

