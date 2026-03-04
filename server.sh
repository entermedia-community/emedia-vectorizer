#!/usr/bin/env sh
set -eu

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-9600}"
WORKERS="${WORKERS:-1}"

export CUDA_VISIBLE_DEVICES=0

exec uvicorn app:create_app \
	--factory \
	--interface wsgi \
	--host "$HOST" \
	--port "$PORT" \
	--workers "$WORKERS"