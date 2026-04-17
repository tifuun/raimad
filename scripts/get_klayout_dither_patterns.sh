#!/bin/sh

wget \
	"https://raw.githubusercontent.com/KLayout/klayout/refs/heads/master/src/laybasic/laybasic/layDitherPattern.cc" \
	-O vendor/klayout/layDitherPattern.cc

wget \
	"https://raw.githubusercontent.com/KLayout/klayout/refs/heads/master/src/laybasic/laybasic/layLineStyles.cc" \
	-O vendor/klayout/layLineStyles.cc

