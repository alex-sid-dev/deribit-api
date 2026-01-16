from datetime import datetime, timezone

from sqlalchemy import String, BigInteger, Float, Index, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

__all__ = ["CurrencyPrice"]


class CurrencyPrice(Base):
    __tablename__ = "currency_prices"

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    __table_args__ = (
        Index("idx_ticker_timestamp", "ticker", "timestamp"),
    )
