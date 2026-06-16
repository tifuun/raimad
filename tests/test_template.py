"""
Test the `init` cli action (create new package template)
"""

import os
import sys
import subprocess
import unittest
import tempfile
from pathlib import Path

import raimad as rai

class TestTemplate(unittest.TestCase):
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)

    #    self.snowman_cif = rai.export_cif(rai.Snowman())
    #    self.rectlw_cif = rai.export_cif(rai.RectLW(420, 6.9))
    #    self.rectlw_defaults_cif = rai.export_cif(rai.RectLW(
    #        length=rai.RectLW.Options.length.browser_default,
    #        width=rai.RectLW.Options.width.browser_default,
    #        ))
    #    self.rectlw_defaults_override_cif = rai.export_cif(rai.RectLW(
    #        length=rai.RectLW.Options.length.browser_default,
    #        width=6.9,
    #        ))

    def test_template_happy_path(self):
        with tempfile.TemporaryDirectory() as folder:

            # Part one: run the interactive wizard

            p = subprocess.Popen(
                (sys.executable, '-m', 'raimad', 'init'),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=folder,
            )

            stdout, stderr = p.communicate("""\
rai_testpkg
./testpkg
This is a test package
Foo Barr
foo@barr.com
FooBarrCompo

""")

            self.assertEqual(p.returncode, 0)

            # Part two: run autogenned package's unittest

            p = subprocess.Popen(
                (sys.executable, '-m', 'unittest'),
                cwd=Path(folder) / 'testpkg',
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env={
                    'PYTHONPATH':
                    ':'.join((
                        *os.environ.get('PYTHONPATH', ()),
                        './src'
                    ))
                }
            )

            stdout, stderr = p.communicate()

            self.assertTrue('OK' in stderr)
            self.assertEqual(p.returncode, 0)

            #p = BasicExpect.python_cli('-m unittest')
            # TODO


if __name__ == '__main__':
    unittest.main()

