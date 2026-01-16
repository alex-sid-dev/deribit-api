from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import CurrencyPrice


class CurrencyPriceRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self, ticker: str, price: float, timestamp: int
    ) -> CurrencyPrice:
        """Создает новую запись о цене валюты."""
        price_record = CurrencyPrice(
            ticker=ticker.upper(),
            price=price,
            timestamp=timestamp,
        )
        self._session.add(price_record)
        await self._session.flush()
        await self._session.refresh(price_record)
        return price_record

    async def get_all_by_ticker(self, ticker: str) -> List[CurrencyPrice]:
        """Получает все записи по указанному тикеру."""
        stmt = select(CurrencyPrice).where(
            CurrencyPrice.ticker == ticker.upper()
        ).order_by(CurrencyPrice.timestamp.desc())
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_latest_by_ticker(self, ticker: str) -> Optional[CurrencyPrice]:
        """Получает последнюю цену по указанному тикеру."""
        stmt = (
            select(CurrencyPrice)
            .where(CurrencyPrice.ticker == ticker.upper())
            .order_by(desc(CurrencyPrice.timestamp))
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ticker_and_date(
        self, ticker: str, date: datetime
    ) -> Optional[CurrencyPrice]:
        """
        Получает цену по тикеру и дате.
        Ищет ближайшую запись к указанной дате.
        """
        target_timestamp = int(date.timestamp())
        ticker_upper = ticker.upper()

        stmt = (
            select(CurrencyPrice)
            .where(CurrencyPrice.ticker == ticker_upper)
            .order_by(
                func.abs(CurrencyPrice.timestamp - target_timestamp)
            )
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
