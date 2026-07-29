#!/bin/sh

set -e

echo > /tmp/raimad-tooling

export "PYTHONPATH=$PYTHONPATH:$PWD"
py_main=/venv$PYTHON_MAIN/bin/python3

for python in $PYTHONS
do
	if "/venv$python/bin/python3" -m unittest 1>&2
	then
		echo "TOOLING_UNITTEST_$python=true  # Did unittests pass?" >> /tmp/raimad-tooling
	else
		echo "TOOLING_UNITTEST_$python=false  # Did unittests pass?" >> /tmp/raimad-tooling
	fi
done

if $py_main -m mypy 1>&2
then
	echo "TOOLING_MYPY=true  # Were there NO mypy issues?" >> /tmp/raimad-tooling
else
	echo "TOOLING_MYPY=false  # Were there NO mypy issues?" >> /tmp/raimad-tooling
fi

$py_main -m coverage run -m unittest 1>&2
coverage_percent=$($py_main -m coverage json -q -o /dev/stdout -i | jq --raw-output '.totals.percent_covered_display')

echo "TOOLING_COVERAGE=$coverage_percent  # Percentage of codebase covered by tests" >> /tmp/raimad-tooling

num_todos=$(
	find . \
		-name '__pycache__' -prune -o \
		-name '.git' -prune -o \
		-name 'dist' -prune -o \
		-name '*egg*info*' -prune -o \
		-name 'archive' -prune -o \
		-type f -exec grep -Eo "TODO|FIXME" {} \; | wc -l)

echo "TOOLING_TODOS=$num_todos  # How many TODOs and FIXMEs are in the code?" >> /tmp/raimad-tooling

# FIXME horrible screenscraping gymnastics
ruff_issues=$($py_main -m ruff check | tail -n 3 | grep 'Found' | tr -cd 0-9)

echo "TOOLING_RUFF=$ruff_issues  # How many issues reported by ruff?" >> /tmp/raimad-tooling

cat /tmp/raimad-tooling

