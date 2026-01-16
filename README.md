# Deribit API

Backend-приложение для получения и хранения цен криптовалют с биржи Deribit.

## Что делает

Приложение каждую минуту получает цены BTC_USD и ETH_USD с Deribit API и сохраняет их в PostgreSQL. Также есть REST API для получения сохраненных данных.

## Технологический стек

- **FastAPI** - веб-фреймворк для создания API
- **PostgreSQL** - реляционная база данных
- **SQLAlchemy** - ORM для работы с БД (async)
- **Celery** - асинхронная очередь задач
- **Redis** - брокер сообщений для Celery
- **aiohttp** - асинхронный HTTP клиент
- **Dishka** - dependency injection контейнер
- **Alembic** - миграции БД
- **orjson** - быстрая JSON сериализация
- **Docker** - контейнеризация приложения

## Что нужно для запуска

- Python 3.12+
- Docker и Docker Compose
- uv (установите с https://github.com/astral-sh/uv)

## Установка и запуск

### 1. Клонируем репозиторий

```bash
git clone <repository-url>
cd deribit-api
```

### 2. Настраиваем переменные окружения

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Или создайте `.env` вручную:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=deribit_db

REDIS_HOST=redis
REDIS_PORT=6379

SERVER_PORT=8000
```

### 3. Запускаем через Docker Compose

```bash
docker-compose up -d
```

Запустятся 5 сервисов:
- PostgreSQL (база данных)
- Redis (брокер для Celery)
- FastAPI приложение
- Celery worker (выполняет задачи)
- Celery beat (планировщик)

### 4. Проверяем что все работает

Приложение доступно на `http://localhost:8000`

Swagger документация: `http://localhost:8000/docs`

## API

Все методы GET, обязательный параметр `ticker` (например, `BTC_USD` или `ETH_USD`).

### Получить все цены по валюте

```
GET /api/v1/prices?ticker=BTC_USD
```

Вернет все сохраненные записи для указанного тикера.

**Пример ответа:**
```json
{
  "ticker": "BTC_USD",
  "prices": [
    {
      "id": 1,
      "ticker": "BTC_USD",
      "price": 50000.5,
      "timestamp": 1705401600,
      "created_at": "2026-01-16T12:00:00"
    }
  ]
}
```

### Получить последнюю цену

```
GET /api/v1/prices/latest?ticker=BTC_USD
```

Вернет самую свежую запись для тикера.

**Пример ответа:**
```json
{
  "id": 1,
  "ticker": "BTC_USD",
  "price": 50000.5,
  "timestamp": 1705401600,
  "created_at": "2026-01-16T12:00:00"
}
```

### Получить цену по дате

```
GET /api/v1/prices/by-date?ticker=BTC_USD&date=2026-01-16
```

Вернет ближайшую к указанной дате запись.

**Параметры:**
- `ticker` - тикер валюты (обязательно)
- `date` - дата в формате `YYYY-MM-DD` или `YYYY-MM-DDTHH:MM:SS` (обязательно)

**Пример ответа:**
```json
{
  "id": 1,
  "ticker": "BTC_USD",
  "price": 50000.5,
  "timestamp": 1705401600,
  "created_at": "2026-01-16T12:00:00"
}
```

## Тесты

```bash
uv sync --extra test
uv run pytest
```

Покрытие базовое - репозиторий, сервис, API endpoints.

## Структура проекта

```
deribit-api/
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── router.py      # API endpoints
│   │       └── schemas.py     # Pydantic схемы
│   ├── core/
│   │   ├── config.py          # Конфигурация
│   │   ├── ioc.py             # Dependency Injection
│   │   └── logging.py         # Логирование
│   ├── db/
│   │   ├── base.py            # Базовый класс моделей
│   │   ├── models.py          # Модели БД
│   │   ├── repository.py      # Репозиторий для работы с БД
│   │   ├── session.py         # Настройка сессий БД
│   │   └── wait_db.py         # Ожидание готовности БД
│   ├── services/
│   │   └── deribit_service.py # Сервис для работы с Deribit API
│   ├── workers/
│   │   ├── celery_app.py      # Конфигурация Celery
│   │   └── tasks.py           # Celery задачи
│   └── main.py                # Точка входа приложения
├── migrations/                # Миграции Alembic
├── scripts/                   # Скрипты для запуска
├── tests/                     # Unit тесты
├── .env.example               # Пример файла с переменными окружения
├── docker-compose.yaml        # Конфигурация Docker Compose
├── Dockerfile                 # Docker образ
├── pyproject.toml             # Зависимости проекта
└── README.md                  # Документация
```

## Design Decisions

### Архитектура

**Dependency Injection (Dishka)**
Использовал Dishka для DI - удобно для тестов и замены реализаций. В FastAPI работает через `DishkaRoute` и `FromDishka`.

**Repository Pattern**
Вынес работу с БД в отдельный слой `CurrencyPriceRepository`. Так проще тестировать и менять реализацию при необходимости.

**Сервисный слой**
`DeribitService` обернул работу с Deribit API. Использует aiohttp, сессию создает сам при необходимости.

### База данных

**Единая таблица `currency_prices`**
Вместо отдельных таблиц для каждой валюты - одна таблица с полем `ticker`. Проще добавлять новые валюты, индексы работают эффективнее.

**Индексы**
- На `ticker` - для фильтрации по валюте
- На `timestamp` - для сортировки
- Составной `(ticker, timestamp)` - для запросов с обоими условиями

**UNIX timestamp**
Храню время как int (timestamp) - проще работать, меньше места занимает.

### Асинхронная обработка

**Celery + Redis**
Celery Beat запускает задачи каждую минуту, Redis как брокер. В задачах использую `asyncio.run()` для выполнения async кода, так как Celery задачи синхронные.

**Проблема с event loop**
Изначально пытался использовать dishka контейнер в Celery задачах, но возникали конфликты event loop. Решение - каждая задача создает свой engine и session напрямую. Менее элегантно, зато работает стабильно.

**Async везде**
БД через SQLAlchemy async, HTTP через aiohttp, FastAPI обрабатывает запросы асинхронно.

### Docker

Отдельные контейнеры для каждого сервиса, health checks чтобы дождаться готовности БД перед запуском приложения. Миграции применяются автоматически при старте через `entrypoint.sh`.

Использую `uv` для установки зависимостей - быстрее чем pip. Образ на базе `python:3.12-slim` для экономии места.

### Тесты

Есть базовые unit тесты:
- Репозиторий тестируется на in-memory SQLite
- Сервис с моками aiohttp
- API endpoints

Фикстуры в `conftest.py`, pytest для запуска.

### Безопасность и валидация

Pydantic схемы для валидации запросов/ответов. Обязательные параметры проверяются на уровне FastAPI. Ошибки обрабатываются с понятными сообщениями.

## Разработка

### Миграции

Создать новую:
```bash
uv run alembic revision --autogenerate -m "описание"
```

Применить:
```bash
uv run alembic upgrade head
```

### Локальный запуск (без Docker)

Если хочешь запустить локально:

1. Установи зависимости: `uv sync`
2. Подними PostgreSQL и Redis (через Docker или локально)
3. Создай `.env` с настройками для локальной БД (host=localhost вместо db)
4. Примени миграции: `uv run alembic upgrade head`
5. Запусти FastAPI: `uv run uvicorn src.main:app --factory --reload`
6. В другом терминале - Celery worker: `uv run celery -A src.workers.celery_app worker --loglevel=info`
7. В третьем терминале - Celery beat: `uv run celery -A src.workers.celery_app beat --loglevel=info`

### Тестовое задание по которому делался проект
```
Тестовое задание на позицию junior backend разработчика
Задание:
1. Написать клиент для криптобиржи Deribit (https://docs.deribit.com/). Клиент должен каждую минуту забирать с биржи текущую цену btc_usd и eth_usd (index price валюты) после чего сохранять в базу данных тикер валюты, текущую цену и время в UNIX timestamp.
2. Написать внешнее API для обработки сохраненных данных на FastAPI.
Обязательные требования:
1. API должно включать в себя следующие методы:
- Получение всех сохраненных данных по указанной валюте
- Получение последней цены валюты
- Получение цены валюты с фильтром по дате
Все методы должны быть GET и у каждого метода должен быть обязательный query-параметр “ticker”.
2. В качестве БД использовать PostgreSQL.
3. Код выложить на gitlab с подробным readme и документацией по разворачиванию. В readme добавить секцию Design decisions.
4. Для периодического получения цен использовать Celery.
Необязательные требования:
1. Написать unit тесты для основных методов
2. Развернуть приложение в двух контейнерах для приложения и базы данных. 
3. Применить aiohttp при написании клиента.
Критерии оценки:
1. Чистая архитектура/чистый код
2. Нейминг
3. Отсутсвие глобальных переменных
4. Умение использовать ООП
5. Понимание принятых решений и способность их объяснить
```
## Лицензия

MIT
