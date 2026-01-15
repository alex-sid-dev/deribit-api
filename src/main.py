import asyncio

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.core.config import PostgresConfig, load_configs
from src.core.ioc import setup_providers

load_dotenv()
configs = load_configs()
context = {
    PostgresConfig: configs.db,
}

container = make_async_container(*setup_providers(), context=context)


def app():
    fastapi_app = FastAPI(
        default_response_class=ORJSONResponse,
        title="Deribit API",
    )
    setup_dishka(container, app=fastapi_app)

    return fastapi_app
