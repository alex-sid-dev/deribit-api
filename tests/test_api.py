import pytest
from datetime import datetime
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from src.main import app
from src.db.models import CurrencyPrice


@pytest.fixture
def client():
    return TestClient(app())


@pytest.mark.asyncio
async def test_get_all_prices_empty(client):
    response = client.get("/api/v1/prices?ticker=BTC_USD")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_get_all_prices_missing_ticker(client):
    response = client.get("/api/v1/prices")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_latest_price_missing_ticker(client):
    response = client.get("/api/v1/prices/latest")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_price_by_date_missing_params(client):
    response = client.get("/api/v1/prices/by-date")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_price_by_date_invalid_format(client):
    response = client.get("/api/v1/prices/by-date?ticker=BTC_USD&date=invalid")
    assert response.status_code == 400
