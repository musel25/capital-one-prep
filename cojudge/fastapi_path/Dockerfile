FROM ghcr.io/astral-sh/uv:0.8.22 AS uv
FROM python@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377
COPY --from=uv /uv /usr/local/bin/uv
RUN apt-get update && apt-get install -y --no-install-recommends time \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/fastapi-path
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
ENV PATH="/opt/fastapi-path/.venv/bin:$PATH"
WORKDIR /app
