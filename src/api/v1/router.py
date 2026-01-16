from datetime import datetime

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas import (
    CurrencyPriceResponse,
    CurrencyPriceListResponse,
    ErrorResponse,
)
from src.db.repository import CurrencyPriceRepository


router = APIRouter(prefix="/api/v1", tags=["prices"], route_class=DishkaRoute)


@router.get(
    "/prices",
    response_model=CurrencyPriceListResponse,
    responses={400: {"model": ErrorResponse}},
)
async def get_all_prices(
    session: FromDishka[AsyncSession],
    ticker: str = Query(..., description="Тикер валюты (например, BTC_USD, ETH_USD)"),
) -> CurrencyPriceListResponse:
    """
    Получает все сохраненные данные по указанной валюте.
    """
    if not ticker:
        raise HTTPException(status_code=400, detail="Параметр ticker обязателен")

    repository = CurrencyPriceRepository(session)
    prices = await repository.get_all_by_ticker(ticker)

    return CurrencyPriceListResponse(
        ticker=ticker.upper(),
        prices=[CurrencyPriceResponse.model_validate(price) for price in prices],
    )


@router.get(
    "/prices/latest",
    response_model=CurrencyPriceResponse,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
)
async def get_latest_price(
    session: FromDishka[AsyncSession],
    ticker: str = Query(..., description="Тикер валюты (например, BTC_USD, ETH_USD)"),
) -> CurrencyPriceResponse:
    """
    Получает последнюю цену валюты.
    """
    if not ticker:
        raise HTTPException(status_code=400, detail="Параметр ticker обязателен")

    repository = CurrencyPriceRepository(session)
    price = await repository.get_latest_by_ticker(ticker)

    if price is None:
        raise HTTPException(
            status_code=404,
            detail=f"Цена для тикера {ticker.upper()} не найдена",
        )

    return CurrencyPriceResponse.model_validate(price)


@router.get(
    "/prices/by-date",
    response_model=CurrencyPriceResponse,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
)
async def get_price_by_date(
    session: FromDishka[AsyncSession],
    ticker: str = Query(..., description="Тикер валюты (например, BTC_USD, ETH_USD)"),
    date: str = Query(..., description="Дата в формате YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS"),
) -> CurrencyPriceResponse:
    """
    Получает цену валюты с фильтром по дате.
    Возвращает ближайшую запись к указанной дате.
    """
    if not ticker:
        raise HTTPException(status_code=400, detail="Параметр ticker обязателен")

    if not date:
        raise HTTPException(status_code=400, detail="Параметр date обязателен")

    try:
        if "T" in date:
            target_date = datetime.fromisoformat(date.replace("Z", "+00:00"))
        else:
            target_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Неверный формат даты: {date}. Используйте YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS",
        )

    repository = CurrencyPriceRepository(session)
    price = await repository.get_by_ticker_and_date(ticker, target_date)

    if price is None:
        raise HTTPException(
            status_code=404,
            detail=f"Цена для тикера {ticker.upper()} на дату {date} не найдена",
        )

    return CurrencyPriceResponse.model_validate(price)
