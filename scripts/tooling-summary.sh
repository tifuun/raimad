#!/bin/sh

eecho() { echo "$@" >&2 ; }
pecho() { printf '%s' "$*" ; }

set -e

echo > /tmp/raimad-tooling

export "PYTHONPATH=$PYTHONPATH:$PWD"
py_main=/venv$PYTHON_MAIN/bin/python3

run_tests() {
	for python in $PYTHONS
	do
		if "/venv$python/bin/python3" -m unittest 1>&2
		then
			echo "TOOLING_UNITTEST_$python=true  # Did unittests pass?" >> /tmp/raimad-tooling
		else
			echo "TOOLING_UNITTEST_$python=false  # Did unittests pass?" >> /tmp/raimad-tooling
		fi
	done
}

run_mypy() {
	if $py_main -m mypy 1>&2
	then
		echo "TOOLING_MYPY=true  # Were there NO mypy issues?" >> /tmp/raimad-tooling
	else
		echo "TOOLING_MYPY=false  # Were there NO mypy issues?" >> /tmp/raimad-tooling
	fi
}


run_coverage() {
	$py_main -m coverage run -m unittest 1>&2
	coverage_percent=$($py_main -m coverage json -q -o /dev/stdout -i | jq --raw-output '.totals.percent_covered_display')

	echo "TOOLING_COVERAGE=$coverage_percent  # Percentage of codebase covered by tests" >> /tmp/raimad-tooling
}

run_count_todos() {
	num_todos=$(
		find . \
			-name '__pycache__' -prune -o \
			-name '.git' -prune -o \
			-name 'dist' -prune -o \
			-name '*egg*info*' -prune -o \
			-name 'archive' -prune -o \
			-type f -exec grep -Eo "TODO|FIXME" {} \; | wc -l)

	echo "TOOLING_TODOS=$num_todos  # How many TODOs and FIXMEs are in the code?" >> /tmp/raimad-tooling
}

run_ruff() {
	# FIXME horrible screenscraping gymnastics
	ruff_output=$($py_main -m ruff check | tail -n 3 | sed '/^\s*$/d')

	eecho "tail of ruff output:"
	eecho "$ruff_output"

	case "$ruff_output" in
		*Found*)
			ruff_issues=$(pecho "$ruff_output" | grep 'Found' | tr -cd 0-9)
			;;
		*passed*)
			ruff_issues=0
			;;
		*)
			ruff_issues='??'
			;;
	esac

	echo "TOOLING_RUFF=$ruff_issues  # How many issues reported by ruff?" >> /tmp/raimad-tooling
}

run_all() {
	run_tests
	run_mypy
	run_coverage
	run_count_todos
	run_ruff
}

if [ -z "$1" ]
then
	run_all
else
	"$@"
fi

cat /tmp/raimad-tooling

