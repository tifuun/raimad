# pycif

pycif: Collaborative CAD platform for hierarchical design of on-chip imaging devices

![DeshimaDemo screenshot](img/DeshimaDemo.png)

## Documentation
You can read the (work-in-progress) documentation on Gitlab Pages:
https://pycif-doc-exp-ast-9eaacae6a67b6164b16cb406c607dd46952114ff89777.gitlab.io/

Unfortunately,
TU Delft's Gitlab instance [disables](https://tu-delft-dcc.github.io/infrastructure/gitlab/gitlab_intro.html#:~:text=Hosting%20a%20website%20through%20pages%20is%20currently%20deactivated)
 <sup>[archived](https://web.archive.org/web/20231104192845/https://tu-delft-dcc.github.io/infrastructure/gitlab/gitlab_intro.html#:~:text=Hosting%20a%20website%20through%20pages%20is%20currently%20deactivated)</sup>
the Pages feature,
so instead we use the public instance at gitlab.com
to host the Pages site.

The source code for the documentation is available at
https://gitlab.tudelft.nl/exp-ast/pycif-doc/

## Installing

Since the TU Delft gitlab is password-protected,
`pip` will ask you to log in.
If you haven't already,
create an access token with `read` permissions from the Gitlab webui.
When pip asks for credentials,
use your netid as the username
and the token as the password.

```bash
pip install git+https://gitlab.tudelft.nl/exp-ast/pycif
```

## Installing in development mode

Installing in editable/development mode will allow you to
edit pycif source code
and have the changes be immediately available,
without having to reinstall every time.

When cloning this repo
make sure that the name of the folder it gets cloned into
is different to the name of the package (i.e. `pycif`),
since that could cause issues.
The check is case-sensitive,
so something like
`pycif` should be fine.

```bash
# Clone this repo
git clone https://gitlab.tudelft.nl/exp-ast/pycif

# Install in development mode
pip install -e ./pycif
```

## Examples

Make sure pycif works by compiling the built-in Snowman component:

```bash
python -m pycif export cif pycif:Snowman -o snowman.cif
```

Want a more *involved* example? Check out [DeshimaDemo](https://gitlab.tudelft.nl/exp-ast/pc_deshimademo)!

