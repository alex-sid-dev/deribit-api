from celery import Celery
from dishka.integrations.celery import DishkaTask

from src.core.config import load_configs

configs = load_configs()

celery_app = Celery(
    "deribit_worker",
    task_cls=DishkaTask,
    broker=configs.redis.url,
    backend=configs.redis.url,
    include=["src.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "fetch-btc-price": {
            "task": "src.workers.tasks.fetch_btc_price",
            "schedule": 60.0,
        },
        "fetch-eth-price": {
            "task": "src.workers.tasks.fetch_eth_price",
            "schedule": 60.0,
        },
    },
)

# Импортируем задачи для их регистрации
from src.workers import tasks  # noqa: F401, E402
