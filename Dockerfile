FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/uvx

WORKDIR /app

ENV PYTHONPATH=/app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
RUN uv pip install alembic

COPY migrations /app/migrations/
COPY scripts /app/scripts/
COPY src /app/src/
COPY alembic.ini /app/alembic.ini
RUN chmod +x /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/celery_entrypoint.sh

ENTRYPOINT ["/app/scripts/entrypoint.sh"]

CMD ["uv", "run", "uvicorn", "src.main:app", "--factory", "--host", "0.0.0.0", "--port", "5000"]