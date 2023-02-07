"""
setup.py -- setuptools metadata.

This file is needed to tell setuptools (an underlying compoent of pip)
about PyCIF.
"""

__version__ = '0.0.0'
__author__ = 'Nikita Soshnin'
__email__ = 'N.A.Soshnin@student.tudelft.nl'
__license__ = "I haven't decided yet"

import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name='PyCIF',
    version=__version__,
    description=
        'Collaborative CAD Platform for hierarchical '
        'design of on-chip imaging devices',
    long_description=README,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__email__,
    classifiers=[
        'Programming Language :: Python :: 3',
        ],
    packages=setuptools.find_packages(),
    python_requires='>=3',
    install_requires=[
        ],
    extras_require={
        'modulebrowser': [
            'jinja2==3.1.2',
            ],
        },
)
