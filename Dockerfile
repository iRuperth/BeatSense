# syntax=docker/dockerfile:1.7
# ---------------------------------------------------------------------------
# BeatSense — single-container Hugging Face Space image
# Runs FastAPI on :8000 (internal) and Next.js on :7860 (public, HF Spaces port)
# Next.js rewrites /api/* -> http://127.0.0.1:8000/*
# ---------------------------------------------------------------------------

# ============================================================================
# Stage 1: build the Next.js frontend (standalone output)
# ============================================================================
FROM node:20-bookworm-slim AS frontend-builder

ENV PNPM_HOME=/pnpm
ENV PATH=$PNPM_HOME:$PATH
RUN corepack enable && corepack prepare pnpm@10 --activate

WORKDIR /app/frontend

# Cache deps
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Build
COPY frontend ./
RUN pnpm build


# ============================================================================
# Stage 2: runtime — Python + FastAPI + Node runtime + Next.js standalone
# ============================================================================
FROM python:3.11-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    NODE_ENV=production \
    PORT=7860 \
    HOSTNAME=0.0.0.0 \
    API_INTERNAL_URL=http://127.0.0.1:8000

# System deps: Node.js (for Next.js standalone), curl (for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# uv for fast Python installs
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /usr/local/bin/uv

# HF Spaces runs containers as a non-root user with UID 1000
RUN useradd -m -u 1000 app
WORKDIR /home/app/code
RUN chown -R app:app /home/app

USER app
ENV HOME=/home/app
ENV PATH="/home/app/.local/bin:$PATH"

# ---- Python deps ----
COPY --chown=app:app pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --compile-bytecode

# ---- App source ----
COPY --chown=app:app api ./api
COPY --chown=app:app models ./models
COPY --chown=app:app data ./data
RUN mkdir -p docs

# ---- Frontend: Next.js standalone bundle ----
COPY --from=frontend-builder --chown=app:app /app/frontend/.next/standalone ./frontend
COPY --from=frontend-builder --chown=app:app /app/frontend/.next/static ./frontend/.next/static
COPY --from=frontend-builder --chown=app:app /app/frontend/public ./frontend/public

# ---- Entrypoint that runs both processes ----
COPY --chown=app:app docker/entrypoint.sh /home/app/entrypoint.sh
RUN chmod +x /home/app/entrypoint.sh

EXPOSE 7860
ENTRYPOINT ["/home/app/entrypoint.sh"]
