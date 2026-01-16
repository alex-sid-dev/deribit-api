import pytest
from unittest.mock import AsyncMock, MagicMock

from src.services.deribit_service import DeribitService


@pytest.mark.asyncio
async def test_get_index_price_success():
    service = DeribitService()
    mock_session = AsyncMock()
    service._session = mock_session
    service._own_session = False

    mock_response = AsyncMock()
    mock_response.json = AsyncMock(
        return_value={"result": {"index_price": 50000.5}}
    )
    mock_response.raise_for_status = MagicMock()
    
    mock_context_manager = MagicMock()
    mock_context_manager.__aenter__ = AsyncMock(return_value=mock_response)
    mock_context_manager.__aexit__ = AsyncMock(return_value=None)
    
    mock_session.get = MagicMock(return_value=mock_context_manager)

    price = await service.get_index_price("btc_usd")

    assert price == 50000.5
    mock_session.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_index_price_invalid_response():
    service = DeribitService()
    mock_session = AsyncMock()
    service._session = mock_session
    service._own_session = False

    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={"result": {}})
    mock_response.raise_for_status = MagicMock()
    
    mock_context_manager = MagicMock()
    mock_context_manager.__aenter__ = AsyncMock(return_value=mock_response)
    mock_context_manager.__aexit__ = AsyncMock(return_value=None)
    
    mock_session.get = MagicMock(return_value=mock_context_manager)

    with pytest.raises(ValueError, match="Invalid response format"):
        await service.get_index_price("btc_usd")


@pytest.mark.asyncio
async def test_close_session():
    service = DeribitService()
    service._session = AsyncMock()
    service._own_session = True

    await service.close()

    service._session.close.assert_called_once()
    assert service._session is None
    assert service._own_session is False
