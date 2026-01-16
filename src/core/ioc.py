from dishka import Provider, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import PostgresConfig, RedisConfig
from src.db.repository import CurrencyPriceRepository
from src.db.session import get_engine, get_sessionmaker, get_session
from src.services.deribit_service import DeribitService


def db_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, scope=Scope.REQUEST, provides=AsyncSession)
    return provider


def configs_provider() -> Provider:
    provider = Provider()
    provider.from_context(provides=PostgresConfig, scope=Scope.APP)
    provider.from_context(provides=RedisConfig, scope=Scope.APP)
    return provider


def deribit_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.provide(DeribitService)
    return provider


def repository_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(CurrencyPriceRepository)
    return provider


def setup_providers() -> tuple[Provider, ...]:
    return (
        db_provider(),
        configs_provider(),
        deribit_provider(),
        repository_provider(),
    )
