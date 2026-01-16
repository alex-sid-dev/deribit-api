import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from src.db.base import Base
from src.db.models import CurrencyPrice
from src.db.repository import CurrencyPriceRepository
from src.services.deribit_service import DeribitService


@pytest.fixture
async def db_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_maker() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def repository(db_session):
    return CurrencyPriceRepository(db_session)


@pytest.fixture
def mock_deribit_service():
    service = DeribitService()
    service._session = AsyncMock()
    service._own_session = False
    return service
