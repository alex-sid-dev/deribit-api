#!/bin/sh
set -e

echo "Waiting for Postgres..."
until uv run -m src.db.wait_db; do
  sleep 1
done

echo "Running Alembic migrations..."
uv run alembic -c /app/alembic.ini upgrade head

exec uv run uvicorn src.main:app --factory --host 0.0.0.0 --port 5000