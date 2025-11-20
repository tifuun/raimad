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
        self.rectlw_cif = rai.export_cif(rai.RectLW(420, 6.9))
        self.rectlw_defaults_cif = rai.export_cif(rai.RectLW(
            length=rai.RectLW.Options.length.browser_default,
            width=rai.RectLW.Options.width.browser_default,
            ))
        self.rectlw_defaults_override_cif = rai.export_cif(rai.RectLW(
            length=rai.RectLW.Options.length.browser_default,
            width=6.9,
            ))

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

    def test_cli_export_opts(self):
        pwd = os.getcwd()
        with tempfile.TemporaryDirectory() as folder:
            os.chdir(folder)
            subprocess.run(shlex.split(
                f'''
                    {sys.executable} -m raimad export
                    raimad:RectLW
                    -o compo.cif
                    --opts length 420 width 6.9
                '''), check=True)

            cif_string = Path('compo.cif').read_text()
        os.chdir(pwd)

        self.assertEqual(self.rectlw_cif, cif_string)

    def test_cli_export_opts_dict(self):
        pwd = os.getcwd()
        with tempfile.TemporaryDirectory() as folder:
            os.chdir(folder)
            subprocess.run(
                [
                    f"{sys.executable}", "-m", "raimad", "export",
                    "raimad:RectLW",
                    "-o", "compo.cif",
                    "--opts-dict", "{'length': 420, 'width': 6.9}",
                    ],
                check=True
                )

            cif_string = Path('compo.cif').read_text()
        os.chdir(pwd)

        self.assertEqual(self.rectlw_cif, cif_string)

    def test_cli_export_opts_json(self):
        pwd = os.getcwd()
        with tempfile.TemporaryDirectory() as folder:
            os.chdir(folder)
            subprocess.run(
                [
                    f"{sys.executable}", "-m", "raimad", "export",
                    "raimad:RectLW",
                    "-o", "compo.cif",
                    "--opts-json", '{"length": 420, "width": 6.9}',
                    ],
                check=True
                )

            cif_string = Path('compo.cif').read_text()
        os.chdir(pwd)

        self.assertEqual(self.rectlw_cif, cif_string)

    def test_cli_export_browser_defaults(self):
        pwd = os.getcwd()
        with tempfile.TemporaryDirectory() as folder:
            os.chdir(folder)
            subprocess.run(shlex.split(
                f'''
                    {sys.executable} -m raimad export
                    raimad:RectLW
                    -o compo.cif
                    --use-browser-defaults
                '''), check=True)

            cif_string = Path('compo.cif').read_text()
        os.chdir(pwd)

        self.assertEqual(self.rectlw_defaults_cif, cif_string)

    def test_cli_export_browser_defaults_override(self):
        pwd = os.getcwd()
        with tempfile.TemporaryDirectory() as folder:
            os.chdir(folder)
            subprocess.run(shlex.split(
                f'''
                    {sys.executable} -m raimad export
                    raimad:RectLW
                    -o compo.cif
                    --use-browser-defaults
                    --opts width 6.9
                '''), check=True)

            cif_string = Path('compo.cif').read_text()
        os.chdir(pwd)

        self.assertEqual(self.rectlw_defaults_override_cif, cif_string)

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

