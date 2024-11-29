"""RAIMAD Command-line interface (CLI)."""

import argparse
from typing import Sequence
import sys
import os

import raimad as rai

ACTION_EXPORT = 'export'
ACTION_SHOW = 'show'
ACTION_FORTUNE = 'fortune'
FILE_STDOUT = '-'

def cli(custom_args: Sequence[str] | None = None) -> None:
    """Parse command line arguments and execute the desired action."""

    ensure_pwd_in_path()

    parser = _setup_parser()

    if custom_args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(custom_args)

    if args.action == ACTION_EXPORT:
        _process_args_export(args)
        compo = args.component()

        rai.export_cif(compo, args.output_file)

    elif args.action == ACTION_SHOW:
        rai.show(args.component(), args.ignore_running)

    elif args.action == ACTION_FORTUNE:
        print(rai.fortune(args.category))

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
    _add_show_action(subparsers)
    _add_fortune_action(subparsers)

    return parser

def _add_export_action(
        # Can someone explain to me what this generic actually does
        # and why it crashes if it's not quoted?
        subparsers: 'argparse._SubParsersAction[argparse.ArgumentParser]'
        ) -> None:
    """Add the export action to the root parser."""
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

def _add_show_action(
        subparsers: 'argparse._SubParsersAction[argparse.ArgumentParser]'
        ) -> None:
    """Add the show action to the root parser."""
    parser = subparsers.add_parser(
        ACTION_SHOW,
        help=(
            "Export a component and open it in a CIF viewer"
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
        '--ignore-running',
        '-i',
        action='store_true',
        help="Launch the CIF viewer again even if it is already running",
        )

def _add_fortune_action(
        subparsers: 'argparse._SubParsersAction[argparse.ArgumentParser]'
        ) -> None:
    """Add the fortune action to the root parser."""
    parser = subparsers.add_parser(
        ACTION_FORTUNE,
        help=(
            "Print a randomly chosen string from RAIMAD's collection "
            "of maxims, one-size-fits-all wisdowms, and questionable "
            "quotations. "
            )
        )

    parser.add_argument(
        'category',
        type=str,
        default='',
        nargs='?',
        help=(
            "Category of fortune. Available categories: "
            "technology, economy, education, politics, engineering, "
            "resilience, misc. "
            "Pass `any`, `all`, or emptystring to select from all "
            "categories. "
            )
        )

def _process_args_export(args: argparse.Namespace) -> None:
    args.output_file = args.output_file.replace(
        '{name}',
        args.component.__name__
        )

def ensure_pwd_in_path() -> None:
    pwd = os.getcwd()
    if pwd not in sys.path:
        sys.path.insert(0, pwd)

