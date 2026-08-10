#!/bin/sh

eecho() { echo "$@" >&2 ; }

py_main=/venv$PYTHON_MAIN/bin/python3

eecho "START PYPI SCRIPT!"

# Exit on error
set -e

if [ -z "$PYPI_TOKEN" ]
then
	eecho "NO PYPI TOKEN!!"
	exit 6
fi

rm -rf dist

eecho "BUILDING..."
$py_main -m build

eecho "UPLOADING..."
$py_main -m twine upload \
	--username '__token__' \
	--password "$PYPI_TOKEN" \
	dist/raimad*

eecho "DONE..."

