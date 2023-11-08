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

from pycif import exporters
from pycif.helpers.import_from_string import import_package_from_string

ACTION_EXPORT = 'export'

def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

    subparsers = parser.add_subparsers(
        title='Action',
        dest='action',
        description='Which action to perform',
        )

    _add_export_action(subparsers)

    args = parser.parse_args()

    if args.action == ACTION_EXPORT:
        for exporter in exporters.CLI_EXPORTERS:
            if args.exporter == exporter.CLI_NAME:
                exporter.run_cli(args)
                break
        else:
            # This should never happen, since
            # argparse validates this.
            parser.error('Unknown exporter')

    else:
        # This should never happen, since
        # argparse validates this.
        parser.error('Unknown action')


def _add_export_action(subparsers):
    """Setup parsers for 'export' action."""
    parser_export = subparsers.add_parser(
        ACTION_EXPORT,
        )

    subparsers_export = parser_export.add_subparsers(
        title='Export',
        dest='exporter',
        description='Export component to CAD file',
        )

    for exporter in exporters.CLI_EXPORTERS:
        _add_exporter_parser(subparsers_export, exporter)


def _add_exporter_parser(subparsers, exporter):
    """
    Add a parser for a given exporter.

    This generates a new parser based on the parser's
    module name and docstring,
    then calls the module's add_parser() method
    to configure parameters.
    """
    parser = subparsers.add_parser(
        exporter.CLI_NAME,
        description=exporter.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

    exporter.create_parser_options(parser)

