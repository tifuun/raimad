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
                "FooBarrCompo",            # camel
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
                "",  # camel
                "",  # snake
            ))
            self._run_package_tests(folder / 'rai_mypkg')

    def test_validator_camel_case(self):
        """Test CamelCase validator for template user input."""
        self.assertTrue(validators.compo_camel("Foobar")[0])
        self.assertTrue(validators.compo_camel("Foo")[0])
        self.assertTrue(validators.compo_camel("Fo")[0])
        self.assertTrue(validators.compo_camel("FoFoFo")[0])
        self.assertTrue(validators.compo_camel("AShapedFilter")[0])
        self.assertTrue(validators.compo_camel("ACRONYMTail")[0])
        self.assertTrue(validators.compo_camel("SomethingE")[0])
        self.assertTrue(validators.compo_camel("SomethingEEEEE")[0])
        self.assertTrue(validators.compo_camel("Something1312")[0])
        self.assertTrue(validators.compo_camel("Some23Thing")[0])
        self.assertTrue(validators.compo_camel("Foo2Bar2")[0])
        self.assertTrue(validators.compo_camel("Maru9")[0])
        self.assertTrue(validators.compo_camel("M9")[0])

        self.assertFalse(validators.compo_camel("f")[0])
        self.assertFalse(validators.compo_camel("fffff")[0])
        self.assertFalse(validators.compo_camel("fffFfff")[0])
        self.assertFalse(validators.compo_camel("fFF")[0])
        self.assertFalse(validators.compo_camel("snake_case")[0])
        self.assertFalse(validators.compo_camel("kebab-case")[0])
        self.assertFalse(validators.compo_camel("CamelCasent_")[0])
        self.assertFalse(validators.compo_camel("")[0])
        self.assertFalse(validators.compo_camel("-")[0])
        self.assertFalse(validators.compo_camel("something1312")[0])
        # Some people say the below should be valid. Not me.
        self.assertFalse(validators.compo_camel("Some23thing")[0])
        self.assertFalse(validators.compo_camel("2Foo2Bar")[0])
        self.assertFalse(validators.compo_camel("99999")[0])
        self.assertFalse(validators.compo_camel("9")[0])
        self.assertFalse(validators.compo_camel("m9")[0])

        # deliberate non-tests
        #
        # self.assert?????(validators.compo_camel("F")[0])



if __name__ == '__main__':
    unittest.main()

