import unittest
from contextlib import redirect_stderr
import shlex
import os
import subprocess
from io import StringIO
import tempfile
import random
import sys
from pathlib import Path

import raimad as rai

class TestCLI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.snowman_cif = rai.export_cif(rai.Snowman())

    def test_cli_export_cif_noargs(self):
        pwd = os.getcwd()
        with tempfile.TemporaryDirectory() as folder:
            os.chdir(folder)
            subprocess.run(shlex.split(
                f'{sys.executable} -m raimad export raimad:Snowman'
                ), check=True)

            cif_string = Path('Snowman.cif').read_text()
        os.chdir(pwd)

        self.assertEqual(self.snowman_cif, cif_string)

    def test_cli_export_cif_file(self):
        pwd = os.getcwd()
        with tempfile.TemporaryDirectory() as folder:
            os.chdir(folder)
            subprocess.run(shlex.split(
                f'{sys.executable} -m raimad export raimad:Snowman -o compo.cif'
                ), check=True)

            cif_string = Path('compo.cif').read_text()
        os.chdir(pwd)

        self.assertEqual(self.snowman_cif, cif_string)

    def test_cli_fortune(self):
        result = subprocess.run(shlex.split(
            f'{sys.executable} -m raimad fortune'
            ),
            check=True,
            capture_output=True,
            )

        fortune = result.stdout.decode('utf-8')
        self.assertIn(
            fortune.strip(),
            map(lambda s: s.strip(), rai.fortunes_all)
            )

    def test_cli_fortune_category(self):
        result = subprocess.run(shlex.split(
            f'{sys.executable} -m raimad fortune resilience'
            ),
            check=True,
            capture_output=True,
            )

        fortune = result.stdout.decode('utf-8')
        self.assertIn(
            fortune.strip(),
            map(lambda s: s.strip(), rai.fortunes_resilience)
            )
        self.assertNotIn(
            fortune.strip(),
            map(lambda s: s.strip(), rai.fortunes_politics)
            )

# TODO other formats? svg?

if __name__ == '__main__':
    unittest.main()

