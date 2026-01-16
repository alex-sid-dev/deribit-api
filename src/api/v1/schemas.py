from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class CurrencyPriceResponse(BaseModel):
    id: int
    ticker: str
    price: float
    timestamp: int
    created_at: datetime

    class Config:
        from_attributes = True


class CurrencyPriceListResponse(BaseModel):
    ticker: str
    prices: List[CurrencyPriceResponse] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    detail: str
