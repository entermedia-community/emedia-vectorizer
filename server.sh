#!/usr/bin/env sh
set -eu

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-9600}"
WORKERS="${WORKERS:-1}"

# Run Flask app through uvicorn using its WSGI interface and app factory.
exec uvicorn app:create_app \
	--factory \
	--interface wsgi \
	--host "$HOST" \
	--port "$PORT" \
	--workers "$WORKERS" \
  > /dev/null 2>&1 &