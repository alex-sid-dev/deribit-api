#!/bin/bash
set -e

echo "Waiting for Postgres..."
until uv run -m src.db.wait_db; do
  sleep 1
done

echo "Waiting for Redis..."
until uv run python -c "import redis; r = redis.Redis(host='${REDIS_HOST:-redis}', port=${REDIS_PORT:-6379}); r.ping()" 2>/dev/null; do
  sleep 1
done

exec "$@"
