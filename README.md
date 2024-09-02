# RAIMAD

RAIMAD Astronomical Instrument MAsk Designer

![RAIMAD banner](img/raimad-banner.png)

![Python 3.12 tests badge](https://raw.githubusercontent.com/gist/maybeetree/767d80027892395f1cc61e4829810985/raw/tests312.svg)
![Python 3.11 tests badge](https://raw.githubusercontent.com/gist/maybeetree/767d80027892395f1cc61e4829810985/raw/tests311.svg)
![Python 3.10 tests badge](https://raw.githubusercontent.com/gist/maybeetree/767d80027892395f1cc61e4829810985/raw/tests310.svg)

![MyPy badge](https://raw.githubusercontent.com/gist/maybeetree/767d80027892395f1cc61e4829810985/raw/mypy.svg)
![Coverage badge](https://raw.githubusercontent.com/gist/maybeetree/767d80027892395f1cc61e4829810985/raw/coverage.svg)
![Number of TODOs and FIXMEs](https://raw.githubusercontent.com/gist/maybeetree/767d80027892395f1cc61e4829810985/raw/todo.svg)

Read the documentation at [RAIDOC](https://tifuun.github.io/raidoc/).

Browse RAIMAD packages at [RAIDEX](https://tifuun.github.io/raidex/).

PyPI page: <https://pypi.org/project/raimad/>

## Development

### tooling

We use flake8, mypy, unit tests, and coverage.py to ensure code quality.

- Unit tests can be run with `python -m unittest` from the root of this
    repo.
    Unit tests MUST PASS in all supported python versions.

- Running `mypy --strict src/raimad` from the root of this repo
    with the latest supported version of Python must report no problems.
    mypy problems detected under older versions of Python can be ignored.

    - Only `src/raimad` files need to pass mypy checks.
        Tests and benchmarks are exempt.

- coverage.py can be a good tool for estimating how much of the codebase
    is covered by unit tests. We are aiming for 100% coverage,
    but it is not yet a requirement.
    

## License

RAIMAD is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, version 3 of the License only.

RAIMAD is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
RAIMAD. If not, see <https://www.gnu.org/licenses/>. 

---

Copyright (c) 2024, maybetree.

