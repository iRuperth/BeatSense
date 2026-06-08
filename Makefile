.PHONY: help install dev streamlit api frontend frontend-install frontend-build frontend-dev all-dev docker-up docker-down docker-build docker-logs jupyter test clean

# ---------------------------------------------------------------------------
# Quick reference
# ---------------------------------------------------------------------------

help:
	@echo "BeatSense — Make targets"
	@echo ""
	@echo "  make install           Sync Python deps with uv"
	@echo "  make frontend-install  Install Next.js deps with pnpm"
	@echo "  make dev               Run BOTH FastAPI (8000) + Next.js (3000)"
	@echo "  make api               Run FastAPI only (uvicorn :8000)"
	@echo "  make frontend          Run Next.js only (pnpm dev :3000)"
	@echo "  make frontend-build    Build Next.js production bundle"
	@echo "  make streamlit         Run the legacy Streamlit app"
	@echo "  make docker-up         docker-compose up -d"
	@echo "  make docker-down       docker-compose down"
	@echo "  make docker-build      docker-compose build --no-cache"
	@echo "  make docker-logs       docker-compose logs -f"
	@echo "  make jupyter           Launch JupyterLab"
	@echo "  make test              Run pytest"
	@echo "  make clean             Remove caches"

# ---------------------------------------------------------------------------
# Python (uv)
# ---------------------------------------------------------------------------

install:
	uv sync

api:
	uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

streamlit:
	uv run streamlit run app.py

# ---------------------------------------------------------------------------
# Frontend (pnpm + Next.js)
# ---------------------------------------------------------------------------

frontend-install:
	cd frontend && pnpm install

frontend:
	cd frontend && pnpm dev

frontend-dev: frontend

frontend-build:
	cd frontend && pnpm build

# ---------------------------------------------------------------------------
# Combined dev: API + frontend in parallel
# ---------------------------------------------------------------------------

dev:
	@echo "Starting FastAPI on :8000 and Next.js on :3000..."
	@trap 'kill 0' INT; \
	uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 & \
	(cd frontend && pnpm dev) & \
	wait

all-dev: dev

# ---------------------------------------------------------------------------
# Docker / misc
# ---------------------------------------------------------------------------

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose build --no-cache

docker-logs:
	docker-compose logs -f

jupyter:
	uv run jupyter lab

test:
	uv run pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/.next
