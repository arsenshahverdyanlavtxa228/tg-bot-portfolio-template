## Builder — installs deps into a venv we can copy into a slim runtime.
FROM python:3.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System deps kept to a minimum. gcc only needed if a dep compiles C extensions.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --upgrade pip \
    && pip install .

## Runtime — no build tools, non-root user.
FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DATABASE_URL="sqlite+aiosqlite:////app/data/bot.db" \
    MEDIA_DIR="/app/media"

RUN groupadd --system bot && useradd --system --gid bot --home /app bot \
    && mkdir -p /app/data /app/media \
    && chown -R bot:bot /app

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --chown=bot:bot src ./src

USER bot

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

CMD ["python", "-m", "bot"]
