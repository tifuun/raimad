import unittest
import tempfile
import shlex
import os
from io import StringIO
from contextlib import redirect_stderr

import pycif as pc
from pycif import cli

log = pc.get_logger(__name__)

class TestCLI(unittest.TestCase):

    def test_cli_no_args(self):

        stream = StringIO()
        with self.assertRaises(SystemExit) as _, redirect_stderr(stream):
            cli.cli(shlex.split(''))

        string = stream.getvalue()
        self.assertIn('Unknown action', string)

    def test_cli_export_no_args(self):

        stream = StringIO()
        with self.assertRaises(SystemExit) as _, redirect_stderr(stream):
            cli.cli(shlex.split('export'))

        string = stream.getvalue()
        self.assertIn('arguments are required', string)

    def test_cli_invalid_action(self):

        stream = StringIO()
        with self.assertRaises(SystemExit) as _, redirect_stderr(stream):
            cli.cli(shlex.split('invalidenfnkjqfewnq'))

        string = stream.getvalue()
        self.assertIn('invalid choice', string)

    def test_cli_invalid_format(self):

        with self.assertRaises(pc.err.UnknownFormatError):
            cli.cli(shlex.split('export pycif:Snowman -o invalid.invalid'))

    def test_cli_invalid_component(self):

        with self.assertRaises(pc.err.ImportFromStringError):
            cli.cli(shlex.split('export pycif:Snowma'))

