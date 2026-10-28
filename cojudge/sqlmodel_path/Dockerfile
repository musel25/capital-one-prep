# The Python image digest is the stock image on the existing ARM VPS.
FROM python@sha256:b7a9e5f6a93d6d4a31f129bbd4bdee69efccb6ded0fb230d78aafaf37af98377
COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /usr/local/bin/uv
RUN apt-get update && apt-get install -y --no-install-recommends time \
    && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock /opt/sqlmodel-course/
ENV UV_PYTHON_DOWNLOADS=never
RUN uv sync --frozen --no-dev --project /opt/sqlmodel-course
ENV PATH="/opt/sqlmodel-course/.venv/bin:$PATH"
ENV PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
WORKDIR /app
