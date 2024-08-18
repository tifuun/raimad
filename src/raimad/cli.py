"""RAIMAD Command-line interface (CLI)."""

import argparse
from typing import Sequence

import raimad as rai

ACTION_EXPORT = 'export'
FILE_STDOUT = '-'

def cli(custom_args: Sequence[str] | None = None) -> None:
    """Parse command line arguments and execute the desired action."""
    parser = _setup_parser()
    if custom_args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(custom_args)

    if args.action == ACTION_EXPORT:
        _process_args(args)
        compo = args.component()

        rai.export_cif(compo, args.output_file)

    else:
        # This should never happen, since
        # argparse validates this.
        parser.error('Unknown action')

def _setup_parser() -> argparse.ArgumentParser:
    """Create the root parser for the CLI interface."""
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

def _add_export_action(
        # Can someone explain to me what this generic actually does
        # and why it crashes if it's not quoted?
        subparsers: 'argparse._SubParsersAction[argparse.ArgumentParser]'
        ) -> None:
    """
    Add the export action to the root parser.

    For now, this is the only action
    """
    parser = subparsers.add_parser(
        ACTION_EXPORT,
        help=(
            "Export a component to disk"
            )
        )

    parser.add_argument(
        'component',
        type=lambda string: rai.string_import(string, multiple=False),
        help=(
            'Component to export in the format '
            '`{dot-separated path to module}:{class name}`. '
            'For example, `raimad:Snowman`.'
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
            ),
        default='{name}.cif',
        )


def _process_args(args: argparse.Namespace) -> None:
    args.output_file = args.output_file.replace(
        '{name}',
        args.component.__name__
        )

