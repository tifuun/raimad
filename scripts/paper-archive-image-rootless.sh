#!/bin/sh

set -e
export DOCKER_HOST=unix://${XDG_RUNTIME_DIR}/docker.sock

mkdir -p ./archive
docker image save openjournals/inara \
	| zstd --long --adapt --threads=0 --verbose \
	> ./archive/openjournals-inara-$(date -I).tar
git annex add ./archive

