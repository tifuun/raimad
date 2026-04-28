#!/bin/sh

set -e

wget \
	"https://raw.githubusercontent.com/KLayout/klayout/refs/heads/master/src/laybasic/laybasic/layDitherPattern.cc" \
	-O reference/vendor/klayout/layDitherPattern.cc

wget \
	"https://raw.githubusercontent.com/KLayout/klayout/refs/heads/master/src/laybasic/laybasic/layLineStyles.cc" \
	-O reference/vendor/klayout/layLineStyles.cc

wget \
	"https://raw.githubusercontent.com/KLayout/klayout/refs/heads/master/LICENSE" \
	-O reference/vendor/klayout/LICENSE

echo SUCCESS
