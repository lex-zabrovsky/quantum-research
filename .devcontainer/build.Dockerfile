ARG base_tag=bookworm
ARG base_img=mcr.microsoft.com/vscode/devcontainers/base:dev-${base_tag}

FROM --platform=linux/amd64 ${base_img} AS builder-install

RUN apt-get update --fix-missing && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
    curl \
    locales \
    wget \
    python3 && \
    rm -rf /var/lib/apt/lists/*

ENV UV_INSTALL_DIR=/usr/local/bin
RUN wget -qO- https://astral.sh/uv/install.sh | sh

WORKDIR /app

COPY pyproject.toml ./

RUN uv sync