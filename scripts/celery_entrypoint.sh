#!/bin/sh
set -e

echo "Waiting for Postgres..."
until uv run -m src.db.wait_db; do
  sleep 1
done

echo "Waiting for Redis..."
until uv run python - <<'EOF'
import os
import redis

host = os.getenv("REDIS_HOST", "redis")
port = int(os.getenv("REDIS_PORT", "6379"))

r = redis.Redis(host=host, port=port)
r.ping()
EOF
do
  sleep 1
done

exec "$@"