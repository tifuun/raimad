import unittest
import tempfile
import shlex
import os
from io import StringIO

import pycif as pc
from pycif import cli

log = pc.get_logger(__name__)

class TestExportCif(unittest.TestCase):
    def test_export_cif_py_string(self):
        compo = pc.Snowman()

        string = pc.export_cif(compo)

        num_polys = string.count('P')
        self.assertEqual(num_polys, 6)

    def test_export_cif_py_stream(self):
        compo = pc.Snowman()

        stream = StringIO()
        pc.export_cif(compo, stream)
        string = stream.getvalue()

        num_polys = string.count('P')
        self.assertEqual(num_polys, 6)

    def test_export_cif_py_file(self):
        compo = pc.Snowman()

        with tempfile.TemporaryFile('w+') as file:
            pc.export_cif(compo, file)
            file.seek(0)
            string = file.read()

        num_polys = string.count('P')
        self.assertEqual(num_polys, 6)

    def test_export_cif_cli_guess_format(self):
        with tempfile.NamedTemporaryFile(
                'w',
                suffix=f'.{cli.FORMAT_CIF}',
                delete=False,
                ) as file:

            path = file.name

        cli.cli(shlex.split(f'export pycif:Snowman -o "{path}"'))

        with open(path, 'r') as file:
            string = file.read()

        num_polys = string.count('P')
        self.assertEqual(num_polys, 6)

    def test_export_cif_cli_guess_filename(self):
        with tempfile.TemporaryDirectory(delete=True) as folder:

            os.chdir(folder)
            cli.cli(shlex.split('export pycif:Snowman --format cif'))

            with open('Snowman.cif', 'r') as file:
                string = file.read()

        num_polys = string.count('P')
        self.assertEqual(num_polys, 6)

