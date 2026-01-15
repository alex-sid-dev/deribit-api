from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from src.core.config import PostgresConfig


async def get_engine(cfg: PostgresConfig) -> AsyncEngine:
    return create_async_engine(cfg.uri, echo=True)


async def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_session(session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, Any]:
    async with session_factory() as session:
        yield session