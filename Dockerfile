FROM ghcr.io/void-linux/void-glibc

# KEEP IN SYNC WITH THE WGET LINES BELOW
ARG PYTHONS="3.14 3.13 3.12 3.11 3.10"

# Which python to use for extended tooling? 
# coverage, ruff, mypy
ARG PYTHON_MAIN="3.13"

RUN \
	--mount=type=cache,target=/root/.cache/pip \
	--mount=type=cache,target=/var/cache/xbps \
	\
	`#install documentation too for interactive use` \
	set -e && \
	rm -rf /etc/xbps.d/noextract.conf && \
	xbps-install -Syu xbps && \
	xbps-install -Syu \
		man \
		wget \
		jq \
		xtools `xdowngrade command` \
		`python deps` \
		libffi \
		sqlite \
		&& \
	wget https://github.com/stratal-systems/freshsnakes-void/releases/download/v4/freshsnakes-python3.10-3.10.20_1.x86_64.xbps && \
	wget https://github.com/stratal-systems/freshsnakes-void/releases/download/v4/freshsnakes-python3.11-3.11.15_1.x86_64.xbps && \
	wget https://github.com/stratal-systems/freshsnakes-void/releases/download/v4/freshsnakes-python3.12-3.12.9_1.x86_64.xbps && \
	wget https://github.com/stratal-systems/freshsnakes-void/releases/download/v4/freshsnakes-python3.13-3.13.14_1.x86_64.xbps && \
	wget https://github.com/stratal-systems/freshsnakes-void/releases/download/v4/freshsnakes-python3.14-3.14.6_1.x86_64.xbps && \
	ls *.xbps | xargs -n 1 xdowngrade && \
	for python in $PYTHONS ; do \
		echo '' | xdowngrade ./freshsnakes-python$python*.xbps | cat && \
		rm ./freshsnakes-python$python*.xbps && \
		/opt/freshsnakes-python$python/bin/python3 -m venv /venv$python && \
		: ; \
	done && \
	/venv$PYTHON_MAIN/bin/pip install coverage mypy ruff twine build && \
	:

COPY . /raimad-source

RUN \
	--mount=type=cache,target=/root/.cache/pip \
	--mount=type=cache,target=/var/cache/xbps \
	\
	for python in $PYTHONS ; do \
		/venv$python/bin/pip install -e /raimad-source[dev] && \
		: ; \
	done && \
	:


ENV PYTHONS=${PYTHONS}
ENV PYTHON_MAIN=${PYTHON_MAIN}
WORKDIR /raimad-source
CMD ["./scripts/tooling-summary.sh"]

