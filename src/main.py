from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1.router import router
from src.core.config import PostgresConfig, RedisConfig, load_configs
from src.core.ioc import setup_providers

load_dotenv()
configs = load_configs()
context = {
    PostgresConfig: configs.db,
    RedisConfig: configs.redis,
}

container = make_async_container(*setup_providers(), context=context)


def app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        yield
        await container.close()

    fastapi_app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        title="Deribit API",
        description="API для получения цен криптовалют с биржи Deribit",
        version="1.0.0",
    )

    fastapi_app.include_router(router)
    setup_dishka(container, app=fastapi_app)

    return fastapi_app
