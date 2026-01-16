import pytest
from datetime import datetime

from src.db.models import CurrencyPrice
from src.db.repository import CurrencyPriceRepository


@pytest.mark.asyncio
async def test_create_price_record(repository: CurrencyPriceRepository):
    ticker = "BTC_USD"
    price = 50000.0
    timestamp = int(datetime.now().timestamp())

    result = await repository.create(ticker, price, timestamp)

    assert result.ticker == ticker.upper()
    assert result.price == price
    assert result.timestamp == timestamp
    assert result.id is not None


@pytest.mark.asyncio
async def test_get_all_by_ticker(repository: CurrencyPriceRepository):
    ticker = "ETH_USD"
    prices = [3000.0, 3100.0, 3200.0]
    timestamps = [int(datetime.now().timestamp()) + i for i in range(3)]

    for price, ts in zip(prices, timestamps):
        await repository.create(ticker, price, ts)
    await repository._session.commit()

    results = await repository.get_all_by_ticker(ticker)

    assert len(results) == 3
    assert all(r.ticker == ticker.upper() for r in results)
    assert results[0].timestamp >= results[1].timestamp


@pytest.mark.asyncio
async def test_get_latest_by_ticker(repository: CurrencyPriceRepository):
    ticker = "BTC_USD"
    timestamps = [int(datetime.now().timestamp()) + i for i in range(3)]

    for i, ts in enumerate(timestamps):
        await repository.create(ticker, 50000.0 + i * 100, ts)
    await repository._session.commit()

    latest = await repository.get_latest_by_ticker(ticker)

    assert latest is not None
    assert latest.timestamp == max(timestamps)


@pytest.mark.asyncio
async def test_get_latest_by_ticker_not_found(repository: CurrencyPriceRepository):
    result = await repository.get_latest_by_ticker("UNKNOWN")
    assert result is None


@pytest.mark.asyncio
async def test_get_by_ticker_and_date(repository: CurrencyPriceRepository):
    ticker = "BTC_USD"
    target_date = datetime(2026, 1, 16, 12, 0, 0)
    target_timestamp = int(target_date.timestamp())

    await repository.create(ticker, 50000.0, target_timestamp - 100)
    await repository.create(ticker, 51000.0, target_timestamp)
    await repository.create(ticker, 52000.0, target_timestamp + 200)
    await repository._session.commit()

    result = await repository.get_by_ticker_and_date(ticker, target_date)

    assert result is not None
    assert result.timestamp == target_timestamp
    assert result.price == 51000.0
