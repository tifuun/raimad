"""
Test the `init` cli action (create new package from template)
"""

import os
import sys
import subprocess
import unittest
import tempfile
from pathlib import Path
from typing import Sequence, cast

import raimad as rai
from raimad.pkg_templates import validators
from raimad.pkg_templates.prompt import pascal2snake

def spawn_python(
        args: Sequence[str],
        cwd: str | Path,
        pythonpath: Sequence[str] | None = None,
        ) -> subprocess.Popen[str]:
        # the [str] generic means the Popen is in text mode
        # (`text=True`)
    """Spawn new Python with subprocess.Popen"""

    env = {}

    if pythonpath is not None:
        env['PYTHONPATH'] = ':'.join((
            *os.environ.get('PYTHONPATH', ()),
            *pythonpath
        ))

    return subprocess.Popen(
        (sys.executable, *args),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        universal_newlines=True,  # TODO needed?
        cwd=cwd,
        env=env,
    )

def send_lines(
        p: subprocess.Popen[str],
        lines: Sequence[str]
        ) -> tuple[str, str]:
    # extra empty string at the end so there's a trailing newline
    stdout, stderr = p.communicate('\n'.join((*lines, '')))
    return stdout, stderr

class TestTemplate(unittest.TestCase):

    def _run_wizard(self, folder: Path, user_input: Sequence[str]) -> None:
        """Run `raimad init` with custom input."""
        p = spawn_python(('-m', 'raimad', 'init'), folder)
        send_lines(p, user_input)
        self.assertEqual(p.returncode, 0)

    def _run_package_tests(self, folder: Path) -> None:
        """Run `python -m unittest` in a folder."""
        p = spawn_python(
            ('-m', 'unittest'),
            folder,
            pythonpath = ('./src', )   # <- make package `import`able
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertTrue('OK' in stderr)


    def test_template_happy_path(self):
        """Test happy user path of creating new package."""
        with tempfile.TemporaryDirectory() as tmpfolder:
            folder = Path(tmpfolder)

            self._run_wizard(folder, (
                "rai_testpkg",             # package name
                "./testpkg",               # path
                "This is a test package",  # description
                "Foo Barr",                # author
                "foo@barr.com",            # email
                "FooBarrCompo",            # pascal
                "",                        # snake (use default)
            ))
            self._run_package_tests(folder / 'testpkg')


    def test_template_default_path(self):
        """Test that all default values of template wizard work."""
        with tempfile.TemporaryDirectory() as tmpfolder:
            folder = Path(tmpfolder)

            self._run_wizard(folder, (
                "",  # package name
                "",  # path
                "",  # description
                "",  # author
                "",  # email
                "",  # pascal
                "",  # snake
            ))
            self._run_package_tests(folder / 'rai_mypkg')

    def test_validator_pascal_case(self):
        """Test PascalCase validator for template user input."""
        self.assertTrue(validators.compo_pascal("Foobar")[0])
        self.assertTrue(validators.compo_pascal("Foo")[0])
        self.assertTrue(validators.compo_pascal("Fo")[0])
        self.assertTrue(validators.compo_pascal("FoFoFo")[0])
        self.assertTrue(validators.compo_pascal("AShapedFilter")[0])
        self.assertTrue(validators.compo_pascal("ACRONYMTail")[0])
        self.assertTrue(validators.compo_pascal("SomethingE")[0])
        self.assertTrue(validators.compo_pascal("SomethingEEEEE")[0])
        self.assertTrue(validators.compo_pascal("Something1312")[0])
        self.assertTrue(validators.compo_pascal("Some23Thing")[0])
        self.assertTrue(validators.compo_pascal("Foo2Bar2")[0])
        self.assertTrue(validators.compo_pascal("Maru9")[0])
        self.assertTrue(validators.compo_pascal("M9")[0])

        self.assertFalse(validators.compo_pascal("f")[0])
        self.assertFalse(validators.compo_pascal("fffff")[0])
        self.assertFalse(validators.compo_pascal("fffFfff")[0])
        self.assertFalse(validators.compo_pascal("fFF")[0])
        self.assertFalse(validators.compo_pascal("snake_case")[0])
        self.assertFalse(validators.compo_pascal("kebab-case")[0])
        self.assertFalse(validators.compo_pascal("PascalCasent_")[0])
        self.assertFalse(validators.compo_pascal("")[0])
        self.assertFalse(validators.compo_pascal("-")[0])
        self.assertFalse(validators.compo_pascal("something1312")[0])
        # Some people say the below should be valid. Not me.
        self.assertFalse(validators.compo_pascal("Some23thing")[0])
        self.assertFalse(validators.compo_pascal("2Foo2Bar")[0])
        self.assertFalse(validators.compo_pascal("99999")[0])
        self.assertFalse(validators.compo_pascal("9")[0])
        self.assertFalse(validators.compo_pascal("m9")[0])

        # deliberate non-tests
        #
        # self.assert?????(validators.compo_pascal("F")[0])

    def test_pascal2snake(self):
        """Test pascal2snake function from template prompt module."""
        self.assertEqual(pascal2snake("Foobar"),         "foobar")
        self.assertEqual(pascal2snake("Foo"),            "foo")
        self.assertEqual(pascal2snake("Fo"),             "fo")
        self.assertEqual(pascal2snake("FoFoFo"),         "fo_fo_fo")
        self.assertEqual(pascal2snake("AShapedFilter"),  "a_shaped_filter")
        self.assertEqual(pascal2snake("ACRONYMTail"),    "acronym_tail")
        self.assertEqual(pascal2snake("SomethingE"),     "something_e")
        self.assertEqual(pascal2snake("SomethingEEEEE"), "something_eeeee")
        self.assertEqual(pascal2snake("Something1312"),  "something1312")
        self.assertEqual(pascal2snake("Some23Thing"),    "some23_thing")
        self.assertEqual(pascal2snake("Foo2Bar2"),       "foo2_bar2")
        self.assertEqual(pascal2snake("Maru9"),          "maru9")
        self.assertEqual(pascal2snake("M9"),             "m9")
        self.assertEqual(pascal2snake("A999a"),          "a999a")
        self.assertEqual(pascal2snake("A999"),           "a999")



if __name__ == '__main__':
    unittest.main()

