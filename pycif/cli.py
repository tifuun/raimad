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
    )
FILE_STDOUT = '-'

def cli(custom_args=None):

    parser = _setup_parser()
    args = parser.parse_args(*[custom_args])
    _process_args(args)

    compo = args.component()

    if args.action == ACTION_EXPORT:
        if args.format == FORMAT_CIF:
            pycif.export_cif(compo, args.output_file)

        elif args.format == FORMAT_SVG:
            pycif.export_svg(compo, args.output_file)

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
            f'Output file. Use `{FILE_STDOUT}` for stdout. '
            '`{name}` will get formatted with component name. '
            '`{format}` will get formatted with the specified format '
            '(cif by default). '
            ),
        default='{name}.{format}',
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
            f'If output file not given or `{FILE_STDOUT}` (stdout), '
            'cif format is assumed. '
            ),
        )

def guess_format(args):
    if args.format:
        return args.format

    if args.output_file == FILE_STDOUT:
        return FORMAT_CIF

    lower = args.output_file.lower()
    for fmt in FORMATS:
        if lower.endswith(f'.{fmt}'):
            return fmt

    raise Exception(
        "Could not determine format from filename."
        )

def guess_file(args, fmt):
    if args.output_file == FILE_STDOUT:
        return stdout

    return (
        args.output_file
        .replace(
            '{name}',
            args.component.__name__
            )
        .replace(
            '{format}',
            fmt
            )
        )


def _process_args(args):

    fmt = guess_format(args)
    file = guess_file(args, fmt)
    args.output_file = file
    args.format = fmt


