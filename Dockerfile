FROM python:3.12-slim-trixie

# Копируем бинарники uv и uvx из официального образа
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/uvx

WORKDIR /app

# Добавляем /app в PYTHONPATH
ENV PYTHONPATH=/app

# Копируем конфиги uv и устанавливаем зависимости
COPY ../pyproject.toml uv.lock ./
RUN uv sync --frozen
RUN uv pip install alembic

# Копируем код бота
COPY ../migrations ./migrations/
COPY ../scripts ./scripts/
COPY ../src ./src/
COPY ../alembic.ini /app/alembic.ini
RUN chmod +x /app/scripts/entrypoint.sh

ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# Самый простой и надежный синтаксис
CMD ["uv", "run", "uvicorn", "src.main:app", "--factory", "--host", "0.0.0.0", "--port", "5000"]


