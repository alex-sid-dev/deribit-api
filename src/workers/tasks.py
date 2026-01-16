import asyncio
import time
from dishka.integrations.celery import setup_dishka
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import PostgresConfig, RedisConfig, load_configs
from src.db.repository import CurrencyPriceRepository
from src.services.deribit_service import DeribitService
from src.workers.celery_app import celery_app

configs = load_configs()


def _get_engine():
    """Создает новый engine для каждой задачи."""
    return create_async_engine(
        configs.db.uri,
        echo=False,
        pool_pre_ping=True,
    )


@celery_app.task
def fetch_btc_price() -> None:
    """Задача для получения и сохранения цены BTC_USD."""
    asyncio.run(_fetch_and_save_price("BTC_USD"))


@celery_app.task
def fetch_eth_price() -> None:
    """Задача для получения и сохранения цены ETH_USD."""
    asyncio.run(_fetch_and_save_price("ETH_USD"))


async def _fetch_and_save_price(ticker: str) -> None:
    """Вспомогательная функция для получения и сохранения цены."""
    engine = _get_engine()
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    
    deribit_service = DeribitService()
    
    try:
        async with session_factory() as session:
            repository = CurrencyPriceRepository(session)
            
            try:
                price = await deribit_service.get_index_price(ticker.lower())
                timestamp = int(time.time())
                
                await repository.create(ticker, price, timestamp)
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    finally:
        await deribit_service.close()
        await engine.dispose()
