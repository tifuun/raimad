import unittest
import tempfile
import shlex
import os
from io import StringIO
from contextlib import redirect_stderr

import pycif as pc
from pycif import cli

log = pc.get_logger(__name__)

class TestExportSvg(unittest.TestCase):

    def test_export_svg_cli_guess_format(self):

        stream = StringIO()
        with self.assertRaises(SystemExit) as _, redirect_stderr(stream):
            cli.cli(shlex.split(''))

        string = stream.getvalue()
        self.assertIn('Unknown action', string)

