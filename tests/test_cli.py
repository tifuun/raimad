import unittest
from contextlib import redirect_stderr
import shlex
import os
import subprocess
from io import StringIO
import tempfile
from pathlib import Path

import raimad as rai

class TestCLI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.snowman_cif = rai.export_cif(rai.Snowman())

    def test_cli_export_cif_noargs(self):
        with tempfile.TemporaryDirectory(delete=True) as folder:
            os.chdir(folder)
            subprocess.run(shlex.split(
                'python -m raimad export raimad:Snowman'
                ), check=True)

            cif_string = Path('Snowman.cif').read_text()

        self.assertEqual(self.snowman_cif, cif_string)

    def test_cli_export_cif_file(self):
        with tempfile.TemporaryDirectory(delete=True) as folder:
            os.chdir(folder)
            subprocess.run(shlex.split(
                'python -m raimad export raimad:Snowman -o compo.cif'
                ), check=True)

            cif_string = Path('compo.cif').read_text()

        self.assertEqual(self.snowman_cif, cif_string)

# TODO other formats? svg?

if __name__ == '__main__':
    unittest.main()

