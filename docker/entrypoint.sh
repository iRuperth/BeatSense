#!/usr/bin/env bash
# Boots FastAPI (8000) + Next.js standalone (7860) in one container.
# Forwards signals so the container stops cleanly under HF Spaces / docker stop.
set -euo pipefail

cd /home/app/code

PORT_API="${PORT_API:-8000}"
PORT_WEB="${PORT:-7860}"
HOST="${HOSTNAME:-0.0.0.0}"

echo "[boot] starting FastAPI on :${PORT_API} ..."
uv run uvicorn api.main:app --host 127.0.0.1 --port "${PORT_API}" --workers 1 &
PID_API=$!

# Wait for FastAPI to become ready (max ~30s)
for i in $(seq 1 30); do
  if curl -fsS "http://127.0.0.1:${PORT_API}/health" >/dev/null 2>&1; then
    echo "[boot] FastAPI is up."
    break
  fi
  sleep 1
done

echo "[boot] starting Next.js on :${PORT_WEB} ..."
cd /home/app/code/frontend
HOSTNAME="${HOST}" PORT="${PORT_WEB}" node server.js &
PID_WEB=$!

terminate() {
  echo "[boot] stopping ..."
  kill -TERM "${PID_API}" "${PID_WEB}" 2>/dev/null || true
  wait || true
  exit 0
}
trap terminate INT TERM

# Exit if either child dies
wait -n "${PID_API}" "${PID_WEB}"
EXIT_CODE=$?
echo "[boot] a child exited with code ${EXIT_CODE}, shutting down."
terminate
