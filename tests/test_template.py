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


if __name__ == '__main__':
    unittest.main()

