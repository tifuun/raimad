import unittest
import tempfile
import shlex
import os
from io import StringIO
from pathlib import Path

import pycif as pc
from pycif import cli

log = pc.get_logger(__name__)

class TestExportSvg(unittest.TestCase):
    def test_export_svg_py_string(self):
        compo = pc.Snowman()

        string = pc.export_svg(compo)

        num_polys = string.count('<polygon')
        self.assertEqual(num_polys, 6)

    def test_export_svg_py_stream(self):
        compo = pc.Snowman()

        stream = StringIO()
        pc.export_svg(compo, stream)
        string = stream.getvalue()

        num_polys = string.count('<polygon')
        self.assertEqual(num_polys, 6)

    def test_export_svg_py_file(self):
        compo = pc.Snowman()

        with tempfile.TemporaryFile('w+') as file:
            pc.export_svg(compo, file)
            file.seek(0)
            string = file.read()

        num_polys = string.count('<polygon')
        self.assertEqual(num_polys, 6)

    def test_export_svg_py_filename(self):
        compo = pc.Snowman()

        with tempfile.NamedTemporaryFile('w', delete=False) as file:
            path = file.name

        pc.export_svg(compo, path)

        string = Path(path).read_text()

        num_polys = string.count('<polygon')
        self.assertEqual(num_polys, 6)

    def test_export_svg_cli_guess_format(self):
        with tempfile.NamedTemporaryFile(
                'w',
                suffix=f'.{cli.FORMAT_SVG}',
                delete=False,
                ) as file:

            path = file.name

        cli.cli(shlex.split(f'export pycif:Snowman -o "{path}"'))

        with open(path, 'r') as file:
            string = file.read()

        num_polys = string.count('<polygon')
        self.assertEqual(num_polys, 6)

    def test_export_svg_cli_guess_filename(self):
        with tempfile.TemporaryDirectory(delete=True) as folder:

            os.chdir(folder)
            cli.cli(shlex.split('export pycif:Snowman --format svg'))

            with open('Snowman.svg', 'r') as file:
                string = file.read()

        num_polys = string.count('<polygon')
        self.assertEqual(num_polys, 6)

    def test_export_svg_compo_repr(self):
        compo = pc.Snowman()
        string = compo._repr_svg_()
        num_polys = string.count('<polygon')
        self.assertEqual(num_polys, 6)

    def test_export_svg_poly_repr(self):
        poly = pc.RectWire(
            pc.Point(0, 0),
            pc.Point(100, 100),
            5,
            )

        string = poly._repr_svg_()
        num_polys = string.count('<polygon')
        self.assertEqual(num_polys, 1)

