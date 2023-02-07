"""
cli.py -- defines cli(),
a function for handling command line invocation
for things like exporting designs,
generating modulebrowser,
etc.
"""

import argparse

from PyCIF import exporters


def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

    subparsers = parser.add_subparsers(
        title='Action',
        dest='action',
        description='Which action to perform',
        )

    parser_export = subparsers.add_parser(
        'export',
        )

    subparsers_export = parser_export.add_subparsers(
        title='Export',
        dest='exporter',
        description='Export component to CAD file',
        )

    for exporter in exporters.CLI_EXPORTERS:
        add_exporter_parser(subparsers_export, exporter)

    args = parser.parse_args()

    if args.action == 'export':
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


def add_exporter_parser(subparsers, exporter):
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
