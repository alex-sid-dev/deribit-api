from dishka import Provider, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import PostgresConfig
from src.db.session import get_engine, get_sessionmaker, get_session


def db_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, scope=Scope.REQUEST, provides=AsyncSession)
    return provider


def configs_provider() -> Provider:
    provider = Provider()
    _ = provider.from_context(provides=PostgresConfig, scope=Scope.APP)

    return provider


def setup_providers() -> tuple[Provider, ...]:
    return (
        db_provider(),
        configs_provider(),
    )
