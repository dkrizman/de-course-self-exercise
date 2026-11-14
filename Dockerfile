FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

RUN uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"