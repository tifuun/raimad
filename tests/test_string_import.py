"""
Test `rai.string_import` method,
a function that taskes a string in the format
{period-separated modules}.{class name}
and imports the corresponding RAIMAD component class
"""

import unittest
from pathlib import Path
import os
import tempfile
import sys

import raimad as rai

class TestStringImport(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.snowman_cif = rai.export_cif(rai.Snowman())

    def test_string_import_single(self):
        """
        Test importing a single component
        """
        self.assertIs(
            rai.Snowman,
            rai.string_import('raimad:Snowman', multiple=False)
            )

    def test_string_import_multiple(self):
        """
        Test importing all components from a module
        """
        # Dear future maintainer:
        # if you added a new built-in component to RAIMAD
        # and this test started failing,
        # just add your new component to the list below
        self.assertEqual(
            {
                rai.Snowman,
                rai.AnSec,
                rai.RectLW,
                rai.Circle,
                rai.RectWire,
                rai.CustomPoly,
                },
            set(
                rai.string_import('raimad', multiple=True)
                )
            )

    def test_string_import_single_fail_compo(self):
        """
        Test that the correct error is thrown importing a component that
        doesn't exist
        """
        with self.assertRaises(rai.err.StringImportError):
            rai.string_import('raimad:ComponentDoesNotExist')

    def test_string_import_single_fail_module(self):
        """
        Test that the correct error is thrown importing a component from
        a module that does not exist
        """
        with self.assertRaises(rai.err.StringImportError):
            rai.string_import('module_does_not_exist:Snowman')

    def test_string_import_single_fail_multiple(self):
        """
        Test that the correct error is thrown when you try
        to import multiple components with `multiple=False`
        """
        with self.assertRaises(rai.err.StringImportError):
            rai.string_import('raimad')

    def test_string_import_single_as_multiple(self):
        """
        Test that no error is thrown is `multiple=False`,
        and the string imports all components from a module,
        but the module has only one component.
        """
        with tempfile.TemporaryDirectory() as folder:
            os.chdir(folder)
            # This test will break pycoverage,
            # because pycoverage will think that `mymodule`
            # is a real module that needs evaluating,
            # but can't find its source.
            # Run pycoverage with `-i` flag.
            Path('mymodule.py').write_text(
                "import raimad as rai\n"
                "\n"
                "class MyCompo(rai.Compo):\n"
                "    def _make(self):\n"
                "        pass"
                )

            # Add the temporary directory to sys.path
            # so that the import machinery
            # can see `mymodule.py`
            sys.path.insert(0, folder)

            compo = rai.string_import("mymodule", multiple=False)

            # remove the temporary directory from sys.path
            # to avoid weirdness down the line.
            sys.path.pop(0)

            self.assertTrue(issubclass(compo, rai.Compo))


if __name__ == '__main__':
    unittest.main()

