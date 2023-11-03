"""
cli.py: Command-line interface to PyCIF.

cli.py -- defines cli(),
a function for handling command line invocation
for things like exporting designs,
generating modulebrowser,
etc.
"""

import argparse
from pathlib import Path

from PyCIF import exporters
from PyCIF.helpers.import_from_string import import_package_from_string


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
    _add_modulebrowser_action(subparsers)

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

    elif args.action == 'browser':

        if args.mb_action == 'generate':
            from PyCIF.modulebrowser.Modulebrowser import Modulebrowser
            browser = Modulebrowser()

            for package in args.packages:
                browser.register_package(package)

            browser.generate_html(args.browser_dir)

        elif args.mb_action == 'open':
            import webbrowser
            # Web browser needs to know the absolute path
            index_path = args.browser_dir.resolve() / 'index.html'
            webbrowser.open(f'file://{index_path}')
    else:
        # This should never happen, since
        # argparse validates this.
        parser.error('Unknown action')


def _add_export_action(subparsers):
    """Setup parsers for 'export' action."""
    parser_export = subparsers.add_parser(
        'export',
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


def _add_modulebrowser_action(subparsers):
    """Setup parsers for 'export' action."""
    parser_mb = subparsers.add_parser(
        'browser',
        )

    subparsers_mb = parser_mb.add_subparsers(
        title='Modulebrowser Action',
        dest='mb_action',
        description='Modulebrowser action',
        )

    parser_mb_gen = subparsers_mb.add_parser(
        'generate',
        )

    parser_mb_gen.add_argument(
        'packages',
        nargs='+',
        help='List of packages to include',
        type=import_package_from_string,
        )

    parser_mb_gen.add_argument(
        '--browser-dir',
        '-d',
        type=Path,
        help='Output directory',
        default='./module_browser',
        )

    parser_mb_open = subparsers_mb.add_parser(
        'open',
        )

    parser_mb_open.add_argument(
        '--browser-dir',
        '-d',
        type=Path,
        help='Module browser directory',
        default='./module_browser',
        )

