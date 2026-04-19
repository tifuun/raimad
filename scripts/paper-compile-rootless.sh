#!/bin/sh

export DOCKER_HOST=unix://${XDG_RUNTIME_DIR}/docker.sock

docker run --rm \
    --volume $PWD/paper:/data \
    `#--user $(id -u):$(id -g)` \
    --env JOURNAL=joss \
    openjournals/inara

