#!/bin/sh

export DOCKER_HOST=unix://${XDG_RUNTIME_DIR}/docker.sock
docker pull openjournals/inara

