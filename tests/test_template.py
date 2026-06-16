"""
Test the `init` cli action (create new package template)
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

    def test_template_happy_path(self):
        with tempfile.TemporaryDirectory() as tmpfolder:
            folder = Path(tmpfolder)

            # Part one: run the interactive wizard

            p = spawn_python(('-m', 'raimad', 'init'), folder)
            send_lines(p, (
                "rai_testpkg",             # package name
                "./testpkg",               # path
                "This is a test package",  # description
                "Foo Barr",                # author
                "foo@barr.com",            # email
                "FooBarrCompo",            # camel
                "",                        # snake (use default)
            ))
            self.assertEqual(p.returncode, 0)

            # Part two: run autogenned package's unittest

            p = spawn_python(
                ('-m', 'unittest'),
                folder / 'testpkg',  # <- cd into package root
                pythonpath = ('./src', )   # <- make package `import`able
            )
            stdout, stderr = p.communicate()
            self.assertEqual(p.returncode, 0)
            self.assertTrue('OK' in stderr)


if __name__ == '__main__':
    unittest.main()

